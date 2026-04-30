# Next Codex Prompt: Broad Vocabulary Teacher Review Packet V1

You are working in the chumash-question-engine repo.

TASK TITLE:
Build Broad Vocabulary Teacher Review Packet V1

CURRENT BRANCH:
Use a new branch named `feature/broad-vocabulary-teacher-review-packet-v1`.

PURPOSE:
Create a teacher review packet for Broad Safe Vocabulary Bank V1 and Simple Vocabulary Question Candidate Lane V1. This task records review prompts only; it must not create fake decisions or promote any content.

SOURCE ARTIFACTS:
- `data/vocabulary_bank/bereishis_perek_4_broad_safe_vocabulary_bank_2026_04_30.tsv`
- `data/question_candidate_lanes/bereishis_perek_4_simple_vocabulary_question_candidates_2026_04_30.tsv`
- `data/question_candidate_lanes/bereishis_perek_4_simple_vocabulary_question_candidate_blockers_2026_04_30.tsv`
- `data/pipeline_rounds/simple_vocabulary_question_candidate_lane_v1_2026_04_30.json`

STRICT BOUNDARIES:
Do not create teacher decisions. Do not create fake approval. Do not promote protected preview. Do not promote reviewed bank. Do not create runtime questions. Do not widen runtime scope. Do not activate Perek 4, 5, or 6. Do not change scoring/mastery, question generation, question selection, source truth, or Runtime Learning Intelligence weighting.

WORK PRODUCTS:
- Create a Markdown teacher review packet for word-level vocabulary items, simple question candidates, and revision/watch items.
- Create a machine-readable review packet contract.
- Include yes/no/needs-revision fields for Yossi to complete later.
- Add a validator and focused tests.
- Update README/index entries concisely.
- Keep all runtime, reviewed-bank, protected-preview, and student-facing gates closed.

VALIDATION:
Run the new validator, focused tests, source text validation, curriculum extraction validation with git diff, streamlined review process validation, and full pytest.

FINAL RESPONSE:
Report files created/modified, review packet contents, blocked items, validation results, full pytest result, and safety confirmation.
