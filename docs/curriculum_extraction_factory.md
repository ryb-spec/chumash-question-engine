# Curriculum Extraction Factory

## What This Is

This branch holds an isolated curriculum extraction factory scaffold. It is a contract layer for organizing curriculum-source data into explicit records, schemas, validation checks, sample files, normalized seed ingests, and loader views before any runtime connection is considered.

## Why It Exists

The live Chumash engine should not absorb extraction data directly from loosely structured source material. This factory creates a safer intermediate lane where source traces, review flags, confidence levels, and record types can be organized and checked before anything is proposed for runtime use.

## Modeled Resource Packages

1. Linear Chumash Translation for Most Parshiyos in Torah
2. What is the Pasuk Coming to Teach?
3. Eli Bacharach: Parshas Shemos Shorashim, Prefix and Suffix Skills
4. Eli Bacharach: Parshas Va'eira Textual Skills
5. Vocabulary Priority Pack
6. First 150 Shorashim and Keywords in Bereishis

The first five are the main modeled packages. The sixth is present as optional vocabulary/translation support.

## Schemas

Phase 1 defines JSON schemas for:

- `source_trace`
- `pasuk_segment`
- `word_parse`
- `word_parse_task`
- `vocab_entry`
- `comprehension_question`
- `question_template`
- `skill_tag`
- `translation_rule`
- `generated_question_preview`
- `extraction_batch_report`

These schemas are still draft scaffolds. They provide the contract shape for later reviewed extraction work.

## Validator

`scripts/validate_curriculum_extraction.py` uses only standard Python libraries and checks:

- manifest and registry load correctly
- schema files exist and are valid JSON
- sample and normalized JSONL records parse correctly
- every record includes `source_package_id` and `source_trace`
- every record stays `needs_review`, `not_runtime_active`, and below `high` confidence
- no record is treated as reviewed or runtime-active
- skill tag references resolve
- ids are unique
- record-type required fields are present
- answer-status rules are respected
- batch raw-source and normalized file declarations exist
- optional git-diff checking can fail if anything outside the isolated allowlist was changed

## Loader

`scripts/load_curriculum_extraction.py` is a read-only loader that:

- reads the manifest
- loads sample records
- loads normalized records declared in the manifest
- groups records by source package
- groups records by skill
- groups pasuk-based records by `sefer/perek/pasuk`
- returns records for a specific pasuk or skill

It does not import runtime code and it does not write any files.

## Sample Records

Phase 1 intentionally includes only tiny manual samples:

- 3 `pasuk_segment`
- 3 `word_parse`
- 3 `word_parse_task`
- 3 `vocab_entry`
- 3 `comprehension_question`
- 5 `question_template`
- 8 `skill_tag`
- 2 `translation_rule`

These are modeled contract samples only. They are not Batch 001 extraction data.

## Batch 001 Cleaned Seed Ingestion

Phase 2 ingests a cleaned seed packet into the same isolated lane without connecting anything to runtime.

- cleaned markdown excerpts live under `data/curriculum_extraction/raw_sources/batch_001/`
- normalized seed JSONL lives under `data/curriculum_extraction/normalized/`
- the manifest records the batch as `batch_001_cleaned_seed`
- every ingested record remains `needs_review` and `not_runtime_active`
- the batch summary report lives at `data/curriculum_extraction/reports/batch_001_summary.md`

These records are still seed material only. They are not production-reviewed content, not generated questions, and not reviewed-bank data.

## What Is Not Live

Nothing in this branch is runtime active.

- No runtime file is modified.
- No active product behavior is changed.
- No corpus slice is promoted.
- No data is written into the reviewed question bank.
- No generated question preview pipeline is connected.

## Phase 2 Should Do Next

Phase 3 should stay outside runtime as well and focus on:

1. manual review of the Batch 001 normalized records
2. extraction batch report refinement and reviewer notes
3. richer normalization-field consistency checks where the cleaned seeds are thin
4. generated question preview scaffolding outside runtime
5. manual review workflow definitions for extracted records

Runtime integration should happen only on a later, explicit integration branch after review gates are satisfied.
