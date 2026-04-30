# Teacher Runtime Evidence Export Suite V1 - 2026-04-30

## Purpose

Create a local teacher-facing export/report layer that preserves lesson/session context and Runtime Exposure Center evidence after a class or pilot session.

## Problem solved

Teachers could see runtime exposure context live in the sidebar, but there was no durable local Markdown/JSON artifact after the session.

## What was added

- Pure runtime export helper in `runtime/teacher_runtime_export.py`.
- Sidebar UI wrapper in `ui/teacher_runtime_export.py`.
- A collapsed Streamlit sidebar section named `Teacher Runtime Report Export`.
- Markdown and JSON export support under `data/teacher_exports/`.
- Cautious teacher interpretation derived only from summary data.
- Validator and focused tests.

## Files created

- `runtime/teacher_runtime_export.py`
- `ui/teacher_runtime_export.py`
- `data/pipeline_rounds/teacher_runtime_exposure_export_report_2026_04_30.md`
- `data/pipeline_rounds/teacher_runtime_exposure_export_report_2026_04_30.json`
- `scripts/validate_teacher_runtime_exposure_export.py`
- `tests/test_teacher_runtime_exposure_export.py`

## Files modified

- `streamlit_app.py`
- `docs/runtime/teacher_lesson_session_setup_v1.md`
- `docs/runtime/runtime_learning_intelligence_v1.md`
- `docs/README.md`
- `data/pipeline_rounds/README.md`
- `scripts/validate_curriculum_extraction.py`
- `tests/test_curriculum_extraction_validation.py`
- `PLANS.md`

## Where it appears in the UI

The export appears in the Streamlit sidebar as a collapsed `Teacher Runtime Report Export` expander near the Teacher Lesson / Session Setup panel and Runtime Exposure Center.

## Export file location

Reports save locally under `data/teacher_exports/`.

## Export naming convention

- `teacher_runtime_exposure_report_<YYYY_MM_DD_HHMMSS>.md`
- `teacher_runtime_exposure_report_<YYYY_MM_DD_HHMMSS>.json`

## Fields included in Markdown

- report metadata
- lesson/session label
- mode focus
- optional class/group label
- optional teacher notes
- recent attempts counted
- malformed/skipped log count
- fallback/scope-small status
- repeated Hebrew targets
- repeated pasuk/skill combinations
- repeated skills and question types
- cautious teacher interpretation
- missing-data warnings
- safety/privacy confirmation

## Fields included in JSON

- `schema_version`
- `report_type`
- `generated_at`
- `session_context`
- `exposure_summary`
- `teacher_interpretation`
- `missing_data_warnings`
- `output_contract`
- `safety`

## How lesson/session context is used

The export normalizes the local Teacher Lesson / Session Setup metadata from Streamlit session state. If the setup is missing or partial, the export records that as missing evidence instead of inventing context.

## How Runtime Exposure Center data is used

The export consumes the already-built Runtime Exposure Center summary. It does not read raw JSONL lines directly and does not change exposure calculations or question-selection weighting.

## How missing logs are handled

If no local attempt history is available, the export records a missing-evidence warning and still writes a valid Markdown/JSON report.

## How malformed logs are handled

Malformed/skipped log counts are carried from the exposure summary and displayed as counts only. Raw malformed lines are not exposed.

## How missing session setup is handled

Missing or partial lesson/session context is recorded in `missing_data_warnings`; report generation still succeeds.

## How write failures are handled

The write helper catches filesystem errors and returns a clear failure status. The UI warns the teacher and does not interrupt student flow.

## Known limitations

- This is local report generation, not a teacher account system.
- The export summarizes local evidence; it does not prove mastery.
- The export does not approve content or authorize promotion.
- The quality of interpretation depends on available local history fields.

## Manual test instructions

1. Open the Streamlit app.
2. Optionally fill in Teacher Lesson / Session Setup.
3. Answer several questions to create local exposure history.
4. Open `Teacher Runtime Report Export` in the sidebar.
5. Save the report and confirm Markdown/JSON files are created under `data/teacher_exports/`.
6. Confirm the report contains no raw JSONL lines or student login data.

## Validation commands run

To be filled in after validation.

## Safety confirmation

- no runtime scope expansion
- no Perek activation
- no reviewed-bank promotion
- no scoring/mastery change
- no question generation change
- no question-selection weighting change
- no source truth change
- no auth/database/PII
- no raw log exposure
- no student-facing content creation
- no validator weakening
