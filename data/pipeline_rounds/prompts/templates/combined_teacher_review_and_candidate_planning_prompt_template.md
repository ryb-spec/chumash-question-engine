You are working in the chumash-question-engine repo.

TASK TITLE:
Create Combined Teacher Review and Candidate Planning Checklist for PEREK_RANGE

CURRENT BRANCH:
BRANCH_NAME

SCOPE:
PEREK_RANGE

SOURCE INVENTORY:
SOURCE_INVENTORY_PATH

COUNTS:
- CANDIDATE_COUNT
- ELIGIBLE_IDS
- HELD_IDS
- BLOCKED_IDS

NEXT ALLOWED TASK:
NEXT_ALLOWED_TASK

HARD BOUNDARIES:
Do not activate runtime. Do not widen active scope. Do not promote reviewed-bank content. Do not create student-facing content. Do not invent fake decisions. Do not invent fake observations.

PROCESS REQUIREMENTS:
- Use one phase validator for this bundled phase.
- Treat the phase JSON as source of truth for counts, gates, decisions, and next allowed task.
- Create tests for the phase validator.
- Run full pytest.
- Provide final safety confirmation.
