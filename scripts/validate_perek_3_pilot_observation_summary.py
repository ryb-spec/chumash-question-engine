from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUMMARY_MD = ROOT / "data/pipeline_rounds/perek_3_fresh_pilot_observation_summary_2026_04_29.md"
SUMMARY_JSON = ROOT / "data/pipeline_rounds/perek_3_fresh_pilot_observation_summary_2026_04_29.json"
OBSERVATION_INTAKE = (
    ROOT / "data/gate_2_protected_preview_packets/reports/bereishis_perek_3_limited_post_preview_observation_intake.md"
)

FORBIDDEN_PATTERNS = [
    re.compile(r"\bruntime_allowed\s*=\s*true\b", re.IGNORECASE),
    re.compile(r"\bruntime_allowed\s*:\s*true\b", re.IGNORECASE),
    re.compile(r"\bperek_4_activated\s*:\s*true\b", re.IGNORECASE),
    re.compile(r"\bapproved_for_runtime\b", re.IGNORECASE),
    re.compile(r"\bpromoted_to_runtime\b", re.IGNORECASE),
    re.compile(r"\bfake student\b", re.IGNORECASE),
    re.compile(r"\bsynthetic observation\b", re.IGNORECASE),
    re.compile(r"\binvented observation\b", re.IGNORECASE),
]


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def line_is_negated_instruction(line: str) -> bool:
    lowered = line.lower()
    if "fake_data_created" in lowered and "false" in lowered:
        return True
    if "perek_4_activated" in lowered and "false" in lowered:
        return True
    negation_markers = ["do not", "does not", "did not", "no ", "not ", "never ", "without ", "must not"]
    return any(marker in lowered for marker in negation_markers)


def forbidden_claim_errors(path: Path) -> list[str]:
    errors: list[str] = []
    text = read_text(path)
    for line_number, line in enumerate(text.splitlines(), start=1):
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(line) and not line_is_negated_instruction(line):
                errors.append(f"{repo_relative(path)}:{line_number}: forbidden claim matched {pattern.pattern!r}")
    return errors


def load_summary_json(errors: list[str]) -> dict[str, Any]:
    if not SUMMARY_JSON.exists():
        errors.append(f"summary JSON missing: {repo_relative(SUMMARY_JSON)}")
        return {}
    try:
        return json.loads(SUMMARY_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"summary JSON parse failed: {exc}")
        return {}


def validate_perek_3_pilot_observation_summary() -> dict[str, Any]:
    errors: list[str] = []

    if not SUMMARY_MD.exists():
        errors.append(f"summary markdown missing: {repo_relative(SUMMARY_MD)}")
    if not OBSERVATION_INTAKE.exists():
        errors.append(f"observation intake missing: {repo_relative(OBSERVATION_INTAKE)}")

    payload = load_summary_json(errors)
    if payload:
        if payload.get("pilot_date") != "2026-04-29":
            errors.append("pilot_date must be 2026-04-29")
        if payload.get("students_observed") != 3:
            errors.append("students_observed must be 3")
        if payload.get("total_questions_answered") != 30:
            errors.append("total_questions_answered must be 30")
        if payload.get("mode") != "Learn Mode":
            errors.append("mode must be Learn Mode")
        if payload.get("no_runtime_promotion") is not True:
            errors.append("no_runtime_promotion must be true")
        if payload.get("perek_4_activated") is not False:
            errors.append("perek_4_activated must be false")
        if payload.get("fake_data_created") is not False:
            errors.append("fake_data_created must be false")
        issues = payload.get("issues")
        if not isinstance(issues, list) or len(issues) < 6:
            errors.append("issues list must contain recorded pilot issues")
        categories = {issue.get("issue_category") for issue in issues if isinstance(issue, dict)} if isinstance(issues, list) else set()
        for category in [
            "unclear wording",
            "bad distractors",
            "shoresh/source follow-up",
            "phrase-translation distractor quality",
        ]:
            if category not in categories:
                errors.append(f"issues missing category: {category}")

    if SUMMARY_MD.exists():
        summary_text = read_text(SUMMARY_MD)
        for phrase in [
            "Perek 3 fresh pilot observation summary - 2026-04-29",
            "What should be fixed first",
            "What should not be changed yet",
            "No Perek 4 activation",
        ]:
            if phrase not in summary_text:
                errors.append(f"summary markdown missing phrase: {phrase}")
        if "total questions observed: 30" not in summary_text.lower():
            errors.append("summary markdown missing phrase: total questions observed: 30")

    if OBSERVATION_INTAKE.exists():
        intake = read_text(OBSERVATION_INTAKE)
        if "Fresh Perek 3 pilot evidence recorded - 2026-04-29" not in intake:
            errors.append("observation intake missing 2026-04-29 pilot evidence section")
        if "No row is runtime-approved" not in intake:
            errors.append("observation intake must state no runtime approval")
        if "No fake observations were added" not in intake:
            errors.append("observation intake must state no fake observations")

    for path in [SUMMARY_MD, SUMMARY_JSON, OBSERVATION_INTAKE]:
        if path.exists():
            errors.extend(forbidden_claim_errors(path))

    return {
        "valid": not errors,
        "summary_markdown": repo_relative(SUMMARY_MD),
        "summary_json": repo_relative(SUMMARY_JSON),
        "observation_intake": repo_relative(OBSERVATION_INTAKE),
        "errors": errors,
    }


def main() -> int:
    summary = validate_perek_3_pilot_observation_summary()
    if summary["valid"]:
        print("Perek 3 pilot observation summary validation passed.")
        return 0
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
