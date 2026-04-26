import csv
import json
import subprocess
import sys
import unittest
from pathlib import Path

from scripts import validate_bereishis_translations as validator


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_HEBREW_TSV = ROOT / "data" / "source_texts" / "bereishis_hebrew_menukad_taamim.tsv"
OUTPUT_DIR = ROOT / "data" / "source_texts" / "translations" / "sefaria"
MANIFEST_PATH = OUTPUT_DIR / "bereishis_english_translations_manifest.json"
DISCOVERY_REPORT_PATH = OUTPUT_DIR / "sefaria_english_versions_genesis_report.json"
LICENSE_REPORT_PATH = OUTPUT_DIR / "bereishis_english_translation_license_report.md"
ALIGNMENT_REPORT_PATH = OUTPUT_DIR / "bereishis_english_translation_alignment_report.md"
FETCH_REPORT_PATH = OUTPUT_DIR / "bereishis_english_translation_fetch_report.json"
LICENSE_REVIEW_MATRIX_PATH = OUTPUT_DIR / "bereishis_english_translation_license_review_matrix.json"
HUMAN_REVIEW_PACKET_PATH = OUTPUT_DIR / "bereishis_english_translation_human_review_packet.md"
TRANSLATION_REGISTRY_PATH = ROOT / "data" / "source_texts" / "translations" / "translation_sources_registry.json"
RECONCILIATION_REPORT_MD_PATH = ROOT / "data" / "source_texts" / "reports" / "bereishis_hebrew_source_reconciliation_report.md"
README_PATH = OUTPUT_DIR / "README.md"
FETCH_SCRIPT = ROOT / "scripts" / "fetch_sefaria_bereishis_translations.py"
VALIDATOR_SCRIPT = ROOT / "scripts" / "validate_bereishis_translations.py"
JSONL_PATHS = {
    "koren": OUTPUT_DIR / "bereishis_english_koren.jsonl",
    "metsudah": OUTPUT_DIR / "bereishis_english_metsudah.jsonl",
}
FORBIDDEN_STATUSES = {
    "approved",
    "reviewed",
    "production",
    "production_ready",
    "runtime_active",
    "active",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                rows.append(json.loads(stripped))
    return rows


def load_canonical_refs():
    with CANONICAL_HEBREW_TSV.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return {f"Genesis {row['perek']}:{row['pasuk']}": row["ref"] for row in reader}


class BereishisTranslationSourcesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load_json(MANIFEST_PATH)
        cls.discovery = load_json(DISCOVERY_REPORT_PATH)
        cls.fetch_report = load_json(FETCH_REPORT_PATH)
        cls.canonical_refs = load_canonical_refs()

    def test_fetch_script_exists(self):
        self.assertTrue(FETCH_SCRIPT.exists())

    def test_validator_script_exists(self):
        self.assertTrue(VALIDATOR_SCRIPT.exists())

    def test_required_reports_exist(self):
        for path in [
            MANIFEST_PATH,
            DISCOVERY_REPORT_PATH,
            LICENSE_REPORT_PATH,
            ALIGNMENT_REPORT_PATH,
            FETCH_REPORT_PATH,
            LICENSE_REVIEW_MATRIX_PATH,
            HUMAN_REVIEW_PACKET_PATH,
            TRANSLATION_REGISTRY_PATH,
            RECONCILIATION_REPORT_MD_PATH,
            README_PATH,
        ]:
            with self.subTest(path=path):
                self.assertTrue(path.exists())

    def test_canonical_hebrew_source_matches_reconciled_expectation(self):
        self.assertEqual(len(self.canonical_refs), 1533)
        self.assertNotIn("Genesis 35:30", self.canonical_refs)

    def test_manifest_records_explicit_koren_and_metsudah_statuses(self):
        for target_key in ["koren", "metsudah"]:
            with self.subTest(target_key=target_key):
                self.assertIn(target_key, self.manifest["selected_versions"])
                self.assertIn(target_key, self.manifest["license_status_by_version"])
                self.assertTrue(self.manifest["selected_versions"][target_key]["pipeline_status"])
        self.assertEqual(self.manifest["expected_total_refs"], 1533)
        self.assertEqual(self.manifest["integration_status"], "source_ready_license_pending")

    def test_discovery_report_records_exact_titles_if_found(self):
        chosen = self.discovery["chosen_exact_version_titles"]
        self.assertEqual(chosen["koren"], self.manifest["exact_version_titles_used"]["koren"])
        self.assertEqual(chosen["metsudah"], self.manifest["exact_version_titles_used"]["metsudah"])

    def test_fallback_filling_is_disabled(self):
        self.assertEqual(self.fetch_report["request_defaults"]["fill_in_missing_segments"], 0)
        for target_key in ["koren", "metsudah"]:
            self.assertFalse(self.fetch_report["versions"][target_key]["missing_segment_warning_detected"])

    def test_jsonl_rows_parse_and_align_when_present(self):
        for target_key, path in JSONL_PATHS.items():
            with self.subTest(target_key=target_key):
                if not path.exists():
                    self.assertIn(
                        self.manifest["selected_versions"][target_key]["pipeline_status"],
                        {
                            "blocked_version_not_found",
                            "blocked_license_unclear",
                            "blocked_fetch_error",
                            "version_discovered",
                        },
                    )
                    continue
                rows = load_jsonl(path)
                self.assertEqual(len(rows), self.manifest["row_counts_by_version"][target_key])
                self.assertEqual(len(rows), len(self.canonical_refs))
                refs = []
                titles = set()
                for row in rows:
                    self.assertEqual(row["translation_version_key"], target_key)
                    self.assertNotIn(row["status"], FORBIDDEN_STATUSES)
                    self.assertIn(row["ref"], self.canonical_refs)
                    self.assertEqual(row["hebrew_ref"], self.canonical_refs[row["ref"]])
                    self.assertIn("license", row)
                    self.assertIn("license_note", row)
                    self.assertIsInstance(row["provenance"], dict)
                    self.assertIn("fill_in_missing_segments=0", row["source_api_endpoint"])
                    refs.append(row["ref"])
                    titles.add(row["translation_version_title"])
                self.assertEqual(len(refs), len(set(refs)))
                self.assertEqual(len(titles), 1)

    def test_missing_refs_are_reported_not_hidden(self):
        for target_key, path in JSONL_PATHS.items():
            with self.subTest(target_key=target_key):
                rows = load_jsonl(path) if path.exists() else []
                actual_missing = sorted(set(self.canonical_refs) - {row["ref"] for row in rows})
                self.assertEqual(actual_missing, sorted(self.manifest["missing_refs_by_version"][target_key]))
                self.assertEqual(actual_missing, sorted(self.fetch_report["versions"][target_key]["missing_refs"]))
                self.assertEqual(actual_missing, [])

    def test_no_forbidden_statuses_appear_in_manifest(self):
        self.assertEqual(self.manifest["production_status"], "not_production_ready")
        self.assertEqual(self.manifest["runtime_status"], "not_runtime_active")
        for target_key, payload in self.manifest["selected_versions"].items():
            with self.subTest(target_key=target_key):
                self.assertNotIn(payload["pipeline_status"], FORBIDDEN_STATUSES)

    def test_license_review_matrix_exists_and_requires_human_review(self):
        matrix = load_json(LICENSE_REVIEW_MATRIX_PATH)
        self.assertEqual(len(matrix), 2)
        for entry in matrix:
            self.assertEqual(entry["status"], "needs_license_review")
            self.assertTrue(entry["human_review_required"])

    def test_translation_registry_exists_and_is_not_runtime_active(self):
        registry = load_json(TRANSLATION_REGISTRY_PATH)
        self.assertEqual(registry["runtime_status"], "not_runtime_active")
        self.assertEqual(registry["production_status"], "not_production_ready")
        self.assertEqual(registry["integration_status"], "source_ready_license_pending")
        self.assertEqual(len(registry["available_translation_versions"]), 2)

    def test_validator_passes(self):
        summary = validator.validate_bereishis_translations()
        self.assertTrue(summary["valid"], summary["errors"])

    def test_fetch_script_is_rerunnable(self):
        result = subprocess.run(
            [
                sys.executable,
                str(FETCH_SCRIPT),
                "--target",
                "koren",
                "--target",
                "metsudah",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        summary = validator.validate_bereishis_translations()
        self.assertTrue(summary["valid"], summary["errors"])


if __name__ == "__main__":
    unittest.main()
