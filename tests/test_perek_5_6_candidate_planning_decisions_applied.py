from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts import validate_perek_5_6_candidate_planning_decisions_applied as validator


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "gate_2_source_discovery" / "reports"
DECISIONS_JSON = REPORT / "bereishis_perek_5_6_candidate_planning_decisions_applied_2026_04_29.json"
REVIEW_TSV = ROOT / "data" / "gate_2_protected_preview_candidates" / "bereishis_perek_5_6_protected_preview_candidate_review.tsv"

ADVANCING_IDS = [
    "g2srcdisc_p5_001",
    "g2srcdisc_p5_002",
    "g2srcdisc_p5_005",
    "g2srcdisc_p6_001",
    "g2srcdisc_p6_003",
    "g2srcdisc_p6_006",
    "g2srcdisc_p6_007",
]
EXCLUDED_IDS = [
    "g2srcdisc_p5_003",
    "g2srcdisc_p5_004",
    "g2srcdisc_p6_002",
    "g2srcdisc_p6_004",
    "g2srcdisc_p6_005",
]


def load_payload() -> dict:
    return json.loads(DECISIONS_JSON.read_text(encoding="utf-8"))


def test_decisions_json_parses_and_counts_match():
    payload = load_payload()
    assert payload["eligible_candidate_count"] == 7
    assert payload["excluded_candidate_count"] == 5
    assert payload["decision_counts"] == {
        "advance_to_protected_preview_candidate_review": 2,
        "advance_with_minor_revision": 5,
    }


def test_advancing_and_excluded_candidates_are_exact():
    payload = load_payload()
    assert [decision["candidate_id"] for decision in payload["decisions"]] == ADVANCING_IDS
    assert [candidate["candidate_id"] for candidate in payload["excluded_candidates"]] == EXCLUDED_IDS
    assert all(decision["eligible_for_protected_preview_candidate_review"] for decision in payload["decisions"])
    assert not any(candidate["eligible_for_protected_preview_candidate_review"] for candidate in payload["excluded_candidates"])


def test_all_decision_gates_false():
    payload = load_payload()
    for decision in payload["decisions"]:
        assert decision["runtime_allowed"] is False
        assert decision["reviewed_bank_allowed"] is False
        assert decision["protected_preview_allowed"] is False
        assert decision["student_facing_allowed"] is False
        assert decision["perek_5_activated"] is False
        assert decision["perek_6_activated"] is False


def test_review_layer_contains_only_advancing_candidates_with_false_gates():
    with REVIEW_TSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert [row["candidate_id"] for row in rows] == ADVANCING_IDS
    assert not ({row["candidate_id"] for row in rows} & set(EXCLUDED_IDS))
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
