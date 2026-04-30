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


SCHEMA_VERSION = "1.0"
REPORT_TYPE = "teacher_runtime_exposure_report"
DEFAULT_OUTPUT_DIR = "data/teacher_exports"

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


def _coerce_datetime(value: Any | None) -> datetime:
    if value is None:
        return datetime.now(timezone.utc)
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return datetime.now(timezone.utc)
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc)


def _iso_timestamp(value: Any | None = None) -> str:
    return _coerce_datetime(value).astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


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
    normalized = {
        "lesson_session_label": _clean_optional(
            context.get("lesson_session_label") or context.get("lesson_label") or context.get("label")
        ),
        "mode_focus": _clean_optional(context.get("mode_focus")),
        "class_group_label": _clean_optional(
            context.get("class_group_label") or context.get("class_period_group")
        ),
        "teacher_notes": _clean_optional(context.get("teacher_notes")),
    }
    missing = [key for key, value in normalized.items() if value is None]
    normalized["context_provided"] = any(value is not None for value in normalized.values())
    normalized["missing_fields"] = missing
    normalized["storage_scope"] = "local_streamlit_session_state_only"
    normalized["uses_auth"] = False
    normalized["uses_database"] = False
    normalized["uses_pii"] = False
    return normalized


def normalize_exposure_summary(exposure_summary: Any) -> dict[str, Any]:
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
        "recent_attempt_count": int(summary.get("recent_attempt_count") or 0),
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
    if not normalized["summary_available"] and not normalized["warning_messages"]:
        normalized["warning_messages"].append("No local attempt history found yet.")
    return normalized


def _missing_data_warnings(session_context: dict[str, Any], exposure_summary: dict[str, Any]) -> list[str]:
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
    if exposure_summary.get("recent_attempt_count", 0) == 0:
        warnings.append("Recent attempt count is zero; exposure interpretation is limited.")
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
        ],
        "missing_evidence": missing_evidence,
        "caution_notes": [
            "This report does not prove mastery.",
            "This report does not approve content for broader use.",
            "This report does not authorize reviewed-bank, runtime-scope, scoring, or question-generation changes.",
        ],
    }


def build_teacher_runtime_export(session_context: Any, exposure_summary: Any, generated_at: Any | None = None) -> dict[str, Any]:
    normalized_session = normalize_teacher_session_context(session_context)
    normalized_exposure = normalize_exposure_summary(exposure_summary)
    export_data = {
        "schema_version": SCHEMA_VERSION,
        "report_type": REPORT_TYPE,
        "generated_at": _iso_timestamp(generated_at),
        "session_context": normalized_session,
        "exposure_summary": normalized_exposure,
        "teacher_interpretation": {},
        "missing_data_warnings": _missing_data_warnings(normalized_session, normalized_exposure),
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

## Lesson / session context

- Lesson/session label: {_line_value(session.get('lesson_session_label'))}
- Mode focus: {_line_value(session.get('mode_focus'))}
- Class/group label: {_line_value(session.get('class_group_label'))}
- Teacher notes: {_line_value(session.get('teacher_notes'))}
- Context storage: local Streamlit session state only

## Runtime exposure summary

- Repetition control active: {str(bool(exposure.get('repetition_control_active'))).lower()}
- Runtime Learning Intelligence enabled: {str(bool(exposure.get('runtime_learning_intelligence_enabled'))).lower()}
- Recent attempts counted: {exposure.get('recent_attempt_count', 0)}
- Malformed/skipped log lines: {exposure.get('skipped_or_malformed_count', 0)}
- Last observed attempt timestamp: {_line_value(exposure.get('last_observed_attempt_timestamp'), 'unknown')}
- Small-pool fallback status: {_line_value(exposure.get('small_pool_fallback_status'), 'unknown_not_determined')}
- Fallback count: {_line_value(exposure.get('fallback_count'), 'unknown')}

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
    return _coerce_datetime(generated_at).astimezone(timezone.utc).strftime("%Y_%m_%d_%H%M%S")


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
