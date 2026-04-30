from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FALLBACK_MD = ROOT / "data" / "pipeline_rounds" / "runtime_learning_intelligence_small_pool_fallback_test_2026_04_30.md"
FALLBACK_JSON = ROOT / "data" / "pipeline_rounds" / "runtime_learning_intelligence_small_pool_fallback_test_2026_04_30.json"
READINESS_MD = ROOT / "data" / "pipeline_rounds" / "runtime_learning_intelligence_v1_product_readiness_gate_2026_04_30.md"
READINESS_JSON = ROOT / "data" / "pipeline_rounds" / "runtime_learning_intelligence_v1_product_readiness_gate_2026_04_30.json"
ROADMAP = ROOT / "data" / "pipeline_rounds" / "runtime_learning_intelligence_post_fallback_product_roadmap_2026_04_30.md"
PROMPT = ROOT / "data" / "pipeline_rounds" / "prompts" / "teacher_lesson_session_setup_v1_prompt.md"
DOC = ROOT / "docs" / "runtime" / "runtime_learning_intelligence_v1.md"
SUMMARY = ROOT / "data" / "validation" / "runtime_learning_intelligence_summary.json"
REPORT = ROOT / "data" / "validation" / "runtime_learning_intelligence_report.md"

FALLBACK_EXPECTED = {
    "report_type": "manual_small_pool_fallback_test",
    "feature_name": "runtime_learning_intelligence_v1",
    "exposure_ui_feature_name": "teacher_facing_runtime_exposure_center",
    "tester": "Yossi",
    "mode": "Full Passuk view",
    "approximate_questions_answered": None,
    "approximate_questions_answered_status": "unknown_not_recorded",
    "small_pool_fallback_served_questions": True,
    "app_avoided_crash_or_blank": True,
    "runtime_exposure_center_showed_fallback_status": True,
    "repeated_targets_reduced_where_possible": True,
    "weird_skips_or_missing_questions": False,
    "slowdown_observed": False,
    "confusing_behavior_observed": False,
    "overall_judgment": "fallback_confirmed",
    "safe_to_keep_enabled": True,
    "targeted_fallback_test_still_needed": False,
    "further_student_pilot_still_useful": True,
}

READINESS_EXPECTED = {
    "readiness_status": "ready_for_continued_pilot_use",
    "keep_enabled_recommended": True,
    "fallback_confirmed": True,
    "teacher_exposure_center_available": True,
    "next_recommended_product_task": "Teacher Lesson / Session Setup V1",
}

