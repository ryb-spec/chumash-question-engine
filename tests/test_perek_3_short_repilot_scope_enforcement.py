from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts import validate_perek_3_short_repilot_scope_enforcement as validator


ROOT = Path(__file__).resolve().parents[1]


def test_enforcement_artifacts_exist():
    for path in validator.REQUIRED_FILES:
        assert path.exists(), path


def test_plan_json_safety_and_enforcement_fields():
    payload = json.loads(validator.PLAN_JSON.read_text(encoding="utf-8"))
    assert payload["runtime_scope_widened"] is False
    assert payload["perek_4_activated"] is False
    assert payload["excludes_ashis_shis"] is True
    assert payload["excludes_unverified_phrase_translation"] is True
    assert payload["enforcement_type"] == "manual"
    assert payload["runtime_enforced"] is False
    assert payload["data_enforced"] is False
    assert payload["ready_for_short_repilot"] is True
    assert payload["manual_scope_watch_required"] is True
    assert payload["fake_data_created"] is False


def test_manual_checklist_names_scope_leaks():
    text = validator.MANUAL_CHECKLIST.read_text(encoding="utf-8")
    assert "אָשִׁית" in text
    assert "שית" in text
    assert "question_type=phrase_translation" in text
    assert "Bereishis Perek 4 content" in text
    assert "does not approve runtime expansion" in text


def test_active_reviewed_questions_do_not_include_perek_4():
    summary = validator.validate()["active_reviewed_question_summary"]
    assert summary["perek_4_count"] == 0


def test_validator_passes_as_script():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_perek_3_short_repilot_scope_enforcement.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "validation passed" in result.stdout


def test_validator_function_passes():
    summary = validator.validate()
    assert summary["ok"], summary["errors"]
