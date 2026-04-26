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
        cls.reviewable_paths = generator.reviewable_preview_paths()
        cls.reviewable_question_path = cls.reviewable_paths["questions"]
        cls.reviewable_packet_path = cls.reviewable_paths["manual_review_packet"]
        cls.reviewable_summary_path = cls.reviewable_paths["summary_json"]
        cls.blueprints = load_jsonl(cls.blueprint_path)
        cls.questions = load_jsonl(cls.question_path)
        cls.summary_json = load_json(cls.summary_json_path)
        cls.reviewable_questions = load_jsonl(cls.reviewable_question_path)
        cls.reviewable_summary = load_json(cls.reviewable_summary_path)

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
        self.assertTrue(self.reviewable_question_path.exists())
        self.assertTrue(self.reviewable_packet_path.exists())
        self.assertTrue(self.reviewable_summary_path.exists())

    def test_existing_ai_review_findings_are_preserved_in_manual_review_packet(self):
        packet_text = self.review_packet_path.read_text(encoding="utf-8")
        self.assertIn("## AI-Assisted Review Findings", packet_text)

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

    def test_reviewable_preview_stays_small_and_curated(self):
        self.assertGreaterEqual(len(self.reviewable_questions), 30)
        self.assertLessEqual(len(self.reviewable_questions), 45)
        self.assertEqual(self.reviewable_summary["total_questions"], len(self.reviewable_questions))
        self.assertEqual(
            self.reviewable_summary["final_recommendation"],
            generator.REVIEWABLE_PREVIEW_FINAL_RECOMMENDATION,
        )

    def test_blueprint_and_question_ids_are_unique(self):
        blueprint_ids = [record["blueprint_id"] for record in self.blueprints]
        question_ids = [record["question_id"] for record in self.questions]
        self.assertEqual(len(blueprint_ids), len(set(blueprint_ids)))
        self.assertEqual(len(question_ids), len(set(question_ids)))
        reviewable_ids = [record["question_id"] for record in self.reviewable_questions]
        self.assertEqual(len(reviewable_ids), len(set(reviewable_ids)))
        self.assertEqual(
            len({record["source_preview_question_id"] for record in self.reviewable_questions}),
            len(self.reviewable_questions),
        )

    def test_questions_point_to_existing_blueprints(self):
        blueprint_ids = {record["blueprint_id"] for record in self.blueprints}
        for question in self.questions:
            self.assertIn(question["blueprint_id"], blueprint_ids)

    def test_rerunning_generator_does_not_duplicate_rows(self):
        rerun_summary = generator.generate_preview(CONFIG_PATH)
        rerun_blueprints = load_jsonl(self.blueprint_path)
        rerun_questions = load_jsonl(self.question_path)
        rerun_reviewable_questions = load_jsonl(self.reviewable_question_path)
        self.assertEqual(rerun_summary["total_blueprints"], self.summary_json["total_blueprints"])
        self.assertEqual(rerun_summary["total_questions"], self.summary_json["total_questions"])
        self.assertEqual(len(rerun_blueprints), len(self.blueprints))
        self.assertEqual(len(rerun_questions), len(self.questions))
        self.assertEqual(len(rerun_reviewable_questions), len(self.reviewable_questions))
        self.assertEqual(
            [record["blueprint_id"] for record in rerun_blueprints],
            [record["blueprint_id"] for record in self.blueprints],
        )
        self.assertEqual(
            [record["question_id"] for record in rerun_questions],
            [record["question_id"] for record in self.questions],
        )
        self.assertEqual(
            [record["question_id"] for record in rerun_reviewable_questions],
            [record["question_id"] for record in self.reviewable_questions],
        )

    def test_reviewable_questions_have_required_review_fields(self):
        required_fields = {
            "question_id",
            "source_preview_question_id",
            "sefer",
            "perek",
            "pasuk",
            "ref",
            "question_text",
            "answer_choices",
            "correct_answer",
            "student_explanation",
            "difficulty_level",
            "skill_category",
            "hebrew_word_or_phrase",
            "hebrew_context",
            "koren_translation_support",
            "metsudah_translation_support",
            "translation_alignment_status",
            "source_support_note",
            "dikduk_rule_id",
            "dikduk_rule_name",
            "dikduk_rule_summary",
            "student_error_pattern_id",
            "student_error_pattern_summary",
            "review_priority",
            "likely_review_status",
            "review_flags",
            "why_this_question_was_generated",
            "what_the_question_tests",
            "why_the_correct_answer_is_correct",
            "why_each_distractor_is_wrong",
            "possible_alternate_answers",
            "teacher_review_note",
            "student_readiness_risk",
            "status",
            "runtime_status",
            "production_status",
            "translation_usage_status",
        }
        for record in self.reviewable_questions:
            self.assertTrue(required_fields.issubset(record))
            self.assertIn(record["correct_answer"], record["answer_choices"])
            self.assertIsInstance(record["review_flags"], list)
            self.assertIsInstance(record["why_each_distractor_is_wrong"], dict)
            self.assertEqual(
                set(record["why_each_distractor_is_wrong"]),
                {choice for choice in record["answer_choices"] if choice != record["correct_answer"]},
            )

    def test_generation_does_not_mutate_runtime_logs(self):
        self.assertEqual(ATTEMPT_LOG_PATH.read_bytes(), self.attempt_log_before)
        self.assertEqual(PILOT_LOG_PATH.read_bytes(), self.pilot_log_before)


if __name__ == "__main__":
    unittest.main()
