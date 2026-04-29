# Perek 3 Short Re-Pilot Scope Enforcement Plan - 2026-04-29

## Purpose

This plan defines the safest minimal enforcement path for the short Perek 3 re-pilot after Yossi's language decisions.

The goal is to keep the re-pilot focused on remediated Perek 3 areas only, while excluding unresolved items:

- `אָשִׁית` / `שית` shoresh question
- unverified `phrase_translation` questions
- Perek 4 content

## Enforcement type

Enforcement type: `manual`.

Runtime enforcement was not added in this task. Data-level suppression/quarantine metadata was not added in this task.

Reason: the current repo has supported suppression paths for some active-scope gold/override cases, but this task would require either a new short-repilot runtime filter or changes to normal question-selection behavior. That is outside the safe scope for this task.

## What is included

The short re-pilot may test only these remediated lanes:

- revised tense/form wording
- revised prefix prompt wording
- `דֶּרֶךְ` translation distractor repair
- `אֲרוּרָה` translation distractor repair

## What is excluded

The short re-pilot must not count these as valid re-pilot evidence:

- `אָשִׁית` / `שית` shoresh question
- unverified `phrase_translation` items
- Perek 4 content
- any runtime expansion
- any reviewed-bank/runtime promotion claim

## Exact risks

- The normal app/runtime can still contain reviewed-bank `phrase_translation` questions.
- The normal app/runtime does not currently have a dedicated short-repilot-only filter.
- A student could still be served an excluded item if Yossi runs the normal app without manual scope watching.
- If an excluded item appears, it must be treated as a scope leak, not as clean re-pilot evidence.

## How Yossi should run the re-pilot

1. Use Learn Mode only.
2. Use 1-2 students.
3. Ask 8-10 questions per student.
4. Keep the teacher monitor or pilot monitor open.
5. Watch every served question type and selected word.
6. Count only remediated wording, `דֶּרֶךְ`, and `אֲרוּרָה` observations as in-scope evidence.
7. If `אָשִׁית`, `שית`, `phrase_translation`, or Perek 4 content appears, stop or skip that evidence and record a scope leak.

## What counts as a scope leak

- Any prompt asking `What is the shoresh of אָשִׁית?`
- Any expected answer or answer choice treating `שית` as a beginner shoresh target.
- Any question with `question_type=phrase_translation`.
- Any question from Bereishis Perek 4.
- Any message or artifact claiming runtime approval, runtime promotion, or Perek 4 activation.

## Current readiness

Short re-pilot readiness: true, manual-only.

Manual scope watch required: true.

The short re-pilot is ready only if Yossi actively watches for the excluded lanes. This plan does not claim that the runtime itself prevents those lanes from being served.

## Scope leak fix update

The 2026-04-29 short re-pilot results found two leaks:

- stored active reviewed-bank prefix prompts still used `What is the prefix in <word>?`;
- excluded `phrase_translation` items were served.

The stale stored prefix wording leak was addressed at the data level for active reviewed-bank prefix-identification prompts. The approved stored wording is now:

`In <word>, which beginning letter is the prefix?`

The `phrase_translation` leak is not runtime-enforced in this task. It remains manual-watch plus validator-guarded because adding a short-repilot-only runtime filter would change question-selection behavior outside this narrow task.

Updated clean short re-pilot readiness:

- ready_for_clean_short_repilot: true
- old_prefix_wording_leak_addressed: true
- phrase_translation_leak_addressed_by_runtime_filter: false
- phrase_translation_leak_guarded_by_validator: true
- manual_scope_watch_required: true
- perek_4_teacher_review_packet_allowed_after_clean_short_repilot: true
- Perek 4 activated: false
- Runtime scope widened: false

## Safety boundary confirmation

- Runtime scope widened: no.
- Perek 4 activated: no.
- Reviewed-bank/runtime promotion: no.
- Source truth changed: no.
- Question selection changed: no.
- Scoring/mastery changed: no.
- Fake data created: no.
