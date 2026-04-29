"""Validate the Perek 3 pilot wording-only prompt clarity fix."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPORT = ROOT / "data/pipeline_rounds/perek_3_pilot_wording_clarity_fix_report_2026_04_29.md"
FLOW_BUILDER = ROOT / "engine/flow_builder.py"

OLD_FORM_PROMPT = "What form is shown?"
NEW_FORM_PROMPT = "What tense or verb form is this word?"
OLD_PREFIX_TEMPLATE = "What is the prefix in"
NEW_PREFIX_TEMPLATE = "which beginning letter is the prefix"

FORBIDDEN_ARTIFACT_PATTERNS = [
    "runtime_allowed=true",
    "runtime_allowed: true",
    "approved_for_runtime",
    "promoted_to_runtime",
    "perek_4_activated: true",
    '"perek_4_activated": true',
]

ALLOWED_NEGATIVE_PHRASES = [
    "no runtime scope expansion",
    "no perek 4 activation",
    "no reviewed-bank or runtime promotion",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fail(errors: list[str]) -> int:
    for error in errors:
        print(f"ERROR: {error}")
    return 1


def forbidden_claim_present(line: str, pattern: str) -> bool:
    lower = line.lower()
    if pattern not in lower:
        return False
    if any(allowed in lower for allowed in ALLOWED_NEGATIVE_PHRASES):
        return False
    return True


def validate() -> list[str]:
    errors: list[str] = []

    if not REPORT.exists():
        errors.append(f"missing wording clarity report: {REPORT.relative_to(ROOT)}")
    if not FLOW_BUILDER.exists():
        errors.append(f"missing active prompt source: {FLOW_BUILDER.relative_to(ROOT)}")
    if errors:
        return errors

    report_text = read_text(REPORT)
    required_report_phrases = [
        "No runtime scope expansion.",
        "No Perek 4 activation.",
        "No distractor changes in this task.",
        "What tense or verb form is this word?",
        "which beginning letter is the prefix",
    ]
    for phrase in required_report_phrases:
        if phrase not in report_text:
            errors.append(f"wording clarity report missing required phrase: {phrase}")

    flow_text = read_text(FLOW_BUILDER)
    if OLD_FORM_PROMPT in flow_text:
        errors.append(f"active prompt code still contains old prompt: {OLD_FORM_PROMPT}")
    if OLD_PREFIX_TEMPLATE in flow_text:
        errors.append(f"active prompt code still contains old prefix template: {OLD_PREFIX_TEMPLATE}")
    if NEW_FORM_PROMPT not in flow_text:
        errors.append(f"active prompt code missing new verb form prompt: {NEW_FORM_PROMPT}")
    if NEW_PREFIX_TEMPLATE not in flow_text:
        errors.append(f"active prompt code missing new prefix wording: {NEW_PREFIX_TEMPLATE}")

    for path in [REPORT]:
        for line_number, line in enumerate(read_text(path).splitlines(), start=1):
            lower = line.lower()
            for pattern in FORBIDDEN_ARTIFACT_PATTERNS:
                if forbidden_claim_present(lower, pattern):
                    errors.append(
                        f"{path.relative_to(ROOT)}:{line_number}: forbidden claim found: {pattern}"
                    )

    return errors


def main() -> int:
    errors = validate()
    if errors:
        return fail(errors)
    print("Perek 3 pilot wording clarity fix validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
