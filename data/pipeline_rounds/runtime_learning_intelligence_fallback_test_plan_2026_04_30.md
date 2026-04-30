# Runtime Learning Intelligence Fallback Test Plan - 2026-04-30

## Why fallback still needs testing

Yossi's manual smoke test found that repeated questions and repeated Hebrew targets decreased, with no observed slowdown, skips, missing questions, or confusing behavior.

However, the small-pool fallback field was left as `yes/no`, so fallback remains unknown / not determined from that smoke test.

## Manual small-pool fallback test

Use a deliberately narrow safe candidate pool and confirm that Runtime Learning Intelligence still serves a question instead of blocking the student flow.

## Recommended test setup

- Use a very narrow safe candidate pool.
- Seed history with repeated target exposures only in a safe local test environment.
- Confirm the app still serves a question.
- Confirm the Runtime Exposure Center shows fallback/scope-small status if local traces expose it.
- Confirm the app does not widen active scope.

## What not to do

- Do not force runtime scope expansion.
- Do not create fake student data in production logs.
- Do not change scoring/mastery.
- Do not change question-selection weighting as part of the manual test.
