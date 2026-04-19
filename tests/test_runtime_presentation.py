import unittest
from pathlib import Path

import adaptive_engine
import skill_tracker
import streamlit_app
from runtime import presentation


class RuntimePresentationTests(unittest.TestCase):
    def test_streamlit_app_uses_shared_presentation_metadata(self):
        self.assertIs(streamlit_app.SKILL_NAMES, presentation.SKILL_NAMES)
        self.assertIs(streamlit_app.QUESTION_TYPE_NAMES, presentation.QUESTION_TYPE_NAMES)
        self.assertIs(streamlit_app.MICRO_STANDARD_NAMES, presentation.MICRO_STANDARD_NAMES)
        self.assertEqual(streamlit_app.skill_path_label("identify_prefix_meaning"), "How words are built")
        self.assertEqual(streamlit_app.QUESTION_TYPE_NAMES["role_clarity"], "Who is doing what")

    def test_error_type_classification_is_shared_and_stable(self):
        self.assertEqual(presentation.get_error_type("identify_prefix_meaning"), "prefix_error")
        self.assertEqual(streamlit_app.get_error_type("identify_suffix_meaning"), "suffix_error")
        self.assertIsNone(streamlit_app.get_error_type("translation"))

    def test_dominant_error_type_is_shared_across_modules(self):
        skill_state = {"error_counts": {"suffix_error": 1, "prefix_error": 3}}

        self.assertEqual(presentation.dominant_error_type(skill_state), "prefix_error")
        self.assertEqual(adaptive_engine.dominant_error_type(skill_state), "prefix_error")
        self.assertEqual(skill_tracker.dominant_error_type(skill_state), "prefix_error")

    def test_streamlit_app_no_longer_defines_local_label_or_error_copies(self):
        source = Path("streamlit_app.py").read_text(encoding="utf-8")

        self.assertNotIn("def get_error_type(", source)
        self.assertNotIn("SKILL_NAMES = {", source)
        self.assertNotIn("QUESTION_TYPE_NAMES = {", source)

    def test_legacy_cli_imports_shared_error_type(self):
        source = Path("run_quiz.py").read_text(encoding="utf-8")

        self.assertIn("from runtime.presentation import get_error_type", source)
        self.assertNotIn("def get_error_type(", source)


if __name__ == "__main__":
    unittest.main()
