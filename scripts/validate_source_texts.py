from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_BEREISHIS_TSV = ROOT / "data" / "source_texts" / "bereishis_hebrew_menukad_taamim.tsv"
EXPECTED_HEADER = [
    "sefer",
    "perek",
    "pasuk",
    "ref",
    "hebrew_menukad_taamim",
    "source",
    "url",
    "source_note",
]
EXPECTED_BEREISHIS_CHAPTER_COUNTS = {
    1: 31,
    2: 25,
    3: 24,
    4: 26,
    5: 32,
    6: 22,
    7: 24,
    8: 22,
    9: 29,
    10: 32,
    11: 32,
    12: 20,
    13: 18,
    14: 24,
    15: 21,
    16: 16,
    17: 27,
    18: 33,
    19: 38,
    20: 18,
    21: 34,
    22: 24,
    23: 20,
    24: 67,
    25: 34,
    26: 35,
    27: 46,
    28: 22,
    29: 35,
    30: 43,
    31: 54,
    32: 33,
    33: 20,
    34: 31,
    35: 30,
    36: 43,
    37: 36,
    38: 30,
    39: 23,
    40: 23,
    41: 57,
    42: 38,
    43: 34,
    44: 34,
    45: 28,
    46: 34,
    47: 31,
    48: 22,
    49: 33,
    50: 26,
}
SPOT_CHECK_REFS = (
    "Bereishis 1:1",
    "Bereishis 4:1",
    "Bereishis 4:16",
    "Bereishis 4:17",
    "Bereishis 50:26",
)
SOURCE_NOTE_REQUIRED_PHRASE = "Miqra according to the Masorah"


def build_expected_refs() -> list[str]:
    refs: list[str] = []
    for perek, pasuk_count in EXPECTED_BEREISHIS_CHAPTER_COUNTS.items():
        for pasuk in range(1, pasuk_count + 1):
            refs.append(f"Bereishis {perek}:{pasuk}")
    return refs


