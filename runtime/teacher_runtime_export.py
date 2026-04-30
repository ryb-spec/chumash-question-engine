"""Teacher-facing runtime exposure export helpers.

This module is read-only with respect to runtime behavior. It combines local
teacher session context and an already-built Runtime Exposure Center summary
into cautious Markdown/JSON reports for teacher review.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from runtime.attempt_history import load_attempt_history
from runtime.exposure_summary import build_runtime_exposure_summary

SCHEMA_VERSION = "1.1"
REPORT_TYPE = "teacher_runtime_exposure_report"
DEFAULT_OUTPUT_DIR = "data/teacher_exports"
RECENT_LOCAL_HISTORY_WARNING = "This report uses recent local history, not a bounded current session."

SCOPE_LABELS = {
    "current_pilot_session": "Current pilot/session only",
    "teacher_setup_window": "Since teacher setup was saved",
    "recent_local_history": "Recent local history diagnostic",
    "no_history_available": "No local history available",
}

SAFETY_CONTRACT = {
    "uses_local_attempt_history": True,
    "uses_auth": False,
    "uses_database": False,
    "uses_pii": False,
    "exposes_raw_logs": False,
    "changes_scoring_mastery": False,
    "changes_question_selection": False,
    "changes_question_selection_weighting": False,
    "changes_runtime_scope": False,
    "widens_runtime_scope": False,
    "activates_perek": False,
    "promotes_reviewed_bank": False,
    "creates_student_facing_content": False,
}


def _coerce_datetime(value: Any | None) -> datetime | None:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    return None


def _now_datetime() -> datetime:
    return datetime.now(timezone.utc)


def _iso_timestamp(value: Any | None = None) -> str:
    return (_coerce_datetime(value) or _now_datetime()).astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _clean_optional(value: Any) -> str | None:
    text = _clean_text(value)
    return text or None


def _as_list(value: Any) -> list:
    return value if isinstance(value, list) else []


def _normalize_counted_items(items: Any, allowed_keys: tuple[str, ...]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for item in _as_list(items):
        if not isinstance(item, dict):
            continue
        clean_item: dict[str, Any] = {}
        for key in allowed_keys:
            if key == "count":
                try:
                    clean_item[key] = int(item.get(key) or 0)
                except (TypeError, ValueError):
                    clean_item[key] = 0
            else:
                value = _clean_optional(item.get(key))
                if value is not None:
                    clean_item[key] = value
        if any(key in clean_item for key in allowed_keys if key != "count"):
            clean_item.setdefault("count", 0)
            normalized.append(clean_item)
    return normalized


def normalize_teacher_session_context(session_context: Any) -> dict[str, Any]:
    """Return a UI/export-safe teacher session context object."""

    context = session_context if isinstance(session_context, dict) else {}
    planned_focus = _clean_optional(
        context.get("planned_lesson_focus")
        or context.get("teacher_focus_label")
        or context.get("mode_focus")
    )
    class_group = _clean_optional(
        context.get("class_group_label")
        or context.get("class_period_group_label")
        or context.get("class_period_group")
        or context.get("class_period_label")
        or context.get("period_label")
        or context.get("group_label")
    )
    saved_at = _clean_optional(
        context.get("saved_at") or context.get("session_context_saved_at") or context.get("updated_at_utc")
    )
    normalized = {
        "lesson_session_label": _clean_optional(
            context.get("lesson_session_label") or context.get("lesson_label") or context.get("label")
        ),
        "planned_lesson_focus": planned_focus,
        "legacy_mode_focus": _clean_optional(context.get("mode_focus")),
        "class_group_label": class_group,
        "teacher_notes": _clean_optional(context.get("teacher_notes")),
        "saved_at": saved_at,
    }
    required_fields = (
        "lesson_session_label",
        "planned_lesson_focus",
        "class_group_label",
        "teacher_notes",
        "saved_at",
    )
    normalized["context_provided"] = any(normalized.get(key) for key in required_fields[:-1])
    normalized["missing_fields"] = [key for key in required_fields if not normalized.get(key)]
    normalized["storage_scope"] = "local_streamlit_session_state_only"
    normalized["uses_auth"] = False
    normalized["uses_database"] = False
    normalized["uses_pii"] = False
    return normalized


def _history_files_from_loaded(history: dict[str, Any]) -> list[dict[str, Any]]:
    source_counts = history.get("source_counts") or {}
    missing = set(history.get("missing_files") or [])
    return [
        {
            "label": "attempt_log",
            "present": not any("attempt_log" in path for path in missing),
            "record_count": int(source_counts.get("attempt_log") or 0),
            "malformed_count": 0,
        },
        {
            "label": "pilot_session_events",
            "present": not any("pilot_session_events" in path for path in missing),
            "record_count": int(source_counts.get("pilot_events") or 0),
            "malformed_count": int(history.get("malformed_count") or 0),
        },
    ]


def _record_timestamp(record: dict[str, Any]) -> datetime | None:
    return _coerce_datetime(record.get("timestamp"))


def _scope_object(
    *,
    scope_type: str,
    pilot_session_id: str | None,
    teacher_setup_saved_at: str | None,
    records_considered: int,
    records_in_scope: int,
    recent_attempt_limit: int,
    scope_warning: str | None,
) -> dict[str, Any]:
    confidence = {
        "current_pilot_session": "high",
        "teacher_setup_window": "medium",
        "recent_local_history": "low",
        "no_history_available": "low",
    }.get(scope_type, "low")
    return {
        "scope_type": scope_type,
        "scope_label": SCOPE_LABELS.get(scope_type, scope_type),
        "current_session_bounded": scope_type == "current_pilot_session",
        "pilot_session_id": pilot_session_id,
        "teacher_setup_saved_at": teacher_setup_saved_at,
        "records_considered": records_considered,
        "records_in_scope": records_in_scope,
        "records_out_of_scope": max(0, records_considered - records_in_scope),
        "recent_attempt_limit": recent_attempt_limit,
        "scope_warning": scope_warning,
        "confidence_level": confidence,
    }


def filter_attempt_records_for_export_scope(
    records: list[dict[str, Any]],
    *,
    scope_type: str,
    pilot_session_id: str | None = None,
    teacher_setup_saved_at: str | None = None,
) -> list[dict[str, Any]]:
    records = [record for record in records if isinstance(record, dict)]
    if scope_type == "current_pilot_session" and pilot_session_id:
        return [record for record in records if record.get("session_id") == pilot_session_id]
    if scope_type == "teacher_setup_window" and teacher_setup_saved_at:
        threshold = _coerce_datetime(teacher_setup_saved_at)
        if threshold is None:
            return []
        return [
            record
            for record in records
            if (_record_timestamp(record) and _record_timestamp(record) >= threshold)
        ]
    if scope_type == "recent_local_history":
        return list(records)
    return []


def determine_teacher_export_scope(
    records: list[dict[str, Any]],
    session_context: Any = None,
    *,
    requested_scope: str = "auto",
    pilot_session_id: str | None = None,
    recent_attempt_limit: int = 500,
) -> dict[str, Any]:
    normalized_session = normalize_teacher_session_context(session_context)
    records = [record for record in records if isinstance(record, dict)]
    records_considered = len(records)
    saved_at = normalized_session.get("saved_at")
    pilot_id = _clean_optional(pilot_session_id)
    requested = requested_scope or "auto"

    if requested in {"auto", "current_pilot_session"} and pilot_id:
        scoped = filter_attempt_records_for_export_scope(
            records,
            scope_type="current_pilot_session",
            pilot_session_id=pilot_id,
        )
        if scoped:
            return _scope_object(
                scope_type="current_pilot_session",
                pilot_session_id=pilot_id,
                teacher_setup_saved_at=saved_at,
                records_considered=records_considered,
                records_in_scope=len(scoped),
                recent_attempt_limit=recent_attempt_limit,
                scope_warning=None,
            )
    if requested in {"auto", "teacher_setup_window"} and saved_at:
        scoped = filter_attempt_records_for_export_scope(
            records,
            scope_type="teacher_setup_window",
            teacher_setup_saved_at=saved_at,
        )
        if scoped:
            return _scope_object(
                scope_type="teacher_setup_window",
                pilot_session_id=pilot_id,
                teacher_setup_saved_at=saved_at,
                records_considered=records_considered,
                records_in_scope=len(scoped),
                recent_attempt_limit=recent_attempt_limit,
                scope_warning="This report is bounded by the teacher setup saved_at timestamp, not by a pilot session id.",
            )
    if records:
        return _scope_object(
            scope_type="recent_local_history",
            pilot_session_id=pilot_id,
            teacher_setup_saved_at=saved_at,
            records_considered=records_considered,
            records_in_scope=records_considered,
            recent_attempt_limit=recent_attempt_limit,
            scope_warning=RECENT_LOCAL_HISTORY_WARNING,
        )
    return _scope_object(
        scope_type="no_history_available",
        pilot_session_id=pilot_id,
        teacher_setup_saved_at=saved_at,
        records_considered=records_considered,
        records_in_scope=0,
        recent_attempt_limit=recent_attempt_limit,
        scope_warning="No local history was available for a bounded teacher report.",
    )


def summarize_export_scope_status(export_scope: dict[str, Any]) -> str:
    if export_scope.get("scope_type") == "current_pilot_session":
        return "Current-session bounded report."
    if export_scope.get("scope_type") == "teacher_setup_window":
        return "Teacher setup window report; medium confidence."
    if export_scope.get("scope_type") == "recent_local_history":
        return RECENT_LOCAL_HISTORY_WARNING
    return "No local history available."


def build_session_bounded_exposure_summary(
    session_context: Any = None,
    *,
    requested_scope: str = "auto",
    pilot_session_id: str | None = None,
    fallback_count: int | None = None,
    max_items: int = 5,
    recent_attempt_limit: int = 500,
) -> tuple[dict[str, Any], dict[str, Any]]:
    history = load_attempt_history(max_records=recent_attempt_limit)
    records = list(history.get("records") or [])
    export_scope = determine_teacher_export_scope(
        records,
        session_context,
        requested_scope=requested_scope,
        pilot_session_id=pilot_session_id,
        recent_attempt_limit=recent_attempt_limit,
    )
    scoped_records = filter_attempt_records_for_export_scope(
        records,
        scope_type=export_scope.get("scope_type"),
        pilot_session_id=export_scope.get("pilot_session_id"),
        teacher_setup_saved_at=export_scope.get("teacher_setup_saved_at"),
    )
    summary = build_runtime_exposure_summary(
        scoped_records,
        max_items=max_items,
        history_files=_history_files_from_loaded(history),
        fallback_count=fallback_count,
        source_counts=history.get("source_counts"),
    )
    summary["attempts_in_scope"] = len(scoped_records)
    summary["malformed_count"] = int(history.get("malformed_count") or 0)
    summary["export_scope_status_message"] = summarize_export_scope_status(export_scope)
    return normalize_exposure_summary(summary, export_scope), export_scope


def normalize_exposure_summary(exposure_summary: Any, export_scope: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return an export-safe exposure summary without raw log records."""

    summary = exposure_summary if isinstance(exposure_summary, dict) else {}
    history_files = []
    for item in _as_list(summary.get("history_files")):
        if not isinstance(item, dict):
            continue
        history_files.append(
            {
                "label": _clean_optional(item.get("label")) or "unknown",
                "present": bool(item.get("present")),
                "record_count": int(item.get("record_count") or 0),
                "malformed_count": int(item.get("malformed_count") or 0),
            }
        )

    fallback_count = summary.get("fallback_count")
    try:
        fallback_count = None if fallback_count is None else int(fallback_count)
    except (TypeError, ValueError):
        fallback_count = None

    normalized = {
        "summary_available": bool(summary.get("summary_available")),
        "repetition_control_active": bool(summary.get("repetition_control_active")),
        "runtime_learning_intelligence_enabled": bool(summary.get("runtime_learning_intelligence_enabled")),
        "recent_attempt_count": int(summary.get("recent_attempt_count") or summary.get("attempts_in_scope") or 0),
        "attempts_in_scope": int(summary.get("attempts_in_scope") or summary.get("recent_attempt_count") or 0),
        "malformed_count": int(summary.get("malformed_count") or summary.get("skipped_or_malformed_count") or 0),
        "history_files": history_files,
        "history_file_status": summary.get("history_file_status") if isinstance(summary.get("history_file_status"), dict) else {},
        "skipped_or_malformed_count": int(summary.get("skipped_or_malformed_count") or 0),
        "last_observed_attempt_timestamp": _clean_optional(summary.get("last_observed_attempt_timestamp")),
        "repeated_hebrew_targets": _normalize_counted_items(
            summary.get("repeated_hebrew_targets"), ("hebrew_target", "count", "last_seen")
        ),
        "repeated_pasuk_skill_pairs": _normalize_counted_items(
            summary.get("repeated_pasuk_skill_pairs"), ("pasuk_ref", "skill", "count")
        ),
        "repeated_skill_types": _normalize_counted_items(
            summary.get("repeated_skill_types"), ("skill", "count")
        ),
        "repeated_question_types": _normalize_counted_items(
            summary.get("repeated_question_types"), ("question_type", "count")
        ),
        "fallback_count": fallback_count,
        "small_pool_fallback_status": _clean_optional(summary.get("small_pool_fallback_status")) or "unknown_not_determined",
        "fallback_targeted_test_still_needed": bool(summary.get("fallback_targeted_test_still_needed")),
        "warning_messages": [_clean_text(message) for message in _as_list(summary.get("warning_messages")) if _clean_text(message)],
        "teacher_interpretation_messages": [
            _clean_text(message)
            for message in _as_list(summary.get("teacher_interpretation_messages"))
            if _clean_text(message)
        ],
        "no_pii_used": True,
        "database_used": False,
        "auth_used": False,
        "raw_logs_exposed": False,
    }
    if export_scope and export_scope.get("scope_warning"):
        normalized["warning_messages"].append(_clean_text(export_scope["scope_warning"]))
    if not normalized["summary_available"] and not normalized["warning_messages"]:
        normalized["warning_messages"].append("No local attempt history found yet.")
    return normalized


