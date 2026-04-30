# Runtime Learning Intelligence V1 Audit

## Purpose

This audit records the runtime-learning-intelligence change for cross-session scope exhaustion, attempt-history weighting, and teacher exposure visibility.

## Files inspected

- `streamlit_app.py`
- `runtime/question_flow.py`
- `runtime/mode_handlers.py`
- `runtime/presentation.py`
- `runtime/session_state.py`
- `runtime/pilot_logging.py`
- `ui/render_question.py`
- `ui/question_support.py`
- `question_ui.py`
- `assessment_scope.py`
- `engine/flow_builder.py`
- `progress_store.py`
- `skill_tracker.py`
- `data/attempt_log.jsonl`
- `data/pilot/pilot_session_events.jsonl`
- `data/active_scope_reviewed_questions.json`
- `data/active_scope_gold_annotations.json`
- `data/validation/runtime_review_exposure_index.json`
- `data/validation/runtime_review_exposure_index.md`
- `data/validation/question_quality_risk_summary.md`
- `data/validation/curriculum_quality_check_summary.md`

## Current attempt-log and session-log behavior

The app already writes local attempt rows to `data/attempt_log.jsonl` through `append_attempt_log`. Pilot served and answered events are also written to `data/pilot/pilot_session_events.jsonl` through `runtime.pilot_logging`.

Both sources are local JSONL artifacts. Neither requires authentication, accounts, cloud services, a database, or student PII.

## Where question selection currently happens

Question selection is centered in `runtime/question_flow.py`.

- `get_skill_ready_pasuks` creates lightweight ready rows.
- `rank_ready_rows` ranks ready rows before full question materialization.
- `select_pasuk_first_question` materializes and validates candidates.
- `choose_weighted_pasuk_question` chooses among validated candidates.
- `remember_recent_question` records same-session signatures.

## Current repetition control

The runtime already blocks or avoids many same-session repeats:

- recent exact repeat checks
- recent target repeat checks
- same pasuk/intent repeat checks
- semantic sibling and translation-meaning repeat checks
- tense-lane overlap checks
- feature, prefix, morpheme-family, and short-run instructional-family caps

The missing product layer was cross-session exposure weighting from prior local attempts and pilot logs.

## Cross-session exposure data available

Available local fields include timestamp, session ID, practice mode, question ID when present, pasuk reference, selected Hebrew target, skill, question type, question text when present, and correctness when present.

## Gaps found

- Same-session repetition controls were stronger than cross-session controls.
- Teacher/pilot monitor exposed session mix and flags but not recent target overuse.
- The app had fallback behavior, but cross-session fallback reasons were not surfaced.

## Implementation strategy

- Add a tolerant attempt-history reader.
- Add stable identity signatures for question, target, pasuk+skill, and skill+question type.
- Build exposure counters from local attempt and pilot logs.
- Apply a scoring penalty in `rank_ready_rows` and `choose_weighted_pasuk_question`.
- Keep candidates available when scope is small.
- Surface teacher-visible exposure information through governed validation/report artifacts for V1.
- Leave direct `streamlit_app.py` sidebar integration for a later task because that path remains intentionally forbidden by the curriculum diff guard unless a UI-specific task opens it.

## Risks

- Very small scopes may still repeat. V1 keeps fallback explicit rather than blocking all questions.
- Existing historical logs may bias selection until fresher attempts diversify the pool.
- Identity matching is conservative and depends on available question metadata.

## What was intentionally not built

- no auth
- no database
- no PII
- no scope expansion
- no scoring/mastery change
- no new content
- no new reviewed-bank promotion
