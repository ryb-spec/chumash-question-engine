from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts import validate_perek_5_6_review_recommendation_report as validator

ROOT = Path(__file__).resolve().parents[1]


def load_payload() -> dict:
    return json.loads(validator.REPORT_JSON.read_text(encoding="utf-8"))


def test_json_parses() -> None:
    payload = load_payload()
    assert payload["report_type"] == "advisory_review_recommendation"


def test_recommendation_lists_are_exact() -> None:
    payload = load_payload()
    assert payload["clean_approved_recommended"] == validator.EXPECTED_CLEAN
    assert payload["revision_watch_recommended"] == validator.EXPECTED_REVISION_WATCH
    assert payload["hold_or_exclude_recommended"] == validator.EXPECTED_HOLD_OR_EXCLUDE


def test_advisory_only_and_no_decisions_applied() -> None:
    payload = load_payload()
    assert payload["recommendation_status"] == "advisory_only"
    assert payload["decisions_applied"] is False


def test_all_safety_booleans_false() -> None:
    payload = load_payload()
    for field in validator.FALSE_FIELDS:
        assert payload[field] is False


def test_validator_function_passes() -> None:
    result = validator.validate()
    assert result["ok"], result["errors"]


def test_validator_script_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_perek_5_6_review_recommendation_report.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Perek 5–6 review recommendation report validation passed." in result.stdout
