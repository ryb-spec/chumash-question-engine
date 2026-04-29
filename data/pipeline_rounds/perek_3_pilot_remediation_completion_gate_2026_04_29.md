# Perek 3 Pilot Remediation Completion Gate - 2026-04-29

## Purpose

This gate records the current Perek 3 pilot-remediation state after the wording-only fix batch, the distractor/source remediation audit, and Yossi's language decisions. It prevents the project from falsely treating Perek 3 as complete while source and phrase-distractor issues remain open.

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
| `אָשִׁית` / `שית` source concern | excluded from short re-pilot; unresolved for full closure | Yossi decided this is not beginner-ready for this pilot level. This does not mean `שית` is wrong. |

## Yossi language decisions applied

- `אָשִׁית` / `שית` is not appropriate as a normal beginner shoresh-identification question without explicit teaching/explanation.
- `אָשִׁית` / `שית` is excluded from the short Perek 3 re-pilot lane and remains documented as source/teacher follow-up.
- Phrase-translation distractors must test the whole phrase.
- Unverified phrase_translation items are excluded from the short Perek 3 re-pilot lane and remain blocking for full closure until item-level whole-phrase audit is complete.

## What was intentionally not changed

- No phrase_translation distractor logic was changed.
- No phrase_translation row was changed or marked fully resolved.
- No runtime suppression metadata was applied; exclusions are recorded in gate/scope artifacts only.
- No source-truth file was changed.
- No runtime scope or question-selection logic was changed.
- No scoring or mastery logic was changed.
- No Perek 4 activation occurred.

## Readiness decision

Perek 3 is not ready for full closure.

Perek 3 is ready for a short re-pilot only with exclusions. The short re-pilot may test the wording clarity fixes plus the repaired `דֶּרֶךְ` and `אֲרוּרָה` translation distractors. The short re-pilot must not treat `אָשִׁית` / `שית` or unverified phrase_translation items as active re-pilot evidence.

Perek 3 is not ready for runtime expansion.

Perek 4 should not proceed to a teacher-review packet because of this gate alone. It may proceed only after a later explicit Yossi decision or after a short re-pilot clarifies whether the Perek 3 remediation is stable.

## Required next validation and re-pilot steps

1. Confirm the repaired `דֶּרֶךְ` and `אֲרוּרָה` answer choices display correctly.
2. Run a short re-pilot of only the remediated lane: wording clarity, `דֶּרֶךְ`, and `אֲרוּרָה`.
3. Keep `אָשִׁית` / `שית` excluded from the short re-pilot and documented as advanced/source follow-up.
4. Keep unverified phrase_translation items excluded from the short re-pilot and blocking full closure.
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
