# Next Codex Prompt: Perek 4 Broad Vocabulary Protected-Preview Candidate Gate V1

You are working in the chumash-question-engine repo.

TASK TITLE:
Build Perek 4 Broad Vocabulary Protected-Preview Candidate Gate V1

CURRENT BRANCH:
Use a new branch named `feature/perek-4-broad-vocabulary-protected-preview-candidate-gate-v1`.

PURPOSE:
Use Yossi's applied Broad Vocabulary Teacher Review decisions to build only a future protected-preview candidate gate for clean eligible Perek 4 simple vocabulary candidates.

SOURCE ARTIFACTS:
- `data/teacher_review_decisions/bereishis_perek_4_broad_vocabulary_teacher_review_decisions_applied_2026_04_30.tsv`
- `data/teacher_review_decisions/bereishis_perek_4_broad_vocabulary_teacher_review_decisions_applied_2026_04_30.json`
- `data/teacher_review_decisions/bereishis_perek_4_broad_vocabulary_future_gate_eligibility_register_2026_04_30.tsv`
- `data/teacher_review_decisions/bereishis_perek_4_broad_vocabulary_future_gate_eligibility_register_2026_04_30.json`

STRICT INPUT SET:
Use only clean eligible rows from the eligibility register:
- `svqcl_p4_001`
- `svqcl_p4_002`
- `svqcl_p4_003`
- `svqcl_p4_005`
- `svqcl_p4_006`

KEEP BLOCKED:
- Revision-required rows: `bsvb_p4_002`, `svqcl_p4_004`
- Held rows: `bsvb_p4_003`, `bsvb_p4_004`, `svqcl_p4_007`, `svqcl_p4_008`, `svqcl_p4_009`

STRICT BOUNDARIES:
Do not activate runtime. Do not widen runtime scope. Do not activate Perek 4, 5, or 6. Do not create a protected-preview packet unless the gate explicitly allows it. Do not promote reviewed bank. Do not create runtime questions. Do not create student-facing content. Do not change scoring/mastery, question generation, question selection, source truth, or Runtime Learning Intelligence weighting.

WORK PRODUCTS:
- Create a protected-preview candidate gate report for the five clean eligible simple candidates only.
- Create a machine-readable candidate gate contract.
- Preserve revision-required and held rows as blocked.
- Add a validator and focused tests.
- Update README/index entries concisely.
- Keep all runtime, reviewed-bank, and student-facing gates closed.

VALIDATION:
Run the new validator, focused tests, source text validation, curriculum extraction validation with git diff, streamlined review process validation, and full pytest.

FINAL RESPONSE:
Report files created/modified, clean eligible rows used, blocked rows preserved, validation results, full pytest result, and safety confirmation.

