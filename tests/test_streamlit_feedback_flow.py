import unittest
from contextlib import contextmanager
from unittest.mock import patch

import streamlit as st

import streamlit_app
from question_ui import build_feedback_context, build_learning_context
from ui import question_support
from ui import render_feedback as render_feedback_module


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

    def test_feedback_context_for_subject_question_uses_role_specific_explanation(self):
        feedback = build_feedback_context(
            question={
                "question_type": "subject_identification",
                "skill": "subject_identification",
                "selected_word": "אֱלֹקִים",
                "action_token": "בָּרָא",
                "correct_answer": "God",
                "explanation": "In בָּרָא, אֱלֹקִים is doing the action.",
            },
            selected_answer="the man",
            is_correct=False,
            clue_text="",
            practice_type="Learn Mode",
            skill_label="Subject Identification",
            next_skill_label="Object Identification",
        )

        self.assertEqual(
            feedback["grammar_feedback"],
            "In בָּרָא, אֱלֹקִים is doing the action.",
        )

    def test_feedback_context_for_object_question_uses_role_specific_explanation(self):
        feedback = build_feedback_context(
            question={
                "question_type": "object_identification",
                "skill": "object_identification",
                "selected_word": "אֹתָם",
                "action_token": "וַיִּתֵּן",
                "correct_answer": "them",
                "explanation": "In וַיִּתֵּן, אֹתָם is what receives the action.",
            },
            selected_answer="the earth",
            is_correct=False,
            clue_text="",
            practice_type="Learn Mode",
            skill_label="Object Identification",
            next_skill_label="Phrase Meaning",
        )

        self.assertEqual(
            feedback["grammar_feedback"],
            "In וַיִּתֵּן, אֹתָם is what receives the action.",
        )

    def test_feedback_context_for_tense_question_uses_explicit_present_to_do_form_contrast(self):
        feedback = build_feedback_context(
            question={
                "question_type": "verb_tense",
                "skill": "verb_tense",
                "selected_word": "לְהַבְדִּיל",
                "correct_answer": "to do form",
                "word_gloss": "to separate",
                "explanation": "לְהַבְדִּיל is read as the 'to do' form.",
            },
            selected_answer="present",
            is_correct=False,
            clue_text="",
            practice_type="Learn Mode",
            skill_label="Verb Tense",
            next_skill_label="Translation",
        )

        self.assertEqual(
            feedback["grammar_feedback"],
            "לְהַבְדִּיל means 'to separate', so here it is the to do form. Present would mean doing / is doing.",
        )
        self.assertEqual(
            feedback["likely_confusion"],
            "Present = doing / is doing. 'To do' form = to do.",
        )

    def test_feedback_context_for_part_of_speech_uses_plain_word_kind_contrast(self):
        feedback = build_feedback_context(
            question={
                "question_type": "part_of_speech",
                "skill": "part_of_speech",
                "selected_word": "אוֹר",
                "correct_answer": "naming word",
                "word_gloss": "light",
                "explanation": "אוֹר means 'light', so here it is a naming word.",
            },
            selected_answer="action word",
            is_correct=False,
            clue_text="",
            practice_type="Learn Mode",
            skill_label="Kinds of words",
            next_skill_label="Word meaning",
        )

        self.assertEqual(
            feedback["grammar_feedback"],
            "אוֹר means 'light', so here it is a naming word. Action word would mean something happening or being done.",
        )
        self.assertEqual(
            feedback["likely_confusion"],
            "אוֹר means 'light', so here it is a naming word. Action word would mean something happening or being done.",
        )

    def test_clue_helpers_hide_placeholder_markers_and_studentize_tense(self):
        rendered = []

        with patch.object(
            question_support,
            "get_word_entry",
            return_value={
                "prefix": "ו",
                "prefix_meaning": "and",
                "shoresh": "???",
                "suffix": "",
                "suffix_meaning": "",
                "tense": "vav_consecutive_past",
            },
        ), patch.object(question_support.st, "markdown", side_effect=lambda text, **kwargs: rendered.append(text)):
            clue = question_support.clue_sentence({"selected_word": "וַיְהִי"})
            question_support.render_grammar_clues({"selected_word": "וַיְהִי"})

        self.assertNotIn("???", clue)
        self.assertIn("past", clue)
        self.assertNotIn("past narrative", clue)
        combined = " ".join(rendered)
        self.assertNotIn("???", combined)
        self.assertNotIn("vav_consecutive_past", combined)
        self.assertNotIn("past narrative", combined)
        self.assertIn("past", combined)

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
             patch.object(streamlit_app.st, "expander", _fake_expander), \
             patch.object(streamlit_app.st, "button", return_value=False):
            streamlit_app.render_feedback(question, {"current_skill": "identify_prefix_meaning"})

        main_panel = next(text for text in rendered if "feedback-panel" in text)
        self.assertIn("Grammar", main_panel)
        self.assertIn("Prefix:", main_panel)
        self.assertIn("to / for", main_panel)
        self.assertNotIn("What Comes Next", main_panel)
        self.assertNotIn("stretch you a bit", main_panel)

    def test_render_feedback_shows_teacher_review_caption_for_flagged_question(self):
        question = {
            "question_type": "phrase_meaning",
            "skill": "phrase_translation",
            "selected_word": "וַיֹּאמֶר אֱלֹהִים",
            "correct_answer": "God said",
            "explanation": "The phrase works as one clause.",
            "choices": ["God said", "God saw", "the earth", "the heavens"],
        }
        st.session_state.pilot_current_question_log_id = "question-1"
        st.session_state.pilot_flagged_question_log_ids = ["question-1"]
        captions = []

        with patch.object(streamlit_app, "last_answer_was_correct", return_value=False), \
             patch.object(streamlit_app.st, "markdown"), \
             patch.object(streamlit_app.st, "caption", side_effect=captions.append), \
             patch.object(streamlit_app.st, "expander", _fake_expander), \
             patch.object(streamlit_app.st, "button", return_value=False):
            streamlit_app.render_feedback(question, {"current_skill": "phrase_translation"})

        self.assertIn("Marked for teacher review.", captions)

    def test_render_feedback_marks_unclear_with_optional_student_note(self):
        question = {
            "question_type": "phrase_meaning",
            "skill": "phrase_translation",
            "selected_word": "וַיֹּאמֶר אֱלֹהִים",
            "correct_answer": "and God said",
            "explanation": "The phrase works as one clause.",
            "choices": ["and God said", "and God saw", "the earth", "the heavens"],
        }

        with patch.object(streamlit_app, "last_answer_was_correct", return_value=False), \
             patch.object(streamlit_app.st, "markdown"), \
             patch.object(streamlit_app.st, "caption"), \
             patch.object(streamlit_app.st, "expander", _fake_expander), \
             patch.object(streamlit_app.st, "text_input", return_value="wording felt unclear"), \
             patch.object(render_feedback_module, "question_is_flagged_unclear", return_value=False), \
             patch.object(render_feedback_module, "mark_current_question_unclear") as mock_mark, \
             patch.object(streamlit_app.st, "button", return_value=True):
            streamlit_app.render_feedback(question, {"current_skill": "phrase_translation"})

        mock_mark.assert_called_once_with(question, note_text="wording felt unclear")

    def test_transition_to_question_clears_transient_messages(self):
        st.session_state.unlocked_skill_message = "Unlocked"
        st.session_state.feature_fallback_message = "Fallback"
        st.session_state.adaptive_status_message = "Status"
        st.session_state.adaptive_status_reason = "Reason"
        st.session_state.adaptive_status_level = "warning"
        st.session_state.answered = True
        st.session_state.selected_answer = "wrong"
        st.session_state.last_skill_state = {"score": 70}
        st.session_state.post_answer_action_pending = "next_mastery"
        st.session_state.scroll_to_question_on_render = False
        st.session_state.current_question_arrival_token = "question-arrival-1"
        st.session_state.question_arrival_counter = 1

        with patch.object(streamlit_app.st, "rerun"):
            streamlit_app.transition_to_question({"question": "Next", "correct_answer": "A"})

        self.assertEqual(st.session_state.unlocked_skill_message, "")
        self.assertEqual(st.session_state.feature_fallback_message, "")
        self.assertEqual(st.session_state.adaptive_status_message, "")
        self.assertEqual(st.session_state.adaptive_status_reason, "")
        self.assertEqual(st.session_state.adaptive_status_level, "info")
        self.assertFalse(st.session_state.answered)
        self.assertIsNone(st.session_state.selected_answer)
        self.assertEqual(st.session_state.post_answer_action_pending, "")
        self.assertTrue(st.session_state.scroll_to_question_on_render)
        self.assertEqual(st.session_state.current_question_arrival_token, "question-arrival-2")


if __name__ == "__main__":
    unittest.main()
