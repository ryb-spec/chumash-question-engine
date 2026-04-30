# Runtime Learning Intelligence V1 Report

## Policy summary

Runtime Learning Intelligence V1 uses local attempt history and pilot session logs to reduce unnecessary repetition across sessions. It changes question-selection weighting only. It does not change scoring, mastery, active scope, source truth, or question content.

## Data sources used

- `data/attempt_log.jsonl`
- `data/pilot/pilot_session_events.jsonl`
- Streamlit session-state recent-question signatures

Missing files are tolerated. Malformed JSONL lines are skipped and counted.

## What is downweighted

- exact recent question repetition
- repeated Hebrew target
- repeated pasuk plus skill combination
- repeated skill plus question-type combination

## What is not suppressed

No candidate is permanently deleted. The policy uses weighting and fallback, not destructive removal.

## Fallback behavior

If the safe candidate pool is small or every candidate is already exposed, the runtime keeps the best available candidate rather than blocking all questions. Fallback is recorded through debug trace reason codes and surfaced in the teacher summary when available.

## Teacher-visible summary

V1 exposes the teacher-facing summary through this governed report, `data/validation/runtime_learning_intelligence_summary.json`, and the Streamlit sidebar Runtime Exposure Center. The sidebar center is read-only observability and does not change question-selection weighting, scoring/mastery, active scope, source truth, or content.

The teacher-facing report summarizes:

- repetition control active/inactive
- recent attempts counted
- most repeated Hebrew targets
- repeated skill/question types
- small-scope fallback count
- small/exhausted target-pool warning when applicable

## Known limitations

- V1 is local-file based and not a student account system.
- Historical attempt logs can bias selection until recent practice diversifies the pool.
- Exact-question matching depends on available question ID or prompt text.

## Safety confirmations

- no auth
- no database
- no PII
- no runtime-scope expansion
- no reviewed-bank promotion
- no source-truth change
- no scoring/mastery change

## Small-pool fallback manual test status

Yossi ran a focused small-pool fallback manual test on 2026-04-30 in Full Passuk view.

Confirmed evidence:

- small-pool fallback served questions
- app avoided crash or blank-screen behavior
- Runtime Exposure Center showed fallback/scope-small status
- repeated targets were still reduced where possible
- no weird skips or missing questions
- no slowdown
- no confusing behavior

Approximate question count was not recorded and remains unknown / not recorded.

## Product readiness status

Runtime Learning Intelligence V1 is ready for continued pilot use and should remain enabled.

Further student pilot evidence remains useful, especially for longer sessions, larger approved active scopes, and teacher usability of the Runtime Exposure Center.

Recommended next product task: Teacher Lesson / Session Setup V1.
