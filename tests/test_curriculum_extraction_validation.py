import copy
import json
import unittest
from unittest import mock
from pathlib import Path

from scripts import validate_curriculum_extraction as validator


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "curriculum_extraction" / "curriculum_extraction_manifest.json"


def load_manifest():
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def validate_with_manifest(manifest):
    original_load_json = validator.load_json

    def side_effect(path):
        if path == validator.MANIFEST_PATH:
            return manifest
        return original_load_json(path)

    with mock.patch.object(validator, "load_json", side_effect=side_effect):
        return validator.validate_curriculum_extraction()


def load_all_sample_records():
    manifest = load_manifest()
    records = []
    for relative in manifest["sample_files"]:
        path = ROOT / relative
        records.extend(validator.load_jsonl(path))
    return records


def load_all_normalized_records():
    manifest = load_manifest()
    records = []
    for relative in validator.collect_manifest_relative_paths(manifest, "normalized_data_files"):
        path = ROOT / relative
        records.extend(validator.load_jsonl(path))
    return records


def load_all_records():
    return [*load_all_sample_records(), *load_all_normalized_records()]


def normalized_records_by_type(record_type):
    return [record for record in load_all_normalized_records() if record["record_type"] == record_type]


def normalized_records_for_batch(batch_id):
    return [record for record in load_all_normalized_records() if record["extraction_batch_id"] == batch_id]


