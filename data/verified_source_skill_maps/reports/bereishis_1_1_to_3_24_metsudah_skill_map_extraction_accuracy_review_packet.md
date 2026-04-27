# Bereishis 1:1-3:24 Metsudah Source-to-Skill Map Extraction Accuracy Review Packet

## A. Source and Scope

This packet reviews the first seed slice of the canonical source-to-skill map:

- Map file: `data/verified_source_skill_maps/bereishis_1_1_to_3_24_metsudah_skill_map.tsv`
- Target scope: Bereishis 1:1-3:24
- Populated seed slice: Bereishis 1:1-1:5
- Primary translation source: Metsudah Chumash, Metsudah Publications, 2009
- Primary source license: CC-BY
- Secondary comparison source: The Koren Jerusalem Bible
- Secondary source license: CC-BY-NC
- Current review status: `pending_yossi_extraction_accuracy_pass`

This is extraction-accuracy confirmation for trusted source-derived content. It is not generated-question review and not runtime approval.

## B. What Yossi Is Confirming

Please confirm only the accuracy of the extracted/source-derived map:

- The Hebrew source text matches the canonical source reference.
- The Metsudah translation was copied/extracted accurately.
- The Koren comparison text, where included, was copied/extracted accurately and remains secondary noncommercial support only.
- The source license and attribution fields are accurate.
- The skill classification is reasonable for future planning.
- Any standards mapping, if later added, is accurate.
- Any uncertainty rows are correctly flagged.
- Any row that should stay blocked from future protected preview is clearly noted.

## C. What Yossi Is Not Being Asked To Approve

This packet does not ask Yossi to approve:

- generated questions
- answer choices
- answer keys
- protected preview generation
- reviewed-bank promotion
- runtime activation
- student-facing use
- commercial use of Koren
- any new educational claim beyond the source-derived map fields

## D. Clean Representative Samples

The seed map contains five verse-level phrase rows from Bereishis 1:1-1:5. Each row is intentionally conservative:

- `question_allowed`: `no`
- `runtime_allowed`: `false`
- `protected_preview_allowed`: `false`
- `reviewed_bank_allowed`: `false`
- `extraction_review_status`: `pending_yossi_extraction_accuracy_pass`

Representative rows for spot-checking:

| Ref | Primary source | Secondary support | Current safety status |
|---|---|---|---|
| Bereishis 1:1 | Metsudah CC-BY | Koren CC-BY-NC | non-runtime, not question-ready |
| Bereishis 1:2 | Metsudah CC-BY | Koren CC-BY-NC | non-runtime, not question-ready |
| Bereishis 1:3 | Metsudah CC-BY | Koren CC-BY-NC | non-runtime, not question-ready |

## E. Unclear / Exception Rows

All current rows are conservative seed rows. They should be checked for:

- whether verse-level phrase mapping is acceptable as the first source-to-skill map layer
- whether any row should be split into smaller word/phrase units in a future map
- whether any row should be blocked from future protected preview planning

## F. Missing Data Rows

The seed map intentionally leaves these fields blank until future review/mapping work:

- `zekelman_standard`
- `difficulty_level`

Rows with blank standards/difficulty fields include `uncertainty_reason` so the omission is explicit and validator-visible.

## G. Ambiguous Skill Mapping Rows

Current rows use:

- `skill_primary`: `translation_context`
- `skill_secondary`: `pasuk_comprehension`

This is a planning classification only. If Yossi wants a narrower skill label for verse-level translation rows, record that in review notes before any downstream preview work.

## H. Possible Translation Ambiguities

This packet does not resolve translation disputes. It asks whether the Metsudah and Koren texts were extracted faithfully from their source records.

Koren remains secondary noncommercial support only. It is not commercially cleared by this packet.

## I. Safety Status Summary

- Runtime: blocked
- Question generation: blocked
- Protected preview: blocked
- Reviewed bank: blocked
- Student-facing use: blocked
- Metsudah attribution: required
- Koren attribution: required
- Koren commercial use: blocked without direct written permission
- Current review status: `pending_yossi_extraction_accuracy_pass`

## J. Recommended Next Action

Yossi should complete an exceptions-only extraction-accuracy pass:

- confirm clean rows are accurately extracted
- note any source/translation/skill mapping corrections
- identify rows that should remain blocked
- approve no question generation, runtime activation, reviewed-bank promotion, or student-facing use from this packet alone
