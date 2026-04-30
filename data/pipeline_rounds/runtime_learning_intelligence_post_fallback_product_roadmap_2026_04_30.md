# Runtime Learning Intelligence Post-Fallback Product Roadmap - 2026-04-30

## Current status

Runtime Learning Intelligence V1 is implemented, smoke-tested, teacher-visible through the Runtime Exposure Center, and manually fallback-confirmed for continued pilot use.

## Why this is now a meaningful product improvement

The runtime now has evidence that it can reduce repeated questions and repeated Hebrew targets while continuing to serve questions when the safe pool is small. The teacher can also see local exposure and fallback/scope-small status without auth, database, PII, or raw log exposure.

## Next recommended product tasks

### 1. Teacher Lesson / Session Setup V1

Purpose: Let a teacher label or select today's lesson/session before practice begins.

Why needed: Runtime exposure is now visible, but teachers still need a classroom-friendly way to say what today's run is for.

What it should accomplish: Store local session metadata, show the selected lesson/session in the teacher-facing area, and connect that context to local runtime exposure summaries.

What it must not do: No auth, no database, no PII, no new content, no scoring/mastery changes, and no runtime scope expansion except existing safe filters/config if explicitly approved.

Rough priority: highest.

### 2. Teacher Runtime Exposure Export / Report

Purpose: Let a teacher export or copy a concise local exposure report after a session.

Why needed: The sidebar view helps live monitoring, but Yossi will eventually need a durable local artifact for pilot review.

What it should accomplish: Export summarized counts, fallback status, and teacher notes without raw logs or PII.

What it must not do: No raw JSONL exposure, no database, no student roster, no public student-facing report, and no scoring/mastery changes.

Rough priority: medium.

### 3. First-30-Seconds Student Onboarding and Mode Clarity

Purpose: Make the first moments of the app clearer for a student or teacher starting a session.

Why needed: Runtime intelligence is improving, but classroom pilots also need the app to explain what mode the student is in and what to expect.

What it should accomplish: Clarify mode choice, session start, and basic expectations in lightweight UI copy.

What it must not do: No new curriculum content, no scoring/mastery changes, no authentication, no database, and no broad UI redesign.

Rough priority: medium.

## What not to do next

- No Perek 7 expansion yet.
- No runtime scope expansion yet.
- No student login/database yet.
- No scoring/mastery changes yet.
- No broad `engine/flow_builder.py` refactor yet.

## Final recommendation

Move next to Teacher Lesson / Session Setup V1.
