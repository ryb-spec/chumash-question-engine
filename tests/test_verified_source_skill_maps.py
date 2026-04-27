import csv
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts import validate_verified_source_skill_maps as validator


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "data" / "verified_source_skill_maps" / "bereishis_1_1_to_3_24_metsudah_skill_map.tsv"
PROOF_MAP_PATH = ROOT / "data" / "verified_source_skill_maps" / "bereishis_1_1_to_1_5_source_to_skill_map.tsv"
REVIEW_PACKET_PATH = (
    ROOT
    / "data"
    / "verified_source_skill_maps"
    / "reports"
    / "bereishis_1_1_to_3_24_metsudah_skill_map_extraction_accuracy_review_packet.md"
)
PROOF_REVIEW_PACKET_PATH = (
    ROOT
    / "data"
    / "verified_source_skill_maps"
    / "reports"
    / "bereishis_1_1_to_1_5_source_to_skill_map_exceptions_review_packet.md"
)
PROOF_VERIFICATION_REPORT_PATH = (
    ROOT
    / "data"
    / "verified_source_skill_maps"
    / "reports"
    / "bereishis_1_1_to_1_5_yossi_extraction_verification_report.md"
)
NEXT_SLICE_MAP_PATH = (
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_1_6_to_1_13_source_to_skill_map.tsv"
)
NEXT_SLICE_BUILD_REPORT_PATH = (
    ROOT
    / "data"
    / "verified_source_skill_maps"
    / "reports"
    / "bereishis_1_6_to_1_13_source_to_skill_map_build_report.md"
)
NEXT_SLICE_REVIEW_PACKET_PATH = (
    ROOT
    / "data"
    / "verified_source_skill_maps"
    / "reports"
    / "bereishis_1_6_to_1_13_source_to_skill_map_exceptions_review_packet.md"
)
NEXT_SLICE_VERIFICATION_REPORT_PATH = (
    ROOT
    / "data"
    / "verified_source_skill_maps"
    / "reports"
    / "bereishis_1_6_to_1_13_yossi_extraction_verification_report.md"
)
PENDING_SLICE_MAP_PATH = (
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_1_14_to_1_23_source_to_skill_map.tsv"
)
PENDING_SLICE_BUILD_REPORT_PATH = (
    ROOT
    / "data"
    / "verified_source_skill_maps"
    / "reports"
    / "bereishis_1_14_to_1_23_source_to_skill_map_build_report.md"
)
PENDING_SLICE_REVIEW_PACKET_PATH = (
    ROOT
    / "data"
    / "verified_source_skill_maps"
    / "reports"
    / "bereishis_1_14_to_1_23_source_to_skill_map_exceptions_review_packet.md"
)
AUDIT_REPORT_PATH = ROOT / "data" / "verified_source_skill_maps" / "reports" / "source_to_skill_map_audit.json"
POLICY_PATH = ROOT / "docs" / "sources" / "trusted_teacher_source_policy.md"
QUESTION_TEMPLATE_POLICY_PATH = ROOT / "docs" / "question_templates" / "approved_question_template_policy.md"
TRANSLATION_REGISTRY_PATH = ROOT / "data" / "source_texts" / "translations" / "translation_sources_registry.json"


def load_rows():
    with MAP_PATH.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_proof_rows():
    with PROOF_MAP_PATH.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_next_slice_rows():
    with NEXT_SLICE_MAP_PATH.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_pending_slice_rows():
    with PENDING_SLICE_MAP_PATH.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


