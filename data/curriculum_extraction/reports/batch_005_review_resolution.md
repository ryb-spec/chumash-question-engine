# Batch 005 Review Resolution

- Cleanup date: `2026-04-24`
- Context: manual review closeout for `batch_005_linear_bereishis_4_1_to_4_16`

## Purpose

- Record the human-review cleanup decisions for Batch 005.
- State clearly whether Batch 005 is now cleared for future curriculum planning while remaining non-runtime.

## Files Inspected

- `data/curriculum_extraction/curriculum_extraction_manifest.json`
- `data/curriculum_extraction/reports/batch_005_manual_review_packet.md`
- `data/curriculum_extraction/reports/batch_005_summary.md`
- `data/curriculum_extraction/reports/batch_005_preview_summary.md`
- `data/curriculum_extraction/raw_sources/batch_005/linear_chumash_bereishis_4_1_to_4_16_cleaned.md`
- `data/source/bereishis_4_1_to_4_16.json`

## Summary Of Review Decisions

- The Batch 005 extraction remains source-traceable and suitable for inactive curriculum planning.
- The main review work in this pass was accepted alias/context handling for names, place names, and several source-faithful but student-facing awkward phrases.
- No blocker was found that requires changing the underlying Batch 005 extraction JSONL or preview JSONL.

## Alias / Context Decisions

- `קַיִן`: preserve the source name rendering. Accepted aliases: `Kayin` and `Cain`. Future prompts should choose one audience-facing name per item.
- `הֶבֶל`: preserve the source name rendering. Accepted aliases: `Hevel` and `Abel`. Future prompts should choose one audience-facing name per item.
- `מִנְחָה`: preserve the source wording `present`. Accepted aliases: `offering` and `gift-offering`.
- `וַיִּשַׁע`: preserve the source wording `turned`. Accepted aliases: `accepted` and `paid attention to`.
- `לֹא שָׁעָה`: preserve the source wording `didn't turn`. Accepted aliases: `did not accept` and `did not pay attention to`.
- `חַטָּאת רֹבֵץ`: preserve the source wording. Accepted smoother phrasing may include `sin crouches` and `sin crouches at the opening`, but the phrase should stay exact-phrase-sensitive in future prompts.
- `הֲשֹׁמֵר אָחִי אָנֹכִי`: preserve the source wording `am I the guard of my brother?`. Accepted aliases: `am I my brother's keeper?` and `am I my brother's watchman?`.
- `דְּמֵי אָחִיךָ`: preserve the source wording. Accepted aliases may include `your brother's blood`; use `bloods` only when the prompt is intentionally studying the more literal phrasing.
- `נָע וָנָד`: preserve the source wording `moving and shaking`. Accepted aliases: `wandering` and `restless wanderer`.
- `אוֹת`: preserve the source wording `sign`. Accepted alias: `mark` when the context already makes the protective sign clear.
- `אֶרֶץ־נוֹד`: preserve the place name `land of Nod`.
- `קִדְמַת־עֵדֶן`: preserve the source-facing phrase while allowing accepted aliases `east of Eden` and `toward the east of Eden`. Prefer `Eden` over the source-literal spelling `Eiden` in future accepted-answer layers.

## Source / Data Preservation

- Original source translations were preserved.
- Extraction data was left unchanged.
- No normalized JSONL, preview JSONL, or raw source markdown files were modified in this review closeout.
- Batch 005 remains `not_runtime_active`; no runtime scope or runtime payload changed.

## Remaining Blockers

- None.

## Final Recommendation

`READY_FOR_BATCH_005_PLANNING`

## Next Action

- Batch 005 is cleared for future curriculum planning while remaining explicitly non-runtime.
- The next branch may begin Batch 006 planning without treating Batch 005 as runtime-active or as reviewed production question-bank content.
