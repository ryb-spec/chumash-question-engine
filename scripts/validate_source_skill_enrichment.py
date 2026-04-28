from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
ENRICHMENT_DIR = ROOT / "data" / "source_skill_enrichment"
SOURCE_MAP_PATH = ROOT / "data" / "verified_source_skill_maps" / "bereishis_1_1_to_1_5_source_to_skill_map.tsv"
NEXT_SOURCE_MAP_PATH = (
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_1_6_to_1_13_source_to_skill_map.tsv"
)
EXPANSION_SOURCE_MAP_PATH = (
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_1_14_to_1_23_source_to_skill_map.tsv"
)
PEREK1_FINAL_SOURCE_MAP_PATH = (
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_1_24_to_1_31_source_to_skill_map.tsv"
)
CONTRACT_PATH = ROOT / "data" / "standards" / "canonical_skill_contract.json"

MORPHOLOGY_PATH = (
    ENRICHMENT_DIR / "morphology_candidates" / "bereishis_1_1_to_1_5_morphology_candidates.tsv"
)
STANDARDS_PATH = (
    ENRICHMENT_DIR / "standards_candidates" / "bereishis_1_1_to_1_5_standards_candidates.tsv"
)
VOCABULARY_PATH = (
    ENRICHMENT_DIR
    / "vocabulary_shoresh_candidates"
    / "bereishis_1_1_to_1_5_vocabulary_shoresh_candidates.tsv"
)
TOKEN_SPLIT_STANDARDS_PATH = (
    ENRICHMENT_DIR
    / "standards_candidates"
    / "bereishis_1_1_to_1_5_token_split_standards_candidates.tsv"
)
NEXT_MORPHOLOGY_PATH = (
    ENRICHMENT_DIR / "morphology_candidates" / "bereishis_1_6_to_1_13_morphology_candidates.tsv"
)
NEXT_STANDARDS_PATH = (
    ENRICHMENT_DIR / "standards_candidates" / "bereishis_1_6_to_1_13_standards_candidates.tsv"
)
NEXT_VOCABULARY_PATH = (
    ENRICHMENT_DIR
    / "vocabulary_shoresh_candidates"
    / "bereishis_1_6_to_1_13_vocabulary_shoresh_candidates.tsv"
)
NEXT_TOKEN_SPLIT_STANDARDS_PATH = (
    ENRICHMENT_DIR
    / "standards_candidates"
    / "bereishis_1_6_to_1_13_token_split_standards_candidates.tsv"
)
EXPANSION_MORPHOLOGY_PATH = (
    ENRICHMENT_DIR / "morphology_candidates" / "bereishis_1_14_to_1_23_morphology_candidates.tsv"
)
EXPANSION_STANDARDS_PATH = (
    ENRICHMENT_DIR / "standards_candidates" / "bereishis_1_14_to_1_23_standards_candidates.tsv"
)
EXPANSION_VOCABULARY_PATH = (
    ENRICHMENT_DIR
    / "vocabulary_shoresh_candidates"
    / "bereishis_1_14_to_1_23_vocabulary_shoresh_candidates.tsv"
)
EXPANSION_TOKEN_SPLIT_STANDARDS_PATH = (
    ENRICHMENT_DIR
    / "standards_candidates"
    / "bereishis_1_14_to_1_23_token_split_standards_candidates.tsv"
)
PEREK1_FINAL_MORPHOLOGY_PATH = (
    ENRICHMENT_DIR / "morphology_candidates" / "bereishis_1_24_to_1_31_morphology_candidates.tsv"
)
PEREK1_FINAL_STANDARDS_PATH = (
    ENRICHMENT_DIR / "standards_candidates" / "bereishis_1_24_to_1_31_standards_candidates.tsv"
)
PEREK1_FINAL_VOCABULARY_PATH = (
    ENRICHMENT_DIR
    / "vocabulary_shoresh_candidates"
    / "bereishis_1_24_to_1_31_vocabulary_shoresh_candidates.tsv"
)
PEREK1_FINAL_TOKEN_SPLIT_STANDARDS_PATH = (
    ENRICHMENT_DIR
    / "standards_candidates"
    / "bereishis_1_24_to_1_31_token_split_standards_candidates.tsv"
)
CONTRACT_PATH = ROOT / "data" / "standards" / "canonical_skill_contract.json"

README_PATH = ENRICHMENT_DIR / "README.md"
AUDIT_REPORT_PATH = ENRICHMENT_DIR / "reports" / "morphology_standards_enrichment_audit.md"

REVIEW_SHEETS = {
    "morphology": (
        ENRICHMENT_DIR / "reports" / "bereishis_1_1_to_1_5_morphology_enrichment_yossi_review_sheet.md",
        ENRICHMENT_DIR / "reports" / "bereishis_1_1_to_1_5_morphology_enrichment_yossi_review_sheet.csv",
    ),
    "standards": (
        ENRICHMENT_DIR / "reports" / "bereishis_1_1_to_1_5_standards_enrichment_yossi_review_sheet.md",
        ENRICHMENT_DIR / "reports" / "bereishis_1_1_to_1_5_standards_enrichment_yossi_review_sheet.csv",
    ),
    "vocabulary_shoresh": (
        ENRICHMENT_DIR / "reports" / "bereishis_1_1_to_1_5_vocabulary_shoresh_enrichment_yossi_review_sheet.md",
        ENRICHMENT_DIR / "reports" / "bereishis_1_1_to_1_5_vocabulary_shoresh_enrichment_yossi_review_sheet.csv",
    ),
}

APPLIED_REVIEW_REPORTS = {
    "morphology": (
        ENRICHMENT_DIR
        / "reports"
        / "bereishis_1_1_to_1_5_morphology_enrichment_yossi_review_applied.md"
    ),
    "standards": (
        ENRICHMENT_DIR
        / "reports"
        / "bereishis_1_1_to_1_5_standards_enrichment_yossi_review_applied.md"
    ),
    "vocabulary_shoresh": (
        ENRICHMENT_DIR
        / "reports"
        / "bereishis_1_1_to_1_5_vocabulary_shoresh_enrichment_yossi_review_applied.md"
    ),
}

FOLLOW_UP_INVENTORY_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_1_to_1_5_enrichment_follow_up_inventory.md"
)
FOLLOW_UP_REVIEW_MD_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_1_to_1_5_enrichment_follow_up_yossi_review_sheet.md"
)
FOLLOW_UP_REVIEW_CSV_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_1_to_1_5_enrichment_follow_up_yossi_review_sheet.csv"
)
TOKEN_SPLIT_AUDIT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_1_to_1_5_token_split_standards_audit.md"
)
TOKEN_SPLIT_REVIEW_MD_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_1_to_1_5_token_split_standards_yossi_review_sheet.md"
)
TOKEN_SPLIT_REVIEW_CSV_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_1_to_1_5_token_split_standards_yossi_review_sheet.csv"
)
TOKEN_SPLIT_APPLIED_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_1_to_1_5_token_split_standards_yossi_review_applied.md"
)
NEXT_REVIEW_SHEETS = {
    "morphology": (
        ENRICHMENT_DIR / "reports" / "bereishis_1_6_to_1_13_morphology_enrichment_yossi_review_sheet.md",
        ENRICHMENT_DIR / "reports" / "bereishis_1_6_to_1_13_morphology_enrichment_yossi_review_sheet.csv",
    ),
    "standards": (
        ENRICHMENT_DIR / "reports" / "bereishis_1_6_to_1_13_standards_enrichment_yossi_review_sheet.md",
        ENRICHMENT_DIR / "reports" / "bereishis_1_6_to_1_13_standards_enrichment_yossi_review_sheet.csv",
    ),
    "vocabulary_shoresh": (
        ENRICHMENT_DIR / "reports" / "bereishis_1_6_to_1_13_vocabulary_shoresh_enrichment_yossi_review_sheet.md",
        ENRICHMENT_DIR / "reports" / "bereishis_1_6_to_1_13_vocabulary_shoresh_enrichment_yossi_review_sheet.csv",
    ),
}
NEXT_TOKEN_SPLIT_REVIEW_MD_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_6_to_1_13_token_split_standards_yossi_review_sheet.md"
)
NEXT_TOKEN_SPLIT_REVIEW_CSV_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_6_to_1_13_token_split_standards_yossi_review_sheet.csv"
)
NEXT_GENERATION_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_6_to_1_13_enrichment_candidate_generation_report.md"
)
EXPANSION_REVIEW_SHEETS = {
    "morphology": (
        ENRICHMENT_DIR / "reports" / "bereishis_1_14_to_1_23_morphology_enrichment_yossi_review_sheet.md",
        ENRICHMENT_DIR / "reports" / "bereishis_1_14_to_1_23_morphology_enrichment_yossi_review_sheet.csv",
    ),
    "standards": (
        ENRICHMENT_DIR / "reports" / "bereishis_1_14_to_1_23_standards_enrichment_yossi_review_sheet.md",
        ENRICHMENT_DIR / "reports" / "bereishis_1_14_to_1_23_standards_enrichment_yossi_review_sheet.csv",
    ),
    "vocabulary_shoresh": (
        ENRICHMENT_DIR
        / "reports"
        / "bereishis_1_14_to_1_23_vocabulary_shoresh_enrichment_yossi_review_sheet.md",
        ENRICHMENT_DIR
        / "reports"
        / "bereishis_1_14_to_1_23_vocabulary_shoresh_enrichment_yossi_review_sheet.csv",
    ),
}
PEREK1_FINAL_REVIEW_SHEETS = {
    "morphology": (
        ENRICHMENT_DIR / "reports" / "bereishis_1_24_to_1_31_morphology_enrichment_yossi_review_sheet.md",
        ENRICHMENT_DIR / "reports" / "bereishis_1_24_to_1_31_morphology_enrichment_yossi_review_sheet.csv",
    ),
    "standards": (
        ENRICHMENT_DIR / "reports" / "bereishis_1_24_to_1_31_standards_enrichment_yossi_review_sheet.md",
        ENRICHMENT_DIR / "reports" / "bereishis_1_24_to_1_31_standards_enrichment_yossi_review_sheet.csv",
    ),
    "vocabulary_shoresh": (
        ENRICHMENT_DIR
        / "reports"
        / "bereishis_1_24_to_1_31_vocabulary_shoresh_enrichment_yossi_review_sheet.md",
        ENRICHMENT_DIR
        / "reports"
        / "bereishis_1_24_to_1_31_vocabulary_shoresh_enrichment_yossi_review_sheet.csv",
    ),
}
EXPANSION_TOKEN_SPLIT_REVIEW_MD_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_14_to_1_23_token_split_standards_yossi_review_sheet.md"
)
EXPANSION_TOKEN_SPLIT_REVIEW_CSV_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_14_to_1_23_token_split_standards_yossi_review_sheet.csv"
)
EXPANSION_AUDIT_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_14_to_1_23_enrichment_candidate_audit.md"
)
EXPANSION_GENERATION_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_14_to_1_23_enrichment_candidate_generation_report.md"
)
EXPANSION_MORPHOLOGY_APPLIED_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_14_to_1_23_morphology_enrichment_yossi_review_applied.md"
)
EXPANSION_VOCAB_APPLIED_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_14_to_1_23_vocabulary_shoresh_enrichment_yossi_review_applied.md"
)
EXPANSION_STANDARDS_APPLIED_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_14_to_1_23_standards_enrichment_yossi_review_applied.md"
)
EXPANSION_TOKEN_SPLIT_APPLIED_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_14_to_1_23_token_split_standards_yossi_review_applied.md"
)
EXPANSION_SLICE_REVIEW_SUMMARY_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_14_to_1_23_enrichment_review_summary.md"
)
EXPANSION_MINI_COMPLETION_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_14_to_1_23_enrichment_mini_completion_report.md"
)
PEREK1_FINAL_TOKEN_SPLIT_REVIEW_MD_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_24_to_1_31_token_split_standards_yossi_review_sheet.md"
)
PEREK1_FINAL_TOKEN_SPLIT_REVIEW_CSV_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_24_to_1_31_token_split_standards_yossi_review_sheet.csv"
)
PEREK1_FINAL_AUDIT_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_24_to_1_31_enrichment_candidate_audit.md"
)
PEREK1_FINAL_GENERATION_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_24_to_1_31_enrichment_candidate_generation_report.md"
)
PEREK1_FINAL_MORPHOLOGY_APPLIED_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_24_to_1_31_morphology_enrichment_yossi_review_applied.md"
)
PEREK1_FINAL_VOCAB_APPLIED_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_24_to_1_31_vocabulary_shoresh_enrichment_yossi_review_applied.md"
)
PEREK1_FINAL_STANDARDS_APPLIED_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_24_to_1_31_standards_enrichment_yossi_review_applied.md"
)
PEREK1_FINAL_TOKEN_SPLIT_APPLIED_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_24_to_1_31_token_split_standards_yossi_review_applied.md"
)
PEREK1_FINAL_REVIEW_SUMMARY_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_24_to_1_31_enrichment_review_summary.md"
)
PEREK1_COVERAGE_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_perek_1_enrichment_review_application_coverage_report.md"
)
PEREK2_SOURCE_MAP_PATHS = (
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_2_1_to_2_3_source_to_skill_map.tsv",
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_2_4_to_2_17_source_to_skill_map.tsv",
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_2_18_to_2_25_source_to_skill_map.tsv",
)
PEREK2_MORPHOLOGY_PATH = (
    ENRICHMENT_DIR / "morphology_candidates" / "bereishis_perek_2_morphology_candidates.tsv"
)
PEREK2_VOCABULARY_PATH = (
    ENRICHMENT_DIR
    / "vocabulary_shoresh_candidates"
    / "bereishis_perek_2_vocabulary_shoresh_candidates.tsv"
)
PEREK2_STANDARDS_PATH = (
    ENRICHMENT_DIR / "standards_candidates" / "bereishis_perek_2_standards_candidates.tsv"
)
PEREK2_TOKEN_SPLIT_STANDARDS_PATH = (
    ENRICHMENT_DIR / "standards_candidates" / "bereishis_perek_2_token_split_standards_candidates.tsv"
)
PEREK2_REVIEW_SHEETS = {
    "morphology": (
        ENRICHMENT_DIR / "reports" / "bereishis_perek_2_morphology_enrichment_yossi_review_sheet.md",
        ENRICHMENT_DIR / "reports" / "bereishis_perek_2_morphology_enrichment_yossi_review_sheet.csv",
    ),
    "vocabulary_shoresh": (
        ENRICHMENT_DIR / "reports" / "bereishis_perek_2_vocabulary_shoresh_enrichment_yossi_review_sheet.md",
        ENRICHMENT_DIR / "reports" / "bereishis_perek_2_vocabulary_shoresh_enrichment_yossi_review_sheet.csv",
    ),
    "standards": (
        ENRICHMENT_DIR / "reports" / "bereishis_perek_2_standards_enrichment_yossi_review_sheet.md",
        ENRICHMENT_DIR / "reports" / "bereishis_perek_2_standards_enrichment_yossi_review_sheet.csv",
    ),
    "token_split_standards": (
        ENRICHMENT_DIR / "reports" / "bereishis_perek_2_token_split_standards_yossi_review_sheet.md",
        ENRICHMENT_DIR / "reports" / "bereishis_perek_2_token_split_standards_yossi_review_sheet.csv",
    ),
}
PEREK2_SOURCE_READINESS_AUDIT_PATH = (
    ROOT / "data" / "pipeline_rounds" / "reports" / "bereishis_perek_2_gate_1_source_readiness_audit.md"
)
PEREK2_GATE1_REPORT_PATH = (
    ROOT / "data" / "pipeline_rounds" / "reports" / "bereishis_perek_2_gate_1_source_enrichment_eligibility_report.md"
)
NEXT_MORPHOLOGY_APPLIED_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_6_to_1_13_morphology_enrichment_yossi_review_applied.md"
)
NEXT_VOCAB_APPLIED_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_6_to_1_13_vocabulary_shoresh_enrichment_yossi_review_applied.md"
)
NEXT_STANDARDS_APPLIED_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_6_to_1_13_standards_enrichment_yossi_review_applied.md"
)
NEXT_TOKEN_SPLIT_APPLIED_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_6_to_1_13_token_split_standards_yossi_review_applied.md"
)
NEXT_SLICE_REVIEW_SUMMARY_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_6_to_1_13_enrichment_review_summary.md"
)
NEXT_MINI_COMPLETION_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_6_to_1_13_enrichment_mini_completion_report.md"
)
NEXT_FOLLOW_UP_INVENTORY_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_6_to_1_13_enrichment_follow_up_inventory.md"
)
PILOT_COMPLETION_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_1_to_1_5_enrichment_pilot_completion_report.md"
)

MORPHOLOGY_COLUMNS = [
    "candidate_id",
    "source_map_file",
    "source_row_id",
    "ref",
    "hebrew_phrase",
    "token_index",
    "hebrew_token",
    "clean_hebrew_no_nikud",
    "proposed_shoresh",
    "proposed_prefixes",
    "proposed_suffixes",
    "proposed_tense",
    "proposed_person",
    "proposed_gender",
    "proposed_number",
    "proposed_part_of_speech",
    "proposed_dikduk_feature",
    "evidence_source_id",
    "evidence_source_type",
    "evidence_note",
    "confidence",
    "enrichment_review_status",
    "yossi_decision",
    "yossi_notes",
    "question_allowed",
    "protected_preview_allowed",
    "runtime_allowed",
    "reviewed_bank_allowed",
]

STANDARDS_COLUMNS = [
    "candidate_id",
    "source_map_file",
    "source_row_id",
    "ref",
    "hebrew_phrase",
    "skill_primary",
    "skill_secondary",
    "proposed_skill_id",
    "proposed_zekelman_standard",
    "proposed_standard_level",
    "evidence_source_id",
    "evidence_source_type",
    "evidence_note",
    "confidence",
    "enrichment_review_status",
    "yossi_decision",
    "yossi_notes",
    "question_allowed",
    "protected_preview_allowed",
    "runtime_allowed",
    "reviewed_bank_allowed",
]

TOKEN_SPLIT_STANDARDS_COLUMNS = [
    "candidate_id",
    "parent_candidate_id",
    "source_map_file",
    "source_row_id",
    "ref",
    "hebrew_phrase",
    "token_index",
    "hebrew_token",
    "clean_hebrew_no_nikud",
    "proposed_skill_id",
    "proposed_zekelman_standard",
    "proposed_standard_level",
    "canonical_skill_id",
    "canonical_standard_anchor",
    "evidence_source_id",
    "evidence_source_type",
    "evidence_note",
    "confidence",
    "enrichment_review_status",
    "yossi_decision",
    "yossi_notes",
    "question_allowed",
    "protected_preview_allowed",
    "reviewed_bank_allowed",
    "runtime_allowed",
]

VOCABULARY_COLUMNS = [
    "candidate_id",
    "source_map_file",
    "source_row_id",
    "ref",
    "hebrew_phrase",
    "token_index",
    "hebrew_token",
    "clean_hebrew_no_nikud",
    "proposed_translation",
    "proposed_shoresh_or_keyword",
    "proposed_vocabulary_category",
    "first_150_match",
    "first_150_entry_id",
    "evidence_source_id",
    "evidence_source_type",
    "evidence_note",
    "confidence",
    "enrichment_review_status",
    "yossi_decision",
    "yossi_notes",
    "question_allowed",
    "protected_preview_allowed",
    "runtime_allowed",
    "reviewed_bank_allowed",
]

