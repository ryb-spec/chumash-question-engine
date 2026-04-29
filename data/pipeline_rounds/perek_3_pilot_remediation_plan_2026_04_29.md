# Perek 3 Pilot Remediation Plan - 2026-04-29

## 1. Executive summary

The 2026-04-29 fresh Perek 3 pilot showed that the app is usable enough to produce real student evidence, but several question-quality problems now need disciplined remediation before broader use. The strongest signals are: students were confused by vague metalinguistic wording, translation distractors were weak for specific vocabulary items, phrase-translation distractors need a separate audit, and one shoresh item needs source/teacher follow-up.

The safest next work is small and targeted: revise unclear wording templates, audit and repair the flagged translation distractors, and prepare a source-review question for the אָשִׁית / שית shoresh concern. This plan is evidence analysis only and creates no runtime change.

Teacher/source follow-up is needed before treating אָשִׁית / שית as a safe beginner shoresh item, and teacher review is strongly recommended before accepting repaired translation or phrase-translation distractors. What should not be changed yet: do not activate Perek 4, do not widen runtime scope, and do not promote any item to runtime or reviewed bank from this plan.

## 2. Evidence basis

Evidence files inspected:

- `data/pipeline_rounds/perek_3_fresh_pilot_observation_summary_2026_04_29.md`
- `data/pipeline_rounds/perek_3_fresh_pilot_observation_summary_2026_04_29.json`
- `data/gate_2_protected_preview_packets/reports/bereishis_perek_3_limited_post_preview_observation_intake.md`
- `docs/review/question_quality_rubric.md`
- `docs/pilots/perek_3_fresh_pilot_runbook.md`
- `data/pipeline_rounds/claude_review_action_plan_2026_04_29.md`
- `data/pipeline_rounds/perek_3_pilot_evidence_manifest_2026_04_29.json`
- `data/validation/curriculum_quality_check_summary.md`
- `data/validation/question_quality_risk_summary.md`
- `data/validation/runtime_review_exposure_index.md`
- `data/validation/protected_preview_source_lineage_matrix.md`
- `data/gate_2_protected_preview_candidates/reports/bereishis_perek_3_candidate_status_index.md`
- Runtime/question surfaces inspected read-only: `engine/flow_builder.py`, `runtime/question_flow.py`, `runtime/presentation.py`, `ui/render_question.py`, `ui/question_support.py`, and `question_ui.py` where present.

Raw log warning: the pilot summary reports that the raw pilot export/log review was not fully isolated and included older sessions. Fresh 2026-04-29 evidence was distinguished by using only the latest relevant 2026-04-29 student sessions and the manual teacher notes. Older historical rows were not treated as part of this fresh pilot.

Manual observation evidence includes Student 1 and Student 2 start times, question counts, teacher notes about confusing questions, bad distractors, and phrase-question quality. Export/session-derived evidence includes the latest 2026-04-29 Student 3 flagged issues and the pilot-summary issue objects. No fake observations are created by this plan.

## 3. Pilot issue table

| Issue ID | Issue title | Evidence source | Affected example | Ref | Word/phrase | Question type/family | Student/teacher observation | Rubric category | Severity | Confidence | Likely root cause | Recommended remediation type | Safe next? | Teacher follow-up? | Source follow-up? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| p3_pilot_001_form_wording | Vague form prompt confused student | Student 1 manual note; pilot summary issue 001 | `What form is shown?` | Bereishis 2:18 | אֶעֱשֶׂה | verb_tense | Student was not sure what "form" means. | unclear_revise | high | high | Prompt uses an abstract grammar label without telling the student what to identify. | prompt-template revision / wording-only | yes | no | no |
| p3_pilot_002_prefix_prompt_wording | Prefix prompt did not make target action clear | Student 3 session evidence; pilot summary issue 006 | `What is the prefix in בְּאִשְׁתּוֹ?` | not_available | בְּאִשְׁתּוֹ | prefix identification | Student found the prefix question unclear. | unclear_revise | high | high | The prompt asks for a prefix but does not visually isolate the first-letter target or explain the action. | prompt-template revision; possible visual highlighting | yes | no | no |
| p3_pilot_003_ashis_shis_source_followup | Shoresh/source follow-up needed | Student 1 manual note; Student 3 session evidence; pilot summary issues 003 and 008 | Student questioned whether שית is a root word for אָשִׁית. | Bereishis 3:15 | אָשִׁית / שית | shoresh | Student questioned the root; another student missed this item. | source_issue_follow_up | high | high | Source/pedagogic appropriateness is unresolved for a beginner shoresh question. | source/teacher follow-up; suppress-until-reviewed | no | yes | yes |
| p3_pilot_004_derech_distractors | דֶּרֶךְ distractors flagged bad | Student 3 session evidence; pilot summary issue 007 | `What does דֶּרֶךְ mean?` | not_available | דֶּרֶךְ | translation | Distractors were flagged as bad. | wrong_answer_or_bad_distractor_reject | high | high | Distractors may not be plausible same-lane alternatives for isolated vocabulary. | distractor-bank repair / audit | yes | yes | no |
| p3_pilot_005_arurah_distractors | אֲרוּרָה distractors flagged bad | Student 1 and Student 2 manual notes; pilot summary issues 002 and 005 | Translation question for אֲרוּרָה; Student 1 selected Eve while expected answer was cursed. | Bereishis 3:17 | אֲרוּרָה | translation | Bad distractors were noted twice; one answer selected a person-name distractor. | wrong_answer_or_bad_distractor_reject | critical | high | Distractor set may cross semantic categories and invite misleading guesses. | distractor-bank repair / audit | yes | yes | no |
| p3_pilot_006_phrase_translation_distractor_audit | Phrase-translation distractors need audit | Student 1 manual note; pilot summary issue 004 | Most phrase questions seemed to have bad distractors. | not_available | phrase-level translation choices | phrase_translation | Teacher saw repeated phrase-question distractor weakness. | wrong_answer_or_bad_distractor_reject | high | medium | Phrase distractors may not be matched by phrase length, syntax, or context. | deeper phrase-translation distractor audit before code | no | yes | no |

