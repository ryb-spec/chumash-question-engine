import unittest
from unittest.mock import patch

import pasuk_flow_generator
import runtime.question_flow as question_flow
from assessment_scope import active_pesukim_records


def _verb_entry(shoresh, tense, **overrides):
    entry = {
        "type": "verb",
        "part_of_speech": "verb",
        "shoresh": shoresh,
        "tense": tense,
        "confidence": "reviewed",
        "prefixes": [],
        "suffixes": [],
    }
    entry.update(overrides)
    return entry


class QuestionValidationFrameworkTests(unittest.TestCase):
    def test_validator_registry_covers_expected_skill_types(self):
        for skill in (
            "identify_prefix_meaning",
            "prefix",
            "identify_suffix_meaning",
            "identify_pronoun_suffix",
            "suffix",
            "shoresh",
            "verb_tense",
            "identify_tense",
        ):
            self.assertIn(skill, pasuk_flow_generator.QUESTION_VALIDATOR_REGISTRY)

    def test_prefix_dispatch_preserves_existing_ambiguous_prefix_rejection(self):
        result = pasuk_flow_generator.validate_question_candidate(
            "identify_prefix_meaning",
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

        self.assertFalse(result["valid"])
        self.assertIn("multiple_prefixes", result["reason_codes"])

    def test_shoresh_validator_accepts_clear_case(self):
        result = pasuk_flow_generator.validate_question_candidate(
            "shoresh",
            "\u05d5\u05d9\u05d0\u05de\u05e8",
            _verb_entry(
                "\u05d0\u05de\u05e8",
                "past",
                prefix="\u05d5",
                prefixes=[{"form": "\u05d5", "translation": "and"}],
            ),
            correct_answer="\u05d0\u05de\u05e8",
            choices=["\u05d0\u05de\u05e8", "\u05e8\u05d0\u05d4", "\u05e0\u05ea\u05df", "\u05e7\u05e8\u05d0"],
        )

        self.assertTrue(result["valid"])
        self.assertEqual(result["reason_codes"], [])

    def test_shoresh_validator_rejects_selection_distractor_leakage(self):
        target_entry = _verb_entry(
            "\u05d0\u05de\u05e8",
            "past",
            prefix="\u05d5",
            prefixes=[{"form": "\u05d5", "translation": "and"}],
        )
        choice_entries = {
            "\u05d5\u05d9\u05d0\u05de\u05e8": target_entry,
            "\u05d5\u05d9\u05d0\u05de\u05e8\u05d5": _verb_entry(
                "\u05d0\u05de\u05e8",
                "past",
                prefix="\u05d5",
                prefixes=[{"form": "\u05d5", "translation": "and"}],
            ),
            "\u05d1\u05e8\u05d0": _verb_entry("\u05d1\u05e8\u05d0", "past"),
            "\u05d0\u05d5\u05e8": {"type": "noun"},
        }

        result = pasuk_flow_generator.validate_question_candidate(
            "shoresh",
            "\u05d5\u05d9\u05d0\u05de\u05e8",
            target_entry,
            correct_answer="\u05d5\u05d9\u05d0\u05de\u05e8",
            choices=list(choice_entries.keys()),
            choice_entries=choice_entries,
        )

        self.assertFalse(result["valid"])
        self.assertIn("shoresh_distractor_leak", result["reason_codes"])

    def test_tense_validator_accepts_clear_case(self):
        result = pasuk_flow_generator.validate_question_candidate(
            "verb_tense",
            "\u05d5\u05d9\u05d0\u05de\u05e8",
            _verb_entry("\u05d0\u05de\u05e8", "past"),
            correct_answer="past",
            choices=["past", "present", "future", "not a verb"],
        )

        self.assertTrue(result["valid"])

    def test_tense_validator_rejects_compound_form(self):
        result = pasuk_flow_generator.validate_question_candidate(
            "verb_tense",
            "\u05d5\u05dc\u05ea\u05d0\u05de\u05e8\u05d9",
            _verb_entry(
                "\u05d0\u05de\u05e8",
                "future",
                prefix="\u05d5",
                prefixes=[
                    {"form": "\u05d5", "translation": "and"},
                    {"form": "\u05dc", "translation": "to / for"},
                ],
            ),
            correct_answer="future",
            choices=["future", "past", "present", "not a verb"],
        )

        self.assertFalse(result["valid"])
        self.assertIn("compound_morphology", result["reason_codes"])

    def test_generate_question_filters_ambiguous_shoresh_selection_targets_early(self):
        analyzed = [
            {"token": "\u05d1\u05e8\u05d0", "entry": _verb_entry("\u05d1\u05e8\u05d0", "past")},
            {
                "token": "\u05d5\u05d9\u05d0\u05de\u05e8",
                "entry": _verb_entry(
                    "\u05d0\u05de\u05e8",
                    "past",
                    prefix="\u05d5",
                    prefixes=[{"form": "\u05d5", "translation": "and"}],
                ),
            },
            {
                "token": "\u05d5\u05d9\u05d0\u05de\u05e8\u05d5",
                "entry": _verb_entry(
                    "\u05d0\u05de\u05e8",
                    "past",
                    prefix="\u05d5",
                    prefixes=[{"form": "\u05d5", "translation": "and"}],
                ),
            },
            {"token": "\u05d0\u05d5\u05e8", "entry": {"type": "noun", "part_of_speech": "noun"}},
        ]

        with patch.object(pasuk_flow_generator, "pick_word_for_skill", return_value="\u05d5\u05d9\u05d0\u05de\u05e8"):
            question = pasuk_flow_generator.generate_question(
                "shoresh",
                "\u05d1\u05e8\u05d0 \u05d5\u05d9\u05d0\u05de\u05e8 \u05d5\u05d9\u05d0\u05de\u05e8\u05d5 \u05d0\u05d5\u05e8",
                mode="selection",
                analyzed_override=analyzed,
            )

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("selected_word"), "\u05d1\u05e8\u05d0")

    def test_generate_question_filters_ambiguous_tense_selection_targets_early(self):
        analyzed = [
            {"token": "\u05ea\u05e6\u05d0", "entry": _verb_entry("\u05d9\u05e6\u05d0", "future")},
            {"token": "\u05d5\u05d9\u05d0\u05de\u05e8", "entry": _verb_entry("\u05d0\u05de\u05e8", "past")},
            {"token": "\u05d5\u05d9\u05e8\u05d0", "entry": _verb_entry("\u05e8\u05d0\u05d4", "past")},
            {"token": "\u05d0\u05d5\u05e8", "entry": {"type": "noun", "part_of_speech": "noun"}},
        ]

        with patch.object(pasuk_flow_generator, "pick_word_for_skill", return_value="\u05d5\u05d9\u05d0\u05de\u05e8"):
            question = pasuk_flow_generator.generate_question(
                "verb_tense",
                "\u05ea\u05e6\u05d0 \u05d5\u05d9\u05d0\u05de\u05e8 \u05d5\u05d9\u05e8\u05d0 \u05d0\u05d5\u05e8",
                mode="selection",
                analyzed_override=analyzed,
            )

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("selected_word"), "\u05ea\u05e6\u05d0")

    def test_runtime_pre_serve_validation_maps_invalid_tense_target_to_explicit_code(self):
        active_record = next(
            record
            for record in active_pesukim_records()
            if record.get("ref", {}).get("perek") == 1
            and record.get("ref", {}).get("pasuk") == 1
        )
        question = {
            "skill": "verb_tense",
            "question_type": "verb_tense",
            "question": "What form is shown?",
            "selected_word": "אֱלֹקִים",
            "word": "אֱלֹקִים",
            "correct_answer": "future",
            "choices": ["future", "past", "present", "to do form"],
            "pasuk": active_record["text"],
        }

        validation = question_flow.validate_question_for_serve(
            question,
            validation_path="framework_test",
            trusted_active_scope=True,
        )

        self.assertFalse(validation["valid"])
        self.assertIn("invalid_tense_target", validation["rejection_codes"])

    def test_runtime_pre_serve_validation_accepts_safe_generated_translation_question(self):
        active_record = next(
            record
            for record in active_pesukim_records()
            if record.get("ref", {}).get("perek") == 1
            and record.get("ref", {}).get("pasuk") == 1
        )

        with patch.object(pasuk_flow_generator, "pick_word_for_skill", return_value="אֱלֹקִים"):
            question = question_flow.generate_skill_question(
                "translation",
                question_flow.candidate_source_for_pasuk(active_record["text"]),
            )

        validation = question_flow.validate_question_for_serve(
            question,
            validation_path="framework_test",
            trusted_active_scope=True,
        )

        self.assertEqual(question.get("selected_word"), "אֱלֹקִים")
        self.assertEqual(question.get("correct_answer"), "God")
        self.assertTrue(validation["valid"])
        self.assertEqual(validation["rejection_codes"], [])

    def test_runtime_pre_serve_validation_rejects_ambiguous_vayehi_translation_target(self):
        active_record = next(
            record
            for record in active_pesukim_records()
            if record.get("ref", {}).get("perek") == 1
            and record.get("ref", {}).get("pasuk") == 3
        )
        question = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does וַיְהִי mean?",
            "selected_word": "וַיְהִי",
            "word": "וַיְהִי",
            "correct_answer": "and it was",
            "word_gloss": "and it was",
            "part_of_speech": "verb",
            "choices": ["and it was", "and there was", "created", "God"],
            "pasuk": active_record["text"],
        }

        validation = question_flow.validate_question_for_serve(
            question,
            validation_path="framework_test",
            trusted_active_scope=True,
        )

        self.assertFalse(validation["valid"])
        self.assertIn("incompatible_skill_target", validation["rejection_codes"])


if __name__ == "__main__":
    unittest.main()
