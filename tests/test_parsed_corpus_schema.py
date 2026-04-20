import unittest

from torah_parser.export_bank import build_parsed_corpus_artifacts


SAMPLE_SOURCE_CORPUS = {
    "metadata": {
        "title": "Sample Bereishis Source",
        "range": "1:1-1:2",
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
            "text": "וְהָאָרֶץ הָיְתָה תֹהוּ וָבֹהוּ",
        },
    ],
}


class ParsedCorpusSchemaTests(unittest.TestCase):
    def test_parsed_corpus_records_have_expected_schema(self):
        artifacts = build_parsed_corpus_artifacts(
            SAMPLE_SOURCE_CORPUS,
            corpus_id="sample_bereishis_1_1_to_1_2",
        )

        parsed = artifacts["parsed_pesukim"]["parsed_pesukim"]
        self.assertEqual(len(parsed), 2)
        first = parsed[0]

        self.assertEqual(
            sorted(first.keys()),
            ["pasuk_id", "ref", "role_layer", "source_ref", "text", "token_records", "tokens"],
        )
        self.assertIn(first["role_layer"]["status"], {"resolved", "no_main_verb", "ambiguous_main_verbs"})
        self.assertTrue(first["token_records"])
        token = first["token_records"][0]
        self.assertEqual(
            sorted(token.keys()),
            [
                "analysis_count",
                "analysis_index",
                "normalized",
                "pasuk_id",
                "role_data",
                "selected_analysis",
                "source_ref",
                "surface",
                "token_index",
            ],
        )
        self.assertEqual(token["role_data"]["token_index"], 0)
        self.assertEqual(token["role_data"]["token"], token["surface"])

    def test_source_metadata_is_preserved_correctly(self):
        artifacts = build_parsed_corpus_artifacts(
            SAMPLE_SOURCE_CORPUS,
            corpus_id="sample_bereishis_1_1_to_1_2",
            source_files=["data/source/sample.json"],
        )

        metadata = artifacts["parsed_pesukim"]["metadata"]
        self.assertEqual(metadata["sefer"], "Bereishis")
        self.assertEqual(metadata["range"]["start"], {"sefer": "Bereishis", "perek": 1, "pasuk": 1})
        self.assertEqual(metadata["range"]["end"], {"sefer": "Bereishis", "perek": 1, "pasuk": 2})
        self.assertEqual(metadata["pesukim_count"], 2)
        self.assertEqual(metadata["source_files"], ["data/source/sample.json"])

    def test_original_text_is_preserved_alongside_normalized_analysis(self):
        artifacts = build_parsed_corpus_artifacts(SAMPLE_SOURCE_CORPUS)

        first = artifacts["parsed_pesukim"]["parsed_pesukim"][0]
        first_token = first["token_records"][0]
        self.assertEqual(first["text"], SAMPLE_SOURCE_CORPUS["pesukim"][0]["text"])
        self.assertEqual(first_token["surface"], "בְּרֵאשִׁית")
        self.assertEqual(first_token["normalized"], "בראשית")


if __name__ == "__main__":
    unittest.main()