def _missing_data_warnings(
    session_context: dict[str, Any],
    exposure_summary: dict[str, Any],
    export_scope: dict[str, Any],
) -> list[str]:
    warnings: list[str] = []
    if not session_context.get("context_provided"):
        warnings.append("Teacher lesson/session setup context was not provided.")
    elif session_context.get("missing_fields"):
        warnings.append(
            "Teacher lesson/session setup was partially filled: "
            + ", ".join(session_context.get("missing_fields") or [])
            + "."
        )
    if not exposure_summary.get("summary_available"):
        warnings.append("No local attempt history was available for this export.")
    if exposure_summary.get("attempts_in_scope", 0) == 0:
        warnings.append("Attempts in export scope is zero; exposure interpretation is limited.")
    if export_scope.get("scope_warning"):
        warnings.append(export_scope["scope_warning"])
    if exposure_summary.get("skipped_or_malformed_count", 0):
        warnings.append(
            f"Malformed local history lines were skipped: {exposure_summary['skipped_or_malformed_count']}."
        )
    if exposure_summary.get("small_pool_fallback_status") in (None, "unknown_not_determined"):
        warnings.append("Small-pool fallback status is unknown or not determined from the available summary.")
    return warnings


def build_teacher_interpretation(export_data: dict[str, Any]) -> dict[str, Any]:
    """Build cautious teacher-facing interpretation from summary data only."""

    exposure = export_data.get("exposure_summary") or {}
    export_scope = export_data.get("export_scope") or {}
    confidence_level = export_scope.get("confidence_level") or "low"
    targets = exposure.get("repeated_hebrew_targets") or []
    pasuk_skill = exposure.get("repeated_pasuk_skill_pairs") or []
    skills = exposure.get("repeated_skill_types") or []
    question_types = exposure.get("repeated_question_types") or []

    possible_reteach_targets = [
        {
            "hebrew_target": item.get("hebrew_target"),
            "count": item.get("count", 0),
            "interpretation": "Consider light reteach or review if this target remained difficult in class.",
        }
        for item in targets
        if int(item.get("count") or 0) >= 2
    ][:5]

    possible_review_focus = []
    for item in pasuk_skill[:5]:
        possible_review_focus.append(
            {
                "focus": f"{item.get('pasuk_ref') or 'unknown ref'} / {item.get('skill') or 'unknown skill'}",
                "count": item.get("count", 0),
                "interpretation": "This pasuk/skill pair appeared repeatedly; monitor whether the safe pool is narrow.",
            }
        )
    for item in skills[:3]:
        possible_review_focus.append(
            {
                "focus": item.get("skill") or "unknown skill",
                "count": item.get("count", 0),
                "interpretation": "This skill appeared often; use teacher judgment before changing lesson focus.",
            }
        )
    for item in question_types[:3]:
        possible_review_focus.append(
            {
                "focus": item.get("question_type") or "unknown question type",
                "count": item.get("count", 0),
                "interpretation": "This question type appeared often; monitor balance in the next session.",
            }
        )

    narrow_pool_indicators = []
    for message in exposure.get("warning_messages") or []:
        lowered = message.lower()
        if "narrow" in lowered or "dominates" in lowered or "scope" in lowered:
            narrow_pool_indicators.append(message)
    if exposure.get("fallback_count"):
        narrow_pool_indicators.append("Fallback/scope-small behavior appeared in local summary counts.")
    if exposure.get("small_pool_fallback_status") == "unknown_not_determined":
        narrow_pool_indicators.append("Fallback status is unknown in this export; keep monitoring small-pool behavior.")
    if export_scope.get("scope_type") == "recent_local_history":
        narrow_pool_indicators.append(RECENT_LOCAL_HISTORY_WARNING)

    missing_evidence = list(export_data.get("missing_data_warnings") or [])
    if not possible_reteach_targets:
        missing_evidence.append("No repeated Hebrew target reached the cautious reteach threshold in this summary.")
    if not possible_review_focus:
        missing_evidence.append("No repeated pasuk/skill, skill, or question-type pattern was available for review focus.")

    return {
        "possible_reteach_targets": possible_reteach_targets,
        "possible_review_focus": possible_review_focus,
        "possible_narrow_pool_indicators": narrow_pool_indicators,
        "monitor_next_session": [
            "Watch whether repeated targets diversify as the session continues.",
            "Confirm that fallback/scope-small messaging remains visible when the safe pool is narrow.",
            "Use this export as teacher evidence only, not as a mastery conclusion.",
            "Review, reteach, or monitor only; do not treat this export as promotion approval.",
        ],
        "missing_evidence": missing_evidence,
        "caution_notes": [
            "This report does not prove mastery.",
            "This report does not approve content for broader use.",
            "This report does not authorize reviewed-bank, runtime-scope, scoring, or question-generation changes.",
        ],
        "confidence_level": confidence_level,
    }


