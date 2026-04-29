You are working in the chumash-question-engine repo.

TASK TITLE:
Begin Bereishis Perek 4 source-to-skill discovery and review-only safe candidate inventory.

This is source-discovery and candidate-inventory work only.
It is not runtime work.
It is not reviewed-bank promotion.
It is not student-facing content.
It is not protected-preview packet creation.

Pre-flight:
1. Run `git branch --show-current` and `git status --short`.
2. If the worktree is dirty, stop and report dirty files with no modifications.
3. Continue only on a clean feature branch.
4. Confirm the Perek 3 to Perek 4 launch gate exists at `data/pipeline_rounds/bereishis_perek_3_to_perek_4_launch_gate.md`.

Goal:
Create a Bereishis Perek 4 source-to-skill discovery and safe-candidate inventory. Do not create a protected-preview packet unless a later explicit task asks for it.

Scope:
- Perek 4 only, not Perek 4 and 5 together.
- Use existing source/provenance layers only.
- Prioritize basic noun recognition and clear source-backed vocabulary.
- Include duplicate-token/session-balance warnings early.
- Preserve source/provenance for every candidate.
- Keep every row review-only and fail-closed.

Avoid:
- runtime activation
- reviewed-bank promotion
- student-facing content
- protected-preview packet creation
- broad candidate generation
- fake expansion
- translation/context unless explicitly source-backed and reviewed later
- suffix/compound morphology unless already reviewed and safe
- advanced verbs
- vav hahipuch
- Rashi/commentary
- higher-order comprehension

Expected artifacts:
- Perek 4 source-discovery report
- Perek 4 review-only safe candidate inventory TSV
- duplicate-token/session-balance warning report
- validator/test updates for review-only closed gates

Validation:
Run relevant validators, the curriculum quality orchestrator, targeted tests, curriculum extraction guard, and full pytest.

Final safety statement:
Confirm no runtime activation, no reviewed-bank promotion, no protected-preview packet, no student-facing content, and no Perek 4 candidates promoted beyond review-only inventory.

## Validation phrase ledger

- source-to-skill discovery only
- review-only safe candidate inventory
- avoid runtime
- avoid reviewed-bank promotion
- avoid student-facing content
- avoid packet creation unless explicitly asked later
- include duplicate-token/session-balance warnings
- Keep every row review-only and fail-closed.
