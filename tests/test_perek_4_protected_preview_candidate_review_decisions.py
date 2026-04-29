from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts import validate_perek_4_protected_preview_candidate_review_decisions as validator


ROOT = Path(__file__).resolve().parents[1]


def test_required_artifacts_exist():
    for path in validator.REQUIRED_FILES:
        assert path.exists(), path


def test_decisions_json_parses_and_counts_are_exact():
    payload = json.loads(validator.DECISIONS_JSON.read_text(encoding="utf-8"))
    assert payload["candidate_count"] == 5
    assert payload["approved_for_internal_packet_count"] == 2
    assert payload["approve_with_revision_count"] == 2
    assert payload["blocked_count"] == 1


def test_exact_decisions_per_candidate():
    payload = json.loads(validator.DECISIONS_JSON.read_text(encoding="utf-8"))
    decisions = {decision["candidate_id"]: decision for decision in payload["decisions"]}
    assert {candidate_id: decision["decision"] for candidate_id, decision in decisions.items()} == validator.EXPECTED_DECISIONS
    assert decisions[validator.BLOCKED_ID]["eligible_for_internal_protected_preview_packet"] is False


def test_eligible_and_blocked_counts_are_preserved():
    result = validator.validate()
    assert result["ok"], result["errors"]
    assert result["eligible_candidate_ids"] == validator.ELIGIBLE_IDS
    assert result["review_tsv_candidate_ids"] == validator.ELIGIBLE_IDS
    assert result["blocked_candidate_ids"] == [validator.BLOCKED_ID]
    assert validator.BLOCKED_ID not in result["review_tsv_candidate_ids"]


def test_no_runtime_reviewed_bank_student_facing_or_activation_promotion():
    payload = json.loads(validator.DECISIONS_JSON.read_text(encoding="utf-8"))
    assert payload["protected_preview_packet_created"] is False
    for decision in payload["decisions"]:
        assert decision["runtime_allowed"] is False
        assert decision["reviewed_bank_allowed"] is False
        assert decision["student_facing_allowed"] is False
        assert decision["perek_4_activated"] is False


def test_planning_artifact_is_not_an_internal_packet():
    assert validator.PLANNING_MD.exists()
    text = validator.PLANNING_MD.read_text(encoding="utf-8")
    assert "planning-only" in text
    assert "not a packet" in text
    assert validator.BLOCKED_ID in text


def test_validator_passes_as_script():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_perek_4_protected_preview_candidate_review_decisions.py")],
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
