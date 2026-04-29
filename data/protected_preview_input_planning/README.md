# Protected Preview Input Planning

This directory contains planning-only protected-preview input-candidate artifacts. It is not a protected-preview input list and does not generate questions, prompts, answer choices, answer keys, protected-preview content, reviewed-bank entries, runtime data, or student-facing content.

## Bereishis Perek 1 First Planning Batch

Artifacts:

- `data/protected_preview_input_planning/bereishis_perek_1_first_input_candidate_planning.tsv`
- `data/protected_preview_input_planning/reports/bereishis_perek_1_first_input_candidate_batch_balance_report.md`
- `data/protected_preview_input_planning/reports/bereishis_perek_1_first_input_candidate_planning_report.md`
- `data/protected_preview_input_planning/reports/bereishis_perek_1_first_input_candidate_yossi_review_sheet.md`
- `data/protected_preview_input_planning/reports/bereishis_perek_1_first_input_candidate_yossi_review_sheet.csv`

All rows are planning-only. All gates remain closed. No questions were generated.

Next action: Yossi reviews the planning candidate sheet.

## Bereishis Perek 1 First Planning Batch Review Applied

Yossi reviewed the first planning batch and approved all 24 rows for template-skeleton planning only.

- Review-applied report: `data/protected_preview_input_planning/reports/bereishis_perek_1_first_input_candidate_yossi_review_applied.md`
- Decision applied: `approve_for_template_skeleton_planning`
- Approved rows: 24
- Questions generated: no
- Protected-preview input list created: no
- Safety gates: closed

Next action: create template skeleton policy/planning for approved rows.

## Downstream Template-Skeleton Planning

The 24 approved first-batch planning rows now feed a template-skeleton planning layer:

- `data/template_skeleton_planning/README.md`
- `data/template_skeleton_planning/bereishis_perek_1_first_batch_template_skeleton_planning.tsv`
- `data/template_skeleton_planning/reports/bereishis_perek_1_first_batch_template_skeleton_planning_report.md`

This downstream layer is still planning-only and does not generate questions, answer choices, answer keys, protected-preview content, reviewed-bank entries, runtime data, or student-facing content.
