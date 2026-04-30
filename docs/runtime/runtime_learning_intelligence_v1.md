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

## Teacher expectations

V1 provides a teacher-facing exposure summary through:

- `data/validation/runtime_learning_intelligence_report.md`
- `data/validation/runtime_learning_intelligence_summary.json`

Direct Pilot Monitor/sidebar integration is deferred because `streamlit_app.py` remains intentionally protected by the curriculum diff guard outside UI-specific tasks.

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
