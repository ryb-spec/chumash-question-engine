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

## Bereishis 1:14-1:23 Review-Applied Slice

Bereishis 1:14-1:23 now has a controlled review-applied enrichment slice built from the approved pilot and review-applied patterns. This slice remains enrichment verification only, all gates remain closed, and no question/protected-preview/reviewed-bank/runtime approval exists.

Candidate counts:

- morphology: 25
- vocabulary_shoresh: 21
- phrase-level standards: 13
- token-split standards: 45
- total candidates: 104
- verified: 53
- needs_follow_up: 51

Candidate files:

- `morphology_candidates/bereishis_1_14_to_1_23_morphology_candidates.tsv`
- `vocabulary_shoresh_candidates/bereishis_1_14_to_1_23_vocabulary_shoresh_candidates.tsv`
- `standards_candidates/bereishis_1_14_to_1_23_standards_candidates.tsv`
- `standards_candidates/bereishis_1_14_to_1_23_token_split_standards_candidates.tsv`

Yossi review sheets:

- `reports/bereishis_1_14_to_1_23_morphology_enrichment_yossi_review_sheet.md`
- `reports/bereishis_1_14_to_1_23_morphology_enrichment_yossi_review_sheet.csv`
- `reports/bereishis_1_14_to_1_23_vocabulary_shoresh_enrichment_yossi_review_sheet.md`
- `reports/bereishis_1_14_to_1_23_vocabulary_shoresh_enrichment_yossi_review_sheet.csv`
- `reports/bereishis_1_14_to_1_23_standards_enrichment_yossi_review_sheet.md`
- `reports/bereishis_1_14_to_1_23_standards_enrichment_yossi_review_sheet.csv`
- `reports/bereishis_1_14_to_1_23_token_split_standards_yossi_review_sheet.md`
- `reports/bereishis_1_14_to_1_23_token_split_standards_yossi_review_sheet.csv`

Reports:

- `reports/bereishis_1_14_to_1_23_enrichment_candidate_audit.md`
- `reports/bereishis_1_14_to_1_23_enrichment_candidate_generation_report.md`
- `reports/bereishis_1_14_to_1_23_morphology_enrichment_yossi_review_applied.md`
- `reports/bereishis_1_14_to_1_23_vocabulary_shoresh_enrichment_yossi_review_applied.md`
- `reports/bereishis_1_14_to_1_23_standards_enrichment_yossi_review_applied.md`
- `reports/bereishis_1_14_to_1_23_token_split_standards_yossi_review_applied.md`
- `reports/bereishis_1_14_to_1_23_enrichment_review_summary.md`
- `reports/bereishis_1_14_to_1_23_enrichment_mini_completion_report.md`

Unresolved items remain follow-up by design and all gates remain closed across the slice.

Next recommended slice: Bereishis 1:24-1:31, using the same review-only pattern after this 1:14-1:23 milestone is checkpointed.

## Bereishis 1:24-1:31 Review-Applied Slice

Bereishis 1:24-1:31 review decisions are now applied. This completes candidate coverage for Bereishis Perek 1 and completes Perek 1 enrichment review-application coverage only after this review-application step; it still does not approve questions or any later gate.

Candidate counts:

- morphology: 26
- vocabulary_shoresh: 40
- phrase-level standards: 14
- token-split standards: 56
- total candidates: 136
- verified: 83
- needs_follow_up: 53

Candidate files:

- `morphology_candidates/bereishis_1_24_to_1_31_morphology_candidates.tsv`
- `vocabulary_shoresh_candidates/bereishis_1_24_to_1_31_vocabulary_shoresh_candidates.tsv`
- `standards_candidates/bereishis_1_24_to_1_31_standards_candidates.tsv`
- `standards_candidates/bereishis_1_24_to_1_31_token_split_standards_candidates.tsv`

Yossi review sheets:

- `reports/bereishis_1_24_to_1_31_morphology_enrichment_yossi_review_sheet.md`
- `reports/bereishis_1_24_to_1_31_morphology_enrichment_yossi_review_sheet.csv`
- `reports/bereishis_1_24_to_1_31_vocabulary_shoresh_enrichment_yossi_review_sheet.md`
- `reports/bereishis_1_24_to_1_31_vocabulary_shoresh_enrichment_yossi_review_sheet.csv`
- `reports/bereishis_1_24_to_1_31_standards_enrichment_yossi_review_sheet.md`
- `reports/bereishis_1_24_to_1_31_standards_enrichment_yossi_review_sheet.csv`
- `reports/bereishis_1_24_to_1_31_token_split_standards_yossi_review_sheet.md`
- `reports/bereishis_1_24_to_1_31_token_split_standards_yossi_review_sheet.csv`

