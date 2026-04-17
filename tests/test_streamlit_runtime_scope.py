import unittest

import streamlit as st

import streamlit_app
from assessment_scope import (
    ACTIVE_ASSESSMENT_SCOPE,
    SUPPORTED_PRACTICE_TYPES,
    SUPPORTED_RUNTIME_ENTRYPOINT,
    SUPPORTED_RUNTIME_NAME,
    active_pasuk_text_set,
    active_pasuk_texts,
    active_runtime_contract,
    is_active_pasuk_text,
)


def reset_streamlit_runtime_state():
    st.session_state.clear()
    for cached in (
        streamlit_app.load_pasuk_flows,
        streamlit_app.get_skill_ready_pasuks,
    ):
        cached.clear()


class StreamlitRuntimeScopeTests(unittest.TestCase):
    def test_active_runtime_contract_metadata(self):
        contract = active_runtime_contract()

        self.assertEqual(contract["supported_runtime"], SUPPORTED_RUNTIME_NAME)
        self.assertEqual(SUPPORTED_RUNTIME_NAME, "streamlit_app")
        self.assertEqual(contract["runtime_entrypoint"], SUPPORTED_RUNTIME_ENTRYPOINT)
        self.assertEqual(SUPPORTED_RUNTIME_ENTRYPOINT, "streamlit_app.py")
        self.assertEqual(contract["supported_practice_types"], SUPPORTED_PRACTICE_TYPES)
        self.assertEqual(
            SUPPORTED_PRACTICE_TYPES,
            ("Learn Mode", "Practice Mode", "Pasuk Flow"),
        )
        self.assertEqual(contract["active_scope"], ACTIVE_ASSESSMENT_SCOPE)
        self.assertEqual(contract["active_pesukim_count"], 20)

    def test_active_pasuk_helpers_match_active_dataset(self):
        pasuk_texts = active_pasuk_texts()
        pasuk_text_set = active_pasuk_text_set()

        self.assertEqual(len(pasuk_texts), 20)
        self.assertEqual(len(pasuk_text_set), len(pasuk_texts))
        self.assertTrue(all(is_active_pasuk_text(text) for text in pasuk_texts))

    def test_legacy_static_bank_helpers_are_removed_from_supported_runtime(self):
        reset_streamlit_runtime_state()

        self.assertFalse(hasattr(streamlit_app, "load_questions"))
        self.assertFalse(hasattr(streamlit_app, "render_standard_mode"))
        self.assertFalse(hasattr(streamlit_app, "choose_question"))


if __name__ == "__main__":
    unittest.main()
