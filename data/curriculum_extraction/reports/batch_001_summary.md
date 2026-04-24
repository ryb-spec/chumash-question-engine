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

## Record Counts By Record Type

- `pasuk_segment`: 23
- `translation_rule`: 6
- `word_parse`: 10
- `word_parse_task`: 8
- `comprehension_question`: 10
- `vocab_entry`: 18

Total normalized Batch 001 records: 75

## Source Packages Represented

- `linear_chumash_translation_most_parshiyos_in_torah`: 29
- `what_is_the_pasuk_coming_to_teach`: 10
- `eli_bacharach_parshas_shemos_shorashim_prefix_suffix_skills`: 8
- `eli_bacharach_parshas_vaeira_textual_skills`: 10
- `vocabulary_priority_pack`: 18

## Review Status Summary

- `needs_review`: 75

## Runtime Status Summary

- `not_runtime_active`: 75

## Extraction Risks

- Batch 001 is a cleaned seed ingest only, not a reviewed production batch.
- The cleaned markdown excerpts are partial source traces, not full source PDFs.
- Some vocabulary records still have empty `english_glosses` and are explicitly flagged with `needs_gloss_review = true`.
- Some `word_parse_task` records do not have source-provided answers and remain `answer_status = not_extracted`.
- These records are isolated only and must not be wired into runtime or the reviewed question bank from this branch.

## Next Recommended Step

Run a manual review pass over the Batch 001 normalized records, especially gloss gaps and task records without source-provided answers, before any preview-generation or integration planning work.
