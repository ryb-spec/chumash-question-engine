from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET_DIR = ROOT / "data" / "gate_2_protected_preview_packets"
REPORT_DIR = PACKET_DIR / "reports"
PIPELINE_DIR = ROOT / "data" / "pipeline_rounds"
ITERATION_JSON = REPORT_DIR / "bereishis_perek_4_two_item_limited_internal_packet_iteration_2026_04_29.json"
GATE_JSON = PIPELINE_DIR / "perek_4_final_internal_iteration_and_perek_5_6_source_discovery_gate_2026_04_29.json"
VALIDATOR = ROOT / "scripts" / "validate_perek_4_final_iteration_and_perek_5_6_gate.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_perek_4_final_iteration_and_perek_5_6_gate", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_iteration_json_has_exactly_two_included_items():
    data = json.loads(ITERATION_JSON.read_text(encoding="utf-8"))
    assert data["item_count"] == 2
    assert set(data["included_candidate_ids"]) == {"g2srcdisc_p4_001", "g2srcdisc_p4_002"}
    assert {item["source_candidate_id"] for item in data["items"]} == {"g2srcdisc_p4_001", "g2srcdisc_p4_002"}


def test_held_and_blocked_items_are_excluded():
    data = json.loads(ITERATION_JSON.read_text(encoding="utf-8"))
    assert set(data["excluded_or_held_ids"]) == {"g2srcdisc_p4_003", "g2srcdisc_p4_004", "g2srcdisc_p4_005"}
    assert not ({"g2srcdisc_p4_003", "g2srcdisc_p4_004", "g2srcdisc_p4_005"} & {item["source_candidate_id"] for item in data["items"]})


def test_iteration_items_keep_all_runtime_permissions_false():
    data = json.loads(ITERATION_JSON.read_text(encoding="utf-8"))
    for item in data["items"]:
        assert item["observation_result"] is None
        assert item["runtime_allowed"] is False
        assert item["reviewed_bank_allowed"] is False
        assert item["student_facing_allowed"] is False
        assert item["perek_4_activated"] is False


def test_perek_5_6_is_allowed_next_only_as_source_discovery():
    gate = json.loads(GATE_JSON.read_text(encoding="utf-8"))
    assert gate["perek_5_6_source_discovery_allowed_next"] is True
    assert gate["perek_5_6_runtime_allowed"] is False
    assert gate["perek_5_6_reviewed_bank_allowed"] is False
    assert gate["perek_5_6_student_facing_allowed"] is False
    assert gate["perek_5_6_protected_preview_packet_allowed"] is False


def test_perek_4_not_closed_or_runtime_active():
    gate = json.loads(GATE_JSON.read_text(encoding="utf-8"))
    assert gate["perek_4_two_item_iteration_created"] is True
    assert gate["perek_4_full_closure"] is False
    assert gate["perek_4_runtime_active"] is False
    assert gate["runtime_scope_widened"] is False
    assert gate["reviewed_bank_promoted"] is False
    assert gate["student_facing_created"] is False


def test_validator_passes():
    module = load_validator()
    module.validate()
