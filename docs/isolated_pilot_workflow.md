# Isolated Pilot Workflow

Use this when you want a fresh pilot export that reflects only the current run.

## Fastest Combined Release-Check Loop

If you want the shortest post-change loop, use the unified wrapper:

```powershell
python scripts/release_check.py prepare --label release-check
$env:CHUMASH_PILOT_EVENT_LOG_PATH = "...\data\pilot\runs\pilot_session_events_...jsonl"
python -m streamlit run streamlit_app.py
python scripts/release_check.py finalize --input "...\data\pilot\runs\pilot_session_events_...jsonl"
```

That single `finalize` command writes:
- `pilot_review.json`
- `hand_audit.json`
- `hand_audit.md`
- `release_check_summary.json`
- `release_check_summary.md`

under a timestamped release-check directory in `data/validation/release_checks/`.

The separate `scripts/pilot_isolated_run.py` workflow still works when you only want the pilot-review side.

## Quick Loop

```powershell
python scripts/pilot_isolated_run.py prepare --label post-fix-check
$env:CHUMASH_PILOT_EVENT_LOG_PATH = "...\data\pilot\runs\pilot_session_events_...jsonl"
python -m streamlit run streamlit_app.py
python scripts/pilot_isolated_run.py review --input "...\data\pilot\runs\pilot_session_events_...jsonl"
```

The `review` command writes the JSON artifact and prints the compact release-check summary in one step.

## 1. Prepare a fresh isolated log

```powershell
python scripts/pilot_isolated_run.py prepare --label fresh-check
```

This prints:
- a new empty pilot events file under `data/pilot/runs/`
- the PowerShell command to point Streamlit at that file
- the export command for that exact run
- the review command for that exact run

## 2. Launch Streamlit against that isolated log

Run the printed environment-variable command first, then start the app:

```powershell
$env:CHUMASH_PILOT_EVENT_LOG_PATH = "...\data\pilot\runs\pilot_session_events_...jsonl"
python -m streamlit run streamlit_app.py
```

## 3. Run the pilot

Use the app normally. Only that run will be written to the isolated log file.

## 4. Review only that run

```powershell
python scripts/pilot_isolated_run.py review --input "...\pilot_session_events_...jsonl"
```

This will:
- write `data/pilot/exports/<log-stem>_review.json` by default
- print the compact release-decision summary to stdout

If you want only the JSON artifact without the compact summary:

```powershell
python scripts/pilot_isolated_run.py export --input "...\pilot_session_events_...jsonl"
```

Optional filters for either command:

```powershell
python scripts/pilot_isolated_run.py review `
  --input "...\pilot_session_events_...jsonl" `
  --scope-id "local_parsed_bereishis_1_1_to_2_17" `
  --trusted-active-scope-only `
  --latest-session-only `
  --session-start-since "2026-04-21T12:28:00+00:00" `
  --session-start-until "2026-04-21T13:00:00+00:00"
```

The `session-start-*` filters are inclusive and apply to whole sessions, not individual events.

## 5. Read the review artifact

The JSON export now includes:
- `runtime_scope_id`
- `review_scope_id`
- `substantive_session_count`
- `shell_session_count`
- `summary.trusted_scope_violations`
- `summary.served_without_validation_signals`
- `summary.top_served_question_families`
- `summary.top_flagged_unclear_items`
- `summary.top_pre_serve_rejection_codes`
- `release_review_summary`
- `review_window`

Check `review_window` first:
- `fresh_run_only: true` means the input log is an isolated `data/pilot/runs/...` file
- `warnings: []` means no mixed-log warning was detected
- `excluded_event_count > 0` means the current artifact was filtered and does not represent the full source log
- `latest_session_only: true` means the artifact was intentionally narrowed to the latest included session window
- if `runtime_scope_id` and `review_scope_id` differ, the artifact will say so explicitly in `review_window.warnings`

For release decisions, the strongest artifact is:
- an isolated run log under `data/pilot/runs/`
- `fresh_run_only: true`
- `review_window.warnings` empty or only `review_filters_applied`
- `summary.trusted_scope_violations` empty
- `summary.served_without_validation_signals.served_without_validation_flag = 0`
- `flagged_review_queue` empty or clearly explainable

The fastest release-check view is `release_review_summary`, which surfaces:
- scope
- session count
- substantive vs shell sessions
- trusted-scope violations
- served-without-validation count
- top unclear items
- top served question families
- top pre-serve rejection codes
- repeated-target feel
- mixed-log warnings

## Notes

- Old pilot history stays untouched in the default log.
- The export reads only the input log you point it at.
- Clear the environment variable or open a new shell when you want to go back to the default pilot log.
