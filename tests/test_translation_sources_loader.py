import unittest

import translation_sources_loader as loader


class TranslationSourcesLoaderTests(unittest.TestCase):
    def test_registry_loads(self):
        registry = loader.load_translation_registry()
        self.assertEqual(registry["runtime_status"], "not_runtime_active")
        self.assertEqual(registry["production_status"], "not_production_ready")

    def test_available_versions_are_koren_and_metsudah(self):
        self.assertEqual(sorted(loader.get_available_translation_versions()), ["koren", "metsudah"])

    def test_loader_loads_full_translations(self):
        koren_rows = loader.load_bereishis_translation("koren")
        metsudah_rows = loader.load_bereishis_translation("metsudah")
        self.assertEqual(len(koren_rows), 1533)
        self.assertEqual(len(metsudah_rows), 1533)

    def test_loader_can_get_genesis_1_1(self):
        koren_row = loader.get_translation_by_ref("koren", "Genesis 1:1")
        metsudah_row = loader.get_translation_by_ref("metsudah", "Genesis 1:1")
        self.assertEqual(koren_row["translation_version_key"], "koren")
        self.assertEqual(metsudah_row["translation_version_key"], "metsudah")
        self.assertTrue(koren_row["translation_text"])
        self.assertTrue(metsudah_row["translation_text"])

    def test_loader_does_not_silently_fallback_between_versions(self):
        with self.assertRaises(KeyError):
            loader.get_translation_by_ref("koren", "Genesis 35:30")

    def test_license_status_lookup(self):
        self.assertEqual(loader.get_translation_license_status("koren"), "needs_license_review")
        self.assertEqual(loader.get_translation_license_status("metsudah"), "needs_license_review")

    def test_compare_translations_by_ref(self):
        comparison = loader.compare_translations_by_ref("Genesis 1:1")
        self.assertEqual(sorted(comparison.keys()), ["koren", "metsudah"])
        self.assertEqual(comparison["koren"]["translation_version_key"], "koren")
        self.assertEqual(comparison["metsudah"]["translation_version_key"], "metsudah")


if __name__ == "__main__":
    unittest.main()
