
from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path

import scripts.validate_template_skeleton_planning as validator


ROOT = Path(__file__).resolve().parents[1]
BASE_DIR = ROOT / "data" / "template_skeleton_planning"
SKELETON_JSON = BASE_DIR / "template_skeleton_policy.v1.json"
EXACT_JSON = BASE_DIR / "exact_template_wording_policy.v1.json"
ANSWER_JSON = BASE_DIR / "answer_key_planning_policy.v1.json"
DISTRACTOR_JSON = BASE_DIR / "distractor_planning_policy.v1.json"
CONTEXT_JSON = BASE_DIR / "context_display_hebrew_policy.v1.json"
SKELETON_TSV = BASE_DIR / "bereishis_perek_1_first_batch_template_skeleton_planning.tsv"
EXACT_TSV = BASE_DIR / "bereishis_perek_1_first_batch_exact_template_wording_planning.tsv"
READINESS = BASE_DIR / "reports" / "bereishis_perek_1_first_batch_pre_generation_readiness_report.md"
POLICY_PACKET = BASE_DIR / "reports" / "bereishis_perek_1_first_batch_answer_distractor_context_policy_yossi_review_packet.md"
POLICY_APPLIED = BASE_DIR / "reports" / "bereishis_perek_1_first_batch_answer_distractor_context_policy_yossi_review_applied.md"
README = BASE_DIR / "README.md"
ET = "\u05d0\u05ea"
HIBDIL = "\u05d4\u05d1\u05d3\u05d9\u05dc"
BDL = "\u05d1\u05d3\u05dc"
HAMAYIM = "\u05d4\u05de\u05d9\u05dd"
HAADAMAH = "\u05d4\u05d0\u05d3\u05de\u05d4"
HAARETZ = "\u05d4\u05d0\u05e8\u05e5"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_tsv(path: Path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


class TemplateSkeletonPlanningTests(unittest.TestCase):
    def test_validator_passes(self):
        summary = validator.validate_template_skeleton_planning()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["row_count"], 24)
        self.assertEqual(summary["exact_row_count"], 24)

    def test_exact_wording_decisions_applied(self):
        policy = load_json(EXACT_JSON)
        rules = policy["family_wording_patterns"]
        self.assertEqual(rules["vocabulary_meaning"]["exact_wording_review_status"], "yossi_exact_wording_family_approved")
        self.assertEqual(rules["basic_noun_recognition"]["exact_wording_review_status"], "yossi_approved_with_revision")
        self.assertEqual(rules["direct_object_marker_recognition"]["exact_wording_review_status"], "yossi_approved_with_revision")
        self.assertEqual(rules["shoresh_identification"]["exact_wording_review_status"], "yossi_approved_with_revision")
        self.assertEqual(policy["basic_verb_form_recognition"]["exact_wording_review_status"], "deferred")

    def test_policy_json_artifacts_exist_and_are_policy_only(self):
        self.assertEqual(load_json(ANSWER_JSON)["status"], "answer_key_policy_only")
        self.assertEqual(load_json(DISTRACTOR_JSON)["status"], "distractor_policy_only")
        self.assertEqual(load_json(CONTEXT_JSON)["status"], "context_display_hebrew_policy_only")
        self.assertEqual(load_json(ANSWER_JSON)["individual_row_answer_keys"], [])
        self.assertEqual(load_json(DISTRACTOR_JSON)["individual_distractors"], [])
        self.assertEqual(load_json(CONTEXT_JSON)["rendered_student_items"], [])
        self.assertEqual(load_json(ANSWER_JSON)["answer_key_planning_policy_review_status"], "yossi_approved_with_revision")
        self.assertEqual(load_json(DISTRACTOR_JSON)["distractor_planning_policy_review_status"], "yossi_approved_with_revision")
        self.assertEqual(load_json(CONTEXT_JSON)["context_display_hebrew_policy_review_status"], "yossi_policy_approved")

    def test_row_level_review_required_before_generation(self):
        required_fields = validator.ROW_LEVEL_REVIEW_FIELDS
        for policy_path in (ANSWER_JSON, DISTRACTOR_JSON, CONTEXT_JSON):
            policy = load_json(policy_path)
            self.assertTrue(policy["row_level_review_required_before_generation"])
            self.assertTrue(required_fields.issubset(set(policy["required_row_level_review_fields"])))

    def test_tsv_rows_and_families(self):
        skeleton_rows = load_tsv(SKELETON_TSV)
        exact_rows = load_tsv(EXACT_TSV)
        self.assertEqual(len(skeleton_rows), 24)
        self.assertEqual(len(exact_rows), 24)
        self.assertTrue({row["approved_family"] for row in exact_rows}.issubset(validator.ALLOWED_FAMILIES))
        self.assertNotIn("basic_verb_form_recognition", {row["approved_family"] for row in exact_rows})

    def test_no_questions_answer_choices_answer_keys_or_distractors(self):
        exact_rows = load_tsv(EXACT_TSV)
        self.assertFalse(set(exact_rows[0].keys()) & validator.FORBIDDEN_CONTENT_COLUMNS)
        self.assertEqual(load_json(EXACT_JSON)["answer_choices"], [])
        self.assertEqual(load_json(EXACT_JSON)["answer_keys"], [])
        self.assertEqual(load_json(ANSWER_JSON)["individual_row_answer_keys"], [])
        self.assertEqual(load_json(DISTRACTOR_JSON)["individual_distractors"], [])

    def test_all_gates_false(self):
        for row in load_tsv(EXACT_TSV):
            for field in validator.REVIEW_STATUS_FIELDS:
                self.assertEqual(row[field], "needs_review")
            for gate in validator.SAFETY_FIELDS:
                self.assertEqual(row[gate], "false")
        for policy_path in (SKELETON_JSON, EXACT_JSON):
            policy = load_json(policy_path)
            for defaults_key in ("safety_gate_defaults",):
                defaults = policy.get(defaults_key, {})
                for gate in validator.SAFETY_FIELDS:
                    if gate in defaults:
                        self.assertFalse(defaults[gate])

    def test_special_cautions_remain(self):
        rows = load_tsv(EXACT_TSV)
        direct_rows = [row for row in rows if row["approved_family"] == "direct_object_marker_recognition"]
        self.assertTrue(direct_rows)
        for row in direct_rows:
            self.assertIn(f"do not ask What does {ET} mean", row["cautions"])
        hibdil = [row for row in rows if row["input_candidate_id"] == "ppplan_b1_024"]
        self.assertEqual(len(hibdil), 1)
        self.assertIn(HIBDIL, hibdil[0]["cautions"])
        self.assertIn(BDL, hibdil[0]["cautions"])
        article_rows = [row for row in rows if row["hebrew_token"] in {HAMAYIM, HAADAMAH, HAARETZ}]
        self.assertTrue(article_rows)
        for row in article_rows:
            self.assertIn("base meaning vs article-inclusive meaning", row["cautions"])

    def test_readiness_report_and_yossi_packet_exist(self):
        self.assertTrue(READINESS.exists())
        self.assertTrue(POLICY_PACKET.exists())
        self.assertTrue(POLICY_APPLIED.exists())
        readiness = READINESS.read_text(encoding="utf-8")
        readiness_lower = readiness.lower()
        self.assertIn("answer-key policy approved: approve_with_revision", readiness_lower)
        self.assertIn("distractor policy approved: approve_with_revision", readiness_lower)
        self.assertIn("context-display/hebrew policy approved: approve_policy", readiness_lower)
        self.assertIn("protected-preview gate approved: needs_review", readiness_lower)
        packet = POLICY_PACKET.read_text(encoding="utf-8")
        self.assertIn("This packet does not generate questions", packet)

    def test_readme_links_artifacts(self):
        readme = README.read_text(encoding="utf-8")
        for path in (ANSWER_JSON, DISTRACTOR_JSON, CONTEXT_JSON, READINESS, POLICY_PACKET, POLICY_APPLIED, EXACT_JSON, EXACT_TSV):
            self.assertIn(path.relative_to(ROOT).as_posix(), readme)


if __name__ == "__main__":
    unittest.main()
