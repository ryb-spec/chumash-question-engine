import unittest
from unittest.mock import patch

import pasuk_flow_generator
from torah_parser.candidate_generator import (
    extract_prefix,
    extract_suffix,
    generate_candidate_analyses,
)


class CandidateGenerationTests(unittest.TestCase):
    def test_candidate_generation_for_active_dataset_verbs(self):
        cases = {
            "\u05d5\u05b7\u05d9\u05bc\u05b9\u05d0\u05de\u05b6\u05e8": ("verb", "vav_consecutive_past", "\u05d0\u05de\u05e8"),
            "\u05d9\u05b4\u05e7\u05bc\u05b8\u05d5\u05d5\u05bc": ("verb", "future_jussive", "\u05e7\u05d5\u05d4"),
            "\u05d5\u05b0\u05ea\u05b5\u05e8\u05b8\u05d0\u05b6\u05d4": ("verb", "future_jussive", "\u05e8\u05d0\u05d4"),
            "\u05d5\u05b4\u05d9\u05d4\u05b4\u05d9": ("verb", "future_jussive", "\u05d4\u05d9\u05d4"),
        }

        for token, expected in cases.items():
            primary = generate_candidate_analyses(token)[0]
            self.assertEqual(
                (primary.get("part_of_speech"), primary.get("tense"), primary.get("shoresh")),
                expected,
            )

    def test_prefix_and_suffix_helpers_are_conservative(self):
        self.assertEqual(extract_prefix("\u05dc\u05b8\u05d0\u05d5\u05b9\u05e8"), "\u05dc")
        self.assertIsNone(extract_prefix("\u05e9\u05c1\u05b0\u05dc\u05b4\u05d9\u05e9\u05c1\u05b4\u05d9"))
        self.assertIsNone(extract_prefix("\u05e9\u05c1\u05b8\u05de\u05b7\u05d9\u05b4\u05dd"))
        self.assertEqual(extract_prefix("\u05d5\u05b7\u05d9\u05bc\u05b9\u05d0\u05de\u05b6\u05e8"), "\u05d5")
        self.assertIsNone(extract_suffix("\u05d9\u05d5\u05b9\u05dd"))
        self.assertIsNone(extract_suffix("\u05de\u05b7\u05d9\u05b4\u05dd"))
        self.assertIsNone(extract_suffix("\u05d9\u05b4\u05e7\u05bc\u05b8\u05d5\u05d5\u05bc"))
        self.assertEqual(extract_suffix("\u05d6\u05b7\u05e8\u05b0\u05e2\u05d5\u05b9"), "\u05d5")

    def test_active_generator_uses_torah_parser_tokenizer(self):
        with patch.object(
            pasuk_flow_generator,
            "parser_tokenize_pasuk",
            return_value=[
                "\u05d5\u05b7\u05d9\u05bc\u05b9\u05d0\u05de\u05b6\u05e8",
                "\u05d0\u05b1\u05dc\u05b9\u05e7\u05b4\u05d9\u05dd",
            ],
        ) as mocked:
            tokens = pasuk_flow_generator.tokenize_pasuk("ignored")

        mocked.assert_called_once_with("ignored")
        self.assertEqual(
            tokens,
            [
                "\u05d5\u05b7\u05d9\u05bc\u05b9\u05d0\u05de\u05b6\u05e8",
                "\u05d0\u05b1\u05dc\u05b9\u05e7\u05b4\u05d9\u05dd",
            ],
        )

    def test_active_generator_uses_torah_parser_candidate_generation(self):
        with patch.object(
            pasuk_flow_generator,
            "parser_generate_candidate_analyses",
            return_value=[
                {
                    "part_of_speech": "verb",
                    "tense": "past",
                    "prefixes": [],
                    "suffixes": [],
                }
            ],
        ) as mocked:
            analysis = pasuk_flow_generator.analyze_word("\u05d1\u05bc\u05b8\u05e8\u05b8\u05d0")

        mocked.assert_called_once_with("\u05d1\u05bc\u05b8\u05e8\u05b8\u05d0")
        self.assertTrue(analysis["is_verb"])
        self.assertEqual(analysis["tense"], "past")


if __name__ == "__main__":
    unittest.main()
