# Perek 3 fresh pilot runbook

## Purpose

This runbook helps Yossi or another teacher run a small fresh Perek 3 pilot and collect real evidence about question clarity, student understanding, and teacher concerns.

This is a pilot-evidence workflow only. It does not approve runtime expansion, does not activate Perek 4, and does not promote any item automatically.

## What this pilot is testing

- Whether students understand the current Learn Mode experience.
- Whether Perek 3 pilot items feel clear, fair, and useful.
- Whether students can answer for the intended Chumash skill rather than by guessing.
- Whether Hebrew tokens, references, prompts, answer choices, and explanations feel accurate enough for continued limited review.
- Whether teacher-monitor evidence points to a small number of concrete fixes.

## What this pilot is not testing

- It is not a schoolwide rollout.
- It is not a runtime expansion review.
- It is not Perek 4 activation.
- It is not reviewed-bank promotion.
- It is not a final standards dashboard review.
- It is not a test of every Chumash skill.

## Who should participate

Use 3-5 students, ideally mixed ability. A tiny mixed group is more useful than a large unobserved run because the goal is evidence quality, not coverage.

## Required mode

Use Learn Mode only.

## Pilot length

Use 8-10 questions per student.

## Teacher setup

- Open the teacher monitor before the student begins.
- Keep the run fresh and separate from older pilot exports.
- Do not coach unless the student is stuck.
- Watch for confusion, hesitation, repeated issues, bad answer choices, and teacher concerns.
- If a student guesses correctly but cannot explain, record that.
- If a student knows the skill but misunderstands the prompt, record that.

## Student instructions

Suggested teacher script:

> We are testing whether this Chumash practice tool is clear and helpful. Try each question on your own. If something is confusing, say so out loud. This is not a grade, and your feedback helps us fix the tool.

## What to record

Record real observations only:

- unclear wording
- wrong morphology
- bad distractor
- wrong pasuk
- too repetitive
- student knew the skill but misunderstood the prompt
- student guessed correctly but could not explain
- teacher concern
- Hebrew display issue
- explanation concern

Use `docs/review/question_quality_rubric.md` to classify each observation.

## How to use existing pilot scripts

The repo includes `scripts/pilot_isolated_run.py`.

Prepare a fresh isolated pilot run label:

```powershell
python scripts/pilot_isolated_run.py prepare --label perek-3-fresh-pilot
```

The command prints the isolated log path, PowerShell environment command, Streamlit command, and review/export commands. Verify script usage before running if the CLI has changed.

After the run, use the printed review or export command. The script currently emits suggested output paths under `data/pilot/exports/`.

## How to find output artifacts after the pilot

- Fresh pilot event log: use the path printed by `scripts/pilot_isolated_run.py prepare`.
- Suggested review export: under `data/pilot/exports/`.
- Manual observation intake: `data/gate_2_protected_preview_packets/reports/bereishis_perek_3_limited_post_preview_observation_intake.md`.
- Rubric: `docs/review/question_quality_rubric.md`.

## Pass / revise / fail criteria

Pass means:

- No outside-scope questions.
- No repeated broken morphology.
- No repeated bad distractors.
- Students generally understand what the prompt asks.
- Teacher concerns are minor and actionable.

Revise means:

- A question is basically sound but needs wording, spacing, or explanation adjustment.
- A student knows the intended skill but the prompt gets in the way.
- A repeated issue appears but is narrow enough to fix.

Fail means:

- A wrong answer key appears.
- A bad distractor repeatedly misleads students.
- A Hebrew/source/reference problem appears.
- A question measures translation/context when it claims to measure a simpler skill.
- A runtime-scope leak appears.

## What counts as enough evidence

Enough evidence for the next internal decision means:

- 3-5 students completed 8-10 Learn Mode questions each.
- The teacher monitor was open.
- Real observations were recorded.
- Each concern is tied to a candidate/question, pasuk/ref, or prompt family where possible.
- The rubric category and next action are filled in for each observed issue.

One clean observation is useful evidence, but it is not automatic runtime approval.

## What to do immediately after the pilot

1. Export the fresh pilot review using the printed `scripts/pilot_isolated_run.py` command.
2. Fill the observation intake with real evidence only.
3. Classify observations with the rubric.
4. Fix only the top repeated pilot issues.
5. Do not expand runtime until the fresh pilot evidence is reviewed.

## Explicit warning

This pilot does not approve runtime expansion. This pilot does not activate Perek 4. This pilot does not promote any item automatically.
