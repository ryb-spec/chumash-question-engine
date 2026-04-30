from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts import validate_perek_5_6_protected_preview_candidate_review_decisions as validator


ROOT = Path(__file__).resolve().parents[1]
DECISIONS_JSON = (
    ROOT
    / "data"
    / "gate_2_protected_preview_candidates"
    / "reports"
    / "bereishis_perek_5_6_protected_preview_candidate_review_decisions_applied_2026_04_29.json"
)
REVIEW_TSV = ROOT / "data" / "gate_2_protected_preview_candidates" / "bereishis_perek_5_6_protected_preview_candidate_review.tsv"
PACKET_TSV = ROOT / "data" / "gate_2_protected_preview_packets" / "bereishis_perek_5_6_internal_protected_preview_packet.tsv"

EXPECTED_IDS = [
    "g2srcdisc_p5_001",
    "g2srcdisc_p5_002",
    "g2srcdisc_p5_005",
    "g2srcdisc_p6_001",
    "g2srcdisc_p6_003",
    "g2srcdisc_p6_006",
    "g2srcdisc_p6_007",
]


def load_payload() -> dict:
    return json.loads(DECISIONS_JSON.read_text(encoding="utf-8"))


def test_json_parses_and_decision_counts_match():
    payload = load_payload()
    assert payload["decision_counts"] == {
        "approve_for_internal_protected_preview_packet": 2,
        "approve_with_revision": 5,
        "needs_follow_up": 0,
        "reject": 0,
        "source_only": 0,
    }
    assert payload["clean_approved_count"] == 2
    assert payload["approve_with_revision_count"] == 5


def test_clean_and_revision_candidates_are_exact():
    payload = load_payload()
    assert [decision["candidate_id"] for decision in payload["decisions"]] == EXPECTED_IDS
    clean = [decision["candidate_id"] for decision in payload["decisions"] if decision["clean_ready_for_internal_packet"]]
    revision = [decision["candidate_id"] for decision in payload["decisions"] if decision["revision_required"]]
    assert clean == ["g2srcdisc_p5_001", "g2srcdisc_p5_005"]
    assert revision == ["g2srcdisc_p5_002", "g2srcdisc_p6_001", "g2srcdisc_p6_003", "g2srcdisc_p6_006", "g2srcdisc_p6_007"]


def test_all_decision_gates_false():
    payload = load_payload()
    for decision in payload["decisions"]:
        assert decision["runtime_allowed"] is False
        assert decision["reviewed_bank_allowed"] is False
        assert decision["protected_preview_allowed"] is False
        assert decision["student_facing_allowed"] is False
        assert decision["perek_5_activated"] is False
        assert decision["perek_6_activated"] is False


def test_review_tsv_excludes_blocked_candidates_and_keeps_gates_false():
    with REVIEW_TSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert [row["candidate_id"] for row in rows] == EXPECTED_IDS
    for row in rows:
        assert row["runtime_allowed"] == "false"
        assert row["reviewed_bank_allowed"] == "false"
        assert row["protected_preview_allowed"] == "false"
        assert row["student_facing_allowed"] == "false"
        assert row["perek_5_activated"] == "false"
        assert row["perek_6_activated"] == "false"


def test_no_internal_packet_created_and_validator_passes():
    assert not PACKET_TSV.exists()
    result = validator.validate()
    assert result["valid"], result["errors"]
