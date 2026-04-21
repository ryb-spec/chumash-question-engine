import unittest
from unittest.mock import patch

from engine import flow_builder, question_builders, skill_logic, token_analysis
import runtime.question_flow as question_flow
from assessment_scope import active_pesukim_records
from runtime.question_flow import build_followup_question


class EngineModuleTests(unittest.TestCase):
    def test_token_analysis_uses_parser_tokenizer(self):
        with patch.object(
            token_analysis,
            "parser_tokenize_pasuk",
            return_value=["וַיֹּאמֶר", "אֱלֹקִים"],
        ) as mocked:
            tokens = token_analysis.tokenize_pasuk("ignored")

        mocked.assert_called_once_with("ignored")
        self.assertEqual(tokens, ["וַיֹּאמֶר", "אֱלֹקִים"])

    def test_token_analysis_uses_parser_candidate_generation(self):
        with patch.object(
            token_analysis,
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
            analysis = token_analysis.analyze_word("בָּרָא")

        mocked.assert_called_once_with("בָּרָא")
        self.assertTrue(analysis["is_verb"])
        self.assertEqual(analysis["tense"], "past")

    def test_question_builder_stays_on_requested_pasuk(self):
        pasuk = "וַיֹּאמֶר אֱלֹקִים יְהִי אוֹר וַיְהִי אוֹר"
        question = question_builders.generate_question("translation", pasuk)

        self.assertEqual(question.get("pasuk"), pasuk)
        self.assertEqual(question.get("skill"), "translation")

    def test_prefix_and_suffix_validation_available_from_skill_logic_module(self):
        prefix_valid, prefix_reason = skill_logic.prefix_question_validation(
            "בצלמנו",
            {
                "prefix": "ב",
                "prefixes": [{"form": "ב", "translation": "in / with"}],
                "suffix": "נו",
            },
            correct_answer="ב",
            choices=["ב", "ל", "מ", "כ"],
        )
        suffix_valid, suffix_reason = skill_logic.suffix_question_validation(
            "זרעוֹ",
            {
                "suffix": "ו",
                "suffixes": [{"form": "ו", "translation": "his"}],
            },
            correct_answer="his",
            choices=["his", "their", "our", "my"],
        )

        self.assertTrue(prefix_valid)
        self.assertEqual(prefix_reason, "")
        self.assertTrue(suffix_valid)
        self.assertEqual(suffix_reason, "")

    def test_flow_builder_suppresses_duplicate_prompts(self):
        record = next(
            item
            for item in active_pesukim_records()
            if item.get("ref", {}).get("perek") == 1
            and item.get("ref", {}).get("pasuk") == 24
        )
        flow = flow_builder.generate_pasuk_flow(record["text"])
        prompts = [item["question"] for item in flow["questions"]]

        self.assertEqual(len(prompts), len(set(prompts)))

    def test_translation_question_skips_thin_definite_article_standalone_form(self):
        analyzed_override = [
            {
                "token": "הָאָרֶץ",
                "entry": {
                    "word": "הָאָרֶץ",
                    "type": "noun",
                    "part_of_speech": "noun",
                    "semantic_group": "place",
                    "group": "common_noun",
                    "entity_type": "common_noun",
                    "translation": "the earth",
                    "translation_literal": "the earth",
                    "translation_context": "the earth",
                    "prefixes": [{"form": "ה", "translation": "the"}],
                    "suffixes": [],
                    "confidence": "reviewed",
                },
            }
        ]

        question = flow_builder.generate_question(
            "translation",
            "הָאָרֶץ",
            analyzed_override=analyzed_override,
        )

        self.assertEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("reason"), "No usable translation target found in this pasuk.")

    def test_translation_question_skips_prefixed_nonverb_standalone_form(self):
        analyzed_override = [
            {
                "token": "לָאוֹר",
                "entry": {
                    "word": "לָאוֹר",
                    "type": "noun",
                    "part_of_speech": "noun",
                    "semantic_group": "natural_object",
                    "group": "common_noun",
                    "entity_type": "common_noun",
                    "translation": "to the light",
                    "translation_literal": "to the light",
                    "translation_context": "to the light",
                    "prefixes": [{"form": "ל", "translation": "to / for"}],
                    "suffixes": [],
                    "confidence": "reviewed",
                },
            }
        ]

        question = flow_builder.generate_question(
            "translation",
            "לָאוֹר",
            analyzed_override=analyzed_override,
        )

        self.assertEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("reason"), "No usable translation target found in this pasuk.")

    def test_runtime_shoresh_question_uses_hebrew_root_distractors_not_generic_fillers(self):
        record = next(
            item
            for item in active_pesukim_records()
            if item.get("ref", {}).get("perek") == 1
            and item.get("ref", {}).get("pasuk") == 10
        )

        question = flow_builder.generate_question("shoresh", record["text"])

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertEqual(len(question.get("choices", [])), 4)
        self.assertNotIn("not a verb", question.get("choices", []))
        self.assertTrue(all(flow_builder.contains_hebrew(choice) for choice in question.get("choices", [])))

    def test_runtime_shoresh_question_avoids_known_false_surface_targets(self):
        blocked_targets = {
            (1, 1): {"בְּרֵאשִׁית", "ראשית"},
            (1, 2): {"תְהוֹם", "תהום", "מְרַחֶפֶת", "רחפת"},
            (1, 11): {"לְמִינוֹ", "מין"},
            (1, 15): {"לִמְאוֹרֹת", "מאורת"},
        }

        for ref, blocked_values in blocked_targets.items():
            record = next(
                item
                for item in active_pesukim_records()
                if item.get("ref", {}).get("perek") == ref[0]
                and item.get("ref", {}).get("pasuk") == ref[1]
            )

            question = flow_builder.generate_question("shoresh", record["text"])

            self.assertNotIn(question.get("selected_word"), blocked_values)
            self.assertNotIn(question.get("correct_answer"), blocked_values)