Reports:

- `reports/bereishis_1_24_to_1_31_enrichment_candidate_audit.md`
- `reports/bereishis_1_24_to_1_31_enrichment_candidate_generation_report.md`
- `reports/bereishis_1_24_to_1_31_morphology_enrichment_yossi_review_applied.md`
- `reports/bereishis_1_24_to_1_31_vocabulary_shoresh_enrichment_yossi_review_applied.md`
- `reports/bereishis_1_24_to_1_31_standards_enrichment_yossi_review_applied.md`
- `reports/bereishis_1_24_to_1_31_token_split_standards_yossi_review_applied.md`
- `reports/bereishis_1_24_to_1_31_enrichment_review_summary.md`

This is enrichment review only. It is not question approval, protected-preview approval, reviewed-bank approval, runtime approval, or student-facing approval.

All gates remain closed across this slice:

- `question_allowed = needs_review`
- `protected_preview_allowed = false`
- `reviewed_bank_allowed = false`
- `runtime_allowed = false`

This is enrichment verification only. It is not question approval, protected-preview approval, reviewed-bank approval, runtime approval, or student-facing approval.

Next required action: create the Bereishis Perek 1 enrichment review-application coverage report before opening the next slice.

## Bereishis Perek 1 Enrichment Review-Application Coverage

Coverage report:

- `reports/bereishis_perek_1_enrichment_review_application_coverage_report.md`

Perek 1 enrichment review-application coverage status:

- coverage exists across Bereishis 1:1-1:31
- unresolved items remain follow-up by design
- all safety gates remain closed

Recommended next step:

- checkpoint this Perek 1 enrichment milestone before either expanding enrichment to Perek 2 or running a controlled Perek 1 question-eligibility audit

## Source Priority

For morphology enrichment, prefer Dikduk review sheets/workbooks, Loshon Hakodesh/Loshon HaTorah resources, Parsha Pshat Dikduk curriculum, First 150 Shorashim and Keywords in Bereishis, General Chumash Skills Workbook, then internal skill alignment docs.

For standards enrichment, prefer Zekelman Chumash Standards, Zekelman sample assessments, internal skill catalog, runtime skill canonical alignment docs, and verified source-to-skill maps as context.

For translation context, Metsudah remains primary; Koren remains secondary noncommercial support only; Sefaria version-level metadata must stay explicit.

## Bereishis Perek 2 Gate 1 Enrichment Readiness

Bereishis Perek 2 now has Gate 1 review-only enrichment candidates generated from verified source-to-skill rows. These candidates are pending Yossi enrichment review and are not question approval, protected-preview approval, reviewed-bank approval, runtime approval, or student-facing approval.

Candidate files:

- `morphology_candidates/bereishis_perek_2_morphology_candidates.tsv`
- `vocabulary_shoresh_candidates/bereishis_perek_2_vocabulary_shoresh_candidates.tsv`
- `standards_candidates/bereishis_perek_2_standards_candidates.tsv`
- `standards_candidates/bereishis_perek_2_token_split_standards_candidates.tsv`

Review sheets:

- `reports/bereishis_perek_2_morphology_enrichment_yossi_review_sheet.md`
- `reports/bereishis_perek_2_morphology_enrichment_yossi_review_sheet.csv`
- `reports/bereishis_perek_2_vocabulary_shoresh_enrichment_yossi_review_sheet.md`
- `reports/bereishis_perek_2_vocabulary_shoresh_enrichment_yossi_review_sheet.csv`
- `reports/bereishis_perek_2_standards_enrichment_yossi_review_sheet.md`
- `reports/bereishis_perek_2_standards_enrichment_yossi_review_sheet.csv`
- `reports/bereishis_perek_2_token_split_standards_yossi_review_sheet.md`
- `reports/bereishis_perek_2_token_split_standards_yossi_review_sheet.csv`

Gate 1 summary:

- `data/pipeline_rounds/reports/bereishis_perek_2_gate_1_source_enrichment_eligibility_report.md`

All safety gates remain closed. Question eligibility and input-candidate planning remain blocked until Yossi applies Perek 2 enrichment review decisions.

## Bereishis Perek 2 Compressed Enrichment Review

