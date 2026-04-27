# Source Truth Reproducibility Finalization Report

## Branch

`feature/source-truth-reproducibility-finalization`

## Files Inspected

- `data/source_texts/`
- `data/source_texts/bereishis_hebrew_menukad_taamim.tsv`
- `data/source_texts/source_text_manifest.json`
- `data/corpus_manifest.json`
- `data/source/`
- `data/pesukim_100.json`
- `data/parsed_pesukim.json`
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

The active parsed runtime scope is:

- Scope ID: `local_parsed_bereishis_1_1_to_3_24`
- Parsed corpus ID: `parsed_bereishis_1_1_to_3_24_root`
- Reviewed question bank: `data/active_scope_reviewed_questions.json`
- Reviewed question count declared in manifest: `238`

`data/active_scope_overrides.json`, `data/active_scope_gold_annotations.json`, and `data/active_scope_reviewed_questions.json` all declare `scope_id` as `local_parsed_bereishis_1_1_to_3_24`.

## Manifest Paths Verified

All paths declared in `data/corpus_manifest.json` were checked for repo-local path safety and existence. This includes:

- source files under `data/source/`
- canonical source text under `data/source_texts/`
- active parsed root files under `data/`
- staged provenance files under `data/staged/`
- readiness reports under `data/validation/`
- preview-only and review-only artifact paths under `data/diagnostic_preview/`, `data/standards/`, and `data/curriculum_extraction/`

No missing manifest paths were found.

## SHA/Hash Values Recomputed and Confirmed

Canonical Hebrew source file:

- Path: `data/source_texts/bereishis_hebrew_menukad_taamim.tsv`
- Scope: `Bereishis 1:1-50:26`
- Row count: `1533`
- SHA-256 recomputed from file bytes: `4d96c615ab63e0419bff079db250d71ea9b5de266ff9ab8d589ae80e4afd0b71`

This SHA-256 matches:

- `data/source_texts/source_text_manifest.json`
- `data/corpus_manifest.json`
- `tests/test_source_texts_validation.py`
- strengthened corpus manifest validation in `tests/test_corpus_manifest.py`

## Active Scope Confirmed

The current active runtime scope is `local_parsed_bereishis_1_1_to_3_24`.

This is supported by the committed corpus manifest, active sidecar metadata, active reviewed question bank metadata, and corpus manifest tests. No runtime scope was expanded or promoted in this task.

## Validation Strengthened

`tests/test_corpus_manifest.py` now verifies:

- every manifest path is relative, repo-local, and under an expected data/review location
- every manifest path exists
- every source corpus declares a canonical source text file and SHA-256
- every declared canonical source SHA-256 matches the actual file bytes
- `data/corpus_manifest.json` and `data/source_texts/source_text_manifest.json` agree on canonical source SHA-256
- active scope sidecar metadata matches the manifest active scope

## Tests Run

- `python scripts/validate_source_texts.py`
  - Passed.
- `python -m pytest tests/test_source_texts_validation.py -q`
  - Passed: `15 passed`.
- `python -m pytest tests/test_corpus_manifest.py -q`
  - Passed after validation strengthening: `19 passed`.
- `python -m pytest -q`
  - Failed: `14 failed, 629 passed, 351 subtests passed`.

## Full Pytest Failure Triage

The remaining full-suite failures are not source-text SHA, corpus-manifest path, or active-scope alignment failures.

Observed unrelated failure groups:

- Curriculum extraction validator tests report missing trusted-source extraction accuracy packet links/evidence for batches `batch_002_linear_bereishis`, `batch_003_linear_bereishis_2_4_to_2_25`, `batch_004_linear_bereishis_3_1_to_3_24`, and `batch_005_linear_bereishis_4_1_to_4_16`.
- Diagnostic/curriculum preview validation tests depend on the same curriculum extraction validator state.
- Verified source skill-map tests expect workflow artifacts that are not present in this branch, including `scripts/build_source_to_skill_map.py`, `docs/question_templates/approved_question_template_policy.md`, translation registry `source_preference` metadata, and Metsudah/Koren policy wording.

No failing full-suite test indicated a stale source-text SHA, missing corpus manifest path, invalid canonical source file, or active runtime scope mismatch.

## Remaining Risks or Ambiguities

The committed source-truth path is aligned for source text, manifest paths, manifest hashes, and active scope.

One non-runtime fallback remains visible in `assessment_scope.py`: `_default_corpus_manifest()` contains older fallback source-corpus notes for `source_bereishis_1_1_to_3_16_local`. This fallback is not used while `data/corpus_manifest.json` exists. It was not changed here because modifying `assessment_scope.py` trips existing governance tests that block runtime-file changes in unrelated validation workflows. If the project wants fallback metadata to mirror the committed manifest, that should be handled in a separate runtime-scope metadata cleanup task.

## Final Status

Source truth is aligned for the committed project data:

- Canonical Hebrew source file exists and validates.
- Canonical SHA-256 matches all committed source-text and corpus-manifest references.
- Corpus manifest paths exist and stay inside expected repo locations.
- Active runtime scope is `local_parsed_bereishis_1_1_to_3_24`.
- Source text validation tests pass.
- Corpus manifest tests pass.

No runtime expansion, question approval, teacher approval, or student-facing promotion was introduced.
