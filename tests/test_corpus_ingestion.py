import json
import unittest
from pathlib import Path
from uuid import uuid4

import assessment_scope
import pasuk_flow_generator
from torah_parser.export_bank import (
    build_staged_corpus_from_source,
    write_parsed_corpus_artifacts,
)


SAMPLE_SOURCE_CORPUS = {
    "metadata": {
        "title": "Sample Bereishis Source",
        "range": "1:1-1:3",
        "format": "sefer,perek,pasuk,text",
    },
    "pesukim": [
        {
            "sefer": "Bereishis",
            "perek": 1,
            "pasuk": 1,
            "text": "בְּרֵאשִׁית בָּרָא אֱלֹקִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ",
        },
        {
            "sefer": "Bereishis",
            "perek": 1,
            "pasuk": 2,
            "text": "וְהָאָרֶץ הָיְתָה תֹהוּ וָבֹהוּ וְחֹשֶׁךְ",
        },
        {
            "sefer": "Bereishis",
            "perek": 1,
            "pasuk": 3,
            "text": "וַיֹּאמֶר אֱלֹקִים יְהִי אוֹר",
        },
    ],
}


class CorpusIngestionTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = assessment_scope.repo_path(".tmp_tests", f"parsed_corpus_test_{uuid4().hex}")
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.source_path = self.temp_dir / "sample_source.json"
        self.source_path.write_text(
            json.dumps(SAMPLE_SOURCE_CORPUS, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def tearDown(self):
        for path in sorted(self.temp_dir.rglob("*"), reverse=True):
            if path.is_file():
                path.unlink(missing_ok=True)
            elif path.is_dir():
                path.rmdir()
        self.temp_dir.rmdir()

    def test_representative_source_pesukim_can_be_ingested_into_parsed_records(self):
        artifacts = build_staged_corpus_from_source(
            self.source_path,
            corpus_id="sample_ingestion_chunk",
            status="parsed",
        )

        runtime_pesukim = artifacts["pesukim"]["pesukim"]
        parsed_pesukim = artifacts["parsed_pesukim"]["parsed_pesukim"]
        self.assertEqual(len(runtime_pesukim), 3)
        self.assertEqual(len(parsed_pesukim), 3)
        self.assertEqual(parsed_pesukim[2]["ref"]["pasuk"], 3)
        self.assertTrue(parsed_pesukim[2]["token_records"][0]["selected_analysis"])

    def test_parsed_output_remains_compatible_with_current_generator_expectations(self):
        artifacts = build_staged_corpus_from_source(
            self.source_path,
            corpus_id="sample_ingestion_chunk",
            status="parsed",
        )

        for record in artifacts["pesukim"]["pesukim"]:
            analyzed = pasuk_flow_generator.analyze_pasuk(record["text"])
            self.assertEqual(len(analyzed), len(record["tokens"]))

    def test_write_parsed_corpus_artifacts_writes_staged_bundle(self):
        artifacts = build_staged_corpus_from_source(
            self.source_path,
            corpus_id="sample_ingestion_chunk",
            status="parsed",
        )
        output_dir = self.temp_dir / "staged_chunk"
        write_parsed_corpus_artifacts(output_dir, artifacts)

        expected = {
            "pesukim.json",
            "parsed_pesukim.json",
            "word_bank.json",
            "word_occurrences.json",
            "translation_reviews.json",
        }
        self.assertEqual({path.name for path in output_dir.iterdir()}, expected)


if __name__ == "__main__":
    unittest.main()
