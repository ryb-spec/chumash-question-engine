from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_TEXTS_DIR = ROOT / "data" / "source_texts"
CANONICAL_BEREISHIS_TSV = SOURCE_TEXTS_DIR / "bereishis_hebrew_menukad_taamim.tsv"
SOURCE_TEXT_MANIFEST = SOURCE_TEXTS_DIR / "source_text_manifest.json"

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
    35: 29,
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

EXPECTED_ROW_COUNT = sum(EXPECTED_BEREISHIS_CHAPTER_COUNTS.values())
EXPECTED_SCOPE = "Bereishis 1:1-50:26"
SPOT_CHECK_REFS = (
    "Bereishis 1:1",
    "Bereishis 4:1",
    "Bereishis 4:16",
    "Bereishis 4:17",
    "Bereishis 50:26",
)
SOF_PASUK = "\u05c3"
SOURCE_NOTE_REQUIRED_PHRASE = "Miqra according to the Masorah"
REF_PATTERN = re.compile(r"^Bereishis (\d+):(\d+)$")


def build_expected_refs() -> list[str]:
    refs: list[str] = []
    for perek, pasuk_count in EXPECTED_BEREISHIS_CHAPTER_COUNTS.items():
        for pasuk in range(1, pasuk_count + 1):
            refs.append(f"Bereishis {perek}:{pasuk}")
    return refs


EXPECTED_REFS = build_expected_refs()
EXPECTED_REF_SET = set(EXPECTED_REFS)


def sha256_for_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summarize_status(
    *,
    exists: bool,
    blockers: list[str],
    missing_refs: list[str],
    extra_refs: list[str],
    malformed_count: int,
) -> str:
    if not exists:
        return "missing"
    if blockers:
        return "malformed"
    if missing_refs or extra_refs:
        return "partial"
    if malformed_count:
        return "malformed"
    return "complete"


