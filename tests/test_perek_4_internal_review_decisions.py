from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts import validate_perek_4_internal_review_decisions as validator


ROOT = Path(__file__).resolve().parents[1]


def test_required_artifacts_exist():
    for path in validator.REQUIRED_FILES:
        assert path.exists(), path


def test_exact_decisions():
    payload = json.loads(validator.DECISIONS_JSON.read_text(encoding="utf-8"))
    decisions = {decision["packet_item_id"]: decision["decision"] for decision in payload["decisions"]}
    assert decisions == validator.EXPECTED_DECISIONS
    assert payload["approve_for_limited_internal_preview_count"] == 2
    assert payload["approve_with_revision_count"] == 2


def test_clean_readiness_lane_has_only_two_items():
    result = validator.validate()
    assert result["ok"], result["errors"]
    assert result["clean_ready"] == validator.CLEAN_READY
    text = validator.READINESS_MD.read_text(encoding="utf-8")
    assert "g2ppacket_p4_001" in text
    assert "g2ppacket_p4_002" in text
    assert "g2ppacket_p4_003" in text
    assert "g2ppacket_p4_004" in text


def test_revision_blocked_register_has_expected_items():
    text = validator.BLOCKED_REGISTER.read_text(encoding="utf-8")
    for item_id in validator.REVISION_BLOCKED:
        assert item_id in text


def test_no_runtime_reviewed_bank_student_facing_promotion():
    payload = json.loads(validator.DECISIONS_JSON.read_text(encoding="utf-8"))
    for field in validator.FALSE_FIELDS:
        assert payload[field] is False
    for decision in payload["decisions"]:
        for field in validator.FALSE_FIELDS:
            assert decision[field] is False


def test_observation_template_fields_are_blank_and_no_fake_observations():
    text = validator.OBSERVATION_TEMPLATE.read_text(encoding="utf-8")
    assert "Observed by: " in text
    assert "Observation date: " in text
    assert "Student/internal reviewer response: " in text
    assert "Decision after observation: " in text
    assert "No fake observations are present" in text
    active = text.split("## Active observation items", 1)[1].split("## Excluded", 1)[0]
    assert "g2ppacket_p4_003" not in active
    assert "g2ppacket_p4_004" not in active


def test_validator_passes_as_script():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_perek_4_internal_review_decisions.py")],
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
