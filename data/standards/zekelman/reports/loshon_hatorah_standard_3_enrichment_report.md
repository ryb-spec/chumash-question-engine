# Loshon HaTorah Standard 3 Enrichment Report

## 1. Current Branch
- `feature/loshon-hatorah-standard-3-enrichment`

## 2. Files Created
- `docs/sources/loshon_hatorah/extracted/loshon_hakodesh_book_ocr_raw_text.md`
- `docs/sources/loshon_hatorah/extracted/loshon_answe_2_combined_raw_text.md`

## 3. Files Modified Or Refreshed
- `PLANS.md`
- `data/sources/loshon_hatorah/loshon_hatorah_source_inventory.json`
- `docs/sources/loshon_hatorah/indexes/loshon_hatorah_document_index.json`
- `docs/sources/loshon_hatorah/reports/loshon_hatorah_source_ingestion_report.md`
- `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json`
- `data/standards/zekelman/crosswalks/loshon_hatorah_to_zekelman_standard_3_crosswalk.json`
- `data/standards/zekelman/review/zekelman_2025_standard_3_teacher_review_packet.md`
- `data/standards/zekelman/review/zekelman_2025_standard_3_review_decision_sheet.md`
- `data/standards/zekelman/reports/loshon_hatorah_standard_3_enrichment_report.md`

## 4. Loshon HaTorah Sources Found
- `docs/sources/loshon_hatorah/raw/loshon_hakodesh_book_ocr.pdf`
- Role: main book PDF.
- Page count: `86`.
- File size: `15218787` bytes.
- SHA-256: `c4eb6adb3841c6c84f3cf63342044ed8ef7890a9d0f6852ebe5edc041ffab130`.
- Extracted text: `docs/sources/loshon_hatorah/extracted/loshon_hakodesh_book_ocr_raw_text.md`.

- `docs/sources/loshon_hatorah/raw/loshon_answe_2_combined.pdf`
- Role: answer booklet PDF for source review only, not an active answer key.
- Page count: `33`.
- File size: `7074942` bytes.
- SHA-256: `de05e9e542a3d9d012d8282f457fcd139a0ab49e6e021281cdbf2688d931a32d`.
- Extracted text: `docs/sources/loshon_hatorah/extracted/loshon_answe_2_combined_raw_text.md`.

- `data/dikduk_rules/rules_loshon_foundation.jsonl`
- Role: existing source-modeled JSONL artifact.
- Rule records observed: `37`.
- File size: `67503` bytes.
- SHA-256: `91f097d2b4688b1b3356181ade74703ac75b3890eb5c75bffcf9b7599b2c9173`.

## 5. Loshon HaTorah Sources Missing
- No expected Loshon HaTorah / Loshon Hakodesh raw source files are currently missing from the protected source layer.
- Exact alignment between the source-modeled JSONL records and raw PDF page locations still needs human review.

## 6. Rule Candidates Extracted
- Refreshed `27` conservative rule candidates in `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json`.
- Existing candidates were enriched with raw-source evidence notes where the PDFs support the rule family.
- New conservative boundary candidates were added for weak letters, ו׳ ההיפוך, present tense, command forms, and pausal/nikud-sensitive forms.
- All candidates remain `needs_teacher_review`, source/Hebrew verification pending, `not_runtime_ready`, and `not_question_ready`.

## 7. Crosswalk Mappings Created
- Refreshed `29` supplemental mappings in `data/standards/zekelman/crosswalks/loshon_hatorah_to_zekelman_standard_3_crosswalk.json`.
- Mapped areas now include `3.02`, `3.04`, `3.05`, `3.06`, `3.07`, `3.08`, and `3.10`.
- Added mappings for weak-letter boundaries, ו׳ ההיפוך, present tense, command forms, and pausal-form/nikud-sensitive evidence.
- No mapping marks a strand runtime-ready, question-ready, or teacher-approved.

