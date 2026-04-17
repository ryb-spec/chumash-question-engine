import unittest

import pasuk_flow_generator


class SuffixQuestionGenerationTests(unittest.TestCase):
    def test_yom_does_not_generate_suffix_question(self):
        question = pasuk_flow_generator.generate_question(
            "identify_suffix_meaning",
            "יוֹם",
        )

        self.assertEqual(question.get("status"), "skipped")
        self.assertIn("No suffixed word found", question.get("reason", ""))

    def test_mayim_does_not_generate_suffix_question(self):
        question = pasuk_flow_generator.generate_question(
            "identify_suffix_meaning",
            "מַיִם",
        )

        self.assertEqual(question.get("status"), "skipped")
        self.assertIn("No suffixed word found", question.get("reason", ""))

    def test_true_suffix_bearing_word_still_generates_suffix_question(self):
        question = pasuk_flow_generator.generate_question(
            "identify_suffix_meaning",
            "זַרְעוֹ",
        )

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("selected_word"), "זַרְעוֹ")
        self.assertEqual(question.get("correct_answer"), "his")


if __name__ == "__main__":
    unittest.main()
