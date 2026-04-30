from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from runtime.teacher_runtime_export import (
    build_teacher_interpretation,
    build_teacher_runtime_export,
    build_teacher_runtime_export_json,
    determine_teacher_export_scope,
    filter_attempt_records_for_export_scope,
    normalize_exposure_summary,
    normalize_teacher_session_context,
    render_teacher_runtime_export_markdown,
    write_teacher_runtime_export,
)
from scripts import validate_teacher_runtime_exposure_export as validator


def sample_session():
    return {
        "lesson_session_label": "Bereishis review",
        "planned_lesson_focus": "Full Passuk view",
        "class_group_label": "Period 2",
        "teacher_notes": "Watch repeated targets.",
        "saved_at": "2026-04-30T12:00:00Z",
    }


def sample_summary():
    return {
        "summary_available": True,
        "repetition_control_active": True,
        "runtime_learning_intelligence_enabled": True,
        "recent_attempt_count": 5,
        "attempts_in_scope": 5,
        "history_files": [
            {"label": "attempt_log", "present": True, "record_count": 3, "malformed_count": 1},
        ],
        "skipped_or_malformed_count": 1,
        "malformed_count": 1,
        "last_observed_attempt_timestamp": "2026-04-30T12:00:00Z",
        "repeated_hebrew_targets": [
            {"hebrew_target": "target_a", "count": 3, "last_seen": "2026-04-30T12:00:00Z"},
        ],
        "repeated_pasuk_skill_pairs": [
            {"pasuk_ref": "Bereishis 1:1", "skill": "translation", "count": 2},
        ],
        "repeated_skill_types": [{"skill": "translation", "count": 4}],
        "repeated_question_types": [{"question_type": "word_meaning", "count": 3}],
        "fallback_count": 1,
        "small_pool_fallback_status": "observed",
        "fallback_targeted_test_still_needed": False,
        "warning_messages": ["One Hebrew target dominates recent history; the safe pool may be narrow."],
    }


def test_builder_handles_empty_and_missing_inputs():
    export_data = build_teacher_runtime_export(None, None, generated_at="2026-04-30T00:00:00Z")

    assert export_data["schema_version"] == "1.1"
    assert export_data["report_type"] == "teacher_runtime_exposure_report"
    assert export_data["generated_at"] == "2026-04-30T00:00:00Z"
    assert export_data["session_context"]["context_provided"] is False
    assert export_data["exposure_summary"]["summary_available"] is False
    assert export_data["export_scope"]["scope_type"] == "no_history_available"
    assert export_data["safety"]["uses_local_attempt_history"] is True


def test_normalizers_tolerate_minimal_input():
    assert normalize_teacher_session_context({})["context_provided"] is False
    summary = normalize_exposure_summary({"repeated_hebrew_targets": ["bad", {"hebrew_target": "or", "count": "2"}]})
    assert summary["repeated_hebrew_targets"] == [{"hebrew_target": "or", "count": 2}]


def test_legacy_teacher_context_keys_normalize_to_canonical_export_fields():
    context = normalize_teacher_session_context(
        {
            "lesson_label": "Legacy lesson",
            "mode_focus": "Pasuk Flow",
            "class_period_label": "Group B",
            "updated_at_utc": "2026-04-30T12:00:00Z",
        }
    )

    assert context["lesson_session_label"] == "Legacy lesson"
    assert context["planned_lesson_focus"] == "Pasuk Flow"
    assert context["class_group_label"] == "Group B"
    assert context["saved_at"] == "2026-04-30T12:00:00Z"


