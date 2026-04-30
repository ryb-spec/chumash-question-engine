from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "curriculum_extraction"
MANIFEST_PATH = DATA_DIR / "curriculum_extraction_manifest.json"
REGISTRY_PATH = DATA_DIR / "source_resource_registry.json"
PREVIEW_DIR = DATA_DIR / "generated_questions_preview"

COMMON_REQUIRED_FIELDS = (
    "id",
    "schema_version",
    "record_type",
    "extraction_batch_id",
    "source_package_id",
    "source_trace",
    "review_status",
    "runtime_status",
    "confidence",
    "extraction_quality_flags",
)

PREVIEW_REQUIRED_FIELDS = (
    "id",
    "schema_version",
    "record_type",
    "source_record_id",
    "source_package_id",
    "question_type",
    "prompt",
    "answer",
    "distractors",
    "skill_tags",
    "source_trace",
    "review_status",
    "runtime_status",
    "confidence",
)

SOURCE_TRACE_REQUIRED_FIELDS = (
    "source_name",
    "source_file",
    "source_page_start",
    "source_page_end",
    "source_section",
    "source_ref",
    "source_snippet_raw",
    "source_snippet_normalized",
    "extraction_method",
    "extraction_note",
    "source_has_answer_key",
    "review_status",
)

ANSWER_STATUS_VALUES = {
    "source_provided",
    "inferred_needs_review",
    "not_provided",
    "not_extracted",
    "not_applicable",
}

EXPECTED_RECORD_TYPES = {
    "data/curriculum_extraction/samples/pasuk_segments.sample.jsonl": "pasuk_segment",
    "data/curriculum_extraction/samples/word_parse.sample.jsonl": "word_parse",
    "data/curriculum_extraction/samples/word_parse_tasks.sample.jsonl": "word_parse_task",
    "data/curriculum_extraction/samples/vocab_entries.sample.jsonl": "vocab_entry",
    "data/curriculum_extraction/samples/comprehension_questions.sample.jsonl": "comprehension_question",
    "data/curriculum_extraction/samples/question_templates.sample.jsonl": "question_template",
    "data/curriculum_extraction/samples/skill_tags.sample.jsonl": "skill_tag",
    "data/curriculum_extraction/samples/translation_rules.sample.jsonl": "translation_rule",
    "data/curriculum_extraction/normalized/linear_chumash_bereishis_1_1_to_1_5_pasuk_segments.seed.jsonl": "pasuk_segment",
    "data/curriculum_extraction/normalized/linear_chumash_translation_rules.seed.jsonl": "translation_rule",
    "data/curriculum_extraction/normalized/pasuk_coming_to_teach_word_parse.seed.jsonl": "word_parse",
    "data/curriculum_extraction/normalized/bacharach_shemos_prefix_suffix_tasks.seed.jsonl": "word_parse_task",
    "data/curriculum_extraction/normalized/bacharach_vaeira_comprehension_questions.seed.jsonl": "comprehension_question",
    "data/curriculum_extraction/normalized/vocabulary_priority_pack.seed.jsonl": "vocab_entry",
    "data/curriculum_extraction/normalized/batch_002_linear_chumash_bereishis_1_6_to_2_3_pasuk_segments.jsonl": "pasuk_segment",
    "data/curriculum_extraction/normalized/batch_002_linear_chumash_translation_rules.jsonl": "translation_rule",
    "data/curriculum_extraction/normalized/batch_003_linear_chumash_bereishis_2_4_to_2_25_pasuk_segments.jsonl": "pasuk_segment",
    "data/curriculum_extraction/normalized/batch_004_linear_chumash_bereishis_3_1_to_3_24_pasuk_segments.jsonl": "pasuk_segment",
    "data/curriculum_extraction/normalized/batch_005_linear_chumash_bereishis_4_1_to_4_16_pasuk_segments.jsonl": "pasuk_segment",
}

PASUK_SEGMENT_REQUIRED_FIELDS = (
    "canonical_ref",
    "sefer",
    "parsha",
    "perek",
    "pasuk",
    "pasuk_range",
    "segment_order",
    "segment_level",
    "hebrew_raw",
    "hebrew_normalized",
    "english_raw",
    "english_normalized",
    "missing_hebrew_flag",
    "missing_translation_flag",
    "translation_type",
    "parenthetical_clarification",
    "translation_rule_tags",
    "source_footnote_refs",
    "skill_tags",
    "linked_vocab_ids",
    "linked_word_parse_ids",
)

WORD_PARSE_REQUIRED_FIELDS = (
    "canonical_ref",
    "sefer",
    "parsha",
    "perek",
    "pasuk",
    "word_in_pasuk_raw",
    "word_in_pasuk_normalized",
    "base_word",
    "target_shoresh_raw",
    "target_shoresh_normalized",
    "shoresh_meaning",
    "prefixes",
    "suffixes",
    "grammar_features",
    "literal_translation",
    "contextual_translation",
    "answer_status",
    "skill_tags",
)

WORD_PARSE_TASK_REQUIRED_FIELDS = (
    "task_type",
    "sefer",
    "parsha",
    "perek",
    "pasuk",
    "pasuk_range",
    "target_shoresh_raw",
    "target_shoresh_normalized",
    "expected_word_in_pasuk",
    "prefixes",
    "suffixes",
    "answer_status",
    "skill_tags",
)

VOCAB_ENTRY_REQUIRED_FIELDS = (
    "hebrew",
    "normalized_hebrew",
    "entry_type",
    "english_glosses",
    "needs_gloss_review",
    "sefer_scope",
    "frequency_source",
    "frequency_band",
    "global_frequency_band",
    "priority_level",
    "skill_tags",
)

COMPREHENSION_REQUIRED_FIELDS = (
    "question_type",
    "sefer",
    "parsha",
    "perek",
    "pasuk",
    "quoted_phrase_raw",
    "question_text",
    "expected_answer",
    "answer_status",
    "skill_tags",
)

QUESTION_TEMPLATE_REQUIRED_FIELDS = (
    "template_key",
    "template_title",
    "question_family",
    "prompt_template",
    "expected_answer_type",
    "supported_record_types",
    "skill_tags",
)

SKILL_TAG_REQUIRED_FIELDS = (
    "skill_key",
    "display_name",
    "category",
    "description",
    "normalized_terms",
    "linked_record_types",
)

TRANSLATION_RULE_REQUIRED_FIELDS = (
    "rule_key",
    "rule_name",
    "applies_to_record_type",
    "trigger_text",
    "guidance",
    "example_source_ref",
    "skill_tags",
)

SAMPLE_ALLOWED_METHODS = {"manual_sample"}
NORMALIZED_ALLOWED_METHODS = {"manual_cleaned_excerpt", "manual_sample"}
ALLOWED_REVIEW_STATUSES = {"needs_review", "reviewed"}
ALLOWED_BATCH_STATUSES = {
    "draft_needs_review",
    "cleaned_seed_reviewed_non_runtime",
    "extracted_needs_review",
    "reviewed_for_planning_non_runtime",
}
REVIEWED_BATCH_STATUSES = {
    "cleaned_seed_reviewed_non_runtime",
    "reviewed_for_planning_non_runtime",
}
RECORD_REVIEW_STATUS_BY_BATCH_STATUS = {
    "reviewed_for_planning_non_runtime": "needs_review",
}

ALLOWED_AUDIT_REPORT_PREFIXES = (
    "data/curriculum_extraction/reports/audits/",
)
ALLOWED_AUDIT_REPORT_SUFFIXES = {".md", ".pdf"}

SKILL_TAG_ALIASES = {
    "phrase_translation": {"translation_context", "skill_tag.translation_context"},
    "translation_context": {"translation_context", "skill_tag.translation_context"},
    "word_translation": {"translation_context", "skill_tag.translation_context"},
    "shoresh": {"shoresh_identification", "skill_tag.shoresh_identification"},
    "prefix_suffix": {
        "prefix_meaning",
        "skill_tag.prefix_meaning",
        "suffix_meaning",
        "skill_tag.suffix_meaning",
    },
    "vocabulary": {"vocabulary_priority", "skill_tag.vocabulary_priority"},
    "pasuk_comprehension": {"text_comprehension", "skill_tag.text_comprehension"},
    "al_mi_neemar": {
        "text_comprehension",
        "skill_tag.text_comprehension",
        "phrase_intent",
        "skill_tag.phrase_intent",
    },
    "mi_amar_el_mi": {
        "text_comprehension",
        "skill_tag.text_comprehension",
        "phrase_intent",
        "skill_tag.phrase_intent",
    },
}

