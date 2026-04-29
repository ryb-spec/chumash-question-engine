from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

RUNBOOK = ROOT / "docs/pilots/perek_3_fresh_pilot_runbook.md"
RUBRIC = ROOT / "docs/review/question_quality_rubric.md"
OBSERVATION_INTAKE = (
    ROOT
    / "data/gate_2_protected_preview_packets/reports/bereishis_perek_3_limited_post_preview_observation_intake.md"
)
PRODUCT_BRIEF = ROOT / "docs/product/bhh_chumash_ai_pilot_one_page_brief.md"
ACTION_PLAN = ROOT / "data/pipeline_rounds/claude_review_action_plan_2026_04_29.md"
HYGIENE_INVENTORY = ROOT / "data/pipeline_rounds/repo_hygiene_inventory_2026_04_29.md"
MANIFEST = ROOT / "data/pipeline_rounds/perek_3_pilot_evidence_manifest_2026_04_29.json"

REQUIRED_FILES = [
    RUNBOOK,
    RUBRIC,
    PRODUCT_BRIEF,
    ACTION_PLAN,
    HYGIENE_INVENTORY,
    MANIFEST,
]

PILOT_EVIDENCE_ARTIFACTS = [
    RUNBOOK,
    RUBRIC,
    OBSERVATION_INTAKE,
    PRODUCT_BRIEF,
    ACTION_PLAN,
    HYGIENE_INVENTORY,
    MANIFEST,
    ROOT / "docs/README.md",
    ROOT / "scripts/README.md",
    ROOT / "data/pipeline_rounds/README.md",
]

RUBRIC_CATEGORIES = [
    "clear_keep",
    "clear_minor_wording_improvement",
    "unclear_revise",
    "wrong_answer_or_bad_distractor_reject",
    "source_issue_follow_up",
    "student_confusion_but_question_valid_teacher_note",
    "insufficient_evidence_observe_again",
]

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


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def line_is_negated_instruction(line: str) -> bool:
    lowered = line.lower()
    if "fake_data_created" in lowered and "false" in lowered:
        return True
    negation_markers = [
        "do not",
        "does not",
        "did not",
        "no ",
        "not ",
        "never ",
        "without ",
        "must not",
    ]
    return any(marker in lowered for marker in negation_markers)


def forbidden_claim_errors(path: Path) -> list[str]:
    errors: list[str] = []
    text = read_text(path)
    for line_number, line in enumerate(text.splitlines(), start=1):
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(line) and not line_is_negated_instruction(line):
                errors.append(f"{repo_relative(path)}:{line_number}: forbidden claim matched {pattern.pattern!r}")
    return errors


def active_runtime_scope_errors() -> list[str]:
    manifest_path = ROOT / "data/corpus_manifest.json"
    if not manifest_path.exists():
        return ["data/corpus_manifest.json is missing; cannot confirm active runtime scope"]
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    for scope in payload.get("scopes", []):
        if scope.get("status") == "active" or scope.get("supported_runtime") is True:
            end_perek = ((scope.get("range") or {}).get("end") or {}).get("perek")
            if isinstance(end_perek, int) and end_perek >= 4:
                errors.append(
                    f"active runtime scope {scope.get('scope_id', 'unknown')} appears to include Perek {end_perek}"
                )
    return errors


def validate_perek_3_pilot_evidence_pack() -> dict[str, Any]:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"required file missing: {repo_relative(path)}")

    if not OBSERVATION_INTAKE.exists():
        errors.append(f"observation intake missing: {repo_relative(OBSERVATION_INTAKE)}")

    if RUNBOOK.exists():
        text = read_text(RUNBOOK)
        if "Learn Mode" not in text:
            errors.append("runbook must contain Learn Mode")
        if "3–5 students" not in text and "3-5 students" not in text:
            errors.append("runbook must contain 3-5 students")
        if "8–10 questions" not in text and "8-10 questions" not in text:
            errors.append("runbook must contain 8-10 questions")
        if "does not approve runtime expansion" not in text:
            errors.append("runbook must warn no runtime expansion approval")
        if "does not activate Perek 4" not in text:
            errors.append("runbook must warn not to activate Perek 4")

    if RUBRIC.exists():
        text = read_text(RUBRIC)
        for category in RUBRIC_CATEGORIES:
            if category not in text:
                errors.append(f"rubric missing category: {category}")
        if "Promotion rule" not in text:
            errors.append("rubric missing Promotion rule section")

    if PRODUCT_BRIEF.exists():
        text = read_text(PRODUCT_BRIEF)
        if "What it does not yet do" not in text:
            errors.append("product brief must say what the app does not yet do")
        if "not ready for schoolwide rollout" not in text:
            errors.append("product brief must avoid schoolwide-rollout overclaim")

    if ACTION_PLAN.exists():
        text = read_text(ACTION_PLAN)
        for phrase in [
            "Do not refactor engine/flow_builder.py",
            "Do not activate Perek 4",
            "does not change runtime behavior",
        ]:
            if phrase not in text:
                errors.append(f"action plan missing phrase: {phrase}")

    if HYGIENE_INVENTORY.exists():
        text = read_text(HYGIENE_INVENTORY).strip()
        if len(text) < 200:
            errors.append("hygiene inventory exists but appears too short")

    manifest: dict[str, Any] = {}
    if MANIFEST.exists():
        try:
            manifest = load_manifest()
        except json.JSONDecodeError as exc:
            errors.append(f"manifest JSON parse failed: {exc}")
        else:
            if manifest.get("no_runtime_behavior_changed") is not True:
                errors.append("manifest no_runtime_behavior_changed must be true")
            if manifest.get("perek_4_activated") is not False:
                errors.append("manifest perek_4_activated must be false")
            if manifest.get("fake_data_created") is not False:
                errors.append("manifest fake_data_created must be false")

    if OBSERVATION_INTAKE.exists():
        intake = read_text(OBSERVATION_INTAKE)
        if "Reviewer Instructions — Real Evidence Only" not in intake:
            errors.append("observation intake missing real-evidence reviewer instructions")
        has_blank_intake_notice = "No observed rows have been recorded" in intake
        has_recorded_evidence_notice = "Fresh Perek 3 pilot evidence recorded - 2026-04-29" in intake
        if not (has_blank_intake_notice or has_recorded_evidence_notice):
            errors.append("observation intake must state either blank-intake status or recorded fresh-pilot evidence")
        if "g2ppcand_p3_004" in intake and "blocked" not in intake.lower():
            errors.append("observation intake mentions g2ppcand_p3_004 without blocked status")

    for path in PILOT_EVIDENCE_ARTIFACTS:
        if path.exists():
            errors.extend(forbidden_claim_errors(path))

    errors.extend(active_runtime_scope_errors())

    return {
        "valid": not errors,
        "required_files": [repo_relative(path) for path in REQUIRED_FILES],
        "observation_intake": repo_relative(OBSERVATION_INTAKE),
        "manifest_branch": manifest.get("branch_name") if manifest else None,
        "errors": errors,
    }


def main() -> int:
    summary = validate_perek_3_pilot_evidence_pack()
    if summary["valid"]:
        print("Perek 3 pilot evidence pack validation passed.")
        return 0
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
