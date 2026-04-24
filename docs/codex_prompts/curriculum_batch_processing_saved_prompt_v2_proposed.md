# Curriculum Batch Processing — Fast, Safe, Review-Ready (V2 Proposed)

Use this proposed prompt when starting a new curriculum extraction batch in the `chumash-question-engine` repo after the Batch 001-005 lessons learned.

```text
You are working in the chumash-question-engine repo.

TASK TYPE:
new curriculum extraction batch

Branch required:
feature/curriculum-batch-XXX-[range-short-name]

Mission:
Process exactly one new contiguous curriculum extraction batch in a way that is fast, review-ready, safe, and explicitly non-runtime.

The goal is not to make content runtime active.
The goal is to create source-backed extraction artifacts, preview question artifacts, summary reports, and a manual-review packet that can later move through review-state cleanup into reviewed_for_planning_non_runtime.

Unattended execution rule:
- Do not pause for approval or confirmation.
- If one subtask is blocked, document the blocker, stop that subtask, and continue with the next safe workstream.
- Only stop the whole task if the branch is wrong, the worktree is dirty in forbidden paths, required source material is missing, or continuing would require touching forbidden files or inventing source data.

Before doing any work:

1. Branch discipline
   - Run `git branch --show-current`.
   - If the current branch is not the required branch, stop immediately.
   - Do not edit files on `main`.
   - Do not create commits.
   - Do not push.
   - Do not create a PR.

2. Worktree check
   - Run `git status --short`.
   - If there are unexpected dirty files outside explicitly allowed report/docs paths, stop.
   - If only generated local noise files are dirty and repo rules allow restoring them, restore them before continuing.

3. Current repo state check
   Inspect:
   - `data/curriculum_extraction/curriculum_extraction_manifest.json`
   - latest relevant batch reports
   - `scripts/validate_curriculum_extraction.py`
   - `scripts/load_curriculum_extraction.py`
   - `docs/codex_prompts/curriculum_batch_processing_saved_prompt.md` if present
   - canonical source-text files under `data/source_texts/` if present
   - local block source files under `data/source/` if needed

   Confirm:
   - the previous batch is either `reviewed_for_planning_non_runtime / reviewed`, or there is explicit repo evidence that it is still safe to build after
   - top-level curriculum integration remains `not_runtime_active`
   - `runtime_active` remains `false`
   - no runtime promotion is needed for this task

4. Determine the next batch range
   - Do not guess the next range from memory.
   - Determine the next contiguous unprocessed range from the manifest and existing batch artifacts.
   - Prefer the smallest clean narrative unit over an oversized batch.
   - State the selected range before generating artifacts.

5. Source gate
   - Prefer canonical Hebrew source files under `data/source_texts/` when the needed pesukim are present there.
   - If canonical Hebrew is not yet available, use an approved local source-prep artifact only if the repo already contains it.
   - Do not OCR, reconstruct, or guess Hebrew.
   - If the Hebrew source is missing, create only a source-gap report and stop the extraction workstream.

Hard rules:
- Do not modify runtime scope.
- Do not mark anything runtime active.
- Do not promote active scope.
- Do not touch `streamlit_app.py`.
- Do not touch `runtime/`.
- Do not touch `engine/`.
- Do not touch scoring/mastery/UI files.
- Do not modify reviewed production question-bank files.
- Do not alter previous batch normalized JSONL or preview JSONL.
- Do not rewrite prior manual-review packets except to link forward if a later review-state branch explicitly requires it.
- Do not invent source data.
- Do not create student-facing production content.
- Do not start more than one batch.

Expected artifacts for the new batch:

1. Raw cleaned source
   - `data/curriculum_extraction/raw_sources/batch_XXX/[source_range]_cleaned.md`

2. Normalized extraction JSONL
   - `data/curriculum_extraction/normalized/batch_XXX_[range]_pasuk_segments.jsonl`

3. Preview question JSONL
   - `data/curriculum_extraction/generated_questions_preview/batch_XXX_preview.jsonl`

4. Batch summary report
   - `data/curriculum_extraction/reports/batch_XXX_summary.md`

5. Preview summary report
   - `data/curriculum_extraction/reports/batch_XXX_preview_summary.md`

6. Manual review packet
   - `data/curriculum_extraction/reports/batch_XXX_manual_review_packet.md`

7. Manifest update
   - `data/curriculum_extraction/curriculum_extraction_manifest.json`

Artifact quality requirements:

A. Raw source
- Keep source text clean and traceable.
- Preserve pasuk boundaries.
- Preserve Hebrew and translation evidence.
- Use canonical Hebrew source when available.
- Do not add interpretive claims into the raw source.

B. Normalized JSONL
- Each record must be traceable to the source.
- Preserve original source translation.
- Do not over-normalize or smooth away source-literal wording.
- Record-level review status should remain `needs_review` unless repo convention clearly allows otherwise.
- Do not mark extracted content as reviewed.
- Keep uncertainty review-safe rather than pretending certainty.

C. Preview questions
- Generate review-preview questions only.
- Do not treat preview questions as production-reviewed questions.
- Include varied skill coverage only where the repo already has support structure.
- Avoid shallow repetition.
- Avoid reusing the same source phrase across every lane by default.
- Avoid overusing the same affix or translation pattern.
- Include phrase-sensitive prompts when the phrase itself matters.
- Do not ask questions that require unsupported commentary.
- If a phrase needs exact context, quote or highlight the Hebrew phrase clearly in the prompt.
- Be careful with apostrophes, contractions, and source-literal English phrasing in prompt rendering.

D. Manual review packet
The manual review packet is one of the most important artifacts. It must make human review faster.

Include:
- batch range
- source files inspected
- record counts
- preview question counts
- watchlist summary
- sample review table

For each meaningful sample include:
- pasuk reference
- Hebrew phrase or word
- original source translation
- generated or normalized translation if applicable
- question type or skill target if applicable
- concern flag
- reviewer note area
- alias/context note area

The packet must include special watchlist sections for:
- unusual translations
- repeated key roots
- aliases that students may know differently
- phrases where a literal translation is correct but awkward
- words with more than one meaning in context
- names and places needing alias handling
- places where the question generator may need exact phrase highlighting

Manual review packet final recommendation must initially be exactly one selected outcome:
- [ ] APPROVE_BATCH_XXX_FOR_INACTIVE_MERGE
- [x] NEEDS_MANUAL_REVIEW
- [ ] BLOCK_BATCH_XXX

Do not select approval during initial extraction unless a separate human-review pass has actually happened.

E. Manifest
Update the manifest consistently.

For a newly extracted, not-yet-reviewed batch:
- `status` should reflect extracted / needs review
- `review_status` should be `needs_review`
- `integration_status` should remain `not_runtime_active`
- `runtime_active` should remain `false`
- `review_artifacts` should list summary, preview summary, and manual review packet
- `notes` should clearly say the batch is extracted for review only and not runtime active

Do not use `reviewed_for_planning_non_runtime` unless a later review/closeout branch has actually cleared the batch.

Efficiency rules:
- Reuse existing scripts and naming patterns.
- Do not redesign the pipeline during extraction branches.
- Do not broaden validation unless the new batch or new report/doc paths require a narrow update.
- Do not fix unrelated issues.
- If a blocker appears, stop that workstream and document it clearly instead of doing speculative work.
- Prefer small, clean, reviewable changes over a large clever refactor.

Validation commands to run:
- `git branch --show-current`
- `git status --short`
- `python scripts/validate_curriculum_extraction.py`
- `python scripts/load_curriculum_extraction.py --summary`
- `python -m pytest tests/test_curriculum_extraction_validation.py tests/test_curriculum_question_preview.py`
- `git diff --name-only`
- `git diff --stat`
- `git status --short`

Run full suite only if touched files or validation changes justify it:
- `python -m pytest`

Expected final report:

1. Current branch
2. Selected batch range and why it is the next contiguous range
3. Files created
4. Files modified
5. Manifest changes
6. Record counts by type
7. Preview question counts by type and skill if available
8. Watchlist items created for human review
9. Final recommendation in the manual review packet
10. Validation result
11. Loader result
12. Test result
13. Git diff summary
14. Git status
15. Confirmation that no runtime/UI/reviewed-bank/extraction-data-from-prior-batches/release files were touched
16. Clear next recommended branch:
    - if extraction is clean: `feature/curriculum-batch-XXX-manual-review`
    - if blocked: the smallest cleanup or source-prep branch needed

Stop after producing the batch extraction and review packet.
Do not commit.
Do not push.
Do not create a PR.
Do not start the next batch.
```
