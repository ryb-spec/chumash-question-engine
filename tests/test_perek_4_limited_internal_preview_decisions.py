from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "data" / "gate_2_protected_preview_packets" / "reports"
DECISIONS_JSON = REPORT_DIR / "bereishis_perek_4_limited_internal_preview_decisions_applied_2026_04_29.json"
VALIDATOR = ROOT / "scripts" / "validate_perek_4_limited_internal_preview_decisions.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_perek_4_limited_internal_preview_decisions", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_decisions():
    return json.loads(DECISIONS_JSON.read_text(encoding="utf-8"))


def test_limited_internal_preview_decisions_json_exists_and_parses():
    data = load_decisions()
    assert data["item_count"] == 5
    assert data["approve_for_later_packet_iteration_count"] == 2
    assert data["hold_count"] == 2
    assert data["source_follow_up_count"] == 1


def test_exact_decisions_and_next_iteration_eligibility():
    data = load_decisions()
    by_id = {item["item_id"]: item for item in data["decisions"]}
    assert by_id["g2ppacket_p4_001"]["decision"] == "approve_for_later_packet_iteration"
    assert by_id["g2ppacket_p4_002"]["decision"] == "approve_for_later_packet_iteration"
    assert by_id["g2ppacket_p4_003"]["decision"] == "hold"
    assert by_id["g2ppacket_p4_004"]["decision"] == "hold"
    assert by_id["g2srcdisc_p4_005"]["decision"] == "needs_source_follow_up"
    eligible = {item["item_id"] for item in data["decisions"] if item["eligible_for_next_packet_iteration"]}
    assert eligible == {"g2ppacket_p4_001", "g2ppacket_p4_002"}


def test_held_and_source_follow_up_items_remain_blocked():
    data = load_decisions()
    by_id = {item["item_id"]: item for item in data["decisions"]}
    for item_id in ("g2ppacket_p4_003", "g2ppacket_p4_004"):
        assert by_id[item_id]["held_for_spacing_or_alias_review"] is True
        assert by_id[item_id]["eligible_for_next_packet_iteration"] is False
    assert by_id["g2srcdisc_p4_005"]["source_follow_up_required"] is True
    assert by_id["g2srcdisc_p4_005"]["eligible_for_next_packet_iteration"] is False


def test_no_runtime_reviewed_bank_student_facing_promotion():
    data = load_decisions()
    for item in data["decisions"]:
        assert item["runtime_allowed"] is False
        assert item["reviewed_bank_allowed"] is False
        assert item["student_facing_allowed"] is False
        assert item["perek_4_activated"] is False


def test_no_fake_observations_in_updated_template():
    template = (REPORT_DIR / "bereishis_perek_4_limited_internal_preview_observation_template_2026_04_29.md").read_text(encoding="utf-8")
    assert "These decisions are not student observation results" in template
    assert "No fake observations were added" in template
    for line in template.splitlines():
        stripped = line.strip()
        if stripped.startswith("- Student/internal reviewer response:"):
            assert stripped.split(":", 1)[1].strip() == ""


def test_validator_passes():
    module = load_validator()
    module.validate()