REVIEW_CSV_COLUMNS = [
    "candidate_id",
    "ref",
    "hebrew_phrase",
    "hebrew_token",
    "proposed_values",
    "evidence_source_id",
    "evidence_note",
    "confidence",
    "current_status",
    "what_to_check",
    "recommended_default_decision",
    "yossi_decision",
    "yossi_notes",
    "safety_warning",
]

FOLLOW_UP_CSV_COLUMNS = [
    "candidate_id",
    "type",
    "ref",
    "hebrew",
    "current_decision",
    "current_status",
    "current_evidence",
    "improved_evidence",
    "missing_evidence",
    "remaining_question",
    "canonical_skill_ids",
    "canonical_standard_ids",
    "contract_mapping_notes",
    "recommended_decision",
    "yossi_decision",
    "yossi_notes",
]

TOKEN_SPLIT_REVIEW_CSV_COLUMNS = [
    "candidate_id",
    "parent_candidate_id",
    "ref",
    "hebrew_token",
    "parent_phrase",
    "proposed_zekelman_standard",
    "canonical_skill_id",
    "canonical_standard_anchor",
    "evidence_note",
    "confidence",
    "current_status",
    "recommended_decision",
    "yossi_decision",
    "yossi_notes",
]

ALLOWED_REVIEW_STATUSES = {
    "pending_yossi_enrichment_review",
    "yossi_enrichment_verified",
    "needs_follow_up",
    "blocked_unclear_evidence",
    "source_only",
}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
ALLOWED_YOSSI_DECISIONS = {
    "",
    "verified",
    "fix_morphology",
    "fix_standard",
    "fix_vocabulary",
    "source_only",
    "block_for_questions",
    "needs_follow_up",
}
ALLOWED_TOKEN_SPLIT_RECOMMENDED_DECISIONS = {
    "verified",
    "needs_follow_up",
    "source_only",
    "block_for_questions",
    "fix_standard",
}
SAFETY_WARNING_PHRASES = (
    "not question approval",
    "not protected-preview approval",
    "not reviewed-bank approval",
    "not runtime approval",
    "not student-facing approval",
)
FORBIDDEN_READY_VALUES = {"true", "yes", "approved", "runtime-ready", "question-ready", "student-facing"}
SAFETY_GATES_SUMMARY = (
    "question_allowed:needs_review/"
    "protected_preview_allowed:false/"
    "reviewed_bank_allowed:false/"
    "runtime_allowed:false"
)


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def load_contract() -> dict[str, object]:
    with CONTRACT_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{repo_relative(CONTRACT_PATH)} must be a JSON object")
    return payload


def parse_semicolon_list(raw_value: str) -> list[str]:
    return [item.strip() for item in raw_value.split(";") if item.strip()]


def canonical_contract_skill_ids() -> set[str]:
    contract = load_contract()

    return {
        record["canonical_skill_id"]
        for record in contract.get("canonical_skills", [])
        if isinstance(record, dict) and record.get("canonical_skill_id")
    }


def canonical_contract_standard_ids() -> set[str]:
    contract = load_contract()
    standard_ids: set[str] = set()
    for record in contract.get("canonical_skills", []):
        if isinstance(record, dict):
            standard_ids.update(
                standard_id
                for standard_id in record.get("related_zekelman_standard_ids", [])
                if isinstance(standard_id, str) and standard_id.strip()
            )
    for mapping in contract.get("zekelman_skill_mappings", []):
        if isinstance(mapping, dict):
            standard_id = mapping.get("zekelman_standard_id")
            if isinstance(standard_id, str) and standard_id.strip():
                standard_ids.add(standard_id)
    return standard_ids


def canonical_contract_record_map() -> dict[str, dict[str, object]]:
    contract = load_contract()
    return {
        record["canonical_skill_id"]: record
        for record in contract.get("canonical_skills", [])
        if isinstance(record, dict) and record.get("canonical_skill_id")
    }


def source_rows_by_id(path: Path = SOURCE_MAP_PATH) -> dict[str, dict[str, str]]:
    _, rows = load_tsv(path)
    return {f"row_{index:03d}": row for index, row in enumerate(rows, 1)}


def has_claim(row: dict[str, str], proposed_columns: Iterable[str]) -> bool:
    return any((row.get(column) or "").strip() for column in proposed_columns)


def review_status_counts(rows: list[dict[str, str]]) -> dict[str, int]:
    counts = {
        "yossi_enrichment_verified": 0,
        "needs_follow_up": 0,
        "source_only": 0,
        "blocked_unclear_evidence": 0,
    }
    for row in rows:
        status = row.get("enrichment_review_status", "")
        if status in counts:
            counts[status] += 1
    return counts


def superseded_phrase_level_count(rows: list[dict[str, str]]) -> int:
    return sum(
        1
        for row in rows
        if "superseded by token-split follow-up candidates" in row.get("evidence_note", "").lower()
    )


def validate_required_files(errors: list[str]) -> None:
    required = [
        README_PATH,
        AUDIT_REPORT_PATH,
        MORPHOLOGY_PATH,
        STANDARDS_PATH,
        VOCABULARY_PATH,
        SOURCE_MAP_PATH,
        NEXT_SOURCE_MAP_PATH,
        EXPANSION_SOURCE_MAP_PATH,
        PEREK1_FINAL_SOURCE_MAP_PATH,
        NEXT_MORPHOLOGY_PATH,
        NEXT_STANDARDS_PATH,
        NEXT_VOCABULARY_PATH,
        EXPANSION_MORPHOLOGY_PATH,
        EXPANSION_STANDARDS_PATH,
        EXPANSION_VOCABULARY_PATH,
        PEREK1_FINAL_MORPHOLOGY_PATH,
        PEREK1_FINAL_STANDARDS_PATH,
        PEREK1_FINAL_VOCABULARY_PATH,
    ]
    for md_path, csv_path in REVIEW_SHEETS.values():
        required.extend([md_path, csv_path])
    for md_path, csv_path in NEXT_REVIEW_SHEETS.values():
        required.extend([md_path, csv_path])
    for md_path, csv_path in EXPANSION_REVIEW_SHEETS.values():
        required.extend([md_path, csv_path])
    for md_path, csv_path in PEREK1_FINAL_REVIEW_SHEETS.values():
        required.extend([md_path, csv_path])
    required.extend(APPLIED_REVIEW_REPORTS.values())
    required.extend([FOLLOW_UP_INVENTORY_PATH, FOLLOW_UP_REVIEW_MD_PATH, FOLLOW_UP_REVIEW_CSV_PATH])
    required.extend(
        [
            TOKEN_SPLIT_STANDARDS_PATH,
            TOKEN_SPLIT_AUDIT_PATH,
            TOKEN_SPLIT_REVIEW_MD_PATH,
            TOKEN_SPLIT_REVIEW_CSV_PATH,
            TOKEN_SPLIT_APPLIED_REPORT_PATH,
            NEXT_TOKEN_SPLIT_STANDARDS_PATH,
            EXPANSION_TOKEN_SPLIT_STANDARDS_PATH,
            PEREK1_FINAL_TOKEN_SPLIT_STANDARDS_PATH,
            NEXT_TOKEN_SPLIT_REVIEW_MD_PATH,
            NEXT_TOKEN_SPLIT_REVIEW_CSV_PATH,
            EXPANSION_TOKEN_SPLIT_REVIEW_MD_PATH,
            EXPANSION_TOKEN_SPLIT_REVIEW_CSV_PATH,
            PEREK1_FINAL_TOKEN_SPLIT_REVIEW_MD_PATH,
            PEREK1_FINAL_TOKEN_SPLIT_REVIEW_CSV_PATH,
            NEXT_GENERATION_REPORT_PATH,
            EXPANSION_AUDIT_REPORT_PATH,
            EXPANSION_GENERATION_REPORT_PATH,
            PEREK1_FINAL_AUDIT_REPORT_PATH,
            PEREK1_FINAL_GENERATION_REPORT_PATH,
            PEREK1_FINAL_MORPHOLOGY_APPLIED_REPORT_PATH,
            PEREK1_FINAL_VOCAB_APPLIED_REPORT_PATH,
            PEREK1_FINAL_STANDARDS_APPLIED_REPORT_PATH,
            PEREK1_FINAL_TOKEN_SPLIT_APPLIED_REPORT_PATH,
            PEREK1_FINAL_REVIEW_SUMMARY_PATH,
            PEREK1_COVERAGE_REPORT_PATH,
            EXPANSION_MORPHOLOGY_APPLIED_REPORT_PATH,
            EXPANSION_VOCAB_APPLIED_REPORT_PATH,
            EXPANSION_STANDARDS_APPLIED_REPORT_PATH,
            EXPANSION_TOKEN_SPLIT_APPLIED_REPORT_PATH,
            EXPANSION_SLICE_REVIEW_SUMMARY_PATH,
            EXPANSION_MINI_COMPLETION_REPORT_PATH,
            NEXT_MORPHOLOGY_APPLIED_REPORT_PATH,
            NEXT_VOCAB_APPLIED_REPORT_PATH,
            NEXT_STANDARDS_APPLIED_REPORT_PATH,
            NEXT_TOKEN_SPLIT_APPLIED_REPORT_PATH,
            NEXT_SLICE_REVIEW_SUMMARY_PATH,
            NEXT_MINI_COMPLETION_REPORT_PATH,
            NEXT_FOLLOW_UP_INVENTORY_PATH,
            PILOT_COMPLETION_REPORT_PATH,
            CONTRACT_PATH,
        ]
    )
    for path in required:
        if not path.exists():
            errors.append(f"required enrichment artifact missing: {repo_relative(path)}")


def validate_columns(path: Path, columns: list[str], required_columns: list[str], errors: list[str]) -> None:
    missing = [column for column in required_columns if column not in columns]
    if missing:
        errors.append(f"{repo_relative(path)} missing required columns: {missing}")


def validate_candidate_rows(
    *,
    path: Path,
    rows: list[dict[str, str]],
    source_rows: dict[str, dict[str, str]],
    expected_source_map: str,
    proposed_columns: list[str],
    errors: list[str],
) -> None:
    seen: set[str] = set()
    for row in rows:
        candidate_id = row.get("candidate_id", "")
        context = f"{repo_relative(path)} candidate {candidate_id or '<blank>'}"
        if not candidate_id:
            errors.append(f"{context}: candidate_id is required")
        if candidate_id in seen:
            errors.append(f"{context}: duplicate candidate_id")
        seen.add(candidate_id)

        if row.get("source_map_file") != expected_source_map:
            errors.append(f"{context}: source_map_file must be {expected_source_map}")
        source_row_id = row.get("source_row_id", "")
        source_row = source_rows.get(source_row_id)
        if not source_row:
            errors.append(f"{context}: source_row_id {source_row_id!r} does not link to an existing source map row")
            continue
        if source_row.get("extraction_review_status") != "yossi_extraction_verified":
            errors.append(f"{context}: source row {source_row_id} is not yossi_extraction_verified")
        if row.get("ref") != source_row.get("ref"):
            errors.append(f"{context}: ref does not match linked source row {source_row_id}")
        if row.get("hebrew_phrase") != source_row.get("hebrew_word_or_phrase"):
            errors.append(f"{context}: hebrew_phrase does not match linked source row {source_row_id}")

        status = row.get("enrichment_review_status", "")
        if status not in ALLOWED_REVIEW_STATUSES:
            errors.append(f"{context}: enrichment_review_status {status!r} must be one of {sorted(ALLOWED_REVIEW_STATUSES)}")
        confidence = row.get("confidence", "")
        if confidence not in ALLOWED_CONFIDENCE:
            errors.append(f"{context}: confidence {confidence!r} must be one of {sorted(ALLOWED_CONFIDENCE)}")
        yossi_decision = row.get("yossi_decision", "")
        if yossi_decision not in ALLOWED_YOSSI_DECISIONS:
            errors.append(f"{context}: yossi_decision {yossi_decision!r} is not allowed")
        if status == "yossi_enrichment_verified" and yossi_decision != "verified":
            errors.append(f"{context}: yossi_enrichment_verified rows must have yossi_decision=verified")
        if yossi_decision == "verified" and status != "yossi_enrichment_verified":
            errors.append(f"{context}: yossi_decision=verified must set enrichment_review_status=yossi_enrichment_verified")
        if yossi_decision.startswith("fix_") and status == "yossi_enrichment_verified":
            errors.append(f"{context}: fix decisions must not be marked yossi_enrichment_verified")
        if yossi_decision == "needs_follow_up" and status != "needs_follow_up":
            errors.append(f"{context}: needs_follow_up decisions must keep enrichment_review_status=needs_follow_up")
        if row.get("question_allowed") != "needs_review":
            errors.append(f"{context}: question_allowed must remain needs_review")
        if row.get("protected_preview_allowed") != "false":
            errors.append(f"{context}: protected_preview_allowed must remain false")
        if row.get("runtime_allowed") != "false":
            errors.append(f"{context}: runtime_allowed must remain false")
        if row.get("reviewed_bank_allowed") != "false":
            errors.append(f"{context}: reviewed_bank_allowed must remain false")
        if status == "yossi_enrichment_verified" and not row.get("yossi_notes", "").strip():
            errors.append(f"{context}: verified enrichment candidates must include yossi_notes")

        for field_name, value in row.items():
            normalized_value = str(value).strip().lower()
            if field_name in {"question_allowed", "protected_preview_allowed", "runtime_allowed", "reviewed_bank_allowed"}:
                continue
            if field_name == "first_150_match":
                continue
            if field_name == "evidence_note" and "not question approval" in normalized_value:
                continue
            if field_name == "student_facing" and normalized_value in {"true", "yes", "approved"}:
                errors.append(f"{context}: student_facing must not be enabled")
            if normalized_value in {"runtime-ready", "question-ready", "student-facing"}:
                errors.append(f"{context}: contains forbidden readiness value {normalized_value!r}")

        if has_claim(row, proposed_columns) and not row.get("evidence_note", "").strip():
            errors.append(f"{context}: proposes enrichment fields but has no evidence_note")
        if has_claim(row, proposed_columns) and not row.get("evidence_source_id", "").strip():
            errors.append(f"{context}: proposes enrichment fields but has no evidence_source_id")
        if "koren" in row.get("evidence_source_id", "").lower() and "secondary" not in row.get("evidence_note", "").lower():
            errors.append(f"{context}: Koren evidence must be described as secondary noncommercial support")
        if "reviewed_bank" in row.get("evidence_source_id", "").lower() and "reference only" not in row.get("evidence_note", "").lower():
            errors.append(f"{context}: reviewed-bank evidence must be reference only")
        if row.get("first_150_match") == "true" and row.get("question_allowed") != "needs_review":
            errors.append(f"{context}: First 150 evidence cannot open question_allowed")
        if row.get("first_150_match") == "true":
            if not row.get("first_150_entry_id", "").strip():
                errors.append(f"{context}: First 150 claims must include first_150_entry_id")
            if not row.get("evidence_source_id", "").strip() or not row.get("evidence_note", "").strip():
                errors.append(f"{context}: First 150 claims must include evidence_source_id and evidence_note")


def validate_review_sheets(errors: list[str]) -> None:
    for label, (md_path, csv_path) in REVIEW_SHEETS.items():
        if not md_path.exists() or not csv_path.exists():
            continue
        text = md_path.read_text(encoding="utf-8")
        for phrase in SAFETY_WARNING_PHRASES:
            if phrase not in text:
                errors.append(f"{repo_relative(md_path)} missing safety warning phrase: {phrase!r}")
        for decision in ALLOWED_YOSSI_DECISIONS - {""}:
            if f"`{decision}`" not in text:
                errors.append(f"{repo_relative(md_path)} missing allowed decision: {decision}")
        if not csv_path.read_bytes().startswith(b"\xef\xbb\xbf"):
            errors.append(f"{repo_relative(csv_path)} must be UTF-8-BOM encoded for Hebrew spreadsheet review")
        columns, rows = load_csv(csv_path)
        validate_columns(csv_path, columns, REVIEW_CSV_COLUMNS, errors)
        if not rows:
            errors.append(f"{repo_relative(csv_path)} must contain review rows")
        for row in rows:
            context = f"{repo_relative(csv_path)} candidate {row.get('candidate_id', '<blank>')}"
            if row.get("yossi_decision", "") != "":
                errors.append(f"{context}: yossi_decision must be blank by default")
            if row.get("yossi_notes", "") != "":
                errors.append(f"{context}: yossi_notes must be blank by default")
            warning = row.get("safety_warning", "").lower()
            for phrase in ("not question", "not runtime", "not student-facing"):
                if phrase not in warning:
                    errors.append(f"{context}: safety_warning must include {phrase!r}")
            if label == "vocabulary_shoresh" and "First 150" not in text:
                errors.append(f"{repo_relative(md_path)} must document First 150 evidence as candidate evidence only")


def candidate_is_unresolved(row: dict[str, str]) -> bool:
    return (
        row.get("enrichment_review_status") != "yossi_enrichment_verified"
        or row.get("yossi_decision", "").startswith("fix_")
    )


def follow_up_contract_labels(candidate_type: str, row: dict[str, str]) -> list[str]:
    if candidate_type == "standards":
        return [row.get("proposed_skill_id", "").strip()]
    if candidate_type == "morphology":
        return [
            row.get("proposed_part_of_speech", "").strip(),
            row.get("proposed_dikduk_feature", "").strip(),
        ]
    if candidate_type == "vocabulary_shoresh":
        return [row.get("proposed_vocabulary_category", "").strip()]
    return []


