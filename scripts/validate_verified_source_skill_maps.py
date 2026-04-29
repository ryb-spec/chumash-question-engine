from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAP_DIR = ROOT / "data" / "verified_source_skill_maps"
SEED_MAP_PATH = MAP_DIR / "bereishis_1_1_to_3_24_metsudah_skill_map.tsv"
PROOF_MAP_PATH = MAP_DIR / "bereishis_1_1_to_1_5_source_to_skill_map.tsv"
SEED_REVIEW_PACKET_PATH = (
    MAP_DIR / "reports" / "bereishis_1_1_to_3_24_metsudah_skill_map_extraction_accuracy_review_packet.md"
)
PROOF_REVIEW_PACKET_PATH = (
    MAP_DIR / "reports" / "bereishis_1_1_to_1_5_source_to_skill_map_exceptions_review_packet.md"
)
PROOF_VERIFICATION_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_1_1_to_1_5_yossi_extraction_verification_report.md"
)
NEXT_SLICE_MAP_PATH = MAP_DIR / "bereishis_1_6_to_1_13_source_to_skill_map.tsv"
NEXT_SLICE_BUILD_REPORT_PATH = MAP_DIR / "reports" / "bereishis_1_6_to_1_13_source_to_skill_map_build_report.md"
NEXT_SLICE_REVIEW_PACKET_PATH = (
    MAP_DIR / "reports" / "bereishis_1_6_to_1_13_source_to_skill_map_exceptions_review_packet.md"
)
NEXT_SLICE_VERIFICATION_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_1_6_to_1_13_yossi_extraction_verification_report.md"
)
PENDING_SLICE_MAP_PATH = MAP_DIR / "bereishis_1_14_to_1_23_source_to_skill_map.tsv"
PENDING_SLICE_BUILD_REPORT_PATH = MAP_DIR / "reports" / "bereishis_1_14_to_1_23_source_to_skill_map_build_report.md"
PENDING_SLICE_REVIEW_PACKET_PATH = (
    MAP_DIR / "reports" / "bereishis_1_14_to_1_23_source_to_skill_map_exceptions_review_packet.md"
)
PENDING_SLICE_VERIFICATION_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_1_14_to_1_23_yossi_extraction_verification_report.md"
)
PEREK_ONE_FINAL_SLICE_MAP_PATH = MAP_DIR / "bereishis_1_24_to_1_31_source_to_skill_map.tsv"
PEREK_ONE_FINAL_SLICE_BUILD_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_1_24_to_1_31_source_to_skill_map_build_report.md"
)
PEREK_ONE_FINAL_SLICE_REVIEW_PACKET_PATH = (
    MAP_DIR / "reports" / "bereishis_1_24_to_1_31_source_to_skill_map_exceptions_review_packet.md"
)
PEREK_ONE_FINAL_SLICE_VERIFICATION_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_1_24_to_1_31_yossi_extraction_verification_report.md"
)
PEREK_ONE_COMPLETION_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_perek_1_source_to_skill_completion_report.md"
)
PEREK_TWO_OPENING_SLICE_MAP_PATH = MAP_DIR / "bereishis_2_1_to_2_3_source_to_skill_map.tsv"
PEREK_TWO_OPENING_SLICE_BUILD_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_2_1_to_2_3_source_to_skill_map_build_report.md"
)
PEREK_TWO_OPENING_SLICE_REVIEW_PACKET_PATH = (
    MAP_DIR / "reports" / "bereishis_2_1_to_2_3_source_to_skill_map_exceptions_review_packet.md"
)
PEREK_TWO_OPENING_SLICE_REVIEW_SHEET_MD_PATH = (
    MAP_DIR / "reports" / "bereishis_2_1_to_2_3_yossi_review_sheet.md"
)
PEREK_TWO_OPENING_SLICE_REVIEW_SHEET_CSV_PATH = (
    MAP_DIR / "reports" / "bereishis_2_1_to_2_3_yossi_review_sheet.csv"
)
PEREK_TWO_OPENING_SLICE_VERIFICATION_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_2_1_to_2_3_yossi_extraction_verification_report.md"
)
PEREK_TWO_EXPANSION_SLICE_MAP_PATH = MAP_DIR / "bereishis_2_4_to_2_17_source_to_skill_map.tsv"
PEREK_TWO_EXPANSION_SLICE_BUILD_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_2_4_to_2_17_source_to_skill_map_build_report.md"
)
PEREK_TWO_EXPANSION_SLICE_REVIEW_PACKET_PATH = (
    MAP_DIR / "reports" / "bereishis_2_4_to_2_17_source_to_skill_map_exceptions_review_packet.md"
)
PEREK_TWO_EXPANSION_SLICE_REVIEW_SHEET_MD_PATH = (
    MAP_DIR / "reports" / "bereishis_2_4_to_2_17_yossi_review_sheet.md"
)
PEREK_TWO_EXPANSION_SLICE_REVIEW_SHEET_CSV_PATH = (
    MAP_DIR / "reports" / "bereishis_2_4_to_2_17_yossi_review_sheet.csv"
)
PEREK_TWO_EXPANSION_SLICE_VERIFICATION_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_2_4_to_2_17_yossi_extraction_verification_report.md"
)
PEREK_TWO_FINAL_SLICE_MAP_PATH = MAP_DIR / "bereishis_2_18_to_2_25_source_to_skill_map.tsv"
PEREK_TWO_FINAL_SLICE_BUILD_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_2_18_to_2_25_source_to_skill_map_build_report.md"
)
PEREK_TWO_FINAL_SLICE_REVIEW_PACKET_PATH = (
    MAP_DIR / "reports" / "bereishis_2_18_to_2_25_source_to_skill_map_exceptions_review_packet.md"
)
PEREK_TWO_FINAL_SLICE_REVIEW_SHEET_MD_PATH = (
    MAP_DIR / "reports" / "bereishis_2_18_to_2_25_yossi_review_sheet.md"
)
PEREK_TWO_FINAL_SLICE_REVIEW_SHEET_CSV_PATH = (
    MAP_DIR / "reports" / "bereishis_2_18_to_2_25_yossi_review_sheet.csv"
)
PEREK_TWO_FINAL_SLICE_VERIFICATION_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_2_18_to_2_25_yossi_extraction_verification_report.md"
)
PEREK_TWO_COMPLETION_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_perek_2_source_to_skill_completion_report.md"
)
PEREK_THREE_COMPLETION_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_perek_3_source_to_skill_completion_report.md"
)
PEREK_THREE_OPENING_SLICE_MAP_PATH = MAP_DIR / "bereishis_3_1_to_3_7_source_to_skill_map.tsv"
PEREK_THREE_OPENING_SLICE_BUILD_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_3_1_to_3_7_source_to_skill_map_build_report.md"
)
PEREK_THREE_OPENING_SLICE_REVIEW_PACKET_PATH = (
    MAP_DIR / "reports" / "bereishis_3_1_to_3_7_source_to_skill_map_exceptions_review_packet.md"
)
PEREK_THREE_OPENING_SLICE_REVIEW_SHEET_MD_PATH = (
    MAP_DIR / "reports" / "bereishis_3_1_to_3_7_yossi_review_sheet.md"
)
PEREK_THREE_OPENING_SLICE_REVIEW_SHEET_CSV_PATH = (
    MAP_DIR / "reports" / "bereishis_3_1_to_3_7_yossi_review_sheet.csv"
)
PEREK_THREE_OPENING_SLICE_VERIFICATION_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_3_1_to_3_7_yossi_extraction_verification_report.md"
)
PEREK_THREE_EXPANSION_SLICE_MAP_PATH = MAP_DIR / "bereishis_3_8_to_3_16_source_to_skill_map.tsv"
PEREK_THREE_EXPANSION_SLICE_BUILD_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_3_8_to_3_16_source_to_skill_map_build_report.md"
)
PEREK_THREE_EXPANSION_SLICE_REVIEW_PACKET_PATH = (
    MAP_DIR / "reports" / "bereishis_3_8_to_3_16_source_to_skill_map_exceptions_review_packet.md"
)
PEREK_THREE_EXPANSION_SLICE_REVIEW_SHEET_MD_PATH = (
    MAP_DIR / "reports" / "bereishis_3_8_to_3_16_yossi_review_sheet.md"
)
PEREK_THREE_EXPANSION_SLICE_REVIEW_SHEET_CSV_PATH = (
    MAP_DIR / "reports" / "bereishis_3_8_to_3_16_yossi_review_sheet.csv"
)
PEREK_THREE_EXPANSION_SLICE_VERIFICATION_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_3_8_to_3_16_yossi_extraction_verification_report.md"
)
PEREK_THREE_FINAL_SLICE_MAP_PATH = MAP_DIR / "bereishis_3_17_to_3_24_source_to_skill_map.tsv"
PEREK_THREE_FINAL_SLICE_BUILD_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_3_17_to_3_24_source_to_skill_map_build_report.md"
)
PEREK_THREE_FINAL_SLICE_REVIEW_PACKET_PATH = (
    MAP_DIR / "reports" / "bereishis_3_17_to_3_24_source_to_skill_map_exceptions_review_packet.md"
)
PEREK_THREE_FINAL_SLICE_REVIEW_SHEET_MD_PATH = (
    MAP_DIR / "reports" / "bereishis_3_17_to_3_24_yossi_review_sheet.md"
)
PEREK_THREE_FINAL_SLICE_REVIEW_SHEET_CSV_PATH = (
    MAP_DIR / "reports" / "bereishis_3_17_to_3_24_yossi_review_sheet.csv"
)
PEREK_THREE_FINAL_SLICE_VERIFICATION_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_3_17_to_3_24_yossi_extraction_verification_report.md"
)
AUDIT_REPORT_PATH = MAP_DIR / "reports" / "source_to_skill_map_audit.json"

REQUIRED_COLUMNS = (
    "sefer",
    "perek",
    "pasuk",
    "ref",
    "hebrew_word_or_phrase",
    "clean_hebrew_no_nikud",
    "source_translation_metsudah",
    "alternate_translation",
    "secondary_translation_koren",
    "source_id",
    "source_version_title",
    "source_license",
    "source_preference",
    "requires_attribution",
    "skill_primary",
    "skill_secondary",
    "zekelman_standard",
    "difficulty_level",
    "question_allowed",
    "runtime_allowed",
    "protected_preview_allowed",
    "reviewed_bank_allowed",
    "extraction_review_status",
    "review_notes",
    "uncertainty_reason",
)

OPTIONAL_KOREN_POLICY_COLUMNS = (
    "secondary_source_id",
    "secondary_source_version_title",
    "secondary_source_license",
    "secondary_source_preference",
    "secondary_commercial_use_allowed",
)

PROOF_REQUIRED_COLUMNS = (
    "sefer",
    "perek",
    "pasuk",
    "ref",
    "hebrew_word_or_phrase",
    "clean_hebrew_no_nikud",
    "source_translation_metsudah",
    "alternate_translation",
    "secondary_translation_koren",
    "source_id",
    "source_version_title",
    "source_license",
    "source_preference",
    "requires_attribution",
    "shoresh",
    "prefixes",
    "suffixes",
    "tense",
    "part_of_speech",
    "dikduk_feature",
    "skill_primary",
    "skill_secondary",
    "skill_id",
    "zekelman_standard",
    "difficulty_level",
    "question_allowed",
    "question_type_allowed",
    "blocked_question_types",
    "runtime_allowed",
    "protected_preview_allowed",
    "reviewed_bank_allowed",
    "extraction_review_status",
    "review_notes",
    "uncertainty_reason",
    "source_files_used",
)

ALLOWED_SOURCE_PREFERENCES = {
    "primary_preferred_translation_source",
    "secondary_noncommercial_translation_support",
}

ALLOWED_EXTRACTION_REVIEW_STATUSES = {
    "pending_yossi_extraction_accuracy_pass",
    "yossi_extraction_verified",
    "needs_specific_confirmation",
    "blocked_unclear_source",
}

OPEN_QUESTION_ALLOWED_VALUES = {"no", "needs_review", "false", ""}
CLOSED_BOOLEAN_VALUES = {"false", "no", ""}
FORBIDDEN_READY_VALUES = {
    "runtime_ready",
    "question_ready",
    "student_facing",
    "reviewed_bank_ready",
    "protected_preview_ready",
    "approved",
    "promoted",
}

REVIEW_PACKET_REQUIRED_PHRASES = (
    "extraction-accuracy confirmation for trusted source-derived content",
    "not generated-question review",
    "not runtime approval",
)

PROOF_REVIEW_PACKET_REQUIRED_PHRASES = (
    "extraction-accuracy and mapping confirmation for trusted source-derived content",
    "not generated-question review",
    "not runtime approval",
)

PROOF_VERIFICATION_REPORT_REQUIRED_PHRASES = (
    "Yossi reviewed the Bereishis 1:1-1:5 source-to-skill proof map",
    "verified all rows for extraction accuracy",
    "not runtime approval",
    "not question approval",
    "Question allowed: `needs_review`",
)

NEXT_SLICE_REVIEW_PACKET_REQUIRED_PHRASES = (
    "extraction-accuracy and mapping confirmation for trusted source-derived content",
    "not generated-question review",
    "not question approval",
    "not protected-preview approval",
    "not reviewed-bank approval",
    "not runtime approval",
)

NEXT_SLICE_BUILD_REPORT_REQUIRED_PHRASES = (
    "pending Yossi extraction-accuracy review",
    "does not authorize question generation",
    "runtime activation",
)

PENDING_SLICE_REVIEW_PACKET_REQUIRED_PHRASES = (
    "extraction-accuracy and mapping confirmation for trusted source-derived content",
    "not generated-question review",
    "not question approval",
    "not protected-preview approval",
    "not reviewed-bank approval",
    "not runtime approval",
    "High-Risk Rows Needing Yossi Review",
    "Long Parentheticals Needing Review",
    "Long Hebrew Phrase Boundaries Needing Review",
    "Awkward But Source-Derived Wording",
)

PENDING_SLICE_BUILD_REPORT_REQUIRED_PHRASES = (
    "pending Yossi extraction-accuracy review",
    "does not authorize question generation",
    "runtime activation",
)

PEREK_ONE_FINAL_SLICE_REVIEW_PACKET_REQUIRED_PHRASES = (
    "extraction-accuracy and mapping confirmation for trusted source-derived content",
    "not generated-question review",
    "not question approval",
    "not protected-preview approval",
    "not reviewed-bank approval",
    "not runtime approval",
    "not student-facing approval",
    "High-Risk Rows Needing Yossi Review",
    "Long Parentheticals Needing Review",
    "Long Hebrew Phrase Boundaries Needing Review",
    "Awkward But Source-Derived Wording",
)

PEREK_ONE_FINAL_SLICE_BUILD_REPORT_REQUIRED_PHRASES = (
    "pending Yossi extraction-accuracy review",
    "does not authorize question generation",
    "runtime activation",
)

NEXT_SLICE_VERIFICATION_REPORT_REQUIRED_PHRASES = (
    "Yossi reviewed and verified all 37 rows",
    "extraction-accuracy confirmation only",
    "Not question approval",
    "Not protected-preview approval",
    "Not runtime approval",
    "`question_allowed` remains `needs_review`",
    "`runtime_allowed` remains `false`",
)

PENDING_SLICE_VERIFICATION_REPORT_REQUIRED_PHRASES = (
    "Yossi reviewed and verified all 39 rows",
    "extraction-accuracy verification",
    "Parenthetical explanations are acceptable as source-derived wording",
    "Awkward English wording should be preserved as source-derived wording",
    "Not question approval",
    "Not protected-preview approval",
    "Not reviewed-bank approval",
    "Not runtime approval",
    "Not student-facing release",
    "`question_allowed` remains `needs_review`",
    "`runtime_allowed` remains `false`",
)

PEREK_ONE_FINAL_SLICE_VERIFICATION_REPORT_REQUIRED_PHRASES = (
    "Yossi reviewed and verified all 38 rows",
    "extraction-accuracy confirmation only",
    "Not question approval",
    "Not protected-preview approval",
    "Not reviewed-bank promotion",
    "Not runtime approval",
    "Not student-facing release",
    "`question_allowed` remains `needs_review`",
    "`runtime_allowed` remains `false`",
    "`protected_preview_allowed` remains `false`",
    "`reviewed_bank_allowed` remains `false`",
)

PEREK_ONE_COMPLETION_REPORT_REQUIRED_PHRASES = (
    "Bereishis Perek 1 now has complete extraction-verified source-to-skill coverage",
    "Total verified rows: 137",
    "Bereishis 1:1-1:31",
    "`extraction_review_status = yossi_extraction_verified`: 137",
    "`question_allowed = needs_review`: 137",
    "`runtime_allowed = false`: 137",
    "`protected_preview_allowed = false`: 137",
    "`reviewed_bank_allowed = false`: 137",
    "question approval",
    "protected-preview approval",
    "reviewed-bank approval",
    "runtime approval",
    "student-facing release",
    "morphology enrichment",
    "Zekelman standards mapping",
)

