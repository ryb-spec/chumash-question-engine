from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts import validate_perek_5_6_small_internal_protected_preview_packet as validator

ROOT = Path(__file__).resolve().parents[1]


def test_packet_files_exist():
    for path in validator.REQUIRED_FILES:
        assert path.exists(), path


def test_packet_json_parses_and_has_exact_two_items():
    payload = json.loads(validator.PACKET_JSON.read_text(encoding="utf-8"))
    assert payload["packet_status"] == "small_internal_protected_preview_only"
    assert payload["item_count"] == 2
    assert payload["included_candidate_ids"] == validator.EXPECTED_INCLUDED_IDS
    assert [item["source_candidate_id"] for item in payload["items"]] == validator.EXPECTED_INCLUDED_IDS


def test_only_clean_approved_items_are_included():
    payload = json.loads(validator.PACKET_JSON.read_text(encoding="utf-8"))
    included = {item["source_candidate_id"] for item in payload["items"]}
    assert included == {"g2srcdisc_p5_001", "g2srcdisc_p5_005"}
    assert {item["hebrew_target"] for item in payload["items"]} == {"?????", "????"}


def test_excluded_items_are_listed_and_not_in_packet():
    payload = json.loads(validator.PACKET_JSON.read_text(encoding="utf-8"))
    included = {item["source_candidate_id"] for item in payload["items"]}
    assert sorted(payload["excluded_candidate_ids"]) == sorted(validator.EXPECTED_EXCLUDED_IDS)
    assert included.isdisjoint(validator.EXPECTED_EXCLUDED_IDS)


def test_all_safety_booleans_are_false_and_decisions_null():
    payload = json.loads(validator.PACKET_JSON.read_text(encoding="utf-8"))
    assert payload["fake_review_decisions_created"] is False
    assert payload["fake_student_data_created"] is False
    assert payload["source_truth_changed"] is False
    assert payload["question_selection_changed"] is False
    assert payload["scoring_mastery_changed"] is False
    for item in payload["items"]:
        assert item["internal_review_decision"] is None
        for field in validator.FALSE_FIELDS:
            assert item[field] is False


def test_validator_passes_as_script():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_perek_5_6_small_internal_protected_preview_packet.py")],
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
    assert result["tsv_candidate_ids"] == validator.EXPECTED_INCLUDED_IDS
    assert result["json_candidate_ids"] == validator.EXPECTED_INCLUDED_IDS
