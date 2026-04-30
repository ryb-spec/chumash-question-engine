# Combined Decisions Applied Template

## Applied decisions table

| candidate_id | teacher_review_decision | candidate_planning_decision | eligible_next_gate | required_revision_or_note |
|---|---|---|---|---|

## Eligible next-gate rows

- ELIGIBLE_IDS:

## Held/source-follow-up register

- HELD_IDS:
- BLOCKED_IDS:

## Machine-readable JSON requirements

- decision_counts
- eligible_candidate_ids
- held_candidate_ids
- blocked_candidate_ids
- next_allowed_task
- safety fields

## Validation requirements

One phase validator must compare table counts, JSON counts, eligible IDs, held IDs, blocked IDs, and safety fields.

## Safety confirmation

- runtime_allowed=false
- reviewed_bank_allowed=false
- protected_preview_allowed=false unless explicitly appropriate for internal protected-preview artifacts
- student_facing_allowed=false
- perek_activated=false
