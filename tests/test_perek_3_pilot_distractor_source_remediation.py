from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts import validate_perek_3_pilot_distractor_source_remediation as validator


ROOT = Path(__file__).resolve().parents[1]


def test_remediation_artifacts_exist():
    for path in validator.REQUIRED_FILES:
        assert path.exists(), path


def test_completion_json_safety_booleans():
    payload = json.loads(validator.COMPLETION_GATE_JSON.read_text(encoding="utf-8"))
    assert payload["ready_for_runtime_expansion"] is False
    assert payload["perek_4_activated"] is False
    assert payload["runtime_scope_widened"] is False
    assert payload["fake_data_created"] is False
    assert payload["reviewed_bank_promoted"] is False
    assert payload["question_selection_changed"] is False
    assert payload["source_truth_changed"] is False
    assert payload["distractor_logic_changed"] is False
    assert payload["data_level_distractor_choices_changed"] is True
    assert payload["issues_remaining"]


def test_required_issue_terms_are_represented():
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in validator.REQUIRED_FILES
        if path.suffix == ".md"
    )
    for term in validator.REQUIRED_TERMS:
        assert term in combined


def test_repaired_translation_distractors_are_targeted_and_source_answers_preserved():
    payload = json.loads(validator.REVIEWED_QUESTIONS.read_text(encoding="utf-8"))
    questions = payload["questions"]

    arurah = next(
        question
        for question in questions
        if question.get("pasuk_id") == "bereishis_3_17"
        and question.get("selected_word") == "אֲרוּרָה"
    )
    assert arurah["correct_answer"] == "cursed"
    assert set(arurah["choices"]) == {"naked", "living", "cursed", "heel"}
    assert not ({"Eve", "Eden", "all"} & set(arurah["choices"]))

    derech = next(
        question
        for question in questions
        if question.get("pasuk_id") == "bereishis_3_24"
        and question.get("selected_word") == "דֶּרֶךְ"
    )
    assert derech["correct_answer"] == "way"
    assert set(derech["choices"]) == {"heel", "children", "naked", "way"}
    assert not ({"Eve", "Eden", "all"} & set(derech["choices"]))


def test_validator_passes_as_script():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_perek_3_pilot_distractor_source_remediation.py")],
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
