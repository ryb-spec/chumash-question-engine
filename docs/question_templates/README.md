# Question Template Policy Docs

This directory contains non-runtime question-template policy documents. These documents do not generate questions, answer choices, answer keys, protected-preview content, reviewed-bank entries, runtime data, or student-facing content.

## Documents

- `approved_question_template_policy.md`
- `perek_1_approved_input_candidate_wording_policy.md`
- `perek_1_protected_preview_input_list_planning_policy.md`

The Perek 1 wording policy defines safe future wording boundaries for already approved input candidates only. It does not approve protected preview or question generation.

The Perek 1 protected-preview input-list planning policy defines constraints for a future planning task only. It does not create an input list or generate questions.

Yossi reviewed the Perek 1 protected-preview input-list planning policy with decision `approve_with_revision`. Future input-list planning may proceed only with the required batch balance table and closed gates.

## Bereishis Perek 1 First-Batch Template-Skeleton Policy

- Policy: `docs/question_templates/perek_1_first_batch_template_skeleton_policy.md`

This policy is skeleton-planning only. It does not generate questions, answer choices, answer keys, protected-preview content, runtime data, or student-facing content.

## Bereishis Perek 1 Template-Skeleton Family Review Applied

- Review-applied report: `data/template_skeleton_planning/reports/bereishis_perek_1_first_batch_template_skeleton_yossi_review_applied.md`

Vocabulary skeletons are approved; noun/direct-object-marker/shoresh skeletons are approved with revision; verb-form skeletons remain deferred. No questions, answer choices, answer keys, protected-preview content, runtime data, or student-facing content were created.

## Bereishis Perek 1 First-Batch Exact Template Wording Policy

- Policy: `docs/question_templates/perek_1_first_batch_exact_template_wording_policy.md`

This policy contains non-student-facing exact wording patterns only. It does not create final questions, student-ready prompts, answer choices, answer keys, protected-preview content, runtime data, or student-facing content.

## Bereishis Perek 1 First-Batch Final Pre-Generation Policies

- Answer-key planning policy: `docs/question_templates/perek_1_first_batch_answer_key_planning_policy.md`
- Distractor planning policy: `docs/question_templates/perek_1_first_batch_distractor_planning_policy.md`
- Context-display/Hebrew policy: `docs/question_templates/perek_1_first_batch_context_display_hebrew_policy.md`

These policies do not create final questions, student-ready prompts, answer choices, answer keys, distractors, protected-preview content, runtime data, or student-facing content.

## First-batch answer/distractor/context policy review applied

- Answer/distractor/context policy review-applied report: `data/template_skeleton_planning/reports/bereishis_perek_1_first_batch_answer_distractor_context_policy_yossi_review_applied.md`
- Row-level review remains required before any generation.
- Generation remains blocked and all gates remain closed.

## Row-level pre-generation review

- Row-level pre-generation review layer: `data/pre_generation_review/README.md`
- Review TSV: `data/pre_generation_review/bereishis_perek_1_first_batch_pre_generation_review.tsv`
- This layer is review-only and does not generate questions, answers, distractors, protected-preview content, runtime data, or student-facing content.

## Controlled draft teacher-review packet

- Controlled draft layer: `data/controlled_draft_generation/README.md`
- First controlled draft TSV: `data/controlled_draft_generation/bereishis_perek_1_first_controlled_draft.tsv`
- Teacher review packet: `data/controlled_draft_generation/reports/bereishis_perek_1_first_controlled_draft_teacher_review_packet.md`
- This is teacher-review-only and not protected-preview, reviewed-bank, runtime, or student-facing content.
