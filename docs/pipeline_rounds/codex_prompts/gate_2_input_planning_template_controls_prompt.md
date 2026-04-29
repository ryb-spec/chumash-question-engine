# Gate 2 Prompt: Input Planning + Template Controls

Use this prompt to select a balanced planning batch and create template-control artifacts. This is still planning/review only.

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

- Select `{BATCH_SIZE}` or `{TARGET_ROW_COUNT}` approved candidates from `{SCOPE_NAME}`.
- Require a batch balance table.
- Apply approved wording, template, answer-key, distractor, context-display, and Hebrew-rendering policies.
- Create row-level review sheets.

Do not generate:

- Student-ready prompts.
- Answer choices.
- Answer keys.
- Protected-preview release content.
- Reviewed-bank data.
- Runtime data.
- Student-facing content.

Validators/tests to run:

- `$env:PYTHONIOENCODING='utf-8'; python scripts/validate_protected_preview_input_planning.py`
- `$env:PYTHONIOENCODING='utf-8'; python scripts/validate_template_skeleton_planning.py`
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
