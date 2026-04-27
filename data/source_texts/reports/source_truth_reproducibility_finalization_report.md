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

All paths declared in `data/corpus_manifest.json` were checked for repo-local path safety and existence. This includes source files, canonical source text, active parsed root files, staged provenance files, readiness reports, preview-only artifacts, and review-only artifacts.

No missing manifest paths were found when the source-truth finalization was completed.

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

This is supported by the committed corpus manifest, active sidecar metadata, active reviewed question bank metadata, and corpus manifest tests. No runtime scope was expanded or promoted in the source-truth finalization task.

## Validation Strengthened

The source-truth finalization strengthened tests to verify:

- manifest paths are repo-local and exist;
- canonical source text SHA values match actual file bytes;
- `data/corpus_manifest.json` agrees with `data/source_texts/source_text_manifest.json`;
- active scope metadata agrees with the source corpus entry;
- active sidecar metadata remains aligned to the active scope;
- preview-only and review-only artifacts remain distinct from runtime-active data.

## Tests Run At Finalization

- `python scripts/validate_source_texts.py`: passed.
- `python -m pytest tests/test_source_texts_validation.py -q`: passed.
- `python -m pytest tests/test_corpus_manifest.py -q`: passed.
- `python -m pytest -q`: passed at source-truth finalization time.

## Remaining Risks

No known remaining source-truth or reproducibility blockers were recorded at finalization time.
