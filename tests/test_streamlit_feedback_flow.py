import unittest
from contextlib import contextmanager
from unittest.mock import patch

import streamlit as st

import streamlit_app
from question_ui import build_feedback_context, build_learning_context


@contextmanager
def _fake_expander(*args, **kwargs):
    yield


class StreamlitFeedbackFlowTests(unittest.TestCase):
    def setUp(self):
        st.session_state.clear()
        st.session_state.selected_answer = "wrong"
        st.session_state.practice_type = "Learn Mode"
        st.session_state.last_skill_state = {"score": 70, "current_streak": 2, "point_change": "+0"}
        st.session_state.answered = True

    def test_learning_context_for_learn_mode_keeps_focus_tip(self):
        context = build_learning_context(
            practice_type="Learn Mode",
            skill_label="Word Meaning",
            current_skill_label="Word Meaning",
            next_skill_label="Verb Tense",
            source_label="Bereishis 1:3",
            focus_tip="Look at the strongest clue before you guess.",
        )

        self.assertIn("strongest clue", context["what_to_focus_on"].lower())

    def test_feedback_context_for_prefix_question_is_skill_specific(self):
        feedback = build_feedback_context(
            question={
                "question_type": "prefix_level_2_identify_prefix_meaning",
                "skill": "identify_prefix_meaning",
                "prefix": "\u05dc",
                "prefix_meaning": "to / for",
                "correct_answer": "to / for",
                "explanation": "In \u05dc\u05b8\u05d0\u05d5\u05b9\u05e8, \u05dc means 'to / for'.",
            },
            selected_answer="in / with",
            is_correct=False,
            clue_text="",
            practice_type="Learn Mode",
            skill_label="Prefixes",
            next_skill_label="Suffixes",
        )

        self.assertEqual(feedback["grammar_feedback"], "Prefix: \u05dc. Here it means 'to / for'.")
        self.assertNotIn("what_comes_next", feedback)

    def test_feedback_context_for_suffix_question_is_skill_specific(self):
        feedback = build_feedback_context(
            question={
                "question_type": "identify_suffix_meaning",
                "skill": "identify_suffix_meaning",
                "suffix": "\u05d9\u05d5",
                "suffix_meaning": "his / its",
                "correct_answer": "his / its",
                "explanation": "The ending \u05d9\u05d5 marks 'his / its'.",
            },
            selected_answer="plural",
            is_correct=False,
            clue_text="",
            practice_type="Learn Mode",
            skill_label="Suffixes",
            next_skill_label="Shoresh",
        )

        self.assertEqual(feedback["grammar_feedback"], "Ending: \u05d9\u05d5. Here it signals 'his / its'.")

    def test_feedback_context_for_shoresh_question_is_skill_specific(self):
        feedback = build_feedback_context(
            question={
                "question_type": "shoresh",
                "skill": "shoresh",
                "selected_word": "\u05d5\u05d9\u05d0\u05de\u05e8",
                "shoresh": "\u05d0\u05de\u05e8",
                "correct_answer": "\u05d0\u05de\u05e8",
                "explanation": "The shoresh of \u05d5\u05d9\u05d0\u05de\u05e8 is \u05d0\u05de\u05e8.",
            },
            selected_answer="\u05d9\u05d0\u05de\u05e8",
            is_correct=False,
            clue_text="",
            practice_type="Learn Mode",
            skill_label="Shoresh",
            next_skill_label="Verb Tense",
        )

        self.assertEqual(
            feedback["grammar_feedback"],
            "Shoresh: \u05d0\u05de\u05e8. Read past the added letters in \u05d5\u05d9\u05d0\u05de\u05e8.",
        )

    def test_render_feedback_does_not_show_progression_narration_in_main_panel(self):
        question = {
            "question_type": "prefix_level_2_identify_prefix_meaning",
            "skill": "identify_prefix_meaning",
            "prefix": "\u05dc",
            "prefix_meaning": "to / for",
            "selected_word": "\u05dc\u05b8\u05d0\u05d5\u05b9\u05e8",
            "correct_answer": "to / for",
            "explanation": "In \u05dc\u05b8\u05d0\u05d5\u05b9\u05e8, \u05dc means 'to / for'.",
            "choices": ["to / for", "in / with", "and", "the"],
        }
        rendered = []

        def capture_markdown(text, **kwargs):
            rendered.append(text)

        with patch.object(streamlit_app, "last_answer_was_correct", return_value=False), \
             patch.object(streamlit_app.st, "markdown", side_effect=capture_markdown), \
             patch.object(streamlit_app.st, "caption"), \
             patch.object(streamlit_app.st, "expander", _fake_expander):
            streamlit_app.render_feedback(question, {"current_skill": "identify_prefix_meaning"})

        main_panel = next(text for text in rendered if "feedback-panel" in text)
        self.assertIn("Grammar", main_panel)
        self.assertIn("Prefix:", main_panel)
        self.assertIn("to / for", main_panel)
        self.assertNotIn("What Comes Next", main_panel)
        self.assertNotIn("stretch you a bit", main_panel)

    def test_transition_to_question_clears_transient_messages(self):
        st.session_state.unlocked_skill_message = "Unlocked"
        st.session_state.feature_fallback_message = "Fallback"
        st.session_state.adaptive_status_message = "Status"
        st.session_state.adaptive_status_reason = "Reason"
        st.session_state.adaptive_status_level = "warning"
        st.session_state.answered = True
        st.session_state.selected_answer = "wrong"
        st.session_state.last_skill_state = {"score": 70}

        with patch.object(streamlit_app.st, "rerun"):
            streamlit_app.transition_to_question({"question": "Next", "correct_answer": "A"})

        self.assertEqual(st.session_state.unlocked_skill_message, "")
        self.assertEqual(st.session_state.feature_fallback_message, "")
        self.assertEqual(st.session_state.adaptive_status_message, "")
        self.assertEqual(st.session_state.adaptive_status_reason, "")
        self.assertEqual(st.session_state.adaptive_status_level, "info")
        self.assertFalse(st.session_state.answered)
        self.assertIsNone(st.session_state.selected_answer)


if __name__ == "__main__":
    unittest.main()
