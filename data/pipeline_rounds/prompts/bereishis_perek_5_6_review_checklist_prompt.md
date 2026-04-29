# Create Compressed Perek 5-6 Teacher-Review Checklist Only

You are working in the chumash-question-engine repo.

Task title: Create compressed Perek 5-6 teacher-review checklist only.

Start from:

- `data/gate_2_source_discovery/bereishis_perek_5_6_review_only_safe_candidate_inventory.tsv`
- `data/gate_2_source_discovery/reports/bereishis_perek_5_6_source_discovery_report.md`
- `data/gate_2_source_discovery/reports/bereishis_perek_5_6_excluded_risk_lanes.md`
- `data/gate_2_source_discovery/reports/bereishis_perek_5_6_duplicate_session_balance_warnings.md`

Purpose: create a compressed teacher-review checklist only. Keep all candidates review-only and all gates false.

Do not:

- activate runtime
- widen active scope
- promote anything to reviewed bank
- create a protected-preview packet
- create student-facing content
- invent teacher decisions
- invent student observations
- mark runtime_allowed true
- mark reviewed_bank_allowed true
- mark protected_preview_allowed true
- mark student_facing_allowed true
- change source truth

Required:

- Preserve source-discovery provenance.
- Include teacher decision fields but leave them blank/null.
- Carry forward duplicate/session-balance warnings.
- Carry forward excluded-risk-lane warnings.
- Create validators and tests.
