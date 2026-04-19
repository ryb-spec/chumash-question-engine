import unittest
from pathlib import Path

from assessment_scope import repo_path
from foundation_resources import (
    FOUNDATION_LAYER_VALUES,
    FOUNDATION_STATUS_VALUES,
    FOUNDATIONS_MANIFEST_PATH,
    foundation_resource_names,
    foundation_resource_path,
    get_foundation_resource_metadata,
    load_foundation_manifest,
    load_foundation_resource,
    validate_all_foundation_resources,
    validate_foundation_manifest,
)


EXPECTED_RESOURCE_NAMES = (
    "canonical_skill_crosswalk_json",
    "canonical_skill_crosswalk_csv",
    "assessment_blueprint",
    "grammar_paradigms",
    "high_frequency_lexicon",
    "teacher_ops_workflow",
)


class FoundationResourcesTests(unittest.TestCase):
    def test_manifest_exists_and_declares_expected_resources(self):
        self.assertTrue(FOUNDATIONS_MANIFEST_PATH.exists())
        manifest = load_foundation_manifest()
        self.assertEqual(tuple(resource["resource_name"] for resource in manifest["resources"]), EXPECTED_RESOURCE_NAMES)

    def test_manifest_is_structurally_valid(self):
        self.assertEqual(validate_foundation_manifest(), [])
        manifest = load_foundation_manifest()
        self.assertEqual(tuple(manifest["metadata"]["layer_values"]), FOUNDATION_LAYER_VALUES)
        self.assertEqual(tuple(manifest["metadata"]["status_values"]), FOUNDATION_STATUS_VALUES)

    def test_resource_files_exist_in_permanent_locations(self):
        for resource_name in foundation_resource_names():
            path = foundation_resource_path(resource_name)
            self.assertTrue(path.exists(), resource_name)
            self.assertTrue(path.is_file(), resource_name)

    def test_manifest_records_point_back_to_incoming_sources(self):
        for resource_name in foundation_resource_names():
            metadata = get_foundation_resource_metadata(resource_name)
            self.assertTrue(repo_path(metadata["source"]).exists(), resource_name)
            self.assertEqual(metadata["status"], "validated_seed")
            self.assertIn(metadata["layer"], FOUNDATION_LAYER_VALUES)
            self.assertTrue(metadata["intended_use"])

    def test_json_and_csv_crosswalk_views_stay_consistent(self):
        crosswalk_json = load_foundation_resource("canonical_skill_crosswalk_json")
        crosswalk_csv = load_foundation_resource("canonical_skill_crosswalk_csv")
        json_ids = [skill["canonical_skill_id"] for skill in crosswalk_json["skills"]]
        csv_ids = [row["canonical_skill_id"] for row in crosswalk_csv]
        self.assertEqual(json_ids, csv_ids)

    def test_loader_returns_expected_shapes(self):
        blueprint = load_foundation_resource("assessment_blueprint")
        paradigms = load_foundation_resource("grammar_paradigms")
        lexicon = load_foundation_resource("high_frequency_lexicon")
        teacher_ops = load_foundation_resource("teacher_ops_workflow")

        self.assertIn("recommended_local_blueprint", blueprint)
        self.assertIn("verb_paradigm_example", paradigms)
        self.assertIn("seed_entries", lexicon)
        self.assertIn("deployment_cycle", teacher_ops)

    def test_all_resource_validators_return_clean_results(self):
        self.assertEqual(
            validate_all_foundation_resources(),
            {resource_name: [] for resource_name in EXPECTED_RESOURCE_NAMES},
        )

    def test_seed_package_readme_marks_itself_as_guidance_not_runtime_truth(self):
        readme = Path("docs/chumash_foundations_package_seed.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("preserved seed-package guide", readme)
        self.assertIn("skill_catalog.py", readme)
        self.assertNotIn(
            "Adopt `canonical_skill_crosswalk_seed.json` as the first pass of `skill_catalog.json`.",
            readme,
        )


if __name__ == "__main__":
    unittest.main()
