# Curriculum Batch Processing — Fast, Safe, Review-Ready

Use this saved prompt when starting a new curriculum extraction batch in the chumash-question-engine repo.

```text
You are working in the chumash-question-engine repo.

TASK TYPE:
new curriculum extraction batch

Branch required:
feature/curriculum-batch-XXX-[range-short-name]

Mission:
Process the next contiguous curriculum extraction batch in a way that is fast, review-ready, and safe.

The goal is not to make content runtime active.
The goal is to create clean extraction artifacts, preview question artifacts, summary reports, and a manual-review packet that can later be reviewed and moved to reviewed_for_planning_non_runtime.

Before doing any work:

1. Branch discipline
   - Confirm the current branch.
   - If the current branch is not the required branch, stop immediately.
   - Do not edit files on main.
   - Do not create commits.
   - Do not push.
   - Do not create a PR.

2. Current repo state check
   Inspect:
   - data/curriculum_extraction/curriculum_extraction_manifest.json
   - latest relevant batch reports
   - scripts/validate_curriculum_extraction.py
   - scripts/load_curriculum_extraction.py --summary behavior if needed

   Confirm:
   - the previous batch is either reviewed_for_planning_non_runtime / reviewed, or otherwise clearly safe to build after
   - top-level curriculum integration remains not_runtime_active
   - runtime_active remains false
   - no runtime promotion is needed for this task

3. Determine the next batch range
   - Do not guess the next range from memory.
   - Determine the next contiguous unprocessed range from the manifest and existing batch artifacts.
   - If the previous completed range ends at Bereishis 3:24, the next batch should begin at Bereishis 4:1 unless repo evidence says otherwise.
   - Choose a modest, reviewable range. Prefer a clean narrative unit over an oversized batch.
   - State the selected range before generating artifacts.

Hard rules:
- Do not modify runtime scope.
- Do not mark anything runtime active.
- Do not touch streamlit_app.py.
- Do not touch runtime/.
- Do not touch engine/.
- Do not touch scoring/mastery/UI files.
- Do not modify reviewed production question-bank files.
- Do not alter previous batch normalized JSONL or preview JSONL.
- Do not rewrite prior manual-review packets except to link forward if absolutely necessary.
- Do not invent source data.
- Do not create student-facing production content.
- Do not promote active scope.
- Do not start more than one batch.

Expected artifacts for the new batch:

Create/update only the files needed for this batch, following existing repo naming conventions:

1. Raw cleaned source
   - data/curriculum_extraction/raw_sources/batch_XXX/[source_range]_cleaned.md

2. Normalized extraction JSONL
   - data/curriculum_extraction/normalized/batch_XXX_[range]_pasuk_segments.jsonl

3. Preview question JSONL
   - data/curriculum_extraction/generated_questions_preview/batch_XXX_preview.jsonl

4. Batch summary report
   - data/curriculum_extraction/reports/batch_XXX_summary.md

5. Preview summary report
   - data/curriculum_extraction/reports/batch_XXX_preview_summary.md

6. Manual review packet
   - data/curriculum_extraction/reports/batch_XXX_manual_review_packet.md

7. Manifest update
   - data/curriculum_extraction/curriculum_extraction_manifest.json

Artifact quality requirements:

A. Raw source
- Keep source text clean and traceable.
- Preserve pasuk boundaries.
- Preserve Hebrew and translation evidence.
- Do not add interpretive claims into the raw source.

B. Normalized JSONL
- Each record must be traceable to the source.
- Preserve original source translation.
- Do not over-normalize or smooth away source-literal wording.
- Record-level review status should remain needs_review unless repo convention clearly allows otherwise.
- Do not mark extracted content as reviewed.

C. Preview questions
- Generate review-preview questions only.
- Do not treat preview questions as production-reviewed questions.
- Include varied skill coverage where supported by the source.
- Avoid shallow repetition.
- Avoid overusing the same affix pattern.
- Include phrase-sensitive questions where the source supports it.
- Do not ask questions that require unsupported commentary.
- If a phrase needs exact context, highlight or quote the phrase clearly in the question.

D. Manual review packet
The manual review packet is extremely important. It must make human review faster.

For each meaningful sample, include:
- pasuk reference
- Hebrew phrase or word
- original source translation
- generated/normalized translation if applicable
- reviewer note area
- alias/context note area when needed
- concern flag if wording is awkward, ambiguous, overly literal, or easy to mis-teach

The packet must include special watchlist sections for:
- unusual translations
- repeated key roots
- aliases that students may know differently
- phrases where a literal translation is correct but awkward
- words with more than one meaning in context
- places where the question generator may need exact phrase highlighting

Manual review packet final recommendation must initially be one clear selected outcome:
- [ ] APPROVE_BATCH_XXX_FOR_INACTIVE_MERGE
- [x] NEEDS_MANUAL_REVIEW
- [ ] BLOCK_BATCH_XXX

Do not select approval during initial extraction unless a separate human-review pass has actually happened.

E. Manifest
Update the manifest consistently.

For a newly extracted, not-yet-reviewed batch:
- status should reflect extracted / needs review
- review_status should be needs_review
- integration_status should remain not_runtime_active
- runtime_active should remain false
- review_artifacts should list all reports and manual-review packet
- notes should clearly say this batch is extracted for review only and not runtime active

Do not use reviewed_for_planning_non_runtime unless a later review/closeout branch has actually cleared the batch.

Efficiency rules:
- Reuse existing scripts and naming patterns.
- Do not redesign the pipeline.
- Do not broaden validation unless needed for this batch.
- Do not fix unrelated issues.
- If you find a blocker, stop and report it clearly instead of doing speculative work.
- Prefer small, clean, reviewable changes over a large clever refactor.

Validation commands to run:
- git branch --show-current
- git status --short
- python scripts/validate_curriculum_extraction.py
- python scripts/load_curriculum_extraction.py --summary
- python -m pytest tests/test_curriculum_extraction_validation.py tests/test_curriculum_question_preview.py
- git diff --name-only
- git diff --stat
- git status --short

Run full suite only if the touched files or validation changes justify it:
- python -m pytest

Expected final report:

1. Current branch
2. Selected batch range and why it is the next contiguous range
3. Files created
4. Files modified
5. Manifest changes
6. Record counts by type
7. Preview question counts by type/skill if available
8. Watchlist items created for human review
9. Final recommendation in the manual review packet
10. Validation result
11. Loader result
12. Test result
13. Git diff summary
14. Git status
15. Confirmation that no runtime/UI/reviewed-bank/extraction-data-from-prior-batches/release files were touched
16. Clear next recommended branch:
    - if extraction is clean: feature/curriculum-batch-XXX-manual-review
    - if blocked: smallest cleanup branch needed

Stop after producing the batch extraction and review packet.
Do not commit.
Do not push.
Do not create a PR.
Do not start the next batch.
```
