import unittest
from pathlib import Path
from unittest.mock import patch
import uuid

import streamlit as st

import progress_store
import streamlit_app


class ProgressStoreTests(unittest.TestCase):
    def temp_path(self, prefix):
        return Path(f"{prefix}_{uuid.uuid4().hex}.json")

    def test_load_progress_state_from_fresh_state(self):
        progress_path = self.temp_path("progress_store_test_progress")
        legacy_path = self.temp_path("progress_store_test_skill")
        try:
            state = progress_store.load_progress_state(progress_path, legacy_path)

            self.assertEqual(state["schema_version"], progress_store.SCHEMA_VERSION)
            self.assertEqual(state["current_skill"], "identify_prefix_meaning")
            self.assertEqual(state["skills"], {})
            self.assertEqual(state["word_exposure"], {})
            self.assertTrue(progress_path.exists())
        finally:
            progress_path.unlink(missing_ok=True)
            legacy_path.unlink(missing_ok=True)

    def test_record_answer_updates_unified_state(self):
        progress = progress_store.default_progress_state()
        question = {
            "word": "בְּרֵאשִׁית",
            "selected_word": "בְּרֵאשִׁית",
            "standard": "WM",
            "micro_standard": "WM1",
            "skill": "translation",
            "correct_answer": "in the beginning",
        }

        result = progress_store.record_answer(progress, question, True)

        self.assertEqual(result["progress"]["words"]["בְּרֵאשִׁית"], 10)
        self.assertEqual(result["progress"]["standards"]["WM"], 10)
        self.assertEqual(result["progress"]["micro_standards"]["WM1"], 10)
        self.assertEqual(result["progress"]["xp"]["WM"], 15)
        self.assertIn("translation", result["progress"]["skills"])
        self.assertIn("בְּרֵאשִׁית", result["progress"]["word_exposure"])
        self.assertEqual(result["skill_state"]["score"], 5)
        self.assertEqual(result["word_state"]["seen"], 1)

    def test_persist_and_reload_without_drift(self):
        progress_path = self.temp_path("progress_store_test_progress")
        legacy_path = self.temp_path("progress_store_test_skill")
        try:
            state = progress_store.default_progress_state()
            state["words"]["בְּרֵאשִׁית"] = 20
            state["skills"]["translation"] = {
                "score": 15,
                "correct_count": 3,
                "incorrect_count": 0,
                "current_streak": 3,
                "best_streak": 3,
                "challenge_streak": 0,
                "last_12_results": [True, True, True],
                "error_counts": {},
                "mastered": False,
                "last_point_change": "+5",
            }
            progress_store.save_progress_state(state, progress_path)

            reloaded = progress_store.load_progress_state(progress_path, legacy_path)

            self.assertEqual(reloaded, progress_store.ensure_progress_state(state))
        finally:
            progress_path.unlink(missing_ok=True)
            legacy_path.unlink(missing_ok=True)

    def test_streamlit_handle_answer_uses_unified_save_path_only(self):
        st.session_state.clear()
        streamlit_app.init_session_state()
        progress = progress_store.default_progress_state()
        progress["current_skill"] = "identify_prefix_meaning"
        question = {
            "word": "בְּרֵאשִׁית",
            "selected_word": "בְּרֵאשִׁית",
            "standard": "WM",
            "micro_standard": "WM1",
            "skill": "translation",
            "correct_answer": "in the beginning",
            "choices": [
                "in the beginning",
                "earth",
                "light",
                "day",
            ],
            "difficulty": 1,
        }

        with patch.object(
            streamlit_app,
            "save_progress",
            side_effect=lambda state: state,
        ) as save_progress_mock, \
             patch.object(streamlit_app, "update_word_skill_score", None), \
             patch.object(streamlit_app, "record_pilot_answer", return_value=None):
            streamlit_app.handle_answer("in the beginning", question, progress)

        self.assertEqual(save_progress_mock.call_count, 1)
        self.assertIn("translation", progress["skills"])
        self.assertIn("בְּרֵאשִׁית", progress["word_exposure"])


if __name__ == "__main__":
    unittest.main()
