# Add Batch 003 Linear Chumash Bereishis 2 extraction

## What changed

This PR adds Batch 003 curriculum extraction artifacts for `Bereishis 2:4` through `Bereishis 2:25` under the inactive curriculum extraction factory.

Included in this batch:
- cleaned source excerpt for the relevant Linear Chumash source range
- normalized Batch 003 `pasuk_segment` records
- Batch 003 preview questions for supported translation lanes
- Batch 003 summary, preview summary, and manual review packet
- merge-readiness documentation for inactive infrastructure review

## What did not change

This PR does not:
- modify `streamlit_app.py`
- modify anything under `runtime/`
- modify anything under `engine/`
- modify `assessment_scope.py`
- modify `data/corpus_manifest.json`
- modify reviewed question bank files
- modify UI, scoring, or mastery behavior
- connect Batch 003 to runtime
- promote any corpus slice

Preview questions are not live, and loader behavior remains isolated from preview files.

## Validation/testing

Validation and tests run cleanly:
- `python scripts/validate_curriculum_extraction.py`
- `python scripts/load_curriculum_extraction.py --summary`
- `python -m pytest`

Current results:
- validator: PASS
- loader summary: PASS
- full pytest: `475 passed`

## Manual review

Batch 003 manual review is documented in:
- `data/curriculum_extraction/reports/batch_003_manual_review_packet.md`

Final reviewer state:
- `[x] APPROVE_BATCH_003_FOR_INACTIVE_MERGE`
- `[ ] NEEDS_MINOR_CLEANUP`
- `[ ] BLOCK_BATCH_003`

## Why this is safe to merge

- The batch remains fully inactive infrastructure.
- Runtime remains untouched.
- Reviewed question bank remains untouched.
- Corpus scope remains unchanged.
- Preview generation is isolated to non-runtime artifacts.
- Loader continues to ignore preview files safely.

## What remains blocked / deferred

- `translation_rule_recognition` remains deferred for this batch because no standalone source-backed `translation_rule` records were extracted in this range.
- Answer-key-dependent lanes such as `mi_amar_el_mi`, `al_mi_neemar`, and `word_parse_task` answer checking are not part of this batch.
- Translation alias cleanup was intentionally deferred to a future cleanup batch.

## Next recommended batch

Continue the inactive Linear Chumash extraction pipeline with the next adjacent source-backed Bereishis block in a separate branch, rather than expanding runtime scope from this branch.
