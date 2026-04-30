from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "pipeline_rounds" / "teacher_lesson_session_setup_v1_2026_04_30.md"
CONTRACT = ROOT / "data" / "pipeline_rounds" / "teacher_lesson_session_setup_v1_2026_04_30.json"
DOC = ROOT / "docs" / "runtime" / "teacher_lesson_session_setup_v1.md"
RLI_DOC = ROOT / "docs" / "runtime" / "runtime_learning_intelligence_v1.md"
HELPER = ROOT / "runtime" / "lesson_session_setup.py"
UI_HELPER = ROOT / "ui" / "teacher_lesson_session_setup.py"
EXPOSURE_UI = ROOT / "ui" / "runtime_exposure_summary.py"
APP = ROOT / "streamlit_app.py"
PIPELINE_README = ROOT / "data" / "pipeline_rounds" / "README.md"
DOCS_README = ROOT / "docs" / "README.md"

FALSE_FIELDS = [
    "uses_auth",
    "uses_database",
    "uses_pii",
    "exposes_raw_logs",
    "creates_new_content",
    "changes_question_selection",
    "changes_question_selection_weighting",
    "changes_scoring_mastery",
    "changes_content_scope",
    "runtime_scope_widened",
    "perek_activated",
    "reviewed_bank_promoted",
    "student_facing_content_created",
    "source_truth_changed",
]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate() -> list[str]:
    errors: list[str] = []
    required = [REPORT, CONTRACT, DOC, RLI_DOC, HELPER, UI_HELPER, EXPOSURE_UI, APP, PIPELINE_README, DOCS_README]
    for path in required:
        require(path.exists(), f"Missing required artifact: {path.relative_to(ROOT)}", errors)
    if errors:
        return errors

    try:
        payload = load_json(CONTRACT)
    except json.JSONDecodeError as error:
        return [f"Implementation JSON does not parse: {error}"]

    report_text = REPORT.read_text(encoding="utf-8")
    doc_text = DOC.read_text(encoding="utf-8")
    rli_doc_text = RLI_DOC.read_text(encoding="utf-8")
    helper_text = HELPER.read_text(encoding="utf-8")
    ui_text = UI_HELPER.read_text(encoding="utf-8")
    exposure_ui_text = EXPOSURE_UI.read_text(encoding="utf-8")
    app_text = APP.read_text(encoding="utf-8")
    readme_text = PIPELINE_README.read_text(encoding="utf-8") + "\n" + DOCS_README.read_text(encoding="utf-8")
    combined = "\n".join([report_text, doc_text, rli_doc_text, helper_text, ui_text, exposure_ui_text, app_text, readme_text])
    lowered = combined.lower()

    require(payload.get("feature_name") == "teacher_lesson_session_setup_v1", "feature_name mismatch", errors)
    require(payload.get("ui_added") is True, "ui_added must be true", errors)
    require(payload.get("stores_session_metadata_locally") is True, "stores_session_metadata_locally must be true", errors)
    require(payload.get("storage_location") == "streamlit_session_state", "storage_location must be streamlit_session_state", errors)
    require(payload.get("integrates_with_runtime_exposure_center") is True, "must integrate with Runtime Exposure Center", errors)
    require(payload.get("safe_ui_fallback") is True, "safe_ui_fallback must be true", errors)
    for key in FALSE_FIELDS:
        require(payload.get(key) is False, f"{key} must be false", errors)

    require(
        "Teacher Lesson / Session Setup" in app_text or "Teacher Lesson / Session Setup" in ui_text,
        "UI must include teacher setup language",
        errors,
    )
    require("render_teacher_lesson_session_setup" in app_text, "app must call teacher lesson setup renderer", errors)
    require("teacher_lesson_session" in app_text, "app must pass session context to exposure summary", errors)
    require("lesson_session_summary_lines" in exposure_ui_text, "Runtime Exposure Center must render lesson/session context", errors)
    require("SESSION_STATE_KEY" in helper_text, "helper must use a session-state key", errors)
    require("no auth" in doc_text.lower(), "docs must mention no auth", errors)
    require("no database" in doc_text.lower(), "docs must mention no database", errors)
    require("no pii" in doc_text.lower(), "docs must mention no PII", errors)
    require("no active runtime scope expansion" in doc_text.lower(), "docs must mention no active runtime scope expansion", errors)
    require("runtime exposure center" in rli_doc_text.lower(), "RLI docs must mention Runtime Exposure Center integration", errors)

    forbidden = [
        "runtime_allowed=true",
        "reviewed_bank_allowed=true",
        "promoted_to_runtime",
        "approved_for_runtime",
        '"uses_auth": true',
        '"uses_database": true',
        '"uses_pii": true',
        '"changes_question_selection": true',
        '"changes_scoring_mastery": true',
        '"runtime_scope_widened": true',
        '"perek_activated": true',
        "runtime scope widened: yes",
        "question selection changed: yes",
        "scoring/mastery changed: yes",
    ]
    for phrase in forbidden:
        require(phrase not in lowered, f"forbidden claim found: {phrase}", errors)

    raw_log_markers = ["st.json(record", "st.write(record", "st.code(line", "st.text(line", "st.write(line"]
    for phrase in raw_log_markers:
        require(phrase not in lowered, f"raw log exposure marker found: {phrase}", errors)

    return errors


def main() -> None:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("Teacher lesson session setup validation passed.")


if __name__ == "__main__":
    main()
