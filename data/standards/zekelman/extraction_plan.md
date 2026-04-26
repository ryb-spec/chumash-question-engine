# Zekelman Structured Extraction Plan

## Branch Scope

This branch is limited to source ingestion, provenance, extraction helpers, inventory, and source mapping for Zekelman-family files.

It does not:
- modify runtime behavior
- generate production questions
- activate app features
- rewrite reviewed-bank content

## Source Hierarchy

1. Canonical standards truth:
   - `docs/standards/zekelman/raw/2025_zekelman_chumash_standards_v2_5_complete_levels_1_8.pdf`
2. Preferred supplemental raw PDFs:
   - `docs/standards/zekelman/raw/2014_intro_vocabulary_language_skills_zekelman_chumash.pdf`
   - `docs/standards/zekelman/raw/2016_sample_assessment_questions_standards_1_2_zekelman_chumash.pdf`
   - `docs/standards/zekelman/raw/2014_appendix_free_resource_packet_zekelman_chumash.pdf`
3. Derived internal artifacts:
   - crosswalk seeds
   - foundations seeds
   - high-frequency lexicon seeds

## Recommended Extraction Order For The Next Branch

1. Extract canonical standard IDs, titles, areas, level progressions, and scope/sequence from the 2025 / Version 2.5 canonical source first.
2. Cross-check Standard 3 vocabulary and language skills against the 2014 Introduction to Vocabulary and Language Skills.
3. Cross-check Hebrew terms by grade and Chumash conventions against the 2014 Appendix / Free Resource Packet.
4. Extract assessment item archetypes from the 2016 Sample Assessment Questions.
5. Do not generate production questions until structured source extraction is reviewed.

## Method Rules

- start from the canonical 2025 raw PDF first
- preserve provenance from every extracted field back to source page(s)
- keep page-level references for all structured extraction drafts
- do not silently normalize Hebrew text
- do not silently correct OCR/extraction errors
- flag all tables, Hebrew terms lists, nikud/taamim fields, and bidi text for human review
- treat raw extracted text as a convenience layer, not production structured data

## Proposed Next Branch

`feature/zekelman-standards-structured-extraction`

## Proposed Next Task

Build a draft machine-readable Zekelman standards and skills extraction from the cleanest sources, starting with:
- canonical standard IDs, titles, areas, and scope/sequence from the 2025 standards
- Standard 3 vocabulary and language skills
- Hebrew terms by grade
- Chumash conventions
- assessment item archetypes
