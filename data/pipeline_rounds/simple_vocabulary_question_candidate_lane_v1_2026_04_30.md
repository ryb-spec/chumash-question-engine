# Simple Vocabulary Question Candidate Lane V1 - 2026-04-30

## Purpose

Create a teacher-review-only question-candidate lane from the Broad Safe Vocabulary Bank V1.

## Why this lane exists

The vocabulary bank allows word-level approval without creating questions. This lane is the next controlled step: it proposes simple prompt wording and expected answers for Yossi review while keeping all higher gates closed.

## Input vocabulary bank

Input: `data/vocabulary_bank/bereishis_perek_4_broad_safe_vocabulary_bank_2026_04_30.tsv`

Perek 4 input words:

- `אִישׁ`
- `צֹאן`
- `אֲדָמָה`
- `מִנְחָה`
- `אוֹת`

## Eligibility rules

Candidates were created only when the vocabulary row had source support, a stable pasuk reference, an English gloss, and no unresolved revision blocker before question-candidate review.

## Allowed simple question lanes

- `translate_hebrew_to_english`
- `find_word_in_pasuk`
- `classify_basic_part_of_speech`

The `identify_hebrew_from_english` lane is allowed by policy but not used in this first lane because it would require reviewed distractors. No distractors were invented.

## Forbidden question lanes

No candidates were created for tense, shoresh identification, prefix or suffix analysis, phrase translation, Rashi, inference, conceptual comprehension, context-sensitive meaning, pasuk-level translation, dikduk morphology, gender/number/person, or vav hahipuch.

## Perek 4 candidate summary

Nine teacher-review-only candidates were created from three words:

| Word | Candidate lanes |
| --- | --- |
| אִישׁ | translate, find word in pasuk, classify basic part of speech |
| צֹאן | translate, find word in pasuk, classify basic part of speech |
| אוֹת | translate, find word in pasuk, classify basic part of speech |

## Candidate count by lane

- `translate_hebrew_to_english`: 3
- `find_word_in_pasuk`: 3
- `classify_basic_part_of_speech`: 3

## Blocked/revision-needed summary

Two vocabulary rows remain blocked from the simple question-candidate lane:

- `אֲדָמָה`: spacing/session-balance caution remains unresolved.
- `מִנְחָה`: Minchah/offering alias, part-of-speech-only, and spacing cautions remain unresolved.

## Perek 5/6 planning-only status

Perek 5/6 remains planning-only. No Perek 5/6 simple question candidates were created, and no Perek 5/6 material was mixed into the Perek 4 lane.

## Distractor policy

All created candidates use `no_distractors_needed`. The lane does not create final distractor banks and does not draw distractors from Perek 5/6 planning-only material.

## What this does NOT authorize

This does not create runtime questions. It does not promote protected preview, reviewed bank, runtime content, or student-facing content. It does not change question generation, question selection, scoring/mastery, source truth, or Runtime Learning Intelligence weighting.

## Recommended next teacher-review packet branch

`feature/broad-vocabulary-teacher-review-packet-v1`

## Safety confirmation

- Runtime scope expansion: no.
- Perek activation: no.
- Protected-preview promotion: no.
- Reviewed-bank promotion: no.
- Runtime content promotion: no.
- App question generation change: no.
- Scoring/mastery change: no.
- Question-selection change: no.
- Source truth change: no.
- Fake teacher approval: no.
- Fake student data: no.
- Raw logs: no.
- Validator weakening: no.
