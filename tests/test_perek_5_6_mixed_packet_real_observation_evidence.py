from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts import validate_perek_5_6_mixed_packet_real_observation_evidence as validator

ROOT = Path(__file__).resolve().parents[1]


def load_contract() -> dict:
    return json.loads(validator.PHASE_JSON.read_text(encoding="utf-8-sig"))


def test_json_parses_and_phase_7_contract() -> None:
    payload = load_contract()
    assert payload["streamlined_process_version"] == "v1"
    assert payload["phase_number"] == 7
    assert payload["phase_name"] == "Observation Decisions + Next-Gate Authorization"
    assert payload["branch_name"] == "feature/perek-5-6-mixed-packet-real-observation-evidence"


def test_evidence_type_is_internal_teacher_review() -> None:
    payload = load_contract()
    assert payload["evidence_type"] == "internal_teacher_review"
    assert payload["reviewer"] == "Yossi"
    assert payload["student_observation_evidence_recorded"] is False
    assert payload["internal_review_evidence_recorded"] is True
    assert payload["fake_observations_created"] is False


def test_observed_count_and_exact_decisions() -> None:
    payload = load_contract()
    assert payload["observed_count"] == 5
    assert payload["not_observed_count"] == 0
    decisions = {item["source_candidate_id"]: item["post_observation_decision"] for item in payload["items"]}
    assert decisions == validator.EXPECTED_DECISIONS


def test_clean_revise_hold_counts_and_ids() -> None:
    payload = load_contract()
    assert payload["clean_after_observation_count"] == 2
    assert payload["revise_count"] == 2
    assert payload["hold_count"] == 1
    clean = [item["source_candidate_id"] for item in payload["items"] if item["next_gate_status"] == "clean_limited_packet_iteration_ready"]
    revise = [item["source_candidate_id"] for item in payload["items"] if item["next_gate_status"] == "revise_before_broader_movement"]
    hold = [item["source_candidate_id"] for item in payload["items"] if item["next_gate_status"] == "held_after_observation"]
    assert clean == validator.EXPECTED_CLEAN_IDS
    assert revise == validator.EXPECTED_REVISE_IDS
    assert hold == validator.EXPECTED_HOLD_IDS


def test_excluded_ids_remain_excluded() -> None:
    payload = load_contract()
    excluded_ids = {item["source_candidate_id"] for item in payload["excluded_candidates"]}
    included_ids = {item["source_candidate_id"] for item in payload["items"]}
    assert excluded_ids == set(validator.EXPECTED_EXCLUDED_IDS)
    assert included_ids == set(validator.EXPECTED_INCLUDED_IDS)
    assert included_ids.isdisjoint(excluded_ids)
    assert all(item["eligible_for_next_gate"] is False for item in payload["excluded_candidates"])


def test_no_fake_observations_and_all_gates_false() -> None:
    payload = load_contract()
    for field in validator.FALSE_TOP_FIELDS:
        assert payload[field] is False
    for item in payload["items"]:
        for field in validator.FALSE_ITEM_FIELDS:
            assert item[field] is False
        assert item["observed"] is True


def test_validator_function_passes() -> None:
    result = validator.validate()
    assert result["ok"], result["errors"]


def test_validator_script_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_perek_5_6_mixed_packet_real_observation_evidence.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        encoding="utf-8",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Perek 5–6 mixed packet real observation evidence validation passed." in result.stdout

