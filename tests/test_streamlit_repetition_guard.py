import unittest
from unittest.mock import patch

import streamlit as st

import streamlit_app


class StreamlitRepetitionGuardTests(unittest.TestCase):
    def setUp(self):
        st.session_state.clear()
        streamlit_app.init_session_state()
        st.session_state.practice_type = "Practice Mode"

    def _translation_question(self, word="בָּרָא", prompt="What does בָּרָא mean?"):
        return {
            "skill": "translation",
            "question_type": "translation",
            "question": prompt,
            "selected_word": word,
            "word": word,
            "correct_answer": "created",
            "choices": ["created", "light", "earth", "water"],
            "pasuk": "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
        }

    def test_recent_question_repeat_reason_blocks_exact_repeat(self):
        question = self._translation_question()
        recent = [streamlit_app.question_signature(question)]

        reason = streamlit_app.recent_question_repeat_reason(question, recent)

        self.assertEqual(reason, "recent_exact_repeat")

    def test_recent_question_repeat_reason_blocks_near_duplicate_same_target(self):
        first = self._translation_question(prompt="What does בָּרָא mean?")
        near_duplicate = self._translation_question(prompt="Choose the meaning of בָּרָא.")
        near_duplicate["question_type"] = "translation_variant"
        recent = [streamlit_app.question_signature(first)]

        reason = streamlit_app.recent_question_repeat_reason(near_duplicate, recent)

        self.assertEqual(reason, "recent_target_repeat")

    def test_select_pasuk_first_question_allows_reteach_exception(self):
        repeated_question = self._translation_question()
        st.session_state.recent_questions = [streamlit_app.question_signature(repeated_question)]

        with patch.object(streamlit_app, "get_skill_ready_pasuks", return_value=[{"pasuk": repeated_question["pasuk"]}]), \
             patch.object(streamlit_app, "generate_skill_question", return_value=dict(repeated_question)), \
             patch.object(streamlit_app, "record_selected_pasuk"), \
             patch.object(streamlit_app, "record_question_feature"), \
             patch.object(streamlit_app, "record_question_prefix"):
            result = streamlit_app.select_pasuk_first_question(
                "translation",
                progress={"current_skill": "translation", "prefix_level": 1},
                adaptive_context={"selection_mode": "reteach", "preferred_pasuk": repeated_question["pasuk"]},
            )

        trace = result.get("_debug_trace") or {}
        self.assertEqual(result["selected_word"], "בָּרָא")
        self.assertFalse(trace.get("fallback_path"))
        self.assertNotIn("limited_candidate_reuse", trace.get("rejection_counts", {}))

    def test_select_pasuk_first_question_uses_limited_candidate_fallback_without_stalling(self):
        repeated_question = self._translation_question()
        st.session_state.recent_questions = [streamlit_app.question_signature(repeated_question)]

        with patch.object(streamlit_app, "get_skill_ready_pasuks", return_value=[{"pasuk": repeated_question["pasuk"]}]), \
             patch.object(streamlit_app, "generate_skill_question", return_value=dict(repeated_question)), \
             patch.object(streamlit_app, "record_selected_pasuk"), \
             patch.object(streamlit_app, "record_question_feature"), \
             patch.object(streamlit_app, "record_question_prefix"):
            result = streamlit_app.select_pasuk_first_question(
                "translation",
                progress={"current_skill": "translation", "prefix_level": 1},
            )

        trace = result.get("_debug_trace") or {}
        self.assertEqual(result["selected_word"], "בָּרָא")
        self.assertEqual(trace.get("fallback_path"), "limited_candidate_reuse")
        self.assertEqual(
            trace.get("transition_reason"),
            "Freshness fallback used because the safe candidate pool was too small.",
        )
        self.assertGreater(trace.get("rejection_counts", {}).get("recent_exact_repeat", 0), 0)
        self.assertEqual(trace.get("rejection_counts", {}).get("limited_candidate_reuse"), 1)


if __name__ == "__main__":
    unittest.main()
