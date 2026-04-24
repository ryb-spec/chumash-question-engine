# Merge Readiness: Inactive Infrastructure

## Branch

- current branch: `isolated/curriculum-extraction-factory`

## Latest Relevant Commits

- `9552293` Add supported-lane Batch 001 preview v2 and final decision report
- `49891f0` Enrich Batch 001 vocabulary glosses and document source-key blockers
- `ff5f394` Add Batch 001 source gap request
- `5e3bc77` Add Batch 001 answer enrichment report
- `31ef45b` Mark Batch 001 answer gaps explicitly
- `56efe04` Add Batch 001 preview question generation
- `62d763c` Finalize Batch 001 cleaned seed ingestion and review packet
- `37def86` Add isolated curriculum extraction factory and cleaned seed batch

## Validation Result

- command: `python scripts/validate_curriculum_extraction.py`
- result: PASS
- `valid: true`
- `schema_file_count: 11`
- `raw_source_file_count: 5`
- `sample_record_count: 30`
- `normalized_record_count: 75`
- `preview_file_count: 2`
- `preview_record_count: 310`

Preview files validated:

- `data/curriculum_extraction/generated_questions_preview/batch_001_preview.jsonl` — 155 questions
- `data/curriculum_extraction/generated_questions_preview/batch_001_preview_v2.jsonl` — 155 questions

## Loader Result

- command: `python scripts/load_curriculum_extraction.py --summary`
- result: PASS
- `integration_status: not_runtime_active`
- `runtime_active: false`
- `record_count: 105`
- loader continues to ignore preview-question artifacts safely

## Full Pytest Result

- command: `python -m pytest`
- result: PASS
- `453 passed`

## Preview Question Count

- current supported-lane preview artifact: `batch_001_preview_v2.jsonl`
- total preview questions in v2: `155`

## Supported Lanes

- `phrase_translation`
- `hebrew_to_english_match`
- `english_to_hebrew_match`
- `shoresh_identification` where source data exists
- `prefix_identification` where source data exists
- `suffix_identification` where source data exists
- vocab matching now that the 8 blocked Batch 001 vocab entries have source-backed glosses

## Blocked Lanes

- `mi_amar_el_mi`
  - blocked because the Va'eira comprehension records still do not have an explicit answer key in repo-local source material
- `al_mi_neemar`
  - blocked because the Va'eira comprehension records still do not have an explicit answer key in repo-local source material
- Shemos `word_parse_task` answer checking
  - blocked because the Shemos answer key is not present in this worktree

## Explicit Safety Statements

- Runtime integration remains blocked.
- The reviewed question bank remains untouched.
- Corpus scope remains unchanged.
- No active-scope expansion was performed.
- No UI, scoring, mastery, or runtime behavior changes were introduced.

## Recommendation

- Safe to merge into `main` as inactive infrastructure only.
- Not safe to connect to runtime yet.
- Future extraction should continue in separate, source-scoped batches with answer-bearing source material before any runtime consideration.
