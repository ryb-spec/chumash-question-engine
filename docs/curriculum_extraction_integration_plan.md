# Curriculum Extraction Integration Plan

## Isolation First

This branch is intentionally isolated. Its job is to define contracts, source tracing, samples, cleaned-seed ingestion, validation rules, and loader tooling without changing the active Chumash product.

It must not connect directly to runtime from this branch.

## How Later Integration Can Happen Safely

Later integration should happen only after extracted records are organized, validated, reviewed, and explicitly approved. A future integration branch can selectively import reviewed outputs from this factory into runtime-facing pipelines.

Batch 001 is intentionally not enough for runtime connection by itself. It is only a cleaned seed ingest with explicit `needs_review` and `not_runtime_active` markers.

## Possible Future Integration Points

- reviewed translation-support ingestion
- reviewed phrase-intent support
- reviewed parse-task support
- vocabulary-priority overlays
- generated-question preview review packets

These are only future possibilities. None of them are wired here.

## Required Gates Before Runtime Connection

1. Batch extraction validated
2. Manual review complete
3. Generated question previews reviewed
4. Promotion decision made
5. Explicit runtime integration branch created

## What This Branch Must Not Do

- modify runtime modules
- modify the active reviewed question bank
- change the active product
- promote corpus slices
- connect loader output directly to runtime selection logic

## Recommended Future Flow

1. Extract into isolated batches with complete source traces.
2. Validate the batch mechanically.
3. Review the extracted records manually.
4. Build preview questions outside runtime.
5. Review the previews.
6. Open a dedicated runtime integration branch only after approval.

That later branch should be narrow, explicit, and separately audited.
