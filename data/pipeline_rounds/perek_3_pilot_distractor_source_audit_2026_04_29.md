# Perek 3 Pilot Distractor and Source Remediation Audit - 2026-04-29

## Purpose

This audit records the remaining Perek 3 pilot issues after the wording-only remediation batch. It is evidence documentation plus narrow remediation only.

This audit does not activate Perek 4, does not widen active runtime scope, does not promote any item to reviewed-bank/runtime status, does not invent teacher decisions, and does not change source truth.

## Evidence reviewed

- `data/pipeline_rounds/perek_3_fresh_pilot_observation_summary_2026_04_29.md`
- `data/pipeline_rounds/perek_3_fresh_pilot_observation_summary_2026_04_29.json`
- `data/gate_2_protected_preview_packets/reports/bereishis_perek_3_limited_post_preview_observation_intake.md`
- `data/pipeline_rounds/perek_3_pilot_remediation_plan_2026_04_29.md`
- `data/pipeline_rounds/perek_3_pilot_remediation_plan_2026_04_29.json`
- `data/pipeline_rounds/perek_3_pilot_remediation_sequence_2026_04_29.md`
- `data/pipeline_rounds/perek_3_pilot_teacher_decision_checklist_2026_04_29.md`
- `data/pipeline_rounds/perek_3_pilot_wording_clarity_fix_report_2026_04_29.md`
- `docs/review/question_quality_rubric.md`
- `data/validation/question_quality_risk_summary.md`
- `data/validation/curriculum_quality_check_summary.md`
- `data/validation/protected_preview_source_lineage_matrix.md`
- `data/gate_2_protected_preview_candidates/reports/bereishis_perek_3_candidate_status_index.md`
- `data/active_scope_reviewed_questions.json`
- `data/active_scope_gold_annotations.json`
- `data/active_scope_overrides.json`
- `data/word_bank.json`
- `data/translation_reviews.json`
- `engine/flow_builder.py` inspected for context only
- `runtime/question_flow.py` inspected for context only

## Summary of outcomes

| Issue | Classification | Located confidently | Repair applied in this task | Follow-up still required | Re-test required |
|---|---|---:|---:|---:|---:|
| `דֶּרֶךְ` translation distractors | fixed_now | yes | yes | no for this exact distractor row | yes |
| `אֲרוּרָה` translation distractors | fixed_now | yes | yes | no for this exact distractor row | yes |
| Perek 3 `phrase_translation` distractor quality | needs_phrase_distractor_audit | yes for sampled rows | no broad repair | yes | yes |
| `אָשִׁית` / `שית` shoresh question | needs_source_followup | yes | no source-truth change | yes | yes after teacher/source decision |

## Issue details

### DS-001: `דֶּרֶךְ` translation distractors

- Evidence: Student 3 export/session issue from 2026-04-29 reported that `What does דֶּרֶךְ mean?` had bad distractors.
- Located row: `data/active_scope_reviewed_questions.json`, id `8233e19cc806`, `pasuk_id=bereishis_3_24`, `question_type=translation`.
- Current correct answer before repair: `way`.
- Current stored distractors before repair: `Eve`, `Eden`, `all`.
- Why suspicious: these are a person/name, a place/name, and a quantifier. They are not useful meaning-level distractors for an isolated vocabulary item and can reward elimination instead of word knowledge.
- Repair applied: replaced the three weak choices with existing Perek 3 vocabulary-style distractors: `heel`, `children`, `naked`; preserved correct answer `way`.
- Repair type: narrow data-level distractor repair.
- Runtime/source impact: no source truth changed, no question-selection logic changed, no distractor-generation logic changed.
- Classification: `fixed_now`.
- Re-test: verify the row no longer contains `Eve`, `Eden`, or `all` and that `way` remains the correct answer.

### DS-002: `אֲרוּרָה` translation distractors

