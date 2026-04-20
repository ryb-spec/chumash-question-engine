"""Readiness metrics for staged parsed corpus bundles."""

import json

from assessment_scope import (
    ACTIVE_ASSESSMENT_SCOPE,
    normalize_corpus_status,
    resolve_repo_path,
)
from pasuk_flow_generator import (
    SKILLS,
    generate_pasuk_flow,
    generate_question,
    is_placeholder_translation,
    is_skip_payload,
    usable_translation,
)
from torah_parser.word_bank_adapter import adapt_word_analysis


READINESS_THRESHOLDS = {
    "analysis_coverage_review_needed_min": 0.90,
    "analysis_coverage_active_candidate_min": 0.98,
    "question_support_review_needed_min": 0.50,
    "question_support_active_candidate_min": 0.80,
    "flow_support_review_needed_min": 0.50,
    "flow_support_active_candidate_min": 0.80,
}

NON_RUNTIME_SKILLS = {
    "identify_prefix_future",
    "identify_suffix_past",
    "identify_present_pattern",
    "convert_future_to_command",
    "match_pronoun_to_verb",
}

EVALUATED_SKILLS = tuple(skill for skill in SKILLS if skill not in NON_RUNTIME_SKILLS)
APPROVED_REVIEW_STATUSES = {"approved", "starter_approved"}


def load_bundle_json(path):
    file_path = resolve_repo_path(path)
    return json.loads(file_path.read_text(encoding="utf-8"))


def load_staged_corpus_bundle(bundle_or_dir):
    if isinstance(bundle_or_dir, dict):
        return bundle_or_dir

    base = resolve_repo_path(bundle_or_dir)
    if base.is_file():
        return load_bundle_json(base)

    return {
        "pesukim": load_bundle_json(base / "pesukim.json"),
        "parsed_pesukim": load_bundle_json(base / "parsed_pesukim.json"),
        "word_bank": load_bundle_json(base / "word_bank.json"),
        "word_occurrences": load_bundle_json(base / "word_occurrences.json"),
        "translation_reviews": load_bundle_json(base / "translation_reviews.json"),
    }


def parsed_token_record_to_item(token_record):
    analysis = dict(token_record.get("selected_analysis") or {})
    token = token_record.get("surface", "")
    analysis.setdefault("normalized", token_record.get("normalized") or analysis.get("normalized"))
    analysis.setdefault("translation_literal", analysis.get("translation") or token)
    analysis.setdefault(
        "translation_context",
        analysis.get("context_translation") or analysis.get("translation") or token,
    )
    entry = adapt_word_analysis(
        token,
        analysis,
        defaults={
            "group": "unknown",
            "semantic_group": "unknown",
            "role_hint": "unknown",
            "entity_type": "unknown",
            "base_word": analysis.get("lemma") or token,
        },
    )
    return {
        "token": token,
        "entry": entry,
        "base": analysis.get("lemma") or token,
    }


def parsed_pasuk_to_analyzed(parsed_pasuk_record):
    return [
        parsed_token_record_to_item(token_record)
        for token_record in parsed_pasuk_record.get("token_records", [])
    ]


def review_summary(bundle):
    reviews = bundle.get("translation_reviews", {}).get("reviews", [])
    unresolved = [
        review for review in reviews
        if review.get("review_status") not in APPROVED_REVIEW_STATUSES
    ]
    return {
        "review_records_count": len(reviews),
        "unresolved_review_records_count": len(unresolved),
    }


def structural_summary(bundle):
    parsed_pesukim = bundle.get("parsed_pesukim", {}).get("parsed_pesukim", [])
    token_records = [
        token_record
        for pasuk in parsed_pesukim
        for token_record in pasuk.get("token_records", [])
    ]
    selected_count = sum(1 for item in token_records if item.get("selected_analysis"))
    placeholder_translation_count = sum(
        1
        for item in token_records
        if is_placeholder_translation(
            ((item.get("selected_analysis") or {}).get("translation_context")),
            item.get("surface"),
        )
    )
    return {
        "pesukim_count": len(parsed_pesukim),
        "token_count": len(token_records),
        "selected_analysis_count": selected_count,
        "selected_analysis_pct": round(selected_count / len(token_records), 4) if token_records else 0.0,
        "tokens_with_placeholder_context_count": placeholder_translation_count,
    }


