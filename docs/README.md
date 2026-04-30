# Documentation index

## Pilot evidence

- Perek 3 fresh pilot runbook: `pilots/perek_3_fresh_pilot_runbook.md`
- Question quality rubric: `review/question_quality_rubric.md`
- School-facing pilot brief: `product/bhh_chumash_ai_pilot_one_page_brief.md`

These documents are pilot-evidence materials only. They do not change runtime behavior, activate Perek 4, promote reviewed-bank content, or create student-facing content.

## Streamlined review process V1

- Process standard: `pipeline/streamlined_review_process_v1.md`
- Process contract JSON: `pipeline/streamlined_review_process_v1.json`
- Adoption guide: `pipeline/streamlined_review_process_adoption_guide.md`
- Reusable templates: `pipeline/templates/`
- Prompt templates: `../data/pipeline_rounds/prompts/templates/`
- Validator/test: `../scripts/validate_streamlined_review_process.py` and `../tests/test_streamlined_review_process.py`

Status: documentation-only future process standard. It does not change runtime, reviewed-bank, protected-preview packet content, or student-facing behavior.

## Runtime learning intelligence V1

- Runtime guide: `runtime/runtime_learning_intelligence_v1.md`
- Policy/audit artifacts: `../data/pipeline_rounds/runtime_learning_intelligence_policy_2026_04_30.json` and `../data/pipeline_rounds/runtime_learning_intelligence_audit_2026_04_30.md`
- Runtime exposure report: `../data/validation/runtime_learning_intelligence_report.md`
- Validator/test: `../scripts/validate_runtime_learning_intelligence.py` and `../tests/test_runtime_learning_intelligence.py`
- Manual smoke test evidence: `../data/pipeline_rounds/runtime_learning_intelligence_manual_smoke_test_2026_04_30.md` and `../data/pipeline_rounds/runtime_learning_intelligence_manual_smoke_test_2026_04_30.json`
- Smoke test validator/test: `../scripts/validate_runtime_learning_intelligence_smoke_test.py` and `../tests/test_runtime_learning_intelligence_smoke_test.py`
- Teacher-facing Runtime Exposure Center: `../data/pipeline_rounds/teacher_facing_runtime_exposure_center_2026_04_30.md`
- Exposure center validator/test: `../scripts/validate_teacher_facing_runtime_exposure_center.py` and `../tests/test_teacher_facing_runtime_exposure_center.py`

- Small-pool fallback test evidence: `../data/pipeline_rounds/runtime_learning_intelligence_small_pool_fallback_test_2026_04_30.md` and `../data/pipeline_rounds/runtime_learning_intelligence_small_pool_fallback_test_2026_04_30.json`
- Product-readiness gate: `../data/pipeline_rounds/runtime_learning_intelligence_v1_product_readiness_gate_2026_04_30.md` and `../data/pipeline_rounds/runtime_learning_intelligence_v1_product_readiness_gate_2026_04_30.json`
- Post-fallback roadmap and next prompt: `../data/pipeline_rounds/runtime_learning_intelligence_post_fallback_product_roadmap_2026_04_30.md` and `../data/pipeline_rounds/prompts/teacher_lesson_session_setup_v1_prompt.md`
- Product-readiness validator/test: `../scripts/validate_runtime_learning_intelligence_product_readiness.py` and `../tests/test_runtime_learning_intelligence_product_readiness.py`

Status: runtime weighting improvement plus teacher-facing observability. It uses local attempt history to reduce repetition and display exposure summaries without changing active scope, reviewed-bank status, scoring/mastery, source truth, auth, database, or PII.

## Teacher Lesson / Session Setup V1

- Runtime guide: `runtime/teacher_lesson_session_setup_v1.md`
- Implementation report/JSON: `../data/pipeline_rounds/teacher_lesson_session_setup_v1_2026_04_30.md` and `../data/pipeline_rounds/teacher_lesson_session_setup_v1_2026_04_30.json`
- Validator/test: `../scripts/validate_teacher_lesson_session_setup.py` and `../tests/test_teacher_lesson_session_setup.py`

