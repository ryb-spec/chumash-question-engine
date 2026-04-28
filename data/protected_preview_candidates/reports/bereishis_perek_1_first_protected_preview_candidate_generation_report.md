# Bereishis Perek 1 First Protected-Preview Candidate Generation Report

## Source

- Source planning-gate TSV: `data/protected_preview_planning_gate/bereishis_perek_1_first_protected_preview_planning_gate.tsv`

## Counts

- Candidate count: 18
- Excluded rows preserved: yes

## Family counts

- `basic_noun_recognition`: 8
- `shoresh_identification`: 1
- `vocabulary_meaning`: 9

## Risk/caution summary

- All candidates remain review-only and require Yossi/teacher protected-preview review.
- Answer-key, distractor, context-display, and Hebrew-rendering reviews remain `needs_yossi_review`.
- Excluded חיה, את, and הבדיל / בדל rows remain outside this layer.

## Hebrew integrity check

- Candidate rows preserve real UTF-8 Hebrew from the planning-gate layer.
- Placeholder corruption is not allowed.

## What was created

- Protected-preview candidate TSV.
- Protected-preview candidate Yossi/teacher review packet.
- Candidate generation report.
- Excluded-preserved report.

## What was not approved

- No protected-preview release content was approved.
- No reviewed-bank use was approved.
- No runtime use was approved.
- No student-facing use was approved.

## Gates closed

- `protected_preview_allowed = false` for every candidate.
- `reviewed_bank_allowed = false` for every candidate.
- `runtime_allowed = false` for every candidate.
- `student_facing_allowed = false` for every candidate.

## Next review task

Yossi reviews the protected-preview candidate packet and decides which items, if any, may be approved for a later protected-preview packet task.
