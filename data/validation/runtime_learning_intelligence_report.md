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

V1 exposes the teacher-facing summary through this governed report and `data/validation/runtime_learning_intelligence_summary.json`. Direct sidebar integration was deferred because `streamlit_app.py` remains intentionally protected by the curriculum diff guard outside UI-specific tasks.

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
