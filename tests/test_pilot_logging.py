import unittest

from runtime.pilot_logging import build_pilot_export, summarize_attempts


class PilotLoggingTests(unittest.TestCase):
    def test_summary_counts_are_internally_consistent(self):
        attempts = [
            {
                "skill": "identify_prefix_meaning",
                "question_type": None,
                "user_answer": "ל",
                "is_correct": True,
                "pasuk_text": "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
                "in_active_scope": True,
            },
            {
                "skill": "translation",
                "question_type": "word_meaning",
                "user_answer": "earth",
                "is_correct": False,
                "pasuk_text": "וְהָאָרֶץ הָיְתָה תֹהוּ וָבֹהוּ",
                "in_active_scope": True,
            },
            {
                "skill": "identify_suffix_meaning",
                "question_type": "suffix",
                "user_answer": "",
                "is_correct": False,
                "pasuk_text": "לָאוֹר",
                "in_active_scope": False,
            },
        ]

        summary = summarize_attempts(attempts)

        self.assertEqual(summary["served"], 3)
        self.assertEqual(summary["question_type_total_count"], 3)
        self.assertEqual(summary["question_family_total_count"], 3)
        self.assertEqual(summary["answered"], 2)
        self.assertEqual(summary["correct"], 1)
        self.assertEqual(summary["out_of_scope_served"], 1)

    def test_export_sets_consistency_flags(self):
        attempts = [
            {
                "skill": "identify_prefix_meaning",
                "question_type": "prefix",
                "user_answer": "ל",
                "is_correct": True,
                "in_active_scope": True,
            },
            {
                "skill": "translation",
                "question_type": "word_meaning",
                "user_answer": "earth",
                "is_correct": False,
                "in_active_scope": True,
            },
        ]

        export = build_pilot_export(attempts)

        self.assertTrue(export["consistency"]["served_equals_question_type_total"])
        self.assertTrue(export["consistency"]["served_equals_question_family_total"])
        self.assertTrue(export["consistency"]["answered_lte_served"])
        self.assertTrue(export["consistency"]["correct_lte_answered"])


if __name__ == "__main__":
    unittest.main()
