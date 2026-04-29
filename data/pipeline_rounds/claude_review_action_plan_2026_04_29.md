# Claude review action plan — 2026-04-29

## Review context

This artifact records the internal response to a fresh Claude review of the Chumash question engine. It is a project decision record only.

## Claude's central diagnosis

- The app is now a real working prototype.
- Validation discipline is strong.
- The teacher monitor is valuable.
- Reviewed-bank discipline and source-truth safeguards are meaningful.
- The main project risk is that process infrastructure now exceeds the amount of student-usable runtime content.
- The fresh Perek 3 pilot evidence loop is the next bottleneck because the observation intake still has zero real observed rows and zero applied observation decisions.

## Accepted findings

- Treat fresh pilot evidence as the next highest-value bottleneck.
- Keep the teacher monitor central to the next pilot.
- Keep scope expansion frozen until real observations are collected.
- Use a plain-English teacher runbook and rubric rather than adding another abstract gate.
- Preserve current validation and fail-closed safety.

## Findings to defer

- Runtime exposure caps.
- Perek 4 source-review compression.
- Reviewed-bank promotion design.
- Auth/database work.
- Broader standards dashboard grouping.
- Major architecture cleanup.

## Findings rejected for now

- Do not treat the current process infrastructure as proof of student usefulness.
- Do not expand runtime to Perek 4 before fresh Perek 3 evidence.
- Do not refactor engine/flow_builder.py as part of pilot preparation.
- Do not add more gate layers before real observations exist.

## Current hard constraints

- Runtime behavior must not change.
- Active runtime scope must not widen.
- Perek 4 must not be activated.
- No content is approved or promoted by this artifact.
- No observations are invented.
- No fake data is created.

## Active runtime scope finding

`data/corpus_manifest.json` and `assessment_scope.py` indicate the supported active runtime scope is `local_parsed_bereishis_1_1_to_3_24`, ending at Bereishis 3:24. No active Perek 4 runtime scope was found.

## Next 5 major steps

1. Prepare the pilot evidence pack.
2. Run a fresh Perek 3 pilot.
3. Complete the observation intake with real evidence.
4. Fix the top pilot issues only.
5. Then compress the Perek 4 review path without runtime activation.

## Do not do yet

- Do not expand runtime to Perek 4.
- Do not activate Perek 4.
- Do not refactor engine/flow_builder.py.
- Do not add more gate layers.
- Do not build auth/database.
- Do not create new standards layers.
- Do not widen active scope.
- Do not promote Perek 3 or Perek 4 content to runtime.

## Safety statement

This artifact does not change runtime behavior. This artifact does not approve any content. This artifact does not activate Perek 4.
