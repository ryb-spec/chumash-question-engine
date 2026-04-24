# Batch 005 Summary

- Source used: `Linear Chumash Translation for Most Parshiyos in Torah`
- Local source file: `local_curriculum_sources/7984C_b_01409_pshat_of_torah.pdf`
- Local Hebrew source file: `data/source/bereishis_4_1_to_4_16.json`
- Pasuk range: `Bereishis 4:1 through Bereishis 4:16`

## Files Created

- `data/curriculum_extraction/raw_sources/batch_005/linear_chumash_bereishis_4_1_to_4_16_cleaned.md`
- `data/curriculum_extraction/normalized/batch_005_linear_chumash_bereishis_4_1_to_4_16_pasuk_segments.jsonl`
- `data/curriculum_extraction/generated_questions_preview/batch_005_preview.jsonl`

## Normalized Record Counts

- `pasuk_segment`: `64`
- `translation_rule`: `0`

## Skipped Records

- `0` skipped source segments

## Extraction Risks

- The PDF text layer is noisy, so Hebrew phrase alignment was anchored against the local source block in `data/source/bereishis_4_1_to_4_16.json` while preserving source-backed English phrasing from the PDF.
- Several source-faithful classroom phrases are intentionally preserved even when they are awkward in student-facing English, including `וַיִּשַׁע`, `לֹא שָׁעָה`, `חַטָּאת רֹבֵץ`, `הֲשֹׁמֵר אָחִי אָנֹכִי`, `דְּמֵי אָחִיךָ`, `נָע וָנָד`, and `אוֹת`.
- No standalone source-backed `translation_rule` notes appeared in this range, so no `translation_rule` file was created.

## Special Review Flags

- `alias_context_review_kayin_name` and `alias_context_review_hevel_name` appear on selected segments where later accepted-alias handling may need `Kayin/Cain` and `Hevel/Abel`.
- `alias_context_review_minchah`, `alias_context_review_vayisha`, and `alias_context_review_lo_shaah` appear where offering / acceptance phrasing may later need review for student-facing aliases such as `offering`, `accepted`, or `paid attention to`.
- `alias_context_review_chatat_rovetz`, `alias_context_review_shomer_achi`, `alias_context_review_demei`, `alias_context_review_na_vanad`, `alias_context_review_ot`, `alias_context_review_eretz_nod`, and `alias_context_review_kidmat_eden` mark the main Bereishis 4 watchlist phrases for future review only.

## Validation Result

- `python scripts/validate_curriculum_extraction.py` passed
- `python scripts/load_curriculum_extraction.py --summary` passed
- `python -m pytest tests/test_curriculum_extraction_validation.py tests/test_curriculum_question_preview.py` passed

## Recommendation

`READY_FOR_MANUAL_REVIEW`
