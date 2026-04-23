"""Readiness metrics for staged parsed corpus bundles."""

import json
from collections import Counter

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
from torah_parser.word_bank_adapter import (
    NORMALIZED_ALIAS_KEY,
    adapt_word_analysis,
    adapt_word_bank_data,
    build_word_bank_lookup,
)


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


def staged_reviewed_support_summary(bundle_or_dir):
    if isinstance(bundle_or_dir, dict):
        payload = bundle_or_dir.get("reviewed_questions") or {}
    else:
        base = resolve_repo_path(bundle_or_dir)
        reviewed_path = base / "reviewed_questions.json"
        if not reviewed_path.exists():
            return {
                "available": False,
                "question_count": 0,
                "lane_counts": {},
                "skill_counts": {},
            }
        payload = load_bundle_json(reviewed_path)
    metadata = payload.get("metadata", {}) if isinstance(payload, dict) else {}
    questions = payload.get("questions", []) if isinstance(payload, dict) else []
    lane_supported_pesukim = Counter()
    skill_supported_pesukim = Counter()
    for question in questions:
        lane = str(question.get("review_family") or "").strip()
        skill = str(question.get("skill") or "").strip()
        pasuk_id = str(question.get("pasuk_id") or "")
        if not pasuk_id:
            continue
        if lane:
            lane_supported_pesukim[(lane, pasuk_id)] += 1
        if skill:
            skill_supported_pesukim[(skill, pasuk_id)] += 1
    return {
        "available": bool(questions),
        "question_count": len(questions),
        "lane_counts": dict(metadata.get("lane_counts") or {}),
        "skill_counts": dict(metadata.get("skill_counts") or {}),
        "lane_supported_pesukim": dict(
            Counter(lane for lane, _pasuk_id in lane_supported_pesukim.keys())
        ),
        "skill_supported_pesukim": dict(
            Counter(skill for skill, _pasuk_id in skill_supported_pesukim.keys())
        ),
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


def bundle_word_bank_lookup(bundle):
    entries = adapt_word_bank_data(
        bundle.get("word_bank"),
        defaults={
            "group": "unknown",
            "semantic_group": "unknown",
            "role_hint": "unknown",
            "entity_type": "unknown",
        },
    )
    by_word = build_word_bank_lookup(entries)
    by_group = {}
    seen_entries = set()
    for entry in by_word.values():
        if entry.get(NORMALIZED_ALIAS_KEY):
            continue
        marker = id(entry)
        if marker in seen_entries:
            continue
        seen_entries.add(marker)
        by_group.setdefault(entry.get("group", "unknown"), []).append(entry)
    return by_word, by_group


def skill_support_summary(parsed_pesukim, word_bank_lookup=None, by_group=None):
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
                    word_bank_override=word_bank_lookup,
                    by_group_override=by_group,
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
    word_bank_lookup, by_group = bundle_word_bank_lookup(bundle)
    question_ready = 0
    flow_ready = 0
    for parsed_pasuk in parsed_pesukim:
        analyzed = parsed_pasuk_to_analyzed(parsed_pasuk)
        pasuk_text = parsed_pasuk.get("text", "")

        has_question = False
        for skill in EVALUATED_SKILLS:
            try:
                question = generate_question(
                    skill,
                    pasuk_text,
                    analyzed_override=analyzed,
                    word_bank_override=word_bank_lookup,
                    by_group_override=by_group,
                )
            except (ValueError, IndexError):
                continue
            if question and not is_skip_payload(question):
                has_question = True
                break
        if has_question:
            question_ready += 1

        try:
            flow = generate_pasuk_flow(
                pasuk_text,
                analyzed_override=analyzed,
                word_bank_override=word_bank_lookup,
                by_group_override=by_group,
            )
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


def staged_phrase_support_pesukim(staged_support):
    return max(
        int((staged_support.get("skill_supported_pesukim") or {}).get("phrase_translation", 0) or 0),
        int((staged_support.get("lane_supported_pesukim") or {}).get("translation", 0) or 0)
        if (staged_support.get("skill_counts") or {}).get("phrase_translation")
        else 0,
    )


def staged_role_support_pesukim(staged_support):
    return max(
        int((staged_support.get("lane_supported_pesukim") or {}).get("role", 0) or 0),
        int((staged_support.get("skill_supported_pesukim") or {}).get("subject_identification", 0) or 0),
        int((staged_support.get("skill_supported_pesukim") or {}).get("object_identification", 0) or 0),
    )


def diagnostic_summary(metrics):
    structural = metrics["structural_summary"]
    generation = metrics["generation_summary"]
    per_skill = metrics["per_skill_support"]
    review = metrics["review_summary"]
    staged_support = metrics["staged_reviewed_support"]
    thresholds = metrics["thresholds"]
    pesukim_count = structural.get("pesukim_count", 0) or 0
    flow_review_needed_min = int(
        round(thresholds["flow_support_review_needed_min"] * pesukim_count)
    ) if pesukim_count else 0
    question_review_needed_min = int(
        round(thresholds["question_support_review_needed_min"] * pesukim_count)
    ) if pesukim_count else 0
    phrase_support = max(
        per_skill.get("phrase_translation", {}).get("supported_pesukim", 0),
        staged_phrase_support_pesukim(staged_support),
    )
    subject_support = max(
        per_skill.get("subject_identification", {}).get("supported_pesukim", 0),
        int((staged_support.get("skill_supported_pesukim") or {}).get("subject_identification", 0) or 0),
    )
    object_support = max(
        per_skill.get("object_identification", {}).get("supported_pesukim", 0),
        int((staged_support.get("skill_supported_pesukim") or {}).get("object_identification", 0) or 0),
    )
    role_support = max(
        staged_role_support_pesukim(staged_support),
        subject_support,
        object_support,
    )
    blocker_categories = []

    if structural["tokens_with_placeholder_context_count"] > 0:
        blocker_categories.append(
            {
                "code": "placeholder_context",
                "count": structural["tokens_with_placeholder_context_count"],
                "message": "Selected analyses still rely on placeholder context translations.",
            }
        )
    if generation["stable_flow_pesukim"] < flow_review_needed_min:
        blocker_categories.append(
            {
                "code": "stable_flow_shortfall",
                "actual": generation["stable_flow_pesukim"],
                "review_needed_min": flow_review_needed_min,
                "message": "Too few pesukim currently support three-question Pasuk Flow cleanly.",
            }
        )
    if generation["question_ready_pesukim"] < question_review_needed_min:
        blocker_categories.append(
            {
                "code": "question_support_shortfall",
                "actual": generation["question_ready_pesukim"],
                "review_needed_min": question_review_needed_min,
                "message": "Too few pesukim currently support even one quiz-ready foundational question.",
            }
        )
    if per_skill.get("translation", {}).get("supported_pesukim", 0) < flow_review_needed_min:
        blocker_categories.append(
            {
                "code": "translation_support_thin",
                "actual": per_skill.get("translation", {}).get("supported_pesukim", 0),
                "review_needed_min": flow_review_needed_min,
                "message": "Standalone translation support is still too thin across the staged chunk.",
            }
        )
    if per_skill.get("shoresh", {}).get("supported_pesukim", 0) < flow_review_needed_min:
        blocker_categories.append(
            {
                "code": "shoresh_support_thin",
                "actual": per_skill.get("shoresh", {}).get("supported_pesukim", 0),
                "review_needed_min": flow_review_needed_min,
                "message": "Shoresh support is still too thin across the staged chunk.",
            }
        )
    if staged_support.get("available") and (
        staged_support.get("lane_supported_pesukim", {}).get("translation", 0) < question_review_needed_min
    ):
        blocker_categories.append(
            {
                "code": "reviewed_translation_support_thin",
                "actual": staged_support.get("lane_supported_pesukim", {}).get("translation", 0),
                "review_needed_min": question_review_needed_min,
                "message": "Curated staged reviewed translation support is still too thin across the chunk.",
            }
        )
    if phrase_support == 0:
        blocker_categories.append(
            {
                "code": "phrase_translation_support_absent",
                "actual": 0,
                "active_candidate_min": 1,
                "message": "No quiz-ready phrase-translation support is available for this staged chunk yet.",
            }
        )
    elif phrase_support < question_review_needed_min:
        blocker_categories.append(
            {
                "code": "phrase_translation_support_thin",
                "actual": phrase_support,
                "review_needed_min": question_review_needed_min,
                "message": "Phrase-translation support exists but is still too thin across the staged chunk.",
            }
        )
    if role_support == 0:
        blocker_categories.append(
            {
                "code": "role_context_support_absent",
                "subject_supported_pesukim": subject_support,
                "object_supported_pesukim": object_support,
                "active_candidate_min": 1,
                "message": "No quiz-ready subject/object support is available for this staged chunk yet.",
            }
        )
    elif role_support < question_review_needed_min:
        blocker_categories.append(
            {
                "code": "role_context_support_thin",
                "subject_supported_pesukim": subject_support,
                "object_supported_pesukim": object_support,
                "review_needed_min": question_review_needed_min,
                "message": "Subject/object support exists but is still too thin across the staged chunk.",
            }
        )
    if review.get("unresolved_review_records_count", 0) > 0:
        blocker_categories.append(
            {
                "code": "translation_reviews_unresolved",
                "count": review.get("unresolved_review_records_count", 0),
                "message": "Human translation review still has unresolved staged records.",
            }
        )

    return {
        "blocker_categories": blocker_categories,
        "flow_review_needed_min_pesukim": flow_review_needed_min,
        "question_review_needed_min_pesukim": question_review_needed_min,
    }


def readiness_recommendation(metrics):
    structural = metrics["structural_summary"]
    generation = metrics["generation_summary"]
    per_skill = metrics["per_skill_support"]
    review = metrics["review_summary"]
    staged_support = metrics["staged_reviewed_support"]
    pesukim_count = structural.get("pesukim_count", 0) or 0
    question_review_needed_min = int(
        round(READINESS_THRESHOLDS["question_support_review_needed_min"] * pesukim_count)
    ) if pesukim_count else 0
    phrase_support = max(
        per_skill.get("phrase_translation", {}).get("supported_pesukim", 0),
        staged_phrase_support_pesukim(staged_support),
    )
    role_support = max(
        staged_role_support_pesukim(staged_support),
        per_skill.get("subject_identification", {}).get("supported_pesukim", 0),
        per_skill.get("object_identification", {}).get("supported_pesukim", 0),
    )

    if (
        structural["selected_analysis_pct"] >= READINESS_THRESHOLDS["analysis_coverage_active_candidate_min"]
        and generation["question_ready_pct"] >= READINESS_THRESHOLDS["question_support_active_candidate_min"]
        and generation["stable_flow_pct"] >= READINESS_THRESHOLDS["flow_support_active_candidate_min"]
        and review["unresolved_review_records_count"] == 0
        and structural["tokens_with_placeholder_context_count"] == 0
        and phrase_support >= question_review_needed_min
        and role_support >= question_review_needed_min
        and (
            not staged_support.get("available")
            or staged_support.get("lane_supported_pesukim", {}).get("translation", 0) >= question_review_needed_min
        )
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
    word_bank_lookup, by_group = bundle_word_bank_lookup(bundle)
    metrics = {
        "scope_under_evaluation": {
            "active_runtime_scope_unchanged": ACTIVE_ASSESSMENT_SCOPE,
            "bundle_status": bundle_status,
            "sefer": bundle.get("parsed_pesukim", {}).get("metadata", {}).get("sefer"),
            "range": bundle.get("parsed_pesukim", {}).get("metadata", {}).get("range"),
        },
        "structural_summary": structural_summary(bundle),
        "generation_summary": generation_summary(bundle),
        "per_skill_support": skill_support_summary(parsed_pesukim, word_bank_lookup, by_group),
        "review_summary": review_summary(bundle),
        "staged_reviewed_support": staged_reviewed_support_summary(bundle_or_dir),
        "thresholds": dict(READINESS_THRESHOLDS),
        "excluded_skills": sorted(NON_RUNTIME_SKILLS),
    }
    metrics["readiness_recommendation"] = readiness_recommendation(metrics)
    metrics["diagnostic_summary"] = diagnostic_summary(metrics)
    metrics["lifecycle"] = {
        "bundle_state": bundle_status,
        "promotion_gate": "only active_candidate bundles may be promoted into the active runtime",
        "next_recommended_state": metrics["readiness_recommendation"],
    }
    return metrics
