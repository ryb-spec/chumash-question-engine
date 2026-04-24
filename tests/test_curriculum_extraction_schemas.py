import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "curriculum_extraction"
SCHEMA_DIR = DATA_DIR / "schemas"

REQUIRED_SCHEMAS = [
    "source_trace.schema.json",
    "pasuk_segment.schema.json",
    "word_parse.schema.json",
    "word_parse_task.schema.json",
    "vocab_entry.schema.json",
    "comprehension_question.schema.json",
    "question_template.schema.json",
    "skill_tag.schema.json",
    "translation_rule.schema.json",
    "generated_question_preview.schema.json",
    "extraction_batch_report.schema.json",
]


class CurriculumExtractionSchemaTests(unittest.TestCase):
    def test_required_schemas_exist(self):
        for filename in REQUIRED_SCHEMAS:
            self.assertTrue((SCHEMA_DIR / filename).exists(), filename)

    def test_schemas_are_valid_json(self):
        for filename in REQUIRED_SCHEMAS:
            with self.subTest(filename=filename):
                payload = json.loads((SCHEMA_DIR / filename).read_text(encoding="utf-8"))
                self.assertIsInstance(payload, dict)
                self.assertIn("title", payload)


if __name__ == "__main__":
    unittest.main()