class CurriculumExtractionValidationTests(unittest.TestCase):
    def test_validator_passes(self):
        summary = validator.validate_curriculum_extraction(check_git_diff=True)
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["normalized_record_count"], 471)
        self.assertEqual(summary["review_status_counts"]["reviewed"], 75)
        self.assertEqual(summary["review_status_counts"]["needs_review"], 426)

    def test_manifest_is_not_runtime_active(self):
        manifest = load_manifest()
        self.assertFalse(manifest["runtime_active"])
        self.assertEqual(manifest["integration_status"], "not_runtime_active")
        self.assertEqual(len(manifest.get("normalized_data_files", [])), 6)
        batches = {batch["batch_id"]: batch for batch in manifest.get("resource_batches", [])}
        self.assertIn("batch_001_cleaned_seed", batches)
        self.assertEqual(batches["batch_001_cleaned_seed"]["review_status"], "reviewed")
        self.assertEqual(batches["batch_001_cleaned_seed"]["status"], "cleaned_seed_reviewed_non_runtime")
        self.assertIn("batch_002_linear_bereishis", batches)
        self.assertEqual(batches["batch_002_linear_bereishis"]["review_status"], "needs_review")
        self.assertEqual(batches["batch_002_linear_bereishis"]["status"], "extracted_needs_review")
        self.assertEqual(
            batches["batch_002_linear_bereishis"]["raw_source_files"],
            ["data/curriculum_extraction/raw_sources/batch_002/linear_chumash_bereishis_1_6_to_2_3_cleaned.md"],
        )
        self.assertEqual(
            batches["batch_002_linear_bereishis"]["normalized_data_files"],
            ["data/curriculum_extraction/normalized/batch_002_linear_chumash_bereishis_1_6_to_2_3_pasuk_segments.jsonl"],
        )
        self.assertEqual(
            batches["batch_002_linear_bereishis"]["generated_question_preview_files"],
            ["data/curriculum_extraction/generated_questions_preview/batch_002_preview.jsonl"],
        )
        self.assertIn("batch_003_linear_bereishis_2_4_to_2_25", batches)
        self.assertEqual(batches["batch_003_linear_bereishis_2_4_to_2_25"]["review_status"], "needs_review")
        self.assertEqual(batches["batch_003_linear_bereishis_2_4_to_2_25"]["status"], "extracted_needs_review")
        self.assertEqual(
            batches["batch_003_linear_bereishis_2_4_to_2_25"]["raw_source_files"],
            ["data/curriculum_extraction/raw_sources/batch_003/linear_chumash_bereishis_2_4_to_2_25_cleaned.md"],
        )
        self.assertEqual(
            batches["batch_003_linear_bereishis_2_4_to_2_25"]["normalized_data_files"],
            ["data/curriculum_extraction/normalized/batch_003_linear_chumash_bereishis_2_4_to_2_25_pasuk_segments.jsonl"],
        )
        self.assertEqual(
            batches["batch_003_linear_bereishis_2_4_to_2_25"]["generated_question_preview_files"],
            ["data/curriculum_extraction/generated_questions_preview/batch_003_preview.jsonl"],
        )
        self.assertIn("batch_004_linear_bereishis_3_1_to_3_24", batches)
        self.assertEqual(batches["batch_004_linear_bereishis_3_1_to_3_24"]["review_status"], "reviewed")
        self.assertEqual(batches["batch_004_linear_bereishis_3_1_to_3_24"]["status"], "reviewed_for_planning_non_runtime")
        self.assertEqual(
            batches["batch_004_linear_bereishis_3_1_to_3_24"]["raw_source_files"],
            ["data/curriculum_extraction/raw_sources/batch_004/linear_chumash_bereishis_3_1_to_3_24_cleaned.md"],
        )
        self.assertEqual(
            batches["batch_004_linear_bereishis_3_1_to_3_24"]["normalized_data_files"],
            ["data/curriculum_extraction/normalized/batch_004_linear_chumash_bereishis_3_1_to_3_24_pasuk_segments.jsonl"],
        )
        self.assertEqual(
            batches["batch_004_linear_bereishis_3_1_to_3_24"]["generated_question_preview_files"],
            ["data/curriculum_extraction/generated_questions_preview/batch_004_preview.jsonl"],
        )
        self.assertEqual(
            batches["batch_004_linear_bereishis_3_1_to_3_24"]["review_artifacts"],
            [
                "data/curriculum_extraction/reports/batch_004_summary.md",
                "data/curriculum_extraction/reports/batch_004_preview_summary.md",
                "data/curriculum_extraction/reports/batch_004_manual_review_packet.md",
                "data/curriculum_extraction/reports/batch_004_review_resolution.md",
            ],
        )
        self.assertIn("batch_005_linear_bereishis_4_1_to_4_16", batches)
        self.assertEqual(batches["batch_005_linear_bereishis_4_1_to_4_16"]["review_status"], "reviewed")
        self.assertEqual(
            batches["batch_005_linear_bereishis_4_1_to_4_16"]["status"],
            "reviewed_for_planning_non_runtime",
        )
        self.assertEqual(
            batches["batch_005_linear_bereishis_4_1_to_4_16"]["raw_source_files"],
            ["data/curriculum_extraction/raw_sources/batch_005/linear_chumash_bereishis_4_1_to_4_16_cleaned.md"],
        )
        self.assertEqual(
            batches["batch_005_linear_bereishis_4_1_to_4_16"]["normalized_data_files"],
            ["data/curriculum_extraction/normalized/batch_005_linear_chumash_bereishis_4_1_to_4_16_pasuk_segments.jsonl"],
        )
        self.assertEqual(
            batches["batch_005_linear_bereishis_4_1_to_4_16"]["generated_question_preview_files"],
            ["data/curriculum_extraction/generated_questions_preview/batch_005_preview.jsonl"],
        )
        self.assertEqual(
            batches["batch_005_linear_bereishis_4_1_to_4_16"]["review_artifacts"],
            [
                "data/curriculum_extraction/reports/batch_005_summary.md",
                "data/curriculum_extraction/reports/batch_005_preview_summary.md",
                "data/curriculum_extraction/reports/batch_005_manual_review_packet.md",
                "data/curriculum_extraction/reports/batch_005_review_resolution.md",
            ],
        )

    def test_phase_1_sample_records_stay_needs_review(self):
        for record in load_all_sample_records():
            self.assertEqual(record["review_status"], "needs_review", record["id"])

    def test_batch_001_normalized_records_are_reviewed(self):
        for record in normalized_records_for_batch("batch_001_cleaned_seed"):
            self.assertEqual(record["review_status"], "reviewed", record["id"])
            self.assertEqual(record["source_trace"]["review_status"], "reviewed", record["id"])

    def test_batch_002_normalized_records_stay_needs_review(self):
        records = normalized_records_for_batch("batch_002_linear_bereishis")
        self.assertEqual(len(records), 123)
        for record in records:
            self.assertEqual(record["review_status"], "needs_review", record["id"])
            self.assertEqual(record["source_trace"]["review_status"], "needs_review", record["id"])
            self.assertEqual(record["confidence"], "low", record["id"])
            self.assertIn("hebrew_aligned_from_local_pasuk_text", record["extraction_quality_flags"], record["id"])

    def test_batch_003_normalized_records_stay_needs_review(self):
        records = normalized_records_for_batch("batch_003_linear_bereishis_2_4_to_2_25")
        self.assertEqual(len(records), 90)
        for record in records:
            self.assertEqual(record["review_status"], "needs_review", record["id"])
            self.assertEqual(record["source_trace"]["review_status"], "needs_review", record["id"])
            self.assertEqual(record["confidence"], "low", record["id"])
            self.assertIn("hebrew_aligned_from_local_pasuk_text", record["extraction_quality_flags"], record["id"])

    def test_batch_004_normalized_records_stay_needs_review(self):
        records = normalized_records_for_batch("batch_004_linear_bereishis_3_1_to_3_24")
        self.assertEqual(len(records), 119)
        for record in records:
            self.assertEqual(record["review_status"], "needs_review", record["id"])
            self.assertEqual(record["source_trace"]["review_status"], "needs_review", record["id"])
            self.assertEqual(record["confidence"], "low", record["id"])
            self.assertIn("hebrew_aligned_from_local_pasuk_text", record["extraction_quality_flags"], record["id"])

    def test_batch_005_normalized_records_stay_needs_review(self):
        records = normalized_records_for_batch("batch_005_linear_bereishis_4_1_to_4_16")
        self.assertEqual(len(records), 64)
        for record in records:
            self.assertEqual(record["review_status"], "needs_review", record["id"])
            self.assertEqual(record["source_trace"]["review_status"], "needs_review", record["id"])
            self.assertEqual(record["confidence"], "low", record["id"])
            self.assertIn("hebrew_aligned_from_local_source_block", record["extraction_quality_flags"], record["id"])

    def test_reviewed_non_runtime_batch_is_valid_when_required_review_artifacts_exist(self):
        summary = validator.validate_curriculum_extraction()
        self.assertTrue(summary["valid"], summary["errors"])

    def test_reviewed_non_runtime_batch_missing_review_artifact_fails_validation(self):
        manifest = copy.deepcopy(load_manifest())
        batch = next(
            batch
            for batch in manifest["resource_batches"]
            if batch["batch_id"] == "batch_004_linear_bereishis_3_1_to_3_24"
        )
        batch["review_artifacts"] = [
            relative
            for relative in batch["review_artifacts"]
            if relative != "data/curriculum_extraction/reports/batch_004_review_resolution.md"
        ]

        summary = validate_with_manifest(manifest)
        self.assertFalse(summary["valid"])
        self.assertIn(
            "curriculum_extraction_manifest.json: batch_004_linear_bereishis_3_1_to_3_24 "
            "reviewed_for_planning_non_runtime batches must declare review_artifact "
            "'data/curriculum_extraction/reports/batch_004_review_resolution.md'",
            summary["errors"],
        )

    def test_reviewed_non_runtime_status_does_not_imply_runtime_promotion(self):
        manifest = copy.deepcopy(load_manifest())
        batch = next(
            batch
            for batch in manifest["resource_batches"]
            if batch["batch_id"] == "batch_004_linear_bereishis_3_1_to_3_24"
        )
        batch["runtime_active"] = True

        summary = validate_with_manifest(manifest)
        self.assertFalse(summary["valid"])
        self.assertIn(
            "curriculum_extraction_manifest.json: batch_004_linear_bereishis_3_1_to_3_24 must have runtime_active=false",
            summary["errors"],
        )

    def test_no_record_is_runtime_active(self):
        for record in load_all_records():
            self.assertEqual(record["runtime_status"], "not_runtime_active", record["id"])

    def test_no_record_has_high_confidence(self):
        for record in load_all_records():
            self.assertNotEqual(record["confidence"], "high", record["id"])

    def test_batch_001_normalized_records_move_to_medium_confidence(self):
        for record in normalized_records_for_batch("batch_001_cleaned_seed"):
            self.assertEqual(record["confidence"], "medium", record["id"])

    def test_every_record_has_source_package_and_source_trace(self):
        for record in load_all_records():
            self.assertIn("source_package_id", record)
            self.assertTrue(record["source_package_id"])
            self.assertIn("source_trace", record)
            self.assertIsInstance(record["source_trace"], dict)

    def test_batch_001_records_have_manual_review_confirmed_flag(self):
        for record in normalized_records_for_batch("batch_001_cleaned_seed"):
            self.assertIn("manual_review_confirmed", record["extraction_quality_flags"], record["id"])
            self.assertNotIn("requires_manual_review", record["extraction_quality_flags"], record["id"])

    def test_batch_002_pasuk_segments_match_expected_count(self):
        records = normalized_records_for_batch("batch_002_linear_bereishis")
        pasuk_segments = [record for record in records if record["record_type"] == "pasuk_segment"]
        self.assertEqual(len(pasuk_segments), 123)
        self.assertTrue(all(record["source_package_id"] == "linear_chumash_translation_most_parshiyos_in_torah" for record in pasuk_segments))

    def test_batch_003_pasuk_segments_match_expected_count(self):
        records = normalized_records_for_batch("batch_003_linear_bereishis_2_4_to_2_25")
        pasuk_segments = [record for record in records if record["record_type"] == "pasuk_segment"]
        self.assertEqual(len(pasuk_segments), 90)
        self.assertTrue(all(record["source_package_id"] == "linear_chumash_translation_most_parshiyos_in_torah" for record in pasuk_segments))

    def test_batch_004_pasuk_segments_match_expected_count(self):
        records = normalized_records_for_batch("batch_004_linear_bereishis_3_1_to_3_24")
        pasuk_segments = [record for record in records if record["record_type"] == "pasuk_segment"]
        self.assertEqual(len(pasuk_segments), 119)
        self.assertTrue(all(record["source_package_id"] == "linear_chumash_translation_most_parshiyos_in_torah" for record in pasuk_segments))

    def test_batch_005_pasuk_segments_match_expected_count(self):
        records = normalized_records_for_batch("batch_005_linear_bereishis_4_1_to_4_16")
        pasuk_segments = [record for record in records if record["record_type"] == "pasuk_segment"]
        self.assertEqual(len(pasuk_segments), 64)
        self.assertTrue(all(record["source_package_id"] == "linear_chumash_translation_most_parshiyos_in_torah" for record in pasuk_segments))

    def test_batch_001_vocab_entries_without_glosses_are_flagged_for_review(self):
        enriched_ids = {
            "vocab_entry_batch_001_011_ארץ",
            "vocab_entry_batch_001_012_אדם",
            "vocab_entry_batch_001_013_אשה",
            "vocab_entry_batch_001_014_בית",
            "vocab_entry_batch_001_015_בן",
            "vocab_entry_batch_001_016_יום",
            "vocab_entry_batch_001_017_מים",
            "vocab_entry_batch_001_018_עץ",
        }
        empty_gloss_ids = []
        seen_enriched = set()
        for record in normalized_records_by_type("vocab_entry"):
            if record["id"] in enriched_ids:
                seen_enriched.add(record["id"])
                self.assertTrue(record["english_glosses"], record["id"])
                self.assertFalse(record["needs_gloss_review"], record["id"])
                self.assertNotIn("missing_english_gloss", record["extraction_quality_flags"], record["id"])
                self.assertEqual(
                    record["source_trace"]["source_name"],
                    "First 150 Shorashim and Keywords in Bereishis",
                    record["id"],
                )
                self.assertEqual(
                    record["source_trace"]["source_file"],
                    "13726D_g_01023_first_150_shorashim_and_keywords_in_chumash.pdf",
                    record["id"],
                )
            if not record.get("english_glosses"):
                empty_gloss_ids.append(record["id"])
                self.assertTrue(record["needs_gloss_review"], record["id"])
                self.assertIn("missing_english_gloss", record["extraction_quality_flags"], record["id"])
        self.assertEqual(seen_enriched, enriched_ids)
        self.assertEqual(len(empty_gloss_ids), 0)

    def test_batch_001_comprehension_records_without_answers_are_flagged(self):
        records = normalized_records_by_type("comprehension_question")
        self.assertEqual(len(records), 10)
        for record in records:
            self.assertIsNone(record["expected_answer"], record["id"])
            self.assertEqual(record["answer_status"], "not_provided", record["id"])
            self.assertIn("missing_expected_answer", record["extraction_quality_flags"], record["id"])

    def test_batch_001_word_parse_task_records_without_answer_key_are_flagged(self):
        records = normalized_records_by_type("word_parse_task")
        self.assertEqual(len(records), 8)
        for record in records:
            self.assertEqual(record["answer_status"], "not_extracted", record["id"])
            self.assertFalse(record["expected_word_in_pasuk"], record["id"])
            self.assertEqual(record["prefixes"], [], record["id"])
            self.assertEqual(record["suffixes"], [], record["id"])
            self.assertIn("answer_key_not_extracted", record["extraction_quality_flags"], record["id"])

    def test_batch_001_word_parse_incomplete_fields_are_flagged(self):
        records = normalized_records_by_type("word_parse")
        missing_shoresh = [
            record["id"]
            for record in records
            if "missing_explicit_shoresh" in record["extraction_quality_flags"]
        ]
        missing_suffix = [
            record["id"]
            for record in records
            if "missing_suffix_payload" in record["extraction_quality_flags"]
        ]
        self.assertEqual(len(missing_shoresh), 4)
        self.assertEqual(len(missing_suffix), 6)

    def test_forbidden_runtime_files_are_not_changed(self):
        changed_paths = validator.collect_changed_paths()
        disallowed = [
            path
            for path in changed_paths
            if not validator.is_allowed_change(path)
            and not validator.is_allowed_source_truth_baseline_repair(path)
            and not validator.is_allowed_perek_3_pilot_wording_fix(path)
            and not validator.is_allowed_perek_3_pilot_distractor_source_remediation(path)
            and not validator.is_allowed_perek_3_short_repilot_scope_leak_fix(path)
        ]
        self.assertEqual(disallowed, [], [validator.forbidden_reason(path) for path in disallowed])

    def test_generated_local_log_paths_are_ignored_by_changed_path_collection(self):
        fake_status = "\n".join(
            [
                " M data/attempt_log.jsonl",
                " M data/pilot/pilot_session_events.jsonl",
            ]
        )
        with mock.patch.object(validator.subprocess, "run") as run_mock:
            run_mock.return_value = mock.Mock(stdout=fake_status)
            self.assertEqual(validator.collect_changed_paths(), [])

    def test_incoming_source_paths_are_ignored_by_changed_path_collection(self):
        fake_status = "\n".join(
            [
                "?? incoming_source/bereishis_hebrew_menukad_taamim.tsv",
                "?? incoming_source/bereishis_hebrew_menukad_taamim_validation.md",
                "?? data/source_texts/source_text_manifest.json",
            ]
        )
        with mock.patch.object(validator.subprocess, "run") as run_mock:
            run_mock.return_value = mock.Mock(stdout=fake_status)
            self.assertEqual(
                validator.collect_changed_paths(),
                ["data/source_texts/source_text_manifest.json"],
            )

    def test_unrelated_path_outside_allowlist_still_fails(self):
        fake_status = " M data/some_other_runtime_like_file.jsonl"
        with mock.patch.object(validator.subprocess, "run") as run_mock:
            run_mock.return_value = mock.Mock(stdout=fake_status)
            changed_paths = validator.collect_changed_paths()
        self.assertEqual(changed_paths, ["data/some_other_runtime_like_file.jsonl"])
        self.assertFalse(validator.is_allowed_change(changed_paths[0]))
        self.assertEqual(
            validator.forbidden_reason(changed_paths[0]),
            "path outside isolated curriculum extraction allowlist: data/some_other_runtime_like_file.jsonl",
        )

    def test_forbidden_runtime_and_scope_paths_still_fail(self):
        forbidden_paths = [
            "engine/flow_builder.py",
            "streamlit_app.py",
            "assessment_scope.py",
            "data/corpus_manifest.json",
        ]
        for path in forbidden_paths:
            with self.subTest(path=path):
                self.assertFalse(validator.is_allowed_change(path))
                self.assertEqual(validator.forbidden_reason(path), f"forbidden path changed: {path}")

    def test_governed_audit_artifact_paths_are_allowed_but_root_audits_are_forbidden(self):
        allowed_paths = [
            "data/curriculum_extraction/reports/audits/AUDIT_OVERNIGHT_CURRICULUM_QUALITY_REVIEW.md",
            "data/curriculum_extraction/reports/audits/AUDIT_OVERNIGHT_CURRICULUM_QUALITY_REVIEW.pdf",
        ]
        for path in allowed_paths:
            with self.subTest(path=path):
                self.assertTrue(validator.is_allowed_change(path))

        forbidden_paths = [
            "AUDIT_OVERNIGHT_CURRICULUM_QUALITY_REVIEW.md",
            "AUDIT_OVERNIGHT_CURRICULUM_QUALITY_REVIEW.pdf",
            "data/curriculum_extraction/reports/audits/AUDIT_OVERNIGHT_CURRICULUM_QUALITY_REVIEW.json",
        ]
        for path in forbidden_paths:
            with self.subTest(path=path):
                self.assertFalse(validator.is_allowed_change(path))
                self.assertEqual(
                    validator.forbidden_reason(path),
                    f"path outside isolated curriculum extraction allowlist: {path}",
                )

    def test_runtime_state_isolation_fix_paths_are_allowed(self):
        allowed_paths = [
            "runtime/question_flow.py",
            "tests/test_runtime_question_flow.py",
        ]
        for path in allowed_paths:
            with self.subTest(path=path):
                self.assertTrue(validator.is_allowed_change(path))

    def test_perek_3_pilot_wording_fix_keeps_engine_allowance_diff_limited(self):
        safe_diff = """diff --git a/engine/flow_builder.py b/engine/flow_builder.py
-        "What form is shown?",
+        "What tense or verb form is this word?",
-                f"What is the prefix in {target['token']}?",
+                f"In {target['token']}, which beginning letter is the prefix?",
"""
        with mock.patch.object(validator.subprocess, "run") as run_mock:
            run_mock.return_value.returncode = 0
            run_mock.return_value.stdout = safe_diff
            self.assertTrue(validator.is_allowed_perek_3_pilot_wording_fix("engine/flow_builder.py"))

        unsafe_diff = """diff --git a/engine/flow_builder.py b/engine/flow_builder.py
+        activate_perek_4_runtime_scope()
"""
        with mock.patch.object(validator.subprocess, "run") as run_mock:
            run_mock.return_value.returncode = 0
            run_mock.return_value.stdout = unsafe_diff
            self.assertFalse(validator.is_allowed_perek_3_pilot_wording_fix("engine/flow_builder.py"))

        self.assertFalse(validator.is_allowed_change("engine/flow_builder.py"))

    def test_perek_3_pilot_distractor_source_remediation_allows_only_exact_choice_repair(self):
        safe_diff = """diff --git a/data/active_scope_reviewed_questions.json b/data/active_scope_reviewed_questions.json
@@
      "question_text": "What does אֲרוּרָה mean?",
-        "Eden",
-        "Eve",
-        "all"
+        "naked",
+        "living",
+        "heel"
@@
      "question_text": "What does דֶּרֶךְ mean?",
-        "Eve",
-        "Eden",
-        "all",
+        "heel",
+        "children",
+        "naked",
"""
        with mock.patch.object(validator.subprocess, "run") as run_mock:
            run_mock.return_value.returncode = 0
            run_mock.return_value.stdout = safe_diff
            self.assertTrue(
                validator.is_allowed_perek_3_pilot_distractor_source_remediation(
                    "data/active_scope_reviewed_questions.json"
                )
            )

        unsafe_diff = """diff --git a/data/active_scope_reviewed_questions.json b/data/active_scope_reviewed_questions.json
@@
      "question_text": "What does אֲרוּרָה mean?",
-      "correct_answer": "cursed",
+      "correct_answer": "blessed",
"""
        with mock.patch.object(validator.subprocess, "run") as run_mock:
            run_mock.return_value.returncode = 0
            run_mock.return_value.stdout = unsafe_diff
            self.assertFalse(
                validator.is_allowed_perek_3_pilot_distractor_source_remediation(
                    "data/active_scope_reviewed_questions.json"
                )
            )

        self.assertFalse(validator.is_allowed_change("data/active_scope_reviewed_questions.json"))

    def test_perek_3_short_repilot_scope_leak_fix_allows_only_prefix_prompt_repair(self):
        safe_diff = """diff --git a/data/active_scope_reviewed_questions.json b/data/active_scope_reviewed_questions.json
@@
-      "question_text": "What is the prefix in בְּאִשְׁתּוֹ?",
-      "question": "What is the prefix in בְּאִשְׁתּוֹ?",
+      "question_text": "In בְּאִשְׁתּוֹ, which beginning letter is the prefix?",
+      "question": "In בְּאִשְׁתּוֹ, which beginning letter is the prefix?",
"""
        with mock.patch.object(validator.subprocess, "run") as run_mock:
            run_mock.return_value.returncode = 0
            run_mock.return_value.stdout = safe_diff
            self.assertTrue(
                validator.is_allowed_perek_3_short_repilot_scope_leak_fix(
                    "data/active_scope_reviewed_questions.json"
                )
            )

        unsafe_diff = """diff --git a/data/active_scope_reviewed_questions.json b/data/active_scope_reviewed_questions.json
@@
       "question_text": "What is the prefix in בְּאִשְׁתּוֹ?",
-      "correct_answer": "ב",
+      "correct_answer": "כ",
"""
        with mock.patch.object(validator.subprocess, "run") as run_mock:
            run_mock.return_value.returncode = 0
            run_mock.return_value.stdout = unsafe_diff
            self.assertFalse(
                validator.is_allowed_perek_3_short_repilot_scope_leak_fix(
                    "data/active_scope_reviewed_questions.json"
                )
            )

        self.assertFalse(validator.is_allowed_change("data/active_scope_reviewed_questions.json"))

    def test_source_truth_baseline_repair_paths_are_a_separate_narrow_exception(self):
        repair_paths = [
            "data/corpus_manifest.json",
            "data/source_texts/reports/source_truth_reproducibility_finalization_report.md",
            "tests/test_corpus_manifest.py",
        ]
        for path in repair_paths:
            with self.subTest(path=path):
                self.assertFalse(validator.is_allowed_change(path))
                self.assertTrue(validator.is_allowed_source_truth_baseline_repair(path))

    def test_curriculum_extraction_paths_still_pass_allowlist(self):
        allowed_paths = [
            ".gitignore",
            "PLANS.md",
            "data/curriculum_extraction/reports/batch_002_merge_readiness.md",
            "data/curriculum_extraction/normalized/batch_002_linear_chumash_bereishis_1_6_to_2_3_pasuk_segments.jsonl",
            "data/source/bereishis_4_1_to_4_16.json",
            "data/dikduk_rules/README.md",
            "data/dikduk_rules/dikduk_error_pattern.schema.json",
            "data/dikduk_rules/dikduk_question_template.schema.json",
            "data/dikduk_rules/dikduk_rule.schema.json",
            "data/dikduk_rules/dikduk_rules_manifest.json",
            "data/dikduk_rules/question_templates.jsonl",
            "data/dikduk_rules/rule_groups.json",
            "data/dikduk_rules/rules_loshon_foundation.jsonl",
            "data/dikduk_rules/student_error_patterns.jsonl",
            "data/source_texts/bereishis_hebrew_menukad_taamim.tsv",
            "data/source_texts/reports/bereishis_hebrew_menukad_taamim_validation.md",
            "data/source_texts/reports/source_text_gap_report.md",
            "data/source_texts/reports/source_text_inventory.md",
            "data/source_texts/reports/bereishis_hebrew_source_reconciliation_report.md",
            "data/source_texts/reports/bereishis_hebrew_source_reconciliation_report.json",
            "data/source_texts/README.md",
            "data/source_texts/source_text_manifest.json",
            "data/source_texts/translations/translation_sources_registry.json",
            "data/source_texts/translations/sefaria/README.md",
            "data/source_texts/translations/sefaria/sefaria_genesis_versions_raw.json",
            "data/source_texts/translations/sefaria/sefaria_english_versions_genesis_report.json",
            "data/source_texts/translations/sefaria/bereishis_english_translations_manifest.json",
            "data/source_texts/translations/sefaria/bereishis_english_koren.jsonl",
            "data/source_texts/translations/sefaria/bereishis_english_metsudah.jsonl",
            "data/source_texts/translations/sefaria/bereishis_english_translation_alignment_report.md",
            "data/source_texts/translations/sefaria/bereishis_english_translation_license_report.md",
            "data/source_texts/translations/sefaria/bereishis_english_translation_fetch_report.json",
            "data/source_texts/translations/sefaria/bereishis_english_translation_license_review_matrix.json",
            "data/source_texts/translations/sefaria/bereishis_english_translation_human_review_packet.md",
            "data/source_texts/translations/sefaria/raw_samples/koren_sample.json",
            "data/source_texts/translations/sefaria/raw_samples/metsudah_sample.json",
            "data/gate_2_source_discovery/bereishis_perek_4_review_only_safe_candidate_inventory.tsv",
            "data/gate_2_source_discovery/reports/bereishis_perek_4_source_discovery_report.md",
            "data/gate_2_source_discovery/reports/bereishis_perek_4_duplicate_session_balance_warnings.md",
            "data/gate_2_source_discovery/reports/bereishis_perek_4_duplicate_session_balance_warnings.tsv",
            "data/gate_2_source_discovery/reports/bereishis_perek_4_excluded_risk_lanes.md",
            "data/gate_2_source_discovery/reports/bereishis_perek_4_source_discovery_status_index.md",
            "docs/sources/trusted_teacher_source_policy.md",
            "docs/question_templates/approved_question_template_policy.md",
            "data/verified_source_skill_maps/README.md",
            "data/verified_source_skill_maps/bereishis_1_1_to_3_24_metsudah_skill_map.tsv",
            "data/verified_source_skill_maps/bereishis_1_1_to_1_5_source_to_skill_map.tsv",
            "data/verified_source_skill_maps/bereishis_1_6_to_1_13_source_to_skill_map.tsv",
            "data/verified_source_skill_maps/bereishis_1_14_to_1_23_source_to_skill_map.tsv",
            "data/verified_source_skill_maps/bereishis_1_24_to_1_31_source_to_skill_map.tsv",
            "data/verified_source_skill_maps/reports/bereishis_1_1_to_3_24_metsudah_skill_map_extraction_accuracy_review_packet.md",
            "data/verified_source_skill_maps/reports/bereishis_1_1_to_1_5_source_to_skill_map_exceptions_review_packet.md",
            "data/verified_source_skill_maps/reports/bereishis_1_1_to_1_5_yossi_extraction_verification_report.md",
            "data/verified_source_skill_maps/reports/bereishis_1_6_to_1_13_source_to_skill_map_build_report.md",
            "data/verified_source_skill_maps/reports/bereishis_1_6_to_1_13_source_to_skill_map_exceptions_review_packet.md",
            "data/verified_source_skill_maps/reports/bereishis_1_6_to_1_13_yossi_extraction_verification_report.md",
            "data/verified_source_skill_maps/reports/bereishis_1_14_to_1_23_source_to_skill_map_build_report.md",
            "data/verified_source_skill_maps/reports/bereishis_1_14_to_1_23_source_to_skill_map_exceptions_review_packet.md",
            "data/verified_source_skill_maps/reports/bereishis_1_14_to_1_23_yossi_extraction_verification_report.md",
            "data/verified_source_skill_maps/reports/bereishis_1_24_to_1_31_source_to_skill_map_build_report.md",
            "data/verified_source_skill_maps/reports/bereishis_1_24_to_1_31_source_to_skill_map_exceptions_review_packet.md",
            "data/verified_source_skill_maps/reports/bereishis_1_24_to_1_31_yossi_extraction_verification_report.md",
            "data/verified_source_skill_maps/reports/bereishis_perek_1_source_to_skill_completion_report.md",
            "data/verified_source_skill_maps/reports/source_to_skill_map_audit.json",
            "data/verified_source_skill_maps/bereishis_2_1_to_2_3_source_to_skill_map.tsv",
            "data/verified_source_skill_maps/reports/bereishis_2_1_to_2_3_source_to_skill_map_build_report.md",
            "data/verified_source_skill_maps/reports/bereishis_2_1_to_2_3_source_to_skill_map_exceptions_review_packet.md",
            "data/verified_source_skill_maps/reports/bereishis_2_1_to_2_3_yossi_review_sheet.csv",
            "data/verified_source_skill_maps/reports/bereishis_2_1_to_2_3_yossi_review_sheet.md",
            "data/verified_source_skill_maps/reports/bereishis_2_1_to_2_3_yossi_extraction_verification_report.md",
            "data/verified_source_skill_maps/bereishis_2_4_to_2_17_source_to_skill_map.tsv",
            "data/verified_source_skill_maps/reports/bereishis_2_4_to_2_17_source_to_skill_map_build_report.md",
            "data/verified_source_skill_maps/reports/bereishis_2_4_to_2_17_source_to_skill_map_exceptions_review_packet.md",
            "data/verified_source_skill_maps/reports/bereishis_2_4_to_2_17_yossi_review_sheet.csv",
            "data/verified_source_skill_maps/reports/bereishis_2_4_to_2_17_yossi_review_sheet.md",
            "data/verified_source_skill_maps/reports/bereishis_2_4_to_2_17_yossi_extraction_verification_report.md",
            "data/verified_source_skill_maps/bereishis_2_18_to_2_25_source_to_skill_map.tsv",
            "data/verified_source_skill_maps/reports/bereishis_2_18_to_2_25_source_to_skill_map_build_report.md",
            "data/verified_source_skill_maps/reports/bereishis_2_18_to_2_25_source_to_skill_map_exceptions_review_packet.md",
            "data/verified_source_skill_maps/reports/bereishis_2_18_to_2_25_yossi_review_sheet.csv",
            "data/verified_source_skill_maps/reports/bereishis_2_18_to_2_25_yossi_review_sheet.md",
            "data/verified_source_skill_maps/reports/bereishis_2_18_to_2_25_yossi_extraction_verification_report.md",
            "data/verified_source_skill_maps/reports/bereishis_perek_2_source_to_skill_completion_report.md",
            "data/verified_source_skill_maps/bereishis_3_1_to_3_7_source_to_skill_map.tsv",
            "data/verified_source_skill_maps/reports/bereishis_3_1_to_3_7_source_to_skill_map_build_report.md",
            "data/verified_source_skill_maps/reports/bereishis_3_1_to_3_7_source_to_skill_map_exceptions_review_packet.md",
            "data/verified_source_skill_maps/reports/bereishis_3_1_to_3_7_yossi_review_sheet.csv",
            "data/verified_source_skill_maps/reports/bereishis_3_1_to_3_7_yossi_review_sheet.md",
            "data/verified_source_skill_maps/reports/bereishis_3_1_to_3_7_yossi_extraction_verification_report.md",
            "data/verified_source_skill_maps/bereishis_3_8_to_3_16_source_to_skill_map.tsv",
            "data/verified_source_skill_maps/reports/bereishis_3_8_to_3_16_source_to_skill_map_build_report.md",
            "data/verified_source_skill_maps/reports/bereishis_3_8_to_3_16_source_to_skill_map_exceptions_review_packet.md",
            "data/verified_source_skill_maps/reports/bereishis_3_8_to_3_16_yossi_review_sheet.csv",
            "data/verified_source_skill_maps/reports/bereishis_3_8_to_3_16_yossi_review_sheet.md",
            "data/verified_source_skill_maps/reports/bereishis_3_8_to_3_16_yossi_extraction_verification_report.md",
            "data/verified_source_skill_maps/bereishis_3_17_to_3_24_source_to_skill_map.tsv",
            "data/verified_source_skill_maps/reports/bereishis_3_17_to_3_24_source_to_skill_map_build_report.md",
            "data/verified_source_skill_maps/reports/bereishis_3_17_to_3_24_source_to_skill_map_exceptions_review_packet.md",
            "data/verified_source_skill_maps/reports/bereishis_3_17_to_3_24_yossi_review_sheet.csv",
            "data/verified_source_skill_maps/reports/bereishis_3_17_to_3_24_yossi_review_sheet.md",
            "data/verified_source_skill_maps/reports/bereishis_3_17_to_3_24_yossi_extraction_verification_report.md",
            "data/verified_source_skill_maps/reports/bereishis_perek_3_source_to_skill_completion_report.md",
            "docs/README.md",
            "docs/pilots/perek_3_fresh_pilot_runbook.md",
            "docs/product/bhh_chumash_ai_pilot_one_page_brief.md",
            "docs/review/question_quality_rubric.md",
            "data/gate_2_protected_preview_packets/reports/bereishis_perek_3_limited_post_preview_observation_intake.md",
            "data/pipeline_rounds/README.md",
            "data/pipeline_rounds/claude_review_action_plan_2026_04_29.md",
            "data/pipeline_rounds/perek_3_pilot_evidence_manifest_2026_04_29.json",
            "data/pipeline_rounds/perek_3_fresh_pilot_observation_summary_2026_04_29.json",
            "data/pipeline_rounds/perek_3_fresh_pilot_observation_summary_2026_04_29.md",
            "data/pipeline_rounds/perek_3_pilot_remediation_plan_2026_04_29.json",
            "data/pipeline_rounds/perek_3_pilot_remediation_plan_2026_04_29.md",
            "data/pipeline_rounds/perek_3_pilot_remediation_sequence_2026_04_29.md",
            "data/pipeline_rounds/perek_3_pilot_teacher_decision_checklist_2026_04_29.md",
            "data/pipeline_rounds/perek_3_pilot_wording_clarity_fix_report_2026_04_29.md",
            "data/pipeline_rounds/perek_3_pilot_distractor_source_audit_2026_04_29.md",
            "data/pipeline_rounds/perek_3_phrase_translation_distractor_audit_2026_04_29.md",
            "data/pipeline_rounds/perek_3_ashis_shis_source_followup_2026_04_29.md",
            "data/pipeline_rounds/perek_3_pilot_remediation_completion_gate_2026_04_29.md",
            "data/pipeline_rounds/perek_3_pilot_remediation_completion_gate_2026_04_29.json",
            "data/pipeline_rounds/perek_3_yossi_language_decisions_2026_04_29.md",
            "data/pipeline_rounds/perek_3_yossi_language_decisions_2026_04_29.json",
            "data/pipeline_rounds/perek_3_short_repilot_scope_2026_04_29.md",
            "data/pipeline_rounds/perek_3_short_repilot_scope_2026_04_29.json",
            "data/pipeline_rounds/perek_3_short_repilot_enforcement_plan_2026_04_29.md",
            "data/pipeline_rounds/perek_3_short_repilot_enforcement_plan_2026_04_29.json",
            "data/pipeline_rounds/perek_3_short_repilot_manual_checklist_2026_04_29.md",
            "data/pipeline_rounds/perek_3_short_repilot_results_2026_04_29.md",
            "data/pipeline_rounds/perek_3_short_repilot_results_2026_04_29.json",
            "data/pipeline_rounds/perek_3_short_repilot_scope_leak_report_2026_04_29.md",
            "data/pipeline_rounds/perek_3_short_repilot_to_perek_4_ready_gate_2026_04_29.md",
            "data/pipeline_rounds/perek_3_short_repilot_to_perek_4_ready_gate_2026_04_29.json",
            "data/pipeline_rounds/perek_3_short_repilot_scope_leak_fix_report_2026_04_29.md",
            "data/pipeline_rounds/perek_3_to_perek_4_yossi_override_2026_04_29.md",
            "data/pipeline_rounds/perek_3_to_perek_4_yossi_override_2026_04_29.json",
            "data/pipeline_rounds/perek_4_teacher_review_packet_readiness_2026_04_29.md",
            "data/pipeline_rounds/perek_4_post_teacher_review_next_gate_readiness_2026_04_29.md",
            "data/pipeline_rounds/perek_4_candidate_planning_review_checklist_readiness_2026_04_29.md",
            "data/pipeline_rounds/perek_4_candidate_planning_decisions_next_gate_readiness_2026_04_29.md",
            "data/pipeline_rounds/perek_4_internal_protected_preview_packet_readiness_2026_04_29.md",
            "data/pipeline_rounds/perek_4_internal_protected_preview_packet_created_2026_04_29.md",
            "data/pipeline_rounds/repo_hygiene_inventory_2026_04_29.md",
            "data/standards/zekelman/review/zekelman_2025_standard_3_review_tracking.json",
            "data/standards/zekelman/review/zekelman_2025_standard_3_teacher_review_packet.md",
            "data/standards/zekelman/reports/zekelman_2025_standard_3_teacher_review_layer_report.md",
            "data/sources/loshon_hatorah/loshon_hatorah_source_inventory.json",
            "data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json",
            "docs/sources/loshon_hatorah/indexes/loshon_hatorah_document_index.json",
            "docs/sources/loshon_hatorah/reports/loshon_hatorah_source_ingestion_report.md",
            "data/diagnostic_preview/README.md",
            "data/diagnostic_preview/configs/bereishis_1_1_to_2_3_dikduk_translation_preview.json",
            "data/diagnostic_preview/blueprints/bereishis_1_1_to_2_3_dikduk_translation_blueprints.jsonl",
            "data/diagnostic_preview/generated_questions/bereishis_1_1_to_2_3_preview_questions.jsonl",
            "data/diagnostic_preview/reports/bereishis_1_1_to_2_3_manual_review_packet.md",
            "data/diagnostic_preview/reports/bereishis_1_1_to_2_3_preview_summary.md",
            "data/diagnostic_preview/reports/bereishis_1_1_to_2_3_preview_summary.json",
            "data/source_skill_enrichment/README.md",
            "data/source_skill_enrichment/morphology_candidates/bereishis_1_1_to_1_5_morphology_candidates.tsv",
            "data/source_skill_enrichment/reports/bereishis_1_1_to_1_5_morphology_enrichment_yossi_review_sheet.csv",
            "dikduk_rules_loader.py",
            "translation_sources_loader.py",
            "scripts/build_source_to_skill_map.py",
            "scripts/generate_yossi_review_sheet.py",
            "scripts/fetch_sefaria_bereishis_translations.py",
            "scripts/generate_diagnostic_preview.py",
            "scripts/validate_bereishis_translations.py",
            "scripts/validate_curriculum_extraction.py",
            "scripts/validate_source_skill_enrichment.py",
            "scripts/validate_diagnostic_preview.py",
            "scripts/validate_dikduk_rules.py",
            "scripts/README.md",
            "scripts/validate_perek_3_pilot_evidence_pack.py",
            "scripts/validate_perek_3_pilot_observation_summary.py",
            "scripts/validate_perek_3_pilot_remediation_plan.py",
            "scripts/validate_perek_3_pilot_wording_clarity_fix.py",
            "scripts/validate_perek_3_pilot_distractor_source_remediation.py",
            "scripts/validate_perek_3_yossi_language_decisions.py",
            "scripts/validate_perek_3_short_repilot_scope_enforcement.py",
            "scripts/validate_perek_3_short_repilot_results.py",
            "scripts/validate_perek_3_short_repilot_scope_leak_fix.py",
            "scripts/validate_perek_4_compressed_teacher_review_packet.py",
            "scripts/validate_perek_4_teacher_review_decisions_applied.py",
            "scripts/validate_perek_4_candidate_planning_review_checklist.py",
            "scripts/validate_perek_4_candidate_planning_decisions_applied.py",
            "scripts/validate_perek_4_protected_preview_candidate_review_decisions.py",
            "scripts/validate_perek_4_internal_protected_preview_packet.py",
            "scripts/validate_standards_data.py",
            "tests/conftest.py",
            "tests/test_curriculum_extraction_validation.py",
            "tests/test_source_skill_enrichment.py",
            "tests/test_bereishis_translation_sources.py",
            "tests/test_diagnostic_preview_generation.py",
            "tests/test_diagnostic_preview_validation.py",
            "tests/test_dikduk_rule_loader.py",
            "tests/test_dikduk_rules_validation.py",
            "tests/test_perek_3_pilot_evidence_pack.py",
            "tests/test_perek_3_pilot_observation_summary.py",
            "tests/test_perek_3_pilot_remediation_plan.py",
            "tests/test_perek_3_pilot_wording_clarity_fix.py",
            "tests/test_perek_3_pilot_distractor_source_remediation.py",
            "tests/test_perek_3_yossi_language_decisions.py",
            "tests/test_perek_3_short_repilot_scope_enforcement.py",
            "tests/test_perek_3_short_repilot_results.py",
            "tests/test_perek_3_short_repilot_scope_leak_fix.py",
            "tests/test_perek_4_compressed_teacher_review_packet.py",
            "tests/test_perek_4_teacher_review_decisions_applied.py",
            "tests/test_perek_4_candidate_planning_review_checklist.py",
            "tests/test_perek_4_candidate_planning_decisions_applied.py",
            "tests/test_perek_4_protected_preview_candidate_review_decisions.py",
            "tests/test_perek_4_internal_protected_preview_packet.py",
            "tests/test_prefix_question_generation.py",
            "tests/test_tense_morphology_questions.py",
            "tests/test_translation_sources_loader.py",
            "tests/test_source_corpus_block_4_1_to_4_16.py",
            "docs/curriculum_pipeline/source_text_foundation_plan.md",
            "docs/curriculum_pipeline/source_text_handoff.md",
            "docs/curriculum_pipeline/source_text_validation_strategy.md",
            "docs/codex_prompts/batch_006_source_ready_prompt_seed.md",
            "scripts/validate_source_texts.py",
            "tests/test_source_texts_validation.py",
            "tests/test_standards_data_validation.py",
            "scripts/validate_verified_source_skill_maps.py",
            "scripts/validate_perek_4_source_discovery.py",
            "tests/test_perek_4_source_discovery.py",
            "tests/test_verified_source_skill_maps.py",
        ]
        for path in allowed_paths:
            with self.subTest(path=path):
                self.assertTrue(validator.is_allowed_change(path))

    def test_unrelated_source_prep_like_paths_still_fail_allowlist(self):
        disallowed_paths = [
            ".gitattributes",
            "data/source/bereishis_4_17_to_4_26.json",
            "tests/test_source_corpus_block_4_17_to_4_26.py",
            "data/source_texts/shemos_hebrew_menukad_taamim.tsv",
            "data/source_texts/reports/shemos_hebrew_menukad_taamim_validation.md",
            "data/source_texts/reports/source_text_future_notes.md",
            "data/source_texts/source_text_manifest_backup.json",
            "docs/curriculum_pipeline/source_text_runtime_promotion.md",
            "docs/codex_prompts/batch_007_source_ready_prompt_seed.md",
            "docs/pilots/perek_3_fake_results.md",
            "data/pipeline_rounds/perek_3_runtime_promotion_plan.md",
            "tests/test_source_texts_validation_shemos.py",
            "data/source_texts/translations/sefaria/runtime_export.json",
            "data/source_texts/translations/other/bereishis_english_other.jsonl",
            "data/source_texts/translations/translation_sources_registry_backup.json",
            "scripts/fetch_sefaria_shemos_translations.py",
            "scripts/generate_diagnostic_runtime_preview.py",
            "tests/test_shemos_translation_sources.py",
            "tests/test_diagnostic_preview_runtime.py",
            "translation_sources_loader_backup.py",
            "tests/conftest_backup.py",
            "PLANS-archive.md",
            "data/diagnostic_preview_runtime/preview.json",
            "data/gate_2_source_discovery_runtime/perek4.tsv",
            "data/standards/other/review/fake_review_packet.md",
            "data/sources/other_source/source_inventory.json",
            "docs/sources/other_source/reports/source_ingestion_report.md",
        ]
        for path in disallowed_paths:
            with self.subTest(path=path):
                self.assertFalse(validator.is_allowed_change(path))
                self.assertEqual(
                    validator.forbidden_reason(path),
                    f"path outside isolated curriculum extraction allowlist: {path}",
                )

    def test_diagnostic_preview_prefix_is_narrow(self):
        self.assertTrue(
            validator.is_allowed_change(
                "data/diagnostic_preview/reports/bereishis_1_1_to_2_3_preview_summary.md"
            )
        )
        self.assertFalse(validator.is_allowed_change("data/diagnostic_preview_runtime/preview_summary.md"))
        self.assertEqual(
            validator.forbidden_reason("data/diagnostic_preview_runtime/preview_summary.md"),
            "path outside isolated curriculum extraction allowlist: data/diagnostic_preview_runtime/preview_summary.md",
        )


if __name__ == "__main__":
    unittest.main()
