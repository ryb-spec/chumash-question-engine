# Bereishis 1:1-1:5 Source-to-Skill Map Exceptions Review Packet

## A. Scope

- Map file: `data/verified_source_skill_maps/bereishis_1_1_to_1_5_source_to_skill_map.tsv`
- Scope: Bereishis 1:1-1:5
- Row count: 23 phrase-level rows
- Current status: proof-of-consolidation map only
- Extraction review status: `pending_yossi_extraction_accuracy_pass`

This is extraction-accuracy and mapping confirmation for trusted source-derived content. It is not generated-question review and not runtime approval.

## B. Source Files Used

- `data/curriculum_extraction/normalized/linear_chumash_bereishis_1_1_to_1_5_pasuk_segments.seed.jsonl`
- `data/curriculum_extraction/raw_sources/batch_001/linear_chumash_bereishis_1_1_to_1_5_cleaned.md`
- `data/source_texts/translations/sefaria/bereishis_english_metsudah.jsonl`
- `data/source_texts/translations/sefaria/bereishis_english_koren.jsonl`
- `data/source_texts/bereishis_hebrew_menukad_taamim.tsv`

## C. What Yossi Is Confirming

Yossi is confirming:

- the Linear Chumash phrase extraction matches the trusted source
- Hebrew phrase text is faithful enough for source-derived planning
- Metsudah verse translation context was joined to the correct pasuk
- Koren secondary noncommercial context was joined to the correct pasuk
- `phrase_translation` / `translation_context` classification is reasonable
- uncertainty fields correctly identify what is not yet safe to use

## D. What Yossi Is Not Approving

This packet does not approve:

- generated questions
- answer choices
- answer keys
- protected preview generation
- reviewed-bank promotion
- runtime activation
- student-facing use
- commercial use of Koren

## E. Representative Clean Rows

| Ref | Hebrew phrase | Alternate / Linear translation | Skill | Safety |
|---|---|---|---|---|
| Bereishis 1:1 | בראשית | in the beginning | phrase_translation | non-runtime, not question-ready |
| Bereishis 1:3 | ויאמר אלקים | and Hashem said | phrase_translation | non-runtime, not question-ready |
| Bereishis 1:5 | יום אחד | one day | phrase_translation | non-runtime, not question-ready |

## F. Rows With Uncertainty

All rows currently carry an uncertainty reason because morphology, Zekelman Standard mapping, difficulty, and question-type eligibility are not safely consolidated at row level yet.

## G. Missing Translations

No proof-map row is missing its Linear phrase translation, Metsudah verse translation context, or Koren secondary verse context.

## H. Ambiguous Shorashim

Shoresh is intentionally blank in this proof map. The Linear phrase rows are phrase-translation rows, not verified word-parse rows.

## I. Prefix / Suffix / Tense Uncertainty

Prefix, suffix, tense, part-of-speech, and dikduk-feature fields are intentionally blank. The repo contains some morphology ingredients in other files, but they are not safely joined to these Bereishis 1:1-1:5 phrase rows yet.

## J. Skill Mapping Questions

Current mapping:

- `skill_primary`: `phrase_translation`
- `skill_secondary`: `translation_context`
- `skill_id`: `phrase_translation`

Question for Yossi/project lead: Is this the correct planning classification for phrase-level Linear Chumash rows before any future protected preview work?

## K. Standards Mapping Questions

`zekelman_standard` is blank for all rows. The Zekelman crosswalks support standards-level skill families, but the repo does not yet have safe row-level Zekelman mapping for these phrase rows.

## L. Rows Recommended As Source-Only

All rows are recommended as source-only until Yossi extraction-accuracy confirmation and a separate future question/protected-preview gate.

## M. Safety Status Summary

- Runtime: blocked
- Question generation: blocked
- Protected preview: blocked
- Reviewed bank: blocked
- Student-facing use: blocked
- Koren commercial use: blocked
- Review status: `pending_yossi_extraction_accuracy_pass`

## N. Recommended Next Action

Yossi should review this as a small proof-of-consolidation map. If the joins and classifications are correct, the next task should build a deterministic consolidation script for additional trusted slices while keeping runtime and question gates closed.