PEREK_TWO_OPENING_SLICE_REVIEW_PACKET_REQUIRED_PHRASES = (
    "extraction-accuracy and mapping confirmation for trusted source-derived content",
    "not generated-question review",
    "not question approval",
    "not protected-preview approval",
    "not reviewed-bank approval",
    "not runtime approval",
    "pending_yossi_extraction_accuracy_pass",
    "High-Risk Rows Needing Yossi Review",
    "Long Parentheticals Needing Review",
    "Long Hebrew Phrase Boundaries Needing Review",
)

PEREK_TWO_OPENING_SLICE_BUILD_REPORT_REQUIRED_PHRASES = (
    "pending Yossi extraction-accuracy review",
    "does not authorize question generation",
    "runtime activation",
    "Row count: 9",
)

PEREK_TWO_EXPANSION_SLICE_REVIEW_PACKET_REQUIRED_PHRASES = (
    "extraction-accuracy and mapping confirmation for trusted source-derived content",
    "not generated-question review",
    "not question approval",
    "not protected-preview approval",
    "not reviewed-bank approval",
    "not runtime approval",
    "pending_yossi_extraction_accuracy_pass",
    "High-Risk Rows Needing Yossi Review",
    "Long Parentheticals Needing Review",
    "Long Hebrew Phrase Boundaries Needing Review",
)

PEREK_TWO_EXPANSION_SLICE_BUILD_REPORT_REQUIRED_PHRASES = (
    "pending Yossi extraction-accuracy review",
    "does not authorize question generation",
    "runtime activation",
    "Row count: 54",
)

PEREK_TWO_FINAL_SLICE_REVIEW_PACKET_REQUIRED_PHRASES = (
    "extraction-accuracy and mapping confirmation for trusted source-derived content",
    "not generated-question review",
    "not question approval",
    "not protected-preview approval",
    "not reviewed-bank approval",
    "not runtime approval",
    "pending_yossi_extraction_accuracy_pass",
    "High-Risk Rows Needing Yossi Review",
    "Long Parentheticals Needing Review",
    "Long Hebrew Phrase Boundaries Needing Review",
)

PEREK_TWO_FINAL_SLICE_BUILD_REPORT_REQUIRED_PHRASES = (
    "pending Yossi extraction-accuracy review",
    "does not authorize question generation",
    "runtime activation",
    "Row count: 36",
)

YOSSI_REVIEW_SHEET_COLUMNS = (
    "row_id",
    "ref",
    "hebrew_phrase",
    "linear_translation",
    "metsudah_context",
    "koren_context",
    "skill_primary",
    "skill_secondary",
    "current_status",
    "issue_type",
    "what_to_check",
    "recommended_default_decision",
    "yossi_decision",
    "yossi_notes",
)

YOSSI_REVIEW_DECISIONS = {
    "verified",
    "fix_translation",
    "fix_hebrew_phrase",
    "fix_phrase_boundary",
    "fix_skill_classification",
    "source_only",
    "block_for_questions",
    "needs_follow_up",
}

YOSSI_REVIEW_SHEET_MD_REQUIRED_PHRASES = (
    "Yossi Source-to-Skill Review Sheet",
    "Mark each row with one of the allowed decisions. If everything is accurate, use `verified`.",
    "Your job is not to approve questions.",
    "source-to-skill extraction is accurate enough to mark this slice extraction-verified",
    "All question, preview, reviewed-bank, runtime, and student-facing gates remain closed.",
    "Not question approval.",
    "Not protected-preview approval.",
    "Not reviewed-bank approval.",
    "Not runtime approval.",
    "Not student-facing release.",
)

PEREK_TWO_OPENING_SLICE_VERIFICATION_REPORT_REQUIRED_PHRASES = (
    "Yossi reviewed the Markdown/CSV review sheet",
    "Rows verified: 9",
    "Markdown review sheet: `data/verified_source_skill_maps/reports/bereishis_2_1_to_2_3_yossi_review_sheet.md`",
    "CSV review sheet: `data/verified_source_skill_maps/reports/bereishis_2_1_to_2_3_yossi_review_sheet.csv`",
    "Not question approval",
    "Not protected-preview approval",
    "Not reviewed-bank promotion",
    "Not runtime approval",
    "Not student-facing release",
    "`question_allowed` remains `needs_review`",
    "`runtime_allowed` remains `false`",
    "`protected_preview_allowed` remains `false`",
    "`reviewed_bank_allowed` remains `false`",
)

PEREK_TWO_EXPANSION_SLICE_VERIFICATION_REPORT_REQUIRED_PHRASES = (
    "Yossi reviewed the Bereishis 2:4-2:17 Yossi review sheet",
    "Rows verified: 54",
    "Markdown review sheet: `data/verified_source_skill_maps/reports/bereishis_2_4_to_2_17_yossi_review_sheet.md`",
    "CSV review sheet: `data/verified_source_skill_maps/reports/bereishis_2_4_to_2_17_yossi_review_sheet.csv`",
    "Yossi note: all 54 rows should remain source-only",
    "Not question approval",
    "Not protected-preview approval",
    "Not reviewed-bank promotion",
    "Not runtime approval",
    "Not student-facing release",
    "`question_allowed` remains `needs_review`",
    "`runtime_allowed` remains `false`",
    "`protected_preview_allowed` remains `false`",
    "`reviewed_bank_allowed` remains `false`",
)

PEREK_TWO_FINAL_SLICE_VERIFICATION_REPORT_REQUIRED_PHRASES = (
    "Yossi reviewed the Bereishis 2:18-2:25 Yossi review sheet",
    "Rows verified: 36",
    "Markdown review sheet: `data/verified_source_skill_maps/reports/bereishis_2_18_to_2_25_yossi_review_sheet.md`",
    "CSV review sheet: `data/verified_source_skill_maps/reports/bereishis_2_18_to_2_25_yossi_review_sheet.csv`",
    "Yossi note: all 36 rows should remain source-only",
    "Not question approval",
    "Not protected-preview approval",
    "Not reviewed-bank promotion",
    "Not runtime approval",
    "Not student-facing release",
    "`question_allowed` remains `needs_review`",
    "`runtime_allowed` remains `false`",
    "`protected_preview_allowed` remains `false`",
    "`reviewed_bank_allowed` remains `false`",
)

PEREK_TWO_COMPLETION_REPORT_REQUIRED_PHRASES = (
    "Bereishis Perek 2 now has complete extraction-verified source-to-skill coverage",
    "Total verified rows: 99",
    "Bereishis 2:1-2:25",
    "Perek 1 verified rows: 137",
    "Perek 2 verified rows: 99",
    "Total verified rows through Bereishis 2:25: 236",
    "Question generation remains blocked",
    "protected-preview approval",
    "reviewed-bank promotion",
    "runtime activation",
)

PEREK_THREE_OPENING_SLICE_REVIEW_PACKET_REQUIRED_PHRASES = (
    "extraction-accuracy and mapping confirmation for trusted source-derived content",
    "not generated-question review",
    "not question approval",
    "not protected-preview approval",
    "not reviewed-bank approval",
    "not runtime approval",
    "pending_yossi_extraction_accuracy_pass",
    "High-Risk Rows Needing Yossi Review",
    "Long Parentheticals Needing Review",
    "Long Hebrew Phrase Boundaries Needing Review",
)

PEREK_THREE_OPENING_SLICE_BUILD_REPORT_REQUIRED_PHRASES = (
    "pending Yossi extraction-accuracy review",
    "does not authorize question generation",
    "runtime activation",
    "Row count: 33",
)

PEREK_THREE_OPENING_SLICE_VERIFICATION_REPORT_REQUIRED_PHRASES = (
    "Yossi reviewed the Bereishis 3:1-3:7 Yossi review sheet",
    "Rows verified: 33",
    "Markdown review sheet: `data/verified_source_skill_maps/reports/bereishis_3_1_to_3_7_yossi_review_sheet.md`",
    "CSV review sheet: `data/verified_source_skill_maps/reports/bereishis_3_1_to_3_7_yossi_review_sheet.csv`",
    "Yossi marked all 33 rows source-only",
    "Dialogue and persuasion language",
    "Not question approval",
    "Not protected-preview approval",
    "Not reviewed-bank promotion",
    "Not runtime approval",
    "Not student-facing release",
    "`question_allowed` remains `needs_review`",
    "`runtime_allowed` remains `false`",
    "`protected_preview_allowed` remains `false`",
    "`reviewed_bank_allowed` remains `false`",
)

PEREK_THREE_EXPANSION_SLICE_REVIEW_PACKET_REQUIRED_PHRASES = (
    "extraction-accuracy and mapping confirmation for trusted source-derived content",
    "not generated-question review",
    "not question approval",
    "not protected-preview approval",
    "not reviewed-bank approval",
    "not runtime approval",
    "pending_yossi_extraction_accuracy_pass",
    "High-Risk Rows Needing Yossi Review",
    "Long Parentheticals Needing Review",
    "Long Hebrew Phrase Boundaries Needing Review",
)

PEREK_THREE_EXPANSION_SLICE_BUILD_REPORT_REQUIRED_PHRASES = (
    "pending Yossi extraction-accuracy review",
    "does not authorize question generation",
    "runtime activation",
    "Row count: 48",
)

PEREK_THREE_EXPANSION_SLICE_VERIFICATION_REPORT_REQUIRED_PHRASES = (
    "Yossi reviewed the Bereishis 3:8-3:16 Yossi review sheet",
    "Rows verified: 48",
    "Markdown review sheet: `data/verified_source_skill_maps/reports/bereishis_3_8_to_3_16_yossi_review_sheet.md`",
    "CSV review sheet: `data/verified_source_skill_maps/reports/bereishis_3_8_to_3_16_yossi_review_sheet.csv`",
    "Yossi marked all 48 rows source-only",
    "Dialogue, accountability, curse/consequence language, and narrative flow",
    "Not question approval",
    "Not protected-preview approval",
    "Not reviewed-bank promotion",
    "Not runtime approval",
    "Not student-facing release",
    "`question_allowed` remains `needs_review`",
    "`runtime_allowed` remains `false`",
    "`protected_preview_allowed` remains `false`",
    "`reviewed_bank_allowed` remains `false`",
)

PEREK_THREE_FINAL_SLICE_REVIEW_PACKET_REQUIRED_PHRASES = (
    "extraction-accuracy and mapping confirmation for trusted source-derived content",
    "not generated-question review",
    "not question approval",
    "not protected-preview approval",
    "not reviewed-bank approval",
    "not runtime approval",
    "pending_yossi_extraction_accuracy_pass",
    "High-Risk Rows Needing Yossi Review",
    "Long Parentheticals Needing Review",
    "Long Hebrew Phrase Boundaries Needing Review",
)

PEREK_THREE_FINAL_SLICE_BUILD_REPORT_REQUIRED_PHRASES = (
    "pending Yossi extraction-accuracy review",
    "does not authorize question generation",
    "runtime activation",
    "Row count: 38",
)

PEREK_THREE_FINAL_SLICE_VERIFICATION_REPORT_REQUIRED_PHRASES = (
    "Yossi reviewed the Bereishis 3:17-3:24 Yossi review sheet",
    "Rows verified: 38",
    "Markdown review sheet: `data/verified_source_skill_maps/reports/bereishis_3_17_to_3_24_yossi_review_sheet.md`",
    "CSV review sheet: `data/verified_source_skill_maps/reports/bereishis_3_17_to_3_24_yossi_review_sheet.csv`",
    "Yossi marked all 38 rows source-only",
    "Consequence/exile/Gan Eden closure language",
    "Not question approval",
    "Not protected-preview approval",
    "Not reviewed-bank promotion",
    "Not runtime approval",
    "Not student-facing release",
    "`question_allowed` remains `needs_review`",
    "`runtime_allowed` remains `false`",
    "`protected_preview_allowed` remains `false`",
    "`reviewed_bank_allowed` remains `false`",
)

PEREK_THREE_COMPLETION_REPORT_REQUIRED_PHRASES = (
    "Bereishis Perek 3 now has complete extraction-verified source-to-skill coverage",
    "Total verified rows: 119",
    "Bereishis 3:1-3:24",
    "Perek 1 verified rows: 137",
    "Perek 2 verified rows: 99",
    "Perek 3 verified rows: 119",
    "Total verified rows through Bereishis 3:24: 355",
    "Question generation remains blocked",
    "protected-preview approval",
    "reviewed-bank promotion",
    "runtime activation",
)

REVIEW_PACKET_FORBIDDEN_PHRASES = (
    "approved for runtime",
    "runtime-ready",
    "question-ready",
    "student-facing approved",
)


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def normalized(value: object) -> str:
    return str(value or "").strip()


