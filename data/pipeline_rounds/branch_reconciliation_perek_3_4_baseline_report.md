# Branch reconciliation and merge-forward plan for Perek 3/Perek 4 quality-control baseline

## Purpose

This is branch reconciliation and merge-forward planning only.

- No content generation.
- No runtime activation.
- No reviewed-bank promotion.
- No student-facing content.
- No branch deletion.
- No force push.

## Current branch and status

- Current branch: `chore/branch-reconciliation-perek-3-4-baseline`
- Started from: `feature/perek-3-pilot-evidence-pack`
- Main branch used for comparison: `main`
- Pre-report worktree status: clean
- `git fetch origin`: passed
- Source integrity gate: passed before report creation

## Branch inventory

| Branch | Exists | Latest SHA | Latest message | Merged into main | Merged into current | Ahead/behind main | Unique work | Merge safety note |
|---|---:|---|---|---:|---:|---|---:|---|
| `audit/overnight-curriculum-quality-review` | yes | `01c373b` | Govern overnight curriculum audit artifacts | no | no | ahead 21 / behind 0 | yes | merge early; governs audit artifact location and guard rules |
| `fix/curriculum-quality-control-center` | yes | `f7d8916` | Add curriculum quality control center | no | no | ahead 22 / behind 0 | yes | depends on audit branch; introduces orchestrator and quality reports |
| `feature/perek-3-approved-protected-preview-packet` | yes | `8671330` | Create Bereishis Perek 3 internal protected-preview packet | no | no | ahead 23 / behind 0 | yes | depends on quality-control/Gate 2 baseline |
| `feature/perek-3-internal-review-checklist` | yes | `dad75cb` | Add Perek 3 internal protected-preview review checklist | no | no | ahead 24 / behind 0 | yes | depends on Perek 3 packet |
| `feature/perek-3-internal-review-decisions` | yes | `5f78d83` | Record Perek 3 internal protected-preview review decisions | no | no | ahead 25 / behind 0 | yes | depends on review checklist |
| `feature/perek-3-item-004-revision-plan` | yes | `ce64f74` | Add Perek 3 item 004 revision plan | no | no | ahead 26 / behind 0 | yes | depends on applied review decisions |
| `feature/perek-3-limited-post-preview-readiness` | yes | `991e28f` | Add Perek 3 limited post-preview readiness lane | no | no | ahead 27 / behind 0 | yes | depends on item 004 revision plan |
| `feature/perek-3-limited-reviewer-handoff` | yes | `e51843c` | Add Perek 3 limited post-preview reviewer handoff | no | no | ahead 28 / behind 0 | yes | depends on readiness lane |
| `feature/perek-3-completion-and-perek-4-launch-gate` | yes | `1572b05` | Complete Perek 3 governance and prepare Perek 4 launch gate | no | no | ahead 29 / behind 0 | yes | depends on Perek 3 handoff; likely overlaps pilot intake/status docs |
| `feature/perek-4-source-discovery-inventory` | yes | `ce00510` | Add Perek 4 source discovery inventory | no | no | ahead 30 / behind 0 | yes | depends on Perek 3 completion/launch gate |
| `feature/perek-3-pilot-evidence-pack` | yes | `f27f7c4` | Add Perek 3 pilot evidence pack | no | yes | ahead 1 / behind 0 | yes | current branch already contains it; merge last into integration baseline |

## Artifact presence matrix

| Group | Current branch | Main | Other local branches containing group | Status |
|---|---|---|---|---|
| Quality-control center | missing | missing | `fix/curriculum-quality-control-center` and later Perek 3/Perek 4 branches | branch drift confirmed |
| Gate 2 protected-preview validators | missing | missing | `audit/overnight-curriculum-quality-review` and later Perek 3/Perek 4 branches | branch drift confirmed |
| Perek 3 packet/review chain | mostly missing; pilot intake only is present | missing | `feature/perek-3-approved-protected-preview-packet` through `feature/perek-4-source-discovery-inventory` | current branch is not the Perek 3 governance baseline |
| Perek 4 source-discovery work | missing | missing | `feature/perek-4-source-discovery-inventory` | do not recreate here; merge after Perek 3 completion chain |
| Perek 3 pilot evidence pack | present | missing | `feature/perek-3-pilot-evidence-pack` | current branch contains pilot evidence pack only |

