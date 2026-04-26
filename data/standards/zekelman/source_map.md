# Zekelman Source Map

## Purpose

This map explains which Zekelman-family source should be used for which purpose in the Torah AI / Chumash Question Engine.

## Canonical Source

Primary canonical file:
- `docs/standards/zekelman/raw/2025_zekelman_chumash_standards_v2_5_complete_levels_1_8.pdf`

Use this file for:
- official current standards wording
- level progression
- standard numbering
- scope and sequence
- future machine-readable standards extraction

Why this file is canonical:
- it is the complete Version 2.5 (2025) Chumash standards source
- it now exists in the repo as the actual raw PDF, not only as a reference in seed metadata
- existing crosswalk and foundations seed files already treated Zekelman Standards 2.5 and the Appendix as canonical truth

Extraction companion:
- `docs/standards/zekelman/extracted/2025_zekelman_chumash_standards_v2_5_complete_levels_1_8_raw_text.md`

Important caution:
- raw extracted text is a convenience layer only
- Hebrew, nikud, taamim, tables, and bidirectional text still require human review before production structuring

## Preferred Supplemental Sources

### 2014 Introduction to Vocabulary and Language Skills

Primary file:
- `docs/standards/zekelman/raw/2014_intro_vocabulary_language_skills_zekelman_chumash.pdf`

Use this for:
- language-skill scaffolding
- student-friendly grammar and language explanations
- dikduk framing
- question-template inspiration for vocabulary and language skills

Extraction companion:
- `docs/standards/zekelman/extracted/2014_intro_vocabulary_language_skills_zekelman_chumash_raw_text.md`

### 2016 Sample Assessment Questions

Primary file:
- `docs/standards/zekelman/raw/2016_sample_assessment_questions_standards_1_2_zekelman_chumash.pdf`

Use this for:
- assessment design
- diagnostic item archetypes
- rigor calibration
- selected-response models
- extended-response examples
- performance-assessment examples

Extraction companion:
- `docs/standards/zekelman/extracted/2016_sample_assessment_questions_standards_1_2_zekelman_chumash_raw_text.md`

### 2014 Appendix / Free Resource Packet

Primary file:
- `docs/standards/zekelman/raw/2014_appendix_free_resource_packet_zekelman_chumash.pdf`

Use this for:
- Hebrew terms by grade
- Chumash conventions
- content appendix material
- high-frequency vocabulary
- cumulative skill and vocabulary progression support

Extraction companion:
- `docs/standards/zekelman/extracted/2014_appendix_free_resource_packet_zekelman_chumash_raw_text.md`

Existing derived artifacts already tied to this appendix:
- `data/foundations/incoming/high_frequency_lexicon_seed.json`
- `data/lexicon/high_frequency/high_frequency_lexicon.seed.v1.json`
- `data/standards/crosswalks/canonical_skill_crosswalk.seed.v1.json`
- `data/standards/crosswalks/canonical_skill_crosswalk.seed.v1.csv`

## Derived Internal Artifacts

These remain useful internal working layers, but they are not substitutes for raw source documents:
- `data/standards/crosswalks/canonical_skill_crosswalk.seed.v1.json`
- `data/standards/crosswalks/canonical_skill_crosswalk.seed.v1.csv`
- `data/foundations/incoming/canonical_skill_crosswalk_seed.json`
- `data/foundations/incoming/high_frequency_lexicon_seed.json`
- `data/lexicon/high_frequency/high_frequency_lexicon.seed.v1.json`

Use them for:
- internal mapping
- foundations seeding
- lexicon seeding
- provenance back-references

Do not use them as the sole authority where exact standards wording, numbering, or table layout matters.

## Conflict Rule

If the 2025 / Version 2.5 canonical standards file conflicts with older 2014/2016 supplemental material:

- the 2025 / Version 2.5 file wins for:
  - current standards wording
  - standard numbering
  - level progression
  - scope and sequence

- the older supplemental files still remain valuable for:
  - language-skill framing
  - appendix content
  - assessment examples
  - historical and educational design support

## Extraction Risk Rule

All extracted PDF text files in this source layer are convenience layers only.

Before any structured production use:
- manually review Hebrew extraction output
- manually review nikud and taamim
- manually review tables and grade-by-grade lists
- manually review bidirectional text
- manually verify assessment examples where formatting affects meaning
