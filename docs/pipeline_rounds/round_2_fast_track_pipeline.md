# Round 2 Fast-Track Pipeline

## A. Purpose

Round 1 built the system: source verification, enrichment review, question eligibility, template controls, row-level review, controlled drafts, candidate gates, and an internal protected-preview packet. Round 2 uses the system. The goal is to move future perakim or slices through the same safe process in fewer steps while preserving review gates and closed downstream status.

This document is planning documentation only. It does not generate questions, answer choices, answer keys, protected-preview release content, reviewed-bank entries, runtime data, or student-facing content.

## B. Four-gate compressed pipeline

### Gate 1: Source + enrichment + eligibility readiness

- Confirm verified source-to-skill coverage for `{SCOPE_NAME}` from `{START_REF}` to `{END_REF}`.
- Confirm enrichment candidates exist and are linked to the verified source map.
- Confirm enrichment review has been applied and unresolved rows remain follow-up or source-only.
- Run the question-eligibility audit.
- Produce approved input candidates only after explicit Yossi eligibility decisions.

### Gate 2: Input planning + template controls

- Select 20-30 approved candidates, or `{TARGET_ROW_COUNT}` if the task specifies a tighter target.
- Require a batch balance table with family counts, risk counts, pasuk/ref ranges, duplicate Hebrew tokens, direct-object-marker rationale, and shoresh rationale.
- Apply approved wording, template, answer-key, distractor, context-display, and Hebrew-rendering policies.
- Create a row-level review sheet with exact wording, answer-key language, distractor constraints, context display, Hebrew rendering, and protected-preview gate fields.

### Gate 3: Controlled draft packet

- Generate controlled teacher-review drafts only from rows explicitly approved for controlled draft generation.
- Keep reviewed-bank, runtime, and student-facing gates closed.
- Keep protected-preview release gates closed unless a later explicit release task exists.
- Apply Yossi draft decisions and resolve revisions before any candidate-packet planning.

### Gate 4: Internal protected-preview packet

- Create an internal protected-preview packet only from approved controlled draft items.
- Preserve prompts, answer choices, expected answers, explanations, and evidence notes as internal review material.
- Do not create reviewed-bank entries, runtime data, or student-facing content.
- Produce a round completion report and keep post-preview review required before broader use.

## C. What can be batched

- Vocabulary meaning rows with reviewed evidence.
- Basic noun recognition rows that stay simple.
- Clean shoresh rows with reviewed roots.
- Input planning selection sheets.
- Yossi review sheets.
- Balance reports, generation reports, and excluded-row reports.

## D. What must stay cautious

- Verb forms remain deferred until a morphology-question wording standard exists.
- Prefix and preposition rows need separate policy support.
- Direct-object marker rows must ask about function, not simple translation.
- Complex shoresh rows need surface/root separation and review.
- Answer keys require explicit review before preview use.
- Distractors must remain reviewed and non-misleading.
- Hebrew rendering must be checked for corruption.
- Protected-preview gate approval remains separate from packet creation.

## E. Stop conditions

Codex must stop and report when any of these appear:

- Unverified source-to-skill rows are being used as inputs.
- Unresolved enrichment rows are selected as inputs.
- Verb-form rows are included without an approved morphology-question wording policy.
- High-risk rows are included in a protected-preview planning batch.
- Hebrew corruption appears, including placeholder marks or mojibake.
- A required batch balance table is missing.
- Protected-preview release, reviewed-bank, runtime, or student-facing gates are opened accidentally.

## F. Review points that still require Yossi

- Extraction verification.
- Enrichment verification.
- Eligibility decision.
- Row-level pre-generation decision.
- Controlled draft review.
- Internal protected-preview packet review.
