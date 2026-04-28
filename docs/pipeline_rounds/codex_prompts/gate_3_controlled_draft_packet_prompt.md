# Gate 3 Prompt: Controlled Draft Packet

Use this prompt to create a controlled teacher-review draft packet from row-approved inputs only.

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

- Generate controlled teacher-review draft items only from rows explicitly approved for controlled draft generation.
- Preserve skipped, revision-required, and source-only rows as excluded.
- Apply Yossi draft decisions when provided.

Allowed output:

- Teacher-review-only controlled drafts.
- Teacher review packet.
- Generation and skipped-row reports.

Still forbidden:

- Protected-preview release content.
- Reviewed-bank entries.
- Runtime data.
- Student-facing content.

Validators/tests to run:

- `$env:PYTHONIOENCODING='utf-8'; python scripts/validate_controlled_draft_generation.py`
- `$env:PYTHONIOENCODING='utf-8'; python scripts/validate_pre_generation_review.py`
- `python scripts/validate_pipeline_rounds.py`
- `python scripts/validate_curriculum_extraction.py --check-git-diff`
- Relevant pytest slices for changed validators.

Final report must include:

- Files changed.
- Safety boundaries confirmed.
- Validators/tests run.
- Remaining risks.
- Recommended next task.
