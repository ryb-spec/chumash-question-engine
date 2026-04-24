# Batch 005 Source Gap Request

- Batch: `batch_005_linear_bereishis_4_1_to_4_16`
- Requested branch: `feature/curriculum-batch-005-bereishis-4-start`
- Audit date: `2026-04-24`

## Summary

Batch 005 cannot be extracted safely from the current repo state because the local Hebrew alignment source used by earlier Linear Chumash batches stops at `Bereishis 3:24`.

The local PDF source is present and confirms that `Bereishis 4:1-4:16` is the next contiguous clean narrative unit, but the PDF text layer alone is not sufficient to preserve reliable Hebrew text for a review-ready extraction batch.

## Evidence Checked

- `local_curriculum_sources/7984C_b_01409_pshat_of_torah.pdf`
  - Present.
  - Source pages show the `Bereishis 4:1-4:16` Kayin/Hevel narrative as one coherent unit ending with Kayin leaving from before Hashem.
- `data/curriculum_extraction/curriculum_extraction_manifest.json`
  - Batch 004 is `reviewed_for_planning_non_runtime` / `reviewed`.
  - Top-level `integration_status` remains `not_runtime_active`.
  - `runtime_active` remains `false`.
- `data/pesukim_100.json`
  - Stops at `Bereishis 3:24` (`80` pesukim total).
- `data/parsed_pesukim.json`
  - Also stops at `Bereishis 3:24`.
- PDF text extraction on pages `15-17`
  - English translation lines are recoverable.
  - Hebrew text is noisy/transliterated and not reliable enough on its own for `hebrew_raw` preservation.

## Exact Blocking Issue

Earlier Linear Chumash batches (`batch_002` through `batch_004`) used the local canonical pasuk corpus to align Hebrew phrase text against noisy PDF extraction while preserving source-backed English translation.

For `Bereishis 4:1-4:16`, that local canonical Hebrew alignment source is missing in the current repo/worktree.

Without a local Hebrew source for this range, Batch 005 would require one of the following unsafe behaviors:

- inventing or manually reconstructing Hebrew without a local source-backed alignment reference
- preserving noisy/transliterated PDF output instead of real Hebrew
- silently broadening the extraction method beyond the existing batch convention

None of those are acceptable for a fast, safe, review-ready extraction batch.

## Blocked Outputs

Blocked in the current repo state:

- `data/curriculum_extraction/raw_sources/batch_005/..._cleaned.md`
- `data/curriculum_extraction/normalized/batch_005_..._pasuk_segments.jsonl`
- `data/curriculum_extraction/generated_questions_preview/batch_005_preview.jsonl`
- `data/curriculum_extraction/reports/batch_005_summary.md`
- `data/curriculum_extraction/reports/batch_005_preview_summary.md`
- `data/curriculum_extraction/reports/batch_005_manual_review_packet.md`
- manifest update for Batch 005

Blocked record types:

- `pasuk_segment`
- any preview questions that depend on preserved Hebrew phrase text

## Exact Source Needed

Provide one local, non-runtime Hebrew source for `Bereishis 4:1-4:16`, for example:

- an expanded repo-local canonical pasuk file that includes `Bereishis 4:1-4:16`
- or a local cleaned Hebrew excerpt under `local_curriculum_sources/` covering `Bereishis 4:1-4:16`
- or a repo-approved local source file used only for non-runtime alignment, matching the batch workflow

The needed content is:

- real Hebrew pasuk text for `Bereishis 4:1-4:16`
- sufficient fidelity to align phrase boundaries against the Linear Chumash English translation
- local availability in the worktree or under `local_curriculum_sources/`

## Recommended Next Action

Create a small source-prep branch to add a local Hebrew alignment source for `Bereishis 4:1-4:16` without promoting runtime scope, then rerun Batch 005 extraction on top of that source-backed input.
