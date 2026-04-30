from __future__ import annotations

import json
from pathlib import Path

from runtime.lesson_session_setup import (
    DEFAULT_MODE_FOCUS,
    default_lesson_session_metadata,
    get_lesson_session_metadata,
    lesson_session_summary_lines,
    reset_lesson_session_metadata,
    update_lesson_session_metadata,
)
from scripts import validate_teacher_lesson_session_setup as validator


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "pipeline_rounds" / "teacher_lesson_session_setup_v1_2026_04_30.json"


def test_default_metadata_is_safe_and_inactive():
    metadata = default_lesson_session_metadata()

    assert metadata["setup_active"] is False
    assert metadata["uses_auth"] is False
    assert metadata["uses_database"] is False
    assert metadata["uses_pii"] is False
    assert metadata["changes_runtime_scope"] is False
    assert metadata["changes_scoring_mastery"] is False
    assert metadata["changes_question_selection"] is False


def test_update_metadata_stores_local_session_context():
    state = {}

    metadata = update_lesson_session_metadata(
        state,
        lesson_label="  Perek 3 review  ",
        mode_focus="Full Passuk view",
        class_period_label="Period 2",
        teacher_notes="Watch repetition.",
    )

    assert metadata["setup_active"] is True
    assert metadata["lesson_label"] == "Perek 3 review"
    assert metadata["mode_focus"] == "Full Passuk view"
    assert metadata["class_period_label"] == "Period 2"
    assert metadata["teacher_notes"] == "Watch repetition."
    assert state


def test_metadata_truncates_long_fields():
    state = {}

    metadata = update_lesson_session_metadata(
        state,
        lesson_label="L" * 120,
        mode_focus="F" * 120,
        class_period_label="P" * 120,
        teacher_notes="N" * 400,
    )

    assert len(metadata["lesson_label"]) == 80
    assert len(metadata["mode_focus"]) == 80
    assert len(metadata["class_period_label"]) == 60
    assert len(metadata["teacher_notes"]) == 240


def test_get_and_reset_metadata():
    state = {}

    assert get_lesson_session_metadata(state)["mode_focus"] == DEFAULT_MODE_FOCUS
    update_lesson_session_metadata(state, lesson_label="Pilot")
    reset = reset_lesson_session_metadata(state)

    assert reset["setup_active"] is False
    assert get_lesson_session_metadata(state)["lesson_label"] == ""


def test_summary_lines_are_teacher_readable():
    metadata = {
        "lesson_label": "Perek 3",
        "mode_focus": "Pilot observation",
        "class_period_label": "Group A",
        "teacher_notes": "Monitor fallback.",
    }

    lines = lesson_session_summary_lines(metadata)

    assert "Lesson: Perek 3" in lines
    assert "Focus: Pilot observation" in lines
    assert "Period: Group A" in lines
    assert "Notes: Monitor fallback." in lines


def test_contract_json_safety_fields():
    payload = json.loads(CONTRACT.read_text(encoding="utf-8"))

    assert payload["feature_name"] == "teacher_lesson_session_setup_v1"
    assert payload["ui_added"] is True
    assert payload["stores_session_metadata_locally"] is True
    assert payload["integrates_with_runtime_exposure_center"] is True
    for key in [
        "uses_auth",
        "uses_database",
        "uses_pii",
        "exposes_raw_logs",
        "creates_new_content",
        "changes_question_selection",
        "changes_scoring_mastery",
        "changes_content_scope",
        "runtime_scope_widened",
        "perek_activated",
        "reviewed_bank_promoted",
        "student_facing_content_created",
        "source_truth_changed",
    ]:
        assert payload[key] is False


def test_ui_helper_imports():
    from ui.teacher_lesson_session_setup import render_teacher_lesson_session_setup

    assert callable(render_teacher_lesson_session_setup)


def test_validator_passes():
    assert validator.validate() == []
