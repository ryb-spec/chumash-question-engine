# Perek 3 fresh pilot observation summary - 2026-04-29

## Purpose

This report records real evidence from the first fresh Perek 3 student pilot on 2026-04-29. It is evidence documentation only.

This report does not change runtime behavior, does not activate Perek 4, does not widen runtime scope, does not promote content to runtime or reviewed bank, and does not create student-facing content.

## Pilot scope

- Pilot date: 2026-04-29
- Number of students: 3
- Questions per student: 10
- Mode: Learn Mode
- Total questions observed: 30
- Source logs used: `data/attempt_log.jsonl`, `data/pilot/pilot_session_events.jsonl`
- Manual notes used: Yossi/teacher notes supplied with this task

## Evidence inclusion and exclusion

- Included: the three latest answered 2026-04-29 sessions matching the 30 fresh-pilot answers.
- Included: manual notes for Student 1, Student 2, and Student 3.
- Excluded: older sessions in exports/logs, because the pilot export was not isolated.
- Excluded: partial 2026-04-29 session `pilot-20260429T161806Z-ab074183`, because it had no answered rows and is not part of the 30-question fresh pilot.
- Export note: no matching 2026-04-29 exported pilot review JSON file was found by filename during this task; the dirty session-event log was used as the exported/session evidence source.

## Student/session summary

| Student | Manual start time | Session evidence | Questions answered | Notes |
|---|---:|---|---:|---|
| Student 1 | 11:20 | `pilot-20260429T161843Z-5801af30` | 10 | Manual notes identify question 4 wording confusion, question 9 ??? follow-up, and phrase-question distractor concerns. |
| Student 2 | 11:25 | `pilot-20260429T162445Z-62918bcf` | 10 | Manual note identifies question 5 ???????? distractor problem. |
| Student 3 | not_available | `pilot-20260429T162905Z-e199528f` | 10 | Session/manual evidence identifies prefix wording issue, ??????? distractor issue, and an incorrect ???-family shoresh answer. |

## Manually observed issues

- Student 1, question 4: student was not sure what ?form? means.
- Student 1, question 9: student questioned whether ??? is a root word.
- Student 1: repeated questions none noted.
- Student 1: most phrase questions seemed to have bad distractors.
- Student 2, question 5: ???????? had bad distractors.
- Student 3: prefix question ?What is the prefix in ?????????????? was unclear.
- Student 3: translation question ?What does ??????? mean?? had bad distractors.

## Exported/session flagged issues

- Student 1, question 5: `????????`, expected `cursed`, answered `Eve`.
- Student 3, question 9: `???????`, expected `???`, answered `???`.
- Session logs confirm the three 10-answer clusters and Learn Mode practice evidence.

## Issue table

| Issue ID | Student | Question | Token/phrase | Category | Rubric decision | Observation | Follow-up action |
|---|---|---:|---|---|---|---|---|
| p3_pilot_2026_04_29_001 | Student 1 | 4 | ???????? | unclear wording | unclear_revise | Student was not sure what ?form? means, even though the logged answer was correct. | Revise or teacher-review wording for form/tense prompts before broader use. |
| p3_pilot_2026_04_29_002 | Student 1 | 5 | ???????? | bad distractors | wrong_answer_or_bad_distractor_reject | Exported attempt log shows wrong answer ?Eve?; this aligns with later teacher note that ???????? had bad distractors. | Block this distractor set from broader use until choices are reviewed and repaired in a later task. |
| p3_pilot_2026_04_29_003 | Student 1 | 9 | ??????? / ??? | shoresh/source follow-up | source_issue_follow_up | Student questioned whether ??? is a root word; answer was logged correct, but source/teacher follow-up is needed before treating this as clean evidence. | Confirm the shoresh/source presentation with teacher/source authority before broader use. |
| p3_pilot_2026_04_29_004 | Student 1 | 7, 8, 10 | ????????? ????????????; ??? ?????? ???????????; ??? ???????? | phrase-translation distractor quality | wrong_answer_or_bad_distractor_reject | Teacher note: most phrase questions seemed to have bad distractors. Logs show phrase questions were served, but distractor content is not safely recoverable from the attempt log alone. | Audit phrase-translation distractors before further pilot expansion; do not infer item approval from correct answers alone. |
| p3_pilot_2026_04_29_005 | Student 2 | 5 | ???????? | bad distractors | wrong_answer_or_bad_distractor_reject | Teacher note: Question 5 ???????? had bad distractors, even though this student answered correctly. | Review and repair distractors before broader use; do not count this as clean approval evidence. |
| p3_pilot_2026_04_29_006 | Student 3 | 1 | ???????????? | unclear wording | unclear_revise | Known exported/session issue: prefix question wording was unclear even though the answer was logged correct. | Revise or teacher-review prefix prompt wording before broader use. |
| p3_pilot_2026_04_29_007 | Student 3 | 2 | ??????? | bad distractors | wrong_answer_or_bad_distractor_reject | Known exported/session issue: translation question had bad distractors, even though the answer was logged correct. | Review and repair distractors before broader use; do not treat correct click as approval. |
| p3_pilot_2026_04_29_008 | Student 3 | 9 | ??????? / ??? | shoresh/source follow-up | source_issue_follow_up | Exported/session evidence shows incorrect answer on the same ??? root-family item that Student 1 questioned. | Treat ???/??????? as a follow-up lane before further use; confirm source and instructional presentation. |

## Issue categories

- Unclear wording: form/tense prompt wording and prefix prompt wording need revision or teacher review.
- Bad distractors: single-word translation distractors for ???????? and ??????? need review.
- Shoresh/source follow-up: ??? / ??????? needs teacher/source confirmation before broader use.
- Phrase-translation distractor quality: phrase questions may have weak distractors even when students answered correctly.

## What should be fixed first

1. Review and repair bad distractors for single-word translation items, especially ???????? and ???????.
2. Revise unclear prompt language for ?What form is shown?? and prefix-identification wording.
3. Audit phrase-translation distractors before expanding or treating phrase results as clean evidence.
4. Teacher/source follow-up for ??? / ??????? shoresh presentation.

## What should not be changed yet

- Do not activate Perek 4.
- Do not widen runtime scope.
- Do not promote any item to runtime or reviewed bank.
- Do not rewrite question generation from this evidence alone.
- Do not treat correct answers as approval when teacher notes identify distractor or wording problems.

## Safety state

- No runtime behavior changed.
- No Perek 4 activation.
- No reviewed-bank promotion.
- No runtime promotion.
- No fake data created.
- No student-facing content created.
- Dirty log files were used as source evidence only and were not modified by this task.