ALLOWED_CHANGE_PREFIXES = (
    "data/curriculum_extraction/",
    "data/diagnostic_preview/",
    "data/question_eligibility_audits/",
    "data/gate_2_input_planning/",
    "data/gate_2_pre_generation_review/",
    "data/gate_2_controlled_draft_generation/",
    "data/gate_2_protected_preview_candidates/",
    "data/gate_2_protected_preview_packets/",
    "data/gate_2_source_discovery/",
    "data/gate_2_exact_wording_planning/",
    "data/gate_2_template_skeleton_planning/",
    "data/protected_preview_input_planning/",
        "data/protected_preview_planning_gate/",
        "data/protected_preview_candidates/",
    "data/protected_preview_packets/",
    "data/pre_generation_review/",
    "data/controlled_draft_generation/",
    "data/source_skill_enrichment/",
    "data/sources/loshon_hatorah/",
    "data/standards/zekelman/",
    "data/template_skeleton_planning/",
    "docs/question_templates/",
    "docs/pipeline_rounds/",
    "docs/pipeline/",
    "docs/runtime/",
    "docs/sources/loshon_hatorah/",
)

ALLOWED_CHANGE_EXACT = {
    ".gitignore",
    "README.md",
    "PLANS.md",
    "docs/runtime_skill_canonical_alignment.md",
    "docs/curriculum_extraction_factory.md",
    "docs/curriculum_extraction_integration_plan.md",
    "docs/codex_prompts/batch_006_source_ready_prompt_seed.md",
    "docs/curriculum_pipeline/source_text_foundation_plan.md",
    "docs/curriculum_pipeline/source_text_handoff.md",
    "docs/curriculum_pipeline/source_text_validation_strategy.md",
    "docs/sources/trusted_teacher_source_policy.md",
    "docs/question_templates/approved_question_template_policy.md",
    "runtime/attempt_history.py",
    "runtime/question_identity.py",
    "runtime/question_flow.py",
    "runtime/scope_exhaustion.py",
    "runtime/session_state.py",
    "tests/conftest.py",
    "data/pipeline_rounds/runtime_learning_intelligence_audit_2026_04_30.md",
    "data/pipeline_rounds/runtime_learning_intelligence_policy_2026_04_30.json",
    "data/pipeline_rounds/runtime_learning_intelligence_manual_smoke_test_2026_04_30.md",
    "data/pipeline_rounds/runtime_learning_intelligence_manual_smoke_test_2026_04_30.json",
    "data/pipeline_rounds/runtime_learning_intelligence_next_step_recommendation_2026_04_30.md",
    "data/validation/runtime_learning_intelligence_report.md",
    "data/validation/runtime_learning_intelligence_summary.json",
    "scripts/validate_runtime_learning_intelligence.py",
    "scripts/validate_runtime_learning_intelligence_smoke_test.py",
    "tests/test_runtime_learning_intelligence.py",
    "tests/test_runtime_learning_intelligence_smoke_test.py",
    "scripts/validate_question_eligibility_audit.py",
    "scripts/validate_question_template_wording_policy.py",
    "scripts/validate_template_skeleton_planning.py",
    "scripts/validate_protected_preview_input_list_planning_policy.py",
    "scripts/validate_protected_preview_input_planning.py",
        "scripts/validate_protected_preview_planning_gate.py",
        "scripts/validate_protected_preview_candidates.py",
    "scripts/validate_protected_preview_packet.py",
    "scripts/validate_gate_2_input_planning.py",
    "scripts/validate_gate_2_pre_generation_review.py",
    "scripts/validate_gate_2_controlled_draft_generation.py",
    "scripts/validate_gate_2_protected_preview_candidates.py",
    "scripts/validate_gate_2_protected_preview_packet.py",
    "scripts/validate_gate_2_exact_wording_planning.py",
    "scripts/validate_gate_2_template_skeleton_planning.py",
    "scripts/validate_pipeline_rounds.py",
    "scripts/validate_pre_generation_review.py",
    "scripts/validate_controlled_draft_generation.py",
    "tests/test_question_eligibility_audit.py",
    "tests/test_question_template_wording_policy.py",
    "tests/test_runtime_question_flow.py",
    "tests/test_template_skeleton_planning.py",
    "tests/test_protected_preview_input_list_planning_policy.py",
    "tests/test_protected_preview_input_planning.py",
        "tests/test_protected_preview_planning_gate.py",
        "tests/test_protected_preview_candidates.py",
    "tests/test_protected_preview_packet.py",
    "tests/test_gate_2_input_planning.py",
    "tests/test_gate_2_pre_generation_review.py",
    "tests/test_gate_2_controlled_draft_generation.py",
    "tests/test_gate_2_protected_preview_candidates.py",
    "tests/test_gate_2_protected_preview_packet.py",
    "tests/test_gate_2_exact_wording_planning.py",
    "tests/test_gate_2_template_skeleton_planning.py",
    "tests/test_pipeline_rounds.py",
    "tests/test_pre_generation_review.py",
    "tests/test_controlled_draft_generation.py",
    "docs/README.md",
    "docs/pilots/perek_3_fresh_pilot_runbook.md",
    "docs/product/bhh_chumash_ai_pilot_one_page_brief.md",
    "docs/review/question_quality_rubric.md",
    "local_curriculum_sources/source_key_excerpt_batch_001.md",
    "data/pipeline_rounds/README.md",
    "data/pipeline_rounds/bereishis_perek_3_to_perek_4_launch_gate.json",
    "data/pipeline_rounds/bereishis_perek_3_to_perek_4_launch_gate.md",
    "data/pipeline_rounds/prompts/bereishis_perek_4_review_checklist_prompt.md",
    "data/pipeline_rounds/prompts/bereishis_perek_4_source_discovery_prompt.md",
    "data/pipeline_rounds/prompts/bereishis_perek_5_6_source_discovery_prompt.md",
    "data/pipeline_rounds/prompts/bereishis_perek_5_6_review_checklist_prompt.md",
    "data/pipeline_rounds/prompts/bereishis_perek_5_6_teacher_review_decisions_apply_prompt.md",
    "data/pipeline_rounds/prompts/bereishis_perek_5_6_candidate_planning_review_prompt.md",
    "data/pipeline_rounds/prompts/bereishis_perek_5_6_candidate_planning_decisions_apply_prompt.md",
    "data/pipeline_rounds/prompts/bereishis_perek_5_6_protected_preview_candidate_review_decisions_prompt.md",
    "data/pipeline_rounds/prompts/bereishis_perek_5_6_internal_protected_preview_packet_prompt.md",
    "data/pipeline_rounds/prompts/templates/source_discovery_bundle_prompt_template.md",
    "data/pipeline_rounds/prompts/templates/combined_teacher_review_and_candidate_planning_prompt_template.md",
    "data/pipeline_rounds/prompts/templates/combined_decisions_applied_prompt_template.md",
    "data/pipeline_rounds/prompts/templates/protected_preview_candidate_review_and_readiness_prompt_template.md",
    "data/pipeline_rounds/prompts/templates/protected_preview_decisions_internal_packet_readiness_prompt_template.md",
    "data/pipeline_rounds/prompts/templates/internal_packet_and_review_checklist_prompt_template.md",
    "data/pipeline_rounds/prompts/templates/observation_decisions_next_gate_authorization_prompt_template.md",
    "data/pipeline_rounds/reports/bereishis_perek_2_gate_1_enrichment_decision_status_report.md",
    "data/pipeline_rounds/reports/bereishis_perek_2_gate_1_source_enrichment_eligibility_report.md",
    "data/pipeline_rounds/reports/bereishis_perek_2_gate_1_source_readiness_audit.md",
    "data/pipeline_rounds/reports/bereishis_perek_2_gate_2_candidate_pool_summary.md",
    "data/pipeline_rounds/reports/perek_1_round_1_pipeline_audit.md",
    "data/pipeline_rounds/reports/round_2_starter_checklist.md",
    "data/pipeline_rounds/round_2_fast_track_pipeline_contract.v1.json",
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_3_limited_post_preview_observation_intake.md",
    "data/pipeline_rounds/claude_review_action_plan_2026_04_29.md",
    "data/pipeline_rounds/perek_3_pilot_evidence_manifest_2026_04_29.json",
    "data/pipeline_rounds/perek_3_fresh_pilot_observation_summary_2026_04_29.json",
    "data/pipeline_rounds/perek_3_fresh_pilot_observation_summary_2026_04_29.md",
    "data/pipeline_rounds/perek_3_pilot_remediation_plan_2026_04_29.json",
    "data/pipeline_rounds/perek_3_pilot_remediation_plan_2026_04_29.md",
    "data/pipeline_rounds/perek_3_pilot_remediation_sequence_2026_04_29.md",
    "data/pipeline_rounds/perek_3_pilot_teacher_decision_checklist_2026_04_29.md",
    "data/pipeline_rounds/perek_3_pilot_wording_clarity_fix_report_2026_04_29.md",
    "data/pipeline_rounds/perek_3_pilot_distractor_source_audit_2026_04_29.md",
    "data/pipeline_rounds/perek_3_phrase_translation_distractor_audit_2026_04_29.md",
    "data/pipeline_rounds/perek_3_ashis_shis_source_followup_2026_04_29.md",
    "data/pipeline_rounds/perek_3_pilot_remediation_completion_gate_2026_04_29.md",
    "data/pipeline_rounds/perek_3_pilot_remediation_completion_gate_2026_04_29.json",
    "data/pipeline_rounds/perek_3_yossi_language_decisions_2026_04_29.md",
    "data/pipeline_rounds/perek_3_yossi_language_decisions_2026_04_29.json",
    "data/pipeline_rounds/perek_3_short_repilot_scope_2026_04_29.md",
    "data/pipeline_rounds/perek_3_short_repilot_scope_2026_04_29.json",
    "data/pipeline_rounds/perek_3_short_repilot_enforcement_plan_2026_04_29.md",
    "data/pipeline_rounds/perek_3_short_repilot_enforcement_plan_2026_04_29.json",
    "data/pipeline_rounds/perek_3_short_repilot_manual_checklist_2026_04_29.md",
    "data/pipeline_rounds/perek_3_short_repilot_results_2026_04_29.md",
    "data/pipeline_rounds/perek_3_short_repilot_results_2026_04_29.json",
    "data/pipeline_rounds/perek_3_short_repilot_scope_leak_report_2026_04_29.md",
    "data/pipeline_rounds/perek_3_short_repilot_to_perek_4_ready_gate_2026_04_29.md",
    "data/pipeline_rounds/perek_3_short_repilot_to_perek_4_ready_gate_2026_04_29.json",
    "data/pipeline_rounds/perek_3_short_repilot_scope_leak_fix_report_2026_04_29.md",
    "data/pipeline_rounds/perek_3_to_perek_4_yossi_override_2026_04_29.md",
    "data/pipeline_rounds/perek_3_to_perek_4_yossi_override_2026_04_29.json",
    "data/pipeline_rounds/perek_4_teacher_review_packet_readiness_2026_04_29.md",
    "data/pipeline_rounds/perek_4_post_teacher_review_next_gate_readiness_2026_04_29.md",
    "data/pipeline_rounds/perek_4_candidate_planning_review_checklist_readiness_2026_04_29.md",
    "data/pipeline_rounds/perek_4_candidate_planning_decisions_next_gate_readiness_2026_04_29.md",
    "data/pipeline_rounds/perek_4_internal_protected_preview_packet_readiness_2026_04_29.md",
    "data/pipeline_rounds/perek_4_internal_protected_preview_packet_created_2026_04_29.md",
    "data/pipeline_rounds/perek_4_internal_review_decisions_and_limited_preview_readiness_2026_04_29.md",
    "data/pipeline_rounds/perek_4_limited_internal_preview_next_packet_iteration_readiness_2026_04_29.md",
    "data/pipeline_rounds/perek_4_final_internal_iteration_and_perek_5_6_source_discovery_gate_2026_04_29.json",
    "data/pipeline_rounds/perek_4_final_internal_iteration_and_perek_5_6_source_discovery_gate_2026_04_29.md",
    "data/pipeline_rounds/bereishis_perek_5_6_source_discovery_gate_2026_04_29.md",
    "data/pipeline_rounds/bereishis_perek_5_6_teacher_review_checklist_readiness_2026_04_29.md",
    "data/pipeline_rounds/bereishis_perek_5_6_post_teacher_review_next_gate_readiness_2026_04_29.md",
    "data/pipeline_rounds/bereishis_perek_5_6_candidate_planning_review_checklist_readiness_2026_04_29.md",
    "data/pipeline_rounds/bereishis_perek_5_6_candidate_planning_decisions_next_gate_readiness_2026_04_29.md",
    "data/pipeline_rounds/bereishis_perek_5_6_internal_protected_preview_packet_readiness_2026_04_29.md",
    "data/pipeline_rounds/bereishis_perek_5_6_small_internal_packet_created_2026_04_29.md",
    "data/pipeline_rounds/bereishis_perek_5_6_mixed_internal_review_packet_created_2026_04_29.md",
    "data/pipeline_rounds/bereishis_perek_5_6_review_recommendation_report_2026_04_29.md",
    "data/pipeline_rounds/bereishis_perek_5_6_review_recommendation_report_2026_04_29.json",
    "data/pipeline_rounds/bereishis_perek_5_6_mixed_packet_real_observation_post_gate_2026_04_30.md",
    "data/pipeline_rounds/bereishis_perek_5_6_clean_two_item_iteration_next_gate_2026_04_30.md",
    "data/pipeline_rounds/streamlined_review_process_comparison_2026_04_29.md",
    "data/pipeline_rounds/repo_hygiene_inventory_2026_04_29.md",
    "data/source/bereishis_4_1_to_4_16.json",
    "data/dikduk_rules/README.md",
    "data/dikduk_rules/dikduk_error_pattern.schema.json",
    "data/dikduk_rules/dikduk_question_template.schema.json",
    "data/dikduk_rules/dikduk_rule.schema.json",
    "data/dikduk_rules/dikduk_rules_manifest.json",
    "data/dikduk_rules/question_templates.jsonl",
    "data/dikduk_rules/rule_groups.json",
    "data/dikduk_rules/rules_loshon_foundation.jsonl",
    "data/dikduk_rules/student_error_patterns.jsonl",
    "data/source_texts/bereishis_hebrew_menukad_taamim.tsv",
    "data/source_texts/reports/bereishis_hebrew_menukad_taamim_validation.md",
    "data/source_texts/reports/source_text_gap_report.md",
    "data/source_texts/reports/source_text_inventory.md",
    "data/source_texts/README.md",
    "data/source_texts/source_text_manifest.json",
    "data/source_texts/reports/bereishis_hebrew_source_reconciliation_report.md",
    "data/source_texts/reports/bereishis_hebrew_source_reconciliation_report.json",
    "data/source_texts/translations/translation_sources_registry.json",
    "data/source_texts/translations/sefaria/README.md",
    "data/source_texts/translations/sefaria/sefaria_genesis_versions_raw.json",
    "data/source_texts/translations/sefaria/sefaria_english_versions_genesis_report.json",
    "data/source_texts/translations/sefaria/bereishis_english_translations_manifest.json",
    "data/source_texts/translations/sefaria/bereishis_english_koren.jsonl",
    "data/source_texts/translations/sefaria/bereishis_english_metsudah.jsonl",
    "data/source_texts/translations/sefaria/bereishis_english_translation_alignment_report.md",
    "data/source_texts/translations/sefaria/bereishis_english_translation_license_report.md",
    "data/source_texts/translations/sefaria/bereishis_english_translation_fetch_report.json",
    "data/source_texts/translations/sefaria/bereishis_english_translation_license_review_matrix.json",
    "data/source_texts/translations/sefaria/bereishis_english_translation_human_review_packet.md",
    "data/source_texts/translations/sefaria/raw_samples/koren_sample.json",
    "data/source_texts/translations/sefaria/raw_samples/metsudah_sample.json",
    "data/verified_source_skill_maps/README.md",
    "data/verified_source_skill_maps/bereishis_1_1_to_3_24_metsudah_skill_map.tsv",
    "data/verified_source_skill_maps/bereishis_1_1_to_1_5_source_to_skill_map.tsv",
    "data/verified_source_skill_maps/bereishis_1_6_to_1_13_source_to_skill_map.tsv",
    "data/verified_source_skill_maps/bereishis_1_14_to_1_23_source_to_skill_map.tsv",
    "data/verified_source_skill_maps/bereishis_1_24_to_1_31_source_to_skill_map.tsv",
    "data/verified_source_skill_maps/reports/bereishis_1_1_to_3_24_metsudah_skill_map_extraction_accuracy_review_packet.md",
    "data/verified_source_skill_maps/reports/bereishis_1_1_to_1_5_source_to_skill_map_exceptions_review_packet.md",
    "data/verified_source_skill_maps/reports/bereishis_1_1_to_1_5_yossi_extraction_verification_report.md",
    "data/verified_source_skill_maps/reports/bereishis_1_6_to_1_13_source_to_skill_map_build_report.md",
    "data/verified_source_skill_maps/reports/bereishis_1_6_to_1_13_source_to_skill_map_exceptions_review_packet.md",
    "data/verified_source_skill_maps/reports/bereishis_1_6_to_1_13_yossi_extraction_verification_report.md",
    "data/verified_source_skill_maps/reports/bereishis_1_14_to_1_23_source_to_skill_map_build_report.md",
    "data/verified_source_skill_maps/reports/bereishis_1_14_to_1_23_source_to_skill_map_exceptions_review_packet.md",
    "data/verified_source_skill_maps/reports/bereishis_1_14_to_1_23_yossi_extraction_verification_report.md",
    "data/verified_source_skill_maps/reports/bereishis_1_24_to_1_31_source_to_skill_map_build_report.md",
    "data/verified_source_skill_maps/reports/bereishis_1_24_to_1_31_source_to_skill_map_exceptions_review_packet.md",
    "data/verified_source_skill_maps/reports/bereishis_1_24_to_1_31_yossi_extraction_verification_report.md",
    "data/verified_source_skill_maps/reports/bereishis_perek_1_source_to_skill_completion_report.md",
    "data/verified_source_skill_maps/reports/source_to_skill_map_audit.json",
    "data/verified_source_skill_maps/bereishis_2_1_to_2_3_source_to_skill_map.tsv",
    "data/verified_source_skill_maps/reports/bereishis_2_1_to_2_3_source_to_skill_map_build_report.md",
    "data/verified_source_skill_maps/reports/bereishis_2_1_to_2_3_source_to_skill_map_exceptions_review_packet.md",
    "data/verified_source_skill_maps/reports/bereishis_2_1_to_2_3_yossi_review_sheet.csv",
    "data/verified_source_skill_maps/reports/bereishis_2_1_to_2_3_yossi_review_sheet.md",
    "data/verified_source_skill_maps/reports/bereishis_2_1_to_2_3_yossi_extraction_verification_report.md",
    "data/verified_source_skill_maps/bereishis_2_4_to_2_17_source_to_skill_map.tsv",
    "data/verified_source_skill_maps/reports/bereishis_2_4_to_2_17_source_to_skill_map_build_report.md",
    "data/verified_source_skill_maps/reports/bereishis_2_4_to_2_17_source_to_skill_map_exceptions_review_packet.md",
    "data/verified_source_skill_maps/reports/bereishis_2_4_to_2_17_yossi_review_sheet.csv",
    "data/verified_source_skill_maps/reports/bereishis_2_4_to_2_17_yossi_review_sheet.md",
    "data/verified_source_skill_maps/reports/bereishis_2_4_to_2_17_yossi_extraction_verification_report.md",
    "data/verified_source_skill_maps/bereishis_2_18_to_2_25_source_to_skill_map.tsv",
    "data/verified_source_skill_maps/reports/bereishis_2_18_to_2_25_source_to_skill_map_build_report.md",
    "data/verified_source_skill_maps/reports/bereishis_2_18_to_2_25_source_to_skill_map_exceptions_review_packet.md",
    "data/verified_source_skill_maps/reports/bereishis_2_18_to_2_25_yossi_review_sheet.csv",
    "data/verified_source_skill_maps/reports/bereishis_2_18_to_2_25_yossi_review_sheet.md",
    "data/verified_source_skill_maps/reports/bereishis_2_18_to_2_25_yossi_extraction_verification_report.md",
    "data/verified_source_skill_maps/reports/bereishis_perek_2_source_to_skill_completion_report.md",
    "data/verified_source_skill_maps/bereishis_3_1_to_3_7_source_to_skill_map.tsv",
    "data/verified_source_skill_maps/reports/bereishis_3_1_to_3_7_source_to_skill_map_build_report.md",
    "data/verified_source_skill_maps/reports/bereishis_3_1_to_3_7_source_to_skill_map_exceptions_review_packet.md",
    "data/verified_source_skill_maps/reports/bereishis_3_1_to_3_7_yossi_review_sheet.csv",
    "data/verified_source_skill_maps/reports/bereishis_3_1_to_3_7_yossi_review_sheet.md",
    "data/verified_source_skill_maps/reports/bereishis_3_1_to_3_7_yossi_extraction_verification_report.md",
    "data/verified_source_skill_maps/bereishis_3_8_to_3_16_source_to_skill_map.tsv",
    "data/verified_source_skill_maps/reports/bereishis_3_8_to_3_16_source_to_skill_map_build_report.md",
    "data/verified_source_skill_maps/reports/bereishis_3_8_to_3_16_source_to_skill_map_exceptions_review_packet.md",
    "data/verified_source_skill_maps/reports/bereishis_3_8_to_3_16_yossi_review_sheet.csv",
    "data/verified_source_skill_maps/reports/bereishis_3_8_to_3_16_yossi_review_sheet.md",
    "data/verified_source_skill_maps/reports/bereishis_3_8_to_3_16_yossi_extraction_verification_report.md",
    "data/verified_source_skill_maps/bereishis_3_17_to_3_24_source_to_skill_map.tsv",
    "data/verified_source_skill_maps/reports/bereishis_3_17_to_3_24_source_to_skill_map_build_report.md",
    "data/verified_source_skill_maps/reports/bereishis_3_17_to_3_24_source_to_skill_map_exceptions_review_packet.md",
    "data/verified_source_skill_maps/reports/bereishis_3_17_to_3_24_yossi_review_sheet.csv",
    "data/verified_source_skill_maps/reports/bereishis_3_17_to_3_24_yossi_review_sheet.md",
    "data/verified_source_skill_maps/reports/bereishis_3_17_to_3_24_yossi_extraction_verification_report.md",
    "data/verified_source_skill_maps/reports/bereishis_perek_3_source_to_skill_completion_report.md",
    "dikduk_rules_loader.py",
    "translation_sources_loader.py",
    "scripts/build_source_to_skill_map.py",
    "scripts/generate_yossi_review_sheet.py",
    "scripts/generate_curriculum_question_preview.py",
    "scripts/fetch_sefaria_bereishis_translations.py",
    "scripts/generate_diagnostic_preview.py",
    "scripts/validate_bereishis_translations.py",
    "scripts/validate_curriculum_extraction.py",
    "scripts/validate_source_skill_enrichment.py",
    "scripts/validate_perek_4_source_discovery.py",
    "scripts/validate_diagnostic_preview.py",
    "scripts/validate_dikduk_rules.py",
    "scripts/README.md",
    "scripts/validate_perek_3_pilot_evidence_pack.py",
    "scripts/validate_perek_3_pilot_observation_summary.py",
    "scripts/validate_perek_3_pilot_remediation_plan.py",
    "scripts/validate_perek_3_pilot_wording_clarity_fix.py",
    "scripts/validate_perek_3_pilot_distractor_source_remediation.py",
    "scripts/validate_perek_3_yossi_language_decisions.py",
    "scripts/validate_perek_3_short_repilot_scope_enforcement.py",
    "scripts/validate_perek_3_short_repilot_results.py",
    "scripts/validate_perek_3_short_repilot_scope_leak_fix.py",
    "scripts/validate_perek_4_compressed_teacher_review_packet.py",
    "scripts/validate_perek_4_teacher_review_decisions_applied.py",
    "scripts/validate_perek_4_candidate_planning_review_checklist.py",
    "scripts/validate_perek_4_candidate_planning_decisions_applied.py",
    "scripts/validate_perek_4_protected_preview_candidate_review_decisions.py",
    "scripts/validate_perek_4_internal_protected_preview_packet.py",
    "scripts/validate_perek_4_internal_review_decisions.py",
    "scripts/validate_perek_4_limited_internal_preview_decisions.py",
    "scripts/validate_perek_4_final_iteration_and_perek_5_6_gate.py",
    "scripts/validate_perek_5_6_source_discovery.py",
    "scripts/validate_perek_5_6_teacher_review_checklist.py",
    "scripts/validate_perek_5_6_teacher_review_decisions_applied.py",
    "scripts/validate_perek_5_6_candidate_planning_review_checklist.py",
    "scripts/validate_perek_5_6_candidate_planning_decisions_applied.py",
    "scripts/validate_perek_5_6_protected_preview_candidate_review_decisions.py",
    "scripts/validate_perek_5_6_small_internal_protected_preview_packet.py",
    "scripts/validate_perek_5_6_mixed_internal_review_packet.py",
    "scripts/validate_perek_5_6_mixed_internal_review_decisions.py",
    "scripts/validate_perek_5_6_review_recommendation_report.py",
    "scripts/validate_perek_5_6_mixed_packet_real_observation_evidence.py",
    "scripts/validate_perek_5_6_clean_two_item_limited_packet_iteration.py",
    "scripts/validate_streamlined_review_process.py",
    "scripts/validate_standards_data.py",
    "scripts/run_curriculum_quality_checks.py",
    "scripts/load_curriculum_extraction.py",
    "scripts/validate_source_texts.py",
    "scripts/validate_verified_source_skill_maps.py",
    "tests/test_bereishis_translation_sources.py",
    "tests/conftest.py",
    "tests/test_diagnostic_preview_generation.py",
    "tests/test_diagnostic_preview_validation.py",
    "tests/test_curriculum_quality_checks.py",
    "tests/test_dikduk_rule_loader.py",
    "tests/test_dikduk_rules_validation.py",
    "tests/test_perek_3_pilot_evidence_pack.py",
    "tests/test_perek_3_pilot_observation_summary.py",
    "tests/test_perek_3_pilot_remediation_plan.py",
    "tests/test_perek_3_pilot_wording_clarity_fix.py",
    "tests/test_perek_3_pilot_distractor_source_remediation.py",
    "tests/test_perek_3_yossi_language_decisions.py",
    "tests/test_perek_3_short_repilot_scope_enforcement.py",
    "tests/test_perek_3_short_repilot_results.py",
    "tests/test_perek_3_short_repilot_scope_leak_fix.py",
    "tests/test_perek_4_compressed_teacher_review_packet.py",
    "tests/test_perek_4_teacher_review_decisions_applied.py",
    "tests/test_perek_4_candidate_planning_review_checklist.py",
    "tests/test_perek_4_candidate_planning_decisions_applied.py",
    "tests/test_perek_4_protected_preview_candidate_review_decisions.py",
    "tests/test_perek_4_internal_protected_preview_packet.py",
    "tests/test_perek_4_internal_review_decisions.py",
    "tests/test_perek_4_limited_internal_preview_decisions.py",
    "tests/test_perek_4_final_iteration_and_perek_5_6_gate.py",
    "tests/test_perek_5_6_source_discovery.py",
    "tests/test_perek_5_6_teacher_review_checklist.py",
    "tests/test_perek_5_6_teacher_review_decisions_applied.py",
    "tests/test_perek_5_6_candidate_planning_review_checklist.py",
    "tests/test_perek_5_6_candidate_planning_decisions_applied.py",
    "tests/test_perek_5_6_protected_preview_candidate_review_decisions.py",
    "tests/test_perek_5_6_small_internal_protected_preview_packet.py",
    "tests/test_perek_5_6_mixed_internal_review_packet.py",
    "tests/test_perek_5_6_mixed_internal_review_decisions.py",
    "tests/test_perek_5_6_review_recommendation_report.py",
    "tests/test_perek_5_6_mixed_packet_real_observation_evidence.py",
    "tests/test_perek_5_6_clean_two_item_limited_packet_iteration.py",
    "tests/test_streamlined_review_process.py",
    "tests/test_prefix_question_generation.py",
    "tests/test_tense_morphology_questions.py",
    "tests/test_translation_sources_loader.py",
    "tests/test_curriculum_question_preview.py",
    "tests/test_curriculum_extraction_schemas.py",
    "tests/test_curriculum_extraction_validation.py",
    "tests/test_source_skill_enrichment.py",
    "tests/test_perek_4_source_discovery.py",
    "tests/test_curriculum_extraction_loader.py",
    "tests/test_standards_data_validation.py",
    "tests/test_source_corpus_block_4_1_to_4_16.py",
    "tests/test_source_texts_validation.py",
    "tests/test_verified_source_skill_maps.py",
    "README_CHROMEBOOK.md",
    "skill_catalog.py",
    "data/standards/canonical_skill_contract.json",
    "data/standards/reports/canonical_skill_standards_contract_report.md",
    "scripts/validate_canonical_skill_contract.py",
    "tests/test_canonical_skill_contract.py",
    "data/validation/curriculum_quality_check_summary.md",
    "data/validation/curriculum_quality_check_summary.json",
    "data/validation/curriculum_quality_control_index.md",
    "data/validation/diagnostic_preview_coverage_index.md",
    "data/validation/diagnostic_preview_coverage_index.json",
    "data/validation/protected_preview_source_lineage_matrix.md",
    "data/validation/protected_preview_source_lineage_matrix.tsv",
    "data/validation/runtime_review_exposure_index.md",
    "data/validation/runtime_review_exposure_index.json",
    "data/validation/standards_evidence_gap_matrix.md",
    "data/validation/standards_evidence_gap_matrix.json",
    "data/validation/question_quality_risk_summary.md",
    "data/validation/question_quality_risk_summary.json",
    "data/gate_2_protected_preview_candidates/reports/bereishis_perek_3_candidate_status_index.md",
}

