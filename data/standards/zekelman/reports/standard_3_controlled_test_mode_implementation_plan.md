# Zekelman Standard 3 Controlled Test-Mode Implementation Plan

## 1. Purpose

This plan defines how a future implementation could expose the 10 protected Zekelman Standard 3 MVP reviewed-bank records in a teacher/admin-only controlled test mode.

This plan does not implement test mode. It does not activate runtime. It does not modify active scope. It does not expose anything to students.

The goal is to describe the safest implementation shape before any runtime, routing, or UI work begins.

## 2. Hard Boundaries

- Runtime activation: blocked
- App routing implementation: blocked
- UI changes: blocked
- Active-scope update: blocked
- Staged reviewed-bank update: blocked
- Student-facing use: blocked
- Current artifact: implementation plan only

This task does not create runtime loader files, does not change app routing, does not modify reviewed-question data, and does not mark anything runtime-active or question-ready.

## 3. Technical Finding From Discovery

Runtime discovery found:

- Runtime currently loads active reviewed questions from `data/active_scope_reviewed_questions.json`.
- `assessment_scope.py` defines `ACTIVE_SCOPE_REVIEWED_QUESTIONS_PATH`, loads active reviewed questions, canonicalizes them, and exposes accessors such as `active_scope_reviewed_questions_for_text(...)`.
- `engine/flow_builder.py` consumes reviewed questions through `reviewed_question_for_pasuk_skill(...)`, then calls `clone_reviewed_question(...)` and `validate_question_payload(...)`.
- `runtime/question_flow.py` provides `validate_question_for_serve(...)`, which reviewed-bank build tooling already uses for serve-readiness checks.
- `scripts/build_reviewed_question_bank.py` builds the active reviewed bank from active/staged reviewed-support sources, but should not be used to silently promote Standard 3 test-mode records into the active bank.
- The protected Standard 3 bank is not runtime-compatible as-is.

The protected bank lacks runtime fields such as:

- `choices`
- `correct_answer`
- `skill`
- `question_type`
- `mode`
- `micro_standard`
- `difficulty`
- `pasuk_id`
- `pasuk_ref`
- `reviewed_id`
- `review_family`

The protected bank has standards/review fields such as `final_prompt`, `expected_answer`, `skill_lane`, `question_type_family`, `review_status`, `runtime_status`, and `student_facing_status`. These are valuable provenance fields, but they are not enough for current runtime question serving.

## 4. Recommended Architecture

Recommended architecture: an adapter/transformation layer behind an explicit test-mode flag.

Core design:

- The protected Standard 3 JSON remains unchanged.
- A future adapter reads `data/standards/zekelman/reviewed_bank/standard_3_mvp_reviewed_bank.json`.
- The adapter transforms protected records into runtime-compatible preview/test records.
- The adapter is used only when an explicit teacher/admin-only test flag is enabled.
- Default runtime remains unchanged.
- `data/active_scope_reviewed_questions.json` remains untouched.
- `data/staged/*/reviewed_questions.json` remains untouched.

This keeps the Standard 3 records traceable to their protected standards source while avoiding accidental default runtime exposure.

## 5. Proposed Future Files

Suggested new files for a later implementation task:

- `runtime/standard_3_test_mode_loader.py`
- `tests/test_standard_3_test_mode_loader.py`

Possible files to inspect or modify only in a later implementation task:

- `assessment_scope.py`
- `engine/flow_builder.py`
- `runtime/question_flow.py`

This planning task must not create or modify those runtime files.

## 6. Runtime-Compatible Transformation Design

| Protected bank field | Future runtime field | Transformation rule | Notes |
|---|---|---|---|
| `reviewed_bank_record_id` | `reviewed_id` | Use candidate record ID as the stable test-mode reviewed ID. | Keeps traceability to protected bank. |
| `source_candidate_record_id` | `_standard_3_source_candidate_record_id` | Preserve as metadata. | Test-mode-only metadata; not required by default runtime. |
| `source_preview_item_id` | `_standard_3_source_preview_item_id` | Preserve as metadata. | Useful for audit and rollback. |
| `standard` | `standard` | Keep `3` or map to a runtime-compatible Standard 3 label if required. | Current runtime often uses broader labels such as `WM`; future tests must decide accepted value. |
| `standard_id` | `micro_standard` | Use Standard 3 lane ID, such as `3.01`. | Keeps Zekelman alignment visible. |
| `skill_lane` | `skill` | Map lane to runtime skill ID. | Requires explicit mapping table. |
| `question_type_family` | `question_type` | Map family to runtime-compatible question type. | Requires explicit mapping table. |
| `approved_hebrew_input` | `word`, `selected_word` | Copy approved input into both fields. | Use only approved inputs. |
| `final_prompt` | `question`, `question_text` | Copy final prompt into both fields. | Use final revised teacher-reviewed prompt only. |
| `expected_answer` | `correct_answer` | Copy expected answer. | Must match one choice if choices are used. |
| `answer_key_rationale` | `explanation` | Use as teacher/admin explanation. | Should not become student-facing without later review. |
| `protected_deferred_content_check` | `_protected_deferred_content_check` | Preserve as metadata. | Future validator should require this. |
| `review_status` | `_standard_3_review_status` | Preserve as metadata. | Do not treat as default runtime reviewed-bank approval. |
| `runtime_status` | `_standard_3_runtime_status` | Preserve as metadata and require `not_runtime_active`. | Test-mode eligibility should be a separate flag, not a status upgrade. |
| `student_facing_status` | `_standard_3_student_facing_status` | Preserve and require `not_student_facing`. | Test mode must remain teacher/admin-only. |
| `reviewer_notes` | `_reviewer_notes` | Preserve as metadata. | Useful in audit/debug output. |

