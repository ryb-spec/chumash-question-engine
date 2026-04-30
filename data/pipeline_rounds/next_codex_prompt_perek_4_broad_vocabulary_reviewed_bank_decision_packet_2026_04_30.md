# Next Codex Prompt: Perek 4 Broad Vocabulary Reviewed-Bank Decision Packet V1

Future branch:

`feature/perek-4-broad-vocabulary-reviewed-bank-decision-packet-v1`

## Purpose

Create a Yossi reviewed-bank decision packet for exactly the five observed Perek 4 broad-vocabulary candidates from the reviewed-bank candidate planning gate.

## Inputs

- `data/reviewed_bank_candidate_planning/bereishis_perek_4_broad_vocabulary_reviewed_bank_candidate_planning_2026_04_30.tsv`
- `data/reviewed_bank_candidate_planning/bereishis_perek_4_broad_vocabulary_reviewed_bank_candidate_planning_2026_04_30.json`
- `data/reviewed_bank_candidate_planning/bereishis_perek_4_broad_vocabulary_reviewed_bank_candidate_evidence_map_2026_04_30.md`
- `data/reviewed_bank_candidate_planning/bereishis_perek_4_broad_vocabulary_reviewed_bank_candidate_blocked_register_2026_04_30.md`

## Candidate Decision Options

For each of the five candidates, provide exactly these Yossi decision options:

- `approve_for_reviewed_bank`
- `approve_with_revision_before_reviewed_bank`
- `hold_for_follow_up`
- `reject_for_reviewed_bank`

## Strict Boundaries

- Do not apply decisions.
- Do not create reviewed-bank entries.
- Do not promote reviewed-bank content.
- Do not activate runtime.
- Do not widen runtime scope.
- Do not create runtime questions.
- Do not create student-facing content.
- Do not change source truth.
- Keep blocked and revision-required rows excluded.

## Required Work

- Create a decision packet Markdown file for Yossi.
- Create a machine-readable blank decision contract.
- Create validator and tests.
- Update docs/indexes concisely.
- Keep all safety flags closed.
