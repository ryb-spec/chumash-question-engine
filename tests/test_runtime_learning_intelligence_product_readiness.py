from __future__ import annotations

import json
from pathlib import Path

from scripts import validate_runtime_learning_intelligence_product_readiness as validator


ROOT = Path(__file__).resolve().parents[1]
FALLBACK_JSON = ROOT / "data" / "pipeline_rounds" / "runtime_learning_intelligence_small_pool_fallback_test_2026_04_30.json"
READINESS_JSON = ROOT / "data" / "pipeline_rounds" / "runtime_learning_intelligence_v1_product_readiness_gate_2026_04_30.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_fallback_json_parses():
    payload = load(FALLBACK_JSON)

    assert payload["report_type"] == "manual_small_pool_fallback_test"
    assert payload["feature_name"] == "runtime_learning_intelligence_v1"


def test_product_readiness_json_parses():
    payload = load(READINESS_JSON)

    assert payload["gate_name"] == "runtime_learning_intelligence_v1_product_readiness"
    assert payload["readiness_status"] == "ready_for_continued_pilot_use"


def test_expected_fallback_values():
    payload = load(FALLBACK_JSON)

    assert payload["tester"] == "Yossi"
    assert payload["mode"] == "Full Passuk view"
    assert payload["small_pool_fallback_served_questions"] is True
    assert payload["app_avoided_crash_or_blank"] is True
    assert payload["runtime_exposure_center_showed_fallback_status"] is True
    assert payload["repeated_targets_reduced_where_possible"] is True
    assert payload["weird_skips_or_missing_questions"] is False
    assert payload["slowdown_observed"] is False
    assert payload["confusing_behavior_observed"] is False
    assert payload["overall_judgment"] == "fallback_confirmed"


def test_approximate_question_count_is_unknown():
    payload = load(FALLBACK_JSON)

    assert payload["approximate_questions_answered"] is None
    assert payload["approximate_questions_answered_status"] == "unknown_not_recorded"


def test_keep_enabled_and_readiness_status():
    fallback = load(FALLBACK_JSON)
    readiness = load(READINESS_JSON)

    assert fallback["safe_to_keep_enabled"] is True
    assert fallback["targeted_fallback_test_still_needed"] is False
    assert readiness["readiness_status"] == "ready_for_continued_pilot_use"
    assert readiness["keep_enabled_recommended"] is True
    assert readiness["fallback_confirmed"] is True


def test_next_task_is_teacher_lesson_session_setup():
    readiness = load(READINESS_JSON)

    assert readiness["next_recommended_product_task"] == "Teacher Lesson / Session Setup V1"


def test_safety_booleans_remain_false():
    fallback = load(FALLBACK_JSON)
    readiness = load(READINESS_JSON)

    for payload in [fallback, readiness]:
        for key in [
            "runtime_scope_widened",
            "reviewed_bank_promoted",
            "scoring_mastery_changed",
            "source_truth_changed",
            "auth_database_pii_added",
            "question_selection_logic_changed_in_this_task",
            "ui_changed_in_this_task",
        ]:
            assert payload[key] is False
    assert readiness["perek_activated"] is False


def test_validator_passes():
    assert validator.validate() == []