class FollowupFallbackModuleTests(unittest.TestCase):
    def setUp(self):
        import streamlit as st
        from runtime.session_state import init_session_state

        st.session_state.clear()
        init_session_state()
        st.session_state.recent_questions = []
        st.session_state.pending_adaptive_context = {}

    def test_build_followup_question_uses_fallback_when_repeat_is_rejected(self):
        import streamlit as st
        import streamlit_app

        active_record = active_pesukim_records()[0]
        question = {
            "skill": "subject_identification",
            "question_type": "subject_identification",
            "question": "Who is doing the action here?",
            "selected_word": "אֱלֹקִים",
            "word": "אֱלֹקִים",
            "correct_answer": "God",
            "choices": ["God", "the heavens", "the earth", "light"],
            "pasuk": active_record["text"],
            "pasuk_ref": active_record["ref"],
        }
        repeated = dict(question)
        repeated["_assessment_source"] = "targeted"
        fallback = {
            "skill": "subject_identification",
            "question_type": "subject_identification",
            "question": "Who is doing the action here?",
            "selected_word": "הַשָּׁמַיִם",
            "word": "הַשָּׁמַיִם",
            "correct_answer": "the heavens",
            "choices": ["the heavens", "God", "the earth", "light"],
            "pasuk": active_record["text"],
            "pasuk_ref": active_record["ref"],
        }

        st.session_state.recent_questions = [streamlit_app.question_signature(question)]

        with patch.object(question_flow, "analyze_generator_pasuk", return_value=active_record["text"]), \
             patch.object(question_flow, "generate_skill_question", return_value=dict(repeated)), \
             patch.object(question_flow, "generate_practice_question", return_value=dict(fallback)):
            result = build_followup_question({"current_skill": "subject_identification"}, question)

        self.assertEqual(result["_assessment_source"], "fallback follow-up from active parsed dataset")
        self.assertEqual(result["_debug_trace"]["transition_path"], "practice_fallback")


if __name__ == "__main__":
    unittest.main()
