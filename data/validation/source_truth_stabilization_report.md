# Source Truth Stabilization Report

## Purpose

This report documents the source-truth stabilization pass for the current runtime corpus. It records the active corpus, source files, reviewed runtime bank, preview-only artifacts, review-only artifacts, and the reason the canonical source-text SHA expectation was updated.

## Current Active Truth

- Active runtime scope: `local_parsed_bereishis_1_1_to_3_24`
- Active runtime range: Bereishis 1:1-3:24
- Active runtime pasuk count: `80`
- Source corpus ID: `source_bereishis_1_1_to_3_24_local`
- Parsed corpus ID: `parsed_bereishis_1_1_to_3_24_root`
- Canonical Hebrew source text: `data/source_texts/bereishis_hebrew_menukad_taamim.tsv`
- Canonical Hebrew source text scope: Bereishis 1:1-50:26
- Canonical Hebrew source text row count: `1533`
- Canonical Hebrew source text SHA-256: `4d96c615ab63e0419bff079db250d71ea9b5de266ff9ab8d589ae80e4afd0b71`
- Active reviewed runtime question bank: `data/active_scope_reviewed_questions.json`
- Active reviewed runtime question count: `238`

## Active Source Files

- `data/source/bereishis_1_1_to_1_30.json`
- `data/source/bereishis_1_31_to_2_9.json`
- `data/source/bereishis_2_10_to_2_17.json`
- `data/source/bereishis_2_18_to_2_25.json`
- `data/source/bereishis_3_1_to_3_8.json`
- `data/source/bereishis_3_9_to_3_16.json`
- `data/source/bereishis_3_17_to_3_24.json`

## Preview-Only Artifacts

- `data/diagnostic_preview/`
- `data/standards/zekelman/preview/standard_3_mvp_protected_preview_packet.md`

These artifacts remain non-runtime and do not define the active runtime scope.

## Review-Only Artifacts

- `data/curriculum_extraction/`
- `data/standards/zekelman/blueprints/`
- `data/standards/zekelman/reports/`
- `data/standards/zekelman/reviewed_bank_candidates/`

These artifacts remain review/planning material unless separately promoted and activated.

## Problems Corrected

- `data/corpus_manifest.json` had a source corpus through Bereishis 3:16 while the active runtime scope pointed to Bereishis 1:1-3:24. The manifest now defines the source corpus as Bereishis 1:1-3:24 and includes the 3:17-3:24 source file.
- `data/source_texts/source_text_manifest.json` counted the TSV header row and did not store the canonical SHA. The manifest now records `1533` data rows and the validated SHA-256.
- `data/source_texts/reports/bereishis_hebrew_menukad_taamim_validation.md` reported a stale SHA. The report now matches the validator output for the canonical TSV.
- `tests/test_source_texts_validation.py` expected the stale SHA. The test now expects the verified canonical SHA and checks the source-text manifest against validator output.
- `tests/test_corpus_manifest.py` did not fail if the active scope referenced a missing or mismatched source corpus. It now verifies source corpus, active scope, reviewed bank, and preview/review-only boundaries.
- `data/validation/question_validation_audit.md` and `.json` reflected an older active scope. They are now marked as historical reports, not current active truth.

## SHA Update Rationale

The canonical TSV was validated directly with `scripts/validate_source_texts.py`. The validator reported a valid complete Bereishis 1:1-50:26 file with `1533` data rows and SHA-256 `4d96c615ab63e0419bff079db250d71ea9b5de266ff9ab8d589ae80e4afd0b71`. The old expected SHA was stale relative to the checked canonical file, so the test and source-text report were updated to match the verified file rather than blindly replacing a hash.

## Runtime Behavior

No question-generation behavior, student-facing runtime behavior, reviewed content, Hebrew text, translations, active-scope reviewed questions, or runtime app routing was changed.

## Remaining Risk

`assessment_scope.py` contains an embedded fallback manifest used only if `data/corpus_manifest.json` cannot be loaded. That fallback was not changed in this stabilization pass in order to avoid changing runtime fallback behavior. The supported source truth is the committed `data/corpus_manifest.json` plus the source-text manifest and validators.
