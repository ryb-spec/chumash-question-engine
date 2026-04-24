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

- `עָרוּם / עֵירֹם / עֵירֻמִּם`: preserve the source translation in each pasuk and keep the context distinction between `cunning/crafty` and `naked/unclothed`.
- `מוֹת תָּמוּת / לֹא מוֹת תְּמֻתוּן`: preserve the source death-warning phrasing; accepted aliases may include `you will surely die` and `you will not surely die` only in the matching pasuk context.
- `עֵץ הַדַּעַת טוֹב וָרָע`: preserve the source phrasing; accepted aliases may include `tree of knowledge of good and bad`.
- `חַוָּה`: preserve the source name rendering; accepted aliases may include `Chava` and `Eve` depending on audience settings.
- `גַּן עֵדֶן`: preserve the source phrase when surfaced; accepted aliases may include `Gan Eden` and `Eden`.

## Source / Data Preservation

- Original source translations were preserved.
- Extraction data was left untouched.
- No normalized JSONL, preview JSONL, or raw source markdown files were modified.

## Final Recommendation

`STILL_BLOCKED`

## Exact Remaining Blocker

- Accepted alias/context handling for the Bereishis 3 watchlist items and smoother student-facing wording for the flagged source-literal phrases are now documented clearly, but they are not yet resolved into a follow-up artifact that clears Batch 004 for Batch 005 planning.

## Next Action

- Run one small follow-up alias/context cleanup branch focused only on Batch 004 reviewer-approved alias wording and the corresponding review-state closeout report.