FALSE_FIELDS = [
    "runtime_scope_widened",
    "reviewed_bank_promoted",
    "scoring_mastery_changed",
    "source_truth_changed",
    "auth_database_pii_added",
    "question_selection_logic_changed_in_this_task",
    "ui_changed_in_this_task",
]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate() -> list[str]:
    errors: list[str] = []
    required = [FALLBACK_MD, FALLBACK_JSON, READINESS_MD, READINESS_JSON, ROADMAP, PROMPT, DOC, SUMMARY, REPORT]
    for path in required:
        require(path.exists(), f"Missing required artifact: {path.relative_to(ROOT)}", errors)
    if errors:
        return errors

    try:
        fallback = load_json(FALLBACK_JSON)
        readiness = load_json(READINESS_JSON)
        summary = load_json(SUMMARY)
    except json.JSONDecodeError as error:
        return [f"JSON does not parse: {error}"]

    fallback_text = FALLBACK_MD.read_text(encoding="utf-8")
    readiness_text = READINESS_MD.read_text(encoding="utf-8")
    roadmap_text = ROADMAP.read_text(encoding="utf-8")
    prompt_text = PROMPT.read_text(encoding="utf-8")
    doc_text = DOC.read_text(encoding="utf-8")
    report_text = REPORT.read_text(encoding="utf-8")
    combined = "\n".join([fallback_text, readiness_text, roadmap_text, prompt_text, doc_text, report_text])
    lowered = combined.lower()

    for key, expected in FALLBACK_EXPECTED.items():
        require(fallback.get(key) == expected, f"fallback JSON {key} must be {expected!r}", errors)
    for key, expected in READINESS_EXPECTED.items():
        require(readiness.get(key) == expected, f"readiness JSON {key} must be {expected!r}", errors)

    for payload_name, payload in [("fallback", fallback), ("readiness", readiness)]:
        for key in FALSE_FIELDS:
            require(payload.get(key) is False, f"{payload_name} JSON {key} must be false", errors)
    require(readiness.get("perek_activated") is False, "readiness JSON perek_activated must be false", errors)

    require(summary.get("small_pool_fallback_manual_test_status") == "confirmed", "summary fallback status must be confirmed", errors)
    require(summary.get("small_pool_fallback_manual_test_date") == "2026-04-30", "summary fallback date mismatch", errors)
    require(summary.get("small_pool_fallback_served_questions") is True, "summary fallback served questions must be true", errors)
    require(summary.get("fallback_targeted_test_still_needed") is False, "summary fallback targeted test must be closed", errors)
    require(summary.get("product_readiness_status") == "ready_for_continued_pilot_use", "summary readiness mismatch", errors)
    require(summary.get("keep_enabled_recommended") is True, "summary keep-enabled recommendation must be true", errors)
    require(summary.get("teacher_lesson_session_setup_recommended_next") is True, "summary next task flag must be true", errors)
    for key in ["runtime_scope_widened", "reviewed_bank_promoted", "scoring_mastery_changed", "source_truth_changed", "pii_used", "database_used"]:
        require(summary.get(key) is False, f"summary {key} must be false", errors)

    require("approximate questions answered | unknown / not recorded" in fallback_text.lower(), "fallback report must leave approximate count unknown", errors)
    require("not a controlled student pilot" in fallback_text.lower(), "fallback report must not claim student pilot evidence", errors)
    require("fallback confirmed" in doc_text.lower(), "docs must mention fallback confirmed", errors)
    require("ready for continued pilot use" in doc_text.lower(), "docs must mention ready for continued pilot use", errors)
    require("no auth/database/pii" in doc_text.lower() or all(term in doc_text.lower() for term in ["no auth", "no database", "no pii"]), "docs must mention no auth/database/PII", errors)
    require("no perek 7 expansion yet" in roadmap_text.lower(), "roadmap must say no Perek 7 expansion yet", errors)

    prompt_lower = prompt_text.lower()
    for phrase in ["add authentication", "add a database", "add student pii", "widen active runtime scope", "change scoring/mastery"]:
        require(phrase in prompt_lower, f"future prompt must prohibit {phrase}", errors)

    forbidden = [
        "runtime_allowed=true",
        "reviewed_bank_allowed=true",
        "promoted_to_runtime",
        "approved_for_runtime",
        "runtime scope widened: yes",
        "runtime scope expansion: yes",
        "reviewed-bank promotion: yes",
        '"student_pilot_evidence": true',
        '"runtime_scope_widened": true',
        '"reviewed_bank_promoted": true',
        '"auth_database_pii_added": true',
        '"question_selection_logic_changed_in_this_task": true',
        '"ui_changed_in_this_task": true',
        '"perek_activated": true',
    ]
    for phrase in forbidden:
        require(phrase not in lowered, f"forbidden claim found: {phrase}", errors)

    fallback_json_text = FALLBACK_JSON.read_text(encoding="utf-8")
    require('"approximate_questions_answered": 15' not in fallback_json_text, "fallback JSON invents approximate count", errors)
    for phrase in [
        "approximate questions answered | 1",
        "approximate questions answered | 5",
        "approximate questions answered | 10",
        "approximate questions answered | 15",
    ]:
        require(phrase not in fallback_text.lower(), f"fallback report invents approximate count: {phrase}", errors)

    return errors


def main() -> None:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("Runtime learning intelligence product readiness validation passed.")


if __name__ == "__main__":
    main()
