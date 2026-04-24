# Batch 004 Summary

- Source used: `Linear Chumash Translation for Most Parshiyos in Torah`
- Local source file: `local_curriculum_sources/7984C_b_01409_pshat_of_torah.pdf`
- Pasuk range: `Bereishis 3:1 through Bereishis 3:24`

## Files Created

- `data/curriculum_extraction/raw_sources/batch_004/linear_chumash_bereishis_3_1_to_3_24_cleaned.md`
- `data/curriculum_extraction/normalized/batch_004_linear_chumash_bereishis_3_1_to_3_24_pasuk_segments.jsonl`
- `data/curriculum_extraction/generated_questions_preview/batch_004_preview.jsonl`

## Normalized Record Counts

- `pasuk_segment`: `119`
- `translation_rule`: `0`

## Skipped Records

- `0` skipped source segments

## Extraction Risks

- The PDF text layer is noisy, so Hebrew phrase alignment was anchored against the local pasuk corpus while preserving source-backed English phrasing.
- Source-faithful classroom phrasing may need later accepted-alias handling, but no alias records were created in this batch.
- No standalone source-backed translation-rule notes appeared in this range, so no `translation_rule` file was created.

## Special Review Flags

- `alias_context_review_arum` appears on selected `Bereishis 3:1`, `3:7`, `3:10`, and `3:11` segments where source phrasing may later need alias/context review against nearby unclothed-language usage.
- `alias_context_review_mot_tamut` appears on the `Bereishis 3:4` death-warning segment for future accepted-alias review such as "you will surely die."
- `עץ הדעת טוב ורע` / knowledge-of-good-and-bad phrasing in `Bereishis 3:5` and `3:22` should stay source-faithful for now and can be reviewed later for accepted alias handling.

## Validation Result

- `python scripts/validate_curriculum_extraction.py` passed
- `python scripts/load_curriculum_extraction.py --summary` passed
- `python -m pytest tests/test_curriculum_extraction_validation.py tests/test_curriculum_question_preview.py` passed

## Recommendation

`READY_FOR_MANUAL_REVIEW`
