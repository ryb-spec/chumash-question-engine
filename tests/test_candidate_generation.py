import unittest
from unittest.mock import patch

import pasuk_flow_generator
from torah_parser.candidate_generator import (
    apply_prefix_metadata,
    apply_suffix_metadata,
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

    def test_apply_prefix_metadata_ignores_legacy_placeholder_prefix_marker(self):
        entry = {
            "prefix": "?",
            "prefix_meaning": "and",
            "prefixes": [],
        }

        updated = apply_prefix_metadata("\u05d5\u05b7\u05d9\u05b0\u05d1\u05b8\u05e8\u05b6\u05da\u05b0", entry, word_bank={})

        self.assertEqual(updated["prefix"], "\u05d5")
        self.assertEqual(updated["prefix_meaning"], "and")

    def test_apply_suffix_metadata_does_not_infer_pronoun_suffix_for_pronoun_forms(self):
        entry = generate_candidate_analyses("\u05d5\u05b0\u05d0\u05b7\u05ea\u05b8\u05bc\u05d4")[0]

        updated = apply_suffix_metadata("\u05d5\u05b0\u05d0\u05b7\u05ea\u05b8\u05bc\u05d4", dict(entry), word_bank={})

        self.assertEqual(updated["suffix"], "")
        self.assertEqual(updated["suffix_meaning"], "")

    def test_high_value_3_9_to_3_16_forms_now_have_explicit_surface_support(self):
        cases = {
            "\u05e9\u05b8\u05c1\u05de\u05b7\u05e2\u05b0\u05ea\u05b4\u05bc\u05d9": ("verb", "past", "\u05e9\u05de\u05e2", "heard"),
            "\u05e2\u05b8\u05e9\u05b4\u05c2\u05d9\u05ea\u05b8": ("verb", "past", "\u05e2\u05e9\u05d4", "you did"),
            "\u05d0\u05b8\u05e9\u05b4\u05c1\u05d9\u05ea": ("verb", "future", "\u05e9\u05d9\u05ea", "I will put"),
            "\u05d0\u05b7\u05e8\u05b0\u05d1\u05b6\u05bc\u05d4": ("verb", "future", "\u05e8\u05d1\u05d4", "I will greatly increase"),
            "\u05d9\u05b4\u05de\u05b0\u05e9\u05b8\u05c1\u05dc": ("verb", "future", "\u05de\u05e9\u05dc", "he will rule"),
        }

        for token, expected in cases.items():
            primary = generate_candidate_analyses(token)[0]
            self.assertEqual(
                (
                    primary.get("part_of_speech"),
                    primary.get("tense"),
                    primary.get("shoresh"),
                    primary.get("translation_context"),
                ),
                expected,
            )

    def test_former_staged_placeholder_blockers_now_have_explicit_surface_support(self):
        cases = {
            "\u05e6\u05b4\u05d5\u05b4\u05bc\u05d9\u05ea\u05b4\u05d9\u05da\u05b8": ("verb", "past", "\u05e6\u05d5\u05d4", "I commanded you"),
            "\u05d0\u05b2\u05db\u05b8\u05dc": ("verb", "infinitive", "\u05d0\u05db\u05dc", "eat"),
            "\u05d4\u05b4\u05e9\u05b4\u05bc\u05c1\u05d9\u05d0\u05b7\u05e0\u05b4\u05d9": ("verb", "past", None, "deceived me"),
            "\u05d9\u05b0\u05e9\u05c1\u05d5\u05bc\u05e4\u05b0\u05da\u05b8": ("verb", "future", None, "he will bruise you"),
            "\u05ea\u05b0\u05bc\u05e9\u05c1\u05d5\u05bc\u05e4\u05b6\u05e0\u05bc\u05d5\u05bc": ("verb", "future", None, "you will bruise him"),
        }

        for token, expected in cases.items():
            primary = generate_candidate_analyses(token)[0]
            self.assertEqual(
                (
                    primary.get("part_of_speech"),
                    primary.get("tense"),
                    primary.get("shoresh"),
                    primary.get("translation_context"),
                ),
                expected,
            )

    def test_remaining_staged_placeholder_forms_now_have_explicit_surface_support(self):
        cases = {
            "\u05de\u05d5\u05b9\u05ea": ("verb", "infinitive", "\u05de\u05d5\u05ea", "surely die"),
            "\u05d0\u05b2\u05db\u05b8\u05dc\u05b0\u05db\u05b6\u05dd": ("verb", "infinitive", "\u05d0\u05db\u05dc", "when you eat"),
            "\u05d5\u05b0\u05db\u05b4\u05d9": ("particle", None, None, "and that"),
            "\u05d4\u05b5\u05dd": ("pronoun", None, None, "they"),
            "\u05dc\u05b0\u05e8\u05d5\u05bc\u05d7\u05b7": ("noun", None, "\u05e8\u05d5\u05d7", "at the breezy time of"),
        }

        for token, expected in cases.items():
            primary = generate_candidate_analyses(token)[0]
            self.assertEqual(
                (
                    primary.get("part_of_speech"),
                    primary.get("tense"),
                    primary.get("shoresh"),
                    primary.get("translation_context"),
                ),
                expected,
            )

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
