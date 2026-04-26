# Zekelman 2025 Standard 3 Supplemental Crosswalk Report

## Current Branch
- `feature/zekelman-standard-3-supplemental-crosswalk`

## Files Created
- `data/standards/zekelman/crosswalks/zekelman_2025_standard_3_supplemental_crosswalk.json`
- `data/standards/zekelman/crosswalks/zekelman_2025_standard_3_skill_mapping_draft.json`
- `data/standards/zekelman/reports/zekelman_2025_standard_3_supplemental_crosswalk_report.md`

## Files Modified
- `PLANS.md`

## Supplemental Sources Found and Used
- `docs/standards/zekelman/raw/2014_intro_vocabulary_language_skills_zekelman_chumash.pdf`
- `docs/standards/zekelman/raw/2014_appendix_free_resource_packet_zekelman_chumash.pdf`
- `docs/standards/zekelman/raw/2016_sample_assessment_questions_standards_1_2_zekelman_chumash.pdf`

## Supplemental Sources Missing
- None. The expected 2014 and 2016 supplemental raw PDFs were present at the requested repo paths.

## Crosswalk Summary
- Standard 3 records checked: `10`
- Direct support statuses: `9`
- Partial support statuses: `1`
- Unclear / no-clear-support statuses: `0`
- Possible conflicts flagged: `0`

## Support Pattern by Standard
- `3.01` noun vocabulary: direct support from intro, appendix vocabulary lists, and sample-assessment section 3.1.
- `3.02` shoresh / verb-root vocabulary: direct support from intro verb-root lessons, appendix verb-frequency lists, and sample-assessment section 3.2.
- `3.03` other vocabulary: direct support from intro function-word lessons, appendix Hebrew Particles, and sample-assessment section 3.3.
- `3.04` nouns and adjectives: direct support from intro grammar lessons, appendix parts-of-speech appendix, and sample-assessment section 3.4.
- `3.05` pronouns: direct support from all three supplemental sources, including teacher charts and referent/suffix assessments.
- `3.06` prepositions, conjunctions, and definite article: direct support from intro prefix/article lessons and appendix material on article rules, ו ההיפוך, and את.
- `3.07` verbs: direct support for foundational verb parsing, with weaker supplemental evidence for the full upper-level binyan/passive range.
- `3.08` grouping and word order: partial support only; the supplemental sources clarify syntax-sensitive translation and סמיכות, but do not mirror the full 2025 strand one-to-one.
- `3.09` parsing the פסוק: direct support from the intro trop section and the appendix dedicated to Standard 3.9 punctuation/parsing.
- `3.10` understanding ניקוד: direct support from the 2014 intro ניקוד sequence, plus partial applied-chart support from the appendix.

## Conflicts Between 2025 and Older Sources
- No direct wording conflict was strong enough to override or alter the 2025 canonical Standard 3 extraction.
- The main historical difference is organizational: some older assessment material groups function-word content under `3.3` rather than splitting later grammar strands the way the 2025 version does.

## Hebrew / OCR / Table Uncertainty
- Hebrew display in extracted text still needs manual confirmation against the raw PDFs.
- Appendix charts and frequency tables remain `table_structure_uncertain` where row/column relationships matter.
- Advanced ניקוד and dense grammar examples remain `hebrew_text_needs_review` before any downstream structured use.
- Sample-assessment sections are helpful for assessment architecture, but OCR punctuation and table flattening should not be treated as production truth.

## What Was Intentionally Not Changed
- No runtime behavior was changed.
- No Streamlit/UI files were changed.
- No reviewed-bank files were changed.
- No production data was changed.
- No generated-question files were created or updated.
- No active question templates or runtime skill lanes were created.

## Validation Results
- JSON validity for the new crosswalk files: passed.
- Coverage check that every Standard 3 record appears in the crosswalk: passed (`10` of `10` Standard 3 records present; `0` missing).
- Draft skill-mapping file validity: passed (`13` draft mappings).
- `python scripts/validate_source_texts.py`: passed.
- `python scripts/validate_curriculum_extraction.py`: passed.
- Standards-specific validator: none found in the repo during this pass.

## Recommended Next Task
- Build the next teacher-review layer that confirms Hebrew/page-level matches for the most question-relevant Standard 3 strands first: noun vocabulary, shoresh/verb roots, pronouns, prepositions/articles, and verbs.
