"""Exposure scoring and small-scope fallback policy for runtime selection."""

from __future__ import annotations

import os
from collections import Counter

from runtime.question_identity import build_question_signatures, normalize_text


EXACT_RECENT_REPEAT_PENALTY = 100.0
TARGET_RECENT_REPEAT_PENALTY = 40.0
PASUK_SKILL_REPEAT_PENALTY = 18.0
SKILL_TYPE_REPEAT_PENALTY = 6.0
FALLBACK_MIN_CANDIDATE_COUNT = 1


def history_weighting_enabled(env=None):
    value = (env or os.environ).get("CHUMASH_DISABLE_HISTORY_WEIGHTING", "")
    return str(value).strip().lower() not in {"1", "true", "yes", "on"}


def build_exposure_index(attempt_records):
    exact = Counter()
    target = Counter()
    pasuk_skill = Counter()
    skill_type = Counter()
    records = []
    for record in attempt_records or []:
        signatures = build_question_signatures(record)
        records.append(signatures)
        if signatures["exact_question_signature"]:
            exact[signatures["exact_question_signature"]] += 1
        if signatures["target_signature"]:
            target[signatures["target_signature"]] += 1
        if signatures["pasuk_skill_signature"]:
            pasuk_skill[signatures["pasuk_skill_signature"]] += 1
        if signatures["skill_type_signature"]:
            skill_type[signatures["skill_type_signature"]] += 1

    return {
        "record_count": len(records),
        "records": records,
        "exact_question_counts": exact,
        "target_counts": target,
        "pasuk_skill_counts": pasuk_skill,
        "skill_type_counts": skill_type,
        "fallback_count": 0,
    }


def _session_signatures(current_session_state):
    state = current_session_state or {}
    exact = Counter()
    target = Counter()
    pasuk_skill = Counter()
    skill_type = Counter()
    for item in list(state.get("recent_questions", [])):
        if item.get("target_word"):
            target[item["target_word"]] += 1
        if item.get("source_pasuk") and item.get("skill"):
            pasuk_skill[normalize_text(f"{item['source_pasuk']}|{item['skill']}")] += 1
        if item.get("skill") or item.get("question_type"):
            skill_type[normalize_text(f"{item.get('skill', '')}|{item.get('question_type', '')}")] += 1
    return {
        "exact": exact,
        "target": target,
        "pasuk_skill": pasuk_skill,
        "skill_type": skill_type,
    }


def score_candidate_exposure(candidate, exposure_index, current_session_state=None):
    if not history_weighting_enabled():
        return {"penalty": 0.0, "reasons": ["history_weighting_disabled"], "signatures": build_question_signatures(candidate)}

    exposure_index = exposure_index or build_exposure_index([])
    signatures = build_question_signatures(candidate)
    session = _session_signatures(current_session_state)
    penalty = 0.0
    reasons = []

    exact_count = exposure_index["exact_question_counts"].get(signatures["exact_question_signature"], 0)
    if exact_count:
        penalty += EXACT_RECENT_REPEAT_PENALTY * exact_count
        reasons.append("exact_recent_repeat")

    target_count = exposure_index["target_counts"].get(signatures["target_signature"], 0)
    target_count += session["target"].get(signatures["target_signature"], 0)
    if target_count:
        penalty += TARGET_RECENT_REPEAT_PENALTY * target_count
        reasons.append("repeated_hebrew_target")

    pasuk_skill_count = exposure_index["pasuk_skill_counts"].get(signatures["pasuk_skill_signature"], 0)
    pasuk_skill_count += session["pasuk_skill"].get(signatures["pasuk_skill_signature"], 0)
    if pasuk_skill_count:
        penalty += PASUK_SKILL_REPEAT_PENALTY * pasuk_skill_count
        reasons.append("repeated_pasuk_skill")

    skill_type_count = exposure_index["skill_type_counts"].get(signatures["skill_type_signature"], 0)
    skill_type_count += session["skill_type"].get(signatures["skill_type_signature"], 0)
    if skill_type_count:
        penalty += SKILL_TYPE_REPEAT_PENALTY * skill_type_count
        reasons.append("repeated_skill_type")

    if not reasons:
        reasons.append("no_history")

    return {
        "penalty": round(penalty, 2),
        "reasons": reasons,
        "signatures": signatures,
        "counts": {
            "exact": exact_count,
            "target": target_count,
            "pasuk_skill": pasuk_skill_count,
            "skill_type": skill_type_count,
        },
    }


def explain_candidate_penalty(candidate, exposure_index, current_session_state=None):
    return score_candidate_exposure(candidate, exposure_index, current_session_state)


def rank_candidates_by_freshness(
    candidates,
    exposure_index,
    current_session_state=None,
    *,
    fallback_min_candidate_count=FALLBACK_MIN_CANDIDATE_COUNT,
):
    candidates = list(candidates or [])
    scored = []
    for index, candidate in enumerate(candidates):
        explanation = score_candidate_exposure(candidate, exposure_index, current_session_state)
        scored.append((explanation["penalty"], index, candidate, explanation))

    scored.sort(key=lambda item: (item[0], item[1]))
    fallback_used = bool(scored) and all(item[0] > 0 for item in scored)
    ranked = []
    for penalty, _index, candidate, explanation in scored:
        if fallback_used and len(scored) <= fallback_min_candidate_count:
            explanation = dict(explanation)
            explanation["reasons"] = list(explanation["reasons"]) + ["fallback_scope_small"]
        ranked.append({"candidate": candidate, "penalty": penalty, "explanation": explanation})
    return ranked


def summarize_exposure(exposure_index, *, limit=5, active=True):
    exposure_index = exposure_index or build_exposure_index([])
    return {
        "repetition_control_active": bool(active and history_weighting_enabled()),
        "recent_attempts_counted": exposure_index.get("record_count", 0),
        "most_repeated_hebrew_targets": exposure_index.get("target_counts", Counter()).most_common(limit),
        "most_repeated_pasuk_skill": exposure_index.get("pasuk_skill_counts", Counter()).most_common(limit),
        "most_repeated_skill_type": exposure_index.get("skill_type_counts", Counter()).most_common(limit),
        "fallback_count": exposure_index.get("fallback_count", 0),
        "scope_small_warning": exposure_index.get("record_count", 0) > 0
        and len(exposure_index.get("target_counts", {})) <= 3,
    }
