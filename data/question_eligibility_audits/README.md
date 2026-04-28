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

## Bereishis Perek 1 Wording Policy Status

A wording/template policy now exists for the 133 first-pass approved future input candidates. This policy layer defines boundaries only; no questions were generated, no answer choices were generated, no answer keys were generated, and no protected-preview input list was created.

Artifacts:

- `docs/question_templates/perek_1_approved_input_candidate_wording_policy.md`
- `question_template_wording_policy.v1.json`
- `reports/perek_1_approved_input_candidate_wording_policy_yossi_review_packet.md`
- `reports/perek_1_question_template_wording_policy_report.md`

Allowed policy families:

- `vocabulary_meaning`
- `basic_noun_recognition`
- `direct_object_marker_recognition`
- `shoresh_identification`

The verb-form remains deferred: `basic_verb_form_recognition` requires a separate morphology-question wording standard before any later input-candidate approval.

Next action: Yossi reviews wording policy and Codex applies only reviewed family-policy decisions in a separate policy-decision task.

## Bereishis Perek 1 Family-Policy Review-Applied Status

Yossi reviewed the family-level wording policy and approved four family policies while keeping one family deferred.

Review-applied artifact:

- `reports/perek_1_approved_input_candidate_wording_policy_yossi_review_applied.md`

Approved family policies:

- `vocabulary_meaning`
- `basic_noun_recognition`
- `direct_object_marker_recognition`
- `shoresh_identification`

Deferred family policy:

- `basic_verb_form_recognition`

Exact template wording review is still required. Protected preview remains a later gate. No questions, answer choices, answer keys, protected-preview input list, reviewed-bank entries, runtime changes, or student-facing content were created.

## Bereishis Perek 1 Protected-Preview Input-List Planning Policy

A protected-preview input-list planning policy now exists for the 133 approved Bereishis Perek 1 input candidates. This is policy only: no input list was created, no questions were generated, and protected preview remains a later gate.

Artifacts:

- `docs/question_templates/perek_1_protected_preview_input_list_planning_policy.md`
- `protected_preview_input_list_planning_policy.v1.json`
- `reports/perek_1_protected_preview_input_list_planning_policy_report.md`
- `reports/perek_1_protected_preview_input_list_planning_policy_yossi_review_packet.md`

Next action: Yossi reviews planning policy and Codex applies only reviewed planning-policy decisions in a separate task.

## Bereishis Perek 1 Planning Policy Review-Applied Status

Yossi reviewed the protected-preview input-list planning policy.

Review-applied artifact:

- `reports/perek_1_protected_preview_input_list_planning_policy_yossi_review_applied.md`

Decision: `approve_with_revision`.

Required revision: the future input-list planning task must include a batch balance table showing total selected input candidates, count by family, count by risk level, count by perek/pasuk range, duplicate Hebrew tokens if any, and the reason each direct-object-marker and shoresh row was included.

Future input-list planning may proceed under the stated constraints. This still does not create an input list or approve protected preview.

## Bereishis Perek 1 First Input-Candidate Planning Batch

The first protected-preview input-candidate planning batch exists in `data/protected_preview_input_planning/`. This is not a protected-preview input list and no questions were generated.

Artifacts:

- `data/protected_preview_input_planning/bereishis_perek_1_first_input_candidate_planning.tsv`
- `data/protected_preview_input_planning/reports/bereishis_perek_1_first_input_candidate_batch_balance_report.md`
- `data/protected_preview_input_planning/reports/bereishis_perek_1_first_input_candidate_planning_report.md`
- `data/protected_preview_input_planning/reports/bereishis_perek_1_first_input_candidate_yossi_review_sheet.md`
- `data/protected_preview_input_planning/reports/bereishis_perek_1_first_input_candidate_yossi_review_sheet.csv`

