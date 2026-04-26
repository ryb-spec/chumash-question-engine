# Zekelman 2025 Standard 3 Teacher Review Layer Report

## 1. Current Branch
- `feature/zekelman-standard-3-teacher-review-layer`

## 2. Files Created
- `data/standards/zekelman/review/zekelman_2025_standard_3_teacher_review_packet.md`
- `data/standards/zekelman/review/zekelman_2025_standard_3_review_tracking.json`
- `data/standards/zekelman/reports/zekelman_2025_standard_3_teacher_review_layer_report.md`

## 3. Files Modified
- `PLANS.md`
- `scripts/validate_curriculum_extraction.py`
- `tests/test_curriculum_extraction_validation.py`

## 4. Review Items Created
- Total review items: `8`
- Standard coverage in this packet:
  - `3.01` noun vocabulary
  - `3.02` shoresh / verb-root recognition
  - `3.04` noun/adjective phrase-structure cues with סמיכות
  - `3.05` pronouns and pronominal / possessive suffixes
  - `3.06` prefixes, articles, prepositions, and the two functions of `את`
  - `3.07` verb features, tense recognition, and translation precision
  - `3.08` grouping and word order
  - `3.10` advanced ניקוד reading

## 5. High-Priority Strands
- `3.01` Vocabulary: שמות עצם (nouns)
- `3.02` Vocabulary: שורשים (for verbs)
- `3.05` Pronouns
- `3.06` Prepositions, Conjunctions and the Definite Article
- `3.07` Verbs
- `3.08` Grouping and Word Order

## 6. What Teacher Review Must Verify
- Canonical 2025 wording, page-level row boundaries, and Hebrew accuracy for each high-priority strand.
- Whether draft mappings should stay bundled or split, especially `3.05` pronouns versus suffixes, `3.04` noun features versus סמיכות, and `3.06` visible prefix/article work versus `את`.
- Level fit for weak-root work in `3.02`, upper-level verb parsing in `3.07`, and advanced-only gating in `3.10`.
- Whether `3.08` has enough source support for later diagnostic planning, given that the older support remains partial and indirect.
- Whether older source organization, especially `3.3` versus `3.6`, affects later internal wording or teacher-facing labels.

## 7. What Was Intentionally Not Changed
- No runtime behavior was changed.
- No Streamlit or UI behavior was changed.
- No scoring or mastery logic was changed.
- No reviewed-bank files were changed.
- No production data was changed.
- No student questions, answer keys, or active question templates were created.
- No strand was marked runtime-ready or question-ready.
- No raw source PDFs were deleted, overwritten, or replaced.

## 8. Validation Results
- Review tracking JSON validity: passed.
- Review-item linkage check: passed (`8` review items, `0` missing standard IDs, `0` missing draft skill IDs).
- `python scripts/validate_source_texts.py`: passed.
- `python scripts/validate_curriculum_extraction.py`: passed after a narrow allowlist update for `data/standards/zekelman/` review-only artifacts.
- Standards-specific validator: none found in `scripts/`.
- Targeted test slice:
  - `python -m pytest tests/test_source_texts_validation.py tests/test_curriculum_extraction_validation.py tests/test_curriculum_extraction_schemas.py tests/test_curriculum_extraction_loader.py`
  - Result: `53 passed`, `1 failed`
  - Remaining failure: `tests/test_source_texts_validation.py::SourceTextsValidationTests::test_validator_reports_expected_sha256_for_real_file`
  - Failure reason: pre-existing SHA mismatch (`expected 0ded...`, actual `4d96...`)
- Focused curriculum validation rerun after adding the final report:
  - `python -m pytest tests/test_curriculum_extraction_validation.py`
  - Result: `32 passed`
- Full pytest:
  - `python -m pytest`
  - Result: `565 passed`, `1 failed`
  - Remaining failure: the same pre-existing SHA assertion in `tests/test_source_texts_validation.py`

## 9. Remaining Uncertainty
- Hebrew, nikud, and table structure still require direct teacher confirmation against the raw PDFs.
- `3.08` remains only partially supported by the older supplemental sources and should stay fully review-only.
- `3.07` is strongly supported for foundational verb work, but the full upper-level binyan/passive range is broader than the older supplemental evidence.
- `3.10` still needs teacher confirmation that its lower-level blank rows are intentional and that it should remain advanced-only.
- The repo still has a separate pre-existing SHA expectation mismatch in `tests/test_source_texts_validation.py`.

## 10. Recommended Next Task
- Conduct the actual teacher review for the six high-priority strands first, record reviewer decisions and notes into `data/standards/zekelman/review/zekelman_2025_standard_3_review_tracking.json`, and keep all resulting decisions non-runtime until a later activation pass is explicitly requested.
