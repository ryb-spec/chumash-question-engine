import unittest
from unittest.mock import patch

import streamlit as st

import runtime.question_flow as question_flow
import runtime.session_state as session_state
import streamlit_app
from assessment_scope import ACTIVE_ASSESSMENT_SCOPE, active_pesukim_records
from pasuk_flow_generator import generate_pasuk_flow


def reset_runtime_state():
    st.session_state.clear()
    for cached in (
        streamlit_app.load_pasuk_flows,
        streamlit_app.get_skill_ready_pasuks,
    ):
        cached.clear()
    question_flow.get_skill_ready_pasuks.clear()
    streamlit_app.init_session_state()


def active_ref_by_text():
    return {
        record["text"]: (record["ref"]["perek"], record["ref"]["pasuk"])
        for record in active_pesukim_records()
    }


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


class StreamlitRuntimeCharacterizationTests(unittest.TestCase):
    def setUp(self):
        reset_runtime_state()

    def test_teacher_pilot_monitor_uses_passed_progress_for_unlocks(self):
        progress = {"current_skill": "translation", "skills": {"translation": {}}}
        review_export = {"sessions": [], "flagged_review_queue": [], "summary": {}}

        with patch.object(streamlit_app, "build_pilot_review_export", return_value=review_export), \
             patch.object(streamlit_app, "current_session_review", return_value=None), \
             patch.object(streamlit_app, "render_unlocks") as mock_render_unlocks:
            streamlit_app.render_teacher_pilot_monitor(progress)

        mock_render_unlocks.assert_called_once_with(progress)

    def test_pasuk_flow_covers_exact_active_runtime_scope(self):
        flows = streamlit_app.load_pasuk_flows()
        ref_lookup = active_ref_by_text()

        flow_refs = {ref_lookup[flow["pasuk"]] for flow in flows}
        active_refs = {
            (record["ref"]["perek"], record["ref"]["pasuk"])
            for record in active_pesukim_records()
        }
        partial_support_refs = {(2, 11), (2, 12), (2, 13), (2, 14)}

        self.assertEqual(len(flows), 44)
        self.assertTrue(flow_refs.issubset(active_refs))
        self.assertEqual(active_refs - flow_refs, partial_support_refs)
        self.assertTrue(
            all(flow.get("source", "").startswith(f"{ACTIVE_ASSESSMENT_SCOPE}:") for flow in flows)
        )

    def test_followup_fallback_after_error_changes_prompt_but_keeps_same_pasuk(self):
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
            "pasuk": question["pasuk"],
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

        self.assertEqual(result["pasuk"], question["pasuk"])
        self.assertNotEqual(result["question"], question["question"])
        self.assertEqual(result["selected_word"], "בָּרָא")
        self.assertEqual(result["_assessment_source"], "fallback follow-up from active parsed dataset")

    def test_generate_mastery_question_respects_reteach_preferred_pasuk(self):
        records = active_pesukim_records()
        preferred_pasuk = records[0]["text"]
        other_pasuk = records[1]["text"]
        st.session_state.pending_adaptive_context = {
            "selection_mode": "reteach",
            "preferred_pasuk": preferred_pasuk,
        }

        question_by_pasuk = {
            preferred_pasuk: {
                "skill": "translation",
                "question_type": "translation",
                "question": "What does בְּרֵאשִׁית mean?",
                "selected_word": "בְּרֵאשִׁית",
                "correct_answer": "in the beginning",
                "choices": ["in the beginning", "created", "God", "earth"],
                "pasuk": preferred_pasuk,
            },
            other_pasuk: {
                "skill": "translation",
                "question_type": "translation",
                "question": "What does בָּרָא mean?",
                "selected_word": "בָּרָא",
                "correct_answer": "created",
                "choices": ["created", "in the beginning", "God", "earth"],
                "pasuk": other_pasuk,
            },
        }

        def fake_generate_skill_question(skill, candidate_source, **kwargs):
            return dict(question_by_pasuk[candidate_source])

        with patch.object(question_flow, "get_skill_ready_pasuks", return_value=[{"pasuk": preferred_pasuk}, {"pasuk": other_pasuk}]), \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(question_flow, "generate_skill_question", side_effect=fake_generate_skill_question), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = streamlit_app.generate_mastery_question({"current_skill": "translation", "prefix_level": 1})

        self.assertEqual(result["pasuk"], preferred_pasuk)
        self.assertEqual(st.session_state.pending_adaptive_context, {})

    def test_submit_then_transition_to_next_question_clears_feedback_state(self):
        question = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does בָּרָא mean?",
            "selected_word": "בָּרָא",
            "correct_answer": "created",
            "choices": ["created", "light", "earth", "water"],
            "difficulty": 1,
            "pasuk": "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
        }
        next_question = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does אֱלֹקִים mean?",
            "selected_word": "אֱלֹקִים",
            "correct_answer": "God",
            "choices": ["God", "created", "heavens", "earth"],
            "pasuk": "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
        }
        progress = {"current_skill": "translation", "skills": {"translation": {}}, "adaptive_state": {}}
        st.session_state.practice_type = "Practice Mode"
        st.session_state.unlocked_skill_message = "Unlocked"
        st.session_state.feature_fallback_message = "Fallback"
        st.session_state.adaptive_status_message = "Status"
        st.session_state.adaptive_status_reason = "Reason"
        st.session_state.adaptive_status_level = "warning"

        with patch.object(streamlit_app, "append_attempt_log"), \
             patch.object(streamlit_app, "record_pilot_answer", return_value=None), \
             patch.object(streamlit_app, "record_answer", return_value={"skill_state": {"point_change": "+0"}}), \
             patch.object(streamlit_app, "save_progress"), \
             patch.object(streamlit_app, "update_word_skill_score"), \
             patch.object(streamlit_app.st, "rerun"):
            streamlit_app.handle_answer("created", question, progress)

            self.assertTrue(st.session_state.answered)
            self.assertEqual(st.session_state.selected_answer, "created")
            self.assertEqual(st.session_state.last_skill_state, {"point_change": "+0"})

            streamlit_app.transition_to_question(next_question)

        self.assertEqual(st.session_state.current_question, next_question)
        self.assertFalse(st.session_state.answered)
        self.assertIsNone(st.session_state.selected_answer)
        self.assertIsNone(st.session_state.last_skill_state)
        self.assertEqual(st.session_state.unlocked_skill_message, "")
        self.assertEqual(st.session_state.feature_fallback_message, "")
        self.assertEqual(st.session_state.adaptive_status_message, "")
        self.assertEqual(st.session_state.adaptive_status_reason, "")
        self.assertEqual(st.session_state.adaptive_status_level, "info")

    def test_promoted_scope_flows_still_suppress_duplicate_prompts(self):
        for pasuk in promoted_scope_pesukim():
            flow = generate_pasuk_flow(pasuk)
            prompts = [question.get("question") for question in flow.get("questions", [])]
            self.assertEqual(
                len(prompts),
                len(set(prompts)),
                f"Repeated prompt found in promoted flow for {pasuk}",
            )


if __name__ == "__main__":
    unittest.main()
