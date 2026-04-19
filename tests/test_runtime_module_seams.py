import unittest
from pathlib import Path


HELPER_MODULES = (
    "runtime/question_flow.py",
    "runtime/session_state.py",
    "runtime/mode_handlers.py",
    "ui/render_question.py",
    "ui/render_feedback.py",
)


class RuntimeModuleSeamTests(unittest.TestCase):
    def test_helper_modules_do_not_back_import_streamlit_app(self):
        for relative_path in HELPER_MODULES:
            source = Path(relative_path).read_text(encoding="utf-8")
            self.assertNotIn("import streamlit_app as app", source, relative_path)
            self.assertNotIn("from streamlit_app import", source, relative_path)


if __name__ == "__main__":
    unittest.main()
