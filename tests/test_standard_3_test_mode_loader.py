import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from runtime.standard_3_test_mode_loader import (
    DEFAULT_PATH,
    EXPECTED_RECORD_COUNT,
    Standard3TestModeLoaderError,
    load_standard_3_protected_bank,
    load_standard_3_test_mode_records,
    standard_3_test_mode_enabled,
    transform_standard_3_record_for_test_mode,
    validate_standard_3_protected_record,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
ACTIVE_SCOPE_PATH = REPO_ROOT / "data" / "active_scope_reviewed_questions.json"
STAGED_REVIEWED_PATHS = tuple((REPO_ROOT / "data" / "staged").glob("*/reviewed_questions.json"))


def file_digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_temp_payload(payload):
    handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False)
    try:
        json.dump(payload, handle, ensure_ascii=False)
    finally:
        handle.close()
    return Path(handle.name)


class Standard3TestModeLoaderTests(unittest.TestCase):
    def test_test_mode_defaults_off(self):
        self.assertFalse(standard_3_test_mode_enabled({}))
        self.assertFalse(standard_3_test_mode_enabled({"STANDARD_3_MVP_TEST_MODE": ""}))
        self.assertFalse(standard_3_test_mode_enabled({"STANDARD_3_MVP_TEST_MODE": "0"}))

    def test_explicit_truthy_flag_enables_test_mode(self):
        for value in ("1", "true", "TRUE", "yes", "on", " On "):
            with self.subTest(value=value):
                self.assertTrue(standard_3_test_mode_enabled({"STANDARD_3_MVP_TEST_MODE": value}))

    def test_loader_returns_empty_when_flag_is_off_without_reading_path(self):
        records = load_standard_3_test_mode_records(env={}, path="missing/path/should/not/be/read.json")
        self.assertEqual(records, [])

    def test_protected_bank_parses_successfully(self):
        records = load_standard_3_protected_bank()
        self.assertEqual(len(records), EXPECTED_RECORD_COUNT)

    def test_test_mode_on_loads_exactly_ten_records(self):
        records = load_standard_3_test_mode_records(env={"STANDARD_3_MVP_TEST_MODE": "1"})
        self.assertEqual(len(records), EXPECTED_RECORD_COUNT)
        self.assertEqual(
            {record["source_record_id"] for record in records},
            {f"STD3-MVP-RB-{index:03d}" for index in range(1, EXPECTED_RECORD_COUNT + 1)},
        )

    def test_transformed_records_contain_required_test_fields(self):
        transformed = load_standard_3_test_mode_records(env={"STANDARD_3_MVP_TEST_MODE": "true"})
        required_fields = {
            "reviewed_id",
            "question",
            "question_text",
            "correct_answer",
            "choices",
            "skill",
            "question_type",
            "mode",
            "micro_standard",
            "difficulty",
            "pasuk_id",
            "pasuk_ref",
            "review_family",
            "runtime_status",
            "student_facing_status",
            "source_record_id",
            "test_mode_only",
        }
        for record in transformed:
            with self.subTest(record=record["reviewed_id"]):
                self.assertTrue(required_fields.issubset(record))
                self.assertEqual(record["mode"], "standard_3_mvp_test_mode")
                self.assertEqual(record["review_family"], "zekelman_standard_3_mvp")
                self.assertEqual(record["difficulty"], "mvp_foundational")
                self.assertEqual(record["pasuk_id"], "standard_3_mvp_test")
                self.assertEqual(record["pasuk_ref"]["label"], "Standard 3 MVP test item")
                self.assertEqual(record["choices"], [])
                self.assertTrue(record["open_response"])

    def test_transformed_records_keep_conservative_statuses_and_marker(self):
        transformed = load_standard_3_test_mode_records(env={"STANDARD_3_MVP_TEST_MODE": "yes"})
        self.assertEqual({record["runtime_status"] for record in transformed}, {"not_runtime_active"})
        self.assertEqual({record["student_facing_status"] for record in transformed}, {"not_student_facing"})
        self.assertEqual({record["test_mode_only"] for record in transformed}, {True})

    def test_active_scope_and_staged_files_are_not_modified_by_loader(self):
        before = {ACTIVE_SCOPE_PATH: file_digest(ACTIVE_SCOPE_PATH)}
        before.update({path: file_digest(path) for path in STAGED_REVIEWED_PATHS})

        load_standard_3_test_mode_records(env={"STANDARD_3_MVP_TEST_MODE": "on"})

        after = {path: file_digest(path) for path in before}
        self.assertEqual(after, before)

    def test_excluded_standard_3_lanes_are_not_present(self):
        records = load_standard_3_protected_bank()
        standard_ids = {record["standard_id"] for record in records}
        lanes = " ".join(record["skill_lane"] for record in records)

        self.assertFalse({"3.04", "3.08", "3.10"} & standard_ids)
        self.assertNotIn("Pronoun Referent Tracking", lanes)
        self.assertNotIn("סמיכות", lanes)

    def test_invalid_runtime_status_causes_validation_failure(self):
        record = copy.deepcopy(load_standard_3_protected_bank()[0])
        record["runtime_status"] = "runtime_active"

        with self.assertRaises(Standard3TestModeLoaderError):
            validate_standard_3_protected_record(record)

    def test_invalid_student_facing_status_causes_validation_failure(self):
        record = copy.deepcopy(load_standard_3_protected_bank()[0])
        record["student_facing_status"] = "student_facing"

        with self.assertRaises(Standard3TestModeLoaderError):
            validate_standard_3_protected_record(record)

    def test_invalid_excluded_standard_id_causes_validation_failure(self):
        record = copy.deepcopy(load_standard_3_protected_bank()[0])
        record["standard_id"] = "3.10"

        with self.assertRaises(Standard3TestModeLoaderError):
            validate_standard_3_protected_record(record)

    def test_unknown_question_family_causes_validation_failure(self):
        record = copy.deepcopy(load_standard_3_protected_bank()[0])
        record["question_type_family"] = "Unapproved family"

        with self.assertRaises(Standard3TestModeLoaderError):
            transform_standard_3_record_for_test_mode(record)

    def test_bank_with_extra_record_is_rejected(self):
        payload = json.loads(DEFAULT_PATH.read_text(encoding="utf-8"))
        payload = copy.deepcopy(payload)
        payload["records"].append(copy.deepcopy(payload["records"][0]))
        temp_path = write_temp_payload(payload)
        try:
            with self.assertRaises(Standard3TestModeLoaderError):
                load_standard_3_protected_bank(temp_path)
        finally:
            temp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
