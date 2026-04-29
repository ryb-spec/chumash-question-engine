# Template Skeleton Planning

This layer is template-skeleton planning only.

It does not generate questions. It does not generate student-ready prompts. It does not generate answer choices. It does not generate answer keys. It does not create protected-preview input rows or protected-preview content. It does not approve reviewed-bank use, runtime use, or student-facing use.

Every skeleton still needs teacher wording review, answer-key review, distractor review, context-display review, Hebrew-rendering review, and protected-preview gate review.

## Bereishis Perek 1 First Batch

- Policy document: `docs/question_templates/perek_1_first_batch_template_skeleton_policy.md`
- Policy JSON: `data/template_skeleton_planning/template_skeleton_policy.v1.json`
- Planning TSV: `data/template_skeleton_planning/bereishis_perek_1_first_batch_template_skeleton_planning.tsv`
- Yossi review packet: `data/template_skeleton_planning/reports/bereishis_perek_1_first_batch_template_skeleton_yossi_review_packet.md`
- Planning report: `data/template_skeleton_planning/reports/bereishis_perek_1_first_batch_template_skeleton_planning_report.md`

Status: 24 rows created for skeleton planning only. All gates remain closed.

Next action: Yossi reviews the template-skeleton family packet.

## Yossi Skeleton-Family Review Applied

Yossi skeleton-family decisions were applied for the 24 first-batch template-skeleton planning rows.

- Review-applied report: `data/template_skeleton_planning/reports/bereishis_perek_1_first_batch_template_skeleton_yossi_review_applied.md`
- `vocabulary_meaning`: approve_skeleton_family
- `basic_noun_recognition`: approve_with_revision
- `direct_object_marker_recognition`: approve_with_revision
- `shoresh_identification`: approve_with_revision
- `basic_verb_form_recognition`: needs_follow_up / deferred

Exact non-student-facing template wording is the next step. No questions were generated. All gates remain closed.

## Exact Template Wording Planning

The first-batch exact template wording planning layer exists for the 24 template-skeleton rows.

- Exact wording policy: `docs/question_templates/perek_1_first_batch_exact_template_wording_policy.md`
- Exact wording JSON: `data/template_skeleton_planning/exact_template_wording_policy.v1.json`
- Exact wording planning TSV: `data/template_skeleton_planning/bereishis_perek_1_first_batch_exact_template_wording_planning.tsv`
- Exact wording Yossi review packet: `data/template_skeleton_planning/reports/bereishis_perek_1_first_batch_exact_template_wording_yossi_review_packet.md`
- Exact wording planning report: `data/template_skeleton_planning/reports/bereishis_perek_1_first_batch_exact_template_wording_planning_report.md`

These are non-student-facing wording patterns only. No final questions, student-ready prompts, answer choices, answer keys, protected-preview input rows, protected-preview content, reviewed-bank entries, runtime data, or student-facing content were created.

## Final Pre-Generation Policy Layer

Exact wording family decisions were applied and the final pre-generation policy layer was created.

- Exact wording review-applied report: `data/template_skeleton_planning/reports/bereishis_perek_1_first_batch_exact_template_wording_yossi_review_applied.md`
- Answer-key policy: `docs/question_templates/perek_1_first_batch_answer_key_planning_policy.md`
- Answer-key JSON: `data/template_skeleton_planning/answer_key_planning_policy.v1.json`
- Distractor policy: `docs/question_templates/perek_1_first_batch_distractor_planning_policy.md`
- Distractor JSON: `data/template_skeleton_planning/distractor_planning_policy.v1.json`
- Context-display/Hebrew policy: `docs/question_templates/perek_1_first_batch_context_display_hebrew_policy.md`
- Context-display/Hebrew JSON: `data/template_skeleton_planning/context_display_hebrew_policy.v1.json`
- Pre-generation readiness report: `data/template_skeleton_planning/reports/bereishis_perek_1_first_batch_pre_generation_readiness_report.md`
- Yossi policy review packet: `data/template_skeleton_planning/reports/bereishis_perek_1_first_batch_answer_distractor_context_policy_yossi_review_packet.md`

No final questions, student-ready prompts, answer choices, answer keys, distractors, protected-preview input rows, protected-preview content, reviewed-bank entries, runtime data, or student-facing content were created. All gates remain closed.

## First-batch answer/distractor/context policy review applied

- Status: Yossi policy decisions applied for answer-key, distractor, context-display/Hebrew-rendering, and pre-generation readiness policies.
- Review-applied report: `data/template_skeleton_planning/reports/bereishis_perek_1_first_batch_answer_distractor_context_policy_yossi_review_applied.md`
- Answer-key planning policy: `approve_with_revision`.
- Distractor planning policy: `approve_with_revision`.
- Context-display/Hebrew-rendering policy: `approve_policy`.
- Pre-generation readiness checklist: `approve_with_revision`.
- Row-level review is required before generation for exact wording, answer-key language, distractor constraints, context display, Hebrew rendering, and protected-preview gate status.
- Generation is still blocked; no questions, answer choices, answer keys, distractors, protected-preview content, reviewed-bank entries, runtime data, or student-facing content were created.

## Row-level pre-generation review layer

- Status: row-level pre-generation Yossi review sheet created.
- Review layer README: `data/pre_generation_review/README.md`
- Review TSV: `data/pre_generation_review/bereishis_perek_1_first_batch_pre_generation_review.tsv`
- Yossi review sheet: `data/pre_generation_review/reports/bereishis_perek_1_first_batch_pre_generation_yossi_review_sheet.md`
- Review report: `data/pre_generation_review/reports/bereishis_perek_1_first_batch_pre_generation_review_report.md`
- All rows remain blocked pending row-level review; no generation gates were opened.

## Row-level pre-generation review decisions applied

- Review-applied report: `data/pre_generation_review/reports/bereishis_perek_1_first_batch_pre_generation_yossi_review_applied.md`
- Direct approvals for future controlled draft-generation planning only: 19
- Approved with revision: 5
- No generation gates were opened.

## Controlled draft teacher-review packet

- Controlled draft layer: `data/controlled_draft_generation/README.md`
- First controlled draft TSV: `data/controlled_draft_generation/bereishis_perek_1_first_controlled_draft.tsv`
- Teacher review packet: `data/controlled_draft_generation/reports/bereishis_perek_1_first_controlled_draft_teacher_review_packet.md`
- This is teacher-review-only and not protected-preview, reviewed-bank, runtime, or student-facing content.
