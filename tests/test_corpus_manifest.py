import unittest

import assessment_scope
import streamlit_app


def reset_manifest_runtime_state():
    assessment_scope.load_corpus_manifest.cache_clear()
    assessment_scope.load_active_pesukim_data.cache_clear()
    assessment_scope.load_active_parsed_pesukim_data.cache_clear()
    assessment_scope._active_parsed_pesukim_by_text.cache_clear()
    assessment_scope.active_pasuk_text_set.cache_clear()
    streamlit_app.load_pasuk_flows.clear()


class CorpusManifestTests(unittest.TestCase):
    def setUp(self):
        reset_manifest_runtime_state()

    def test_corpus_manifest_loads_correctly(self):
        manifest = assessment_scope.load_corpus_manifest()

        self.assertIn("metadata", manifest)
        self.assertIn("source_corpora", manifest)
        self.assertIn("parsed_corpora", manifest)
        self.assertIn("scopes", manifest)
        self.assertIn("future_scopes", manifest)
        self.assertEqual(
            tuple(manifest["metadata"]["status_values"]),
            assessment_scope.CORPUS_STATUS_VALUES,
        )

    def test_active_scope_resolves_correctly_from_manifest(self):
        active_scope = assessment_scope.active_scope_metadata()

        self.assertEqual(active_scope["scope_id"], assessment_scope.ACTIVE_ASSESSMENT_SCOPE)
        self.assertEqual(active_scope["status"], "active")
        self.assertTrue(active_scope["supported_runtime"])

    def test_scope_metadata_includes_sefer_range_pesukim_count_status(self):
        active_scope = assessment_scope.active_scope_metadata()

        self.assertEqual(active_scope["sefer"], "Bereishis")
        self.assertEqual(active_scope["range"]["start"], {"perek": 1, "pasuk": 1})
        self.assertEqual(active_scope["range"]["end"], {"perek": 2, "pasuk": 9})
        self.assertEqual(active_scope["pesukim_count"], 40)
        self.assertEqual(active_scope["status"], "active")

    def test_source_corpus_metadata_matches_expanded_local_source_boundary(self):
        source_corpus = assessment_scope.corpus_source_corpora()[0]

        self.assertEqual(source_corpus["corpus_id"], "source_bereishis_1_1_to_2_9_local")
        self.assertEqual(source_corpus["status"], "source")
        self.assertEqual(source_corpus["range"]["start"], {"perek": 1, "pasuk": 1})
        self.assertEqual(source_corpus["range"]["end"], {"perek": 2, "pasuk": 9})
        self.assertEqual(source_corpus["pesukim_count"], 40)
        self.assertEqual(
            source_corpus["source_files"],
            [
                "data/source/bereishis_1_1_to_1_30.json",
                "data/source/bereishis_1_31_to_2_9.json",
            ],
        )
        self.assertEqual(source_corpus["declared_source_range"], "1:1-2:9")

    def test_legacy_status_aliases_normalize_to_canonical_lifecycle_states(self):
        self.assertEqual(assessment_scope.normalize_corpus_status("experimental"), "source")
        self.assertEqual(assessment_scope.normalize_corpus_status("parsed"), "staged")
        self.assertEqual(assessment_scope.normalize_corpus_status("reviewed"), "review_needed")
        self.assertEqual(assessment_scope.normalize_corpus_status("active_candidate"), "active_candidate")
        self.assertEqual(assessment_scope.normalize_corpus_status("active"), "active")

    def test_active_runtime_contract_still_points_to_valid_active_scope(self):
        contract = assessment_scope.active_runtime_contract()
        active_scope = assessment_scope.active_scope_metadata()

        self.assertEqual(contract["active_scope"], active_scope["scope_id"])
        self.assertEqual(contract["active_scope_status"], active_scope["status"])
        self.assertEqual(contract["active_pesukim_count"], active_scope["pesukim_count"])
        self.assertIn("parsed_pesukim", contract["active_dataset_paths"])

    def test_manifest_active_scope_lists_committed_parsed_analysis_artifact(self):
        active_scope = assessment_scope.active_scope_metadata()
        parsed_files = active_scope.get("parsed_files", {})

        self.assertEqual(parsed_files.get("parsed_pesukim"), "data/parsed_pesukim.json")
        self.assertTrue(assessment_scope.ACTIVE_PARSED_ANALYSIS_PATH.exists())

    def test_streamlit_runtime_remains_compatible_with_manifest_backed_scope_resolution(self):
        flows = streamlit_app.load_pasuk_flows()
        active_scope = assessment_scope.active_scope_metadata()

        self.assertEqual(len(flows), active_scope["pesukim_count"])
        self.assertTrue(
            all(
                flow.get("source", "").startswith(f"{assessment_scope.ACTIVE_ASSESSMENT_SCOPE}:")
                for flow in flows
            )
        )


if __name__ == "__main__":
    unittest.main()