class VerifiedSourceSkillMapTests(unittest.TestCase):
    def test_validator_passes(self):
        summary = validator.validate_verified_source_skill_maps()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["row_count"], 5)
        self.assertEqual(summary["proof_row_count"], 23)
        self.assertEqual(summary["next_slice_row_count"], 37)
        self.assertEqual(summary["pending_slice_row_count"], 39)

    def test_map_has_required_columns(self):
        with MAP_PATH.open("r", encoding="utf-8", newline="") as handle:
            columns = list(csv.DictReader(handle, delimiter="\t").fieldnames or [])
        for column in validator.REQUIRED_COLUMNS:
            self.assertIn(column, columns)

    def test_proof_map_has_full_required_columns(self):
        with PROOF_MAP_PATH.open("r", encoding="utf-8", newline="") as handle:
            columns = list(csv.DictReader(handle, delimiter="\t").fieldnames or [])
        for column in validator.PROOF_REQUIRED_COLUMNS:
            self.assertIn(column, columns)

    def test_map_rows_do_not_unlock_runtime_or_questions(self):
        for row in load_rows():
            with self.subTest(ref=row["ref"]):
                self.assertEqual(row["question_allowed"], "no")
                self.assertEqual(row["runtime_allowed"], "false")
                self.assertEqual(row["protected_preview_allowed"], "false")
                self.assertEqual(row["reviewed_bank_allowed"], "false")
                self.assertEqual(row["extraction_review_status"], "pending_yossi_extraction_accuracy_pass")

    def test_proof_map_rows_do_not_unlock_runtime_or_questions(self):
        for row in load_proof_rows():
            with self.subTest(ref=row["ref"], hebrew=row["hebrew_word_or_phrase"]):
                self.assertEqual(row["question_allowed"], "needs_review")
                self.assertEqual(row["runtime_allowed"], "false")
                self.assertEqual(row["protected_preview_allowed"], "false")
                self.assertEqual(row["reviewed_bank_allowed"], "false")
                self.assertEqual(row["extraction_review_status"], "yossi_extraction_verified")
                self.assertTrue(row["uncertainty_reason"])
                self.assertTrue(row["source_files_used"])

    def test_builder_script_exists_and_supports_scope_arguments(self):
        result = subprocess.run(
            ["python", "scripts/build_source_to_skill_map.py", "--help"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        self.assertIn("--start-ref", result.stdout)
        self.assertIn("--end-ref", result.stdout)
        self.assertIn("--output", result.stdout)
        self.assertIn("--dry-run", result.stdout)
        self.assertIn("--strict", result.stdout)

    def test_builder_deterministically_recreates_next_slice_schema(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "slice.tsv"
            report = Path(tmpdir) / "build_report.md"
            review_packet = Path(tmpdir) / "review_packet.md"
            subprocess.run(
                [
                    "python",
                    "scripts/build_source_to_skill_map.py",
                    "--start-ref",
                    "Bereishis 1:6",
                    "--end-ref",
                    "Bereishis 1:13",
                    "--output",
                    str(output),
                    "--report-output",
                    str(report),
                    "--review-packet-output",
                    str(review_packet),
                    "--strict",
                ],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            with output.open("r", encoding="utf-8", newline="") as handle:
                generated_rows = list(csv.DictReader(handle, delimiter="\t"))
            self.assertEqual(len(generated_rows), 37)
            self.assertEqual(list(generated_rows[0].keys()), list(validator.PROOF_REQUIRED_COLUMNS))
            self.assertTrue(report.exists())
            self.assertTrue(review_packet.exists())

    def test_next_slice_rows_are_verified_and_safety_closed(self):
        rows = load_next_slice_rows()
        self.assertEqual(len(rows), 37)
        refs = {row["ref"] for row in rows}
        self.assertEqual(refs, {f"Bereishis 1:{pasuk}" for pasuk in range(6, 14)})
        for row in rows:
            with self.subTest(ref=row["ref"], hebrew=row["hebrew_word_or_phrase"]):
                self.assertEqual(row["extraction_review_status"], "yossi_extraction_verified")
                self.assertEqual(row["question_allowed"], "needs_review")
                self.assertEqual(row["runtime_allowed"], "false")
                self.assertEqual(row["protected_preview_allowed"], "false")
                self.assertEqual(row["reviewed_bank_allowed"], "false")
                self.assertNotEqual(row["question_allowed"], "yes")
                self.assertIn("Yossi confirmed extraction accuracy", row["review_notes"])
                self.assertTrue(row["uncertainty_reason"])
                self.assertTrue(row["source_files_used"])

    def test_next_slice_translation_metadata_is_conservative(self):
        for row in load_next_slice_rows():
            with self.subTest(ref=row["ref"], hebrew=row["hebrew_word_or_phrase"]):
                self.assertIn("Metsudah Chumash, Metsudah Publications, 2009", row["source_version_title"])
                self.assertIn("CC-BY", row["source_license"])
                self.assertEqual(row["source_preference"], "primary_preferred_translation_source")
                self.assertEqual(row["requires_attribution"], "true")
                self.assertTrue(row["source_translation_metsudah"])
                self.assertTrue(row["secondary_translation_koren"])
                self.assertIn("bereishis_english_koren.jsonl", row["source_files_used"])
                self.assertNotIn("commercial_use_approved", row["source_files_used"])

    def test_pending_slice_rows_remain_pending_and_safety_closed(self):
        rows = load_pending_slice_rows()
        self.assertEqual(len(rows), 39)
        refs = {row["ref"] for row in rows}
        self.assertEqual(refs, {f"Bereishis 1:{pasuk}" for pasuk in range(14, 24)})
        for row in rows:
            with self.subTest(ref=row["ref"], hebrew=row["hebrew_word_or_phrase"]):
                self.assertEqual(row["extraction_review_status"], "pending_yossi_extraction_accuracy_pass")
                self.assertEqual(row["question_allowed"], "needs_review")
                self.assertEqual(row["runtime_allowed"], "false")
                self.assertEqual(row["protected_preview_allowed"], "false")
                self.assertEqual(row["reviewed_bank_allowed"], "false")
                self.assertNotEqual(row["question_allowed"], "yes")
                self.assertTrue(row["uncertainty_reason"])
                self.assertTrue(row["source_files_used"])

    def test_pending_slice_reports_exist_and_call_out_yossi_review_needs(self):
        build_text = PENDING_SLICE_BUILD_REPORT_PATH.read_text(encoding="utf-8")
        packet_text = PENDING_SLICE_REVIEW_PACKET_PATH.read_text(encoding="utf-8")
        self.assertIn("pending Yossi extraction-accuracy review", build_text)
        self.assertIn("does not authorize question generation", build_text)
        self.assertIn("not generated-question review", packet_text)
        self.assertIn("not question approval", packet_text)
        self.assertIn("not protected-preview approval", packet_text)
        self.assertIn("not reviewed-bank approval", packet_text)
        self.assertIn("not runtime approval", packet_text)
        self.assertIn("High-Risk Rows Needing Yossi Review", packet_text)
        self.assertIn("Long Parentheticals Needing Review", packet_text)
        self.assertIn("Long Hebrew Phrase Boundaries Needing Review", packet_text)
        self.assertIn("Awkward But Source-Derived Wording", packet_text)
        self.assertIn("Extraction review status: `pending_yossi_extraction_accuracy_pass`", packet_text)

    def test_pending_slice_translation_metadata_is_conservative(self):
        for row in load_pending_slice_rows():
            with self.subTest(ref=row["ref"], hebrew=row["hebrew_word_or_phrase"]):
                self.assertIn("Metsudah Chumash, Metsudah Publications, 2009", row["source_version_title"])
                self.assertIn("CC-BY", row["source_license"])
                self.assertEqual(row["source_preference"], "primary_preferred_translation_source")
                self.assertEqual(row["requires_attribution"], "true")
                self.assertTrue(row["source_translation_metsudah"])
                self.assertTrue(row["secondary_translation_koren"])
                self.assertIn("bereishis_english_koren.jsonl", row["source_files_used"])
                self.assertNotIn("commercial_use_approved", row["source_files_used"])

    def test_next_slice_reports_exist_and_preserve_review_gates(self):
        build_text = NEXT_SLICE_BUILD_REPORT_PATH.read_text(encoding="utf-8")
        packet_text = NEXT_SLICE_REVIEW_PACKET_PATH.read_text(encoding="utf-8")
        verification_text = NEXT_SLICE_VERIFICATION_REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn("pending Yossi extraction-accuracy review", build_text)
        self.assertIn("does not authorize question generation", build_text)
        self.assertIn("not generated-question review", packet_text)
        self.assertIn("not question approval", packet_text)
        self.assertIn("not protected-preview approval", packet_text)
        self.assertIn("not reviewed-bank approval", packet_text)
        self.assertIn("not runtime approval", packet_text)
        self.assertNotIn("re-approve the educational value", packet_text)
        self.assertIn("Yossi reviewed and verified all 37 rows", verification_text)
        self.assertIn("extraction-accuracy confirmation only", verification_text)
        self.assertIn("Not question approval", verification_text)
        self.assertIn("Not runtime approval", verification_text)
        self.assertIn("`question_allowed` remains `needs_review`", verification_text)
        self.assertIn("`runtime_allowed` remains `false`", verification_text)
        self.assertNotIn("approved for generated questions", verification_text)

    def test_metsudah_is_primary_preferred_cc_by(self):
        for row in load_rows():
            with self.subTest(ref=row["ref"]):
                self.assertEqual(row["source_version_title"], "Metsudah Chumash, Metsudah Publications, 2009")
                self.assertEqual(row["source_license"], "CC-BY")
                self.assertEqual(row["source_preference"], "primary_preferred_translation_source")
                self.assertEqual(row["requires_attribution"], "true")

    def test_koren_is_secondary_noncommercial_support_only(self):
        for row in load_rows():
            with self.subTest(ref=row["ref"]):
                self.assertEqual(row["secondary_source_version_title"], "The Koren Jerusalem Bible")
                self.assertEqual(row["secondary_source_license"], "CC-BY-NC")
                self.assertEqual(row["secondary_source_preference"], "secondary_noncommercial_translation_support")
                self.assertEqual(row["secondary_commercial_use_allowed"], "false")

    def test_proof_map_uses_metsudah_and_koren_context_without_commercial_approval(self):
        for row in load_proof_rows():
            with self.subTest(ref=row["ref"], hebrew=row["hebrew_word_or_phrase"]):
                self.assertIn("CC-BY", row["source_license"])
                self.assertEqual(row["source_preference"], "primary_preferred_translation_source")
                self.assertEqual(row["requires_attribution"], "true")
                self.assertIn("bereishis_english_koren.jsonl", row["source_files_used"])
                self.assertNotIn("commercial_use_approved", row["source_files_used"])

    def test_review_packet_uses_extraction_accuracy_language(self):
        text = REVIEW_PACKET_PATH.read_text(encoding="utf-8")
        self.assertIn("extraction-accuracy confirmation for trusted source-derived content", text)
        self.assertIn("not generated-question review", text)
        self.assertIn("not runtime approval", text)
        self.assertNotIn("re-approve the educational value", text)

    def test_proof_review_packet_exists_and_is_exceptions_only(self):
        text = PROOF_REVIEW_PACKET_PATH.read_text(encoding="utf-8")
        self.assertIn("extraction-accuracy and mapping confirmation for trusted source-derived content", text)
        self.assertIn("not generated-question review", text)
        self.assertIn("not runtime approval", text)
        self.assertIn("Rows With Uncertainty", text)
        self.assertIn("Runtime: blocked", text)

    def test_proof_verification_report_records_yossi_extraction_accuracy_only(self):
        text = PROOF_VERIFICATION_REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn("Yossi reviewed the Bereishis 1:1-1:5 source-to-skill proof map", text)
        self.assertIn("verified all rows for extraction accuracy", text)
        self.assertIn("not runtime approval", text)
        self.assertIn("not question approval", text)
        self.assertIn("Question allowed: `needs_review`", text)
        self.assertNotIn("approved for runtime", text)
        self.assertNotIn("approved for generated questions", text)

    def test_audit_report_records_partial_finding_and_candidate_ingredients(self):
        audit = json.loads(AUDIT_REPORT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(audit["audit_finding"], "partial_not_full_canonical_map")
        self.assertEqual(
            audit["shortest_path_decision"],
            "C_existing_data_is_partial_create_small_proof_consolidation_map",
        )
        self.assertEqual(
            audit["map_created"],
            "data/verified_source_skill_maps/bereishis_1_1_to_1_5_source_to_skill_map.tsv",
        )
        candidate_paths = {candidate["path"] for candidate in audit["candidate_sources"]}
        self.assertIn("data/source_texts/translations/sefaria/bereishis_english_metsudah.jsonl", candidate_paths)
        self.assertIn("data/curriculum_extraction/normalized/linear_chumash_bereishis_1_1_to_1_5_pasuk_segments.seed.jsonl", candidate_paths)
        fields = {entry["field"]: entry for entry in audit["field_coverage"]}
        self.assertEqual(fields["shoresh"]["coverage_status"], "exists partially")
        self.assertFalse(fields["zekelman_standard"]["safe_to_consolidate_automatically"])

    def test_question_template_policy_is_scaffold_only(self):
        text = QUESTION_TEMPLATE_POLICY_PATH.read_text(encoding="utf-8")
        self.assertIn("does not approve any template for use", text)
        self.assertIn("No template in this document is approved for question generation", text)
        self.assertIn("not_runtime_ready", text)
        self.assertIn("not_question_ready", text)

    def test_translation_registry_records_metsudah_and_koren_policy(self):
        registry = json.loads(TRANSLATION_REGISTRY_PATH.read_text(encoding="utf-8"))
        versions = {entry["translation_version_key"]: entry for entry in registry["available_translation_versions"]}
        self.assertEqual(versions["metsudah"]["source_preference"], "primary_preferred_translation_source")
        self.assertEqual(versions["metsudah"]["license"], "CC-BY")
        self.assertTrue(versions["metsudah"]["requires_attribution"])
        self.assertEqual(versions["koren"]["source_preference"], "secondary_noncommercial_translation_support")
        self.assertEqual(versions["koren"]["license"], "CC-BY-NC")
        self.assertEqual(versions["koren"]["commercial_use_status"], "requires_direct_written_permission")
        for entry in versions.values():
            self.assertEqual(entry["runtime_eligibility"], "not_runtime_active")
            self.assertEqual(entry["question_ready_status"], "not_question_ready")
            self.assertEqual(entry["student_facing_status"], "not_student_facing")

    def test_trusted_source_policy_documents_translation_source_order(self):
        text = POLICY_PATH.read_text(encoding="utf-8")
        self.assertIn("Metsudah is the preferred primary translation source", text)
        self.assertIn("Koren may be used only as secondary noncommercial translation support", text)
        self.assertIn("Sefaria availability is not blanket approval", text)


if __name__ == "__main__":
    unittest.main()