def test_markdown_includes_session_and_exposure_fields():
    export_data = build_teacher_runtime_export(sample_session(), sample_summary(), generated_at="2026-04-30T00:00:00Z")
    markdown = render_teacher_runtime_export_markdown(export_data)

    assert "Bereishis review" in markdown
    assert "Full Passuk view" in markdown
    assert "Period 2" in markdown
    assert "Planned lesson focus: Full Passuk view" in markdown
    assert "Mode focus:" not in markdown
    assert "does not change the student question mode" in markdown
    assert "Watch repeated targets." in markdown
    assert "target_a" in markdown
    assert "Bereishis 1:1 / translation" in markdown
    assert "Small-pool fallback status: observed" in markdown
    assert "Malformed/skipped log lines: 1" in markdown
    assert "Attempts in export scope: 5" in markdown
    assert "No login/auth: true" in markdown
    assert "No database: true" in markdown
    assert "No PII: true" in markdown


def test_markdown_does_not_expose_raw_jsonl_lines():
    export_data = build_teacher_runtime_export(sample_session(), sample_summary())
    markdown = render_teacher_runtime_export_markdown(export_data).lower()

    assert "raw_lines" not in markdown
    assert '{"timestamp' not in markdown
    assert "st.write(line" not in markdown


def test_current_pilot_session_scope_filters_matching_records_only():
    records = [
        {"session_id": "s1", "timestamp": "2026-04-30T12:00:00Z", "hebrew_target": "a"},
        {"session_id": "s2", "timestamp": "2026-04-30T12:01:00Z", "hebrew_target": "b"},
    ]

    scope = determine_teacher_export_scope(records, sample_session(), requested_scope="current_pilot_session", pilot_session_id="s1")
    scoped = filter_attempt_records_for_export_scope(records, scope_type=scope["scope_type"], pilot_session_id="s1")

    assert scope["scope_type"] == "current_pilot_session"
    assert scope["current_session_bounded"] is True
    assert len(scoped) == 1
    assert scoped[0]["session_id"] == "s1"


def test_teacher_setup_window_scope_filters_after_saved_at():
    records = [
        {"session_id": "old", "timestamp": "2026-04-30T11:59:00Z", "hebrew_target": "old"},
        {"session_id": "new", "timestamp": "2026-04-30T12:01:00Z", "hebrew_target": "new"},
    ]

    scope = determine_teacher_export_scope(records, sample_session(), requested_scope="teacher_setup_window")
    scoped = filter_attempt_records_for_export_scope(
        records,
        scope_type=scope["scope_type"],
        teacher_setup_saved_at=scope["teacher_setup_saved_at"],
    )

    assert scope["scope_type"] == "teacher_setup_window"
    assert scope["confidence_level"] == "medium"
    assert len(scoped) == 1
    assert scoped[0]["hebrew_target"] == "new"


def test_recent_local_history_fallback_is_clearly_labeled():
    records = [{"timestamp": "2026-04-30T12:01:00Z", "hebrew_target": "history"}]

    scope = determine_teacher_export_scope(records, {}, requested_scope="recent_local_history")

    assert scope["scope_type"] == "recent_local_history"
    assert scope["current_session_bounded"] is False
    assert scope["confidence_level"] == "low"
    assert "recent local history" in scope["scope_warning"].lower()


def test_missing_session_id_and_timestamps_do_not_crash():
    records = [{"hebrew_target": "history"}]

    current_scope = determine_teacher_export_scope(records, sample_session(), requested_scope="current_pilot_session")
    setup_scope = determine_teacher_export_scope(records, sample_session(), requested_scope="teacher_setup_window")

    assert current_scope["scope_type"] in {"teacher_setup_window", "recent_local_history", "no_history_available"}
    assert setup_scope["scope_type"] in {"recent_local_history", "no_history_available"}


def test_json_serializes_and_includes_safety_fields():
    export_data = build_teacher_runtime_export(sample_session(), sample_summary())
    payload = json.loads(build_teacher_runtime_export_json(export_data))

    assert payload["report_type"] == "teacher_runtime_exposure_report"
    assert payload["export_scope"]["scope_type"]
    assert "content_expansion_readiness" in payload
    safety = payload["safety"]
    assert safety["uses_local_attempt_history"] is True
    assert safety["uses_auth"] is False
    assert safety["uses_database"] is False
    assert safety["uses_pii"] is False
    assert safety["exposes_raw_logs"] is False
    assert safety["changes_question_selection"] is False
    assert safety["changes_question_selection_weighting"] is False
    assert safety["changes_scoring_mastery"] is False


