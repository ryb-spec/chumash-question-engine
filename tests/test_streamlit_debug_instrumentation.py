import unittest
from unittest.mock import patch

import streamlit as st

from assessment_scope import active_pesukim_records
import runtime.question_flow as question_flow
import runtime.session_state as session_state
import streamlit_app


class StreamlitDebugInstrumentationTests(unittest.TestCase):
    def setUp(self):
        st.session_state.clear()
        streamlit_app.init_session_state()
        st.session_state.practice_type = "Practice Mode"
        st.session_state.pilot_scope_mode = "open_pilot_scope"

    def test_generate_practice_question_marks_progress_reloaded_when_not_passed(self):
        question = {"question": "Q", "selected_word": "word", "skill": "translation"}

        with patch.object(streamlit_app, "load_progress", return_value={"current_skill": "translation"}), \
             patch.object(question_flow, "select_pasuk_first_question", return_value=dict(question)):
            result = streamlit_app.generate_practice_question("translation")

        trace = result.get("_debug_trace") or {}
        self.assertEqual(trace.get("progress_source"), "reloaded")
        self.assertIsNotNone(trace.get("question_generation_ms"))

    def test_generate_practice_question_marks_progress_reused_when_passed(self):
        question = {"question": "Q", "selected_word": "word", "skill": "translation"}

        with patch.object(question_flow, "select_pasuk_first_question", return_value=dict(question)):
            result = streamlit_app.generate_practice_question("translation", {"current_skill": "translation"})

        trace = result.get("_debug_trace") or {}
        self.assertEqual(trace.get("progress_source"), "reused")
        self.assertIsNotNone(trace.get("question_generation_ms"))

    def test_build_quiz_debug_payload_surfaces_trace_fields(self):
        question = {
            "skill": "identify_suffix_meaning",
            "selected_word": "\u05d6\u05b7\u05e8\u05b0\u05e2\u05d5\u05b9",
            "_assessment_source": "generated skill question from active parsed dataset",
            "_debug_trace": {
                "transition_path": "practice_fallback",
                "fallback_path": "practice_fallback",
                "progress_source": "reused",
                "candidate_filtered": True,
                "candidate_filter_reasons": ["Targeted follow-up unavailable; used practice fallback."],
                "rejection_counts": {
                    "repeated_followup_candidate": 2,
                    "followup_skipped": 1,
                },
                "transition_reason": "Feature repetition fallback used after 10 attempts.",
                "question_generation_ms": 12.5,
                "followup_generation_ms": 8.2,
                "answer_to_next_ready_ms": 44.9,
                "candidate_score_breakdown": {
                    "total": 11.5,
                    "adaptive_weight": 6,
                    "clarity": 2.5,
                    "distractor_separation": 1.5,
                    "novelty": 1.0,
                    "context_dependence": 0.0,
                    "display_compactness": 0.5,
                    "display_context_mode": "compact",
                    "display_context_reason": "word_level_question",
                },
            },
        }

        payload = streamlit_app.build_quiz_debug_payload(
            question,
            progress={"current_skill": "identify_suffix_meaning"},
        )

        self.assertEqual(payload["current_question_source"], "generated skill question from active parsed dataset")
        self.assertEqual(payload["current_skill"], "identify_suffix_meaning")
        self.assertEqual(payload["target_word"], "\u05d6\u05b7\u05e8\u05b0\u05e2\u05d5\u05b9")
        self.assertEqual(payload["routing_mode"], "Practice Mode")
        self.assertEqual(payload["next_question_path"], "practice_fallback")
        self.assertEqual(payload["fallback_path"], "practice_fallback")
        self.assertEqual(payload["progress_source"], "reused")
        self.assertTrue(payload["candidate_filtered"])
        self.assertIn("Targeted follow-up unavailable", payload["candidate_filter_reasons"][0])
        self.assertEqual(payload["rejection_total"], 3)
        self.assertEqual(
            payload["rejection_reason_counts"][0],
            {
                "code": "repeated_followup_candidate",
                "label": "repeated follow-up rejected",
                "count": 2,
            },
        )
        self.assertEqual(payload["transition_reason"], "Feature repetition fallback used after 10 attempts.")
        self.assertEqual(payload["question_generation_ms"], 12.5)
        self.assertEqual(payload["followup_generation_ms"], 8.2)
        self.assertEqual(payload["answer_to_next_ready_ms"], 44.9)
        self.assertEqual(payload["candidate_score_breakdown"]["total"], 11.5)
        self.assertEqual(payload["candidate_score_breakdown"]["display_context_mode"], "compact")

    def test_summarize_debug_rejection_counts_sorts_and_labels_rows(self):
        rows = streamlit_app.summarize_debug_rejection_counts(
            {
                "followup_skipped": 1,
                "repeated_followup_candidate": 3,
                "multiple_prefixes": 2,
            }
        )

        self.assertEqual(
            rows,
            [
                {
                    "code": "repeated_followup_candidate",
                    "label": "repeated follow-up rejected",
                    "count": 3,
                },
                {
                    "code": "multiple_prefixes",
                    "label": "multiple prefixes",
                    "count": 2,
                },
                {
                    "code": "followup_skipped",
                    "label": "follow-up skipped",
                    "count": 1,
                },
            ],
        )

    def test_build_followup_question_fallback_records_rejection_reasons(self):
        active_record = active_pesukim_records()[0]
        second_record = active_pesukim_records()[1]
        progress = {"current_skill": "subject_identification", "prefix_level": 1}
        question = {
            "skill": "subject_identification",
            "question_type": "subject_identification",
            "pasuk": active_record["text"],
            "selected_word": "\u05d0\u05b1\u05dc\u05b9\u05e7\u05b4\u05d9\u05dd",
            "question": "Who is doing the action in \u05d1\u05bc\u05b8\u05e8\u05b8\u05d0?",
        }
        stale_followup = {
            "skill": "subject_identification",
            "question_type": "subject_identification",
            "question": "Who is doing the action in \u05d1\u05bc\u05b8\u05e8\u05b8\u05d0?",
            "selected_word": "\u05d0\u05b1\u05dc\u05b9\u05e7\u05b4\u05d9\u05dd",
            "correct_answer": "God",
            "choices": ["God", "the man", "the earth", "the light"],
        }
        fallback_question = {
            "skill": "subject_identification",
            "question_type": "subject_identification",
            "question": "Who is doing the action here?",
            "selected_word": "\u05d4\u05b8\u05d0\u05b8\u05e8\u05b6\u05e5",
            "word": "\u05d4\u05b8\u05d0\u05b8\u05e8\u05b6\u05e5",
            "correct_answer": "the earth",
            "choices": ["the earth", "God", "light", "water"],
            "pasuk": second_record["text"],
            "pasuk_ref": {"pasuk_id": second_record["pasuk_id"], "label": "Bereishis 1:2"},
        }

        with patch.object(question_flow, "analyze_generator_pasuk", return_value=[{"word": "\u05d0\u05b1\u05dc\u05b9\u05e7\u05b4\u05d9\u05dd"}]), \
             patch.object(question_flow, "generate_skill_question", return_value=stale_followup), \
             patch.object(question_flow, "generate_practice_question", return_value=dict(fallback_question)), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = streamlit_app.build_followup_question(progress, question)

        trace = result.get("_debug_trace") or {}
        self.assertEqual(trace.get("transition_path"), "practice_fallback")
        self.assertEqual(trace.get("progress_source"), "reused")
        self.assertTrue(trace.get("candidate_filtered"))
        self.assertEqual(trace.get("fallback_path"), "practice_fallback")
        self.assertTrue(any("repeated follow-up candidate" in reason for reason in trace.get("candidate_filter_reasons", [])))
        self.assertTrue(any("used practice fallback" in reason for reason in trace.get("candidate_filter_reasons", [])))
        self.assertEqual(trace.get("rejection_counts", {}).get("repeated_followup_candidate"), 2)
        self.assertEqual(trace.get("transition_reason"), "Targeted follow-up unavailable; used practice fallback.")
        self.assertIsNotNone(trace.get("followup_generation_ms"))


if __name__ == "__main__":
    unittest.main()
