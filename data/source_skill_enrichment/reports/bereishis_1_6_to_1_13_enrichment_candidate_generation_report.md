# Bereishis 1:6-1:13 Enrichment Candidate Generation Report

## Source Map Used

- `data/verified_source_skill_maps/bereishis_1_6_to_1_13_source_to_skill_map.tsv`

## Candidate Counts By Category

- morphology: 7
- vocabulary_shoresh: 6
- standards: 6
- token_split_standards: 13

## Evidence Sources Used

- `data/verified_source_skill_maps/bereishis_1_6_to_1_13_source_to_skill_map.tsv`
- `data/word_bank.json`
- `data/curriculum_extraction/reports/batch_002_manual_review_packet.md`
- `data/curriculum_extraction/raw_sources/batch_001/vocabulary_priority_pack_cleaned.md`
- `data/standards/zekelman/structured/zekelman_2025_standard_3_vocabulary_language_skills.json`
- `data/standards/zekelman/crosswalks/zekelman_2025_standard_3_supplemental_crosswalk.json`

## Confidence Breakdown

- high: 0
- medium: 21
- low: 11

## Token-Split Standards Summary

- parent bundled standards rows prepared: 6
- token-level replacement candidates prepared: 13
- token-split rows are review-only and safety-closed

## Follow-Up Count

- candidates currently marked `needs_follow_up`: 18

## Contract Alignment Summary

- token-split standards candidates use canonical skill ids and canonical standard anchors from `data/standards/canonical_skill_contract.json`
- phrase-level standards candidates stay conservative and point only to contract-supported Standard 3 lanes
- morphology and vocabulary candidates remain in the enrichment layer only and do not imply later approval gates

## Safety Gate Summary

- `question_allowed = needs_review` on every new candidate
- `protected_preview_allowed = false` on every new candidate
- `reviewed_bank_allowed = false` on every new candidate
- `runtime_allowed = false` on every new candidate
- no candidate is question-ready, protected-preview-ready, reviewed-bank-ready, runtime-ready, or student-facing

## Next Yossi Action

- Review the Bereishis 1:6-1:13 morphology, vocabulary/shoresh, standards, and token-split standards review sheets and apply only reviewed decisions back into the enrichment layer.
