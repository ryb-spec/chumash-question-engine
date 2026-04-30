# Teacher Lesson / Session Setup V1

## Purpose

Teacher Lesson / Session Setup V1 gives the teacher a lightweight local way to label the current classroom or pilot session.

It is designed to make Runtime Learning Intelligence exposure summaries easier to interpret without adding accounts, a database, PII, new content, or scope changes.

## Where it appears

The panel appears in the Streamlit sidebar as a collapsed `Teacher Lesson / Session Setup` expander near the teacher/pilot monitor and Runtime Exposure Center.

## What it captures

- lesson/session label
- mode focus
- optional class period or group label
- optional teacher notes

## How it is stored

Metadata is stored in Streamlit session state only. It is local, temporary session context.

## Runtime Exposure Center integration

When a setup is active, the Runtime Exposure Center shows the current lesson/session context before the exposure summaries. This helps the teacher connect repeated targets, pasuk/skill concentration, and fallback/scope-small status to the current instructional purpose.

## What it does not do

- no auth
- no database
- no PII
- no student roster
- no raw log exposure
- no new content
- no question generation changes
- no question-selection changes
- no scoring/mastery changes
- no active runtime scope expansion
- no Perek activation

## Limitations

This is not an LMS, roster, or durable teacher account feature. It is a local classroom usability layer.

## Next possible improvement

If the session label proves useful, add it to a teacher-facing runtime exposure export/report in a later governed task.

## Teacher Runtime Exposure Export / Report

Teacher Runtime Evidence Export Suite V1 adds a collapsed sidebar `Teacher Runtime Report Export` section near the lesson setup and Runtime Exposure Center.

The export includes:

- teacher session metadata from this setup panel
- Runtime Exposure Center summary data
- repeated Hebrew targets
- repeated pasuk/skill concentration
- repeated skill/question-type concentration
- fallback/scope-small status
- missing or malformed log awareness
- cautious teacher interpretation
- safety and privacy notes

Reports save locally under `data/teacher_exports/` as Markdown and JSON files. The export uses local history only and includes no login, no database, no PII, and no raw JSONL logs.

The export has no scoring/mastery impact, no question-selection impact, no Runtime Learning Intelligence weighting impact, no reviewed-bank impact, and no runtime scope expansion. It is a teacher evidence artifact, not a mastery claim or content-approval gate.

Limitations: if session setup is missing or local logs are empty, the report records that evidence gap instead of inventing context or observations.

## Teacher Runtime Export Session Accuracy V1

Teacher Runtime Exposure Export now treats `Planned lesson focus` as a teacher/report label only. It does not change the student question mode, scoring/mastery, question selection, or active content scope.

The setup context is local Streamlit session state only. The canonical class/group key is `class_group_label`, with legacy class-period/group labels normalized for backward compatibility. Setup saves a local `saved_at` timestamp so exports can use a teacher-setup-window scope when a current pilot/session id is unavailable.

Reports can be current-session bounded when session identifiers are available. If that is not possible, they can use the teacher setup window, or clearly fall back to Recent local history. Recent local history may include prior testing sessions and should be treated as diagnostic only.

Markdown and JSON exports are generated from one export snapshot. No raw logs are exported. No login, No database, and No PII are used. No scoring/mastery, question-selection, question-generation, or content-scope changes are made.
