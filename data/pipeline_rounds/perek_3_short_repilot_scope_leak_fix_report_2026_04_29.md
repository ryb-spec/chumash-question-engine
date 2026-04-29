# Perek 3 Short Re-Pilot Scope Leak Fix Report - 2026-04-29

## Purpose

This report records the narrow remediation for the short Perek 3 re-pilot scope leaks found in the 2026-04-29 evidence.

This task does not activate Perek 4, widen runtime scope, promote content, mark Perek 3 fully closed, mark phrase_translation resolved, approve `אָשִׁית` / `שית`, change source truth, or change scoring/mastery behavior.

## Evidence of the leaks

- Short re-pilot results: `data/pipeline_rounds/perek_3_short_repilot_results_2026_04_29.md`
- Scope leak report: `data/pipeline_rounds/perek_3_short_repilot_scope_leak_report_2026_04_29.md`
- Active reviewed-bank data: `data/active_scope_reviewed_questions.json`

The short re-pilot leaked in two ways:

1. Excluded `phrase_translation` items were served.
2. Stored active reviewed-bank prefix prompts still used the stale pattern `What is the prefix in <word>?`, including the observed `בְּאִשְׁתּוֹ` item.

## Where each leak was found

| Leak | Location | Finding |
| --- | --- | --- |
| Stale prefix wording | `data/active_scope_reviewed_questions.json` | Stored `prefix_level_1_identify_prefix_letter` rows used `What is the prefix in <word>?`. |
| phrase_translation scope leak | raw short re-pilot logs summarized in `perek_3_short_repilot_results_2026_04_29.md` | `phrase_translation` questions were served even though unverified phrase_translation was excluded from short re-pilot evidence. |

## What was fixed

The stale stored reviewed-bank prefix wording was repaired at the data level.

Old stored wording:

`What is the prefix in <word>?`

New stored wording:

`In <word>, which beginning letter is the prefix?`

The fix was limited to the prompt fields for active reviewed-bank `prefix_level_1_identify_prefix_letter` rows. It did not change answers, distractors, skill IDs, reviewed IDs, pasuk bindings, runtime permission, reviewed-bank status, or source truth.

## What was intentionally not fixed

The `phrase_translation` leak was not fixed through runtime selection logic in this task.

Reason: the repo has an isolated pilot export/review helper, but there is not an existing short-repilot-only runtime filter that can be enabled without changing normal question selection behavior. Adding that architecture here would be broader than this task.

Instead, phrase_translation is now guarded by validator/reporting:

- the updated enforcement plan keeps `phrase_translation` excluded;
- the updated Perek 3-to-Perek 4 gate still requires a clean short re-pilot;
- this task adds validation that prevents claiming the stale prefix fix or Perek 4 gate is open while phrase_translation remains unresolved.

## Enforcement type

Enforcement type: manual plus validator guard.

- Runtime-enforced: no.
- Data-enforced for stale prefix wording: yes, prompt text only.
- Validator-enforced for the short re-pilot gate: yes.
- Manual watch still required for `phrase_translation`, `אָשִׁית` / `שית`, and Perek 4 scope leaks.

## Clean short re-pilot requirement

Another short re-pilot is still required before Perek 4 teacher-review packet work proceeds, unless Yossi explicitly overrides that requirement.

The next short re-pilot should test only:

- revised tense/form wording;
- revised prefix wording;
- repaired `דֶּרֶךְ` translation distractors if served;
- repaired `אֲרוּרָה` translation distractors if served.

The next short re-pilot must exclude:

- `phrase_translation`;
- `אָשִׁית` / `שית`;
- Perek 4 content.

## Perek 4 gate implication

Perek 4 teacher-review packet work may proceed only after a clean short Perek 3 re-pilot or an explicit Yossi override.

Perek 4 runtime activation remains blocked.

## Safety boundary confirmation

- Runtime scope changed: no.
- Perek 4 activated: no.
- Reviewed-bank/runtime promoted: no.
- Fake data created: no.
- Source truth changed: no.
- Question selection changed: no.
- Scoring/mastery changed: no.
- Validators weakened: no.