FORBIDDEN_CHANGE_PREFIXES = (
    "streamlit_app.py",
    "runtime/",
    "engine/",
    "assessment_scope.py",
    "data/corpus_manifest.json",
    "data/active_scope_reviewed_questions.json",
    "data/active_scope_gold_annotations.json",
    "data/active_scope_overrides.json",
    "ui/",
    "skill_tracker.py",
    "progress_store.py",
)

SOURCE_TRUTH_BASELINE_REPAIR_EXACT = {
    "data/corpus_manifest.json",
    "data/source_texts/reports/source_truth_reproducibility_finalization_report.md",
    "tests/test_corpus_manifest.py",
}

PEREK_3_PILOT_WORDING_FIX_EXACT = {"engine/flow_builder.py"}
PEREK_3_PILOT_WORDING_FIX_ALLOWED_DIFF_FRAGMENTS = (
    "What verb tense is shown?",
    "What form is shown?",
    'What form is " + "shown?',
    "What tense or verb form is this word?",
    "What is the prefix in",
    "which beginning letter is the prefix",
)
PEREK_3_PILOT_DISTRACTOR_SOURCE_REMEDIATION_EXACT = {
    "data/active_scope_reviewed_questions.json",
}
PEREK_3_PILOT_DISTRACTOR_SOURCE_REMEDIATION_REQUIRED_DIFF_CONTEXT = (
    '"question_text": "What does ×Ö²×¨×•Ö¼×¨Ö¸×” mean?"',
    '"question_text": "What does ×“Ö¶Ö¼×¨Ö¶×šÖ° mean?"',
)
PEREK_3_PILOT_DISTRACTOR_SOURCE_REMEDIATION_ALLOWED_CHANGED_LINES = {
    '        "Eden",',
    '        "Eve",',
    '        "all"',
    '        "all",',
    '        "naked",',
    '        "living",',
    '        "heel"',
    '        "heel",',
    '        "children",',
    '        "way"',
    '        "cursed",',
}

