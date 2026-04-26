# Zekelman Source Map

## Purpose

This map explains which Zekelman-family source should be used for which purpose in the Torah AI / Chumash Question Engine.

## A. Canonical Standards Source

The repo's current policy already treats the 2025 / Version 2.5 Zekelman Standards file as the canonical source for current standards wording and level progression.

- Canonical reference in repo metadata:
  - `data/standards/crosswalks/canonical_skill_crosswalk.seed.v1.json`
  - `data/foundations/incoming/canonical_skill_crosswalk_seed.json`
- Canonical source label in those files:
  - `Zekelman Standards 2.5 and Appendix = canonical truth`
- Raw-file status on this branch:
  - The actual 2025 / Version 2.5 PDF was not present in the repo on this branch.
  - It therefore remains canonical by policy/reference, but not by newly ingested bytes in this branch.

Use the 2025 / Version 2.5 standards whenever current wording, level progression, or standard numbering must be treated as authoritative.

## B. Preferred Supplemental Sources

### Introduction to Vocabulary and Language Skills

Primary file:
- `docs/standards/zekelman/raw/2014_intro_vocabulary_language_skills_zekelman_chumash.pdf`

Use this for:
- atomic language-skill explanations
- student-friendly skill framing
- dikduk scaffolding
- question-template inspiration for nouns, adjectives, סמיכות, טעמי המקרא, prefixes, pronouns, possessives, verbs, נקודות, דגשים, שוא, and מפיק

Extraction companion:
- `docs/standards/zekelman/extracted/2014_intro_vocabulary_language_skills_zekelman_chumash_raw_text.md`

### Sample Assessment Questions

Primary file:
- `docs/standards/zekelman/raw/2016_sample_assessment_questions_standards_1_2_zekelman_chumash.pdf`

Use this for:
- assessment design
- rigor calibration
- diagnostic item models
- selected-response patterns
- extended-response examples
- performance-assessment models
- Standards 1-2 question architecture

Extraction companion:
- `docs/standards/zekelman/extracted/2016_sample_assessment_questions_standards_1_2_zekelman_chumash_raw_text.md`

### Free Resource Packet / Appendix

Primary file:
- `docs/standards/zekelman/raw/2014_appendix_free_resource_packet_zekelman_chumash.pdf`

Use this for:
- Hebrew terms by grade
- Chumash conventions
- Standard 2 content appendix
- high-frequency vocabulary
- cumulative skill/vocabulary progression

Extraction companion:
- `docs/standards/zekelman/extracted/2014_appendix_free_resource_packet_zekelman_chumash_raw_text.md`

Existing derived artifacts already tied to this appendix:
- `data/foundations/incoming/high_frequency_lexicon_seed.json`
- `data/lexicon/high_frequency/high_frequency_lexicon.seed.v1.json`
- `data/standards/crosswalks/canonical_skill_crosswalk.seed.v1.json`
- `data/standards/crosswalks/canonical_skill_crosswalk.seed.v1.csv`

## C. Derived Internal Artifacts

These are useful internal working layers, but they are not substitutes for raw source documents:

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

Do not use them as the sole authority where exact standards wording or exact appendix/tabular wording matters.

## D. Superseded or Lower-Quality Scans

No overlapping older raw Zekelman scans or OCR-only source files were located in this repo on this branch.

That means:
- no raw in-repo Zekelman PDF was deleted
- no raw in-repo Zekelman PDF was overwritten
- no raw in-repo Zekelman PDF was reclassified as superseded based on direct byte-for-byte overlap

If lower-quality scans surface later, keep them for provenance but classify them as `superseded` or `archive` when a cleaner copy is confirmed to contain the same material.

## E. Conflict Rule

If a conflict exists between the referenced 2025 / Version 2.5 standards and older 2014/2016 materials:

- the newer canonical standards source wins for standards wording and level progression
- the older files still remain valuable for:
  - examples
  - appendices
  - question design
  - vocabulary and language-skill scaffolding
  - historical/source support

## F. Extraction Risk Rule

Raw PDF extraction files are convenience layers only.

Before any structured production use:
- manually review Hebrew OCR/extraction output
- manually review nikud and taamim
- manually review bidirectional text
- manually verify tables and grade-by-grade lists
- manually confirm assessment examples where formatting affects meaning