Conservative defaults for fields missing from the protected bank:

- `choices`: generated only from approved inputs or omitted if runtime test mode supports open response
- `correct_answer`: from `expected_answer`
- `skill`: mapped from `skill_lane`
- `question_type`: mapped from `question_type_family`
- `mode`: `standard_3_mvp_test_mode`
- `micro_standard`: Standard 3 lane or candidate ID
- `difficulty`: `mvp_foundational`
- `pasuk_id`: `standard_3_mvp_test`
- `pasuk_ref`: `Standard 3 MVP test item`
- `reviewed_id`: candidate record ID
- `review_family`: `zekelman_standard_3_mvp`

The safest first implementation should produce teacher/admin test records separately from the normal active-scope reviewed question stream.

## 7. Choice / Distractor Policy

Current runtime validation expects choices in many paths. Future implementation should use this policy:

- Prefer open-response teacher/admin test mode if supported.
- If choices are required, use only approved inputs from the same locked lane.
- Never invent distractors from unapproved or excluded content.
- Never use weak roots, ו ההיפוך, את, 3.04, 3.08, or 3.10 content.
- If safe choices cannot be generated, block that record from test-mode runtime.
- Do not use broad corpus distractor generation for these records.
- Do not allow distractors that require deferred skills to reject.

Because several protected records are short-answer style, the future implementation may need either a teacher/admin open-response renderer or a deliberately separate test-mode payload validator. It should not force unsafe multiple-choice distractors just to satisfy the current runtime shape.

## 8. Test-Mode Flag Design

Proposed flag name:

- `STANDARD_3_MVP_TEST_MODE`

Flag behavior:

- Default: off
- Only teacher/admin testing may enable it
- When off, no Standard 3 protected records load
- When on, only the 10 approved records are eligible
- Active scope remains untouched
- Staged reviewed questions remain untouched
- Student-facing status remains blocked

The flag should be read in a future isolated test-mode loader, not as a broad runtime behavior switch.

## 9. Required Tests for Future Implementation

Future implementation must add tests that prove:

- protected bank parses
- adapter transforms all 10 records
- transformed records contain required runtime fields
- test mode off loads zero Standard 3 protected records
- test mode on loads only the 10 records
- default active scope remains unchanged
- staged reviewed questions remain unchanged
- excluded content remains absent
- unsafe distractor generation is blocked
- no student-facing status is changed
- no record becomes runtime-active
- transformed payloads either pass `validate_question_payload(...)` or are handled by a separate teacher/admin open-response validator
- no test-mode records enter progress/mastery/adaptive routing unless separately authorized

## 10. Rollback Plan

Rollback should be simple:

- turn off `STANDARD_3_MVP_TEST_MODE`
- remove or disable the adapter reference
- do not touch `data/active_scope_reviewed_questions.json`
- do not touch `data/staged/*/reviewed_questions.json`
- confirm default tests still pass
- confirm no Standard 3 protected records are reachable when the flag is off

No data rewrite should be required for rollback.

## 11. Recommended Future Sequence

1. Create adapter/test-mode loader in isolated files.
2. Add tests for transformation and flag behavior.
3. Keep runtime default off.
4. Run teacher/admin-only local test.
5. Produce feedback report.
6. Only later consider a runtime activation gate.

## 12. Still Blocked

The following remain blocked:

- runtime activation
- student-facing use
- UI changes
- active-scope update
- staged reviewed-bank update
- broader question generation
- expansion beyond the 10 records
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

## 13. Final Status Summary

- Runtime activation: blocked
- Test-mode implementation: not created
- Active scope: untouched
- Staged reviewed questions: untouched
- Student-facing use: blocked
- Current artifact: controlled test-mode implementation plan only
- Recommended next step: isolated adapter/test-mode loader implementation with tests, still default-off

## 14. Validation Results

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
