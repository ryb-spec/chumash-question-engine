# Bereishis Perek 1 First-Batch Answer/Distractor/Context Policy Yossi Review Applied

## Scope

First-batch Bereishis Perek 1 pre-generation policy layer for the 24 template/exact-wording planning candidates.

## Decisions applied

| Policy area | Decision |
|---|---|
| Answer-key planning policy | `approve_with_revision` |
| Distractor planning policy | `approve_with_revision` |
| Context-display/Hebrew-rendering policy | `approve_policy` |
| Pre-generation readiness checklist | `approve_with_revision` |

## Counts

- Policies reviewed: 4
- Approved policies: 1
- Approved-with-revision policies: 3
- Blocked policies: 0
- Needs-follow-up policies: 0

## Required row-level review before generation

Before any protected-preview draft generation, every selected row must still receive row-level review of:

- `exact_wording_review_status`
- `answer_key_language_review_status`
- `distractor_constraints_review_status`
- `context_display_review_status`
- `hebrew_rendering_review_status`
- `protected_preview_gate_review_status`

## What was not approved

- No final questions were generated or approved.
- No student-ready prompts were generated or approved.
- No answer choices were generated or approved.
- No answer keys were generated or approved.
- No distractors were generated or approved.
- No protected-preview input rows were created.
- No protected-preview content was created or approved.
- No reviewed-bank use was approved.
- No runtime use was approved.
- No student-facing use was approved.

## Safety gates

All gates remain closed:

- `final_question_allowed = false`
- `answer_choices_allowed = false`
- `answer_key_allowed = false`
- `distractors_allowed = false`
- `protected_preview_allowed = false`
- `reviewed_bank_allowed = false`
- `runtime_allowed = false`
- `student_facing_allowed = false`

## Recommended next task

Create a row-level pre-generation review sheet for the 24 selected rows so Yossi can review exact wording, answer-key language, distractor constraints, context display, Hebrew rendering, and protected-preview gate status before any draft generation is considered.
