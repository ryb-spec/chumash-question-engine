# Broad Vocabulary Teacher Review Decisions Applied

Date: 2026-04-30

## Purpose

This report records Yossi's actual manual teacher-review decisions for Broad Vocabulary Teacher Review Packet V1.

The decisions apply only to the broad vocabulary and simple question candidate review layer. They do not create runtime questions, a protected-preview packet, reviewed-bank content, or runtime activation.

## Decision source

Yossi explicitly stated in chat: "I agree with these decisions. Mark them as mine and rewrite the prompt."

That instruction is treated as the manual decision source for this branch. These are actual Yossi decisions, not inferred approvals.

## Summary of Yossi decisions

- Word-level vocabulary decisions: 5
- Simple question candidate decisions: 9
- Revision/watch decisions: 2
- Clean candidates eligible only for a future protected-preview candidate gate: 5
- Revision-required rows before a future gate: 2
- Held/follow-up rows: 7 decision rows, represented as 5 unique held sources in the eligibility register

## Word-level vocabulary decisions

| Vocabulary ID | Hebrew | Decision | Effect |
|---|---|---|---|
| bsvb_p4_001 | אִישׁ | approve_word_level | word_level_approved_by_yossi |
| bsvb_p4_002 | צֹאן | approve_word_level_with_revision | word_level_approved_with_revision_by_yossi |
| bsvb_p4_003 | אֲדָמָה | hold_for_follow_up | held_for_follow_up |
| bsvb_p4_004 | מִנְחָה | hold_for_follow_up | held_for_follow_up |
| bsvb_p4_005 | אוֹת | approve_word_level | word_level_approved_by_yossi |

## Simple question candidate decisions

| Candidate ID | Hebrew | Lane | Decision | Effect |
|---|---|---|---|---|
| svqcl_p4_001 | אִישׁ | translate_hebrew_to_english | approve_for_protected_preview_candidate | eligible_for_future_protected_preview_candidate_gate |
| svqcl_p4_002 | אִישׁ | find_word_in_pasuk | approve_for_protected_preview_candidate | eligible_for_future_protected_preview_candidate_gate |
| svqcl_p4_003 | אִישׁ | classify_basic_part_of_speech | approve_for_protected_preview_candidate | eligible_for_future_protected_preview_candidate_gate |
| svqcl_p4_004 | צֹאן | translate_hebrew_to_english | approve_with_revision | revision_required_before_future_protected_preview_candidate_gate |
| svqcl_p4_005 | צֹאן | find_word_in_pasuk | approve_for_protected_preview_candidate | eligible_for_future_protected_preview_candidate_gate |
| svqcl_p4_006 | צֹאן | classify_basic_part_of_speech | approve_for_protected_preview_candidate | eligible_for_future_protected_preview_candidate_gate |
| svqcl_p4_007 | אוֹת | translate_hebrew_to_english | hold_for_follow_up | held_for_follow_up |
| svqcl_p4_008 | אוֹת | find_word_in_pasuk | hold_for_follow_up | held_for_follow_up |
| svqcl_p4_009 | אוֹת | classify_basic_part_of_speech | hold_for_follow_up | held_for_follow_up |

## Revision/watch decisions

| Vocabulary ID | Hebrew | Decision | Required next step |
|---|---|---|---|
| bsvb_p4_003 | אֲדָמָה | hold_for_follow_up | Decide whether the beginner gloss should be ground, earth, land, or context-specific. |
| bsvb_p4_004 | מִנְחָה | hold_for_follow_up | Decide whether the beginner gloss should be offering, gift, tribute, or context-specific. |

## Gloss revision required for צֹאן

Yossi approved צֹאן as a word-level item with revision. The next branch must normalize the beginner gloss consistently, using a teacher-approved gloss such as "flock / sheep". The prior expected answer "sheep and goats" must not remain in conflict with the reviewed beginner gloss unless it is intentionally preserved as an alternate note.

The translate_hebrew_to_english candidate `svqcl_p4_004` also requires that expected-answer revision before any future candidate gate.

## Held status for אוֹת question candidates

The word-level item `bsvb_p4_005` is approved, but all three simple question candidates for אוֹת remain held because the pasuk context may be conceptually loaded.

## Held status for אֲדָמָה and מִנְחָה

`bsvb_p4_003` and `bsvb_p4_004` remain held for follow-up. They are not clean candidates for the next gate.

## Eligible for future protected-preview candidate gate

Only these five simple candidates are clean eligible for a future protected-preview candidate gate:

- `svqcl_p4_001`
- `svqcl_p4_002`
- `svqcl_p4_003`
- `svqcl_p4_005`
- `svqcl_p4_006`

The future gate must still validate source evidence, prompt wording, expected answers, safety fields, and closed runtime/reviewed-bank gates.

## What remains blocked or held

- `bsvb_p4_002` and `svqcl_p4_004` require gloss/answer consistency revision.
- `bsvb_p4_003` remains held for gloss follow-up.
- `bsvb_p4_004` remains held for gloss follow-up.
- `svqcl_p4_007`, `svqcl_p4_008`, and `svqcl_p4_009` remain held with the אוֹת question-candidate group.

## What this does not authorize

- No runtime activation.
- No runtime scope expansion.
- No Perek activation.
- No protected-preview packet.
- No reviewed-bank movement.
- No runtime questions.
- No student-facing content.
- No scoring, mastery, question generation, question selection, source truth, or Runtime Learning Intelligence weighting change.

## Safety confirmation

- Runtime scope expansion: no
- Perek activation: no
- Protected-preview packet: no
- Protected-preview movement: no
- Reviewed-bank movement: no
- Runtime questions: no
- Runtime content movement: no
- Source-truth change: no
- Fake student data: no
- Raw log exposure: no
- Validator weakening: no