PEREK_3_SHORT_REPILOT_SCOPE_LEAK_FIX_EXACT = {
    "data/active_scope_reviewed_questions.json",
}

IGNORED_GENERATED_CHANGE_EXACT = {
    "data/attempt_log.jsonl",
    "data/pilot/pilot_session_events.jsonl",
}

IGNORED_CHANGE_PREFIXES = (
    "incoming_source/",
)


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> list[dict]:
    records: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                payload = json.loads(stripped)
            except json.JSONDecodeError as error:
                raise ValueError(f"{repo_relative(path)} line {line_number}: invalid JSON ({error})") from error
            if not isinstance(payload, dict):
                raise ValueError(f"{repo_relative(path)} line {line_number}: expected JSON object")
            payload["_meta_source_file"] = repo_relative(path)
            payload["_meta_line_number"] = line_number
            records.append(payload)
    return records


def collect_preview_records(preview_dir: Path, errors: list[str]) -> tuple[dict[str, list[dict]], list[dict]]:
    records_by_file: dict[str, list[dict]] = {}
    all_records: list[dict] = []
    if not preview_dir.exists():
        return records_by_file, all_records
    for path in sorted(preview_dir.glob("*.jsonl")):
        try:
            records = load_jsonl(path)
        except ValueError as error:
            errors.append(str(error))
            continue
        relative = repo_relative(path)
        records_by_file[relative] = records
        all_records.extend(records)
    return records_by_file, all_records


