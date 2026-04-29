# Question quality rubric

## Purpose

This rubric helps a teacher or reviewer classify real pilot evidence consistently. It classifies evidence only. It does not promote content, approve runtime expansion, or activate any new scope.

## Decision table

| Decision category | Plain-English meaning | When to use it | Evidence required | Permits runtime promotion? | Required next action | Example note wording |
|---|---|---|---|---|---|---|
| `clear_keep` | The item appears clear and instructionally aligned in this observation. | Student understood the prompt, answered for the intended skill, and teacher saw no concern. | Real observation or explicit teacher review tied to a candidate/question. | No. | Keep as evidence for later review; do not promote automatically. | Student understood the noun-recognition prompt and explained the answer clearly. |
| `clear_minor_wording_improvement` | The item is basically usable, but wording could be smoother. | Student succeeded, but teacher noticed a small wording or explanation improvement. | Observation plus teacher note identifying the wording issue. | No. | Queue minor wording review before any broader use. | Prompt was understandable, but the explanation should say the target word more plainly. |
| `unclear_revise` | The item may be valid, but the student was confused by the prompt or presentation. | Student likely had the skill but misunderstood the question. | Student behavior, teacher note, and the confusing phrase/prompt element. | No. | Revise or re-observe after teacher wording review. | Student knew the word was a noun but did not understand “type of word.” |
| `wrong_answer_or_bad_distractor_reject` | The answer key or distractors make the item unsafe. | Expected answer is wrong, a distractor is also correct, or choices mislead unfairly. | Concrete answer/distractor concern with candidate ID or prompt. | No. | Block from broader use and repair only in a later explicit task. | Distractor “verb” felt plausible because the phrase display pushed the student toward action meaning. |
| `source_issue_follow_up` | There is a possible Hebrew, pasuk, source, or provenance issue. | Token, phrase, pasuk reference, or source confidence is questioned. | Source/ref concern and enough detail to re-check source artifacts. | No. | Follow up against source/provenance before any further use. | Token display may not match the cited pasuk phrase. |
| `student_confusion_but_question_valid_teacher_note` | The question seems valid, but the student confusion is pedagogically useful. | Confusion reflects a teachable misconception rather than a broken item. | Student behavior and teacher explanation of why the item itself remains valid. | No. | Keep note for reteach/teacher guidance; observe again if repeated. | Student confused noun vs name; item may still be useful with teacher framing. |
| `insufficient_evidence_observe_again` | There is not enough evidence to decide. | Observation was incomplete, student was distracted, or teacher cannot tell whether the item was clear. | Note explaining what evidence was missing. | No. | Observe again before making any decision. | Student clicked quickly without explaining; need another observation. |

## Promotion rule

One clean observation alone is not automatic runtime approval unless the repo's normal policy explicitly allows it. Runtime promotion requires the repo's normal reviewed-bank/runtime gate. This rubric only classifies evidence.

## Reviewer discipline

- Do not infer approval because an item looks good.
- Do not fill decisions from memory.
- Do not invent observations.
- Do not use this rubric to bypass reviewed-bank or runtime gates.
- Record the candidate ID, pasuk/ref, skill, prompt/target, student behavior, teacher note, rubric decision, and follow-up action.
