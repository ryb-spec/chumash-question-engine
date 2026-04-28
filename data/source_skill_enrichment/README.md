# Source-Skill Enrichment Layer

This directory holds candidate enrichment data for verified source-to-skill maps.

The verified source-to-skill maps remain the phrase-level extraction-verified source truth. This enrichment layer is a separate, review-gated planning layer for morphology, standards, vocabulary, and shoresh candidates. It does not change source text, translation text, answer keys, runtime scope, reviewed-bank status, or question eligibility.

## Layer Boundaries

1. Source-to-skill map

   Phrase-level extraction-verified source truth. These rows record Hebrew phrases, trusted translation/context sources, source alignment, current planning classification, extraction review status, and closed safety gates.

2. Morphology enrichment

   Usually word/token-level candidate data linked back to a phrase-level source-to-skill row. Morphology candidates may propose shoresh, prefixes, suffixes, tense, person, gender, number, part of speech, and dikduk features only when supported by explicit evidence. Unclear tokens must stay blank or `needs_follow_up`.

3. Standards enrichment

   Candidate skill and Zekelman mapping data linked to verified source-to-skill rows. A proposed standard is not final until separately reviewed. Draft Zekelman crosswalks and internal skill catalogs may support a candidate, but they do not make a row question-ready.

4. Vocabulary/shoresh enrichment

   Candidate vocabulary or shoresh evidence supported by resources such as First 150 Shorashim and Keywords in Bereishis, Loshon Hakodesh/Loshon HaTorah resources, Dikduk resources, verified source-to-skill maps, and reviewed-bank examples as reference only.

5. Question eligibility

   Separate later gate. Enrichment candidates are not question approval.

6. Runtime/reviewed-bank status

   Separate later gate. Enrichment candidates are not runtime approval, reviewed-bank approval, protected-preview approval, or student-facing release.

## Directory Layout

- `morphology_candidates/`: token-level morphology candidate TSVs.
- `standards_candidates/`: source-row-level standards mapping candidate TSVs.
- `vocabulary_shoresh_candidates/`: token-level vocabulary and shoresh candidate TSVs.
- `reports/`: audit reports and Yossi-friendly enrichment review sheets.

## Linking Model

Candidate rows must link back to verified source-to-skill rows using:

- `source_map_file`
- `source_row_id`
- `ref`
- `hebrew_phrase`
- `token_index` when word-level
- `hebrew_token` when word-level
- `clean_hebrew_no_nikud`

For the pilot, `source_row_id` uses the deterministic map row label `row_###`, where `row_001` is the first data row in the source-to-skill TSV.

## Review and Safety Defaults

Allowed enrichment review statuses:

- `pending_yossi_enrichment_review`
- `yossi_enrichment_verified`
- `needs_follow_up`
- `blocked_unclear_evidence`
- `source_only`

Allowed confidence values:

- `high`
- `medium`
- `low`

Default safety statuses for every candidate:

- `question_allowed = needs_review`
- `protected_preview_allowed = false`
- `runtime_allowed = false`
- `reviewed_bank_allowed = false`

No enrichment candidate may claim question-ready, protected-preview-ready, reviewed-bank-ready, runtime-ready, or student-facing status.

## Pilot Review Status

Yossi and the review assistant audited the Bereishis 1:1-1:5 enrichment pilot. The review was applied candidate-by-candidate; no blanket enrichment verification was applied.

- Morphology candidates: 5 reviewed; 3 `yossi_enrichment_verified`; 2 `needs_follow_up`.
- Vocabulary/shoresh candidates: 6 reviewed; 3 `yossi_enrichment_verified`; 3 `needs_follow_up`, including 1 `fix_vocabulary` decision for `ברא` that remains follow-up because exact First 150 evidence was not located locally.
- Standards candidates: 6 reviewed; 1 `yossi_enrichment_verified`; 5 `needs_follow_up`.

Applied review reports:

- `reports/bereishis_1_1_to_1_5_morphology_enrichment_yossi_review_applied.md`
- `reports/bereishis_1_1_to_1_5_vocabulary_shoresh_enrichment_yossi_review_applied.md`
- `reports/bereishis_1_1_to_1_5_standards_enrichment_yossi_review_applied.md`

These applied decisions are enrichment-only. They are not question approval, protected-preview approval, reviewed-bank approval, runtime approval, or student-facing approval.

## Pilot Follow-Up Evidence Status

The first pilot review left 10 candidates unresolved before evidence strengthening:

- Morphology follow-up: 2 candidates.
- Vocabulary/shoresh follow-up: 3 candidates.
- Standards follow-up: 5 candidates.

This follow-up pass strengthened evidence links and documented exact evidence gaps, but it did not verify any unresolved candidate. The verified count remains 7 candidates, and all 10 unresolved candidates still require Yossi follow-up review before any enrichment verification can be applied.

Follow-up artifacts:

- `reports/bereishis_1_1_to_1_5_enrichment_follow_up_inventory.md`
- `reports/bereishis_1_1_to_1_5_enrichment_follow_up_yossi_review_sheet.md`
- `reports/bereishis_1_1_to_1_5_enrichment_follow_up_yossi_review_sheet.csv`

