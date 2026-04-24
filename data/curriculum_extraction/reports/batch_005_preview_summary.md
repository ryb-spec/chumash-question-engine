# Batch 005 Preview Summary

## Preview Question Counts By Type

- `phrase_translation`: `50`
- `hebrew_to_english_match`: `25`
- `english_to_hebrew_match`: `25`

Total preview questions: `100`

## Supported Lanes

- `phrase_translation`
- `hebrew_to_english_match`
- `english_to_hebrew_match`

## Coverage Notes

- The selected preview phrases intentionally cover names, offerings, acceptance/rejection language, actor/action turns, sequence-sensitive phrases, and the main Bereishis 4 alias watchlist items inside the current supported non-runtime preview lanes.
- Phrase-sensitive wording was preserved for `חַטָּאת רֹבֵץ`, `הֲשֹׁמֵר אָחִי אָנֹכִי`, `דְּמֵי אָחִיךָ`, `נָע וָנָד`, `אוֹת`, `אֶרֶץ נוֹד`, and `קִדְמַת עֵדֶן`.

## Blocked / Deferred Lanes

- `mi_amar_el_mi`
- `al_mi_neemar`
- `formal shoresh / prefix / suffix preview lanes` because this Linear Chumash extraction branch still uses only the established translation-and-match preview contract
- `standalone actor/action role questions` and `standalone sequence/comprehension preview lanes` because those lanes are not yet part of the isolated Batch 002-005 preview contract
- `word_parse_task answer checking`

## Comparison To Batch 004

- Batch 004 also produced `100` preview questions across the same three supported lanes.
- Batch 004 contained `119` `pasuk_segment` records; Batch 005 contains `64`.
- Batch 005 begins the next contiguous non-runtime Bereishis curriculum block after the reviewed-for-planning Batch 004 closeout.

## Recommendation

`READY_FOR_MANUAL_REVIEW`
