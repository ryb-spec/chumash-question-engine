# Broad Safe Vocabulary Bank V1 - 2026-04-30

## Purpose

This task creates a broader vocabulary-expansion layer that can move source-backed words forward as vocabulary-bank entries without turning them into generated questions, protected-preview packets, reviewed-bank content, or runtime content.

## Why the current gate is too narrow

The protected-preview process correctly advances only a tiny number of fully governed items. That is safe, but slow. A separate vocabulary-bank lane lets the project track more source-backed words and their blockers while keeping every higher approval gate closed.

## Approval-lane model

- Word-level approval means the word appears in canonical source text, has a stable pasuk reference, has an existing source-backed gloss or project-artifact basis, and has a clear basic skill category.
- Word-level approval does not mean question approval.
- Question-candidate readiness does not mean protected-preview approval.
- Protected-preview approval does not mean reviewed-bank approval.
- Reviewed-bank approval does not mean runtime activation.

## Perek 4 bank summary

The Perek 4 bank contains five source-backed vocabulary entries:

| Classification | Count | Items |
| --- | ---: | --- |
| protected_preview_ready | 2 | אִישׁ, צֹאן |
| revision_needed | 2 | אֲדָמָה, מִנְחָה |
| teacher_review_ready | 1 | אוֹת |

The two protected-preview-ready items are already separated from the broader word-level lane and remain protected-preview/internal only. The revision-needed items remain blocked from protected-preview movement until their revision notes are resolved.

## Perek 5/6 planning-only status

Existing Perek 5/6 artifacts were located and inventoried separately as planning-only references. They are not mixed into the Perek 4 protected-preview flow, and no Perek 5/6 word-level approval is created in this task.

## How this speeds expansion safely

The bank lets the team accumulate a broader list of known source-backed vocabulary targets while preserving a fail-closed chain:

- vocabulary bank first,
- then teacher review,
- then question-candidate review,
- then protected preview,
- then reviewed bank only after explicit approval,
- then runtime only after a separate runtime gate.

## What remains blocked

- Runtime activation remains blocked.
- Reviewed-bank promotion remains blocked.
- Question approval remains blocked.
- Revision-needed Perek 4 rows remain blocked from protected-preview use.
- Perek 5/6 rows remain planning-only in this task.

## Next recommended branch

`feature/simple-vocabulary-question-candidate-lane-v1`

Recommended next task: build a question-candidate lane that can convert selected word-level approved entries into teacher-review-ready question candidates without activating runtime or promoting reviewed-bank content.

## Safety confirmation

- Runtime scope widened: no.
- Perek activated: no.
- Reviewed-bank promotion: no.
- Runtime content promotion: no.
- Question approval created: no.
- Question generation changed: no.
- Question selection changed: no.
- Runtime Learning Intelligence weighting changed: no.
- Source truth changed: no.
- Fake teacher approval created: no.
- Fake student data created: no.
- Raw logs exposed: no.
- Validators weakened: no.
