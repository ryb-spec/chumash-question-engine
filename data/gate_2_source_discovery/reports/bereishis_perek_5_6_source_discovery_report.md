# Bereishis Perek 5-6 Source Discovery Report

## Purpose

This is Bereishis Perek 5-6 source discovery only. It creates a review-only inventory from canonical source evidence and does not create runtime content, reviewed-bank content, protected-preview content, or student-facing content.

## Source files inspected

- `data/pipeline_rounds/perek_4_final_internal_iteration_and_perek_5_6_source_discovery_gate_2026_04_29.md`
- `data/pipeline_rounds/perek_4_final_internal_iteration_and_perek_5_6_source_discovery_gate_2026_04_29.json`
- `data/pipeline_rounds/prompts/bereishis_perek_5_6_source_discovery_prompt.md`
- `data/source_texts/bereishis_hebrew_menukad_taamim.tsv`
- `data/curriculum_extraction/`
- `data/curriculum_extraction/normalized/`
- `data/verified_source_skill_maps/`
- `data/standards/`
- `data/word_bank.json`
- `data/translation_reviews.json`
- `data/active_scope_reviewed_questions.json`
- `data/active_scope_gold_annotations.json`

## Source/curriculum artifacts found

- Canonical Hebrew source text exists for Bereishis Perek 5 and Bereishis Perek 6 in `data/source_texts/bereishis_hebrew_menukad_taamim.tsv`.
- The Perek 4-to-Perek 5-6 launch gate exists and permits source discovery only.
- Canonical skill standards support conservative `WORD.PART_OF_SPEECH_BASIC` review-only classification.

## Source/curriculum artifacts missing

- No dedicated Bereishis Perek 5-6 curriculum-extraction normalized source-to-skill artifact was found.
- No verified Perek 5-6 source-to-skill map was found in `data/verified_source_skill_maps/`.
- No Perek 5-6 translation-review layer was found.
- `data/word_bank.json` does not currently provide broad Perek 5-6 lexical coverage.

## Summary of Perek 5 material inspected

Perek 5 is heavily genealogy/name-chain material. The safest review-only candidates are limited to a few visible noun targets such as `סֵפֶר`, `תּוֹלְדֹת`, `בָּנִים`, `בָנוֹת`, and `בֵּן`. Name-heavy rows, age formulas, repeated `שָׁנָה` clusters, and advanced verb formulas were excluded from the safe inventory.

## Summary of Perek 6 material inspected

Perek 6 includes narrative and ark-building material. Review-only candidates were limited to visible noun targets such as `בָשָׂר`, `חָמָס`, `תֵּבַת`, `קִנִּים`, `צֹהַר`, `פֶתַח`, and `מַבּוּל`. Context-heavy interpretation, phrase translation, advanced verbs, and technical vocabulary beyond a basic noun-recognition review lane were flagged for teacher review.

## Candidate-discovery method

Candidates were selected only when canonical Hebrew source text was present and the target looked useful for a conservative beginner-facing review discussion. Because no Perek 5-6 source-to-skill map exists, every row remains teacher-review-needed and review-only.

## Safe candidate criteria

- Canonical Hebrew source text exists.
- Candidate is in Perek 5 or Perek 6 only.
- Candidate is suitable for review-only basic noun-recognition discussion.
- Candidate can be reviewed without creating runtime or student-facing content.
- All permission gates remain false.

## Excluded-risk criteria

- Genealogy/name-heavy targets.
- Advanced shoresh or morphology.
- Ambiguous word forms.
- Phrase translation without whole-phrase review.
- Context-heavy interpretation.
- Repeated token clusters.
- Translation uncertainty.
- Weak source confidence beyond canonical text.
- Non-beginner grammar.

## Candidate count by perek

- Perek 5: 5
- Perek 6: 7
- Total: 12

## Candidate count by skill family

- basic_noun_recognition: 12

## Warnings

- All candidates are source-text-backed but not source-to-skill-map-backed.
- All candidates require teacher review.
- Perek 5 genealogy material is highly repetitive.
- Perek 6 ark/flood vocabulary can become translation/context-heavy if not tightly scoped.

## What was intentionally not created

- No runtime questions.
- No student-facing questions.
- No reviewed-bank rows.
- No protected-preview packet.
- No teacher decisions.
- No student observations.
- No source-truth edits.

## Explicit safety boundaries

- No Perek 5 runtime activation.
- No Perek 6 runtime activation.
- No active scope expansion.
- No reviewed-bank promotion.
- No protected-preview packet creation.
- No student-facing content.
- All gates remain false.
