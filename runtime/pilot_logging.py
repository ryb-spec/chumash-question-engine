from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from assessment_scope import is_active_pasuk_text

AFFIX_FAMILY_SKILLS = {
    "identify_prefix_meaning",
    "identify_suffix_meaning",
    "identify_pronoun_suffix",
    "identify_verb_marker",
    "identify_prefix_future",
    "identify_suffix_past",
    "prefix",
    "suffix",
}


def classify_question_family(record: dict) -> str:
    skill = str(record.get("skill") or "")
    question_type = str(record.get("question_type") or "")
    if skill in AFFIX_FAMILY_SKILLS:
        return "affix_mechanics"
    if "prefix" in question_type or "suffix" in question_type:
        return "affix_mechanics"
    if question_type in {"verb_tense", "identify_tense"}:
        return "verb_mechanics"
    if question_type in {"translation", "phrase_meaning", "subject_identification", "object_identification"}:
        return "meaning_or_context"
    return "other"


def normalize_attempt_record(record: dict) -> dict:
    normalized = dict(record or {})
    question_type = normalized.get("question_type") or normalized.get("skill") or "unknown"
    normalized["question_type"] = question_type
    normalized["question_family"] = normalized.get("question_family") or classify_question_family(normalized)
    if "in_active_scope" not in normalized:
        pasuk_text = normalized.get("pasuk_text")
        normalized["in_active_scope"] = bool(pasuk_text and is_active_pasuk_text(pasuk_text))
    return normalized


def load_attempts(path: Path) -> list[dict]:
    attempts = []
    if not path.exists():
        return attempts
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                attempts.append(normalize_attempt_record(json.loads(line)))
            except json.JSONDecodeError:
                continue
    return attempts


def append_attempt(path: Path, record: dict) -> None:
    row = normalize_attempt_record(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def summarize_attempts(attempts: list[dict]) -> dict:
    normalized = [normalize_attempt_record(item) for item in attempts]
    served = len(normalized)
    answered = sum(1 for row in normalized if row.get("user_answer") not in {None, ""})
    correct = sum(1 for row in normalized if bool(row.get("is_correct")))

    question_type_totals = Counter(row["question_type"] for row in normalized)
    question_family_totals = Counter(row["question_family"] for row in normalized)
    in_scope_served = sum(1 for row in normalized if row.get("in_active_scope"))

    return {
        "served": served,
        "answered": answered,
        "correct": correct,
        "incorrect": max(0, answered - correct),
        "in_active_scope_served": in_scope_served,
        "out_of_scope_served": max(0, served - in_scope_served),
        "question_type_totals": dict(question_type_totals),
        "question_family_totals": dict(question_family_totals),
        "question_type_total_count": sum(question_type_totals.values()),
        "question_family_total_count": sum(question_family_totals.values()),
    }


def build_pilot_export(attempts: list[dict]) -> dict:
    summary = summarize_attempts(attempts)
    return {
        "summary": summary,
        "consistency": {
            "served_equals_question_type_total": summary["served"] == summary["question_type_total_count"],
            "served_equals_question_family_total": summary["served"] == summary["question_family_total_count"],
            "answered_lte_served": summary["answered"] <= summary["served"],
            "correct_lte_answered": summary["correct"] <= summary["answered"],
        },
    }
