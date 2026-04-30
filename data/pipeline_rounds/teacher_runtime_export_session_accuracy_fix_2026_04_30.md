# Teacher Runtime Export Session Accuracy Fix

## Purpose

Fix Teacher Runtime Exposure Export V1 so teacher reports are session-aware, accurately labeled, and safe enough to support a separate content-expansion planning task.

## Manual QA issue discovered

Manual QA showed that the export could look like a current class/session report while using broad recent local history. It also showed a field mismatch for class/group labels and a misleading `Mode focus` label that sounded like it controlled student runtime mode.

## Root causes

- The export consumed the broad Runtime Exposure Center summary without export-scope metadata.
- Teacher setup stored a legacy class-period key while export normalization expected `class_group_label`.
- `Mode focus` was a teacher context label, not a runtime-control setting.
- Markdown and JSON rendering needed to be tied to one shared export data snapshot for each save/export action.

## What was fixed

- Added canonical `class_group_label` mapping while preserving legacy class/period/group keys.
- Added `saved_at` session context for teacher setup window filtering.
- Renamed the teacher label to `Planned lesson focus`.
- Added helper text that planned focus is a teacher/report label only and does not change student question mode.
- Added export-scope metadata and scoped exposure summaries.
- Added shared export snapshot behavior for Markdown and JSON rendering.

## Export scope behavior

Reports now identify one of four scope types:

- `current_pilot_session`
- `teacher_setup_window`
- `recent_local_history`
- `no_history_available`

Current-session scope is preferred when a pilot/session id is available and matching records exist. Teacher setup window scope is used when a setup `saved_at` timestamp can bound records. Recent local history remains available as a clearly labeled diagnostic fallback.

## Teacher setup field mapping fix

The canonical key is now `class_group_label`. The export still accepts legacy keys such as `class_period_label`, `class_period_group_label`, `period_label`, and `group_label`.

## Wording fix

Markdown exports and UI labels now use `Planned lesson focus`, not `Mode focus`. The report states that this label does not change student question mode.

## Single snapshot fix

The UI builds one export data snapshot and renders Markdown and JSON from that same object, so `generated_at`, repeated target counts, fallback counts, missing-data warnings, and export scope metadata match.

## Tests added

Focused tests cover class/group normalization, planned-focus wording, current-session filtering, teacher-setup-window filtering, recent-history fallback labeling, missing timestamp/session behavior, confidence level, and shared Markdown/JSON snapshot behavior.

## Validators added

Created `scripts/validate_teacher_runtime_export_session_accuracy.py`.

## Safety confirmation

- no runtime scope expansion
- no Perek activation
- no reviewed-bank promotion
- no scoring/mastery change
- no question-selection behavior change
- no question-selection weighting change
- no question generation change
- no source truth change
- no auth/database/PII
- no raw log exposure
- no student-facing content creation
- no validator weakening

## Content expansion readiness conclusion

The teacher evidence layer is ready to support a separate content-expansion planning branch. This artifact does not perform or authorize content expansion.

## Recommended next manual test

Run one Streamlit teacher export after saving Teacher Lesson / Session Setup with a class/group label and confirm the Markdown and JSON show the same generated timestamp, scope, records in scope, planned lesson focus, and class/group label.
