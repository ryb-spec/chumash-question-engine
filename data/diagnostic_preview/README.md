# Diagnostic Preview

This folder holds a non-runtime diagnostic preview layer for Chumash assessment design.

It exists to prove that the repo's new source layers can generate reviewable student questions before anything becomes student-facing. The preview stays offline, editable, and fully human-review-first.

## What This Uses

- Canonical Hebrew Bereishis source TSV
- Sefaria Bereishis English translations for Koren and Metsudah
- Dikduk rule records
- Dikduk question templates
- Dikduk student error patterns

## Why This Is Not Runtime

Nothing in this folder is active in the live quiz engine.

Every config, blueprint, question, and report in this package must stay:

- `preview_only`
- `not_runtime_active`
- `not_production_ready`

The English translation layer also still requires human license review, so every translation-backed preview item keeps the warning:

- `source_preview_only_license_review_required`

## Why Bereishis 1:1-2:3

This pilot range is narrow but strong for a first preview:

- repeated core creation vocabulary
- clear noun and verb targets
- article and conjunction prefixes
- plural forms
- direct-object marker usage
- simple clause-order patterns
- early verb-analysis opportunities

## Diagnostic Lanes

- `translation`
  Source-backed word and phrase meaning questions
- `dikduk`
  Prefix, marker, plurality, agreement, and word-order questions
- `word_analysis`
  Shoresh and added-letter decomposition questions
- `translation_comparison`
  Preview-only acceptance of source-backed English variants without asking students to compare translations directly
- `error_diagnosis`
  Likely mistake diagnosis tied to mastery tags and Dikduk error patterns

## What Mastery Tags And Rule IDs Do

Mastery tags show which learning bucket a question is trying to measure.

Rule IDs trace the question back to a specific Dikduk rule record, so later branches can connect diagnostics, tutoring feedback, and mastery tracking without inventing new grammar categories on the fly.

## Generated Files

- `configs/`
  The preview config and output paths
- `blueprints/`
  One machine-readable assessable blueprint per preview item
- `generated_questions/`
  One machine-readable preview question per blueprint
- `reports/`
  The manual review packet and summary reports

## How To Regenerate

```powershell
python scripts/generate_diagnostic_preview.py --config data/diagnostic_preview/configs/bereishis_1_1_to_2_3_dikduk_translation_preview.json
```

## How To Validate

```powershell
python scripts/validate_diagnostic_preview.py --config data/diagnostic_preview/configs/bereishis_1_1_to_2_3_dikduk_translation_preview.json
python -m pytest tests/test_diagnostic_preview_generation.py tests/test_diagnostic_preview_validation.py -q
```

## How A Human Should Review It

Open:

- `reports/bereishis_1_1_to_2_3_manual_review_packet.md`

Reviewers should check:

- source fidelity to the Hebrew pasuk
- whether the Koren and Metsudah English evidence supports the accepted answers
- whether the question wording is classroom-usable
- whether the Dikduk rule linkage is correct
- whether the distractors reveal real student mistakes instead of random wrong answers

## What Is Ready Now

- preview config
- machine-readable blueprints
- machine-readable preview questions
- manual review packet
- summary reports
- generator
- validator
- focused tests

## What Is Still Not Ready

- runtime activation
- reviewed-bank promotion
- production approval
- translation license signoff
- human pedagogic review of the generated items

## Next Branch

The next strongest branch should be a human-review or diagnostic-integration branch that:

- reviews and edits this preview packet
- locks a first approved non-runtime diagnostic subset
- decides which preview question families are safe enough to connect to future mastery and tutoring flows