The follow-up CSV is UTF-8-BOM encoded for spreadsheet review. The Markdown sheet remains the primary human-review surface. This follow-up review is enrichment-only; it is not question approval, protected-preview approval, reviewed-bank approval, runtime approval, or student-facing approval.

## Token-Split Standards Cleanup

The bundled phrase-level standards follow-up rows for Bereishis 1:1-1:5 remain unresolved until Yossi reviews precise token-level replacements. Token-split candidates are standards-enrichment review only, not question-ready, not protected-preview-ready, not reviewed-bank-ready, not runtime-ready, and not student-facing.

Yossi has now reviewed the token-split sheet: 10 token-split standards candidates were reviewed, 7 are `yossi_enrichment_verified`, and 3 remain `needs_follow_up`. The original phrase-level standards candidates remain in place as unresolved parent rows.

Token-split standards cleanup artifacts:

- `reports/bereishis_1_1_to_1_5_token_split_standards_audit.md`
- `standards_candidates/bereishis_1_1_to_1_5_token_split_standards_candidates.tsv`
- `reports/bereishis_1_1_to_1_5_token_split_standards_yossi_review_sheet.md`
- `reports/bereishis_1_1_to_1_5_token_split_standards_yossi_review_sheet.csv`
- `reports/bereishis_1_1_to_1_5_token_split_standards_yossi_review_applied.md`

## Pilot Completion Milestone

The Bereishis 1:1-1:5 enrichment pilot is completed as a pattern, not fully resolved as a slice. Unresolved items remain follow-up only, all safety gates are closed, and no question/protected-preview/reviewed-bank/runtime approval exists.

Completion milestone report:

- `reports/bereishis_1_1_to_1_5_enrichment_pilot_completion_report.md`

Outstanding follow-up retained by design:

- `וחשך`
- `יהי`
- `שמים`
- prefixed `ל`
- original phrase-level standards candidates remain in place as unresolved parent rows until later review decisions narrow or replace them

## Bereishis 1:6-1:13 Review-Applied Slice

Bereishis 1:6-1:13 now has a controlled review-applied enrichment slice built from the approved pilot pattern. This remains enrichment review only, all gates remain closed, and no question/protected-preview/reviewed-bank/runtime approval exists.

Review-applied totals:

- verified: 14
- needs_follow_up: 18

Candidate files:

- `morphology_candidates/bereishis_1_6_to_1_13_morphology_candidates.tsv`
- `vocabulary_shoresh_candidates/bereishis_1_6_to_1_13_vocabulary_shoresh_candidates.tsv`
- `standards_candidates/bereishis_1_6_to_1_13_standards_candidates.tsv`
- `standards_candidates/bereishis_1_6_to_1_13_token_split_standards_candidates.tsv`

Yossi review sheets:

- `reports/bereishis_1_6_to_1_13_morphology_enrichment_yossi_review_sheet.md`
- `reports/bereishis_1_6_to_1_13_morphology_enrichment_yossi_review_sheet.csv`
- `reports/bereishis_1_6_to_1_13_vocabulary_shoresh_enrichment_yossi_review_sheet.md`
- `reports/bereishis_1_6_to_1_13_vocabulary_shoresh_enrichment_yossi_review_sheet.csv`
- `reports/bereishis_1_6_to_1_13_standards_enrichment_yossi_review_sheet.md`
- `reports/bereishis_1_6_to_1_13_standards_enrichment_yossi_review_sheet.csv`
- `reports/bereishis_1_6_to_1_13_token_split_standards_yossi_review_sheet.md`
- `reports/bereishis_1_6_to_1_13_token_split_standards_yossi_review_sheet.csv`

Generation report:

- `reports/bereishis_1_6_to_1_13_enrichment_candidate_generation_report.md`

Applied-review reports:

- `reports/bereishis_1_6_to_1_13_morphology_enrichment_yossi_review_applied.md`
- `reports/bereishis_1_6_to_1_13_vocabulary_shoresh_enrichment_yossi_review_applied.md`
- `reports/bereishis_1_6_to_1_13_standards_enrichment_yossi_review_applied.md`
- `reports/bereishis_1_6_to_1_13_token_split_standards_yossi_review_applied.md`
- `reports/bereishis_1_6_to_1_13_enrichment_review_summary.md`
- `reports/bereishis_1_6_to_1_13_enrichment_follow_up_inventory.md`
- `reports/bereishis_1_6_to_1_13_enrichment_mini_completion_report.md`

This is enrichment verification only. It is not question approval, protected-preview approval, reviewed-bank approval, runtime approval, or student-facing approval.

Unresolved items remain follow-up by design, all gates remain closed, and the next recommended slice is Bereishis 1:14-1:23.

## Source Priority

For morphology enrichment, prefer Dikduk review sheets/workbooks, Loshon Hakodesh/Loshon HaTorah resources, Parsha Pshat Dikduk curriculum, First 150 Shorashim and Keywords in Bereishis, General Chumash Skills Workbook, then internal skill alignment docs.

For standards enrichment, prefer Zekelman Chumash Standards, Zekelman sample assessments, internal skill catalog, runtime skill canonical alignment docs, and verified source-to-skill maps as context.

For translation context, Metsudah remains primary; Koren remains secondary noncommercial support only; Sefaria version-level metadata must stay explicit.
