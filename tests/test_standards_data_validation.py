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
    loshon_source_inventory=None,
    loshon_document_index=None,
    loshon_rule_candidates=None,
    loshon_standard_3_crosswalk=None,
):
    payloads = {
        validator.STRUCTURED_STANDARD_3_PATH: load_json(validator.STRUCTURED_STANDARD_3_PATH),
        validator.SUPPLEMENTAL_CROSSWALK_PATH: load_json(validator.SUPPLEMENTAL_CROSSWALK_PATH),
        validator.SKILL_MAPPING_DRAFT_PATH: load_json(validator.SKILL_MAPPING_DRAFT_PATH),
        validator.REVIEW_TRACKING_PATH: load_json(validator.REVIEW_TRACKING_PATH),
        validator.LOSHON_SOURCE_INVENTORY_PATH: load_json(validator.LOSHON_SOURCE_INVENTORY_PATH),
        validator.LOSHON_DOCUMENT_INDEX_PATH: load_json(validator.LOSHON_DOCUMENT_INDEX_PATH),
        validator.LOSHON_RULE_CANDIDATES_PATH: load_json(validator.LOSHON_RULE_CANDIDATES_PATH),
        validator.LOSHON_ZEKELMAN_CROSSWALK_PATH: load_json(validator.LOSHON_ZEKELMAN_CROSSWALK_PATH),
    }
    if structured is not None:
        payloads[validator.STRUCTURED_STANDARD_3_PATH] = structured
    if supplemental_crosswalk is not None:
        payloads[validator.SUPPLEMENTAL_CROSSWALK_PATH] = supplemental_crosswalk
    if skill_mapping is not None:
        payloads[validator.SKILL_MAPPING_DRAFT_PATH] = skill_mapping
    if review_tracking is not None:
        payloads[validator.REVIEW_TRACKING_PATH] = review_tracking
    if loshon_source_inventory is not None:
        payloads[validator.LOSHON_SOURCE_INVENTORY_PATH] = loshon_source_inventory
    if loshon_document_index is not None:
        payloads[validator.LOSHON_DOCUMENT_INDEX_PATH] = loshon_document_index
    if loshon_rule_candidates is not None:
        payloads[validator.LOSHON_RULE_CANDIDATES_PATH] = loshon_rule_candidates
    if loshon_standard_3_crosswalk is not None:
        payloads[validator.LOSHON_ZEKELMAN_CROSSWALK_PATH] = loshon_standard_3_crosswalk

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
        self.assertGreaterEqual(summary["loshon_rule_candidate_count"], 1)
        self.assertGreaterEqual(summary["loshon_crosswalk_mapping_count"], 1)

    def test_loshon_sources_use_trusted_source_policy_without_runtime_promotion(self):
        source_inventory = load_json(validator.LOSHON_SOURCE_INVENTORY_PATH)
        source = source_inventory["sources"][0]

        self.assertEqual(source["teacher_source_status"], "trusted_teacher_source")
        self.assertEqual(source["extraction_review_status"], "pending_yossi_extraction_accuracy_pass")
        self.assertTrue(source["requires_yossi_accuracy_pass"])
        self.assertEqual(source["runtime_status"], "not_runtime_ready")
        self.assertEqual(source["question_ready_status"], "not_question_ready")

    def test_unclear_loshon_source_requires_specific_confirmation_reason(self):
        source_inventory = load_json(validator.LOSHON_SOURCE_INVENTORY_PATH)
        source_inventory = copy.deepcopy(source_inventory)
        source_inventory["sources"][0]["teacher_source_status"] = "needs_specific_confirmation"
        source_inventory["sources"][0]["confirmation_needed_reason"] = ""

        summary = validate_with_overrides(loshon_source_inventory=source_inventory)

        self.assertFalse(summary["valid"])
        self.assertTrue(any("confirmation_needed_reason" in error for error in summary["errors"]), summary["errors"])

    def test_trusted_source_status_does_not_allow_runtime_or_question_ready(self):
        source_inventory = load_json(validator.LOSHON_SOURCE_INVENTORY_PATH)
        source_inventory = copy.deepcopy(source_inventory)
        source_inventory["sources"][0]["runtime_status"] = "runtime_ready"

        summary = validate_with_overrides(loshon_source_inventory=source_inventory)

        self.assertFalse(summary["valid"])
        self.assertTrue(any("runtime_status" in error for error in summary["errors"]), summary["errors"])

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

    def test_invalid_loshon_rule_candidate_status_is_rejected(self):
        rule_candidates = load_json(validator.LOSHON_RULE_CANDIDATES_PATH)
        rule_candidates = copy.deepcopy(rule_candidates)
        rule_candidates["rule_candidates"][0]["review_status"] = ["needs_teacher_review", "ready_for_runtime"]

        summary = validate_with_overrides(loshon_rule_candidates=rule_candidates)

        self.assertFalse(summary["valid"])
        self.assertTrue(any("loshon_rule_candidates[0]: review_status[1]" in error for error in summary["errors"]), summary["errors"])

    def test_loshon_crosswalk_missing_standard_is_rejected(self):
        crosswalk = load_json(validator.LOSHON_ZEKELMAN_CROSSWALK_PATH)
        crosswalk = copy.deepcopy(crosswalk)
        crosswalk["mappings"][0]["standard_id"] = "3.99"

        summary = validate_with_overrides(loshon_standard_3_crosswalk=crosswalk)

        self.assertFalse(summary["valid"])
        self.assertTrue(any("3.99" in error for error in summary["errors"]), summary["errors"])

    def test_loshon_crosswalk_missing_candidate_is_rejected(self):
        crosswalk = load_json(validator.LOSHON_ZEKELMAN_CROSSWALK_PATH)
        crosswalk = copy.deepcopy(crosswalk)
        crosswalk["mappings"][0]["loshon_hatorah_candidate_id"] = "lht_cand_missing"

        summary = validate_with_overrides(loshon_standard_3_crosswalk=crosswalk)

        self.assertFalse(summary["valid"])
        self.assertTrue(any("lht_cand_missing" in error for error in summary["errors"]), summary["errors"])

    def test_loshon_forbidden_ready_token_is_rejected(self):
        rule_candidates = load_json(validator.LOSHON_RULE_CANDIDATES_PATH)
        rule_candidates = copy.deepcopy(rule_candidates)
        rule_candidates["rule_candidates"][0]["workflow_flag"] = "question_ready"

        summary = validate_with_overrides(loshon_rule_candidates=rule_candidates)

        self.assertFalse(summary["valid"])
        self.assertTrue(any("forbidden readiness token" in error for error in summary["errors"]), summary["errors"])


if __name__ == "__main__":
    unittest.main()