The raw Bereishis Perek 2 enrichment review surface has been compressed from 1,083 raw candidates into review groups for a practical Yossi first pass. This compression does not apply Yossi decisions and does not verify any raw candidate.

Compressed review artifacts:

- `reports/bereishis_perek_2_enrichment_review_compression_audit.md`
- `reports/bereishis_perek_2_enrichment_compressed_yossi_review_packet.md`
- `reports/bereishis_perek_2_enrichment_compressed_yossi_review_sheet.csv`
- `reports/bereishis_perek_2_enrichment_raw_to_compressed_crosswalk.tsv`
- `reports/bereishis_perek_2_enrichment_compressed_review_summary.md`

Raw Perek 2 enrichment candidates outside the later clean-group decision crosswalk remain review-only. Clean-group decisions have been applied separately for enrichment mapping only, and all gates remain closed:

- `question_allowed = needs_review`
- `protected_preview_allowed = false`
- `reviewed_bank_allowed = false`
- `runtime_allowed = false`

## Bereishis Perek 2 Clean-Group Evidence Strengthening

The clean-group evidence packet focuses only on clean vocabulary/noun groups, token-split clean noun standards, and clean shoresh groups from the compressed Perek 2 enrichment review layer.

Clean-group review artifacts:

- `reports/bereishis_perek_2_clean_group_evidence_inventory.md`
- `reports/bereishis_perek_2_clean_group_yossi_review_packet.md`
- `reports/bereishis_perek_2_clean_group_yossi_review_sheet.csv`
- `reports/bereishis_perek_2_clean_group_raw_crosswalk.tsv`
- `reports/bereishis_perek_2_clean_group_evidence_strengthening_summary.md`

Clean-group Yossi decisions have now been applied separately for enrichment mapping only. Raw Perek 2 enrichment candidates outside that crosswalk remain review-only, and all question/protected-preview/reviewed-bank/runtime/student-facing gates remain closed.

## Bereishis Perek 2 Clean-Group Review Applied

Yossi's clean-group enrichment decisions have been applied through the clean-group raw crosswalk.

- [clean-group Yossi review applied report](reports/bereishis_perek_2_clean_group_yossi_review_applied.md)
- verified: 31 token-split clean noun standards groups / 91 raw candidates
- needs_follow_up: 38 clean vocabulary/noun and clean shoresh groups / 100 raw candidates

This is enrichment verification only. No question/protected-preview/reviewed-bank/runtime/student-facing gates were opened.

## Bereishis Perek 2 Gate 1 Enrichment-Decision Status

Perek 2 clean-group decisions have been applied for enrichment mapping only, and Gate 2 has not started.

- Gate 1 enrichment-decision status report: `data/pipeline_rounds/reports/bereishis_perek_2_gate_1_enrichment_decision_status_report.md`
- Gate 2 candidate-pool summary: `data/pipeline_rounds/reports/bereishis_perek_2_gate_2_candidate_pool_summary.md`
- verified subset: 31 token-split clean noun standards groups / 91 raw token-split standards candidates
- follow-up subset: 38 clean vocabulary/noun and clean shoresh groups / 100 raw vocabulary/shoresh candidates
- constrained Gate 2 may proceed only from verified token-split clean noun standards rows
- follow-up vocabulary/noun groups, follow-up shoresh groups, morphology, verb forms, prefix/preposition, function-word rows, direct-object marker rows, phrase-level standards, context-heavy rows, and high-risk rows remain excluded from Gate 2 for now
- no Gate 2 batch file exists
- all raw Perek 2 enrichment candidates remain safety-gated with question/protected-preview/reviewed-bank/runtime/student-facing gates closed

## Bereishis Perek 2 Constrained Gate 2 Proposal

A constrained Gate 2 input-planning proposal has been created from verified token-split clean noun standards rows only.

- Gate 2 proposal TSV: `data/gate_2_input_planning/bereishis_perek_2_gate_2_input_planning_proposal.tsv`
- selected rows: 20
- source pool: 91 verified token-split clean noun standards raw candidates
- no follow-up vocabulary/noun rows used
- no follow-up shoresh rows used
- no morphology, verb-form, prefix/preposition, function-word, direct-object-marker, phrase-level parent, context-heavy, or high-risk rows used
- all gates remain closed
- no questions, answer choices, answer keys, distractors, controlled drafts, protected-preview content, reviewed-bank entries, runtime data, or student-facing content were created
