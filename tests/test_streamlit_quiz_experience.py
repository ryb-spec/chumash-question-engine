import unittest
from contextlib import contextmanager
from unittest.mock import patch

import streamlit as st

import pasuk_flow_generator
import runtime.question_flow as question_flow
import runtime.session_state as session_state
import streamlit_app


@contextmanager
def _fake_expander(*args, **kwargs):
    yield


class StreamlitQuizExperienceTests(unittest.TestCase):
    def setUp(self):
        st.session_state.clear()
        streamlit_app.init_session_state()
        st.session_state.practice_type = "Learn Mode"
        st.session_state.show_nekudos = True
        st.session_state.pasuk_view_mode = "Full pasuk view"
        st.session_state.selected_answer = "wrong"
        st.session_state.answered = True
        st.session_state.last_skill_state = {"score": 72, "current_streak": 2, "point_change": "+0"}

    def _sample_prefix_question(self):
        return {
            "id": "quiz-experience-q1",
            "question": "What does לָאוֹר mean?",
            "selected_word": "לָאוֹר",
            "word": "לָאוֹר",
            "correct_answer": "to / for light",
            "choices": ["to / for light", "in the light", "and light", "the light"],
            "skill": "identify_prefix_meaning",
            "question_type": "prefix_level_3_apply_prefix_meaning",
            "prefix": "ל",
            "prefix_meaning": "to / for",
            "explanation": "Prefix: ל. Here it means 'to / for'.",
            "pasuk": "וַיַּבְדֵּל אֱלֹקִים בֵּין הָאוֹר וּבֵין הַחֹשֶׁךְ",
        }

    def test_learning_header_omits_old_explanatory_panels(self):
        question = self._sample_prefix_question()
        rendered = []

        with patch.object(streamlit_app.st, "markdown", side_effect=lambda body, **kwargs: rendered.append(body)), \
             patch.object(streamlit_app.st, "progress"):
            streamlit_app.render_learning_header(
                question,
                {"standards": {"PR": 70}, "xp": {"PR": 10}, "current_skill": "identify_prefix_meaning"},
            )

        header_html = next(body for body in rendered if "learning-header" in body)
        self.assertNotIn("Why This Question", header_html)
        self.assertNotIn("What Happens Next", header_html)
        self.assertIn("Mastery", header_html)

    def test_answer_choice_labels_support_expanded_affix_choice_banks(self):
        self.assertEqual(streamlit_app.answer_choice_label("ש", 6), "G. ש")

    def test_quiz_render_sequence_prioritizes_question_answers_and_submit(self):
        question = self._sample_prefix_question()
        progress = {"standards": {"PR": 70}, "xp": {"PR": 10}, "current_skill": "identify_prefix_meaning"}
        events = []
        st.session_state.answered = False

        def capture_markdown(body, **kwargs):
            events.append(("markdown", body))

        def capture_radio(label, *args, **kwargs):
            events.append(("radio", label))
            return None

        def capture_button(label, **kwargs):
            events.append(("button", label))
            return False

        with patch.object(streamlit_app.st, "markdown", side_effect=capture_markdown), \
             patch.object(streamlit_app.st, "radio", side_effect=capture_radio), \
             patch.object(streamlit_app.st, "button", side_effect=capture_button), \
             patch.object(streamlit_app.st, "progress"), \
             patch.object(streamlit_app.st, "expander", _fake_expander), \
             patch.object(streamlit_app, "render_enter_key_handler"):
            streamlit_app.render_question(question, progress, "quiz_experience")

        radio_index = next(index for index, event in enumerate(events) if event[0] == "radio")
        button_index = next(index for index, event in enumerate(events) if event[0] == "button")
        question_index = next(
            index
            for index, event in enumerate(events)
            if event[0] == "markdown" and "question-card" in event[1]
        )
        answer_label_index = next(
            index
            for index, event in enumerate(events)
            if event[0] == "markdown" and "answer-label" in event[1]
        )

        self.assertLess(question_index, answer_label_index)
        self.assertLess(answer_label_index, radio_index)
        self.assertLess(radio_index, button_index)
        self.assertLessEqual(question_index, 5)

    def test_no_duplicate_explanatory_panels_before_question(self):
        question = self._sample_prefix_question()
        progress = {"standards": {"PR": 70}, "xp": {"PR": 10}, "current_skill": "identify_prefix_meaning"}
        events = []

        def capture_markdown(body, **kwargs):
            events.append(body)

        with patch.object(streamlit_app.st, "markdown", side_effect=capture_markdown), \
             patch.object(streamlit_app.st, "radio", return_value=None), \
             patch.object(streamlit_app.st, "button", return_value=False), \
             patch.object(streamlit_app.st, "progress"), \
             patch.object(streamlit_app.st, "expander", _fake_expander), \
             patch.object(streamlit_app, "render_enter_key_handler"):
            streamlit_app.render_question(question, progress, "quiz_experience")

        pre_answer_html = "\n".join(body for body in events if "feedback-panel" not in body)
        self.assertEqual(pre_answer_html.count("learning-header"), 1)
        self.assertEqual(pre_answer_html.count("question-card"), 1)
        self.assertNotIn("Why This Question", pre_answer_html)
        self.assertNotIn("What Happens Next", pre_answer_html)
        self.assertNotIn("Why this question", pre_answer_html)

    def test_ambiguous_prefix_runtime_form_is_skipped(self):
        question = pasuk_flow_generator.generate_question(
            "identify_prefix_meaning",
            "ולמראה",
        )

        self.assertEqual(question.get("status"), "skipped")
        self.assertIn("No usable prefixed word", question.get("reason", ""))

    def test_feedback_main_panel_omits_generic_progression_narration(self):
        question = self._sample_prefix_question()
        rendered = []

        with patch.object(streamlit_app, "last_answer_was_correct", return_value=False), \
             patch.object(streamlit_app.st, "markdown", side_effect=lambda body, **kwargs: rendered.append(body)), \
             patch.object(streamlit_app.st, "caption"), \
             patch.object(streamlit_app.st, "expander", _fake_expander), \
             patch.object(streamlit_app.st, "button", return_value=False):
            streamlit_app.render_feedback(question, {"current_skill": "identify_prefix_meaning"})

        main_panel = next(body for body in rendered if "feedback-panel" in body)
        self.assertIn("Grammar", main_panel)
        self.assertNotIn("What Comes Next", main_panel)
        self.assertNotIn("What Happens Next", main_panel)
        self.assertNotIn("Why This Question", main_panel)

    def test_followup_generation_does_not_repeat_same_question_unnecessarily(self):
        progress = {"current_skill": "translation", "prefix_level": 1}
        question = {
            "skill": "translation",
            "pasuk": "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
            "selected_word": "בְּרֵאשִׁית",
            "question": "What does בְּרֵאשִׁית mean?",
        }
        stale_followup = {
            "skill": "translation",
            "question": "What does בְּרֵאשִׁית mean?",
            "selected_word": "בְּרֵאשִׁית",
            "correct_answer": "in the beginning",
            "choices": ["in the beginning", "created", "God", "earth"],
        }
        fallback_question = {
            "skill": "translation",
            "question": "What does בָּרָא mean?",
            "selected_word": "בָּרָא",
            "correct_answer": "created",
            "choices": ["created", "in the beginning", "earth", "light"],
        }

        with patch.object(question_flow, "analyze_generator_pasuk", return_value=[{"word": "בְּרֵאשִׁית"}]), \
             patch.object(question_flow, "generate_skill_question", return_value=stale_followup), \
             patch.object(question_flow, "generate_practice_question", return_value=dict(fallback_question)), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = streamlit_app.build_followup_question(progress, question)

        self.assertEqual(result["selected_word"], "בָּרָא")
        self.assertNotEqual(result["question"], question["question"])


if __name__ == "__main__":
    unittest.main()
