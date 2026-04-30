from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNING_DIR = ROOT / "data" / "reviewed_bank_candidate_planning"
PIPELINE = ROOT / "data" / "pipeline_rounds"

PLANNING_TSV = PLANNING_DIR / "bereishis_perek_4_broad_vocabulary_reviewed_bank_candidate_planning_2026_04_30.tsv"
PLANNING_JSON = PLANNING_DIR / "bereishis_perek_4_broad_vocabulary_reviewed_bank_candidate_planning_2026_04_30.json"
EVIDENCE_MD = PLANNING_DIR / "bereishis_perek_4_broad_vocabulary_reviewed_bank_candidate_evidence_map_2026_04_30.md"
EVIDENCE_JSON = PLANNING_DIR / "bereishis_perek_4_broad_vocabulary_reviewed_bank_candidate_evidence_map_2026_04_30.json"
BLOCKED_MD = PLANNING_DIR / "bereishis_perek_4_broad_vocabulary_reviewed_bank_candidate_blocked_register_2026_04_30.md"
BLOCKED_JSON = PLANNING_DIR / "bereishis_perek_4_broad_vocabulary_reviewed_bank_candidate_blocked_register_2026_04_30.json"
REPORT_JSON = PIPELINE / "perek_4_broad_vocabulary_reviewed_bank_candidate_planning_2026_04_30.json"
VALIDATOR = ROOT / "scripts" / "validate_perek_4_broad_vocabulary_reviewed_bank_candidate_planning.py"

EXPECTED_INCLUDED = {
    "svqcl_p4_001",
    "svqcl_p4_002",
    "svqcl_p4_003",
    "svqcl_p4_005",
    "svqcl_p4_006",
}
EXPECTED_BLOCKED = {"bsvb_p4_002", "svqcl_p4_004", "bsvb_p4_003", "bsvb_p4_004", "svqcl_p4_007", "svqcl_p4_008", "svqcl_p4_009"}


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_candidate_planning_tsv_parses_and_has_exact_five_rows() -> None:
    rows = _rows(PLANNING_TSV)
    assert len(rows) == 5
    assert {row["source_candidate_id"] for row in rows} == EXPECTED_INCLUDED
    assert EXPECTED_BLOCKED.isdisjoint({row["source_candidate_id"] for row in rows})
    assert all(row["candidate_planning_status"] == "ready_for_yossi_reviewed_bank_decision_packet" for row in rows)


def test_candidate_planning_json_parses_and_keeps_safety_closed() -> None:
    payload = json.loads(PLANNING_JSON.read_text(encoding="utf-8"))
    assert payload["planning_only"] is True
    assert payload["candidate_count"] == 5
    assert set(payload["included_candidate_ids"]) == EXPECTED_INCLUDED
    assert payload["ready_for_reviewed_bank_decision_packet"] is True
    assert payload["ready_for_reviewed_bank_promotion"] is False
    assert payload["ready_for_runtime_activation"] is False
    assert payload["runtime_activation_authorized"] is False
    for field in [
        "reviewed_bank_promoted",
        "reviewed_bank_entries_created",
        "runtime_scope_widened",
        "perek_activated",
        "runtime_questions_created",
        "student_facing_content_created",
        "source_truth_changed",
    ]:
        assert payload[field] is False


def test_candidate_rows_do_not_create_reviewed_bank_or_runtime_status() -> None:
    rows = _rows(PLANNING_TSV)
    assert all(row["reviewed_bank_status"] == "not_reviewed_bank" for row in rows)
    assert all(row["runtime_status"] == "not_runtime" for row in rows)
    assert all(row["student_facing_status"] == "not_student_facing" for row in rows)


def test_evidence_map_and_blocked_register_exist_and_match_ids() -> None:
    assert EVIDENCE_MD.exists()
    assert BLOCKED_MD.exists()
    evidence = json.loads(EVIDENCE_JSON.read_text(encoding="utf-8"))
    blocked = json.loads(BLOCKED_JSON.read_text(encoding="utf-8"))
    assert {item["source_candidate_id"] for item in evidence["items"]} == EXPECTED_INCLUDED
    assert {item["source_candidate_id"] for item in blocked["items"]} == EXPECTED_BLOCKED
    assert "bereishis_perek_4_broad_vocabulary_final_observation_evidence_2026_04_30.json" in EVIDENCE_MD.read_text(
        encoding="utf-8"
    )


def test_main_planning_contract_is_planning_only() -> None:
    payload = json.loads(REPORT_JSON.read_text(encoding="utf-8"))
    assert payload["planning_only"] is True
    assert payload["reviewed_bank_candidate_planning_created"] is True
    assert payload["candidate_count"] == 5
    assert payload["reviewed_bank_promoted"] is False
    assert payload["reviewed_bank_entries_created"] is False
    assert payload["runtime_questions_created"] is False
    assert payload["runtime_activation_authorized"] is False


def test_validator_passes() -> None:
    result = subprocess.run(
        ["python", str(VALIDATOR)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Perek 4 broad vocabulary reviewed-bank candidate planning validation passed." in result.stdout
