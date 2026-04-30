from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "data" / "pipeline_rounds" / "runtime_learning_intelligence_policy_2026_04_30.json"
AUDIT_PATH = ROOT / "data" / "pipeline_rounds" / "runtime_learning_intelligence_audit_2026_04_30.md"
REPORT_PATH = ROOT / "data" / "validation" / "runtime_learning_intelligence_report.md"
SUMMARY_PATH = ROOT / "data" / "validation" / "runtime_learning_intelligence_summary.json"
DOC_PATH = ROOT / "docs" / "runtime" / "runtime_learning_intelligence_v1.md"
MODULE_PATHS = [
    ROOT / "runtime" / "attempt_history.py",
    ROOT / "runtime" / "question_identity.py",
    ROOT / "runtime" / "scope_exhaustion.py",
]


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require(condition, message, errors):
    if not condition:
        errors.append(message)


def assert_false(payload, key, errors):
    require(payload.get(key) is False, f"{key} must be false", errors)


def validate():
    errors = []
    for path in [POLICY_PATH, AUDIT_PATH, REPORT_PATH, SUMMARY_PATH, DOC_PATH, *MODULE_PATHS]:
        require(path.exists(), f"Missing required artifact: {path.relative_to(ROOT)}", errors)
    if errors:
        return errors

    policy = load_json(POLICY_PATH)
    summary = load_json(SUMMARY_PATH)
    report_text = REPORT_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")
    artifact_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [AUDIT_PATH, REPORT_PATH, DOC_PATH]
    )

    require(policy.get("uses_attempt_history") is True, "policy must use attempt history", errors)
    require(policy.get("uses_cross_session_history") is True, "policy must use cross-session history", errors)
    assert_false(policy, "uses_student_auth", errors)
    assert_false(policy, "uses_database", errors)
    assert_false(policy, "uses_pii", errors)
    require(
        policy.get("changes_question_selection_weighting") is True,
        "policy must change question-selection weighting",
        errors,
    )
    assert_false(policy, "changes_scoring_mastery", errors)
    assert_false(policy, "changes_content_scope", errors)
    assert_false(policy, "activates_new_perek", errors)
    require(
        policy.get("fallback_allowed_when_scope_small") is True,
        "fallback must be allowed when scope is small",
        errors,
    )

    safety = policy.get("safety_fields", {})
    for key in [
        "runtime_scope_widened",
        "reviewed_bank_promoted",
        "student_facing_content_created",
        "source_truth_changed",
        "scoring_mastery_changed",
    ]:
        require(safety.get(key) is False, f"policy safety field {key} must be false", errors)

    for key in [
        "runtime_scope_widened",
        "reviewed_bank_promoted",
        "scoring_mastery_changed",
        "source_truth_changed",
        "pii_used",
        "database_used",
    ]:
        assert_false(summary, key, errors)

    require("fallback" in doc_text.lower(), "runtime docs must mention fallback behavior", errors)
    require("no auth" in doc_text.lower(), "runtime docs must mention no auth", errors)
    require("no database" in doc_text.lower(), "runtime docs must mention no database", errors)
    require("no pii" in doc_text.lower(), "runtime docs must mention no PII", errors)

    lowered = artifact_text.lower()
    forbidden = [
        "runtime_allowed=true",
        "reviewed_bank_allowed=true",
        "promoted_to_runtime",
        "approved_for_runtime",
        "perek_5_activated: true",
        "perek_6_activated: true",
        '"perek_5_activated": true',
        '"perek_6_activated": true',
    ]
    for phrase in forbidden:
        require(phrase not in lowered, f"forbidden runtime/scope phrase found: {phrase}", errors)

    return errors


def main():
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("Runtime learning intelligence validation passed.")


if __name__ == "__main__":
    main()
