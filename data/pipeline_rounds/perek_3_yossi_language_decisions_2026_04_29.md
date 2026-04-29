# Perek 3 Yossi Language Decisions - 2026-04-29

## Date and branch

- Date: 2026-04-29
- Branch: `feature/perek-3-yossi-language-decisions-final-gate`

## Purpose

This record applies Yossi's explicit language/curriculum decisions for the remaining Perek 3 pilot blockers. It records what is allowed for a short re-pilot and what remains blocked for full closure.

This artifact does not activate Perek 4, does not widen runtime scope, does not promote content to runtime, and does not invent source truth.

## Decision #1: `אָשִׁית` / `שית`

For the current Perek 3 pilot level, do not serve `אָשִׁית` as a standard beginner shoresh-identification question.

Treat `אָשִׁית` / `שית` as an advanced or source-follow-up item.

This does not mean `שית` is wrong.

`אָשִׁית` / `שית` is not appropriate as a normal beginner shoresh-identification question without explicit teaching/explanation.

Implementation implication:

- Exclude `אָשִׁית` / `שית` from the short Perek 3 re-pilot scope.
- Keep it documented as a source/teacher follow-up item.
- Do not mark it approved.
- Do not change source truth.
- Do not promote it.
- Do not delete the issue.

## Decision #2: phrase_translation distractor policy

Phrase-translation distractors must test the whole phrase.

A good `phrase_translation` distractor should be a plausible but incorrect phrase-level translation.

Bad `phrase_translation` distractors include:

- random nearby words
- random nouns from the pasuk
- single-word translations when the question asks for a phrase
- choices that only test one word inside the phrase
- choices that are obviously unrelated and do not test comprehension
- choices that could also be correct in context
- choices that are confusing because they mix phrase-level and word-level tasks

Implementation implication:

- Record this as the Perek 3 phrase_translation distractor policy.
- Do not broadly rewrite phrase_translation logic in this task.
- Do not mark phrase_translation fully resolved until each item is audited against the whole-phrase rule.
- Exclude unverified phrase_translation items from the short Perek 3 re-pilot scope.

## What these decisions allow

- A short Perek 3 re-pilot may proceed if `אָשִׁית` / `שית` and unverified phrase_translation items are explicitly excluded from the short re-pilot.
- The short re-pilot may test already-remediated wording clarity fixes.
- The short re-pilot may test the repaired `דֶּרֶךְ` and `אֲרוּרָה` translation distractors.

## What these decisions do not allow

- No runtime expansion.
- No Perek 4 activation.
- No reviewed-bank/runtime promotion.
- No claim that all Perek 3 question types are approved.
- No claim that `אָשִׁית` / `שית` is wrong.
- No claim that phrase_translation is fully resolved.
- No fake student observations or invented teacher decisions.

## Short re-pilot implication

Short re-pilot readiness is allowed only for the remediated lane:

- revised tense/form wording
- revised prefix prompt wording
- `דֶּרֶךְ` translation distractor repair
- `אֲרוּרָה` translation distractor repair

The short re-pilot must exclude:

- `אָשִׁית` / `שית`
- unverified phrase_translation items
- Perek 4 content
- any runtime expansion

## Full closure implication

Full Perek 3 closure is not allowed now. Full closure remains blocked until:

- `אָשִׁית` / `שית` receives a later explicit teacher/source outcome.
- phrase_translation items receive item-level whole-phrase distractor review.
- new real re-pilot evidence is recorded and applied in a later explicit task.

## Perek 4 implication

Perek 4 remains inactive. These decisions do not authorize Perek 4 activation, Perek 4 runtime work, Perek 4 reviewed-bank promotion, or Perek 4 student-facing content.

## Safety boundary confirmation

- No runtime scope expansion.
- No Perek 4 activation.
- No reviewed-bank/runtime promotion.
- No source-truth change.
- No phrase_translation logic change.
- No question-selection change.
- No fake student data.