def validate_required_files(errors: list[str]) -> None:
    if not MAP_DIR.exists():
        errors.append("data/verified_source_skill_maps directory is missing")
    if not SEED_MAP_PATH.exists():
        errors.append(f"required seed source-to-skill map missing: {repo_relative(SEED_MAP_PATH)}")
    if not PROOF_MAP_PATH.exists():
        errors.append(f"required proof source-to-skill map missing: {repo_relative(PROOF_MAP_PATH)}")
    if not SEED_REVIEW_PACKET_PATH.exists():
        errors.append(f"required source-to-skill review packet missing: {repo_relative(SEED_REVIEW_PACKET_PATH)}")
    if not PROOF_REVIEW_PACKET_PATH.exists():
        errors.append(f"required proof source-to-skill review packet missing: {repo_relative(PROOF_REVIEW_PACKET_PATH)}")
    if not PROOF_VERIFICATION_REPORT_PATH.exists():
        errors.append(
            f"required proof source-to-skill extraction verification report missing: {repo_relative(PROOF_VERIFICATION_REPORT_PATH)}"
        )
    if not NEXT_SLICE_MAP_PATH.exists():
        errors.append(f"required pending expansion source-to-skill map missing: {repo_relative(NEXT_SLICE_MAP_PATH)}")
    if not NEXT_SLICE_BUILD_REPORT_PATH.exists():
        errors.append(f"required pending expansion build report missing: {repo_relative(NEXT_SLICE_BUILD_REPORT_PATH)}")
    if not NEXT_SLICE_REVIEW_PACKET_PATH.exists():
        errors.append(f"required pending expansion review packet missing: {repo_relative(NEXT_SLICE_REVIEW_PACKET_PATH)}")
    if not NEXT_SLICE_VERIFICATION_REPORT_PATH.exists():
        errors.append(
            f"required next-slice extraction verification report missing: {repo_relative(NEXT_SLICE_VERIFICATION_REPORT_PATH)}"
        )
    if not PENDING_SLICE_MAP_PATH.exists():
        errors.append(f"required pending source-to-skill map missing: {repo_relative(PENDING_SLICE_MAP_PATH)}")
    if not PENDING_SLICE_BUILD_REPORT_PATH.exists():
        errors.append(f"required pending source-to-skill build report missing: {repo_relative(PENDING_SLICE_BUILD_REPORT_PATH)}")
    if not PENDING_SLICE_REVIEW_PACKET_PATH.exists():
        errors.append(f"required pending source-to-skill review packet missing: {repo_relative(PENDING_SLICE_REVIEW_PACKET_PATH)}")
    if not PENDING_SLICE_VERIFICATION_REPORT_PATH.exists():
        errors.append(
            f"required current-slice extraction verification report missing: {repo_relative(PENDING_SLICE_VERIFICATION_REPORT_PATH)}"
        )
    if not PEREK_ONE_FINAL_SLICE_MAP_PATH.exists():
        errors.append(f"required perek-one final pending source-to-skill map missing: {repo_relative(PEREK_ONE_FINAL_SLICE_MAP_PATH)}")
    if not PEREK_ONE_FINAL_SLICE_BUILD_REPORT_PATH.exists():
        errors.append(
            f"required perek-one final pending source-to-skill build report missing: {repo_relative(PEREK_ONE_FINAL_SLICE_BUILD_REPORT_PATH)}"
        )
    if not PEREK_ONE_FINAL_SLICE_REVIEW_PACKET_PATH.exists():
        errors.append(
            f"required perek-one final pending source-to-skill review packet missing: {repo_relative(PEREK_ONE_FINAL_SLICE_REVIEW_PACKET_PATH)}"
        )
    if not PEREK_ONE_FINAL_SLICE_VERIFICATION_REPORT_PATH.exists():
        errors.append(
            f"required perek-one final extraction verification report missing: {repo_relative(PEREK_ONE_FINAL_SLICE_VERIFICATION_REPORT_PATH)}"
        )
    if not PEREK_ONE_COMPLETION_REPORT_PATH.exists():
        errors.append(
            f"required perek-one source-to-skill completion report missing: {repo_relative(PEREK_ONE_COMPLETION_REPORT_PATH)}"
        )
    if not PEREK_TWO_OPENING_SLICE_MAP_PATH.exists():
        errors.append(
            f"required perek-two opening pending source-to-skill map missing: {repo_relative(PEREK_TWO_OPENING_SLICE_MAP_PATH)}"
        )
    if not PEREK_TWO_OPENING_SLICE_BUILD_REPORT_PATH.exists():
        errors.append(
            f"required perek-two opening pending source-to-skill build report missing: {repo_relative(PEREK_TWO_OPENING_SLICE_BUILD_REPORT_PATH)}"
        )
    if not PEREK_TWO_OPENING_SLICE_REVIEW_PACKET_PATH.exists():
        errors.append(
            f"required perek-two opening pending source-to-skill review packet missing: {repo_relative(PEREK_TWO_OPENING_SLICE_REVIEW_PACKET_PATH)}"
        )
    if not PEREK_TWO_OPENING_SLICE_REVIEW_SHEET_MD_PATH.exists():
        errors.append(
            f"required perek-two opening Yossi Markdown review sheet missing: {repo_relative(PEREK_TWO_OPENING_SLICE_REVIEW_SHEET_MD_PATH)}"
        )
    if not PEREK_TWO_OPENING_SLICE_REVIEW_SHEET_CSV_PATH.exists():
        errors.append(
            f"required perek-two opening Yossi CSV review sheet missing: {repo_relative(PEREK_TWO_OPENING_SLICE_REVIEW_SHEET_CSV_PATH)}"
        )
    if not PEREK_TWO_OPENING_SLICE_VERIFICATION_REPORT_PATH.exists():
        errors.append(
            f"required perek-two opening extraction verification report missing: {repo_relative(PEREK_TWO_OPENING_SLICE_VERIFICATION_REPORT_PATH)}"
        )
    if not PEREK_TWO_EXPANSION_SLICE_MAP_PATH.exists():
        errors.append(
            f"required perek-two expansion pending source-to-skill map missing: {repo_relative(PEREK_TWO_EXPANSION_SLICE_MAP_PATH)}"
        )
    if not PEREK_TWO_EXPANSION_SLICE_BUILD_REPORT_PATH.exists():
        errors.append(
            f"required perek-two expansion pending source-to-skill build report missing: {repo_relative(PEREK_TWO_EXPANSION_SLICE_BUILD_REPORT_PATH)}"
        )
    if not PEREK_TWO_EXPANSION_SLICE_REVIEW_PACKET_PATH.exists():
        errors.append(
            f"required perek-two expansion pending source-to-skill review packet missing: {repo_relative(PEREK_TWO_EXPANSION_SLICE_REVIEW_PACKET_PATH)}"
        )
    if not PEREK_TWO_EXPANSION_SLICE_REVIEW_SHEET_MD_PATH.exists():
        errors.append(
            f"required perek-two expansion Yossi Markdown review sheet missing: {repo_relative(PEREK_TWO_EXPANSION_SLICE_REVIEW_SHEET_MD_PATH)}"
        )
    if not PEREK_TWO_EXPANSION_SLICE_REVIEW_SHEET_CSV_PATH.exists():
        errors.append(
            f"required perek-two expansion Yossi CSV review sheet missing: {repo_relative(PEREK_TWO_EXPANSION_SLICE_REVIEW_SHEET_CSV_PATH)}"
        )
    if not PEREK_TWO_EXPANSION_SLICE_VERIFICATION_REPORT_PATH.exists():
        errors.append(
            f"required perek-two expansion extraction verification report missing: {repo_relative(PEREK_TWO_EXPANSION_SLICE_VERIFICATION_REPORT_PATH)}"
        )
    if not PEREK_TWO_FINAL_SLICE_MAP_PATH.exists():
        errors.append(
            f"required perek-two final pending source-to-skill map missing: {repo_relative(PEREK_TWO_FINAL_SLICE_MAP_PATH)}"
        )
    if not PEREK_TWO_FINAL_SLICE_BUILD_REPORT_PATH.exists():
        errors.append(
            f"required perek-two final pending source-to-skill build report missing: {repo_relative(PEREK_TWO_FINAL_SLICE_BUILD_REPORT_PATH)}"
        )
    if not PEREK_TWO_FINAL_SLICE_REVIEW_PACKET_PATH.exists():
        errors.append(
            f"required perek-two final pending source-to-skill review packet missing: {repo_relative(PEREK_TWO_FINAL_SLICE_REVIEW_PACKET_PATH)}"
        )
    if not PEREK_TWO_FINAL_SLICE_REVIEW_SHEET_MD_PATH.exists():
        errors.append(
            f"required perek-two final Yossi Markdown review sheet missing: {repo_relative(PEREK_TWO_FINAL_SLICE_REVIEW_SHEET_MD_PATH)}"
        )
    if not PEREK_TWO_FINAL_SLICE_REVIEW_SHEET_CSV_PATH.exists():
        errors.append(
            f"required perek-two final Yossi UTF-8-BOM CSV review sheet missing: {repo_relative(PEREK_TWO_FINAL_SLICE_REVIEW_SHEET_CSV_PATH)}"
        )
    if not PEREK_TWO_FINAL_SLICE_VERIFICATION_REPORT_PATH.exists():
        errors.append(
            f"required perek-two final extraction verification report missing: {repo_relative(PEREK_TWO_FINAL_SLICE_VERIFICATION_REPORT_PATH)}"
        )
    if not PEREK_TWO_COMPLETION_REPORT_PATH.exists():
        errors.append(
            f"required perek-two source-to-skill completion report missing: {repo_relative(PEREK_TWO_COMPLETION_REPORT_PATH)}"
        )
    if not PEREK_THREE_OPENING_SLICE_MAP_PATH.exists():
        errors.append(
            f"required perek-three opening pending source-to-skill map missing: {repo_relative(PEREK_THREE_OPENING_SLICE_MAP_PATH)}"
        )
    if not PEREK_THREE_OPENING_SLICE_BUILD_REPORT_PATH.exists():
        errors.append(
            f"required perek-three opening pending source-to-skill build report missing: {repo_relative(PEREK_THREE_OPENING_SLICE_BUILD_REPORT_PATH)}"
        )
    if not PEREK_THREE_OPENING_SLICE_REVIEW_PACKET_PATH.exists():
        errors.append(
            f"required perek-three opening pending source-to-skill review packet missing: {repo_relative(PEREK_THREE_OPENING_SLICE_REVIEW_PACKET_PATH)}"
        )
    if not PEREK_THREE_OPENING_SLICE_REVIEW_SHEET_MD_PATH.exists():
        errors.append(
            f"required perek-three opening Yossi Markdown review sheet missing: {repo_relative(PEREK_THREE_OPENING_SLICE_REVIEW_SHEET_MD_PATH)}"
        )
    if not PEREK_THREE_OPENING_SLICE_REVIEW_SHEET_CSV_PATH.exists():
        errors.append(
            f"required perek-three opening Yossi UTF-8-BOM CSV review sheet missing: {repo_relative(PEREK_THREE_OPENING_SLICE_REVIEW_SHEET_CSV_PATH)}"
        )
    if not PEREK_THREE_OPENING_SLICE_VERIFICATION_REPORT_PATH.exists():
        errors.append(
            f"required perek-three opening extraction verification report missing: {repo_relative(PEREK_THREE_OPENING_SLICE_VERIFICATION_REPORT_PATH)}"
        )
    if not PEREK_THREE_EXPANSION_SLICE_MAP_PATH.exists():
        errors.append(
            f"required perek-three expansion pending source-to-skill map missing: {repo_relative(PEREK_THREE_EXPANSION_SLICE_MAP_PATH)}"
        )
    if not PEREK_THREE_EXPANSION_SLICE_BUILD_REPORT_PATH.exists():
        errors.append(
            f"required perek-three expansion pending source-to-skill build report missing: {repo_relative(PEREK_THREE_EXPANSION_SLICE_BUILD_REPORT_PATH)}"
        )
    if not PEREK_THREE_EXPANSION_SLICE_REVIEW_PACKET_PATH.exists():
        errors.append(
            f"required perek-three expansion pending source-to-skill review packet missing: {repo_relative(PEREK_THREE_EXPANSION_SLICE_REVIEW_PACKET_PATH)}"
        )
    if not PEREK_THREE_EXPANSION_SLICE_REVIEW_SHEET_MD_PATH.exists():
        errors.append(
            f"required perek-three expansion Yossi Markdown review sheet missing: {repo_relative(PEREK_THREE_EXPANSION_SLICE_REVIEW_SHEET_MD_PATH)}"
        )
    if not PEREK_THREE_EXPANSION_SLICE_REVIEW_SHEET_CSV_PATH.exists():
        errors.append(
            f"required perek-three expansion Yossi UTF-8-BOM CSV review sheet missing: {repo_relative(PEREK_THREE_EXPANSION_SLICE_REVIEW_SHEET_CSV_PATH)}"
        )
    if not PEREK_THREE_EXPANSION_SLICE_VERIFICATION_REPORT_PATH.exists():
        errors.append(
            f"required perek-three expansion extraction verification report missing: {repo_relative(PEREK_THREE_EXPANSION_SLICE_VERIFICATION_REPORT_PATH)}"
        )
    if not PEREK_THREE_FINAL_SLICE_MAP_PATH.exists():
        errors.append(
            f"required perek-three final pending source-to-skill map missing: {repo_relative(PEREK_THREE_FINAL_SLICE_MAP_PATH)}"
        )
    if not PEREK_THREE_FINAL_SLICE_BUILD_REPORT_PATH.exists():
        errors.append(
            f"required perek-three final pending source-to-skill build report missing: {repo_relative(PEREK_THREE_FINAL_SLICE_BUILD_REPORT_PATH)}"
        )
    if not PEREK_THREE_FINAL_SLICE_REVIEW_PACKET_PATH.exists():
        errors.append(
            f"required perek-three final pending source-to-skill review packet missing: {repo_relative(PEREK_THREE_FINAL_SLICE_REVIEW_PACKET_PATH)}"
        )
    if not PEREK_THREE_FINAL_SLICE_REVIEW_SHEET_MD_PATH.exists():
        errors.append(
            f"required perek-three final Yossi Markdown review sheet missing: {repo_relative(PEREK_THREE_FINAL_SLICE_REVIEW_SHEET_MD_PATH)}"
        )
    if not PEREK_THREE_FINAL_SLICE_REVIEW_SHEET_CSV_PATH.exists():
        errors.append(
            f"required perek-three final Yossi UTF-8-BOM CSV review sheet missing: {repo_relative(PEREK_THREE_FINAL_SLICE_REVIEW_SHEET_CSV_PATH)}"
        )
    if not PEREK_THREE_FINAL_SLICE_VERIFICATION_REPORT_PATH.exists():
        errors.append(
            f"required perek-three final extraction verification report missing: {repo_relative(PEREK_THREE_FINAL_SLICE_VERIFICATION_REPORT_PATH)}"
        )
    if not PEREK_THREE_COMPLETION_REPORT_PATH.exists():
        errors.append(
            f"required perek-three source-to-skill completion report missing: {repo_relative(PEREK_THREE_COMPLETION_REPORT_PATH)}"
        )
    if not AUDIT_REPORT_PATH.exists():
        errors.append(f"required source-to-skill audit report missing: {repo_relative(AUDIT_REPORT_PATH)}")


