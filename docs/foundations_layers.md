# Foundations Layers

These foundation resources are a versioned reference layer for future standards
alignment, analytics, hinting, paradigms, and teacher operations. They are
loadable and validated, but they are not auto-promoted into the student-facing
runtime.

## Current source of truth

- `streamlit_app.py`
  - supported student-facing runtime
- `assessment_scope.py` and `data/corpus_manifest.json`
  - active runtime corpus and scope
- `data/pesukim_100.json`, `data/word_bank.json`, `data/word_occurrences.json`,
  `data/translation_reviews.json`
  - active parsed runtime data
- `skill_catalog.py`
  - current runtime skill catalog and ordering

The new foundation resources do not replace any of the above yet.

## Helper modules

- `foundation_resources.py`
  - manifest-backed loading and structural validation
- `foundation_benchmark.py`
  - read-only access to benchmark section weights, archetypes, and coverage
- `foundation_paradigms.py`
  - read-only access to grammar paradigm and pronoun query helpers
- `foundation_lexicon.py`
  - read-only access to high-frequency lexicon tiers and priority profiles
- `foundation_teacher_ops.py`
  - read-only access to teacher/admin workflow seed data

These helpers are safe integration seams. They do not change runtime scoring,
mastery, corpus scope, or student-facing behavior by themselves.

## Layer structure

- `data/standards/crosswalks/`
  - canonical standards crosswalk seeds
  - use for future catalog alignment and standards mapping
- `data/benchmarks/jsat/`
  - benchmark and blueprint seed material
  - use for analytics, reporting, and assessment design, not live scoring
- `data/paradigms/grammar/`
  - grammar paradigm seeds
  - use for future hinting, reteach, and teacher support
- `data/lexicon/high_frequency/`
  - high-frequency lexicon policy and seed entries
  - use for future mastery prioritization and lexicon analytics
- `data/teacher_ops/`
  - teacher/admin workflow seeds
  - use for dashboards, DDI reporting, and deployment support
- `data/foundations/incoming/`
  - raw intake drop zone
  - not the long-term versioned home

## Versioning and manifest

- The permanent seed snapshots use versioned filenames like `seed.v1`.
- `data/foundations/manifest.json` records:
  - resource name
  - layer
  - source
  - status
  - intended use
- `foundation_resources.py` is the shared loader and structural validator.
- `docs/chumash_foundations_package_seed.md`
  - preserved copy of the original incoming package README for provenance

## Promotion rules

- These resources are validated and available to code, but not wired into the
  student-facing runtime by default.
- No new standards, lexicon entries, paradigms, or teacher-ops rules should
  affect runtime behavior until a separate explicit integration pass is made.
- Review-needed or seed-only content must not be treated as active runtime
  truth automatically.
