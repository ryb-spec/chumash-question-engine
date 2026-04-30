# Combined Teacher Review + Candidate Planning Checklist Template

## Candidate rows

| candidate_id | target | teacher_review_decision | candidate_planning_decision | risk notes | spacing/balance notes | source follow-up field |
|---|---|---|---|---|---|---|

## Decision values

- approve_for_next_candidate_planning
- approve_with_revision
- advance_to_protected_preview_candidate_review
- hold_for_spacing_or_balance
- needs_source_follow_up
- reject
- source_only

## Required fields

- teacher_review_decision
- candidate_planning_decision
- risk notes
- spacing/balance notes
- source follow-up field
- all gates false

## Safety confirmation

- runtime_allowed=false
- reviewed_bank_allowed=false
- protected_preview_allowed=false unless explicitly appropriate for internal protected-preview artifacts
- student_facing_allowed=false
- perek_activated=false