def build_teacher_runtime_export(
    session_context: Any,
    exposure_summary: Any,
    generated_at: Any | None = None,
    *,
    export_scope: dict[str, Any] | None = None,
    requested_scope: str = "auto",
    pilot_session_id: str | None = None,
) -> dict[str, Any]:
    normalized_session = normalize_teacher_session_context(session_context)
    resolved_scope = export_scope or determine_teacher_export_scope(
        [],
        normalized_session,
        requested_scope=requested_scope,
        pilot_session_id=pilot_session_id,
    )
    normalized_exposure = normalize_exposure_summary(exposure_summary, resolved_scope)
    export_data = {
        "schema_version": SCHEMA_VERSION,
        "report_type": REPORT_TYPE,
        "generated_at": _iso_timestamp(generated_at),
        "export_scope": resolved_scope,
        "session_context": normalized_session,
        "exposure_summary": normalized_exposure,
        "teacher_interpretation": {},
        "missing_data_warnings": _missing_data_warnings(normalized_session, normalized_exposure, resolved_scope),
        "output_contract": {
            "supports_markdown_export": True,
            "supports_json_export": True,
            "default_output_dir": DEFAULT_OUTPUT_DIR,
            "raw_log_export_allowed": False,
            "teacher_interpretation_is_cautious": True,
            "mastery_claims_allowed": False,
            "promotion_claims_allowed": False,
        },
        "safety": dict(SAFETY_CONTRACT),
        "content_expansion_readiness": {
            "teacher_export_session_accuracy_fixed": True,
            "current_session_export_supported": resolved_scope.get("scope_type") == "current_pilot_session",
            "teacher_context_field_mapping_fixed": True,
            "misleading_mode_focus_label_fixed": True,
            "markdown_json_single_snapshot": True,
            "ready_for_content_expansion_planning": True,
            "runtime_scope_expansion_allowed_by_this_report": False,
        },
    }
    export_data["teacher_interpretation"] = build_teacher_interpretation(export_data)
    return export_data


