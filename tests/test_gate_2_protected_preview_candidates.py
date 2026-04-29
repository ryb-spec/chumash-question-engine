from __future__ import annotations

import csv

import scripts.validate_gate_2_protected_preview_candidates as validator


def _read_rows(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def test_validator_passes():
    summary = validator.validate_gate_2_protected_preview_candidates()
    assert summary["row_count"] == 10
    assert summary["perek3_row_count"] == 10


def test_perek2_approved_candidate_layer_still_valid():
    rows = _read_rows(validator.TSV)
    assert len(rows) == 10
    assert {row["protected_preview_candidate_status"] for row in rows} == {
        validator.P2_APPROVED_STATUS
    }
    assert {row["yossi_protected_preview_decision"] for row in rows} == {
        validator.P2_APPROVED_DECISION
    }
    for row in rows:
        for col in validator.CLOSED_GATES:
            assert row[col] == "false"


def test_perek3_candidate_file_exists_and_matches_schema():
    assert validator.PEREK3_TSV.exists()
    rows = _read_rows(validator.PEREK3_TSV)
    assert len(rows) == 10
    assert list(rows[0].keys()) == validator.REQUIRED_COLUMNS
    assert {row["approved_family"] for row in rows} == {"basic_noun_recognition"}
    assert all(row["source_ref"].startswith("Bereishis 3:") for row in rows)


def test_perek3_candidates_remain_review_only_and_fail_closed():
    rows = _read_rows(validator.PEREK3_TSV)
    for row in rows:
        assert row["protected_preview_candidate_status"] == validator.P3_PENDING_STATUS
        assert row["draft_review_status"] == validator.NEEDS_YOSSI_REVIEW
        for col in validator.REVIEW_STATUS_COLUMNS:
            assert row[col] == validator.NEEDS_YOSSI_REVIEW
        for col in validator.CLOSED_GATES:
            assert row[col] == "false"
        assert row["yossi_protected_preview_decision"] == ""
        assert row["yossi_protected_preview_notes"] == ""


def test_perek3_rows_are_source_backed_and_have_review_notes():
    source_refs = validator._load_perek3_source_refs()
    rows = _read_rows(validator.PEREK3_TSV)
    for row in rows:
        assert row["source_ref"] in source_refs
        assert "verified Perek 3 source-to-skill" in row["source_evidence_note"]
        assert "not protected-preview approval" in row["caution_note"]
        assert row["explanation"]


def test_perek3_review_packet_and_readiness_report_exist():
    assert validator.PEREK3_PACKET.exists()
    assert validator.PEREK3_SOURCE_READINESS_REPORT.exists()
    packet = validator.PEREK3_PACKET.read_text(encoding="utf-8")
    assert "This is not runtime approval." in packet
    assert "This is not reviewed-bank approval." in packet
    assert "This is not protected-preview approval." in packet
    assert "All Bereishis Perek 3 candidates in this packet remain pending" in packet


def test_no_perek3_internal_packet_created():
    assert not validator.PEREK3_FORBIDDEN_PACKET.exists()
