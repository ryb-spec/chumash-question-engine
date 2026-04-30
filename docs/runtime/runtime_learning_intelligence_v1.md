# Runtime Learning Intelligence V1

## Purpose

Runtime Learning Intelligence V1 makes the quiz runtime less repetitive across sessions without expanding content.

It reads local attempt history, builds stable question/target signatures, and downweights candidates that have already appeared often when safe alternatives exist.

## How repetition control works

The runtime builds signatures for:

- exact question
- Hebrew target
- pasuk plus skill
- skill plus question type

When candidate questions are ranked, the runtime subtracts a freshness penalty for repeated exposure:

- exact repeat: strongest penalty
- Hebrew target repeat: strong penalty
- pasuk plus skill repeat: moderate penalty
- skill plus question type repeat: mild penalty

## What it reads

- `data/attempt_log.jsonl`
- `data/pilot/pilot_session_events.jsonl`
- current Streamlit session-state recent-question signatures

Missing history files are safe. Malformed JSONL lines are skipped and counted.

## What it does not read

- no external services
- no auth
- no cloud database
- no database
- no account system
- no student roster
- no PII

## Fallback behavior

The runtime does not permanently suppress candidates. If the current safe scope is too small, or every candidate is already exposed, the best available safe candidate is still served. This keeps the app usable while making the fallback visible.

## Teacher-Facing Runtime Exposure Center

Runtime Learning Intelligence V1 now appears in the Streamlit sidebar as a collapsed `Runtime Exposure Center` near the teacher/pilot monitor.

It shows:

- whether repetition control is active
- whether Runtime Learning Intelligence is enabled
- recent attempts counted
- attempt-log and pilot-event log presence
- malformed/skipped log-line count
- last observed attempt timestamp when available
- most repeated Hebrew targets
- most repeated pasuk plus skill combinations
- most repeated skills and question types
- small-pool fallback status and fallback count when local traces expose it

Repeated targets are counted from normalized local attempt-history records. Pasuk/skill repeats are summarized by pairing each available `pasuk_ref` with its `skill`. Question-type and skill counts are summarized separately so a teacher can see when one lane is dominating the run.

The center uses local logs only:

- no login
- no database
- no PII
- no raw JSONL lines exposed in the UI

If logs are missing, the center shows `No local attempt history found yet.` and does not interrupt the student flow. If logs contain malformed lines, those lines are skipped and counted without exposing raw log content.

Teacher interpretation guidance:

- If one word or pasuk-skill pair appears many times, the app may be working with a narrow safe pool.
- Repetition control downweights overused items but will still serve questions when the pool is small.
- This is a teacher visibility tool; it does not change scores.

Limitation: small-pool fallback still needs focused confirmation because the manual smoke test left that field unknown / not determined.

## Teacher expectations

V1 provides a teacher-facing exposure summary through:

- `data/validation/runtime_learning_intelligence_report.md`
- `data/validation/runtime_learning_intelligence_summary.json`

The app also provides direct sidebar visibility through the `Runtime Exposure Center`.

The report shows:

- whether repetition control is active
- recent attempts counted
- most repeated Hebrew targets
- repeated skill/question type combinations
- small-scope fallback count
- warning when the available target pool looks small

## Debugging toggle

Set this environment variable to disable history weighting temporarily:

```powershell
$env:CHUMASH_DISABLE_HISTORY_WEIGHTING = "1"
```

Default behavior is enabled.

## Privacy and PII note

This V1 layer uses only local runtime artifacts. It does not add authentication, a database, a class roster, network services, or student PII.

## Limitations

- It is not a full student account system.
- It relies on the quality of available local log fields.
- It reduces repetition by weighting rather than guaranteeing no repeats.
- Small scopes can still repeat when no safer alternative exists.

## Next possible improvements

- Add a richer teacher export for stale/underused targets.
- Add per-mode exposure thresholds.
- Add a future account-safe identity layer only if a later product task explicitly authorizes it.

## Small-Pool Fallback Manual Test - 2026-04-30

Yossi ran a focused small-pool fallback manual test in Full Passuk view.

Recorded evidence:

- fallback confirmed
- app kept serving questions when the safe pool was small
- no crash or blank screen
- Runtime Exposure Center showed fallback/scope-small status
- repeated targets were still reduced where possible
- no weird skips or missing questions
- no slowdown
- no confusing behavior
- approximate question count was not recorded

This is manual fallback test evidence, not controlled student pilot evidence. No missing question count was invented.

## Product Readiness Status - 2026-04-30

Runtime Learning Intelligence V1 is ready for continued pilot use and should remain enabled.

This readiness status does not authorize runtime scope expansion, reviewed-bank promotion, student-facing public rollout, student login/database, scoring/mastery changes, source-truth changes, or Perek activation.

Safety status remains:

- no auth/database/PII
- no scoring/mastery change
- no scope expansion
- no source-truth change
- no reviewed-bank promotion

## Recommended Next Product Step

The recommended next product task is Teacher Lesson / Session Setup V1.

That task should let the teacher label or select today's local session context while preserving the existing safety boundaries: no auth, no database, no PII, no new content, no scoring/mastery change, and no active runtime scope expansion.

## Teacher Lesson / Session Setup V1 - 2026-04-30

Teacher Lesson / Session Setup V1 adds a local sidebar setup panel so a teacher can label the current lesson/session before or during practice.

It captures local session context only:

- lesson/session label
- mode focus
- optional class period or group label
- optional teacher notes

The Runtime Exposure Center shows this session context above the exposure summaries, so repeated targets, repeated pasuk/skill pairs, and fallback/scope-small status can be interpreted against the current classroom purpose.

Safety boundaries remain unchanged:

- no auth
- no database
- no PII
- no raw log exposure
- no new content
- no question generation change
- no question-selection change
- no scoring/mastery change
- no active runtime scope expansion

## Teacher Runtime Exposure Export / Report

Teacher Runtime Evidence Export Suite V1 saves the Runtime Exposure Center summary for local teacher review after a class or pilot session.

The export includes lesson/session setup metadata, repeated target summaries, pasuk/skill concentration, fallback/scope-small status, cautious teacher interpretation, and safety/privacy notes.

It does not change Runtime Learning Intelligence behavior, question-selection weighting, scoring/mastery, question generation, active scope, reviewed-bank status, or source truth. It exposes no raw JSONL logs and adds no login, database, or PII.

## Teacher Runtime Export / Report Session Accuracy

Teacher Runtime Exposure Export now includes export-scope metadata so a report does not misleadingly look like a current-session report when it is using broader local history. The export can be current-session bounded when a pilot/session id is available, can fall back to the teacher setup `saved_at` window, and otherwise labels Recent local history as diagnostic.

The export uses `Planned lesson focus` as a teacher/report label only; it does not change the student question mode. Markdown and JSON are generated from one export snapshot so repeated-target counts, fallback count, generated timestamp, warnings, and scope metadata match.

No raw logs are exposed. No login, No database, and No PII are used. No scoring/mastery change, No runtime scope expansion, No question-selection change, No question-generation change, and No reviewed-bank promotion are authorized by this report.
