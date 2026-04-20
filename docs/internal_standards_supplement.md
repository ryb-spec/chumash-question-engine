# Internal Standards Supplement Governance

This repo now distinguishes three different standards-alignment layers:

## 1. External / canonical standards truth

- stored in the canonical skill crosswalk with `system_layer = canonical_truth`
- anchored to the external standards packet and benchmark references already in
  the foundations package

## 2. Internal reviewed supplement

- reserved for internal rows that have been deliberately reviewed and approved
  because the supported runtime needs a real skill concept that the external
  packet does not represent cleanly
- this layer is available in the crosswalk model, but **no rows are approved
  into it yet**

## 3. Engine-only alignment shim

- stored in the crosswalk with `system_layer = engine_extension`
- used when the supported runtime has a real lane that needs structural
  alignment, but we have not yet completed human standards review
- these rows help catalog alignment without claiming new external truth

## Current governance queue

The current review queue lives in:

- `data/standards/internal/engine_extension_review_queue.v1.json`

It covers the current `engine_extension` rows:

- `WORD.MEANING_BASIC`
  - runtime skill: `translation`
  - proposed disposition: `promote_reviewed_internal_supplement`
- `PREFIX.FORM_IDENTIFY`
  - runtime skill: `prefix`
  - proposed disposition: `keep_engine_extension`
- `PHRASE.UNIT_TRANSLATE`
  - runtime skill: `phrase_translation`
  - proposed disposition: `promote_reviewed_internal_supplement`

All three records still require human review. None should be treated as
external canonical truth, and none should silently become runtime-changing
policy.

## Governance status model

- `proposed`
- `under_review`
- `approved_internal`
- `kept_engine_only`
- `merged`
- `rejected`

The queue documents review intent, but it does not change runtime behavior,
scoring, mastery math, or student-facing UI.