def validate_bereishis_source_texts(path: Path = CANONICAL_BEREISHIS_TSV) -> dict:
    path = Path(path)
    warnings: list[str] = []
    blockers: list[str] = []
    rows: list[dict[str, str]] = []
    actual_refs: list[str] = []
    duplicate_refs: set[str] = set()
    duplicate_pairs: set[tuple[int, int]] = set()
    seen_refs: set[str] = set()
    seen_pairs: set[tuple[int, int]] = set()
    perakim: set[int] = set()
    malformed_rows: set[int] = set()
    blank_line_numbers: list[int] = []
    short_hebrew_refs: list[str] = []
    source_issue_count = 0
    empty_hebrew_count = 0

    summary = {
        "valid": False,
        "status": "missing",
        "file_path": path.as_posix(),
        "exists": path.exists(),
        "expected_scope": EXPECTED_SCOPE,
        "expected_row_count": EXPECTED_ROW_COUNT,
        "row_count": 0,
        "perek_count": 0,
        "first_ref": None,
        "last_ref": None,
        "duplicate_count": 0,
        "missing_count": 0,
        "malformed_count": 0,
        "empty_hebrew_count": 0,
        "source_issue_count": 0,
        "duplicate_refs": [],
        "duplicate_pairs": [],
        "missing_refs": [],
        "extra_refs": [],
        "spot_check_refs": list(SPOT_CHECK_REFS),
        "warnings": warnings,
        "blockers": blockers,
        "sha256": None,
    }

    if not path.exists():
        blockers.append(f"source file missing: {path.as_posix()}")
        return summary

    summary["sha256"] = sha256_for_path(path)

    try:
        raw_text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        blockers.append(f"invalid UTF-8: {error}")
        summary["status"] = "malformed"
        return summary

    raw_lines = raw_text.splitlines()
    if not raw_lines:
        blockers.append("file is empty")
        summary["status"] = "malformed"
        return summary

    for line_number, line in enumerate(raw_lines, start=1):
        if not line.strip():
            blank_line_numbers.append(line_number)
    if blank_line_numbers:
        warnings.append(f"suspicious blank lines at rows: {blank_line_numbers}")

    header = next(csv.reader([raw_lines[0]], delimiter="\t"))
    if header != EXPECTED_HEADER:
        blockers.append(f"header must be exactly {EXPECTED_HEADER}, got {header}")

    reader = csv.reader(raw_lines[1:], delimiter="\t")
    for row_number, row in enumerate(reader, start=2):
        if len(row) != len(EXPECTED_HEADER):
            malformed_rows.add(row_number)
            blockers.append(f"{path.as_posix()}:{row_number}: expected 8 columns, got {len(row)}")
            continue

        record = dict(zip(EXPECTED_HEADER, row, strict=True))
        rows.append(record)

        sefer = record["sefer"]
        if sefer != "Bereishis":
            malformed_rows.add(row_number)
            blockers.append(f"{path.as_posix()}:{row_number}: sefer must be Bereishis, got {sefer!r}")

        perek: int | None
        pasuk: int | None
        try:
            perek = int(record["perek"])
            if perek <= 0:
                raise ValueError
        except ValueError:
            malformed_rows.add(row_number)
            blockers.append(f"{path.as_posix()}:{row_number}: perek must be a positive integer")
            perek = None

        try:
            pasuk = int(record["pasuk"])
            if pasuk <= 0:
                raise ValueError
        except ValueError:
            malformed_rows.add(row_number)
            blockers.append(f"{path.as_posix()}:{row_number}: pasuk must be a positive integer")
            pasuk = None

        ref = record["ref"]
        ref_match = REF_PATTERN.fullmatch(ref)
        if not ref_match:
            malformed_rows.add(row_number)
            blockers.append(f"{path.as_posix()}:{row_number}: malformed ref {ref!r}")
        elif perek is not None and pasuk is not None:
            ref_perek = int(ref_match.group(1))
            ref_pasuk = int(ref_match.group(2))
            if ref_perek != perek or ref_pasuk != pasuk:
                malformed_rows.add(row_number)
                blockers.append(
                    f"{path.as_posix()}:{row_number}: ref {ref!r} does not match perek/pasuk {perek}:{pasuk}"
                )

        if perek is not None:
            perakim.add(perek)

        if perek is not None and pasuk is not None:
            pair = (perek, pasuk)
            if pair in seen_pairs:
                duplicate_pairs.add(pair)
            seen_pairs.add(pair)

        if ref in seen_refs:
            duplicate_refs.add(ref)
        seen_refs.add(ref)
        actual_refs.append(ref)

        hebrew_text = record["hebrew_menukad_taamim"]
        if not hebrew_text.strip():
            empty_hebrew_count += 1
            malformed_rows.add(row_number)
            blockers.append(f"{path.as_posix()}:{row_number}: hebrew_menukad_taamim must not be blank")
        else:
            if len(hebrew_text.strip()) < 4:
                short_hebrew_refs.append(ref)
            if not hebrew_text.endswith(SOF_PASUK):
                malformed_rows.add(row_number)
                blockers.append(
                    f"{path.as_posix()}:{row_number}: hebrew_menukad_taamim must end with sof pasuk {SOF_PASUK}"
                )

        source = record["source"].strip()
        if not source:
            source_issue_count += 1
            malformed_rows.add(row_number)
            blockers.append(f"{path.as_posix()}:{row_number}: source must not be blank")
        elif source != "Sefaria":
            source_issue_count += 1
            malformed_rows.add(row_number)
            blockers.append(f"{path.as_posix()}:{row_number}: source must be Sefaria, got {source!r}")

        source_note = record["source_note"].strip()
        if not source_note:
            source_issue_count += 1
            malformed_rows.add(row_number)
            blockers.append(f"{path.as_posix()}:{row_number}: source_note must not be blank")
        elif SOURCE_NOTE_REQUIRED_PHRASE not in source_note:
            source_issue_count += 1
            malformed_rows.add(row_number)
            blockers.append(
                f"{path.as_posix()}:{row_number}: source_note must include {SOURCE_NOTE_REQUIRED_PHRASE!r}"
            )

        url = record["url"].strip()
        if not url:
            source_issue_count += 1
            malformed_rows.add(row_number)
            blockers.append(
                f"{path.as_posix()}:{row_number}: url must not be blank unless source_note explains why"
            )

    if duplicate_refs:
        blockers.append(f"{path.as_posix()}: duplicate refs found: {sorted(duplicate_refs)}")
    if duplicate_pairs:
        blockers.append(f"{path.as_posix()}: duplicate perek/pasuk pairs found: {sorted(duplicate_pairs)}")

    actual_ref_set = set(actual_refs)
    missing_refs = sorted(EXPECTED_REF_SET - actual_ref_set)
    extra_refs = sorted(actual_ref_set - EXPECTED_REF_SET)

    if len(rows) != EXPECTED_ROW_COUNT:
        blockers.append(f"{path.as_posix()}: expected {EXPECTED_ROW_COUNT} data rows, got {len(rows)}")
    if len(perakim) != len(EXPECTED_BEREISHIS_CHAPTER_COUNTS):
        blockers.append(
            f"{path.as_posix()}: expected {len(EXPECTED_BEREISHIS_CHAPTER_COUNTS)} perakim, got {len(perakim)}"
        )
    if actual_refs and actual_refs[0] != EXPECTED_REFS[0]:
        blockers.append(f"{path.as_posix()}: first ref must be {EXPECTED_REFS[0]!r}, got {actual_refs[0]!r}")
    if actual_refs and actual_refs[-1] != EXPECTED_REFS[-1]:
        blockers.append(f"{path.as_posix()}: last ref must be {EXPECTED_REFS[-1]!r}, got {actual_refs[-1]!r}")
    if missing_refs:
        blockers.append(f"{path.as_posix()}: missing refs: {missing_refs}")
    if extra_refs:
        blockers.append(f"{path.as_posix()}: extra refs: {extra_refs}")
    if short_hebrew_refs:
        warnings.append(f"suspiciously short Hebrew text at refs: {short_hebrew_refs}")

    row_lookup = {row["ref"]: row for row in rows}
    for ref in SPOT_CHECK_REFS:
        row = row_lookup.get(ref)
        if row is None:
            blockers.append(f"{path.as_posix()}: required spot-check ref missing: {ref}")
        elif not row["hebrew_menukad_taamim"].strip():
            blockers.append(f"{path.as_posix()}: required spot-check ref has blank Hebrew: {ref}")

    status = summarize_status(
        exists=True,
        blockers=blockers,
        missing_refs=missing_refs,
        extra_refs=extra_refs,
        malformed_count=len(malformed_rows),
    )

    summary.update(
        {
            "valid": status == "complete",
            "status": status,
            "exists": True,
            "row_count": len(rows),
            "perek_count": len(perakim),
            "first_ref": actual_refs[0] if actual_refs else None,
            "last_ref": actual_refs[-1] if actual_refs else None,
            "duplicate_count": len(duplicate_refs) + len(duplicate_pairs),
            "missing_count": len(missing_refs),
            "malformed_count": len(malformed_rows),
            "empty_hebrew_count": empty_hebrew_count,
            "source_issue_count": source_issue_count,
            "duplicate_refs": sorted(duplicate_refs),
            "duplicate_pairs": [f"{p}:{s}" for p, s in sorted(duplicate_pairs)],
            "missing_refs": missing_refs,
            "extra_refs": extra_refs,
            "warnings": warnings,
            "blockers": blockers,
        }
    )
    return summary


