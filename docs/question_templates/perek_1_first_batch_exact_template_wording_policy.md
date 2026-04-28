# Bereishis Perek 1 First-Batch Exact Template Wording Policy

This policy defines exact non-student-facing wording patterns only.

These are template patterns only. They are not generated questions. They are not student-ready prompts. They are not answer choices. They are not answer keys. They do not create protected-preview input rows or protected-preview content.

## Allowed Families

- `vocabulary_meaning`
- `basic_noun_recognition`
- `direct_object_marker_recognition`
- `shoresh_identification`

## Deferred Family

`basic_verb_form_recognition` remains deferred. No exact wording patterns may be created for verb-form questions.

## vocabulary_meaning

Allowed non-student-facing wording patterns:

- `In this phrase, what does {hebrew_token} mean?`
- `Choose the basic meaning of {hebrew_token}.`
- `In this pasuk phrase, {hebrew_token} means ____.`

Required placeholders:

- `{hebrew_token}`
- `{hebrew_phrase}`
- `{approved_meaning}`
- `{context_display}`

Forbidden: full phrase translation, deeper interpretation, multiple vocabulary targets, unreviewed meanings, answer choices, answer keys.

## basic_noun_recognition

Allowed non-student-facing wording patterns:

- `Which word in this phrase is a noun?`
- `What type of word is {hebrew_token}?`
- `{hebrew_token} names a person/place/thing. What type of word is it?`

Required placeholders:

- `{hebrew_token}`
- `{hebrew_phrase}`
- `{noun_category_review}`

Required revision language: wording must stay simple: noun/object/person/place/thing only; no advanced grammar labels; no construct/suffix/adjective/advanced part-of-speech claims.

Forbidden: advanced grammar labels, construct/suffix claims, adjective/verb distinctions unless separately reviewed, answer choices, answer keys.

## direct_object_marker_recognition

Allowed non-student-facing wording patterns:

- `What is the job of את in this phrase?`
- `Which word marks the direct object?`
- `In this phrase, את points to the object receiving the action.`

Required placeholders:

- `{hebrew_token}`
- `{hebrew_phrase}`
- `{function_wording_review}`

Required revision language: ask about function, not translation; do not ask "What does את mean?"; do not translate את as "the"; do not translate את as "with".

Forbidden: asking "What does את mean?", translating את as "the", translating את as "with", mixing with prefix or conjunction analysis, answer choices, answer keys.

## shoresh_identification

Allowed non-student-facing wording patterns:

- `What is the shoresh of {hebrew_token}?`
- `Which root letters are inside {hebrew_token}?`
- `Identify the shoresh for this reviewed word: {hebrew_token}.`

Required placeholders:

- `{hebrew_token}`
- `{target_shoresh}`
- `{shoresh_review_status}`

Required revision language: surface word and target shoresh must be clearly separated; for `הבדיל`, target shoresh is `בדל`; do not imply `הבדיל` itself is the shoresh.

Forbidden: unresolved roots, compound/suffix-heavy forms, advanced binyan/stem questions, answer choices, answer keys.

## Safety Boundary

No final questions, student-ready prompts, answer choices, answer keys, protected-preview input rows, protected-preview content, reviewed-bank entries, runtime data, or student-facing content are created by this policy.

## Yossi Exact-Wording Family Review Status

- `vocabulary_meaning`: approve_exact_wording_family.
- `basic_noun_recognition`: approve_with_revision.
- `direct_object_marker_recognition`: approve_with_revision.
- `shoresh_identification`: approve_with_revision.
- `basic_verb_form_recognition`: needs_follow_up / keep deferred.

### Required Revisions

For `basic_noun_recognition`:

- Wording must stay simple: noun/object/person/place/thing.
- Do not use advanced grammar labels.
- Do not ask about construct, suffix, adjective, or advanced part-of-speech distinctions.

For `direct_object_marker_recognition`:

- Wording must ask about the function of `את`.
- Do not ask "What does את mean?"
- Do not translate `את` as "the."
- Do not translate `את` as "with."
- Exact final wording still needs teacher review.

For `shoresh_identification`:

- Wording must separate surface word from target shoresh.
- For `ppplan_b1_024` / `הבדיל`, the target shoresh is `בדל`.
- Do not imply `הבדיל` itself is the shoresh.
- Exact final wording and answer-key language still need teacher review.

For `basic_verb_form_recognition`:

- Remains deferred.
- No verb-form exact wording, answer-key, distractor, protected-preview, or runtime planning may proceed.

These decisions do not approve final questions, student-ready prompts, answer choices, answer keys, protected-preview content, reviewed-bank use, runtime use, or student-facing use.
