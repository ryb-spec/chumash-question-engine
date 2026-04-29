from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts import validate_perek_3_pilot_evidence_pack as validator


ROOT = Path(__file__).resolve().parents[1]


def test_required_artifacts_exist():
    for path in validator.REQUIRED_FILES:
        assert path.exists(), validator.repo_relative(path)
    assert validator.OBSERVATION_INTAKE.exists()


def test_manifest_json_parses_and_safety_booleans_are_closed():
    manifest = json.loads(validator.MANIFEST.read_text(encoding="utf-8"))
    assert manifest["branch_name"] == "feature/perek-3-pilot-evidence-pack"
    assert manifest["no_runtime_behavior_changed"] is True
    assert manifest["perek_4_activated"] is False
    assert manifest["fake_data_created"] is False


def test_validator_helper_passes():
    summary = validator.validate_perek_3_pilot_evidence_pack()
    assert summary["valid"], summary["errors"]


def test_validator_script_exits_successfully():
    completed = subprocess.run(
        [sys.executable, "scripts/validate_perek_3_pilot_evidence_pack.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0
    assert "Perek 3 pilot evidence pack validation passed." in completed.stdout


def test_forbidden_promotion_claims_are_not_present_in_pilot_evidence_artifacts():
    errors = []
    for path in validator.PILOT_EVIDENCE_ARTIFACTS:
        if path.exists():
            errors.extend(validator.forbidden_claim_errors(path))
    assert errors == []


def test_required_safety_phrases_are_present():
    runbook = validator.RUNBOOK.read_text(encoding="utf-8")
    action_plan = validator.ACTION_PLAN.read_text(encoding="utf-8")
    observation_intake = validator.OBSERVATION_INTAKE.read_text(encoding="utf-8")
    assert "Learn Mode" in runbook
    assert "does not approve runtime expansion" in runbook
    assert "does not activate Perek 4" in runbook
    assert "does not change runtime behavior" in action_plan
    assert "Reviewer Instructions — Real Evidence Only" in observation_intake
