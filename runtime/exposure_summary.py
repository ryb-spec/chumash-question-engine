"""Teacher-facing runtime exposure summaries.

This module is read-only. It summarizes local attempt and pilot history for
teacher visibility without changing question selection, scoring, or mastery.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from runtime.attempt_history import (
    DEFAULT_ATTEMPT_LOG_PATH,
    DEFAULT_PILOT_EVENTS_PATH,
    SERVE_OR_ANSWER_EVENTS,
    read_jsonl_records,
)
from runtime.scope_exhaustion import history_weighting_enabled


UNKNOWN_FALLBACK_STATUS = "unknown_not_determined"


def _clean_text(value):
    return " ".join(str(value or "").strip().split())


def _top_counter_items(counter, *, max_items, key_name):
    return [
        {key_name: key, "count": count}
        for key, count in counter.most_common(max_items)
        if key
    ]


def _last_seen_by(records, key_func):
    last_seen = {}
    for record in records:
        key = key_func(record)
        if not key:
            continue
        timestamp = _clean_text(record.get("timestamp"))
        if timestamp:
            last_seen[key] = timestamp
    return last_seen


def _format_history_file(label, result):
    return {
        "label": label,
        "present": not bool(result.get("missing")),
        "record_count": len(result.get("records") or []),
        "malformed_count": int(result.get("malformed_count") or 0),
    }


def _read_pilot_fallback_count(path):
    path = Path(path)
    if not path.exists():
        return 0, 0

    fallback_count = 0
    malformed_count = 0
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            text = line.strip()
            if not text:
                continue
            try:
                record = json.loads(text)
            except json.JSONDecodeError:
                malformed_count += 1
                continue
            if record.get("event_type") not in SERVE_OR_ANSWER_EVENTS:
                continue
            debug_counts = record.get("debug_rejection_counts") or {}
            if isinstance(debug_counts, dict):
                fallback_count += int(debug_counts.get("fallback_scope_small") or 0)
            if record.get("debug_fallback_path") == "fallback_scope_small":
                fallback_count += 1
    return fallback_count, malformed_count


def summarize_history_file_status(history_files):
    files = list(history_files or [])
    present_count = sum(1 for item in files if item.get("present"))
    malformed_count = sum(int(item.get("malformed_count") or 0) for item in files)
    return {
        "file_count": len(files),
        "present_count": present_count,
        "missing_count": len(files) - present_count,
        "malformed_count": malformed_count,
    }


def build_runtime_exposure_summary(
    attempt_records,
    max_items=5,
    *,
    history_files=None,
    fallback_count=None,
    source_counts=None,
):
    records = [record for record in list(attempt_records or []) if isinstance(record, dict)]
    target_counts = Counter()
    pasuk_skill_counts = Counter()
    skill_counts = Counter()
    question_type_counts = Counter()

    for record in records:
        target = _clean_text(record.get("hebrew_target"))
        pasuk_ref = _clean_text(record.get("pasuk_ref"))
        skill = _clean_text(record.get("skill"))
        question_type = _clean_text(record.get("question_type"))
        if target:
            target_counts[target] += 1
        if pasuk_ref or skill:
            pasuk_skill_counts[(pasuk_ref or "unknown ref", skill or "unknown skill")] += 1
        if skill:
            skill_counts[skill] += 1
        if question_type:
            question_type_counts[question_type] += 1

    target_last_seen = _last_seen_by(records, lambda record: _clean_text(record.get("hebrew_target")))
    repeated_targets = _top_counter_items(target_counts, max_items=max_items, key_name="hebrew_target")
    for item in repeated_targets:
        item["last_seen"] = target_last_seen.get(item["hebrew_target"])

    repeated_pasuk_skill_pairs = [
        {"pasuk_ref": pasuk_ref, "skill": skill, "count": count}
        for (pasuk_ref, skill), count in pasuk_skill_counts.most_common(max_items)
    ]
    repeated_skill_types = _top_counter_items(skill_counts, max_items=max_items, key_name="skill")
    repeated_question_types = _top_counter_items(question_type_counts, max_items=max_items, key_name="question_type")

    fallback_value = None if fallback_count is None else int(fallback_count)
    fallback_observed = bool(fallback_value)
    history_status = summarize_history_file_status(history_files or [])
    summary_available = bool(records)
    warning_messages = []
    if not records:
        warning_messages.append("No local attempt history found yet.")
    if history_status["malformed_count"]:
        warning_messages.append(
            f"Skipped malformed local history lines: {history_status['malformed_count']}."
        )
    if repeated_targets and records:
        top_target = repeated_targets[0]
        if top_target["count"] >= 3 and top_target["count"] / max(1, len(records)) >= 0.35:
            warning_messages.append("One Hebrew target dominates recent history; the safe pool may be narrow.")
    if repeated_pasuk_skill_pairs and records:
        top_pair = repeated_pasuk_skill_pairs[0]
        if top_pair["count"] >= 3 and top_pair["count"] / max(1, len(records)) >= 0.35:
            warning_messages.append("One pasuk/skill pair dominates recent history; watch for scope exhaustion.")

    teacher_messages = [
        "If one word or pasuk-skill pair appears many times, the app may be working with a narrow safe pool.",
        "Repetition control downweights overused items but will still serve questions when the pool is small.",
        "This is a teacher visibility tool; it does not change scores.",
    ]
    if fallback_observed:
        teacher_messages.append("Fallback has appeared in local runtime traces.")
    else:
        teacher_messages.append("Small-pool fallback still needs focused confirmation.")

    return {
        "repetition_control_active": history_weighting_enabled(),
        "runtime_learning_intelligence_enabled": history_weighting_enabled(),
        "recent_attempt_count": len(records),
        "history_files": list(history_files or []),
        "history_file_status": history_status,
        "source_counts": dict(source_counts or {}),
        "skipped_or_malformed_count": history_status["malformed_count"],
        "last_observed_attempt_timestamp": next(
            (record.get("timestamp") for record in reversed(records) if record.get("timestamp")),
            None,
        ),
        "repeated_hebrew_targets": repeated_targets,
        "repeated_pasuk_skill_pairs": repeated_pasuk_skill_pairs,
        "repeated_skill_types": repeated_skill_types,
        "repeated_question_types": repeated_question_types,
        "fallback_count": fallback_value,
        "small_pool_fallback_status": "observed" if fallback_observed else UNKNOWN_FALLBACK_STATUS,
        "fallback_targeted_test_still_needed": not fallback_observed,
        "no_pii_used": True,
        "database_used": False,
        "auth_used": False,
        "raw_logs_exposed": False,
        "summary_available": summary_available,
        "warning_messages": warning_messages,
        "teacher_interpretation_messages": teacher_messages,
    }


def build_runtime_exposure_summary_from_default_logs(
    max_items=5,
    *,
    attempt_log_path=None,
    pilot_events_path=None,
    fallback_count=None,
    max_records=500,
):
    attempt_path = Path(attempt_log_path or DEFAULT_ATTEMPT_LOG_PATH)
    pilot_path = Path(pilot_events_path or DEFAULT_PILOT_EVENTS_PATH)
    attempt_result = read_jsonl_records(attempt_path, max_records=max_records)
    pilot_result = read_jsonl_records(
        pilot_path,
        max_records=max_records,
        event_types=SERVE_OR_ANSWER_EVENTS,
    )
    pilot_fallback_count, pilot_debug_malformed_count = _read_pilot_fallback_count(pilot_path)
    computed_fallback_count = int(fallback_count or 0) + pilot_fallback_count
    fallback_value = computed_fallback_count if computed_fallback_count else None
    history_files = [
        _format_history_file("attempt_log", attempt_result),
        _format_history_file("pilot_session_events", pilot_result),
    ]
    history_files[1]["malformed_count"] = max(
        int(history_files[1].get("malformed_count") or 0),
        pilot_debug_malformed_count,
    )
    records = [*attempt_result.get("records", []), *pilot_result.get("records", [])]
    records = records[-max_records:] if max_records is not None and max_records >= 0 else records
    return build_runtime_exposure_summary(
        records,
        max_items=max_items,
        history_files=history_files,
        fallback_count=fallback_value,
        source_counts={
            "attempt_log": len(attempt_result.get("records") or []),
            "pilot_session_events": len(pilot_result.get("records") or []),
        },
    )


def _format_items(items, label_key):
    if not items:
        return ["None yet."]
    lines = []
    for item in items:
        label = item.get(label_key) or "unknown"
        suffix = f" (last seen: {item['last_seen']})" if item.get("last_seen") else ""
        lines.append(f"{label}: {item.get('count', 0)}{suffix}")
    return lines


def format_repeated_targets(summary):
    return _format_items((summary or {}).get("repeated_hebrew_targets"), "hebrew_target")


def format_repeated_pasuk_skill_pairs(summary):
    items = (summary or {}).get("repeated_pasuk_skill_pairs") or []
    if not items:
        return ["None yet."]
    return [
        f"{item.get('pasuk_ref') or 'unknown ref'} / {item.get('skill') or 'unknown skill'}: {item.get('count', 0)}"
        for item in items
    ]


def format_repeated_skill_types(summary):
    return _format_items((summary or {}).get("repeated_skill_types"), "skill")


def get_runtime_exposure_status_message(summary):
    summary = summary or {}
    if not summary.get("summary_available"):
        return "No local attempt history found yet."
    if summary.get("fallback_count"):
        return "Repetition control is active; small-scope fallback has appeared in local traces."
    return "Repetition control is active; small-pool fallback still needs focused confirmation."