def skill_support_summary(parsed_pesukim):
    per_skill = {}
    total = len(parsed_pesukim)
    for skill in EVALUATED_SKILLS:
        supported = 0
        for parsed_pasuk in parsed_pesukim:
            analyzed = parsed_pasuk_to_analyzed(parsed_pasuk)
            pasuk_text = parsed_pasuk.get("text", "")
            try:
                question = generate_question(
                    skill,
                    pasuk_text,
                    analyzed_override=analyzed,
                )
            except (ValueError, IndexError):
                question = None
            if question and not is_skip_payload(question):
                supported += 1
        per_skill[skill] = {
            "supported_pesukim": supported,
            "support_rate": round(supported / total, 4) if total else 0.0,
        }
    return per_skill


def generation_summary(bundle):
    parsed_pesukim = bundle.get("parsed_pesukim", {}).get("parsed_pesukim", [])
    question_ready = 0
    flow_ready = 0
    for parsed_pasuk in parsed_pesukim:
        analyzed = parsed_pasuk_to_analyzed(parsed_pasuk)
        pasuk_text = parsed_pasuk.get("text", "")

        has_question = False
        for skill in EVALUATED_SKILLS:
            try:
                question = generate_question(skill, pasuk_text, analyzed_override=analyzed)
            except (ValueError, IndexError):
                continue
            if question and not is_skip_payload(question):
                has_question = True
                break
        if has_question:
            question_ready += 1

        try:
            flow = generate_pasuk_flow(pasuk_text, analyzed_override=analyzed)
        except (ValueError, IndexError):
            flow = None
        if flow and len(flow.get("questions", [])) >= 3:
            flow_ready += 1

    total = len(parsed_pesukim)
    return {
        "question_ready_pesukim": question_ready,
        "question_ready_pct": round(question_ready / total, 4) if total else 0.0,
        "stable_flow_pesukim": flow_ready,
        "stable_flow_pct": round(flow_ready / total, 4) if total else 0.0,
    }


def readiness_recommendation(metrics):
    structural = metrics["structural_summary"]
    generation = metrics["generation_summary"]
    review = metrics["review_summary"]

    if (
        structural["selected_analysis_pct"] >= READINESS_THRESHOLDS["analysis_coverage_active_candidate_min"]
        and generation["question_ready_pct"] >= READINESS_THRESHOLDS["question_support_active_candidate_min"]
        and generation["stable_flow_pct"] >= READINESS_THRESHOLDS["flow_support_active_candidate_min"]
        and review["unresolved_review_records_count"] == 0
        and structural["tokens_with_placeholder_context_count"] == 0
    ):
        return "active_candidate"

    if (
        structural["selected_analysis_pct"] >= READINESS_THRESHOLDS["analysis_coverage_review_needed_min"]
        and generation["question_ready_pct"] >= READINESS_THRESHOLDS["question_support_review_needed_min"]
        and generation["stable_flow_pct"] >= READINESS_THRESHOLDS["flow_support_review_needed_min"]
    ):
        return "review_needed"

    return "not_ready"


def evaluate_staged_corpus_readiness(bundle_or_dir):
    bundle = load_staged_corpus_bundle(bundle_or_dir)
    parsed_pesukim = bundle.get("parsed_pesukim", {}).get("parsed_pesukim", [])
    bundle_status = normalize_corpus_status(
        bundle.get("metadata", {}).get("status")
        or bundle.get("parsed_pesukim", {}).get("metadata", {}).get("status")
    ) or "staged"
    metrics = {
        "scope_under_evaluation": {
            "active_runtime_scope_unchanged": ACTIVE_ASSESSMENT_SCOPE,
            "bundle_status": bundle_status,
            "sefer": bundle.get("parsed_pesukim", {}).get("metadata", {}).get("sefer"),
            "range": bundle.get("parsed_pesukim", {}).get("metadata", {}).get("range"),
        },
        "structural_summary": structural_summary(bundle),
        "generation_summary": generation_summary(bundle),
        "per_skill_support": skill_support_summary(parsed_pesukim),
        "review_summary": review_summary(bundle),
        "thresholds": dict(READINESS_THRESHOLDS),
        "excluded_skills": sorted(NON_RUNTIME_SKILLS),
    }
    metrics["readiness_recommendation"] = readiness_recommendation(metrics)
    metrics["lifecycle"] = {
        "bundle_state": bundle_status,
        "promotion_gate": "only active_candidate bundles may be promoted into the active runtime",
        "next_recommended_state": metrics["readiness_recommendation"],
    }
    return metrics
