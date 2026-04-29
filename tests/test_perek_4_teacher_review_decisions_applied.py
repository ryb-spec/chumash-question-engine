from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts import validate_perek_4_teacher_review_decisions_applied as validator


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_DECISIONS = {
    "g2srcdisc_p4_001": "approve_with_revision",
    "g2srcdisc_p4_002": "approve_for_protected_preview",
    "g2srcdisc_p4_003": "approve_with_revision",
    "g2srcdisc_p4_004": "approve_with_revision",
    "g2srcdisc_p4_005": "needs_source_follow_up",
}


def test_required_artifacts_exist():
    for path in validator.REQUIRED_FILES:
        assert path.exists(), path


def test_decisions_json_parses_and_has_expected_count():
    payload = json.loads(validator.DECISIONS_JSON.read_text(encoding="utf-8"))
    assert payload["candidate_count"] == 5
    assert len(payload["decisions"]) == 5


def test_exact_yossi_decisions_are_applied():
    payload = json.loads(validator.DECISIONS_JSON.read_text(encoding="utf-8"))
    decisions = {decision["candidate_id"]: decision for decision in payload["decisions"]}
    assert {candidate_id: decision["teacher_decision"] for candidate_id, decision in decisions.items()} == EXPECTED_DECISIONS
    assert "In this phrase" in decisions["g2srcdisc_p4_001"]["revised_question_wording"]
    assert decisions["g2srcdisc_p4_005"]["eligible_for_next_gate"] is False
    assert decisions["g2srcdisc_p4_005"]["source_follow_up_required"] is True


def test_no_runtime_reviewed_bank_or_student_facing_promotion():
    payload = json.loads(validator.DECISIONS_JSON.read_text(encoding="utf-8"))
    for decision in payload["decisions"]:
        assert decision["runtime_allowed"] is False
        assert decision["reviewed_bank_allowed"] is False
        assert decision["student_facing_allowed"] is False
        assert decision["protected_preview_packet_allowed_now"] is False
        assert decision["perek_4_activated"] is False


def test_candidate_planning_layer_excludes_blocked_ot_candidate():
    result = validator.validate()
    assert result["ok"], result["errors"]
    assert result["planning_candidate_ids"] == validator.ELIGIBLE_IDS
    assert validator.BLOCKED_ID not in result["planning_candidate_ids"]


def test_validator_passes_as_script():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_perek_4_teacher_review_decisions_applied.py")],
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
