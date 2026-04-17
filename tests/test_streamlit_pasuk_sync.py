import unittest
from html import escape
from unittest.mock import patch

import streamlit as st

import streamlit_app
from assessment_scope import active_pesukim_records


class StreamlitPasukSyncTests(unittest.TestCase):
    def setUp(self):
        st.session_state.clear()
        streamlit_app.init_session_state()
        st.session_state.pasuk_view_mode = "Full pasuk view"
        st.session_state.show_nekudos = True

    def _rendered_pasuk_html(self, question):
        calls = []

        def capture_markdown(body, unsafe_allow_html=False):
            calls.append(body)

        with patch.object(streamlit_app.st, "markdown", side_effect=capture_markdown):
            streamlit_app.render_pasukh_panel(question)

        pasuk_calls = [body for body in calls if "pasuk-box" in body]
        self.assertEqual(len(pasuk_calls), 1)
        return pasuk_calls[0]

    def test_advancing_question_updates_displayed_pasuk(self):
        records = active_pesukim_records()
        first_pasuk = records[0]["text"]
        second_pasuk = records[1]["text"]

        first_question = {
            "question_type": "subject_identification",
            "pasuk": first_pasuk,
            "source": "test:first",
        }
        second_question = {
            "question_type": "subject_identification",
            "pasuk": second_pasuk,
            "source": "test:second",
        }

        streamlit_app.set_question(first_question)
        first_html = self._rendered_pasuk_html(st.session_state.current_question)
        self.assertIn(escape(streamlit_app.menukad_text(first_pasuk)), first_html)

        streamlit_app.set_question(second_question)
        second_html = self._rendered_pasuk_html(st.session_state.current_question)

        self.assertIn(escape(streamlit_app.menukad_text(second_pasuk)), second_html)
        self.assertNotIn(escape(streamlit_app.menukad_text(first_pasuk)), second_html)


if __name__ == "__main__":
    unittest.main()
