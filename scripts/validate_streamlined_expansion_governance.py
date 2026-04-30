"""Validate Streamlined Expansion Governance contract usage.

This validator enforces the machine-readable expansion contract for files that
opt into the streamlined governance process. A specific ``--path`` is validated
strictly when it contains recognizable governance fields. Repo-wide/default
validation avoids brittle failures on older legacy artifacts by enforcing only
contract-area files and files with explicit governance opt-in metadata.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = (
    PROJECT_ROOT
    / "data"
    / "expansion_governance"
    / "streamlined_expansion_contract.json"
)

SUPPORTED_SUFFIXES = {".csv", ".json", ".jsonl", ".tsv"}

ERROR_CONTRACT_MISSING = "STREAMLINED_CONTRACT_MISSING"
ERROR_TRACEABILITY_MISSING = "STREAMLINED_TRACEABILITY_MISSING"
ERROR_PLANNING_ONLY_ACTIVATION = "PLANNING_ONLY_ACTIVATION_VIOLATION"
ERROR_RUNTIME_WITHOUT_APPROVAL = "RUNTIME_WITHOUT_REVIEWED_BANK_APPROVAL"
ERROR_PROTECTED_PREVIEW_SHORTCUT = "PROTECTED_PREVIEW_RUNTIME_SHORTCUT"
ERROR_REVIEWED_BANK_CANDIDATE_SHORTCUT = (
    "REVIEWED_BANK_CANDIDATE_RUNTIME_SHORTCUT"
)
ERROR_DEPTH_GATE = "DEPTH_LADDER_GATE_VIOLATION"
ERROR_UNKNOWN_STATUS = "UNKNOWN_GOVERNANCE_STATUS"
ERROR_MIXED_PACKET_TYPE = "MIXED_REVIEW_PACKET_TYPE"

GOVERNANCE_FIELD_HINTS = {
    "review_status",
    "runtime_status",
    "runtime_active",
    "runtime_ready",
    "runtime_allowed",
    "protected_preview_allowed",
    "reviewed_bank_allowed",
    "reviewed_bank_status",
    "question_allowed",
    "protected_preview_ready",
    "observed_internally",
    "reviewed_bank_candidate",
    "reviewed_bank_approved",
    "planning_only",
    "skill_depth_stage",
    "depth_stage",
    "packet_type",
    "governance_status",
    "expansion_status",
}

EXPLICIT_OPT_IN_FIELDS = {
    "expansion_governance_contract",
    "streamlined_expansion_contract",
    "governance_contract",
    "governed_by",
}

BANK_ITEM_HINT_FIELDS = {
    "candidate_id",
    "candidate_planning_id",
    "item_id",
    "packet_item_id",
    "question_id",
    "source_candidate_id",
    "vocabulary_id",
    "sefer",
    "perek",
    "pasuk",
    "pasuk_ref",
    "hebrew_word",
    "hebrew_phrase",
    "basic_gloss",
    "gloss",
    "skill_category",
    "source_evidence",
    "source_ref",
    "prompt_text",
    "expected_answer",
}

TRACEABILITY_ALIASES = {
    "sefer": ("sefer",),
    "perek": ("perek",),
    "pasuk": ("pasuk",),
    "hebrew_text": ("hebrew_word", "hebrew_phrase"),
    "basic_gloss": ("basic_gloss", "gloss"),
    "skill_category": ("skill_category",),
    "source_evidence": ("source_evidence", "source_ref"),
    "review_status": (
        "review_status",
        "status",
        "governance_status",
        "expansion_status",
    ),
    "runtime_status": (
        "runtime_status",
        "runtime_active",
        "runtime_ready",
        "runtime_allowed",
    ),
}

STATUS_FIELDS = (
    "review_status",
    "status",
    "governance_status",
    "expansion_status",
)

BOOLEAN_TRUE = {"1", "true", "yes", "y", "active", "allowed", "approved"}
BOOLEAN_FALSE = {
    "",
    "0",
    "false",
    "no",
    "n",
    "none",
    "not_allowed",
    "not_runtime",
    "not_reviewed_bank",
    "not_student_facing",
}

DOCUMENTED_STATUS_ALIASES = {
    "approved_after_internal_observation": "observed_internally",
    "approved_after_observation": "observed_internally",
    "simple_question_reviewed": "teacher_approved",
    "reviewed_by_teacher": "teacher_approved",
    "ready_for_reviewed_bank_candidate_planning": "reviewed_bank_candidate",
    "reviewed_bank_candidate_planning_ready": "reviewed_bank_candidate",
    "ready_for_yossi_reviewed_bank_decision_packet": "reviewed_bank_candidate",
}

SIMPLE_QUESTION_REVIEW_ALIASES = {
    "simple_question_reviewed",
    "teacher_approved",
    "reviewed_by_teacher",
}

LATE_STAGE_APPROVAL_ALIASES = {
    "late_stage_approved",
    "stage_6_approved",
    "rashi_or_deeper_pshat_approved",
}


@dataclass(frozen=True)
class ValidationError:
    code: str
    path: Path
    location: str
    message: str

    def format(self) -> str:
        return f"{self.code} {self.path}:{self.location} {self.message}"


@dataclass
class ValidationResult:
    errors: list[ValidationError] = field(default_factory=list)
    files_checked: int = 0
    files_ignored: int = 0
    items_checked: int = 0

    @property
    def ok(self) -> bool:
        return not self.errors

    def extend(self, other: "ValidationResult") -> None:
        self.errors.extend(other.errors)
        self.files_checked += other.files_checked
        self.files_ignored += other.files_ignored
        self.items_checked += other.items_checked


def normalized_key(value: str) -> str:
    return re.sub(r"_+", "_", str(value).strip().lower().replace("-", "_").replace(" ", "_"))


def normalized_value(value: Any) -> str:
    if value is None:
        return ""
    return normalized_key(str(value).strip())


def normalized_record(record: dict[str, Any]) -> dict[str, Any]:
    return {normalized_key(key): value for key, value in record.items()}


def load_contract(path: Path = CONTRACT_PATH) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(ERROR_CONTRACT_MISSING) from exc


def truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    text = normalized_value(value)
    if text in BOOLEAN_TRUE:
        return True
    if text in BOOLEAN_FALSE:
        return False
    return False


def split_status_values(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, bool):
        return ["true"] if value else ["false"]
    if isinstance(value, (list, tuple, set)):
        values: list[str] = []
        for item in value:
            values.extend(split_status_values(item))
        return values
    text = str(value).strip()
    if not text:
        return []
    return [
        normalized_value(part)
        for part in re.split(r"[|,;]", text)
        if normalized_value(part)
    ]


def first_present(record: dict[str, Any], aliases: Iterable[str]) -> Any:
    for alias in aliases:
        key = normalized_key(alias)
        if key in record and str(record[key]).strip() != "":
            return record[key]
    return None


def status_values(record: dict[str, Any]) -> set[str]:
    values: set[str] = set()
    for field_name in STATUS_FIELDS:
        values.update(split_status_values(record.get(field_name)))
    for alias, canonical in DOCUMENTED_STATUS_ALIASES.items():
        if alias in values:
            values.add(canonical)
    return values


def all_status_like_values(record: dict[str, Any]) -> set[str]:
    values = status_values(record)
    values.update(split_status_values(record.get("reviewed_bank_status")))
    values.update(split_status_values(record.get("runtime_status")))
    return values


def has_status(record: dict[str, Any], status: str) -> bool:
    normalized_status = normalized_value(status)
    if truthy(record.get(normalized_status)):
        return True
    if normalized_status in all_status_like_values(record):
        return True
    for alias, canonical in DOCUMENTED_STATUS_ALIASES.items():
        if canonical == normalized_status and alias in all_status_like_values(record):
            return True
    return False


def is_governed_record(
    record: dict[str, Any],
    *,
    explicit_path: bool,
    path: Path,
) -> bool:
    keys = set(record)
    if not keys:
        return False
    if explicit_path:
        return bool(keys & GOVERNANCE_FIELD_HINTS)
    if is_under_expansion_governance(path):
        return bool(keys & GOVERNANCE_FIELD_HINTS)
    if keys & EXPLICIT_OPT_IN_FIELDS:
        return True
    if normalized_value(record.get("governed_by")) == "streamlined_expansion_contract":
        return True
    if normalized_value(record.get("expansion_governance_contract")):
        return True
    return False


def is_under_expansion_governance(path: Path) -> bool:
    try:
        path.resolve().relative_to(
            PROJECT_ROOT / "data" / "expansion_governance"
        )
        return True
    except ValueError:
        return False


def is_bank_like_record(record: dict[str, Any]) -> bool:
    keys = set(record)
    if "packet_type" in keys and not (keys & (BANK_ITEM_HINT_FIELDS - {"packet_type"})):
        return False
    return bool(keys & BANK_ITEM_HINT_FIELDS)


def traceability_missing(record: dict[str, Any]) -> list[str]:
    missing = []
    for logical_name, aliases in TRACEABILITY_ALIASES.items():
        if first_present(record, aliases) is None:
            missing.append(logical_name)
    return missing


def is_planning_only(record: dict[str, Any]) -> bool:
    return truthy(record.get("planning_only")) or "planning_only" in status_values(record)


def is_runtime_active(record: dict[str, Any]) -> bool:
    return truthy(record.get("runtime_active")) or has_status(record, "runtime_active")


def is_runtime_ready(record: dict[str, Any]) -> bool:
    return truthy(record.get("runtime_ready")) or has_status(record, "runtime_ready") or has_status(record, "runtime_active")


def has_reviewed_bank_approval(record: dict[str, Any]) -> bool:
    return truthy(record.get("reviewed_bank_approved")) or has_status(record, "reviewed_bank_approved")


def has_reviewed_bank_candidate_only(record: dict[str, Any]) -> bool:
    if not (truthy(record.get("reviewed_bank_candidate")) or has_status(record, "reviewed_bank_candidate")):
        return False
    return not has_reviewed_bank_approval(record)


def has_observed_or_later(record: dict[str, Any], ladder: list[str]) -> bool:
    if truthy(record.get("observed_internally")):
        return True
    statuses = all_status_like_values(record)
    statuses.update(
        canonical
        for alias, canonical in DOCUMENTED_STATUS_ALIASES.items()
        if alias in statuses
    )
    if "observed_internally" not in ladder:
        return "observed_internally" in statuses
    observed_index = ladder.index("observed_internally")
    later_statuses = set(ladder[observed_index:])
    return bool(statuses & later_statuses)


def has_simple_question_review(record: dict[str, Any]) -> bool:
    if truthy(record.get("simple_question_reviewed")):
        return True
    if truthy(record.get("teacher_approved")):
        return True
    statuses = all_status_like_values(record)
    return bool(statuses & SIMPLE_QUESTION_REVIEW_ALIASES)


def parse_depth_stage(record: dict[str, Any], depth_stage_by_id: dict[str, int]) -> int | None:
    raw_value = first_present(record, ("skill_depth_stage", "depth_stage"))
    if raw_value is None:
        return None
    value = normalized_value(raw_value)
    if not value:
        return None
    if value.isdigit():
        return int(value)
    match = re.search(r"stage_(\d+)", value)
    if match:
        return int(match.group(1))
    match = re.search(r"\b(\d+)\b", str(raw_value))
    if match:
        return int(match.group(1))
    return depth_stage_by_id.get(value)


def has_late_stage_approval(record: dict[str, Any]) -> bool:
    if truthy(record.get("late_stage_approved")):
        return True
    if truthy(record.get("rashi_or_deeper_pshat_approved")):
        return True
    if truthy(record.get("depth_stage_approved")):
        return True
    return bool(all_status_like_values(record) & LATE_STAGE_APPROVAL_ALIASES)


def packet_types(record: dict[str, Any]) -> set[str]:
    value = record.get("packet_type")
    if value is None:
        return set()
    return set(split_status_values(value))


def has_packet_type_exception(record: dict[str, Any]) -> bool:
    exception_enabled = (
        truthy(record.get("mixed_packet_type_exception"))
        or truthy(record.get("packet_type_exception"))
        or truthy(record.get("review_packet_exception"))
    )
    if not exception_enabled:
        return False
    reason = first_present(
        record,
        (
            "mixed_packet_type_exception_reason",
            "packet_type_exception_reason",
            "review_packet_exception_reason",
            "exception_reason",
        ),
    )
    return reason is not None


def validate_status_values(
    record: dict[str, Any],
    *,
    path: Path,
    location: str,
    ladder: list[str],
) -> list[ValidationError]:
    allowed = set(ladder) | set(DOCUMENTED_STATUS_ALIASES)
    errors = []
    for field_name in STATUS_FIELDS:
        for value in split_status_values(record.get(field_name)):
            if value and value not in allowed:
                errors.append(
                    ValidationError(
                        ERROR_UNKNOWN_STATUS,
                        path,
                        location,
                        f"{field_name} has unknown governance status {value!r}",
                    )
                )
    return errors


def validate_record(
    record: dict[str, Any],
    *,
    path: Path,
    location: str,
    contract: dict[str, Any],
) -> list[ValidationError]:
    errors: list[ValidationError] = []
    ladder = [normalized_value(value) for value in contract["approval_status_ladder"]]
    depth_stage_by_id = {
        normalized_value(stage["id"]): index + 1
        for index, stage in enumerate(contract["depth_ladder"])
    }
    review_packet_rule = contract["review_packet_separation_rule"]
    allowed_packet_type_values = review_packet_rule.get(
        "allowed_review_packet_types",
        review_packet_rule.get("allowed_packet_types", []),
    )
    allowed_packet_types = {
        normalized_value(value) for value in allowed_packet_type_values
    }

    errors.extend(
        validate_status_values(record, path=path, location=location, ladder=ladder)
    )

    if is_bank_like_record(record):
        missing = traceability_missing(record)
        if missing:
            errors.append(
                ValidationError(
                    ERROR_TRACEABILITY_MISSING,
                    path,
                    location,
                    "missing logical fields: " + ", ".join(missing),
                )
            )

    if is_planning_only(record):
        forbidden_truthy = [
            field_name
            for field_name in (
                "runtime_active",
                "runtime_ready",
                "runtime_allowed",
                "protected_preview_allowed",
                "reviewed_bank_allowed",
            )
            if truthy(record.get(field_name))
        ]
        if forbidden_truthy:
            errors.append(
                ValidationError(
                    ERROR_PLANNING_ONLY_ACTIVATION,
                    path,
                    location,
                    "planning_only item has open promotion/runtime flags: "
                    + ", ".join(forbidden_truthy),
                )
            )

    runtime_active = is_runtime_active(record)
    if runtime_active:
        protected_preview_ready = truthy(record.get("protected_preview_ready")) or has_status(
            record, "protected_preview_ready"
        )
        if protected_preview_ready and not has_observed_or_later(record, ladder):
            errors.append(
                ValidationError(
                    ERROR_PROTECTED_PREVIEW_SHORTCUT,
                    path,
                    location,
                    "protected_preview_ready cannot shortcut to runtime_active",
                )
            )
        if has_reviewed_bank_candidate_only(record):
            errors.append(
                ValidationError(
                    ERROR_REVIEWED_BANK_CANDIDATE_SHORTCUT,
                    path,
                    location,
                    "reviewed_bank_candidate cannot shortcut to runtime_active",
                )
            )
        if not (
            has_reviewed_bank_approval(record)
            and is_runtime_ready(record)
            and has_observed_or_later(record, ladder)
        ):
            errors.append(
                ValidationError(
                    ERROR_RUNTIME_WITHOUT_APPROVAL,
                    path,
                    location,
                    "runtime_active requires observed evidence, reviewed-bank approval, and runtime_ready evidence",
                )
            )

    depth_stage = parse_depth_stage(record, depth_stage_by_id)
    if depth_stage is not None and depth_stage >= 2:
        missing_depth_evidence = []
        if not has_status(record, "word_level_approved"):
            missing_depth_evidence.append("word_level_approved")
        if not has_simple_question_review(record):
            missing_depth_evidence.append("simple_question_reviewed_or_teacher_approved")
        if not has_observed_or_later(record, ladder):
            missing_depth_evidence.append("observed_internally")
        if depth_stage >= 6 and not has_late_stage_approval(record):
            missing_depth_evidence.append("late_stage_approved")
        if missing_depth_evidence:
            errors.append(
                ValidationError(
                    ERROR_DEPTH_GATE,
                    path,
                    location,
                    "depth stage "
                    + str(depth_stage)
                    + " missing prerequisites: "
                    + ", ".join(missing_depth_evidence),
                )
            )

    types = packet_types(record)
    if types:
        unknown_types = types - allowed_packet_types
        if unknown_types:
            errors.append(
                ValidationError(
                    ERROR_UNKNOWN_STATUS,
                    path,
                    location,
                    "unknown packet_type values: " + ", ".join(sorted(unknown_types)),
                )
            )
        if len(types) > 1 and not has_packet_type_exception(record):
            errors.append(
                ValidationError(
                    ERROR_MIXED_PACKET_TYPE,
                    path,
                    location,
                    "mixed packet_type values require explicit exception metadata with a reason",
                )
            )

    return errors


def extract_json_records(data: Any, prefix: str = "$") -> list[tuple[str, dict[str, Any]]]:
    records: list[tuple[str, dict[str, Any]]] = []
    if isinstance(data, dict):
        records.append((prefix, normalized_record(data)))
        for key in ("items", "rows", "records", "candidates", "included_items"):
            value = data.get(key)
            if isinstance(value, list):
                for index, item in enumerate(value, start=1):
                    if isinstance(item, dict):
                        records.append((f"{prefix}.{key}[{index}]", normalized_record(item)))
    elif isinstance(data, list):
        for index, item in enumerate(data, start=1):
            if isinstance(item, dict):
                records.append((f"{prefix}[{index}]", normalized_record(item)))
    return records


def read_records(path: Path) -> list[tuple[str, dict[str, Any]]]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        with path.open("r", encoding="utf-8-sig") as handle:
            return extract_json_records(json.load(handle))
    if suffix == ".jsonl":
        records: list[tuple[str, dict[str, Any]]] = []
        with path.open("r", encoding="utf-8-sig") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                value = json.loads(line)
                if isinstance(value, dict):
                    records.append((f"line {line_number}", normalized_record(value)))
        return records
    if suffix in {".csv", ".tsv"}:
        delimiter = "\t" if suffix == ".tsv" else ","
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter=delimiter)
            return [
                (f"row {index}", normalized_record(row))
                for index, row in enumerate(reader, start=2)
            ]
    return []


def validate_file(
    path: Path,
    *,
    contract: dict[str, Any],
    explicit_path: bool = False,
) -> ValidationResult:
    result = ValidationResult()
    if path.suffix.lower() not in SUPPORTED_SUFFIXES:
        result.files_ignored = 1
        return result
    try:
        records = read_records(path)
    except (OSError, csv.Error, json.JSONDecodeError) as exc:
        result.errors.append(
            ValidationError(
                ERROR_UNKNOWN_STATUS,
                path,
                "$",
                f"could not parse governed expansion file: {exc}",
            )
        )
        result.files_checked = 1
        return result

    governed_records: list[tuple[str, dict[str, Any]]] = []
    for location, record in records:
        if is_governed_record(record, explicit_path=explicit_path, path=path):
            governed_records.append((location, record))

    if not governed_records:
        result.files_ignored = 1
        return result

    result.files_checked = 1
    result.items_checked = len(governed_records)
    all_file_packet_types: set[str] = set()
    has_file_packet_exception = False

    for location, record in governed_records:
        result.errors.extend(
            validate_record(
                record,
                path=path,
                location=location,
                contract=contract,
            )
        )
        all_file_packet_types.update(packet_types(record))
        has_file_packet_exception = has_file_packet_exception or has_packet_type_exception(record)

    if len(all_file_packet_types) > 1 and not has_file_packet_exception:
        result.errors.append(
            ValidationError(
                ERROR_MIXED_PACKET_TYPE,
                path,
                "$",
                "file mixes review packet types without explicit exception metadata",
            )
        )

    return result


def validate_paths(
    paths: Iterable[Path],
    *,
    contract: dict[str, Any],
    explicit_path: bool = False,
) -> ValidationResult:
    result = ValidationResult()
    for path in paths:
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file():
                    result.extend(
                        validate_file(
                            child,
                            contract=contract,
                            explicit_path=explicit_path,
                        )
                    )
        else:
            result.extend(
                validate_file(path, contract=contract, explicit_path=explicit_path)
            )
    return result


def discover_paths(strict: bool) -> list[Path]:
    if strict:
        return [PROJECT_ROOT / "data"]
    return [PROJECT_ROOT / "data" / "expansion_governance"]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Streamlined Expansion Governance contract enforcement."
    )
    parser.add_argument(
        "--path",
        type=Path,
        help="Validate a specific governed expansion file or directory.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Scan repo data for files that explicitly opt into expansion governance.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        contract = load_contract()
    except RuntimeError:
        print(f"{ERROR_CONTRACT_MISSING} {CONTRACT_PATH}")
        return 1

    if args.path:
        paths = [args.path if args.path.is_absolute() else PROJECT_ROOT / args.path]
        explicit_path = True
    else:
        paths = discover_paths(args.strict)
        explicit_path = False

    result = validate_paths(paths, contract=contract, explicit_path=explicit_path)
    if result.errors:
        for error in result.errors:
            print(error.format())
        return 1

    print(
        "Streamlined expansion governance validation passed. "
        f"checked {result.items_checked} governed item(s); "
        f"ignored {result.files_ignored} unmanaged file(s)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
