# Chumash system foundations package

This package translates the uploaded standards/curriculum files into system-ready seed artifacts.

## Files
- `canonical_skill_crosswalk_seed.json`
  - Canonical skill ontology linking Zekelman, JSAT, L'havin, and current engine skills.
- `canonical_skill_crosswalk_seed.csv`
  - Spreadsheet-friendly view of the skill crosswalk.
- `assessment_blueprint_seed.json`
  - Benchmark-informed blueprint for section weights, item archetypes, and DDI timing.
- `grammar_paradigms_seed.json`
  - Pre-teach / rescue tables for pronouns and model verb paradigms.
- `high_frequency_lexicon_seed.json`
  - High-frequency Bereishis lexicon policy plus starter entries and tiering rules.
- `teacher_ops_workflow_seed.json`
  - Teacher/admin workflow based on the Deployment Guide.

## How to use these
1. Adopt `canonical_skill_crosswalk_seed.json` as the first pass of `skill_catalog.json`.
2. Normalize your runtime skill labels against the canonical ids.
3. Use `assessment_blueprint_seed.json` to define question-family balance and interim assessment reports.
4. Use `grammar_paradigms_seed.json` to power hint panels, pre-teach playlists, and rescue cards.
5. Use `high_frequency_lexicon_seed.json` to create a mastered-vocabulary priority queue.
6. Use `teacher_ops_workflow_seed.json` to shape dashboards and review cycles, not student runtime.

## Layering
- Canonical truth: Zekelman + L'havin
- Benchmark / assessment: JSAT
- Teaching scaffolds: poster paradigms
- Teacher operations: Deployment Guide

## Important
These are seed artifacts, not final locked schemas.
They are designed to reduce drift and give the repo a clean source-of-truth starting point.