def meaningful_value(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, bool):
        return True
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, set, dict)):
        return bool(value)
    return True


def require_fields(record: dict, fields: tuple[str, ...], errors: list[str], context: str) -> None:
    for field_name in fields:
        if field_name not in record:
            errors.append(f"{context}: missing required field '{field_name}'")


def validate_declared_files(manifest: dict, key: str, errors: list[str]) -> list[Path]:
    paths: list[Path] = []
    for relative in manifest.get(key, []):
        path = ROOT / relative
        paths.append(path)
        if not path.exists():
            errors.append(f"manifest file missing under {key}: {relative}")
    return paths


def collect_manifest_relative_paths(manifest: dict, key: str) -> list[str]:
    ordered_paths: list[str] = []
    seen: set[str] = set()

    def add_paths(values: object) -> None:
        if not isinstance(values, list):
            return
        for relative in values:
            if not isinstance(relative, str):
                continue
            if relative in seen:
                continue
            seen.add(relative)
            ordered_paths.append(relative)

    add_paths(manifest.get(key, []))
    for batch in manifest.get("resource_batches", []):
        if isinstance(batch, dict):
            add_paths(batch.get(key, []))
    return ordered_paths


def report_file_stem_for_batch(batch_id: str) -> str:
    parts = batch_id.split("_")
    if len(parts) >= 2 and parts[0] == "batch":
        return "_".join(parts[:2])
    return batch_id


def required_review_artifacts_for_reviewed_planning_batch(batch_id: str) -> set[str]:
    stem = report_file_stem_for_batch(batch_id)
    return {
        f"data/curriculum_extraction/reports/{stem}_summary.md",
        f"data/curriculum_extraction/reports/{stem}_preview_summary.md",
        f"data/curriculum_extraction/reports/{stem}_manual_review_packet.md",
        f"data/curriculum_extraction/reports/{stem}_review_resolution.md",
    }


def validate_declared_relative_paths(relative_paths: list[str], key: str, errors: list[str]) -> list[Path]:
    paths: list[Path] = []
    for relative in relative_paths:
        path = ROOT / relative
        paths.append(path)
        if not path.exists():
            errors.append(f"manifest file missing under {key}: {relative}")
    return paths


def expected_batch_review_status(record: dict, record_origin: str, batch_lookup: dict[str, dict]) -> str:
    batch = batch_lookup.get(str(record.get("extraction_batch_id", "")), {})
    batch_status = batch.get("status")
    if batch_status in RECORD_REVIEW_STATUS_BY_BATCH_STATUS:
        return RECORD_REVIEW_STATUS_BY_BATCH_STATUS[str(batch_status)]
    review_status = batch.get("review_status")
    if review_status in ALLOWED_REVIEW_STATUSES:
        return str(review_status)
    return "needs_review" if record_origin == "sample" else "needs_review"


