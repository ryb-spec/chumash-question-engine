# Perek 3 Pilot Remediation Completion Gate - 2026-04-29

## Purpose

This gate records the current Perek 3 pilot-remediation state after the wording-only fix batch and the distractor/source remediation audit. It prevents the project from falsely treating Perek 3 as complete while source and phrase-distractor issues remain open.

This gate does not activate Perek 4, does not widen runtime scope, does not promote reviewed-bank/runtime content, and does not approve student-facing expansion.

## Fixed or improved

| Issue | Status | Notes |
|---|---|---|
| Vague verb-form prompt | fixed in prior wording batch | `What form is shown?` was replaced with clearer tense/form wording. |
| Prefix prompt wording | fixed in prior wording batch | Prefix prompt now asks for the beginning letter prefix more clearly. |
| `דֶּרֶךְ` translation distractors | fixed now | Stored choices now avoid `Eve`, `Eden`, and `all`; correct answer `way` preserved. |
| `אֲרוּרָה` translation distractors | fixed now | Stored choices now avoid `Eve`, `Eden`, and `all`; correct answer `cursed` preserved. |

## Unresolved

| Issue | Status | Required next step |
|---|---|---|
| Perek 3 phrase_translation distractor quality | unresolved | Teacher/source review should inspect exact choices before broad repair. |
| `אָשִׁית` / `שית` source concern | unresolved | Yossi/source reviewer must confirm whether `שית` is correct and level-appropriate for `אָשִׁית`. |

## What was intentionally not changed

- No phrase_translation distractor logic was changed.
- No phrase_translation row was suppressed.
- No `אָשִׁית` / `שית` source decision was applied.
- No source-truth file was changed.
- No runtime scope or question-selection logic was changed.
- No scoring or mastery logic was changed.
- No Perek 4 activation occurred.

## Readiness decision

Perek 3 is not ready for full closure.

Perek 3 is not yet ready for a clean short re-pilot unless Yossi explicitly decides how to handle the unresolved phrase_translation distractor concern and the `אָשִׁית` / `שית` source follow-up. A narrow re-pilot can be prepared after those unresolved items are either reviewed, revised, suppressed in a later explicit task, or intentionally observed again.

Perek 3 is not ready for runtime expansion.

Perek 4 should not proceed to a teacher-review packet because of this gate alone. It may proceed only after a later explicit Yossi decision or after a short re-pilot clarifies whether the Perek 3 remediation is stable.

## Required next validation and re-pilot steps

1. Confirm the repaired `דֶּרֶךְ` and `אֲרוּרָה` answer choices display correctly.
2. Ask Yossi/source reviewer to decide the `אָשִׁית` / `שית` follow-up.
3. Build a focused phrase_translation distractor review packet before broad phrase repair.
4. Run a short re-pilot only after the unresolved items are handled or explicitly scoped out.
5. Record new real observations before any closure decision.

## Safety boundary confirmation

- No runtime scope expansion.
- No Perek 4 activation.
- No reviewed-bank/runtime promotion.
- No fake student data.
- No source-truth change.
- No distractor-generation logic change.
- No question-selection logic change.
- No scoring/mastery change.
