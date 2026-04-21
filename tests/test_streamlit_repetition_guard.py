import unittest
from unittest.mock import patch

import streamlit as st

import runtime.question_flow as question_flow
import runtime.session_state as session_state
import streamlit_app


class StreamlitRepetitionGuardTests(unittest.TestCase):
    def setUp(self):
        st.session_state.clear()
        streamlit_app.init_session_state()
        st.session_state.practice_type = "Practice Mode"
        st.session_state.pilot_scope_mode = "open_pilot_scope"

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

    def test_recent_question_repeat_reason_blocks_same_pasuk_intent_inside_near_window(self):
        first = self._translation_question(prompt="What does בָּרָא mean?")
        first["correct_answer"] = "God"
        first["choices"] = ["God", "water", "earth", "garden"]
        middle = self._translation_question(word="אֱלֹקִים", prompt="What does אֱלֹקִים mean?")
        middle["correct_answer"] = "God"
        next_question = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does רָקִיעַ mean?",
            "selected_word": "רָקִיעַ",
            "word": "רָקִיעַ",
            "correct_answer": "earth",
            "choices": ["earth", "water", "light", "garden"],
            "pasuk": first["pasuk"],
        }
        recent = [
            streamlit_app.question_signature(first),
            streamlit_app.question_signature(middle),
        ]

        reason = streamlit_app.recent_question_repeat_reason(next_question, recent)

        self.assertEqual(reason, "recent_same_pasuk_intent_repeat")

    def test_select_pasuk_first_question_allows_reteach_exception(self):
        repeated_question = self._translation_question()
        st.session_state.recent_questions = [streamlit_app.question_signature(repeated_question)]

        with patch.object(question_flow, "get_skill_ready_pasuks", return_value=[{"pasuk": repeated_question["pasuk"]}]), \
             patch.object(question_flow, "generate_skill_question", return_value=dict(repeated_question)), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = streamlit_app.select_pasuk_first_question(
                "translation",
                progress={"current_skill": "translation", "prefix_level": 1},
                adaptive_context={"selection_mode": "reteach", "preferred_pasuk": repeated_question["pasuk"]},
            )

        trace = result.get("_debug_trace") or {}
        self.assertEqual(result["selected_word"], "בָּרָא")
        self.assertFalse(trace.get("fallback_path"))
        self.assertNotIn("limited_candidate_reuse", trace.get("rejection_counts", {}))
        self.assertEqual(trace.get("reuse_mode"), "explicit_reteach_reuse")
        self.assertEqual(trace.get("selection_mode"), "reteach")
        self.assertEqual(trace.get("rejection_counts", {}).get("explicit_reteach_reuse"), 1)

    def test_select_pasuk_first_question_uses_limited_candidate_fallback_without_stalling(self):
        repeated_question = self._translation_question()
        st.session_state.recent_questions = [streamlit_app.question_signature(repeated_question)]

        with patch.object(question_flow, "get_skill_ready_pasuks", return_value=[{"pasuk": repeated_question["pasuk"]}]), \
             patch.object(question_flow, "generate_skill_question", return_value=dict(repeated_question)), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
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

    def test_select_pasuk_first_question_prefers_different_prefix_letter_when_available(self):
        st.session_state.practice_type = "Learn Mode"
        st.session_state.recent_prefixes = ["ל"]

        def generate_question(skill, candidate_source, **kwargs):
            if candidate_source == "pasuk_lamed":
                return {
                    "skill": "identify_prefix_meaning",
                    "question_type": "prefix_level_3_apply_prefix_meaning",
                    "question": "What does לָאוֹר mean?",
                    "selected_word": "לָאוֹר",
                    "word": "לָאוֹר",
                    "prefix": "ל",
                    "correct_answer": "to / for light",
                    "choices": ["to / for light", "in the light", "the light", "light"],
                    "pasuk": "pasuk_lamed",
                }
            return {
                "skill": "identify_prefix_meaning",
                "question_type": "prefix_level_1_identify_prefix_meaning",
                "question": "What does בַּמָּיִם mean?",
                "selected_word": "בַּמָּיִם",
                "word": "בַּמָּיִם",
                "prefix": "ב",
                "correct_answer": "in",
                "choices": ["in", "to / for", "from", "the"],
                "pasuk": "pasuk_bet",
            }

        with patch.object(
            question_flow,
            "get_skill_ready_pasuks",
            return_value=[
                {"pasuk": "pasuk_lamed", "word": "לָאוֹר", "feature": "prefix", "prefix": "ל", "morpheme_family": ""},
                {"pasuk": "pasuk_bet", "word": "בַּמָּיִם", "feature": "prefix", "prefix": "ב", "morpheme_family": ""},
            ],
        ), \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(question_flow, "generate_skill_question", side_effect=generate_question), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = streamlit_app.select_pasuk_first_question(
                "identify_prefix_meaning",
                progress={"current_skill": "identify_prefix_meaning", "prefix_level": 3},
            )

        self.assertEqual(result["prefix"], "ב")
        self.assertEqual(result["_debug_trace"]["rejection_counts"].get("prefix_repeat_blocked"), 1)


if __name__ == "__main__":
    unittest.main()