## 4. Prioritized remediation queue

### Immediate safe fixes

- Wording-only prompt revisions for `What form is shown?`, because the pilot showed direct student confusion and the fix can be tested without changing scope.
- Wording and display strategy for `What is the prefix in בְּאִשְׁתּוֹ?`, because it is a prompt clarity problem rather than a content expansion problem.
- Translation distractor audit and repair plan for אֲרוּרָה and דֶּרֶךְ, because these were concrete flagged examples with high-confidence pilot evidence.

### Needs teacher/source decision first

- אָשִׁית / שית shoresh: ask whether this is a defensible beginner-level shoresh question and whether it should be suppressed until review.
- Phrase-translation distractors: teacher review should confirm what counts as a fair phrase distractor before broad generation rules are changed.

### Needs deeper audit before code

- Phrase-translation distractor family, especially whether distractors are copied from single-word translation logic or are too obviously wrong.
- Runtime exposure for translation/context lanes, because quality-control reports already mark translation/context as high risk and teacher-review-required.

### Do not fix yet

- Do not refactor `engine/flow_builder.py` broadly.
- Do not alter runtime scope or Perek 4 activation.
- Do not promote Perek 3 protected-preview items to reviewed bank.
- Do not treat correct answers in this pilot as item approval.
- Do not broaden morphology, suffix, vav hahipuch, Rashi, or higher-order lanes from this evidence.

## 5. Recommended first implementation batch

Recommended first batch: no more than two implementation targets.

1. Wording-only prompt clarity pass for `What form is shown?` and `What is the prefix in בְּאִשְׁתּוֹ?`.
   This is first because the evidence is direct, the risk is low, and tests can lock the old confusing wording out of the affected lanes without changing runtime scope.

2. Translation distractor audit and minimal repair for the flagged אֲרוּרָה and דֶּרֶךְ examples.
   This is second because it addresses concrete student/teacher flags while keeping the work narrow. The implementation should first capture current generated choices in tests or an audit artifact, then repair the smallest responsible source of bad distractors.

Do not include אָשִׁית / שית source handling in the first implementation batch unless Yossi first answers the source/teacher review question. Do not implement phrase-translation generator changes until a focused phrase distractor audit exists.

## 6. Wording remediation strategy

The phrase `What form is shown?` was too vague for at least one student. Proposed wording should name the student action and the intended skill.

Possible proposed wording, not implemented wording:

- `Which verb form is this word showing?`
- `Is this word telling about past, present, future, or a command?`
- `What kind of verb form is this word?`

Recommendation: use the most concrete option that matches the existing answer choices. If answer choices are tense labels, the prompt should say tense or time/action form. If answer choices are broader verb forms, the prompt should avoid implying only tense.

Testing implication: future implementation should assert that the old bare prompt `What form is shown?` does not appear for the affected beginner-facing verb-tense lane unless explicitly reviewed.

## 7. Prefix prompt remediation strategy

The prompt `What is the prefix in בְּאִשְׁתּוֹ?` may be unclear because a student must know both the term prefix and how to visually isolate it inside a pointed Hebrew word. The target may be especially hard when the word includes nekudos and a suffix-like ending.

Possible fix types, not implemented here:

- Wording: `Which beginning letter is added to the word בְּאִשְׁתּוֹ?`
- Visual highlighting: show the prefix letter separately before asking the question, if the UI already supports safe formatting.
- Answer choice formatting: keep prefix choices short and visually distinct, and avoid choices that look like full words.
- Teacher-facing explanation: add a support line that this question is asking about the added beginning letter, not the whole word.

