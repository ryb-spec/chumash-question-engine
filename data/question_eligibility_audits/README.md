# Question Eligibility Audits

This directory is an audit-only layer. It does not generate questions, answer choices, answer keys, protected-preview content, reviewed-bank content, runtime data, or student-facing content. It does not approve protected-preview use, does not approve reviewed-bank use, and does not approve runtime use.

Existing source-to-skill and enrichment safety gates remain closed. Eligibility recommendations require later Yossi review. Only later, after separate approval, can a protected-preview input list be created.

## Allowed Audit Recommendation Statuses

- `eligible_candidate_for_yossi_question_review`
- `source_only`
- `needs_follow_up`
- `blocked_for_questions`

## Forbidden Statuses And Phrases

- `question_ready`
- `protected_preview_ready`
- `reviewed_bank_ready`
- `runtime_ready`
- `student_facing`
- `approved_for_questions`
- `approved_for_preview`

## Bereishis Perek 1 Audit Artifacts

- `bereishis_perek_1_question_eligibility_audit.tsv`
- `reports/bereishis_perek_1_question_eligibility_audit_report.md`
- `reports/bereishis_perek_1_question_eligibility_yossi_review_sheet.md`
- `reports/bereishis_perek_1_question_eligibility_yossi_review_sheet.csv`

## Bereishis Perek 1 First-Pass Review-Applied Status

Yossi first-pass question-eligibility decisions have been applied in the audit layer only.

Artifacts:

- `reports/bereishis_perek_1_question_eligibility_yossi_review_applied.md`
- `reports/bereishis_perek_1_approved_input_candidate_planning_sheet.md`
- `reports/bereishis_perek_1_approved_input_candidate_planning_sheet.csv`

Decision counts:

- approve_as_input_candidate: 133
- needs_follow_up: 155
- source_only: 6
- block_for_questions: 5

Input-candidate approval is not question approval. Protected preview remains a separate later gate. Morphology/basic verb-form rows were deferred pending a morphology-question wording standard.
