# Perek 3 Short Re-Pilot Results - 2026-04-29

## Purpose

This report records real short Perek 3 re-pilot evidence from the raw local pilot logs.

This artifact is evidence documentation only. It does not change runtime behavior, widen active scope, activate Perek 4, promote reviewed-bank content, approve any item for runtime, or create student-facing content.

## Evidence basis

- Raw attempt log evidence: `data/attempt_log.jsonl`
- Raw pilot session event evidence: `data/pilot/pilot_session_events.jsonl`
- Manual short re-pilot scope: `data/pipeline_rounds/perek_3_short_repilot_scope_2026_04_29.md`
- Manual scope-watch checklist: `data/pipeline_rounds/perek_3_short_repilot_manual_checklist_2026_04_29.md`
- Enforcement plan: `data/pipeline_rounds/perek_3_short_repilot_enforcement_plan_2026_04_29.md`

The raw JSONL files are dirty worktree evidence from the 2026-04-29 short re-pilot. They were not edited manually by this task and are not treated as committed governance artifacts.

## Session summary

- Pilot date: 2026-04-29
- Session evidence reviewed: `pilot-20260429T190709Z-c9d9987e` plus one served event from `pilot-20260429T190951Z-d1910a27`
- Mode: Learn Mode
- Active scope observed: `local_parsed_bereishis_1_1_to_3_24`
- Trusted active scope: true
- Answered attempts in raw diff: 8
- Correct answered attempts in raw diff: 8
- Perek 4 content served: no
- Reviewed-bank/runtime promotion applied: no
- Fake student data created: no

## Clean positive evidence

| Evidence ID | Question family | Example | Result | Note |
| --- | --- | --- | --- | --- |
| p3_short_repilot_pos_001 | prefix identification | `In בְּיוֹם, which beginning letter is the prefix?` | answered correctly | The generated prefix wording was clear enough for this observed item. |
| p3_short_repilot_pos_002 | verb tense/form | `What tense or verb form is this word?` for `וְתֵרָאֶה` | answered correctly | The revised tense/form wording appeared in served content and was answered correctly. |
| p3_short_repilot_pos_003 | word translation | `הִשִּׁיאַנִי`, `חָי`, `טוֹב` | answered correctly | These were answered correctly, but they do not prove the targeted `דֶּרֶךְ` or `אֲרוּרָה` repairs. |
| p3_short_repilot_pos_004 | shoresh identification | `וַיְגָרֶשׁ` | answered correctly | This was not the blocked `אָשִׁית` / `שית` beginner shoresh issue. |

## Scope leaks and cautions

| Finding ID | Finding | Evidence | Result |
| --- | --- | --- | --- |
| p3_short_repilot_leak_001 | Excluded `phrase_translation` was served. | `בְּעֶצֶב תֵּלְדִי בָנִים`, Bereishis 3:16 | Answered correctly, but it must not count as clean short re-pilot evidence because unverified phrase_translation was excluded from this short scope. |
| p3_short_repilot_leak_002 | Excluded `phrase_translation` was served again. | `וְאֵיבָה אָשִׁית`, Bereishis 3:15 | Answered correctly, but it must not count as clean short re-pilot evidence because unverified phrase_translation was excluded and the phrase contains the still-follow-up `אָשִׁית` context. |
| p3_short_repilot_wording_001 | Old prefix wording still appeared in a later served event. | `What is the prefix in בְּאִשְׁתּוֹ?` | This suggests at least one active reviewed-bank row still carries old prefix wording. It was served after the first session restart and was not answered in the attempt-log diff. |

## Targeted issue coverage

| Target | Intended short re-pilot status | Evidence result |
| --- | --- | --- |
| Revised tense/form wording | test | Tested once and answered correctly. |
| Revised prefix prompt wording | test | Revised wording appeared once and was answered correctly. Old wording also appeared in a later served event, so the fix is not fully clean across served content. |
| `דֶּרֶךְ` distractor repair | test | Not observed in the answered raw evidence reviewed for this short re-pilot. |
| `אֲרוּרָה` distractor repair | test | Not observed in the answered raw evidence reviewed for this short re-pilot. |
| `אָשִׁית` / `שית` beginner shoresh exclusion | exclude | No `אָשִׁית` / `שית` beginner shoresh question was observed. A phrase_translation item containing `אָשִׁית` was served and is treated as an excluded-lane leak. |
| Unverified `phrase_translation` exclusion | exclude | Failed manual-only scope enforcement: two phrase_translation items were served. |
| Perek 4 exclusion | exclude | Passed: no Perek 4 content was observed in the reviewed raw evidence. |

## Interpretation

The short re-pilot produced useful evidence that the revised tense/form prompt can work and that at least one generated prefix prompt used the clearer wording. It did not produce clean closure evidence because excluded phrase_translation items were served and because an old prefix prompt appeared in a later served event.

The results support a narrow follow-up: clean up the remaining old prefix wording source and use a stronger short re-pilot scope-control mechanism before relying on the next re-pilot as closure evidence.

## Gate result

- Ready for full Perek 3 closure: no
- Ready for runtime expansion: no
- Ready for reviewed-bank/runtime promotion: no
- Ready for Perek 4 runtime activation: no
- Ready for Perek 4 reviewed-bank promotion: no
- Ready for Perek 4 student-facing use: no
- Ready to continue Perek 4 review-only planning automatically: no, not from this evidence alone

## Recommended next action

Create a narrow follow-up task to either:

1. enforce the short re-pilot scope with a pilot-only filter, or
2. update the manual re-pilot protocol so excluded phrase_translation items are skipped immediately, and
3. locate and repair the active reviewed-bank row that still serves `What is the prefix in בְּאִשְׁתּוֹ?`.

Then run a cleaner short re-pilot focused only on revised tense/form wording, revised prefix wording, `דֶּרֶךְ`, and `אֲרוּרָה`.

## Safety boundary confirmation

- Runtime behavior changed by this task: no
- Question generation changed by this task: no
- Active runtime scope widened: no
- Perek 4 activated: no
- Reviewed-bank/runtime promotion: no
- Student-facing content created: no
- Source truth changed: no
- Raw logs manually modified: no
- Fake data created: no
