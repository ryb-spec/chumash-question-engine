import unittest
from contextlib import contextmanager
from unittest.mock import patch

import streamlit as st

import pasuk_flow_generator
import runtime.mode_handlers as mode_handlers
import runtime.question_flow as question_flow
import runtime.session_state as session_state
import streamlit_app
from ui import render_question as render_question_module


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
        self.assertLessEqual(question_index, 6)

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


    def test_answered_mastery_mode_keeps_next_action_visible(self):
        question = self._sample_prefix_question()
        progress = {"current_skill": "identify_prefix_meaning"}
        st.session_state.current_question = question
        st.session_state.answered = True
        rendered = []

        with patch.object(mode_handlers, "render_question"), \
             patch.object(mode_handlers, "render_assessment_diagnostics"), \
             patch.object(mode_handlers, "last_answer_was_correct", return_value=True), \
             patch.object(mode_handlers, "render_enter_key_handler"), \
             patch.object(mode_handlers.st, "markdown", side_effect=lambda body, **kwargs: rendered.append(body)), \
             patch.object(mode_handlers.st, "button", return_value=False) as mock_button:
            streamlit_app.render_mastery_mode(progress)

        self.assertTrue(any("post-answer-action-sentinel" in body for body in rendered))
        mock_button.assert_called_with(
            "Next Question",
            type="primary",
            use_container_width=True,
            key="next_mastery",
        )

    def test_pending_mastery_continue_after_error_shows_loading_and_blocks_duplicate_clicks(self):
        question = self._sample_prefix_question()
        next_question = {
            **question,
            "question": "What does ×‘Ö¸Ö¼×¨Ö¸× mean?",
            "selected_word": "×‘Ö¸Ö¼×¨Ö¸×",
            "correct_answer": "created",
            "choices": ["created", "light", "earth", "water"],
        }
        progress = {"current_skill": "identify_prefix_meaning"}
        st.session_state.current_question = question
        st.session_state.answered = True
        st.session_state.post_answer_action_pending = "continue_mastery_after_error"
        button_calls = []

        def capture_button(label, **kwargs):
            button_calls.append((label, kwargs))
            return False

        with patch.object(mode_handlers, "render_question"), \
             patch.object(mode_handlers, "render_assessment_diagnostics"), \
             patch.object(mode_handlers, "last_answer_was_correct", return_value=False), \
             patch.object(mode_handlers, "render_enter_key_handler"), \
             patch.object(mode_handlers, "generate_mastery_question", return_value=next_question) as mock_generate, \
             patch.object(mode_handlers, "transition_to_question") as mock_transition, \
             patch.object(mode_handlers.st, "spinner", _fake_expander), \
             patch.object(mode_handlers.st, "button", side_effect=capture_button):
            streamlit_app.render_mastery_mode(progress)

        self.assertEqual(button_calls[0][0], "Loading next question...")
        self.assertTrue(button_calls[0][1]["disabled"])
        self.assertNotIn("Continue", [label for label, _ in button_calls[1:]])
        self.assertEqual(st.session_state.post_answer_action_pending, "")
        mock_generate.assert_called_once_with(progress)
        mock_transition.assert_called_once()

    def test_render_question_emits_unique_arrival_token_and_wrapper_id(self):
        question = self._sample_prefix_question()
        progress = {"standards": {"PR": 70}, "xp": {"PR": 10}, "current_skill": "identify_prefix_meaning"}
        st.session_state.answered = False
        st.session_state.current_question_arrival_token = "question-arrival-7"
        rendered = []
        emitted_scripts = []

        with patch.object(streamlit_app.st, "markdown", side_effect=lambda body, **kwargs: rendered.append(body)), \
             patch.object(streamlit_app.st, "radio", return_value=None), \
             patch.object(streamlit_app.st, "button", return_value=False), \
             patch.object(streamlit_app.st, "progress"), \
             patch.object(streamlit_app.st, "expander", _fake_expander), \
             patch.object(streamlit_app, "render_enter_key_handler"), \
             patch.object(render_question_module.components, "html", side_effect=lambda body, **kwargs: emitted_scripts.append(body)):
            streamlit_app.render_question(question, progress, "quiz_experience")

        question_markup = next(body for body in rendered if "question-card" in body)
        self.assertIn('id="student-question-wrapper-question-arrival-7"', question_markup)
        self.assertIn('data-arrival-token="question-arrival-7"', question_markup)
        self.assertTrue(any("student-question-wrapper-question-arrival-7" in body for body in emitted_scripts))
        self.assertTrue(any("__assessmentArrivalHandledToken" in body for body in emitted_scripts))

    def test_render_question_skips_arrival_hook_without_new_question_state(self):
        question = self._sample_prefix_question()
        progress = {"standards": {"PR": 70}, "xp": {"PR": 10}, "current_skill": "identify_prefix_meaning"}
        st.session_state.answered = False
        st.session_state.current_question_arrival_token = "question-arrival-9"
        st.session_state.last_question_scroll_token = "question-arrival-9"
        st.session_state.scroll_to_question_on_render = False
        emitted_scripts = []

        with patch.object(streamlit_app.st, "markdown"), \
             patch.object(streamlit_app.st, "radio", return_value=None), \
             patch.object(streamlit_app.st, "button", return_value=False), \
             patch.object(streamlit_app.st, "progress"), \
             patch.object(streamlit_app.st, "expander", _fake_expander), \
             patch.object(streamlit_app, "render_enter_key_handler"), \
             patch.object(render_question_module.components, "html", side_effect=lambda body, **kwargs: emitted_scripts.append(body)):
            streamlit_app.render_question(question, progress, "quiz_experience")

        self.assertFalse(any("__assessmentArrivalHandledToken" in body for body in emitted_scripts))


if __name__ == "__main__":
    unittest.main()
