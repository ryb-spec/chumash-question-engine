from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_streamlined_expansion_governance.py"
SPEC = importlib.util.spec_from_file_location(
    "validate_streamlined_expansion_governance", VALIDATOR_PATH
)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


BASE_ROW = {
    "sefer": "Bereishis",
    "perek": "4",
    "pasuk": "1",
    "hebrew_word": "ish",
    "basic_gloss": "man",
    "skill_category": "single_word_vocabulary",
    "source_evidence": "local_source_fixture",
    "review_status": "planning_only",
    "runtime_status": "not_runtime",
}


def write_tsv(path: Path, rows: list[dict[str, str]]) -> Path:
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    return path


def write_json(path: Path, payload: object) -> Path:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def validate(path: Path, *, explicit_path: bool = True):
    return validator.validate_paths(
        [path],
        contract=validator.load_contract(),
        explicit_path=explicit_path,
    )


def assert_passes(path: Path, *, explicit_path: bool = True):
    result = validate(path, explicit_path=explicit_path)
    assert result.ok, [error.format() for error in result.errors]
    return result


def assert_fails_with(path: Path, code: str):
    result = validate(path)
    assert not result.ok
    assert code in {error.code for error in result.errors}
    return result


def test_valid_planning_only_item_passes(tmp_path: Path):
    row = {
        **BASE_ROW,
        "planning_only": "true",
        "runtime_active": "false",
        "runtime_ready": "false",
        "runtime_allowed": "false",
        "protected_preview_allowed": "false",
        "reviewed_bank_allowed": "false",
    }

    assert_passes(write_tsv(tmp_path / "valid_planning.tsv", [row]))


def test_planning_only_runtime_active_fails(tmp_path: Path):
    row = {
        **BASE_ROW,
        "planning_only": "true",
        "runtime_active": "true",
    }

    assert_fails_with(
        write_tsv(tmp_path / "planning_runtime.tsv", [row]),
        validator.ERROR_PLANNING_ONLY_ACTIVATION,
    )


def test_runtime_active_without_reviewed_bank_approval_fails(tmp_path: Path):
    row = {
        **BASE_ROW,
        "review_status": "observed_internally",
        "runtime_active": "true",
        "runtime_ready": "true",
        "reviewed_bank_status": "not_reviewed_bank",
        "observed_internally": "true",
    }

    assert_fails_with(
        write_tsv(tmp_path / "runtime_without_approval.tsv", [row]),
        validator.ERROR_RUNTIME_WITHOUT_APPROVAL,
    )


def test_protected_preview_ready_runtime_active_fails_unless_later_statuses_present(
    tmp_path: Path,
):
    shortcut_row = {
        **BASE_ROW,
        "review_status": "protected_preview_ready",
        "protected_preview_ready": "true",
        "runtime_active": "true",
    }
    assert_fails_with(
        write_tsv(tmp_path / "protected_preview_shortcut.tsv", [shortcut_row]),
        validator.ERROR_PROTECTED_PREVIEW_SHORTCUT,
    )

    valid_later_row = {
        **BASE_ROW,
        "review_status": "reviewed_bank_approved",
        "protected_preview_ready": "true",
        "observed_internally": "true",
        "reviewed_bank_status": "reviewed_bank_approved",
        "runtime_ready": "true",
        "runtime_active": "true",
        "runtime_status": "runtime_ready",
    }
    assert_passes(write_tsv(tmp_path / "protected_preview_with_later_status.tsv", [valid_later_row]))


def test_reviewed_bank_candidate_runtime_active_fails(tmp_path: Path):
    row = {
        **BASE_ROW,
        "review_status": "reviewed_bank_candidate",
        "observed_internally": "true",
        "reviewed_bank_status": "reviewed_bank_candidate",
        "runtime_ready": "true",
        "runtime_active": "true",
    }

    assert_fails_with(
        write_tsv(tmp_path / "candidate_shortcut.tsv", [row]),
        validator.ERROR_REVIEWED_BANK_CANDIDATE_SHORTCUT,
    )


def test_depth_stage_2_without_prerequisites_fails(tmp_path: Path):
    row = {
        **BASE_ROW,
        "review_status": "teacher_approved",
        "depth_stage": "word_function",
    }

    assert_fails_with(
        write_tsv(tmp_path / "depth_without_prereqs.tsv", [row]),
        validator.ERROR_DEPTH_GATE,
    )


def test_valid_depth_stage_2_with_prerequisites_passes(tmp_path: Path):
    row = {
        **BASE_ROW,
        "review_status": "observed_internally",
        "depth_stage": "word_function",
        "word_level_approved": "true",
        "teacher_approved": "true",
        "observed_internally": "true",
    }

    assert_passes(write_tsv(tmp_path / "depth_with_prereqs.tsv", [row]))


def test_missing_traceability_fails_for_bank_like_governed_item(tmp_path: Path):
    payload = {
        "items": [
            {
                "hebrew_word": "ish",
                "review_status": "planning_only",
                "runtime_status": "not_runtime",
                "planning_only": True,
            }
        ]
    }

    assert_fails_with(
        write_json(tmp_path / "missing_traceability.json", payload),
        validator.ERROR_TRACEABILITY_MISSING,
    )


def test_valid_packet_type_passes(tmp_path: Path):
    payload = {
        "packet_type": "word_bank_review",
        "governance_status": "planning_only",
    }

    assert_passes(write_json(tmp_path / "packet_type.json", payload))


def test_unknown_packet_type_fails(tmp_path: Path):
    payload = {
        "packet_type": "mystery_review",
        "governance_status": "planning_only",
    }

    assert_fails_with(
        write_json(tmp_path / "unknown_packet_type.json", payload),
        validator.ERROR_UNKNOWN_STATUS,
    )


def test_mixed_packet_type_fails_unless_exception_metadata_present(tmp_path: Path):
    mixed_payload = {
        "packet_type": "word_bank_review|simple_question_review",
        "governance_status": "planning_only",
    }
    assert_fails_with(
        write_json(tmp_path / "mixed_packet_type.json", mixed_payload),
        validator.ERROR_MIXED_PACKET_TYPE,
    )

    exception_payload = {
        "packet_type": "word_bank_review|simple_question_review",
        "governance_status": "planning_only",
        "mixed_packet_type_exception": True,
        "mixed_packet_type_exception_reason": "Documented combined review packet fixture.",
    }
    assert_passes(write_json(tmp_path / "mixed_packet_type_exception.json", exception_payload))


def test_unknown_governance_status_fails(tmp_path: Path):
    row = {
        **BASE_ROW,
        "review_status": "teleport_to_runtime",
    }

    assert_fails_with(
        write_tsv(tmp_path / "unknown_status.tsv", [row]),
        validator.ERROR_UNKNOWN_STATUS,
    )


def test_legacy_unmanaged_file_without_governance_fields_is_ignored(tmp_path: Path):
    path = tmp_path / "legacy.csv"
    path.write_text("name,value\nlegacy,kept outside governance\n", encoding="utf-8")

    result = assert_passes(path, explicit_path=False)
    assert result.files_ignored == 1
    assert result.items_checked == 0
