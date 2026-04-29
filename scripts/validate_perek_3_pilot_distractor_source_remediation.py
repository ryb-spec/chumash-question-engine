from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

AUDIT_REPORT = ROOT / "data/pipeline_rounds/perek_3_pilot_distractor_source_audit_2026_04_29.md"
PHRASE_AUDIT = ROOT / "data/pipeline_rounds/perek_3_phrase_translation_distractor_audit_2026_04_29.md"
ASHIS_FOLLOWUP = ROOT / "data/pipeline_rounds/perek_3_ashis_shis_source_followup_2026_04_29.md"
COMPLETION_GATE_MD = ROOT / "data/pipeline_rounds/perek_3_pilot_remediation_completion_gate_2026_04_29.md"
COMPLETION_GATE_JSON = ROOT / "data/pipeline_rounds/perek_3_pilot_remediation_completion_gate_2026_04_29.json"
REVIEWED_QUESTIONS = ROOT / "data/active_scope_reviewed_questions.json"

REQUIRED_FILES = (
    AUDIT_REPORT,
    PHRASE_AUDIT,
    ASHIS_FOLLOWUP,
    COMPLETION_GATE_MD,
    COMPLETION_GATE_JSON,
)

REQUIRED_TERMS = (
    "דֶּרֶךְ",
    "אֲרוּרָה",
    "אָשִׁית",
    "שית",
    "phrase_translation",
)

FORBIDDEN_PATTERNS = (
    "runtime_allowed=true",
    "runtime_allowed: true",
    "promoted_to_runtime",
    "approved_for_runtime",
    "perek_4_activated: true",
    '"perek_4_activated": true',
    "Perek 4 is activated",
    "activate Perek 4 now",
)

EXPECTED_SAFETY_VALUES = {
    "ready_for_runtime_expansion": False,
    "perek_4_activated": False,
    "runtime_scope_widened": False,
    "fake_data_created": False,
    "reviewed_bank_promoted": False,
    "question_selection_changed": False,
}


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_completion_json(errors: list[str]) -> dict:
    try:
        payload = json.loads(_read_text(COMPLETION_GATE_JSON))
    except json.JSONDecodeError as exc:
        errors.append(f"{_relative(COMPLETION_GATE_JSON)} is invalid JSON: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"{_relative(COMPLETION_GATE_JSON)} must be a JSON object")
        return {}
    return payload


def _load_reviewed_questions(errors: list[str]) -> list[dict]:
    try:
        payload = json.loads(_read_text(REVIEWED_QUESTIONS))
    except json.JSONDecodeError as exc:
        errors.append(f"{_relative(REVIEWED_QUESTIONS)} is invalid JSON: {exc}")
        return []
    questions = payload.get("questions") if isinstance(payload, dict) else None
    if not isinstance(questions, list):
        errors.append(f"{_relative(REVIEWED_QUESTIONS)} must contain a questions list")
        return []
    return [question for question in questions if isinstance(question, dict)]


def _find_question(questions: list[dict], *, pasuk_id: str, selected_word: str) -> dict | None:
    for question in questions:
        if question.get("pasuk_id") == pasuk_id and question.get("selected_word") == selected_word:
            return question
    return None


def _validate_repaired_translation_rows(errors: list[str]) -> None:
    questions = _load_reviewed_questions(errors)
    if not questions:
        return

    arurah = _find_question(questions, pasuk_id="bereishis_3_17", selected_word="אֲרוּרָה")
    if arurah is None:
        errors.append("Could not find repaired אֲרוּרָה translation row")
    else:
        if arurah.get("correct_answer") != "cursed":
            errors.append("אֲרוּרָה correct_answer must remain cursed")
        if set(arurah.get("choices", [])) != {"naked", "living", "cursed", "heel"}:
            errors.append("אֲרוּרָה choices must be the repaired evidence-backed set")
        if {"Eve", "Eden", "all"} & set(arurah.get("choices", [])):
            errors.append("אֲרוּרָה choices still include weak pilot-flagged distractors")

    derech = _find_question(questions, pasuk_id="bereishis_3_24", selected_word="דֶּרֶךְ")
    if derech is None:
        errors.append("Could not find repaired דֶּרֶךְ translation row")
    else:
        if derech.get("correct_answer") != "way":
            errors.append("דֶּרֶךְ correct_answer must remain way")
        if set(derech.get("choices", [])) != {"heel", "children", "naked", "way"}:
            errors.append("דֶּרֶךְ choices must be the repaired evidence-backed set")
        if {"Eve", "Eden", "all"} & set(derech.get("choices", [])):
            errors.append("דֶּרֶךְ choices still include weak pilot-flagged distractors")


def validate() -> dict:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required file: {_relative(path)}")

    if errors:
        return {"ok": False, "errors": errors}

    completion = _load_completion_json(errors)
    for key, expected in EXPECTED_SAFETY_VALUES.items():
        if completion.get(key) is not expected:
            errors.append(f"{_relative(COMPLETION_GATE_JSON)} must set {key} to {expected}")

    remaining = completion.get("issues_remaining")
    if not isinstance(remaining, list) or not remaining:
        errors.append("Completion JSON must keep unresolved issues_remaining populated")

    combined_text = "\n".join(_read_text(path) for path in REQUIRED_FILES if path.suffix == ".md")
    for term in REQUIRED_TERMS:
        if term not in combined_text:
            errors.append(f"Required issue term missing from remediation artifacts: {term}")

    completion_text = _read_text(COMPLETION_GATE_MD)
    if remaining and "not ready for full closure" not in completion_text:
        errors.append("Completion gate must say Perek 3 is not ready for full closure while unresolved issues remain")
    for phrase in (
        "Perek 3 is fully complete",
        "ready for full closure: yes",
        "ready_for_full_closure: true",
    ):
        if phrase in completion_text:
            errors.append(f"Completion gate contains forbidden full-completion claim: {phrase}")

    for path in REQUIRED_FILES:
        text = _read_text(path)
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in text:
                errors.append(f"{_relative(path)} contains forbidden claim: {pattern}")

    _validate_repaired_translation_rows(errors)

    return {"ok": not errors, "errors": errors}


def main() -> int:
    summary = validate()
    if not summary["ok"]:
        for error in summary["errors"]:
            print(f"ERROR: {error}")
        return 1
    print("Perek 3 pilot distractor/source remediation validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
