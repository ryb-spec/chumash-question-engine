import re
import unittest
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

    def _plain_pasuk_html(self, rendered_html):
        return re.sub(r"<[^>]+>", "", rendered_html)

    def test_advancing_question_updates_displayed_pasuk(self):
        records = active_pesukim_records()
        first_pasuk = records[0]["text"]
        second_pasuk = records[1]["text"]

        first_question = {
            "skill": "subject_identification",
            "question_type": "subject_identification",
            "question": "Who is doing the action in בָּרָא?",
            "selected_word": "אֱלֹקִים",
            "word": "אֱלֹקִים",
            "correct_answer": "God",
            "choices": ["God", "the man", "the earth", "the light"],
            "pasuk": first_pasuk,
            "source": "test:first",
        }
        second_question = {
            "skill": "subject_identification",
            "question_type": "subject_identification",
            "question": "Who is doing the action in הָיְתָה?",
            "selected_word": "הָאָרֶץ",
            "word": "הָאָרֶץ",
            "correct_answer": "the earth",
            "choices": ["the earth", "God", "light", "water"],
            "pasuk": second_pasuk,
            "source": "test:second",
        }

        streamlit_app.set_question(first_question)
        first_html = self._rendered_pasuk_html(st.session_state.current_question)
        self.assertIn(streamlit_app.menukad_text(first_pasuk), self._plain_pasuk_html(first_html))

        streamlit_app.set_question(second_question)
        second_html = self._rendered_pasuk_html(st.session_state.current_question)

        self.assertIn(streamlit_app.menukad_text(second_pasuk), self._plain_pasuk_html(second_html))
        self.assertNotIn(streamlit_app.menukad_text(first_pasuk), self._plain_pasuk_html(second_html))

    def test_set_question_blocks_stale_mismatched_pasuk_payload(self):
        records = active_pesukim_records()
        valid_question = {
            "skill": "subject_identification",
            "question_type": "subject_identification",
            "question": "Who is doing the action in בָּרָא?",
            "selected_word": "אֱלֹקִים",
            "word": "אֱלֹקִים",
            "correct_answer": "God",
            "choices": ["God", "the man", "the earth", "the light"],
            "pasuk": records[0]["text"],
        }
        invalid_question = {
            "skill": "subject_identification",
            "question_type": "subject_identification",
            "question": "Who is doing the action in בָּרָא?",
            "selected_word": "אֱלֹקִים",
            "word": "אֱלֹקִים",
            "correct_answer": "God",
            "choices": ["God", "the man", "the earth", "the light"],
            "pasuk": records[1]["text"],
            "pasuk_ref": {"pasuk_id": records[0]["pasuk_id"], "label": "Bereishis 1:1"},
        }

        streamlit_app.set_question(valid_question)

        with self.assertRaises(ValueError):
            streamlit_app.set_question(invalid_question)

        self.assertEqual(st.session_state.current_question["pasuk"], records[0]["text"])


if __name__ == "__main__":
    unittest.main()