Status: local teacher session-context setup only. It does not add auth, database, PII, content, runtime scope expansion, scoring/mastery changes, or question-selection changes.

## Teacher Runtime Evidence Export Suite V1

- Implementation report/JSON: `../data/pipeline_rounds/teacher_runtime_exposure_export_report_2026_04_30.md` and `../data/pipeline_rounds/teacher_runtime_exposure_export_report_2026_04_30.json`
- Export helper: `../runtime/teacher_runtime_export.py`
- UI helper: `../ui/teacher_runtime_export.py`
- Validator/test: `../scripts/validate_teacher_runtime_exposure_export.py` and `../tests/test_teacher_runtime_exposure_export.py`

Status: local teacher report/export layer only. It saves Markdown and JSON runtime exposure reports without changing runtime scope, question selection, weighting, scoring/mastery, question generation, reviewed-bank status, source truth, auth, database, PII, raw-log exposure, or student-facing content.

- Teacher Runtime Export Session Accuracy V1: documents planned lesson focus as a report label only, current-session bounded reports when identifiers are available, teacher-setup-window fallback, Recent local history diagnostic fallback, one export snapshot for Markdown/JSON, No raw logs, No login, No database, No PII, No scoring/mastery changes, and No runtime scope expansion.

- Content Expansion Planning Gate V1: planning-only inventory/readiness map and Perek 4 protected-preview build recommendation. Artifacts live in `data/content_expansion_planning/` and `data/pipeline_rounds/content_expansion_planning_gate_2026_04_30.*`; no runtime activation, reviewed-bank promotion, source truth change, question-generation change, or scope widening.

- Broad Safe Vocabulary Bank V1: word-level vocabulary approval lane only. Artifacts live in `../data/vocabulary_bank/` and `../data/pipeline_rounds/broad_safe_vocabulary_bank_v1_2026_04_30.*`; no question approval, protected-preview promotion, reviewed-bank promotion, runtime activation, or source-truth change.

- Simple Vocabulary Question Candidate Lane V1: teacher-review-only simple question candidates from the broad vocabulary bank. Artifacts live in `../data/question_candidate_lanes/` and `../data/pipeline_rounds/simple_vocabulary_question_candidate_lane_v1_2026_04_30.*`; no runtime questions, protected-preview promotion, reviewed-bank promotion, or runtime activation.

- Broad Vocabulary Teacher Review Packet V1: blank Yossi review prompts for word-level vocabulary items, simple question candidates, and revision/watch items. Artifacts live in `../data/pipeline_rounds/broad_vocabulary_teacher_review_packet_v1_2026_04_30.*`; no decisions, promotion, runtime questions, or runtime activation.

- Broad Vocabulary Teacher Review Decisions V1: applies Yossi's explicit manual decisions as decision artifacts only. Clean simple candidates become eligible only for a future protected-preview candidate gate; revision-required and held rows stay blocked. No runtime questions, protected-preview packet, reviewed-bank movement, or runtime activation.

- Perek 4 Broad Vocabulary Protected-Preview Candidate Gate V1: gates exactly five clean simple vocabulary candidates for future protected-preview packet planning while preserving revision-required and held rows as blocked. No protected-preview packet, reviewed-bank movement, runtime questions, or runtime activation.

- Perek 4 Broad Vocabulary Internal Protected-Preview Packet V1: creates a five-item internal packet plus review checklist, observation template, excluded register, and lineage reconciliation. It does not activate runtime, create student-facing content, or promote reviewed bank.

- Perek 4 Broad Vocabulary Final Observation Gate V1: applies Yossi's final internal observation evidence to five packet items, marks them approved for later reviewed-bank-candidate planning, keeps blocked/revision rows excluded, and leaves runtime activation blocked.
