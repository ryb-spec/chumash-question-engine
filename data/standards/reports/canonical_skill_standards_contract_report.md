# Canonical Skill Standards Contract Report

- Branch: `feature/canonical-skill-standards-contract`
- Scope audited:
  - runtime skill catalog in `skill_catalog.py`
  - canonical crosswalk seed in `data/standards/crosswalks/canonical_skill_crosswalk.seed.v1.json`
  - Zekelman Standard 3 draft mappings in `data/standards/zekelman/crosswalks/zekelman_2025_standard_3_skill_mapping_draft.json`
  - verified source-to-skill maps in `data/verified_source_skill_maps/`
  - source-skill enrichment pilot artifacts in `data/source_skill_enrichment/`
- Chosen status model:
  - `review_only`
  - `source_extraction_verified`
  - `teacher_approved_input_candidate`
  - `teacher_approved_for_protected_preview`
  - `protected_preview_only`
  - `reviewed_bank_candidate`
  - `runtime_ready`

## What Was Repaired

- Runtime skills already had a crosswalk-based mapping path, but the repo did not have one deterministic contract that also tracked:
  - Zekelman draft skill IDs
  - verified source-map skill labels
  - enrichment-candidate mappings
  - conservative status boundaries across review-only, source-verified, and runtime-ready layers
- The new contract keeps runtime-backed lanes explicit without treating Standard 3 review work, source extraction verification, or enrichment as runtime approval.
- The contract also records the active source scope and canonical source SHA so the alignment layer cannot drift away from the current Step 3 source truth.

## Canonical Skill Coverage

- Canonical skills included: 28
- Runtime skills mapped: 21
- Zekelman Standard 3 draft skill mappings covered: 13
- Verified source-skill labels covered:
  - `skill_primary = phrase_translation`
  - `skill_secondary = translation_context`
  - `skill_id = phrase_translation`
- Source-skill enrichment candidate mappings covered: 17

## Safety Gates Confirmed Closed

- Verified source-to-skill rows remain extraction-verified or pending extraction review only.
- Source-to-skill rows still keep:
  - `question_allowed = needs_review` or closed
  - `runtime_allowed = false`
  - `protected_preview_allowed = false`
  - `reviewed_bank_allowed = false`
- Source-skill enrichment rows still keep:
  - `question_allowed = needs_review`
  - `runtime_allowed = false`
  - `protected_preview_allowed = false`
  - `reviewed_bank_allowed = false`
- No Standard 3 review-only or enrichment-only artifact is treated as teacher approval.
- No protected-preview, reviewed-bank, or runtime approval is introduced by this Step 3 contract.

## Validation Commands

- `python scripts/validate_source_texts.py`
- `python scripts/validate_curriculum_extraction.py`
- `python scripts/validate_verified_source_skill_maps.py`
- `python scripts/validate_source_skill_enrichment.py`
- `python scripts/validate_canonical_skill_contract.py`
- `python -m pytest tests/test_source_texts_validation.py -q`
- `python -m pytest tests/test_corpus_manifest.py -q`
- `python -m pytest tests/test_verified_source_skill_maps.py -q`
- `python -m pytest tests/test_source_skill_enrichment.py -q`
- `python -m pytest tests/test_canonical_skill_contract.py -q`
- `python -m pytest -q`

## Remaining Gaps

- No known remaining canonical skill/standards contract blockers.
- Future work may tighten granularity further, but that work belongs to later review or teacher-approval steps, not this Step 3 contract pass.
