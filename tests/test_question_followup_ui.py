import unittest
from unittest.mock import patch

import streamlit as st

import runtime.question_flow as question_flow
import runtime.session_state as session_state
import streamlit_app
from assessment_scope import active_pesukim_records
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

    def test_followup_plan_keeps_canonical_skill_labels_intact(self):
        plan = build_followup_plan(
            practice_type="Learn Mode",
            is_correct=False,
            skill_label="How verbs are built · Verb tense",
            next_skill_label="Word meaning",
        )

        self.assertIn("How verbs are built · Verb tense", plan["summary"])
        self.assertNotIn("how verbs are built · verb tense", plan["summary"])

    def test_build_followup_question_prefers_targeted_same_skill_output(self):
        active_record = active_pesukim_records()[0]
        progress = {"current_skill": "subject_identification", "prefix_level": 1}
        question = {
            "skill": "subject_identification",
            "question_type": "subject_identification",
            "pasuk": active_record["text"],
            "pasuk_ref": active_record["ref"],
            "selected_word": "אֱלֹקִים",
            "word": "אֱלֹקִים",
            "question": "Who is doing the action here?",
        }
        followup_question = {
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

        with patch.object(question_flow, "analyze_generator_pasuk", return_value=[{"word": "אֱלֹקִים"}]), \
             patch.object(question_flow, "generate_skill_question", return_value=followup_question), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = streamlit_app.build_followup_question(progress, question)

        self.assertEqual(result["selected_word"], "הַשָּׁמַיִם")
        self.assertEqual(result["_assessment_source"], "targeted follow-up from active parsed dataset")
        self.assertEqual(result["pasuk"], question["pasuk"])


if __name__ == "__main__":
    unittest.main()
