# Batch 002 Preview Summary

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

- `mi_amar_el_mi`: deferred because this translation-only batch does not extract comprehension-answer records.
- `al_mi_neemar`: deferred because this translation-only batch does not extract comprehension-answer records.
- `word_parse_task` answer checking: deferred because this batch does not contain answer-key-backed parse-task records.
- `translation_rule_recognition`: deferred because no standalone `translation_rule` records were extracted for this range.

## Comparison To Batch 001

- Batch 001 preview v2 produced `155` questions across six supported lanes.
- Batch 002 preview produced `100` questions across three translation-only lanes.
- Batch 002 intentionally omits vocab, word-parse, prefix/suffix, and comprehension lanes because those source types are not part of this extraction batch.

## Weak Data Areas

- The source PDF text layer is noisy on the Hebrew side, so phrase-level Hebrew alignment depends on the local canonical pasuk corpus.
- Some source translations include embedded teaching clarifications, so answers remain source-shaped rather than smoothed into polished English.

## Recommendation

- `READY_FOR_MANUAL_REVIEW`
- Human review should check the phrase boundaries, the Hebrew alignment, and the source-shaped English wording before any future reuse in later isolated extraction batches.
