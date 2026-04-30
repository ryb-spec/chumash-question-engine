from __future__ import annotations

import json
from pathlib import Path

from runtime.exposure_summary import (
    build_runtime_exposure_summary,
    build_runtime_exposure_summary_from_default_logs,
)
from scripts import validate_teacher_facing_runtime_exposure_center as validator


def test_exposure_summary_handles_empty_attempt_records():
    summary = build_runtime_exposure_summary([])

    assert summary["recent_attempt_count"] == 0
    assert summary["summary_available"] is False
    assert summary["repetition_control_active"] is True
    assert "No local attempt history found yet." in summary["warning_messages"]


def test_exposure_summary_handles_missing_files_safely(tmp_path):
    summary = build_runtime_exposure_summary_from_default_logs(
        attempt_log_path=tmp_path / "missing_attempts.jsonl",
        pilot_events_path=tmp_path / "missing_pilot.jsonl",
    )

    assert summary["recent_attempt_count"] == 0
    assert summary["history_file_status"]["missing_count"] == 2
    assert summary["summary_available"] is False


def test_exposure_summary_skips_malformed_jsonl(tmp_path):
    attempt_log = tmp_path / "attempt_log.jsonl"
    pilot_log = tmp_path / "pilot_session_events.jsonl"
    attempt_log.write_text(
        "{bad json\n"
        + json.dumps(
            {
                "timestamp_utc": "2026-04-30T00:00:00+00:00",
                "selected_word": "בָּרָא",
                "pasuk_ref": "Bereishis 1:1",
                "skill": "translation",
                "question_type": "translation",
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    pilot_log.write_text("", encoding="utf-8")

    summary = build_runtime_exposure_summary_from_default_logs(
        attempt_log_path=attempt_log,
        pilot_events_path=pilot_log,
    )

    assert summary["recent_attempt_count"] == 1
    assert summary["skipped_or_malformed_count"] == 1


def test_repeated_hebrew_targets_are_counted():
    summary = build_runtime_exposure_summary(
        [
            {"hebrew_target": "בָּרָא", "pasuk_ref": "Bereishis 1:1", "skill": "translation"},
            {"hebrew_target": "בָּרָא", "pasuk_ref": "Bereishis 1:1", "skill": "shoresh"},
            {"hebrew_target": "אוֹר", "pasuk_ref": "Bereishis 1:3", "skill": "translation"},
        ]
    )

    assert summary["repeated_hebrew_targets"][0]["hebrew_target"] == "בָּרָא"
    assert summary["repeated_hebrew_targets"][0]["count"] == 2


def test_repeated_pasuk_skill_pairs_are_counted():
    summary = build_runtime_exposure_summary(
        [
            {"hebrew_target": "בָּרָא", "pasuk_ref": "Bereishis 1:1", "skill": "translation"},
            {"hebrew_target": "אֵת", "pasuk_ref": "Bereishis 1:1", "skill": "translation"},
        ]
    )

    pair = summary["repeated_pasuk_skill_pairs"][0]
    assert pair["pasuk_ref"] == "Bereishis 1:1"
    assert pair["skill"] == "translation"
    assert pair["count"] == 2


def test_repeated_skill_and_question_types_are_counted():
    summary = build_runtime_exposure_summary(
        [
            {"skill": "translation", "question_type": "translation"},
            {"skill": "translation", "question_type": "translation"},
            {"skill": "shoresh", "question_type": "shoresh"},
        ]
    )

    assert summary["repeated_skill_types"][0] == {"skill": "translation", "count": 2}
    assert summary["repeated_question_types"][0] == {"question_type": "translation", "count": 2}


def test_missing_fields_do_not_crash():
    summary = build_runtime_exposure_summary([{}, {"hebrew_target": "אוֹר"}])

    assert summary["recent_attempt_count"] == 2
    assert summary["repeated_hebrew_targets"][0]["hebrew_target"] == "אוֹר"


def test_fallback_status_can_remain_unknown():
    summary = build_runtime_exposure_summary([{"hebrew_target": "אוֹר"}])

    assert summary["small_pool_fallback_status"] == "unknown_not_determined"
    assert summary["fallback_count"] is None
    assert summary["fallback_targeted_test_still_needed"] is True


def test_fallback_status_can_be_observed_when_count_available():
    summary = build_runtime_exposure_summary([{"hebrew_target": "אוֹר"}], fallback_count=2)

    assert summary["small_pool_fallback_status"] == "observed"
    assert summary["fallback_count"] == 2
    assert summary["fallback_targeted_test_still_needed"] is False


def test_no_raw_logs_are_returned_in_summary():
    summary = build_runtime_exposure_summary([{"hebrew_target": "אוֹר", "prompt": "raw prompt"}])

    assert "records" not in summary
    assert "raw_lines" not in summary
    assert "prompt" not in json.dumps(summary, ensure_ascii=False)


def test_ui_helper_imports():
    from ui.runtime_exposure_summary import render_runtime_exposure_center

    assert callable(render_runtime_exposure_center)


def test_validator_passes():
    assert validator.validate() == []
