from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from scripts import validate_perek_5_6_teacher_review_decisions_applied as validator


ROOT = Path(__file__).resolve().parents[1]
DECISIONS_JSON = (
    ROOT
    / "data"
    / "gate_2_source_discovery"
    / "reports"
    / "bereishis_perek_5_6_teacher_review_decisions_applied_2026_04_29.json"
)
PLANNING_TSV = ROOT / "data" / "gate_2_source_discovery" / "bereishis_perek_5_6_candidate_planning.tsv"

EXPECTED_COUNTS = {
    "approve_for_next_candidate_planning": 2,
    "approve_with_revision": 5,
    "hold_for_spacing_or_balance": 2,
    "needs_source_follow_up": 2,
    "source_only": 1,
    "reject": 0,
}
ELIGIBLE_IDS = {
    "g2srcdisc_p5_001",
    "g2srcdisc_p5_002",
    "g2srcdisc_p5_005",
    "g2srcdisc_p6_001",
    "g2srcdisc_p6_003",
    "g2srcdisc_p6_006",
    "g2srcdisc_p6_007",
}
BLOCKED_IDS = {
    "g2srcdisc_p5_003",
    "g2srcdisc_p5_004",
    "g2srcdisc_p6_002",
    "g2srcdisc_p6_004",
    "g2srcdisc_p6_005",
}


def load_payload() -> dict:
    return json.loads(DECISIONS_JSON.read_text(encoding="utf-8"))


def test_decisions_json_parses_and_counts_match():
    payload = load_payload()
    assert payload["candidate_count"] == 12
    assert payload["perek_5_candidate_count"] == 5
    assert payload["perek_6_candidate_count"] == 7
    assert payload["decision_counts"] == EXPECTED_COUNTS
    counts = Counter(decision["teacher_decision"] for decision in payload["decisions"])
    for key, expected in EXPECTED_COUNTS.items():
        assert counts[key] == expected


def test_exactly_seven_candidates_are_eligible():
    payload = load_payload()
    eligible = {
        decision["candidate_id"]
        for decision in payload["decisions"]
        if decision["eligible_for_next_candidate_planning"]
    }
    assert eligible == ELIGIBLE_IDS
    blocked = {
        decision["candidate_id"]
        for decision in payload["decisions"]
        if not decision["eligible_for_next_candidate_planning"]
    }
    assert blocked == BLOCKED_IDS


def test_all_decision_gates_remain_false():
    payload = load_payload()
    for decision in payload["decisions"]:
        assert decision["runtime_allowed"] is False
        assert decision["reviewed_bank_allowed"] is False
        assert decision["protected_preview_allowed"] is False
        assert decision["student_facing_allowed"] is False
        assert decision["perek_5_activated"] is False
        assert decision["perek_6_activated"] is False


def test_candidate_planning_tsv_contains_only_eligible_candidates():
    with PLANNING_TSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    row_ids = {row["candidate_id"] for row in rows}
    assert row_ids == ELIGIBLE_IDS
    assert not (row_ids & BLOCKED_IDS)
    for row in rows:
        assert row["runtime_allowed"] == "false"
        assert row["reviewed_bank_allowed"] == "false"
        assert row["protected_preview_allowed"] == "false"
        assert row["student_facing_allowed"] == "false"
        assert row["perek_5_activated"] == "false"
        assert row["perek_6_activated"] == "false"


def test_validator_passes():
    result = validator.validate()
    assert result["valid"], result["errors"]
