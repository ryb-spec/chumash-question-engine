from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts import validate_perek_4_limited_protected_preview_build_gate as validator

ROOT = Path(__file__).resolve().parents[1]
TSV = ROOT / "data/gate_2_protected_preview_packets/bereishis_perek_4_limited_protected_preview_build_gate_2026_04_30.tsv"
JSON_PATH = ROOT / "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_limited_protected_preview_build_gate_2026_04_30.json"
MD = ROOT / "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_limited_protected_preview_build_gate_2026_04_30.md"


def test_contract_json_parses_and_links_planning_gate():
    payload = json.loads(JSON_PATH.read_text(encoding="utf-8-sig"))
    assert payload["feature_name"] == "perek_4_limited_protected_preview_build_gate"
    assert payload["source_planning_candidate_id"] == "cepg_primary_bereishis_perek_4_limited_protected_preview_build"
    assert payload["packet_item_count"] == 2


def test_selected_items_are_exactly_two_clean_items():
    payload = json.loads(JSON_PATH.read_text(encoding="utf-8-sig"))
    assert payload["selected_candidate_ids"] == ["g2srcdisc_p4_001", "g2srcdisc_p4_002"]
    assert [item["source_candidate_id"] for item in payload["selected_items"]] == ["g2srcdisc_p4_001", "g2srcdisc_p4_002"]


def test_revision_watch_items_are_preserved_outside_packet():
    payload = json.loads(JSON_PATH.read_text(encoding="utf-8-sig"))
    assert payload["revision_watch_candidate_ids"] == ["g2srcdisc_p4_003", "g2srcdisc_p4_004"]
    assert {item["status"] for item in payload["revision_watch_items"]} == {"revision_watch_preserved"}


def test_tsv_contains_only_selected_items_and_all_gates_false():
    with TSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert [row["source_candidate_id"] for row in rows] == ["g2srcdisc_p4_001", "g2srcdisc_p4_002"]
    for row in rows:
        assert row["runtime_allowed"] == "false"
        assert row["reviewed_bank_allowed"] == "false"
        assert row["student_facing_allowed"] == "false"
        assert row["perek_4_activated"] == "false"


def test_contract_safety_flags_are_false():
    payload = json.loads(JSON_PATH.read_text(encoding="utf-8-sig"))
    for key in [
        "runtime_scope_widened",
        "perek_activated",
        "perek_4_activated",
        "reviewed_bank_promoted",
        "runtime_content_promoted",
        "student_facing_content_created",
        "scoring_mastery_changed",
        "question_generation_changed",
        "question_selection_changed",
        "question_selection_weighting_changed",
        "source_truth_changed",
        "fake_teacher_approval_created",
        "fake_student_data_created",
        "raw_logs_exposed",
        "validators_weakened",
        "ready_for_runtime_activation",
        "runtime_activation_authorized",
        "reviewed_bank_promotion_authorized",
    ]:
        assert payload[key] is False


def test_report_preserves_boundaries_without_runtime_language():
    text = MD.read_text(encoding="utf-8-sig").lower()
    assert "revision-watch items preserved" in text
    assert "runtime scope widened: no" in text
    assert "reviewed-bank promoted: no" in text
    assert "approved for runtime" not in text
    assert "promoted to reviewed bank" not in text


def test_validator_passes():
    assert validator.validate() == []
