from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path

import scripts.validate_source_skill_enrichment as validator


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
MORPHOLOGY_PATH = (
    ENRICHMENT_DIR / "morphology_candidates" / "bereishis_1_1_to_1_5_morphology_candidates.tsv"
)
STANDARDS_PATH = ENRICHMENT_DIR / "standards_candidates" / "bereishis_1_1_to_1_5_standards_candidates.tsv"
VOCABULARY_PATH = (
    ENRICHMENT_DIR
    / "vocabulary_shoresh_candidates"
    / "bereishis_1_1_to_1_5_vocabulary_shoresh_candidates.tsv"
)
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
NEXT_MORPHOLOGY_REVIEW_MD_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_6_to_1_13_morphology_enrichment_yossi_review_sheet.md"
)
NEXT_MORPHOLOGY_REVIEW_CSV_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_6_to_1_13_morphology_enrichment_yossi_review_sheet.csv"
)
NEXT_VOCAB_REVIEW_MD_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_6_to_1_13_vocabulary_shoresh_enrichment_yossi_review_sheet.md"
)
NEXT_VOCAB_REVIEW_CSV_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_6_to_1_13_vocabulary_shoresh_enrichment_yossi_review_sheet.csv"
)
NEXT_STANDARDS_REVIEW_MD_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_6_to_1_13_standards_enrichment_yossi_review_sheet.md"
)
NEXT_STANDARDS_REVIEW_CSV_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_6_to_1_13_standards_enrichment_yossi_review_sheet.csv"
)
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
NEXT_MORPH_APPLIED_REPORT_PATH = (
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
NEXT_REVIEW_SUMMARY_PATH = (
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
EXPANSION_MORPHOLOGY_REVIEW_MD_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_14_to_1_23_morphology_enrichment_yossi_review_sheet.md"
)
EXPANSION_MORPHOLOGY_REVIEW_CSV_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_14_to_1_23_morphology_enrichment_yossi_review_sheet.csv"
)
EXPANSION_VOCAB_REVIEW_MD_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_14_to_1_23_vocabulary_shoresh_enrichment_yossi_review_sheet.md"
)
EXPANSION_VOCAB_REVIEW_CSV_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_14_to_1_23_vocabulary_shoresh_enrichment_yossi_review_sheet.csv"
)
EXPANSION_STANDARDS_REVIEW_MD_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_14_to_1_23_standards_enrichment_yossi_review_sheet.md"
)
EXPANSION_STANDARDS_REVIEW_CSV_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_14_to_1_23_standards_enrichment_yossi_review_sheet.csv"
)
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
EXPANSION_MORPH_APPLIED_REPORT_PATH = (
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
EXPANSION_REVIEW_SUMMARY_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_14_to_1_23_enrichment_review_summary.md"
)
EXPANSION_MINI_COMPLETION_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_14_to_1_23_enrichment_mini_completion_report.md"
)
PEREK1_FINAL_MORPHOLOGY_REVIEW_MD_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_24_to_1_31_morphology_enrichment_yossi_review_sheet.md"
)
PEREK1_FINAL_MORPHOLOGY_REVIEW_CSV_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_24_to_1_31_morphology_enrichment_yossi_review_sheet.csv"
)
PEREK1_FINAL_VOCAB_REVIEW_MD_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_24_to_1_31_vocabulary_shoresh_enrichment_yossi_review_sheet.md"
)
PEREK1_FINAL_VOCAB_REVIEW_CSV_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_24_to_1_31_vocabulary_shoresh_enrichment_yossi_review_sheet.csv"
)
PEREK1_FINAL_STANDARDS_REVIEW_MD_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_24_to_1_31_standards_enrichment_yossi_review_sheet.md"
)
PEREK1_FINAL_STANDARDS_REVIEW_CSV_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_24_to_1_31_standards_enrichment_yossi_review_sheet.csv"
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
PILOT_COMPLETION_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_1_to_1_5_enrichment_pilot_completion_report.md"
)
PEREK1_COVERAGE_REPORT_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_perek_1_enrichment_review_application_coverage_report.md"
)
CONTRACT_PATH = ROOT / "data" / "standards" / "canonical_skill_contract.json"


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def source_rows_by_id() -> dict[str, dict[str, str]]:
    rows = load_tsv(SOURCE_MAP_PATH)
    return {f"row_{index:03d}": row for index, row in enumerate(rows, 1)}


def all_candidate_rows() -> list[dict[str, str]]:
    return load_tsv(MORPHOLOGY_PATH) + load_tsv(STANDARDS_PATH) + load_tsv(VOCABULARY_PATH)


def next_source_rows_by_id() -> dict[str, dict[str, str]]:
    rows = load_tsv(NEXT_SOURCE_MAP_PATH)
    return {f"row_{index:03d}": row for index, row in enumerate(rows, 1)}


def next_slice_candidate_rows() -> list[dict[str, str]]:
    return load_tsv(NEXT_MORPHOLOGY_PATH) + load_tsv(NEXT_STANDARDS_PATH) + load_tsv(NEXT_VOCABULARY_PATH)


def expansion_source_rows_by_id() -> dict[str, dict[str, str]]:
    rows = load_tsv(EXPANSION_SOURCE_MAP_PATH)
    return {f"row_{index:03d}": row for index, row in enumerate(rows, 1)}


def expansion_candidate_rows() -> list[dict[str, str]]:
    return (
        load_tsv(EXPANSION_MORPHOLOGY_PATH)
        + load_tsv(EXPANSION_STANDARDS_PATH)
        + load_tsv(EXPANSION_VOCABULARY_PATH)
    )


def perek1_final_source_rows_by_id() -> dict[str, dict[str, str]]:
    rows = load_tsv(PEREK1_FINAL_SOURCE_MAP_PATH)
    return {f"row_{index:03d}": row for index, row in enumerate(rows, 1)}


def perek1_final_candidate_rows() -> list[dict[str, str]]:
    return (
        load_tsv(PEREK1_FINAL_MORPHOLOGY_PATH)
        + load_tsv(PEREK1_FINAL_STANDARDS_PATH)
        + load_tsv(PEREK1_FINAL_VOCABULARY_PATH)
    )