def load_source_text_manifest(path: Path = SOURCE_TEXT_MANIFEST) -> dict:
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate canonical local source-text TSV files.")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON instead of text output.",
    )
    return parser.parse_args()


def print_human_summary(summary: dict) -> None:
    print(f"{'PASS' if summary['valid'] else 'FAIL'}: source-text validation status is {summary['status']}.")
    print(f"file path: {summary['file_path']}")
    print(f"row count: {summary['row_count']}")
    print(f"first ref: {summary['first_ref']}")
    print(f"last ref: {summary['last_ref']}")
    print(f"duplicate count: {summary['duplicate_count']}")
    print(f"missing count: {summary['missing_count']}")
    print(f"malformed count: {summary['malformed_count']}")
    print(f"empty Hebrew count: {summary['empty_hebrew_count']}")
    print(f"source issue count: {summary['source_issue_count']}")
    if summary["sha256"]:
        print(f"SHA-256: {summary['sha256']}")
    if summary["warnings"]:
        print("warnings:")
        for warning in summary["warnings"]:
            print(f"- {warning}")
    if summary["blockers"]:
        print("blockers:")
        for blocker in summary["blockers"]:
            print(f"- {blocker}")


def main() -> int:
    args = parse_args()
    summary = validate_bereishis_source_texts()
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print_human_summary(summary)
    return 0 if summary["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
