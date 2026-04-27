# Review Artifact Integrity Full-Suite Fix Report

## Branch

`feature/review-artifact-integrity-full-suite`

## Conflicts Encountered

The stash apply left eight unresolved paths:

- `data/corpus_manifest.json`
- `data/verified_source_skill_maps/README.md`
- `docs/sources/trusted_teacher_source_extraction_review_packet_template.md`
- `docs/sources/trusted_teacher_source_policy.md`
- `scripts/validate_curriculum_extraction.py`
- `scripts/validate_verified_source_skill_maps.py`
- `tests/test_curriculum_extraction_validation.py`
- `tests/test_verified_source_skill_maps.py`

## Conflict-Resolution Choices

- `data/corpus_manifest.json`: resolved with the stash version because it preserved the source-truth-finalized canonical corpus metadata and added review-only source-to-skill artifact metadata without opening runtime or question gates.
- `data/verified_source_skill_maps/README.md`: restored from stash because the verified source-skill-map workflow and validator tests require this documentation and artifact index.
- `docs/sources/trusted_teacher_source_extraction_review_packet_template.md`: restored from stash because trusted-source packet generation tests require the current extraction-accuracy packet template.
- `docs/sources/trusted_teacher_source_policy.md`: restored from stash because trusted-source policy tests and validation rely on the policy/status language.
- `scripts/validate_curriculum_extraction.py`: restored from stash because it contains the stricter trusted-source packet and extraction-evidence validation rules needed by this branch.
- `scripts/validate_verified_source_skill_maps.py`: restored from stash because the source-skill-map validator is required by workflow tests.
- `tests/test_curriculum_extraction_validation.py`: restored from stash because it tests the trusted-source review-artifact evidence rules.
- `tests/test_verified_source_skill_maps.py`: restored from stash because it tests the verified source-skill-map workflow artifacts and safety gates.

No conflict markers remain in the resolved files.

## Artifacts Restored Or Linked

- Restored trusted-source extraction accuracy packet artifacts for batches 002, 003, 004, and 005 under `data/curriculum_extraction/reports/`.
- Restored the Batch 002 and Batch 003 print-friendly Markdown/PDF packets and the combined PDF packet.
- Added `data/source_review_confirmation_items.json` so trusted-source packet generation can distinguish unrelated global confirmation items from batch-specific review items.
- Restored and generated verified source-skill-map artifacts for Bereishis 1:1-1:5, 1:6-1:13, 1:14-1:23, and the first Metsudah seed map.
- Added source-skill-map build, exception-review, audit, and Yossi verification reports under `data/verified_source_skill_maps/reports/`.
- Updated curriculum extraction manifest and source registry metadata so trusted teacher-source packages and batches have explicit extraction-review and closed safety statuses.
- Updated source-text/corpus tests to align with the finalized Bereishis 1:1-3:24 canonical corpus and SHA evidence.
- Restored the Step 1 source-truth finalization report and strengthened source-text/corpus validation tests that had been missing after conflict resolution.
- Added exact git-diff allowlist entries for the restored source-truth report and the isolated Streamlit runtime characterization test-isolation fix.

## Step 1 Source-Truth Preservation Check

The initial post-conflict state was missing some Step 1 source-truth finalization improvements:

- `tests/test_source_texts_validation.py` had 14 tests instead of the finalized 15.
- `tests/test_corpus_manifest.py` had 12 tests instead of the finalized 19.
- `data/source_texts/reports/source_truth_reproducibility_finalization_report.md` was absent.
- `data/source_texts/source_text_manifest.json` still had stale source-text metadata: row count `1534` and no canonical SHA field.

Restored source-truth protections:

- manifest path existence and repo-location checks;
- canonical source SHA checks;
- source-text manifest agreement checks;
- active scope/source corpus agreement checks;
- active sidecar scope checks;
- preview-only/review-only artifact boundary checks.

Current source truth:

- Active scope: `local_parsed_bereishis_1_1_to_3_24`
- Canonical source SHA-256: `4d96c615ab63e0419bff079db250d71ea9b5de266ff9ab8d589ae80e4afd0b71`
- `tests/test_source_texts_validation.py -q`: `15 passed`
- `tests/test_corpus_manifest.py -q`: `19 passed`

The test counts changed back to the Step 1 counts because the missing source-truth validation tests were restored, and the source-text manifest metadata was corrected to match the validator's recomputed source truth.

## Streamlit Order-Dependent Failure

Root cause:

- `runtime.question_flow._cached_candidate_source` is an LRU cache keyed by the identity of `analyze_generator_pasuk` and the pasuk text.
- The failing characterization test patches `analyze_generator_pasuk` and `generate_skill_question`.
- In full-suite order, the candidate-source cache could retain a stale source shape from earlier tests, causing the fake generator to receive an unexpected candidate source and return no usable mastery question.
- The test passed alone because the cache was empty in isolation.

Fix applied:

- `tests/test_streamlit_runtime_characterization.py` now clears `question_flow._cached_candidate_source` in its runtime reset helper.
- This is a test-isolation fix only; runtime question behavior was not changed.

## Safety Gate Confirmation

No question approval, runtime approval, or protected-preview approval was introduced.

The repaired artifacts and metadata keep runtime, question, protected-preview, reviewed-bank, and student-facing gates closed unless a separate existing review path already supports the narrow extraction-review status.

## Validators And Tests Run

- `python scripts/validate_curriculum_extraction.py`: passed.
- `python scripts/validate_verified_source_skill_maps.py`: passed.
- `python scripts/validate_curriculum_extraction.py --check-git-diff`: passed.
- `python scripts/validate_source_texts.py`: passed.
- `python -m pytest tests/test_streamlit_runtime_characterization.py -q`: passed, `6 passed`.
- `python -m pytest tests/test_curriculum_extraction_validation.py -q`: passed, `40 passed, 145 subtests passed`.
- `python -m pytest tests/test_verified_source_skill_maps.py -q`: passed, `23 passed, 213 subtests passed`.
- `python -m pytest tests/test_trusted_source_extraction_packet_generation.py -q`: passed, `14 passed`.
- `python -m pytest tests/test_bereishis_translation_sources.py -q`: passed, `14 passed, 18 subtests passed`.
- `python -m pytest tests/test_source_texts_validation.py -q`: passed, `15 passed`.
- `python -m pytest tests/test_corpus_manifest.py -q`: passed, `19 passed`.
- `python -m pytest tests/test_curriculum_extraction_validation.py tests/test_verified_source_skill_maps.py tests/test_trusted_source_extraction_packet_generation.py -q`: passed, `77 passed, 358 subtests passed`.
- `python -m pytest tests/test_streamlit_runtime_characterization.py::StreamlitRuntimeCharacterizationTests::test_generate_mastery_question_respects_reteach_preferred_pasuk -q`: passed in isolation, `1 passed`.
- `python -m pytest -q`: passed, `628 passed, 416 subtests passed`.

## Final Pytest Result

Full suite result after source-truth restoration, review-artifact repairs, and the Streamlit test-isolation fix: `628 passed, 416 subtests passed`.

## Remaining Risks

- No known remaining review-artifact integrity blockers.
- No known remaining source-truth reproducibility blockers.
- Batch 002 and Batch 003 remain pending Yossi extraction-accuracy review; restored packets improve review evidence but do not mark those batches verified.
