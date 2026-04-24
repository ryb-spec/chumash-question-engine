# Batch 003 Summary

- Batch ID: `batch_003_linear_bereishis_2_4_to_2_25`
- Source used: `Linear Chumash Translation for Most Parshiyos in Torah`
- Source file: `local_curriculum_sources/7984C_b_01409_pshat_of_torah.pdf`
- Pasuk range: `Bereishis 2:4 through Bereishis 2:25`

## Files Created

- `data/curriculum_extraction/raw_sources/batch_003/linear_chumash_bereishis_2_4_to_2_25_cleaned.md`
- `data/curriculum_extraction/normalized/batch_003_linear_chumash_bereishis_2_4_to_2_25_pasuk_segments.jsonl`
- `data/curriculum_extraction/generated_questions_preview/batch_003_preview.jsonl`

## Normalized Record Counts

- `pasuk_segment`: `90`
- `translation_rule`: `0`

## Skipped Records

- `0` skipped segments

## Extraction Risks

- The PDF text layer is noisy, so cleaned English phrasing was preserved manually from the local source excerpt.
- Canonical Hebrew alignment was anchored to local `data/pesukim_100.json` pasuk text rather than relying on PDF glyph extraction.
- No standalone explicit translation-rule notes were extracted in this range, so no `translation_rule` records were created.
- All extracted records remain `needs_review`, `not_runtime_active`, and low confidence pending manual review.

## Validation Result

- `python scripts/validate_curriculum_extraction.py`: PASS
- `python scripts/load_curriculum_extraction.py --summary`: PASS
- `python -m pytest tests/test_curriculum_extraction_validation.py tests/test_curriculum_question_preview.py`: PASS
- `python -m pytest`: PASS

## Recommendation

- `READY_FOR_MANUAL_REVIEW`
