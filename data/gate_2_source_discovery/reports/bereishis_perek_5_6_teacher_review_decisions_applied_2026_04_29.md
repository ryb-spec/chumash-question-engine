# Bereishis Perek 5-6 Teacher-Review Decisions Applied - 2026-04-29

## Purpose

This artifact records Yossi's explicit teacher-review decisions for the 12 Bereishis Perek 5-6 review-only source-discovery candidates and separates candidates that may proceed to the next safe candidate-planning gate from candidates that remain held, source-only, or source-follow-up.

## Yossi decision table

| Candidate | Perek | Ref | Target | Decision | Eligible next? | Note |
|---|---:|---|---|---|---|---|
| g2srcdisc_p5_001 | 5 | Bereishis 5:1 | סֵפֶר | approve_for_next_candidate_planning | true | Do not cluster with other genealogy-opening terms. |
| g2srcdisc_p5_002 | 5 | Bereishis 5:1 | תּוֹלְדֹת | approve_with_revision | true | Keep wording strictly part-of-speech; do not make this a translation or genealogy-concept question. |
| g2srcdisc_p5_003 | 5 | Bereishis 5:4 | בָּנִים | hold_for_spacing_or_balance | false | Hold for spacing/balance before any future packet or planning layer. |
| g2srcdisc_p5_004 | 5 | Bereishis 5:4 | בָנוֹת | hold_for_spacing_or_balance | false | Hold for spacing/balance before any future packet or planning layer. |
| g2srcdisc_p5_005 | 5 | Bereishis 5:28 | בֵּן | approve_for_next_candidate_planning | true | Avoid clustering with בָּנִים / בָנוֹת in a tiny packet. |
| g2srcdisc_p6_001 | 6 | Bereishis 6:3 | בָשָׂר | approve_with_revision | true | Keep part-of-speech only; do not use multiple בָשָׂר-context items together. |
| g2srcdisc_p6_002 | 6 | Bereishis 6:11 | חָמָס | source_only | false | Preserve as source evidence only; do not advance toward candidate planning yet. |
| g2srcdisc_p6_003 | 6 | Bereishis 6:14 | תֵּבַת | approve_with_revision | true | Keep as part-of-speech only; avoid translation/context-heavy treatment; avoid clustering with other ark terms. |
| g2srcdisc_p6_004 | 6 | Bereishis 6:14 | קִנִּים | needs_source_follow_up | false | Teacher/source review required before any next gate. |
| g2srcdisc_p6_005 | 6 | Bereishis 6:16 | צֹהַר | needs_source_follow_up | false | Teacher/source review required before any next gate. |
| g2srcdisc_p6_006 | 6 | Bereishis 6:16 | פֶתַח | approve_with_revision | true | Keep as part-of-speech only; avoid clustering with צֹהַר / תֵּבָה in a tiny packet. |
| g2srcdisc_p6_007 | 6 | Bereishis 6:17 | מַבּוּל | approve_with_revision | true | Do not make this a translation/context question without later review. |

## Expected decision counts

- approve_for_next_candidate_planning: 2
- approve_with_revision: 5
- hold_for_spacing_or_balance: 2
- needs_source_follow_up: 2
- source_only: 1
- reject: 0

## Candidates eligible for next candidate-planning gate

- g2srcdisc_p5_001 / סֵפֶר: approve_for_next_candidate_planning; Do not cluster with other genealogy-opening terms.
- g2srcdisc_p5_002 / תּוֹלְדֹת: approve_with_revision; Keep wording strictly part-of-speech; do not make this a translation or genealogy-concept question.
- g2srcdisc_p5_005 / בֵּן: approve_for_next_candidate_planning; Avoid clustering with בָּנִים / בָנוֹת in a tiny packet.
- g2srcdisc_p6_001 / בָשָׂר: approve_with_revision; Keep part-of-speech only; do not use multiple בָשָׂר-context items together.
- g2srcdisc_p6_003 / תֵּבַת: approve_with_revision; Keep as part-of-speech only; avoid translation/context-heavy treatment; avoid clustering with other ark terms.
- g2srcdisc_p6_006 / פֶתַח: approve_with_revision; Keep as part-of-speech only; avoid clustering with צֹהַר / תֵּבָה in a tiny packet.
- g2srcdisc_p6_007 / מַבּוּל: approve_with_revision; Do not make this a translation/context question without later review.

## Candidates held/source-only/source-follow-up

- g2srcdisc_p5_003 / בָּנִים: hold_for_spacing_or_balance; Hold for spacing/balance before any future packet or planning layer.
- g2srcdisc_p5_004 / בָנוֹת: hold_for_spacing_or_balance; Hold for spacing/balance before any future packet or planning layer.
- g2srcdisc_p6_002 / חָמָס: source_only; Preserve as source evidence only; do not advance toward candidate planning yet.
- g2srcdisc_p6_004 / קִנִּים: needs_source_follow_up; Teacher/source review required before any next gate.
- g2srcdisc_p6_005 / צֹהַר: needs_source_follow_up; Teacher/source review required before any next gate.

## What was not changed

- Perek 5 and Perek 6 remain inactive in runtime.
- No active runtime scope was widened.
- No reviewed-bank rows were created or promoted.
- No protected-preview packet or internal protected-preview packet was created.
- No student-facing content was created.
- No source text, source truth, scoring, mastery, or question-selection logic was changed.

## Safety boundary confirmation

All 12 candidates remain gated with runtime_allowed=false, reviewed_bank_allowed=false, protected_preview_allowed=false, student_facing_allowed=false, perek_5_activated=false, and perek_6_activated=false.

## Recommendation for next gate

Create a Perek 5-6 candidate-planning review checklist for the seven eligible candidates only. The next gate should remain planning-only and keep all runtime, reviewed-bank, protected-preview, and student-facing gates false.
