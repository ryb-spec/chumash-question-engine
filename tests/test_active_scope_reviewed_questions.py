import unittest

from assessment_scope import (
    active_pasuk_id_set,
    active_pesukim_records,
    active_scope_reviewed_question_records,
    load_active_scope_reviewed_questions_data,
)
from engine.flow_builder import generate_question
from scripts.build_reviewed_question_bank import validate_reviewed_bank
from torah_parser.word_bank_adapter import normalize_hebrew_key


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
        self.assertEqual(summary["baseline_lane_counts"].get("translation"), 25)
        self.assertEqual(summary["baseline_lane_counts"].get("shoresh"), 17)
        self.assertEqual(summary["baseline_lane_counts"].get("tense"), 18)
        self.assertEqual(summary["baseline_lane_counts"].get("affix"), 25)
        self.assertGreaterEqual(summary["lane_count_delta"].get("translation", 0), 20)
        self.assertGreaterEqual(summary["lane_count_delta"].get("shoresh", 0), 8)
        self.assertGreaterEqual(summary["lane_count_delta"].get("tense", 0), 7)
        self.assertGreaterEqual(summary["lane_count_delta"].get("affix", 0), 7)
        self.assertGreaterEqual(summary["lane_counts"].get("role", 0), 11)
        self.assertGreaterEqual(summary["lane_counts"].get("translation", 0), 52)
        self.assertGreaterEqual(summary["lane_counts"].get("part_of_speech", 0), 9)
        self.assertGreaterEqual(summary["skill_counts"].get("translation", 0), 31)
        self.assertGreaterEqual(summary["skill_counts"].get("part_of_speech", 0), 9)
        self.assertGreaterEqual(summary["skill_counts"].get("subject_identification", 0), 7)
        self.assertGreaterEqual(summary["skill_counts"].get("object_identification", 0), 4)
        self.assertGreaterEqual(summary["skill_counts"].get("phrase_translation", 0), 21)
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

    def test_reviewed_bank_omits_low_value_standalone_translation_targets(self):
        weak_targets = {"הוּא", "אֱלֹהִים", "אֱלֹקִים", "יְהוָה"}

        for question in active_scope_reviewed_question_records():
            if question.get("skill") != "translation":
                continue
            self.assertNotIn(question.get("selected_word"), weak_targets)

    def test_reviewed_bank_keeps_analysis_slippery_standalone_translation_targets_blocked(self):
        blocked_targets = {
            normalize_hebrew_key("\u05d5\u05b7\u05ea\u05b9\u05bc\u05d0\u05de\u05b6\u05e8"),
            normalize_hebrew_key("\u05d5\u05b7\u05d9\u05b5\u05bc\u05d3\u05b0\u05e2\u05d5\u05bc"),
        }

        for question in active_scope_reviewed_question_records():
            if question.get("skill") != "translation" or question.get("question_type") != "translation":
                continue
            self.assertNotIn(normalize_hebrew_key(question.get("selected_word") or ""), blocked_targets)

    def test_reviewed_bank_keeps_hotspot_adjacent_weak_standalone_targets_blocked(self):
        blocked_targets = {
            ("bereishis_2_25", normalize_hebrew_key("\u05e2\u05b2\u05e8\u05d5\u05bc\u05de\u05b4\u05bc\u05d9\u05dd")),
            ("bereishis_2_25", normalize_hebrew_key("\u05d9\u05b4\u05ea\u05b0\u05d1\u05b9\u05bc\u05e9\u05b8\u05c1\u05e9\u05c1\u05d5\u05bc")),
            ("bereishis_3_8", normalize_hebrew_key("\u05d5\u05b7\u05d9\u05b4\u05bc\u05e9\u05c1\u05b0\u05de\u05e2\u05d5\u05bc")),
        }

        for question in active_scope_reviewed_question_records():
            if question.get("skill") != "translation" or question.get("question_type") != "translation":
                continue
            key = (question.get("pasuk_id"), normalize_hebrew_key(question.get("selected_word") or ""))
            self.assertNotIn(key, blocked_targets)

    def test_reviewed_bank_omits_low_value_part_of_speech_targets(self):
        weak_targets = {
            normalize_hebrew_key("בַּיּוֹם"),
            normalize_hebrew_key("בְּצַלְמֵנוּ"),
            normalize_hebrew_key("הַיּוֹם"),
        }

        for question in active_scope_reviewed_question_records():
            if question.get("skill") != "part_of_speech":
                continue
            self.assertNotIn(normalize_hebrew_key(question.get("selected_word")), weak_targets)

    def test_reviewed_bank_omits_low_value_bare_form_shoresh_targets(self):
        weak_targets = {"אָמַר", "עָשָׂה"}

        for question in active_scope_reviewed_question_records():
            if question.get("skill") != "shoresh":
                continue
            self.assertNotIn(question.get("selected_word"), weak_targets)

    def test_runtime_prefers_reviewed_translation_when_available(self):
        question = generate_question("translation", pasuk_by_id("bereishis_2_7"))

        self.assertEqual(question.get("analysis_source"), "active_scope_reviewed_bank")
        self.assertEqual(question.get("skill"), "translation")
        self.assertEqual(question.get("question_type"), "phrase_translation")
        self.assertEqual(
            question.get("selected_word"),
            "וַיִּיצֶר יְהוָה אֱלֹהִים אֶת הָאָדָם",
        )
        self.assertEqual(
            question.get("correct_answer"),
            "and the LORD God formed the man",
        )

    def test_runtime_prefers_reviewed_translation_for_audited_standalone_target(self):
        question = generate_question("translation", pasuk_by_id("bereishis_1_5"))

        self.assertEqual(question.get("analysis_source"), "active_scope_reviewed_bank")
        self.assertEqual(question.get("skill"), "translation")
        self.assertEqual(question.get("question_type"), "translation")
        self.assertEqual(normalize_hebrew_key(question.get("selected_word")), normalize_hebrew_key("וַיִּקְרָא"))
        self.assertEqual(question.get("correct_answer"), "and he called")

    def test_runtime_prefers_reviewed_translation_for_new_foundation_targets(self):
        expected = {
            "bereishis_2_4": ("עֲשׂוֹת", "to make"),
            "bereishis_2_15": ("\u05d5\u05b7\u05d9\u05bc\u05b4\u05e7\u05bc\u05b7\u05d7", "and he took"),
            "bereishis_2_23": ("וַיֹּאמֶר", "and he said"),
            "bereishis_3_3": ("\u05ea\u05b0\u05bc\u05de\u05bb\u05ea\u05d5\u05bc\u05df", "you will die"),
        }

        for pasuk_id, (token, answer) in expected.items():
            question = generate_question("translation", pasuk_by_id(pasuk_id))
            self.assertEqual(question.get("analysis_source"), "active_scope_reviewed_bank")
            self.assertEqual(question.get("skill"), "translation")
            self.assertEqual(question.get("question_type"), "translation")
            self.assertEqual(normalize_hebrew_key(question.get("selected_word")), normalize_hebrew_key(token))
            self.assertEqual(question.get("correct_answer"), answer)

    def test_reviewed_bank_contains_new_standalone_translation_foundation_targets(self):
        expected = {
            ("bereishis_1_4", normalize_hebrew_key("\u05d5\u05b7\u05d9\u05bc\u05b7\u05e8\u05b0\u05d0")): "and he saw",
            ("bereishis_1_4", normalize_hebrew_key("\u05d5\u05b7\u05d9\u05bc\u05b7\u05d1\u05b0\u05d3\u05bc\u05b5\u05dc")): "and he separated",
            ("bereishis_2_15", normalize_hebrew_key("\u05d5\u05b7\u05d9\u05bc\u05b4\u05e7\u05bc\u05b7\u05d7")): "and he took",
            ("bereishis_3_1", normalize_hebrew_key("\u05d4\u05b8\u05d9\u05b8\u05d4")): "was",
            ("bereishis_3_1", normalize_hebrew_key("\u05ea\u05b9\u05d0\u05db\u05b0\u05dc\u05d5\u05bc")): "you will eat",
            ("bereishis_3_1", normalize_hebrew_key("\u05e2\u05b8\u05e9\u05b8\u05c2\u05d4")): "made",
            ("bereishis_3_3", normalize_hebrew_key("\u05ea\u05b0\u05bc\u05de\u05bb\u05ea\u05d5\u05bc\u05df")): "you will die",
            ("bereishis_3_3", normalize_hebrew_key("\u05ea\u05b4\u05d2\u05b0\u05bc\u05e2\u05d5\u05bc")): "you will touch",
            ("bereishis_3_5", normalize_hebrew_key("\u05d9\u05b9\u05d3\u05b5\u05e2\u05b7")): "knows",
            ("bereishis_3_6", normalize_hebrew_key("\u05dc\u05b0\u05d4\u05b7\u05e9\u05b0\u05c2\u05db\u05b4\u05bc\u05d9\u05dc")): "to make wise",
            ("bereishis_3_7", normalize_hebrew_key("\u05ea\u05b0\u05d0\u05b5\u05e0\u05b8\u05d4")): "fig",
            ("bereishis_3_7", normalize_hebrew_key("\u05d7\u05b2\u05d2\u05b9\u05e8\u05b9\u05ea")): "belts",
            ("bereishis_3_7", normalize_hebrew_key("\u05d5\u05b7\u05d9\u05b4\u05bc\u05ea\u05b0\u05e4\u05b0\u05bc\u05e8\u05d5\u05bc")): "and he sewed",
            ("bereishis_3_8", normalize_hebrew_key("\u05de\u05b4\u05ea\u05b0\u05d4\u05b7\u05dc\u05b5\u05bc\u05da\u05b0")): "walking",
            ("bereishis_3_8", normalize_hebrew_key("\u05d5\u05b7\u05d9\u05bc\u05b4\u05ea\u05b0\u05d7\u05b7\u05d1\u05b5\u05bc\u05d0")): "and he hid himself",
            ("bereishis_3_8", normalize_hebrew_key("\u05e2\u05b5\u05e5")): "a tree",
        }

        found = {}
        for question in active_scope_reviewed_question_records():
            if question.get("skill") != "translation" or question.get("question_type") != "translation":
                continue
            key = (question.get("pasuk_id"), normalize_hebrew_key(question.get("selected_word") or ""))
            if key in expected:
                found[key] = question.get("correct_answer")

        self.assertEqual(found, expected)

    def test_generate_question_can_rotate_away_from_tov_hotspot_when_recent(self):
        recent_questions = [
            {
                "skill": "translation",
                "question_type": "translation",
                "selected_word": "\u05d8\u05d5\u05b9\u05d1",
                "correct_answer": "good",
            }
        ]

        question = generate_question(
            "translation",
            pasuk_by_id("bereishis_1_4"),
            recent_questions=recent_questions,
        )

        self.assertEqual(question.get("analysis_source"), "active_scope_reviewed_bank")
        self.assertEqual(question.get("question_type"), "translation")
        self.assertIn(
            normalize_hebrew_key(question.get("selected_word")),
            {
                normalize_hebrew_key("\u05d5\u05b7\u05d9\u05bc\u05b7\u05e8\u05b0\u05d0"),
                normalize_hebrew_key("\u05d5\u05b7\u05d9\u05bc\u05b7\u05d1\u05b0\u05d3\u05bc\u05b5\u05dc"),
            },
        )

    def test_generate_question_can_rotate_to_new_crafty_hotspot_escape_target(self):
        recent_questions = [
            {
                "skill": "translation",
                "question_type": "translation",
                "selected_word": "\u05e2\u05b8\u05e8\u05d5\u05bc\u05dd",
                "correct_answer": "crafty",
            },
            {
                "skill": "translation",
                "question_type": "translation",
                "selected_word": "\u05d4\u05b8\u05d9\u05b8\u05d4",
                "correct_answer": "was",
            },
            {
                "skill": "translation",
                "question_type": "translation",
                "selected_word": "\u05ea\u05b9\u05d0\u05db\u05b0\u05dc\u05d5\u05bc",
                "correct_answer": "you will eat",
            },
        ]

        question = generate_question(
            "translation",
            pasuk_by_id("bereishis_3_1"),
            recent_questions=recent_questions,
        )

        self.assertEqual(question.get("analysis_source"), "active_scope_reviewed_bank")
        self.assertEqual(question.get("question_type"), "translation")
        self.assertEqual(normalize_hebrew_key(question.get("selected_word")), normalize_hebrew_key("\u05e2\u05b8\u05e9\u05b8\u05c2\u05d4"))
        self.assertEqual(question.get("correct_answer"), "made")

    def test_generate_question_can_rotate_to_new_naked_hotspot_escape_target(self):
        recent_questions = [
            {
                "skill": "translation",
                "question_type": "translation",
                "selected_word": "\u05e2\u05b5\u05d9\u05e8\u05bb\u05de\u05b4\u05bc\u05dd",
                "correct_answer": "naked",
            },
            {
                "skill": "translation",
                "question_type": "translation",
                "selected_word": "\u05ea\u05b0\u05d0\u05b5\u05e0\u05b8\u05d4",
                "correct_answer": "fig",
            },
            {
                "skill": "translation",
                "question_type": "translation",
                "selected_word": "\u05d7\u05b2\u05d2\u05b9\u05e8\u05b9\u05ea",
                "correct_answer": "belts",
            },
        ]

        question = generate_question(
            "translation",
            pasuk_by_id("bereishis_3_7"),
            recent_questions=recent_questions,
        )

        self.assertEqual(question.get("analysis_source"), "active_scope_reviewed_bank")
        self.assertEqual(question.get("question_type"), "translation")
        self.assertEqual(normalize_hebrew_key(question.get("selected_word")), normalize_hebrew_key("\u05d5\u05b7\u05d9\u05b4\u05bc\u05ea\u05b0\u05e4\u05b0\u05bc\u05e8\u05d5\u05bc"))
        self.assertEqual(question.get("correct_answer"), "and he sewed")

    def test_generate_question_can_rotate_to_new_voice_hotspot_escape_target(self):
        recent_questions = [
            {
                "skill": "translation",
                "question_type": "translation",
                "selected_word": "\u05e7\u05d5\u05b9\u05dc",
                "correct_answer": "voice",
            },
            {
                "skill": "translation",
                "question_type": "translation",
                "selected_word": "\u05de\u05b4\u05ea\u05b0\u05d4\u05b7\u05dc\u05b5\u05bc\u05da\u05b0",
                "correct_answer": "walking",
            },
            {
                "skill": "translation",
                "question_type": "translation",
                "selected_word": "\u05d5\u05b7\u05d9\u05bc\u05b4\u05ea\u05b0\u05d7\u05b7\u05d1\u05b5\u05bc\u05d0",
                "correct_answer": "and he hid himself",
            },
        ]

        question = generate_question(
            "translation",
            pasuk_by_id("bereishis_3_8"),
            recent_questions=recent_questions,
        )

        self.assertEqual(question.get("analysis_source"), "active_scope_reviewed_bank")
        self.assertEqual(question.get("question_type"), "translation")
        self.assertEqual(normalize_hebrew_key(question.get("selected_word")), normalize_hebrew_key("\u05e2\u05b5\u05e5"))
        self.assertEqual(question.get("correct_answer"), "a tree")

    def test_generate_question_uses_longer_reviewed_translation_history_for_hotspot_rotation(self):
        recent_questions = [
            {
                "skill": "translation",
                "question_type": "translation",
                "selected_word": "\u05e7\u05d5\u05b9\u05dc",
                "correct_answer": "voice",
            }
        ]
        for index in range(14):
            recent_questions.append(
                {
                    "skill": "translation",
                    "question_type": "translation",
                    "selected_word": f"filler-{index}",
                    "correct_answer": f"filler-answer-{index}",
                }
            )

        question = generate_question(
            "translation",
            pasuk_by_id("bereishis_3_8"),
            recent_questions=recent_questions,
        )

        self.assertEqual(question.get("analysis_source"), "active_scope_reviewed_bank")
        self.assertEqual(question.get("question_type"), "translation")
        self.assertEqual(
            normalize_hebrew_key(question.get("selected_word")),
            normalize_hebrew_key("\u05de\u05b4\u05ea\u05b0\u05d4\u05b7\u05dc\u05b5\u05bc\u05da\u05b0"),
        )
        self.assertEqual(question.get("correct_answer"), "walking")

    def test_generate_question_prefers_less_recent_reviewed_translation_in_multi_reviewed_pasuk(self):
        recent_questions = [
            {
                "skill": "translation",
                "question_type": "translation",
                "selected_word": "\u05e2\u05b5\u05d9\u05e8\u05bb\u05de\u05b4\u05bc\u05dd",
                "correct_answer": "naked",
            }
        ]

        question = generate_question(
            "translation",
            pasuk_by_id("bereishis_3_7"),
            recent_questions=recent_questions,
        )

        self.assertEqual(question.get("analysis_source"), "active_scope_reviewed_bank")
        self.assertEqual(question.get("question_type"), "translation")
        self.assertEqual(normalize_hebrew_key(question.get("selected_word")), normalize_hebrew_key("\u05ea\u05b0\u05d0\u05b5\u05e0\u05b8\u05d4"))
        self.assertEqual(question.get("correct_answer"), "fig")

    def test_runtime_prefers_reviewed_part_of_speech_for_audited_target(self):
        question = generate_question("part_of_speech", pasuk_by_id("bereishis_1_3"))

        self.assertEqual(question.get("analysis_source"), "active_scope_reviewed_bank")
        self.assertEqual(question.get("skill"), "part_of_speech")
        self.assertEqual(question.get("question_type"), "part_of_speech")
        self.assertEqual(normalize_hebrew_key(question.get("selected_word")), normalize_hebrew_key("וַיְהִי"))
        self.assertEqual(question.get("correct_answer"), "action word")

    def test_runtime_prefers_reviewed_part_of_speech_for_new_foundation_targets(self):
        expected = {
            "bereishis_1_11": ("עֵץ", "naming word"),
            "bereishis_2_8": ("וַיִּטַּע", "action word"),
            "bereishis_2_23": ("וַיֹּאמֶר", "action word"),
            "bereishis_3_8": ("קוֹל", "naming word"),
        }

        for pasuk_id, (token, answer) in expected.items():
            question = generate_question("part_of_speech", pasuk_by_id(pasuk_id))
            self.assertEqual(question.get("analysis_source"), "active_scope_reviewed_bank")
            self.assertEqual(question.get("skill"), "part_of_speech")
            self.assertEqual(question.get("question_type"), "part_of_speech")
            self.assertEqual(normalize_hebrew_key(question.get("selected_word")), normalize_hebrew_key(token))
            self.assertEqual(question.get("correct_answer"), answer)

    def test_runtime_prefers_reviewed_subject_identification_when_available(self):
        question = generate_question("subject_identification", pasuk_by_id("bereishis_1_21"))

        self.assertEqual(question.get("analysis_source"), "active_scope_reviewed_bank")
        self.assertEqual(normalize_hebrew_key(question.get("selected_word")), normalize_hebrew_key("אֱלֹקִים"))
        self.assertEqual(question.get("correct_answer"), "God")
        self.assertEqual(normalize_hebrew_key(question.get("action_token")), normalize_hebrew_key("וַיִּבְרָא"))
        self.assertEqual(question.get("role_focus"), "subject")

    def test_runtime_prefers_reviewed_object_identification_when_available(self):
        question = generate_question("object_identification", pasuk_by_id("bereishis_1_21"))

        self.assertEqual(question.get("analysis_source"), "active_scope_reviewed_bank")
        self.assertEqual(
            normalize_hebrew_key(question.get("selected_word")),
            normalize_hebrew_key("הַתַּנִּינִם הַגְּדֹלִים"),
        )
        self.assertEqual(question.get("correct_answer"), "the great sea creatures")
        self.assertEqual(normalize_hebrew_key(question.get("action_token")), normalize_hebrew_key("וַיִּבְרָא"))
        self.assertEqual(question.get("role_focus"), "direct_object")

    def test_runtime_prefers_reviewed_phrase_translation_when_available_for_new_richer_clause(self):
        question = generate_question("phrase_translation", pasuk_by_id("bereishis_1_21"))

        self.assertEqual(question.get("analysis_source"), "active_scope_reviewed_bank")
        self.assertEqual(
            normalize_hebrew_key(question.get("selected_word")),
            normalize_hebrew_key("וַיִּבְרָא אֱלֹקִים אֶת הַתַּנִּינִם הַגְּדֹלִים"),
        )
        self.assertEqual(
            question.get("correct_answer"),
            "and God created the great sea creatures",
        )

    def test_phrase_translation_still_skips_non_contiguous_gold_target(self):
        question = generate_question("phrase_translation", pasuk_by_id("bereishis_2_9"))

        self.assertEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("reason"), "No quiz-ready phrase target found in this pasuk.")

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
