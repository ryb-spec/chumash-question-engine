from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PACKET_TSV = ROOT / "data/gate_2_protected_preview_packets/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.tsv"
PACKET_JSON = ROOT / "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.json"
CHECKLIST_TSV = ROOT / "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_review_checklist_2026_04_30.tsv"
OBS_TSV = ROOT / "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_observation_template_2026_04_30.tsv"
EXCLUDED_JSON = ROOT / "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_packet_excluded_register_2026_04_30.json"
LINEAGE_MD = ROOT / "data/pipeline_rounds/perek_4_broad_vocabulary_packet_lineage_reconciliation_2026_04_30.md"
MAIN_JSON = ROOT / "data/pipeline_rounds/perek_4_broad_vocabulary_internal_protected_preview_packet_v1_2026_04_30.json"

EXPECTED_INCLUDED = {
    "svqcl_p4_001",
    "svqcl_p4_002",
    "svqcl_p4_003",
    "svqcl_p4_005",
    "svqcl_p4_006",
}
EXCLUDED = {
    "svqcl_p4_004",
    "svqcl_p4_007",
    "svqcl_p4_008",
    "svqcl_p4_009",
    "bsvb_p4_003",
    "bsvb_p4_004",
}


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_packet_tsv_parses_and_contains_exact_five_candidates() -> None:
    rows = _rows(PACKET_TSV)

    assert len(rows) == 5
    assert {row["source_candidate_id"] for row in rows} == EXPECTED_INCLUDED
    assert not {row["source_candidate_id"] for row in rows}.intersection(EXCLUDED)
    assert not {row["vocabulary_id"] for row in rows}.intersection({"bsvb_p4_003", "bsvb_p4_004"})


def test_packet_json_parses_and_keeps_gates_closed() -> None:
    packet = json.loads(PACKET_JSON.read_text(encoding="utf-8"))
    main = json.loads(MAIN_JSON.read_text(encoding="utf-8"))

    assert set(packet["included_candidate_ids"]) == EXPECTED_INCLUDED
    assert packet["protected_preview_packet_created"] is True
    assert main["packet_created"] is True
    assert main["protected_preview_packet_created"] is True
    assert main["reviewed_bank_promoted"] is False
    assert main["runtime_questions_created"] is False
    assert main["runtime_content_promoted"] is False
    assert main["student_facing_content_created"] is False
    assert main["runtime_scope_widened"] is False
    assert main["perek_activated"] is False
    assert main["fake_observation_evidence_created"] is False
    assert main["ready_for_runtime_activation"] is False
    assert main["runtime_activation_authorized"] is False


def test_packet_rows_are_not_runtime_or_reviewed_bank() -> None:
    rows = _rows(PACKET_TSV)

    assert all(row["runtime_status"] == "not_runtime" for row in rows)
    assert all(row["reviewed_bank_status"] == "not_reviewed_bank" for row in rows)
    assert all(row["student_facing_status"] == "not_student_facing" for row in rows)
    assert all(row["distractor_policy"] == "no_distractors_needed" for row in rows)


def test_review_checklist_has_pending_decisions() -> None:
    rows = _rows(CHECKLIST_TSV)

    assert len(rows) == 5
    assert {row["source_candidate_id"] for row in rows} == EXPECTED_INCLUDED
    assert all(row["reviewer_decision"] in {"", "pending"} for row in rows)


def test_observation_template_fields_are_blank() -> None:
    rows = _rows(OBS_TSV)
    blank_fields = [
        "observed",
        "reviewer_name",
        "observation_date",
        "setting",
        "student_or_group_context_optional",
        "did_prompt_make_sense",
        "did_expected_answer_match_teacher_intent",
        "student_confusion_observed",
        "issue_category",
        "recommended_decision",
        "notes",
    ]

    assert len(rows) == 5
    for row in rows:
        assert all(row[field] == "" for field in blank_fields)


def test_excluded_register_and_lineage_exist() -> None:
    excluded = json.loads(EXCLUDED_JSON.read_text(encoding="utf-8"))
    lineage = LINEAGE_MD.read_text(encoding="utf-8")

    assert set(excluded["excluded_revision_required_ids"]) == {"bsvb_p4_002", "svqcl_p4_004"}
    assert set(excluded["excluded_held_ids"]) == {
        "bsvb_p4_003",
        "bsvb_p4_004",
        "svqcl_p4_007",
        "svqcl_p4_008",
        "svqcl_p4_009",
    }
    assert "prior limited" in lineage.lower()
    assert "broad vocabulary" in lineage.lower()


def test_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_perek_4_broad_vocabulary_internal_packet.py"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Perek 4 broad vocabulary internal packet validation passed." in result.stdout

