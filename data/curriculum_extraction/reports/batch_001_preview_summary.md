# Batch 001 Preview Summary

## Totals

- Total question count: 155
- Skipped source record count: 26
- Skipped requested question slots: 20
- Usable source records: 43 / 69 (62.3%)

## Count By Type

- phrase_translation: 50
- hebrew_to_english_match: 25
- english_to_hebrew_match: 25
- shoresh_identification: 25
- prefix_identification: 15
- suffix_identification: 15
- mi_amar_el_mi: 0
- al_mi_neemar: 0

## Weak Data Areas

- All 10 comprehension_question records are missing expected_answer, so mi_amar_el_mi and al_mi_neemar previews were skipped.
- All 8 word_parse_task records have answer_status=not_extracted and no expected_word/prefix/suffix payload.
- Only 6 of 10 word_parse records include an explicit shoresh.
- Only 4 of 10 word_parse records include a suffix payload.
- 8 of 18 vocab_entry records still have empty english_glosses and remain unusable for matching previews.

## Structural Issues Found

- Requested comprehension preview distribution could not be met without inventing answers.
- Preview generation currently depends on repeating prompt families across a small approved source pool.
- Affix lanes are sourced from word_parse records only because the task-model records have no answer payload yet.

## Recommendation

- NOT READY for the next phase until comprehension answers and task-model answer payloads are present.
