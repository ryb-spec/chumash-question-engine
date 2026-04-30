# Runtime Learning Intelligence Next-Step Recommendation - 2026-04-30

## Summary of manual smoke test result

Yossi's manual smoke test of Runtime Learning Intelligence V1 in Full Passuk view covered approximately 15 answered questions.

The smoke test found that repeated questions decreased and repeated Hebrew targets decreased. No weird skips, missing questions, slowdown, or confusing behavior were observed.

The overall judgment was: clean enough.

## Why Runtime Learning Intelligence V1 should remain enabled

- It appears to reduce repetition in the live runtime path.
- It did not show obvious UX or performance regression in the manual smoke test.
- It uses local attempt/pilot history only.
- It preserves fallback behavior in the implementation, though the fallback-specific smoke-test answer was ambiguous and still needs targeted confirmation.
- It does not change scoring/mastery, active scope, source truth, reviewed-bank status, auth, database behavior, or PII handling.

## What remains unproven

Small-pool fallback behavior still needs targeted confirmation because the manual answer was left as `yes/no`.

The recorded status is therefore: unknown / not determined.

## Recommended next product task

Add Teacher-Facing Runtime Exposure Summary in the App UI.

This is the highest-value next product task because Yossi can already see a positive repetition-control signal, and the next useful step is making exposure behavior visible to the teacher without adding accounts, a database, or PII.

## Optional focused test

Run a small-pool fallback test with an intentionally limited candidate pool.

This should confirm that the app still serves questions when all or nearly all safe candidates are overexposed.

## What not to do yet

- No Perek 7 expansion.
- No runtime scope expansion.
- No student login/database.
- No scoring/mastery changes.
- No broad `engine/flow_builder.py` refactor.
