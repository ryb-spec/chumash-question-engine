# Zekelman Standard 3 Runtime Activation Design Plan

## 1. Purpose

This plan describes how the 10 protected Zekelman Standard 3 MVP reviewed-bank records could be exposed in a controlled future test mode.

This plan does not activate runtime. It does not modify app routing. It does not modify active scope. It does not expose anything to students.

The purpose is to name a safe future design path before any runtime task changes code or data wiring.

## 2. Hard Boundaries

- Runtime activation: blocked
- App routing: disconnected
- Active-scope update: blocked
- Student-facing use: blocked
- UI changes: blocked
- Current artifact: runtime activation design plan only

This document does not authorize runtime activation, UI changes, active-scope changes, staged reviewed-bank changes, student-facing use, or question-ready status.

## 3. Reviewed Records in Scope

- Source file: `data/standards/zekelman/reviewed_bank/standard_3_mvp_reviewed_bank.json`
- Record count: 10
- `runtime_status`: `not_runtime_active`
- `student_facing_status`: `not_student_facing`
- Scope: Standard 3 MVP only

The records cover only these locked MVP lanes:

- `3.01` Nouns / שמות עצם
- `3.02` Simple Shorashim / שורשים
- `3.05` Pronominal Suffix Decoding
- `3.06` Visible Prefixes / Articles
- `3.07` Foundational Verb Clues

## 4. Proposed Controlled Test Mode

A future controlled test mode should use a separate test-mode loader or explicit feature flag. It should not reuse the default active-scope reviewed-question path automatically.

Proposed design:

- Add a separate test-mode loader for `data/standards/zekelman/reviewed_bank/standard_3_mvp_reviewed_bank.json`.
- Load only records where `source_scope` is `zekelman_standard_3_mvp`.
- Load only the 10 records currently present in the protected bank.
- Require a test-mode flag before any record is considered by runtime.
- Keep default app behavior unchanged when the flag is absent.
- Keep general student-facing availability disabled.
- Limit first exposure to teacher/admin-only testing.
- Display a clear label: "Standard 3 MVP test mode".
- Log every served test-mode item with the reviewed-bank record ID and source preview item ID.
- Collect feedback notes separately from production attempt/progress logs unless a future task explicitly designs that integration.
- Provide a clear rollback method: remove or disable the test-mode flag and the loader must stop serving all Standard 3 MVP records.

This plan intentionally does not define the final UI surface. A future implementation should decide whether the controlled test mode is CLI-only, developer-only, admin-only, or hidden behind an explicit debug/test parameter.

## 5. Required Future Runtime Changes

A future runtime activation task would need to inspect or modify candidate files such as:

- `assessment_scope.py`
- `engine/flow_builder.py`
- `runtime/question_flow.py`
- `streamlit_app.py`, only if an explicit UI/test-mode surface is authorized
- tests around active-scope reviewed questions and runtime generation, especially `tests/test_active_scope_reviewed_questions.py` and relevant runtime-quality tests

The current runtime-reviewed path is:

- `assessment_scope.py` defines `ACTIVE_SCOPE_REVIEWED_QUESTIONS_PATH` as `data/active_scope_reviewed_questions.json`.
- `assessment_scope.py` exposes `active_scope_reviewed_questions_for_text(...)`.
- `engine/flow_builder.py` calls `active_scope_reviewed_questions_for_text(...)` and clones matching records into runtime questions.
- Staged reviewed-support files are referenced through corpus manifest/staged paths such as `data/staged/*/reviewed_questions.json`.

Future design requirements:

- The protected Standard 3 bank should be referenced only by an explicit test-mode loader.
- The loader should reject records unless they are still `runtime_status: not_runtime_active`, until a future activation task defines a limited activation status or flag.
- A future activation task may add a separate test-mode eligibility flag without changing these records to generally runtime-active.
- Test mode should avoid touching `data/active_scope_reviewed_questions.json`.
- Test mode should avoid touching `data/staged/*/reviewed_questions.json`.
- Rollback should be a flag/config reversal, not a data rewrite.
- The loader must enforce a hard count of 10 records and fail closed if additional records appear without a new approval gate.

If the future implementation decides to translate Standard 3 protected records into the existing active-scope question schema, that should be a separate design and validation task. This plan does not authorize that transformation.

## 6. Safety Requirements Before Activation

Before any future activation, the project needs:

- explicit runtime activation prompt
- teacher/product approval for controlled test exposure
- exact runtime scope decision
- loader/routing design review
- status-change plan
- rollback plan
- confirmation only 10 records are loadable
- validation that excluded content remains blocked
- review of student-facing wording before any student exposure

Additional recommended safety checks:

- test-mode records must be auditable by record ID
- no records may enter mastery/progress tracking without an explicit plan
- no records may affect adaptive routing without an explicit plan
- logs must distinguish protected test-mode activity from normal student attempts
- teacher/admin review notes should remain separate from student-facing correctness data

## 7. Blocked Content and Scope Limits

The following remain blocked:

- expansion beyond 10 records
- expansion beyond locked lanes and approved inputs
- 3.05 Pronoun Referent Tracking
- expanded 3.02 shoresh list beyond שמר
- 3.04
- 3.08
- 3.10
- weak-letter roots
- altered-root recognition
- advanced contextual shoresh translation
- full verb parsing
- two functions of את
- ו ההיפוך
- ה השאלה
- ה המגמה
- בנינים
- passive forms
- ציווי
- מקור
- שם הפועל
- weak-root verb analysis
- cross-pasuk pronoun referents
- ambiguous pronoun referents
- context-stripped word-order questions
- compact סמיכות questions

## 8. Recommended Future Activation Sequence

1. Runtime loader discovery
2. Test-mode implementation plan
3. Controlled test-mode activation prompt
4. Teacher/admin-only testing
5. Feedback report
6. Separate student-facing exposure decision, if ever appropriate

## 9. Final Status Summary

- Runtime activation: blocked
- Active scope: untouched
- Staged reviewed questions: untouched
- Student-facing use: blocked
- Current artifact: design plan only
- Next step: runtime loader discovery or PR/merge, depending on project workflow

## 10. Validation Results

Required validation commands:

- `python scripts/validate_source_texts.py`: passed
- `python scripts/validate_curriculum_extraction.py`: passed
- `python scripts/validate_standards_data.py`: passed
- `python -m pytest tests/test_standards_data_validation.py`: passed, 9 tests passed

Protected reviewed-bank parse check:

- `data/standards/zekelman/reviewed_bank/standard_3_mvp_reviewed_bank.json`: parsed successfully
- record count: 10
- runtime statuses: `not_runtime_active`
- student-facing statuses: `not_student_facing`
