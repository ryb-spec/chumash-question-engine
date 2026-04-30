# Bereishis Perek 5-6 Protected-Preview Candidate Review Decisions Applied - 2026-04-29

## Purpose

This artifact records Yossi's explicit protected-preview-candidate review decisions for seven Perek 5-6 review-layer candidates and separates clean-approved items from approved-with-revision items.

## Yossi decision table

| Candidate | Perek | Ref | Target | Decision | Required note |
|---|---:|---|---|---|---|
| g2srcdisc_p5_001 | 5 | Bereishis 5:1 | סֵפֶר | approve_for_internal_protected_preview_packet | Do not cluster with other genealogy-opening terms. |
| g2srcdisc_p5_002 | 5 | Bereishis 5:1 | תּוֹלְדֹת | approve_with_revision | Keep strictly part-of-speech. Do not make this a translation or genealogy-concept question. |
| g2srcdisc_p5_005 | 5 | Bereishis 5:28 | בֵּן | approve_for_internal_protected_preview_packet | Avoid clustering with בָּנִים / בָנוֹת. |
| g2srcdisc_p6_001 | 6 | Bereishis 6:3 | בָשָׂר | approve_with_revision | Keep part-of-speech only; do not cluster with other בָשָׂר-context items. |
| g2srcdisc_p6_003 | 6 | Bereishis 6:14 | תֵּבַת | approve_with_revision | Keep part-of-speech only; avoid translation/context-heavy treatment. |
| g2srcdisc_p6_006 | 6 | Bereishis 6:16 | פֶתַח | approve_with_revision | Keep as part-of-speech only and avoid clustering with צֹהַר / תֵּבָה. |
| g2srcdisc_p6_007 | 6 | Bereishis 6:17 | מַבּוּל | approve_with_revision | Do not make this a translation/context question without later review. |

## Clean approved items

- g2srcdisc_p5_001 / סֵפֶר: Clear noun target; good simple opening item.
- g2srcdisc_p5_005 / בֵּן: Clear simple family noun; lower risk than plural family cluster.

## Approved-with-revision items

- g2srcdisc_p5_002 / תּוֹלְדֹת: Keep strictly part-of-speech. Do not make this a translation or genealogy-concept question.
- g2srcdisc_p6_001 / בָשָׂר: Keep part-of-speech only; do not cluster with other בָשָׂר-context items.
- g2srcdisc_p6_003 / תֵּבַת: Keep part-of-speech only; avoid translation/context-heavy treatment.
- g2srcdisc_p6_006 / פֶתַח: Keep as part-of-speech only and avoid clustering with צֹהַר / תֵּבָה.
- g2srcdisc_p6_007 / מַבּוּל: Do not make this a translation/context question without later review.

## Excluded candidates that remain excluded

- g2srcdisc_p5_003
- g2srcdisc_p5_004
- g2srcdisc_p6_002
- g2srcdisc_p6_004
- g2srcdisc_p6_005

## Required revision notes

Revision items remain eligible for future planning discussion but should not be mixed into a clean internal packet lane unless Yossi explicitly authorizes that later. Their part-of-speech-only and spacing/context cautions must remain visible.

## What was not changed

- Perek 5 and Perek 6 remain inactive in runtime.
- Active runtime scope was not widened.
- Reviewed-bank content was not created.
- No internal protected-preview packet was created.
- Student-facing content was not created.
- Source truth, scoring, mastery, and question-selection logic were not changed.

## Safety boundary confirmation

Every reviewed row keeps runtime_allowed=false, reviewed_bank_allowed=false, protected_preview_allowed=false, student_facing_allowed=false, perek_5_activated=false, and perek_6_activated=false.

## Recommendation for next gate

Create a later small internal protected-preview packet from the two clean-approved items only unless Yossi explicitly authorizes a mixed packet that includes revision items.
