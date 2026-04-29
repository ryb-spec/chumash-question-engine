# Source Truth Reproducibility Finalization Report

## Branch

`feature/teacher-approved-input-list-protected-preview`

## Repair Context

This branch was missing part of the completed Step 1 source-truth reproducibility baseline. Baseline pytest failed because `tests/test_source_texts_validation.py` still expected an older stale SHA-256 value from before the source-truth finalization.

The actual canonical source file SHA-256 was recomputed from `data/source_texts/bereishis_hebrew_menukad_taamim.tsv` before repair:

`4d96c615ab63e0419bff079db250d71ea9b5de266ff9ab8d589ae80e4afd0b71`

## Files Inspected

- `data/source_texts/`
- `data/source_texts/bereishis_hebrew_menukad_taamim.tsv`
- `data/source_texts/source_text_manifest.json`
- `data/corpus_manifest.json`
- `data/source/`
- `data/active_scope_overrides.json`
- `data/active_scope_gold_annotations.json`
- `data/active_scope_reviewed_questions.json`
- `assessment_scope.py`
- `scripts/validate_source_texts.py`
- `tests/test_source_texts_validation.py`
- `tests/test_corpus_manifest.py`

## Source Corpus Entries Verified

The committed corpus manifest declares one current local source corpus:

- Corpus ID: `source_bereishis_1_1_to_3_24_local`
- Sefer: `Bereishis`
- Declared source range: `1:1-3:24`
- Range start: `Bereishis 1:1`
- Range end: `Bereishis 3:24`
- Pesukim count: `80`

The active parsed runtime scope remains:

- Scope ID: `local_parsed_bereishis_1_1_to_3_24`
- Parsed corpus ID: `parsed_bereishis_1_1_to_3_24_root`
- Reviewed question bank: `data/active_scope_reviewed_questions.json`
- Reviewed question count declared in manifest: `238`

`data/active_scope_overrides.json`, `data/active_scope_gold_annotations.json`, and `data/active_scope_reviewed_questions.json` all declare `scope_id` as `local_parsed_bereishis_1_1_to_3_24`.

## Manifest Paths Verified

Corpus-manifest tests verify that all paths declared in `data/corpus_manifest.json` are relative, repo-local, under expected data/review locations, and exist. This includes:

- source files under `data/source/`
- canonical source text under `data/source_texts/`
- active parsed root files under `data/`
- staged provenance files under `data/staged/`
- readiness reports under `data/validation/`
- preview-only and review-only artifact paths under `data/diagnostic_preview/`, `data/standards/`, and `data/curriculum_extraction/`

## SHA/Hash Values Recomputed and Confirmed

Canonical Hebrew source file:

- Path: `data/source_texts/bereishis_hebrew_menukad_taamim.tsv`
- Scope: `Bereishis 1:1-50:26`
- Row count recomputed from TSV rows: `1533`
- First ref: `Bereishis 1:1`
- Last ref: `Bereishis 50:26`
- SHA-256 recomputed from file bytes: `4d96c615ab63e0419bff079db250d71ea9b5de266ff9ab8d589ae80e4afd0b71`

This SHA-256 now matches:

- `data/source_texts/source_text_manifest.json`
- `data/corpus_manifest.json`
- `tests/test_source_texts_validation.py`
- strengthened corpus manifest validation in `tests/test_corpus_manifest.py`

## Active Scope Confirmed

The current active runtime scope is `local_parsed_bereishis_1_1_to_3_24`.

This repair did not expand runtime, promote questions, or alter runtime behavior. It only restored the source-truth baseline expected before Step 4 protected-preview work can begin.

## Validation Strengthened

`tests/test_source_texts_validation.py` verifies the canonical source file SHA and the agreement between the source-text manifest and validator summary.

`tests/test_corpus_manifest.py` verifies:

- every manifest path is relative, repo-local, and under an expected data/review location
- every manifest path exists
- every source corpus declares a canonical source text file and SHA-256
- every declared canonical source SHA-256 matches the actual file bytes
- `data/corpus_manifest.json` and `data/source_texts/source_text_manifest.json` agree on canonical source SHA-256
- active scope sidecar metadata matches the manifest active scope
- preview-only and review-only artifacts remain distinct from runtime

## Final Status

Source truth is aligned for the committed project data:

- Canonical Hebrew source file exists and validates.
- Canonical SHA-256 matches all committed source-text and corpus-manifest references.
- Corpus manifest paths exist and stay inside expected repo locations.
- Active runtime scope is `local_parsed_bereishis_1_1_to_3_24`.
- Source text validation tests pass.
- Corpus manifest tests pass.

No runtime expansion, question approval, reviewed-bank approval, teacher approval, or student-facing promotion was introduced.
