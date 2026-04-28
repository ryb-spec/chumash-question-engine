# Bereishis 1:24-1:31 Enrichment Candidate Generation Report

## Source Map Used

- `data/verified_source_skill_maps/bereishis_1_24_to_1_31_source_to_skill_map.tsv`

## Scope

Bereishis 1:24-1:31.

## Source-to-Skill Row Count

- source-to-skill rows: 38

## Candidate Counts By Category

- morphology: 26
- vocabulary_shoresh: 40
- standards: 14
- token_split_standards: 56
- total_candidates: 136

## Evidence Sources Used

- `data/verified_source_skill_maps/bereishis_1_24_to_1_31_source_to_skill_map.tsv`
- `data/word_bank.json`
- `data/curriculum_extraction/raw_sources/batch_001/vocabulary_priority_pack_cleaned.md`
- `data/curriculum_extraction/reports/batch_001_source_gap_request.md`
- `data/standards/zekelman/structured/zekelman_2025_standard_3_vocabulary_language_skills.json`
- `data/standards/canonical_skill_contract.json`

## Confidence Breakdown

- high: 0
- medium: 94
- low: 42

## Morphology Summary

- review-only morphology candidates: 26
- follow-up morphology candidates: 13
- no morphology candidate is verified in this task

## Vocabulary/Shoresh Summary

- review-only vocabulary/shoresh candidates: 40
- follow-up vocabulary/shoresh candidates: 6
- First 150-style evidence is treated as review evidence only, not question approval

## Standards Summary

- phrase-level standards candidates: 14
- all phrase-level standards candidates remain `needs_follow_up` because they are broad or mixed-lane

## Token-Split Standards Summary

- token-split standards candidates: 56
- token-split standards rows are review-only and safety-closed
- noun vocabulary rows are pending Yossi review, not verified
- weak verb/prefix rows remain `needs_follow_up`

## Unresolved/Follow-Up Themes

- future/jussive/imperative verb-form uncertainty
- vav narrative/stem interpretation uncertainty
- prefix/preposition standards mapping
- context-heavy construct/inflected noun tokens
- phrase-level standards rows superseded by token-split candidates

## Perek 1 Enrichment Coverage Note

- This slice completes enrichment candidate coverage across Bereishis Perek 1 (1:1-1:5, 1:6-1:13, 1:14-1:23, 1:24-1:31).
- It does not complete Yossi review or any later approval gate.

## Canonical Contract Alignment Summary

- token-split standards candidates use canonical skill ids and canonical standard anchors from `data/standards/canonical_skill_contract.json`
- standards anchors use 3.01, 3.02, 3.03, 3.06, or 3.07 where contract-supported
- no contract mapping concern blocks this review-ready slice

## Hebrew Encoding Check

- TSV, CSV, and Markdown artifacts are written as UTF-8
- review CSV files are UTF-8-BOM
- Hebrew tokens are real UTF-8 Hebrew and not placeholder question marks

## Safety Gate Summary

- `question_allowed = needs_review` on every candidate
- `protected_preview_allowed = false` on every candidate
- `reviewed_bank_allowed = false` on every candidate
- `runtime_allowed = false` on every candidate
- no candidate is question-ready, protected-preview-ready, reviewed-bank-ready, runtime-ready, or student-facing

## Next Yossi Action

- Yossi reviews the Bereishis 1:24-1:31 enrichment review sheets, then only explicit reviewed decisions are applied back into the enrichment layer.
