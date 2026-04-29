# Perek 3 Pilot Remediation Sequence - 2026-04-29

This sequencing map turns the fresh pilot evidence into small, safe engineering phases. It does not implement the fixes.

## Phase 1: wording-only low-risk fixes

Goal: clarify the flagged verb-form and prefix prompts without changing runtime scope.

Why this phase comes here: the evidence is direct, the fixes are narrow, and tests can prove the confusing wording is gone from the targeted lanes.

Files likely involved in the future: `engine/flow_builder.py`, possibly `question_ui.py` or UI support files if wording is rendered outside the payload.

Risk: medium, because wording affects student experience but should not alter selection logic.

Validation commands: `python -m pytest tests/test_streamlit_quiz_experience.py tests/test_streamlit_candidate_quality.py`, plus targeted wording tests created in the implementation task, then `python -m pytest`.

Stop conditions: any active-scope change, Perek 4 activation, reviewed-bank promotion, source-truth edit, or broad refactor requirement.

## Phase 2: distractor-quality audit and repair

Goal: audit and minimally repair the flagged translation distractors for the concrete examples, especially אֲרוּרָה and דֶּרֶךְ.

Why this phase comes here: these issues can cause wrong evidence even when students understand the target skill, but they need a visible before/after audit.

Files likely involved in the future: `engine/candidate_selection.py`, `engine/flow_builder.py`, relevant tests, and possibly a non-runtime distractor audit artifact.

Risk: high, because translation/context lanes already have quality-control warnings and distractor changes can affect many generated questions.

Validation commands: targeted translation/distractor tests, `python scripts/run_curriculum_quality_checks.py`, `python scripts/validate_curriculum_extraction.py --check-git-diff`, then `python -m pytest`.

Stop conditions: broad answer-bank rewrites, unreviewed translation expansion, phrase-translation changes without an audit, or validator weakening.

## Phase 3: source/teacher follow-up outcomes

Goal: record Yossi/source decisions for אָשִׁית / שית and decide whether the item is suppressed, revised, rejected, or observed again.

Why this phase comes here: engineering should not decide source truth. The pilot exposed uncertainty that must be resolved by teacher/source review.

Files likely involved in the future: a review-decision artifact, possibly tests for a suppression rule if explicitly approved.

Risk: high, because wrong source handling can make a question look authoritative when it is not.

Validation commands: source-follow-up validator if created, source text validation, curriculum extraction git-diff guard, then `python -m pytest`.

Stop conditions: no explicit Yossi/source decision, source-truth edits, or runtime approval from a planning artifact.

## Phase 4: re-pilot / regression observation

Goal: run another small pilot after the Phase 1 and Phase 2 fixes, then record real observations.

Why this phase comes here: the next evidence should prove whether the wording and distractor repairs actually helped students.

Files likely involved in the future: pilot observation intake, pilot observation summary artifacts, and validator/tests for real evidence only.

Risk: medium, because evidence can become noisy if logs are not isolated.

Validation commands: `python scripts/validate_perek_3_pilot_observation_summary.py`, `python scripts/validate_perek_3_pilot_evidence_pack.py`, and `python -m pytest`.

Stop conditions: fake observations, inferred approvals, unisolated data treated as fresh evidence without a warning, or runtime promotion.

## Phase 5: only then resume Perek 4 teacher-review packet work

Goal: resume Perek 4 teacher-review packet planning only after Perek 3 pilot remediation has a clean evidence loop.

Why this phase comes here: the Perek 3 pilot found runtime-content quality issues; Perek 4 should not move faster than the evidence loop can support.

Files likely involved in the future: Perek 4 source-discovery inventory, a Perek 4 teacher-review packet prompt, and source-discovery validators.

Risk: medium, because Perek 4 work must remain review-only and must not become runtime activation.

Validation commands: `python scripts/validate_perek_4_source_discovery.py`, Perek 4 checklist tests if created, `python scripts/run_curriculum_quality_checks.py`, then `python -m pytest`.

Stop conditions: Perek 4 runtime activation, protected-preview packet creation before review, Perek 5 expansion, or reviewed-bank promotion.
