# Batch 003 Preview Summary

- Batch ID: `batch_003_linear_bereishis_2_4_to_2_25`
- Preview file: `data/curriculum_extraction/generated_questions_preview/batch_003_preview.jsonl`
- Recommendation: `READY_FOR_MANUAL_REVIEW`

## Preview Question Counts By Type

- `phrase_translation`: `50`
- `hebrew_to_english_match`: `25`
- `english_to_hebrew_match`: `25`
- Total: `100`

## Supported Lanes

- `phrase_translation`
- `hebrew_to_english_match`
- `english_to_hebrew_match`

## Blocked Lanes

- `mi_amar_el_mi`: not applicable for this source batch
- `al_mi_neemar`: not applicable for this source batch
- `word_parse_task answer checking`: no answer-key task records in this batch
- `translation_rule_recognition`: no standalone source-backed `translation_rule` records were extracted in this range

## Comparison To Batch 002

- Batch 002 preview also produced `100` preview questions across the same three supported lanes.
- Batch 003 covers `Bereishis 2:4-2:25`, while Batch 002 covered `Bereishis 1:6-2:3`.
- Batch 003 extracted `90` source `pasuk_segment` records, compared with Batch 002's `123`.

## Weak Areas

- The source PDF still requires careful manual review because its text layer is noisy.
- Translation-rule extraction remains deferred in this range because explicit reusable rules were not clearly present.