def validate_resource_batches(manifest: dict, errors: list[str]) -> dict[str, dict]:
    batch_lookup: dict[str, dict] = {}
    for batch in manifest.get("resource_batches", []):
        if not isinstance(batch, dict):
            errors.append("curriculum_extraction_manifest.json: each resource batch must be an object")
            continue
        batch_id = batch.get("batch_id")
        if not batch_id:
            errors.append("curriculum_extraction_manifest.json: resource batch missing batch_id")
            continue
        status = batch.get("status")
        if status not in ALLOWED_BATCH_STATUSES:
            errors.append(f"curriculum_extraction_manifest.json: {batch_id} has invalid status '{status}'")
        if batch.get("runtime_active") is not False:
            errors.append(f"curriculum_extraction_manifest.json: {batch_id} must have runtime_active=false")
        if batch.get("integration_status") != "not_runtime_active":
            errors.append(f"curriculum_extraction_manifest.json: {batch_id} must have integration_status=not_runtime_active")
        review_status = batch.get("review_status")
        if review_status is not None and review_status not in ALLOWED_REVIEW_STATUSES:
            errors.append(f"curriculum_extraction_manifest.json: {batch_id} has invalid review_status '{review_status}'")
        review_artifacts = batch.get("review_artifacts", [])
        if review_artifacts is None:
            review_artifacts = []
        if not isinstance(review_artifacts, list):
            errors.append(f"curriculum_extraction_manifest.json: {batch_id} review_artifacts must be a list")
            review_artifacts = []
        else:
            for relative in review_artifacts:
                if not isinstance(relative, str):
                    errors.append(f"curriculum_extraction_manifest.json: {batch_id} review_artifacts entries must be strings")
                    continue
                if not (ROOT / relative).exists():
                    errors.append(
                        f"curriculum_extraction_manifest.json: {batch_id} review_artifact missing: {relative}"
                    )
        if status in REVIEWED_BATCH_STATUSES and review_status != "reviewed":
            errors.append(
                f"curriculum_extraction_manifest.json: {batch_id} reviewed non-runtime batches must have review_status=reviewed"
            )
        if status in {"draft_needs_review", "extracted_needs_review"} and review_status not in {None, "needs_review"}:
            errors.append(
                f"curriculum_extraction_manifest.json: {batch_id} {status} batches must keep review_status=needs_review"
            )
        if status == "reviewed_for_planning_non_runtime":
            declared_review_artifacts = {
                relative
                for relative in review_artifacts
                if isinstance(relative, str)
            }
            for required_artifact in sorted(required_review_artifacts_for_reviewed_planning_batch(str(batch_id))):
                if required_artifact not in declared_review_artifacts:
                    errors.append(
                        "curriculum_extraction_manifest.json: "
                        f"{batch_id} reviewed_for_planning_non_runtime batches must declare review_artifact "
                        f"'{required_artifact}'"
                    )
        batch_lookup[str(batch_id)] = batch
    return batch_lookup


def validate_source_trace(
    record: dict,
    errors: list[str],
    context: str,
    *,
    record_origin: str,
    expected_review_status: str,
) -> None:
    source_trace = record.get("source_trace")
    if not isinstance(source_trace, dict):
        errors.append(f"{context}: source_trace must be an object")
        return
    require_fields(source_trace, SOURCE_TRACE_REQUIRED_FIELDS, errors, f"{context} source_trace")

    extraction_method = source_trace.get("extraction_method")
    if record_origin == "sample":
        if extraction_method not in SAMPLE_ALLOWED_METHODS:
            errors.append(
                f"{context}: sample records must use extraction_method in {sorted(SAMPLE_ALLOWED_METHODS)}"
            )
    elif record_origin == "normalized":
        if extraction_method not in NORMALIZED_ALLOWED_METHODS:
            errors.append(
                f"{context}: normalized records must use extraction_method in {sorted(NORMALIZED_ALLOWED_METHODS)}"
            )

    if source_trace.get("review_status") != expected_review_status:
        errors.append(f"{context}: source_trace.review_status must be '{expected_review_status}'")
    page_start = source_trace.get("source_page_start")
    page_end = source_trace.get("source_page_end")
    if isinstance(page_start, int) and isinstance(page_end, int) and page_end < page_start:
        errors.append(f"{context}: source_page_end must be >= source_page_start")


def validate_review_flags(record: dict, errors: list[str], context: str, *, expected_review_status: str) -> None:
    if record.get("review_status") != expected_review_status:
        errors.append(f"{context}: review_status must be '{expected_review_status}'")
    if record.get("runtime_status") != "not_runtime_active":
        errors.append(f"{context}: runtime_status must be 'not_runtime_active'")
    if record.get("confidence") == "high":
        errors.append(f"{context}: confidence must not be 'high'")
    if expected_review_status == "reviewed" and record.get("confidence") == "low":
        errors.append(f"{context}: reviewed records must not stay at low confidence")


def validate_skill_tags(record: dict, valid_skill_refs: set[str], errors: list[str], context: str) -> None:
    skill_tags = record.get("skill_tags", [])
    if skill_tags is None:
        skill_tags = []
    if not isinstance(skill_tags, list):
        errors.append(f"{context}: skill_tags must be a list")
        return
    for skill_tag in skill_tags:
        skill_tag = str(skill_tag)
        if skill_tag in valid_skill_refs:
            continue
        alias_targets = SKILL_TAG_ALIASES.get(skill_tag, set())
        if alias_targets and any(target in valid_skill_refs for target in alias_targets):
            continue
        errors.append(f"{context}: unknown skill tag '{skill_tag}'")


def validate_preview_source_trace(record: dict, errors: list[str], context: str) -> None:
    source_trace = record.get("source_trace")
    if not isinstance(source_trace, dict):
        errors.append(f"{context}: source_trace must be an object")
        return
    require_fields(source_trace, SOURCE_TRACE_REQUIRED_FIELDS, errors, f"{context} source_trace")
    page_start = source_trace.get("source_page_start")
    page_end = source_trace.get("source_page_end")
    if isinstance(page_start, int) and isinstance(page_end, int) and page_end < page_start:
        errors.append(f"{context}: source_page_end must be >= source_page_start")


def has_quality_flag(record: dict, flag: str) -> bool:
    flags = record.get("extraction_quality_flags")
    if not isinstance(flags, list):
        return False
    return flag in flags


def validate_answer_status(record: dict, answer_fields: tuple[str, ...], errors: list[str], context: str) -> None:
    answer_status = record.get("answer_status")
    if answer_status not in ANSWER_STATUS_VALUES:
        errors.append(f"{context}: invalid answer_status '{answer_status}'")
        return
    if answer_status == "source_provided":
        if not any(meaningful_value(record.get(field_name)) for field_name in answer_fields):
            errors.append(f"{context}: source_provided records need a non-empty answer/translation/parse field")
    if answer_status == "inferred_needs_review" and record.get("review_status") != "needs_review":
        errors.append(f"{context}: inferred_needs_review records must stay needs_review")
    if answer_status in {"not_provided", "not_extracted", "not_applicable"}:
        answer_values = [record.get(field_name) for field_name in answer_fields]
        if any(meaningful_value(value) for value in answer_values):
            errors.append(f"{context}: {answer_status} records must not invent answer content")


