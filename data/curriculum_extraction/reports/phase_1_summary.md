# Curriculum Extraction Factory Phase 1 Summary

This directory holds the Phase 1 scaffold for an isolated curriculum extraction lane.

## Scope

- Create contracts only: registry, manifest, schemas, tiny sample records, validator, loader, tests, and docs.
- Keep everything outside runtime and outside the active reviewed question bank.
- Preserve raw Hebrew and English fields in sample records.

## Modeled Resource Packages

1. Linear Chumash Translation for Most Parshiyos in Torah
2. What is the Pasuk Coming to Teach?
3. Eli Bacharach: Parshas Shemos Shorashim, Prefix and Suffix Skills
4. Eli Bacharach: Parshas Va'eira Textual Skills
5. Vocabulary Priority Pack
6. First 150 Shorashim and Keywords in Bereishis (optional support)

## Phase 1 Guarantees

- `runtime_active` is `false` everywhere in the extraction manifest and source registry.
- Sample records are marked `needs_review`, `not_runtime_active`, and `low`.
- The validator is designed to fail if a sample record is marked reviewed, runtime-active, or high-confidence.

## Not Included Yet

- Full dataset extraction
- Normalization passes
- Generated question previews
- Runtime wiring
- Reviewed question bank import
