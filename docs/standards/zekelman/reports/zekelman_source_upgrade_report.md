# Zekelman Source Upgrade Report

> Historical note: this report reflects the state before the 2025 / Version 2.5 canonical standards PDF was ingested into the repo. For the canonical-source update, see `docs/standards/zekelman/reports/zekelman_2025_canonical_source_ingestion_report.md`.

## 1. Summary

### What was added

- Three clean Zekelman-family PDFs were added under `docs/standards/zekelman/raw/`.
- Page-delimited extraction companions were added under `docs/standards/zekelman/extracted/`.
- A repo-wide Zekelman source inventory was added at `data/standards/zekelman/source_inventory.json`.
- A human-readable source map was added at `data/standards/zekelman/source_map.md`.
- A short extraction plan was added at `data/standards/zekelman/extraction_plan.md`.
- A document index with hashes, file sizes, and extraction coverage was added at `docs/standards/zekelman/indexes/zekelman_document_index.json`.

### What was already present

- Existing repo seed and crosswalk artifacts already referenced:
  - Zekelman Standards 2.5 (2025)
  - the 2014 Appendix / Free Resource Packet
- Existing derived artifacts include:
  - `data/standards/crosswalks/canonical_skill_crosswalk.seed.v1.json`
  - `data/standards/crosswalks/canonical_skill_crosswalk.seed.v1.csv`
  - `data/foundations/incoming/canonical_skill_crosswalk_seed.json`
  - `data/foundations/incoming/high_frequency_lexicon_seed.json`
  - `data/lexicon/high_frequency/high_frequency_lexicon.seed.v1.json`

### What was extracted

- `2014_intro_vocabulary_language_skills_zekelman_chumash_raw_text.md`
- `2016_sample_assessment_questions_standards_1_2_zekelman_chumash_raw_text.md`
- `2014_appendix_free_resource_packet_zekelman_chumash_raw_text.md`

### What was classified

- canonical reference-only standards source
- three newly ingested preferred supplemental PDFs
- five existing derived Zekelman-dependent artifacts

### What was not done

- no runtime feature work
- no structured standards extraction yet
- no production question generation
- no normalization/correction of extracted Hebrew
- no claim that OCR/extracted text is production-safe

## 2. File-by-File Review

### Canonical reference already present in repo metadata

- Path:
  - `REFERENCE_ONLY:data/standards/crosswalks/canonical_skill_crosswalk.seed.v1.json#meta.sources.zekelman_standards_2025`
- Title:
  - `Zekelman Standards for Chumash`
- Year/version:
  - `2025 / Version 2.5`
- Quality:
  - `unknown on this branch`
- Contents:
  - canonical standards wording and level progression, as referenced by repo seed files
- Project relevance:
  - canonical standards mapping truth
  - skill taxonomy authority
  - vocabulary/language-skill progression authority
- Warnings:
  - raw 2025 PDF not present in repo on this branch
  - canonical status is reference-backed, not newly ingested

### Newly added clean supplemental source: Vocabulary / language skills

- Path:
  - `docs/standards/zekelman/raw/2014_intro_vocabulary_language_skills_zekelman_chumash.pdf`
- Title:
  - `Introduction to Vocabulary and Language Skills for the Zekelman Standards for Chumash`
- Year/version:
  - `תשע"ד / August 2014`
- Page count:
  - `53`
- Quality:
  - `born-digital / clean PDF`
- Contents:
  - vocabulary and language-skill explanations
  - nouns
  - adjectives
  - סמיכות
  - טעמי המקרא
  - conjunctions, prepositions, pronouns, possessives, verbs
  - נקודות, דגשים, שוא, מפיק
- Project relevance:
  - skill taxonomy
  - dikduk rules
  - question-template design
  - vocabulary progression scaffolding
- Warnings:
  - extracted text is a convenience layer only
  - Hebrew and layout-sensitive content still require human review

### Newly added clean supplemental source: Sample assessments

- Path:
  - `docs/standards/zekelman/raw/2016_sample_assessment_questions_standards_1_2_zekelman_chumash.pdf`
- Title:
  - `Sample Assessment Questions For Zekelman Standards for Chumash - Standard 1-2`
- Year/version:
  - `Second Edition / February 2016`
- Page count:
  - `190`
- Quality:
  - `born-digital / clean PDF`
- Contents:
  - selected-response assessment items
  - question architecture for Standards 1-2
  - extended-response and performance-assessment examples
- Project relevance:
  - assessment model generation
  - diagnostic engine design
  - rigor calibration
  - sample item archetypes
- Warnings:
  - early pages contain slightly different grade-range wording that should be manually reviewed
  - extracted text should not be treated as exact truth where formatting changes meaning

### Newly added clean supplemental source: Appendix / free resource packet

- Path:
  - `docs/standards/zekelman/raw/2014_appendix_free_resource_packet_zekelman_chumash.pdf`
