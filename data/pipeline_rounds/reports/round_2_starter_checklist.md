# Round 2 Starter Checklist

This checklist prepares the next perek or slice for the fast-track pipeline. It is planning-only and does not create questions, answer choices, answer keys, protected-preview release content, reviewed-bank entries, runtime data, or student-facing content.

## Branch and worktree

- Run `git branch --show-current`.
- Run `git status --short`.
- Run `git diff --stat`.
- Stop if unrelated uncommitted changes are present.

## Source-to-skill coverage

- Confirm `{SOURCE_MAP_FILE}` exists for `{SCOPE_NAME}`.
- Confirm coverage from `{START_REF}` to `{END_REF}`.
- Run `python scripts/validate_verified_source_skill_maps.py`.
- Run `python scripts/validate_source_texts.py`.

## Enrichment readiness

- Confirm morphology, standards, vocabulary, and shoresh candidate files exist where needed.
- Confirm enrichment review-applied reports exist.
- Keep unresolved enrichment rows out of input planning.
- Run `$env:PYTHONIOENCODING='utf-8'; python scripts/validate_source_skill_enrichment.py`.

## Allowed family check

- Allow `vocabulary_meaning`.
- Allow `basic_noun_recognition`.
- Allow `direct_object_marker_recognition` only with function wording review.
- Allow clean `shoresh_identification` only with reviewed root evidence.
- Keep `basic_verb_form_recognition` deferred.

## Batch size rule

- Default batch size is 20-30 rows.
- Use `{BATCH_SIZE}` or `{TARGET_ROW_COUNT}` when the task specifies a tighter target.
- Exclude high-risk, source-only, follow-up, blocked, and verb-form rows.

## Balance table rule

Every input planning batch must report:

- Total selected candidates.
- Count by family.
- Count by risk level.
- Count by perek/pasuk or ref range.
- Duplicate Hebrew tokens, if any.
- Reason each direct-object-marker row was included.
- Reason each shoresh row was included.

## Validator list

- `python scripts/validate_pipeline_rounds.py`
- `$env:PYTHONIOENCODING='utf-8'; python scripts/validate_question_eligibility_audit.py`
- `$env:PYTHONIOENCODING='utf-8'; python scripts/validate_protected_preview_input_planning.py`
- `$env:PYTHONIOENCODING='utf-8'; python scripts/validate_template_skeleton_planning.py`
- `$env:PYTHONIOENCODING='utf-8'; python scripts/validate_pre_generation_review.py`
- `$env:PYTHONIOENCODING='utf-8'; python scripts/validate_controlled_draft_generation.py`
- `$env:PYTHONIOENCODING='utf-8'; python scripts/validate_protected_preview_candidates.py`
- `$env:PYTHONIOENCODING='utf-8'; python scripts/validate_protected_preview_packet.py`
- `python scripts/validate_curriculum_extraction.py --check-git-diff`

## Review artifact list

- Source-to-skill review packet or verification report.
- Enrichment review sheets and applied reports.
- Eligibility review sheet and applied report.
- Input planning TSV and batch balance report.
- Row-level pre-generation review sheet.
- Controlled draft teacher review packet.
- Internal protected-preview packet and completion report.

## Stop conditions

Stop if source-to-skill rows are unverified, enrichment evidence is unresolved, verb-form rows appear without policy, high-risk rows are selected, Hebrew corruption appears, balance table is missing, or protected-preview release, reviewed-bank, runtime, or student-facing gates open accidentally.