def sha256_for_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_bereishis_source_texts(path: Path = CANONICAL_BEREISHIS_TSV) -> dict:
    errors: list[str] = []
    rows: list[dict[str, str]] = []
    actual_refs: list[str] = []
    path = Path(path)

    if not path.exists():
        errors.append(f"source file missing: {path.as_posix()}")
        return {
            "valid": False,
            "source_file_path": path.as_posix(),
            "row_count": 0,
            "perek_count": 0,
            "first_ref": None,
            "last_ref": None,
            "sha256": None,
            "errors": errors,
        }

    try:
        raw_text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        errors.append(f"{path.as_posix()}: invalid UTF-8 ({error})")
        return {
            "valid": False,
            "source_file_path": path.as_posix(),
            "row_count": 0,
            "perek_count": 0,
            "first_ref": None,
            "last_ref": None,
            "sha256": None,
            "errors": errors,
        }

    lines = raw_text.splitlines()
    if not lines:
        errors.append(f"{path.as_posix()}: file is empty")
        return {
            "valid": False,
            "source_file_path": path.as_posix(),
            "row_count": 0,
            "perek_count": 0,
            "first_ref": None,
            "last_ref": None,
            "sha256": sha256_for_path(path),
            "errors": errors,
        }

    header = next(csv.reader([lines[0]], delimiter="\t"))
    if header != EXPECTED_HEADER:
        errors.append(
            f"{path.as_posix()}: header must be exactly {EXPECTED_HEADER}, got {header}"
        )

    reader = csv.reader(lines[1:], delimiter="\t")
    seen_refs: set[str] = set()
    duplicate_refs: set[str] = set()
    perakim: set[int] = set()

    for row_number, row in enumerate(reader, start=2):
        if len(row) != 8:
            errors.append(f"{path.as_posix()}:{row_number}: expected 8 columns, got {len(row)}")
            continue

        record = dict(zip(EXPECTED_HEADER, row, strict=True))
        rows.append(record)

        sefer = record["sefer"]
        if sefer != "Bereishis":
            errors.append(f"{path.as_posix()}:{row_number}: sefer must be Bereishis, got {sefer!r}")

        try:
            perek = int(record["perek"])
            if perek <= 0:
                raise ValueError
        except ValueError:
            errors.append(f"{path.as_posix()}:{row_number}: perek must be a positive integer")
            perek = None

        try:
            pasuk = int(record["pasuk"])
            if pasuk <= 0:
                raise ValueError
        except ValueError:
            errors.append(f"{path.as_posix()}:{row_number}: pasuk must be a positive integer")
            pasuk = None

        if perek is not None:
            perakim.add(perek)

        if perek is not None and pasuk is not None:
            expected_ref = f"Bereishis {perek}:{pasuk}"
            if record["ref"] != expected_ref:
                errors.append(
                    f"{path.as_posix()}:{row_number}: ref must match {expected_ref!r}, got {record['ref']!r}"
                )

        hebrew_text = record["hebrew_menukad_taamim"]
        if not hebrew_text.strip():
            errors.append(f"{path.as_posix()}:{row_number}: hebrew_menukad_taamim must not be blank")
        if "\t" in hebrew_text:
            errors.append(f"{path.as_posix()}:{row_number}: hebrew_menukad_taamim must not contain embedded tabs")
        if hebrew_text and not hebrew_text.endswith("׃"):
            errors.append(f"{path.as_posix()}:{row_number}: hebrew_menukad_taamim must end with sof pasuk ׃")

        if not record["source"].strip():
            errors.append(f"{path.as_posix()}:{row_number}: source must not be blank")
        elif record["source"] != "Sefaria":
            errors.append(f"{path.as_posix()}:{row_number}: source must be Sefaria, got {record['source']!r}")

        if not record["url"].strip():
            errors.append(f"{path.as_posix()}:{row_number}: url must not be blank")

        source_note = record["source_note"]
        if not source_note.strip():
            errors.append(f"{path.as_posix()}:{row_number}: source_note must not be blank")
        elif SOURCE_NOTE_REQUIRED_PHRASE not in source_note:
            errors.append(
                f"{path.as_posix()}:{row_number}: source_note must include {SOURCE_NOTE_REQUIRED_PHRASE!r}"
            )

        ref = record["ref"]
        actual_refs.append(ref)
        if ref in seen_refs:
            duplicate_refs.add(ref)
        seen_refs.add(ref)

    if duplicate_refs:
        errors.append(
            f"{path.as_posix()}: duplicate refs found: {sorted(duplicate_refs)}"
        )

    expected_refs = build_expected_refs()
    expected_ref_set = set(expected_refs)
    actual_ref_set = set(actual_refs)
    missing_refs = sorted(expected_ref_set - actual_ref_set)
    extra_refs = sorted(actual_ref_set - expected_ref_set)

    if len(rows) != 1534:
        errors.append(f"{path.as_posix()}: expected 1534 data rows, got {len(rows)}")
    if len(perakim) != 50:
        errors.append(f"{path.as_posix()}: expected 50 perakim, got {len(perakim)}")
    if actual_refs:
        if actual_refs[0] != "Bereishis 1:1":
            errors.append(f"{path.as_posix()}: first ref must be 'Bereishis 1:1', got {actual_refs[0]!r}")
        if actual_refs[-1] != "Bereishis 50:26":
            errors.append(f"{path.as_posix()}: last ref must be 'Bereishis 50:26', got {actual_refs[-1]!r}")
    if missing_refs:
        errors.append(f"{path.as_posix()}: missing refs: {missing_refs}")
    if extra_refs:
        errors.append(f"{path.as_posix()}: extra refs: {extra_refs}")

    row_lookup = {row["ref"]: row for row in rows}
    for ref in SPOT_CHECK_REFS:
        row = row_lookup.get(ref)
        if row is None:
            errors.append(f"{path.as_posix()}: required spot-check ref missing: {ref}")
            continue
        if not row["hebrew_menukad_taamim"].strip():
            errors.append(f"{path.as_posix()}: required spot-check ref has blank Hebrew: {ref}")

    return {
        "valid": not errors,
        "source_file_path": path.as_posix(),
        "row_count": len(rows),
        "perek_count": len(perakim),
        "first_ref": actual_refs[0] if actual_refs else None,
        "last_ref": actual_refs[-1] if actual_refs else None,
        "sha256": sha256_for_path(path),
        "errors": errors,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate canonical local source-text TSV files.")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON instead of text output.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = validate_bereishis_source_texts()
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    elif summary["valid"]:
        print("PASS: canonical Bereishis Hebrew source text validation succeeded.")
        print(f"source file path: {summary['source_file_path']}")
        print(f"row count: {summary['row_count']}")
        print(f"perek count: {summary['perek_count']}")
        print(f"first ref: {summary['first_ref']}")
        print(f"last ref: {summary['last_ref']}")
        print(f"SHA-256: {summary['sha256']}")
    else:
        print("FAIL: canonical Bereishis Hebrew source text validation failed.")
        for error in summary["errors"]:
            print(f"- {error}")
    return 0 if summary["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
