# Bereishis Perek 2 Gate 1 Source/Enrichment/Eligibility Report

This Gate 1 report covers Bereishis 2:1-2:25. It is source/enrichment/eligibility readiness only. It does not generate questions, answer choices, answer keys, distractors, controlled drafts, protected-preview content, reviewed-bank entries, runtime data, or student-facing content.

## Source-to-skill readiness

- Source readiness audit: `data/pipeline_rounds/reports/bereishis_perek_2_gate_1_source_readiness_audit.md`
- Source-to-skill rows checked: 99
- All rows are `yossi_extraction_verified`: yes
- Safety gates remain closed: yes

## Enrichment candidate counts

| candidate type | rows | path |
| --- | ---: | --- |
| morphology | 328 | `data/source_skill_enrichment/morphology_candidates/bereishis_perek_2_morphology_candidates.tsv` |
| vocabulary/shoresh | 328 | `data/source_skill_enrichment/vocabulary_shoresh_candidates/bereishis_perek_2_vocabulary_shoresh_candidates.tsv` |
| phrase-level standards | 99 | `data/source_skill_enrichment/standards_candidates/bereishis_perek_2_standards_candidates.tsv` |
| token-split standards | 328 | `data/source_skill_enrichment/standards_candidates/bereishis_perek_2_token_split_standards_candidates.tsv` |

All candidates are review-only with `enrichment_review_status = pending_yossi_enrichment_review`, `question_allowed = needs_review`, `protected_preview_allowed = false`, `reviewed_bank_allowed = false`, and `runtime_allowed = false`.

## Review sheet paths

- `data/source_skill_enrichment/reports/bereishis_perek_2_morphology_enrichment_yossi_review_sheet.md`
- `data/source_skill_enrichment/reports/bereishis_perek_2_morphology_enrichment_yossi_review_sheet.csv`
- `data/source_skill_enrichment/reports/bereishis_perek_2_vocabulary_shoresh_enrichment_yossi_review_sheet.md`
- `data/source_skill_enrichment/reports/bereishis_perek_2_vocabulary_shoresh_enrichment_yossi_review_sheet.csv`
- `data/source_skill_enrichment/reports/bereishis_perek_2_standards_enrichment_yossi_review_sheet.md`
- `data/source_skill_enrichment/reports/bereishis_perek_2_standards_enrichment_yossi_review_sheet.csv`
- `data/source_skill_enrichment/reports/bereishis_perek_2_token_split_standards_yossi_review_sheet.md`
- `data/source_skill_enrichment/reports/bereishis_perek_2_token_split_standards_yossi_review_sheet.csv`

## Unresolved/follow-up themes

- Morphology candidates are intentionally conservative and require Yossi review before any morphology claim is verified.
- Vocabulary/shoresh candidates do not supply isolated answer-key meanings in this task.
- Phrase-level standards are copied from verified source-to-skill rows but remain pending enrichment review.
- Token-split standards require Yossi confirmation when phrase-level standards are broad.
- Verb-form question lanes remain deferred under the Round 2 contract.

## Allowed and deferred families

- Allowed planning families after later eligibility review: `vocabulary_meaning`, `basic_noun_recognition`, `direct_object_marker_recognition`, `shoresh_identification`.
- Deferred family: `basic_verb_form_recognition`.

## Stop conditions

- Stop if any source-to-skill row is unverified.
- Stop if unresolved enrichment rows are used as approved inputs.
- Stop if verb-form rows are included without approved morphology-question policy.
- Stop if Hebrew corruption appears.
- Stop if protected-preview, reviewed-bank, runtime, or student-facing gates open accidentally.

## What is ready for Yossi review

The four Perek 2 enrichment review sheets are ready for Yossi review.

## What is not ready

Question-eligibility decisions and approved input-candidate planning are not ready until Yossi applies enrichment decisions. Gate 2 should not start from these pending candidates.

## Next gate recommendation

Apply Yossi enrichment review decisions for Perek 2, then run a Perek 2 question-eligibility audit before Gate 2 input planning.
