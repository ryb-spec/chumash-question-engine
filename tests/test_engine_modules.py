import unittest
from unittest.mock import patch

from engine import flow_builder, question_builders, skill_logic, token_analysis
from runtime.question_flow import build_followup_question


class EngineModuleTests(unittest.TestCase):
    def test_token_analysis_uses_parser_tokenizer(self):
        with patch.object(
            token_analysis,
            "parser_tokenize_pasuk",
            return_value=["וַיֹּאמֶר", "אֱלֹקִים"],
        ) as mocked:
            tokens = token_analysis.tokenize_pasuk("ignored")

        mocked.assert_called_once_with("ignored")
        self.assertEqual(tokens, ["וַיֹּאמֶר", "אֱלֹקִים"])

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
            analysis = token_analysis.analyze_word("בָּרָא")

        mocked.assert_called_once_with("בָּרָא")
        self.assertTrue(analysis["is_verb"])
        self.assertEqual(analysis["tense"], "past")

    def test_question_builder_stays_on_requested_pasuk(self):
        pasuk = "וַיֹּאמֶר אֱלֹקִים יְהִי אוֹר וַיְהִי אוֹר"
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
        flow = flow_builder.generate_pasuk_flow("וַיְהִי עֶרֶב וַיְהִי בֹקֶר יוֹם שְׁלִישִׁי")
        prompts = [item["question"] for item in flow["questions"]]

        self.assertEqual(len(prompts), len(set(prompts)))


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

        question = {
            "skill": "translation",
            "question": "What does בָּרָא mean?",
            "selected_word": "בָּרָא",
            "word": "בָּרָא",
            "correct_answer": "created",
            "choices": ["created", "light", "earth", "water"],
            "pasuk": "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
        }
        repeated = dict(question)
        repeated["_assessment_source"] = "targeted"
        fallback = {
            "skill": "translation",
            "question": "What does אֱלֹקִים mean?",
            "selected_word": "אֱלֹקִים",
            "word": "אֱלֹקִים",
            "correct_answer": "God",
            "choices": ["God", "created", "light", "water"],
            "pasuk": "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
        }

        st.session_state.recent_questions = [streamlit_app.question_signature(question)]

        with patch.object(streamlit_app, "analyze_generator_pasuk", return_value="בְּרֵאשִׁית בָּרָא אֱלֹקִים"), \
             patch.object(streamlit_app, "generate_skill_question", return_value=dict(repeated)), \
             patch.object(streamlit_app, "generate_practice_question", return_value=dict(fallback)):
            result = build_followup_question({"current_skill": "translation"}, question)

        self.assertEqual(result["_assessment_source"], "fallback follow-up from active parsed dataset")
        self.assertEqual(result["_debug_trace"]["transition_path"], "practice_fallback")


if __name__ == "__main__":
    unittest.main()
