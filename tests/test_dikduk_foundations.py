import json
import unittest

from foundation_dikduk import (
    DIKDUK_COLLECTION_CONFIG,
    DIKDUK_JSON_FILENAMES,
    DIKDUK_FOUNDATIONS_DIR,
    INFERRED_STANDARDS_CONFIDENCE_VALUES,
    INFERRED_STANDARDS_FRAMEWORK,
    dikduk_json_paths,
    dikduk_schema_paths,
    dikduk_seed_collection_names,
    load_dikduk_schema_map,
    load_dikduk_seed_map,
    load_unresolved_candidates,
    validate_dikduk_foundations,
)


class DikdukFoundationsTests(unittest.TestCase):
    def test_all_expected_package_files_exist(self):
        self.assertTrue(DIKDUK_FOUNDATIONS_DIR.exists())
        self.assertEqual(
            sorted(path.name for path in DIKDUK_FOUNDATIONS_DIR.iterdir() if path.is_file()),
            sorted(DIKDUK_JSON_FILENAMES),
        )

    def test_every_json_file_parses(self):
        for filename, path in dikduk_json_paths().items():
            with self.subTest(filename=filename):
                with path.open("r", encoding="utf-8") as file:
                    json.load(file)

    def test_schema_files_are_json_objects(self):
        schemas = load_dikduk_schema_map()
        self.assertEqual(sorted(schemas.keys()), sorted(dikduk_schema_paths().keys()))
        for schema_name, schema in schemas.items():
            with self.subTest(schema_name=schema_name):
                self.assertIsInstance(schema, dict)
                self.assertEqual(schema.get("type"), "object")
                self.assertIsInstance(schema.get("properties"), dict)
                self.assertIsInstance(schema.get("required"), list)

    def test_seed_files_match_schema_and_resolve_links(self):
        self.assertEqual(validate_dikduk_foundations(), [])

    def test_seed_collections_exclude_unresolved_candidates(self):
        self.assertEqual(
            sorted(dikduk_seed_collection_names()),
            sorted(DIKDUK_COLLECTION_CONFIG.keys()),
        )
        self.assertNotIn("unresolved_candidates", dikduk_seed_collection_names())
        self.assertEqual(
            sorted(load_dikduk_seed_map().keys()),
            sorted(DIKDUK_COLLECTION_CONFIG.keys()),
        )

    def test_unresolved_candidates_remains_separate_non_seed_data(self):
        unresolved = load_unresolved_candidates()
        self.assertIsInstance(unresolved, dict)
        self.assertEqual(
            sorted(unresolved.keys()),
            ["examples", "morphology_patterns", "rules", "standards", "vocabulary"],
        )
        self.assertNotIn("unresolved_candidates", load_dikduk_seed_map())

    def test_no_duplicate_ids_exist_within_seed_files(self):
        seed_map = load_dikduk_seed_map()
        for collection_name, records in seed_map.items():
            config = DIKDUK_COLLECTION_CONFIG[collection_name]
            id_field = config["id_field"]
            with self.subTest(collection_name=collection_name):
                ids = [record[id_field] for record in records]
                self.assertEqual(len(ids), len(set(ids)))

    def test_inferred_standards_mappings_stay_clearly_labeled(self):
        standards = load_dikduk_seed_map()["standards_mappings"]
        self.assertTrue(standards)
        for record in standards:
            self.assertEqual(record["standard_framework"], INFERRED_STANDARDS_FRAMEWORK)
            self.assertIn(record["confidence"], INFERRED_STANDARDS_CONFIDENCE_VALUES)
            self.assertNotEqual(record["confidence"], "explicit")


if __name__ == "__main__":
    unittest.main()
