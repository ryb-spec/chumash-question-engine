# Perek 4 Broad Vocabulary Protected-Preview Candidate Gate V1

Date: 2026-04-30

## Purpose

This gate uses Yossi's applied Broad Vocabulary Teacher Review decisions to identify only the clean eligible Perek 4 simple vocabulary candidates that may move to a future protected-preview packet planning step.

This is a candidate gate only. It does not create a protected-preview packet, reviewed-bank content, runtime questions, student-facing content, or runtime activation.

## Source artifacts

- `data/teacher_review_decisions/bereishis_perek_4_broad_vocabulary_teacher_review_decisions_applied_2026_04_30.tsv`
- `data/teacher_review_decisions/bereishis_perek_4_broad_vocabulary_teacher_review_decisions_applied_2026_04_30.json`
- `data/teacher_review_decisions/bereishis_perek_4_broad_vocabulary_future_gate_eligibility_register_2026_04_30.tsv`
- `data/teacher_review_decisions/bereishis_perek_4_broad_vocabulary_future_gate_eligibility_register_2026_04_30.json`

## Clean input set used

Only these five clean eligible rows are included:

| Candidate ID | Vocabulary ID | Hebrew | Lane | Expected answer |
|---|---|---|---|---|
| svqcl_p4_001 | bsvb_p4_001 | אִישׁ | translate_hebrew_to_english | man |
| svqcl_p4_002 | bsvb_p4_001 | אִישׁ | find_word_in_pasuk | אִישׁ |
| svqcl_p4_003 | bsvb_p4_001 | אִישׁ | classify_basic_part_of_speech | noun |
| svqcl_p4_005 | bsvb_p4_002 | צֹאן | find_word_in_pasuk | צֹאן |
| svqcl_p4_006 | bsvb_p4_002 | צֹאן | classify_basic_part_of_speech | noun |

## Blocked rows preserved

Revision-required rows remain outside this gate:

- `bsvb_p4_002`: צֹאן word-level gloss consistency must be resolved.
- `svqcl_p4_004`: צֹאן translate_hebrew_to_english expected answer must be normalized before any later gate.

Held rows remain outside this gate:

- `bsvb_p4_003`: אֲדָמָה remains held for ground / earth / land follow-up.
- `bsvb_p4_004`: מִנְחָה remains held for offering / gift / tribute follow-up.
- `svqcl_p4_007`: אוֹת translate_hebrew_to_english remains held.
- `svqcl_p4_008`: אוֹת find_word_in_pasuk remains held.
- `svqcl_p4_009`: אוֹת classify_basic_part_of_speech remains held.

## Gate decision

The five clean candidates are eligible only for a future protected-preview packet planning step. The next step must still build a bounded packet, preserve safety metadata, and keep runtime/reviewed-bank gates closed.

## What this does not authorize

- No runtime activation.
- No runtime scope expansion.
- No Perek activation.
- No protected-preview packet creation.
- No reviewed-bank movement.
- No runtime questions.
- No student-facing content.
- No scoring/mastery change.
- No question generation or question selection change.
- No source-truth change.
- No Runtime Learning Intelligence weighting change.

## Safety confirmation

- Runtime scope widened: no
- Perek activated: no
- Protected-preview packet created: no
- Protected-preview movement: no
- Reviewed-bank movement: no
- Runtime questions created: no
- Runtime content movement: no
- Student-facing content created: no
- Source truth changed: no
- Fake teacher approval created: no
- Fake student data created: no
- Raw logs exposed: no
- Validators weakened: no

