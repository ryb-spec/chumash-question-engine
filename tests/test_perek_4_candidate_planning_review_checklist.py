from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts import validate_perek_4_candidate_planning_review_checklist as validator


ROOT = Path(__file__).resolve().parents[1]


def test_required_artifacts_exist():
    for path in validator.REQUIRED_FILES:
        assert path.exists(), path


def test_checklist_json_parses_and_has_four_eligible_candidates():
    payload = json.loads(validator.CHECKLIST_JSON.read_text(encoding="utf-8"))
    assert payload["checklist_status"] == "planning_review_only"
    assert payload["eligible_candidate_ids"] == validator.EXPECTED_ELIGIBLE_IDS
    assert len(payload["candidates"]) == 4


def test_blocked_candidate_remains_blocked():
    payload = json.loads(validator.CHECKLIST_JSON.read_text(encoding="utf-8"))
    assert payload["blocked_candidate_ids"] == [validator.BLOCKED_ID]
    assert validator.BLOCKED_ID not in [candidate["candidate_id"] for candidate in payload["candidates"]]


def test_planning_decisions_are_null():
    payload = json.loads(validator.CHECKLIST_JSON.read_text(encoding="utf-8"))
    for candidate in payload["candidates"]:
        assert candidate["planning_review_decision"] is None


def test_no_runtime_reviewed_bank_student_facing_or_packet_promotion():
    payload = json.loads(validator.CHECKLIST_JSON.read_text(encoding="utf-8"))
    assert payload["runtime_allowed"] is False
    assert payload["reviewed_bank_allowed"] is False
    assert payload["protected_preview_packet_allowed_now"] is False
    assert payload["student_facing_allowed"] is False
    assert payload["perek_4_activated"] is False
    for candidate in payload["candidates"]:
        assert candidate["runtime_allowed"] is False
        assert candidate["reviewed_bank_allowed"] is False
        assert candidate["protected_preview_packet_allowed_now"] is False
        assert candidate["student_facing_allowed"] is False
        assert candidate["perek_4_activated"] is False


def test_validator_passes_as_script():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_perek_4_candidate_planning_review_checklist.py")],
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
    assert result["eligible_candidate_ids"] == validator.EXPECTED_ELIGIBLE_IDS
    assert result["planning_tsv_candidate_ids"] == validator.EXPECTED_ELIGIBLE_IDS
