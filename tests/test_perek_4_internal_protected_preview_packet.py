from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts import validate_perek_4_internal_protected_preview_packet as validator


ROOT = Path(__file__).resolve().parents[1]


def test_packet_files_exist():
    for path in validator.REQUIRED_FILES:
        assert path.exists(), path


def test_packet_json_parses_and_has_exact_four_items():
    payload = json.loads(validator.PACKET_JSON.read_text(encoding="utf-8"))
    assert payload["packet_status"] == "internal_protected_preview_only"
    assert payload["perek"] == 4
    assert payload["item_count"] == 4
    assert [item["source_candidate_id"] for item in payload["items"]] == validator.EXPECTED_IDS


def test_blocked_candidate_excluded_and_listed():
    payload = json.loads(validator.PACKET_JSON.read_text(encoding="utf-8"))
    assert payload["blocked_candidate_ids"] == [validator.BLOCKED_ID]
    assert validator.BLOCKED_ID not in [item["source_candidate_id"] for item in payload["items"]]


def test_all_safety_booleans_are_false_and_internal_decisions_safe():
    payload = json.loads(validator.PACKET_JSON.read_text(encoding="utf-8"))
    for field in validator.FALSE_FIELDS:
        assert payload[field] is False
    assert payload["reviewed_bank_promoted"] is False
    assert payload["fake_review_decisions_created"] is False
    assert payload["fake_student_data_created"] is False
    for item in payload["items"]:
        expected = validator.EXPECTED_INTERNAL_REVIEW_DECISIONS.get(item["packet_item_id"])
        assert item["internal_review_decision"] in (None, expected)
        for field in validator.FALSE_FIELDS:
            assert item[field] is False


def test_required_notes_are_preserved():
    payload = json.loads(validator.PACKET_JSON.read_text(encoding="utf-8"))
    by_id = {item["source_candidate_id"]: item for item in payload["items"]}
    assert "In this phrase" in by_id["g2srcdisc_p4_001"]["question"]
    assert "spacing/session-balance" in by_id["g2srcdisc_p4_003"]["spacing_note"].lower()
    assert "Minchah/offering alias" in by_id["g2srcdisc_p4_004"]["source_or_alias_note"]
    combined_p4_004_notes = (
        by_id["g2srcdisc_p4_004"]["revision_note"] + " " + by_id["g2srcdisc_p4_004"]["source_or_alias_note"]
    )
    assert "part-of-speech only" in combined_p4_004_notes


def test_validator_passes_as_script():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_perek_4_internal_protected_preview_packet.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "validation passed" in result.stdout


def test_validator_function_passes():
    result = validator.validate()
    assert result["ok"], result["errors"]
    assert result["tsv_candidate_ids"] == validator.EXPECTED_IDS
    assert result["json_candidate_ids"] == validator.EXPECTED_IDS