def validate_record_type_specific(record: dict, errors: list[str], context: str) -> None:
    record_type = record.get("record_type")
    batch_id = record.get("extraction_batch_id")
    if record_type == "pasuk_segment":
        require_fields(record, PASUK_SEGMENT_REQUIRED_FIELDS, errors, context)
        for field_name in ("sefer", "perek", "pasuk", "segment_order"):
            if not meaningful_value(record.get(field_name)):
                errors.append(f"{context}: pasuk_segment field '{field_name}' must be populated")
    elif record_type == "word_parse":
        require_fields(record, WORD_PARSE_REQUIRED_FIELDS, errors, context)
        validate_answer_status(
            record,
            (
                "target_shoresh_raw",
                "target_shoresh_normalized",
                "shoresh_meaning",
                "literal_translation",
                "contextual_translation",
                "grammar_features",
            ),
            errors,
            context,
        )
        if batch_id == "batch_001_cleaned_seed":
            if not meaningful_value(record.get("target_shoresh_raw")) and not has_quality_flag(
                record,
                "missing_explicit_shoresh",
            ):
                errors.append(f"{context}: missing explicit shoresh records must carry 'missing_explicit_shoresh'")
            if not meaningful_value(record.get("suffixes")) and not has_quality_flag(record, "missing_suffix_payload"):
                errors.append(f"{context}: records without suffix payload must carry 'missing_suffix_payload'")
    elif record_type == "word_parse_task":
        require_fields(record, WORD_PARSE_TASK_REQUIRED_FIELDS, errors, context)
        validate_answer_status(
            record,
            (
                "expected_word_in_pasuk",
                "prefixes",
                "suffixes",
            ),
            errors,
            context,
        )
        missing_answer_payload = not any(
            meaningful_value(record.get(field_name))
            for field_name in ("expected_word_in_pasuk", "prefixes", "suffixes")
        )
        if missing_answer_payload and record.get("answer_status") not in {"not_extracted", "not_provided"}:
            errors.append(
                f"{context}: word_parse_task records missing answer content must use not_extracted or not_provided"
            )
        if (
            batch_id == "batch_001_cleaned_seed"
            and missing_answer_payload
            and not has_quality_flag(record, "answer_key_not_extracted")
        ):
            errors.append(f"{context}: missing task answers must carry 'answer_key_not_extracted'")
    elif record_type == "vocab_entry":
        require_fields(record, VOCAB_ENTRY_REQUIRED_FIELDS, errors, context)
        english_glosses = record.get("english_glosses") or []
        if not english_glosses and record.get("needs_gloss_review") is not True:
            errors.append(f"{context}: vocab entries with empty english_glosses must set needs_gloss_review=true")
        if batch_id == "batch_001_cleaned_seed" and not english_glosses and not has_quality_flag(
            record,
            "missing_english_gloss",
        ):
            errors.append(f"{context}: missing vocab glosses must carry 'missing_english_gloss'")
    elif record_type == "comprehension_question":
        require_fields(record, COMPREHENSION_REQUIRED_FIELDS, errors, context)
        validate_answer_status(record, ("expected_answer",), errors, context)
        if (
            batch_id == "batch_001_cleaned_seed"
            and not meaningful_value(record.get("expected_answer"))
            and not has_quality_flag(record, "missing_expected_answer")
        ):
            errors.append(f"{context}: missing expected answers must carry 'missing_expected_answer'")
    elif record_type == "question_template":
        require_fields(record, QUESTION_TEMPLATE_REQUIRED_FIELDS, errors, context)
    elif record_type == "skill_tag":
        require_fields(record, SKILL_TAG_REQUIRED_FIELDS, errors, context)
    elif record_type == "translation_rule":
        require_fields(record, TRANSLATION_RULE_REQUIRED_FIELDS, errors, context)
    else:
        errors.append(f"{context}: unsupported record_type '{record_type}'")


def validate_preview_records(
    preview_records_by_file: dict[str, list[dict]],
    valid_skill_refs: set[str],
    valid_source_record_ids: set[str],
    registry_lookup: dict[str, dict],
    errors: list[str],
) -> tuple[list[dict], dict[str, dict[str, int]], dict[str, int]]:
    preview_records: list[dict] = []
    seen_preview_ids: set[str] = set()
    preview_file_question_type_counts: dict[str, dict[str, int]] = {}
    preview_file_record_counts: dict[str, int] = {}
    for relative_path, records in preview_records_by_file.items():
        seen_prompts: set[str] = set()
        preview_file_record_counts[relative_path] = len(records)
        preview_file_question_type_counts[relative_path] = dict(
            sorted(Counter(record.get("question_type") for record in records if record.get("question_type")).items())
        )
        for record in records:
            line_number = record.pop("_meta_line_number", "?")
            source_file = record.pop("_meta_source_file", relative_path)
            context = f"{source_file}:{line_number}"
            preview_records.append(record)

            require_fields(record, PREVIEW_REQUIRED_FIELDS, errors, context)
            validate_preview_source_trace(record, errors, context)

            preview_id = str(record.get("id", "")).strip()
            if not preview_id:
                errors.append(f"{context}: id must be populated")
            elif preview_id in seen_preview_ids:
                errors.append(f"{context}: duplicate preview id '{preview_id}'")
            else:
                seen_preview_ids.add(preview_id)

            if record.get("schema_version") != "0.1":
                errors.append(f"{context}: schema_version must be '0.1'")
            if record.get("record_type") != "generated_question_preview":
                errors.append(f"{context}: record_type must be 'generated_question_preview'")

            source_record_id = str(record.get("source_record_id", "")).strip()
            if not source_record_id:
                errors.append(f"{context}: source_record_id must be populated")
            elif source_record_id not in valid_source_record_ids:
                errors.append(f"{context}: unknown source_record_id '{source_record_id}'")

            source_package_id = record.get("source_package_id")
            if source_package_id not in registry_lookup:
                errors.append(f"{context}: unknown source_package_id '{source_package_id}'")

            prompt = str(record.get("prompt", "")).strip()
            if not prompt:
                errors.append(f"{context}: prompt must be populated")
            elif prompt in seen_prompts:
                errors.append(f"{context}: duplicate prompt text is not allowed")
            else:
                seen_prompts.add(prompt)

            if not meaningful_value(record.get("answer")):
                errors.append(f"{context}: answer must be populated")
            distractors = record.get("distractors")
            if not isinstance(distractors, list):
                errors.append(f"{context}: distractors must be a list")

            if record.get("review_status") != "needs_review":
                errors.append(f"{context}: preview questions must have review_status='needs_review'")
            if record.get("runtime_status") != "not_runtime_active":
                errors.append(f"{context}: preview questions must have runtime_status='not_runtime_active'")
            if record.get("confidence") != "low":
                errors.append(f"{context}: preview questions must have confidence='low'")

            validate_skill_tags(record, valid_skill_refs, errors, context)
    return preview_records, preview_file_question_type_counts, preview_file_record_counts


def validate_registry(registry: dict, errors: list[str]) -> dict[str, dict]:
    packages = registry.get("source_packages")
    if not isinstance(packages, list) or not packages:
        errors.append("source_resource_registry.json: source_packages must be a non-empty list")
        return {}
    registry_lookup: dict[str, dict] = {}
    for package in packages:
        if not isinstance(package, dict):
            errors.append("source_resource_registry.json: each source package must be an object")
            continue
        source_package_id = package.get("source_package_id")
        if not source_package_id:
            errors.append("source_resource_registry.json: source package missing source_package_id")
            continue
        if package.get("runtime_active") is not False:
            errors.append(f"source_resource_registry.json: {source_package_id} must have runtime_active=false")
        registry_lookup[source_package_id] = package
    return registry_lookup


def validate_schema_files(manifest: dict, errors: list[str]) -> list[Path]:
    schema_paths: list[Path] = []
    for relative in manifest.get("schema_files", []):
        schema_path = ROOT / relative
        schema_paths.append(schema_path)
        if not schema_path.exists():
            errors.append(f"manifest schema missing: {relative}")
            continue
        try:
            payload = load_json(schema_path)
        except json.JSONDecodeError as error:
            errors.append(f"{relative}: invalid JSON ({error})")
            continue
        if not isinstance(payload, dict):
            errors.append(f"{relative}: schema must be a JSON object")
    return schema_paths


def collect_records_from_relative_paths(
    relative_paths: list[str],
    key: str,
    errors: list[str],
) -> tuple[dict[str, list[dict]], list[dict]]:
    records_by_file: dict[str, list[dict]] = {}
    all_records: list[dict] = []
    for relative in relative_paths:
        path = ROOT / relative
        if not path.exists():
            errors.append(f"manifest {key} file missing: {relative}")
            continue
        try:
            records = load_jsonl(path)
        except ValueError as error:
            errors.append(str(error))
            continue
        records_by_file[relative] = records
        all_records.extend(records)
    return records_by_file, all_records


def collect_changed_paths() -> list[str]:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    paths: list[str] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        path = path.strip().strip('"').replace("\\", "/")
        if (
            path
            and path not in IGNORED_GENERATED_CHANGE_EXACT
            and not any(path.startswith(prefix) for prefix in IGNORED_CHANGE_PREFIXES)
        ):
            paths.append(path)
    return paths


def is_allowed_change(path: str) -> bool:
    if any(path.startswith(prefix) for prefix in ALLOWED_AUDIT_REPORT_PREFIXES):
        return Path(path).suffix in ALLOWED_AUDIT_REPORT_SUFFIXES
    if path in ALLOWED_CHANGE_EXACT:
        return True
    return any(path.startswith(prefix) for prefix in ALLOWED_CHANGE_PREFIXES)


def is_allowed_source_truth_baseline_repair(path: str) -> bool:
    return path in SOURCE_TRUTH_BASELINE_REPAIR_EXACT


