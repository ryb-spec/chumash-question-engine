# Gate 1 Prompt: Source + Enrichment + Eligibility Readiness

Use this prompt to prepare source, enrichment, and eligibility readiness for a future Round 2 scope. This is not content generation.

Parameters:

- Scope: `{SCOPE_NAME}`
- Start ref: `{START_REF}`
- End ref: `{END_REF}`
- Source map file: `{SOURCE_MAP_FILE}`
- Target row count: `{TARGET_ROW_COUNT}`
- Batch size: `{BATCH_SIZE}`

Hard boundaries:

- Do not commit.
- Do not push.
- Do not create reviewed-bank entries.
- Do not promote runtime.
- Do not create student-facing content.
- Do not modify the live app or runtime data.
- Keep reviewed-bank, runtime, and student-facing gates closed.

Mission:

- Confirm verified source-to-skill coverage for `{SCOPE_NAME}` from `{START_REF}` to `{END_REF}`.
- Confirm enrichment candidates exist and review-applied reports are present.
- Run or update the question-eligibility audit only if the scope is ready.
- Produce review artifacts, not questions.

Do not generate:

- Questions.
- Answer choices.
- Answer keys.
- Protected-preview release content.
- Reviewed-bank data.
- Runtime data.
- Student-facing content.

Validators/tests to run:

- `python scripts/validate_verified_source_skill_maps.py`
- `python scripts/validate_source_texts.py`
- `$env:PYTHONIOENCODING='utf-8'; python scripts/validate_source_skill_enrichment.py`
- `$env:PYTHONIOENCODING='utf-8'; python scripts/validate_question_eligibility_audit.py`
- `python scripts/validate_curriculum_extraction.py --check-git-diff`
- Relevant pytest slices for changed validators.

Final report must include:

- Files changed.
- Safety boundaries confirmed.
- Validators/tests run.
- Remaining risks.
- Recommended next task.
