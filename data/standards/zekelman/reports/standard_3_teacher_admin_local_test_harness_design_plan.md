# Zekelman Standard 3 Teacher/Admin Local Test Harness Design Plan

## 1. Purpose

This plan describes how a teacher/admin-only local harness could manually exercise the isolated Zekelman Standard 3 MVP test-mode loader and its transformed records.

This plan does not implement the harness. It does not wire the loader into normal runtime. It does not modify UI. It does not expose anything to students.

The goal is to define a safe future local review path where a teacher or project lead can inspect the 10 transformed Standard 3 records before any runtime wiring, UI work, student-facing use, or activation decision.

## 2. Hard Boundaries

- Runtime activation: blocked
- App routing integration: blocked
- UI integration: blocked
- Active-scope update: blocked
- Staged reviewed-bank update: blocked
- Student-facing use: blocked
- Current artifact: local test harness design plan only

This design plan does not authorize implementation, runtime activation, app routing, UI changes, active-scope changes, staged reviewed-bank changes, student-facing use, runtime-active status, or question-ready status.

## 3. Existing Loader Capabilities

Existing loader file:

- `runtime/standard_3_test_mode_loader.py`

Existing test file:

- `tests/test_standard_3_test_mode_loader.py`

Loader capabilities already implemented:

- Test mode flag: `STANDARD_3_MVP_TEST_MODE`
- Default behavior: off
- Explicit truthy flag values: `1`, `true`, `yes`, `on`
- When disabled: returns no records and does not read the protected bank path
- When enabled: loads and transforms only the 10 protected Standard 3 records
- Record-count enforcement: exactly 10 records
- Status preservation: `not_runtime_active`
- Student-facing preservation: `not_student_facing`
- App routing integration: none
- Active-scope integration: none
- Staged reviewed-bank integration: none

The loader produces teacher/admin test-mode records with fields such as `question`, `question_text`, `correct_answer`, `skill`, `question_type`, `mode`, `micro_standard`, `review_family`, `runtime_status`, `student_facing_status`, `source_record_id`, `test_mode_only`, and `open_response`.

The loader currently uses open-response records with `choices: []` rather than inventing distractors.

## 4. Proposed Local Harness Purpose

The future harness should help a teacher or admin inspect:

- all 10 transformed records
- prompts
- expected answers
- skill lanes
- question-type families
- approved Hebrew inputs
- approved input references
- conservative runtime and student-facing statuses
- protected/deferred-content checks
- whether items are understandable before any runtime wiring

The harness should be a local review surface only. It should not simulate student progress, mastery, adaptive routing, scoring, production app flow, or live UI behavior.

## 5. Proposed Future Harness Shape

Suggested future file:

- `scripts/standard_3_local_test_harness.py`

Suggested future behavior:

- Requires explicit `STANDARD_3_MVP_TEST_MODE=1`.
- Refuses to run when the test-mode flag is off.
- Calls the isolated loader directly.
- Prints or exports the 10 transformed records.
- Shows prompt, expected answer, skill lane, question-type family, approved input, source record ID, runtime status, student-facing status, and test-mode marker.
- Optionally writes a local review-only markdown report.
- Never modifies `data/active_scope_reviewed_questions.json`.
- Never modifies `data/staged/*/reviewed_questions.json`.
- Never modifies runtime routing.
- Never creates student-facing files.
- Never marks anything runtime-active.
- Never marks anything question-ready.

Suggested report output, if created later:

- Local-only review date
- Loader flag state
- Record count
- Per-record prompt and expected answer
- Per-record skill/question-type summary
- Per-record teacher/admin notes field
- Confirmation that all records remain `not_runtime_active`
- Confirmation that all records remain `not_student_facing`
- Confirmation that no excluded content is present

The future harness should be deliberately boring. Its job is visibility and manual review, not feature excitement.

## 6. Manual Review Workflow

Recommended teacher/admin workflow:

1. Run the harness locally with the test flag enabled.
2. Review each of the 10 items.
3. Confirm prompts and expected answers are understandable.
4. Confirm each item stays within its stated skill lane.
5. Confirm no excluded lane or excluded content appears.
6. Record feedback in a local review report.
7. Turn off the flag.
8. Confirm default runtime remains unchanged.

The review should focus on clarity, accuracy, skill alignment, wording, and whether open-response display is acceptable for teacher/admin testing.

## 7. Required Future Implementation Tests

If the harness is later implemented, focused tests should prove:

- harness refuses to run when the flag is off
- harness loads exactly 10 records when the flag is on
- output contains no runtime-active statuses
- output contains no student-facing statuses
- output contains no excluded lanes or excluded content
- active scope is unchanged
- staged reviewed questions are unchanged
- no UI files are imported or modified
- no runtime-routing files are imported or modified
- review-only report, if created, is clearly non-runtime
- review-only report, if created, contains exactly 10 records
- review-only report, if created, preserves `not_runtime_active` and `not_student_facing`

These tests should stay separate from full app runtime tests. The harness should remain local and isolated.

## 8. Safety and Rollback

Rollback is simple:

- Turn off `STANDARD_3_MVP_TEST_MODE`.
- Delete any local review-only output created by the future harness.
- Confirm the loader returns no records when the flag is off.
- Confirm default tests still pass.

No runtime data files should need rollback because the future harness should not modify runtime data.

Active scope and staged reviewed-question files should remain untouched:

- `data/active_scope_reviewed_questions.json`
- `data/staged/*/reviewed_questions.json`

## 9. Still Blocked

The following remain blocked:

- harness implementation
- runtime activation
- app routing integration
- UI integration
- active-scope update
- staged reviewed-bank update
- student-facing use
- progress/mastery/adaptive-routing integration
- expansion beyond 10 records
- expansion beyond locked lanes and approved inputs
- all excluded content

## 10. Recommended Future Sequence

1. Implement local harness as an isolated script.
2. Add focused harness tests.
3. Run teacher/admin local review.
4. Produce feedback report.
5. Only then consider a runtime activation gate.

The next implementation should still keep default runtime off and should not wire the loader into normal app routing.

## 11. Validation Results

Required validation commands:

- `python -m pytest tests/test_standard_3_test_mode_loader.py`: passed, 14 tests passed
- `python scripts/validate_source_texts.py`: passed
- `python scripts/validate_curriculum_extraction.py`: passed
- `python scripts/validate_standards_data.py`: passed
- `python -m pytest tests/test_standards_data_validation.py`: passed, 9 tests passed

## 12. Final Status Summary

- Runtime activation: blocked
- Local harness: not implemented
- Loader: isolated and default-off
- App routing: unchanged
- Active scope: untouched
- Staged reviewed questions: untouched
- Student-facing use: blocked
- Current artifact: design plan only
- Recommended next step: implement isolated local harness with focused tests
