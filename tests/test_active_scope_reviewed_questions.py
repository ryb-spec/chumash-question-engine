import unittest

from assessment_scope import (
    active_pasuk_id_set,
    active_pesukim_records,
    active_scope_reviewed_question_records,
    load_active_scope_reviewed_questions_data,
)
from engine.flow_builder import generate_question
from scripts.build_reviewed_question_bank import validate_reviewed_bank


def pasuk_by_id(pasuk_id):
    for record in active_pesukim_records():
        if record.get("pasuk_id") == pasuk_id:
            return record["text"]
    raise AssertionError(f"Missing active pasuk {pasuk_id}")


class ActiveScopeReviewedQuestionTests(unittest.TestCase):
    def test_reviewed_question_bank_validates_cleanly(self):
        payload = load_active_scope_reviewed_questions_data()
        summary = validate_reviewed_bank(payload)

        self.assertTrue(summary["valid"])
        self.assertFalse(summary["issues"])
        self.assertFalse(summary["duplicate_items"])
        self.assertFalse(summary["duplicate_reviewed_ids"])
        self.assertGreaterEqual(summary["lane_counts"].get("translation", 0), 25)
        self.assertGreaterEqual(summary["lane_counts"].get("affix", 0), 25)
        self.assertGreaterEqual(summary["lane_counts"].get("shoresh", 0), 25)
        self.assertGreaterEqual(summary["lane_counts"].get("tense", 0), 25)
        self.assertEqual(summary["baseline_lane_counts"].get("shoresh"), 17)
        self.assertEqual(summary["baseline_lane_counts"].get("tense"), 18)
        self.assertGreaterEqual(summary["lane_count_delta"].get("shoresh", 0), 8)
        self.assertGreaterEqual(summary["lane_count_delta"].get("tense", 0), 7)
        self.assertFalse(summary["shortfalls"])
        self.assertTrue(summary["morphology_support_additions"])

    def test_reviewed_questions_stay_inside_active_scope(self):
        active_ids = set(active_pasuk_id_set())

        for question in active_scope_reviewed_question_records():
            self.assertIn(question.get("pasuk_id"), active_ids)

    def test_reviewed_bank_limits_duplicate_feel_padding_in_shoresh_and_tense(self):
        payload = load_active_scope_reviewed_questions_data()
        summary = validate_reviewed_bank(payload)

        for repeated in summary["repeated_targets"]:
            if repeated["family"] in {"shoresh", "tense"}:
                self.assertLessEqual(repeated["count"], 2)

    def test_runtime_prefers_reviewed_translation_when_available(self):
        question = generate_question("translation", pasuk_by_id("bereishis_2_7"))

        self.assertEqual(question.get("analysis_source"), "active_scope_reviewed_bank")
        self.assertEqual(question.get("selected_word"), "נִשְׁמַת")
        self.assertEqual(question.get("correct_answer"), "breath of")

    def test_runtime_prefers_reviewed_backfilled_shoresh_when_available(self):
        question = generate_question("shoresh", pasuk_by_id("bereishis_2_8"))

        self.assertEqual(question.get("analysis_source"), "active_scope_reviewed_bank")
        self.assertEqual(question.get("selected_word"), "וַיִּטַּע")
        self.assertEqual(question.get("correct_answer"), "נטע")

    def test_runtime_prefers_reviewed_tense_alias_for_verb_tense(self):
        question = generate_question("verb_tense", pasuk_by_id("bereishis_1_6"))

        self.assertEqual(question.get("analysis_source"), "active_scope_reviewed_bank")
        self.assertEqual(question.get("question_type"), "verb_tense")
        self.assertEqual(question.get("skill"), "verb_tense")
        self.assertEqual(question.get("selected_word"), "וִיהִי")
        self.assertEqual(question.get("correct_answer"), "future")

    def test_runtime_prefers_reviewed_backfilled_infinitive_tense_alias(self):
        question = generate_question("verb_tense", pasuk_by_id("bereishis_2_4"))

        self.assertEqual(question.get("analysis_source"), "active_scope_reviewed_bank")
        self.assertEqual(question.get("question_type"), "verb_tense")
        self.assertEqual(question.get("skill"), "verb_tense")
        self.assertEqual(question.get("selected_word"), "עֲשׂוֹת")
        self.assertEqual(question.get("correct_answer"), "to do form")
        self.assertEqual(question.get("tense_code"), "infinitive")

    def test_runtime_falls_back_when_no_reviewed_question_exists_for_skill(self):
        question = generate_question("part_of_speech", pasuk_by_id("bereishis_1_1"))

        self.assertNotEqual(question.get("analysis_source"), "active_scope_reviewed_bank")


if __name__ == "__main__":
    unittest.main()