def validate_follow_up_artifacts(
    *,
    morphology_rows: list[dict[str, str]],
    standards_rows: list[dict[str, str]],
    vocabulary_rows: list[dict[str, str]],
    errors: list[str],
) -> None:
    if not FOLLOW_UP_INVENTORY_PATH.exists() or not FOLLOW_UP_REVIEW_MD_PATH.exists() or not FOLLOW_UP_REVIEW_CSV_PATH.exists():
        return

    all_rows = morphology_rows + standards_rows + vocabulary_rows
    unresolved = {row["candidate_id"]: row for row in all_rows if candidate_is_unresolved(row)}
    verified = {row["candidate_id"] for row in all_rows if row["enrichment_review_status"] == "yossi_enrichment_verified"}

    inventory_text = FOLLOW_UP_INVENTORY_PATH.read_text(encoding="utf-8")
    md_text = FOLLOW_UP_REVIEW_MD_PATH.read_text(encoding="utf-8")
    contract = load_contract()
    canonical_records = {
        record["canonical_skill_id"]: record
        for record in contract.get("canonical_skills", [])
        if isinstance(record, dict) and record.get("canonical_skill_id")
    }
    known_standard_ids = {
        standard_id
        for record in canonical_records.values()
        for standard_id in record.get("related_zekelman_standard_ids", [])
        if isinstance(standard_id, str) and standard_id.strip()
    }

    for phrase in (
        "This inventory lists exactly the unresolved candidates",
        "Already verified candidates are not repeated",
        "Data hygiene audit",
        "data/standards/canonical_skill_contract.json",
    ):
        if phrase not in inventory_text:
            errors.append(f"{repo_relative(FOLLOW_UP_INVENTORY_PATH)} missing inventory phrase: {phrase!r}")

    safety_phrase = (
        "This is enrichment follow-up review only. It is not question approval, protected-preview approval, "
        "reviewed-bank approval, runtime approval, or student-facing approval."
    )
    if safety_phrase not in md_text:
        errors.append(f"{repo_relative(FOLLOW_UP_REVIEW_MD_PATH)} missing follow-up safety warning")
    if "data/standards/canonical_skill_contract.json" not in md_text:
        errors.append(f"{repo_relative(FOLLOW_UP_REVIEW_MD_PATH)} must cite the canonical skill contract")
    for heading in ("Vocabulary/Shoresh Follow-Up", "Morphology Follow-Up", "Standards Follow-Up"):
        if heading not in md_text:
            errors.append(f"{repo_relative(FOLLOW_UP_REVIEW_MD_PATH)} missing section heading: {heading}")
    for decision in (
        "verified",
        "needs_follow_up",
        "source_only",
        "block_for_questions",
        "fix_morphology",
        "fix_standard",
        "fix_vocabulary",
    ):
        if f"`{decision}`" not in md_text:
            errors.append(f"{repo_relative(FOLLOW_UP_REVIEW_MD_PATH)} missing allowed decision: {decision}")

    if not FOLLOW_UP_REVIEW_CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf"):
        errors.append(f"{repo_relative(FOLLOW_UP_REVIEW_CSV_PATH)} must be UTF-8-BOM encoded")
    columns, csv_rows = load_csv(FOLLOW_UP_REVIEW_CSV_PATH)
    validate_columns(FOLLOW_UP_REVIEW_CSV_PATH, columns, FOLLOW_UP_CSV_COLUMNS, errors)
    csv_ids = {row.get("candidate_id", "") for row in csv_rows}

    if csv_ids != set(unresolved):
        missing = sorted(set(unresolved) - csv_ids)
        extra = sorted(csv_ids - set(unresolved))
        errors.append(
            f"{repo_relative(FOLLOW_UP_REVIEW_CSV_PATH)} must list exactly unresolved candidates; "
            f"missing={missing}, extra={extra}"
        )
    for candidate_id in unresolved:
        if candidate_id not in inventory_text:
            errors.append(f"{repo_relative(FOLLOW_UP_INVENTORY_PATH)} missing unresolved candidate {candidate_id}")
        if candidate_id not in md_text:
            errors.append(f"{repo_relative(FOLLOW_UP_REVIEW_MD_PATH)} missing unresolved candidate {candidate_id}")
    for candidate_id in verified:
        if f"### `{candidate_id}`" in inventory_text or f"### `{candidate_id}`" in md_text:
            errors.append(f"{candidate_id} is already verified and must not appear as a follow-up review row")

    for row in csv_rows:
        context = f"{repo_relative(FOLLOW_UP_REVIEW_CSV_PATH)} candidate {row.get('candidate_id', '<blank>')}"
        source_row = unresolved.get(row.get("candidate_id", ""))
        if row.get("yossi_decision", "") != "":
            errors.append(f"{context}: yossi_decision must be blank for follow-up review")
        if row.get("yossi_notes", "") != "":
            errors.append(f"{context}: yossi_notes must be blank for follow-up review")
        if row.get("recommended_decision") not in {
            "verified",
            "needs_follow_up",
            "source_only",
            "block_for_questions",
            "fix_morphology",
            "fix_standard",
            "fix_vocabulary",
        }:
            errors.append(f"{context}: recommended_decision is not allowed")
        if row.get("recommended_decision") == "verified":
            errors.append(f"{context}: unresolved follow-up rows must not recommend verified automatically")
        canonical_skill_ids = parse_semicolon_list(row.get("canonical_skill_ids", ""))
        canonical_standard_ids = parse_semicolon_list(row.get("canonical_standard_ids", ""))
        if not canonical_skill_ids:
            errors.append(f"{context}: canonical_skill_ids must be populated")
            continue
        if not canonical_standard_ids:
            errors.append(f"{context}: canonical_standard_ids must be populated")
        if not row.get("contract_mapping_notes", "").strip():
            errors.append(f"{context}: contract_mapping_notes must be populated")
        listed_records = []
        for canonical_skill_id in canonical_skill_ids:
            record = canonical_records.get(canonical_skill_id)
            if record is None:
                errors.append(f"{context}: unknown canonical_skill_id {canonical_skill_id!r}")
                continue
            listed_records.append(record)
        for standard_id in canonical_standard_ids:
            if standard_id not in known_standard_ids:
                errors.append(f"{context}: unknown canonical standard id {standard_id!r}")
        if source_row is None:
            errors.append(f"{context}: candidate must correspond to an unresolved enrichment row")
            continue
        mapped_labels = {
            label
            for record in listed_records
            for label in record.get("enrichment_labels_allowed", [])
            if isinstance(label, str) and label.strip()
        }
        for label in follow_up_contract_labels(row.get("type", ""), source_row):
            if label and label not in mapped_labels:
                errors.append(f"{context}: proposed label {label!r} is not mapped by listed canonical_skill_ids")
        proposed_standard = source_row.get("proposed_zekelman_standard", "").strip()
        if proposed_standard and proposed_standard != "needs_mapping_review" and proposed_standard not in canonical_standard_ids:
            errors.append(f"{context}: canonical_standard_ids must include proposed standard {proposed_standard!r}")
        for standard_id in canonical_standard_ids:
            if listed_records and not any(standard_id in record.get("related_zekelman_standard_ids", []) for record in listed_records):
                errors.append(f"{context}: standard {standard_id!r} is not supported by listed canonical_skill_ids")

    standards_by_id = {row["candidate_id"]: row for row in standards_rows}
    for candidate_id in ("std_b1_1_r002", "std_b1_1_r003", "std_b1_3_r013", "std_b1_5_r020"):
        note = standards_by_id.get(candidate_id, {}).get("evidence_note", "").lower()
        if "token-level" not in note or not any(marker in note for marker in ("split", "separate")):
            errors.append(f"{candidate_id}: phrase-level standards follow-up must be flagged for token-level split")


def validate_token_split_standards_artifacts(
    *,
    standards_rows: list[dict[str, str]],
    errors: list[str],
) -> list[dict[str, str]]:
    columns, rows = load_tsv(TOKEN_SPLIT_STANDARDS_PATH)
    validate_columns(TOKEN_SPLIT_STANDARDS_PATH, columns, TOKEN_SPLIT_STANDARDS_COLUMNS, errors)
    parent_rows = {row["candidate_id"]: row for row in standards_rows}
    canonical_skills = canonical_contract_skill_ids()
    canonical_records = canonical_contract_record_map()
    canonical_standards = canonical_contract_standard_ids()
    seen_ids: set[str] = set()
    expected_source_map = repo_relative(SOURCE_MAP_PATH)

    for row in rows:
        context = f"{repo_relative(TOKEN_SPLIT_STANDARDS_PATH)} candidate {row.get('candidate_id', '<blank>')}"
        candidate_id = row.get("candidate_id", "").strip()
        if not candidate_id:
            errors.append(f"{context}: candidate_id must be populated")
        elif candidate_id in seen_ids:
            errors.append(f"{context}: duplicate candidate_id")
        else:
            seen_ids.add(candidate_id)

        parent_candidate_id = row.get("parent_candidate_id", "").strip()
        if parent_candidate_id not in parent_rows:
            errors.append(f"{context}: parent_candidate_id must reference an existing phrase-level standards candidate")
        else:
            parent_row = parent_rows[parent_candidate_id]
            if parent_row.get("enrichment_review_status") == "yossi_enrichment_verified":
                errors.append(f"{context}: parent bundled row must remain unresolved")

        if row.get("source_map_file") != expected_source_map:
            errors.append(f"{context}: source_map_file must match the Bereishis 1:1-1:5 proof map")
        if not row.get("source_row_id", "").strip():
            errors.append(f"{context}: source_row_id must be populated")
        if not row.get("ref", "").strip():
            errors.append(f"{context}: ref must be populated")
        if not row.get("hebrew_phrase", "").strip():
            errors.append(f"{context}: hebrew_phrase must be populated")
        if not row.get("hebrew_token", "").strip():
            errors.append(f"{context}: hebrew_token must be populated")
        elif "?" in row.get("hebrew_token", ""):
            errors.append(f"{context}: hebrew_token must contain real Hebrew, not placeholder question marks")
        if not row.get("clean_hebrew_no_nikud", "").strip():
            errors.append(f"{context}: clean_hebrew_no_nikud must be populated")
        elif "?" in row.get("clean_hebrew_no_nikud", ""):
            errors.append(f"{context}: clean_hebrew_no_nikud must contain real Hebrew, not placeholder question marks")
        try:
            if int(row.get("token_index", "0")) <= 0:
                errors.append(f"{context}: token_index must be a positive integer")
        except ValueError:
            errors.append(f"{context}: token_index must be a positive integer")

        canonical_skill_id = row.get("canonical_skill_id", "").strip()
        if canonical_skill_id not in canonical_skills:
            errors.append(f"{context}: unknown canonical_skill_id {canonical_skill_id!r}")
        canonical_standard_anchor = row.get("canonical_standard_anchor", "").strip()
        if canonical_standard_anchor != "needs_mapping_review" and canonical_standard_anchor not in canonical_standards:
            errors.append(f"{context}: canonical_standard_anchor must map through the canonical contract or use needs_mapping_review")
        proposed_standard = row.get("proposed_zekelman_standard", "").strip()
        if proposed_standard != "needs_mapping_review" and proposed_standard not in canonical_standards:
            errors.append(f"{context}: proposed_zekelman_standard must map through the canonical contract or use needs_mapping_review")
        if (
            proposed_standard
            and canonical_standard_anchor
            and proposed_standard != "needs_mapping_review"
            and canonical_standard_anchor != "needs_mapping_review"
            and proposed_standard != canonical_standard_anchor
        ):
            errors.append(f"{context}: canonical_standard_anchor must match proposed_zekelman_standard when both are mapped")
        record = canonical_records.get(canonical_skill_id)
        if (
            record is not None
            and canonical_standard_anchor != "needs_mapping_review"
            and canonical_standard_anchor not in record.get("related_zekelman_standard_ids", [])
        ):
            errors.append(f"{context}: canonical_standard_anchor is not supported by canonical_skill_id")

        if not row.get("proposed_skill_id", "").strip():
            errors.append(f"{context}: proposed_skill_id must be populated")
        if not row.get("proposed_standard_level", "").strip():
            errors.append(f"{context}: proposed_standard_level must be populated")
        if not row.get("evidence_source_id", "").strip():
            errors.append(f"{context}: evidence_source_id must be populated")
        if not row.get("evidence_source_type", "").strip():
            errors.append(f"{context}: evidence_source_type must be populated")
        if not row.get("evidence_note", "").strip():
            errors.append(f"{context}: evidence_note must be populated")
        if row.get("confidence") not in ALLOWED_CONFIDENCE:
            errors.append(f"{context}: confidence must be one of {sorted(ALLOWED_CONFIDENCE)}")
        yossi_decision = row.get("yossi_decision", "")
        status = row.get("enrichment_review_status", "")
        if yossi_decision not in ALLOWED_TOKEN_SPLIT_RECOMMENDED_DECISIONS:
            errors.append(f"{context}: yossi_decision must be one of {sorted(ALLOWED_TOKEN_SPLIT_RECOMMENDED_DECISIONS)}")
        expected_status = {
            "verified": "yossi_enrichment_verified",
            "needs_follow_up": "needs_follow_up",
            "source_only": "source_only",
            "block_for_questions": "blocked_unclear_evidence",
            "fix_standard": "needs_follow_up",
        }.get(yossi_decision)
        if expected_status is None:
            errors.append(f"{context}: yossi_decision could not be mapped to an enrichment_review_status")
        elif status != expected_status:
            errors.append(f"{context}: enrichment_review_status must match yossi_decision={yossi_decision!r}")
        if not row.get("yossi_notes", "").strip():
            errors.append(f"{context}: yossi_notes must be populated after Yossi review")
        if row.get("question_allowed") != "needs_review":
            errors.append(f"{context}: question_allowed must remain needs_review")
        if row.get("protected_preview_allowed") != "false":
            errors.append(f"{context}: protected_preview_allowed must remain false")
        if row.get("reviewed_bank_allowed") != "false":
            errors.append(f"{context}: reviewed_bank_allowed must remain false")
        if row.get("runtime_allowed") != "false":
            errors.append(f"{context}: runtime_allowed must remain false")

    if not TOKEN_SPLIT_REVIEW_MD_PATH.exists():
        errors.append(f"required enrichment artifact missing: {repo_relative(TOKEN_SPLIT_REVIEW_MD_PATH)}")
    else:
        md_text = TOKEN_SPLIT_REVIEW_MD_PATH.read_text(encoding="utf-8")
        safety_phrase = (
            "This is standards enrichment follow-up only. It is not question approval, protected-preview approval, "
            "reviewed-bank approval, runtime approval, or student-facing approval."
        )
        if safety_phrase not in md_text:
            errors.append(f"{repo_relative(TOKEN_SPLIT_REVIEW_MD_PATH)} missing token-split safety warning")
        if "???" in md_text:
            errors.append(f"{repo_relative(TOKEN_SPLIT_REVIEW_MD_PATH)} must render real Hebrew rather than question-mark placeholders")
        for decision in ALLOWED_TOKEN_SPLIT_RECOMMENDED_DECISIONS:
            if f"`{decision}`" not in md_text:
                errors.append(f"{repo_relative(TOKEN_SPLIT_REVIEW_MD_PATH)} missing allowed decision: {decision}")

    if not TOKEN_SPLIT_REVIEW_CSV_PATH.exists():
        errors.append(f"required enrichment artifact missing: {repo_relative(TOKEN_SPLIT_REVIEW_CSV_PATH)}")
    else:
        if not TOKEN_SPLIT_REVIEW_CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf"):
            errors.append(f"{repo_relative(TOKEN_SPLIT_REVIEW_CSV_PATH)} must be UTF-8-BOM encoded")
        csv_columns, csv_rows = load_csv(TOKEN_SPLIT_REVIEW_CSV_PATH)
        validate_columns(TOKEN_SPLIT_REVIEW_CSV_PATH, csv_columns, TOKEN_SPLIT_REVIEW_CSV_COLUMNS, errors)
        candidate_ids = {row["candidate_id"] for row in rows}
        csv_ids = {row.get("candidate_id", "") for row in csv_rows}
        if csv_ids != candidate_ids:
            missing = sorted(candidate_ids - csv_ids)
            extra = sorted(csv_ids - candidate_ids)
            errors.append(
                f"{repo_relative(TOKEN_SPLIT_REVIEW_CSV_PATH)} must list exactly the token-split standards candidates; "
                f"missing={missing}, extra={extra}"
            )
        token_rows_by_id = {row["candidate_id"]: row for row in rows}
        for row in csv_rows:
            context = f"{repo_relative(TOKEN_SPLIT_REVIEW_CSV_PATH)} candidate {row.get('candidate_id', '<blank>')}"
            if "?" in row.get("hebrew_token", ""):
                errors.append(f"{context}: hebrew_token must contain real Hebrew, not placeholder question marks")
            if row.get("recommended_decision") not in ALLOWED_TOKEN_SPLIT_RECOMMENDED_DECISIONS:
                errors.append(f"{context}: recommended_decision is not allowed")
            token_row = token_rows_by_id.get(row.get("candidate_id", ""))
            if token_row is None:
                continue
            if row.get("current_status") != token_row.get("enrichment_review_status"):
                errors.append(f"{context}: current_status must match the token-split TSV")
            if row.get("yossi_decision") != token_row.get("yossi_decision"):
                errors.append(f"{context}: yossi_decision must match the token-split TSV")
            if row.get("yossi_notes") != token_row.get("yossi_notes"):
                errors.append(f"{context}: yossi_notes must match the token-split TSV")
            if row.get("canonical_skill_id") != token_row.get("canonical_skill_id"):
                errors.append(f"{context}: canonical_skill_id must match the token-split TSV")
            if row.get("canonical_standard_anchor") != token_row.get("canonical_standard_anchor"):
                errors.append(f"{context}: canonical_standard_anchor must match the token-split TSV")

    applied_text = TOKEN_SPLIT_APPLIED_REPORT_PATH.read_text(encoding="utf-8")
    for phrase in (
        "total token-split candidates reviewed: 10",
        "verified candidates: 7",
        "needs_follow_up candidates: 3",
        "parent bundled rows preserved unresolved",
        "Hebrew rendering check result",
        "safety gates confirmed closed",
        "not question approval",
        "not protected-preview approval",
        "not reviewed-bank approval",
        "not runtime approval",
        "not student-facing approval",
    ):
        if phrase not in applied_text:
            errors.append(f"{repo_relative(TOKEN_SPLIT_APPLIED_REPORT_PATH)} missing applied-review phrase: {phrase!r}")

    if not TOKEN_SPLIT_AUDIT_PATH.exists():
        errors.append(f"required enrichment artifact missing: {repo_relative(TOKEN_SPLIT_AUDIT_PATH)}")
    return rows


