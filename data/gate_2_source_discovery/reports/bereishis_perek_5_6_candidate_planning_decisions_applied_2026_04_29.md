# Bereishis Perek 5-6 Candidate-Planning Decisions Applied - 2026-04-29

## Purpose

This artifact records Yossi's explicit candidate-planning decisions for the seven Perek 5-6 candidates that were eligible for planning review.

## Yossi planning decision table

| Candidate | Perek | Ref | Target | Decision | Required note |
|---|---:|---|---|---|---|
| g2srcdisc_p5_001 | 5 | Bereishis 5:1 | סֵפֶר | advance_to_protected_preview_candidate_review | Do not cluster with other genealogy-opening terms. |
| g2srcdisc_p5_002 | 5 | Bereishis 5:1 | תּוֹלְדֹת | advance_with_minor_revision | Keep strictly part-of-speech. Do not turn into translation or genealogy concept. |
| g2srcdisc_p5_005 | 5 | Bereishis 5:28 | בֵּן | advance_to_protected_preview_candidate_review | Avoid clustering with בָּנִים / בָנוֹת. |
| g2srcdisc_p6_001 | 6 | Bereishis 6:3 | בָשָׂר | advance_with_minor_revision | Keep part-of-speech only. Do not cluster with other בָשָׂר-context items. |
| g2srcdisc_p6_003 | 6 | Bereishis 6:14 | תֵּבַת | advance_with_minor_revision | Keep part-of-speech only; avoid translation/context-heavy treatment. |
| g2srcdisc_p6_006 | 6 | Bereishis 6:16 | פֶתַח | advance_with_minor_revision | Keep as part-of-speech only and avoid clustering with צֹהַר / תֵּבָה. |
| g2srcdisc_p6_007 | 6 | Bereishis 6:17 | מַבּוּל | advance_with_minor_revision | Do not make this a translation/context question without later review. |

## Two clean advancing candidates

- g2srcdisc_p5_001 / סֵפֶר: Clear noun target. Good simple Perek 5 candidate.
- g2srcdisc_p5_005 / בֵּן: Clear simple family noun. Lower-risk than plural family cluster.

## Five advancing-with-minor-revision candidates

- g2srcdisc_p5_002 / תּוֹלְדֹת: Keep strictly part-of-speech. Do not turn into translation or genealogy concept.
- g2srcdisc_p6_001 / בָשָׂר: Keep part-of-speech only. Do not cluster with other בָשָׂר-context items.
- g2srcdisc_p6_003 / תֵּבַת: Keep part-of-speech only; avoid translation/context-heavy treatment.
- g2srcdisc_p6_006 / פֶתַח: Keep as part-of-speech only and avoid clustering with צֹהַר / תֵּבָה.
- g2srcdisc_p6_007 / מַבּוּל: Do not make this a translation/context question without later review.

## Excluded candidates that remain blocked

- g2srcdisc_p5_003: held for spacing/balance
- g2srcdisc_p5_004: held for spacing/balance
- g2srcdisc_p6_002: source_only
- g2srcdisc_p6_004: needs_source_follow_up
- g2srcdisc_p6_005: needs_source_follow_up

## Required notes/revisions

All advancing-with-minor-revision items must preserve their part-of-speech-only lane and spacing/context cautions before any later review layer can consider them further.

## What was not changed

- Perek 5 and Perek 6 remain inactive in runtime.
- Active runtime scope was not widened.
- Reviewed-bank content was not created.
- A protected-preview packet was not created.
- Student-facing content was not created.
- Source truth, scoring, mastery, and question-selection logic were not changed.

## Safety boundary confirmation

Every advancing row keeps runtime_allowed=false, reviewed_bank_allowed=false, protected_preview_allowed=false, student_facing_allowed=false, perek_5_activated=false, and perek_6_activated=false.

## Recommendation for next gate

Yossi should review the protected-preview-candidate review-only TSV next and decide which, if any, may later advance toward an internal protected-preview packet task.
