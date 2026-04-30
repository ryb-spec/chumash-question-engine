"""Local teacher lesson/session setup helpers.

This module stores classroom session context in Streamlit session state only.
It does not change active runtime scope, scoring, mastery, question selection,
or content generation.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

SESSION_STATE_KEY = "teacher_lesson_session_setup"
MAX_LABEL_LENGTH = 80
MAX_FOCUS_LENGTH = 80
MAX_PERIOD_LENGTH = 60
MAX_NOTES_LENGTH = 240
DEFAULT_PLANNED_LESSON_FOCUS = "Current app mode"
DEFAULT_MODE_FOCUS = DEFAULT_PLANNED_LESSON_FOCUS


@dataclass(frozen=True)
class LessonSessionMetadata:
    lesson_label: str = ""
    mode_focus: str = DEFAULT_MODE_FOCUS
    planned_lesson_focus: str = DEFAULT_PLANNED_LESSON_FOCUS
    class_period_label: str = ""
    class_group_label: str = ""
    teacher_notes: str = ""
    setup_active: bool = False
    updated_at_utc: str | None = None
    saved_at: str | None = None


def _clean_text(value, max_length: int) -> str:
    text = " ".join(str(value or "").strip().split())
    return text[:max_length]


def default_lesson_session_metadata() -> dict:
    return {
        "lesson_label": "",
        "lesson_session_label": "",
        "planned_lesson_focus": DEFAULT_PLANNED_LESSON_FOCUS,
        "mode_focus": DEFAULT_MODE_FOCUS,
        "class_group_label": "",
        "class_period_label": "",
        "teacher_notes": "",
        "setup_active": False,
        "saved_at": None,
        "updated_at_utc": None,
        "context_provided": False,
        "storage_scope": "local_streamlit_session_state_only",
        "uses_auth": False,
        "uses_database": False,
        "uses_pii": False,
        "changes_runtime_scope": False,
        "changes_scoring_mastery": False,
        "changes_question_selection": False,
    }


def normalize_lesson_session_metadata(metadata: dict | None) -> dict:
    metadata = dict(metadata or {})
    lesson_label = _clean_text(
        metadata.get("lesson_session_label") or metadata.get("lesson_label"),
        MAX_LABEL_LENGTH,
    )
    planned_lesson_focus = _clean_text(
        metadata.get("planned_lesson_focus")
        or metadata.get("teacher_focus_label")
        or metadata.get("mode_focus")
        or DEFAULT_PLANNED_LESSON_FOCUS,
        MAX_FOCUS_LENGTH,
    )
    class_group_label = _clean_text(
        metadata.get("class_group_label")
        or metadata.get("class_period_group_label")
        or metadata.get("class_period_group")
        or metadata.get("class_period_label")
        or metadata.get("period_label")
        or metadata.get("group_label"),
        MAX_PERIOD_LENGTH,
    )
    teacher_notes = _clean_text(metadata.get("teacher_notes"), MAX_NOTES_LENGTH)
    setup_active = bool(
        lesson_label
        or class_group_label
        or teacher_notes
        or planned_lesson_focus != DEFAULT_PLANNED_LESSON_FOCUS
    )
    saved_at = metadata.get("saved_at") or metadata.get("session_context_saved_at") or metadata.get("updated_at_utc")
    saved_at = saved_at if setup_active else None
    return {
        "lesson_label": lesson_label,
        "lesson_session_label": lesson_label,
        "planned_lesson_focus": planned_lesson_focus or DEFAULT_PLANNED_LESSON_FOCUS,
        "mode_focus": planned_lesson_focus or DEFAULT_MODE_FOCUS,
        "class_group_label": class_group_label,
        "class_period_label": class_group_label,
        "teacher_notes": teacher_notes,
        "setup_active": setup_active,
        "saved_at": saved_at,
        "updated_at_utc": saved_at,
        "context_provided": setup_active,
        "storage_scope": "local_streamlit_session_state_only",
        "uses_auth": False,
        "uses_database": False,
        "uses_pii": False,
        "changes_runtime_scope": False,
        "changes_scoring_mastery": False,
        "changes_question_selection": False,
    }


def get_lesson_session_metadata(session_state) -> dict:
    if SESSION_STATE_KEY not in session_state:
        session_state[SESSION_STATE_KEY] = default_lesson_session_metadata()
    session_state[SESSION_STATE_KEY] = normalize_lesson_session_metadata(session_state[SESSION_STATE_KEY])
    return dict(session_state[SESSION_STATE_KEY])


def update_lesson_session_metadata(
    session_state,
    *,
    lesson_label: str = "",
    mode_focus: str = DEFAULT_MODE_FOCUS,
    planned_lesson_focus: str | None = None,
    class_period_label: str = "",
    class_group_label: str | None = None,
    teacher_notes: str = "",
) -> dict:
    saved_at = datetime.now(timezone.utc).isoformat()
    resolved_focus = planned_lesson_focus if planned_lesson_focus is not None else mode_focus
    resolved_group = class_group_label if class_group_label is not None else class_period_label
    payload = normalize_lesson_session_metadata(
        {
            "lesson_label": lesson_label,
            "lesson_session_label": lesson_label,
            "planned_lesson_focus": resolved_focus,
            "mode_focus": resolved_focus,
            "class_group_label": resolved_group,
            "class_period_label": resolved_group,
            "teacher_notes": teacher_notes,
            "saved_at": saved_at,
            "updated_at_utc": saved_at,
        }
    )
    session_state[SESSION_STATE_KEY] = payload
    return dict(payload)


def reset_lesson_session_metadata(session_state) -> dict:
    session_state[SESSION_STATE_KEY] = default_lesson_session_metadata()
    return dict(session_state[SESSION_STATE_KEY])


def lesson_session_summary_lines(metadata: dict | None) -> list[str]:
    metadata = normalize_lesson_session_metadata(metadata)
    if not metadata["setup_active"]:
        return ["No lesson/session label set yet."]
    lines = []
    if metadata["lesson_label"]:
        lines.append(f"Lesson: {metadata['lesson_label']}")
    if metadata["planned_lesson_focus"]:
        lines.append(f"Planned lesson focus: {metadata['planned_lesson_focus']}")
    if metadata["class_group_label"]:
        lines.append(f"Class/group: {metadata['class_group_label']}")
    if metadata["teacher_notes"]:
        lines.append(f"Notes: {metadata['teacher_notes']}")
    return lines or ["No lesson/session label set yet."]
