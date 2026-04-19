import json
import unittest

import assessment_scope


class SourceCorpusBlock131To29Tests(unittest.TestCase):
    def test_new_source_block_matches_existing_source_schema_and_ordering(self):
        existing_path = assessment_scope.repo_path("data", "source", "bereishis_1_1_to_4_20.json")
        new_path = assessment_scope.repo_path("data", "source", "bereishis_1_31_to_2_9.json")

        existing = json.loads(existing_path.read_text(encoding="utf-8"))
        new = json.loads(new_path.read_text(encoding="utf-8"))

        self.assertEqual(list(new.keys()), list(existing.keys()))
        self.assertEqual(list(new["metadata"].keys()), list(existing["metadata"].keys()))
        self.assertEqual(list(new["pesukim"][0].keys()), list(existing["pesukim"][0].keys()))

    def test_new_source_block_is_contiguous_after_bereishis_1_30(self):
        existing_path = assessment_scope.repo_path("data", "source", "bereishis_1_1_to_4_20.json")
        new_path = assessment_scope.repo_path("data", "source", "bereishis_1_31_to_2_9.json")

        existing = json.loads(existing_path.read_text(encoding="utf-8"))
        new = json.loads(new_path.read_text(encoding="utf-8"))

        self.assertEqual(existing["pesukim"][-1]["sefer"], "Bereishis")
        self.assertEqual(existing["pesukim"][-1]["perek"], 1)
        self.assertEqual(existing["pesukim"][-1]["pasuk"], 30)

        self.assertEqual(new["pesukim"][0]["sefer"], "Bereishis")
        self.assertEqual(new["pesukim"][0]["perek"], 1)
        self.assertEqual(new["pesukim"][0]["pasuk"], 31)

    def test_new_source_block_contains_complete_ordered_target_range(self):
        new_path = assessment_scope.repo_path("data", "source", "bereishis_1_31_to_2_9.json")
        new = json.loads(new_path.read_text(encoding="utf-8"))

        expected_refs = [
            (1, 31),
            (2, 1),
            (2, 2),
            (2, 3),
            (2, 4),
            (2, 5),
            (2, 6),
            (2, 7),
            (2, 8),
            (2, 9),
        ]

        actual_refs = [(record["perek"], record["pasuk"]) for record in new["pesukim"]]

        self.assertEqual(new["metadata"]["title"], "Bereishis source text")
        self.assertEqual(new["metadata"]["range"], "1:31-2:9")
        self.assertEqual(new["metadata"]["format"], "sefer,perek,pasuk,text")
        self.assertEqual(actual_refs, expected_refs)
        self.assertTrue(all(record["text"] for record in new["pesukim"]))


if __name__ == "__main__":
    unittest.main()