def validate_reports(errors: list[str]) -> None:
    if README_PATH.exists():
        text = README_PATH.read_text(encoding="utf-8")
        for phrase in (
            "Question eligibility",
            "Separate later gate",
            "Koren remains secondary noncommercial support only",
            "No enrichment candidate may claim question-ready",
            "Pilot Review Status",
            "Token-Split Standards Cleanup",
            "Pilot Completion Milestone",
            "reports/bereishis_1_1_to_1_5_enrichment_pilot_completion_report.md",
            "pilot is completed as a pattern, not fully resolved",
            "no question/protected-preview/reviewed-bank/runtime approval exists",
            "Bereishis 1:6-1:13 Review-Applied Slice",
            "enrichment review only",
            "all gates remain closed",
            "bereishis_1_6_to_1_13_morphology_candidates.tsv",
            "bereishis_1_6_to_1_13_vocabulary_shoresh_candidates.tsv",
            "bereishis_1_6_to_1_13_standards_candidates.tsv",
            "bereishis_1_6_to_1_13_token_split_standards_candidates.tsv",
            "bereishis_1_6_to_1_13_enrichment_candidate_generation_report.md",
            "bereishis_1_6_to_1_13_morphology_enrichment_yossi_review_applied.md",
            "bereishis_1_6_to_1_13_vocabulary_shoresh_enrichment_yossi_review_applied.md",
            "bereishis_1_6_to_1_13_standards_enrichment_yossi_review_applied.md",
            "bereishis_1_6_to_1_13_token_split_standards_yossi_review_applied.md",
            "bereishis_1_6_to_1_13_enrichment_review_summary.md",
            "bereishis_1_6_to_1_13_enrichment_mini_completion_report.md",
            "verified: 14",
            "needs_follow_up: 18",
            "Unresolved items remain follow-up by design",
            "next recommended slice is Bereishis 1:14-1:23",
            "Bereishis 1:14-1:23 Review-Applied Slice",
            "morphology: 25",
            "vocabulary_shoresh: 21",
            "phrase-level standards: 13",
            "token-split standards: 45",
            "total candidates: 104",
            "verified: 53",
            "needs_follow_up: 51",
            "bereishis_1_14_to_1_23_morphology_candidates.tsv",
            "bereishis_1_14_to_1_23_vocabulary_shoresh_candidates.tsv",
            "bereishis_1_14_to_1_23_standards_candidates.tsv",
            "bereishis_1_14_to_1_23_token_split_standards_candidates.tsv",
            "bereishis_1_14_to_1_23_enrichment_candidate_audit.md",
            "bereishis_1_14_to_1_23_enrichment_candidate_generation_report.md",
            "bereishis_1_14_to_1_23_morphology_enrichment_yossi_review_applied.md",
            "bereishis_1_14_to_1_23_vocabulary_shoresh_enrichment_yossi_review_applied.md",
            "bereishis_1_14_to_1_23_standards_enrichment_yossi_review_applied.md",
            "bereishis_1_14_to_1_23_token_split_standards_yossi_review_applied.md",
            "bereishis_1_14_to_1_23_enrichment_review_summary.md",
            "bereishis_1_14_to_1_23_enrichment_mini_completion_report.md",
            "Unresolved items remain follow-up by design and all gates remain closed across the slice.",
            "Next recommended slice: Bereishis 1:24-1:31",
            "Bereishis 1:24-1:31 Review-Applied Slice",
            "morphology: 26",
            "vocabulary_shoresh: 40",
            "phrase-level standards: 14",
            "token-split standards: 56",
            "total candidates: 136",
            "verified: 83",
            "needs_follow_up: 53",
            "bereishis_1_24_to_1_31_morphology_candidates.tsv",
            "bereishis_1_24_to_1_31_vocabulary_shoresh_candidates.tsv",
            "bereishis_1_24_to_1_31_standards_candidates.tsv",
            "bereishis_1_24_to_1_31_token_split_standards_candidates.tsv",
            "bereishis_1_24_to_1_31_morphology_enrichment_yossi_review_applied.md",
            "bereishis_1_24_to_1_31_vocabulary_shoresh_enrichment_yossi_review_applied.md",
            "bereishis_1_24_to_1_31_standards_enrichment_yossi_review_applied.md",
            "bereishis_1_24_to_1_31_token_split_standards_yossi_review_applied.md",
            "bereishis_1_24_to_1_31_enrichment_review_summary.md",
            "Bereishis Perek 1 Enrichment Review-Application Coverage",
            "reports/bereishis_perek_1_enrichment_review_application_coverage_report.md",
            "coverage exists across Bereishis 1:1-1:31",
            "unresolved items remain follow-up by design",
        ):
            if phrase not in text:
                errors.append(f"{repo_relative(README_PATH)} missing required enrichment policy phrase: {phrase!r}")
    if AUDIT_REPORT_PATH.exists():
        text = AUDIT_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in (
            "reviewed-bank examples; reference only",
            "Koren as primary",
            "Do not backfill all morphology fields",
            "What Should Not Be Auto-Filled",
        ):
            if phrase not in text:
                errors.append(f"{repo_relative(AUDIT_REPORT_PATH)} missing audit finding phrase: {phrase!r}")
    for path in APPLIED_REVIEW_REPORTS.values():
        if path.exists():
            text = path.read_text(encoding="utf-8")
            for phrase in SAFETY_WARNING_PHRASES:
                if phrase not in text:
                    errors.append(f"{repo_relative(path)} missing applied-review safety warning phrase: {phrase!r}")
            if "No source-to-skill map rows were changed" not in text:
                errors.append(f"{repo_relative(path)} must confirm source-to-skill maps were not changed")


def validate_pilot_completion_report(
    *,
    morphology_rows: list[dict[str, str]],
    standards_rows: list[dict[str, str]],
    vocabulary_rows: list[dict[str, str]],
    token_split_rows: list[dict[str, str]],
    errors: list[str],
) -> None:
    if not PILOT_COMPLETION_REPORT_PATH.exists():
        return

    text = PILOT_COMPLETION_REPORT_PATH.read_text(encoding="utf-8")
    for phrase in (
        "Bereishis 1:1-1:5 now has a reviewed enrichment pilot pattern across morphology, vocabulary/shoresh, and standards.",
        "source-to-skill maps remain phrase-level extraction truth",
        "enrichment lives in separate candidate layers",
        "token-level morphology and standards are handled outside the source-to-skill maps",
        "canonical skill contract anchors standards and skill IDs",
        "question eligibility remains a later gate",
        "Hebrew corruption was detected in the token-split TSV/CSV",
        "source artifacts were corrected to real UTF-8 Hebrew",
        "validation now checks real Hebrew rendering",
        "question generation remains blocked",
        "protected preview remains blocked",
        "reviewed bank remains blocked",
        "runtime remains blocked",
        "student-facing use remains blocked",
        "generate candidate rows only from verified source-to-skill rows",
        "map skill/standard IDs through canonical contract",
        "use token-level splits for standards where phrase-level row is too broad",
        "apply only reviewed decisions",
        "leave uncertain items follow-up",
        "Bereishis 1:6-1:13",
        "data/standards/canonical_skill_contract.json",
    ):
        if phrase not in text:
            errors.append(f"{repo_relative(PILOT_COMPLETION_REPORT_PATH)} missing required phrase: {phrase!r}")

    morphology_counts = review_status_counts(morphology_rows)
    vocabulary_counts = review_status_counts(vocabulary_rows)
    standards_counts = review_status_counts(standards_rows)
    token_split_counts = review_status_counts(token_split_rows)
    expected_lines = (
        (
            "morphology",
            f"- morphology: total={len(morphology_rows)}; verified={morphology_counts['yossi_enrichment_verified']}; "
            f"needs_follow_up={morphology_counts['needs_follow_up']}; source_only={morphology_counts['source_only']}; "
            f"blocked={morphology_counts['blocked_unclear_evidence']}; safety_gates={SAFETY_GATES_SUMMARY}"
        ),
        (
            "vocabulary/shoresh",
            f"- vocabulary_shoresh: total={len(vocabulary_rows)}; verified={vocabulary_counts['yossi_enrichment_verified']}; "
            f"needs_follow_up={vocabulary_counts['needs_follow_up']}; source_only={vocabulary_counts['source_only']}; "
            f"blocked={vocabulary_counts['blocked_unclear_evidence']}; safety_gates={SAFETY_GATES_SUMMARY}"
        ),
        (
            "phrase-level standards",
            f"- phrase_level_standards: total={len(standards_rows)}; verified={standards_counts['yossi_enrichment_verified']}; "
            f"needs_follow_up={standards_counts['needs_follow_up']}; superseded_unresolved={superseded_phrase_level_count(standards_rows)}; "
            f"safety_gates={SAFETY_GATES_SUMMARY}"
        ),
        (
            "token-split standards",
            f"- token_split_standards: total={len(token_split_rows)}; verified={token_split_counts['yossi_enrichment_verified']}; "
            f"needs_follow_up={token_split_counts['needs_follow_up']}; source_only={token_split_counts['source_only']}; "
            f"blocked={token_split_counts['blocked_unclear_evidence']}; safety_gates={SAFETY_GATES_SUMMARY}"
        ),
    )
    for label, line in expected_lines:
        if line not in text:
            errors.append(f"{repo_relative(PILOT_COMPLETION_REPORT_PATH)} missing or stale {label} count line")

    for phrase in (
        "וחשך",
        "יהי",
        "שמים",
        "prefixed ל",
        "std_b1_1_r002",
        "std_b1_1_r003",
        "std_b1_3_r013",
        "std_b1_5_r020",
        "std_b1_2_r010",
    ):
        if phrase not in text:
            errors.append(f"{repo_relative(PILOT_COMPLETION_REPORT_PATH)} missing follow-up item {phrase!r}")


def validate_source_map_readiness(path: Path, errors: list[str]) -> None:
    _, rows = load_tsv(path)
    for index, row in enumerate(rows, 1):
        context = f"{repo_relative(path)} row_{index:03d}"
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


def validate_pending_review_sheet_bundle(
    *,
    label: str,
    rows: list[dict[str, str]],
    md_path: Path,
    csv_path: Path,
    errors: list[str],
) -> None:
    text = md_path.read_text(encoding="utf-8")
    if "Yossi is reviewing enrichment candidates only." not in text:
        errors.append(f"{repo_relative(md_path)} must say Yossi is reviewing enrichment candidates only")
    if SAFETY_WARNING_PHRASES[0] not in text or "This is enrichment review only." not in text:
        errors.append(f"{repo_relative(md_path)} missing enrichment review safety warning")
    for decision in ALLOWED_YOSSI_DECISIONS - {""}:
        if f"`{decision}`" not in text:
            errors.append(f"{repo_relative(md_path)} missing allowed decision: {decision}")

    if not csv_path.read_bytes().startswith(b"\xef\xbb\xbf"):
        errors.append(f"{repo_relative(csv_path)} must be UTF-8-BOM encoded")
    columns, csv_rows = load_csv(csv_path)
    validate_columns(csv_path, columns, REVIEW_CSV_COLUMNS, errors)
    candidate_ids = {row["candidate_id"] for row in rows}
    csv_ids = {row.get("candidate_id", "") for row in csv_rows}
    if csv_ids != candidate_ids:
        missing = sorted(candidate_ids - csv_ids)
        extra = sorted(csv_ids - candidate_ids)
        errors.append(
            f"{repo_relative(csv_path)} must list exactly the pending review candidates; missing={missing}, extra={extra}"
        )
    rows_by_id = {row["candidate_id"]: row for row in rows}
    for row in csv_rows:
        context = f"{repo_relative(csv_path)} candidate {row.get('candidate_id', '<blank>')}"
        if row.get("recommended_default_decision") not in ALLOWED_YOSSI_DECISIONS - {""}:
            errors.append(f"{context}: recommended_default_decision is not allowed")
        token = row.get("hebrew_token", "")
        if token and "?" in token:
            errors.append(f"{context}: hebrew_token must render real Hebrew, not placeholder question marks")
        warning = row.get("safety_warning", "").lower()
        for phrase in ("question approval", "runtime approval", "student-facing approval"):
            if phrase not in warning:
                errors.append(f"{context}: safety_warning must include {phrase!r}")
        source_row = rows_by_id.get(row.get("candidate_id", ""))
        if source_row is None:
            continue
        if row.get("ref") != source_row.get("ref"):
            errors.append(f"{context}: ref must match the candidate TSV")
        if row.get("hebrew_phrase") != source_row.get("hebrew_phrase"):
            errors.append(f"{context}: hebrew_phrase must match the candidate TSV")
        if row.get("hebrew_token", "") != source_row.get("hebrew_token", ""):
            errors.append(f"{context}: hebrew_token must match the candidate TSV")
        if not row.get("proposed_values", "").strip():
            errors.append(f"{context}: proposed_values must be populated")


def validate_next_slice_token_split_artifacts(
    *,
    standards_rows: list[dict[str, str]],
    source_rows: dict[str, dict[str, str]],
    errors: list[str],
) -> list[dict[str, str]]:
    columns, rows = load_tsv(NEXT_TOKEN_SPLIT_STANDARDS_PATH)
    validate_columns(NEXT_TOKEN_SPLIT_STANDARDS_PATH, columns, TOKEN_SPLIT_STANDARDS_COLUMNS, errors)
    expected_source_map = repo_relative(NEXT_SOURCE_MAP_PATH)
    canonical_skills = canonical_contract_skill_ids()
    canonical_records = canonical_contract_record_map()
    canonical_standards = canonical_contract_standard_ids()
    parent_rows = {row["candidate_id"]: row for row in standards_rows}
    seen_ids: set[str] = set()

    for row in rows:
        context = f"{repo_relative(NEXT_TOKEN_SPLIT_STANDARDS_PATH)} candidate {row.get('candidate_id', '<blank>')}"
        candidate_id = row.get("candidate_id", "").strip()
        if not candidate_id:
            errors.append(f"{context}: candidate_id must be populated")
        elif candidate_id in seen_ids:
            errors.append(f"{context}: duplicate candidate_id")
        else:
            seen_ids.add(candidate_id)
        parent_candidate_id = row.get("parent_candidate_id", "").strip()
        if parent_candidate_id not in parent_rows:
            errors.append(f"{context}: parent_candidate_id must reference an existing next-slice phrase-level standards candidate")
        if row.get("source_map_file") != expected_source_map:
            errors.append(f"{context}: source_map_file must match the Bereishis 1:6-1:13 proof map")
        source_row_id = row.get("source_row_id", "")
        source_row = source_rows.get(source_row_id)
        if not source_row:
            errors.append(f"{context}: source_row_id must reference an existing next-slice source row")
            continue
        if row.get("ref") != source_row.get("ref"):
            errors.append(f"{context}: ref must match the linked source row")
        if row.get("hebrew_phrase") != source_row.get("hebrew_word_or_phrase"):
            errors.append(f"{context}: hebrew_phrase must match the linked source row")
        if not row.get("hebrew_token", "").strip() or "?" in row.get("hebrew_token", ""):
            errors.append(f"{context}: hebrew_token must contain real Hebrew")
        if not row.get("clean_hebrew_no_nikud", "").strip() or "?" in row.get("clean_hebrew_no_nikud", ""):
            errors.append(f"{context}: clean_hebrew_no_nikud must contain real Hebrew")
        try:
            if int(row.get("token_index", "0")) <= 0:
                errors.append(f"{context}: token_index must be a positive integer")
        except ValueError:
            errors.append(f"{context}: token_index must be a positive integer")
        canonical_skill_id = row.get("canonical_skill_id", "").strip()
        if canonical_skill_id not in canonical_skills:
            errors.append(f"{context}: unknown canonical_skill_id {canonical_skill_id!r}")
        canonical_standard_anchor = row.get("canonical_standard_anchor", "").strip()
        if canonical_standard_anchor not in canonical_standards:
            errors.append(f"{context}: canonical_standard_anchor must map through the canonical contract")
        if row.get("proposed_zekelman_standard", "").strip() != canonical_standard_anchor:
            errors.append(f"{context}: proposed_zekelman_standard must match canonical_standard_anchor")
        record = canonical_records.get(canonical_skill_id)
        if record is not None and canonical_standard_anchor not in record.get("related_zekelman_standard_ids", []):
            errors.append(f"{context}: canonical_standard_anchor is not supported by canonical_skill_id")
        if row.get("confidence") not in ALLOWED_CONFIDENCE:
            errors.append(f"{context}: confidence must be one of {sorted(ALLOWED_CONFIDENCE)}")
        if row.get("question_allowed") != "needs_review":
            errors.append(f"{context}: question_allowed must remain needs_review")
        if row.get("protected_preview_allowed") != "false":
            errors.append(f"{context}: protected_preview_allowed must remain false")
        if row.get("reviewed_bank_allowed") != "false":
            errors.append(f"{context}: reviewed_bank_allowed must remain false")
        if row.get("runtime_allowed") != "false":
            errors.append(f"{context}: runtime_allowed must remain false")

    md_text = NEXT_TOKEN_SPLIT_REVIEW_MD_PATH.read_text(encoding="utf-8")
    if "This is enrichment review only." not in md_text:
        errors.append(f"{repo_relative(NEXT_TOKEN_SPLIT_REVIEW_MD_PATH)} missing token-split enrichment review warning")
    if "???" in md_text:
        errors.append(f"{repo_relative(NEXT_TOKEN_SPLIT_REVIEW_MD_PATH)} must render real Hebrew rather than placeholders")
    for decision in ALLOWED_TOKEN_SPLIT_RECOMMENDED_DECISIONS:
        if f"`{decision}`" not in md_text:
            errors.append(f"{repo_relative(NEXT_TOKEN_SPLIT_REVIEW_MD_PATH)} missing allowed decision: {decision}")

    if not NEXT_TOKEN_SPLIT_REVIEW_CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf"):
        errors.append(f"{repo_relative(NEXT_TOKEN_SPLIT_REVIEW_CSV_PATH)} must be UTF-8-BOM encoded")
    csv_columns, csv_rows = load_csv(NEXT_TOKEN_SPLIT_REVIEW_CSV_PATH)
    validate_columns(NEXT_TOKEN_SPLIT_REVIEW_CSV_PATH, csv_columns, TOKEN_SPLIT_REVIEW_CSV_COLUMNS, errors)
    candidate_ids = {row["candidate_id"] for row in rows}
    csv_ids = {row.get("candidate_id", "") for row in csv_rows}
    if csv_ids != candidate_ids:
        missing = sorted(candidate_ids - csv_ids)
        extra = sorted(csv_ids - candidate_ids)
        errors.append(
            f"{repo_relative(NEXT_TOKEN_SPLIT_REVIEW_CSV_PATH)} must list exactly the next-slice token-split candidates; missing={missing}, extra={extra}"
        )
    rows_by_id = {row["candidate_id"]: row for row in rows}
    for row in csv_rows:
        context = f"{repo_relative(NEXT_TOKEN_SPLIT_REVIEW_CSV_PATH)} candidate {row.get('candidate_id', '<blank>')}"
        if "?" in row.get("hebrew_token", ""):
            errors.append(f"{context}: hebrew_token must contain real Hebrew")
        if row.get("recommended_decision") not in ALLOWED_TOKEN_SPLIT_RECOMMENDED_DECISIONS:
            errors.append(f"{context}: recommended_decision is not allowed")
        source_row = rows_by_id.get(row.get("candidate_id", ""))
        if source_row is None:
            continue
        if row.get("canonical_skill_id") != source_row.get("canonical_skill_id"):
            errors.append(f"{context}: canonical_skill_id must match the token-split TSV")
        if row.get("canonical_standard_anchor") != source_row.get("canonical_standard_anchor"):
            errors.append(f"{context}: canonical_standard_anchor must match the token-split TSV")
    return rows


def validate_next_slice_generation_report(
    *,
    morphology_rows: list[dict[str, str]],
    vocabulary_rows: list[dict[str, str]],
    standards_rows: list[dict[str, str]],
    token_split_rows: list[dict[str, str]],
    errors: list[str],
) -> None:
    text = NEXT_GENERATION_REPORT_PATH.read_text(encoding="utf-8")
    follow_up_count = sum(
        1
        for row in morphology_rows + vocabulary_rows + standards_rows + token_split_rows
        if row.get("enrichment_review_status") == "needs_follow_up"
    )
    for phrase in (
        "Bereishis 1:6-1:13 Enrichment Candidate Generation Report",
        repo_relative(NEXT_SOURCE_MAP_PATH),
        f"- morphology: {len(morphology_rows)}",
        f"- vocabulary_shoresh: {len(vocabulary_rows)}",
        f"- standards: {len(standards_rows)}",
        f"- token_split_standards: {len(token_split_rows)}",
        f"- candidates currently marked `needs_follow_up`: {follow_up_count}",
        "token-split rows are review-only and safety-closed",
        "canonical skill ids and canonical standard anchors",
        "question_allowed = needs_review",
        "protected_preview_allowed = false",
        "reviewed_bank_allowed = false",
        "runtime_allowed = false",
        "Next Yossi Action",
    ):
        if phrase not in text:
            errors.append(f"{repo_relative(NEXT_GENERATION_REPORT_PATH)} missing required phrase: {phrase!r}")


