import unittest
from contextlib import contextmanager
from unittest.mock import patch

import streamlit as st

import streamlit_app
from assessment_scope import active_pesukim_records


@contextmanager
def _fake_expander(*args, **kwargs):
    yield


class StreamlitCandidateQualityTests(unittest.TestCase):
    def setUp(self):
        st.session_state.clear()
        streamlit_app.init_session_state()
        st.session_state.show_nekudos = True
        st.session_state.pasuk_view_mode = "Full pasuk view"

    def test_clearer_candidate_beats_weaker_but_valid_one(self):
        clear_row = {
            "pasuk": "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
            "word": "בָּרָא",
            "question": {
                "id": "clear",
                "skill": "translation",
                "question_type": "translation",
                "question": "What does בָּרָא mean?",
                "selected_word": "בָּרָא",
                "correct_answer": "created",
                "choices": ["created", "light", "earth", "water"],
                "pasuk": "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
            },
        }
        weak_row = {
            "pasuk": "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
            "word": "בָּרָא",
            "question": {
                "id": "weak",
                "skill": "translation",
                "question_type": "translation",
                "question": "What does בָּרָא mean?",
                "selected_word": "בָּרָא",
                "correct_answer": "created",
                "choices": ["created", "created one", "created now", "create"],
                "pasuk": "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
            },
        }

        clear_breakdown = streamlit_app.candidate_quality_breakdown(
            clear_row,
            recent_pesukim=[],
            recent_words=[],
            recent_questions=[],
            progress={},
            adaptive_context={},
        )
        weak_breakdown = streamlit_app.candidate_quality_breakdown(
            weak_row,
            recent_pesukim=[],
            recent_words=[],
            recent_questions=[],
            progress={},
            adaptive_context={},
        )

        selected = streamlit_app.choose_weighted_pasuk_question(
            [weak_row, clear_row],
            recent_pesukim=[],
            recent_words=[],
            progress={},
            adaptive_context={},
            recent_questions=[],
        )

        self.assertEqual(selected["question"]["id"], "clear")
        self.assertGreater(clear_breakdown["distractor_separation"], weak_breakdown["distractor_separation"])

    def test_simple_morphology_question_stays_compact(self):
        question = {
            "skill": "identify_prefix_meaning",
            "question_type": "prefix_level_3_apply_prefix_meaning",
            "question": "What does לָאוֹר mean?",
            "selected_word": "לָאוֹר",
            "correct_answer": "to / for light",
            "pasuk": "וַיַּבְדֵּל אֱלֹקִים בֵּין הָאוֹר וּבֵין הַחֹשֶׁךְ",
        }

        policy = streamlit_app.display_context_policy(question)

        self.assertEqual(policy["mode"], "compact")
        self.assertEqual(policy["reason"], "word_level_question")
        self.assertTrue(streamlit_app.uses_compact_pasuk_context(question))

    def test_contextual_question_still_uses_full_pasuk(self):
        question = {
            "skill": "subject_identification",
            "question_type": "subject_identification",
            "question": "Who is doing the action in בָּרָא?",
            "selected_word": "אֱלֹקִים",
            "correct_answer": "אֱלֹקִים",
            "pasuk": "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
        }

        policy = streamlit_app.display_context_policy(question)

        self.assertEqual(policy["mode"], "full")
        self.assertEqual(policy["reason"], "surrounding_context_required")
        self.assertFalse(streamlit_app.uses_compact_pasuk_context(question))

    def test_compact_context_keeps_question_render_priority(self):
        question = {
            "id": "quality-q1",
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
            "pasuk": "וַיַּבְדֵּל אֱלֹקִים בֵּין הָאוֹר וּבֵין הַחֹשֶׁךְ",
        }
        progress = {"standards": {"PR": 70}, "xp": {"PR": 10}, "current_skill": "identify_prefix_meaning"}
        events = []
        st.session_state.answered = False

        def capture_markdown(body, **kwargs):
            events.append(("markdown", body))

        with patch.object(streamlit_app.st, "markdown", side_effect=capture_markdown), \
             patch.object(streamlit_app.st, "radio", return_value=None), \
             patch.object(streamlit_app.st, "button", return_value=False), \
             patch.object(streamlit_app.st, "progress"), \
             patch.object(streamlit_app.st, "expander", _fake_expander), \
             patch.object(streamlit_app, "render_enter_key_handler"):
            streamlit_app.render_question(question, progress, "candidate_quality")

        compact_index = next(
            index for index, event in enumerate(events) if event[0] == "markdown" and "compact-context" in event[1]
        )
        compact_markup = next(
            event[1] for event in events if event[0] == "markdown" and "compact-context" in event[1]
        )
        question_index = next(
            index for index, event in enumerate(events) if event[0] == "markdown" and "question-card" in event[1]
        )

        self.assertLess(compact_index, question_index)
        self.assertIn("target-word", compact_markup)
        self.assertNotIn("context-snippet", compact_markup)
        self.assertNotIn(question["pasuk"], compact_markup)

    def test_pre_serve_validation_rejects_trivial_duplicate_choice_text(self):
        record = active_pesukim_records()[0]
        question = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does בָּרָא mean?",
            "selected_word": "בָּרָא",
            "word": "בָּרָא",
            "correct_answer": "created",
            "choices": ["created", "Created", "light", "earth"],
            "pasuk": record["text"],
        }

        validation = streamlit_app.validate_question_for_serve(
            question,
            validation_path="candidate_quality_test",
            trusted_active_scope=True,
        )

        self.assertFalse(validation["valid"])
        self.assertIn("duplicate_distractors", validation["rejection_codes"])
        self.assertIn("ambiguous_answer_key", validation["rejection_codes"])

    def test_candidate_quality_penalizes_duplicate_feel_translation_meaning(self):
        recent_questions = [
            streamlit_app.question_signature(
                {
                    "skill": "translation",
                    "question_type": "translation",
                    "question": "What does אֶרֶץ mean?",
                    "selected_word": "אֶרֶץ",
                    "word": "אֶרֶץ",
                    "correct_answer": "earth",
                    "choices": ["earth", "light", "water", "sky"],
                    "pasuk": "מקור א",
                }
            )
        ]
        repeated_meaning = {
            "pasuk": "מקור ב",
            "word": "הָאָרֶץ",
            "question": {
                "skill": "translation",
                "question_type": "translation",
                "question": "What does הָאָרֶץ mean?",
                "selected_word": "הָאָרֶץ",
                "word": "הָאָרֶץ",
                "correct_answer": "the earth",
                "choices": ["the earth", "the light", "the water", "the sky"],
                "pasuk": "מקור ב",
            },
        }
        fresh_meaning = {
            "pasuk": "מקור ג",
            "word": "אוֹר",
            "question": {
                "skill": "translation",
                "question_type": "translation",
                "question": "What does אוֹר mean?",
                "selected_word": "אוֹר",
                "word": "אוֹר",
                "correct_answer": "light",
                "choices": ["light", "earth", "water", "sky"],
                "pasuk": "מקור ג",
            },
        }

        repeated_breakdown = streamlit_app.candidate_quality_breakdown(
            repeated_meaning,
            recent_pesukim=[],
            recent_words=[],
            recent_questions=recent_questions,
            progress={},
            adaptive_context={},
        )
        fresh_breakdown = streamlit_app.candidate_quality_breakdown(
            fresh_meaning,
            recent_pesukim=[],
            recent_words=[],
            recent_questions=recent_questions,
            progress={},
            adaptive_context={},
        )

        self.assertLess(repeated_breakdown["novelty"], fresh_breakdown["novelty"])


if __name__ == "__main__":
    unittest.main()
