# Zekelman 2025 Structured Extraction Report

## Summary

This branch adds the first machine-readable structured extraction layer from the canonical 2025 / Version 2.5 Zekelman Standards for Chumash source.

Created outputs:
- `data/standards/zekelman/structured/zekelman_2025_standards_index.json`
- `data/standards/zekelman/structured/zekelman_2025_standard_3_vocabulary_language_skills.json`
- `data/standards/zekelman/structured/zekelman_2025_question_generation_relevance.json`
- `data/standards/zekelman/reports/zekelman_2025_structured_extraction_report.md`

## What Was Extracted

- Standard 1 substandards `1.03-1.10` that affect conventions, navigation, and text reading
- Standard 3 substandards `3.01-3.10`, with a separate detailed file
- Standard 4 substandards `4.01-4.08`
- Standard 5 substandards `5.01-5.08` at a high-level index stage only

## What Was Intentionally Not Extracted

- full Standard 2 structured extraction
- full Standard 5 level-by-level machine extraction
- appendix tables and supporting lists from the 2025 PDF
- question templates or question banks
- runtime-facing mappings or app connections

## OCR, Table, and Hebrew Uncertainty

- the canonical PDF text layer is usable, but some Hebrew still displays imperfectly in the markdown extraction
- many standards tables flatten multiple level columns into one text stream
- some Standard 3 and Standard 4 rows clearly span multiple levels, so those were preserved conservatively instead of overfit into brittle exact cells
- advanced ניקוד extraction is especially table-sensitive
- all Hebrew terms still require human review before being treated as final machine truth

## Runtime Safety

No runtime, student-facing, generated-question, reviewed-bank, release, or production files were changed by this task.

## Validation Note

No dedicated Zekelman / standards-specific validator exists yet in this repo. This branch relies on JSON validity checks plus the existing lightweight repo validators requested for source/documentation work.

## Recommended Next Task

Recommended next branch:
- `feature/zekelman-standard-3-supplemental-crosswalk`

Recommended next task:
- cross-check the new Standard 3 structure against the 2014 vocabulary/language guide and the 2014 appendix
- add a human-reviewed mapping layer from standards to internal skill tags
- keep everything non-runtime until that review work is complete
