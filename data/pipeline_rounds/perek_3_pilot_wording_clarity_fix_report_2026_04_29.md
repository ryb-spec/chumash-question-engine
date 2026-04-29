# Perek 3 Pilot Wording Clarity Fix Report - 2026-04-29

## Purpose

This report records the Perek 3 pilot wording-only prompt clarity fix. It changes student-facing prompt text only. It does not change question selection, distractor generation, scoring, mastery, runtime scope, reviewed-bank status, source truth, or Perek 4 activation.

## Evidence source

- `data/pipeline_rounds/perek_3_pilot_remediation_plan_2026_04_29.md`
- `data/pipeline_rounds/perek_3_pilot_remediation_plan_2026_04_29.json`
- `data/pipeline_rounds/perek_3_pilot_remediation_sequence_2026_04_29.md`
- `data/pipeline_rounds/perek_3_fresh_pilot_observation_summary_2026_04_29.md`
- `data/gate_2_protected_preview_packets/reports/bereishis_perek_3_limited_post_preview_observation_intake.md`
- `docs/review/question_quality_rubric.md`

## Wording issues addressed

1. Student confusion around the vague verb-tense prompt `What form is shown?`
2. Student confusion around the prefix-identification prompt pattern `What is the prefix in <word>?`

## Files changed

- `engine/flow_builder.py`
- `tests/test_prefix_question_generation.py`
- `tests/test_tense_morphology_questions.py`
- `scripts/validate_perek_3_pilot_wording_clarity_fix.py`
- `tests/test_perek_3_pilot_wording_clarity_fix.py`
- `scripts/validate_curriculum_extraction.py`
- `tests/test_curriculum_extraction_validation.py`
- `data/pipeline_rounds/perek_3_pilot_wording_clarity_fix_report_2026_04_29.md`

## Old wording

- `What form is shown?`
- `What is the prefix in <word>?`

## New wording

- `What tense or verb form is this word?`
- `In <word>, which beginning letter is the prefix?`

## Why this change is safe

- The change is wording-only.
- The existing answer choices remain unchanged.
- The existing target selection logic remains unchanged.
- Distractor generation remains unchanged.
- Runtime scope remains unchanged.
- Perek 4 is not activated.
- No content is promoted to reviewed bank or runtime.

## What was intentionally not changed

- No דֶּרֶךְ distractor changes.
- No אֲרוּרָה distractor changes.
- No phrase-translation distractor changes.
- No שית / אָשִׁית source-truth decision.
- No scoring, mastery, runtime scope, or question selection changes.
- No source-truth changes.

## Validation run

The required validation commands for this task are:

- `python scripts/validate_perek_3_pilot_wording_clarity_fix.py`
- `python -m pytest tests/test_perek_3_pilot_wording_clarity_fix.py`
- `python scripts/validate_perek_3_pilot_remediation_plan.py`
- `python scripts/validate_perek_3_pilot_observation_summary.py`
- `python scripts/validate_perek_3_pilot_evidence_pack.py`
- `python scripts/validate_curriculum_extraction.py`
- `python scripts/validate_curriculum_extraction.py --check-git-diff`
- `python -m pytest`

## Next recommended step

Run the next planning/implementation step for the distractor audit and repair plan, focused on דֶּרֶךְ and אֲרוּרָה, without broadening translation/context generation.

## Safety confirmation

- No runtime scope expansion.
- No Perek 4 activation.
- No distractor changes in this task.
- No question selection changes.
- No scoring or mastery changes.
- No reviewed-bank or runtime promotion.
- No fake student data.