- Evidence: Student 1 question 5 and Student 2 question 5 flagged `אֲרוּרָה`; Student 1 selected `Eve`, and the teacher note says the item had bad distractors.
- Located row: `data/active_scope_reviewed_questions.json`, id `275167d3acbf`, `pasuk_id=bereishis_3_17`, `question_type=translation`.
- Current correct answer before repair: `cursed`.
- Current stored distractors before repair: `Eden`, `Eve`, `all`.
- Why suspicious: these are a place/name, a person/name, and a quantifier. They are weak distractors for the meaning `cursed` and likely contributed to student confusion or unhelpful elimination.
- Repair applied: replaced the three weak choices with existing Perek 3 vocabulary-style distractors: `naked`, `living`, `heel`; preserved correct answer `cursed`.
- Repair type: narrow data-level distractor repair.
- Runtime/source impact: no source truth changed, no question-selection logic changed, no distractor-generation logic changed.
- Classification: `fixed_now`.
- Re-test: verify the row no longer contains `Eve`, `Eden`, or `all` and that `cursed` remains the correct answer.

### DS-003: Perek 3 `phrase_translation` distractor quality

- Evidence: teacher note from Student 1: most phrase questions seemed to have bad distractors. Fresh pilot summary listed phrase questions at Bereishis 3:10, 3:13, and 3:20; generated/source inspection also reviewed Bereishis 3:15, 3:17, and 3:24 as nearby Perek 3 phrase examples.
- Located rows: active reviewed-bank phrase_translation rows for Bereishis 3:10, 3:13, 3:15, 3:17, 3:20, and 3:24.
- Current pattern: answer choices are usually other full phrase translations from Perek 3.
- Why suspicious: this can be acceptable when phrases are similar enough to require comprehension, but some choices are so contextually different that students can eliminate them by story knowledge or phrase length rather than by reading the Hebrew phrase.
- Repair applied: no broad repair in this task.
- Reason no broad repair was applied: the pilot log did not preserve exact distractor content for every served phrase question, and a phrase-distractor rule change would be broader than the evidence supports.
- Classification: `needs_phrase_distractor_audit`.
- Follow-up: teacher/source review should decide which phrase distractors are acceptable, which need replacement, and whether any phrase_translation rows should be suppressed until reviewed.

### DS-004: `אָשִׁית` / `שית` shoresh source follow-up

- Evidence: Student 3 questioned whether `שית` is a root word for the prompt involving `אָשִׁית`.
- Located row: `data/active_scope_reviewed_questions.json`, id `30726360f3bf`, `pasuk_id=bereishis_3_15`, `question_type=shoresh`.
- Current expected answer in repo data: `שית`.
- Current explanation in repo data: `The shoresh of אָשִׁית is שית.`
- Why unresolved: the repo contains the expected answer, but the pilot evidence shows that this target may need teacher/source confirmation and level-appropriateness review.
- Repair applied: no source-truth change and no suppression applied in this task.
- Reason no source change was applied: this task has no explicit new teacher/source decision. Deciding whether `שית` is appropriate as a student-facing shoresh target would invent source authority.
- Classification: `needs_source_followup`.
- Follow-up: ask Yossi/source reviewer whether `שית` is the correct and age-appropriate shoresh target for `אָשִׁית` in Bereishis 3:15, and whether the item should be kept, revised, suppressed until reviewed, or observed again.

## What was intentionally not changed

- No phrase_translation logic was rewritten.
- No phrase_translation rows were suppressed.
- No `אָשִׁית` / `שית` source decision was applied.
- No Perek 4 activation or Perek 4 runtime work was done.
- No runtime scope, scoring, mastery, or question-selection logic was changed.

## Safety boundary confirmation

- No runtime scope expansion.
- No Perek 4 activation.
- No reviewed-bank/runtime promotion.
- No fake student data.
- No source-truth change.
- No distractor-generation logic change.
- No question-selection logic change.
