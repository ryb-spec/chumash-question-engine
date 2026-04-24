import tempfile
import unittest
from pathlib import Path

from scripts import validate_source_texts as validator


ROOT = Path(__file__).resolve().parents[1]
TSV_PATH = ROOT / "data" / "source_texts" / "bereishis_hebrew_menukad_taamim.tsv"
EXPECTED_SHA256 = "a5fc8a32ff7d01c6c557e361d0c09a5a8d2267140dc4ba2e11a821bac4985f8d"


def load_lines() -> list[str]:
    return TSV_PATH.read_text(encoding="utf-8").splitlines()


def write_temp_tsv(lines: list[str]) -> Path:
    temp_dir = Path(tempfile.mkdtemp())
    path = temp_dir / "bereishis_hebrew_menukad_taamim.tsv"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


class SourceTextsValidationTests(unittest.TestCase):
    def test_canonical_bereishis_tsv_passes_validation(self):
        summary = validator.validate_bereishis_source_texts()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["row_count"], 1534)
        self.assertEqual(summary["perek_count"], 50)
        self.assertEqual(summary["first_ref"], "Bereishis 1:1")
        self.assertEqual(summary["last_ref"], "Bereishis 50:26")

    def test_validator_reports_expected_sha256_for_real_file(self):
        summary = validator.validate_bereishis_source_texts()
        self.assertEqual(summary["sha256"], EXPECTED_SHA256)

    def test_validator_fails_clearly_on_bad_header(self):
        lines = load_lines()
        lines[0] = lines[0].replace("source_note", "source_notes")
        summary = validator.validate_bereishis_source_texts(write_temp_tsv(lines))
        self.assertFalse(summary["valid"])
        self.assertTrue(any("header must be exactly" in error for error in summary["errors"]))

    def test_validator_fails_clearly_on_blank_hebrew_text_field(self):
        lines = load_lines()
        row = lines[1].split("\t")
        row[4] = ""
        lines[1] = "\t".join(row)
        summary = validator.validate_bereishis_source_texts(write_temp_tsv(lines))
        self.assertFalse(summary["valid"])
        self.assertTrue(any("hebrew_menukad_taamim must not be blank" in error for error in summary["errors"]))

    def test_validator_fails_clearly_on_duplicate_refs(self):
        lines = load_lines()
        lines.append(lines[1])
        summary = validator.validate_bereishis_source_texts(write_temp_tsv(lines))
        self.assertFalse(summary["valid"])
        self.assertTrue(any("duplicate refs found" in error for error in summary["errors"]))

    def test_validator_fails_clearly_on_missing_ref(self):
        lines = load_lines()
        lines = [line for line in lines if "\tBereishis 4:1\t" not in f"\t{line}\t"]
        summary = validator.validate_bereishis_source_texts(write_temp_tsv(lines))
        self.assertFalse(summary["valid"])
        self.assertTrue(any("missing refs" in error and "Bereishis 4:1" in error for error in summary["errors"]))

    def test_validator_fails_clearly_on_extra_ref(self):
        lines = load_lines()
        row = lines[1].split("\t")
        row[1] = "51"
        row[2] = "1"
        row[3] = "Bereishis 51:1"
        lines.append("\t".join(row))
        summary = validator.validate_bereishis_source_texts(write_temp_tsv(lines))
        self.assertFalse(summary["valid"])
        self.assertTrue(any("extra refs" in error and "Bereishis 51:1" in error for error in summary["errors"]))

    def test_validator_fails_clearly_when_row_does_not_end_with_sof_pasuk(self):
        lines = load_lines()
        row = lines[1].split("\t")
        row[4] = row[4].removesuffix("׃")
        lines[1] = "\t".join(row)
        summary = validator.validate_bereishis_source_texts(write_temp_tsv(lines))
        self.assertFalse(summary["valid"])
        self.assertTrue(any("must end with sof pasuk" in error for error in summary["errors"]))


if __name__ == "__main__":
    unittest.main()
