from __future__ import annotations

import csv
import unittest
from pathlib import Path

import scripts.validate_source_skill_enrichment as validator


ROOT = Path(__file__).resolve().parents[1]
ENRICHMENT_DIR = ROOT / "data" / "source_skill_enrichment"
SOURCE_MAP_PATH = ROOT / "data" / "verified_source_skill_maps" / "bereishis_1_1_to_1_5_source_to_skill_map.tsv"
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


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def source_rows_by_id() -> dict[str, dict[str, str]]:
    rows = load_tsv(SOURCE_MAP_PATH)
    return {f"row_{index:03d}": row for index, row in enumerate(rows, 1)}


def all_candidate_rows() -> list[dict[str, str]]:
    return load_tsv(MORPHOLOGY_PATH) + load_tsv(STANDARDS_PATH) + load_tsv(VOCABULARY_PATH)


class SourceSkillEnrichmentTests(unittest.TestCase):
    def test_validator_passes(self):
        summary = validator.validate_source_skill_enrichment()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["morphology_candidate_count"], 5)
        self.assertEqual(summary["standards_candidate_count"], 6)
        self.assertEqual(summary["vocabulary_candidate_count"], 6)
        self.assertEqual(summary["review_sheet_count"], 3)
        self.assertEqual(summary["applied_review_report_count"], 3)
        self.assertEqual(summary["follow_up_candidate_count"], 10)

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
        self.assertIn("What Should Not Be Auto-Filled", audit_text)
        self.assertIn("reviewed-bank examples; reference only", audit_text)
        self.assertIn("Do not backfill all morphology fields", audit_text)

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
        self.assertIn("Vocabulary/Shoresh Follow-Up", md_text)
        self.assertIn("Morphology Follow-Up", md_text)
        self.assertIn("Standards Follow-Up", md_text)
        self.assertIn("This is enrichment follow-up review only", md_text)
        self.assertIn("not question approval", md_text)
        self.assertIn("protected-preview approval", md_text)
        self.assertIn("reviewed-bank approval", md_text)
        self.assertIn("runtime approval", md_text)
        self.assertIn("student-facing approval", md_text)

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
        with FOLLOW_UP_REVIEW_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(list(rows[0].keys()), validator.FOLLOW_UP_CSV_COLUMNS)
        csv_ids = {row["candidate_id"] for row in rows}
        self.assertEqual(csv_ids, unresolved_ids)
        self.assertEqual(len(csv_ids), 10)
        self.assertTrue(all(row["yossi_decision"] == "" for row in rows))
        self.assertTrue(all(row["yossi_notes"] == "" for row in rows))

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


if __name__ == "__main__":
    unittest.main()
