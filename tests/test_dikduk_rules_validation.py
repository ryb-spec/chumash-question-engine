import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import validate_dikduk_rules as validator


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "data" / "dikduk_rules"


class DikdukRulesValidationTests(unittest.TestCase):
    def test_expected_package_files_exist(self):
        expected = {
            "README.md",
            "dikduk_rules_manifest.json",
            "rule_groups.json",
            "rules_loshon_foundation.jsonl",
            "question_templates.jsonl",
            "student_error_patterns.jsonl",
            "dikduk_rule.schema.json",
            "dikduk_question_template.schema.json",
            "dikduk_error_pattern.schema.json",
        }
        self.assertEqual(expected, {path.name for path in PACKAGE_DIR.iterdir() if path.is_file()})

    def test_validator_passes_on_real_package(self):
        summary = validator.validate_dikduk_rules()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["rule_group_count"], 15)
        self.assertEqual(summary["rule_count"], 37)
        self.assertEqual(summary["question_template_count"], 47)
        self.assertEqual(summary["student_error_pattern_count"], 25)

    def test_rule_ids_are_unique_in_real_package(self):
        rule_ids = []
        for raw_line in (PACKAGE_DIR / "rules_loshon_foundation.jsonl").read_text(encoding="utf-8").splitlines():
            if raw_line.strip():
                rule_ids.append(json.loads(raw_line)["rule_id"])
        self.assertEqual(len(rule_ids), len(set(rule_ids)))

    def test_every_question_template_points_to_existing_rule(self):
        rules = {
            json.loads(raw_line)["rule_id"]
            for raw_line in (PACKAGE_DIR / "rules_loshon_foundation.jsonl").read_text(encoding="utf-8").splitlines()
            if raw_line.strip()
        }
        for raw_line in (PACKAGE_DIR / "question_templates.jsonl").read_text(encoding="utf-8").splitlines():
            if not raw_line.strip():
                continue
            record = json.loads(raw_line)
            self.assertIn(record["rule_id"], rules)

    def test_every_error_pattern_points_to_existing_rule(self):
        rules = {
            json.loads(raw_line)["rule_id"]
            for raw_line in (PACKAGE_DIR / "rules_loshon_foundation.jsonl").read_text(encoding="utf-8").splitlines()
            if raw_line.strip()
        }
        for raw_line in (PACKAGE_DIR / "student_error_patterns.jsonl").read_text(encoding="utf-8").splitlines():
            if not raw_line.strip():
                continue
            record = json.loads(raw_line)
            for linked_rule_id in record["linked_rule_ids"]:
                self.assertIn(linked_rule_id, rules)

    def test_validator_fails_on_duplicate_rule_id_in_temp_copy(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_package = Path(temp_dir) / "dikduk_rules"
            shutil.copytree(PACKAGE_DIR, temp_package)
            rules_path = temp_package / "rules_loshon_foundation.jsonl"
            records = [
                json.loads(line)
                for line in rules_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            records[1]["rule_id"] = records[0]["rule_id"]
            rules_path.write_text(
                "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
                encoding="utf-8",
            )
            summary = validator.validate_dikduk_rules(temp_package)
            self.assertFalse(summary["valid"])
            self.assertTrue(any("Duplicate rule_id" in message for message in summary["errors"]))

    def test_validator_fails_on_missing_rule_reference_in_temp_copy(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_package = Path(temp_dir) / "dikduk_rules"
            shutil.copytree(PACKAGE_DIR, temp_package)
            templates_path = temp_package / "question_templates.jsonl"
            records = [
                json.loads(line)
                for line in templates_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            records[0]["rule_id"] = "DK-ARTICLE-999"
            templates_path.write_text(
                "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
                encoding="utf-8",
            )
            summary = validator.validate_dikduk_rules(temp_package)
            self.assertFalse(summary["valid"])
            self.assertTrue(any("does not point to an existing rule" in message for message in summary["errors"]))


if __name__ == "__main__":
    unittest.main()
