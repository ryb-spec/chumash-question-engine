from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts import validate_perek_4_compressed_teacher_review_packet as validator


ROOT = Path(__file__).resolve().parents[1]


def test_required_artifacts_exist():
    for path in validator.REQUIRED_FILES:
        assert path.exists(), path


def test_override_json_safety_booleans():
    payload = json.loads(validator.OVERRIDE_JSON.read_text(encoding="utf-8"))
    assert payload["override_given_by"] == "Yossi"
    assert payload["allows_perek_4_teacher_review_packet"] is True
    assert payload["allows_perek_4_runtime_activation"] is False
    assert payload["allows_active_scope_expansion"] is False
    assert payload["allows_reviewed_bank_promotion"] is False
    assert payload["allows_protected_preview_packet_creation"] is False
    assert payload["unresolved_perek_3_items_remain"] is True
    assert payload["fake_data_created"] is False


def test_packet_json_is_teacher_review_only_and_matches_inventory():
    result = validator.validate()
    assert result["ok"], result["errors"]
    payload = json.loads(validator.PACKET_JSON.read_text(encoding="utf-8"))
    assert payload["packet_status"] == "teacher_review_only"
    assert payload["candidate_count"] == 5
    assert result["candidate_ids"] == result["source_inventory_candidate_ids"]
    assert payload["perek_4_activated"] is False
    assert payload["runtime_scope_widened"] is False
    assert payload["reviewed_bank_promoted"] is False
    assert payload["fake_teacher_decisions_created"] is False


def test_every_candidate_keeps_gates_closed_and_no_teacher_decision():
    payload = json.loads(validator.PACKET_JSON.read_text(encoding="utf-8"))
    for candidate in payload["candidates"]:
        assert candidate["teacher_decision"] is None
        assert candidate["runtime_allowed"] is False
        assert candidate["reviewed_bank_allowed"] is False
        assert candidate["protected_preview_allowed"] is False
        assert candidate["student_facing_allowed"] is False
        assert candidate["broader_use_allowed"] is False
        assert candidate["perek_4_activated"] is False
        assert candidate["expected_answer"] == "noun"
        assert len(candidate["distractors"]) == 3


def test_packet_and_readiness_reports_state_safety_boundaries():
    packet_text = validator.PACKET_MD.read_text(encoding="utf-8")
    readiness_text = validator.READINESS_MD.read_text(encoding="utf-8")
    assert "teacher-review only" in packet_text
    assert "not runtime content" in packet_text
    assert "not a protected-preview packet" in packet_text
    assert "No teacher decisions are applied by this packet." in packet_text
    assert "This packet is not a protected-preview packet and is not runtime content" in readiness_text
    assert "No Perek 4 runtime activation occurred." in readiness_text
    assert "No active scope expansion occurred." in readiness_text


def test_validator_passes_as_script():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_perek_4_compressed_teacher_review_packet.py")],
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
