# Content Expansion Planning Gate V1

## Purpose

Create a planning-only gate that inventories existing content/review evidence, identifies the safest next candidate set, and prepares the next content-build branch without activating or promoting anything.

## Strategic goal: move the project three steps forward

1. Know exactly what content exists and what is safe.
2. Choose the best next expansion target.
3. Create gated artifacts and validators so the next branch can build without guessing.

## What was inspected

- `assessment_scope.py` and active runtime scope metadata
- `data/source_texts/`
- `data/verified_source_skill_maps/`
- `data/gate_2_protected_preview_candidates/`
- `data/gate_2_protected_preview_packets/`
- `data/curriculum_extraction/curriculum_extraction_manifest.json`
- `data/diagnostic_preview/`
- `data/standards/zekelman/`
- runtime-learning and teacher-export readiness gates

## Current active runtime scope, as detected

The current supported runtime scope is `local_parsed_bereishis_1_1_to_3_24`, covering Bereishis 1:1 through Bereishis 3:24. This task did not change that scope.

## Existing content/review inventory summary

The inventory builder created 33 planning rows. Classifications include active-existing runtime scope, source support only, extraction-verified planning-only rows, protected-preview-ready rows, pending teacher-review rows, one reviewed-bank candidate standards artifact, and blocked diagnostic-preview material.

## Source-to-skill map summary

Verified source-to-skill maps are present through Bereishis 3:24, with completion reports for Perek 1, Perek 2, and Perek 3. These maps support planning but do not constitute question approval or runtime authorization.

## Protected preview summary

Protected preview candidate and packet layers exist for Perek 2, Perek 3, Perek 4, and limited Perek 5-6 packets. Protected preview remains distinct from reviewed-bank status and runtime use.

## Diagnostic preview summary

Diagnostic preview artifacts exist for Bereishis 1:1-2:3. The optional diagnostic preview generation test had a pre-implementation idempotency failure, so diagnostic preview is marked blocked as a basis for expansion until that is fixed.

## Trusted-source extraction summary

Curriculum extraction is isolated from runtime. Batch 004 and Batch 005 are reviewed for planning/non-runtime use, while Batch 002 and Batch 003 still need review. Extraction verification does not mean question approval.

## Zekelman Standard 3 coverage summary

Standard 3 artifacts include source verification, teacher review, protected preview, reviewed-bank planning, and reviewed-bank artifacts. This planning gate does not authorize using those artifacts for runtime activation.

## Gaps and blockers

- No runtime authorization beyond the current active Bereishis 1:1-3:24 scope.
- Diagnostic preview generation idempotency should be fixed before using diagnostic preview as an expansion basis.
- Extraction reviewed/planning state is not question approval.
- Protected preview is not reviewed bank.
- Teacher review artifacts do not authorize runtime activation without a separate gate.

## Primary recommended expansion candidate

Primary candidate: `cepg_primary_bereishis_perek_4_limited_protected_preview_build`.

This recommends a future Perek 4 limited protected-preview/teacher-review build branch using existing Perek 4 review artifacts and Batch 005 planning evidence. It does not authorize runtime activation.

## Alternate candidates

- `cepg_alt_perek_5_6_clean_two_item_followup`
- `cepg_alt_standard_3_reviewed_bank_alignment_audit`

## Why the primary candidate is safest/highest leverage

Perek 4 is the next contiguous non-runtime Bereishis slice after the active scope. It already has reviewed planning evidence, protected-preview candidates, internal protected-preview packets, and limited packet iteration artifacts. It is more classroom-useful than a tiny two-item follow-up, and more concrete than a standards-only audit.

## What must remain blocked

- Runtime scope expansion
- Perek activation
- Reviewed-bank promotion
- Runtime content promotion
- Diagnostic preview as an expansion basis until generation idempotency is addressed
- Any inference that extraction verification equals question approval

## Required validators for the future content-build branch

- candidate packet validator
- machine-readable contract validator
- no-runtime-activation safety validator
- existing source text and curriculum extraction validators
- focused tests for the new packet/report only

## Required teacher review artifacts for the future content-build branch

- bounded Perek 4 packet/report
- explicit item status table
- revision/hold register
- next-gate authorization
- clear no-runtime safety confirmation

## Why no runtime activation happened in this task

This branch is planning-only. It created inventory, gap, candidate, and next-prompt artifacts only. No active scope file, reviewed-bank file, runtime manifest, source text, or question generation behavior was changed.

## Known limitations

- The inventory is artifact-based and conservative.
- Diagnostic preview generation has a known optional-test issue.
- Standard 3 reviewed-bank artifacts require their own authorization path.
- Perek 4 still needs a separate content-build branch to create the next allowed packet/report.

## Next Codex task recommendation

Use `data/pipeline_rounds/next_codex_prompt_content_build_candidate_2026_04_30.md` to create a future branch: `feature/perek-4-limited-protected-preview-build-gate`.

## Safety confirmation

- no runtime scope expansion
- no Perek activation
- no reviewed-bank promotion
- no runtime content promotion
- no scoring/mastery change
- no question generation change
- no question-selection change
- no Runtime Learning Intelligence weighting change
- no source truth change
- no fake teacher approval
- no fake student data
- no raw log exposure
- no validator weakening