def test_write_helper_creates_output_directory_and_files(tmp_path):
    export_data = build_teacher_runtime_export(
        sample_session(),
        sample_summary(),
        generated_at=datetime(2026, 4, 30, 12, 1, 2, tzinfo=timezone.utc),
    )
    status = write_teacher_runtime_export(export_data, output_dir=tmp_path / "exports")

    assert status["ok"] is True
    assert Path(status["markdown_path"]).exists()
    assert Path(status["json_path"]).exists()
    assert Path(status["markdown_path"]).name == "teacher_runtime_exposure_report_2026_04_30_120102.md"
    assert json.loads(Path(status["json_path"]).read_text(encoding="utf-8"))["report_type"] == "teacher_runtime_exposure_report"


def test_write_helper_handles_write_failure_safely(tmp_path):
    blocker = tmp_path / "not_a_directory"
    blocker.write_text("block", encoding="utf-8")
    export_data = build_teacher_runtime_export(sample_session(), sample_summary())

    status = write_teacher_runtime_export(export_data, output_dir=blocker)

    assert status["ok"] is False
    assert status["markdown_path"] is None
    assert status["json_path"] is None
    assert status["error"]


def test_teacher_interpretation_is_cautious():
    export_data = build_teacher_runtime_export(sample_session(), sample_summary())
    interpretation = build_teacher_interpretation(export_data)
    text = json.dumps(interpretation, ensure_ascii=False).lower()

    assert interpretation["possible_reteach_targets"]
    assert "does not prove mastery" in text
    assert "does not approve content" in text
    assert "reviewed-bank" in text
    assert "mastered" not in text
    assert "approved for runtime" not in text


def test_teacher_interpretation_confidence_level_tracks_scope():
    export_data = build_teacher_runtime_export(
        sample_session(),
        sample_summary(),
        export_scope={
            "scope_type": "current_pilot_session",
            "scope_label": "Current pilot/session only",
            "current_session_bounded": True,
            "pilot_session_id": "s1",
            "teacher_setup_saved_at": "2026-04-30T12:00:00Z",
            "records_considered": 2,
            "records_in_scope": 1,
            "records_out_of_scope": 1,
            "recent_attempt_limit": 500,
            "scope_warning": None,
            "confidence_level": "high",
        },
    )

    assert export_data["teacher_interpretation"]["confidence_level"] == "high"


def test_markdown_and_json_share_one_export_snapshot():
    export_data = build_teacher_runtime_export(sample_session(), sample_summary(), generated_at="2026-04-30T12:34:56Z")
    markdown = render_teacher_runtime_export_markdown(export_data)
    payload = json.loads(build_teacher_runtime_export_json(export_data))

    assert payload["generated_at"] == "2026-04-30T12:34:56Z"
    assert "`2026-04-30T12:34:56Z`" in markdown
    assert f"Fallback count: {payload['exposure_summary']['fallback_count']}" in markdown
    assert payload["exposure_summary"]["repeated_hebrew_targets"][0]["count"] == 3
    assert "target_a: 3" in markdown


def test_missing_evidence_is_identified_when_summary_empty():
    export_data = build_teacher_runtime_export({}, {})
    interpretation = export_data["teacher_interpretation"]

    assert any("No local attempt history" in item for item in interpretation["missing_evidence"])
    assert any("Teacher lesson/session setup" in item for item in interpretation["missing_evidence"])


def test_ui_helper_imports():
    from ui.teacher_runtime_export import render_teacher_runtime_export

    assert callable(render_teacher_runtime_export)


def test_validator_passes():
    assert validator.validate() == []
