from __future__ import annotations

import csv
import importlib.util
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "data" / "gate_2_protected_preview_packets" / "reports"
PIPELINE = ROOT / "data" / "pipeline_rounds"

OBS_TSV = REPORTS / "bereishis_perek_4_broad_vocabulary_final_observation_evidence_2026_04_30.tsv"
OBS_JSON = REPORTS / "bereishis_perek_4_broad_vocabulary_final_observation_evidence_2026_04_30.json"
COMPLETION_JSON = PIPELINE / "perek_4_broad_vocabulary_final_internal_completion_gate_2026_04_30.json"
READINESS_TSV = REPORTS / "bereishis_perek_4_broad_vocabulary_final_readiness_register_2026_04_30.tsv"
READINESS_JSON = REPORTS / "bereishis_perek_4_broad_vocabulary_final_readiness_register_2026_04_30.json"
VALIDATOR = ROOT / "scripts" / "validate_perek_4_broad_vocabulary_final_observation_gate.py"

EXPECTED_PACKET_ITEMS = {
    "p4bv_ipp_001",
    "p4bv_ipp_002",
    "p4bv_ipp_003",
    "p4bv_ipp_004",
    "p4bv_ipp_005",
}
EXPECTED_BLOCKED = {"bsvb_p4_002", "svqcl_p4_004", "bsvb_p4_003", "bsvb_p4_004", "svqcl_p4_007", "svqcl_p4_008", "svqcl_p4_009"}


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_perek_4_broad_vocabulary_final_observation_gate", VALIDATOR
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_final_observation_tsv_parses_and_has_five_rows() -> None:
    rows = _rows(OBS_TSV)
    assert len(rows) == 5
    assert {row["packet_item_id"] for row in rows} == EXPECTED_PACKET_ITEMS
    assert all(row["observed"] == "yes" for row in rows)
    assert all(row["reviewer_name"] == "Yossi" for row in rows)


def test_final_observation_json_parses_and_enforces_closed_flags() -> None:
    payload = json.loads(OBS_JSON.read_text(encoding="utf-8"))
    assert payload["evidence_type"] == "perek_4_broad_vocabulary_final_internal_observation"
    assert payload["reviewed_by"] == "Yossi"
    assert payload["observed_count"] == 5
    assert payload["approved_after_observation_count"] == 5
    assert payload["ready_for_reviewed_bank_candidate_planning"] is True
    assert payload["ready_for_runtime_readiness_planning"] is True
    assert payload["ready_for_runtime_activation"] is False
    assert payload["runtime_activation_authorized"] is False
    assert payload["fake_observation_evidence_created"] is False
    for item in payload["items"]:
        assert item["observed"] is True
        assert item["reviewer_name"] == "Yossi"
        assert item["recommended_decision"] == "approve_after_observation"
        assert item["final_internal_status"] == "approved_after_internal_observation"
        assert item["reviewed_bank_status"] == "not_reviewed_bank"
        assert item["runtime_status"] == "not_runtime"
        assert item["student_facing_status"] == "not_student_facing"


def test_completion_json_requires_no_runtime_or_promotion() -> None:
    payload = json.loads(COMPLETION_JSON.read_text(encoding="utf-8"))
    assert payload["internal_observation_evidence_applied"] is True
    assert payload["observed_count"] == 5
    assert payload["approved_after_observation_count"] == 5
    assert payload["ready_for_reviewed_bank_candidate_planning"] is True
    assert payload["ready_for_runtime_activation"] is False
    assert payload["runtime_activation_authorized"] is False
    assert payload["reviewed_bank_promotion_authorized"] is False
    for field in [
        "runtime_scope_widened",
        "perek_activated",
        "reviewed_bank_promoted",
        "runtime_questions_created",
        "runtime_content_promoted",
        "student_facing_content_created",
        "source_truth_changed",
        "fake_student_data_created",
        "raw_logs_exposed",
        "validators_weakened",
    ]:
        assert payload[field] is False
    assert EXPECTED_BLOCKED.issubset(set(payload["still_blocked_items"]))


def test_readiness_register_exists_and_keeps_blocked_rows() -> None:
    rows = _rows(READINESS_TSV)
    payload = json.loads(READINESS_JSON.read_text(encoding="utf-8"))
    assert len(rows) == 12
    assert payload["ready_for_reviewed_bank_candidate_planning"] is True
    assert payload["ready_for_runtime_readiness_planning"] is True
    assert payload["ready_for_runtime_activation"] is False
    assert {row["source_candidate_id"] for row in rows if row["block_type"] == "observed"} == {
        "svqcl_p4_001",
        "svqcl_p4_002",
        "svqcl_p4_003",
        "svqcl_p4_005",
        "svqcl_p4_006",
    }
    assert EXPECTED_BLOCKED.issubset({row["source_candidate_id"] for row in rows if row["block_type"] in {"revision_required", "held"}})
    assert all(row["reviewed_bank_status"] == "not_reviewed_bank" for row in rows)
    assert all(row["runtime_status"] == "not_runtime" for row in rows)
    assert all(row["runtime_activation_authorized"] == "false" for row in rows)


def test_validator_passes() -> None:
    result = subprocess.run(
        ["python", str(VALIDATOR)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Perek 4 broad vocabulary final observation gate validation passed." in result.stdout
