# Broad Vocabulary Teacher Review Packet V1

Date: 2026-04-30

## Purpose

This packet gives Yossi a focused teacher-review workspace for Broad Safe Vocabulary Bank V1 and Simple Vocabulary Question Candidate Lane V1.

It records review prompts only. It does not record teacher decisions, create question approval, move anything into protected preview, move anything into reviewed bank, or make anything available to runtime.

## Source artifacts

- `data/vocabulary_bank/bereishis_perek_4_broad_safe_vocabulary_bank_2026_04_30.tsv`
- `data/question_candidate_lanes/bereishis_perek_4_simple_vocabulary_question_candidates_2026_04_30.tsv`
- `data/question_candidate_lanes/bereishis_perek_4_simple_vocabulary_question_candidate_blockers_2026_04_30.tsv`
- `data/pipeline_rounds/simple_vocabulary_question_candidate_lane_v1_2026_04_30.json`

## Review instructions

For each row, Yossi should fill in the blank review fields later.

Allowed manual review responses:

- yes
- no
- needs revision
- hold

No response has been filled in by this packet.

## Word-level vocabulary review

Word-level review asks whether the vocabulary item itself is safe and useful as a teacher-reviewed word item. Word-level review is not question approval.

| Vocabulary ID | Pasuk | Hebrew | Gloss for review | Safety classification | Teacher word-level decision | Gloss notes | Safe for simple question review? |
|---|---:|---|---|---|---|---|---|
| bsvb_p4_001 | Bereishis 4:1 | אִישׁ | man | protected_preview_ready | ____ | ____ | ____ |
| bsvb_p4_002 | Bereishis 4:2 | צֹאן | flock / sheep | protected_preview_ready | ____ | ____ | ____ |
| bsvb_p4_003 | Bereishis 4:2 | אֲדָמָה | ground | revision_needed | ____ | ____ | ____ |
| bsvb_p4_004 | Bereishis 4:3 | מִנְחָה | offering | revision_needed | ____ | ____ | ____ |
| bsvb_p4_005 | Bereishis 4:15 | אוֹת | sign | teacher_review_ready | ____ | ____ | ____ |

## Simple question candidate review

These are teacher-review-only prompt candidates. They are not runtime questions.

| Candidate ID | Vocabulary ID | Lane | Review prompt preview | Expected answer for review | Distractor policy | Yossi prompt decision | Wording notes | Expected-answer notes |
|---|---|---|---|---|---|---|---|---|
| svqcl_p4_001 | bsvb_p4_001 | translate_hebrew_to_english | What does the word "אִישׁ" mean? | man | no_distractors_needed | ____ | ____ | ____ |
| svqcl_p4_002 | bsvb_p4_001 | find_word_in_pasuk | Find the word "אִישׁ" in the pasuk. | אִישׁ | no_distractors_needed | ____ | ____ | ____ |
| svqcl_p4_003 | bsvb_p4_001 | classify_basic_part_of_speech | Is "אִישׁ" a noun, verb, or keyword? | noun | no_distractors_needed | ____ | ____ | ____ |
| svqcl_p4_004 | bsvb_p4_002 | translate_hebrew_to_english | What does the word "צֹאן" mean? | sheep and goats | no_distractors_needed | ____ | ____ | ____ |
| svqcl_p4_005 | bsvb_p4_002 | find_word_in_pasuk | Find the word "צֹאן" in the pasuk. | צֹאן | no_distractors_needed | ____ | ____ | ____ |
| svqcl_p4_006 | bsvb_p4_002 | classify_basic_part_of_speech | Is "צֹאן" a noun, verb, or keyword? | noun | no_distractors_needed | ____ | ____ | ____ |
| svqcl_p4_007 | bsvb_p4_005 | translate_hebrew_to_english | What does the word "אוֹת" mean? | sign | no_distractors_needed | ____ | ____ | ____ |
| svqcl_p4_008 | bsvb_p4_005 | find_word_in_pasuk | Find the word "אוֹת" in the pasuk. | אוֹת | no_distractors_needed | ____ | ____ | ____ |
| svqcl_p4_009 | bsvb_p4_005 | classify_basic_part_of_speech | Is "אוֹת" a noun, verb, or keyword? | noun | no_distractors_needed | ____ | ____ | ____ |

## Revision and watch register

These items remain outside the simple question candidate lane until Yossi resolves the noted issue. They are not available for protected preview, reviewed bank, or runtime use.

| Vocabulary ID | Hebrew | Gloss for review | Current status | Reason held | Reconsider later? | Revision notes |
|---|---|---|---|---|---|---|
| bsvb_p4_003 | אֲדָמָה | ground | revision_needed | Needs teacher attention before question-candidate wording can be trusted. | ____ | ____ |
| bsvb_p4_004 | מִנְחָה | offering | revision_needed | Needs teacher attention before question-candidate wording can be trusted. | ____ | ____ |

## Perek 5 and Perek 6 status

Perek 5 and Perek 6 vocabulary remains planning-only in this packet. Those items are not mixed into the Perek 4 review lane.

## What this packet does not authorize

- It does not create teacher decisions.
- It does not create question approval.
- It does not move anything into protected preview.
- It does not move anything into reviewed bank.
- It does not create runtime questions.
- It does not widen runtime scope.
- It does not activate Perek 4, Perek 5, or Perek 6.
- It does not change scoring, mastery, question generation, question selection, source truth, or Runtime Learning Intelligence weighting.

## Safety confirmation

- Runtime scope expansion: no
- Perek activation: no
- Protected-preview promotion: no
- Reviewed-bank promotion: no
- Runtime content promotion: no
- Student-facing content creation: no
- Source-truth change: no
- Fake teacher approval: no
- Fake student data: no
- Raw log exposure: no
- Validator weakening: no
