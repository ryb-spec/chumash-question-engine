# Dikduk Foundations Seed Package

This package lives in [`data/foundations/dikduk`](/c:/Users/ybassman/Documents/GitHub/chumash-question-engine/data/foundations/dikduk) and is a validated foundation-data layer for future Chumash dikduk work.

It is intentionally **not wired into live runtime selection, mastery updates, or question serving** in this pass.

## What These Files Are

- `*.schema.json`: local JSON schemas for the dikduk package structures
- `*.seed.json`: high-confidence, source-supported seed records
- `unresolved_candidates.json`: plausible-but-unresolved items that are **not** seed data

## Seed Data vs. Unresolved Candidates

Seed data is the validated foundation set we are comfortable storing as structured repo assets right now.

`unresolved_candidates.json` is the holding area for:

- lower-confidence candidates
- OCR-damaged examples
- ambiguous patterns that need human review
- anything that should not silently graduate into production-facing data

The validator and tests treat `unresolved_candidates.json` as a separate non-seed artifact on purpose.

## Source-Supported vs. Inferred

- Skills, rules, morphology patterns, vocabulary, archetypes, and confusion patterns are seeded only where the attached extraction supported them strongly enough to keep.
- Standards mappings remain explicitly **inferred**, not canonical external standards codes.
- The standards package must keep caution labels intact:
  - `standard_framework = "inferred_chumash_mastery_framework"`
  - `confidence` stays in an inferred band, not `explicit`

## How to Validate the Package

Run the local validator:

```powershell
python scripts/validate_dikduk_foundations.py
```

Run the focused tests:

```powershell
python -m pytest tests/test_dikduk_foundations.py -q
```

Or run the full suite:

```powershell
python -m pytest -q
```

## Recommended Next Step

The next honest integration step is to use this package as a **read-only foundation layer** for internal tooling:

1. reviewed-bank enrichment helpers
2. offline curriculum/coverage analysis
3. hand-audit and release-check reporting support

Only after that should we consider selective runtime integration, and even then it should remain reviewed-first and fail-closed.
