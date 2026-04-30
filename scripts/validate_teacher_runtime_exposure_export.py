from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "data" / "pipeline_rounds" / "teacher_runtime_exposure_export_report_2026_04_30.md"
JSON_PATH = ROOT / "data" / "pipeline_rounds" / "teacher_runtime_exposure_export_report_2026_04_30.json"
RUNTIME_HELPER_PATH = ROOT / "runtime" / "teacher_runtime_export.py"
UI_HELPER_PATH = ROOT / "ui" / "teacher_runtime_export.py"
APP_PATH = ROOT / "streamlit_app.py"
TEST_PATH = ROOT / "tests" / "test_teacher_runtime_exposure_export.py"
LESSON_DOC_PATH = ROOT / "docs" / "runtime" / "teacher_lesson_session_setup_v1.md"
RLI_DOC_PATH = ROOT / "docs" / "runtime" / "runtime_learning_intelligence_v1.md"
DOCS_README_PATH = ROOT / "docs" / "README.md"
PIPELINE_README_PATH = ROOT / "data" / "pipeline_rounds" / "README.md"

FALSE_FIELDS = [
    "uses_auth",
    "uses_database",
    "uses_pii",
    "exposes_raw_logs",
    "changes_question_selection_weighting",
    "changes_question_selection_behavior",
    "changes_scoring_mastery",
    "changes_question_generation",
    "changes_source_truth",
    "changes_content_scope",
    "runtime_scope_widened",
    "perek_activated",
    "reviewed_bank_promoted",
    "student_facing_content_created",
    "raw_log_export_allowed",
    "mastery_claims_allowed",
    "promotion_claims_allowed",
]

TRUE_FIELDS = [
    "ui_added",
    "export_helper_added",
    "supports_markdown_export",
    "supports_json_export",
    "uses_teacher_lesson_session_setup",
    "uses_runtime_exposure_summary",
    "uses_local_attempt_history",
    "handles_missing_logs",
    "handles_empty_logs",
    "handles_malformed_logs",
    "handles_missing_session_context",
    "handles_write_failure",
    "teacher_interpretation_is_cautious",
]


def require(condition, message, errors):
    if not condition:
        errors.append(message)


def _read(path):
    return path.read_text(encoding="utf-8")


def _load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate():
    errors = []
    required_paths = [
        REPORT_PATH,
        JSON_PATH,
        RUNTIME_HELPER_PATH,
        UI_HELPER_PATH,
        APP_PATH,
        TEST_PATH,
        LESSON_DOC_PATH,
        RLI_DOC_PATH,
        DOCS_README_PATH,
        PIPELINE_README_PATH,
    ]
    for path in required_paths:
        require(path.exists(), f"Missing required artifact: {path.relative_to(ROOT)}", errors)
    if errors:
        return errors

    try:
        payload = _load_json(JSON_PATH)
    except json.JSONDecodeError as error:
        return [f"Implementation JSON does not parse: {error}"]

    helper_text = _read(RUNTIME_HELPER_PATH)
    ui_text = _read(UI_HELPER_PATH)
    app_text = _read(APP_PATH)
    report_text = _read(REPORT_PATH)
    lesson_doc = _read(LESSON_DOC_PATH)
    rli_doc = _read(RLI_DOC_PATH)
    docs_readme = _read(DOCS_README_PATH)
    pipeline_readme = _read(PIPELINE_README_PATH)
    combined = "\n".join([helper_text, ui_text, app_text, report_text, lesson_doc, rli_doc, docs_readme, pipeline_readme])
    lowered = combined.lower()

    require(payload.get("feature_name") == "teacher_runtime_exposure_export_report", "feature_name mismatch", errors)
    require(payload.get("feature_version") == "v1", "feature_version mismatch", errors)
    require(payload.get("export_location") == "data/teacher_exports", "export location mismatch", errors)
    for key in TRUE_FIELDS:
        require(payload.get(key) is True, f"{key} must be true", errors)
    for key in FALSE_FIELDS:
        require(payload.get(key) is False, f"{key} must be false", errors)

    require("def render_teacher_runtime_export_markdown" in helper_text, "Markdown renderer missing", errors)
    require("def build_teacher_runtime_export_json" in helper_text, "JSON builder missing", errors)
    require("def write_teacher_runtime_export" in helper_text, "write helper missing", errors)
    require("data/teacher_exports" in helper_text, "export path missing from helper", errors)
    require("SAFETY_CONTRACT" in helper_text and "uses_local_attempt_history" in helper_text, "safety fields missing", errors)
    require("from runtime.teacher_runtime_export import" in ui_text, "UI helper must reference export helper", errors)
    require("st.sidebar.expander" in ui_text and "Teacher Runtime Report Export" in ui_text, "UI helper must use a contained teacher section", errors)
    require("render_teacher_runtime_export" in app_text, "app must reference teacher runtime export renderer", errors)

    raw_log_markers = [
        "raw_lines",
        "st.json(record",
        "st.write(record",
        "st.code(line",
        "st.text(line",
        "st.write(line",
    ]
    for marker in raw_log_markers:
        require(marker not in lowered, f"raw log exposure marker found: {marker}", errors)

    for doc_text, label in [(lesson_doc, "lesson docs"), (rli_doc, "runtime docs")]:
        doc_lower = doc_text.lower()
        require("no login" in doc_lower, f"{label} must mention no login", errors)
        require("no database" in doc_lower, f"{label} must mention no database", errors)
        require("no pii" in doc_lower, f"{label} must mention no PII", errors)
        require("raw" in doc_lower and "log" in doc_lower, f"{label} must mention raw logs", errors)
        require("scoring/mastery" in doc_lower, f"{label} must mention no scoring/mastery change", errors)
        require("scope expansion" in doc_lower or "active scope" in doc_lower, f"{label} must mention no scope expansion", errors)

    require("teacher_runtime_exposure_export_report_2026_04_30" in docs_readme, "docs README entry missing", errors)
    require("teacher_runtime_exposure_export_report_2026_04_30" in pipeline_readme, "pipeline README entry missing", errors)

    forbidden = [
        "runtime_allowed=true",
        "reviewed_bank_allowed=true",
        "promoted_to_runtime",
        "approved_for_runtime",
        "runtime scope widened: yes",
        "perek activated: yes",
        '"perek_activated": true',
        "reviewed bank promoted: true",
        "scoring/mastery changed: true",
        "question generation changed: true",
        "raw logs exposed: true",
        "student-facing content created: true",
        "proves mastery",
        "content approved",
        "approved content",
        "authorizes promotion",
    ]
    for phrase in forbidden:
        require(phrase not in lowered, f"forbidden phrase found: {phrase}", errors)

    auth_db_pii_patterns = [
        "student_id",
        "student_name",
        "email",
        "password",
        "sqlalchemy",
        "sqlite3.connect",
        "requests.post",
        "firebase",
    ]
    for phrase in auth_db_pii_patterns:
        require(phrase not in lowered, f"auth/database/PII pattern found: {phrase}", errors)

    return errors


def main():
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("Teacher runtime exposure export validation passed.")


if __name__ == "__main__":
    main()