## Source integrity result

- Command: `python scripts/validate_source_texts.py`
- Result: passed
- Canonical SHA-256: `4d96c615ab63e0419bff079db250d71ea9b5de266ff9ab8d589ae80e4afd0b71`
- Command: `python -m pytest tests/test_source_texts_validation.py -q`
- Result: passed, `14 passed`
- `data/source_texts/bereishis_hebrew_menukad_taamim.tsv` dirty status: clean
- Source validation remains strict.
- No source-truth files were modified.

## Validator baseline result

| Command | Result | Note |
|---|---|---|
| `python scripts/run_curriculum_quality_checks.py` | skipped | script missing on current branch; present on `fix/curriculum-quality-control-center` and later branches |
| `python scripts/validate_pipeline_rounds.py` | skipped | script missing on current branch |
| `python scripts/validate_gate_2_protected_preview_candidates.py` | skipped | script missing on current branch; present on audit/quality-control/Perek 3 chain branches |
| `python scripts/validate_gate_2_protected_preview_packet.py` | skipped | script missing on current branch; present on audit/quality-control/Perek 3 chain branches |
| `python scripts/validate_perek_4_source_discovery.py` | skipped | script missing on current branch; present on `feature/perek-4-source-discovery-inventory` |
| `python scripts/validate_perek_3_pilot_evidence_pack.py` | passed | current branch contains pilot evidence validator |
| `python scripts/validate_curriculum_extraction.py` | passed | `valid: true` |
| `python scripts/validate_curriculum_extraction.py --check-git-diff` | passed | `valid: true`, no dirty paths before report creation |
| `python -m pytest tests/test_curriculum_quality_checks.py` | skipped | test missing on current branch |
| `python -m pytest tests/test_gate_2_protected_preview_candidates.py` | skipped | test missing on current branch |
| `python -m pytest tests/test_gate_2_protected_preview_packet.py` | skipped | test missing on current branch |
| `python -m pytest tests/test_perek_4_source_discovery.py` | skipped | test missing on current branch |
| `python -m pytest tests/test_perek_3_pilot_evidence_pack.py` | passed | `6 passed` |
| `python -m pytest tests/test_curriculum_extraction_validation.py tests/test_diagnostic_preview_validation.py` | passed | `44 passed` |
| `python -m pytest` | passed | `581 passed` |

## Missing validator/artifact explanation

The current branch is not stale in the sense of failing its own tests, but it is incomplete relative to the newer quality-control baseline. It contains the Perek 3 pilot evidence pack on top of `main`, while the larger Perek 3/Perek 4 governance chain lives on separate local branches.

Likely source branches for missing work:

- Quality-control center: `fix/curriculum-quality-control-center`
- Gate 2 protected-preview validators: `audit/overnight-curriculum-quality-review` and `fix/curriculum-quality-control-center`
- Perek 3 packet/review chain: ordered Perek 3 feature branches from packet through completion/launch gate
- Perek 4 source-discovery work: `feature/perek-4-source-discovery-inventory`

## Likely conflict areas

Likely overlaps when merging the pilot evidence pack after the Perek 3/Perek 4 chain:

- `data/pipeline_rounds/README.md`
- `scripts/validate_curriculum_extraction.py`
- `tests/test_curriculum_extraction_validation.py`
- `tests/test_source_texts_validation.py`
- `data/gate_2_protected_preview_packets/reports/bereishis_perek_3_limited_post_preview_observation_intake.md`

These are planning/docs/validator-test conflicts, not runtime conflicts. Resolve by preserving the richer Perek 3/Perek 4 governance artifacts and adding the pilot evidence pack instructions/validator as a final layer.

## Proposed merge-forward order

