from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts import validate_perek_3_yossi_language_decisions as validator


ROOT = Path(__file__).resolve().parents[1]


def test_required_language_decision_artifacts_exist():
    for path in validator.REQUIRED_FILES:
        assert path.exists(), path


def test_language_decision_json_safety_fields():
    payload = json.loads(validator.DECISIONS_JSON.read_text(encoding="utf-8"))
    assert payload["ashis_shis_decision"]["suppress_or_quarantine_for_short_repilot"] is True
    assert payload["ashis_shis_decision"]["source_truth_changed"] is False
    assert payload["ashis_shis_decision"]["approved"] is False
    assert payload["ashis_shis_decision"]["beginner_shoresh_ready"] is False
    assert payload["phrase_translation_decision"]["whole_phrase_distractor_policy"] is True
    assert payload["phrase_translation_decision"]["broad_logic_change_now"] is False
    assert payload["full_perek_3_closure_allowed_now"] is False
    assert payload["runtime_expansion_allowed_now"] is False
    assert payload["perek_4_activation_allowed_now"] is False
    assert payload["fake_data_created"] is False


def test_short_repilot_scope_excludes_unresolved_lanes():
    payload = json.loads(validator.SCOPE_JSON.read_text(encoding="utf-8"))
    exclusions = "\n".join(payload["exclude_targets"])
    assert "אָשִׁית" in exclusions
    assert "שית" in exclusions
    assert "phrase_translation" in exclusions
    assert "Perek 4" in exclusions
    assert payload["short_repilot_ready"] is True
    assert payload["full_closure_allowed"] is False
    assert payload["perek_4_activated"] is False
    assert payload["runtime_scope_widened"] is False


def test_completion_gate_keeps_full_closure_and_runtime_blocked():
    payload = json.loads(validator.COMPLETION_GATE_JSON.read_text(encoding="utf-8"))
    assert payload["ready_for_short_repilot"] is True
    assert payload["ready_for_full_closure"] is False
    assert payload["ready_for_runtime_expansion"] is False
    assert payload["perek_4_activated"] is False
    assert payload["full_closure_blockers"]


def test_required_hebrew_and_policy_phrases_present():
    text = validator.DECISIONS_MD.read_text(encoding="utf-8")
    assert "This does not mean `שית` is wrong." in text
    assert "אָשִׁית" in text
    assert "שית" in text
    assert "Phrase-translation distractors must test the whole phrase." in text


def test_validator_passes_as_script():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_perek_3_yossi_language_decisions.py")],
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
