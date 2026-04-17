import unittest
from unittest.mock import patch

import streamlit as st

import streamlit_app
from adaptive_engine import candidate_weight
from progress_store import ensure_progress_state


class ReteachRoutingTests(unittest.TestCase):
    def setUp(self):
        st.session_state.clear()
        st.session_state.answered = False
        st.session_state.selected_answer = None
        st.session_state.questions_answered = 0
        st.session_state.level5_answered = 0
        st.session_state.asked_tokens = []
        st.session_state.asked_question_ids = []
        st.session_state.asked_pasuks = []
        st.session_state.recent_phrases = []
        st.session_state.recent_question_formats = []
        st.session_state.practice_type = "Learn Mode"
        st.session_state.unlocked_skill_message = ""
        st.session_state.adaptive_status_message = ""
        st.session_state.adaptive_status_reason = ""
        st.session_state.adaptive_status_level = "info"
        st.session_state.pending_adaptive_context = {}

    def test_candidate_weight_prefers_same_pasuk_for_reteach(self):
        progress = {
            "word_exposure": {
                "לָאוֹר": {"seen": 2, "correct": 0, "recent_streak": 0, "mastered": False},
                "הָאוֹר": {"seen": 4, "correct": 4, "recent_streak": 4, "mastered": True},
            }
        }
        recent_pesukim = ["Bereishis 1:3"]
        recent_words = ["אוֹר"]
        adaptive_context = {
            "selection_mode": "reteach",
            "preferred_pasuk": "Bereishis 1:3",
            "avoid_word": "אוֹר",
        }

        reteach_score = candidate_weight(
            {"pasuk": "Bereishis 1:3", "word": "לָאוֹר"},
            progress,
            recent_pesukim,
            recent_words,
            adaptive_context=adaptive_context,
        )
        mastered_score = candidate_weight(
            {"pasuk": "Bereishis 1:5", "word": "הָאוֹר"},
            progress,
            recent_pesukim,
            recent_words,
            adaptive_context=adaptive_context,
        )

        self.assertGreater(reteach_score, mastered_score)

    def test_clustered_errors_keep_current_skill_and_explain_why(self):
        progress = ensure_progress_state(
            {
                "current_skill": "identify_prefix_meaning",
                "skills": {
                    "identify_prefix_meaning": {
                        "score": 52,
                        "correct_count": 1,
                        "incorrect_count": 2,
                        "current_streak": 0,
                        "best_streak": 1,
                        "challenge_streak": 0,
                        "last_12_results": [True, False, False],
                        "error_counts": {"prefix_error": 1},
                        "mastered": False,
                    }
                },
            }
        )
        question = {
            "skill": "identify_prefix_meaning",
            "standard": "PR",
            "micro_standard": "PR1",
            "word": "לָאוֹר",
            "selected_word": "לָאוֹר",
            "correct_answer": "ל",
            "difficulty": 1,
            "pasuk": "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
        }

        with patch.object(streamlit_app, "save_progress"), patch.object(streamlit_app, "update_word_skill_score"):
            streamlit_app.handle_answer("ב", question, progress)

        self.assertEqual(progress["current_skill"], "identify_prefix_meaning")
        self.assertEqual(st.session_state.adaptive_status_level, "warning")
        self.assertIn("staying with", st.session_state.adaptive_status_message.lower())
        self.assertEqual(
            st.session_state.pending_adaptive_context.get("selection_mode"),
            "reteach",
        )


if __name__ == "__main__":
    unittest.main()
