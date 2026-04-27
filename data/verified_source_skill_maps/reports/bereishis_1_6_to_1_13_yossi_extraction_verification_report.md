# Bereishis 1:6-1:13 Yossi Extraction Verification Report

## A. Verification Summary

Yossi reviewed and verified all 37 rows in the Bereishis 1:6-1:13 source-to-skill map for extraction accuracy.

This verification records extraction-accuracy confirmation only. It does not approve question generation, protected-preview use, reviewed-bank promotion, runtime activation, or student-facing release.

## B. Scope

- Scope: Bereishis 1:6-1:13
- Map file: `data/verified_source_skill_maps/bereishis_1_6_to_1_13_source_to_skill_map.tsv`
- Review packet: `data/verified_source_skill_maps/reports/bereishis_1_6_to_1_13_source_to_skill_map_exceptions_review_packet.md`
- Build report: `data/verified_source_skill_maps/reports/bereishis_1_6_to_1_13_source_to_skill_map_build_report.md`

## C. Rows Verified

- Rows verified: 37
- Verification status applied: `yossi_extraction_verified`

## D. What Was Verified

- Source matching
- Phrase joins
- Metsudah alignment
- Koren secondary alignment where present
- Translation/source matching
- Classification reasonableness for the current `phrase_translation` slice

## E. What Was Not Approved

- Not question approval
- Not protected-preview approval
- Not runtime approval
- Not reviewed-bank promotion
- Not student-facing release
- Not generated-question approval
- Not answer-key approval

## F. Safety Statuses

- `question_allowed` remains `needs_review`
- `runtime_allowed` remains `false`
- `protected_preview_allowed` remains `false`
- `reviewed_bank_allowed` remains `false`

Every row in this slice remains not question-ready, not runtime-ready, not protected-preview-ready, not reviewed-bank-ready, and not student-facing.

## G. Next Recommended Step

Use `scripts/build_source_to_skill_map.py` to generate the next safe contiguous source-to-skill slice after Bereishis 1:13 with conservative statuses, then create an exceptions review packet for Yossi before any further verification.
