import unittest
from pathlib import Path

import assessment_scope
import streamlit_app


class SupportedRuntimeTests(unittest.TestCase):
    def test_streamlit_supported_runtime_import_smoke(self):
        self.assertTrue(callable(streamlit_app.main))
        self.assertEqual(assessment_scope.SUPPORTED_RUNTIME_ENTRYPOINT, "streamlit_app.py")

    def test_runtime_metadata_matches_readme_entrypoint(self):
        readme = Path("README.md").read_text(encoding="utf-8")

        self.assertIn("streamlit run streamlit_app.py", readme)
        self.assertIn("run_quiz.py` is kept only as a legacy/dev CLI wrapper", readme)
        self.assertIn(assessment_scope.SUPPORTED_RUNTIME_ENTRYPOINT, readme)
        self.assertEqual(
            assessment_scope.active_runtime_contract()["runtime_entrypoint"],
            assessment_scope.SUPPORTED_RUNTIME_ENTRYPOINT,
        )

    def test_readme_and_agents_agree_on_runtime_truth(self):
        agents = Path("AGENTS.md").read_text(encoding="utf-8")

        self.assertIn("`streamlit_app.py` - supported live quiz UI/runtime.", agents)
        self.assertIn("`run_quiz.py` - legacy/dev CLI wrapper.", agents)
        self.assertEqual(assessment_scope.SUPPORTED_RUNTIME_ENTRYPOINT, "streamlit_app.py")

    def test_supported_runtime_does_not_import_legacy_cli_modules(self):
        runtime_source = Path("streamlit_app.py").read_text(encoding="utf-8")

        self.assertNotIn("import run_quiz", runtime_source)
        self.assertNotIn("import question_generator", runtime_source)


if __name__ == "__main__":
    unittest.main()
