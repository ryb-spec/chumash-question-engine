# Batch 005 Hebrew Source Prep

- Branch: `feature/curriculum-batch-005-hebrew-source-prep`
- Date: `2026-04-24`

## Purpose

Unblock Batch 005 by adding a traceable local Hebrew source for `Bereishis 4:1-4:16` in the repo's existing canonical source-file format, without starting extraction work or changing runtime scope.

## Files Inspected

- `data/curriculum_extraction/reports/batch_005_source_gap_request.md`
- `data/pesukim_100.json`
- `data/parsed_pesukim.json`
- `data/source/bereishis_3_17_to_3_24.json`
- `data/curriculum_extraction/curriculum_extraction_manifest.json`
- `tests/test_source_corpus_block_3_17_to_3_24.py`
- `tests/test_corpus_manifest.py`

## Files Created / Modified

- Created: `data/source/bereishis_4_1_to_4_16.json`
- Created: `data/curriculum_extraction/reports/batch_005_hebrew_source_prep.md`
- Created: `tests/test_source_corpus_block_4_1_to_4_16.py`
- Modified: none

## Exact Range Added

- `Bereishis 4:1-4:16`

## Source Attribution

- Source: `Sefaria`
- Source provenance: `user-provided Hebrew text`
- URL supplied by user: `https://www.sefaria.org/Genesis.4.16?lang=he&aliyot=0`

## Source Format Used

The repo's existing canonical Hebrew source format was used:

- `data/source/bereishis_4_1_to_4_16.json`

Schema used:

- `metadata.title`
- `metadata.range`
- `metadata.format`
- `pesukim[]`
- each pasuk entry contains:
  - `sefer`
  - `perek`
  - `pasuk`
  - `text`

The user-provided vocalized Hebrew text was preserved exactly in the `text` field for each pasuk.

## Source Trust Confirmations

- Hebrew was not taken from noisy PDF OCR/text.
- The source file uses the user-provided Sefaria Hebrew text exactly for `Bereishis 4:1-4:16`.
- `Bereishis 4:17` was reportedly supplied by the user outside the needed Batch 005 range, but it was intentionally excluded from this source-prep output.

## Batch Boundary Confirmations

- Batch 005 extraction was not started.
- No Batch 005 normalized JSONL was created.
- No Batch 005 preview JSONL was created.
- No Batch 005 manual-review packet was created.
- No runtime scope or runtime payload was changed.

## Validation Results

- `python scripts/validate_curriculum_extraction.py`: PASS
- `python scripts/load_curriculum_extraction.py --summary`: PASS
- `python -m pytest tests/test_curriculum_extraction_validation.py tests/test_curriculum_question_preview.py tests/test_source_corpus_block_4_1_to_4_16.py`: PASS
- `python -m pytest`: PASS

## Remaining Blockers

- No Hebrew-source blocker remains for `Bereishis 4:1-4:16`.
- Batch 005 extraction remains intentionally out of scope for this branch.
- No remaining source-prep blocker remains in this branch.

## Recommendation

`READY_FOR_BATCH_005_EXTRACTION`

Next action:

- return to `feature/curriculum-batch-005-bereishis-4-start`, or recreate it fresh from `main`
- rerun Batch 005 extraction using the newly added `data/source/bereishis_4_1_to_4_16.json` as the local Hebrew alignment source
