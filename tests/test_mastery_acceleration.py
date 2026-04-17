import unittest
from unittest.mock import patch

import streamlit as st

import streamlit_app
from adaptive_engine import evaluate_skill_progression
from progress_store import ensure_progress_state


class MasteryAccelerationTests(unittest.TestCase):
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

    def test_fast_pass_advances_one_skill_on_strong_recent_run(self):
        decision = evaluate_skill_progression(
            current_skill="identify_prefix_meaning",
            answered_skill="identify_prefix_meaning",
            skill_state={
                "score": 76,
                "current_streak": 4,
                "challenge_streak": 1,
                "mastered": False,
                "last_12_results": [True, True, False, True, True],
                "error_counts": {},
            },
            is_correct=True,
            skill_order=[
                "identify_prefix_meaning",
                "identify_suffix_meaning",
                "identify_pronoun_suffix",
            ],
            skill_label="How words are built",
            next_skill_label="How words are built",
        )

        self.assertEqual(decision["route"], "fast_pass")
        self.assertEqual(decision["target_skill"], "identify_suffix_meaning")

    def test_handle_answer_applies_fast_pass_in_learn_mode(self):
        progress = ensure_progress_state(
            {
                "current_skill": "identify_prefix_meaning",
                "skills": {
                    "identify_prefix_meaning": {
                        "score": 73,
                        "correct_count": 3,
                        "incorrect_count": 0,
                        "current_streak": 3,
                        "best_streak": 3,
                        "challenge_streak": 0,
                        "last_12_results": [True, True, False, True],
                        "error_counts": {},
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
        }

        with patch.object(streamlit_app, "save_progress"), patch.object(streamlit_app, "update_word_skill_score"):
            streamlit_app.handle_answer("ל", question, progress)

        self.assertEqual(progress["current_skill"], "identify_suffix_meaning")
        self.assertEqual(st.session_state.adaptive_status_level, "success")
        self.assertIn("move early", st.session_state.adaptive_status_message.lower())

    def test_clear_elite_run_can_skip_two_skills(self):
        decision = evaluate_skill_progression(
            current_skill="identify_prefix_meaning",
            answered_skill="identify_prefix_meaning",
            skill_state={
                "score": 92,
                "current_streak": 6,
                "challenge_streak": 2,
                "mastered": False,
                "last_12_results": [True, True, True, True, True, True],
                "error_counts": {},
            },
            is_correct=True,
            skill_order=[
                "identify_prefix_meaning",
                "identify_suffix_meaning",
                "identify_pronoun_suffix",
                "identify_verb_marker",
            ],
            skill_label="How words are built",
            next_skill_label="How words are built",
        )

        self.assertEqual(decision["route"], "double_fast_pass")
        self.assertEqual(decision["target_skill"], "identify_pronoun_suffix")


if __name__ == "__main__":
    unittest.main()
