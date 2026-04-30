from __future__ import annotations

import json
from pathlib import Path

from scripts import validate_runtime_learning_intelligence_smoke_test as validator


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "data" / "pipeline_rounds" / "runtime_learning_intelligence_manual_smoke_test_2026_04_30.json"


def load_payload():
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def test_json_parses():
    payload = load_payload()

    assert payload["report_type"] == "manual_smoke_test"
    assert payload["feature_name"] == "runtime_learning_intelligence_v1"


def test_expected_smoke_test_values():
    payload = load_payload()

    assert payload["tester"] == "Yossi"
    assert payload["mode"] == "Full Passuk view"
    assert payload["approximate_questions_answered"] == 15
    assert payload["repeated_questions_decreased"] is True
    assert payload["repeated_hebrew_targets_decreased"] is True
    assert payload["weird_skips_or_missing_questions"] is False
    assert payload["slowdown_observed"] is False
    assert payload["confusing_behavior_observed"] is False
    assert payload["overall_judgment"] == "clean_enough"


def test_small_pool_fallback_remains_unknown():
    payload = load_payload()

    assert payload["small_pool_fallback_served_questions"] is None
    assert payload["small_pool_fallback_status"] == "unknown_not_determined"


def test_safe_to_keep_enabled_and_fallback_test_needed():
    payload = load_payload()

    assert payload["safe_to_keep_enabled"] is True
    assert payload["targeted_fallback_test_still_needed"] is True


def test_safety_booleans_remain_false():
    payload = load_payload()

    for key in [
        "runtime_scope_widened",
        "reviewed_bank_promoted",
        "scoring_mastery_changed",
        "source_truth_changed",
        "auth_database_pii_added",
    ]:
        assert payload[key] is False


def test_validator_passes():
    assert validator.validate() == []
