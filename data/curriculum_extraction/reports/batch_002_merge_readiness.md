# Batch 002 Merge Readiness

## Branch

- Branch: `feature/curriculum-batch-002-linear-bereishis`

## Batch Scope

- Source package: `linear_chumash_translation`
- Source name: `Linear Chumash Translation for Most Parshiyos in Torah`
- Source range: `Bereishis 1:6 through Bereishis 2:3`
- Raw source excerpt: `data/curriculum_extraction/raw_sources/batch_002/linear_chumash_bereishis_1_6_to_2_3_cleaned.md`

## Record Counts

- `pasuk_segment`: `123`
- `translation_rule`: `0`
- Distinct pesukim covered: `29`

## Preview Question Counts

- `phrase_translation`: `50`
- `hebrew_to_english_match`: `25`
- `english_to_hebrew_match`: `25`
- Total preview questions: `100`

## Validation Result

- `python scripts/validate_curriculum_extraction.py` - PASS
- Validator summary:
  - `valid: true`
  - `normalized_record_count: 198`
  - `record_count: 228`
  - `preview_record_count: 410`

## Loader Result

- `python scripts/load_curriculum_extraction.py --summary` - PASS
- Loader remains isolated from preview and Batch 002 extraction data:
  - `integration_status: not_runtime_active`
  - `runtime_active: false`
  - `normalized_record_count: 75`
  - `record_count: 105`

## Pytest Result

- `python -m pytest` - PASS
- Full suite result: `467 passed`

## Manual Review Status

- Manual review packet created and reviewer-edited version applied:
  - `data/curriculum_extraction/reports/batch_002_manual_review_packet.md`
- Manual review is complete for merge-readiness purposes.
- Batch 002 extraction records remain inactive and unchanged by manual review.

## Supported Lanes

- `phrase_translation`
- `hebrew_to_english_match`
- `english_to_hebrew_match`

## Blocked / Deferred Lanes

- `mi_amar_el_mi`: deferred because this batch extracts translation/context records only.
- `al_mi_neemar`: deferred because this batch extracts translation/context records only.
- `word_parse_task` answer checking: deferred because this batch contains no answer-key-backed parse-task records.
- `translation_rule_recognition`: deferred because no standalone `translation_rule` records were extracted for this range.

## Inactive Infrastructure Guardrails

- Runtime remains untouched.
- Reviewed question bank remains untouched.
- Corpus scope remains unchanged.
- Nothing in this batch is runtime-active.
- Nothing in this batch is promoted live.

## Recommendation

- `MERGE_INACTIVE_BATCH_002`

Batch 002 is safe to merge into `main` as inactive curriculum extraction infrastructure. It is not safe for runtime integration, reviewed-question-bank promotion, or corpus promotion from this branch.