def validate_expansion_token_split_artifacts(
    *,
    standards_rows: list[dict[str, str]],
    source_rows: dict[str, dict[str, str]],
    errors: list[str],
) -> list[dict[str, str]]:
    columns, rows = load_tsv(EXPANSION_TOKEN_SPLIT_STANDARDS_PATH)
    validate_columns(EXPANSION_TOKEN_SPLIT_STANDARDS_PATH, columns, TOKEN_SPLIT_STANDARDS_COLUMNS, errors)
    expected_source_map = repo_relative(EXPANSION_SOURCE_MAP_PATH)
    canonical_skills = canonical_contract_skill_ids()
    canonical_records = canonical_contract_record_map()
    canonical_standards = canonical_contract_standard_ids()
    parent_rows = {row["candidate_id"]: row for row in standards_rows}
    seen_ids: set[str] = set()

    for row in rows:
        context = f"{repo_relative(EXPANSION_TOKEN_SPLIT_STANDARDS_PATH)} candidate {row.get('candidate_id', '<blank>')}"
        candidate_id = row.get("candidate_id", "").strip()
        if not candidate_id:
            errors.append(f"{context}: candidate_id must be populated")
        elif candidate_id in seen_ids:
            errors.append(f"{context}: duplicate candidate_id")
        else:
            seen_ids.add(candidate_id)
        if row.get("parent_candidate_id", "").strip() not in parent_rows:
            errors.append(f"{context}: parent_candidate_id must reference a phrase-level standards candidate")
        if row.get("source_map_file") != expected_source_map:
            errors.append(f"{context}: source_map_file must match the Bereishis 1:14-1:23 proof map")
        source_row = source_rows.get(row.get("source_row_id", ""))
        if not source_row:
            errors.append(f"{context}: source_row_id must reference an existing source row")
            continue
        if row.get("ref") != source_row.get("ref"):
            errors.append(f"{context}: ref must match the linked source row")
        if row.get("hebrew_phrase") != source_row.get("hebrew_word_or_phrase"):
            errors.append(f"{context}: hebrew_phrase must match the linked source row")
        if not row.get("hebrew_token", "").strip() or "?" in row.get("hebrew_token", ""):
            errors.append(f"{context}: hebrew_token must contain real Hebrew")
        if not row.get("clean_hebrew_no_nikud", "").strip() or "?" in row.get("clean_hebrew_no_nikud", ""):
            errors.append(f"{context}: clean_hebrew_no_nikud must contain real Hebrew")
        canonical_skill_id = row.get("canonical_skill_id", "").strip()
        canonical_standard_anchor = row.get("canonical_standard_anchor", "").strip()
        if canonical_skill_id not in canonical_skills:
            errors.append(f"{context}: unknown canonical_skill_id {canonical_skill_id!r}")
        if canonical_standard_anchor not in canonical_standards:
            errors.append(f"{context}: canonical_standard_anchor must map through the canonical contract")
        if row.get("proposed_zekelman_standard", "").strip() != canonical_standard_anchor:
            errors.append(f"{context}: proposed_zekelman_standard must match canonical_standard_anchor")
        record = canonical_records.get(canonical_skill_id)
        if record is not None and canonical_standard_anchor not in record.get("related_zekelman_standard_ids", []):
            errors.append(f"{context}: canonical_standard_anchor is not supported by canonical_skill_id")
        if row.get("confidence") not in ALLOWED_CONFIDENCE:
            errors.append(f"{context}: confidence must be one of {sorted(ALLOWED_CONFIDENCE)}")
        if row.get("question_allowed") != "needs_review":
            errors.append(f"{context}: question_allowed must remain needs_review")
        if row.get("protected_preview_allowed") != "false":
            errors.append(f"{context}: protected_preview_allowed must remain false")
        if row.get("reviewed_bank_allowed") != "false":
            errors.append(f"{context}: reviewed_bank_allowed must remain false")
        if row.get("runtime_allowed") != "false":
            errors.append(f"{context}: runtime_allowed must remain false")

    md_text = EXPANSION_TOKEN_SPLIT_REVIEW_MD_PATH.read_text(encoding="utf-8")
    if "This is enrichment review only." not in md_text:
        errors.append(f"{repo_relative(EXPANSION_TOKEN_SPLIT_REVIEW_MD_PATH)} missing enrichment review warning")
    if "???" in md_text:
        errors.append(f"{repo_relative(EXPANSION_TOKEN_SPLIT_REVIEW_MD_PATH)} must render real Hebrew rather than placeholders")
    if not EXPANSION_TOKEN_SPLIT_REVIEW_CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf"):
        errors.append(f"{repo_relative(EXPANSION_TOKEN_SPLIT_REVIEW_CSV_PATH)} must be UTF-8-BOM encoded")
    csv_columns, csv_rows = load_csv(EXPANSION_TOKEN_SPLIT_REVIEW_CSV_PATH)
    validate_columns(EXPANSION_TOKEN_SPLIT_REVIEW_CSV_PATH, csv_columns, TOKEN_SPLIT_REVIEW_CSV_COLUMNS, errors)
    candidate_ids = {row["candidate_id"] for row in rows}
    csv_ids = {row.get("candidate_id", "") for row in csv_rows}
    if csv_ids != candidate_ids:
        errors.append(f"{repo_relative(EXPANSION_TOKEN_SPLIT_REVIEW_CSV_PATH)} must list exactly the token-split candidates")
    rows_by_id = {row["candidate_id"]: row for row in rows}
    for row in csv_rows:
        context = f"{repo_relative(EXPANSION_TOKEN_SPLIT_REVIEW_CSV_PATH)} candidate {row.get('candidate_id', '<blank>')}"
        if row.get("yossi_decision", "") != "":
            errors.append(f"{context}: yossi_decision must be blank before Yossi review")
        if row.get("yossi_notes", "") != "":
            errors.append(f"{context}: yossi_notes must be blank before Yossi review")
        if "?" in row.get("hebrew_token", ""):
            errors.append(f"{context}: hebrew_token must contain real Hebrew")
        source_row = rows_by_id.get(row.get("candidate_id", ""))
        if source_row is not None:
            if row.get("current_status") != source_row.get("enrichment_review_status"):
                errors.append(f"{context}: current_status must match the token-split TSV")
            if row.get("canonical_skill_id") != source_row.get("canonical_skill_id"):
                errors.append(f"{context}: canonical_skill_id must match the token-split TSV")
            if row.get("canonical_standard_anchor") != source_row.get("canonical_standard_anchor"):
                errors.append(f"{context}: canonical_standard_anchor must match the token-split TSV")
    return rows


def validate_expansion_generation_report(
    *,
    morphology_rows: list[dict[str, str]],
    vocabulary_rows: list[dict[str, str]],
    standards_rows: list[dict[str, str]],
    token_split_rows: list[dict[str, str]],
    errors: list[str],
) -> None:
    text = EXPANSION_GENERATION_REPORT_PATH.read_text(encoding="utf-8")
    all_rows = morphology_rows + vocabulary_rows + standards_rows + token_split_rows
    confidence_counts = {label: sum(1 for row in all_rows if row.get("confidence") == label) for label in ALLOWED_CONFIDENCE}
    follow_up_count = sum(1 for row in all_rows if row.get("enrichment_review_status") == "needs_follow_up")
    for phrase in (
        "Bereishis 1:14-1:23 Enrichment Candidate Generation Report",
        repo_relative(EXPANSION_SOURCE_MAP_PATH),
        f"- source-to-skill rows: {len(source_rows_by_id(EXPANSION_SOURCE_MAP_PATH))}",
        f"- morphology: {len(morphology_rows)}",
        f"- vocabulary_shoresh: {len(vocabulary_rows)}",
        f"- standards: {len(standards_rows)}",
        f"- token_split_standards: {len(token_split_rows)}",
        f"- total_candidates: {len(all_rows)}",
        f"- medium: {confidence_counts['medium']}",
        f"- low: {confidence_counts['low']}",
        "token-split standards rows are review-only and safety-closed",
        "canonical skill ids and canonical standard anchors",
        "Hebrew tokens are real UTF-8 Hebrew and not placeholder question marks",
        "question_allowed = needs_review",
        "protected_preview_allowed = false",
        "reviewed_bank_allowed = false",
        "runtime_allowed = false",
        "Next Yossi Action",
    ):
        if phrase not in text:
            errors.append(f"{repo_relative(EXPANSION_GENERATION_REPORT_PATH)} missing required phrase: {phrase!r}")
    if f"- follow-up morphology candidates: {sum(1 for row in morphology_rows if row.get('enrichment_review_status') == 'needs_follow_up')}" not in text:
        errors.append(f"{repo_relative(EXPANSION_GENERATION_REPORT_PATH)} missing morphology follow-up count")
    if follow_up_count <= 0:
        errors.append("Bereishis 1:14-1:23 expansion must retain unresolved follow-up candidates")


def validate_perek1_final_token_split_artifacts(
    *,
    standards_rows: list[dict[str, str]],
    source_rows: dict[str, dict[str, str]],
    errors: list[str],
) -> list[dict[str, str]]:
    columns, rows = load_tsv(PEREK1_FINAL_TOKEN_SPLIT_STANDARDS_PATH)
    validate_columns(PEREK1_FINAL_TOKEN_SPLIT_STANDARDS_PATH, columns, TOKEN_SPLIT_STANDARDS_COLUMNS, errors)
    expected_source_map = repo_relative(PEREK1_FINAL_SOURCE_MAP_PATH)
    canonical_skills = canonical_contract_skill_ids()
    canonical_records = canonical_contract_record_map()
    canonical_standards = canonical_contract_standard_ids()
    parent_rows = {row["candidate_id"]: row for row in standards_rows}
    seen_ids: set[str] = set()

    for row in rows:
        context = f"{repo_relative(PEREK1_FINAL_TOKEN_SPLIT_STANDARDS_PATH)} candidate {row.get('candidate_id', '<blank>')}"
        candidate_id = row.get("candidate_id", "").strip()
        if not candidate_id:
            errors.append(f"{context}: candidate_id must be populated")
        elif candidate_id in seen_ids:
            errors.append(f"{context}: duplicate candidate_id")
        else:
            seen_ids.add(candidate_id)
        if row.get("parent_candidate_id", "").strip() not in parent_rows:
            errors.append(f"{context}: parent_candidate_id must reference a phrase-level standards candidate")
        if row.get("source_map_file") != expected_source_map:
            errors.append(f"{context}: source_map_file must match the Bereishis 1:24-1:31 proof map")
        source_row = source_rows.get(row.get("source_row_id", ""))
        if not source_row:
            errors.append(f"{context}: source_row_id must reference an existing source row")
            continue
        if row.get("ref") != source_row.get("ref"):
            errors.append(f"{context}: ref must match the linked source row")
        if row.get("hebrew_phrase") != source_row.get("hebrew_word_or_phrase"):
            errors.append(f"{context}: hebrew_phrase must match the linked source row")
        if not row.get("hebrew_token", "").strip() or "?" in row.get("hebrew_token", ""):
            errors.append(f"{context}: hebrew_token must contain real Hebrew")
        if not row.get("clean_hebrew_no_nikud", "").strip() or "?" in row.get("clean_hebrew_no_nikud", ""):
            errors.append(f"{context}: clean_hebrew_no_nikud must contain real Hebrew")
        canonical_skill_id = row.get("canonical_skill_id", "").strip()
        canonical_standard_anchor = row.get("canonical_standard_anchor", "").strip()
        if canonical_skill_id not in canonical_skills:
            errors.append(f"{context}: unknown canonical_skill_id {canonical_skill_id!r}")
        if canonical_standard_anchor not in canonical_standards:
            errors.append(f"{context}: canonical_standard_anchor must map through the canonical contract")
        if row.get("proposed_zekelman_standard", "").strip() != canonical_standard_anchor:
            errors.append(f"{context}: proposed_zekelman_standard must match canonical_standard_anchor")
        record = canonical_records.get(canonical_skill_id)
        if record is not None and canonical_standard_anchor not in record.get("related_zekelman_standard_ids", []):
            errors.append(f"{context}: canonical_standard_anchor is not supported by canonical_skill_id")
        if row.get("confidence") not in ALLOWED_CONFIDENCE:
            errors.append(f"{context}: confidence must be one of {sorted(ALLOWED_CONFIDENCE)}")
        if row.get("question_allowed") != "needs_review":
            errors.append(f"{context}: question_allowed must remain needs_review")
        if row.get("protected_preview_allowed") != "false":
            errors.append(f"{context}: protected_preview_allowed must remain false")
        if row.get("reviewed_bank_allowed") != "false":
            errors.append(f"{context}: reviewed_bank_allowed must remain false")
        if row.get("runtime_allowed") != "false":
            errors.append(f"{context}: runtime_allowed must remain false")

    md_text = PEREK1_FINAL_TOKEN_SPLIT_REVIEW_MD_PATH.read_text(encoding="utf-8")
    if "This is enrichment review only." not in md_text:
        errors.append(f"{repo_relative(PEREK1_FINAL_TOKEN_SPLIT_REVIEW_MD_PATH)} missing enrichment review warning")
    if "???" in md_text:
        errors.append(f"{repo_relative(PEREK1_FINAL_TOKEN_SPLIT_REVIEW_MD_PATH)} must render real Hebrew rather than placeholders")
    if not PEREK1_FINAL_TOKEN_SPLIT_REVIEW_CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf"):
        errors.append(f"{repo_relative(PEREK1_FINAL_TOKEN_SPLIT_REVIEW_CSV_PATH)} must be UTF-8-BOM encoded")
    csv_columns, csv_rows = load_csv(PEREK1_FINAL_TOKEN_SPLIT_REVIEW_CSV_PATH)
    validate_columns(PEREK1_FINAL_TOKEN_SPLIT_REVIEW_CSV_PATH, csv_columns, TOKEN_SPLIT_REVIEW_CSV_COLUMNS, errors)
    candidate_ids = {row["candidate_id"] for row in rows}
    csv_ids = {row.get("candidate_id", "") for row in csv_rows}
    if csv_ids != candidate_ids:
        errors.append(f"{repo_relative(PEREK1_FINAL_TOKEN_SPLIT_REVIEW_CSV_PATH)} must list exactly the token-split candidates")
    rows_by_id = {row["candidate_id"]: row for row in rows}
    for row in csv_rows:
        context = f"{repo_relative(PEREK1_FINAL_TOKEN_SPLIT_REVIEW_CSV_PATH)} candidate {row.get('candidate_id', '<blank>')}"
        if "?" in row.get("hebrew_token", ""):
            errors.append(f"{context}: hebrew_token must contain real Hebrew")
        source_row = rows_by_id.get(row.get("candidate_id", ""))
        if source_row is not None:
            if row.get("canonical_skill_id") != source_row.get("canonical_skill_id"):
                errors.append(f"{context}: canonical_skill_id must match the token-split TSV")
            if row.get("canonical_standard_anchor") != source_row.get("canonical_standard_anchor"):
                errors.append(f"{context}: canonical_standard_anchor must match the token-split TSV")
    return rows


def validate_perek1_final_generation_report(
    *,
    morphology_rows: list[dict[str, str]],
    vocabulary_rows: list[dict[str, str]],
    standards_rows: list[dict[str, str]],
    token_split_rows: list[dict[str, str]],
    errors: list[str],
) -> None:
    text = PEREK1_FINAL_GENERATION_REPORT_PATH.read_text(encoding="utf-8")
    all_rows = morphology_rows + vocabulary_rows + standards_rows + token_split_rows
    confidence_counts = {label: sum(1 for row in all_rows if row.get("confidence") == label) for label in ALLOWED_CONFIDENCE}
    for phrase in (
        "Bereishis 1:24-1:31 Enrichment Candidate Generation Report",
        repo_relative(PEREK1_FINAL_SOURCE_MAP_PATH),
        f"- source-to-skill rows: {len(source_rows_by_id(PEREK1_FINAL_SOURCE_MAP_PATH))}",
        f"- morphology: {len(morphology_rows)}",
        f"- vocabulary_shoresh: {len(vocabulary_rows)}",
        f"- standards: {len(standards_rows)}",
        f"- token_split_standards: {len(token_split_rows)}",
        f"- total_candidates: {len(all_rows)}",
        f"- medium: {confidence_counts['medium']}",
        f"- low: {confidence_counts['low']}",
        "This slice completes enrichment candidate coverage across Bereishis Perek 1",
        "canonical skill ids and canonical standard anchors",
        "Hebrew tokens are real UTF-8 Hebrew and not placeholder question marks",
        "question_allowed = needs_review",
        "protected_preview_allowed = false",
        "reviewed_bank_allowed = false",
        "runtime_allowed = false",
        "Next Yossi Action",
    ):
        if phrase not in text:
            errors.append(f"{repo_relative(PEREK1_FINAL_GENERATION_REPORT_PATH)} missing required phrase: {phrase!r}")
def validate_perek1_final_review_applied_reports(
    *,
    morphology_rows: list[dict[str, str]],
    vocabulary_rows: list[dict[str, str]],
    standards_rows: list[dict[str, str]],
    token_split_rows: list[dict[str, str]],
    errors: list[str],
) -> None:
    report_specs = (
        (
            PEREK1_FINAL_MORPHOLOGY_APPLIED_REPORT_PATH,
            len(morphology_rows),
            review_status_counts(morphology_rows)["yossi_enrichment_verified"],
            review_status_counts(morphology_rows)["needs_follow_up"],
        ),
        (
            PEREK1_FINAL_VOCAB_APPLIED_REPORT_PATH,
            len(vocabulary_rows),
            review_status_counts(vocabulary_rows)["yossi_enrichment_verified"],
            review_status_counts(vocabulary_rows)["needs_follow_up"],
        ),
        (
            PEREK1_FINAL_STANDARDS_APPLIED_REPORT_PATH,
            len(standards_rows),
            review_status_counts(standards_rows)["yossi_enrichment_verified"],
            review_status_counts(standards_rows)["needs_follow_up"],
        ),
        (
            PEREK1_FINAL_TOKEN_SPLIT_APPLIED_REPORT_PATH,
            len(token_split_rows),
            review_status_counts(token_split_rows)["yossi_enrichment_verified"],
            review_status_counts(token_split_rows)["needs_follow_up"],
        ),
    )
    for path, total, verified, follow_up in report_specs:
        text = path.read_text(encoding="utf-8")
        for phrase in (
            f"- total candidates reviewed: {total}",
            f"- verified count: {verified}",
            f"- needs_follow_up count: {follow_up}",
            "Safety Gate Confirmation",
            "question_allowed = needs_review",
            "protected_preview_allowed = false",
            "reviewed_bank_allowed = false",
            "runtime_allowed = false",
            "What Was Not Approved",
        ):
            if phrase not in text:
                errors.append(f"{repo_relative(path)} missing required phrase: {phrase!r}")


def validate_perek1_final_review_summary(
    *,
    morphology_rows: list[dict[str, str]],
    vocabulary_rows: list[dict[str, str]],
    standards_rows: list[dict[str, str]],
    token_split_rows: list[dict[str, str]],
    errors: list[str],
) -> None:
    text = PEREK1_FINAL_REVIEW_SUMMARY_PATH.read_text(encoding="utf-8")
    total = len(morphology_rows) + len(vocabulary_rows) + len(standards_rows) + len(token_split_rows)
    m_counts = review_status_counts(morphology_rows)
    v_counts = review_status_counts(vocabulary_rows)
    s_counts = review_status_counts(standards_rows)
    ts_counts = review_status_counts(token_split_rows)
    verified = (
        m_counts["yossi_enrichment_verified"]
        + v_counts["yossi_enrichment_verified"]
        + s_counts["yossi_enrichment_verified"]
        + ts_counts["yossi_enrichment_verified"]
    )
    follow_up = (
        m_counts["needs_follow_up"]
        + v_counts["needs_follow_up"]
        + s_counts["needs_follow_up"]
        + ts_counts["needs_follow_up"]
    )
    for phrase in (
        "Bereishis 1:24-1:31 Enrichment Review Summary",
        f"- total candidates: {total}",
        f"- total verified: {verified}",
        f"- total needs_follow_up: {follow_up}",
        "future/jussive/imperative verb forms",
        "vav narrative/stem interpretation",
        "prefix/preposition standards mapping",
        "construct/suffix and compound forms",
        "phrase-level standards superseded by token-split rows",
        "question_allowed = needs_review",
        "protected_preview_allowed = false",
        "reviewed_bank_allowed = false",
        "runtime_allowed = false",
        "What Was Not Approved",
    ):
        if phrase not in text:
            errors.append(f"{repo_relative(PEREK1_FINAL_REVIEW_SUMMARY_PATH)} missing required phrase: {phrase!r}")


