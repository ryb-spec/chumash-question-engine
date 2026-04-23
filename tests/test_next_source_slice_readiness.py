import unittest

import assessment_scope
from corpus_metrics import evaluate_staged_corpus_readiness, load_staged_corpus_bundle
from pasuk_flow_generator import is_placeholder_translation
from torah_parser.export_bank import load_json


class NextSourceSliceReadinessTests(unittest.TestCase):
    def test_next_source_file_exists_and_matches_expected_range(self):
        source_path = assessment_scope.repo_path("data", "source", "bereishis_3_9_to_3_16.json")

        self.assertTrue(source_path.exists())
        source = load_json(source_path, {"metadata": {}, "pesukim": []})
        self.assertEqual(source["metadata"]["range"], "3:9-3:16")
        self.assertEqual(len(source["pesukim"]), 8)
        self.assertEqual(source["pesukim"][0]["perek"], 3)
        self.assertEqual(source["pesukim"][0]["pasuk"], 9)
        self.assertEqual(source["pesukim"][-1]["perek"], 3)
        self.assertEqual(source["pesukim"][-1]["pasuk"], 16)

    def test_staged_bundle_exists_for_the_next_3_9_to_3_16_chunk(self):
        bundle_dir = assessment_scope.repo_path("data", "staged", "parsed_bereishis_3_9_to_3_16_staged")

        self.assertTrue(bundle_dir.exists())
        expected_files = {
            "pesukim.json",
            "parsed_pesukim.json",
            "word_bank.json",
            "word_occurrences.json",
            "translation_reviews.json",
            "reviewed_questions.json",
        }
        self.assertEqual({path.name for path in bundle_dir.iterdir()}, expected_files)
        bundle = load_staged_corpus_bundle(bundle_dir)
        self.assertEqual(bundle["pesukim"]["metadata"]["corpus_id"], "parsed_bereishis_3_9_to_3_16_staged")
        self.assertEqual(bundle["pesukim"]["metadata"]["status"], "staged")
        self.assertEqual(bundle["pesukim"]["metadata"]["pesukim_count"], 8)
        self.assertEqual(
            bundle["pesukim"]["metadata"]["range"]["end"],
            {"sefer": "Bereishis", "perek": 3, "pasuk": 16},
        )
        self.assertEqual(assessment_scope.ACTIVE_ASSESSMENT_SCOPE, "local_parsed_bereishis_1_1_to_3_8")

    def test_readiness_report_records_the_review_needed_state_for_3_9_to_3_16(self):
        readiness_path = assessment_scope.repo_path(
            "data",
            "validation",
            "bereishis_3_9_to_3_16_readiness.json",
        )

        self.assertTrue(readiness_path.exists())
        report = load_json(readiness_path, {})
        self.assertEqual(
            report["scope_under_evaluation"]["active_runtime_scope_unchanged"],
            "local_parsed_bereishis_1_1_to_3_8",
        )
        self.assertEqual(report["readiness_recommendation"], "active_candidate")
        self.assertEqual(report["generation_summary"]["question_ready_pesukim"], 8)
        self.assertEqual(report["generation_summary"]["stable_flow_pesukim"], 8)
        self.assertEqual(report["structural_summary"]["tokens_with_placeholder_context_count"], 0)
        self.assertEqual(report["per_skill_support"]["shoresh"]["supported_pesukim"], 8)
        self.assertEqual(
            report["comparison_to_previous"]["current_readiness_recommendation"],
            "active_candidate",
        )
        self.assertEqual(
            report["comparison_to_previous"]["current_tokens_with_placeholder_context_count"],
            0,
        )
        self.assertEqual(
            report["comparison_to_previous"]["current_stable_flow_pesukim"],
            8,
        )
        self.assertEqual(
            report["comparison_to_previous"]["current_shoresh_supported_pesukim"],
            8,
        )
        self.assertTrue(report["staged_reviewed_support"]["available"])
        self.assertEqual(report["staged_reviewed_support"]["question_count"], 43)
        self.assertEqual(report["remaining_blockers"], [])
        self.assertEqual(report["diagnostic_summary"]["blocker_categories"], [])

    def test_staged_bundle_readiness_evaluation_matches_committed_report(self):
        bundle_dir = assessment_scope.repo_path("data", "staged", "parsed_bereishis_3_9_to_3_16_staged")

        metrics = evaluate_staged_corpus_readiness(bundle_dir)
        self.assertEqual(metrics["readiness_recommendation"], "active_candidate")
        self.assertEqual(metrics["structural_summary"]["pesukim_count"], 8)
        self.assertEqual(metrics["scope_under_evaluation"]["bundle_status"], "staged")
        self.assertEqual(metrics["generation_summary"]["stable_flow_pesukim"], 8)
        self.assertEqual(metrics["structural_summary"]["tokens_with_placeholder_context_count"], 0)
        self.assertEqual(metrics["per_skill_support"]["shoresh"]["supported_pesukim"], 8)
        self.assertTrue(metrics["staged_reviewed_support"]["available"])
        self.assertEqual(metrics["staged_reviewed_support"]["question_count"], 43)

    def test_staged_reviewed_support_is_present_once_the_chunk_reaches_review_needed(self):
        reviewed_path = assessment_scope.repo_path(
            "data",
            "staged",
            "parsed_bereishis_3_9_to_3_16_staged",
            "reviewed_questions.json",
        )

        self.assertTrue(reviewed_path.exists())
        payload = load_json(reviewed_path, {})
        self.assertEqual(payload["metadata"]["corpus_id"], "parsed_bereishis_3_9_to_3_16_staged")
        self.assertEqual(
            payload["metadata"]["lane_counts"],
            {"translation": 17, "shoresh": 5, "tense": 5, "affix": 8, "role": 8},
        )
        self.assertEqual(
            payload["metadata"]["skill_counts"],
            {
                "translation": 9,
                "shoresh": 5,
                "identify_tense": 5,
                "identify_prefix_meaning": 4,
                "identify_pronoun_suffix": 4,
                "phrase_translation": 8,
                "subject_identification": 3,
                "object_identification": 5,
            },
        )

    def test_staged_reviewed_support_contains_phrase_and_role_lifts_but_keeps_weak_targets_out(self):
        reviewed_path = assessment_scope.repo_path(
            "data",
            "staged",
            "parsed_bereishis_3_9_to_3_16_staged",
            "reviewed_questions.json",
        )
        payload = load_json(reviewed_path, {})
        questions = payload.get("questions", [])
        found = {
            (question.get("skill"), question.get("pasuk_id"), question.get("selected_word"), question.get("correct_answer"))
            for question in questions
            if question.get("skill") in {"phrase_translation", "subject_identification", "object_identification"}
        }
        expected = {
            ("phrase_translation", "bereishis_3_9", "וַיִּקְרָא יְהוָה אֱלֹהִים אֶל הָאָדָם", "and the LORD God called to the man"),
            ("phrase_translation", "bereishis_3_13", "הַנָּחָשׁ הִשִּׁיאַנִי", "the snake deceived me"),
            ("subject_identification", "bereishis_3_9", "יְהוָה אֱלֹהִים", "the LORD God"),
            ("subject_identification", "bereishis_3_13", "הַנָּחָשׁ", "the snake"),
            ("object_identification", "bereishis_3_15", "אֵיבָה", "enmity"),
            ("object_identification", "bereishis_3_16", "בָנִים", "children"),
        }
        self.assertTrue(expected.issubset(found))
        blocked = {
            ("phrase_translation", "bereishis_3_15", "הוּא יְשׁוּפְךָ רֹאשׁ"),
            ("phrase_translation", "bereishis_3_15", "וְאַתָּה תְּשׁוּפֶנּוּ עָקֵב"),
            ("subject_identification", "bereishis_3_15", "הוּא"),
            ("object_identification", "bereishis_3_14", "זֹּאת"),
        }
        found_brief = {
            (question.get("skill"), question.get("pasuk_id"), question.get("selected_word"))
            for question in questions
            if question.get("skill") in {"phrase_translation", "subject_identification", "object_identification"}
        }
        for item in blocked:
            self.assertNotIn(item, found_brief)

    def test_former_placeholder_context_blockers_now_resolve_to_non_placeholder_translations(self):
        parsed_path = assessment_scope.repo_path(
            "data",
            "staged",
            "parsed_bereishis_3_9_to_3_16_staged",
            "parsed_pesukim.json",
        )
        parsed_payload = load_json(parsed_path, {"parsed_pesukim": []})
        placeholder_targets = {
            "צִוִּיתִיךָ",
            "אֲכָל",
            "הִשִּׁיאַנִי",
            "יְשׁוּפְךָ",
            "תְּשׁוּפֶנּוּ",
        }
        found = {}

        for record in parsed_payload.get("parsed_pesukim", []):
            for token_record in record.get("token_records", []):
                surface = token_record.get("surface")
                if surface not in placeholder_targets:
                    continue
                found[surface] = token_record.get("selected_analysis", {}).get("translation_context")

        self.assertEqual(set(found.keys()), placeholder_targets)
        self.assertTrue(all(not is_placeholder_translation(value, token) for token, value in found.items()))


if __name__ == "__main__":
    unittest.main()
