# Next Codex Prompt: Perek 4 Limited Protected-Preview Build Gate

You are working in the chumash-question-engine repo.

TASK TITLE:
Build Perek 4 Limited Protected-Preview Candidate Packet from Content Expansion Planning Gate

CURRENT BRANCH:
Use a new branch named feature/perek-4-limited-protected-preview-build-gate.

PURPOSE:
Use the Content Expansion Planning Gate V1 recommendation to build only the next allowed Perek 4 protected-preview/teacher-review artifact set. Do not activate runtime content.

SOURCE PLANNING ARTIFACTS:
- data/pipeline_rounds/content_expansion_planning_gate_2026_04_30.md
- data/pipeline_rounds/content_expansion_planning_gate_2026_04_30.json
- data/content_expansion_planning/content_expansion_candidate_plan_2026_04_30.json
- data/content_expansion_planning/content_expansion_inventory_2026_04_30.json

PRIMARY CANDIDATE:
cepg_primary_bereishis_perek_4_limited_protected_preview_build

STRICT BOUNDARIES:
Do not widen runtime scope. Do not activate any Perek. Do not promote reviewed bank. Do not create public/student-facing content. Do not change scoring/mastery, question generation, question selection, source truth, or Runtime Learning Intelligence weighting. Do not infer question approval from extraction verification.

PRE-FLIGHT:
Run branch/status checks and existing planning validator. Stop if dirty or if validators fail.

WORK PRODUCTS:
1. Create a bounded Perek 4 limited protected-preview build report.
2. Create a machine-readable contract.
3. Preserve revision/hold/blocked items.
4. Add a validator and focused tests.
5. Update README/index entries concisely.
6. Keep all runtime/reviewed-bank/student-facing gates false.

VALIDATION:
Run the new validator, focused tests, source text validation, curriculum extraction validation with git diff, streamlined review process validation, and full pytest.

FINAL RESPONSE:
Report files created/modified, selected Perek 4 items, blockers, validation results, full pytest result, and safety confirmation.
