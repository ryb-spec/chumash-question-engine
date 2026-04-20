# Pilot Freeze — 2026-04-20

## Purpose

This note freezes the current student pilot build before the next fresh classroom pilot.

## Build included

- faster answer -> next-question path
- affix cooldown / exit behavior
- affix answer-bank shape consistency
- trusted active-scope enforcement
- cleaner pilot accounting and teacher monitor
- short-run Learn Mode sequencing
- student-facing wording cleanup
- tightened verb-tense eligibility
- cleaner vav-led translation style

## What this build should now prevent

- no tense questions on forms like בְּצַלְמֵנוּ, הָרֹמֶשֶׂת, הַמְּאֹרֹת
- no broken affix answer banks
- no placeholder clue junk like `?` or `???`
- no trusted-mode outside-scope serving
- cleaner and more consistent `and he ...` / `and God ...` translations

## What remains weak or unproven

- not a full Hebrew parser
- not a full translation engine
- fresh live pilot still needed
- old pilot exports may contain stale pre-fix issues
- full suite was not run on every narrow pass

## Fresh pilot protocol

- 3–5 students
- Learn Mode only
- trusted active-scope mode
- 8–10 questions each
- teacher monitor open during the run
- evaluate only fresh sessions after this freeze

## What to watch

- speed in real browser use
- no outside-scope leaks
- no bogus morphology
- no broken distractors
- run feels like warmup -> meaning -> context when available
- unclear wording complaints

## Pass / fail criteria

Pass:

- zero outside-scope questions
- no repeated bogus tense targets
- no repeated broken clue/distractor issues
- students say it feels reasonably fast and clear
- unclear rate is materially lower than the recent bad sessions

Fail:

- repeated unclear wording across students
- any outside-scope leak
- any tense-on-non-verb question
- translations still feel inconsistent
- run still feels too mechanical

## Next steps after the pilot

- if the pilot is mostly clean: build a small teacher-authored truth layer for current scope
- if repeated issues remain: patch only the repeated issues
- do not expand scope until one fresh pilot is clean

## Evidence baseline

Older exports included stale issues. Newer trusted sessions were structurally cleaner but still showed high unclear rates. Only fresh post-freeze sessions should be used to judge this build.