def validate_perek1_coverage_report(
    *,
    next_morphology_rows: list[dict[str, str]],
    next_vocabulary_rows: list[dict[str, str]],
    next_standards_rows: list[dict[str, str]],
    next_token_split_rows: list[dict[str, str]],
    expansion_morphology_rows: list[dict[str, str]],
    expansion_vocabulary_rows: list[dict[str, str]],
    expansion_standards_rows: list[dict[str, str]],
    expansion_token_split_rows: list[dict[str, str]],
    perek1_final_morphology_rows: list[dict[str, str]],
    perek1_final_vocabulary_rows: list[dict[str, str]],
    perek1_final_standards_rows: list[dict[str, str]],
    perek1_final_token_split_rows: list[dict[str, str]],
    errors: list[str],
) -> None:
    text = PEREK1_COVERAGE_REPORT_PATH.read_text(encoding="utf-8")

    _, pilot_morphology_rows = load_tsv(MORPHOLOGY_PATH)
    _, pilot_vocabulary_rows = load_tsv(VOCABULARY_PATH)
    _, pilot_standards_rows = load_tsv(STANDARDS_PATH)
    _, pilot_token_split_rows = load_tsv(TOKEN_SPLIT_STANDARDS_PATH)

    def counts(rows: list[dict[str, str]]) -> tuple[int, int]:
        status = review_status_counts(rows)
        return status["yossi_enrichment_verified"], status["needs_follow_up"]

    m_total = (
        len(pilot_morphology_rows)
        + len(next_morphology_rows)
        + len(expansion_morphology_rows)
        + len(perek1_final_morphology_rows)
    )
    v_total = (
        len(pilot_vocabulary_rows)
        + len(next_vocabulary_rows)
        + len(expansion_vocabulary_rows)
        + len(perek1_final_vocabulary_rows)
    )
    s_total = (
        len(pilot_standards_rows)
        + len(next_standards_rows)
        + len(expansion_standards_rows)
        + len(perek1_final_standards_rows)
    )
    ts_total = (
        len(pilot_token_split_rows)
        + len(next_token_split_rows)
        + len(expansion_token_split_rows)
        + len(perek1_final_token_split_rows)
    )

    m_verified = (
        counts(pilot_morphology_rows)[0]
        + counts(next_morphology_rows)[0]
        + counts(expansion_morphology_rows)[0]
        + counts(perek1_final_morphology_rows)[0]
    )
    m_follow = (
        counts(pilot_morphology_rows)[1]
        + counts(next_morphology_rows)[1]
        + counts(expansion_morphology_rows)[1]
        + counts(perek1_final_morphology_rows)[1]
    )
    v_verified = (
        counts(pilot_vocabulary_rows)[0]
        + counts(next_vocabulary_rows)[0]
        + counts(expansion_vocabulary_rows)[0]
        + counts(perek1_final_vocabulary_rows)[0]
    )
    v_follow = (
        counts(pilot_vocabulary_rows)[1]
        + counts(next_vocabulary_rows)[1]
        + counts(expansion_vocabulary_rows)[1]
        + counts(perek1_final_vocabulary_rows)[1]
    )
    s_verified = (
        counts(pilot_standards_rows)[0]
        + counts(next_standards_rows)[0]
        + counts(expansion_standards_rows)[0]
        + counts(perek1_final_standards_rows)[0]
    )
    s_follow = (
        counts(pilot_standards_rows)[1]
        + counts(next_standards_rows)[1]
        + counts(expansion_standards_rows)[1]
        + counts(perek1_final_standards_rows)[1]
    )
    ts_verified = (
        counts(pilot_token_split_rows)[0]
        + counts(next_token_split_rows)[0]
        + counts(expansion_token_split_rows)[0]
        + counts(perek1_final_token_split_rows)[0]
    )
    ts_follow = (
        counts(pilot_token_split_rows)[1]
        + counts(next_token_split_rows)[1]
        + counts(expansion_token_split_rows)[1]
        + counts(perek1_final_token_split_rows)[1]
    )

    total_candidates = m_total + v_total + s_total + ts_total
    total_verified = m_verified + v_verified + s_verified + ts_verified
    total_follow_up = m_follow + v_follow + s_follow + ts_follow

    for phrase in (
        "Bereishis Perek 1 Enrichment Review-Application Coverage Report",
        "Bereishis 1:1-1:31",
        "| Bereishis 1:1-1:5 | 23 | 27 | 14 | 13 |",
        "| Bereishis 1:6-1:13 | 37 | 32 | 14 | 18 |",
        "| Bereishis 1:14-1:23 | 39 | 104 | 53 | 51 |",
        "| Bereishis 1:24-1:31 | 38 | 136 | 83 | 53 |",
        f"| morphology | {m_total} | {m_verified} | {m_follow} |",
        f"| vocabulary/shoresh | {v_total} | {v_verified} | {v_follow} |",
        f"| phrase-level standards | {s_total} | {s_verified} | {s_follow} |",
        f"| token-split standards | {ts_total} | {ts_verified} | {ts_follow} |",
        f"| **total** | **{total_candidates}** | **{total_verified}** | **{total_follow_up}** |",
        "question generation remains blocked",
        "protected preview remains blocked",
        "reviewed bank remains blocked",
        "runtime remains blocked",
        "student-facing use remains blocked",
    ):
        if phrase not in text:
            errors.append(f"{repo_relative(PEREK1_COVERAGE_REPORT_PATH)} missing required phrase: {phrase!r}")

def validate_next_slice_review_applied_reports(
    *,
    morphology_rows: list[dict[str, str]],
    vocabulary_rows: list[dict[str, str]],
    standards_rows: list[dict[str, str]],
    token_split_rows: list[dict[str, str]],
    errors: list[str],
) -> None:
    report_specs = (
        (
            NEXT_MORPHOLOGY_APPLIED_REPORT_PATH,
            len(morphology_rows),
            review_status_counts(morphology_rows)["yossi_enrichment_verified"],
            review_status_counts(morphology_rows)["needs_follow_up"],
        ),
        (
            NEXT_VOCAB_APPLIED_REPORT_PATH,
            len(vocabulary_rows),
            review_status_counts(vocabulary_rows)["yossi_enrichment_verified"],
            review_status_counts(vocabulary_rows)["needs_follow_up"],
        ),
        (
            NEXT_STANDARDS_APPLIED_REPORT_PATH,
            len(standards_rows),
            review_status_counts(standards_rows)["yossi_enrichment_verified"],
            review_status_counts(standards_rows)["needs_follow_up"],
        ),
        (
            NEXT_TOKEN_SPLIT_APPLIED_REPORT_PATH,
            len(token_split_rows),
            review_status_counts(token_split_rows)["yossi_enrichment_verified"],
            review_status_counts(token_split_rows)["needs_follow_up"],
        ),
    )
    for path, total, verified, follow_up in report_specs:
        text = path.read_text(encoding="utf-8")
        for phrase in (
            f"- total candidates reviewed: {total}",
            f"- verified count: {verified}",
            f"- needs_follow_up count: {follow_up}",
            "Safety gate confirmation",
            "question_allowed = needs_review",
            "protected_preview_allowed = false",
            "reviewed_bank_allowed = false",
            "runtime_allowed = false",
            "What was not approved",
        ):
            if phrase not in text:
                errors.append(f"{repo_relative(path)} missing required phrase: {phrase!r}")


def validate_next_slice_review_summary(
    *,
    morphology_rows: list[dict[str, str]],
    vocabulary_rows: list[dict[str, str]],
    standards_rows: list[dict[str, str]],
    token_split_rows: list[dict[str, str]],
    errors: list[str],
) -> None:
    text = NEXT_SLICE_REVIEW_SUMMARY_PATH.read_text(encoding="utf-8")
    total = len(morphology_rows) + len(vocabulary_rows) + len(standards_rows) + len(token_split_rows)
    m_counts = review_status_counts(morphology_rows)
    v_counts = review_status_counts(vocabulary_rows)
    s_counts = review_status_counts(standards_rows)
    ts_counts = review_status_counts(token_split_rows)
    verified = (
        m_counts["yossi_enrichment_verified"]
        + v_counts["yossi_enrichment_verified"]
        + s_counts["yossi_enrichment_verified"]
        + ts_counts["yossi_enrichment_verified"]
    )
    follow_up = (
        m_counts["needs_follow_up"]
        + v_counts["needs_follow_up"]
        + s_counts["needs_follow_up"]
        + ts_counts["needs_follow_up"]
    )
    required_phrases = (
        "Bereishis 1:6-1:13 Enrichment Review Summary",
        f"- total candidates: {total}",
        f"- total verified: {verified}",
        f"- total needs_follow_up: {follow_up}",
        f"- morphology: verified={m_counts['yossi_enrichment_verified']}, needs_follow_up={m_counts['needs_follow_up']}",
        f"- vocabulary_shoresh: verified={v_counts['yossi_enrichment_verified']}, needs_follow_up={v_counts['needs_follow_up']}",
        f"- phrase_level_standards: verified={s_counts['yossi_enrichment_verified']}, needs_follow_up={s_counts['needs_follow_up']}",
        f"- token_split_standards: verified={ts_counts['yossi_enrichment_verified']}, needs_follow_up={ts_counts['needs_follow_up']}",
        "jussive/future verb forms",
        "vav-hahipuch and stem uncertainty",
        "prefix/preposition standard mapping",
        "contextual vocabulary such as ימים and יבשה",
        "phrase-level standards rows remain superseded by token-split rows",
        "question_allowed = needs_review",
        "protected_preview_allowed = false",
        "reviewed_bank_allowed = false",
        "runtime_allowed = false",
    )
    for phrase in required_phrases:
        if phrase not in text:
            errors.append(f"{repo_relative(NEXT_SLICE_REVIEW_SUMMARY_PATH)} missing required phrase: {phrase!r}")

    followup_text = NEXT_FOLLOW_UP_INVENTORY_PATH.read_text(encoding="utf-8")
    for phrase in (
        "Bereishis 1:6-1:13 Enrichment Follow-Up Inventory",
        "Morphology follow-up",
        "Vocabulary/shoresh follow-up",
        "Phrase-level standards follow-up",
        "Token-split standards follow-up",
        "question_allowed = needs_review",
        "protected_preview_allowed = false",
        "reviewed_bank_allowed = false",
        "runtime_allowed = false",
    ):
        if phrase not in followup_text:
            errors.append(f"{repo_relative(NEXT_FOLLOW_UP_INVENTORY_PATH)} missing required phrase: {phrase!r}")


def validate_expansion_review_applied_reports(
    *,
    morphology_rows: list[dict[str, str]],
    vocabulary_rows: list[dict[str, str]],
    standards_rows: list[dict[str, str]],
    token_split_rows: list[dict[str, str]],
    errors: list[str],
) -> None:
    report_specs = (
        (
            EXPANSION_MORPHOLOGY_APPLIED_REPORT_PATH,
            len(morphology_rows),
            review_status_counts(morphology_rows)["yossi_enrichment_verified"],
            review_status_counts(morphology_rows)["needs_follow_up"],
        ),
        (
            EXPANSION_VOCAB_APPLIED_REPORT_PATH,
            len(vocabulary_rows),
            review_status_counts(vocabulary_rows)["yossi_enrichment_verified"],
            review_status_counts(vocabulary_rows)["needs_follow_up"],
        ),
        (
            EXPANSION_STANDARDS_APPLIED_REPORT_PATH,
            len(standards_rows),
            review_status_counts(standards_rows)["yossi_enrichment_verified"],
            review_status_counts(standards_rows)["needs_follow_up"],
        ),
        (
            EXPANSION_TOKEN_SPLIT_APPLIED_REPORT_PATH,
            len(token_split_rows),
            review_status_counts(token_split_rows)["yossi_enrichment_verified"],
            review_status_counts(token_split_rows)["needs_follow_up"],
        ),
    )
    for path, total, verified, follow_up in report_specs:
        text = path.read_text(encoding="utf-8")
        for phrase in (
            f"- total candidates reviewed: {total}",
            f"- verified count: {verified}",
            f"- needs_follow_up count: {follow_up}",
            "safety gates confirmed",
            "question_allowed=needs_review",
            "protected_preview_allowed=false",
            "reviewed_bank_allowed=false",
            "runtime_allowed=false",
            "what was not approved",
        ):
            if phrase not in text:
                errors.append(f"{repo_relative(path)} missing required phrase: {phrase!r}")


def validate_expansion_review_summary(
    *,
    morphology_rows: list[dict[str, str]],
    vocabulary_rows: list[dict[str, str]],
    standards_rows: list[dict[str, str]],
    token_split_rows: list[dict[str, str]],
    errors: list[str],
) -> None:
    text = EXPANSION_SLICE_REVIEW_SUMMARY_PATH.read_text(encoding="utf-8")
    m_counts = review_status_counts(morphology_rows)
    v_counts = review_status_counts(vocabulary_rows)
    s_counts = review_status_counts(standards_rows)
    ts_counts = review_status_counts(token_split_rows)
    total_verified = (
        m_counts["yossi_enrichment_verified"]
        + v_counts["yossi_enrichment_verified"]
        + s_counts["yossi_enrichment_verified"]
        + ts_counts["yossi_enrichment_verified"]
    )
    total_follow_up = (
        m_counts["needs_follow_up"]
        + v_counts["needs_follow_up"]
        + s_counts["needs_follow_up"]
        + ts_counts["needs_follow_up"]
    )
    for phrase in (
        "Bereishis 1:14-1:23 Enrichment Review Summary",
        "- total candidates: 104",
        f"- verified count: {total_verified}",
        f"- needs_follow_up count: {total_follow_up}",
        f"| morphology | {len(morphology_rows)} | {m_counts['yossi_enrichment_verified']} | {m_counts['needs_follow_up']} | {m_counts['source_only']} | {m_counts['blocked_unclear_evidence']} |",
        f"| vocabulary/shoresh | {len(vocabulary_rows)} | {v_counts['yossi_enrichment_verified']} | {v_counts['needs_follow_up']} | {v_counts['source_only']} | {v_counts['blocked_unclear_evidence']} |",
        f"| phrase-level standards | {len(standards_rows)} | {s_counts['yossi_enrichment_verified']} | {s_counts['needs_follow_up']} | {s_counts['source_only']} | {s_counts['blocked_unclear_evidence']} |",
        f"| token-split standards | {len(token_split_rows)} | {ts_counts['yossi_enrichment_verified']} | {ts_counts['needs_follow_up']} | {ts_counts['source_only']} | {ts_counts['blocked_unclear_evidence']} |",
        "all later gates remain closed",
        "What Was Not Approved",
    ):
        if phrase not in text:
            errors.append(f"{repo_relative(EXPANSION_SLICE_REVIEW_SUMMARY_PATH)} missing required phrase: {phrase!r}")


def validate_expansion_mini_completion_report(
    *,
    morphology_rows: list[dict[str, str]],
    vocabulary_rows: list[dict[str, str]],
    standards_rows: list[dict[str, str]],
    token_split_rows: list[dict[str, str]],
    errors: list[str],
) -> None:
    text = EXPANSION_MINI_COMPLETION_REPORT_PATH.read_text(encoding="utf-8")
    m_counts = review_status_counts(morphology_rows)
    v_counts = review_status_counts(vocabulary_rows)
    s_counts = review_status_counts(standards_rows)
    ts_counts = review_status_counts(token_split_rows)
    total = len(morphology_rows) + len(vocabulary_rows) + len(standards_rows) + len(token_split_rows)
    total_verified = (
        m_counts["yossi_enrichment_verified"]
        + v_counts["yossi_enrichment_verified"]
        + s_counts["yossi_enrichment_verified"]
        + ts_counts["yossi_enrichment_verified"]
    )
    total_follow_up = (
        m_counts["needs_follow_up"]
        + v_counts["needs_follow_up"]
        + s_counts["needs_follow_up"]
        + ts_counts["needs_follow_up"]
    )
    required_phrases = (
        "Bereishis 1:14-1:23 Enrichment Mini-Completion Report",
        "enrichment review decisions have been applied",
        "completed enrichment-review milestone",
        f"| morphology | {len(morphology_rows)} | {m_counts['yossi_enrichment_verified']} | {m_counts['needs_follow_up']} | {m_counts['source_only']} | {m_counts['blocked_unclear_evidence']} |",
        f"| vocabulary/shoresh | {len(vocabulary_rows)} | {v_counts['yossi_enrichment_verified']} | {v_counts['needs_follow_up']} | {v_counts['source_only']} | {v_counts['blocked_unclear_evidence']} |",
        f"| phrase-level standards | {len(standards_rows)} | {s_counts['yossi_enrichment_verified']} | {s_counts['needs_follow_up']} | {s_counts['source_only']} | {s_counts['blocked_unclear_evidence']} |",
        f"| token-split standards | {len(token_split_rows)} | {ts_counts['yossi_enrichment_verified']} | {ts_counts['needs_follow_up']} | {ts_counts['source_only']} | {ts_counts['blocked_unclear_evidence']} |",
        f"| total | {total} | {total_verified} | {total_follow_up} | 0 | 0 |",
        "phrase-level standards rows remain unresolved",
        "token-split standards rows produced the useful verified mappings",
        "question generation remains blocked",
        "protected-preview remains blocked",
        "reviewed bank remains blocked",
        "runtime remains blocked",
        "student-facing use remains blocked",
        "not question approval",
        "not protected-preview approval",
        "not reviewed-bank approval",
        "not runtime approval",
        "not student-facing approval",
        "not answer-key approval",
        "Bereishis 1:24-1:31",
    )
    for phrase in required_phrases:
        if phrase not in text:
            errors.append(f"{repo_relative(EXPANSION_MINI_COMPLETION_REPORT_PATH)} missing required phrase: {phrase!r}")


