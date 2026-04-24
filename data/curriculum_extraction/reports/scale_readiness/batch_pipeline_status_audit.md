**Status:** Partial readiness  
**Key Finding:** Batches 004 and 005 are aligned to the reviewed non-runtime contract, but Batch 002 and Batch 003 still have approved manual packets without matching manifest closeout.  
**Top Blocker:** Review-state inconsistency between `data/curriculum_extraction/curriculum_extraction_manifest.json` and the Batch 002/003 manual review packets.  
**Recommended Next Action:** Close out Batch 002 and Batch 003 with review-resolution reports and consistent manifest state before treating the pipeline as uniformly scalable.

**Scope**
- Evidence sources:
  - `data/curriculum_extraction/curriculum_extraction_manifest.json`
  - `data/curriculum_extraction/normalized/*.jsonl`
  - `data/curriculum_extraction/generated_questions_preview/*.jsonl`
  - `data/curriculum_extraction/reports/batch_00*_summary.md`
  - `data/curriculum_extraction/reports/batch_00*_manual_review_packet.md`
  - `data/curriculum_extraction/reports/batch_00*_review_resolution.md`

**Batch Table**

| Batch | Range | Status | Review Status | Integration Status | Runtime Active | Artifacts Present | Normalized Record Count | Preview Question Count | Manual Review Status | Ready for Planning | Blocker |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | --- | --- | --- |
| `batch_001_cleaned_seed` | Bereishis 1:1-1:5 plus seed skill packs | `cleaned_seed_reviewed_non_runtime` | `reviewed` | `not_runtime_active` | `false` | raw seed sources, 6 normalized seed files, legacy preview artifacts, summary, manual packet | 75 | 155 in `batch_001_preview.jsonl`, 155 in `batch_001_preview_v2.jsonl` | legacy reviewed packet, no current three-checkbox contract | Yes, as historical seed foundation | Legacy artifact contract predates later review-resolution pattern |
| `batch_002_linear_bereishis` | Bereishis 1:6-2:3 | `extracted_needs_review` | `needs_review` | `not_runtime_active` | `false` | raw source, normalized JSONL, preview JSONL, summary, preview summary, manual packet | 123 | 100 | manual packet shows `APPROVE_BATCH_002_FOR_INACTIVE_MERGE` | No | Manifest still says not reviewed; no review-resolution report |
| `batch_003_linear_bereishis_2_4_to_2_25` | Bereishis 2:4-2:25 | `extracted_needs_review` | `needs_review` | `not_runtime_active` | `false` | raw source, normalized JSONL, preview JSONL, summary, preview summary, manual packet | 90 | 100 | manual packet shows `APPROVE_BATCH_003_FOR_INACTIVE_MERGE` | No | Manifest still says not reviewed; no review-resolution report |
| `batch_004_linear_bereishis_3_1_to_3_24` | Bereishis 3:1-3:24 | `reviewed_for_planning_non_runtime` | `reviewed` | `not_runtime_active` | `false` | raw source, normalized JSONL, preview JSONL, summary, preview summary, manual packet, review resolution | 119 | 100 | approve checked, review resolution present | Yes | No blocking issue found inside batch artifacts |
| `batch_005_linear_bereishis_4_1_to_4_16` | Bereishis 4:1-4:16 | `reviewed_for_planning_non_runtime` | `reviewed` | `not_runtime_active` | `false` | raw source, normalized JSONL, preview JSONL, summary, preview summary, manual packet, review resolution | 64 | 100 | approve checked, review resolution present | Yes | Review-resolution wording says `READY_FOR_BATCH_005_PLANNING`, which is semantically stale now that Batch 005 is the reviewed batch |

**Batch-by-Batch Findings**

| Finding | Evidence Source Path | Affected Batch/File | Risk | Confidence | Recommended Next Action |
| --- | --- | --- | --- | --- | --- |
| Batch 001 is usable as seed infrastructure but still follows a legacy artifact contract with preview files outside the manifest path pattern used later. | `data/curriculum_extraction/curriculum_extraction_manifest.json`, `data/curriculum_extraction/generated_questions_preview/batch_001_preview.jsonl`, `data/curriculum_extraction/generated_questions_preview/batch_001_preview_v2.jsonl` | Batch 001 | Low | High | Keep as legacy seed baseline; do not use it as the template for new batch lifecycle rules. |
| Batch 002 has evidence of human approval in the manual review packet but no matching reviewed manifest state or review-resolution artifact. | `data/curriculum_extraction/reports/batch_002_manual_review_packet.md`, `data/curriculum_extraction/curriculum_extraction_manifest.json` | Batch 002 | Medium | High | Add a small review-contract closeout branch for Batch 002. |
| Batch 003 has the same approval-vs-manifest mismatch as Batch 002. | `data/curriculum_extraction/reports/batch_003_manual_review_packet.md`, `data/curriculum_extraction/curriculum_extraction_manifest.json` | Batch 003 | Medium | High | Close out Batch 003 with the same reviewed non-runtime contract used in Batch 004 and Batch 005. |
| Batch 004 is the first batch fully aligned to the reviewed-for-planning non-runtime contract. | `data/curriculum_extraction/reports/batch_004_review_resolution.md`, `data/curriculum_extraction/curriculum_extraction_manifest.json` | Batch 004 | Low | High | Treat Batch 004 as the current contract baseline for future manual-review closeout branches. |
| Batch 005 is also aligned to the reviewed non-runtime contract, but its resolution wording still references Batch 005 planning instead of the next step. | `data/curriculum_extraction/reports/batch_005_review_resolution.md` | Batch 005 | Low | Medium | Fix wording only when a future report-only cleanup branch is already touching Batch 005 review artifacts. |
| Top-level curriculum integration remains intentionally inactive. | `data/curriculum_extraction/curriculum_extraction_manifest.json` | Curriculum extraction system | Low | High | Preserve this boundary until source-text, alias, and generator variety work are in place. |

**Cross-Batch Observations**
- The repo has contiguous extracted coverage from Bereishis 1:1 through 4:16.
- Only Batch 004 and Batch 005 currently satisfy the newer `reviewed_for_planning_non_runtime` / `reviewed` contract.
- Batch 002 and Batch 003 are the main lifecycle inconsistency preventing the batch pipeline from feeling uniform and scalable.
- None of the audited curriculum batches are runtime active, and nothing in the manifest suggests that runtime promotion is pending.

**Ready / Not Ready Judgment**
- Not fully ready for uniform scale operations yet.
- The extraction pipeline itself works, but the review-state contract is still inconsistent across Batches 001-005.

**Next Branch Recommendation**
- `feature/curriculum-batch-002-and-003-review-contract-closeout`
