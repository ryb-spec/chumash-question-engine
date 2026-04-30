from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "data" / "pipeline_rounds" / "runtime_learning_intelligence_manual_smoke_test_2026_04_30.md"
JSON_PATH = ROOT / "data" / "pipeline_rounds" / "runtime_learning_intelligence_manual_smoke_test_2026_04_30.json"
RECOMMENDATION_PATH = ROOT / "data" / "pipeline_rounds" / "runtime_learning_intelligence_next_step_recommendation_2026_04_30.md"


EXPECTED_VALUES = {
    "report_type": "manual_smoke_test",
    "feature_name": "runtime_learning_intelligence_v1",
    "tester": "Yossi",
    "mode": "Full Passuk view",
    "approximate_questions_answered": 15,
    "repeated_questions_decreased": True,
    "repeated_hebrew_targets_decreased": True,
    "small_pool_fallback_served_questions": None,
    "small_pool_fallback_status": "unknown_not_determined",
    "weird_skips_or_missing_questions": False,
    "slowdown_observed": False,
    "confusing_behavior_observed": False,
    "overall_judgment": "clean_enough",
    "safe_to_keep_enabled": True,
    "targeted_fallback_test_still_needed": True,
}

SAFETY_FALSE_FIELDS = [
    "runtime_scope_widened",
    "reviewed_bank_promoted",
    "scoring_mastery_changed",
    "source_truth_changed",
    "auth_database_pii_added",
]


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require(condition, message, errors):
    if not condition:
        errors.append(message)


def validate():
    errors = []
    for path in [REPORT_PATH, JSON_PATH, RECOMMENDATION_PATH]:
        require(path.exists(), f"Missing required artifact: {path.relative_to(ROOT)}", errors)
    if errors:
        return errors

    try:
        payload = load_json(JSON_PATH)
    except json.JSONDecodeError as error:
        return [f"Smoke test JSON does not parse: {error}"]

    report_text = REPORT_PATH.read_text(encoding="utf-8")
    recommendation_text = RECOMMENDATION_PATH.read_text(encoding="utf-8")
    combined_text = f"{report_text}\n{recommendation_text}"
    lowered = combined_text.lower()

    for key, expected in EXPECTED_VALUES.items():
        require(payload.get(key) == expected, f"{key} must be {expected!r}", errors)

    for key in SAFETY_FALSE_FIELDS:
        require(payload.get(key) is False, f"{key} must be false", errors)

    require(
        "unknown / not determined" in lowered,
        "report must record small-pool fallback as unknown / not determined",
        errors,
    )
    forbidden_fallback_claims = [
        "small-pool fallback served questions | yes",
        "small-pool fallback served questions | no",
        "small pool fallback served questions | yes",
        "small pool fallback served questions | no",
        "small-pool fallback answer was yes",
        "small-pool fallback answer was no",
        "small pool fallback answer was yes",
        "small pool fallback answer was no",
    ]
    for phrase in forbidden_fallback_claims:
        require(phrase not in lowered, f"report invents fallback answer: {phrase}", errors)

    require(
        payload.get("student_pilot_evidence") is False,
        "student_pilot_evidence must be false",
        errors,
    )
    require(
        "not a controlled student pilot" in lowered,
        "report must not claim controlled student pilot evidence",
        errors,
    )

    forbidden_runtime_claims = [
        "runtime_allowed=true",
        "reviewed_bank_allowed=true",
        "promoted_to_runtime",
        "approved_for_runtime",
        '"runtime_scope_widened": true',
        "runtime scope widened: yes",
        "runtime scope expanded: yes",
        "reviewed-bank promotion: yes",
    ]
    for phrase in forbidden_runtime_claims:
        require(phrase not in lowered, f"forbidden runtime/reviewed-bank claim found: {phrase}", errors)

    return errors


def main():
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("Runtime learning intelligence smoke test validation passed.")


if __name__ == "__main__":
    main()