def validate_next_slice_mini_completion_report(
    *,
    morphology_rows: list[dict[str, str]],
    vocabulary_rows: list[dict[str, str]],
    standards_rows: list[dict[str, str]],
    token_split_rows: list[dict[str, str]],
    errors: list[str],
) -> None:
    text = NEXT_MINI_COMPLETION_REPORT_PATH.read_text(encoding="utf-8")
    m_counts = review_status_counts(morphology_rows)
    v_counts = review_status_counts(vocabulary_rows)
    s_counts = review_status_counts(standards_rows)
    ts_counts = review_status_counts(token_split_rows)
    total = len(morphology_rows) + len(vocabulary_rows) + len(standards_rows) + len(token_split_rows)
    verified = (
        m_counts["yossi_enrichment_verified"]
        + v_counts["yossi_enrichment_verified"]
        + s_counts["yossi_enrichment_verified"]
        + ts_counts["yossi_enrichment_verified"]
    )
    follow_up = (
        m_counts["needs_follow_up"]
        + v_counts["needs_follow_up"]
        + s_counts["needs_follow_up"]
        + ts_counts["needs_follow_up"]
    )
    required_phrases = (
        "Bereishis 1:6-1:13 Enrichment Mini-Completion Report",
        "question generation remains blocked",
        "protected-preview remains blocked",
        "reviewed bank remains blocked",
        "runtime remains blocked",
        "student-facing use remains blocked",
        "not question approval",
        "not protected-preview approval",
        "not reviewed-bank approval",
        "not runtime approval",
        "not student-facing approval",
        "not answer-key approval",
        "Bereishis 1:14-1:23",
        f"| morphology | {len(morphology_rows)} | {m_counts['yossi_enrichment_verified']} | {m_counts['needs_follow_up']} | {m_counts['source_only']} | {m_counts['blocked_unclear_evidence']} |",
        f"| vocabulary/shoresh | {len(vocabulary_rows)} | {v_counts['yossi_enrichment_verified']} | {v_counts['needs_follow_up']} | {v_counts['source_only']} | {v_counts['blocked_unclear_evidence']} |",
        f"| phrase-level standards | {len(standards_rows)} | {s_counts['yossi_enrichment_verified']} | {s_counts['needs_follow_up']} | {s_counts['source_only']} | {s_counts['blocked_unclear_evidence']} |",
        f"| token-split standards | {len(token_split_rows)} | {ts_counts['yossi_enrichment_verified']} | {ts_counts['needs_follow_up']} | {ts_counts['source_only']} | {ts_counts['blocked_unclear_evidence']} |",
        f"| total | {total} | {verified} | {follow_up} | 0 | 0 |",
    )
    for phrase in required_phrases:
        if phrase not in text:
            errors.append(f"{repo_relative(NEXT_MINI_COMPLETION_REPORT_PATH)} missing required phrase: {phrase!r}")


def perek2_source_rows_by_file() -> dict[str, dict[str, dict[str, str]]]:
    rows_by_file: dict[str, dict[str, dict[str, str]]] = {}
    for path in PEREK2_SOURCE_MAP_PATHS:
        _, rows = load_tsv(path)
        rows_by_file[repo_relative(path)] = {f"row_{index:03d}": row for index, row in enumerate(rows, 1)}
    return rows_by_file


def validate_perek2_gate1_artifacts(errors: list[str]) -> dict[str, int]:
    expected_files = (
        PEREK2_MORPHOLOGY_PATH,
        PEREK2_VOCABULARY_PATH,
        PEREK2_STANDARDS_PATH,
        PEREK2_TOKEN_SPLIT_STANDARDS_PATH,
        PEREK2_SOURCE_READINESS_AUDIT_PATH,
        PEREK2_GATE1_REPORT_PATH,
    )
    for path in expected_files:
        if not path.exists():
            errors.append(f"missing Perek 2 Gate 1 artifact: {repo_relative(path)}")
    for md_path, csv_path in PEREK2_REVIEW_SHEETS.values():
        if not md_path.exists():
            errors.append(f"missing Perek 2 review sheet: {repo_relative(md_path)}")
        if not csv_path.exists():
            errors.append(f"missing Perek 2 review CSV: {repo_relative(csv_path)}")
        elif not csv_path.read_bytes().startswith(b"\xef\xbb\xbf"):
            errors.append(f"Perek 2 review CSV must be UTF-8-BOM: {repo_relative(csv_path)}")
    if any(not path.exists() for path in expected_files):
        return {"morphology": 0, "vocabulary": 0, "standards": 0, "token_split": 0, "source_rows": 0}

    perek2_source_rows = perek2_source_rows_by_file()
    source_row_count = sum(len(rows) for rows in perek2_source_rows.values())
    for source_file, rows in perek2_source_rows.items():
        for row_id, row in rows.items():
            context = f"{source_file}:{row_id}"
            if row.get("extraction_review_status") != "yossi_extraction_verified":
                errors.append(f"{context}: source row must be yossi_extraction_verified")
            for field, expected in (
                ("question_allowed", "needs_review"),
                ("protected_preview_allowed", "false"),
                ("reviewed_bank_allowed", "false"),
                ("runtime_allowed", "false"),
            ):
                if row.get(field) != expected:
                    errors.append(f"{context}: {field} must be {expected}")
            if "?" in row.get("hebrew_word_or_phrase", ""):
                errors.append(f"{context}: Hebrew phrase contains placeholder corruption")

    candidate_specs = (
        (PEREK2_MORPHOLOGY_PATH, MORPHOLOGY_COLUMNS, "morphology"),
        (PEREK2_VOCABULARY_PATH, VOCABULARY_COLUMNS, "vocabulary"),
        (PEREK2_STANDARDS_PATH, STANDARDS_COLUMNS, "standards"),
        (PEREK2_TOKEN_SPLIT_STANDARDS_PATH, TOKEN_SPLIT_STANDARDS_COLUMNS, "token_split"),
    )
    counts: dict[str, int] = {"source_rows": source_row_count}
    standards_ids: set[str] = set()
    for path, expected_columns, label in candidate_specs:
        fields, rows = load_tsv(path)
        counts[label] = len(rows)
        if fields != expected_columns:
            errors.append(f"{repo_relative(path)} columns do not match expected {label} schema")
        if not rows:
            errors.append(f"{repo_relative(path)} must not be empty")
        if label == "standards":
            standards_ids = {row.get("candidate_id", "") for row in rows}
        for row in rows:
            candidate_id = row.get("candidate_id", "unknown")
            source_file = row.get("source_map_file", "")
            source_row_id = row.get("source_row_id", "")
            source_row = perek2_source_rows.get(source_file, {}).get(source_row_id)
            if source_row is None:
                errors.append(f"{candidate_id}: must link to a verified Perek 2 source row")
                continue
            if row.get("ref") != source_row.get("ref"):
                errors.append(f"{candidate_id}: ref must match linked source row")
            if row.get("hebrew_phrase") != source_row.get("hebrew_word_or_phrase"):
                errors.append(f"{candidate_id}: Hebrew phrase must match linked source row")
            if row.get("enrichment_review_status") != "pending_yossi_enrichment_review":
                errors.append(f"{candidate_id}: Perek 2 Gate 1 candidates must remain pending Yossi review")
            if row.get("yossi_decision") or row.get("yossi_notes"):
                errors.append(f"{candidate_id}: Yossi decision fields must be blank at Gate 1")
            for field, expected in (
                ("question_allowed", "needs_review"),
                ("protected_preview_allowed", "false"),
                ("runtime_allowed", "false"),
                ("reviewed_bank_allowed", "false"),
            ):
                if row.get(field) != expected:
                    errors.append(f"{candidate_id}: {field} must be {expected}")
            if "?" in row.get("hebrew_phrase", "") or "?" in row.get("hebrew_token", ""):
                errors.append(f"{candidate_id}: Hebrew fields must not contain placeholder corruption")
    _, token_rows = load_tsv(PEREK2_TOKEN_SPLIT_STANDARDS_PATH)
    for row in token_rows:
        if row.get("parent_candidate_id") not in standards_ids:
            errors.append(f"{row.get('candidate_id', 'unknown')}: token-split row must link to a Perek 2 standards parent")

    for md_path, csv_path in PEREK2_REVIEW_SHEETS.values():
        text = md_path.read_text(encoding="utf-8")
        safety_sentence = (
            "This is enrichment review only. It is not question approval, protected-preview approval, "
            "reviewed-bank approval, runtime approval, or student-facing approval."
        )
        if safety_sentence not in text:
            errors.append(f"{repo_relative(md_path)} missing required safety sentence")
        if "??" in text or "???" in text:
            errors.append(f"{repo_relative(md_path)} contains placeholder corruption")
        csv_fields, csv_rows = load_csv(csv_path)
        if csv_fields != REVIEW_CSV_COLUMNS:
            errors.append(f"{repo_relative(csv_path)} columns must match review CSV schema")
        if any(row.get("yossi_decision") or row.get("yossi_notes") for row in csv_rows):
            errors.append(f"{repo_relative(csv_path)} Yossi decision fields must be blank")

    source_text = PEREK2_SOURCE_READINESS_AUDIT_PATH.read_text(encoding="utf-8")
    gate_text = PEREK2_GATE1_REPORT_PATH.read_text(encoding="utf-8")
    readme_text = README_PATH.read_text(encoding="utf-8")
    for phrase in ("Perek 2 source-to-skill readiness is confirmed", "Enrichment remains review-only"):
        if phrase not in source_text:
            errors.append(f"Perek 2 source readiness audit missing phrase: {phrase}")
    for phrase in (
        "Question-eligibility decisions and approved input-candidate planning are not ready",
        "All candidates are review-only",
        "basic_verb_form_recognition",
    ):
        if phrase not in gate_text:
            errors.append(f"Perek 2 Gate 1 report missing phrase: {phrase}")
    for path in (
        PEREK2_MORPHOLOGY_PATH,
        PEREK2_VOCABULARY_PATH,
        PEREK2_STANDARDS_PATH,
        PEREK2_TOKEN_SPLIT_STANDARDS_PATH,
        PEREK2_GATE1_REPORT_PATH,
    ):
        relative = repo_relative(path)
        if relative not in readme_text and relative.replace("data/source_skill_enrichment/", "") not in readme_text:
            errors.append(f"source enrichment README must link {relative}")

    return counts


