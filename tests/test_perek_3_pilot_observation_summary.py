from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts import validate_perek_3_pilot_observation_summary as validator


ROOT = Path(__file__).resolve().parents[1]


def test_summary_artifacts_exist():
    assert validator.SUMMARY_MD.exists()
    assert validator.SUMMARY_JSON.exists()
    assert validator.OBSERVATION_INTAKE.exists()


def test_summary_json_counts_and_safety_booleans():
    payload = json.loads(validator.SUMMARY_JSON.read_text(encoding="utf-8"))
    assert payload["pilot_date"] == "2026-04-29"
    assert payload["students_observed"] == 3
    assert payload["total_questions_answered"] == 30
    assert payload["mode"] == "Learn Mode"
    assert payload["no_runtime_promotion"] is True
    assert payload["perek_4_activated"] is False
    assert payload["fake_data_created"] is False


def test_issues_cover_required_categories_and_no_candidate_forcing():
    payload = json.loads(validator.SUMMARY_JSON.read_text(encoding="utf-8"))
    categories = {issue["issue_category"] for issue in payload["issues"]}
    assert "unclear wording" in categories
    assert "bad distractors" in categories
    assert "shoresh/source follow-up" in categories
    assert "phrase-translation distractor quality" in categories
    assert any(issue["candidate_id"] == "not_available" for issue in payload["issues"])


def test_observation_intake_records_real_pilot_evidence_without_promotion():
    intake = validator.OBSERVATION_INTAKE.read_text(encoding="utf-8")
    assert "Fresh Perek 3 pilot evidence recorded - 2026-04-29" in intake
    assert "No row is runtime-approved" in intake
    assert "No row is reviewed-bank-approved" in intake
    assert "No fake observations were added" in intake
    assert "runtime_allowed=true" not in intake


def test_validator_helper_passes():
    summary = validator.validate_perek_3_pilot_observation_summary()
    assert summary["valid"], summary["errors"]


def test_validator_script_exits_successfully():
    completed = subprocess.run(
        [sys.executable, "scripts/validate_perek_3_pilot_observation_summary.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0
    assert "Perek 3 pilot observation summary validation passed." in completed.stdout
