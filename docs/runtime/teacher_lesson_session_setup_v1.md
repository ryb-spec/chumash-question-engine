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
