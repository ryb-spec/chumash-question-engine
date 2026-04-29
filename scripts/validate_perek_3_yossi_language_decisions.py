from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DECISIONS_MD = ROOT / "data/pipeline_rounds/perek_3_yossi_language_decisions_2026_04_29.md"
DECISIONS_JSON = ROOT / "data/pipeline_rounds/perek_3_yossi_language_decisions_2026_04_29.json"
SCOPE_MD = ROOT / "data/pipeline_rounds/perek_3_short_repilot_scope_2026_04_29.md"
SCOPE_JSON = ROOT / "data/pipeline_rounds/perek_3_short_repilot_scope_2026_04_29.json"
COMPLETION_GATE_MD = ROOT / "data/pipeline_rounds/perek_3_pilot_remediation_completion_gate_2026_04_29.md"
COMPLETION_GATE_JSON = ROOT / "data/pipeline_rounds/perek_3_pilot_remediation_completion_gate_2026_04_29.json"

REQUIRED_FILES = (
    DECISIONS_MD,
    DECISIONS_JSON,
    SCOPE_MD,
    SCOPE_JSON,
    COMPLETION_GATE_MD,
    COMPLETION_GATE_JSON,
)

REQUIRED_DECISION_PHRASES = (
    "This does not mean `שית` is wrong.",
    "`אָשִׁית` / `שית` is not appropriate as a normal beginner shoresh-identification question without explicit teaching/explanation.",
    "Phrase-translation distractors must test the whole phrase.",
)

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


def validate() -> dict:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required file: {_relative(path)}")

    if errors:
        return {"ok": False, "errors": errors}

    decisions = _load_json(DECISIONS_JSON, errors)
    scope = _load_json(SCOPE_JSON, errors)
    completion = _load_json(COMPLETION_GATE_JSON, errors)

    decision_text = _read_text(DECISIONS_MD)
    scope_text = _read_text(SCOPE_MD)
    completion_text = _read_text(COMPLETION_GATE_MD)
    combined_text = "\n".join(_read_text(path) for path in REQUIRED_FILES)

    for phrase in REQUIRED_DECISION_PHRASES:
        if phrase not in decision_text:
            errors.append(f"Missing required decision phrase: {phrase}")

    ashis = decisions.get("ashis_shis_decision", {})
    if not isinstance(ashis, dict):
        errors.append("ashis_shis_decision must be an object")
        ashis = {}
    if ashis.get("suppress_or_quarantine_for_short_repilot") is not True:
        errors.append("ashis_shis_decision must suppress/quarantine for short re-pilot")
    if ashis.get("source_truth_changed") is not False:
        errors.append("ashis_shis_decision.source_truth_changed must be false")
    if ashis.get("approved") is not False:
        errors.append("ashis_shis_decision.approved must be false")
    if ashis.get("beginner_shoresh_ready") is not False:
        errors.append("ashis_shis_decision.beginner_shoresh_ready must be false")
    if ashis.get("teacher_follow_up_required") is not True:
        errors.append("ashis_shis_decision.teacher_follow_up_required must be true")

    phrase = decisions.get("phrase_translation_decision", {})
    if not isinstance(phrase, dict):
        errors.append("phrase_translation_decision must be an object")
        phrase = {}
    if phrase.get("whole_phrase_distractor_policy") is not True:
        errors.append("phrase_translation_decision.whole_phrase_distractor_policy must be true")
    if phrase.get("broad_logic_change_now") is not False:
        errors.append("phrase_translation_decision.broad_logic_change_now must be false")
    if phrase.get("item_level_audit_required_for_full_closure") is not True:
        errors.append("phrase_translation_decision.item_level_audit_required_for_full_closure must be true")
    if phrase.get("exclude_unverified_items_from_short_repilot") is not True:
        errors.append("phrase_translation_decision.exclude_unverified_items_from_short_repilot must be true")

    if decisions.get("full_perek_3_closure_allowed_now") is not False:
        errors.append("full_perek_3_closure_allowed_now must be false")
    if decisions.get("runtime_expansion_allowed_now") is not False:
        errors.append("runtime_expansion_allowed_now must be false")
    if decisions.get("perek_4_activation_allowed_now") is not False:
        errors.append("perek_4_activation_allowed_now must be false")
    if decisions.get("fake_data_created") is not False:
        errors.append("fake_data_created must be false")

    exclude_targets = scope.get("exclude_targets", [])
    exclude_text = "\n".join(str(item) for item in exclude_targets)
    if "אָשִׁית" not in exclude_text or "שית" not in exclude_text:
        errors.append("short re-pilot scope must exclude אָשִׁית / שית")
    if "phrase_translation" not in exclude_text:
        errors.append("short re-pilot scope must exclude unverified phrase_translation")
    if "Perek 4" not in exclude_text:
        errors.append("short re-pilot scope must exclude Perek 4")
    if scope.get("perek_4_activated") is not False:
        errors.append("scope perek_4_activated must be false")
    if scope.get("runtime_scope_widened") is not False:
        errors.append("scope runtime_scope_widened must be false")
    if scope.get("full_closure_allowed") is not False:
        errors.append("scope full_closure_allowed must be false")
    if scope.get("short_repilot_ready") is not True:
        errors.append("scope short_repilot_ready must be true")

    if completion.get("ready_for_short_repilot") is True:
        if completion.get("ready_for_full_closure") is not False:
            errors.append("completion gate ready_for_full_closure must be false when short re-pilot is true")
        if completion.get("ready_for_runtime_expansion") is not False:
            errors.append("completion gate ready_for_runtime_expansion must be false")
    if completion.get("perek_4_activated") is not False:
        errors.append("completion gate perek_4_activated must be false")
    if "not ready for full closure" not in completion_text:
        errors.append("completion gate must state Perek 3 is not ready for full closure")
    if "ready for a short re-pilot only with exclusions" not in completion_text:
        errors.append("completion gate must state short re-pilot readiness is only with exclusions")

    for required in ("אָשִׁית", "שית", "phrase_translation", "Perek 4"):
        if required not in scope_text:
            errors.append(f"short re-pilot scope missing required exclusion term: {required}")

    for path in REQUIRED_FILES:
        text = _read_text(path)
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in text:
                errors.append(f"{_relative(path)} contains forbidden claim: {pattern}")

    return {"ok": not errors, "errors": errors}


def main() -> int:
    summary = validate()
    if not summary["ok"]:
        for error in summary["errors"]:
            print(f"ERROR: {error}")
        return 1
    print("Perek 3 Yossi language decisions validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
