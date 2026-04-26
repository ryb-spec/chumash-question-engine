# Dikduk Rules Engine

This folder is the first source-modeled Dikduk rules library for the Torah AI / Chumash Question Engine.

It exists to turn early Lashon Hakodesh lessons into structured rule records that future branches can use for:

- student diagnostics
- adaptive question generation
- mastery tracking
- Hebrew word and phrase analysis
- translation assessment
- tutoring explanations
- future curriculum expansion

## What Source Was Used

- Source file: `loshon 2.pdf`
- Source type: scanned Lashon Hakodesh / Dikduk workbook PDF
- Extraction method: manually modeled from visible early lesson pages
- Scope: foundational lessons only
- Status: source-modeled draft, not reviewed production curriculum

## Source Notes

- The PDF available in this branch is image-only and does not expose a direct text layer.
- This package models only rules that were clearly identified from the visible early lessons and the page-by-page lesson progression described in the source review prompt.
- Exact page numbers were not machine-extracted from the scan in this pass, so rule records stay lesson-traceable and note the scan limitation explicitly.
- No OCR output was trusted blindly for rule content in this pass.

## What Is In This Package

- `dikduk_rules_manifest.json`
  - package metadata, counts, commands, and safety notes
- `rule_groups.json`
  - the major Dikduk rule families this package covers
- `rules_loshon_foundation.jsonl`
  - one stable, searchable rule per line
- `question_templates.jsonl`
  - non-runtime question templates tied to specific rule IDs
- `student_error_patterns.jsonl`
  - machine-readable student-mistake diagnoses tied to rule IDs
- `dikduk_rule.schema.json`
  - schema documentation for rule records
- `dikduk_question_template.schema.json`
  - schema documentation for question template records
- `dikduk_error_pattern.schema.json`
  - schema documentation for error pattern records

## What The Rule Records Contain

Each rule record stores:

- a stable rule ID
- a rule group
- a skill name
- source traceability back to `loshon 2.pdf`
- student-facing wording
- a technical pattern description
- examples
- warnings and ambiguity notes
- common student errors
- linked question template IDs
- feedback templates
- mastery tags
- a difficulty level
- prerequisite and follow-up rule links
- Zekelman alignment notes

## What Question Templates Are

Question templates describe safe future ways to test a rule without wiring anything into runtime yet.

Examples include:

- identifying a marker
- translating a word
- identifying a possessive owner
- choosing the meaning of a prefix
- deciding whether a verb is past or future
- parsing a word into root, prefix, suffix, and agreement clues

## What Student Error Patterns Are

Student error patterns connect a likely wrong answer or behavior to:

- the rule or rules involved
- the likely misunderstanding
- a remediation hint
- mastery penalty tags that a future diagnostic engine could use

## How This Connects To Diagnostics

This package gives future diagnostic branches a stable way to ask:

- what exact rule a student missed
- what mistake pattern that wrong answer suggests
- what follow-up explanation should be shown
- which mastery bucket should be updated

## How This Connects To Adaptive Question Generation

Future branches can use these files to:

- select a rule group
- find all rules with a mastery tag
- choose question templates for a specific rule
- surface likely distractor patterns
- preserve ambiguity warnings instead of over-claiming certainty

## How This Connects To Mastery Tracking

The rule records include mastery tags and difficulty levels so a later branch can:

- group mistakes by rule family
- route reteach prompts
- distinguish beginner morphology from harder parsing work
- connect Dikduk rules to existing skill and standards layers

## What Is Ready Now

- source-traceable non-runtime rule data
- question template scaffolding
- student error pattern scaffolding
- a loader
- a validator
- focused tests

## What Is Not Ready Yet

- no runtime promotion
- no student-facing UI integration
- no automatic question serving from this package
- no reviewed production status
- no automatic parser that derives every rule from real pasuk data
- no human-reviewed lesson packet for the workbook source

## Validation

Run:

```powershell
python scripts/validate_dikduk_rules.py
```

## Tests

Run the focused tests:

```powershell
python -m pytest tests/test_dikduk_rules_validation.py tests/test_dikduk_rule_loader.py
```

Run the full suite:

```powershell
python -m pytest
```

## How To Add Future Lessons

When later lessons are modeled:

1. add new rule records with stable IDs
2. keep source references explicit
3. add question templates tied to those rule IDs
4. add error patterns for likely student mistakes
5. update manifest counts
6. run the validator and tests
7. keep new rules in draft/non-runtime status until reviewed

## Relation To Existing Foundations

This package does not replace `data/foundations/dikduk`.

Instead, it is a source-modeled upstream layer that future reviewed branches can use to promote carefully selected rules into the existing validated foundations package after human review.

## Why Nothing Is Production-Active Yet

This branch creates structured grammar knowledge, not reviewed runtime truth.

The records stay draft on purpose so the project can:

- preserve source limitations honestly
- avoid overgeneralizing Biblical Hebrew
- support future review and refinement
- keep student-facing behavior unchanged until a separate, tested integration pass
