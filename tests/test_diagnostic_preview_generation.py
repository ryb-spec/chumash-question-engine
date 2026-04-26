import json
import unittest
from pathlib import Path

from scripts import generate_diagnostic_preview as generator


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data" / "diagnostic_preview" / "configs" / "bereishis_1_1_to_2_3_dikduk_translation_preview.json"
ATTEMPT_LOG_PATH = ROOT / "data" / "attempt_log.jsonl"
PILOT_LOG_PATH = ROOT / "data" / "pilot" / "pilot_session_events.jsonl"


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


class DiagnosticPreviewGenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.attempt_log_before = ATTEMPT_LOG_PATH.read_bytes()
        cls.pilot_log_before = PILOT_LOG_PATH.read_bytes()
        cls.summary = generator.generate_preview(CONFIG_PATH)
        cls.config = generator.load_config(CONFIG_PATH)
        outputs = cls.config["output_files"]
        cls.blueprint_path = ROOT / outputs["blueprints"]
        cls.question_path = ROOT / outputs["questions"]
        cls.review_packet_path = ROOT / outputs["manual_review_packet"]
        cls.summary_md_path = ROOT / outputs["summary_markdown"]
        cls.summary_json_path = ROOT / outputs["summary_json"]
        cls.blueprints = load_jsonl(cls.blueprint_path)
        cls.questions = load_jsonl(cls.question_path)
        cls.summary_json = load_json(cls.summary_json_path)

    def test_generator_script_exists(self):
        self.assertTrue((ROOT / "scripts" / "generate_diagnostic_preview.py").exists())

    def test_config_exists(self):
        self.assertTrue(CONFIG_PATH.exists())

    def test_generator_produces_expected_artifacts(self):
        self.assertTrue(self.blueprint_path.exists())
        self.assertTrue(self.question_path.exists())
        self.assertTrue(self.review_packet_path.exists())
        self.assertTrue(self.summary_md_path.exists())
        self.assertTrue(self.summary_json_path.exists())

    def test_generation_counts_meet_targets(self):
        minimums = self.config["minimum_question_counts"]
        self.assertGreaterEqual(self.summary_json["total_blueprints"], minimums["total_questions"])
        self.assertGreaterEqual(self.summary_json["total_questions"], minimums["total_questions"])
        self.assertGreaterEqual(self.summary_json["question_count_by_lane"]["translation"], minimums["translation"])
        self.assertGreaterEqual(self.summary_json["question_count_by_lane"]["dikduk"], minimums["dikduk"])
        self.assertGreaterEqual(self.summary_json["question_count_by_lane"]["word_analysis"], minimums["word_analysis"])
        self.assertGreaterEqual(
            self.summary_json["question_count_by_lane"]["error_diagnosis"],
            minimums["error_diagnosis"],
        )
        self.assertGreaterEqual(
            self.summary_json["question_count_by_skill"]["mixed_skill_translation_rule"],
            minimums["mixed_skill"],
        )

    def test_blueprint_and_question_ids_are_unique(self):
        blueprint_ids = [record["blueprint_id"] for record in self.blueprints]
        question_ids = [record["question_id"] for record in self.questions]
        self.assertEqual(len(blueprint_ids), len(set(blueprint_ids)))
        self.assertEqual(len(question_ids), len(set(question_ids)))

    def test_questions_point_to_existing_blueprints(self):
        blueprint_ids = {record["blueprint_id"] for record in self.blueprints}
        for question in self.questions:
            self.assertIn(question["blueprint_id"], blueprint_ids)

    def test_rerunning_generator_does_not_duplicate_rows(self):
        rerun_summary = generator.generate_preview(CONFIG_PATH)
        rerun_blueprints = load_jsonl(self.blueprint_path)
        rerun_questions = load_jsonl(self.question_path)
        self.assertEqual(rerun_summary["total_blueprints"], self.summary_json["total_blueprints"])
        self.assertEqual(rerun_summary["total_questions"], self.summary_json["total_questions"])
        self.assertEqual(len(rerun_blueprints), len(self.blueprints))
        self.assertEqual(len(rerun_questions), len(self.questions))
        self.assertEqual(
            [record["blueprint_id"] for record in rerun_blueprints],
            [record["blueprint_id"] for record in self.blueprints],
        )
        self.assertEqual(
            [record["question_id"] for record in rerun_questions],
            [record["question_id"] for record in self.questions],
        )

    def test_generation_does_not_mutate_runtime_logs(self):
        self.assertEqual(ATTEMPT_LOG_PATH.read_bytes(), self.attempt_log_before)
        self.assertEqual(PILOT_LOG_PATH.read_bytes(), self.pilot_log_before)


if __name__ == "__main__":
    unittest.main()
