# Teacher Lesson / Session Setup V1 - 2026-04-30

## Purpose

Create a lightweight teacher-facing way to label or select today's lesson/session before practice begins, so classroom pilots can connect Runtime Learning Intelligence exposure summaries to a clear instructional context.

## What was added

- A local lesson/session metadata helper in `runtime/lesson_session_setup.py`.
- A collapsed Streamlit sidebar panel titled `Teacher Lesson / Session Setup`.
- Session context fields for lesson/session label, mode focus, optional class period/group label, and optional teacher notes.
- Runtime Exposure Center integration that shows the current lesson/session context above exposure counts.
- Governed JSON contract, validator, tests, and documentation updates.

## UI location

The setup panel appears in the Streamlit sidebar near the teacher/pilot monitor and Runtime Exposure Center.

## What it stores

The setup stores local session metadata in Streamlit session state only:

- lesson/session label
- mode focus
- class period or group label
- teacher notes
- local updated timestamp

## What it does not store or use

- no auth
- no database
- no PII
- no student roster
- no external services
- no raw log exposure

## Runtime safety boundaries

This task does not change runtime scope, question-selection weighting, scoring/mastery, source truth, question generation, reviewed-bank status, Perek activation, or student-facing content.

## Teacher workflow

A teacher can open the sidebar, expand `Teacher Lesson / Session Setup`, add a short label for the current lesson or pilot run, and then view that same context inside the Runtime Exposure Center while monitoring repeated targets and fallback/scope-small status.

## Known limitations

- Metadata is local session-state context, not a durable account system.
- It is not a class roster or LMS feature.
- It does not filter active scope by itself.

## Recommended next step

Use this in a live/manual classroom-style session and decide whether a local export/report should include the session label.
