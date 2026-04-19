import unittest

import streamlit as st

import streamlit_app
from assessment_scope import ACTIVE_ASSESSMENT_SCOPE, active_pasuk_text_set


def reset_streamlit_runtime_state():
    st.session_state.clear()
    for cached in (
        streamlit_app.load_pasuk_flows,
        streamlit_app.get_skill_ready_pasuks,
    ):
        cached.clear()
    streamlit_app.init_session_state()


class StreamlitModesSmokeTests(unittest.TestCase):
    def test_learn_mode_uses_only_active_parsed_pesukim(self):
        reset_streamlit_runtime_state()

        question = streamlit_app.generate_mastery_question(
            {"current_skill": "translation"}
        )

        self.assertIsNotNone(question)
        self.assertIn(question["pasuk"], active_pasuk_text_set())

    def test_practice_mode_uses_only_active_parsed_pesukim(self):
        reset_streamlit_runtime_state()

        question = streamlit_app.generate_practice_question("translation")

        self.assertIsNotNone(question)
        self.assertIn(question["pasuk"], active_pasuk_text_set())

    def test_pasuk_flow_uses_only_active_parsed_pesukim(self):
        reset_streamlit_runtime_state()

        flows = streamlit_app.load_pasuk_flows()

        self.assertEqual(len(flows), 40)
        self.assertTrue(all(flow["pasuk"] in active_pasuk_text_set() for flow in flows))
        self.assertTrue(
            all(
                flow.get("source", "").startswith(f"{ACTIVE_ASSESSMENT_SCOPE}:")
                for flow in flows
            )
        )


if __name__ == "__main__":
    unittest.main()
