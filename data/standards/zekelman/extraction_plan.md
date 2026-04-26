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
   - 2025 / Version 2.5 Zekelman Standards when available
2. Preferred supplemental raw PDFs:
   - 2014 Introduction to Vocabulary and Language Skills
   - 2016 Sample Assessment Questions for Standards 1-2
   - 2014 Appendix / Free Resource Packet
3. Derived internal artifacts:
   - crosswalk seeds
   - foundations seeds
   - high-frequency lexicon seeds

## Extraction Priorities For The Next Branch

### Priority 1

- Standard 3 vocabulary and language skills
- Hebrew terms by grade
- Chumash conventions

### Priority 2

- assessment item archetypes
- standards-to-skill mapping candidates
- high-frequency vocabulary policy tables

### Priority 3

- question-template exemplars
- diagnostic lane candidates for vocabulary, dikduk, and passage comprehension

## Method Rules

- start from the cleanest raw PDF available
- preserve provenance from every extracted field back to source page(s)
- keep page-level references for all structured extraction drafts
- do not silently normalize Hebrew text
- do not silently correct OCR/extraction errors
- flag all tables, Hebrew terms lists, nikud/taamim fields, and bidi text for human review

## Proposed Next Branch

`feature/zekelman-standards-structured-extraction`

## Proposed Next Task

Build a draft machine-readable Zekelman standards/skills extraction from the cleanest sources, starting with:
- Standard 3 vocabulary and language skills
- Hebrew terms by grade
- Chumash conventions
- assessment item archetypes
