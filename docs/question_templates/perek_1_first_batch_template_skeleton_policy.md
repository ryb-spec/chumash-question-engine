# Bereishis Perek 1 First-Batch Template-Skeleton Policy

This document defines template-skeleton planning rules only.

It does not generate questions. It does not generate student-ready prompts. It does not generate answer choices. It does not generate answer keys. It does not create protected-preview input rows or protected-preview content. It does not approve reviewed-bank use, runtime use, or student-facing use.

Every skeleton still needs teacher wording review, answer-key review, distractor review, context-display review, Hebrew-rendering review, and protected-preview gate review.

## Approved Families

- `vocabulary_meaning`
- `basic_noun_recognition`
- `direct_object_marker_recognition`
- `shoresh_identification`

## Deferred Family

`basic_verb_form_recognition` remains deferred. No verb-form skeletons may be created.

## vocabulary_meaning

Purpose: plan a non-student-facing skeleton for the meaning of one reviewed Hebrew token.

Allowed non-student-facing skeleton shape:

- Meaning-of-single-reviewed-token skeleton.
- Context phrase may be displayed later, but context-display review is required.
- No answer choices or answer key in this task.

Required variables:

- `{hebrew_token}`
- `{hebrew_phrase}`
- `{approved_family}`
- `{meaning_review_status}`
- `{context_display_review_status}`

Forbidden wording:

- No full phrase translation.
- No deeper interpretation.
- No multiple vocabulary targets.
- No unreviewed meanings.
- No answer choices.
- No answer key.

Required review gates: teacher wording, answer key, distractor, context display, Hebrew rendering, protected-preview gate.

Cautions: article/prefix vocabulary rows such as `המים`, `האדמה`, or `הארץ` need later answer-key review to decide base meaning vs article-inclusive meaning.

## basic_noun_recognition

Purpose: plan a non-student-facing skeleton for recognizing a reviewed token as a noun/object/person/place/thing.

Allowed non-student-facing skeleton shape:

- Basic noun-token recognition skeleton.
- Must stay simple and level-appropriate.
- No advanced parts of speech.

Required variables:

- `{hebrew_token}`
- `{hebrew_phrase}`
- `{noun_review_status}`
- `{context_display_review_status}`

Forbidden wording:

- No construct/suffix-sensitive claims unless separately reviewed.
- No adjectives or verbs unless separately reviewed.
- No advanced grammar labels.
- No answer choices.
- No answer key.

Required review gates: teacher wording, answer key, distractor, context display, Hebrew rendering, protected-preview gate.

Cautions: do not treat every vocabulary token as automatically safe for noun recognition.

## direct_object_marker_recognition

Purpose: plan a non-student-facing skeleton for the function of `את` as a direct-object marker.

Allowed non-student-facing skeleton shape:

- Direct-object-marker function skeleton.
- Must use function wording only.

Required variables:

- `{hebrew_token}`
- `{hebrew_phrase}`
- `{function_review_status}`
- `{wording_review_status}`

Forbidden wording:

- Do not ask what `את` means as a simple translation.
- Do not translate `את` as "the".
- Do not translate `את` as "with".
- Do not mix with prefix/conjunction analysis.
- No answer choices.
- No answer key.

Required review gates: teacher wording, answer key, distractor, context display, Hebrew rendering, protected-preview gate.

Cautions: Function wording only; do not ask what `את` means as a simple translation.

## shoresh_identification

Purpose: plan a non-student-facing skeleton for the shoresh/root of one reviewed token.

Allowed non-student-facing skeleton shape:

- Single-token shoresh identification skeleton.
- Must identify the target root separately from the surface token.

Required variables:

- `{hebrew_token}`
- `{target_shoresh}`
- `{shoresh_review_status}`
- `{wording_review_status}`

Forbidden wording:

- No unresolved compound forms.
- No advanced binyan/stem.
- No prefix/suffix-heavy forms without review.
- No answer choices.
- No answer key.

Required review gates: teacher wording, answer key, distractor, context display, Hebrew rendering, protected-preview gate.

Cautions: for `הבדיל`, target shoresh is `בדל`; surface token is `הבדיל`.

## Yossi Skeleton-Family Review Status

- `vocabulary_meaning`: vocabulary skeleton family approved.
- `basic_noun_recognition`: noun recognition approved with revision.
- `direct_object_marker_recognition`: direct-object-marker approved with revision.
- `shoresh_identification`: shoresh identification approved with revision.
- `basic_verb_form_recognition`: verb-form recognition remains deferred.

### Required Revisions

For `basic_noun_recognition`:

- Future exact wording must stay simple: noun/object/person/place/thing.
- Do not use advanced grammar labels.
- Do not ask about construct, suffix, adjective, or advanced part-of-speech distinctions.

For `direct_object_marker_recognition`:

- Future exact wording must ask about the function of `את`.
- Do not ask "What does את mean?"
- Do not translate `את` as "the" or "with."
- All `את` rows still require teacher wording review.

For `shoresh_identification`:

- Future exact wording must clearly separate the surface word from the target shoresh.
- For `ppplan_b1_024` / `הבדיל`, the target shoresh is `בדל`.
- Do not imply `הבדיל` itself is the shoresh.
- All shoresh rows still require teacher wording review and answer-key review.

For `basic_verb_form_recognition`:

- Keep deferred.
- No verb-form skeletons may be approved until a separate morphology-question wording standard exists.

These decisions do not approve questions, student-ready prompts, answer choices, answer keys, protected-preview content, reviewed-bank use, runtime use, or student-facing use.
