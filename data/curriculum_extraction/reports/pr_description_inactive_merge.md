Title:
Add inactive curriculum extraction factory and Batch 001 preview pipeline

## Summary

This PR adds an isolated curriculum extraction factory under `data/curriculum_extraction`. It includes schemas, source registry, manifest, cleaned seed data, validation, loader, preview question generation, and reports. It is inactive infrastructure only and does not affect runtime behavior.

## What Changed

- Added the isolated curriculum extraction scaffold and contract files under `data/curriculum_extraction`
- Added source registry, manifest, JSON schemas, tiny samples, and normalized Batch 001 cleaned seed data
- Added curriculum extraction validation and loading scripts
- Added review reports, source-gap reports, answer-enrichment reports, and merge-readiness reports
- Added Batch 001 preview generation tooling and preserved both preview artifacts:
  - `batch_001_preview.jsonl`
  - `batch_001_preview_v2.jsonl`
- Regenerated preview v2 using supported lanes only after vocab gloss enrichment

## What Did Not Change

- No changes to `streamlit_app.py`
- No changes under `runtime/`
- No changes under `engine/`
- No changes to `assessment_scope.py`
- No changes to `data/corpus_manifest.json`
- No changes to active reviewed question bank files
- No UI, scoring, mastery, or active-scope changes
- No runtime integration
- No corpus promotion

## Validation/Testing

- `python scripts/validate_curriculum_extraction.py` — PASS
- `python scripts/load_curriculum_extraction.py --summary` — PASS
- `python -m pytest` — PASS (`453 passed`)

## Supported Lanes

- `phrase_translation`
- `hebrew_to_english_match`
- `english_to_hebrew_match`
- `shoresh_identification` where source data exists
- `prefix_identification` where source data exists
- `suffix_identification` where source data exists
- vocab matching with source-backed Batch 001 gloss enrichment

## Blocked Lanes

- `mi_amar_el_mi`
  - blocked because Va'eira answer keys are not present
- `al_mi_neemar`
  - blocked because Va'eira answer keys are not present
- Shemos `word_parse_task` answer checking
  - blocked because the Shemos answer key is not present

## Why This Is Safe To Merge

- All extraction artifacts remain non-runtime and isolated
- The loader still ignores preview data safely
- The validator enforces non-runtime status and source linkage
- The reviewed question bank remains untouched
- Corpus scope remains unchanged
- Full test coverage remains green

## What Comes Next

- Continue future extraction in separate source-scoped batches
- Add answer-bearing source material for blocked Shemos and Va'eira lanes
- Regenerate previews only after those source keys are present
- Keep runtime integration blocked until a separate explicit integration effort is reviewed and approved
