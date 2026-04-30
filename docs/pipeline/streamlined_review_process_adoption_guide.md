# Streamlined Review Process Adoption Guide

## How to use this for the next Perek batch

Start with Phase 1 and keep each future Perek batch inside the seven-phase process unless a real safety or evidence change requires remediation.

## How to retrofit future Perek 5-6 work without rewriting history

Continue from the latest Perek 5-6 state, but use the streamlined phase names and bundled JSON contracts going forward. Do not retroactively alter historical Perek 2/3/4/5-6 artifacts just to fit the new process.

## When to split a phase

Split only when a human decision, student/internal observation, runtime-safety boundary, or source-confidence status changes outside the current phase.

## When to combine phases

Combine paperwork-only readiness, status-index, duplicate-warning, and register artifacts into the phase bundle when they do not represent a new decision or evidence boundary.

## Examples

- Small clean batch: use Phase 1 through Phase 6 with concise JSON counts and one validator per phase.
- Risky grammar batch: keep grammar risk in Phase 1 and add remediation only if source confidence changes.
- Mixed clean/revision-watch batch: keep revision-watch labels in Phase 6 and decide outcomes in Phase 7.
- Post-pilot remediation batch: create an extra remediation phase only for observed failures or safety leaks.

## Naming conventions

Use `bereishis_perek_<range>_phase_<n>_<short_name>.*` for future phase artifacts and `validate_perek_<range>_phase_<n>_<short_name>.py` for validators.

## Validator and test naming

Use one validator per bundled phase and one matching test file: `tests/test_perek_<range>_phase_<n>_<short_name>.py`.

## Warning

Do not retroactively alter historical Perek 2/3/4/5-6 artifacts just to fit the new process.