## 8. Strongest Support Areas
- `3.08` Grouping and Word Order: main-book extracted page 4 directly supports variable Hebrew word order and natural English reordering. The answer booklet adds practice/activity evidence for literal-to-natural translation handling.
- `3.04` Nouns and Adjectives: main-book extracted pages support noun gender/number, plural endings, סמיכות as a construct phrase, and common construct-form changes.
- `3.06` Prefixes, Articles, and Prepositions: main-book summary and answer-booklet evidence support visible ה, ו, prepositions, prefix prepositions, and context-sensitive את-family cautions.
- `3.05` Pronouns and Suffixes: source evidence supports keeping possessive-suffix decoding separate from pronoun referent tracking.
- `3.07` Verbs: evidence now supports foundational agreement and tense/form planning while also documenting deferred boundaries for weak letters, ו׳ ההיפוך, present tense, and command forms.

## 9. Remaining Weak Or Unresolved Areas
- `3.10` is improved but still unresolved. Pausal/vowel-change and את-family nikud-sensitive evidence was found, but this does not cover the full Zekelman scope of תנועות, שבאים, דגשים, syllables, or טעמי המקרא interaction.
- The main-book embedded OCR layer is partial; many pages extract as blank and require direct PDF review.
- Weak-letter roots, ו׳ ההיפוך, present tense, command forms, and pausal forms remain deferred/context-sensitive lanes.
- The answer booklet is useful for review evidence but must not become an active answer key or question source.

## 10. Possible Conflicts With Zekelman 2025
- No confirmed conflict with Zekelman 2025 was found.
- Possible scope mismatch: Loshon material supports grammar and translation skills that may not follow the same level progression as Zekelman 2025.
- Possible scope mismatch: Loshon evidence around nikud-sensitive forms is narrower than Zekelman `3.10`; Zekelman remains authoritative for scope and level placement.

## 11. Hebrew/OCR/Table Uncertainty
- Hebrew examples, nekudos, weak-letter examples, and table structures require human verification against the raw PDFs.
- The main book OCR/text extraction is incomplete.
- The answer booklet extraction is more complete, but it contains OCR noise and layout uncertainty.
- Existing JSONL records cite `loshon 2.pdf`; the new main PDF metadata title is `loshon 2`, but exact record-to-page matching remains unresolved.

## 12. What Was Intentionally Not Changed
- No runtime behavior was changed.
- No Streamlit/UI behavior was changed.
- No student questions, answer keys for active use, or active question templates were created.
- No reviewed-bank files or production data were modified.
- No standards data was connected to runtime.
- No strand was marked runtime-ready or question-ready.
- No teacher decisions were invented or changed.
- Zekelman 2025 wording, numbering, scope, and level progression were not overridden.

## 13. Validation Results
- `python scripts/validate_source_texts.py`: passed.
- `python scripts/validate_curriculum_extraction.py`: passed.
- `python scripts/validate_curriculum_extraction.py --check-git-diff`: passed.
- `python scripts/validate_standards_data.py`: passed.
- `python -m pytest tests/test_standards_data_validation.py`: `9 passed`.
- `python -m pytest tests/test_curriculum_extraction_validation.py tests/test_diagnostic_preview_validation.py tests/test_standards_data_validation.py`: `53 passed`.
- `python -m pytest`: `574 passed`, `1 failed`.
- Full-suite unrelated failure: `tests/test_source_texts_validation.py::SourceTextsValidationTests::test_validator_reports_expected_sha256_for_real_file`, where the current source-text SHA is `4d96c615ab63e0419bff079db250d71ea9b5de266ff9ab8d589ae80e4afd0b71` and the test expects `0dedb854e1e8b59fa5dc08f93be5baffe4c1faaa09d00c148c8ef3113b065913`.

## 14. Recommended Next Task
- Have a human reviewer inspect the raw PDFs directly for `3.08`, `3.04`, and `3.10`, starting with main-book extracted pages 4, 6, 8, 63, and 80-86 plus answer-booklet pages 8-12, 25, and 28-33.
- After that review, create a compact teacher-reviewed decision grid for which Loshon-supported evidence can inform later diagnostic skill planning, while still keeping runtime and question generation blocked.
