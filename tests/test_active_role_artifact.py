import json
import unittest
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

from engine import flow_builder
from torah_parser.export_bank import rebuild_active_parsed_pesukim_artifact


class ActiveRoleArtifactTests(unittest.TestCase):
    def test_rebuild_active_parsed_pesukim_artifact_writes_role_layer(self):
        temp_path = Path(".tmp_tests") / f"parsed_role_artifact_{uuid4().hex}.json"
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            artifact = rebuild_active_parsed_pesukim_artifact(output_path=temp_path)
            self.assertEqual(artifact["metadata"]["pesukim_count"], 64)
            self.assertTrue(temp_path.exists())

            persisted = json.loads(temp_path.read_text(encoding="utf-8"))
            first = persisted["parsed_pesukim"][0]
            self.assertIn("role_layer", first)
            self.assertTrue(first["token_records"])
            self.assertIn("role_data", first["token_records"][0])
        finally:
            temp_path.unlink(missing_ok=True)

    def test_runtime_analysis_uses_active_parsed_artifact_when_available(self):
        pasuk = "וַיֹּאמֶר אֱלֹהִים"
        parsed_record = {
            "text": pasuk,
            "token_records": [
                {
                    "surface": "וַיֹּאמֶר",
                    "normalized": "ויאמר",
                    "selected_analysis": {
                        "word": "וַיֹּאמֶר",
                        "translation": "said",
                        "type": "verb",
                        "part_of_speech": "verb",
                        "semantic_group": "action",
                        "role_hint": "unknown",
                        "entity_type": "verb",
                    },
                    "role_data": {
                        "role_status": "resolved",
                        "clause_role": "verb",
                        "verb_index": 0,
                        "verb_token": "וַיֹּאמֶר",
                        "token_index": 0,
                        "token": "וַיֹּאמֶר",
                    },
                },
                {
                    "surface": "אֱלֹהִים",
                    "normalized": "אלהים",
                    "selected_analysis": {
                        "word": "אֱלֹהִים",
                        "translation": "God",
                        "type": "noun",
                        "part_of_speech": "noun",
                        "semantic_group": "divine",
                        "role_hint": "subject_candidate",
                        "entity_type": "divine_being",
                    },
                    "role_data": {
                        "role_status": "resolved",
                        "clause_role": "subject",
                        "verb_index": 0,
                        "verb_token": "וַיֹּאמֶר",
                        "token_index": 1,
                        "token": "אֱלֹהִים",
                    },
                },
            ],
        }

        with patch.object(flow_builder, "active_parsed_pasuk_record_for_text", return_value=parsed_record):
            analyzed = flow_builder.analyze_pasuk(pasuk, word_bank={})

        self.assertEqual(analyzed[0]["role_data"]["clause_role"], "verb")
        self.assertEqual(analyzed[1]["role_data"]["clause_role"], "subject")
        self.assertEqual(analyzed[1]["entry"]["translation"], "God")


if __name__ == "__main__":
    unittest.main()
