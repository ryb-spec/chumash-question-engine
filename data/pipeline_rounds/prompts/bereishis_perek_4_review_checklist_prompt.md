You are working in the chumash-question-engine repo.

TASK TITLE:
Create Bereishis Perek 4 teacher/source review checklist from review-only inventory.

Use these source-discovery artifacts as source of truth:

- data/gate_2_source_discovery/bereishis_perek_4_review_only_safe_candidate_inventory.tsv
- data/gate_2_source_discovery/reports/bereishis_perek_4_source_discovery_report.md
- data/gate_2_source_discovery/reports/bereishis_perek_4_duplicate_session_balance_warnings.md
- data/gate_2_source_discovery/reports/bereishis_perek_4_excluded_risk_lanes.md
- data/gate_2_source_discovery/reports/bereishis_perek_4_source_discovery_status_index.md

Create a teacher/source review checklist only. Do not create a Perek 4 protected-preview packet. Do not activate runtime. Do not promote anything to reviewed bank. Do not create student-facing content. Keep runtime_allowed=false, reviewed_bank_allowed=false, protected_preview_allowed=false, student_facing_allowed=false, and broader_use_allowed=false for every row.

The checklist should include every review-only inventory row, source/provenance fields, duplicate-token/session-balance warnings, and blank teacher decision fields. It should ask the reviewer to verify Hebrew token accuracy, phrase/context accuracy, whether each token is truly a simple noun, whether the skill family is appropriate, whether repeated-token clusters should be spaced or excluded, and whether any row should remain source-only.

Add validator/test coverage and run:

- python scripts/validate_perek_4_source_discovery.py
- python scripts/run_curriculum_quality_checks.py
- python -m pytest tests/test_perek_4_source_discovery.py
- python -m pytest

Do not revise item content, create packets, approve broader use, include Perek 5, or weaken validators.
