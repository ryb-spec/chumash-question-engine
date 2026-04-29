# Bereishis Perek 1 Question-Eligibility Audit Report

## A. Executive Summary

This audit identifies future question-review candidates only and opens no gates. It does not generate questions, answer choices, answer keys, protected-preview inputs, reviewed-bank entries, runtime data, or student-facing content.

## B. Scope

Bereishis 1:1-1:31.

## C. Inputs Audited

- `data/source_skill_enrichment/morphology_candidates/bereishis_1_1_to_1_5_morphology_candidates.tsv` (morphology)
- `data/source_skill_enrichment/vocabulary_shoresh_candidates/bereishis_1_1_to_1_5_vocabulary_shoresh_candidates.tsv` (vocabulary_shoresh)
- `data/source_skill_enrichment/standards_candidates/bereishis_1_1_to_1_5_standards_candidates.tsv` (phrase_level_standards)
- `data/source_skill_enrichment/standards_candidates/bereishis_1_1_to_1_5_token_split_standards_candidates.tsv` (token_split_standards)
- `data/source_skill_enrichment/morphology_candidates/bereishis_1_6_to_1_13_morphology_candidates.tsv` (morphology)
- `data/source_skill_enrichment/vocabulary_shoresh_candidates/bereishis_1_6_to_1_13_vocabulary_shoresh_candidates.tsv` (vocabulary_shoresh)
- `data/source_skill_enrichment/standards_candidates/bereishis_1_6_to_1_13_standards_candidates.tsv` (phrase_level_standards)
- `data/source_skill_enrichment/standards_candidates/bereishis_1_6_to_1_13_token_split_standards_candidates.tsv` (token_split_standards)
- `data/source_skill_enrichment/morphology_candidates/bereishis_1_14_to_1_23_morphology_candidates.tsv` (morphology)
- `data/source_skill_enrichment/vocabulary_shoresh_candidates/bereishis_1_14_to_1_23_vocabulary_shoresh_candidates.tsv` (vocabulary_shoresh)
- `data/source_skill_enrichment/standards_candidates/bereishis_1_14_to_1_23_standards_candidates.tsv` (phrase_level_standards)
- `data/source_skill_enrichment/standards_candidates/bereishis_1_14_to_1_23_token_split_standards_candidates.tsv` (token_split_standards)
- `data/source_skill_enrichment/morphology_candidates/bereishis_1_24_to_1_31_morphology_candidates.tsv` (morphology)
- `data/source_skill_enrichment/vocabulary_shoresh_candidates/bereishis_1_24_to_1_31_vocabulary_shoresh_candidates.tsv` (vocabulary_shoresh)
- `data/source_skill_enrichment/standards_candidates/bereishis_1_24_to_1_31_standards_candidates.tsv` (phrase_level_standards)
- `data/source_skill_enrichment/standards_candidates/bereishis_1_24_to_1_31_token_split_standards_candidates.tsv` (token_split_standards)

## D. Overall Counts

- total enrichment candidates considered: 299
- total verified enrichment candidates considered: 164
- total audit rows created: 299

Count by eligibility recommendation:

- eligible_candidate_for_yossi_question_review: 158
- source_only: 6
- needs_follow_up: 130
- blocked_for_questions: 5

Count by proposed question family:

- basic_noun_recognition: 60
- basic_verb_form_recognition: 25
- direct_object_marker_recognition: 14
- not_recommended: 141
- shoresh_identification: 3
- vocabulary_meaning: 56

Count by risk level:

- low: 119
- medium: 114
- high: 66

## E. Eligible Candidate Summary

- vocabulary/noun: 116
- shoresh/root: 3
- direct-object marker/function word: 14
- morphology: 25
- standards token-split eligible rows are included only when verified and token-scoped.

## F. Source-Only Summary

Source-only rows are useful as context but are not clean question inputs. This includes many verified morphology rows whose wording still needs design review and phrase-level standards rows better represented by token-split rows.

## G. Needs-Follow-Up Summary

Needs-follow-up rows are grouped around verb form uncertainty, prefix/preposition uncertainty, construct/suffix uncertainty, thin evidence, context dependence, and phrase-level bundles.

## H. Blocked-For-Questions Summary

- blocked_for_questions: 5
Rows are blocked only when the audit sees high-risk conceptual or wording sensitivity.

## I. Safety Gate Summary

- no questions generated
- no answer choices generated
- no answer keys generated
- no protected-preview inputs created
- no reviewed-bank entries created
- no runtime changes
- all existing source/enrichment gates remain closed

## J. Strategic Meaning

Perek 1 enrichment now supports a realistic later review path for clean vocabulary, noun recognition, shoresh, direct-object marker, and a small set of basic morphology inputs. Wording/templates and protected-preview eligibility still require separate review.

## K. Recommended Next Step

1. Yossi reviews the eligibility audit sheet.
2. Codex applies only reviewed eligibility decisions into a separate reviewed input-candidate layer.
3. Only after that should protected-preview question generation be considered.
