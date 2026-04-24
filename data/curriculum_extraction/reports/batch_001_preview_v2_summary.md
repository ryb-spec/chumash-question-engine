# Batch 001 Preview V2 Summary

## Totals

- Total preview questions: 155
- Preview file: `data/curriculum_extraction/generated_questions_preview/batch_001_preview_v2.jsonl`

## Question Counts By Type

- phrase_translation: 50
- hebrew_to_english_match: 25
- english_to_hebrew_match: 25
- shoresh_identification: 25
- prefix_identification: 15
- suffix_identification: 15

## Comparison To V1 Preview

- V1 file kept for comparison: `data/curriculum_extraction/generated_questions_preview/batch_001_preview.jsonl`
- V1 total questions: 155
- V2 total questions: 155
- phrase_translation: v1=50, v2=50
- hebrew_to_english_match: v1=25, v2=25
- english_to_hebrew_match: v1=25, v2=25
- shoresh_identification: v1=25, v2=25
- prefix_identification: v1=15, v2=15
- suffix_identification: v1=15, v2=15

## Lanes Improved After Vocab Enrichment

- hebrew_to_english_match: unique Batch 001 vocab source coverage increased from 10 records in v1 to 18 in v2.
- english_to_hebrew_match: same expanded source coverage from 10 to 18 vocab records.
- Newly usable enriched vocab entries: ארץ, אדם, אשה, בית, בן, יום, מים, עץ.
- Distractor quality improved because the vocab matching pool now includes all 18 Batch 001 vocab entries.

## Lanes Still Blocked

- mi_amar_el_mi: deferred records=1; blocker=Va'eira comprehension questions still have no explicit answer key in repo-local sources.
- al_mi_neemar: deferred records=9; blocker=Va'eira comprehension questions still have no explicit answer key in repo-local sources.
- shemos_word_parse_task_answer_checking: deferred records=8; blocker=The Shemos prefix/suffix task answer key is still not present in the worktree, so task-answer checking remains deferred.

## Recommendation

- MERGE_INACTIVE_INFRASTRUCTURE as isolated extraction scaffolding and preview tooling.
- BLOCK_RUNTIME_INTEGRATION until explicit source answer keys exist for Va'eira comprehension and Shemos task-answer lanes.
