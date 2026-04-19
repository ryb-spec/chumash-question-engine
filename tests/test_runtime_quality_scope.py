import unittest
from unittest.mock import patch
import json
from pathlib import Path

import streamlit as st

import runtime.question_flow as question_flow
import runtime.session_state as session_state
import streamlit_app
from assessment_scope import active_pesukim_records
from pasuk_flow_generator import generate_pasuk_flow, generate_question, is_placeholder_translation


def newly_active_scope_pesukim():
    return [
        record["text"]
        for record in active_pesukim_records()
        if record.get("ref", {}).get("perek") == 1
        and 21 <= record.get("ref", {}).get("pasuk", 0) <= 30
    ]


def promoted_scope_pesukim():
    return [
        record["text"]
        for record in active_pesukim_records()
        if (
            record.get("ref", {}).get("perek") == 1
            and record.get("ref", {}).get("pasuk", 0) == 31
        )
        or (
            record.get("ref", {}).get("perek") == 2
            and 1 <= record.get("ref", {}).get("pasuk", 0) <= 9
        )
    ]


class ActiveRuntimeQualityTests(unittest.TestCase):
    def setUp(self):
        st.session_state.clear()
        st.session_state.asked_tokens = []
        st.session_state.asked_question_ids = []
        st.session_state.asked_pasuks = []
        st.session_state.recent_pesukim = []
        st.session_state.recent_phrases = []
        st.session_state.recent_question_formats = []
        st.session_state.recent_prefixes = []
        st.session_state.recent_features = []
        st.session_state.feature_fallback_message = ""

    def test_newly_active_flows_avoid_duplicate_question_prompts(self):
        for pasuk in newly_active_scope_pesukim():
            flow = generate_pasuk_flow(pasuk)
            prompts = [question.get("question") for question in flow.get("questions", [])]
            self.assertEqual(
                len(prompts),
                len(set(prompts)),
                f"Repeated prompt found in flow for {pasuk}",
            )

    def test_newly_active_translation_like_questions_avoid_placeholder_answers(self):
        translation_like_types = {
            "translation",
            "phrase_meaning",
            "phrase_translation",
            "subject_identification",
        }

        for pasuk in newly_active_scope_pesukim():
            flow = generate_pasuk_flow(pasuk)
            for question in flow.get("questions", []):
                if question.get("question_type") not in translation_like_types:
                    continue

                token = question.get("selected_word") or question.get("word")
                self.assertFalse(
                    is_placeholder_translation(question.get("correct_answer"), token),
                    f"Weak translation output for {token} in {pasuk}",
                )
                self.assertEqual(len(question.get("choices", [])), 4)
                self.assertEqual(len(set(question.get("choices", []))), 4)
                self.assertFalse(
                    any(
                        is_placeholder_translation(choice, token)
                        for choice in question.get("choices", [])
                    ),
                    f"Placeholder distractor found for {token} in {pasuk}",
                )

    def test_promoted_scope_translation_like_questions_avoid_placeholder_answers(self):
        translation_like_types = {
            "translation",
            "phrase_meaning",
            "phrase_translation",
            "subject_identification",
        }

        for pasuk in promoted_scope_pesukim():
            flow = generate_pasuk_flow(pasuk)
            self.assertGreaterEqual(len(flow.get("questions", [])), 3)
            for question in flow.get("questions", []):
                if question.get("question_type") not in translation_like_types:
                    continue

                token = question.get("selected_word") or question.get("word")
                self.assertFalse(
                    is_placeholder_translation(question.get("correct_answer"), token),
                    f"Weak promoted-scope translation output for {token} in {pasuk}",
                )
                self.assertEqual(len(question.get("choices", [])), 4)
                self.assertEqual(len(set(question.get("choices", []))), 4)
                self.assertFalse(
                    any(
                        is_placeholder_translation(choice, token)
                        for choice in question.get("choices", [])
                    ),
                    f"Placeholder promoted-scope distractor found for {token} in {pasuk}",
                )

    def test_promoted_scope_phrase_questions_translate_cleanly_or_skip_honestly(self):
        supported = 0
        for pasuk in promoted_scope_pesukim():
            question = generate_question("phrase_translation", pasuk)
            if question.get("status") == "skipped":
                self.assertEqual(
                    question.get("reason"),
                    "No quiz-ready phrase target found in this pasuk.",
                )
                continue

            supported += 1
            answer = question.get("correct_answer", "")
            token = question.get("selected_word") or question.get("word")
            self.assertFalse(
                is_placeholder_translation(answer, token),
                f"Weak promoted-scope phrase answer for {token} in {pasuk}",
            )
            self.assertNotIn("God and ", answer)
            self.assertNotIn("the LORD and ", answer)
            self.assertNotIn("God making", answer)
            self.assertNotIn("the LORD God making", answer)

        self.assertGreaterEqual(supported, 8)

    def test_promoted_scope_translation_reviews_remain_needs_review(self):
        reviews = json.loads(
            Path("data/translation_reviews.json").read_text(encoding="utf-8")
        )["reviews"]
        promoted_pasuks = {
            "bereishis_1_31",
            "bereishis_2_4",
            "bereishis_2_7",
            "bereishis_2_8",
            "bereishis_2_9",
        }
        enriched = [
            review
            for review in reviews
            if review.get("pasuk_id") in promoted_pasuks
            and review.get("authority_source") == "local_data_enrichment"
        ]

        self.assertTrue(enriched)
        self.assertTrue(all(review.get("review_status") == "needs_review" for review in enriched))
        self.assertTrue(all(review.get("approved_context") is None for review in enriched))

    def test_build_followup_question_falls_back_when_same_question_repeats(self):
        progress = {"current_skill": "translation", "prefix_level": 1}
        question = {
            "skill": "translation",
            "pasuk": "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
            "selected_word": "בְּרֵאשִׁית",
            "question": "What does בְּרֵאשִׁית mean?",
        }
        stale_followup = {
            "skill": "translation",
            "question": "What does בְּרֵאשִׁית mean?",
            "selected_word": "בְּרֵאשִׁית",
            "correct_answer": "in the beginning",
            "choices": ["in the beginning", "created", "God", "earth"],
        }
        fallback_question = {
            "skill": "translation",
            "question": "What does בָּרָא mean?",
            "selected_word": "בָּרָא",
            "correct_answer": "created",
            "choices": ["created", "in the beginning", "earth", "light"],
        }

        with patch.object(question_flow, "analyze_generator_pasuk", return_value=[{"word": "בְּרֵאשִׁית"}]), \
             patch.object(question_flow, "generate_skill_question", return_value=stale_followup), \
             patch.object(question_flow, "generate_practice_question", return_value=dict(fallback_question)), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = streamlit_app.build_followup_question(progress, question)

        self.assertEqual(result["selected_word"], "בָּרָא")
        self.assertEqual(result["_assessment_source"], "fallback follow-up from active parsed dataset")
        self.assertEqual(result["_cache_status"], "fallback follow-up regenerated after the current error")

    def test_select_pasuk_first_question_uses_feature_fallback_instead_of_stalling(self):
        ready_rows = [
            {
                "pasuk": "לָאוֹר",
                "word": "לָאוֹר",
                "feature": "prefix",
                "prefix": "ל",
            }
        ]
        blocked_prefix_question = {
            "skill": "prefix",
            "question_type": "prefix",
            "question": "What is the prefix in לָאוֹר?",
            "selected_word": "לָאוֹר",
            "correct_answer": "ל",
            "choices": ["ל", "ב", "מ", "ו"],
            "prefix": "ל",
        }

        st.session_state.recent_features = ["prefix", "translation", "prefix", "verb", "suffix"]
        st.session_state.recent_prefixes = ["ל", "ל"]

        with patch.object(question_flow, "get_skill_ready_pasuks", return_value=ready_rows), \
             patch.object(question_flow, "generate_skill_question", return_value=dict(blocked_prefix_question)), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = streamlit_app.select_pasuk_first_question("prefix", progress={"prefix_level": 1})

        self.assertEqual(result["selected_word"], "לָאוֹר")
        self.assertEqual(
            st.session_state.feature_fallback_message,
            "Feature repetition fallback used after 10 attempts.",
        )


if __name__ == "__main__":
    unittest.main()
