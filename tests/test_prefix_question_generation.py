import unittest

import pasuk_flow_generator


class PrefixQuestionGenerationTests(unittest.TestCase):
    def test_shlishi_does_not_generate_prefix_question(self):
        question = pasuk_flow_generator.generate_question(
            "identify_prefix_meaning",
            "\u05e9\u05c1\u05b0\u05dc\u05b4\u05d9\u05e9\u05c1\u05b4\u05d9",
        )

        self.assertEqual(question.get("status"), "skipped")
        self.assertIn("No usable prefixed word", question.get("reason", ""))

    def test_shamayim_does_not_generate_prefix_question(self):
        question = pasuk_flow_generator.generate_question(
            "identify_prefix_meaning",
            "\u05e9\u05b8\u05c1\u05de\u05b7\u05d9\u05b4\u05dd",
        )

        self.assertEqual(question.get("status"), "skipped")
        self.assertIn("No usable prefixed word", question.get("reason", ""))

    def test_true_prefixed_word_still_generates_prefix_question(self):
        question = pasuk_flow_generator.generate_question(
            "identify_prefix_meaning",
            "\u05dc\u05b8\u05d0\u05d5\u05b9\u05e8",
        )

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("selected_word"), "\u05dc\u05b8\u05d0\u05d5\u05b9\u05e8")
        self.assertEqual(question.get("correct_answer"), "\u05dc")

    def test_stacked_prefix_letters_are_not_treated_as_single_clear_prefix_question(self):
        is_valid, reason = pasuk_flow_generator.prefix_question_validation(
            "\u05d5\u05dc\u05de\u05e8\u05d0\u05d4",
            {
                "prefix": "\u05d5",
                "prefixes": [
                    {"form": "\u05d5", "translation": "and"},
                    {"form": "\u05dc", "translation": "to / for"},
                ],
            },
            correct_answer="\u05d5",
            choices=["\u05d5", "\u05dc", "\u05d1", "\u05db"],
        )

        self.assertFalse(is_valid)
        self.assertIn("multiple defensible prefixes", reason)

    def test_suffix_bearing_stacked_form_is_not_a_valid_simple_prefix_question(self):
        is_valid, reason = pasuk_flow_generator.prefix_question_validation(
            "\u05d5\u05dc\u05de\u05d9\u05de\u05d9\u05d5",
            {
                "prefix": "\u05d5",
                "prefixes": [
                    {"form": "\u05d5", "translation": "and"},
                    {"form": "\u05dc", "translation": "to / for"},
                ],
                "suffix": "\u05d9\u05d5",
            },
            correct_answer="\u05d5",
            choices=["\u05d5", "\u05dc", "\u05d1", "\u05de"],
        )

        self.assertFalse(is_valid)
        self.assertIn("multiple defensible prefixes", reason)

    def test_plausible_distractor_meaning_is_rejected(self):
        is_valid, reason = pasuk_flow_generator.prefix_question_validation(
            "\u05d5\u05dc\u05de\u05e7\u05d5\u05d4",
            {
                "prefix": "\u05d5",
                "prefixes": [
                    {"form": "\u05d5", "translation": "and"},
                    {"form": "\u05dc", "translation": "to / for"},
                ],
            },
            correct_answer="and",
            choices=["and", "to / for", "from", "the"],
        )

        self.assertFalse(is_valid)
        self.assertIn("multiple defensible prefixes", reason)

    def test_single_clear_prefix_with_suffix_still_validates(self):
        is_valid, reason = pasuk_flow_generator.prefix_question_validation(
            "\u05d1\u05e6\u05dc\u05de\u05e0\u05d5",
            {
                "prefix": "\u05d1",
                "prefixes": [
                    {"form": "\u05d1", "translation": "in / with"},
                ],
                "suffix": "\u05e0\u05d5",
            },
            correct_answer="\u05d1",
            choices=["\u05d1", "\u05dc", "\u05de", "\u05db"],
        )

        self.assertTrue(is_valid)
        self.assertEqual(reason, "")


if __name__ == "__main__":
    unittest.main()
