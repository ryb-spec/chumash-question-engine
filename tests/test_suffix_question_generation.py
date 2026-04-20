import unittest

import pasuk_flow_generator


class SuffixQuestionGenerationTests(unittest.TestCase):
    def test_yom_does_not_generate_suffix_question(self):
        question = pasuk_flow_generator.generate_question(
            "identify_suffix_meaning",
            "\u05d9\u05d5\u05b9\u05dd",
        )

        self.assertEqual(question.get("status"), "skipped")
        self.assertIn("No suffixed word found", question.get("reason", ""))

    def test_mayim_does_not_generate_suffix_question(self):
        question = pasuk_flow_generator.generate_question(
            "identify_suffix_meaning",
            "\u05de\u05b7\u05d9\u05b4\u05dd",
        )

        self.assertEqual(question.get("status"), "skipped")
        self.assertIn("No suffixed word found", question.get("reason", ""))

    def test_true_suffix_bearing_word_still_generates_suffix_question(self):
        question = pasuk_flow_generator.generate_question(
            "identify_suffix_meaning",
            "\u05d6\u05b7\u05e8\u05b0\u05e2\u05d5\u05b9",
        )

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("selected_word"), "\u05d6\u05b7\u05e8\u05b0\u05e2\u05d5\u05b9")
        self.assertEqual(question.get("correct_answer"), "his")

    def test_suffix_meaning_questions_use_lane_consistent_meaning_choices(self):
        suffix_question = pasuk_flow_generator.generate_question(
            "identify_suffix_meaning",
            "\u05d6\u05b7\u05e8\u05b0\u05e2\u05d5\u05b9",
        )
        pronoun_question = pasuk_flow_generator.generate_question(
            "identify_pronoun_suffix",
            "\u05d6\u05b7\u05e8\u05b0\u05e2\u05d5\u05b9",
        )

        expected_bank = set(pasuk_flow_generator.SUFFIX_MEANINGS.values())
        self.assertNotEqual(suffix_question.get("status"), "skipped")
        self.assertNotEqual(pronoun_question.get("status"), "skipped")
        self.assertTrue(set(suffix_question.get("choices", [])).issubset(expected_bank))
        self.assertTrue(set(pronoun_question.get("choices", [])).issubset(expected_bank))
        self.assertTrue(all(not any("\u0590" <= char <= "\u05ff" for char in choice) for choice in suffix_question.get("choices", [])))
        self.assertTrue(all(not any("\u0590" <= char <= "\u05ff" for char in choice) for choice in pronoun_question.get("choices", [])))

    def test_veshanim_lexical_plural_ending_is_not_treated_as_pronominal_suffix(self):
        is_valid, reason = pasuk_flow_generator.suffix_question_validation(
            "\u05d5\u05b0\u05e9\u05c1\u05b8\u05e0\u05b4\u05d9\u05dd",
            {
                "type": "noun",
                "suffix": "\u05dd",
            },
            correct_answer="their",
            choices=["their", "his", "our", "my"],
        )

        self.assertFalse(is_valid)
        self.assertIn("plural/lexical ending", reason)

    def test_veshanim_does_not_generate_bogus_pronoun_or_segmentation_prompt(self):
        pronoun_question = pasuk_flow_generator.generate_question(
            "identify_pronoun_suffix",
            "\u05d5\u05b0\u05e9\u05c1\u05b8\u05e0\u05b4\u05d9\u05dd",
        )
        segmentation_question = pasuk_flow_generator.generate_question(
            "segment_word_parts",
            "\u05d5\u05b0\u05e9\u05c1\u05b8\u05e0\u05b4\u05d9\u05dd",
        )

        self.assertEqual(pronoun_question.get("status"), "skipped")
        self.assertIn("No pronoun suffix found", pronoun_question.get("reason", ""))
        self.assertNotIn("their", pronoun_question.get("question", ""))
        self.assertNotEqual(segmentation_question.get("correct_answer"), "their")
        self.assertNotIn("their", segmentation_question.get("question", ""))

    def test_segment_word_parts_affix_choices_stay_unit_consistent(self):
        prefix_question = pasuk_flow_generator.generate_question(
            "segment_word_parts",
            "\u05dc\u05b8\u05d0\u05d5\u05b9\u05e8",
        )
        suffix_question = pasuk_flow_generator.generate_question(
            "segment_word_parts",
            "\u05d6\u05b7\u05e8\u05b0\u05e2\u05d5\u05b9",
        )

        self.assertNotEqual(prefix_question.get("status"), "skipped")
        self.assertEqual(prefix_question.get("morpheme_type"), "prefix")
        self.assertTrue(
            set(prefix_question.get("choices", [])).issubset(set(pasuk_flow_generator.PREFIX_FORM_BANK))
        )

        self.assertNotEqual(suffix_question.get("status"), "skipped")
        self.assertEqual(suffix_question.get("morpheme_type"), "suffix")
        self.assertTrue(
            set(suffix_question.get("choices", [])).issubset(set(pasuk_flow_generator.SUFFIX_FORM_BANK))
        )

    def test_segment_word_parts_rejects_mixed_shape_answer_banks(self):
        with self.assertRaises(ValueError):
            pasuk_flow_generator.validate_question_payload(
                {
                    "question": "Which part means 'to / for'?",
                    "choices": ["\u05dc", "\u05e9\u05c1\u05b9\u05e8\u05b6\u05e9\u05c1", "\u05dd", "\u05dc\u05b8\u05d0\u05d5\u05b9\u05e8"],
                    "correct_answer": "\u05dc",
                    "skill": "segment_word_parts",
                    "question_type": "segment_word_parts",
                    "morpheme_type": "prefix",
                }
            )

    def test_stacked_ambiguous_endings_are_not_treated_as_single_clear_suffix_question(self):
        is_valid, reason = pasuk_flow_generator.suffix_question_validation(
            "\u05de\u05d9\u05de\u05d9\u05d5",
            {
                "suffix": "\u05d9\u05d5",
                "suffixes": [
                    {"form": "\u05d9\u05d5", "translation": "his"},
                    {"form": "\u05d5", "translation": "his"},
                ],
            },
            correct_answer="his",
            choices=["his", "their", "our", "my"],
        )

        self.assertFalse(is_valid)
        self.assertIn("multiple defensible suffixes", reason)

    def test_plausible_alternate_suffix_choice_is_rejected(self):
        is_valid, reason = pasuk_flow_generator.suffix_question_validation(
            "\u05d6\u05b7\u05e8\u05b0\u05e2\u05d5\u05b9",
            {
                "suffix": "\u05d5",
                "suffixes": [
                    {"form": "\u05d5", "translation": "his"},
                ],
            },
            correct_answer="\u05d5",
            choices=["\u05d5", "\u05d9\u05d5", "\u05e0\u05d5", "\u05d9"],
        )

        self.assertFalse(is_valid)
        self.assertIn("more than one plausible correct answer", reason)

    def test_single_clear_suffix_still_validates(self):
        is_valid, reason = pasuk_flow_generator.suffix_question_validation(
            "\u05d6\u05b7\u05e8\u05b0\u05e2\u05d5\u05b9",
            {
                "suffix": "\u05d5",
                "suffixes": [
                    {"form": "\u05d5", "translation": "his"},
                ],
            },
            correct_answer="his",
            choices=["his", "their", "our", "my"],
        )

        self.assertTrue(is_valid)
        self.assertEqual(reason, "")

    def test_single_prefix_plus_clear_suffix_still_validates(self):
        is_valid, reason = pasuk_flow_generator.suffix_question_validation(
            "\u05d1\u05e6\u05dc\u05de\u05e0\u05d5",
            {
                "prefix": "\u05d1",
                "prefixes": [
                    {"form": "\u05d1", "translation": "in / with"},
                ],
                "suffix": "\u05e0\u05d5",
                "suffixes": [
                    {"form": "\u05e0\u05d5", "translation": "our"},
                ],
            },
            correct_answer="our",
            choices=["our", "his", "their", "my"],
        )

        self.assertTrue(is_valid)
        self.assertEqual(reason, "")

    def test_context_dependent_suffix_interpretation_is_rejected(self):
        is_valid, reason = pasuk_flow_generator.suffix_question_validation(
            "\u05ea\u05d0\u05de\u05e8\u05d9",
            {
                "part_of_speech": "verb",
                "tense": "future",
                "suffix": "\u05d9",
                "suffixes": [
                    {"form": "\u05d9", "translation": "my"},
                ],
            },
            correct_answer="my",
            choices=["my", "his", "our", "their"],
        )

        self.assertFalse(is_valid)
        self.assertIn("isolated-word suffix question", reason)

    def test_stacked_prefix_plus_suffix_form_is_skipped_for_simple_suffix_question(self):
        question = pasuk_flow_generator.generate_question(
            "identify_suffix_meaning",
            "\u05d5\u05dc\u05de\u05d9\u05de\u05d9\u05d5",
        )

        self.assertEqual(question.get("status"), "skipped")
        self.assertIn("No suffixed word found", question.get("reason", ""))


if __name__ == "__main__":
    unittest.main()
