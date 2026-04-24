# Batch 004 Review Resolution

- Cleanup date: `2026-04-24`
- Context: review-state cleanup for `batch_004_linear_bereishis_3_1_to_3_24`

## Files Inspected

- `data/curriculum_extraction/reports/batch_004_manual_review_packet.md`
- `data/curriculum_extraction/reports/batch_004_summary.md`
- `data/curriculum_extraction/reports/batch_004_preview_summary.md`
- `data/curriculum_extraction/curriculum_extraction_manifest.json`

## Watchlist / Placeholder Fixes

- Replaced the garbled Batch 004 watchlist labels with readable Hebrew labels for:
  - `עָרוּם / עֵירֹם / עֵירֻמִּם`
  - `מוֹת תָּמוּת / לֹא מוֹת תְּמֻתוּן`
  - `עֵץ הַדַּעַת טוֹב וָרָע`
  - `חַוָּה`
  - `גַּן עֵדֶן`

## Alias / Context Decisions

- `עָרוּם / עֵירֹם / עֵירֻמִּם`: preserve the source translation in each pasuk and keep the context distinction between `cunning/crafty` and `naked/unclothed`. Future-generation note: never collapse the crafty/cunning sense into the naked/unclothed sense.
- `מוֹת תָּמוּת / לֹא מוֹת תְּמֻתוּן`: preserve the source death-warning phrasing. Accepted aliases are `you will surely die`, `you will not surely die`, and the shorter `you will die` / `you will not die` only when the prompt context already anchors the correct pasuk polarity.
- `עֵץ הַדַּעַת טוֹב וָרָע`: preserve the source phrasing. Accepted aliases are `tree of knowledge of good and bad` and `tree of knowledge of good and evil`. Future-generation note: do not shorten this to just `the tree` in alias-sensitive prompts.
- `חַוָּה`: preserve the source name rendering. Accepted aliases are `Chava` and `Eve`. Future-generation note: choose one audience-facing name per prompt and avoid mixing both names inside the same item unless the task is explicitly about aliases.
- `גַּן עֵדֶן`: preserve the source phrase when surfaced. Accepted aliases are `Gan Eden` and `Eden`. Student-facing wording note: `Gan Eden` is the safer direct transliteration; `Eden` is acceptable when the surrounding prompt already signals the place name clearly.

## Source / Data Preservation

- Original source translations were preserved.
- Extraction data was left untouched.
- No normalized JSONL, preview JSONL, or raw source markdown files were modified.

## Final Recommendation

`STILL_BLOCKED`

## Exact Remaining Blocker

- The alias/context cleanup is now resolved in the review artifacts, but Batch 004 still remains under the current repo contract as `review_status = needs_review` and `status = extracted_needs_review`. The current validation suite also expects that state to remain in place for Batch 004, so this branch cannot honestly promote the batch to a cleared planning state without widening scope beyond the allowed report/manifest cleanup.

## Next Action

- Run one small follow-up review-contract branch to decide whether Batch 004 should remain permanently `needs_review` as inactive infrastructure or whether the repo’s curriculum-extraction manifest/test contract should be widened to allow a non-runtime reviewed/cleared state for post-review batches.
