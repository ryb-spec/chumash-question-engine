# Bereishis Perek 1 First Controlled Draft Generation Report

## Source

- Source row-level review file: `data/pre_generation_review/bereishis_perek_1_first_batch_pre_generation_review.tsv`

## Counts

- Generated draft count: 19
- Skipped revision-required count: 5

## Family counts

- `basic_noun_recognition`: 9
- `shoresh_identification`: 1
- `vocabulary_meaning`: 9

## Risk/caution summary

- Direct-object-marker rows were skipped because they require revision.
- `הבדיל` / `בדל` row was skipped because it requires revision.
- Article/prefix rows `המים` and `האדמה` were skipped because answer-key wording requires revision.

## Hebrew integrity check

All draft rows use real UTF-8 Hebrew and no placeholder corruption. Required Hebrew anchors include `את`, `הבדיל`, `בדל`, `המים`, `האדמה`, and `הארץ` in reports where applicable.

## What was generated

Teacher-review-only controlled draft prompts, answer choices, expected answers, explanations, and evidence notes for 19 direct-approved rows.

## What was not approved

No protected-preview release content, reviewed-bank entries, runtime data, or student-facing content were approved.

## Gates

All draft rows have `protected_preview_allowed = false`, `reviewed_bank_allowed = false`, `runtime_allowed = false`, and `student_facing_allowed = false`.

## Next review task

Yossi/teacher review of the controlled draft packet.