class SourceSkillEnrichmentTests(unittest.TestCase):
    def test_validator_passes(self):
        summary = validator.validate_source_skill_enrichment()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["morphology_candidate_count"], 5)
        self.assertEqual(summary["standards_candidate_count"], 6)
        self.assertEqual(summary["vocabulary_candidate_count"], 6)
        self.assertEqual(summary["token_split_standards_candidate_count"], 10)
        self.assertEqual(summary["review_sheet_count"], 3)
        self.assertEqual(summary["applied_review_report_count"], 3)
        self.assertEqual(summary["follow_up_candidate_count"], 10)
        self.assertEqual(
            summary["pilot_completion_report_path"],
            "data/source_skill_enrichment/reports/bereishis_1_1_to_1_5_enrichment_pilot_completion_report.md",
        )
        self.assertEqual(summary["next_slice_morphology_candidate_count"], 7)
        self.assertEqual(summary["next_slice_vocabulary_candidate_count"], 6)
        self.assertEqual(summary["next_slice_standards_candidate_count"], 6)
        self.assertEqual(summary["next_slice_token_split_standards_candidate_count"], 13)
        self.assertEqual(
            summary["next_slice_generation_report_path"],
            "data/source_skill_enrichment/reports/bereishis_1_6_to_1_13_enrichment_candidate_generation_report.md",
        )
        self.assertEqual(summary["next_slice_total_verified"], 14)
        self.assertEqual(summary["next_slice_total_needs_follow_up"], 18)
        self.assertEqual(
            summary["next_slice_mini_completion_report_path"],
            "data/source_skill_enrichment/reports/bereishis_1_6_to_1_13_enrichment_mini_completion_report.md",
        )
        self.assertEqual(summary["expansion_morphology_candidate_count"], 25)
        self.assertEqual(summary["expansion_vocabulary_candidate_count"], 21)
        self.assertEqual(summary["expansion_standards_candidate_count"], 13)
        self.assertEqual(summary["expansion_token_split_standards_candidate_count"], 45)
        self.assertEqual(summary["expansion_total_candidate_count"], 104)
        self.assertEqual(summary["expansion_verified_candidate_count"], 53)
        self.assertEqual(summary["expansion_follow_up_candidate_count"], 51)
        self.assertEqual(
            summary["expansion_mini_completion_report_path"],
            "data/source_skill_enrichment/reports/bereishis_1_14_to_1_23_enrichment_mini_completion_report.md",
        )
        self.assertEqual(summary["perek1_final_morphology_candidate_count"], 26)
        self.assertEqual(summary["perek1_final_vocabulary_candidate_count"], 40)
        self.assertEqual(summary["perek1_final_standards_candidate_count"], 14)
        self.assertEqual(summary["perek1_final_token_split_standards_candidate_count"], 56)
        self.assertEqual(summary["perek1_final_total_candidate_count"], 136)
        self.assertEqual(summary["perek1_final_follow_up_candidate_count"], 53)
        self.assertEqual(
            summary["perek1_final_generation_report_path"],
            "data/source_skill_enrichment/reports/bereishis_1_24_to_1_31_enrichment_candidate_generation_report.md",
        )
        self.assertEqual(
            summary["perek1_coverage_report_path"],
            "data/source_skill_enrichment/reports/bereishis_perek_1_enrichment_review_application_coverage_report.md",
        )

    def test_enrichment_readme_and_audit_exist(self):
        readme = ENRICHMENT_DIR / "README.md"
        audit = ENRICHMENT_DIR / "reports" / "morphology_standards_enrichment_audit.md"
        self.assertTrue(readme.exists())
        self.assertTrue(audit.exists())
        readme_text = readme.read_text(encoding="utf-8")
        audit_text = audit.read_text(encoding="utf-8")
        self.assertIn("The verified source-to-skill maps remain the phrase-level extraction-verified source truth", readme_text)
        self.assertIn("Question eligibility", readme_text)
        self.assertIn("Separate later gate", readme_text)
        self.assertIn("Pilot Follow-Up Evidence Status", readme_text)
        self.assertIn("10 candidates unresolved before evidence strengthening", readme_text)
        self.assertIn("did not verify any unresolved candidate", readme_text)
        self.assertIn("Pilot Completion Milestone", readme_text)
        self.assertIn("bereishis_1_1_to_1_5_enrichment_pilot_completion_report.md", readme_text)
        self.assertIn("pilot is completed as a pattern, not fully resolved", readme_text)
        self.assertIn("no question/protected-preview/reviewed-bank/runtime approval exists", readme_text)
        self.assertIn("Bereishis 1:6-1:13 Review-Applied Slice", readme_text)
        self.assertIn("enrichment review only", readme_text)
        self.assertIn("all gates remain closed", readme_text)
        self.assertIn("bereishis_1_6_to_1_13_morphology_candidates.tsv", readme_text)
        self.assertIn("bereishis_1_6_to_1_13_enrichment_candidate_generation_report.md", readme_text)
        self.assertIn("bereishis_1_6_to_1_13_morphology_enrichment_yossi_review_applied.md", readme_text)
        self.assertIn("bereishis_1_6_to_1_13_enrichment_review_summary.md", readme_text)
        self.assertIn("bereishis_1_6_to_1_13_enrichment_mini_completion_report.md", readme_text)
        self.assertIn("verified: 14", readme_text)
        self.assertIn("needs_follow_up: 18", readme_text)
        self.assertIn("Unresolved items remain follow-up by design", readme_text)
        self.assertIn("next recommended slice is Bereishis 1:14-1:23", readme_text)
        self.assertIn("Bereishis 1:14-1:23 Review-Applied Slice", readme_text)
        self.assertIn("morphology: 25", readme_text)
        self.assertIn("vocabulary_shoresh: 21", readme_text)
        self.assertIn("phrase-level standards: 13", readme_text)
        self.assertIn("token-split standards: 45", readme_text)
        self.assertIn("total candidates: 104", readme_text)
        self.assertIn("verified: 53", readme_text)
        self.assertIn("needs_follow_up: 51", readme_text)
        self.assertIn("bereishis_1_14_to_1_23_enrichment_candidate_audit.md", readme_text)
        self.assertIn("bereishis_1_14_to_1_23_enrichment_candidate_generation_report.md", readme_text)
        self.assertIn("bereishis_1_14_to_1_23_morphology_enrichment_yossi_review_applied.md", readme_text)
        self.assertIn("bereishis_1_14_to_1_23_vocabulary_shoresh_enrichment_yossi_review_applied.md", readme_text)
        self.assertIn("bereishis_1_14_to_1_23_standards_enrichment_yossi_review_applied.md", readme_text)
        self.assertIn("bereishis_1_14_to_1_23_token_split_standards_yossi_review_applied.md", readme_text)
        self.assertIn("bereishis_1_14_to_1_23_enrichment_review_summary.md", readme_text)
        self.assertIn("bereishis_1_14_to_1_23_enrichment_mini_completion_report.md", readme_text)
        self.assertIn("Unresolved items remain follow-up by design and all gates remain closed across the slice.", readme_text)
        self.assertIn("Next recommended slice: Bereishis 1:24-1:31", readme_text)
        self.assertIn("Bereishis 1:24-1:31 Review-Applied Slice", readme_text)
        self.assertIn("completes candidate coverage for Bereishis Perek 1", readme_text)
        self.assertIn("morphology: 26", readme_text)
        self.assertIn("vocabulary_shoresh: 40", readme_text)
        self.assertIn("phrase-level standards: 14", readme_text)
        self.assertIn("token-split standards: 56", readme_text)
        self.assertIn("total candidates: 136", readme_text)
        self.assertIn("verified: 83", readme_text)
        self.assertIn("needs_follow_up: 53", readme_text)
        self.assertIn("Bereishis Perek 1 Enrichment Review-Application Coverage", readme_text)
        self.assertIn("reports/bereishis_perek_1_enrichment_review_application_coverage_report.md", readme_text)
        self.assertIn("coverage exists across Bereishis 1:1-1:31", readme_text)
        self.assertIn("unresolved items remain follow-up by design", readme_text)
        self.assertIn("This is enrichment review only.", readme_text)
        self.assertIn("bereishis_1_24_to_1_31_enrichment_candidate_audit.md", readme_text)
        self.assertIn("bereishis_1_24_to_1_31_enrichment_candidate_generation_report.md", readme_text)
        self.assertIn("bereishis_1_24_to_1_31_token_split_standards_yossi_review_sheet.csv", readme_text)
        self.assertIn("What Should Not Be Auto-Filled", audit_text)
        self.assertIn("reviewed-bank examples; reference only", audit_text)
        self.assertIn("Do not backfill all morphology fields", audit_text)

    def test_pilot_completion_report_exists_and_matches_candidate_counts(self):
        self.assertTrue(PILOT_COMPLETION_REPORT_PATH.exists())
        report_text = PILOT_COMPLETION_REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn(
            "Bereishis 1:1-1:5 now has a reviewed enrichment pilot pattern across morphology, vocabulary/shoresh, and standards.",
            report_text,
        )
        self.assertIn("Bereishis 1:6-1:13", report_text)
        self.assertIn("Hebrew corruption was detected in the token-split TSV/CSV", report_text)
        self.assertIn("validation now checks real Hebrew rendering", report_text)
        safety_summary = (
            "question_allowed:needs_review/"
            "protected_preview_allowed:false/"
            "reviewed_bank_allowed:false/"
            "runtime_allowed:false"
        )

        def status_counts(rows: list[dict[str, str]]) -> dict[str, int]:
            counts = {
                "yossi_enrichment_verified": 0,
                "needs_follow_up": 0,
                "source_only": 0,
                "blocked_unclear_evidence": 0,
            }
            for row in rows:
                status = row["enrichment_review_status"]
                if status in counts:
                    counts[status] += 1
            return counts

        morphology_rows = load_tsv(MORPHOLOGY_PATH)
        vocabulary_rows = load_tsv(VOCABULARY_PATH)
        standards_rows = load_tsv(STANDARDS_PATH)
        token_split_rows = load_tsv(TOKEN_SPLIT_STANDARDS_PATH)
        morphology_counts = status_counts(morphology_rows)
        vocabulary_counts = status_counts(vocabulary_rows)
        standards_counts = status_counts(standards_rows)
        token_split_counts = status_counts(token_split_rows)
        superseded_phrase_count = sum(
            1
            for row in standards_rows
            if "superseded by token-split follow-up candidates" in row["evidence_note"].lower()
        )
        for expected_line in (
            f"- morphology: total={len(morphology_rows)}; verified={morphology_counts['yossi_enrichment_verified']}; needs_follow_up={morphology_counts['needs_follow_up']}; source_only={morphology_counts['source_only']}; blocked={morphology_counts['blocked_unclear_evidence']}; safety_gates={safety_summary}",
            f"- vocabulary_shoresh: total={len(vocabulary_rows)}; verified={vocabulary_counts['yossi_enrichment_verified']}; needs_follow_up={vocabulary_counts['needs_follow_up']}; source_only={vocabulary_counts['source_only']}; blocked={vocabulary_counts['blocked_unclear_evidence']}; safety_gates={safety_summary}",
            f"- phrase_level_standards: total={len(standards_rows)}; verified={standards_counts['yossi_enrichment_verified']}; needs_follow_up={standards_counts['needs_follow_up']}; superseded_unresolved={superseded_phrase_count}; safety_gates={safety_summary}",
            f"- token_split_standards: total={len(token_split_rows)}; verified={token_split_counts['yossi_enrichment_verified']}; needs_follow_up={token_split_counts['needs_follow_up']}; source_only={token_split_counts['source_only']}; blocked={token_split_counts['blocked_unclear_evidence']}; safety_gates={safety_summary}",
        ):
            self.assertIn(expected_line, report_text)

        for required_item in (
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
            self.assertIn(required_item, report_text)

    def test_candidate_files_have_required_columns(self):
        for path, expected_columns in (
            (MORPHOLOGY_PATH, validator.MORPHOLOGY_COLUMNS),
            (STANDARDS_PATH, validator.STANDARDS_COLUMNS),
            (VOCABULARY_PATH, validator.VOCABULARY_COLUMNS),
        ):
            with self.subTest(path=path):
                with path.open("r", encoding="utf-8", newline="") as handle:
                    columns = list(csv.DictReader(handle, delimiter="\t").fieldnames or [])
                self.assertEqual(columns, expected_columns)

    def test_candidates_link_to_verified_source_to_skill_rows(self):
        source_rows = source_rows_by_id()
        for row in all_candidate_rows():
            with self.subTest(candidate=row["candidate_id"]):
                linked = source_rows[row["source_row_id"]]
                self.assertEqual(row["source_map_file"], "data/verified_source_skill_maps/bereishis_1_1_to_1_5_source_to_skill_map.tsv")
                self.assertEqual(linked["extraction_review_status"], "yossi_extraction_verified")
                self.assertEqual(row["ref"], linked["ref"])
                self.assertEqual(row["hebrew_phrase"], linked["hebrew_word_or_phrase"])

    def test_candidates_record_review_decisions_and_safety_closed(self):
        allowed_statuses = validator.ALLOWED_REVIEW_STATUSES
        for row in all_candidate_rows():
            with self.subTest(candidate=row["candidate_id"]):
                self.assertIn(row["enrichment_review_status"], allowed_statuses)
                self.assertIn(row["confidence"], validator.ALLOWED_CONFIDENCE)
                self.assertIn(row["yossi_decision"], validator.ALLOWED_YOSSI_DECISIONS)
                if row["enrichment_review_status"] == "yossi_enrichment_verified":
                    self.assertEqual(row["yossi_decision"], "verified")
                    self.assertTrue(row["yossi_notes"])
                if row["yossi_decision"].startswith("fix_"):
                    self.assertNotEqual(row["enrichment_review_status"], "yossi_enrichment_verified")
                self.assertEqual(row["question_allowed"], "needs_review")
                self.assertEqual(row["protected_preview_allowed"], "false")
                self.assertEqual(row["runtime_allowed"], "false")
                self.assertEqual(row["reviewed_bank_allowed"], "false")

    def test_yossi_review_decision_counts_are_mixed_not_blanket_verified(self):
        decision_counts = {}
        status_counts = {}
        for row in all_candidate_rows():
            decision_counts[row["yossi_decision"]] = decision_counts.get(row["yossi_decision"], 0) + 1
            status_counts[row["enrichment_review_status"]] = status_counts.get(row["enrichment_review_status"], 0) + 1
        self.assertEqual(decision_counts.get("verified"), 7)
        self.assertEqual(decision_counts.get("needs_follow_up"), 9)
        self.assertEqual(decision_counts.get("fix_vocabulary"), 1)
        self.assertEqual(status_counts.get("yossi_enrichment_verified"), 7)
        self.assertEqual(status_counts.get("needs_follow_up"), 10)

    def test_review_sheets_exist_are_utf8_bom_and_safety_scoped(self):
        for label, (md_path, csv_path) in validator.REVIEW_SHEETS.items():
            with self.subTest(label=label):
                self.assertTrue(md_path.exists())
                self.assertTrue(csv_path.exists())
                self.assertTrue(csv_path.read_bytes().startswith(b"\xef\xbb\xbf"))
                md_text = md_path.read_text(encoding="utf-8")
                self.assertIn("Yossi is reviewing enrichment candidates only.", md_text)
                self.assertIn("not question approval", md_text)
                self.assertIn("not protected-preview approval", md_text)
                self.assertIn("not reviewed-bank approval", md_text)
                self.assertIn("not runtime approval", md_text)
                self.assertIn("not student-facing approval", md_text)
                for decision in validator.ALLOWED_YOSSI_DECISIONS - {""}:
                    self.assertIn(f"`{decision}`", md_text)
                with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
                    rows = list(csv.DictReader(handle))
                self.assertTrue(rows)
                self.assertEqual(list(rows[0].keys()), validator.REVIEW_CSV_COLUMNS)
                self.assertTrue(all(row["yossi_decision"] == "" for row in rows))
                self.assertTrue(all(row["yossi_notes"] == "" for row in rows))
                self.assertTrue(all("not question" in row["safety_warning"] for row in rows))
                self.assertTrue(all("not runtime" in row["safety_warning"] for row in rows))

    def test_first_150_vocabulary_evidence_is_candidate_only(self):
        rows = load_tsv(VOCABULARY_PATH)
        first_150_rows = [row for row in rows if row["first_150_match"] == "true"]
        self.assertGreaterEqual(len(first_150_rows), 3)
        for row in first_150_rows:
            with self.subTest(candidate=row["candidate_id"]):
                self.assertTrue(row["first_150_entry_id"])
                note = row["evidence_note"].lower()
                self.assertTrue("candidate evidence only" in note or "does not become automatically verified" in note)
                self.assertEqual(row["question_allowed"], "needs_review")
                self.assertEqual(row["protected_preview_allowed"], "false")
                self.assertEqual(row["runtime_allowed"], "false")
                self.assertEqual(row["reviewed_bank_allowed"], "false")
        bara = next(row for row in rows if row["candidate_id"] == "vocab_b1_1_r002_t001")
        self.assertEqual(bara["yossi_decision"], "fix_vocabulary")
        self.assertEqual(bara["enrichment_review_status"], "needs_follow_up")
        self.assertEqual(bara["first_150_match"], "false")
        self.assertIn("First 150 record", bara["evidence_note"])

    def test_applied_review_reports_exist_and_preserve_boundaries(self):
        for path in validator.APPLIED_REVIEW_REPORTS.values():
            with self.subTest(path=path):
                self.assertTrue(path.exists())
                text = path.read_text(encoding="utf-8")
                self.assertIn("This is not question approval", text)
                self.assertIn("not protected-preview approval", text)
                self.assertIn("not reviewed-bank approval", text)
                self.assertIn("not runtime approval", text)
                self.assertIn("not student-facing approval", text)
                self.assertIn("No source-to-skill map rows were changed", text)

    def test_koren_and_reviewed_bank_are_not_auto_approval_sources(self):
        for row in all_candidate_rows():
            with self.subTest(candidate=row["candidate_id"]):
                self.assertNotIn("koren primary", row["evidence_note"].lower())
                self.assertNotIn("commercial_use_approved", row["evidence_note"].lower())
                if "reviewed_bank" in row["evidence_source_id"].lower():
                    self.assertIn("reference only", row["evidence_note"].lower())

    def test_follow_up_inventory_and_review_sheets_exist(self):
        self.assertTrue(FOLLOW_UP_INVENTORY_PATH.exists())
        self.assertTrue(FOLLOW_UP_REVIEW_MD_PATH.exists())
        self.assertTrue(FOLLOW_UP_REVIEW_CSV_PATH.exists())
        self.assertTrue(FOLLOW_UP_REVIEW_CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf"))

        inventory_text = FOLLOW_UP_INVENTORY_PATH.read_text(encoding="utf-8")
        md_text = FOLLOW_UP_REVIEW_MD_PATH.read_text(encoding="utf-8")
        self.assertIn("This inventory lists exactly the unresolved candidates", inventory_text)
        self.assertIn("Data hygiene audit", inventory_text)
        self.assertIn("data/standards/canonical_skill_contract.json", inventory_text)
        self.assertIn("Vocabulary/Shoresh Follow-Up", md_text)
        self.assertIn("Morphology Follow-Up", md_text)
        self.assertIn("Standards Follow-Up", md_text)
        self.assertIn("This is enrichment follow-up review only", md_text)
        self.assertIn("data/standards/canonical_skill_contract.json", md_text)
        self.assertIn("not question approval", md_text)
        self.assertIn("protected-preview approval", md_text)
        self.assertIn("reviewed-bank approval", md_text)
        self.assertIn("runtime approval", md_text)
        self.assertIn("student-facing approval", md_text)

    def test_token_split_standards_artifacts_exist_and_are_safety_scoped(self):
        self.assertTrue(TOKEN_SPLIT_STANDARDS_PATH.exists())
        self.assertTrue(TOKEN_SPLIT_AUDIT_PATH.exists())
        self.assertTrue(TOKEN_SPLIT_REVIEW_MD_PATH.exists())
        self.assertTrue(TOKEN_SPLIT_REVIEW_CSV_PATH.exists())
        self.assertTrue(TOKEN_SPLIT_APPLIED_REPORT_PATH.exists())
        self.assertTrue(TOKEN_SPLIT_REVIEW_CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf"))

        audit_text = TOKEN_SPLIT_AUDIT_PATH.read_text(encoding="utf-8")
        review_text = TOKEN_SPLIT_REVIEW_MD_PATH.read_text(encoding="utf-8")
        applied_text = TOKEN_SPLIT_APPLIED_REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn("No token-level standards candidate in this audit is verified", audit_text)
        self.assertIn("no question, protected-preview, reviewed-bank, runtime, or student-facing gate was opened", audit_text)
        self.assertIn("This is standards enrichment follow-up only", review_text)
        self.assertIn("question approval", review_text)
        self.assertIn("protected-preview approval", review_text)
        self.assertIn("reviewed-bank approval", review_text)
        self.assertIn("runtime approval", review_text)
        self.assertIn("student-facing approval", review_text)
        self.assertNotIn("???", review_text)
        self.assertIn("total token-split candidates reviewed: 10", applied_text)
        self.assertIn("verified candidates: 7", applied_text)
        self.assertIn("needs_follow_up candidates: 3", applied_text)
        self.assertIn("Hebrew rendering check result", applied_text)

    def test_follow_up_sheet_lists_only_unresolved_candidates(self):
        candidates = all_candidate_rows()
        unresolved_ids = {
            row["candidate_id"]
            for row in candidates
            if row["enrichment_review_status"] != "yossi_enrichment_verified"
            or row["yossi_decision"].startswith("fix_")
        }
        verified_ids = {
            row["candidate_id"]
            for row in candidates
            if row["enrichment_review_status"] == "yossi_enrichment_verified"
        }
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        canonical_by_id = {record["canonical_skill_id"]: record for record in contract["canonical_skills"]}
        with FOLLOW_UP_REVIEW_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(list(rows[0].keys()), validator.FOLLOW_UP_CSV_COLUMNS)
        csv_ids = {row["candidate_id"] for row in rows}
        self.assertEqual(csv_ids, unresolved_ids)
        self.assertEqual(len(csv_ids), 10)
        self.assertTrue(all(row["yossi_decision"] == "" for row in rows))
        self.assertTrue(all(row["yossi_notes"] == "" for row in rows))
        self.assertTrue(all(row["recommended_decision"] != "verified" for row in rows))
        for row in rows:
            with self.subTest(candidate=row["candidate_id"]):
                canonical_skill_ids = [item.strip() for item in row["canonical_skill_ids"].split(";") if item.strip()]
                canonical_standard_ids = [item.strip() for item in row["canonical_standard_ids"].split(";") if item.strip()]
                self.assertTrue(canonical_skill_ids)
                self.assertTrue(canonical_standard_ids)
                self.assertTrue(row["contract_mapping_notes"].strip())
                for canonical_skill_id in canonical_skill_ids:
                    self.assertIn(canonical_skill_id, canonical_by_id)
                for standard_id in canonical_standard_ids:
                    self.assertTrue(
                        any(
                            standard_id in canonical_by_id[canonical_skill_id]["related_zekelman_standard_ids"]
                            for canonical_skill_id in canonical_skill_ids
                        )
                    )

        inventory_text = FOLLOW_UP_INVENTORY_PATH.read_text(encoding="utf-8")
        md_text = FOLLOW_UP_REVIEW_MD_PATH.read_text(encoding="utf-8")
        for candidate_id in unresolved_ids:
            with self.subTest(candidate=candidate_id):
                self.assertIn(candidate_id, inventory_text)
                self.assertIn(candidate_id, md_text)
        for candidate_id in verified_ids:
            with self.subTest(verified_candidate=candidate_id):
                self.assertNotIn(f"### `{candidate_id}`", inventory_text)
                self.assertNotIn(f"### `{candidate_id}`", md_text)

    def test_token_split_candidates_map_to_contract_and_keep_gates_closed(self):
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        canonical_by_id = {record["canonical_skill_id"]: record for record in contract["canonical_skills"]}
        valid_standards = {
            standard_id
            for record in contract["canonical_skills"]
            for standard_id in record["related_zekelman_standard_ids"]
        }
        rows = load_tsv(TOKEN_SPLIT_STANDARDS_PATH)
        self.assertEqual(len(rows), 10)
        parent_ids = {row["candidate_id"] for row in load_tsv(STANDARDS_PATH)}
        self.assertEqual({row["parent_candidate_id"] for row in rows}, {"std_b1_1_r002", "std_b1_1_r003", "std_b1_3_r013", "std_b1_5_r020"})
        verified_count = 0
        follow_up_count = 0
        for row in rows:
            with self.subTest(candidate=row["candidate_id"]):
                self.assertIn(row["parent_candidate_id"], parent_ids)
                self.assertIn(row["canonical_skill_id"], canonical_by_id)
                self.assertIn(row["canonical_standard_anchor"], valid_standards)
                self.assertEqual(row["canonical_standard_anchor"], row["proposed_zekelman_standard"])
                self.assertIn(row["canonical_standard_anchor"], canonical_by_id[row["canonical_skill_id"]]["related_zekelman_standard_ids"])
                self.assertNotIn("?", row["hebrew_token"])
                self.assertNotIn("?", row["clean_hebrew_no_nikud"])
                self.assertTrue(row["yossi_notes"])
                self.assertEqual(row["question_allowed"], "needs_review")
                self.assertEqual(row["protected_preview_allowed"], "false")
                self.assertEqual(row["reviewed_bank_allowed"], "false")
                self.assertEqual(row["runtime_allowed"], "false")
                if row["yossi_decision"] == "verified":
                    verified_count += 1
                    self.assertEqual(row["enrichment_review_status"], "yossi_enrichment_verified")
                elif row["yossi_decision"] == "needs_follow_up":
                    follow_up_count += 1
                    self.assertEqual(row["enrichment_review_status"], "needs_follow_up")
                else:
                    self.fail(f"unexpected yossi_decision {row['yossi_decision']!r}")
        self.assertEqual(verified_count, 7)
        self.assertEqual(follow_up_count, 3)

    def test_parent_bundled_rows_remain_unresolved_after_token_split_preparation(self):
        by_id = {row["candidate_id"]: row for row in load_tsv(STANDARDS_PATH)}
        for candidate_id in ("std_b1_1_r002", "std_b1_1_r003", "std_b1_3_r013", "std_b1_5_r020"):
            with self.subTest(candidate=candidate_id):
                row = by_id[candidate_id]
                self.assertEqual(row["enrichment_review_status"], "needs_follow_up")
                self.assertEqual(row["yossi_decision"], "needs_follow_up")
                self.assertIn("superseded by token-split follow-up candidates", row["evidence_note"])
                self.assertIn("remains unresolved", row["yossi_notes"])
                self.assertEqual(row["question_allowed"], "needs_review")
                self.assertEqual(row["protected_preview_allowed"], "false")
                self.assertEqual(row["reviewed_bank_allowed"], "false")
                self.assertEqual(row["runtime_allowed"], "false")

    def test_token_split_review_csv_matches_applied_tsv(self):
        token_rows = {row["candidate_id"]: row for row in load_tsv(TOKEN_SPLIT_STANDARDS_PATH)}
        with TOKEN_SPLIT_REVIEW_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(list(rows[0].keys()), validator.TOKEN_SPLIT_REVIEW_CSV_COLUMNS)
        self.assertEqual({row["candidate_id"] for row in rows}, set(token_rows))
        for row in rows:
            with self.subTest(candidate=row["candidate_id"]):
                token_row = token_rows[row["candidate_id"]]
                self.assertEqual(row["hebrew_token"], token_row["hebrew_token"])
                self.assertEqual(row["parent_phrase"], token_row["hebrew_phrase"])
                self.assertEqual(row["current_status"], token_row["enrichment_review_status"])
                self.assertEqual(row["yossi_decision"], token_row["yossi_decision"])
                self.assertEqual(row["yossi_notes"], token_row["yossi_notes"])
                self.assertEqual(row["recommended_decision"], "needs_follow_up")

    def test_follow_up_evidence_strengthening_did_not_verify_unresolved_candidates(self):
        by_id = {row["candidate_id"]: row for row in all_candidate_rows()}
        for candidate_id in (
            "morph_b1_2_r004_t001",
            "morph_b1_3_r013_t001",
            "vocab_b1_1_r002_t001",
            "vocab_b1_3_r013_t002",
            "vocab_b1_2_r007_t001",
            "std_b1_1_r002",
            "std_b1_1_r003",
            "std_b1_3_r013",
            "std_b1_5_r020",
            "std_b1_2_r010",
        ):
            with self.subTest(candidate=candidate_id):
                self.assertNotEqual(by_id[candidate_id]["enrichment_review_status"], "yossi_enrichment_verified")
                self.assertNotEqual(by_id[candidate_id]["yossi_decision"], "verified")
                self.assertEqual(by_id[candidate_id]["question_allowed"], "needs_review")
                self.assertEqual(by_id[candidate_id]["protected_preview_allowed"], "false")
                self.assertEqual(by_id[candidate_id]["runtime_allowed"], "false")
                self.assertEqual(by_id[candidate_id]["reviewed_bank_allowed"], "false")

    def test_follow_up_vocabulary_morphology_and_standards_notes_are_precise(self):
        by_id = {row["candidate_id"]: row for row in all_candidate_rows()}

        bara = by_id["vocab_b1_1_r002_t001"]
        self.assertIn("vocab_entry.bara", bara["evidence_source_id"])
        self.assertIn("word_parse.bereishis_1_1.bara", bara["evidence_source_id"])
        self.assertEqual(bara["first_150_match"], "false")
        self.assertIn("First 150 remains unconfirmed", bara["evidence_note"])

        or_row = by_id["vocab_b1_3_r013_t002"]
        self.assertIn("vocab_entry.or", or_row["evidence_source_id"])
        self.assertEqual(or_row["first_150_match"], "true")
        self.assertIn("manual_sample_only", or_row["evidence_note"])

        darkness = by_id["vocab_b1_2_r007_t001"]
        self.assertIn("source_to_skill_map_row_007", darkness["evidence_source_id"])
        self.assertIn("no exact First 150", darkness["evidence_note"])

        vehaaretz = by_id["morph_b1_2_r004_t001"]
        self.assertIn("DK-CONJ-001", vehaaretz["evidence_source_id"])
        self.assertIn("DK-ARTICLE-001", vehaaretz["evidence_source_id"])
        self.assertEqual(vehaaretz["confidence"], "medium")
        self.assertIn("does not by itself verify", vehaaretz["evidence_note"])

        yehi = by_id["morph_b1_3_r013_t001"]
        self.assertIn("data/word_bank.json", yehi["evidence_source_id"])
        self.assertIn("3.07", yehi["evidence_source_id"])
        self.assertIn("No trusted reviewed source", yehi["evidence_note"])

        for candidate_id in ("std_b1_1_r002", "std_b1_1_r003", "std_b1_3_r013", "std_b1_5_r020"):
            with self.subTest(candidate=candidate_id):
                note = by_id[candidate_id]["evidence_note"].lower()
                self.assertIn("token-level", note)
                self.assertTrue("split" in note or "separate" in note)

        merachefet = by_id["std_b1_2_r010"]
        self.assertIn("Evidence gap remains", merachefet["evidence_note"])
        self.assertIn("needs_mapping_review", merachefet["evidence_note"])

    def test_next_slice_source_map_is_verified_and_safety_closed(self):
        rows = load_tsv(NEXT_SOURCE_MAP_PATH)
        self.assertEqual(len(rows), 37)
        self.assertTrue(all(row["extraction_review_status"] == "yossi_extraction_verified" for row in rows))
        self.assertEqual({row["question_allowed"] for row in rows}, {"needs_review"})
        self.assertEqual({row["runtime_allowed"] for row in rows}, {"false"})
        self.assertEqual({row["protected_preview_allowed"] for row in rows}, {"false"})
        self.assertEqual({row["reviewed_bank_allowed"] for row in rows}, {"false"})

    def test_next_slice_candidate_files_have_required_columns(self):
        for path, expected_columns in (
            (NEXT_MORPHOLOGY_PATH, validator.MORPHOLOGY_COLUMNS),
            (NEXT_STANDARDS_PATH, validator.STANDARDS_COLUMNS),
            (NEXT_VOCABULARY_PATH, validator.VOCABULARY_COLUMNS),
            (NEXT_TOKEN_SPLIT_STANDARDS_PATH, validator.TOKEN_SPLIT_STANDARDS_COLUMNS),
        ):
            with self.subTest(path=path):
                with path.open("r", encoding="utf-8", newline="") as handle:
                    columns = list(csv.DictReader(handle, delimiter="\t").fieldnames or [])
                self.assertEqual(columns, expected_columns)

    def test_next_slice_candidates_link_to_verified_source_rows_and_stay_review_only(self):
        source_rows = next_source_rows_by_id()
        for row in next_slice_candidate_rows():
            with self.subTest(candidate=row["candidate_id"]):
                linked = source_rows[row["source_row_id"]]
                self.assertEqual(
                    row["source_map_file"],
                    "data/verified_source_skill_maps/bereishis_1_6_to_1_13_source_to_skill_map.tsv",
                )
                self.assertEqual(linked["extraction_review_status"], "yossi_extraction_verified")
                self.assertEqual(row["ref"], linked["ref"])
                self.assertEqual(row["hebrew_phrase"], linked["hebrew_word_or_phrase"])
                self.assertIn(row["enrichment_review_status"], validator.ALLOWED_REVIEW_STATUSES)
                self.assertIn(row["yossi_decision"], validator.ALLOWED_YOSSI_DECISIONS)
                if row["enrichment_review_status"] == "yossi_enrichment_verified":
                    self.assertEqual(row["yossi_decision"], "verified")
                    self.assertTrue(row["yossi_notes"])
                self.assertEqual(row["question_allowed"], "needs_review")
                self.assertEqual(row["protected_preview_allowed"], "false")
                self.assertEqual(row["runtime_allowed"], "false")
                self.assertEqual(row["reviewed_bank_allowed"], "false")

    def test_next_slice_review_sheets_exist_are_utf8_bom_and_blank_before_review(self):
        review_paths = (
            (NEXT_MORPHOLOGY_REVIEW_MD_PATH, NEXT_MORPHOLOGY_REVIEW_CSV_PATH, 7),
            (NEXT_VOCAB_REVIEW_MD_PATH, NEXT_VOCAB_REVIEW_CSV_PATH, 6),
            (NEXT_STANDARDS_REVIEW_MD_PATH, NEXT_STANDARDS_REVIEW_CSV_PATH, 6),
        )
        for md_path, csv_path, expected_count in review_paths:
            with self.subTest(csv_path=csv_path):
                self.assertTrue(md_path.exists())
                self.assertTrue(csv_path.exists())
                self.assertTrue(csv_path.read_bytes().startswith(b"\xef\xbb\xbf"))
                md_text = md_path.read_text(encoding="utf-8")
                self.assertIn("Yossi is reviewing enrichment candidates only.", md_text)
                self.assertIn("This is enrichment review only.", md_text)
                for decision in validator.ALLOWED_YOSSI_DECISIONS - {""}:
                    self.assertIn(f"`{decision}`", md_text)
                with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
                    rows = list(csv.DictReader(handle))
                self.assertEqual(list(rows[0].keys()), validator.REVIEW_CSV_COLUMNS)
                self.assertEqual(len(rows), expected_count)
                self.assertTrue(all("not question approval" in row["safety_warning"] for row in rows))

    def test_next_slice_token_split_candidates_map_to_contract_and_are_review_only(self):
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        canonical_by_id = {record["canonical_skill_id"]: record for record in contract["canonical_skills"]}
        valid_standards = {
            standard_id
            for record in contract["canonical_skills"]
            for standard_id in record["related_zekelman_standard_ids"]
        }
        rows = load_tsv(NEXT_TOKEN_SPLIT_STANDARDS_PATH)
        self.assertEqual(len(rows), 13)
        self.assertTrue(NEXT_TOKEN_SPLIT_REVIEW_CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf"))
        review_text = NEXT_TOKEN_SPLIT_REVIEW_MD_PATH.read_text(encoding="utf-8")
        self.assertIn("This is enrichment review only.", review_text)
        self.assertNotIn("???", review_text)
        for row in rows:
            with self.subTest(candidate=row["candidate_id"]):
                self.assertIn(row["canonical_skill_id"], canonical_by_id)
                self.assertIn(row["canonical_standard_anchor"], valid_standards)
                self.assertEqual(row["proposed_zekelman_standard"], row["canonical_standard_anchor"])
                self.assertIn(
                    row["canonical_standard_anchor"],
                    canonical_by_id[row["canonical_skill_id"]]["related_zekelman_standard_ids"],
                )
                self.assertNotIn("?", row["hebrew_token"])
                self.assertNotIn("?", row["clean_hebrew_no_nikud"])
                self.assertIn(row["enrichment_review_status"], validator.ALLOWED_REVIEW_STATUSES)
                self.assertIn(row["yossi_decision"], validator.ALLOWED_YOSSI_DECISIONS)
                if row["enrichment_review_status"] == "yossi_enrichment_verified":
                    self.assertEqual(row["yossi_decision"], "verified")
                    self.assertTrue(row["yossi_notes"])
                self.assertEqual(row["question_allowed"], "needs_review")
                self.assertEqual(row["protected_preview_allowed"], "false")
                self.assertEqual(row["reviewed_bank_allowed"], "false")
                self.assertEqual(row["runtime_allowed"], "false")

    def test_next_slice_generation_report_exists_and_matches_counts(self):
        self.assertTrue(NEXT_GENERATION_REPORT_PATH.exists())
        report_text = NEXT_GENERATION_REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn("data/verified_source_skill_maps/bereishis_1_6_to_1_13_source_to_skill_map.tsv", report_text)
        self.assertIn("- morphology: 7", report_text)
        self.assertIn("- vocabulary_shoresh: 6", report_text)
        self.assertIn("- standards: 6", report_text)
        self.assertIn("- token_split_standards: 13", report_text)
        self.assertIn("- candidates currently marked `needs_follow_up`: 18", report_text)
        self.assertIn("token-split rows are review-only and safety-closed", report_text)
        self.assertIn("question_allowed = needs_review", report_text)

    def test_next_slice_review_applied_reports_and_summary_exist(self):
        for path in (
            NEXT_MORPH_APPLIED_REPORT_PATH,
            NEXT_VOCAB_APPLIED_REPORT_PATH,
            NEXT_STANDARDS_APPLIED_REPORT_PATH,
            NEXT_TOKEN_SPLIT_APPLIED_REPORT_PATH,
            NEXT_REVIEW_SUMMARY_PATH,
            NEXT_MINI_COMPLETION_REPORT_PATH,
            NEXT_FOLLOW_UP_INVENTORY_PATH,
        ):
            with self.subTest(path=path):
                self.assertTrue(path.exists())

    def test_next_slice_review_applied_counts_match_expected(self):
        morph_rows = load_tsv(NEXT_MORPHOLOGY_PATH)
        vocab_rows = load_tsv(NEXT_VOCABULARY_PATH)
        standards_rows = load_tsv(NEXT_STANDARDS_PATH)
        token_rows = load_tsv(NEXT_TOKEN_SPLIT_STANDARDS_PATH)

        def counts(rows: list[dict[str, str]]) -> tuple[int, int]:
            verified = sum(1 for row in rows if row["enrichment_review_status"] == "yossi_enrichment_verified")
            follow_up = sum(1 for row in rows if row["enrichment_review_status"] == "needs_follow_up")
            return verified, follow_up

        self.assertEqual(counts(morph_rows), (3, 4))
        self.assertEqual(counts(vocab_rows), (5, 1))
        self.assertEqual(counts(standards_rows), (0, 6))
        self.assertEqual(counts(token_rows), (6, 7))
        total_verified = sum(counts(rows)[0] for rows in (morph_rows, vocab_rows, standards_rows, token_rows))
        total_follow_up = sum(counts(rows)[1] for rows in (morph_rows, vocab_rows, standards_rows, token_rows))
        self.assertEqual(total_verified, 14)
        self.assertEqual(total_follow_up, 18)
        self.assertTrue(all(row["yossi_decision"] == "needs_follow_up" for row in standards_rows))
        self.assertTrue(all(row["enrichment_review_status"] == "needs_follow_up" for row in standards_rows))

    def test_next_slice_mini_completion_report_matches_counts_and_safety(self):
        text = NEXT_MINI_COMPLETION_REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn("Bereishis 1:6-1:13 Enrichment Mini-Completion Report", text)
        self.assertIn("not question approval", text)
        self.assertIn("not protected-preview approval", text)
        self.assertIn("not reviewed-bank approval", text)
        self.assertIn("not runtime approval", text)
        self.assertIn("not student-facing approval", text)
        self.assertIn("not answer-key approval", text)
        self.assertIn("Bereishis 1:14-1:23", text)
        self.assertIn("| morphology | 7 | 3 | 4 | 0 | 0 |", text)
        self.assertIn("| vocabulary/shoresh | 6 | 5 | 1 | 0 | 0 |", text)
        self.assertIn("| phrase-level standards | 6 | 0 | 6 | 0 | 0 |", text)
        self.assertIn("| token-split standards | 13 | 6 | 7 | 0 | 0 |", text)
        self.assertIn("| total | 32 | 14 | 18 | 0 | 0 |", text)

    def test_expansion_source_map_is_verified_and_safety_closed(self):
        rows = load_tsv(EXPANSION_SOURCE_MAP_PATH)
        self.assertEqual(len(rows), 39)
        self.assertTrue(all(row["extraction_review_status"] == "yossi_extraction_verified" for row in rows))
        self.assertEqual({row["question_allowed"] for row in rows}, {"needs_review"})
        self.assertEqual({row["runtime_allowed"] for row in rows}, {"false"})
        self.assertEqual({row["protected_preview_allowed"] for row in rows}, {"false"})
        self.assertEqual({row["reviewed_bank_allowed"] for row in rows}, {"false"})
        self.assertTrue(all("?" not in row["hebrew_word_or_phrase"] for row in rows))

    def test_expansion_candidate_files_have_required_columns(self):
        for path, expected_columns in (
            (EXPANSION_MORPHOLOGY_PATH, validator.MORPHOLOGY_COLUMNS),
            (EXPANSION_STANDARDS_PATH, validator.STANDARDS_COLUMNS),
            (EXPANSION_VOCABULARY_PATH, validator.VOCABULARY_COLUMNS),
            (EXPANSION_TOKEN_SPLIT_STANDARDS_PATH, validator.TOKEN_SPLIT_STANDARDS_COLUMNS),
        ):
            with self.subTest(path=path):
                with path.open("r", encoding="utf-8", newline="") as handle:
                    columns = list(csv.DictReader(handle, delimiter="\t").fieldnames or [])
                self.assertEqual(columns, expected_columns)

    def test_expansion_candidates_link_to_verified_source_rows_and_keep_safety_closed(self):
        source_rows = expansion_source_rows_by_id()
        for row in expansion_candidate_rows():
            with self.subTest(candidate=row["candidate_id"]):
                linked = source_rows[row["source_row_id"]]
                self.assertEqual(
                    row["source_map_file"],
                    "data/verified_source_skill_maps/bereishis_1_14_to_1_23_source_to_skill_map.tsv",
                )
                self.assertEqual(linked["extraction_review_status"], "yossi_extraction_verified")
                self.assertEqual(row["ref"], linked["ref"])
                self.assertEqual(row["hebrew_phrase"], linked["hebrew_word_or_phrase"])
                self.assertIn(row["enrichment_review_status"], {"yossi_enrichment_verified", "needs_follow_up"})
                if row["enrichment_review_status"] == "yossi_enrichment_verified":
                    self.assertEqual(row["yossi_decision"], "verified")
                if row["enrichment_review_status"] == "needs_follow_up":
                    self.assertEqual(row["yossi_decision"], "needs_follow_up")
                self.assertNotEqual(row["yossi_notes"].strip(), "")
                self.assertEqual(row["question_allowed"], "needs_review")
                self.assertEqual(row["protected_preview_allowed"], "false")
                self.assertEqual(row["runtime_allowed"], "false")
                self.assertEqual(row["reviewed_bank_allowed"], "false")

    def test_expansion_review_sheets_exist_are_utf8_bom_and_blank(self):
        review_paths = (
            (EXPANSION_MORPHOLOGY_REVIEW_MD_PATH, EXPANSION_MORPHOLOGY_REVIEW_CSV_PATH, 25),
            (EXPANSION_VOCAB_REVIEW_MD_PATH, EXPANSION_VOCAB_REVIEW_CSV_PATH, 21),
            (EXPANSION_STANDARDS_REVIEW_MD_PATH, EXPANSION_STANDARDS_REVIEW_CSV_PATH, 13),
        )
        for md_path, csv_path, expected_count in review_paths:
            with self.subTest(csv_path=csv_path):
                self.assertTrue(md_path.exists())
                self.assertTrue(csv_path.exists())
                self.assertTrue(csv_path.read_bytes().startswith(b"\xef\xbb\xbf"))
                md_text = md_path.read_text(encoding="utf-8")
                self.assertIn("This is enrichment review only.", md_text)
                self.assertNotIn("???", md_text)
                with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
                    rows = list(csv.DictReader(handle))
                self.assertEqual(list(rows[0].keys()), validator.REVIEW_CSV_COLUMNS)
                self.assertEqual(len(rows), expected_count)
                self.assertTrue(all(row["yossi_decision"] == "" for row in rows))
                self.assertTrue(all(row["yossi_notes"] == "" for row in rows))

    def test_expansion_token_split_candidates_map_to_contract_and_match_review_applied_status(self):
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        canonical_by_id = {record["canonical_skill_id"]: record for record in contract["canonical_skills"]}
        valid_standards = {
            standard_id
            for record in contract["canonical_skills"]
            for standard_id in record["related_zekelman_standard_ids"]
        }
        rows = load_tsv(EXPANSION_TOKEN_SPLIT_STANDARDS_PATH)
        self.assertEqual(len(rows), 45)
        self.assertTrue(EXPANSION_TOKEN_SPLIT_REVIEW_CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf"))
        review_text = EXPANSION_TOKEN_SPLIT_REVIEW_MD_PATH.read_text(encoding="utf-8")
        self.assertIn("This is enrichment review only.", review_text)
        self.assertNotIn("???", review_text)
        for row in rows:
            with self.subTest(candidate=row["candidate_id"]):
                self.assertIn(row["canonical_skill_id"], canonical_by_id)
                self.assertIn(row["canonical_standard_anchor"], valid_standards)
                self.assertIn(
                    row["canonical_standard_anchor"],
                    canonical_by_id[row["canonical_skill_id"]]["related_zekelman_standard_ids"],
                )
                self.assertNotIn("?", row["hebrew_token"])
                self.assertNotIn("?", row["clean_hebrew_no_nikud"])
                self.assertIn(row["enrichment_review_status"], {"yossi_enrichment_verified", "needs_follow_up"})
                if row["enrichment_review_status"] == "yossi_enrichment_verified":
                    self.assertEqual(row["yossi_decision"], "verified")
                if row["enrichment_review_status"] == "needs_follow_up":
                    self.assertEqual(row["yossi_decision"], "needs_follow_up")
                self.assertNotEqual(row["yossi_notes"].strip(), "")
                self.assertEqual(row["question_allowed"], "needs_review")
                self.assertEqual(row["protected_preview_allowed"], "false")
                self.assertEqual(row["reviewed_bank_allowed"], "false")
                self.assertEqual(row["runtime_allowed"], "false")

    def test_expansion_review_applied_counts_match_expected(self):
        morph_rows = load_tsv(EXPANSION_MORPHOLOGY_PATH)
        vocab_rows = load_tsv(EXPANSION_VOCABULARY_PATH)
        standards_rows = load_tsv(EXPANSION_STANDARDS_PATH)
        token_rows = load_tsv(EXPANSION_TOKEN_SPLIT_STANDARDS_PATH)

        def counts(rows: list[dict[str, str]]) -> tuple[int, int]:
            verified = sum(1 for row in rows if row["enrichment_review_status"] == "yossi_enrichment_verified")
            follow_up = sum(1 for row in rows if row["enrichment_review_status"] == "needs_follow_up")
            return verified, follow_up

        self.assertEqual(counts(morph_rows), (11, 14))
        self.assertEqual(counts(vocab_rows), (14, 7))
        self.assertEqual(counts(standards_rows), (0, 13))
        self.assertEqual(counts(token_rows), (28, 17))
        total_verified = sum(counts(rows)[0] for rows in (morph_rows, vocab_rows, standards_rows, token_rows))
        total_follow_up = sum(counts(rows)[1] for rows in (morph_rows, vocab_rows, standards_rows, token_rows))
        self.assertEqual(total_verified, 53)
        self.assertEqual(total_follow_up, 51)
        self.assertTrue(all(row["enrichment_review_status"] == "needs_follow_up" for row in standards_rows))
        self.assertTrue(all(row["yossi_decision"] == "needs_follow_up" for row in standards_rows))

    def test_expansion_applied_reports_and_summary_exist_and_match(self):
        for path in (
            EXPANSION_MORPH_APPLIED_REPORT_PATH,
            EXPANSION_VOCAB_APPLIED_REPORT_PATH,
            EXPANSION_STANDARDS_APPLIED_REPORT_PATH,
            EXPANSION_TOKEN_SPLIT_APPLIED_REPORT_PATH,
            EXPANSION_REVIEW_SUMMARY_PATH,
        ):
            with self.subTest(path=path):
                self.assertTrue(path.exists())

        summary_text = EXPANSION_REVIEW_SUMMARY_PATH.read_text(encoding="utf-8")
        self.assertIn("Bereishis 1:14-1:23 Enrichment Review Summary", summary_text)
        self.assertIn("- total candidates: 104", summary_text)
        self.assertIn("- verified count: 53", summary_text)
        self.assertIn("- needs_follow_up count: 51", summary_text)
        self.assertIn("all later gates remain closed", summary_text)
        self.assertIn("What Was Not Approved", summary_text)

    def test_expansion_mini_completion_report_exists_and_matches_counts_and_safety(self):
        self.assertTrue(EXPANSION_MINI_COMPLETION_REPORT_PATH.exists())
        text = EXPANSION_MINI_COMPLETION_REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn("Bereishis 1:14-1:23 Enrichment Mini-Completion Report", text)
        self.assertIn("| morphology | 25 | 11 | 14 | 0 | 0 |", text)
        self.assertIn("| vocabulary/shoresh | 21 | 14 | 7 | 0 | 0 |", text)
        self.assertIn("| phrase-level standards | 13 | 0 | 13 | 0 | 0 |", text)
        self.assertIn("| token-split standards | 45 | 28 | 17 | 0 | 0 |", text)
        self.assertIn("| total | 104 | 53 | 51 | 0 | 0 |", text)
        self.assertIn("not question approval", text)
        self.assertIn("not protected-preview approval", text)
        self.assertIn("not reviewed-bank approval", text)
        self.assertIn("not runtime approval", text)
        self.assertIn("not student-facing approval", text)
        self.assertIn("not answer-key approval", text)
        self.assertIn("Bereishis 1:24-1:31", text)

    def test_expansion_generation_report_exists_and_matches_counts(self):
        self.assertTrue(EXPANSION_AUDIT_REPORT_PATH.exists())
        self.assertTrue(EXPANSION_GENERATION_REPORT_PATH.exists())
        report_text = EXPANSION_GENERATION_REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn("data/verified_source_skill_maps/bereishis_1_14_to_1_23_source_to_skill_map.tsv", report_text)
        self.assertIn("- source-to-skill rows: 39", report_text)
        self.assertIn("- morphology: 25", report_text)
        self.assertIn("- vocabulary_shoresh: 21", report_text)
        self.assertIn("- standards: 13", report_text)
        self.assertIn("- token_split_standards: 45", report_text)
        self.assertIn("- total_candidates: 104", report_text)
        self.assertIn("Hebrew tokens are real UTF-8 Hebrew and not placeholder question marks", report_text)
        self.assertIn("question_allowed = needs_review", report_text)

    def test_perek1_final_source_map_is_verified_and_safety_closed(self):
        rows = load_tsv(PEREK1_FINAL_SOURCE_MAP_PATH)
        self.assertEqual(len(rows), 38)
        self.assertTrue(all(row["extraction_review_status"] == "yossi_extraction_verified" for row in rows))
        self.assertEqual({row["question_allowed"] for row in rows}, {"needs_review"})
        self.assertEqual({row["runtime_allowed"] for row in rows}, {"false"})
        self.assertEqual({row["protected_preview_allowed"] for row in rows}, {"false"})
        self.assertEqual({row["reviewed_bank_allowed"] for row in rows}, {"false"})
        self.assertTrue(all("?" not in row["hebrew_word_or_phrase"] for row in rows))

    def test_perek1_final_candidate_files_have_required_columns(self):
        for path, expected_columns in (
            (PEREK1_FINAL_MORPHOLOGY_PATH, validator.MORPHOLOGY_COLUMNS),
            (PEREK1_FINAL_STANDARDS_PATH, validator.STANDARDS_COLUMNS),
            (PEREK1_FINAL_VOCABULARY_PATH, validator.VOCABULARY_COLUMNS),
            (PEREK1_FINAL_TOKEN_SPLIT_STANDARDS_PATH, validator.TOKEN_SPLIT_STANDARDS_COLUMNS),
        ):
            with self.subTest(path=path):
                with path.open("r", encoding="utf-8", newline="") as handle:
                    columns = list(csv.DictReader(handle, delimiter="\t").fieldnames or [])
                self.assertEqual(columns, expected_columns)

    def test_perek1_final_candidates_link_to_verified_source_rows_and_keep_safety_closed(self):
        source_rows = perek1_final_source_rows_by_id()
        for row in perek1_final_candidate_rows():
            with self.subTest(candidate=row["candidate_id"]):
                linked = source_rows[row["source_row_id"]]
                self.assertEqual(
                    row["source_map_file"],
                    "data/verified_source_skill_maps/bereishis_1_24_to_1_31_source_to_skill_map.tsv",
                )
                self.assertEqual(linked["extraction_review_status"], "yossi_extraction_verified")
                self.assertEqual(row["ref"], linked["ref"])
                self.assertEqual(row["hebrew_phrase"], linked["hebrew_word_or_phrase"])
                self.assertIn(row["enrichment_review_status"], {"yossi_enrichment_verified", "needs_follow_up"})
                if row["enrichment_review_status"] == "yossi_enrichment_verified":
                    self.assertEqual(row["yossi_decision"], "verified")
                else:
                    self.assertEqual(row["yossi_decision"], "needs_follow_up")
                self.assertNotEqual(row["yossi_notes"].strip(), "")
                self.assertEqual(row["question_allowed"], "needs_review")
                self.assertEqual(row["protected_preview_allowed"], "false")
                self.assertEqual(row["runtime_allowed"], "false")
                self.assertEqual(row["reviewed_bank_allowed"], "false")

    def test_perek1_final_review_sheets_exist_are_utf8_bom(self):
        review_paths = (
            (PEREK1_FINAL_MORPHOLOGY_REVIEW_MD_PATH, PEREK1_FINAL_MORPHOLOGY_REVIEW_CSV_PATH, 26),
            (PEREK1_FINAL_VOCAB_REVIEW_MD_PATH, PEREK1_FINAL_VOCAB_REVIEW_CSV_PATH, 40),
            (PEREK1_FINAL_STANDARDS_REVIEW_MD_PATH, PEREK1_FINAL_STANDARDS_REVIEW_CSV_PATH, 14),
        )
        for md_path, csv_path, expected_count in review_paths:
            with self.subTest(csv_path=csv_path):
                self.assertTrue(md_path.exists())
                self.assertTrue(csv_path.exists())
                self.assertTrue(csv_path.read_bytes().startswith(b"\xef\xbb\xbf"))
                md_text = md_path.read_text(encoding="utf-8")
                self.assertIn("This is enrichment review only.", md_text)
                self.assertNotIn("???", md_text)
                with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
                    rows = list(csv.DictReader(handle))
                self.assertEqual(list(rows[0].keys()), validator.REVIEW_CSV_COLUMNS)
                self.assertEqual(len(rows), expected_count)

    def test_perek1_final_token_split_candidates_map_to_contract_and_are_review_applied(self):
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        canonical_by_id = {record["canonical_skill_id"]: record for record in contract["canonical_skills"]}
        valid_standards = {
            standard_id
            for record in contract["canonical_skills"]
            for standard_id in record["related_zekelman_standard_ids"]
        }
        rows = load_tsv(PEREK1_FINAL_TOKEN_SPLIT_STANDARDS_PATH)
        self.assertEqual(len(rows), 56)
        self.assertTrue(PEREK1_FINAL_TOKEN_SPLIT_REVIEW_CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf"))
        review_text = PEREK1_FINAL_TOKEN_SPLIT_REVIEW_MD_PATH.read_text(encoding="utf-8")
        self.assertIn("This is enrichment review only.", review_text)
        self.assertNotIn("???", review_text)
        for row in rows:
            with self.subTest(candidate=row["candidate_id"]):
                self.assertIn(row["canonical_skill_id"], canonical_by_id)
                self.assertIn(row["canonical_standard_anchor"], valid_standards)
                self.assertIn(
                    row["canonical_standard_anchor"],
                    canonical_by_id[row["canonical_skill_id"]]["related_zekelman_standard_ids"],
                )
                self.assertNotIn("?", row["hebrew_token"])
                self.assertNotIn("?", row["clean_hebrew_no_nikud"])
                self.assertIn(row["enrichment_review_status"], {"yossi_enrichment_verified", "needs_follow_up"})
                if row["enrichment_review_status"] == "yossi_enrichment_verified":
                    self.assertEqual(row["yossi_decision"], "verified")
                else:
                    self.assertEqual(row["yossi_decision"], "needs_follow_up")
                self.assertNotEqual(row["yossi_notes"].strip(), "")
                self.assertEqual(row["question_allowed"], "needs_review")
                self.assertEqual(row["protected_preview_allowed"], "false")
                self.assertEqual(row["reviewed_bank_allowed"], "false")
                self.assertEqual(row["runtime_allowed"], "false")

    def test_perek1_final_generation_report_exists_and_matches_counts(self):
        self.assertTrue(PEREK1_FINAL_AUDIT_REPORT_PATH.exists())
        self.assertTrue(PEREK1_FINAL_GENERATION_REPORT_PATH.exists())
        report_text = PEREK1_FINAL_GENERATION_REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn("data/verified_source_skill_maps/bereishis_1_24_to_1_31_source_to_skill_map.tsv", report_text)
        self.assertIn("- source-to-skill rows: 38", report_text)
        self.assertIn("- morphology: 26", report_text)
        self.assertIn("- vocabulary_shoresh: 40", report_text)
        self.assertIn("- standards: 14", report_text)
        self.assertIn("- token_split_standards: 56", report_text)
        self.assertIn("- total_candidates: 136", report_text)
        self.assertIn("completes enrichment candidate coverage across Bereishis Perek 1", report_text)
        self.assertIn("Hebrew tokens are real UTF-8 Hebrew and not placeholder question marks", report_text)
        self.assertIn("question_allowed = needs_review", report_text)
        self.assertIn("protected_preview_allowed = false", report_text)
        self.assertIn("reviewed_bank_allowed = false", report_text)
        self.assertIn("runtime_allowed = false", report_text)

    def test_perek1_final_review_applied_counts_match_expected(self):
        morph_rows = load_tsv(PEREK1_FINAL_MORPHOLOGY_PATH)
        vocab_rows = load_tsv(PEREK1_FINAL_VOCABULARY_PATH)
        standards_rows = load_tsv(PEREK1_FINAL_STANDARDS_PATH)
        token_rows = load_tsv(PEREK1_FINAL_TOKEN_SPLIT_STANDARDS_PATH)

        def counts(rows: list[dict[str, str]]) -> tuple[int, int]:
            verified = sum(1 for row in rows if row["enrichment_review_status"] == "yossi_enrichment_verified")
            follow_up = sum(1 for row in rows if row["enrichment_review_status"] == "needs_follow_up")
            return verified, follow_up

        self.assertEqual(counts(morph_rows), (13, 13))
        self.assertEqual(counts(vocab_rows), (34, 6))
        self.assertEqual(counts(standards_rows), (0, 14))
        self.assertEqual(counts(token_rows), (36, 20))
        total_verified = sum(counts(rows)[0] for rows in (morph_rows, vocab_rows, standards_rows, token_rows))
        total_follow_up = sum(counts(rows)[1] for rows in (morph_rows, vocab_rows, standards_rows, token_rows))
        self.assertEqual(total_verified, 83)
        self.assertEqual(total_follow_up, 53)
        self.assertTrue(all(row["yossi_decision"] in {"verified", "needs_follow_up"} for row in morph_rows + vocab_rows + standards_rows + token_rows))
        self.assertTrue(all(row["yossi_notes"].strip() for row in morph_rows + vocab_rows + standards_rows + token_rows))

    def test_perek1_final_applied_reports_and_summary_exist(self):
        for path in (
            Path("data/source_skill_enrichment/reports/bereishis_1_24_to_1_31_morphology_enrichment_yossi_review_applied.md"),
            Path("data/source_skill_enrichment/reports/bereishis_1_24_to_1_31_vocabulary_shoresh_enrichment_yossi_review_applied.md"),
            Path("data/source_skill_enrichment/reports/bereishis_1_24_to_1_31_standards_enrichment_yossi_review_applied.md"),
            Path("data/source_skill_enrichment/reports/bereishis_1_24_to_1_31_token_split_standards_yossi_review_applied.md"),
            Path("data/source_skill_enrichment/reports/bereishis_1_24_to_1_31_enrichment_review_summary.md"),
        ):
            with self.subTest(path=path):
                self.assertTrue(path.exists())

    def test_perek1_coverage_report_exists_and_matches_counts(self):
        self.assertTrue(PEREK1_COVERAGE_REPORT_PATH.exists())
        text = PEREK1_COVERAGE_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in (
            "Bereishis Perek 1 Enrichment Review-Application Coverage Report",
            "| Bereishis 1:1-1:5 | 23 | 27 | 14 | 13 |",
            "| Bereishis 1:6-1:13 | 37 | 32 | 14 | 18 |",
            "| Bereishis 1:14-1:23 | 39 | 104 | 53 | 51 |",
            "| Bereishis 1:24-1:31 | 38 | 136 | 83 | 53 |",
            "| morphology | 63 | 30 | 33 |",
            "| vocabulary/shoresh | 73 | 56 | 17 |",
            "| phrase-level standards | 39 | 1 | 38 |",
            "| token-split standards | 124 | 77 | 47 |",
            "| **total** | **299** | **164** | **135** |",
            "question generation remains blocked",
            "protected preview remains blocked",
            "reviewed bank remains blocked",
            "runtime remains blocked",
            "student-facing use remains blocked",
        ):
            self.assertIn(phrase, text)

    def test_perek2_gate1_artifacts_exist_and_match_counts(self):
        summary = validator.validate_source_skill_enrichment()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["perek2_source_row_count"], 99)
        self.assertEqual(summary["perek2_morphology_candidate_count"], 328)
        self.assertEqual(summary["perek2_vocabulary_candidate_count"], 328)
        self.assertEqual(summary["perek2_standards_candidate_count"], 99)
        self.assertEqual(summary["perek2_token_split_candidate_count"], 328)
        self.assertTrue(validator.PEREK2_SOURCE_READINESS_AUDIT_PATH.exists())
        self.assertTrue(validator.PEREK2_GATE1_REPORT_PATH.exists())

    def test_perek2_candidates_link_to_verified_source_rows_and_are_review_only(self):
        source_rows = validator.perek2_source_rows_by_file()
        for path in (
            validator.PEREK2_MORPHOLOGY_PATH,
            validator.PEREK2_VOCABULARY_PATH,
            validator.PEREK2_STANDARDS_PATH,
            validator.PEREK2_TOKEN_SPLIT_STANDARDS_PATH,
        ):
            rows = load_tsv(path)
            self.assertTrue(rows)
            for row in rows:
                with self.subTest(candidate=row["candidate_id"]):
                    linked = source_rows[row["source_map_file"]][row["source_row_id"]]
                    self.assertEqual(linked["extraction_review_status"], "yossi_extraction_verified")
                    self.assertEqual(row["ref"], linked["ref"])
                    self.assertEqual(row["hebrew_phrase"], linked["hebrew_word_or_phrase"])
                    self.assertEqual(row["enrichment_review_status"], "pending_yossi_enrichment_review")
                    self.assertEqual(row["yossi_decision"], "")
                    self.assertEqual(row["yossi_notes"], "")
                    self.assertEqual(row["question_allowed"], "needs_review")
                    self.assertEqual(row["protected_preview_allowed"], "false")
                    self.assertEqual(row["runtime_allowed"], "false")
                    self.assertEqual(row["reviewed_bank_allowed"], "false")
                    self.assertNotIn("?", row["hebrew_phrase"])
                    self.assertNotIn("?", row.get("hebrew_token", ""))

    def test_perek2_review_sheets_exist_are_utf8_bom_and_blank(self):
        for md_path, csv_path in validator.PEREK2_REVIEW_SHEETS.values():
            with self.subTest(csv_path=csv_path):
                self.assertTrue(md_path.exists())
                self.assertTrue(csv_path.exists())
                self.assertTrue(csv_path.read_bytes().startswith(b"\xef\xbb\xbf"))
                md_text = md_path.read_text(encoding="utf-8")
                self.assertIn("This is enrichment review only.", md_text)
                self.assertNotIn("???", md_text)
                with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
                    rows = list(csv.DictReader(handle))
                self.assertTrue(rows)
                self.assertEqual(list(rows[0].keys()), validator.REVIEW_CSV_COLUMNS)
                self.assertTrue(all(row["yossi_decision"] == "" for row in rows))
                self.assertTrue(all(row["yossi_notes"] == "" for row in rows))

    def test_perek2_gate1_reports_document_blocked_eligibility(self):
        source_text = validator.PEREK2_SOURCE_READINESS_AUDIT_PATH.read_text(encoding="utf-8")
        gate_text = validator.PEREK2_GATE1_REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn("Perek 2 source-to-skill readiness is confirmed", source_text)
        self.assertIn("Enrichment remains review-only", source_text)
        self.assertIn("Question-eligibility decisions and approved input-candidate planning are not ready", gate_text)
        self.assertIn("basic_verb_form_recognition", gate_text)


if __name__ == "__main__":
    unittest.main()
