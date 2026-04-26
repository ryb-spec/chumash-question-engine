import json
import tempfile
import unittest
from pathlib import Path

from scripts import validate_source_texts as validator


ROOT = Path(__file__).resolve().parents[1]
TSV_PATH = ROOT / "data" / "source_texts" / "bereishis_hebrew_menukad_taamim.tsv"
MANIFEST_PATH = ROOT / "data" / "source_texts" / "source_text_manifest.json"
EXPECTED_SHA256 = "0dedb854e1e8b59fa5dc08f93be5baffe4c1faaa09d00c148c8ef3113b065913"


def load_lines() -> list[str]:
    return TSV_PATH.read_text(encoding="utf-8").splitlines()


def write_temp_tsv(lines: list[str]) -> Path:
    temp_dir = Path(tempfile.mkdtemp())
    path = temp_dir / "bereishis_hebrew_menukad_taamim.tsv"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


class SourceTextsValidationTests(unittest.TestCase):
    def test_validator_can_be_imported(self):
        self.assertTrue(callable(validator.validate_bereishis_source_texts))

    def test_canonical_bereishis_tsv_passes_validation(self):
        summary = validator.validate_bereishis_source_texts()
        self.assertTrue(summary["valid"], summary["blockers"])
        self.assertEqual(summary["status"], "complete")
        self.assertEqual(summary["row_count"], 1533)
        self.assertEqual(summary["perek_count"], 50)
        self.assertEqual(summary["first_ref"], "Bereishis 1:1")
        self.assertEqual(summary["last_ref"], "Bereishis 50:26")
        self.assertEqual(summary["missing_count"], 0)
        self.assertEqual(summary["duplicate_count"], 0)
        self.assertEqual(summary["malformed_count"], 0)
        self.assertEqual(summary["empty_hebrew_count"], 0)
        self.assertEqual(summary["source_issue_count"], 0)

    def test_validator_reports_expected_sha256_for_real_file(self):
        summary = validator.validate_bereishis_source_texts()
        self.assertEqual(summary["sha256"], EXPECTED_SHA256)

    def test_validator_reports_missing_canonical_file_clearly(self):
        summary = validator.validate_bereishis_source_texts(Path("missing_source_text.tsv"))
        self.assertFalse(summary["valid"])
        self.assertEqual(summary["status"], "missing")
        self.assertTrue(any("source file missing" in blocker for blocker in summary["blockers"]))

    def test_validator_fails_clearly_on_bad_header(self):
        lines = load_lines()
        lines[0] = lines[0].replace("source_note", "source_notes")
        summary = validator.validate_bereishis_source_texts(write_temp_tsv(lines))
        self.assertFalse(summary["valid"])
        self.assertEqual(summary["status"], "malformed")
        self.assertTrue(any("header must be exactly" in blocker for blocker in summary["blockers"]))

    def test_validator_fails_clearly_on_duplicate_refs(self):
        lines = load_lines()
        lines.append(lines[1])
        summary = validator.validate_bereishis_source_texts(write_temp_tsv(lines))
        self.assertFalse(summary["valid"])
        self.assertTrue(any("duplicate refs found" in blocker for blocker in summary["blockers"]))

    def test_validator_fails_clearly_on_malformed_ref(self):
        lines = load_lines()
        row = lines[1].split("\t")
        row[3] = "Bereishis one:one"
        lines[1] = "\t".join(row)
        summary = validator.validate_bereishis_source_texts(write_temp_tsv(lines))
        self.assertFalse(summary["valid"])
        self.assertTrue(any("malformed ref" in blocker for blocker in summary["blockers"]))

    def test_validator_fails_clearly_on_blank_hebrew_text_field(self):
        lines = load_lines()
        row = lines[1].split("\t")
        row[4] = ""
        lines[1] = "\t".join(row)
        summary = validator.validate_bereishis_source_texts(write_temp_tsv(lines))
        self.assertFalse(summary["valid"])
        self.assertTrue(any("hebrew_menukad_taamim must not be blank" in blocker for blocker in summary["blockers"]))

    def test_validator_fails_clearly_on_non_bereishis_sefer(self):
        lines = load_lines()
        row = lines[1].split("\t")
        row[0] = "Shemos"
        lines[1] = "\t".join(row)
        summary = validator.validate_bereishis_source_texts(write_temp_tsv(lines))
        self.assertFalse(summary["valid"])
        self.assertTrue(any("sefer must be Bereishis" in blocker for blocker in summary["blockers"]))

    def test_validator_fails_clearly_on_malformed_row(self):
        lines = load_lines()
        lines[1] = "\t".join(lines[1].split("\t")[:-1])
        summary = validator.validate_bereishis_source_texts(write_temp_tsv(lines))
        self.assertFalse(summary["valid"])
        self.assertTrue(any("expected 8 columns" in blocker for blocker in summary["blockers"]))

    def test_validator_fails_clearly_on_missing_ref(self):
        lines = load_lines()
        lines = [line for line in lines if "\tBereishis 4:1\t" not in f"\t{line}\t"]
        summary = validator.validate_bereishis_source_texts(write_temp_tsv(lines))
        self.assertFalse(summary["valid"])
        self.assertEqual(summary["status"], "malformed")
        self.assertTrue(any("missing refs" in blocker and "Bereishis 4:1" in blocker for blocker in summary["blockers"]))

    def test_validator_fails_clearly_on_extra_ref(self):
        lines = load_lines()
        row = lines[1].split("\t")
        row[1] = "51"
        row[2] = "1"
        row[3] = "Bereishis 51:1"
        lines.append("\t".join(row))
        summary = validator.validate_bereishis_source_texts(write_temp_tsv(lines))
        self.assertFalse(summary["valid"])
        self.assertTrue(any("extra refs" in blocker and "Bereishis 51:1" in blocker for blocker in summary["blockers"]))

    def test_validator_fails_clearly_when_row_does_not_end_with_sof_pasuk(self):
        lines = load_lines()
        row = lines[1].split("\t")
        row[4] = row[4].removesuffix("\u05c3")
        lines[1] = "\t".join(row)
        summary = validator.validate_bereishis_source_texts(write_temp_tsv(lines))
        self.assertFalse(summary["valid"])
        self.assertTrue(any("must end with sof pasuk" in blocker for blocker in summary["blockers"]))

    def test_manifest_shape_if_present(self):
        self.assertTrue(MANIFEST_PATH.exists())
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], "0.1")
        self.assertIn("files", manifest)
        self.assertIsInstance(manifest["files"], list)
        self.assertGreaterEqual(len(manifest["files"]), 1)
        entry = manifest["files"][0]
        for field in [
            "sefer",
            "file_path",
            "status",
            "expected_scope",
            "actual_scope",
            "row_count",
            "first_ref",
            "last_ref",
            "validation_status",
            "source_label",
            "source_notes",
            "safe_for_extraction_planning",
            "safe_for_runtime",
            "blockers",
            "next_action",
        ]:
            self.assertIn(field, entry)


if __name__ == "__main__":
    unittest.main()
