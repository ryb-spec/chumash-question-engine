from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

GATE_TSV = ROOT / "data/protected_preview_candidate_gates/bereishis_perek_4_broad_vocabulary_protected_preview_candidate_gate_2026_04_30.tsv"
GATE_JSON = ROOT / "data/protected_preview_candidate_gates/bereishis_perek_4_broad_vocabulary_protected_preview_candidate_gate_2026_04_30.json"
REPORT_MD = ROOT / "data/pipeline_rounds/perek_4_broad_vocabulary_protected_preview_candidate_gate_2026_04_30.md"
CONTRACT_JSON = ROOT / "data/pipeline_rounds/perek_4_broad_vocabulary_protected_preview_candidate_gate_2026_04_30.json"
ELIGIBILITY_JSON = ROOT / "data/teacher_review_decisions/bereishis_perek_4_broad_vocabulary_future_gate_eligibility_register_2026_04_30.json"

EXPECTED_CLEAN = {
    "svqcl_p4_001",
    "svqcl_p4_002",
    "svqcl_p4_003",
    "svqcl_p4_005",
    "svqcl_p4_006",
}
EXPECTED_BLOCKED = {
    "bsvb_p4_002",
    "svqcl_p4_004",
    "bsvb_p4_003",
    "bsvb_p4_004",
    "svqcl_p4_007",
    "svqcl_p4_008",
    "svqcl_p4_009",
}


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_gate_tsv_contains_exact_clean_candidate_set() -> None:
    rows = _rows(GATE_TSV)

    assert {row["candidate_id"] for row in rows} == EXPECTED_CLEAN
    assert len(rows) == 5
    assert all(row["gate_status"] == "protected_preview_candidate_gate_eligible" for row in rows)
    assert all(row["runtime_status"] == "not_runtime" for row in rows)
    assert all(row["reviewed_bank_status"] == "not_reviewed_bank" for row in rows)
    assert all(row["protected_preview_packet_status"] == "not_created" for row in rows)


def test_gate_json_and_contract_keep_safety_flags_closed() -> None:
    gate_json = json.loads(GATE_JSON.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT_JSON.read_text(encoding="utf-8"))

    assert set(gate_json["clean_candidate_ids"]) == EXPECTED_CLEAN
    assert set(contract["clean_candidate_ids"]) == EXPECTED_CLEAN
    assert contract["candidate_gate_created"] is True
    assert gate_json["candidate_gate_created"] is True
    for payload in [gate_json, contract]:
        assert payload["protected_preview_packet_created"] is False
        assert payload["protected_preview_promoted"] is False
        assert payload["reviewed_bank_promoted"] is False
        assert payload["runtime_questions_created"] is False
        assert payload["runtime_content_promoted"] is False
        assert payload["runtime_scope_widened"] is False
        assert payload["perek_activated"] is False
        assert payload["ready_for_runtime_activation"] is False
        assert payload["runtime_activation_authorized"] is False


def test_gate_matches_source_eligibility_register() -> None:
    eligibility = json.loads(ELIGIBILITY_JSON.read_text(encoding="utf-8"))

    assert set(eligibility["clean_eligible_candidate_ids"]) == EXPECTED_CLEAN
    assert set(eligibility["revision_required_source_ids"]) == {"bsvb_p4_002", "svqcl_p4_004"}
    assert set(eligibility["held_source_ids"]) == {
        "bsvb_p4_003",
        "bsvb_p4_004",
        "svqcl_p4_007",
        "svqcl_p4_008",
        "svqcl_p4_009",
    }


def test_blocked_rows_are_preserved_in_report_but_not_gate_tsv() -> None:
    report = REPORT_MD.read_text(encoding="utf-8")
    gate_ids = {row["candidate_id"] for row in _rows(GATE_TSV)}

    assert not gate_ids.intersection(EXPECTED_BLOCKED)
    for blocked_id in EXPECTED_BLOCKED:
        assert blocked_id in report
    assert "Protected-preview packet created: no" in report


def test_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_perek_4_broad_vocabulary_protected_preview_candidate_gate.py"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Perek 4 broad vocabulary protected-preview candidate gate validation passed." in result.stdout

