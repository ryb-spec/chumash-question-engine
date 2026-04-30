# Next Codex Prompt: Perek 4 Broad Vocabulary Post-Preview Decisions V1

You are working in the chumash-question-engine repo.

TASK TITLE:
Apply Perek 4 Broad Vocabulary Post-Preview Review and Observation Decisions V1

CURRENT BRANCH:
Use a new branch named `feature/perek-4-broad-vocabulary-post-preview-decisions-v1`.

PURPOSE:
Apply only real completed internal review checklist decisions and/or real observation evidence for the Perek 4 Broad Vocabulary Internal Protected-Preview Packet V1.

REQUIRED INPUTS:
- `data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_review_checklist_2026_04_30.tsv`
- `data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_observation_template_2026_04_30.tsv`
- `data/gate_2_protected_preview_packets/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.tsv`

STRICT RULES:
- Stop if review checklist rows are blank or pending and no explicit Yossi instruction supplies decisions.
- Stop if observation rows are blank and the task asks to apply observation evidence.
- Do not infer observations.
- Do not create fake teacher approval.
- Do not create fake observation evidence.
- Do not promote reviewed bank unless explicitly approved and separately gated.
- Do not activate runtime.
- Do not widen runtime scope.
- Do not create app-consumable runtime questions.

WORK PRODUCTS:
- Create decision-applied report and JSON.
- Preserve unresolved rows as held or revision-required.
- Create validator and focused tests.
- Update README/index entries concisely.

VALIDATION:
Run the new validator, focused tests, source text validation, curriculum extraction validation with git diff, streamlined review process validation, and full pytest.

FINAL RESPONSE:
Report real decisions/evidence applied, unresolved rows, validation results, full pytest result, and safety confirmation.