def validate_source_skill_enrichment() -> dict[str, object]:
    errors: list[str] = []
    validate_required_files(errors)
    if errors:
        return {"valid": False, "errors": errors}

    source_rows = source_rows_by_id(SOURCE_MAP_PATH)
    next_source_rows = source_rows_by_id(NEXT_SOURCE_MAP_PATH)
    expansion_source_rows = source_rows_by_id(EXPANSION_SOURCE_MAP_PATH)
    perek1_final_source_rows = source_rows_by_id(PEREK1_FINAL_SOURCE_MAP_PATH)
    validate_source_map_readiness(NEXT_SOURCE_MAP_PATH, errors)
    validate_source_map_readiness(EXPANSION_SOURCE_MAP_PATH, errors)
    validate_source_map_readiness(PEREK1_FINAL_SOURCE_MAP_PATH, errors)

    morphology_columns, morphology_rows = load_tsv(MORPHOLOGY_PATH)
    standards_columns, standards_rows = load_tsv(STANDARDS_PATH)
    vocabulary_columns, vocabulary_rows = load_tsv(VOCABULARY_PATH)
    next_morphology_columns, next_morphology_rows = load_tsv(NEXT_MORPHOLOGY_PATH)
    next_standards_columns, next_standards_rows = load_tsv(NEXT_STANDARDS_PATH)
    next_vocabulary_columns, next_vocabulary_rows = load_tsv(NEXT_VOCABULARY_PATH)
    expansion_morphology_columns, expansion_morphology_rows = load_tsv(EXPANSION_MORPHOLOGY_PATH)
    expansion_standards_columns, expansion_standards_rows = load_tsv(EXPANSION_STANDARDS_PATH)
    expansion_vocabulary_columns, expansion_vocabulary_rows = load_tsv(EXPANSION_VOCABULARY_PATH)
    perek1_final_morphology_columns, perek1_final_morphology_rows = load_tsv(PEREK1_FINAL_MORPHOLOGY_PATH)
    perek1_final_standards_columns, perek1_final_standards_rows = load_tsv(PEREK1_FINAL_STANDARDS_PATH)
    perek1_final_vocabulary_columns, perek1_final_vocabulary_rows = load_tsv(PEREK1_FINAL_VOCABULARY_PATH)

    validate_columns(MORPHOLOGY_PATH, morphology_columns, MORPHOLOGY_COLUMNS, errors)
    validate_columns(STANDARDS_PATH, standards_columns, STANDARDS_COLUMNS, errors)
    validate_columns(VOCABULARY_PATH, vocabulary_columns, VOCABULARY_COLUMNS, errors)
    validate_columns(NEXT_MORPHOLOGY_PATH, next_morphology_columns, MORPHOLOGY_COLUMNS, errors)
    validate_columns(NEXT_STANDARDS_PATH, next_standards_columns, STANDARDS_COLUMNS, errors)
    validate_columns(NEXT_VOCABULARY_PATH, next_vocabulary_columns, VOCABULARY_COLUMNS, errors)
    validate_columns(EXPANSION_MORPHOLOGY_PATH, expansion_morphology_columns, MORPHOLOGY_COLUMNS, errors)
    validate_columns(EXPANSION_STANDARDS_PATH, expansion_standards_columns, STANDARDS_COLUMNS, errors)
    validate_columns(EXPANSION_VOCABULARY_PATH, expansion_vocabulary_columns, VOCABULARY_COLUMNS, errors)
    validate_columns(PEREK1_FINAL_MORPHOLOGY_PATH, perek1_final_morphology_columns, MORPHOLOGY_COLUMNS, errors)
    validate_columns(PEREK1_FINAL_STANDARDS_PATH, perek1_final_standards_columns, STANDARDS_COLUMNS, errors)
    validate_columns(PEREK1_FINAL_VOCABULARY_PATH, perek1_final_vocabulary_columns, VOCABULARY_COLUMNS, errors)

    validate_candidate_rows(
        path=MORPHOLOGY_PATH,
        rows=morphology_rows,
        source_rows=source_rows,
        expected_source_map=repo_relative(SOURCE_MAP_PATH),
        proposed_columns=[
            "proposed_shoresh",
            "proposed_prefixes",
            "proposed_suffixes",
            "proposed_tense",
            "proposed_person",
            "proposed_gender",
            "proposed_number",
            "proposed_part_of_speech",
            "proposed_dikduk_feature",
        ],
        errors=errors,
    )
    validate_candidate_rows(
        path=STANDARDS_PATH,
        rows=standards_rows,
        source_rows=source_rows,
        expected_source_map=repo_relative(SOURCE_MAP_PATH),
        proposed_columns=["proposed_skill_id", "proposed_zekelman_standard", "proposed_standard_level"],
        errors=errors,
    )
    validate_candidate_rows(
        path=VOCABULARY_PATH,
        rows=vocabulary_rows,
        source_rows=source_rows,
        expected_source_map=repo_relative(SOURCE_MAP_PATH),
        proposed_columns=["proposed_translation", "proposed_shoresh_or_keyword", "proposed_vocabulary_category"],
        errors=errors,
    )
    validate_candidate_rows(
        path=NEXT_MORPHOLOGY_PATH,
        rows=next_morphology_rows,
        source_rows=next_source_rows,
        expected_source_map=repo_relative(NEXT_SOURCE_MAP_PATH),
        proposed_columns=[
            "proposed_shoresh",
            "proposed_prefixes",
            "proposed_suffixes",
            "proposed_tense",
            "proposed_person",
            "proposed_gender",
            "proposed_number",
            "proposed_part_of_speech",
            "proposed_dikduk_feature",
        ],
        errors=errors,
    )
    validate_candidate_rows(
        path=NEXT_STANDARDS_PATH,
        rows=next_standards_rows,
        source_rows=next_source_rows,
        expected_source_map=repo_relative(NEXT_SOURCE_MAP_PATH),
        proposed_columns=["proposed_skill_id", "proposed_zekelman_standard", "proposed_standard_level"],
        errors=errors,
    )
    validate_candidate_rows(
        path=NEXT_VOCABULARY_PATH,
        rows=next_vocabulary_rows,
        source_rows=next_source_rows,
        expected_source_map=repo_relative(NEXT_SOURCE_MAP_PATH),
        proposed_columns=["proposed_translation", "proposed_shoresh_or_keyword", "proposed_vocabulary_category"],
        errors=errors,
    )
    validate_candidate_rows(
        path=EXPANSION_MORPHOLOGY_PATH,
        rows=expansion_morphology_rows,
        source_rows=expansion_source_rows,
        expected_source_map=repo_relative(EXPANSION_SOURCE_MAP_PATH),
        proposed_columns=[
            "proposed_shoresh",
            "proposed_prefixes",
            "proposed_suffixes",
            "proposed_tense",
            "proposed_person",
            "proposed_gender",
            "proposed_number",
            "proposed_part_of_speech",
            "proposed_dikduk_feature",
        ],
        errors=errors,
    )
    validate_candidate_rows(
        path=EXPANSION_STANDARDS_PATH,
        rows=expansion_standards_rows,
        source_rows=expansion_source_rows,
        expected_source_map=repo_relative(EXPANSION_SOURCE_MAP_PATH),
        proposed_columns=["proposed_skill_id", "proposed_zekelman_standard", "proposed_standard_level"],
        errors=errors,
    )
    validate_candidate_rows(
        path=EXPANSION_VOCABULARY_PATH,
        rows=expansion_vocabulary_rows,
        source_rows=expansion_source_rows,
        expected_source_map=repo_relative(EXPANSION_SOURCE_MAP_PATH),
        proposed_columns=["proposed_translation", "proposed_shoresh_or_keyword", "proposed_vocabulary_category"],
        errors=errors,
    )
    validate_candidate_rows(
        path=PEREK1_FINAL_MORPHOLOGY_PATH,
        rows=perek1_final_morphology_rows,
        source_rows=perek1_final_source_rows,
        expected_source_map=repo_relative(PEREK1_FINAL_SOURCE_MAP_PATH),
        proposed_columns=[
            "proposed_shoresh",
            "proposed_prefixes",
            "proposed_suffixes",
            "proposed_tense",
            "proposed_person",
            "proposed_gender",
            "proposed_number",
            "proposed_part_of_speech",
            "proposed_dikduk_feature",
        ],
        errors=errors,
    )
    validate_candidate_rows(
        path=PEREK1_FINAL_STANDARDS_PATH,
        rows=perek1_final_standards_rows,
        source_rows=perek1_final_source_rows,
        expected_source_map=repo_relative(PEREK1_FINAL_SOURCE_MAP_PATH),
        proposed_columns=["proposed_skill_id", "proposed_zekelman_standard", "proposed_standard_level"],
        errors=errors,
    )
    validate_candidate_rows(
        path=PEREK1_FINAL_VOCABULARY_PATH,
        rows=perek1_final_vocabulary_rows,
        source_rows=perek1_final_source_rows,
        expected_source_map=repo_relative(PEREK1_FINAL_SOURCE_MAP_PATH),
        proposed_columns=["proposed_translation", "proposed_shoresh_or_keyword", "proposed_vocabulary_category"],
        errors=errors,
    )
    validate_review_sheets(errors)
    for label, (md_path, csv_path) in NEXT_REVIEW_SHEETS.items():
        rows = {
            "morphology": next_morphology_rows,
            "standards": next_standards_rows,
            "vocabulary_shoresh": next_vocabulary_rows,
        }[label]
        validate_pending_review_sheet_bundle(label=label, rows=rows, md_path=md_path, csv_path=csv_path, errors=errors)
    token_split_rows = validate_token_split_standards_artifacts(
        standards_rows=standards_rows,
        errors=errors,
    )
    next_token_split_rows = validate_next_slice_token_split_artifacts(
        standards_rows=next_standards_rows,
        source_rows=next_source_rows,
        errors=errors,
    )
    expansion_token_split_rows = validate_expansion_token_split_artifacts(
        standards_rows=expansion_standards_rows,
        source_rows=expansion_source_rows,
        errors=errors,
    )
    perek1_final_token_split_rows = validate_perek1_final_token_split_artifacts(
        standards_rows=perek1_final_standards_rows,
        source_rows=perek1_final_source_rows,
        errors=errors,
    )
    validate_follow_up_artifacts(
        morphology_rows=morphology_rows,
        standards_rows=standards_rows,
        vocabulary_rows=vocabulary_rows,
        errors=errors,
    )
    validate_reports(errors)
    validate_pilot_completion_report(
        morphology_rows=morphology_rows,
        standards_rows=standards_rows,
        vocabulary_rows=vocabulary_rows,
        token_split_rows=token_split_rows,
        errors=errors,
    )
    validate_next_slice_generation_report(
        morphology_rows=next_morphology_rows,
        vocabulary_rows=next_vocabulary_rows,
        standards_rows=next_standards_rows,
        token_split_rows=next_token_split_rows,
        errors=errors,
    )
    validate_expansion_generation_report(
        morphology_rows=expansion_morphology_rows,
        vocabulary_rows=expansion_vocabulary_rows,
        standards_rows=expansion_standards_rows,
        token_split_rows=expansion_token_split_rows,
        errors=errors,
    )
    validate_perek1_final_generation_report(
        morphology_rows=perek1_final_morphology_rows,
        vocabulary_rows=perek1_final_vocabulary_rows,
        standards_rows=perek1_final_standards_rows,
        token_split_rows=perek1_final_token_split_rows,
        errors=errors,
    )
    validate_perek1_final_review_applied_reports(
        morphology_rows=perek1_final_morphology_rows,
        vocabulary_rows=perek1_final_vocabulary_rows,
        standards_rows=perek1_final_standards_rows,
        token_split_rows=perek1_final_token_split_rows,
        errors=errors,
    )
    validate_perek1_final_review_summary(
        morphology_rows=perek1_final_morphology_rows,
        vocabulary_rows=perek1_final_vocabulary_rows,
        standards_rows=perek1_final_standards_rows,
        token_split_rows=perek1_final_token_split_rows,
        errors=errors,
    )
    validate_perek1_coverage_report(
        next_morphology_rows=next_morphology_rows,
        next_vocabulary_rows=next_vocabulary_rows,
        next_standards_rows=next_standards_rows,
        next_token_split_rows=next_token_split_rows,
        expansion_morphology_rows=expansion_morphology_rows,
        expansion_vocabulary_rows=expansion_vocabulary_rows,
        expansion_standards_rows=expansion_standards_rows,
        expansion_token_split_rows=expansion_token_split_rows,
        perek1_final_morphology_rows=perek1_final_morphology_rows,
        perek1_final_vocabulary_rows=perek1_final_vocabulary_rows,
        perek1_final_standards_rows=perek1_final_standards_rows,
        perek1_final_token_split_rows=perek1_final_token_split_rows,
        errors=errors,
    )
    validate_next_slice_review_applied_reports(
        morphology_rows=next_morphology_rows,
        vocabulary_rows=next_vocabulary_rows,
        standards_rows=next_standards_rows,
        token_split_rows=next_token_split_rows,
        errors=errors,
    )
    validate_next_slice_review_summary(
        morphology_rows=next_morphology_rows,
        vocabulary_rows=next_vocabulary_rows,
        standards_rows=next_standards_rows,
        token_split_rows=next_token_split_rows,
        errors=errors,
    )
    validate_expansion_review_applied_reports(
        morphology_rows=expansion_morphology_rows,
        vocabulary_rows=expansion_vocabulary_rows,
        standards_rows=expansion_standards_rows,
        token_split_rows=expansion_token_split_rows,
        errors=errors,
    )
    validate_expansion_review_summary(
        morphology_rows=expansion_morphology_rows,
        vocabulary_rows=expansion_vocabulary_rows,
        standards_rows=expansion_standards_rows,
        token_split_rows=expansion_token_split_rows,
        errors=errors,
    )
    validate_expansion_mini_completion_report(
        morphology_rows=expansion_morphology_rows,
        vocabulary_rows=expansion_vocabulary_rows,
        standards_rows=expansion_standards_rows,
        token_split_rows=expansion_token_split_rows,
        errors=errors,
    )
    validate_next_slice_mini_completion_report(
        morphology_rows=next_morphology_rows,
        vocabulary_rows=next_vocabulary_rows,
        standards_rows=next_standards_rows,
        token_split_rows=next_token_split_rows,
        errors=errors,
    )

    next_morph_counts = review_status_counts(next_morphology_rows)
    next_vocab_counts = review_status_counts(next_vocabulary_rows)
    next_standards_counts = review_status_counts(next_standards_rows)
    next_token_counts = review_status_counts(next_token_split_rows)
    expected_review_counts = (
        ("morphology", next_morph_counts, 3, 4),
        ("vocabulary_shoresh", next_vocab_counts, 5, 1),
        ("phrase_level_standards", next_standards_counts, 0, 6),
        ("token_split_standards", next_token_counts, 6, 7),
    )
    for label, counts, verified_expected, follow_up_expected in expected_review_counts:
        if counts["yossi_enrichment_verified"] != verified_expected:
            errors.append(
                f"{label}: expected {verified_expected} yossi_enrichment_verified rows, found {counts['yossi_enrichment_verified']}"
            )
        if counts["needs_follow_up"] != follow_up_expected:
            errors.append(f"{label}: expected {follow_up_expected} needs_follow_up rows, found {counts['needs_follow_up']}")
    total_verified = (
        next_morph_counts["yossi_enrichment_verified"]
        + next_vocab_counts["yossi_enrichment_verified"]
        + next_standards_counts["yossi_enrichment_verified"]
        + next_token_counts["yossi_enrichment_verified"]
    )
    total_follow_up = (
        next_morph_counts["needs_follow_up"]
        + next_vocab_counts["needs_follow_up"]
        + next_standards_counts["needs_follow_up"]
        + next_token_counts["needs_follow_up"]
    )
    if total_verified != 14:
        errors.append(f"next-slice review totals: expected 14 verified rows, found {total_verified}")
    if total_follow_up != 18:
        errors.append(f"next-slice review totals: expected 18 follow-up rows, found {total_follow_up}")

    expansion_morph_counts = review_status_counts(expansion_morphology_rows)
    expansion_vocab_counts = review_status_counts(expansion_vocabulary_rows)
    expansion_standards_counts = review_status_counts(expansion_standards_rows)
    expansion_token_counts = review_status_counts(expansion_token_split_rows)
    expansion_expected_review_counts = (
        ("expansion_morphology", expansion_morph_counts, 11, 14),
        ("expansion_vocabulary_shoresh", expansion_vocab_counts, 14, 7),
        ("expansion_phrase_level_standards", expansion_standards_counts, 0, 13),
        ("expansion_token_split_standards", expansion_token_counts, 28, 17),
    )
    for label, counts, verified_expected, follow_up_expected in expansion_expected_review_counts:
        if counts["yossi_enrichment_verified"] != verified_expected:
            errors.append(
                f"{label}: expected {verified_expected} yossi_enrichment_verified rows, found {counts['yossi_enrichment_verified']}"
            )
        if counts["needs_follow_up"] != follow_up_expected:
            errors.append(f"{label}: expected {follow_up_expected} needs_follow_up rows, found {counts['needs_follow_up']}")

    if any(row.get("enrichment_review_status") != "needs_follow_up" for row in expansion_standards_rows):
        errors.append("Bereishis 1:14-1:23 phrase-level standards rows must remain needs_follow_up")
    if any(row.get("yossi_decision") != "needs_follow_up" for row in expansion_standards_rows):
        errors.append("Bereishis 1:14-1:23 phrase-level standards rows must keep yossi_decision=needs_follow_up")

    expansion_rows = (
        expansion_morphology_rows
        + expansion_vocabulary_rows
        + expansion_standards_rows
        + expansion_token_split_rows
    )
    expansion_total_verified = (
        expansion_morph_counts["yossi_enrichment_verified"]
        + expansion_vocab_counts["yossi_enrichment_verified"]
        + expansion_standards_counts["yossi_enrichment_verified"]
        + expansion_token_counts["yossi_enrichment_verified"]
    )
    expansion_total_follow_up = (
        expansion_morph_counts["needs_follow_up"]
        + expansion_vocab_counts["needs_follow_up"]
        + expansion_standards_counts["needs_follow_up"]
        + expansion_token_counts["needs_follow_up"]
    )
    if expansion_total_verified != 53:
        errors.append(f"expansion review totals: expected 53 verified rows, found {expansion_total_verified}")
    if expansion_total_follow_up != 51:
        errors.append(f"expansion review totals: expected 51 follow-up rows, found {expansion_total_follow_up}")

    perek1_final_rows = (
        perek1_final_morphology_rows
        + perek1_final_vocabulary_rows
        + perek1_final_standards_rows
        + perek1_final_token_split_rows
    )
    perek1_final_follow_up = sum(1 for row in perek1_final_rows if row.get("enrichment_review_status") == "needs_follow_up")
    perek1_final_verified = sum(
        1 for row in perek1_final_rows if row.get("enrichment_review_status") == "yossi_enrichment_verified"
    )
    if perek1_final_follow_up <= 0:
        errors.append("Bereishis 1:24-1:31 must retain unresolved follow-up candidates")
    if perek1_final_verified <= 0:
        errors.append("Bereishis 1:24-1:31 review-applied slice must include verified enrichment candidates")

    perek1_final_morph_counts = review_status_counts(perek1_final_morphology_rows)
    perek1_final_vocab_counts = review_status_counts(perek1_final_vocabulary_rows)
    perek1_final_standards_counts = review_status_counts(perek1_final_standards_rows)
    perek1_final_token_counts = review_status_counts(perek1_final_token_split_rows)
    perek1_final_expected_review_counts = (
        ("perek1_final_morphology", perek1_final_morph_counts, 13, 13),
        ("perek1_final_vocabulary_shoresh", perek1_final_vocab_counts, 34, 6),
        ("perek1_final_phrase_level_standards", perek1_final_standards_counts, 0, 14),
        ("perek1_final_token_split_standards", perek1_final_token_counts, 36, 20),
    )
    for label, counts, verified_expected, follow_up_expected in perek1_final_expected_review_counts:
        if counts["yossi_enrichment_verified"] != verified_expected:
            errors.append(
                f"{label}: expected {verified_expected} yossi_enrichment_verified rows, found {counts['yossi_enrichment_verified']}"
            )
        if counts["needs_follow_up"] != follow_up_expected:
            errors.append(f"{label}: expected {follow_up_expected} needs_follow_up rows, found {counts['needs_follow_up']}")
    if perek1_final_verified != 83:
        errors.append(f"perek1-final review totals: expected 83 verified rows, found {perek1_final_verified}")
    if perek1_final_follow_up != 53:
        errors.append(f"perek1-final review totals: expected 53 follow-up rows, found {perek1_final_follow_up}")

    perek2_gate1_counts = validate_perek2_gate1_artifacts(errors)

    return {
        "valid": not errors,
        "readme_path": repo_relative(README_PATH),
        "audit_report_path": repo_relative(AUDIT_REPORT_PATH),
        "pilot_completion_report_path": repo_relative(PILOT_COMPLETION_REPORT_PATH),
        "morphology_candidate_path": repo_relative(MORPHOLOGY_PATH),
        "standards_candidate_path": repo_relative(STANDARDS_PATH),
        "vocabulary_candidate_path": repo_relative(VOCABULARY_PATH),
        "morphology_candidate_count": len(morphology_rows),
        "standards_candidate_count": len(standards_rows),
        "vocabulary_candidate_count": len(vocabulary_rows),
        "token_split_standards_candidate_path": repo_relative(TOKEN_SPLIT_STANDARDS_PATH),
        "token_split_standards_candidate_count": len(token_split_rows),
        "token_split_review_md_path": repo_relative(TOKEN_SPLIT_REVIEW_MD_PATH),
        "token_split_review_csv_path": repo_relative(TOKEN_SPLIT_REVIEW_CSV_PATH),
        "token_split_applied_report_path": repo_relative(TOKEN_SPLIT_APPLIED_REPORT_PATH),
        "review_sheet_count": len(REVIEW_SHEETS),
        "applied_review_report_count": len(APPLIED_REVIEW_REPORTS),
        "follow_up_inventory_path": repo_relative(FOLLOW_UP_INVENTORY_PATH),
        "follow_up_review_md_path": repo_relative(FOLLOW_UP_REVIEW_MD_PATH),
        "follow_up_review_csv_path": repo_relative(FOLLOW_UP_REVIEW_CSV_PATH),
        "follow_up_candidate_count": sum(
            1 for row in morphology_rows + standards_rows + vocabulary_rows if candidate_is_unresolved(row)
        ),
        "next_slice_source_map_path": repo_relative(NEXT_SOURCE_MAP_PATH),
        "next_slice_morphology_candidate_path": repo_relative(NEXT_MORPHOLOGY_PATH),
        "next_slice_standards_candidate_path": repo_relative(NEXT_STANDARDS_PATH),
        "next_slice_vocabulary_candidate_path": repo_relative(NEXT_VOCABULARY_PATH),
        "next_slice_morphology_candidate_count": len(next_morphology_rows),
        "next_slice_standards_candidate_count": len(next_standards_rows),
        "next_slice_vocabulary_candidate_count": len(next_vocabulary_rows),
        "next_slice_token_split_standards_candidate_path": repo_relative(NEXT_TOKEN_SPLIT_STANDARDS_PATH),
        "next_slice_token_split_standards_candidate_count": len(next_token_split_rows),
        "next_slice_generation_report_path": repo_relative(NEXT_GENERATION_REPORT_PATH),
        "next_slice_morphology_applied_report_path": repo_relative(NEXT_MORPHOLOGY_APPLIED_REPORT_PATH),
        "next_slice_vocabulary_applied_report_path": repo_relative(NEXT_VOCAB_APPLIED_REPORT_PATH),
        "next_slice_standards_applied_report_path": repo_relative(NEXT_STANDARDS_APPLIED_REPORT_PATH),
        "next_slice_token_split_applied_report_path": repo_relative(NEXT_TOKEN_SPLIT_APPLIED_REPORT_PATH),
        "next_slice_review_summary_path": repo_relative(NEXT_SLICE_REVIEW_SUMMARY_PATH),
        "next_slice_mini_completion_report_path": repo_relative(NEXT_MINI_COMPLETION_REPORT_PATH),
        "next_slice_follow_up_inventory_path": repo_relative(NEXT_FOLLOW_UP_INVENTORY_PATH),
        "next_slice_total_verified": total_verified,
        "next_slice_total_needs_follow_up": total_follow_up,
        "expansion_source_map_path": repo_relative(EXPANSION_SOURCE_MAP_PATH),
        "expansion_morphology_candidate_path": repo_relative(EXPANSION_MORPHOLOGY_PATH),
        "expansion_standards_candidate_path": repo_relative(EXPANSION_STANDARDS_PATH),
        "expansion_vocabulary_candidate_path": repo_relative(EXPANSION_VOCABULARY_PATH),
        "expansion_token_split_standards_candidate_path": repo_relative(EXPANSION_TOKEN_SPLIT_STANDARDS_PATH),
        "expansion_morphology_candidate_count": len(expansion_morphology_rows),
        "expansion_vocabulary_candidate_count": len(expansion_vocabulary_rows),
        "expansion_standards_candidate_count": len(expansion_standards_rows),
        "expansion_token_split_standards_candidate_count": len(expansion_token_split_rows),
        "expansion_candidate_audit_path": repo_relative(EXPANSION_AUDIT_REPORT_PATH),
        "expansion_generation_report_path": repo_relative(EXPANSION_GENERATION_REPORT_PATH),
        "expansion_morphology_applied_report_path": repo_relative(EXPANSION_MORPHOLOGY_APPLIED_REPORT_PATH),
        "expansion_vocabulary_applied_report_path": repo_relative(EXPANSION_VOCAB_APPLIED_REPORT_PATH),
        "expansion_standards_applied_report_path": repo_relative(EXPANSION_STANDARDS_APPLIED_REPORT_PATH),
        "expansion_token_split_applied_report_path": repo_relative(EXPANSION_TOKEN_SPLIT_APPLIED_REPORT_PATH),
        "expansion_review_summary_path": repo_relative(EXPANSION_SLICE_REVIEW_SUMMARY_PATH),
        "expansion_mini_completion_report_path": repo_relative(EXPANSION_MINI_COMPLETION_REPORT_PATH),
        "expansion_total_candidate_count": len(expansion_rows),
        "expansion_verified_candidate_count": expansion_total_verified,
        "expansion_follow_up_candidate_count": sum(
            1 for row in expansion_rows if row.get("enrichment_review_status") == "needs_follow_up"
        ),
        "perek1_final_source_map_path": repo_relative(PEREK1_FINAL_SOURCE_MAP_PATH),
        "perek1_final_morphology_candidate_path": repo_relative(PEREK1_FINAL_MORPHOLOGY_PATH),
        "perek1_final_standards_candidate_path": repo_relative(PEREK1_FINAL_STANDARDS_PATH),
        "perek1_final_vocabulary_candidate_path": repo_relative(PEREK1_FINAL_VOCABULARY_PATH),
        "perek1_final_token_split_standards_candidate_path": repo_relative(PEREK1_FINAL_TOKEN_SPLIT_STANDARDS_PATH),
        "perek1_final_morphology_candidate_count": len(perek1_final_morphology_rows),
        "perek1_final_vocabulary_candidate_count": len(perek1_final_vocabulary_rows),
        "perek1_final_standards_candidate_count": len(perek1_final_standards_rows),
        "perek1_final_token_split_standards_candidate_count": len(perek1_final_token_split_rows),
        "perek1_final_total_candidate_count": len(perek1_final_rows),
        "perek1_final_verified_candidate_count": perek1_final_verified,
        "perek1_final_follow_up_candidate_count": perek1_final_follow_up,
        "perek1_final_candidate_audit_path": repo_relative(PEREK1_FINAL_AUDIT_REPORT_PATH),
        "perek1_final_generation_report_path": repo_relative(PEREK1_FINAL_GENERATION_REPORT_PATH),
        "perek1_final_morphology_applied_report_path": repo_relative(PEREK1_FINAL_MORPHOLOGY_APPLIED_REPORT_PATH),
        "perek1_final_vocabulary_applied_report_path": repo_relative(PEREK1_FINAL_VOCAB_APPLIED_REPORT_PATH),
        "perek1_final_standards_applied_report_path": repo_relative(PEREK1_FINAL_STANDARDS_APPLIED_REPORT_PATH),
        "perek1_final_token_split_applied_report_path": repo_relative(PEREK1_FINAL_TOKEN_SPLIT_APPLIED_REPORT_PATH),
        "perek1_final_review_summary_path": repo_relative(PEREK1_FINAL_REVIEW_SUMMARY_PATH),
        "perek1_coverage_report_path": repo_relative(PEREK1_COVERAGE_REPORT_PATH),
        "perek2_source_readiness_audit_path": repo_relative(PEREK2_SOURCE_READINESS_AUDIT_PATH),
        "perek2_gate1_report_path": repo_relative(PEREK2_GATE1_REPORT_PATH),
        "perek2_source_row_count": perek2_gate1_counts["source_rows"],
        "perek2_morphology_candidate_path": repo_relative(PEREK2_MORPHOLOGY_PATH),
        "perek2_morphology_candidate_count": perek2_gate1_counts["morphology"],
        "perek2_vocabulary_candidate_path": repo_relative(PEREK2_VOCABULARY_PATH),
        "perek2_vocabulary_candidate_count": perek2_gate1_counts["vocabulary"],
        "perek2_standards_candidate_path": repo_relative(PEREK2_STANDARDS_PATH),
        "perek2_standards_candidate_count": perek2_gate1_counts["standards"],
        "perek2_token_split_candidate_path": repo_relative(PEREK2_TOKEN_SPLIT_STANDARDS_PATH),
        "perek2_token_split_candidate_count": perek2_gate1_counts["token_split"],
        "errors": errors,
    }


def main() -> int:
    summary = validate_source_skill_enrichment()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
