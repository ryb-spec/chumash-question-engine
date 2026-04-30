# Streamlined Review Process V1

## Purpose

Create a reusable seven-phase review process for future Perek batches so the project keeps its safety posture while reducing recurring process overhead.

## Why this exists

The current process became too fragmented across Perek 2, Perek 3, Perek 4, and Perek 5-6. The goal is at least 35% fewer repeat steps. Safety gates remain intact: human decisions, observation evidence, runtime boundaries, reviewed-bank promotion, and student-facing release still require explicit gates.

## The old repeated pipeline pattern

The historical pattern often split source discovery, separate risk reports, separate duplicate/session-balance reports, status indexes, teacher review checklists, candidate planning checklists, decisions-applied reports, protected-preview candidate review layers, internal packets, observation gates, and next-Perek gates into many micro-artifacts.

## The new 7-phase process

1. Phase 1: Source Discovery Bundle.
2. Phase 2: Combined Teacher Review + Candidate Planning Checklist.
3. Phase 3: Combined Teacher/Planning Decisions Applied.
4. Phase 4: Protected-Preview Candidate Review + Readiness.
5. Phase 5: Protected-Preview Decisions Applied + Internal Packet Readiness.
6. Phase 6: Internal Packet + Review Checklist.
7. Phase 7: Observation Decisions + Next-Gate Authorization.

## What each phase must produce

- Phase JSON contract with counts, gates, decisions when applicable, blocked/held IDs, and next allowed task.
- One phase validator covering the bundled outputs.
- One focused test file for the phase validator.
- Human-readable report/checklist only when it carries decisions, evidence, risk, or next-task scope.
- Safety confirmation with all required gate fields.

## What each phase must not do

- Do not activate runtime by default.
- Do not allow active scope expansion by default.
- Do not allow reviewed-bank promotion by default.
- Do not allow student-facing content by default.
- Do not invent teacher decisions, student observations, source truth, or pilot data.
- Do not create standalone readiness/index artifacts when the phase JSON/report already carries the same status.

## Required safety fields for every phase

- runtime_allowed=false
- reviewed_bank_allowed=false
- protected_preview_allowed=false unless explicitly appropriate for internal protected-preview artifacts
- student_facing_allowed=false
- perek_activated=false

## Core rule

No separate gate unless a human decision, student/internal observation, runtime-safety boundary, or source-confidence status changes.

## What may be combined

- Source discovery report, excluded-risk lanes, duplicate/session-balance warnings, status index, and summary JSON may be one Source Discovery Bundle.
- Teacher review and candidate planning may share one checklist when the same human can decide both.
- Teacher-review and planning decisions may be applied in one decision-applied phase.
- Protected-preview candidate review may include readiness summary and revision/hold register.
- Internal packet and internal review checklist should usually be one phase.

## What may not be combined

- Runtime/reviewed-bank/student-facing promotion may not be combined with source, candidate, or packet planning.
- Observation decisions may not be invented or bundled before evidence exists.
- Source-confidence changes require explicit reporting.
- Remediation that changes item wording, source confidence, or safety status must be explicit.

## When to add an extra remediation phase

Add one only when evidence shows a source-truth issue, unsafe distractor/wording issue, leaked excluded scope, changed runtime-safety boundary, or teacher-requested repair that cannot be safely captured in the next normal phase.

## When next-Perek source discovery may begin

Next-Perek source discovery may begin after Phase 7 authorizes source discovery only, or after Yossi explicitly overrides with written boundaries. It must remain review-only unless a later explicit runtime gate exists.

## Explicit runtime boundary

Runtime/reviewed-bank/student-facing promotion always requires a separate later task.