Recommended next step: start with wording and answer-choice display tests. Do not add new UI highlighting unless existing rendering support can do it narrowly without refactoring.

## 8. Shoresh/source follow-up strategy

The אָשִׁית / שית issue should not be resolved by engineering guesswork. The pilot evidence says a student questioned whether שית is really a root word, and another student missed the item. That makes this a source/teacher-review issue, not merely a wording issue.

Exact teacher/source question to ask:

> For Bereishis 3:15, should אָשִׁית be taught to this student level as having shoresh שית, and is that answer source-backed enough for a runtime shoresh question?

Until that is answered, recommended handling is to suppress or avoid this item for broader use, or mark it for observe-again only if Yossi wants more evidence. Do not decide source truth from this plan.

## 9. Translation distractor remediation strategy

The concrete flagged translation items are דֶּרֶךְ and אֲרוּרָה. A bad distractor in this context is an answer choice that is so unrelated, cross-category, misleading, or contextually noisy that the item stops measuring vocabulary recognition. For example, a person-name distractor in a question expecting `cursed` may invite category confusion rather than skill evidence.

Recommended audit method:

- Capture the generated choices for each flagged question.
- Classify each distractor by semantic category, part of speech, and whether it is plausible but not misleading.
- Remove distractors that are names, roles, or phrase meanings when the target is an adjective or single-word vocabulary item.
- Add a regression test that the repaired pool keeps all gates and active scope unchanged.

No answer banks are changed by this plan.

## 10. Phrase-translation distractor audit strategy

Phrase-translation distractors should differ from single-word distractors. A fair phrase distractor should be comparable in length, syntax, and plausibility, while still clearly wrong to a student who understands the phrase. It should not be a random word meaning, a person name, an unrelated clause, or a phrase that tests broad context rather than the target phrase.

Future audit examples to inspect:

- Are all choices phrase-like rather than a mix of words and phrases?
- Are distractors pulled from nearby phrase translations that share grammatical shape?
- Do distractors avoid giving away the correct answer by length or obvious category mismatch?
- Does the explanation justify the phrase meaning without requiring unsupported context?

Do not implement phrase-translation generator changes until this audit identifies the exact failure mode.

## 11. Testing and validation plan for future implementation

Future implementation should include:

- Wording template tests: assert old confusing prompt text is replaced only in the intended lanes.
- Prefix prompt tests: assert prefix questions explain the student action clearly and preserve answer correctness.
- Distractor quality tests: assert אֲרוּרָה and דֶּרֶךְ choices stay in a fair semantic lane and do not include misleading category leaks.
- Phrase-translation audit tests: assert phrase choices are phrase-like and do not degrade into single-word distractors.
- No-runtime-scope-expansion tests: assert Perek 4 remains inactive and active runtime scope is unchanged.
- Pilot evidence regression tests: assert pilot issue IDs remain represented in the remediation plan and follow-up artifacts.
- Source-follow-up tests if applicable: after Yossi decides אָשִׁית / שית, assert the item is either suppressed, revised, or explicitly reviewed.

## 12. Safety boundaries for the next implementation prompt

The next implementation prompt must not:

- change active runtime scope
- activate Perek 4
- promote Perek 3 or Perek 4 content to reviewed bank or runtime
- create student-facing content approvals
- invent observations or teacher decisions
- rewrite source truth
- broadly refactor `engine/flow_builder.py`
- broaden morphology, suffix, vav hahipuch, Rashi, or higher-order comprehension lanes
- hide failing validators
- treat this remediation plan as approval

## 13. Recommended next Codex implementation prompts

### Prompt 1: Implement Perek 3 pilot wording-only prompt clarity fixes

Scope: update only the minimum prompt-template wording needed for the flagged verb-form and prefix questions, add tests that verify clearer wording, and confirm active runtime scope and Perek 4 activation status do not change. Do not touch distractor generation or source-truth files.

### Prompt 2: Audit and repair flagged Perek 3 translation distractors

Scope: create a focused audit for the אֲרוּרָה and דֶּרֶךְ answer choices, repair only the minimal distractor source or rule needed, and add regression tests for fair choices. Do not broaden translation/context generation and do not modify phrase-translation logic until the phrase audit is complete.

### Prompt 3: Resolve Perek 3 shoresh/source follow-up and phrase-translation audit decisions

Scope: record Yossi/source decisions for אָשִׁית / שית, decide whether to suppress, revise, or observe again, and create a phrase-translation distractor audit artifact before any phrase generator changes. Do not decide source truth without explicit human review.

## Safety confirmation

- no runtime change was made by this plan
- no question generation changed
- do not activate Perek 4
- no runtime scope was widened
- no reviewed-bank or runtime promotion occurred
- no fake student data was created
- no raw logs were modified
