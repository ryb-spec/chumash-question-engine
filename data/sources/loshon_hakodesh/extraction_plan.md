# Loshon Hakodesh Rule Extraction Plan

## Current Branch Scope

This branch is limited to protected source ingestion, provenance, indexing, lesson pairing, and planning.

It does not:
- modify runtime behavior
- generate production questions
- expose answer-booklet content to students
- promote protected source text into app-facing data

## Next Recommended Branch

`feature/loshon-hakodesh-rule-extraction`

## Next Branch Goal

Extract the main textbook's lesson-by-lesson rule sequence into a machine-readable skill and rule schema, then use the answer booklet only to validate exercise-answer alignment.

Use the cleaner 33-page answer-booklet OCR metadata source as the preferred teacher-only validation reference. Keep any answer-booklet extraction protected and out of runtime/student-facing content.

## Proposed Rule Schema Fields

- `rule_id`
- `lesson_number`
- `rule_title`
- `rule_group`
- `student_facing_summary`
- `technical_summary`
- `hebrew_markers`
- `english_meaning`
- `example_forms`
- `counterexamples`
- `exceptions_or_warnings`
- `zekelman_standard_alignment`
- `ocr_confidence`
- `source_trace`
- `human_review_status`

## Proposed Exercise Schema Fields

- `exercise_id`
- `lesson_number`
- `exercise_number`
- `exercise_type`
- `prompt_summary`
- `target_skill_ids`
- `source_page`
- `answer_page`
- `hebrew_surface_forms`
- `translation_dependency`
- `teacher_only_validation_needed`
- `ocr_confidence`
- `source_trace`

## Proposed Teacher-Only Answer Validation Fields

- `exercise_id`
- `expected_answer_summary`
- `expected_answer_hebrew`
- `expected_answer_english`
- `alternate_acceptable_answers`
- `answer_source_page`
- `validation_notes`
- `student_facing_allowed` set to `false`
- `teacher_only` set to `true`
- `human_review_status`

## Zekelman Standard 3 Alignment Approach

- start with rule-to-standard alignment at the lesson level
- map Loshon Hakodesh lessons into Standard 3 categories such as:
  - vocabulary
  - parts of speech
  - syntax
  - verb forms
  - word-building / affixes
- avoid claiming exact one-to-one alignment until the lesson rules are human-reviewed

## OCR Review Workflow

1. Use OCR text only as a draft locator.
2. Compare rule and exercise extraction against page images or protected PDFs.
3. Mark low-confidence Hebrew, punctuation, arrows, tables, and layout-sensitive sections for manual review.
4. Do not treat extracted answer text as final until teacher-reviewed.

## Human Review Requirements

- verify each lesson boundary
- verify each rule title and explanation
- verify each exercise prompt before any structured reuse
- verify answer-booklet alignments
- review any generated derived skill labels before downstream use

## What Must Remain Out Of Runtime / Student-Facing Content

- full textbook pages
- full answer-booklet pages
- answer-key dumps
- OCR-only answer banks
- unreviewed protected-source excerpts
