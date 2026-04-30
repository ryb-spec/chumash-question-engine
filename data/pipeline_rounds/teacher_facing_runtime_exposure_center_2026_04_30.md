# Teacher-Facing Runtime Exposure Center V1 - 2026-04-30

## Purpose

Make Runtime Learning Intelligence V1 visible and useful to the teacher inside the existing Streamlit app without changing question selection, scoring/mastery, active scope, or content.

## What was added

- A read-only runtime exposure summary helper.
- A Streamlit rendering helper for a teacher-facing sidebar expander.
- A collapsed `Runtime Exposure Center` in the app sidebar near the teacher/pilot monitor.
- Governed report, JSON contract, validator, and tests.

## Where it appears in the UI

The exposure center appears in the Streamlit sidebar as a collapsed expander titled `Runtime Exposure Center`, immediately after the existing teacher/pilot monitor call.

## Helper modules created

- `runtime/exposure_summary.py`
- `ui/runtime_exposure_summary.py`

## What data it uses

- `data/attempt_log.jsonl`
- `data/pilot/pilot_session_events.jsonl`
- in-session fallback count when available from `st.session_state.history_weighting_fallback_count`

The helper summarizes local history into counts only.

## What it does not use

- no auth
- no database
- no PII
- no external service
- no new content scope
- no raw JSONL display in the UI

## Missing-log behavior

If local logs are missing, the exposure center shows `No local attempt history found yet.` and does not interrupt the student flow.

## Malformed-log behavior

Malformed JSONL lines are skipped and counted. The UI shows only the skipped/malformed count and never displays raw lines.

## Fallback status

Small-pool fallback is shown as `observed` only when local runtime traces expose fallback counts. Otherwise it remains `unknown_not_determined`.

The prior manual smoke test left fallback behavior unknown, so a focused fallback test is still recommended.

## What remains unproven

Small-pool fallback still needs focused confirmation in a deliberately narrow safe-pool scenario.

## How the teacher should use this

- Check whether repetition control is active.
- Look for overused Hebrew targets.
- Look for repeated pasuk/skill combinations.
- Watch whether one skill or question type dominates recent history.
- Use fallback status as a signal that the safe candidate pool may be narrow.
- Treat this as observability only; it does not change scores.

## Safety confirmation

- Runtime scope expansion: no
- Perek activation: no
- Reviewed-bank promotion: no
- Scoring/mastery change: no
- Question generation change: no
- Question-selection weighting change: no
- Source-truth change: no
- Auth/database/PII: no
- Raw logs exposed: no
