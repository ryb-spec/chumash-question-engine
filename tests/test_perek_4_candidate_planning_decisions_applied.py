from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts import validate_perek_4_candidate_planning_decisions_applied as validator


ROOT = Path(__file__).resolve().parents[1]


def test_required_artifacts_exist():
    for path in validator.REQUIRED_FILES:
        assert path.exists(), path


def test_decisions_json_parses_and_counts_are_exact():
    payload = json.loads(validator.DECISIONS_JSON.read_text(encoding="utf-8"))
    assert payload["candidate_count"] == 5
    assert payload["advancing_candidate_count"] == 4
    assert payload["blocked_candidate_count"] == 1


def test_exact_decisions_per_candidate():
    payload = json.loads(validator.DECISIONS_JSON.read_text(encoding="utf-8"))
    decisions = {decision["candidate_id"]: decision for decision in payload["decisions"]}
    assert {candidate_id: decision["planning_review_decision"] for candidate_id, decision in decisions.items()} == validator.EXPECTED_DECISIONS
    assert decisions[validator.BLOCKED_ID]["eligible_for_protected_preview_candidate_review"] is False
    assert decisions[validator.BLOCKED_ID]["source_follow_up_required"] is True


def test_four_candidates_advance_and_blocked_candidate_does_not():
    result = validator.validate()
    assert result["ok"], result["errors"]
    assert result["advancing_candidate_ids"] == validator.ADVANCING_IDS
    assert result["review_tsv_candidate_ids"] == validator.ADVANCING_IDS
    assert validator.BLOCKED_ID not in result["review_tsv_candidate_ids"]


def test_no_runtime_reviewed_bank_student_facing_or_packet_promotion():
    payload = json.loads(validator.DECISIONS_JSON.read_text(encoding="utf-8"))
    assert payload["protected_preview_packet_created"] is False
    for decision in payload["decisions"]:
        assert decision["runtime_allowed"] is False
        assert decision["reviewed_bank_allowed"] is False
        assert decision["student_facing_allowed"] is False
        assert decision["protected_preview_packet_allowed_now"] is False
        assert decision["perek_4_activated"] is False


def test_validator_passes_as_script():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_perek_4_candidate_planning_decisions_applied.py")],
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
