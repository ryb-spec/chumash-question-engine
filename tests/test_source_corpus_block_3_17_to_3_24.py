import json
import unittest

import assessment_scope


class SourceCorpusBlock317To324Tests(unittest.TestCase):
    def test_new_source_block_is_contiguous_after_bereishis_3_16(self):
        previous_path = assessment_scope.repo_path("data", "source", "bereishis_3_9_to_3_16.json")
        new_path = assessment_scope.repo_path("data", "source", "bereishis_3_17_to_3_24.json")

        previous = json.loads(previous_path.read_text(encoding="utf-8"))
        new = json.loads(new_path.read_text(encoding="utf-8"))

        self.assertEqual(previous["pesukim"][-1]["sefer"], "Bereishis")
        self.assertEqual(previous["pesukim"][-1]["perek"], 3)
        self.assertEqual(previous["pesukim"][-1]["pasuk"], 16)

        self.assertEqual(new["pesukim"][0]["sefer"], "Bereishis")
        self.assertEqual(new["pesukim"][0]["perek"], 3)
        self.assertEqual(new["pesukim"][0]["pasuk"], 17)

    def test_new_source_block_matches_existing_source_schema_and_ordering(self):
        existing_path = assessment_scope.repo_path("data", "source", "bereishis_3_9_to_3_16.json")
        new_path = assessment_scope.repo_path("data", "source", "bereishis_3_17_to_3_24.json")

        existing = json.loads(existing_path.read_text(encoding="utf-8"))
        new = json.loads(new_path.read_text(encoding="utf-8"))

        self.assertEqual(list(new.keys()), list(existing.keys()))
        self.assertEqual(list(new["metadata"].keys()), list(existing["metadata"].keys()))
        self.assertEqual(list(new["pesukim"][0].keys()), list(existing["pesukim"][0].keys()))

    def test_new_source_block_contains_complete_ordered_target_range(self):
        new_path = assessment_scope.repo_path("data", "source", "bereishis_3_17_to_3_24.json")
        new = json.loads(new_path.read_text(encoding="utf-8"))

        expected_refs = [
            (3, 17),
            (3, 18),
            (3, 19),
            (3, 20),
            (3, 21),
            (3, 22),
            (3, 23),
            (3, 24),
        ]

        actual_refs = [(record["perek"], record["pasuk"]) for record in new["pesukim"]]

        self.assertEqual(new["metadata"]["title"], "Bereishis source text")
        self.assertEqual(new["metadata"]["range"], "3:17-3:24")
        self.assertEqual(new["metadata"]["format"], "sefer,perek,pasuk,text")
        self.assertEqual(actual_refs, expected_refs)
        self.assertTrue(all(record["text"] for record in new["pesukim"]))


if __name__ == "__main__":
    unittest.main()
