from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts import validate_perek_3_short_repilot_scope_leak_fix as validator


ROOT = Path(__file__).resolve().parents[1]


def test_scope_leak_fix_artifacts_exist():
    for path in validator.REQUIRED_FILES:
        assert path.exists(), path


def test_enforcement_json_records_manual_validator_guard():
    payload = json.loads(validator.ENFORCEMENT_JSON.read_text(encoding="utf-8"))
    assert payload["runtime_scope_widened"] is False
    assert payload["perek_4_activated"] is False
    assert payload["old_prefix_wording_leak_addressed"] is True
    assert payload["stale_prefix_prompt_fixed_in_active_reviewed_bank"] is True
    assert payload["phrase_translation_leak_addressed_by_runtime_filter"] is False
    assert payload["phrase_translation_leak_guarded_by_validator"] is True
    assert payload["ready_for_clean_short_repilot"] is True
    assert payload["manual_scope_watch_required"] is True
    assert payload["reviewed_bank_runtime_promoted"] is False
    assert payload["question_selection_changed"] is False


def test_perek_4_gate_requires_clean_short_repilot():
    payload = json.loads(validator.PEREK_4_GATE_JSON.read_text(encoding="utf-8"))
    assert payload["scope_leak_fix_completed"] is True
    assert payload["clean_short_repilot_still_required"] is True
    assert payload["perek_4_teacher_review_packet_go"] is False
    assert payload["perek_4_teacher_review_packet_allowed_after_clean_short_repilot"] is True
    assert payload["perek_4_activated"] is False
    assert payload["perek_4_runtime_activation_go"] is False
    assert payload["perek_4_reviewed_bank_promotion_go"] is False


def test_active_reviewed_bank_prefix_prompt_was_repaired():
    summary = validator.validate()
    assert summary["stale_prefix_row_count"] == 0
    assert summary["baishto_row_count"] == 1
    active = json.loads(validator.ACTIVE_REVIEWED_QUESTIONS.read_text(encoding="utf-8-sig"))
    baishto_rows = [
        item
        for item in active["questions"]
        if item.get("question_type") == validator.PREFIX_QUESTION_TYPE
        and (item.get("selected_word") or item.get("word")) == validator.BAISHTO
    ]
    assert len(baishto_rows) == 1
    assert baishto_rows[0]["question"] == validator.BAISHTO_NEW_PROMPT
    assert baishto_rows[0]["question_text"] == validator.BAISHTO_NEW_PROMPT
    assert baishto_rows[0]["correct_answer"] == "ב"


def test_phrase_translation_and_ashis_exclusions_are_represented():
    report = validator.FIX_REPORT.read_text(encoding="utf-8")
    enforcement = validator.ENFORCEMENT_MD.read_text(encoding="utf-8")
    assert "phrase_translation" in report
    assert "phrase_translation" in enforcement
    assert "אָשִׁית" in report
    assert "שית" in report
    assert "Perek 4 activated: false" in enforcement


def test_validator_passes_as_script():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_perek_3_short_repilot_scope_leak_fix.py")],
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
