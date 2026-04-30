from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "data" / "pipeline_rounds" / "teacher_facing_runtime_exposure_center_2026_04_30.md"
JSON_PATH = ROOT / "data" / "pipeline_rounds" / "teacher_facing_runtime_exposure_center_2026_04_30.json"
FALLBACK_PLAN_PATH = ROOT / "data" / "pipeline_rounds" / "runtime_learning_intelligence_fallback_test_plan_2026_04_30.md"
DOC_PATH = ROOT / "docs" / "runtime" / "runtime_learning_intelligence_v1.md"
SUMMARY_HELPER_PATH = ROOT / "runtime" / "exposure_summary.py"
UI_HELPER_PATH = ROOT / "ui" / "runtime_exposure_summary.py"
APP_PATH = ROOT / "streamlit_app.py"


FALSE_FIELDS = [
    "uses_database",
    "uses_auth",
    "uses_pii",
    "exposes_raw_logs",
    "changes_question_selection_weighting",
    "changes_scoring_mastery",
    "changes_content_scope",
    "runtime_scope_widened",
    "perek_activated",
    "reviewed_bank_promoted",
    "student_facing_content_created",
]


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require(condition, message, errors):
    if not condition:
        errors.append(message)


def validate():
    errors = []
    required_paths = [
        REPORT_PATH,
        JSON_PATH,
        FALLBACK_PLAN_PATH,
        DOC_PATH,
        SUMMARY_HELPER_PATH,
        UI_HELPER_PATH,
        APP_PATH,
    ]
    for path in required_paths:
        require(path.exists(), f"Missing required artifact: {path.relative_to(ROOT)}", errors)
    if errors:
        return errors

    try:
        payload = load_json(JSON_PATH)
    except json.JSONDecodeError as error:
        return [f"Implementation JSON does not parse: {error}"]

    report_text = REPORT_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")
    helper_text = SUMMARY_HELPER_PATH.read_text(encoding="utf-8")
    ui_text = UI_HELPER_PATH.read_text(encoding="utf-8")
    app_text = APP_PATH.read_text(encoding="utf-8")
    fallback_text = FALLBACK_PLAN_PATH.read_text(encoding="utf-8")
    combined = "\n".join([report_text, doc_text, helper_text, ui_text, app_text, fallback_text])
    lowered = combined.lower()

    require(payload.get("feature_name") == "teacher_facing_runtime_exposure_center", "feature_name mismatch", errors)
    require(payload.get("ui_added") is True, "ui_added must be true", errors)
    require(payload.get("uses_local_attempt_history") is True, "uses_local_attempt_history must be true", errors)
    require(payload.get("fallback_targeted_test_still_needed") is True, "fallback test must still be needed", errors)
    require(payload.get("handles_missing_logs") is True, "missing logs must be handled", errors)
    require(payload.get("handles_malformed_logs") is True, "malformed logs must be handled", errors)
    require(payload.get("safe_ui_fallback") is True, "safe UI fallback must be true", errors)
    for key in FALSE_FIELDS:
        require(payload.get(key) is False, f"{key} must be false", errors)

    require("runtime exposure center" in app_text.lower() or "runtime exposure center" in ui_text.lower(), "UI integration must include Runtime Exposure Center language", errors)
    require("render_runtime_exposure_center" in app_text, "app must call the exposure center renderer", errors)
    require("build_runtime_exposure_summary_from_default_logs" in app_text, "app must build summary from local logs", errors)

    require("no login" in doc_text.lower(), "docs must mention no login", errors)
    require("no database" in doc_text.lower(), "docs must mention no database", errors)
    require("no pii" in doc_text.lower(), "docs must mention no PII", errors)
    require("fallback" in doc_text.lower(), "docs must mention fallback limitation", errors)
    require("small-pool fallback still needs focused confirmation" in doc_text.lower(), "docs must preserve fallback limitation", errors)

    forbidden = [
        "runtime_allowed=true",
        "reviewed_bank_allowed=true",
        "promoted_to_runtime",
        "approved_for_runtime",
        "runtime scope widened: yes",
        "runtime scope expansion: yes",
        "perek activated: yes",
        "perek_5_activated: true",
        "perek_6_activated: true",
        '"perek_activated": true',
        '"uses_database": true',
        '"uses_auth": true',
        '"uses_pii": true',
        '"exposes_raw_logs": true',
    ]
    for phrase in forbidden:
        require(phrase not in lowered, f"forbidden phrase found: {phrase}", errors)

    raw_log_exposure_markers = [
        "st.json(record",
        "st.write(record",
        "st.code(line",
        "st.text(line",
        "st.write(line",
    ]
    for phrase in raw_log_exposure_markers:
        require(phrase not in lowered, f"raw log exposure marker found: {phrase}", errors)

    return errors


def main():
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("Teacher-facing runtime exposure center validation passed.")


if __name__ == "__main__":
    main()
