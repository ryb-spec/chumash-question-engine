from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DECISION_TSV = ROOT / "data/teacher_review_decisions/bereishis_perek_4_broad_vocabulary_teacher_review_decisions_applied_2026_04_30.tsv"
DECISION_JSON = ROOT / "data/teacher_review_decisions/bereishis_perek_4_broad_vocabulary_teacher_review_decisions_applied_2026_04_30.json"
ELIGIBILITY_TSV = ROOT / "data/teacher_review_decisions/bereishis_perek_4_broad_vocabulary_future_gate_eligibility_register_2026_04_30.tsv"
ELIGIBILITY_JSON = ROOT / "data/teacher_review_decisions/bereishis_perek_4_broad_vocabulary_future_gate_eligibility_register_2026_04_30.json"
CONTRACT_JSON = ROOT / "data/pipeline_rounds/broad_vocabulary_teacher_review_decisions_applied_2026_04_30.json"
NEXT_PROMPT = ROOT / "data/pipeline_rounds/next_codex_prompt_perek_4_broad_vocabulary_protected_preview_candidate_gate_2026_04_30.md"

EXPECTED_CLEAN = {
    "svqcl_p4_001",
    "svqcl_p4_002",
    "svqcl_p4_003",
    "svqcl_p4_005",
    "svqcl_p4_006",
}

EXPECTED_HELD = {
    "bsvb_p4_003",
    "bsvb_p4_004",
    "svqcl_p4_007",
    "svqcl_p4_008",
    "svqcl_p4_009",
}

EXPECTED_REVISION = {"bsvb_p4_002", "svqcl_p4_004"}


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_decision_artifacts_parse_and_mark_yossi_review() -> None:
    rows = _rows(DECISION_TSV)
    decision_json = json.loads(DECISION_JSON.read_text(encoding="utf-8"))

    assert len(rows) == 16
    assert decision_json["teacher_decisions_created"] is True
    assert decision_json["fake_teacher_approval_created"] is False
    assert decision_json["reviewed_by"] == "Yossi"
    assert decision_json["reviewed_at"] == "2026-04-30"
    assert len(decision_json["decisions"]) == 16
    assert all(row["reviewed_by"] == "Yossi" for row in rows)
    assert all(row["reviewed_at"] == "2026-04-30" for row in rows)


def test_no_blank_or_pending_decisions_remain() -> None:
    rows = _rows(DECISION_TSV)

    forbidden = {"", "pending", "needs_teacher_review", "not_applicable"}
    assert all(row["yossi_decision"] not in forbidden for row in rows)


def test_clean_revision_and_held_sets_are_exact() -> None:
    rows = _rows(ELIGIBILITY_TSV)

    clean = {row["source_id"] for row in rows if row["eligibility_classification"] == "clean_eligible_for_future_protected_preview_candidate_gate"}
    held = {row["source_id"] for row in rows if row["eligibility_classification"] == "held_for_follow_up"}
    revision = {row["source_id"] for row in rows if row["eligibility_classification"] == "revision_required_before_future_gate"}

    assert clean == EXPECTED_CLEAN
    assert held == EXPECTED_HELD
    assert revision == EXPECTED_REVISION
    assert not clean.intersection(held | revision)


def test_eligibility_json_matches_register() -> None:
    eligibility = json.loads(ELIGIBILITY_JSON.read_text(encoding="utf-8"))

    assert set(eligibility["clean_eligible_candidate_ids"]) == EXPECTED_CLEAN
    assert set(eligibility["held_source_ids"]) == EXPECTED_HELD
    assert set(eligibility["revision_required_source_ids"]) == EXPECTED_REVISION
    assert eligibility["runtime_status"] == "not_runtime"
    assert eligibility["reviewed_bank_status"] == "not_reviewed_bank"
    assert eligibility["protected_preview_packet_created"] is False
    assert eligibility["runtime_activation_authorized"] is False


def test_no_runtime_or_reviewed_bank_eligibility_exists() -> None:
    decision_rows = _rows(DECISION_TSV)
    eligibility_rows = _rows(ELIGIBILITY_TSV)

    assert all(row["runtime_status"] == "not_runtime" for row in decision_rows)
    assert all(row["reviewed_bank_status"] == "not_reviewed_bank" for row in decision_rows)
    assert all(row["runtime_status"] == "not_runtime" for row in eligibility_rows)
    assert all(row["reviewed_bank_status"] == "not_reviewed_bank" for row in eligibility_rows)


def test_contract_keeps_all_safety_gates_closed() -> None:
    contract = json.loads(CONTRACT_JSON.read_text(encoding="utf-8"))

    assert contract["teacher_decisions_created"] is True
    assert contract["fake_teacher_approval_created"] is False
    assert contract["clean_protected_preview_candidate_eligible_count"] == 5
    assert contract["revision_required_count"] == 2
    assert contract["held_count"] == 7
    assert contract["protected_preview_packet_created"] is False
    assert contract["protected_preview_promoted"] is False
    assert contract["reviewed_bank_promoted"] is False
    assert contract["runtime_questions_created"] is False
    assert contract["runtime_content_promoted"] is False
    assert contract["runtime_scope_widened"] is False
    assert contract["perek_activated"] is False
    assert contract["source_truth_changed"] is False
    assert contract["ready_for_runtime_activation"] is False
    assert contract["runtime_activation_authorized"] is False


def test_next_prompt_exists_and_limits_future_input_set() -> None:
    prompt = NEXT_PROMPT.read_text(encoding="utf-8")

    for candidate_id in EXPECTED_CLEAN:
        assert candidate_id in prompt
    for blocked_id in EXPECTED_HELD | EXPECTED_REVISION:
        assert blocked_id in prompt
    assert "Do not activate runtime." in prompt
    assert "Do not promote reviewed bank." in prompt


def test_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_broad_vocabulary_teacher_review_decisions.py"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Broad vocabulary teacher review decisions validation passed." in result.stdout

