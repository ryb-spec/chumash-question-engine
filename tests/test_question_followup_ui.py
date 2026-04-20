import unittest
from unittest.mock import patch

import streamlit as st

import runtime.question_flow as question_flow
import runtime.session_state as session_state
import streamlit_app
from question_ui import build_followup_plan


class QuestionFollowupUiTests(unittest.TestCase):
    def setUp(self):
        st.session_state.clear()
        st.session_state.pilot_scope_mode = "open"
        st.session_state.recent_phrases = []
        st.session_state.asked_tokens = []
        st.session_state.asked_question_ids = []
        st.session_state.asked_pasuks = []
        st.session_state.recent_pesukim = []
        st.session_state.recent_question_formats = []
        st.session_state.recent_prefixes = []
        st.session_state.recent_features = []

    def test_followup_plan_after_error_prefers_retry_similar(self):
        plan = build_followup_plan(
            practice_type="Practice Mode",
            is_correct=False,
            skill_label="Prefixes",
            next_skill_label="Suffixes",
        )

        self.assertEqual(plan["route"], "retry_similar")
        self.assertEqual(plan["primary_label"], "Try One Like This")
        self.assertEqual(plan["secondary_label"], "Continue")

    def test_build_followup_question_prefers_targeted_same_skill_output(self):
        progress = {"current_skill": "translation", "prefix_level": 1}
        question = {
            "skill": "translation",
            "pasuk": "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
            "selected_word": "בְּרֵאשִׁית",
            "question": "What does בְּרֵאשִׁית mean?",
        }
        followup_question = {
            "skill": "translation",
            "question": "What does בָּרָא mean?",
            "selected_word": "בָּרָא",
            "correct_answer": "created",
            "choices": ["created", "began", "saw", "said"],
        }

        with patch.object(question_flow, "analyze_generator_pasuk", return_value=[{"word": "בְּרֵאשִׁית"}]), \
             patch.object(question_flow, "generate_skill_question", return_value=followup_question), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = streamlit_app.build_followup_question(progress, question)

        self.assertEqual(result["selected_word"], "בָּרָא")
        self.assertEqual(result["_assessment_source"], "targeted follow-up from active parsed dataset")
        self.assertEqual(result["pasuk"], question["pasuk"])


if __name__ == "__main__":
    unittest.main()