def is_allowed_perek_3_pilot_wording_fix(path: str) -> bool:
    if path not in PEREK_3_PILOT_WORDING_FIX_EXACT:
        return False
    result = subprocess.run(
        ["git", "diff", "--", path],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        return False
    changed_lines = []
    for line in result.stdout.splitlines():
        if line.startswith(("+++", "---")):
            continue
        if line.startswith(("+", "-")):
            changed_lines.append(line[1:])
    if not changed_lines:
        return False
    return all(
        any(fragment in line for fragment in PEREK_3_PILOT_WORDING_FIX_ALLOWED_DIFF_FRAGMENTS)
        for line in changed_lines
    )


def is_allowed_perek_3_pilot_distractor_source_remediation(path: str) -> bool:
    if path not in PEREK_3_PILOT_DISTRACTOR_SOURCE_REMEDIATION_EXACT:
        return False
    result = subprocess.run(
        ["git", "diff", "--unified=20", "--", path],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        return False
    diff = result.stdout
    if not diff:
        return False
    if not all(
        context in diff
        for context in PEREK_3_PILOT_DISTRACTOR_SOURCE_REMEDIATION_REQUIRED_DIFF_CONTEXT
    ):
        return False
    changed_lines = []
    for line in diff.splitlines():
        if line.startswith(("+++", "---")):
            continue
        if line.startswith(("+", "-")):
            changed_lines.append(line[1:])
    if not changed_lines:
        return False
    return all(
        line in PEREK_3_PILOT_DISTRACTOR_SOURCE_REMEDIATION_ALLOWED_CHANGED_LINES
        for line in changed_lines
    )


def is_allowed_perek_3_short_repilot_scope_leak_fix(path: str) -> bool:
    if path not in PEREK_3_SHORT_REPILOT_SCOPE_LEAK_FIX_EXACT:
        return False
    result = subprocess.run(
        ["git", "diff", "--unified=2", "--", path],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        return False
    diff = result.stdout
    if not diff:
        return False
    if "×‘Ö°Ö¼×Ö´×©Ö°××ªÖ¼×•Ö¹" not in diff:
        return False
    if "What is the prefix in" not in diff:
        return False
    if "which beginning letter is the prefix" not in diff:
        return False

    changed_lines = []
    for line in diff.splitlines():
        if line.startswith(("+++", "---")):
            continue
        if line.startswith(("+", "-")):
            changed_lines.append(line[1:])
    if not changed_lines:
        return False

    def allowed_prompt_line(line: str) -> bool:
        stripped = line.strip()
        if stripped.startswith('"question_text": "What is the prefix in '):
            return stripped.endswith('?",')
        if stripped.startswith('"question": "What is the prefix in '):
            return stripped.endswith('?",')
        if stripped.startswith('"question_text": "In ') and "which beginning letter is the prefix?" in stripped:
            return stripped.endswith('",')
        if stripped.startswith('"question": "In ') and "which beginning letter is the prefix?" in stripped:
            return stripped.endswith('",')
        return False

    return all(allowed_prompt_line(line) for line in changed_lines)


def forbidden_reason(path: str) -> str:
    for prefix in FORBIDDEN_CHANGE_PREFIXES:
        if path == prefix or path.startswith(prefix):
            return f"forbidden path changed: {path}"
    return f"path outside isolated curriculum extraction allowlist: {path}"


def validate_curriculum_extraction(*, check_git_diff: bool = False) -> dict:
    errors: list[str] = []
    manifest = load_json(MANIFEST_PATH)
    registry = load_json(REGISTRY_PATH)

    if not isinstance(manifest, dict):
        errors.append("curriculum_extraction_manifest.json must be a JSON object")
        manifest = {}
    if not isinstance(registry, dict):
        errors.append("source_resource_registry.json must be a JSON object")
        registry = {}

    if manifest.get("runtime_active") is not False:
        errors.append("curriculum_extraction_manifest.json: runtime_active must be false")
    if manifest.get("integration_status") != "not_runtime_active":
        errors.append("curriculum_extraction_manifest.json: integration_status must be not_runtime_active")

    registry_lookup = validate_registry(registry, errors)
    batch_lookup = validate_resource_batches(manifest, errors)
    schema_paths = validate_schema_files(manifest, errors)
    raw_source_paths = validate_declared_relative_paths(
        collect_manifest_relative_paths(manifest, "raw_source_files"),
        "raw_source_files",
        errors,
    )
    sample_relative_paths = collect_manifest_relative_paths(manifest, "sample_files")
    normalized_relative_paths = collect_manifest_relative_paths(manifest, "normalized_data_files")
    validate_declared_relative_paths(
        collect_manifest_relative_paths(manifest, "generated_question_preview_files"),
        "generated_question_preview_files",
        errors,
    )
    sample_records_by_file, sample_records = collect_records_from_relative_paths(
        sample_relative_paths,
        "sample_files",
        errors,
    )
    normalized_records_by_file, normalized_records = collect_records_from_relative_paths(
        normalized_relative_paths,
        "normalized_data_files",
        errors,
    )
    preview_records_by_file, preview_records = collect_preview_records(PREVIEW_DIR, errors)
    all_records = [*sample_records, *normalized_records]

    seen_ids: set[str] = set()
    valid_skill_refs: set[str] = set()
    for record in sample_records:
        if record.get("record_type") == "skill_tag":
            if record.get("id"):
                valid_skill_refs.add(str(record["id"]))
            if record.get("skill_key"):
                valid_skill_refs.add(str(record["skill_key"]))

    def validate_record_collection(records_by_file: dict[str, list[dict]], record_origin: str) -> None:
        for relative_path, records in records_by_file.items():
            expected_record_type = EXPECTED_RECORD_TYPES.get(relative_path)
            for record in records:
                line_number = record.pop("_meta_line_number", "?")
                source_file = record.pop("_meta_source_file", relative_path)
                context = f"{source_file}:{line_number}"
                expected_review_status = expected_batch_review_status(record, record_origin, batch_lookup)

                require_fields(record, COMMON_REQUIRED_FIELDS, errors, context)
                validate_source_trace(
                    record,
                    errors,
                    context,
                    record_origin=record_origin,
                    expected_review_status=expected_review_status,
                )
                validate_review_flags(record, errors, context, expected_review_status=expected_review_status)

                record_id = record.get("id")
                if record_id in seen_ids:
                    errors.append(f"{context}: duplicate record id '{record_id}'")
                elif record_id:
                    seen_ids.add(str(record_id))

                source_package_id = record.get("source_package_id")
                if source_package_id not in registry_lookup:
                    errors.append(f"{context}: unknown source_package_id '{source_package_id}'")

                record_type = record.get("record_type")
                if expected_record_type and record_type != expected_record_type:
                    errors.append(f"{context}: expected record_type '{expected_record_type}', got '{record_type}'")

                validate_record_type_specific(record, errors, context)
                if record_type != "skill_tag":
                    validate_skill_tags(record, valid_skill_refs, errors, context)

    validate_record_collection(sample_records_by_file, "sample")
    validate_record_collection(normalized_records_by_file, "normalized")
    valid_source_record_ids = {
        str(record.get("id"))
        for record in all_records
        if meaningful_value(record.get("id"))
    }
    preview_records, preview_file_question_type_counts, preview_file_record_counts = validate_preview_records(
        preview_records_by_file,
        valid_skill_refs,
        valid_source_record_ids,
        registry_lookup,
        errors,
    )

    changed_paths: list[str] = []
    if check_git_diff:
        changed_paths = collect_changed_paths()
        for path in changed_paths:
            if (
                not is_allowed_change(path)
                and not is_allowed_source_truth_baseline_repair(path)
                and not is_allowed_perek_3_pilot_wording_fix(path)
                and not is_allowed_perek_3_pilot_distractor_source_remediation(path)
                and not is_allowed_perek_3_short_repilot_scope_leak_fix(path)
            ):
                errors.append(forbidden_reason(path))

    record_counts = Counter(record.get("record_type") for record in all_records if record.get("record_type"))
    review_status_counts = Counter(record.get("review_status") for record in all_records if record.get("review_status"))
    runtime_status_counts = Counter(record.get("runtime_status") for record in all_records if record.get("runtime_status"))
    preview_question_type_counts = Counter(
        record.get("question_type") for record in preview_records if record.get("question_type")
    )
    summary = {
        "valid": not errors,
        "manifest_path": repo_relative(MANIFEST_PATH),
        "registry_path": repo_relative(REGISTRY_PATH),
        "schema_file_count": len(schema_paths),
        "raw_source_file_count": len(raw_source_paths),
        "sample_file_count": len(sample_records_by_file),
        "normalized_file_count": len(normalized_records_by_file),
        "preview_file_count": len(preview_records_by_file),
        "sample_record_count": len(sample_records),
        "normalized_record_count": len(normalized_records),
        "record_count": len(all_records),
        "preview_record_count": len(preview_records),
        "preview_file_record_counts": preview_file_record_counts,
        "preview_file_question_type_counts": preview_file_question_type_counts,
        "record_type_counts": dict(sorted(record_counts.items())),
        "review_status_counts": dict(sorted(review_status_counts.items())),
        "runtime_status_counts": dict(sorted(runtime_status_counts.items())),
        "preview_question_type_counts": dict(sorted(preview_question_type_counts.items())),
        "checked_git_diff": check_git_diff,
        "changed_paths": changed_paths,
        "errors": errors,
    }
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the isolated curriculum extraction scaffold.")
    parser.add_argument(
        "--check-git-diff",
        action="store_true",
        help="Fail if changes outside the curriculum extraction allowlist are present.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = validate_curriculum_extraction(check_git_diff=bool(args.check_git_diff))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())





