# Batch 002 Summary

## Source Used

- Source package: `linear_chumash_translation_most_parshiyos_in_torah`
- Source name: `Linear Chumash Translation for Most Parshiyos in Torah`
- Local source file: `local_curriculum_sources/7984C_b_01409_pshat_of_torah.pdf`
- Pasuk range: `Bereishis 1:6 through Bereishis 2:3`
- Source pages used: `4-8`

## Files Created

- Raw source excerpt: `data/curriculum_extraction/raw_sources/batch_002/linear_chumash_bereishis_1_6_to_2_3_cleaned.md`
- Normalized records: `data/curriculum_extraction/normalized/batch_002_linear_chumash_bereishis_1_6_to_2_3_pasuk_segments.jsonl`
- Preview file: `data/curriculum_extraction/generated_questions_preview/batch_002_preview.jsonl`

## Normalized Record Counts

- `pasuk_segment`: `123`
- `translation_rule`: `0`

## Skipped Records

- Unusable phrase segments skipped: `0`
- Separate `translation_rule` records skipped: `0 extracted`; the source notes in this range were kept attached to segment-level translation context instead of being split into reusable standalone rules.

## Extraction Risks

- The local PDF text layer surfaced noisy/transliterated Hebrew, so the Hebrew phrase text was aligned against the local canonical pasuk text in `data/pesukim_100.json` by exact pasuk reference and source phrase order.
- The extracted English remains linear and source-shaped, including some parenthetical teaching notes inside phrase translations.
- All Batch 002 records remain `needs_review`, `not_runtime_active`, and low confidence.

## Validation Result

- `python scripts/validate_curriculum_extraction.py` - PASS
- `python scripts/load_curriculum_extraction.py --summary` - PASS
- `python -m pytest` - PASS (`467 passed`)

## Recommendation

- `READY_FOR_MANUAL_REVIEW`
- Keep Batch 002 as isolated inactive infrastructure only. It is not ready for runtime integration or reviewed-question-bank promotion.
