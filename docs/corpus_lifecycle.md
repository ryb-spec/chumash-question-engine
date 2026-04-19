# Corpus Lifecycle

The local corpus moves through these states:

1. `source`
   Local source text on disk. Source text may extend past the active runtime.

2. `staged`
   Parsed artifacts built from source for evaluation only. Staged bundles do not
   change the supported runtime.

3. `review_needed`
   A staged bundle with enough structural/question support to merit review, but
   not enough approval to become active automatically.

4. `active_candidate`
   A staged bundle that passes the current readiness gates. It is eligible for
   explicit promotion, but is still not active until promotion is applied.

5. `active`
   The blessed local runtime layer used by `streamlit_app.py`.

## Promotion Rules

- The active runtime stays fixed until an explicit promotion step updates the
  manifest.
- `review_needed` content is never auto-promoted.
- Only `active_candidate` chunks may be promoted into the active runtime.
- Runtime remains local-only. Source, staged, reviews, and promotion decisions
  all use local repo data.

## Current Repo Shape

- `data/source/` contains the local source files.
- `data/` root parsed artifacts are the active runtime layer.
- `data/corpus_manifest.json` records:
  - source corpora
  - parsed corpora
  - runtime scopes

Manifest status values, readiness metrics, promotion helpers, and tests should
all use the same canonical lifecycle vocabulary above.
