"""Validate Teacher Runtime Export Session Accuracy V1 artifacts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FIX_MD = ROOT / "data" / "pipeline_rounds" / "teacher_runtime_export_session_accuracy_fix_2026_04_30.md"
FIX_JSON = ROOT / "data" / "pipeline_rounds" / "teacher_runtime_export_session_accuracy_fix_2026_04_30.json"
READINESS_MD = ROOT / "data" / "pipeline_rounds" / "content_expansion_readiness_after_teacher_export_accuracy_2026_04_30.md"
READINESS_JSON = ROOT / "data" / "pipeline_rounds" / "content_expansion_readiness_after_teacher_export_accuracy_2026_04_30.json"
EXPORT_HELPER = ROOT / "runtime" / "teacher_runtime_export.py"
LESSON_HELPER = ROOT / "runtime" / "lesson_session_setup.py"
LESSON_UI = ROOT / "ui" / "teacher_lesson_session_setup.py"
EXPORT_UI = ROOT / "ui" / "teacher_runtime_export.py"
EXPORT_TEST = ROOT / "tests" / "test_teacher_runtime_exposure_export.py"
LESSON_TEST = ROOT / "tests" / "test_teacher_lesson_session_setup.py"
LESSON_DOC = ROOT / "docs" / "runtime" / "teacher_lesson_session_setup_v1.md"
RLI_DOC = ROOT / "docs" / "runtime" / "runtime_learning_intelligence_v1.md"


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _expect_false(errors: list[str], payload: dict, keys: list[str], label: str) -> None:
    for key in keys:
        if payload.get(key) is not False:
            errors.append(f"{label}.{key} must be false")


def validate() -> list[str]:
    errors: list[str] = []
    for path in [
        FIX_MD,
        FIX_JSON,
        READINESS_MD,
        READINESS_JSON,
        EXPORT_HELPER,
        LESSON_HELPER,
        LESSON_UI,
        EXPORT_UI,
        EXPORT_TEST,
        LESSON_TEST,
        LESSON_DOC,
        RLI_DOC,
    ]:
        if not path.exists():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")

    if errors:
        return errors

    try:
        fix_payload = _json(FIX_JSON)
        readiness_payload = _json(READINESS_JSON)
    except Exception as exc:  # pragma: no cover - defensive validator path
        return [f"JSON parse failed: {exc}"]

    expected_true = {
        "fixes_current_session_export_accuracy",
        "fixes_class_group_label_mapping",
        "renames_mode_focus_to_planned_lesson_focus",
        "adds_teacher_setup_saved_at",
        "adds_export_scope_metadata",
        "supports_current_pilot_session_scope",
        "supports_teacher_setup_window_scope",
        "supports_recent_local_history_fallback",
        "markdown_json_single_snapshot",
        "ready_for_content_expansion_planning",
    }
    for key in expected_true:
        if fix_payload.get(key) is not True:
            errors.append(f"fix JSON {key} must be true")

    _expect_false(
        errors,
        fix_payload,
        [
            "exposes_raw_logs",
            "uses_auth",
            "uses_database",
            "uses_pii",
            "changes_question_selection",
            "changes_question_selection_weighting",
            "changes_scoring_mastery",
            "changes_question_generation",
            "changes_content_scope",
            "runtime_scope_widened",
            "perek_activated",
            "reviewed_bank_promoted",
        ],
        "fix JSON",
    )

    if readiness_payload.get("ready_for_content_expansion_planning") is not True:
        errors.append("readiness gate must be ready for content expansion planning")
    _expect_false(
        errors,
        readiness_payload,
        [
            "content_expansion_performed",
            "runtime_scope_expansion_authorized",
            "perek_activation_authorized",
            "reviewed_bank_promotion_authorized",
            "runtime_scope_widened",
            "perek_activated",
            "reviewed_bank_promoted",
            "scoring_mastery_changed",
            "question_selection_changed",
            "question_generation_changed",
            "source_truth_changed",
            "auth_database_pii_added",
            "raw_logs_exposed",
        ],
        "readiness JSON",
    )

    export_helper = _read(EXPORT_HELPER)
    export_ui = _read(EXPORT_UI)
    lesson_ui = _read(LESSON_UI)
    tests = _read(EXPORT_TEST) + "\n" + _read(LESSON_TEST)
    docs = _read(LESSON_DOC) + "\n" + _read(RLI_DOC)

    required_helper_fragments = [
        'SCHEMA_VERSION = "1.1"',
        "planned_lesson_focus",
        "class_group_label",
        "saved_at",
        "export_scope",
        "current_session_bounded",
        "records_in_scope",
        "records_considered",
        "confidence_level",
        "content_expansion_readiness",
        "determine_teacher_export_scope",
        "filter_attempt_records_for_export_scope",
        "build_session_bounded_exposure_summary",
        "Teacher setup note: planned lesson focus is a teacher/report label only",
    ]
    for fragment in required_helper_fragments:
        if fragment not in export_helper:
            errors.append(f"export helper missing fragment: {fragment}")

    if "- Mode focus:" in export_helper:
        errors.append("export Markdown renderer must not use Mode focus as primary label")
    if "Report scope" not in export_ui or "Build/refresh report snapshot" not in export_ui:
        errors.append("export UI must include report scope selector and shared snapshot action")
    if "does not change the student question mode" not in lesson_ui:
        errors.append("lesson setup UI must explain planned focus does not change student question mode")
    if "markdown_and_json_share_one_export_snapshot" not in tests:
        errors.append("single-snapshot behavior must be tested")
    if "current_pilot_session_scope_filters" not in tests:
        errors.append("current-session filtering must be tested")
    if "legacy" not in tests.lower() or "class_group_label" not in tests:
        errors.append("legacy class/group mapping must be tested")

    required_doc_fragments = [
        "Planned lesson focus",
        "does not change the student question mode",
        "current-session bounded",
        "Recent local history",
        "one export snapshot",
        "No raw logs",
        "No login",
        "No database",
        "No PII",
        "No scoring/mastery",
        "No runtime scope expansion",
    ]
    for fragment in required_doc_fragments:
        if fragment not in docs:
            errors.append(f"docs missing fragment: {fragment}")

    forbidden_positive_claims = [
        "runtime scope was widened",
        "new Perek was activated",
        "reviewed bank was promoted",
        "scoring/mastery was changed",
        "question generation was changed",
        "raw logs exposed: true",
        "student-facing content was created",
        "export proves mastery",
        "export approves content",
    ]
    combined = "\n".join(
        [
            _read(FIX_MD),
            json.dumps(fix_payload, ensure_ascii=False),
            _read(READINESS_MD),
            json.dumps(readiness_payload, ensure_ascii=False),
            export_helper,
            export_ui,
            docs,
        ]
    ).lower()
    for phrase in forbidden_positive_claims:
        if phrase.lower() in combined:
            errors.append(f"forbidden positive claim found: {phrase}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Teacher runtime export session accuracy validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
