# Batch 001 Cleaned Seed Summary

## Files Ingested

Raw cleaned markdown files:

- `data/curriculum_extraction/raw_sources/batch_001/linear_chumash_bereishis_1_1_to_1_5_cleaned.md`
- `data/curriculum_extraction/raw_sources/batch_001/pasuk_coming_to_teach_sample_answer_key_cleaned.md`
- `data/curriculum_extraction/raw_sources/batch_001/bacharach_shemos_prefix_suffix_perek_1_1_to_7_cleaned.md`
- `data/curriculum_extraction/raw_sources/batch_001/bacharach_vaeira_textual_skills_perek_6_cleaned.md`
- `data/curriculum_extraction/raw_sources/batch_001/vocabulary_priority_pack_cleaned.md`

Normalized seed files:

- `data/curriculum_extraction/normalized/linear_chumash_bereishis_1_1_to_1_5_pasuk_segments.seed.jsonl`
- `data/curriculum_extraction/normalized/linear_chumash_translation_rules.seed.jsonl`
- `data/curriculum_extraction/normalized/pasuk_coming_to_teach_word_parse.seed.jsonl`
- `data/curriculum_extraction/normalized/bacharach_shemos_prefix_suffix_tasks.seed.jsonl`
- `data/curriculum_extraction/normalized/bacharach_vaeira_comprehension_questions.seed.jsonl`
- `data/curriculum_extraction/normalized/vocabulary_priority_pack.seed.jsonl`

## Batch Status

Batch 001 is now manually reviewed for isolated non-runtime use. It remains outside runtime and outside the active reviewed question bank.

## Record Counts By Record Type

- `pasuk_segment`: 23
- `translation_rule`: 6
- `word_parse`: 10
- `word_parse_task`: 8
- `comprehension_question`: 10
- `vocab_entry`: 18

Total normalized Batch 001 records: 75

## Source Packages Represented

- `eli_bacharach_parshas_shemos_shorashim_prefix_suffix_skills`: 8
- `eli_bacharach_parshas_vaeira_textual_skills`: 10
- `linear_chumash_translation_most_parshiyos_in_torah`: 29
- `vocabulary_priority_pack`: 18
- `what_is_the_pasuk_coming_to_teach`: 10

## Review Status Summary

- `reviewed`: 75

## Runtime Status Summary

- `not_runtime_active`: 75

## Extraction Risks

- Batch 001 is manually reviewed for isolated non-runtime use, but it is still not a runtime-approved batch.
- The cleaned markdown excerpts are partial source traces, not full source PDFs.
- Some vocabulary records still have empty `english_glosses` and remain explicitly flagged with `needs_gloss_review = true`.
- Some `word_parse_task` records do not have source-provided answers and correctly remain `answer_status = not_extracted`.
- These records remain isolated only and must not be wired into runtime or the reviewed question bank from this branch.

## Next Recommended Step

If desired, use this reviewed non-runtime batch to build preview-generation scaffolding outside runtime, or ingest the next cleaned batch with the same isolated review workflow.
