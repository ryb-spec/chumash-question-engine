import csv
import json
import unittest
from pathlib import Path

import dikduk_rules_loader
import translation_sources_loader
from scripts import generate_diagnostic_preview as generator
from scripts import validate_diagnostic_preview as validator


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data" / "diagnostic_preview" / "configs" / "bereishis_1_1_to_2_3_dikduk_translation_preview.json"
HEBREW_SOURCE_PATH = ROOT / "data" / "source_texts" / "bereishis_hebrew_menukad_taamim.tsv"
FORBIDDEN_STATUSES = {"active", "runtime_active", "production", "production_ready", "approved", "reviewed"}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_hebrew_refs(path: Path) -> set[str]:
    refs = set()
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            refs.add(f"Genesis {row['perek']}:{row['pasuk']}")
    return refs


class DiagnosticPreviewValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        generator.generate_preview(CONFIG_PATH)
        cls.validation = validator.validate_preview(CONFIG_PATH)
        cls.config = generator.load_config(CONFIG_PATH)
        outputs = cls.config["output_files"]
        cls.blueprints = load_jsonl(ROOT / outputs["blueprints"])
        cls.questions = load_jsonl(ROOT / outputs["questions"])
        cls.summary = load_json(ROOT / outputs["summary_json"])
        cls.review_packet = (ROOT / outputs["manual_review_packet"]).read_text(encoding="utf-8")
        cls.reviewable_paths = generator.reviewable_preview_paths()
        cls.reviewable_questions = load_jsonl(cls.reviewable_paths["questions"])
        cls.reviewable_summary = load_json(cls.reviewable_paths["summary_json"])
        cls.reviewable_packet = cls.reviewable_paths["manual_review_packet"].read_text(encoding="utf-8")
        cls.hebrew_refs = load_hebrew_refs(HEBREW_SOURCE_PATH)
        cls.rule_index = dikduk_rules_loader.dikduk_rule_index()
        cls.error_index = dikduk_rules_loader.dikduk_error_index()
        cls.koren_refs = {row["ref"] for row in translation_sources_loader.load_bereishis_translation("koren")}
        cls.metsudah_refs = {row["ref"] for row in translation_sources_loader.load_bereishis_translation("metsudah")}

    def test_validator_script_exists(self):
        self.assertTrue((ROOT / "scripts" / "validate_diagnostic_preview.py").exists())

    def test_validator_passes(self):
        self.assertTrue(self.validation["valid"], self.validation["errors"])

    def test_refs_align_to_canonical_hebrew(self):
        for blueprint in self.blueprints:
            self.assertIn(blueprint["ref"], self.hebrew_refs)
        for question in self.questions:
            self.assertIn(question["ref"], self.hebrew_refs)

    def test_translation_refs_align_when_used(self):
        for question in self.questions:
            self.assertIn(question["ref"], self.koren_refs)
            self.assertIn(question["ref"], self.metsudah_refs)

    def test_rule_ids_exist_when_used(self):
        for blueprint in self.blueprints:
            for rule_id in blueprint.get("dikduk_rule_ids", []):
                self.assertIn(rule_id, self.rule_index)
        for question in self.questions:
            for rule_id in question.get("dikduk_rule_ids", []):
                self.assertIn(rule_id, self.rule_index)

    def test_no_forbidden_statuses_appear(self):
        self.assertEqual(self.summary["status"], generator.PREVIEW_STATUS)
        self.assertEqual(self.summary["runtime_status"], generator.RUNTIME_STATUS)
        self.assertEqual(self.summary["production_status"], generator.PRODUCTION_STATUS)
        for record in [*self.blueprints, *self.questions]:
            self.assertNotIn(record["status"], FORBIDDEN_STATUSES)

    def test_translation_license_warning_is_preserved(self):
        for blueprint in self.blueprints:
            self.assertEqual(blueprint["translation_usage_status"], generator.TRANSLATION_USAGE_STATUS)
        for question in self.questions:
            self.assertEqual(question["translation_usage_status"], generator.TRANSLATION_USAGE_STATUS)
        self.assertEqual(
            question["source_evidence"]["translation_usage_status"],
            generator.TRANSLATION_USAGE_STATUS,
        )
        self.assertIn(generator.TRANSLATION_USAGE_STATUS, self.review_packet)
        self.assertIn(generator.TRANSLATION_USAGE_STATUS, self.reviewable_packet)

    def test_required_counts_are_met(self):
        self.assertEqual(self.summary["range_covered"]["pesukim_covered"], 34)
        self.assertEqual(self.summary["total_blueprints"], 77)
        self.assertEqual(self.summary["total_questions"], 77)
        self.assertEqual(
            self.summary["question_count_by_lane"],
            {
                "dikduk": 26,
                "error_diagnosis": 10,
                "translation": 26,
                "translation_comparison": 5,
                "word_analysis": 10,
            },
        )

    def test_summary_and_review_packet_exist_and_are_nonempty(self):
        self.assertTrue(self.review_packet.strip())
        self.assertTrue(self.summary["warnings"])
        self.assertTrue(self.summary["ready_for_human_review"])

    def test_reviewable_preview_validator_block_is_present(self):
        self.assertIn("reviewable_preview", self.validation)
        self.assertEqual(self.validation["reviewable_preview"]["total_questions"], len(self.reviewable_questions))

    def test_reviewable_questions_align_to_sources_and_review_schema(self):
        for record in self.reviewable_questions:
            self.assertIn(record["ref"], self.hebrew_refs)
            self.assertIn(record["ref"], self.koren_refs)
            self.assertIn(record["ref"], self.metsudah_refs)
            self.assertIn(record["difficulty_level"], generator.REVIEWABLE_DIFFICULTY_VALUES)
            self.assertIn(record["skill_category"], generator.REVIEWABLE_SKILL_CATEGORIES)
            self.assertIn(record["translation_alignment_status"], generator.REVIEWABLE_TRANSLATION_ALIGNMENT_VALUES)
            self.assertIn(record["review_priority"], generator.REVIEWABLE_REVIEW_PRIORITY_VALUES)
            self.assertIn(record["likely_review_status"], generator.REVIEWABLE_REVIEW_STATUS_VALUES)
            self.assertIn(record["student_readiness_risk"], generator.REVIEWABLE_STUDENT_RISK_VALUES)
            self.assertEqual(record["runtime_status"], generator.REVIEWABLE_RUNTIME_STATUS)
            self.assertEqual(record["production_status"], generator.REVIEWABLE_PRODUCTION_STATUS)
            self.assertEqual(record["translation_usage_status"], generator.TRANSLATION_USAGE_STATUS)
            for flag in record["review_flags"]:
                self.assertIn(flag, generator.REVIEWABLE_REVIEW_FLAGS)
            if record["dikduk_rule_id"]:
                self.assertIn(record["dikduk_rule_id"], self.rule_index)
            if record["student_error_pattern_id"]:
                self.assertIn(record["student_error_pattern_id"], self.error_index)

    def test_reviewable_summary_counts_match_jsonl(self):
        self.assertEqual(self.reviewable_summary["total_questions"], len(self.reviewable_questions))
        self.assertEqual(self.reviewable_summary["final_recommendation"], generator.REVIEWABLE_PREVIEW_FINAL_RECOMMENDATION)
        self.assertGreaterEqual(len(self.reviewable_questions), 30)
        self.assertLessEqual(len(self.reviewable_questions), 45)
        self.assertEqual(self.reviewable_summary["likely_review_status_counts"]["likely_rewrite"], 0)


if __name__ == "__main__":
    unittest.main()