def validate_review_packet(errors: list[str]) -> None:
    if not SEED_REVIEW_PACKET_PATH.exists():
        return
    text = SEED_REVIEW_PACKET_PATH.read_text(encoding="utf-8")
    for phrase in REVIEW_PACKET_REQUIRED_PHRASES:
        if phrase not in text:
            errors.append(
                f"{repo_relative(SEED_REVIEW_PACKET_PATH)} is missing required extraction-accuracy language: {phrase!r}"
            )
    for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
        if phrase in text and f"not {phrase}" not in text:
            errors.append(
                f"{repo_relative(SEED_REVIEW_PACKET_PATH)} contains forbidden readiness language: {phrase!r}"
            )
    if PROOF_REVIEW_PACKET_PATH.exists():
        proof_text = PROOF_REVIEW_PACKET_PATH.read_text(encoding="utf-8")
        for phrase in PROOF_REVIEW_PACKET_REQUIRED_PHRASES:
            if phrase not in proof_text:
                errors.append(
                    f"{repo_relative(PROOF_REVIEW_PACKET_PATH)} is missing required proof review language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in proof_text and f"not {phrase}" not in proof_text:
                errors.append(
                    f"{repo_relative(PROOF_REVIEW_PACKET_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if PROOF_VERIFICATION_REPORT_PATH.exists():
        verification_text = PROOF_VERIFICATION_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in PROOF_VERIFICATION_REPORT_REQUIRED_PHRASES:
            if phrase not in verification_text:
                errors.append(
                    f"{repo_relative(PROOF_VERIFICATION_REPORT_PATH)} is missing required verification language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in verification_text and f"not {phrase}" not in verification_text:
                errors.append(
                    f"{repo_relative(PROOF_VERIFICATION_REPORT_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if NEXT_SLICE_REVIEW_PACKET_PATH.exists():
        next_text = NEXT_SLICE_REVIEW_PACKET_PATH.read_text(encoding="utf-8")
        for phrase in NEXT_SLICE_REVIEW_PACKET_REQUIRED_PHRASES:
            if phrase not in next_text:
                errors.append(
                    f"{repo_relative(NEXT_SLICE_REVIEW_PACKET_PATH)} is missing required pending-slice review language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in next_text and f"not {phrase}" not in next_text:
                errors.append(
                    f"{repo_relative(NEXT_SLICE_REVIEW_PACKET_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if NEXT_SLICE_BUILD_REPORT_PATH.exists():
        build_text = NEXT_SLICE_BUILD_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in NEXT_SLICE_BUILD_REPORT_REQUIRED_PHRASES:
            if phrase not in build_text:
                errors.append(
                    f"{repo_relative(NEXT_SLICE_BUILD_REPORT_PATH)} is missing required build-report language: {phrase!r}"
                )
    if NEXT_SLICE_VERIFICATION_REPORT_PATH.exists():
        next_verification_text = NEXT_SLICE_VERIFICATION_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in NEXT_SLICE_VERIFICATION_REPORT_REQUIRED_PHRASES:
            if phrase not in next_verification_text:
                errors.append(
                    f"{repo_relative(NEXT_SLICE_VERIFICATION_REPORT_PATH)} is missing required verification language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in next_verification_text and f"not {phrase}" not in next_verification_text:
                errors.append(
                    f"{repo_relative(NEXT_SLICE_VERIFICATION_REPORT_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if PENDING_SLICE_REVIEW_PACKET_PATH.exists():
        pending_text = PENDING_SLICE_REVIEW_PACKET_PATH.read_text(encoding="utf-8")
        for phrase in PENDING_SLICE_REVIEW_PACKET_REQUIRED_PHRASES:
            if phrase not in pending_text:
                errors.append(
                    f"{repo_relative(PENDING_SLICE_REVIEW_PACKET_PATH)} is missing required pending-slice review language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in pending_text and f"not {phrase}" not in pending_text:
                errors.append(
                    f"{repo_relative(PENDING_SLICE_REVIEW_PACKET_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if PENDING_SLICE_BUILD_REPORT_PATH.exists():
        pending_build_text = PENDING_SLICE_BUILD_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in PENDING_SLICE_BUILD_REPORT_REQUIRED_PHRASES:
            if phrase not in pending_build_text:
                errors.append(
                    f"{repo_relative(PENDING_SLICE_BUILD_REPORT_PATH)} is missing required build-report language: {phrase!r}"
                )
    if PENDING_SLICE_VERIFICATION_REPORT_PATH.exists():
        pending_verification_text = PENDING_SLICE_VERIFICATION_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in PENDING_SLICE_VERIFICATION_REPORT_REQUIRED_PHRASES:
            if phrase not in pending_verification_text:
                errors.append(
                    f"{repo_relative(PENDING_SLICE_VERIFICATION_REPORT_PATH)} is missing required verification language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in pending_verification_text and f"not {phrase}" not in pending_verification_text:
                errors.append(
                    f"{repo_relative(PENDING_SLICE_VERIFICATION_REPORT_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if PEREK_ONE_FINAL_SLICE_REVIEW_PACKET_PATH.exists():
        final_slice_text = PEREK_ONE_FINAL_SLICE_REVIEW_PACKET_PATH.read_text(encoding="utf-8")
        for phrase in PEREK_ONE_FINAL_SLICE_REVIEW_PACKET_REQUIRED_PHRASES:
            if phrase not in final_slice_text:
                errors.append(
                    f"{repo_relative(PEREK_ONE_FINAL_SLICE_REVIEW_PACKET_PATH)} is missing required perek-one final-slice review language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in final_slice_text and f"not {phrase}" not in final_slice_text:
                errors.append(
                    f"{repo_relative(PEREK_ONE_FINAL_SLICE_REVIEW_PACKET_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if PEREK_ONE_FINAL_SLICE_BUILD_REPORT_PATH.exists():
        final_slice_build_text = PEREK_ONE_FINAL_SLICE_BUILD_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in PEREK_ONE_FINAL_SLICE_BUILD_REPORT_REQUIRED_PHRASES:
            if phrase not in final_slice_build_text:
                errors.append(
                    f"{repo_relative(PEREK_ONE_FINAL_SLICE_BUILD_REPORT_PATH)} is missing required build-report language: {phrase!r}"
                )
    if PEREK_ONE_FINAL_SLICE_VERIFICATION_REPORT_PATH.exists():
        final_slice_verification_text = PEREK_ONE_FINAL_SLICE_VERIFICATION_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in PEREK_ONE_FINAL_SLICE_VERIFICATION_REPORT_REQUIRED_PHRASES:
            if phrase not in final_slice_verification_text:
                errors.append(
                    f"{repo_relative(PEREK_ONE_FINAL_SLICE_VERIFICATION_REPORT_PATH)} is missing required verification language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in final_slice_verification_text and f"not {phrase}" not in final_slice_verification_text:
                errors.append(
                    f"{repo_relative(PEREK_ONE_FINAL_SLICE_VERIFICATION_REPORT_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if PEREK_ONE_COMPLETION_REPORT_PATH.exists():
        perek_one_completion_text = PEREK_ONE_COMPLETION_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in PEREK_ONE_COMPLETION_REPORT_REQUIRED_PHRASES:
            if phrase not in perek_one_completion_text:
                errors.append(
                    f"{repo_relative(PEREK_ONE_COMPLETION_REPORT_PATH)} is missing required completion language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in perek_one_completion_text and f"not {phrase}" not in perek_one_completion_text:
                errors.append(
                    f"{repo_relative(PEREK_ONE_COMPLETION_REPORT_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if PEREK_TWO_OPENING_SLICE_REVIEW_PACKET_PATH.exists():
        perek_two_text = PEREK_TWO_OPENING_SLICE_REVIEW_PACKET_PATH.read_text(encoding="utf-8")
        for phrase in PEREK_TWO_OPENING_SLICE_REVIEW_PACKET_REQUIRED_PHRASES:
            if phrase not in perek_two_text:
                errors.append(
                    f"{repo_relative(PEREK_TWO_OPENING_SLICE_REVIEW_PACKET_PATH)} is missing required perek-two review language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in perek_two_text and f"not {phrase}" not in perek_two_text:
                errors.append(
                    f"{repo_relative(PEREK_TWO_OPENING_SLICE_REVIEW_PACKET_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if PEREK_TWO_OPENING_SLICE_BUILD_REPORT_PATH.exists():
        perek_two_build_text = PEREK_TWO_OPENING_SLICE_BUILD_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in PEREK_TWO_OPENING_SLICE_BUILD_REPORT_REQUIRED_PHRASES:
            if phrase not in perek_two_build_text:
                errors.append(
                    f"{repo_relative(PEREK_TWO_OPENING_SLICE_BUILD_REPORT_PATH)} is missing required build-report language: {phrase!r}"
                )
    if PEREK_TWO_OPENING_SLICE_VERIFICATION_REPORT_PATH.exists():
        perek_two_verification_text = PEREK_TWO_OPENING_SLICE_VERIFICATION_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in PEREK_TWO_OPENING_SLICE_VERIFICATION_REPORT_REQUIRED_PHRASES:
            if phrase not in perek_two_verification_text:
                errors.append(
                    f"{repo_relative(PEREK_TWO_OPENING_SLICE_VERIFICATION_REPORT_PATH)} is missing required verification language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in perek_two_verification_text and f"not {phrase}" not in perek_two_verification_text:
                errors.append(
                    f"{repo_relative(PEREK_TWO_OPENING_SLICE_VERIFICATION_REPORT_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if PEREK_TWO_EXPANSION_SLICE_REVIEW_PACKET_PATH.exists():
        perek_two_expansion_text = PEREK_TWO_EXPANSION_SLICE_REVIEW_PACKET_PATH.read_text(encoding="utf-8")
        for phrase in PEREK_TWO_EXPANSION_SLICE_REVIEW_PACKET_REQUIRED_PHRASES:
            if phrase not in perek_two_expansion_text:
                errors.append(
                    f"{repo_relative(PEREK_TWO_EXPANSION_SLICE_REVIEW_PACKET_PATH)} is missing required perek-two expansion review language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in perek_two_expansion_text and f"not {phrase}" not in perek_two_expansion_text:
                errors.append(
                    f"{repo_relative(PEREK_TWO_EXPANSION_SLICE_REVIEW_PACKET_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if PEREK_TWO_EXPANSION_SLICE_BUILD_REPORT_PATH.exists():
        perek_two_expansion_build_text = PEREK_TWO_EXPANSION_SLICE_BUILD_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in PEREK_TWO_EXPANSION_SLICE_BUILD_REPORT_REQUIRED_PHRASES:
            if phrase not in perek_two_expansion_build_text:
                errors.append(
                    f"{repo_relative(PEREK_TWO_EXPANSION_SLICE_BUILD_REPORT_PATH)} is missing required build-report language: {phrase!r}"
                )
    if PEREK_TWO_EXPANSION_SLICE_VERIFICATION_REPORT_PATH.exists():
        perek_two_expansion_verification_text = PEREK_TWO_EXPANSION_SLICE_VERIFICATION_REPORT_PATH.read_text(
            encoding="utf-8"
        )
        for phrase in PEREK_TWO_EXPANSION_SLICE_VERIFICATION_REPORT_REQUIRED_PHRASES:
            if phrase not in perek_two_expansion_verification_text:
                errors.append(
                    f"{repo_relative(PEREK_TWO_EXPANSION_SLICE_VERIFICATION_REPORT_PATH)} is missing required verification language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in perek_two_expansion_verification_text and f"not {phrase}" not in perek_two_expansion_verification_text:
                errors.append(
                    f"{repo_relative(PEREK_TWO_EXPANSION_SLICE_VERIFICATION_REPORT_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if PEREK_TWO_FINAL_SLICE_REVIEW_PACKET_PATH.exists():
        perek_two_final_text = PEREK_TWO_FINAL_SLICE_REVIEW_PACKET_PATH.read_text(encoding="utf-8")
        for phrase in PEREK_TWO_FINAL_SLICE_REVIEW_PACKET_REQUIRED_PHRASES:
            if phrase not in perek_two_final_text:
                errors.append(
                    f"{repo_relative(PEREK_TWO_FINAL_SLICE_REVIEW_PACKET_PATH)} is missing required perek-two final review language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in perek_two_final_text and f"not {phrase}" not in perek_two_final_text:
                errors.append(
                    f"{repo_relative(PEREK_TWO_FINAL_SLICE_REVIEW_PACKET_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if PEREK_TWO_FINAL_SLICE_BUILD_REPORT_PATH.exists():
        perek_two_final_build_text = PEREK_TWO_FINAL_SLICE_BUILD_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in PEREK_TWO_FINAL_SLICE_BUILD_REPORT_REQUIRED_PHRASES:
            if phrase not in perek_two_final_build_text:
                errors.append(
                    f"{repo_relative(PEREK_TWO_FINAL_SLICE_BUILD_REPORT_PATH)} is missing required build-report language: {phrase!r}"
                )
    if PEREK_TWO_FINAL_SLICE_VERIFICATION_REPORT_PATH.exists():
        perek_two_final_verification_text = PEREK_TWO_FINAL_SLICE_VERIFICATION_REPORT_PATH.read_text(
            encoding="utf-8"
        )
        for phrase in PEREK_TWO_FINAL_SLICE_VERIFICATION_REPORT_REQUIRED_PHRASES:
            if phrase not in perek_two_final_verification_text:
                errors.append(
                    f"{repo_relative(PEREK_TWO_FINAL_SLICE_VERIFICATION_REPORT_PATH)} is missing required verification language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in perek_two_final_verification_text and f"not {phrase}" not in perek_two_final_verification_text:
                errors.append(
                    f"{repo_relative(PEREK_TWO_FINAL_SLICE_VERIFICATION_REPORT_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if PEREK_TWO_COMPLETION_REPORT_PATH.exists():
        perek_two_completion_text = PEREK_TWO_COMPLETION_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in PEREK_TWO_COMPLETION_REPORT_REQUIRED_PHRASES:
            if phrase not in perek_two_completion_text:
                errors.append(
                    f"{repo_relative(PEREK_TWO_COMPLETION_REPORT_PATH)} is missing required completion language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in perek_two_completion_text and f"not {phrase}" not in perek_two_completion_text:
                errors.append(
                    f"{repo_relative(PEREK_TWO_COMPLETION_REPORT_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if PEREK_THREE_OPENING_SLICE_REVIEW_PACKET_PATH.exists():
        perek_three_opening_text = PEREK_THREE_OPENING_SLICE_REVIEW_PACKET_PATH.read_text(encoding="utf-8")
        for phrase in PEREK_THREE_OPENING_SLICE_REVIEW_PACKET_REQUIRED_PHRASES:
            if phrase not in perek_three_opening_text:
                errors.append(
                    f"{repo_relative(PEREK_THREE_OPENING_SLICE_REVIEW_PACKET_PATH)} is missing required perek-three opening review language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in perek_three_opening_text and f"not {phrase}" not in perek_three_opening_text:
                errors.append(
                    f"{repo_relative(PEREK_THREE_OPENING_SLICE_REVIEW_PACKET_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if PEREK_THREE_OPENING_SLICE_BUILD_REPORT_PATH.exists():
        perek_three_opening_build_text = PEREK_THREE_OPENING_SLICE_BUILD_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in PEREK_THREE_OPENING_SLICE_BUILD_REPORT_REQUIRED_PHRASES:
            if phrase not in perek_three_opening_build_text:
                errors.append(
                    f"{repo_relative(PEREK_THREE_OPENING_SLICE_BUILD_REPORT_PATH)} is missing required build-report language: {phrase!r}"
                )
    if PEREK_THREE_OPENING_SLICE_VERIFICATION_REPORT_PATH.exists():
        perek_three_opening_verification_text = PEREK_THREE_OPENING_SLICE_VERIFICATION_REPORT_PATH.read_text(
            encoding="utf-8"
        )
        for phrase in PEREK_THREE_OPENING_SLICE_VERIFICATION_REPORT_REQUIRED_PHRASES:
            if phrase not in perek_three_opening_verification_text:
                errors.append(
                    f"{repo_relative(PEREK_THREE_OPENING_SLICE_VERIFICATION_REPORT_PATH)} is missing required verification language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in perek_three_opening_verification_text and f"not {phrase}" not in perek_three_opening_verification_text:
                errors.append(
                    f"{repo_relative(PEREK_THREE_OPENING_SLICE_VERIFICATION_REPORT_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if PEREK_THREE_EXPANSION_SLICE_REVIEW_PACKET_PATH.exists():
        perek_three_expansion_text = PEREK_THREE_EXPANSION_SLICE_REVIEW_PACKET_PATH.read_text(encoding="utf-8")
        for phrase in PEREK_THREE_EXPANSION_SLICE_REVIEW_PACKET_REQUIRED_PHRASES:
            if phrase not in perek_three_expansion_text:
                errors.append(
                    f"{repo_relative(PEREK_THREE_EXPANSION_SLICE_REVIEW_PACKET_PATH)} is missing required perek-three expansion review language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in perek_three_expansion_text and f"not {phrase}" not in perek_three_expansion_text:
                errors.append(
                    f"{repo_relative(PEREK_THREE_EXPANSION_SLICE_REVIEW_PACKET_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if PEREK_THREE_EXPANSION_SLICE_BUILD_REPORT_PATH.exists():
        perek_three_expansion_build_text = PEREK_THREE_EXPANSION_SLICE_BUILD_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in PEREK_THREE_EXPANSION_SLICE_BUILD_REPORT_REQUIRED_PHRASES:
            if phrase not in perek_three_expansion_build_text:
                errors.append(
                    f"{repo_relative(PEREK_THREE_EXPANSION_SLICE_BUILD_REPORT_PATH)} is missing required build-report language: {phrase!r}"
                )
    if PEREK_THREE_EXPANSION_SLICE_VERIFICATION_REPORT_PATH.exists():
        perek_three_expansion_verification_text = PEREK_THREE_EXPANSION_SLICE_VERIFICATION_REPORT_PATH.read_text(
            encoding="utf-8"
        )
        for phrase in PEREK_THREE_EXPANSION_SLICE_VERIFICATION_REPORT_REQUIRED_PHRASES:
            if phrase not in perek_three_expansion_verification_text:
                errors.append(
                    f"{repo_relative(PEREK_THREE_EXPANSION_SLICE_VERIFICATION_REPORT_PATH)} is missing required verification language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in perek_three_expansion_verification_text and f"not {phrase}" not in perek_three_expansion_verification_text:
                errors.append(
                    f"{repo_relative(PEREK_THREE_EXPANSION_SLICE_VERIFICATION_REPORT_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if PEREK_THREE_FINAL_SLICE_REVIEW_PACKET_PATH.exists():
        perek_three_final_text = PEREK_THREE_FINAL_SLICE_REVIEW_PACKET_PATH.read_text(encoding="utf-8")
        for phrase in PEREK_THREE_FINAL_SLICE_REVIEW_PACKET_REQUIRED_PHRASES:
            if phrase not in perek_three_final_text:
                errors.append(
                    f"{repo_relative(PEREK_THREE_FINAL_SLICE_REVIEW_PACKET_PATH)} is missing required perek-three final review language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in perek_three_final_text and f"not {phrase}" not in perek_three_final_text:
                errors.append(
                    f"{repo_relative(PEREK_THREE_FINAL_SLICE_REVIEW_PACKET_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if PEREK_THREE_FINAL_SLICE_BUILD_REPORT_PATH.exists():
        perek_three_final_build_text = PEREK_THREE_FINAL_SLICE_BUILD_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in PEREK_THREE_FINAL_SLICE_BUILD_REPORT_REQUIRED_PHRASES:
            if phrase not in perek_three_final_build_text:
                errors.append(
                    f"{repo_relative(PEREK_THREE_FINAL_SLICE_BUILD_REPORT_PATH)} is missing required build-report language: {phrase!r}"
                )
    if PEREK_THREE_FINAL_SLICE_VERIFICATION_REPORT_PATH.exists():
        perek_three_final_verification_text = PEREK_THREE_FINAL_SLICE_VERIFICATION_REPORT_PATH.read_text(
            encoding="utf-8"
        )
        for phrase in PEREK_THREE_FINAL_SLICE_VERIFICATION_REPORT_REQUIRED_PHRASES:
            if phrase not in perek_three_final_verification_text:
                errors.append(
                    f"{repo_relative(PEREK_THREE_FINAL_SLICE_VERIFICATION_REPORT_PATH)} is missing required verification language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in perek_three_final_verification_text and f"not {phrase}" not in perek_three_final_verification_text:
                errors.append(
                    f"{repo_relative(PEREK_THREE_FINAL_SLICE_VERIFICATION_REPORT_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if PEREK_THREE_COMPLETION_REPORT_PATH.exists():
        perek_three_completion_text = PEREK_THREE_COMPLETION_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in PEREK_THREE_COMPLETION_REPORT_REQUIRED_PHRASES:
            if phrase not in perek_three_completion_text:
                errors.append(
                    f"{repo_relative(PEREK_THREE_COMPLETION_REPORT_PATH)} is missing required completion language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in perek_three_completion_text and f"not {phrase}" not in perek_three_completion_text:
                errors.append(
                    f"{repo_relative(PEREK_THREE_COMPLETION_REPORT_PATH)} contains forbidden readiness language: {phrase!r}"
                )


def validate_yossi_review_sheets(errors: list[str]) -> None:
    review_sheet_pairs = (
        (PEREK_TWO_OPENING_SLICE_REVIEW_SHEET_MD_PATH, PEREK_TWO_OPENING_SLICE_REVIEW_SHEET_CSV_PATH),
        (PEREK_TWO_EXPANSION_SLICE_REVIEW_SHEET_MD_PATH, PEREK_TWO_EXPANSION_SLICE_REVIEW_SHEET_CSV_PATH),
        (PEREK_TWO_FINAL_SLICE_REVIEW_SHEET_MD_PATH, PEREK_TWO_FINAL_SLICE_REVIEW_SHEET_CSV_PATH),
        (PEREK_THREE_OPENING_SLICE_REVIEW_SHEET_MD_PATH, PEREK_THREE_OPENING_SLICE_REVIEW_SHEET_CSV_PATH),
        (PEREK_THREE_EXPANSION_SLICE_REVIEW_SHEET_MD_PATH, PEREK_THREE_EXPANSION_SLICE_REVIEW_SHEET_CSV_PATH),
        (PEREK_THREE_FINAL_SLICE_REVIEW_SHEET_MD_PATH, PEREK_THREE_FINAL_SLICE_REVIEW_SHEET_CSV_PATH),
    )
    for md_path, csv_path in review_sheet_pairs:
        if not md_path.exists():
            continue
        text = md_path.read_text(encoding="utf-8")
        for phrase in YOSSI_REVIEW_SHEET_MD_REQUIRED_PHRASES:
            if phrase not in text:
                errors.append(
                    f"{repo_relative(md_path)} is missing required Yossi review-sheet language: {phrase!r}"
                )
        for decision in YOSSI_REVIEW_DECISIONS:
            if f"`{decision}`" not in text:
                errors.append(
                    f"{repo_relative(md_path)} must document allowed decision `{decision}`"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in text and f"not {phrase}" not in text:
                errors.append(
                    f"{repo_relative(md_path)} contains forbidden readiness language: {phrase!r}"
                )

        if not csv_path.exists():
            continue
        if csv_path == PEREK_TWO_FINAL_SLICE_REVIEW_SHEET_CSV_PATH and not csv_path.read_bytes().startswith(
            b"\xef\xbb\xbf"
        ):
            errors.append(f"{repo_relative(csv_path)} must be encoded as UTF-8 with BOM for Excel Hebrew display")
        if csv_path == PEREK_THREE_OPENING_SLICE_REVIEW_SHEET_CSV_PATH and not csv_path.read_bytes().startswith(
            b"\xef\xbb\xbf"
        ):
            errors.append(f"{repo_relative(csv_path)} must be encoded as UTF-8 with BOM for Excel Hebrew display")
        if csv_path == PEREK_THREE_EXPANSION_SLICE_REVIEW_SHEET_CSV_PATH and not csv_path.read_bytes().startswith(
            b"\xef\xbb\xbf"
        ):
            errors.append(f"{repo_relative(csv_path)} must be encoded as UTF-8 with BOM for Excel Hebrew display")
        if csv_path == PEREK_THREE_FINAL_SLICE_REVIEW_SHEET_CSV_PATH and not csv_path.read_bytes().startswith(
            b"\xef\xbb\xbf"
        ):
            errors.append(f"{repo_relative(csv_path)} must be encoded as UTF-8 with BOM for Excel Hebrew display")
        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
            rows = list(reader)

        missing_columns = [column for column in YOSSI_REVIEW_SHEET_COLUMNS if column not in columns]
        if missing_columns:
            errors.append(f"{repo_relative(csv_path)} missing required columns: {missing_columns}")
        if not rows:
            errors.append(f"{repo_relative(csv_path)} must include at least one review row")

        for row_number, row in enumerate(rows, 2):
            context = f"{repo_relative(csv_path)} row {row_number}"
            if not normalized(row.get("row_id")):
                errors.append(f"{context}: row_id must be populated")
            if not normalized(row.get("ref")):
                errors.append(f"{context}: ref must be populated")
            if not normalized(row.get("hebrew_phrase")):
                errors.append(f"{context}: hebrew_phrase must be populated")
            if not normalized(row.get("linear_translation")):
                errors.append(f"{context}: linear_translation must be populated")
            if row.get("current_status") != "pending_yossi_extraction_accuracy_pass":
                errors.append(f"{context}: current_status must be pending_yossi_extraction_accuracy_pass")
            if not normalized(row.get("issue_type")):
                errors.append(f"{context}: issue_type must be populated")
            if not normalized(row.get("what_to_check")):
                errors.append(f"{context}: what_to_check must be populated")
            decision = normalized(row.get("yossi_decision"))
            if decision and decision not in YOSSI_REVIEW_DECISIONS:
                errors.append(f"{context}: yossi_decision must be blank or one of {sorted(YOSSI_REVIEW_DECISIONS)}")
            recommended = normalized(row.get("recommended_default_decision"))
            if recommended not in YOSSI_REVIEW_DECISIONS:
                errors.append(f"{context}: recommended_default_decision must be one of {sorted(YOSSI_REVIEW_DECISIONS)}")


def validate_row(row: dict[str, str], row_number: int, errors: list[str]) -> None:
    context = f"{repo_relative(SEED_MAP_PATH)} row {row_number}"
    ref = normalized(row.get("ref")) or f"row {row_number}"
    hebrew = normalized(row.get("hebrew_word_or_phrase"))
    clean_hebrew = normalized(row.get("clean_hebrew_no_nikud"))

    if not ref:
        errors.append(f"{context}: ref must be populated")
    if not hebrew:
        errors.append(f"{context}: hebrew_word_or_phrase must be populated")
    if not clean_hebrew:
        errors.append(f"{context}: clean_hebrew_no_nikud must be populated")

    if normalized(row.get("source_translation_metsudah")):
        if row.get("source_license") != "CC-BY":
            errors.append(f"Map row {ref} / {clean_hebrew} has Metsudah translation but source_license is not CC-BY")
        if row.get("source_version_title") != "Metsudah Chumash, Metsudah Publications, 2009":
            errors.append(f"Map row {ref} / {clean_hebrew} has unexpected Metsudah source_version_title")
        if row.get("source_preference") != "primary_preferred_translation_source":
            errors.append(f"Map row {ref} / {clean_hebrew} must mark Metsudah as primary_preferred_translation_source")
        if row.get("requires_attribution") != "true":
            errors.append(f"Map row {ref} / {clean_hebrew} has source translation but requires_attribution is not true")

    if normalized(row.get("secondary_translation_koren")):
        if row.get("secondary_source_license") != "CC-BY-NC":
            errors.append(f"Map row {ref} / {clean_hebrew} has Koren secondary translation but secondary_source_license is not CC-BY-NC")
        if row.get("secondary_source_preference") != "secondary_noncommercial_translation_support":
            errors.append(f"Map row {ref} / {clean_hebrew} must mark Koren as secondary_noncommercial_translation_support")
        if row.get("secondary_commercial_use_allowed") != "false":
            errors.append(f"Map row {ref} / {clean_hebrew} must not mark Koren commercial use as allowed")

    if row.get("source_preference") and row["source_preference"] not in ALLOWED_SOURCE_PREFERENCES:
        errors.append(f"{context}: source_preference must be one of {sorted(ALLOWED_SOURCE_PREFERENCES)}")

    extraction_status = row.get("extraction_review_status")
    if extraction_status not in ALLOWED_EXTRACTION_REVIEW_STATUSES:
        errors.append(f"{context}: extraction_review_status must be one of {sorted(ALLOWED_EXTRACTION_REVIEW_STATUSES)}")
    if extraction_status == "pending_yossi_extraction_accuracy_pass":
        if "Yossi" not in row.get("review_notes", ""):
            errors.append(f"{context}: pending rows should clearly name Yossi extraction-accuracy confirmation in review_notes")

    if row.get("question_allowed") not in OPEN_QUESTION_ALLOWED_VALUES:
        errors.append(f"{context}: question_allowed must remain no/needs_review/false until a future gate")
    for field in ("runtime_allowed", "protected_preview_allowed", "reviewed_bank_allowed"):
        if row.get(field) not in CLOSED_BOOLEAN_VALUES:
            errors.append(f"{context}: {field} must remain false/no/blank until a future gate")

    for field, value in row.items():
        lowered = normalized(value).lower()
        if field not in {"review_notes", "uncertainty_reason"} and lowered in FORBIDDEN_READY_VALUES:
            errors.append(f"{context}: field {field} contains forbidden readiness value {value!r}")

    if (not normalized(row.get("zekelman_standard")) or not normalized(row.get("difficulty_level"))) and not normalized(
        row.get("uncertainty_reason")
    ):
        errors.append(f"{context}: missing standards/difficulty fields require uncertainty_reason")


def validate_proof_row(row: dict[str, str], row_number: int, errors: list[str]) -> None:
    context = f"{repo_relative(PROOF_MAP_PATH)} row {row_number}"
    ref = normalized(row.get("ref")) or f"row {row_number}"
    hebrew = normalized(row.get("hebrew_word_or_phrase"))
    clean_hebrew = normalized(row.get("clean_hebrew_no_nikud"))

    if not ref:
        errors.append(f"{context}: ref must be populated")
    if not hebrew:
        errors.append(f"{context}: hebrew_word_or_phrase must be populated")
    if not clean_hebrew:
        errors.append(f"{context}: clean_hebrew_no_nikud must be populated")
    if not normalized(row.get("source_files_used")):
        errors.append(f"{context}: source_files_used must record the contributing source paths")

    if normalized(row.get("source_translation_metsudah")):
        if "CC-BY" not in row.get("source_license", ""):
            errors.append(f"Map row {ref} / {clean_hebrew} has Metsudah translation but source_license does not include CC-BY")
        if "Metsudah Chumash, Metsudah Publications, 2009" not in row.get("source_version_title", ""):
            errors.append(f"Map row {ref} / {clean_hebrew} has Metsudah translation but source_version_title is missing Metsudah")
        if row.get("source_preference") != "primary_preferred_translation_source":
            errors.append(f"Map row {ref} / {clean_hebrew} must mark Metsudah as primary_preferred_translation_source")
        if row.get("requires_attribution") != "true":
            errors.append(f"Map row {ref} / {clean_hebrew} has source translation but requires_attribution is not true")

    if normalized(row.get("secondary_translation_koren")) and "bereishis_english_koren.jsonl" not in row.get(
        "source_files_used",
        "",
    ):
        errors.append(f"Map row {ref} / {clean_hebrew} has Koren secondary translation but source_files_used omits Koren JSONL")

    if row.get("question_allowed") not in OPEN_QUESTION_ALLOWED_VALUES:
        errors.append(f"{context}: question_allowed must remain no/needs_review/false until a future gate")
    for field in ("runtime_allowed", "protected_preview_allowed", "reviewed_bank_allowed"):
        if row.get(field) not in CLOSED_BOOLEAN_VALUES:
            errors.append(f"{context}: {field} must remain false/no/blank until a future gate")
    if row.get("extraction_review_status") not in ALLOWED_EXTRACTION_REVIEW_STATUSES:
        errors.append(f"{context}: extraction_review_status must be one of {sorted(ALLOWED_EXTRACTION_REVIEW_STATUSES)}")
    if row.get("extraction_review_status") == "yossi_extraction_verified" and not PROOF_VERIFICATION_REPORT_PATH.exists():
        errors.append(f"{context}: yossi_extraction_verified rows require {repo_relative(PROOF_VERIFICATION_REPORT_PATH)}")
    if not normalized(row.get("uncertainty_reason")):
        errors.append(f"{context}: proof-map rows must explain uncertainty_reason")
    if not normalized(row.get("blocked_question_types")):
        errors.append(f"{context}: blocked_question_types must explain that question use is blocked")

    for field, value in row.items():
        lowered = normalized(value).lower()
        if field not in {"review_notes", "uncertainty_reason", "blocked_question_types"} and lowered in FORBIDDEN_READY_VALUES:
            errors.append(f"{context}: field {field} contains forbidden readiness value {value!r}")


def validate_pending_expansion_row(row: dict[str, str], row_number: int, errors: list[str]) -> None:
    context = f"{repo_relative(NEXT_SLICE_MAP_PATH)} row {row_number}"
    ref = normalized(row.get("ref")) or f"row {row_number}"
    hebrew = normalized(row.get("hebrew_word_or_phrase"))
    clean_hebrew = normalized(row.get("clean_hebrew_no_nikud"))

    if not ref:
        errors.append(f"{context}: ref must be populated")
    if not hebrew:
        errors.append(f"{context}: hebrew_word_or_phrase must be populated")
    if not clean_hebrew:
        errors.append(f"{context}: clean_hebrew_no_nikud must be populated")
    if not normalized(row.get("source_files_used")):
        errors.append(f"{context}: source_files_used must record the contributing source paths")

    if normalized(row.get("source_translation_metsudah")):
        if "CC-BY" not in row.get("source_license", ""):
            errors.append(f"{context}: has Metsudah translation but source_license does not include CC-BY")
        if "Metsudah Chumash, Metsudah Publications, 2009" not in row.get("source_version_title", ""):
            errors.append(f"{context}: has Metsudah translation but source_version_title is missing Metsudah")
        if row.get("source_preference") != "primary_preferred_translation_source":
            errors.append(f"{context}: must mark Metsudah as primary_preferred_translation_source")
        if row.get("requires_attribution") != "true":
            errors.append(f"{context}: has source translation but requires_attribution is not true")

    if normalized(row.get("secondary_translation_koren")) and "bereishis_english_koren.jsonl" not in row.get(
        "source_files_used",
        "",
    ):
        errors.append(f"{context}: has Koren secondary translation but source_files_used omits Koren JSONL")

    extraction_status = row.get("extraction_review_status")
    if extraction_status not in {"pending_yossi_extraction_accuracy_pass", "yossi_extraction_verified"}:
        errors.append(f"{context}: extraction_review_status must remain pending or yossi_extraction_verified")
    if extraction_status == "pending_yossi_extraction_accuracy_pass" and "Yossi" not in row.get("review_notes", ""):
        errors.append(f"{context}: pending rows should clearly name Yossi extraction-accuracy confirmation in review_notes")
    if extraction_status == "yossi_extraction_verified":
        if not NEXT_SLICE_VERIFICATION_REPORT_PATH.exists():
            errors.append(
                f"{context}: yossi_extraction_verified rows require {repo_relative(NEXT_SLICE_VERIFICATION_REPORT_PATH)}"
            )
        if "Yossi confirmed extraction accuracy" not in row.get("review_notes", ""):
            errors.append(f"{context}: verified rows must record Yossi extraction-accuracy confirmation in review_notes")
    if row.get("question_allowed") != "needs_review":
        errors.append(f"{context}: question_allowed must remain needs_review until a future gate")
    for field in ("runtime_allowed", "protected_preview_allowed", "reviewed_bank_allowed"):
        if row.get(field) != "false":
            errors.append(f"{context}: {field} must remain false until a future gate")
    if not normalized(row.get("uncertainty_reason")):
        errors.append(f"{context}: pending expansion rows must explain uncertainty_reason")
    if not normalized(row.get("blocked_question_types")):
        errors.append(f"{context}: blocked_question_types must explain that question use is blocked")

    for field, value in row.items():
        lowered = normalized(value).lower()
        if field not in {"review_notes", "uncertainty_reason", "blocked_question_types"} and lowered in FORBIDDEN_READY_VALUES:
            errors.append(f"{context}: field {field} contains forbidden readiness value {value!r}")


def validate_current_pending_slice_row(row: dict[str, str], row_number: int, errors: list[str]) -> None:
    context = f"{repo_relative(PENDING_SLICE_MAP_PATH)} row {row_number}"
    ref = normalized(row.get("ref")) or f"row {row_number}"
    hebrew = normalized(row.get("hebrew_word_or_phrase"))
    clean_hebrew = normalized(row.get("clean_hebrew_no_nikud"))

    if not ref:
        errors.append(f"{context}: ref must be populated")
    if not hebrew:
        errors.append(f"{context}: hebrew_word_or_phrase must be populated")
    if not clean_hebrew:
        errors.append(f"{context}: clean_hebrew_no_nikud must be populated")
    if not normalized(row.get("source_files_used")):
        errors.append(f"{context}: source_files_used must record the contributing source paths")

    if normalized(row.get("source_translation_metsudah")):
        if "CC-BY" not in row.get("source_license", ""):
            errors.append(f"{context}: has Metsudah translation but source_license does not include CC-BY")
        if "Metsudah Chumash, Metsudah Publications, 2009" not in row.get("source_version_title", ""):
            errors.append(f"{context}: has Metsudah translation but source_version_title is missing Metsudah")
        if row.get("source_preference") != "primary_preferred_translation_source":
            errors.append(f"{context}: must mark Metsudah as primary_preferred_translation_source")
        if row.get("requires_attribution") != "true":
            errors.append(f"{context}: has source translation but requires_attribution is not true")

    if normalized(row.get("secondary_translation_koren")) and "bereishis_english_koren.jsonl" not in row.get(
        "source_files_used",
        "",
    ):
        errors.append(f"{context}: has Koren secondary translation but source_files_used omits Koren JSONL")

    extraction_status = row.get("extraction_review_status")
    if extraction_status not in {"pending_yossi_extraction_accuracy_pass", "yossi_extraction_verified"}:
        errors.append(f"{context}: extraction_review_status must remain pending or yossi_extraction_verified")
    if extraction_status == "pending_yossi_extraction_accuracy_pass" and "Yossi" not in row.get("review_notes", ""):
        errors.append(f"{context}: pending rows should clearly name Yossi extraction-accuracy confirmation in review_notes")
    if extraction_status == "yossi_extraction_verified":
        if not PENDING_SLICE_VERIFICATION_REPORT_PATH.exists():
            errors.append(
                f"{context}: yossi_extraction_verified rows require {repo_relative(PENDING_SLICE_VERIFICATION_REPORT_PATH)}"
            )
        if "Yossi confirmed extraction accuracy" not in row.get("review_notes", ""):
            errors.append(f"{context}: verified rows must record Yossi extraction-accuracy confirmation in review_notes")
    if row.get("question_allowed") != "needs_review":
        errors.append(f"{context}: question_allowed must remain needs_review until a future gate")
    for field in ("runtime_allowed", "protected_preview_allowed", "reviewed_bank_allowed"):
        if row.get(field) != "false":
            errors.append(f"{context}: {field} must remain false until a future gate")
    if not normalized(row.get("uncertainty_reason")):
        errors.append(f"{context}: pending rows must explain uncertainty_reason")
    if not normalized(row.get("blocked_question_types")):
        errors.append(f"{context}: blocked_question_types must explain that question use is blocked")

    for field, value in row.items():
        lowered = normalized(value).lower()
        if field not in {"review_notes", "uncertainty_reason", "blocked_question_types"} and lowered in FORBIDDEN_READY_VALUES:
            errors.append(f"{context}: field {field} contains forbidden readiness value {value!r}")


def validate_perek_one_final_pending_slice_row(row: dict[str, str], row_number: int, errors: list[str]) -> None:
    context = f"{repo_relative(PEREK_ONE_FINAL_SLICE_MAP_PATH)} row {row_number}"
    ref = normalized(row.get("ref")) or f"row {row_number}"
    hebrew = normalized(row.get("hebrew_word_or_phrase"))
    clean_hebrew = normalized(row.get("clean_hebrew_no_nikud"))

    if not ref:
        errors.append(f"{context}: ref must be populated")
    if not hebrew:
        errors.append(f"{context}: hebrew_word_or_phrase must be populated")
    if not clean_hebrew:
        errors.append(f"{context}: clean_hebrew_no_nikud must be populated")
    if not normalized(row.get("source_files_used")):
        errors.append(f"{context}: source_files_used must record the contributing source paths")

    if normalized(row.get("source_translation_metsudah")):
        if "CC-BY" not in row.get("source_license", ""):
            errors.append(f"{context}: has Metsudah translation but source_license does not include CC-BY")
        if "Metsudah Chumash, Metsudah Publications, 2009" not in row.get("source_version_title", ""):
            errors.append(f"{context}: has Metsudah translation but source_version_title is missing Metsudah")
        if row.get("source_preference") != "primary_preferred_translation_source":
            errors.append(f"{context}: must mark Metsudah as primary_preferred_translation_source")
        if row.get("requires_attribution") != "true":
            errors.append(f"{context}: has source translation but requires_attribution is not true")

    if normalized(row.get("secondary_translation_koren")) and "bereishis_english_koren.jsonl" not in row.get(
        "source_files_used",
        "",
    ):
        errors.append(f"{context}: has Koren secondary translation but source_files_used omits Koren JSONL")

    extraction_status = row.get("extraction_review_status")
    if extraction_status not in {"pending_yossi_extraction_accuracy_pass", "yossi_extraction_verified"}:
        errors.append(f"{context}: extraction_review_status must remain pending or yossi_extraction_verified")
    if extraction_status == "pending_yossi_extraction_accuracy_pass" and "Yossi" not in row.get("review_notes", ""):
        errors.append(f"{context}: pending rows should clearly name Yossi extraction-accuracy confirmation in review_notes")
    if extraction_status == "yossi_extraction_verified":
        if not PEREK_ONE_FINAL_SLICE_VERIFICATION_REPORT_PATH.exists():
            errors.append(
                f"{context}: yossi_extraction_verified rows require {repo_relative(PEREK_ONE_FINAL_SLICE_VERIFICATION_REPORT_PATH)}"
            )
        if "Yossi confirmed extraction accuracy" not in row.get("review_notes", ""):
            errors.append(f"{context}: verified rows must record Yossi extraction-accuracy confirmation in review_notes")
    if row.get("question_allowed") != "needs_review":
        errors.append(f"{context}: question_allowed must remain needs_review until a future gate")
    for field in ("runtime_allowed", "protected_preview_allowed", "reviewed_bank_allowed"):
        if row.get(field) != "false":
            errors.append(f"{context}: {field} must remain false until a future gate")
    if not normalized(row.get("uncertainty_reason")):
        errors.append(f"{context}: pending rows must explain uncertainty_reason")
    if not normalized(row.get("blocked_question_types")):
        errors.append(f"{context}: blocked_question_types must explain that question use is blocked")

    for field, value in row.items():
        lowered = normalized(value).lower()
        if field not in {"review_notes", "uncertainty_reason", "blocked_question_types"} and lowered in FORBIDDEN_READY_VALUES:
            errors.append(f"{context}: field {field} contains forbidden readiness value {value!r}")


def validate_perek_two_opening_pending_slice_row(row: dict[str, str], row_number: int, errors: list[str]) -> None:
    context = f"{repo_relative(PEREK_TWO_OPENING_SLICE_MAP_PATH)} row {row_number}"
    ref = normalized(row.get("ref")) or f"row {row_number}"
    hebrew = normalized(row.get("hebrew_word_or_phrase"))
    clean_hebrew = normalized(row.get("clean_hebrew_no_nikud"))

    if not ref:
        errors.append(f"{context}: ref must be populated")
    if not hebrew:
        errors.append(f"{context}: hebrew_word_or_phrase must be populated")
    if not clean_hebrew:
        errors.append(f"{context}: clean_hebrew_no_nikud must be populated")
    if not normalized(row.get("source_files_used")):
        errors.append(f"{context}: source_files_used must record the contributing source paths")

    if normalized(row.get("source_translation_metsudah")):
        if "CC-BY" not in row.get("source_license", ""):
            errors.append(f"{context}: has Metsudah translation but source_license does not include CC-BY")
        if "Metsudah Chumash, Metsudah Publications, 2009" not in row.get("source_version_title", ""):
            errors.append(f"{context}: has Metsudah translation but source_version_title is missing Metsudah")
        if row.get("source_preference") != "primary_preferred_translation_source":
            errors.append(f"{context}: must mark Metsudah as primary_preferred_translation_source")
        if row.get("requires_attribution") != "true":
            errors.append(f"{context}: has source translation but requires_attribution is not true")

    if normalized(row.get("secondary_translation_koren")) and "bereishis_english_koren.jsonl" not in row.get(
        "source_files_used",
        "",
    ):
        errors.append(f"{context}: has Koren secondary translation but source_files_used omits Koren JSONL")

    extraction_status = row.get("extraction_review_status")
    if extraction_status not in {"pending_yossi_extraction_accuracy_pass", "yossi_extraction_verified"}:
        errors.append(f"{context}: extraction_review_status must remain pending or yossi_extraction_verified")
    if extraction_status == "pending_yossi_extraction_accuracy_pass" and "Yossi" not in row.get("review_notes", ""):
        errors.append(f"{context}: pending rows should clearly name Yossi extraction-accuracy confirmation in review_notes")
    if extraction_status == "yossi_extraction_verified":
        if not PEREK_TWO_OPENING_SLICE_VERIFICATION_REPORT_PATH.exists():
            errors.append(
                f"{context}: yossi_extraction_verified rows require {repo_relative(PEREK_TWO_OPENING_SLICE_VERIFICATION_REPORT_PATH)}"
            )
        if "Yossi confirmed extraction accuracy" not in row.get("review_notes", ""):
            errors.append(f"{context}: verified rows must record Yossi extraction-accuracy confirmation in review_notes")
    if row.get("question_allowed") != "needs_review":
        errors.append(f"{context}: question_allowed must remain needs_review until a future gate")
    for field in ("runtime_allowed", "protected_preview_allowed", "reviewed_bank_allowed"):
        if row.get(field) != "false":
            errors.append(f"{context}: {field} must remain false until a future gate")
    if not normalized(row.get("uncertainty_reason")):
        errors.append(f"{context}: pending rows must explain uncertainty_reason")
    if not normalized(row.get("blocked_question_types")):
        errors.append(f"{context}: blocked_question_types must explain that question use is blocked")

    for field, value in row.items():
        lowered = normalized(value).lower()
        if field not in {"review_notes", "uncertainty_reason", "blocked_question_types"} and lowered in FORBIDDEN_READY_VALUES:
            errors.append(f"{context}: field {field} contains forbidden readiness value {value!r}")


def validate_perek_two_expansion_verified_slice_row(row: dict[str, str], row_number: int, errors: list[str]) -> None:
    context = f"{repo_relative(PEREK_TWO_EXPANSION_SLICE_MAP_PATH)} row {row_number}"
    ref = normalized(row.get("ref")) or f"row {row_number}"
    hebrew = normalized(row.get("hebrew_word_or_phrase"))
    clean_hebrew = normalized(row.get("clean_hebrew_no_nikud"))

    if not ref:
        errors.append(f"{context}: ref must be populated")
    if not hebrew:
        errors.append(f"{context}: hebrew_word_or_phrase must be populated")
    if not clean_hebrew:
        errors.append(f"{context}: clean_hebrew_no_nikud must be populated")
    if not normalized(row.get("source_files_used")):
        errors.append(f"{context}: source_files_used must record the contributing source paths")

    if normalized(row.get("source_translation_metsudah")):
        if "CC-BY" not in row.get("source_license", ""):
            errors.append(f"{context}: has Metsudah translation but source_license does not include CC-BY")
        if "Metsudah Chumash, Metsudah Publications, 2009" not in row.get("source_version_title", ""):
            errors.append(f"{context}: has Metsudah translation but source_version_title is missing Metsudah")
        if row.get("source_preference") != "primary_preferred_translation_source":
            errors.append(f"{context}: must mark Metsudah as primary_preferred_translation_source")
        if row.get("requires_attribution") != "true":
            errors.append(f"{context}: has source translation but requires_attribution is not true")

    if normalized(row.get("secondary_translation_koren")) and "bereishis_english_koren.jsonl" not in row.get(
        "source_files_used",
        "",
    ):
        errors.append(f"{context}: has Koren secondary translation but source_files_used omits Koren JSONL")

    if row.get("extraction_review_status") != "yossi_extraction_verified":
        errors.append(f"{context}: extraction_review_status must be yossi_extraction_verified")
    if not PEREK_TWO_EXPANSION_SLICE_VERIFICATION_REPORT_PATH.exists():
        errors.append(
            f"{context}: yossi_extraction_verified rows require {repo_relative(PEREK_TWO_EXPANSION_SLICE_VERIFICATION_REPORT_PATH)}"
        )
    review_notes = row.get("review_notes", "")
    if "Yossi confirmed extraction accuracy" not in review_notes:
        errors.append(f"{context}: verified rows must record Yossi extraction-accuracy confirmation in review_notes")
    if "source-only for future question/protected-preview planning" not in review_notes:
        errors.append(f"{context}: verified rows must preserve Yossi source-only planning note in review_notes")
    if row.get("question_allowed") != "needs_review":
        errors.append(f"{context}: question_allowed must remain needs_review until a future gate")
    for field in ("runtime_allowed", "protected_preview_allowed", "reviewed_bank_allowed"):
        if row.get(field) != "false":
            errors.append(f"{context}: {field} must remain false until a future gate")
    if not normalized(row.get("uncertainty_reason")):
        errors.append(f"{context}: verified rows must preserve uncertainty_reason for future planning")
    if not normalized(row.get("blocked_question_types")):
        errors.append(f"{context}: blocked_question_types must explain that question use is blocked")

    for field, value in row.items():
        lowered = normalized(value).lower()
        if field not in {"review_notes", "uncertainty_reason", "blocked_question_types"} and lowered in FORBIDDEN_READY_VALUES:
            errors.append(f"{context}: field {field} contains forbidden readiness value {value!r}")


def validate_perek_two_final_verified_slice_row(row: dict[str, str], row_number: int, errors: list[str]) -> None:
    context = f"{repo_relative(PEREK_TWO_FINAL_SLICE_MAP_PATH)} row {row_number}"
    ref = normalized(row.get("ref")) or f"row {row_number}"
    hebrew = normalized(row.get("hebrew_word_or_phrase"))
    clean_hebrew = normalized(row.get("clean_hebrew_no_nikud"))

    if not ref:
        errors.append(f"{context}: ref must be populated")
    if not hebrew:
        errors.append(f"{context}: hebrew_word_or_phrase must be populated")
    if not clean_hebrew:
        errors.append(f"{context}: clean_hebrew_no_nikud must be populated")
    if not normalized(row.get("source_files_used")):
        errors.append(f"{context}: source_files_used must record the contributing source paths")

    if normalized(row.get("source_translation_metsudah")):
        if "CC-BY" not in row.get("source_license", ""):
            errors.append(f"{context}: has Metsudah translation but source_license does not include CC-BY")
        if "Metsudah Chumash, Metsudah Publications, 2009" not in row.get("source_version_title", ""):
            errors.append(f"{context}: has Metsudah translation but source_version_title is missing Metsudah")
        if row.get("source_preference") != "primary_preferred_translation_source":
            errors.append(f"{context}: must mark Metsudah as primary_preferred_translation_source")
        if row.get("requires_attribution") != "true":
            errors.append(f"{context}: has source translation but requires_attribution is not true")

    if normalized(row.get("secondary_translation_koren")) and "bereishis_english_koren.jsonl" not in row.get(
        "source_files_used",
        "",
    ):
        errors.append(f"{context}: has Koren secondary translation but source_files_used omits Koren JSONL")

    if row.get("extraction_review_status") != "yossi_extraction_verified":
        errors.append(f"{context}: extraction_review_status must be yossi_extraction_verified")
    if not PEREK_TWO_FINAL_SLICE_VERIFICATION_REPORT_PATH.exists():
        errors.append(
            f"{context}: yossi_extraction_verified rows require {repo_relative(PEREK_TWO_FINAL_SLICE_VERIFICATION_REPORT_PATH)}"
        )
    review_notes = row.get("review_notes", "")
    if "Yossi confirmed extraction accuracy" not in review_notes:
        errors.append(f"{context}: verified rows must record Yossi extraction-accuracy confirmation in review_notes")
    if "source-only for future question/protected-preview planning" not in review_notes:
        errors.append(f"{context}: verified rows must preserve Yossi source-only planning note in review_notes")
    if row.get("question_allowed") != "needs_review":
        errors.append(f"{context}: question_allowed must remain needs_review until a future gate")
    for field in ("runtime_allowed", "protected_preview_allowed", "reviewed_bank_allowed"):
        if row.get(field) != "false":
            errors.append(f"{context}: {field} must remain false until a future gate")
    if not normalized(row.get("uncertainty_reason")):
        errors.append(f"{context}: verified rows must preserve uncertainty_reason for future planning")
    if not normalized(row.get("blocked_question_types")):
        errors.append(f"{context}: blocked_question_types must explain that question use is blocked")

    for field, value in row.items():
        lowered = normalized(value).lower()
        if field not in {"review_notes", "uncertainty_reason", "blocked_question_types"} and lowered in FORBIDDEN_READY_VALUES:
            errors.append(f"{context}: field {field} contains forbidden readiness value {value!r}")


def validate_perek_three_opening_verified_slice_row(row: dict[str, str], row_number: int, errors: list[str]) -> None:
    context = f"{repo_relative(PEREK_THREE_OPENING_SLICE_MAP_PATH)} row {row_number}"
    ref = normalized(row.get("ref")) or f"row {row_number}"
    hebrew = normalized(row.get("hebrew_word_or_phrase"))
    clean_hebrew = normalized(row.get("clean_hebrew_no_nikud"))

    if not ref:
        errors.append(f"{context}: ref must be populated")
    if not hebrew:
        errors.append(f"{context}: hebrew_word_or_phrase must be populated")
    if not clean_hebrew:
        errors.append(f"{context}: clean_hebrew_no_nikud must be populated")
    if not normalized(row.get("source_files_used")):
        errors.append(f"{context}: source_files_used must record the contributing source paths")

    if normalized(row.get("source_translation_metsudah")):
        if "CC-BY" not in row.get("source_license", ""):
            errors.append(f"{context}: has Metsudah translation but source_license does not include CC-BY")
        if "Metsudah Chumash, Metsudah Publications, 2009" not in row.get("source_version_title", ""):
            errors.append(f"{context}: has Metsudah translation but source_version_title is missing Metsudah")
        if row.get("source_preference") != "primary_preferred_translation_source":
            errors.append(f"{context}: must mark Metsudah as primary_preferred_translation_source")
        if row.get("requires_attribution") != "true":
            errors.append(f"{context}: has source translation but requires_attribution is not true")

    if normalized(row.get("secondary_translation_koren")) and "bereishis_english_koren.jsonl" not in row.get(
        "source_files_used",
        "",
    ):
        errors.append(f"{context}: has Koren secondary translation but source_files_used omits Koren JSONL")

    if row.get("extraction_review_status") != "yossi_extraction_verified":
        errors.append(f"{context}: extraction_review_status must be yossi_extraction_verified")
    if not PEREK_THREE_OPENING_SLICE_VERIFICATION_REPORT_PATH.exists():
        errors.append(
            f"{context}: yossi_extraction_verified rows require {repo_relative(PEREK_THREE_OPENING_SLICE_VERIFICATION_REPORT_PATH)}"
        )
    review_notes = row.get("review_notes", "")
    if "Yossi confirmed extraction accuracy" not in review_notes:
        errors.append(f"{context}: verified rows must record Yossi extraction-accuracy confirmation in review_notes")
    if "source-only for future question/protected-preview planning" not in review_notes:
        errors.append(f"{context}: verified rows must preserve Yossi source-only planning note in review_notes")
    if "Dialogue and persuasion language" not in review_notes:
        errors.append(f"{context}: verified rows must preserve Yossi dialogue/persuasion question-use note in review_notes")
    if row.get("question_allowed") != "needs_review":
        errors.append(f"{context}: question_allowed must remain needs_review until a future gate")
    for field in ("runtime_allowed", "protected_preview_allowed", "reviewed_bank_allowed"):
        if row.get(field) != "false":
            errors.append(f"{context}: {field} must remain false until a future gate")
    if not normalized(row.get("uncertainty_reason")):
        errors.append(f"{context}: verified rows must preserve uncertainty_reason for future planning")
    if not normalized(row.get("blocked_question_types")):
        errors.append(f"{context}: blocked_question_types must explain that question use is blocked")

    for field, value in row.items():
        lowered = normalized(value).lower()
        if field not in {"review_notes", "uncertainty_reason", "blocked_question_types"} and lowered in FORBIDDEN_READY_VALUES:
            errors.append(f"{context}: field {field} contains forbidden readiness value {value!r}")


def validate_perek_three_expansion_verified_slice_row(row: dict[str, str], row_number: int, errors: list[str]) -> None:
    context = f"{repo_relative(PEREK_THREE_EXPANSION_SLICE_MAP_PATH)} row {row_number}"
    ref = normalized(row.get("ref")) or f"row {row_number}"
    hebrew = normalized(row.get("hebrew_word_or_phrase"))
    clean_hebrew = normalized(row.get("clean_hebrew_no_nikud"))

    if not ref:
        errors.append(f"{context}: ref must be populated")
    if not hebrew:
        errors.append(f"{context}: hebrew_word_or_phrase must be populated")
    if not clean_hebrew:
        errors.append(f"{context}: clean_hebrew_no_nikud must be populated")
    if not normalized(row.get("source_files_used")):
        errors.append(f"{context}: source_files_used must record the contributing source paths")

    if normalized(row.get("source_translation_metsudah")):
        if "CC-BY" not in row.get("source_license", ""):
            errors.append(f"{context}: has Metsudah translation but source_license does not include CC-BY")
        if "Metsudah Chumash, Metsudah Publications, 2009" not in row.get("source_version_title", ""):
            errors.append(f"{context}: has Metsudah translation but source_version_title is missing Metsudah")
        if row.get("source_preference") != "primary_preferred_translation_source":
            errors.append(f"{context}: must mark Metsudah as primary_preferred_translation_source")
        if row.get("requires_attribution") != "true":
            errors.append(f"{context}: has source translation but requires_attribution is not true")

    if normalized(row.get("secondary_translation_koren")) and "bereishis_english_koren.jsonl" not in row.get(
        "source_files_used",
        "",
    ):
        errors.append(f"{context}: has Koren secondary translation but source_files_used omits Koren JSONL")

    if row.get("extraction_review_status") != "yossi_extraction_verified":
        errors.append(f"{context}: extraction_review_status must be yossi_extraction_verified")
    if not PEREK_THREE_EXPANSION_SLICE_VERIFICATION_REPORT_PATH.exists():
        errors.append(
            f"{context}: yossi_extraction_verified rows require {repo_relative(PEREK_THREE_EXPANSION_SLICE_VERIFICATION_REPORT_PATH)}"
        )
    review_notes = row.get("review_notes", "")
    if "Yossi confirmed extraction accuracy" not in review_notes:
        errors.append(f"{context}: verified rows must record Yossi extraction-accuracy confirmation in review_notes")
    if "source-only for future question/protected-preview planning" not in review_notes:
        errors.append(f"{context}: verified rows must preserve Yossi source-only planning note in review_notes")
    if "Dialogue, accountability, curse/consequence language" not in review_notes:
        errors.append(f"{context}: verified rows must preserve Yossi dialogue/accountability/consequence question-use note in review_notes")
    if row.get("question_allowed") != "needs_review":
        errors.append(f"{context}: question_allowed must remain needs_review until a future gate")
    for field in ("runtime_allowed", "protected_preview_allowed", "reviewed_bank_allowed"):
        if row.get(field) != "false":
            errors.append(f"{context}: {field} must remain false until a future gate")
    if not normalized(row.get("uncertainty_reason")):
        errors.append(f"{context}: verified rows must preserve uncertainty_reason for future planning")
    if not normalized(row.get("blocked_question_types")):
        errors.append(f"{context}: blocked_question_types must explain that question use is blocked")

    for field, value in row.items():
        lowered = normalized(value).lower()
        if field not in {"review_notes", "uncertainty_reason", "blocked_question_types"} and lowered in FORBIDDEN_READY_VALUES:
            errors.append(f"{context}: field {field} contains forbidden readiness value {value!r}")


def validate_perek_three_final_verified_slice_row(row: dict[str, str], row_number: int, errors: list[str]) -> None:
    context = f"{repo_relative(PEREK_THREE_FINAL_SLICE_MAP_PATH)} row {row_number}"
    ref = normalized(row.get("ref")) or f"row {row_number}"
    hebrew = normalized(row.get("hebrew_word_or_phrase"))
    clean_hebrew = normalized(row.get("clean_hebrew_no_nikud"))

    if not ref:
        errors.append(f"{context}: ref must be populated")
    if not hebrew:
        errors.append(f"{context}: hebrew_word_or_phrase must be populated")
    if not clean_hebrew:
        errors.append(f"{context}: clean_hebrew_no_nikud must be populated")
    if not normalized(row.get("source_files_used")):
        errors.append(f"{context}: source_files_used must record the contributing source paths")

    if normalized(row.get("source_translation_metsudah")):
        if "CC-BY" not in row.get("source_license", ""):
            errors.append(f"{context}: has Metsudah translation but source_license does not include CC-BY")
        if "Metsudah Chumash, Metsudah Publications, 2009" not in row.get("source_version_title", ""):
            errors.append(f"{context}: has Metsudah translation but source_version_title is missing Metsudah")
        if row.get("source_preference") != "primary_preferred_translation_source":
            errors.append(f"{context}: must mark Metsudah as primary_preferred_translation_source")
        if row.get("requires_attribution") != "true":
            errors.append(f"{context}: has source translation but requires_attribution is not true")

    if normalized(row.get("secondary_translation_koren")) and "bereishis_english_koren.jsonl" not in row.get(
        "source_files_used",
        "",
    ):
        errors.append(f"{context}: has Koren secondary translation but source_files_used omits Koren JSONL")

    if row.get("extraction_review_status") != "yossi_extraction_verified":
        errors.append(f"{context}: extraction_review_status must be yossi_extraction_verified")
    if not PEREK_THREE_FINAL_SLICE_VERIFICATION_REPORT_PATH.exists():
        errors.append(
            f"{context}: yossi_extraction_verified rows require {repo_relative(PEREK_THREE_FINAL_SLICE_VERIFICATION_REPORT_PATH)}"
        )
    review_notes = row.get("review_notes", "")
    if "Yossi confirmed extraction accuracy" not in review_notes:
        errors.append(f"{context}: verified rows must record Yossi extraction-accuracy confirmation in review_notes")
    if "source-only for future question/protected-preview planning" not in review_notes:
        errors.append(f"{context}: verified rows must preserve Yossi source-only planning note in review_notes")
    if "Consequence/exile/Gan Eden closure language" not in review_notes:
        errors.append(f"{context}: verified rows must preserve Yossi consequence/exile/Gan Eden question-use note in review_notes")
    if row.get("question_allowed") != "needs_review":
        errors.append(f"{context}: question_allowed must remain needs_review until a future gate")
    for field in ("runtime_allowed", "protected_preview_allowed", "reviewed_bank_allowed"):
        if row.get(field) != "false":
            errors.append(f"{context}: {field} must remain false until a future gate")
    if not normalized(row.get("uncertainty_reason")):
        errors.append(f"{context}: verified rows must preserve uncertainty_reason for future planning")
    if not normalized(row.get("blocked_question_types")):
        errors.append(f"{context}: blocked_question_types must explain that question use is blocked")

    for field, value in row.items():
        lowered = normalized(value).lower()
        if field not in {"review_notes", "uncertainty_reason", "blocked_question_types"} and lowered in FORBIDDEN_READY_VALUES:
            errors.append(f"{context}: field {field} contains forbidden readiness value {value!r}")


def validate_audit_report(errors: list[str]) -> None:
    if not AUDIT_REPORT_PATH.exists():
        return
    try:
        audit = json.loads(AUDIT_REPORT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        errors.append(f"{repo_relative(AUDIT_REPORT_PATH)} is invalid JSON: {error}")
        return
    if audit.get("audit_finding") != "partial_not_full_canonical_map":
        errors.append(f"{repo_relative(AUDIT_REPORT_PATH)} must record audit_finding partial_not_full_canonical_map")
    if audit.get("shortest_path_decision") != "C_existing_data_is_partial_create_small_proof_consolidation_map":
        errors.append(f"{repo_relative(AUDIT_REPORT_PATH)} must record shortest path decision C")
    if audit.get("map_created") != repo_relative(PROOF_MAP_PATH):
        errors.append(f"{repo_relative(AUDIT_REPORT_PATH)} must link the proof map path")
    if not isinstance(audit.get("field_coverage"), list) or not audit["field_coverage"]:
        errors.append(f"{repo_relative(AUDIT_REPORT_PATH)} must include field_coverage entries")


def validate_verified_source_skill_maps() -> dict[str, Any]:
    errors: list[str] = []
    validate_required_files(errors)
    validate_review_packet(errors)
    validate_yossi_review_sheets(errors)
    validate_audit_report(errors)

    rows: list[dict[str, str]] = []
    columns: list[str] = []
    if SEED_MAP_PATH.exists():
        columns, rows = load_tsv(SEED_MAP_PATH)
        missing_columns = [column for column in REQUIRED_COLUMNS if column not in columns]
        if missing_columns:
            errors.append(f"{repo_relative(SEED_MAP_PATH)} missing required columns: {missing_columns}")
        for column in OPTIONAL_KOREN_POLICY_COLUMNS:
            if column not in columns:
                errors.append(f"{repo_relative(SEED_MAP_PATH)} missing Koren policy column: {column}")
        for row_number, row in enumerate(rows, 2):
            validate_row(row, row_number, errors)
    proof_rows: list[dict[str, str]] = []
    proof_columns: list[str] = []
    if PROOF_MAP_PATH.exists():
        proof_columns, proof_rows = load_tsv(PROOF_MAP_PATH)
        missing_columns = [column for column in PROOF_REQUIRED_COLUMNS if column not in proof_columns]
        if missing_columns:
            errors.append(f"{repo_relative(PROOF_MAP_PATH)} missing required columns: {missing_columns}")
        for row_number, row in enumerate(proof_rows, 2):
            validate_proof_row(row, row_number, errors)
    next_slice_rows: list[dict[str, str]] = []
    next_slice_columns: list[str] = []
    if NEXT_SLICE_MAP_PATH.exists():
        next_slice_columns, next_slice_rows = load_tsv(NEXT_SLICE_MAP_PATH)
        missing_columns = [column for column in PROOF_REQUIRED_COLUMNS if column not in next_slice_columns]
        if missing_columns:
            errors.append(f"{repo_relative(NEXT_SLICE_MAP_PATH)} missing required columns: {missing_columns}")
        for row_number, row in enumerate(next_slice_rows, 2):
            validate_pending_expansion_row(row, row_number, errors)
    pending_slice_rows: list[dict[str, str]] = []
    pending_slice_columns: list[str] = []
    if PENDING_SLICE_MAP_PATH.exists():
        pending_slice_columns, pending_slice_rows = load_tsv(PENDING_SLICE_MAP_PATH)
        missing_columns = [column for column in PROOF_REQUIRED_COLUMNS if column not in pending_slice_columns]
        if missing_columns:
            errors.append(f"{repo_relative(PENDING_SLICE_MAP_PATH)} missing required columns: {missing_columns}")
        for row_number, row in enumerate(pending_slice_rows, 2):
            validate_current_pending_slice_row(row, row_number, errors)
    final_slice_rows: list[dict[str, str]] = []
    final_slice_columns: list[str] = []
    if PEREK_ONE_FINAL_SLICE_MAP_PATH.exists():
        final_slice_columns, final_slice_rows = load_tsv(PEREK_ONE_FINAL_SLICE_MAP_PATH)
        missing_columns = [column for column in PROOF_REQUIRED_COLUMNS if column not in final_slice_columns]
        if missing_columns:
            errors.append(f"{repo_relative(PEREK_ONE_FINAL_SLICE_MAP_PATH)} missing required columns: {missing_columns}")
        for row_number, row in enumerate(final_slice_rows, 2):
            validate_perek_one_final_pending_slice_row(row, row_number, errors)

    perek_one_rows = proof_rows + next_slice_rows + pending_slice_rows + final_slice_rows
    if len(perek_one_rows) != 137:
        errors.append(f"Bereishis Perek 1 source-to-skill row count must be 137, found {len(perek_one_rows)}")
    for row in perek_one_rows:
        ref = normalized(row.get("ref"))
        hebrew = normalized(row.get("hebrew_word_or_phrase"))
        context = f"Bereishis Perek 1 completion row {ref} / {hebrew}"
        if row.get("extraction_review_status") != "yossi_extraction_verified":
            errors.append(f"{context}: extraction_review_status must be yossi_extraction_verified")
        if row.get("question_allowed") != "needs_review":
            errors.append(f"{context}: question_allowed must remain needs_review")
        if row.get("runtime_allowed") != "false":
            errors.append(f"{context}: runtime_allowed must remain false")
        if row.get("protected_preview_allowed") != "false":
            errors.append(f"{context}: protected_preview_allowed must remain false")
        if row.get("reviewed_bank_allowed") != "false":
            errors.append(f"{context}: reviewed_bank_allowed must remain false")
    perek_two_opening_rows: list[dict[str, str]] = []
    perek_two_opening_columns: list[str] = []
    if PEREK_TWO_OPENING_SLICE_MAP_PATH.exists():
        perek_two_opening_columns, perek_two_opening_rows = load_tsv(PEREK_TWO_OPENING_SLICE_MAP_PATH)
        missing_columns = [column for column in PROOF_REQUIRED_COLUMNS if column not in perek_two_opening_columns]
        if missing_columns:
            errors.append(f"{repo_relative(PEREK_TWO_OPENING_SLICE_MAP_PATH)} missing required columns: {missing_columns}")
        for row_number, row in enumerate(perek_two_opening_rows, 2):
            validate_perek_two_opening_pending_slice_row(row, row_number, errors)
        refs = {row.get("ref") for row in perek_two_opening_rows}
        if refs != {"Bereishis 2:1", "Bereishis 2:2", "Bereishis 2:3"}:
            errors.append(f"{repo_relative(PEREK_TWO_OPENING_SLICE_MAP_PATH)} must cover only Bereishis 2:1-2:3, found {sorted(refs)}")
        if len(perek_two_opening_rows) != 9:
            errors.append(f"{repo_relative(PEREK_TWO_OPENING_SLICE_MAP_PATH)} must contain 9 rows, found {len(perek_two_opening_rows)}")
    perek_two_expansion_rows: list[dict[str, str]] = []
    perek_two_expansion_columns: list[str] = []
    if PEREK_TWO_EXPANSION_SLICE_MAP_PATH.exists():
        perek_two_expansion_columns, perek_two_expansion_rows = load_tsv(PEREK_TWO_EXPANSION_SLICE_MAP_PATH)
        missing_columns = [column for column in PROOF_REQUIRED_COLUMNS if column not in perek_two_expansion_columns]
        if missing_columns:
            errors.append(f"{repo_relative(PEREK_TWO_EXPANSION_SLICE_MAP_PATH)} missing required columns: {missing_columns}")
        for row_number, row in enumerate(perek_two_expansion_rows, 2):
            validate_perek_two_expansion_verified_slice_row(row, row_number, errors)
        refs = {row.get("ref") for row in perek_two_expansion_rows}
        expected_refs = {f"Bereishis 2:{pasuk}" for pasuk in range(4, 18)}
        if refs != expected_refs:
            errors.append(f"{repo_relative(PEREK_TWO_EXPANSION_SLICE_MAP_PATH)} must cover only Bereishis 2:4-2:17, found {sorted(refs)}")
        if len(perek_two_expansion_rows) != 54:
            errors.append(f"{repo_relative(PEREK_TWO_EXPANSION_SLICE_MAP_PATH)} must contain 54 rows, found {len(perek_two_expansion_rows)}")
    perek_two_final_rows: list[dict[str, str]] = []
    perek_two_final_columns: list[str] = []
    if PEREK_TWO_FINAL_SLICE_MAP_PATH.exists():
        perek_two_final_columns, perek_two_final_rows = load_tsv(PEREK_TWO_FINAL_SLICE_MAP_PATH)
        missing_columns = [column for column in PROOF_REQUIRED_COLUMNS if column not in perek_two_final_columns]
        if missing_columns:
            errors.append(f"{repo_relative(PEREK_TWO_FINAL_SLICE_MAP_PATH)} missing required columns: {missing_columns}")
        for row_number, row in enumerate(perek_two_final_rows, 2):
            validate_perek_two_final_verified_slice_row(row, row_number, errors)
        refs = {row.get("ref") for row in perek_two_final_rows}
        expected_refs = {f"Bereishis 2:{pasuk}" for pasuk in range(18, 26)}
        if refs != expected_refs:
            errors.append(f"{repo_relative(PEREK_TWO_FINAL_SLICE_MAP_PATH)} must cover only Bereishis 2:18-2:25, found {sorted(refs)}")
        if len(perek_two_final_rows) != 36:
            errors.append(f"{repo_relative(PEREK_TWO_FINAL_SLICE_MAP_PATH)} must contain 36 rows, found {len(perek_two_final_rows)}")

    perek_two_rows = perek_two_opening_rows + perek_two_expansion_rows + perek_two_final_rows
    if len(perek_two_rows) != 99:
        errors.append(f"Bereishis Perek 2 source-to-skill row count must be 99, found {len(perek_two_rows)}")
    for row in perek_two_rows:
        ref = normalized(row.get("ref"))
        hebrew = normalized(row.get("hebrew_word_or_phrase"))
        context = f"Bereishis Perek 2 completion row {ref} / {hebrew}"
        if row.get("extraction_review_status") != "yossi_extraction_verified":
            errors.append(f"{context}: extraction_review_status must be yossi_extraction_verified")
        if row.get("question_allowed") != "needs_review":
            errors.append(f"{context}: question_allowed must remain needs_review")
        if row.get("runtime_allowed") != "false":
            errors.append(f"{context}: runtime_allowed must remain false")
        if row.get("protected_preview_allowed") != "false":
            errors.append(f"{context}: protected_preview_allowed must remain false")
        if row.get("reviewed_bank_allowed") != "false":
            errors.append(f"{context}: reviewed_bank_allowed must remain false")

    combined_verified_rows = perek_one_rows + perek_two_rows
    if len(combined_verified_rows) != 236:
        errors.append(
            f"Combined Bereishis Perek 1-2 source-to-skill row count must be 236, found {len(combined_verified_rows)}"
        )
    perek_three_opening_rows: list[dict[str, str]] = []
    perek_three_opening_columns: list[str] = []
    if PEREK_THREE_OPENING_SLICE_MAP_PATH.exists():
        perek_three_opening_columns, perek_three_opening_rows = load_tsv(PEREK_THREE_OPENING_SLICE_MAP_PATH)
        missing_columns = [column for column in PROOF_REQUIRED_COLUMNS if column not in perek_three_opening_columns]
        if missing_columns:
            errors.append(f"{repo_relative(PEREK_THREE_OPENING_SLICE_MAP_PATH)} missing required columns: {missing_columns}")
        for row_number, row in enumerate(perek_three_opening_rows, 2):
            validate_perek_three_opening_verified_slice_row(row, row_number, errors)
        refs = {row.get("ref") for row in perek_three_opening_rows}
        expected_refs = {f"Bereishis 3:{pasuk}" for pasuk in range(1, 8)}
        if refs != expected_refs:
            errors.append(f"{repo_relative(PEREK_THREE_OPENING_SLICE_MAP_PATH)} must cover only Bereishis 3:1-3:7, found {sorted(refs)}")
        if len(perek_three_opening_rows) != 33:
            errors.append(f"{repo_relative(PEREK_THREE_OPENING_SLICE_MAP_PATH)} must contain 33 rows, found {len(perek_three_opening_rows)}")

    perek_three_expansion_rows: list[dict[str, str]] = []
    perek_three_expansion_columns: list[str] = []
    if PEREK_THREE_EXPANSION_SLICE_MAP_PATH.exists():
        perek_three_expansion_columns, perek_three_expansion_rows = load_tsv(PEREK_THREE_EXPANSION_SLICE_MAP_PATH)
        missing_columns = [column for column in PROOF_REQUIRED_COLUMNS if column not in perek_three_expansion_columns]
        if missing_columns:
            errors.append(f"{repo_relative(PEREK_THREE_EXPANSION_SLICE_MAP_PATH)} missing required columns: {missing_columns}")
        for row_number, row in enumerate(perek_three_expansion_rows, 2):
            validate_perek_three_expansion_verified_slice_row(row, row_number, errors)
        refs = {row.get("ref") for row in perek_three_expansion_rows}
        expected_refs = {f"Bereishis 3:{pasuk}" for pasuk in range(8, 17)}
        if refs != expected_refs:
            errors.append(
                f"{repo_relative(PEREK_THREE_EXPANSION_SLICE_MAP_PATH)} must cover only Bereishis 3:8-3:16, found {sorted(refs)}"
            )
        if len(perek_three_expansion_rows) != 48:
            errors.append(
                f"{repo_relative(PEREK_THREE_EXPANSION_SLICE_MAP_PATH)} must contain 48 rows, found {len(perek_three_expansion_rows)}"
            )

    perek_three_final_rows: list[dict[str, str]] = []
    perek_three_final_columns: list[str] = []
    if PEREK_THREE_FINAL_SLICE_MAP_PATH.exists():
        perek_three_final_columns, perek_three_final_rows = load_tsv(PEREK_THREE_FINAL_SLICE_MAP_PATH)
        missing_columns = [column for column in PROOF_REQUIRED_COLUMNS if column not in perek_three_final_columns]
        if missing_columns:
            errors.append(f"{repo_relative(PEREK_THREE_FINAL_SLICE_MAP_PATH)} missing required columns: {missing_columns}")
        for row_number, row in enumerate(perek_three_final_rows, 2):
            validate_perek_three_final_verified_slice_row(row, row_number, errors)
        refs = {row.get("ref") for row in perek_three_final_rows}
        expected_refs = {f"Bereishis 3:{pasuk}" for pasuk in range(17, 25)}
        if refs != expected_refs:
            errors.append(
                f"{repo_relative(PEREK_THREE_FINAL_SLICE_MAP_PATH)} must cover only Bereishis 3:17-3:24, found {sorted(refs)}"
            )
        if len(perek_three_final_rows) != 38:
            errors.append(
                f"{repo_relative(PEREK_THREE_FINAL_SLICE_MAP_PATH)} must contain 38 rows, found {len(perek_three_final_rows)}"
            )

    perek_three_rows = perek_three_opening_rows + perek_three_expansion_rows + perek_three_final_rows
    if len(perek_three_rows) != 119:
        errors.append(f"Bereishis Perek 3 source-to-skill row count must be 119, found {len(perek_three_rows)}")
    for row in perek_three_rows:
        ref = normalized(row.get("ref"))
        hebrew = normalized(row.get("hebrew_word_or_phrase"))
        context = f"Bereishis Perek 3 completion row {ref} / {hebrew}"
        if row.get("extraction_review_status") != "yossi_extraction_verified":
            errors.append(f"{context}: extraction_review_status must be yossi_extraction_verified")
        if row.get("question_allowed") != "needs_review":
            errors.append(f"{context}: question_allowed must remain needs_review")
        if row.get("runtime_allowed") != "false":
            errors.append(f"{context}: runtime_allowed must remain false")
        if row.get("protected_preview_allowed") != "false":
            errors.append(f"{context}: protected_preview_allowed must remain false")
        if row.get("reviewed_bank_allowed") != "false":
            errors.append(f"{context}: reviewed_bank_allowed must remain false")

    combined_perek_one_two_three_rows = perek_one_rows + perek_two_rows + perek_three_rows
    if len(combined_perek_one_two_three_rows) != 355:
        errors.append(
            "Combined Bereishis Perek 1-3 source-to-skill row count must be 355, "
            f"found {len(combined_perek_one_two_three_rows)}"
        )

    return {
        "valid": not errors,
        "map_path": repo_relative(SEED_MAP_PATH),
        "proof_map_path": repo_relative(PROOF_MAP_PATH),
        "review_packet_path": repo_relative(SEED_REVIEW_PACKET_PATH),
        "proof_review_packet_path": repo_relative(PROOF_REVIEW_PACKET_PATH),
        "proof_verification_report_path": repo_relative(PROOF_VERIFICATION_REPORT_PATH),
        "next_slice_map_path": repo_relative(NEXT_SLICE_MAP_PATH),
        "next_slice_build_report_path": repo_relative(NEXT_SLICE_BUILD_REPORT_PATH),
        "next_slice_review_packet_path": repo_relative(NEXT_SLICE_REVIEW_PACKET_PATH),
        "next_slice_verification_report_path": repo_relative(NEXT_SLICE_VERIFICATION_REPORT_PATH),
        "pending_slice_map_path": repo_relative(PENDING_SLICE_MAP_PATH),
        "pending_slice_build_report_path": repo_relative(PENDING_SLICE_BUILD_REPORT_PATH),
        "pending_slice_review_packet_path": repo_relative(PENDING_SLICE_REVIEW_PACKET_PATH),
        "pending_slice_verification_report_path": repo_relative(PENDING_SLICE_VERIFICATION_REPORT_PATH),
        "perek_one_final_slice_map_path": repo_relative(PEREK_ONE_FINAL_SLICE_MAP_PATH),
        "perek_one_final_slice_build_report_path": repo_relative(PEREK_ONE_FINAL_SLICE_BUILD_REPORT_PATH),
        "perek_one_final_slice_review_packet_path": repo_relative(PEREK_ONE_FINAL_SLICE_REVIEW_PACKET_PATH),
        "perek_one_final_slice_verification_report_path": repo_relative(PEREK_ONE_FINAL_SLICE_VERIFICATION_REPORT_PATH),
        "perek_one_completion_report_path": repo_relative(PEREK_ONE_COMPLETION_REPORT_PATH),
        "perek_two_opening_slice_map_path": repo_relative(PEREK_TWO_OPENING_SLICE_MAP_PATH),
        "perek_two_opening_slice_build_report_path": repo_relative(PEREK_TWO_OPENING_SLICE_BUILD_REPORT_PATH),
        "perek_two_opening_slice_review_packet_path": repo_relative(PEREK_TWO_OPENING_SLICE_REVIEW_PACKET_PATH),
        "perek_two_opening_slice_review_sheet_md_path": repo_relative(PEREK_TWO_OPENING_SLICE_REVIEW_SHEET_MD_PATH),
        "perek_two_opening_slice_review_sheet_csv_path": repo_relative(PEREK_TWO_OPENING_SLICE_REVIEW_SHEET_CSV_PATH),
        "perek_two_opening_slice_verification_report_path": repo_relative(PEREK_TWO_OPENING_SLICE_VERIFICATION_REPORT_PATH),
        "perek_two_expansion_slice_map_path": repo_relative(PEREK_TWO_EXPANSION_SLICE_MAP_PATH),
        "perek_two_expansion_slice_build_report_path": repo_relative(PEREK_TWO_EXPANSION_SLICE_BUILD_REPORT_PATH),
        "perek_two_expansion_slice_review_packet_path": repo_relative(PEREK_TWO_EXPANSION_SLICE_REVIEW_PACKET_PATH),
        "perek_two_expansion_slice_review_sheet_md_path": repo_relative(PEREK_TWO_EXPANSION_SLICE_REVIEW_SHEET_MD_PATH),
        "perek_two_expansion_slice_review_sheet_csv_path": repo_relative(PEREK_TWO_EXPANSION_SLICE_REVIEW_SHEET_CSV_PATH),
        "perek_two_expansion_slice_verification_report_path": repo_relative(
            PEREK_TWO_EXPANSION_SLICE_VERIFICATION_REPORT_PATH
        ),
        "perek_two_final_slice_map_path": repo_relative(PEREK_TWO_FINAL_SLICE_MAP_PATH),
        "perek_two_final_slice_build_report_path": repo_relative(PEREK_TWO_FINAL_SLICE_BUILD_REPORT_PATH),
        "perek_two_final_slice_review_packet_path": repo_relative(PEREK_TWO_FINAL_SLICE_REVIEW_PACKET_PATH),
        "perek_two_final_slice_review_sheet_md_path": repo_relative(PEREK_TWO_FINAL_SLICE_REVIEW_SHEET_MD_PATH),
        "perek_two_final_slice_review_sheet_csv_path": repo_relative(PEREK_TWO_FINAL_SLICE_REVIEW_SHEET_CSV_PATH),
        "perek_two_final_slice_verification_report_path": repo_relative(
            PEREK_TWO_FINAL_SLICE_VERIFICATION_REPORT_PATH
        ),
        "perek_two_completion_report_path": repo_relative(PEREK_TWO_COMPLETION_REPORT_PATH),
        "perek_three_opening_slice_map_path": repo_relative(PEREK_THREE_OPENING_SLICE_MAP_PATH),
        "perek_three_opening_slice_build_report_path": repo_relative(PEREK_THREE_OPENING_SLICE_BUILD_REPORT_PATH),
        "perek_three_opening_slice_review_packet_path": repo_relative(PEREK_THREE_OPENING_SLICE_REVIEW_PACKET_PATH),
        "perek_three_opening_slice_review_sheet_md_path": repo_relative(PEREK_THREE_OPENING_SLICE_REVIEW_SHEET_MD_PATH),
        "perek_three_opening_slice_review_sheet_csv_path": repo_relative(PEREK_THREE_OPENING_SLICE_REVIEW_SHEET_CSV_PATH),
        "perek_three_opening_slice_verification_report_path": repo_relative(
            PEREK_THREE_OPENING_SLICE_VERIFICATION_REPORT_PATH
        ),
        "perek_three_expansion_slice_map_path": repo_relative(PEREK_THREE_EXPANSION_SLICE_MAP_PATH),
        "perek_three_expansion_slice_build_report_path": repo_relative(PEREK_THREE_EXPANSION_SLICE_BUILD_REPORT_PATH),
        "perek_three_expansion_slice_review_packet_path": repo_relative(PEREK_THREE_EXPANSION_SLICE_REVIEW_PACKET_PATH),
        "perek_three_expansion_slice_review_sheet_md_path": repo_relative(PEREK_THREE_EXPANSION_SLICE_REVIEW_SHEET_MD_PATH),
        "perek_three_expansion_slice_review_sheet_csv_path": repo_relative(
            PEREK_THREE_EXPANSION_SLICE_REVIEW_SHEET_CSV_PATH
        ),
        "perek_three_expansion_slice_verification_report_path": repo_relative(
            PEREK_THREE_EXPANSION_SLICE_VERIFICATION_REPORT_PATH
        ),
        "perek_three_final_slice_map_path": repo_relative(PEREK_THREE_FINAL_SLICE_MAP_PATH),
        "perek_three_final_slice_build_report_path": repo_relative(PEREK_THREE_FINAL_SLICE_BUILD_REPORT_PATH),
        "perek_three_final_slice_review_packet_path": repo_relative(PEREK_THREE_FINAL_SLICE_REVIEW_PACKET_PATH),
        "perek_three_final_slice_review_sheet_md_path": repo_relative(PEREK_THREE_FINAL_SLICE_REVIEW_SHEET_MD_PATH),
        "perek_three_final_slice_review_sheet_csv_path": repo_relative(PEREK_THREE_FINAL_SLICE_REVIEW_SHEET_CSV_PATH),
        "perek_three_final_slice_verification_report_path": repo_relative(PEREK_THREE_FINAL_SLICE_VERIFICATION_REPORT_PATH),
        "perek_three_completion_report_path": repo_relative(PEREK_THREE_COMPLETION_REPORT_PATH),
        "audit_report_path": repo_relative(AUDIT_REPORT_PATH),
        "row_count": len(rows),
        "proof_row_count": len(proof_rows),
        "next_slice_row_count": len(next_slice_rows),
        "pending_slice_row_count": len(pending_slice_rows),
        "perek_one_final_slice_row_count": len(final_slice_rows),
        "perek_one_verified_row_count": len(perek_one_rows),
        "perek_two_opening_slice_row_count": len(perek_two_opening_rows),
        "perek_two_expansion_slice_row_count": len(perek_two_expansion_rows),
        "perek_two_final_slice_row_count": len(perek_two_final_rows),
        "perek_two_verified_row_count": len(perek_two_rows),
        "perek_one_two_verified_row_count": len(combined_verified_rows),
        "perek_three_opening_slice_row_count": len(perek_three_opening_rows),
        "perek_three_expansion_slice_row_count": len(perek_three_expansion_rows),
        "perek_three_final_slice_row_count": len(perek_three_final_rows),
        "perek_three_verified_row_count": len(perek_three_rows),
        "perek_one_two_three_verified_row_count": len(combined_perek_one_two_three_rows),
        "columns": columns,
        "proof_columns": proof_columns,
        "next_slice_columns": next_slice_columns,
        "pending_slice_columns": pending_slice_columns,
        "perek_one_final_slice_columns": final_slice_columns,
        "perek_two_opening_slice_columns": perek_two_opening_columns,
        "perek_two_expansion_slice_columns": perek_two_expansion_columns,
        "perek_two_final_slice_columns": perek_two_final_columns,
        "perek_three_opening_slice_columns": perek_three_opening_columns,
        "perek_three_expansion_slice_columns": perek_three_expansion_columns,
        "perek_three_final_slice_columns": perek_three_final_columns,
        "errors": errors,
    }


def main() -> int:
    summary = validate_verified_source_skill_maps()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
