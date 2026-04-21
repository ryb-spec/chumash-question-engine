# Isolated Pilot Workflow

Use this when you want a fresh pilot export that reflects only the current run.

## 1. Prepare a fresh isolated log

```powershell
python scripts/pilot_isolated_run.py prepare --label fresh-check
```

This prints:
- a new empty pilot events file under `data/pilot/runs/`
- the PowerShell command to point Streamlit at that file
- the export command for that exact run

## 2. Launch Streamlit against that isolated log

Run the printed environment-variable command first, then start the app:

```powershell
$env:CHUMASH_PILOT_EVENT_LOG_PATH = "...\data\pilot\runs\pilot_session_events_...jsonl"
python -m streamlit run streamlit_app.py
```

## 3. Run the pilot

Use the app normally. Only that run will be written to the isolated log file.

## 4. Export only that run

```powershell
python scripts/pilot_isolated_run.py export --input "...\pilot_session_events_...jsonl" --output "...\pilot_session_events_..._review.json"
```

## Notes

- Old pilot history stays untouched in the default log.
- The export reads only the input log you point it at.
- Clear the environment variable or open a new shell when you want to go back to the default pilot log.