def _line_value(value: Any, fallback: str = "not provided") -> str:
    return _clean_optional(value) or fallback


def _bullet_lines(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- none"


def _render_counted_targets(items: list[dict[str, Any]]) -> str:
    if not items:
        return "- none"
    lines = []
    for item in items:
        label = item.get("hebrew_target") or "unknown target"
        last_seen = f"; last seen: {item['last_seen']}" if item.get("last_seen") else ""
        lines.append(f"- {label}: {item.get('count', 0)}{last_seen}")
    return "\n".join(lines)


def _render_pasuk_skill(items: list[dict[str, Any]]) -> str:
    if not items:
        return "- none"
    return "\n".join(
        f"- {item.get('pasuk_ref') or 'unknown ref'} / {item.get('skill') or 'unknown skill'}: {item.get('count', 0)}"
        for item in items
    )


def _render_counted(items: list[dict[str, Any]], key: str, fallback: str) -> str:
    if not items:
        return "- none"
    return "\n".join(f"- {item.get(key) or fallback}: {item.get('count', 0)}" for item in items)


def render_teacher_runtime_export_markdown(export_data: dict[str, Any]) -> str:
    session = export_data.get("session_context") or {}
    export_scope = export_data.get("export_scope") or {}
    exposure = export_data.get("exposure_summary") or {}
    interpretation = export_data.get("teacher_interpretation") or {}
    safety = export_data.get("safety") or {}
    possible_reteach = [
        f"{item.get('hebrew_target')}: {item.get('count', 0)} - {item.get('interpretation')}"
        for item in interpretation.get("possible_reteach_targets", [])
    ]
    possible_focus = [
        f"{item.get('focus')}: {item.get('count', 0)} - {item.get('interpretation')}"
        for item in interpretation.get("possible_review_focus", [])
    ]

    return f"""# Teacher Runtime Exposure Report

## Report metadata

- Report type: `{export_data.get('report_type')}`
- Generated at: `{export_data.get('generated_at')}`
- Schema version: `{export_data.get('schema_version')}`
- Export scope type: `{export_scope.get('scope_type')}`
- Export scope label: {_line_value(export_scope.get('scope_label'), 'unknown')}
- Current-session bounded: {str(bool(export_scope.get('current_session_bounded'))).lower()}
- Export confidence level: {_line_value(export_scope.get('confidence_level'), 'low')}

## Lesson / session context

- Lesson/session label: {_line_value(session.get('lesson_session_label'))}
- Planned lesson focus: {_line_value(session.get('planned_lesson_focus'))}
- Class/group label: {_line_value(session.get('class_group_label'))}
- Teacher notes: {_line_value(session.get('teacher_notes'))}
- Setup saved at: {_line_value(session.get('saved_at'), 'not provided')}
- Context storage: local Streamlit session state only
- Teacher setup note: planned lesson focus is a teacher/report label only. It does not change the student question mode.

## Runtime exposure summary

- Repetition control active: {str(bool(exposure.get('repetition_control_active'))).lower()}
- Runtime Learning Intelligence enabled: {str(bool(exposure.get('runtime_learning_intelligence_enabled'))).lower()}
- Attempts in export scope: {exposure.get('attempts_in_scope', exposure.get('recent_attempt_count', 0))}
- Records considered: {export_scope.get('records_considered', 0)}
- Records in scope: {export_scope.get('records_in_scope', 0)}
- Records out of scope: {export_scope.get('records_out_of_scope', 0)}
- Malformed/skipped log lines: {exposure.get('malformed_count', exposure.get('skipped_or_malformed_count', 0))}
- Last observed attempt timestamp: {_line_value(exposure.get('last_observed_attempt_timestamp'), 'unknown')}
- Small-pool fallback status: {_line_value(exposure.get('small_pool_fallback_status'), 'unknown_not_determined')}
- Fallback count: {_line_value(exposure.get('fallback_count'), 'unknown')}
- Scope warning: {_line_value(export_scope.get('scope_warning'), 'none')}

## Repeated Hebrew targets

{_render_counted_targets(exposure.get('repeated_hebrew_targets') or [])}

## Repeated pasuk / skill combinations

{_render_pasuk_skill(exposure.get('repeated_pasuk_skill_pairs') or [])}

## Repeated skills

{_render_counted(exposure.get('repeated_skill_types') or [], 'skill', 'unknown skill')}

## Repeated question types

{_render_counted(exposure.get('repeated_question_types') or [], 'question_type', 'unknown question type')}

## Teacher interpretation

### Possible reteach targets

{_bullet_lines(possible_reteach)}

### Possible review focus

{_bullet_lines(possible_focus)}

### Possible narrow-pool indicators

{_bullet_lines(interpretation.get('possible_narrow_pool_indicators') or [])}

### Monitor next session

{_bullet_lines(interpretation.get('monitor_next_session') or [])}

### Missing evidence

{_bullet_lines(interpretation.get('missing_evidence') or [])}

### Caution notes

{_bullet_lines(interpretation.get('caution_notes') or [])}

### Current-session confidence level

- {_line_value(interpretation.get('confidence_level'), 'low')}

## Missing data warnings

{_bullet_lines(export_data.get('missing_data_warnings') or [])}

## Safety and privacy confirmation

- Local attempt history only: {str(bool(safety.get('uses_local_attempt_history'))).lower()}
- No login/auth: {str(not bool(safety.get('uses_auth'))).lower()}
- No database: {str(not bool(safety.get('uses_database'))).lower()}
- No PII: {str(not bool(safety.get('uses_pii'))).lower()}
- Raw logs exposed: {str(bool(safety.get('exposes_raw_logs'))).lower()}
- Scoring/mastery changed: {str(bool(safety.get('changes_scoring_mastery'))).lower()}
- Question-selection behavior changed: {str(bool(safety.get('changes_question_selection'))).lower()}
- Question-selection weighting changed: {str(bool(safety.get('changes_question_selection_weighting'))).lower()}
- Runtime scope changed: {str(bool(safety.get('changes_runtime_scope'))).lower()}
- Runtime scope widened: {str(bool(safety.get('widens_runtime_scope'))).lower()}
- Perek activated: {str(bool(safety.get('activates_perek'))).lower()}
- Reviewed bank promoted: {str(bool(safety.get('promotes_reviewed_bank'))).lower()}
- Student-facing content created: {str(bool(safety.get('creates_student_facing_content'))).lower()}

## Privacy note

This export summarizes local teacher/session metadata and local runtime exposure summary fields only. It does not include raw JSONL log lines, student login data, a database record, or PII.
""".strip() + "\n"


def build_teacher_runtime_export_json(export_data: dict[str, Any]) -> str:
    return json.dumps(export_data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def safe_filename_timestamp(generated_at: Any | None = None) -> str:
    return (_coerce_datetime(generated_at) or _now_datetime()).astimezone(timezone.utc).strftime("%Y_%m_%d_%H%M%S")


def write_teacher_runtime_export(export_data: dict[str, Any], output_dir: str | Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    """Write Markdown and JSON export files, returning a safe status object."""

    try:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        timestamp = safe_filename_timestamp(export_data.get("generated_at"))
        md_path = output_path / f"teacher_runtime_exposure_report_{timestamp}.md"
        json_path = output_path / f"teacher_runtime_exposure_report_{timestamp}.json"
        md_path.write_text(render_teacher_runtime_export_markdown(export_data), encoding="utf-8")
        json_path.write_text(build_teacher_runtime_export_json(export_data), encoding="utf-8")
        return {"ok": True, "markdown_path": str(md_path), "json_path": str(json_path), "error": None}
    except Exception as error:
        return {
            "ok": False,
            "markdown_path": None,
            "json_path": None,
            "error": f"{type(error).__name__}: {error}",
        }
