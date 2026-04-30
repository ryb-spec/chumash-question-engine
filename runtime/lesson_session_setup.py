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
DEFAULT_MODE_FOCUS = "Current app mode"


@dataclass(frozen=True)
class LessonSessionMetadata:
    lesson_label: str = ""
    mode_focus: str = DEFAULT_MODE_FOCUS
    class_period_label: str = ""
    teacher_notes: str = ""
    setup_active: bool = False
    updated_at_utc: str | None = None


def _clean_text(value, max_length: int) -> str:
    text = " ".join(str(value or "").strip().split())
    return text[:max_length]


def default_lesson_session_metadata() -> dict:
    return {
        "lesson_label": "",
        "mode_focus": DEFAULT_MODE_FOCUS,
        "class_period_label": "",
        "teacher_notes": "",
        "setup_active": False,
        "updated_at_utc": None,
        "uses_auth": False,
        "uses_database": False,
        "uses_pii": False,
        "changes_runtime_scope": False,
        "changes_scoring_mastery": False,
        "changes_question_selection": False,
    }


def normalize_lesson_session_metadata(metadata: dict | None) -> dict:
    metadata = dict(metadata or {})
    lesson_label = _clean_text(metadata.get("lesson_label"), MAX_LABEL_LENGTH)
    mode_focus = _clean_text(metadata.get("mode_focus") or DEFAULT_MODE_FOCUS, MAX_FOCUS_LENGTH)
    class_period_label = _clean_text(metadata.get("class_period_label"), MAX_PERIOD_LENGTH)
    teacher_notes = _clean_text(metadata.get("teacher_notes"), MAX_NOTES_LENGTH)
    setup_active = bool(lesson_label or class_period_label or teacher_notes or mode_focus != DEFAULT_MODE_FOCUS)
    updated_at = metadata.get("updated_at_utc") if setup_active else None
    return {
        "lesson_label": lesson_label,
        "mode_focus": mode_focus or DEFAULT_MODE_FOCUS,
        "class_period_label": class_period_label,
        "teacher_notes": teacher_notes,
        "setup_active": setup_active,
        "updated_at_utc": updated_at,
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
    class_period_label: str = "",
    teacher_notes: str = "",
) -> dict:
    payload = normalize_lesson_session_metadata(
        {
            "lesson_label": lesson_label,
            "mode_focus": mode_focus,
            "class_period_label": class_period_label,
            "teacher_notes": teacher_notes,
            "updated_at_utc": datetime.now(timezone.utc).isoformat(),
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
    if metadata["mode_focus"]:
        lines.append(f"Focus: {metadata['mode_focus']}")
    if metadata["class_period_label"]:
        lines.append(f"Period: {metadata['class_period_label']}")
    if metadata["teacher_notes"]:
        lines.append(f"Notes: {metadata['teacher_notes']}")
    return lines or ["No lesson/session label set yet."]
