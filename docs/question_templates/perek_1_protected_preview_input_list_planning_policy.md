# Bereishis Perek 1 Protected-Preview Input-List Planning Policy

## Status And Boundaries

This document is a planning policy only. It does not create a protected-preview input list. It does not generate questions. It does not generate answer choices. It does not generate answer keys. It does not create protected-preview content, approve reviewed-bank use, approve runtime use, or approve student-facing use.

This policy defines constraints that a future protected-preview input-list planning task must obey. It does not approve any candidate for protected-preview generation.

## Yossi Review Decision

Decision: `approve_with_revision`.

Future input-list planning may proceed under the constraints in this policy. The required revision is that the future input-list planning task must include a batch balance table showing:

- total selected input candidates
- count by family
- count by risk level
- count by perek/pasuk range
- duplicate Hebrew tokens, if any
- reason each direct-object-marker row was included
- reason each shoresh row was included

The first batch remains limited to 20-30 input candidates. Direct-object-marker rows remain capped to a small sample. Shoresh rows remain capped to 1-3 rows. Verb-form rows remain deferred.

This decision still does not create a protected-preview input list and still does not generate questions.

## Eligible Source Rows For A Future Planning Task

Only rows may be considered if all of the following are true:

- The row appears in `data/question_eligibility_audits/reports/bereishis_perek_1_approved_input_candidate_planning_sheet.csv`.
- The row's family policy is approved.
- The row's family is one of `vocabulary_meaning`, `basic_noun_recognition`, `direct_object_marker_recognition`, or `shoresh_identification`.
- The row is not `basic_verb_form_recognition`.
- The row is not `source_only`.
- The row is not `needs_follow_up`.
- The row is not `block_for_questions`.
- Future wording review is still required.

## Required Future Input-List Fields

A future protected-preview input-list candidate file must include these fields:

- `input_candidate_id`
- `audit_id`
- `ref`
- `hebrew_token`
- `hebrew_phrase`
- `approved_family`
- `canonical_skill_id`
- `canonical_standard_anchor`
- `source_candidate_type`
- `risk_level`
- `risk_reasons`
- `required_template_family`
- `wording_policy_version`
- `teacher_wording_review_status`
- `answer_key_review_status`
- `distractor_review_status`
- `context_display_review_status`
- `protected_preview_candidate_status`
- `protected_preview_allowed`
- `reviewed_bank_allowed`
- `runtime_allowed`
- `student_facing_allowed`
- `notes`

Required default statuses:

- `teacher_wording_review_status = needs_review`
- `answer_key_review_status = needs_review`
- `distractor_review_status = needs_review`
- `context_display_review_status = needs_review`
- `protected_preview_candidate_status = planning_only`
- `protected_preview_allowed = false`
- `reviewed_bank_allowed = false`
- `runtime_allowed = false`
- `student_facing_allowed = false`

## First Protected-Preview Input-List Balance Rules

A conservative first planning batch should use these constraints:

- Total suggested size: 20-30 input candidates.
- Prioritize low-risk rows.
- Prioritize `vocabulary_meaning` and `basic_noun_recognition`.
- Include only a small sample of `direct_object_marker_recognition`.
- Include only 1-3 `shoresh_identification` rows.
- Exclude all verb-form rows.
- Avoid duplicate Hebrew tokens unless intentionally reviewing repetition.
- Avoid emotionally or theologically sensitive phrases.
- Avoid broad phrase-level rows.
- Avoid high-risk rows.
- Avoid rows requiring advanced morphology.
- Preserve perek/pasuk spread if possible.

## Family-Specific Planning Constraints

### `vocabulary_meaning`

- One token only.
- One reviewed meaning only.
- Context phrase optional.
- No full phrase translation.

### `basic_noun_recognition`

- Token must be a clean noun/object/person/place/thing candidate.
- No construct/suffix-sensitive forms unless separately approved.
- No advanced parts of speech.

### `direct_object_marker_recognition`

- Must ask function, not translation.
- Must not translate `את` as "the" or "with."
- Must require exact wording review.
- Small batch only.

### `shoresh_identification`

- Clean root only.
- No compound/root-sensitive forms.
- Exact root letters must be reviewed.

### `basic_verb_form_recognition`

- Explicitly deferred.
- No input list rows allowed yet.

## Required Later Review Gates

Before protected-preview generation, all of these later gates are required:

- exact template wording review
- answer key review
- distractor-bank review
- context-display review
- Hebrew rendering review
- teacher approval
- protected-preview gate approval

## Forbidden Outputs

This policy forbids:

- actual questions
- answer choices
- answer keys
- protected-preview input rows
- protected-preview generation
- reviewed-bank entries
- runtime data
- student-facing content

## Next Required Action

Yossi reviews this planning policy. Only after a separate review-applied task may Codex create a future planning-layer candidate file, and that future file still may not generate questions or protected-preview content without another gate.
