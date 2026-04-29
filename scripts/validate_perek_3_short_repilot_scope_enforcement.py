from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PLAN_MD = ROOT / "data/pipeline_rounds/perek_3_short_repilot_enforcement_plan_2026_04_29.md"
PLAN_JSON = ROOT / "data/pipeline_rounds/perek_3_short_repilot_enforcement_plan_2026_04_29.json"
MANUAL_CHECKLIST = ROOT / "data/pipeline_rounds/perek_3_short_repilot_manual_checklist_2026_04_29.md"
ACTIVE_REVIEWED_QUESTIONS = ROOT / "data/active_scope_reviewed_questions.json"

REQUIRED_FILES = (PLAN_MD, PLAN_JSON, MANUAL_CHECKLIST)

FORBIDDEN_PATTERNS = (
    "runtime_allowed=true",
    "runtime_allowed: true",
    "approved_for_runtime",
    "promoted_to_runtime",
    '"perek_4_activated": true',
    "Perek 4 is active",
    "Perek 4 is activated",
    "activate Perek 4 now",
    "invented observation",
    "synthetic observation",
)


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path, errors: list[str]) -> dict:
    try:
        payload = json.loads(_read_text(path))
    except json.JSONDecodeError as exc:
        errors.append(f"{_relative(path)} is invalid JSON: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"{_relative(path)} must be a JSON object")
        return {}
    return payload


def _active_reviewed_question_summary(errors: list[str]) -> dict:
    payload = _load_json(ACTIVE_REVIEWED_QUESTIONS, errors)
    questions = payload.get("questions", []) if isinstance(payload, dict) else []
    if not isinstance(questions, list):
        errors.append("data/active_scope_reviewed_questions.json must contain a questions list")
        return {"perek_4_count": 0, "perek_3_phrase_translation_count": 0}
    perek_4_count = 0
    perek_3_phrase_translation_count = 0
    for question in questions:
        if not isinstance(question, dict):
            continue
        pasuk_id = str(question.get("pasuk_id", ""))
        if pasuk_id.startswith("bereishis_4_"):
            perek_4_count += 1
        if pasuk_id.startswith("bereishis_3_") and question.get("question_type") == "phrase_translation":
            perek_3_phrase_translation_count += 1
    return {
        "perek_4_count": perek_4_count,
        "perek_3_phrase_translation_count": perek_3_phrase_translation_count,
    }


def validate() -> dict:
    errors: list[str] = []
    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required file: {_relative(path)}")
    if errors:
        return {"ok": False, "errors": errors}

    plan = _load_json(PLAN_JSON, errors)
    active_summary = _active_reviewed_question_summary(errors)

    if plan.get("runtime_scope_widened") is not False:
        errors.append("runtime_scope_widened must be false")
    if plan.get("perek_4_activated") is not False:
        errors.append("perek_4_activated must be false")
    if plan.get("excludes_ashis_shis") is not True:
        errors.append("excludes_ashis_shis must be true")
    if plan.get("excludes_unverified_phrase_translation") is not True:
        errors.append("excludes_unverified_phrase_translation must be true")
    if plan.get("enforcement_type") not in {"runtime", "data", "manual"}:
        errors.append("enforcement_type must be one of runtime, data, manual")
    if plan.get("ready_for_short_repilot") not in {True, False}:
        errors.append("ready_for_short_repilot must be explicit true/false")
    if plan.get("manual_scope_watch_required") not in {True, False}:
        errors.append("manual_scope_watch_required must be explicit true/false")
    if plan.get("enforcement_type") == "manual":
        if plan.get("runtime_enforced") is not False:
            errors.append("manual enforcement must set runtime_enforced=false")
        if plan.get("data_enforced") is not False:
            errors.append("manual enforcement must set data_enforced=false")
        if plan.get("manual_scope_watch_required") is not True:
            errors.append("manual enforcement must require manual_scope_watch_required=true")
        if plan.get("manual_checklist_path") != _relative(MANUAL_CHECKLIST):
            errors.append("manual enforcement must point to the manual checklist")

    if active_summary["perek_4_count"] != 0:
        errors.append("active reviewed question bank must not contain Bereishis Perek 4 rows")

    plan_text = _read_text(PLAN_MD)
    checklist_text = _read_text(MANUAL_CHECKLIST)
    for required in (
        "Enforcement type: `manual`.",
        "`אָשִׁית` / `שית`",
        "`phrase_translation`",
        "Perek 4",
        "manual scope watch",
        "scope leak",
    ):
        if required not in plan_text:
            errors.append(f"enforcement plan missing required phrase: {required}")
    for required in (
        "`אָשִׁית` / `שית`",
        "`question_type=phrase_translation`",
        "Bereishis Perek 4 content",
        "does not approve runtime expansion",
    ):
        if required not in checklist_text:
            errors.append(f"manual checklist missing required phrase: {required}")

    for path in REQUIRED_FILES:
        text = _read_text(path)
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in text:
                errors.append(f"{_relative(path)} contains forbidden claim: {pattern}")

    return {
        "ok": not errors,
        "errors": errors,
        "active_reviewed_question_summary": active_summary,
    }


def main() -> int:
    summary = validate()
    if not summary["ok"]:
        for error in summary["errors"]:
            print(f"ERROR: {error}")
        return 1
    print("Perek 3 short re-pilot scope enforcement validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
