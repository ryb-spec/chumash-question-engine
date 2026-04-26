# Zekelman 2025 Canonical Source Ingestion Report

## 1. Summary

### What was added

- The canonical 2025 / Version 2.5 Zekelman Chumash Standards PDF was added as a raw source file:
  - `docs/standards/zekelman/raw/2025_zekelman_chumash_standards_v2_5_complete_levels_1_8.pdf`
- A page-delimited raw text extraction companion was added:
  - `docs/standards/zekelman/extracted/2025_zekelman_chumash_standards_v2_5_complete_levels_1_8_raw_text.md`
- The document index was updated to include the 2025 canonical source with checksum, page count, and extraction coverage metadata.

### Whether the 2025 PDF was previously missing

Yes.

Before this branch, the repo's Zekelman source-management layer only had a reference-only canonical record for the 2025 / Version 2.5 standards. The raw PDF itself was not yet present in the repo.

### Whether raw text extraction was created

Yes.

The canonical PDF was successfully extracted with page boundaries preserved.

### Whether inventory, map, and extraction plan were updated

Yes.

- `data/standards/zekelman/source_inventory.json`
- `data/standards/zekelman/source_map.md`
- `data/standards/zekelman/extraction_plan.md`

## 2. Canonical Source Confirmation

The 2025 / Version 2.5 Zekelman Chumash Standards PDF is now the actual canonical raw source, not merely a reference-only metadata record.

Canonical file:
- `docs/standards/zekelman/raw/2025_zekelman_chumash_standards_v2_5_complete_levels_1_8.pdf`

Use this source for:
- current standards wording
- level progression
- standard numbering
- scope and sequence

## 3. Files Inspected

### Raw PDFs

- `docs/standards/zekelman/raw/2014_intro_vocabulary_language_skills_zekelman_chumash.pdf`
- `docs/standards/zekelman/raw/2016_sample_assessment_questions_standards_1_2_zekelman_chumash.pdf`
- `docs/standards/zekelman/raw/2014_appendix_free_resource_packet_zekelman_chumash.pdf`
- `docs/standards/zekelman/raw/2025_zekelman_chumash_standards_v2_5_complete_levels_1_8.pdf`

### Extracted text files

- `docs/standards/zekelman/extracted/2014_intro_vocabulary_language_skills_zekelman_chumash_raw_text.md`
- `docs/standards/zekelman/extracted/2016_sample_assessment_questions_standards_1_2_zekelman_chumash_raw_text.md`
- `docs/standards/zekelman/extracted/2014_appendix_free_resource_packet_zekelman_chumash_raw_text.md`
- `docs/standards/zekelman/extracted/2025_zekelman_chumash_standards_v2_5_complete_levels_1_8_raw_text.md`

### Provenance and planning files

- `data/standards/zekelman/source_inventory.json`
- `data/standards/zekelman/source_map.md`
- `data/standards/zekelman/extraction_plan.md`
- `docs/standards/zekelman/reports/zekelman_source_upgrade_report.md`

## 4. Files Changed

### Added files

- `docs/standards/zekelman/extracted/2025_zekelman_chumash_standards_v2_5_complete_levels_1_8_raw_text.md`
- `docs/standards/zekelman/reports/zekelman_2025_canonical_source_ingestion_report.md`

### Modified files

- `PLANS.md`
- `docs/standards/zekelman/indexes/zekelman_document_index.json`
- `data/standards/zekelman/source_inventory.json`
- `data/standards/zekelman/source_map.md`
- `data/standards/zekelman/extraction_plan.md`

## 5. Source Hierarchy

### Canonical source

- `docs/standards/zekelman/raw/2025_zekelman_chumash_standards_v2_5_complete_levels_1_8.pdf`

### Supplemental sources

- `docs/standards/zekelman/raw/2014_intro_vocabulary_language_skills_zekelman_chumash.pdf`
- `docs/standards/zekelman/raw/2016_sample_assessment_questions_standards_1_2_zekelman_chumash.pdf`
- `docs/standards/zekelman/raw/2014_appendix_free_resource_packet_zekelman_chumash.pdf`

### Conflict rule

If the 2025 / Version 2.5 canonical standards file conflicts with older 2014/2016 supplemental material, the 2025 source wins for:
- current standards wording
- standard numbering
- level progression
- scope and sequence

The older sources remain valid as supplemental educational-design material, appendices, and scaffolding references.

## 6. OCR / Extraction Risks

- Hebrew requires human review
- nikud and taamim require human review
- tables require human review
- bidirectional text may be imperfect
- raw extracted text must not be treated as production structured data

## 7. Runtime Safety

No runtime, student-facing, generated-question, reviewed-bank, release, or production files were changed in this branch task.

## 8. Next Recommended Task

Recommended next branch:
- `feature/zekelman-standards-structured-extraction`

Recommended next task:
- extract canonical standard IDs, titles, areas, and scope/sequence from the 2025 canonical standards source
- cross-check Standard 3 vocabulary and language skills against the 2014 introduction guide
- cross-check Hebrew terms by grade and Chumash conventions against the 2014 appendix
- extract assessment item archetypes from the 2016 sample assessments
- keep all structured extraction in draft/source mode until reviewed
