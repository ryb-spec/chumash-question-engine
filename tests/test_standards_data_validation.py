import copy
import json
import unittest
from unittest import mock

from scripts import validate_standards_data as validator


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_with_overrides(
    *,
    structured=None,
    supplemental_crosswalk=None,
    skill_mapping=None,
    review_tracking=None,
):
    payloads = {
        validator.STRUCTURED_STANDARD_3_PATH: load_json(validator.STRUCTURED_STANDARD_3_PATH),
        validator.SUPPLEMENTAL_CROSSWALK_PATH: load_json(validator.SUPPLEMENTAL_CROSSWALK_PATH),
        validator.SKILL_MAPPING_DRAFT_PATH: load_json(validator.SKILL_MAPPING_DRAFT_PATH),
        validator.REVIEW_TRACKING_PATH: load_json(validator.REVIEW_TRACKING_PATH),
    }
    if structured is not None:
        payloads[validator.STRUCTURED_STANDARD_3_PATH] = structured
    if supplemental_crosswalk is not None:
        payloads[validator.SUPPLEMENTAL_CROSSWALK_PATH] = supplemental_crosswalk
    if skill_mapping is not None:
        payloads[validator.SKILL_MAPPING_DRAFT_PATH] = skill_mapping
    if review_tracking is not None:
        payloads[validator.REVIEW_TRACKING_PATH] = review_tracking

    original_load_json = validator.load_json

    def side_effect(path):
        if path in payloads:
            return payloads[path]
        return original_load_json(path)

    with mock.patch.object(validator, "load_json", side_effect=side_effect):
        return validator.validate_standards_data()


class StandardsDataValidationTests(unittest.TestCase):
    def test_validator_passes_on_current_standard_3_review_data(self):
        summary = validator.validate_standards_data()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["review_item_count"], 8)

    def test_invalid_review_status_is_rejected(self):
        review_tracking = load_json(validator.REVIEW_TRACKING_PATH)
        review_tracking = copy.deepcopy(review_tracking)
        review_tracking["review_items"][0]["current_review_status"] = ["needs_teacher_review", "review_complete"]

        summary = validate_with_overrides(review_tracking=review_tracking)

        self.assertFalse(summary["valid"])
        self.assertTrue(any("current_review_status[1]" in error for error in summary["errors"]), summary["errors"])

    def test_missing_standard_id_is_rejected(self):
        review_tracking = load_json(validator.REVIEW_TRACKING_PATH)
        review_tracking = copy.deepcopy(review_tracking)
        del review_tracking["review_items"][0]["standard_id"]

        summary = validate_with_overrides(review_tracking=review_tracking)

        self.assertFalse(summary["valid"])
        self.assertTrue(any("missing required field 'standard_id'" in error for error in summary["errors"]), summary["errors"])

    def test_missing_related_skill_mapping_is_rejected(self):
        review_tracking = load_json(validator.REVIEW_TRACKING_PATH)
        review_tracking = copy.deepcopy(review_tracking)
        review_tracking["review_items"][0]["related_skill_ids"] = ["std3_missing_skill"]

        summary = validate_with_overrides(review_tracking=review_tracking)

        self.assertFalse(summary["valid"])
        self.assertTrue(any("std3_missing_skill" in error for error in summary["errors"]), summary["errors"])

    def test_forbidden_runtime_or_question_ready_token_is_rejected(self):
        review_tracking = load_json(validator.REVIEW_TRACKING_PATH)
        review_tracking = copy.deepcopy(review_tracking)
        review_tracking["review_items"][0]["workflow_flag"] = "approved_for_runtime"

        summary = validate_with_overrides(review_tracking=review_tracking)

        self.assertFalse(summary["valid"])
        self.assertTrue(any("forbidden readiness token" in error for error in summary["errors"]), summary["errors"])


if __name__ == "__main__":
    unittest.main()