| Order | Branch | Dependency | Risk | Validation after merge |
|---:|---|---|---|---|
| 1 | `audit/overnight-curriculum-quality-review` | none | medium: many governance/report paths | `python scripts/validate_curriculum_extraction.py --check-git-diff`; `python -m pytest tests/test_curriculum_extraction_validation.py` |
| 2 | `fix/curriculum-quality-control-center` | audit branch | medium: adds orchestrator/generated reports | `python scripts/run_curriculum_quality_checks.py`; `python -m pytest tests/test_curriculum_quality_checks.py` |
| 3 | `feature/perek-3-approved-protected-preview-packet` | quality-control center | medium: Gate 2 packet paths/validators | Gate 2 validators and packet tests |
| 4 | `feature/perek-3-internal-review-checklist` | Perek 3 packet | low-medium | Gate 2 packet validator/tests |
| 5 | `feature/perek-3-internal-review-decisions` | checklist | low-medium | Gate 2 packet validator/tests |
| 6 | `feature/perek-3-item-004-revision-plan` | decisions | low-medium | Gate 2 packet validator/tests |
| 7 | `feature/perek-3-limited-post-preview-readiness` | item 004 revision plan | medium | Gate 2 packet validator/tests |
| 8 | `feature/perek-3-limited-reviewer-handoff` | readiness lane | medium | Gate 2 packet validator/tests |
| 9 | `feature/perek-3-completion-and-perek-4-launch-gate` | reviewer handoff | medium-high: status/index artifacts | Gate 2 validators, curriculum quality checks, full pytest |
| 10 | `feature/perek-4-source-discovery-inventory` | Perek 3 launch gate | medium: source-discovery validator/report paths | `python scripts/validate_perek_4_source_discovery.py`; Perek 4 source-discovery tests |
| 11 | `feature/perek-3-pilot-evidence-pack` | should come after Perek 3/Perek 4 baseline | medium-high: README, allowlist, observation intake overlap | pilot evidence validator/tests, curriculum guard, full pytest |

## Go/no-go recommendation

- Merging pilot evidence pack forward: Go, but only after integrating the quality-control/Perek 3/Perek 4 chain in order.
- Perek 4 source-review checklist: No-Go until `feature/perek-4-source-discovery-inventory` is merged and validated.
- Runtime activation: No-Go.
- Reviewed-bank promotion: No-Go.
- Student-facing content: No-Go.

## Next exact commands for Yossi

Recommended integration branch path:

```powershell
git switch main
git pull --ff-only origin main
git switch -c integration/perek-3-4-quality-control-baseline

git merge --no-ff audit/overnight-curriculum-quality-review
python scripts/validate_curriculum_extraction.py --check-git-diff
python -m pytest tests/test_curriculum_extraction_validation.py

git merge --no-ff fix/curriculum-quality-control-center
python scripts/run_curriculum_quality_checks.py
python -m pytest tests/test_curriculum_quality_checks.py

git merge --no-ff feature/perek-3-approved-protected-preview-packet
git merge --no-ff feature/perek-3-internal-review-checklist
git merge --no-ff feature/perek-3-internal-review-decisions
git merge --no-ff feature/perek-3-item-004-revision-plan
git merge --no-ff feature/perek-3-limited-post-preview-readiness
git merge --no-ff feature/perek-3-limited-reviewer-handoff
git merge --no-ff feature/perek-3-completion-and-perek-4-launch-gate
python scripts/validate_gate_2_protected_preview_candidates.py
python scripts/validate_gate_2_protected_preview_packet.py
python -m pytest tests/test_gate_2_protected_preview_candidates.py tests/test_gate_2_protected_preview_packet.py

git merge --no-ff feature/perek-4-source-discovery-inventory
python scripts/validate_perek_4_source_discovery.py
python -m pytest tests/test_perek_4_source_discovery.py

git merge --no-ff feature/perek-3-pilot-evidence-pack
python scripts/validate_perek_3_pilot_evidence_pack.py
python -m pytest tests/test_perek_3_pilot_evidence_pack.py
python scripts/validate_curriculum_extraction.py --check-git-diff
python -m pytest
```

If any merge conflicts, stop, inspect only the conflicted paths, resolve conservatively, and rerun that branch's validator/test slice before continuing.

## Safety boundary confirmation

- No runtime activation.
- No active scope change.
- No reviewed-bank promotion.
- No student-facing content.
- No source-truth changes.
- No validators weakened.
- No branch deletion.
- No force push.