- Title:
  - `Zekelman Standards for Chumash, 2014 - Appendix / Free Resource Packet`
- Year/version:
  - `2014 / Appendix 0`
- Page count:
  - `65`
- Quality:
  - `born-digital / clean PDF`
- Contents:
  - Hebrew terms by grade
  - Chumash conventions
  - content appendices
  - high-frequency vocabulary study and progression support
- Project relevance:
  - vocabulary development
  - Chumash conventions
  - standards appendix support
  - source validation for derived lexicon artifacts
- Warnings:
  - tables and frequency-study layouts require manual validation before structuring
  - extracted text is not a substitute for source-checked appendix data

### Existing derived artifact: canonical crosswalk seed JSON

- Path:
  - `data/standards/crosswalks/canonical_skill_crosswalk.seed.v1.json`
- Quality:
  - `derived structured artifact`
- Project relevance:
  - internal standards mapping
  - canonical-to-engine bridge
- Warnings:
  - not a raw standards source
  - some Hebrew appendix references show encoding issues

### Existing derived artifact: canonical crosswalk seed CSV

- Path:
  - `data/standards/crosswalks/canonical_skill_crosswalk.seed.v1.csv`
- Quality:
  - `derived structured artifact`
- Project relevance:
  - review/export convenience for mapping work
- Warnings:
  - not a raw standards source

### Existing derived artifact: incoming canonical crosswalk seed

- Path:
  - `data/foundations/incoming/canonical_skill_crosswalk_seed.json`
- Quality:
  - `derived structured artifact`
- Project relevance:
  - foundations staging
  - provenance back-reference
- Warnings:
  - not a raw standards source

### Existing derived artifact: incoming high-frequency lexicon seed

- Path:
  - `data/foundations/incoming/high_frequency_lexicon_seed.json`
- Quality:
  - `derived structured artifact`
- Project relevance:
  - vocabulary development
  - appendix-backed foundations staging
- Warnings:
  - not a raw appendix source
  - some Hebrew output appears encoding-sensitive

### Existing derived artifact: stable high-frequency lexicon seed

- Path:
  - `data/lexicon/high_frequency/high_frequency_lexicon.seed.v1.json`
- Quality:
  - `derived structured artifact`
- Project relevance:
  - vocabulary progression policy
  - appendix-backed lexicon seeding
- Warnings:
  - not a raw appendix source
  - some Hebrew output appears encoding-sensitive

## 3. Duplicate / Overlap Analysis

- No older raw Zekelman PDFs, scan-only copies, or OCR-only overlap files were found in this repo on this branch.
- No newly added PDF overwrote an existing repo file.
- The strongest overlap observed was indirect:
  - the 2014 Appendix PDF is already cited by existing crosswalk and lexicon seed artifacts
  - the 2025 standards file is already cited by crosswalk seed artifacts, but the raw file itself was not present

Practical conclusion:
- the new Appendix PDF strengthens provenance for existing derived artifacts
- the new Introduction and Sample Assessments PDFs expand the source base rather than replacing an in-repo raw file

## 4. Recommended Source Hierarchy

### Canonical source

- `Zekelman Standards for Chumash` (2025 / Version 2.5), as referenced in existing repo metadata
- Use for:
  - standards wording
  - level progression
  - canonical standard numbering

### Preferred supplemental sources

- `2014_intro_vocabulary_language_skills_zekelman_chumash.pdf`
- `2016_sample_assessment_questions_standards_1_2_zekelman_chumash.pdf`
- `2014_appendix_free_resource_packet_zekelman_chumash.pdf`

### Archive / superseded sources

- None found as raw overlapping source files on this branch

## 5. Project Usefulness

These sources strengthen:

- skill taxonomy
  - vocabulary/language-skills guide provides atomic skill framing
- standards mapping
  - canonical crosswalk references gain clearer raw-source provenance
- vocabulary development
  - appendix supports grade-by-grade Hebrew terms and frequency policy
- dikduk/language rules
  - introduction guide supports rule-group framing and terminology
- assessment model generation
  - sample assessments provide item-shape exemplars
- diagnostic engine design
  - sample assessments and skill guide together support future non-runtime item modeling
- mastery tracking
  - standards hierarchy and vocabulary progression can be mapped more carefully
- future reviewed question bank validation
  - appendix and sample assessments can support human review criteria and scope checks

## 6. OCR / Extraction Risk

Even though these PDFs appear clean and text extraction works:

- Hebrew extraction may still be unreliable
- nikud and taamim may not extract correctly
- tables may require manual validation
- bidirectional text may shift order or spacing
- no production extraction should rely on raw extracted text alone

## 7. Next Recommended Branch / Task

Recommended next branch:

- `feature/zekelman-standards-structured-extraction`

Recommended next task:

Build a draft machine-readable Zekelman standards/skills extraction from the cleanest sources, starting with:
- Standard 3 vocabulary and language skills
- Hebrew terms by grade
- Chumash conventions
- assessment item archetypes
