"""Validate the Perek 3 pilot remediation planning artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PLAN_MD = ROOT / "data/pipeline_rounds/perek_3_pilot_remediation_plan_2026_04_29.md"
PLAN_JSON = ROOT / "data/pipeline_rounds/perek_3_pilot_remediation_plan_2026_04_29.json"
CHECKLIST_MD = ROOT / "data/pipeline_rounds/perek_3_pilot_teacher_decision_checklist_2026_04_29.md"
SEQUENCE_MD = ROOT / "data/pipeline_rounds/perek_3_pilot_remediation_sequence_2026_04_29.md"

REQUIRED_FILES = [PLAN_MD, PLAN_JSON, CHECKLIST_MD, SEQUENCE_MD]

REQUIRED_ISSUE_IDS = {
    "p3_pilot_001_form_wording",
    "p3_pilot_002_prefix_prompt_wording",
    "p3_pilot_003_ashis_shis_source_followup",
    "p3_pilot_004_derech_distractors",
    "p3_pilot_005_arurah_distractors",
    "p3_pilot_006_phrase_translation_distractor_audit",
}

REQUIRED_PLAN_PHRASES = [
    "What form is shown?",
    "בְּאִשְׁתּוֹ",
    "אָשִׁית",
    "שית",
    "דֶּרֶךְ",
    "אֲרוּרָה",
    "phrase-translation",
    "no runtime change",
    "do not activate Perek 4",
]

REQUIRED_CHECKLIST_PHRASES = ["source follow-up", "suppress", "observe again"]
REQUIRED_SEQUENCE_PHRASES = ["Phase 1", "Phase 2", "Phase 3", "re-pilot", "Perek 4 teacher-review packet"]

FORBIDDEN_PATTERNS = [
    "runtime_allowed=true",
    "runtime_allowed: true",
    "promoted_to_runtime",
    "approved_for_runtime",
    "perek_4_activated: true",
    '"perek_4_activated": true',
    "fake student",
    "invented observation",
    "synthetic observation",
]

ALLOWED_NEGATIVE_PHRASES = [
    "fake_data_created: false",
    '"fake_data_created": false',
    "do not create fake student data",
    "no fake student data",
    "do not invent student observations",
    "no runtime change",
    "do not activate perek 4",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fail(errors: list[str]) -> int:
    for error in errors:
        print(f"ERROR: {error}")
    return 1


def line_has_forbidden_claim(line: str, pattern: str) -> bool:
    lower = line.lower()
    if pattern not in lower:
        return False
    if any(allowed in lower for allowed in ALLOWED_NEGATIVE_PHRASES):
        return False
    return True


def validate() -> list[str]:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"missing required remediation artifact: {path.relative_to(ROOT)}")

    if errors:
        return errors

    try:
        data = json.loads(read_text(PLAN_JSON))
    except json.JSONDecodeError as exc:
        errors.append(f"remediation JSON does not parse: {exc}")
        return errors

    expected_booleans = {
        "no_runtime_change_in_this_task": True,
        "perek_4_activated": False,
        "runtime_scope_widened": False,
        "fake_data_created": False,
    }
    for key, expected in expected_booleans.items():
        if data.get(key) is not expected:
            errors.append(f"{PLAN_JSON.relative_to(ROOT)}: {key} must be {expected!r}")

    issue_ids = {issue.get("issue_id") for issue in data.get("remediation_issues", [])}
    missing_issue_ids = sorted(REQUIRED_ISSUE_IDS - issue_ids)
    if missing_issue_ids:
        errors.append(f"remediation JSON missing issue IDs: {missing_issue_ids}")

    plan_text = read_text(PLAN_MD)
    for phrase in REQUIRED_PLAN_PHRASES:
        if phrase not in plan_text:
            errors.append(f"plan markdown missing required phrase: {phrase}")

    checklist_text = read_text(CHECKLIST_MD).lower()
    for phrase in REQUIRED_CHECKLIST_PHRASES:
        if phrase not in checklist_text:
            errors.append(f"teacher checklist missing required phrase: {phrase}")

    sequence_text = read_text(SEQUENCE_MD)
    for phrase in REQUIRED_SEQUENCE_PHRASES:
        if phrase not in sequence_text:
            errors.append(f"remediation sequence missing required phrase: {phrase}")

    for path in REQUIRED_FILES:
        for line_number, line in enumerate(read_text(path).splitlines(), start=1):
            lower = line.lower()
            for pattern in FORBIDDEN_PATTERNS:
                if line_has_forbidden_claim(lower, pattern):
                    errors.append(
                        f"{path.relative_to(ROOT)}:{line_number}: forbidden claim found: {pattern}"
                    )

    return errors


def main() -> int:
    errors = validate()
    if errors:
        return fail(errors)
    print("Perek 3 pilot remediation plan validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
