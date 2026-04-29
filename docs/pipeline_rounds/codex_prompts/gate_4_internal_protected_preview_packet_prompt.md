# Gate 4 Prompt: Internal Protected-Preview Packet

Use this prompt to create internal protected-preview packet artifacts from approved candidate rows only.

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

- Create protected-preview candidate artifacts only from approved controlled draft/planning-gate rows.
- Create an internal protected-preview packet for Yossi/teacher review only.
- Produce a round completion report.

Allowed output:

- Internal protected-preview packet TSV.
- Internal packet Markdown.
- Generation report.
- Excluded-preserved report.
- Round completion report.

Still forbidden:

- Reviewed-bank entries.
- Runtime data.
- Student-facing content.
- Any broader release approval.

Validators/tests to run:

- `$env:PYTHONIOENCODING='utf-8'; python scripts/validate_protected_preview_planning_gate.py`
- `$env:PYTHONIOENCODING='utf-8'; python scripts/validate_protected_preview_candidates.py`
- `$env:PYTHONIOENCODING='utf-8'; python scripts/validate_protected_preview_packet.py`
- `python scripts/validate_pipeline_rounds.py`
- `python scripts/validate_curriculum_extraction.py --check-git-diff`
- Relevant pytest slices for changed validators.

Final report must include:

- Files changed.
- Safety boundaries confirmed.
- Validators/tests run.
- Remaining risks.
- Recommended next task.
