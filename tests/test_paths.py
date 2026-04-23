import os
import unittest
import uuid
from pathlib import Path

import assessment_scope
import pasuk_flow_generator
import progress_store
import streamlit_app


class PathResolutionTests(unittest.TestCase):
    def test_legacy_preview_artifacts_live_outside_repo_root(self):
        self.assertEqual(
            assessment_scope.LEGACY_QUESTIONS_PATH,
            assessment_scope.PREVIEW_ARTIFACTS_DIR / "questions.json",
        )
        self.assertEqual(
            assessment_scope.LEGACY_PASUK_FLOW_PREVIEW_PATH,
            assessment_scope.PREVIEW_ARTIFACTS_DIR / "pasuk_flow_questions.json",
        )
        self.assertTrue(assessment_scope.LEGACY_QUESTIONS_PATH.is_absolute())
        self.assertTrue(assessment_scope.LEGACY_PASUK_FLOW_PREVIEW_PATH.is_absolute())
        self.assertTrue(assessment_scope.LEGACY_QUESTIONS_PATH.exists())
        self.assertTrue(assessment_scope.LEGACY_PASUK_FLOW_PREVIEW_PATH.exists())
        self.assertFalse(assessment_scope.repo_path("questions.json").exists())
        self.assertFalse(assessment_scope.repo_path("pasuk_flow_questions.json").exists())

    def test_active_runtime_data_resolution_works_from_non_repo_cwd(self):
        original_cwd = Path.cwd()
        try:
            os.chdir(assessment_scope.REPO_ROOT.parent)
            assessment_scope.load_active_pesukim_data.cache_clear()
            assessment_scope.load_active_parsed_pesukim_data.cache_clear()
            assessment_scope._active_parsed_pesukim_by_text.cache_clear()
            streamlit_app.load_pasuk_flows.clear()

            pesukim = assessment_scope.load_active_pesukim_data()
            parsed_pesukim = assessment_scope.load_active_parsed_pesukim_data()
            flows = streamlit_app.load_pasuk_flows()
            active_texts = {record.get("text") for record in pesukim.get("pesukim", [])}
            flow_pesukim = {flow.get("pasuk") for flow in flows}
            expected_flow_refs = {(2, 18), (2, 20), (2, 21), (2, 22), (2, 23)}
            expected_flow_texts = {
                record.get("text")
                for record in pesukim.get("pesukim", [])
                if (
                    record.get("ref", {}).get("perek"),
                    record.get("ref", {}).get("pasuk"),
                ) in expected_flow_refs
            }

            self.assertEqual(len(pesukim.get("pesukim", [])), 64)
            self.assertEqual(len(parsed_pesukim.get("parsed_pesukim", [])), 64)
            self.assertLessEqual(len(flows), 64)
            self.assertTrue(flow_pesukim.issubset(active_texts))
            self.assertTrue(expected_flow_texts.issubset(flow_pesukim))
        finally:
            os.chdir(original_cwd)

    def test_generator_and_runtime_resolve_active_dataset_paths_consistently(self):
        self.assertTrue(assessment_scope.ACTIVE_PARSED_PESUKIM_PATH.is_absolute())
        self.assertTrue(assessment_scope.ACTIVE_PARSED_ANALYSIS_PATH.is_absolute())
        self.assertTrue(assessment_scope.ACTIVE_WORD_BANK_PATH.is_absolute())
        self.assertTrue(assessment_scope.ACTIVE_PARSED_ANALYSIS_PATH.exists())
        self.assertEqual(pasuk_flow_generator.WORD_BANK_PATH, assessment_scope.ACTIVE_WORD_BANK_PATH)
        self.assertEqual(streamlit_app.WORD_BANK_PATH, assessment_scope.ACTIVE_WORD_BANK_PATH)
        self.assertEqual(progress_store.UNIFIED_PROGRESS_PATH, assessment_scope.repo_path("progress.json"))

    def test_unified_progress_round_trip_works_from_different_cwd(self):
        progress_path = assessment_scope.repo_path(f"path_test_progress_{uuid.uuid4().hex}.json")
        legacy_path = assessment_scope.repo_path(f"path_test_skill_{uuid.uuid4().hex}.json")
        original_cwd = Path.cwd()
        try:
            os.chdir(assessment_scope.REPO_ROOT.parent)
            state = progress_store.default_progress_state()
            state["words"]["בְּרֵאשִׁית"] = 25
            progress_store.save_progress_state(state, progress_path)
            reloaded = progress_store.load_progress_state(progress_path, legacy_path)

            self.assertEqual(reloaded["words"]["בְּרֵאשִׁית"], 25)
            self.assertEqual(reloaded["schema_version"], progress_store.SCHEMA_VERSION)
        finally:
            os.chdir(original_cwd)
            progress_path.unlink(missing_ok=True)
            legacy_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
