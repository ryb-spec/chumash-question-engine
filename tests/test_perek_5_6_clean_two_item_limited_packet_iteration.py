from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts import validate_perek_5_6_clean_two_item_limited_packet_iteration as validator

ROOT = Path(__file__).resolve().parents[1]


def load_contract() -> dict:
    return json.loads(validator.JSON_PATH.read_text(encoding="utf-8-sig"))


def test_json_parses() -> None:
    payload = load_contract()
    assert payload["iteration_status"] == "clean_two_item_limited_packet_iteration"
    assert payload["item_count"] == 2


def test_exactly_two_included_items() -> None:
    payload = load_contract()
    assert payload["included_candidate_ids"] == validator.EXPECTED_INCLUDED_IDS
    assert [item["source_candidate_id"] for item in payload["items"]] == validator.EXPECTED_INCLUDED_IDS
    assert {item["hebrew_target"] for item in payload["items"]} == {"סֵפֶר", "בֵּן"}


def test_revise_held_excluded_items_are_not_included() -> None:
    payload = load_contract()
    included = set(payload["included_candidate_ids"])
    assert payload["revise_candidate_ids"] == validator.EXPECTED_REVISE_IDS
    assert payload["held_candidate_ids"] == validator.EXPECTED_HELD_IDS
    assert set(payload["excluded_candidate_ids"]) == set(validator.EXPECTED_EXCLUDED_IDS)
    assert included.isdisjoint(set(validator.EXPECTED_REVISE_IDS))
    assert included.isdisjoint(set(validator.EXPECTED_HELD_IDS))
    assert included.isdisjoint(set(validator.EXPECTED_EXCLUDED_IDS))


def test_all_gates_false_and_decisions_null() -> None:
    payload = load_contract()
    for field in validator.FALSE_TOP_FIELDS:
        assert payload[field] is False
    for item in payload["items"]:
        assert item["iteration_review_decision"] is None
        for field in validator.FALSE_ITEM_FIELDS:
            assert item[field] is False


def test_validator_function_passes() -> None:
    result = validator.validate()
    assert result["ok"], result["errors"]


def test_validator_script_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_perek_5_6_clean_two_item_limited_packet_iteration.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        encoding="utf-8",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Perek 5-6 clean two-item limited packet iteration validation passed." in result.stdout
