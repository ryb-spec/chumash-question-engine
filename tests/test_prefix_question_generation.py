import unittest

import pasuk_flow_generator


class PrefixQuestionGenerationTests(unittest.TestCase):
    def test_shlishi_does_not_generate_prefix_question(self):
        question = pasuk_flow_generator.generate_question(
            "identify_prefix_meaning",
            "שְׁלִישִׁי",
        )

        self.assertEqual(question.get("status"), "skipped")
        self.assertIn("No usable prefixed word", question.get("reason", ""))

    def test_shamayim_does_not_generate_prefix_question(self):
        question = pasuk_flow_generator.generate_question(
            "identify_prefix_meaning",
            "שָׁמַיִם",
        )

        self.assertEqual(question.get("status"), "skipped")
        self.assertIn("No usable prefixed word", question.get("reason", ""))

    def test_true_prefixed_word_still_generates_prefix_question(self):
        question = pasuk_flow_generator.generate_question(
            "identify_prefix_meaning",
            "לָאוֹר",
        )

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("selected_word"), "לָאוֹר")
        self.assertEqual(question.get("correct_answer"), "ל")


if __name__ == "__main__":
    unittest.main()
