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
        self.assertIn("reviewed_question_banks", manifest)
        self.assertIn("preview_only_artifacts", manifest)
        self.assertIn("review_only_artifacts", manifest)
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
        self.assertEqual(active_scope["range"]["end"], {"perek": 3, "pasuk": 24})
        self.assertEqual(active_scope["pesukim_count"], 80)
        self.assertEqual(active_scope["status"], "active")

    def test_source_corpus_metadata_tracks_prepared_local_source_boundary(self):
        source_corpus = assessment_scope.corpus_source_corpora()[0]

        self.assertEqual(source_corpus["corpus_id"], "source_bereishis_1_1_to_3_24_local")
        self.assertEqual(source_corpus["status"], "source")
        self.assertEqual(source_corpus["range"]["start"], {"perek": 1, "pasuk": 1})
        self.assertEqual(source_corpus["range"]["end"], {"perek": 3, "pasuk": 24})
        self.assertEqual(source_corpus["pesukim_count"], 80)
        self.assertEqual(
            source_corpus["source_files"],
            [
                "data/source/bereishis_1_1_to_1_30.json",
                "data/source/bereishis_1_31_to_2_9.json",
                "data/source/bereishis_2_10_to_2_17.json",
                "data/source/bereishis_2_18_to_2_25.json",
                "data/source/bereishis_3_1_to_3_8.json",
                "data/source/bereishis_3_9_to_3_16.json",
                "data/source/bereishis_3_17_to_3_24.json",
            ],
        )
        self.assertEqual(
            source_corpus["canonical_source_text"],
            {
                "file": "data/source_texts/bereishis_hebrew_menukad_taamim.tsv",
                "scope": "Bereishis 1:1-50:26",
                "sha256": "4d96c615ab63e0419bff079db250d71ea9b5de266ff9ab8d589ae80e4afd0b71",
            },
        )
        self.assertEqual(source_corpus["declared_source_range"], "1:1-3:24")

    def test_active_scope_source_corpus_id_resolves_to_matching_source_corpus(self):
        active_scope = assessment_scope.active_scope_metadata()
        source_corpus = next(
            corpus
            for corpus in assessment_scope.corpus_source_corpora()
            if corpus["corpus_id"] == active_scope["source_corpus_id"]
        )

        self.assertEqual(source_corpus["range"], active_scope["range"])
        self.assertEqual(source_corpus["pesukim_count"], active_scope["pesukim_count"])
        self.assertEqual(source_corpus["source_files"], active_scope["source_files"])

    def test_active_scope_reviewed_question_bank_metadata_matches_manifest_scope(self):
        active_scope = assessment_scope.active_scope_metadata()
        manifest = assessment_scope.load_corpus_manifest()
        manifest_bank = manifest["reviewed_question_banks"][0]
        reviewed_payload = assessment_scope.load_active_scope_reviewed_questions_data()
        reviewed_metadata = reviewed_payload["metadata"]

        self.assertEqual(manifest_bank["file"], "data/active_scope_reviewed_questions.json")
        self.assertEqual(manifest_bank["scope_id"], active_scope["scope_id"])
        self.assertEqual(manifest_bank["source_corpus_id"], active_scope["source_corpus_id"])
        self.assertEqual(manifest_bank["parsed_corpus_id"], active_scope["parsed_corpus_id"])
        self.assertEqual(manifest_bank["question_count"], len(reviewed_payload["questions"]))
        self.assertTrue(manifest_bank["runtime_active"])
        self.assertEqual(reviewed_metadata["scope_id"], active_scope["scope_id"])
        self.assertEqual(reviewed_metadata["status"], "active")
        self.assertGreater(len(reviewed_payload["questions"]), 0)
        self.assertTrue(
            all(
                question["pasuk_id"] in assessment_scope.active_pasuk_id_set()
                for question in reviewed_payload["questions"]
            )
        )

    def test_manifest_distinguishes_preview_and_review_only_artifacts_from_runtime(self):
        manifest = assessment_scope.load_corpus_manifest()

        self.assertTrue(
            all(
                artifact["status"].endswith("not_runtime_active")
                for artifact in manifest["preview_only_artifacts"]
            )
        )
        self.assertTrue(
            all(
                artifact["status"].endswith("not_runtime_active")
                for artifact in manifest["review_only_artifacts"]
            )
        )
        self.assertTrue(
            any(
                artifact["artifact_id"] == "diagnostic_preview_bereishis_1_1_to_2_3"
                for artifact in manifest["preview_only_artifacts"]
            )
        )
        self.assertTrue(
            any(
                artifact["artifact_id"] == "zekelman_standard_3_planning_and_review_materials"
                for artifact in manifest["review_only_artifacts"]
            )
        )

    def test_no_future_scope_remains_once_3_17_to_3_24_is_live(self):
        future_scopes = assessment_scope.load_corpus_manifest()["future_scopes"]

        self.assertEqual(future_scopes, [])

    def test_promoted_staged_parsed_corpus_metadata_tracks_provenance_bundle(self):
        staged_corpus = next(
            corpus
            for corpus in assessment_scope.corpus_parsed_corpora()
            if corpus["corpus_id"] == "parsed_bereishis_3_1_to_3_8_staged"
        )

        self.assertEqual(staged_corpus["status"], "active")
        self.assertEqual(staged_corpus["storage_layer"], "data_staged")
        self.assertEqual(
            staged_corpus["parsed_files"]["reviewed_questions"],
            "data/staged/parsed_bereishis_3_1_to_3_8_staged/reviewed_questions.json",
        )
        self.assertEqual(
            staged_corpus["readiness_report"],
            "data/validation/bereishis_3_1_to_3_8_readiness.json",
        )

    def test_next_staged_parsed_corpus_metadata_tracks_the_promoted_3_9_to_3_16_bundle(self):
        staged_corpus = next(
            corpus
            for corpus in assessment_scope.corpus_parsed_corpora()
            if corpus["corpus_id"] == "parsed_bereishis_3_9_to_3_16_staged"
        )

        self.assertEqual(staged_corpus["status"], "active")
        self.assertEqual(staged_corpus["storage_layer"], "data_staged")
        self.assertEqual(
            staged_corpus["parsed_files"]["parsed_pesukim"],
            "data/staged/parsed_bereishis_3_9_to_3_16_staged/parsed_pesukim.json",
        )
        self.assertEqual(
            staged_corpus["parsed_files"]["reviewed_questions"],
            "data/staged/parsed_bereishis_3_9_to_3_16_staged/reviewed_questions.json",
        )
        self.assertEqual(
            staged_corpus["readiness_report"],
            "data/validation/bereishis_3_9_to_3_16_readiness.json",
        )

    def test_promoted_3_17_to_3_24_staged_corpus_metadata_tracks_provenance_bundle(self):
        staged_corpus = next(
            corpus
            for corpus in assessment_scope.corpus_parsed_corpora()
            if corpus["corpus_id"] == "parsed_bereishis_3_17_to_3_24_staged"
        )

        self.assertEqual(staged_corpus["status"], "active")
        self.assertEqual(staged_corpus["storage_layer"], "data_staged")
        self.assertEqual(
            staged_corpus["parsed_files"]["parsed_pesukim"],
            "data/staged/parsed_bereishis_3_17_to_3_24_staged/parsed_pesukim.json",
        )
        self.assertEqual(
            staged_corpus["parsed_files"]["reviewed_questions"],
            "data/staged/parsed_bereishis_3_17_to_3_24_staged/reviewed_questions.json",
        )
        self.assertEqual(
            staged_corpus["readiness_report"],
            "data/validation/bereishis_3_17_to_3_24_readiness.json",
        )

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
        active_texts = {record.get("text") for record in assessment_scope.active_pesukim_records()}
        flow_pesukim = {flow.get("pasuk") for flow in flows}
        expected_flow_refs = {
            (2, 18),
            (2, 20),
            (2, 21),
            (2, 22),
            (2, 23),
        }
        expected_flow_texts = {
            record.get("text")
            for record in assessment_scope.active_pesukim_records()
            if (
                record.get("ref", {}).get("perek"),
                record.get("ref", {}).get("pasuk"),
            ) in expected_flow_refs
        }

        self.assertLessEqual(len(flows), active_scope["pesukim_count"])
        self.assertTrue(flow_pesukim.issubset(active_texts))
        self.assertTrue(expected_flow_texts.issubset(flow_pesukim))
        self.assertTrue(
            all(
                flow.get("source", "").startswith(f"{assessment_scope.ACTIVE_ASSESSMENT_SCOPE}:")
                for flow in flows
            )
        )


if __name__ == "__main__":
    unittest.main()
