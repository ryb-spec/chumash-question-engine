from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY_MD = Path("data/validation/curriculum_quality_check_summary.md")
DEFAULT_SUMMARY_JSON = Path("data/validation/curriculum_quality_check_summary.json")
CONTROL_INDEX_PATH = Path("data/validation/curriculum_quality_control_index.md")
PEREK3_STATUS_INDEX_PATH = Path(
    "data/gate_2_protected_preview_candidates/reports/bereishis_perek_3_candidate_status_index.md"
)
DIAGNOSTIC_COVERAGE_MD = Path("data/validation/diagnostic_preview_coverage_index.md")
DIAGNOSTIC_COVERAGE_JSON = Path("data/validation/diagnostic_preview_coverage_index.json")
LINEAGE_MD = Path("data/validation/protected_preview_source_lineage_matrix.md")
LINEAGE_TSV = Path("data/validation/protected_preview_source_lineage_matrix.tsv")
RUNTIME_EXPOSURE_MD = Path("data/validation/runtime_review_exposure_index.md")
RUNTIME_EXPOSURE_JSON = Path("data/validation/runtime_review_exposure_index.json")
STANDARDS_GAP_MD = Path("data/validation/standards_evidence_gap_matrix.md")
STANDARDS_GAP_JSON = Path("data/validation/standards_evidence_gap_matrix.json")
QUESTION_RISK_MD = Path("data/validation/question_quality_risk_summary.md")
QUESTION_RISK_JSON = Path("data/validation/question_quality_risk_summary.json")

SCHEMA_VERSION = "1.0"
GENERATED_BY = "scripts/run_curriculum_quality_checks.py"
TAIL_LIMIT = 1800

SAFETY_BOUNDARIES = {
    "no_runtime_activation": True,
    "no_perek_3_activation": True,
    "no_reviewed_bank_promotion": True,
    "no_protected_preview_packet_creation": True,
    "no_student_facing_content_creation": True,
    "no_runtime_ui_scoring_mastery_assessment_flow_changes": True,
}

AUDIT_WARNING_KEYS = [
    "runtime_coverage_broader_than_reviewed_preview_coverage",
    "translation_context_low_safe_valid_rate",
    "suffix_compound_morphology_fragile",
    "standards_evidence_not_teacher_facing_enough",
    "diagnostic_preview_under_scoped",
    "perek_3_stale_packet_status_clarity",
    "validators_scattered_manual",
    "source_lineage_visibility_gap",
    "readme_command_drift",
]

REQUIRED_VALIDATOR_SCRIPTS = [
    ("source integrity", "source text validation", "scripts/validate_source_texts.py"),
    ("source integrity", "Bereishis translation validation", "scripts/validate_bereishis_translations.py"),
    ("source integrity", "verified source-to-skill maps", "scripts/validate_verified_source_skill_maps.py"),
    ("curriculum extraction", "curriculum extraction validation", "scripts/validate_curriculum_extraction.py"),
    ("standards", "standards data validation", "scripts/validate_standards_data.py"),
    ("standards", "canonical skill contract validation", "scripts/validate_canonical_skill_contract.py"),
    ("pipeline", "pipeline rounds validation", "scripts/validate_pipeline_rounds.py"),
    (
        "protected preview",
        "Gate 2 protected-preview candidates validation",
        "scripts/validate_gate_2_protected_preview_candidates.py",
    ),
    (
        "protected preview",
        "Gate 2 protected-preview packet validation",
        "scripts/validate_gate_2_protected_preview_packet.py",
    ),
    ("enrichment", "source skill enrichment validation", "scripts/validate_source_skill_enrichment.py"),
    ("eligibility", "question eligibility audit validation", "scripts/validate_question_eligibility_audit.py"),
]

OPTIONAL_VALIDATOR_SCRIPTS = [
    ("Gate 2", "Gate 2 input planning validation", "scripts/validate_gate_2_input_planning.py"),
    ("Gate 2", "Gate 2 controlled draft validation", "scripts/validate_gate_2_controlled_draft_generation.py"),
    ("protected preview", "Round 1 protected-preview packet validation", "scripts/validate_protected_preview_packet.py"),
    (
        "protected preview",
        "Round 1 protected-preview candidates validation",
        "scripts/validate_protected_preview_candidates.py",
    ),
    ("dikduk", "dikduk foundations validation", "scripts/validate_dikduk_foundations.py"),
    ("dikduk", "dikduk rules validation", "scripts/validate_dikduk_rules.py"),
]


@dataclass(frozen=True)
class CheckSpec:
    label: str
    category: str
    args: list[str]
    required: bool = True
    kind: str = "subprocess"
    skip_reason: str = ""


@dataclass
class CheckResult:
    label: str
    category: str
    args: list[str]
    required: bool
    status: str
    exit_code: int | None
    duration_seconds: float
    stdout_tail: str = ""
    stderr_tail: str = ""
    note: str = ""


def repo_path(path: Path | str) -> Path:
    return ROOT / Path(path)


def repo_relative(path: Path | str) -> str:
    return str(Path(path).as_posix())


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def short_tail(text: str, limit: int = TAIL_LIMIT) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[-limit:]


def branch_name() -> str:
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip() or "not_available"


def python_command(script: str, *extra: str) -> list[str]:
    return [sys.executable, script, *extra]


def build_checks(*, include_slow: bool = False) -> list[CheckSpec]:
    checks: list[CheckSpec] = []
    for category, label, script in REQUIRED_VALIDATOR_SCRIPTS:
        checks.append(CheckSpec(label=label, category=category, args=python_command(script), required=True))
    for category, label, script in OPTIONAL_VALIDATOR_SCRIPTS:
        checks.append(CheckSpec(label=label, category=category, args=python_command(script), required=False))

    diagnostic_validator = repo_path("scripts/validate_diagnostic_preview.py")
    diagnostic_configs = sorted(repo_path("data/diagnostic_preview/configs").glob("*.json"))
    if diagnostic_validator.exists() and diagnostic_configs:
        for config in diagnostic_configs:
            checks.append(
                CheckSpec(
                    label=f"diagnostic preview validation: {config.name}",
                    category="diagnostic preview",
                    args=python_command("scripts/validate_diagnostic_preview.py", "--config", repo_relative(config.relative_to(ROOT))),
                    required=True,
                )
            )
    elif diagnostic_validator.exists():
        checks.append(
            CheckSpec(
                label="diagnostic preview validation",
                category="diagnostic preview",
                args=[],
                required=False,
                kind="skip",
                skip_reason="No diagnostic preview config files were found.",
            )
        )

    checks.append(
        CheckSpec(
            label="question validation audit metrics",
            category="question quality",
            args=[],
            required=False,
            kind="warn",
            skip_reason=(
                "Existing question-validation metrics are read from data/validation/question_validation_audit.json "
                "and the overnight audit report; the generator is not run because it rewrites tracked audit artifacts."
            ),
        )
    )
    return sorted(checks, key=lambda check: (check.category, check.label))


def missing_script_note(args: list[str]) -> str:
    if len(args) >= 2 and args[1].endswith(".py") and not repo_path(args[1]).exists():
        return f"Missing script: {args[1]}"
    return ""


def run_check(check: CheckSpec) -> CheckResult:
    start = time.perf_counter()
    if check.kind == "skip":
        return CheckResult(
            label=check.label,
            category=check.category,
            args=check.args,
            required=check.required,
            status="SKIP",
            exit_code=None,
            duration_seconds=0.0,
            note=check.skip_reason,
        )
    if check.kind == "warn":
        return CheckResult(
            label=check.label,
            category=check.category,
            args=check.args,
            required=check.required,
            status="WARN",
            exit_code=None,
            duration_seconds=0.0,
            note=check.skip_reason,
        )

    missing = missing_script_note(check.args)
    if missing:
        return CheckResult(
            label=check.label,
            category=check.category,
            args=check.args,
            required=check.required,
            status="FAIL" if check.required else "SKIP",
            exit_code=None,
            duration_seconds=0.0,
            note=missing,
        )

    result = subprocess.run(check.args, cwd=ROOT, capture_output=True, text=True, check=False)
    duration = round(time.perf_counter() - start, 3)
    return CheckResult(
        label=check.label,
        category=check.category,
        args=check.args,
        required=check.required,
        status="PASS" if result.returncode == 0 else "FAIL",
        exit_code=result.returncode,
        duration_seconds=duration,
        stdout_tail=short_tail(result.stdout),
        stderr_tail=short_tail(result.stderr),
    )


def summarize_results(results: list[CheckResult], *, strict: bool = False) -> tuple[str, dict[str, int]]:
    counts = {
        "required_passed": sum(1 for result in results if result.required and result.status == "PASS"),
        "required_failed": sum(1 for result in results if result.required and result.status == "FAIL"),
        "optional_passed": sum(1 for result in results if not result.required and result.status == "PASS"),
        "optional_failed": sum(1 for result in results if not result.required and result.status == "FAIL"),
        "skipped": sum(1 for result in results if result.status == "SKIP"),
        "warnings": sum(1 for result in results if result.status == "WARN"),
    }
    if counts["required_failed"] or (strict and counts["warnings"]):
        return "FAIL", counts
    if counts["optional_failed"] or counts["warnings"] or counts["skipped"]:
        return "WARN", counts
    return "PASS", counts


def format_command(args: list[str]) -> str:
    if not args:
        return "not_applicable"
    return " ".join(args)


def build_summary_payload(results: list[CheckResult], *, strict: bool, summary_md: Path, summary_json: Path) -> dict[str, Any]:
    overall_status, counts = summarize_results(results, strict=strict)
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_by": GENERATED_BY,
        "branch": branch_name(),
        "overall_status": overall_status,
        "strict": strict,
        "counts": counts,
        "checks": [asdict(result) for result in results],
        "audit_warning_keys": AUDIT_WARNING_KEYS,
        "safety_boundary_confirmations": SAFETY_BOUNDARIES,
        "output_paths": {
            "summary_md": repo_relative(summary_md),
            "summary_json": repo_relative(summary_json),
            "control_index": repo_relative(CONTROL_INDEX_PATH),
            "diagnostic_preview_coverage_index_md": repo_relative(DIAGNOSTIC_COVERAGE_MD),
            "diagnostic_preview_coverage_index_json": repo_relative(DIAGNOSTIC_COVERAGE_JSON),
            "protected_preview_source_lineage_matrix_md": repo_relative(LINEAGE_MD),
            "protected_preview_source_lineage_matrix_tsv": repo_relative(LINEAGE_TSV),
            "runtime_review_exposure_index_md": repo_relative(RUNTIME_EXPOSURE_MD),
            "runtime_review_exposure_index_json": repo_relative(RUNTIME_EXPOSURE_JSON),
            "standards_evidence_gap_matrix_md": repo_relative(STANDARDS_GAP_MD),
            "standards_evidence_gap_matrix_json": repo_relative(STANDARDS_GAP_JSON),
            "question_quality_risk_summary_md": repo_relative(QUESTION_RISK_MD),
            "question_quality_risk_summary_json": repo_relative(QUESTION_RISK_JSON),
            "perek_3_status_index": repo_relative(PEREK3_STATUS_INDEX_PATH),
        },
    }


def render_summary_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Curriculum Quality Check Summary",
        "",
        f"Generated by `{GENERATED_BY}`.",
        "",
        "This is a non-runtime report. It does not activate content, promote reviewed-bank data, create protected-preview packets, or create student-facing content.",
        "",
        f"- Branch: `{payload['branch']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Required passed: {payload['counts']['required_passed']}",
        f"- Required failed: {payload['counts']['required_failed']}",
        f"- Optional passed: {payload['counts']['optional_passed']}",
        f"- Optional failed: {payload['counts']['optional_failed']}",
        f"- Skipped: {payload['counts']['skipped']}",
        f"- Warnings: {payload['counts']['warnings']}",
        "",
        "## Command table",
        "",
        "| Category | Label | Command | Required | Status | Exit code | Note |",
        "|---|---|---|---:|---|---:|---|",
    ]
    for result in payload["checks"]:
        lines.append(
            "| {category} | {label} | `{command}` | {required} | `{status}` | {exit_code} | {note} |".format(
                category=result["category"],
                label=result["label"],
                command=format_command(result["args"]),
                required="yes" if result["required"] else "no",
                status=result["status"],
                exit_code="not_available" if result["exit_code"] is None else result["exit_code"],
                note=(result.get("note") or "").replace("|", "/") or "not_available",
            )
        )
    lines.extend(
        [
            "",
            "## Audit risk radar",
            "",
            "- Runtime coverage is broader than reviewed preview coverage.",
            "- Translation/context safe-valid rate is low in existing audit evidence.",
            "- Suffix and compound morphology remain fragile.",
            "- Standards evidence is not yet teacher-facing enough.",
            "- Diagnostic preview coverage is promising but under-scoped.",
            "- Perek 3 review packet status can become stale without a current-status index.",
            "- Validators are strong but scattered/manual.",
            "- Source lineage visibility is incomplete at item level.",
            "- README validation commands had drifted from pytest/current orchestration.",
            "",
            "## Safety boundary confirmation",
            "",
        ]
    )
    for key, value in payload["safety_boundary_confirmations"].items():
        lines.append(f"- {key}: `{str(value).lower()}`")
    return "\n".join(lines) + "\n"


def perek_from_ref(ref: str) -> str:
    if not ref:
        return "not_available"
    try:
        chapter = ref.split()[1].split(":", 1)[0]
        return chapter
    except Exception:
        return "not_available"


def build_perek3_status() -> dict[str, Any]:
    candidates_path = repo_path("data/gate_2_protected_preview_candidates/bereishis_perek_3_protected_preview_candidates.tsv")
    rows = read_tsv(candidates_path)
    decision_counts = Counter(row.get("yossi_protected_preview_decision") or "blank" for row in rows)
    approved = [
        row.get("protected_preview_candidate_id", "")
        for row in rows
        if row.get("yossi_protected_preview_decision") == "approve_for_internal_protected_preview_packet"
    ]
    packet_path = repo_path("data/gate_2_protected_preview_packets/bereishis_perek_3_internal_protected_preview_packet.tsv")
    checklist_path = repo_path(
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_3_internal_protected_preview_review_checklist.md"
    )
    return {
        "candidate_tsv": repo_relative(candidates_path.relative_to(ROOT)),
        "historical_review_packet": "data/gate_2_protected_preview_candidates/reports/bereishis_perek_3_protected_preview_candidate_review_packet.md",
        "applied_decision_report": "data/gate_2_protected_preview_candidates/reports/bereishis_perek_3_protected_preview_candidate_yossi_review_applied.md",
        "status_index": repo_relative(PEREK3_STATUS_INDEX_PATH),
        "internal_packet_tsv": repo_relative(packet_path.relative_to(ROOT)),
        "internal_review_checklist": repo_relative(checklist_path.relative_to(ROOT)),
        "decision_counts": {
            "approve_for_internal_protected_preview_packet": decision_counts.get("approve_for_internal_protected_preview_packet", 0),
            "approve_with_revision": decision_counts.get("approve_with_revision", 0),
            "needs_follow_up": decision_counts.get("needs_follow_up", 0),
            "reject_for_preview": decision_counts.get("reject_for_preview", 0),
            "source_only": decision_counts.get("source_only", 0),
        },
        "approved_candidate_ids": sorted(approved),
        "perek_3_internal_packet_exists": packet_path.exists(),
    }


def write_perek3_status_index() -> dict[str, Any]:
    data = build_perek3_status()
    lines = [
        "# Bereishis Perek 3 candidate status index",
        "",
        "## Current status",
        "",
        "Perek 3 protected-preview candidate decisions have been applied. The applied-decision report is the current status source. The original candidate review packet is a historical pre-decision artifact; readers should not treat the original packet's pending language as current status after decisions were applied.",
        "",
        "## Paths",
        "",
        f"- Candidate TSV: `{data['candidate_tsv']}`",
        f"- Original historical candidate review packet: `{data['historical_review_packet']}`",
        f"- Applied-decision report: `{data['applied_decision_report']}`",
        f"- Four-item internal protected-preview packet TSV: `{data['internal_packet_tsv']}`",
        f"- Internal review checklist: `{data['internal_review_checklist']}`",
        f"- Status index: `{data['status_index']}`",
        "",
        "## Decision counts",
        "",
    ]
    for decision, count in data["decision_counts"].items():
        lines.append(f"- `{decision}`: {count}")
    lines.extend(
        [
            "",
            "## Approved candidate IDs",
            "",
            *(f"- `{candidate_id}`" for candidate_id in data["approved_candidate_ids"]),
            "",
            "## Exclusion warning",
            "",
            "Revision items are not included in the internal packet. Follow-up items are not included in the internal packet.",
            "",
            "## Explicit safety state",
            "",
            "- A four-item internal protected-preview packet now exists for the approved IDs only.",
            "- A four-item internal review checklist now exists with blank reviewer decision fields only.",
            "- No approve-with-revision rows were included.",
            "- No needs-follow-up rows were included.",
            "- No Perek 3 runtime activation.",
            "- No reviewed-bank promotion.",
            "- No student-facing content.",
            "",
            "## Next permitted action",
            "",
            "Yossi/teacher review may now review the four-item internal packet. Any later reviewed-bank, runtime, or student-facing step requires a separate explicit task and must keep gates fail-closed until approved.",
        ]
    )
    write_text(repo_path(PEREK3_STATUS_INDEX_PATH), "\n".join(lines) + "\n")
    return data


def build_lineage_rows() -> list[dict[str, str]]:
    packet_paths = sorted(repo_path("data/gate_2_protected_preview_packets").glob("*_internal_protected_preview_packet.tsv"))
    candidate_rows = {}
    for candidate_path in sorted(repo_path("data/gate_2_protected_preview_candidates").glob("*_protected_preview_candidates.tsv")):
        for row in read_tsv(candidate_path):
            candidate_rows[row.get("protected_preview_candidate_id", "")] = (repo_relative(candidate_path.relative_to(ROOT)), row)
    rows: list[dict[str, str]] = []
    for packet_path in packet_paths:
        for packet_row in read_tsv(packet_path):
            candidate_id = packet_row.get("protected_preview_candidate_id", "")
            candidate_path, candidate_row = candidate_rows.get(candidate_id, ("not_available", {}))
            rows.append(
                {
                    "packet_path": repo_relative(packet_path.relative_to(ROOT)),
                    "packet_item_id": packet_row.get("protected_preview_packet_item_id") or "not_available",
                    "candidate_id": candidate_id or "not_available",
                    "candidate_path": candidate_path,
                    "perek": perek_from_ref(packet_row.get("source_ref", "")),
                    "ref": packet_row.get("source_ref") or "not_available",
                    "hebrew_token": packet_row.get("hebrew_token") or "not_available",
                    "hebrew_phrase": packet_row.get("hebrew_phrase") or "not_available",
                    "skill_id": packet_row.get("approved_family") or "not_available",
                    "canonical_skill_id": "not_available",
                    "zekelman_standard_mapping": "not_available",
                    "source_artifact_path": candidate_path,
                    "review_decision_source": candidate_row.get("yossi_protected_preview_decision") or "not_available",
                    "review_status": packet_row.get("internal_preview_review_status") or "not_available",
                    "runtime_allowed": packet_row.get("runtime_allowed") or "not_available",
                    "reviewed_bank_allowed": packet_row.get("reviewed_bank_allowed") or "not_available",
                    "protected_preview_allowed": packet_row.get("internal_packet_status") or "not_available",
                    "student_facing_allowed": packet_row.get("student_facing_allowed") or "not_available",
                    "source_row_id": "not_available",
                    "source_to_skill_id": candidate_row.get("gate_2_input_candidate_id") or "not_available",
                    "enrichment_id": "not_available",
                    "translation_authority": "not_available",
                    "notes": "Audit-only lineage. Missing lineage fields use not_available and do not imply invalid source.",
                }
            )
    return rows


def write_lineage_reports() -> list[dict[str, str]]:
    rows = build_lineage_rows()
    headers = [
        "packet_path",
        "packet_item_id",
        "candidate_id",
        "candidate_path",
        "perek",
        "ref",
        "hebrew_token",
        "hebrew_phrase",
        "skill_id",
        "canonical_skill_id",
        "zekelman_standard_mapping",
        "source_artifact_path",
        "review_decision_source",
        "review_status",
        "runtime_allowed",
        "reviewed_bank_allowed",
        "protected_preview_allowed",
        "student_facing_allowed",
        "source_row_id",
        "source_to_skill_id",
        "enrichment_id",
        "translation_authority",
        "notes",
    ]
    LINEAGE_TSV.parent.mkdir(parents=True, exist_ok=True)
    with repo_path(LINEAGE_TSV).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    lines = [
        "# Protected-preview source lineage matrix",
        "",
        "This is an audit-only lineage report. It does not approve protected-preview release, reviewed-bank use, runtime use, or student-facing use.",
        "",
        "Missing lineage fields use `not_available`; missing lineage does not imply invalid source, and present lineage does not imply runtime approval.",
        "",
        f"- TSV matrix: `{repo_relative(LINEAGE_TSV)}`",
        f"- Rows: {len(rows)}",
        "",
        "| Packet item | Candidate | Ref | Skill | Runtime allowed | Reviewed-bank allowed | Student-facing allowed | Source-to-skill ID |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['packet_item_id']}` | `{row['candidate_id']}` | {row['ref']} | `{row['skill_id']}` | `{row['runtime_allowed']}` | `{row['reviewed_bank_allowed']}` | `{row['student_facing_allowed']}` | `{row['source_to_skill_id']}` |"
        )
    write_text(repo_path(LINEAGE_MD), "\n".join(lines) + "\n")
    return rows


def build_diagnostic_coverage() -> dict[str, Any]:
    configs = sorted(repo_path("data/diagnostic_preview/configs").glob("*.json"))
    summaries = sorted(repo_path("data/diagnostic_preview/reports").glob("*preview_summary.json"))
    records = []
    for config in configs:
        config_payload = read_json(config)
        preview_id = config_payload.get("preview_id", config.stem)
        matching = [summary for summary in summaries if preview_id in summary.stem]
        record: dict[str, Any] = {
            "config_path": repo_relative(config.relative_to(ROOT)),
            "preview_id": preview_id,
            "summary_paths": [repo_relative(path.relative_to(ROOT)) for path in matching],
            "covered_refs": "not_available",
            "covered_ref_count": "not_available",
            "question_count_by_lane": {},
            "question_count_by_skill": {},
            "reviewable_item_count": "not_available",
            "caution_count": "not_available",
            "runtime_approval_warning": "Diagnostic preview coverage does not equal runtime approval, reviewed-bank approval, or protected-preview approval.",
        }
        for summary_path in matching:
            summary = read_json(summary_path)
            range_data = summary.get("range") or summary.get("range_covered") or {}
            refs = range_data.get("refs_with_questions")
            if refs:
                record["covered_refs"] = sorted(refs)
                record["covered_ref_count"] = len(refs)
            elif range_data.get("start_ref") and range_data.get("end_ref"):
                record["covered_refs"] = f"{range_data.get('start_ref')} to {range_data.get('end_ref')}"
                record["covered_ref_count"] = range_data.get("pesukim_covered", "not_available")
            if summary.get("question_count_by_lane"):
                record["question_count_by_lane"] = summary["question_count_by_lane"]
            if summary.get("question_count_by_skill"):
                record["question_count_by_skill"] = summary["question_count_by_skill"]
            if "total_questions" in summary and "reviewable" in summary_path.stem:
                record["reviewable_item_count"] = summary["total_questions"]
                record["caution_count"] = summary.get("likely_review_status_counts", {}).get("caution", 0)
            if summary.get("reviewable_preview"):
                reviewable = summary["reviewable_preview"]
                record["reviewable_item_count"] = reviewable.get("total_questions", "not_available")
                record["caution_count"] = reviewable.get("likely_review_status_counts", {}).get("caution", "not_available")
        records.append(record)
    return {
        "schema_version": SCHEMA_VERSION,
        "records": records,
        "warnings": [
            "Diagnostic preview coverage does not equal runtime approval.",
            "Diagnostic preview coverage does not equal reviewed-bank approval.",
            "Diagnostic preview coverage does not equal protected-preview approval.",
            "Coverage gaps marked not_available are unknown, not inferred.",
        ],
    }


def write_diagnostic_coverage_reports() -> dict[str, Any]:
    data = build_diagnostic_coverage()
    lines = [
        "# Diagnostic preview coverage index",
        "",
        "This report discovers existing diagnostic preview configs and summaries. It does not generate new diagnostic preview content.",
        "",
        "- Diagnostic preview coverage does not equal runtime approval.",
        "- Diagnostic preview coverage does not equal reviewed-bank approval.",
        "- Diagnostic preview coverage does not equal protected-preview approval.",
        "",
        "| Preview ID | Config | Summaries | Covered refs | Lanes | Reviewable items | Cautions |",
        "|---|---|---|---|---|---:|---:|",
    ]
    for record in data["records"]:
        lines.append(
            "| {preview_id} | `{config}` | {summaries} | {refs} | {lanes} | {reviewable} | {cautions} |".format(
                preview_id=record["preview_id"],
                config=record["config_path"],
                summaries="<br>".join(f"`{path}`" for path in record["summary_paths"]) or "not_available",
                refs=record["covered_refs"],
                lanes=", ".join(f"{key}: {value}" for key, value in sorted(record["question_count_by_lane"].items()))
                or "not_available",
                reviewable=record["reviewable_item_count"],
                cautions=record["caution_count"],
            )
        )
    write_text(repo_path(DIAGNOSTIC_COVERAGE_MD), "\n".join(lines) + "\n")
    write_json(repo_path(DIAGNOSTIC_COVERAGE_JSON), data)
    return data


def build_question_quality_risk() -> dict[str, Any]:
    audit_path = repo_path("data/curriculum_extraction/reports/audits/AUDIT_OVERNIGHT_CURRICULUM_QUALITY_REVIEW.md")
    question_audit_path = repo_path("data/validation/question_validation_audit.json")
    existing_audit = read_json(question_audit_path) if question_audit_path.exists() else {}
    return {
        "schema_version": SCHEMA_VERSION,
        "source_paths": [repo_relative(audit_path.relative_to(ROOT)), repo_relative(question_audit_path.relative_to(ROOT))],
        "audit_report_metrics": {
            "translation_context": {"valid": 223, "total": 1109, "safe_valid_rate": "20.1%"},
            "suffix": {"valid": 94, "total": 258, "safe_valid_rate": "36.4%"},
        },
        "current_question_validation_audit_scope": existing_audit.get("scope_summary", {}).get("scope", "not_available"),
        "top_rejection_reasons": [
            "placeholder_translation",
            "low_instructional_value",
            "grammatical_particle",
            "compound_morphology",
            "no_clear_suffix",
            "lexical_plural_ending",
        ],
        "recommendation_categories": {
            "safe_reviewed_lanes": ["basic_noun_recognition where reviewed"],
            "teacher_review_required": ["translation/context", "suffix forms", "shoresh pools", "phrase translation"],
            "engineering_review_required": ["runtime exposure reporting", "standards evidence dashboard"],
            "do_not_expand_yet": ["vav hahipuch", "advanced verb forms", "Rashi/commentary", "higher-order inference"],
        },
        "runtime_change_warning": "This report does not change question generators, runtime behavior, or validation thresholds.",
    }


def write_question_quality_risk_reports() -> dict[str, Any]:
    data = build_question_quality_risk()
    lines = [
        "# Question quality risk summary",
        "",
        "This report uses existing audit evidence only. It does not change runtime behavior, question generators, or validation thresholds.",
        "",
        "## Key risk metrics",
        "",
        f"- Translation/context safe-valid rate: {data['audit_report_metrics']['translation_context']['valid']} / {data['audit_report_metrics']['translation_context']['total']} ({data['audit_report_metrics']['translation_context']['safe_valid_rate']})",
        f"- Suffix safe-valid rate: {data['audit_report_metrics']['suffix']['valid']} / {data['audit_report_metrics']['suffix']['total']} ({data['audit_report_metrics']['suffix']['safe_valid_rate']})",
        "",
        "## Top rejection reasons",
        "",
        *(f"- `{reason}`" for reason in data["top_rejection_reasons"]),
        "",
        "## Recommendation categories",
        "",
    ]
    for category, values in data["recommendation_categories"].items():
        lines.append(f"- {category}: {', '.join(values)}")
    write_text(repo_path(QUESTION_RISK_MD), "\n".join(lines) + "\n")
    write_json(repo_path(QUESTION_RISK_JSON), data)
    return data


def canonical_skill_status_counts() -> dict[str, int]:
    contract_path = repo_path("data/standards/canonical_skill_contract.json")
    if not contract_path.exists():
        return {}
    contract = read_json(contract_path)
    return dict(Counter(skill.get("status", "unknown") for skill in contract.get("canonical_skills", [])))


def build_standards_gap() -> dict[str, Any]:
    contract_path = repo_path("data/standards/canonical_skill_contract.json")
    contract = read_json(contract_path) if contract_path.exists() else {}
    packet_rows = build_lineage_rows()
    packet_count_by_skill = Counter(row["skill_id"] for row in packet_rows)
    diagnostic_data = build_diagnostic_coverage()
    diagnostic_skill_counts = Counter()
    for record in diagnostic_data["records"]:
        diagnostic_skill_counts.update(record.get("question_count_by_skill", {}))
    source_to_skill_counts = Counter()
    for map_path in sorted(repo_path("data/verified_source_skill_maps").glob("*.tsv")):
        for row in read_tsv(map_path):
            source_to_skill_counts[row.get("skill_primary") or row.get("skill") or "not_available"] += 1
    runtime_mapping = defaultdict(list)
    for mapping in contract.get("runtime_skill_mappings", []):
        for canonical_id in mapping.get("canonical_skill_ids", []):
            runtime_mapping[canonical_id].append(mapping.get("runtime_skill_id", "not_available"))
    z_mapping = defaultdict(list)
    for mapping in contract.get("zekelman_skill_mappings", []):
        for canonical_id in mapping.get("canonical_skill_ids", []):
            z_mapping[canonical_id].append(
                f"{mapping.get('zekelman_standard_id', 'not_available')}:{mapping.get('mapping_status', 'not_available')}"
            )
    records = []
    for skill in sorted(contract.get("canonical_skills", []), key=lambda item: item.get("canonical_skill_id", "")):
        canonical_id = skill.get("canonical_skill_id", "not_available")
        related_question_types = skill.get("related_question_types", [])
        diagnostic_count = sum(diagnostic_skill_counts.get(question_type, 0) for question_type in related_question_types)
        records.append(
            {
                "canonical_skill_id": canonical_id,
                "runtime_skill_ids": sorted(runtime_mapping.get(canonical_id, [])) or ["not_available"],
                "zekelman_mapping_status": sorted(z_mapping.get(canonical_id, [])) or ["not_available"],
                "status": skill.get("status", "unknown"),
                "protected_preview_evidence_count": packet_count_by_skill.get(skill.get("skill_lane", ""), 0)
                + packet_count_by_skill.get(canonical_id, 0),
                "diagnostic_preview_evidence_count": diagnostic_count,
                "reviewed_bank_evidence_count": "not_available",
                "source_to_skill_evidence_count": sum(
                    source_to_skill_counts.get(question_type, 0) for question_type in related_question_types
                ),
                "teacher_review_needed": skill.get("status") != "runtime_ready" or bool(z_mapping.get(canonical_id)),
                "risk_note": "Final teacher-facing standards grouping requires review.",
            }
        )
    return {
        "schema_version": SCHEMA_VERSION,
        "canonical_status_counts": canonical_skill_status_counts(),
        "records": records,
        "warning": "This matrix does not create new standards or decide final teacher dashboard groupings.",
    }


def write_standards_gap_reports() -> dict[str, Any]:
    data = build_standards_gap()
    lines = [
        "# Standards evidence gap matrix",
        "",
        "This report uses existing standards/canonical-skill evidence only. It does not create standards, change mappings, or decide final teacher dashboard groupings.",
        "",
        "Final teacher-facing standards groupings require teacher review where indicated.",
        "",
        "| Canonical skill | Runtime mapping | Zekelman mapping/status | Status | Protected-preview evidence | Diagnostic evidence | Source-to-skill evidence | Teacher review needed |",
        "|---|---|---|---|---:|---:|---:|---|",
    ]
    for row in data["records"]:
        lines.append(
            "| `{canonical}` | {runtime} | {zekelman} | `{status}` | {pp} | {diag} | {source} | `{teacher}` |".format(
                canonical=row["canonical_skill_id"],
                runtime=", ".join(f"`{item}`" for item in row["runtime_skill_ids"]),
                zekelman=", ".join(f"`{item}`" for item in row["zekelman_mapping_status"]),
                status=row["status"],
                pp=row["protected_preview_evidence_count"],
                diag=row["diagnostic_preview_evidence_count"],
                source=row["source_to_skill_evidence_count"],
                teacher=str(row["teacher_review_needed"]).lower(),
            )
        )
    write_text(repo_path(STANDARDS_GAP_MD), "\n".join(lines) + "\n")
    write_json(repo_path(STANDARDS_GAP_JSON), data)
    return data


def build_runtime_exposure() -> dict[str, Any]:
    corpus_path = repo_path("data/corpus_manifest.json")
    corpus = read_json(corpus_path) if corpus_path.exists() else {}
    active_scope = next((scope for scope in corpus.get("scopes", []) if scope.get("runtime_active")), None)
    if not active_scope and corpus.get("scopes"):
        active_scope = corpus["scopes"][0]
    packet_rows = build_lineage_rows()
    diagnostic_data = build_diagnostic_coverage()
    protected_families = Counter(row["skill_id"] for row in packet_rows)
    diagnostic_lanes = Counter()
    for record in diagnostic_data["records"]:
        diagnostic_lanes.update(record.get("question_count_by_lane", {}))
    families = [
        ("basic_noun_recognition", "yes", "yes" if protected_families.get("basic_noun_recognition") else "no", "unknown", "safe reviewed lane"),
        ("translation/context", "yes", "unknown", "yes" if diagnostic_lanes.get("translation") else "no", "teacher review required"),
        ("suffix/compound morphology", "yes", "unknown", "unknown", "teacher review required"),
        ("phrase translation", "yes", "unknown", "yes" if diagnostic_lanes.get("translation") else "unknown", "teacher review required"),
        ("pasuk comprehension/context", "unknown", "unknown", "unknown", "teacher review required"),
        ("vav hahipuch/advanced verb forms", "unknown", "no", "unknown", "do not expand yet"),
        ("Rashi/commentary/higher-order inference", "no", "no", "no", "do not expand yet"),
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "active_scope": active_scope or {},
        "protected_preview_family_counts": dict(sorted(protected_families.items())),
        "diagnostic_lane_counts": dict(sorted(diagnostic_lanes.items())),
        "family_exposure": [
            {
                "family_or_skill": family,
                "runtime_evidence_detected": runtime_detected,
                "reviewed_evidence_detected": reviewed_detected,
                "diagnostic_evidence_detected": diagnostic_detected,
                "protected_preview_evidence_detected": reviewed_detected,
                "risk_level": "high" if recommended != "safe reviewed lane" else "medium",
                "recommended_status": recommended,
            }
            for family, runtime_detected, reviewed_detected, diagnostic_detected, recommended in families
        ],
        "warning": "Read-only report. No runtime code, scope, generation caps, UI, scoring, or mastery behavior changed.",
    }


def write_runtime_exposure_reports() -> dict[str, Any]:
    data = build_runtime_exposure()
    scope = data.get("active_scope") or {}
    lines = [
        "# Runtime reviewed-evidence exposure index",
        "",
        "This is a read-only, non-runtime report. It surfaces reviewed-evidence exposure gaps without changing runtime generation, scope, caps, UI, scoring, or mastery behavior.",
        "",
        f"- Active scope ID: `{scope.get('scope_id', 'not_available')}`",
        f"- Active scope range: `{scope.get('range', 'not_available')}`",
        f"- Active scope pesukim count: `{scope.get('pesukim_count', 'not_available')}`",
        "",
        "| Family / skill | Runtime evidence detected | Reviewed evidence detected | Diagnostic evidence detected | Protected-preview evidence detected | Risk | Recommended status |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in data["family_exposure"]:
        lines.append(
            f"| {row['family_or_skill']} | `{row['runtime_evidence_detected']}` | `{row['reviewed_evidence_detected']}` | `{row['diagnostic_evidence_detected']}` | `{row['protected_preview_evidence_detected']}` | `{row['risk_level']}` | {row['recommended_status']} |"
        )
    write_text(repo_path(RUNTIME_EXPOSURE_MD), "\n".join(lines) + "\n")
    write_json(repo_path(RUNTIME_EXPOSURE_JSON), data)
    return data


def write_control_index(output_paths: dict[str, str]) -> None:
    lines = [
        "# Curriculum Quality Control Center",
        "",
        "This index is a non-runtime navigation page for curriculum quality, validation, provenance, and review-governance reports.",
        "",
        "It does not activate runtime content, promote reviewed-bank data, approve protected-preview packets, or create student-facing content.",
        "",
        "## Reports",
        "",
        f"- Curriculum quality check summary: `{output_paths['summary_md']}`",
        f"- Curriculum quality check summary JSON: `{output_paths['summary_json']}`",
        f"- Diagnostic preview coverage index: `{repo_relative(DIAGNOSTIC_COVERAGE_MD)}`",
        f"- Diagnostic preview coverage JSON: `{repo_relative(DIAGNOSTIC_COVERAGE_JSON)}`",
        f"- Protected-preview source lineage matrix: `{repo_relative(LINEAGE_MD)}`",
        f"- Protected-preview source lineage TSV: `{repo_relative(LINEAGE_TSV)}`",
        f"- Runtime reviewed-evidence exposure index: `{repo_relative(RUNTIME_EXPOSURE_MD)}`",
        f"- Runtime reviewed-evidence exposure JSON: `{repo_relative(RUNTIME_EXPOSURE_JSON)}`",
        f"- Standards evidence gap matrix: `{repo_relative(STANDARDS_GAP_MD)}`",
        f"- Standards evidence gap JSON: `{repo_relative(STANDARDS_GAP_JSON)}`",
        f"- Question quality risk summary: `{repo_relative(QUESTION_RISK_MD)}`",
        f"- Question quality risk JSON: `{repo_relative(QUESTION_RISK_JSON)}`",
        f"- Perek 3 candidate status index: `{repo_relative(PEREK3_STATUS_INDEX_PATH)}`",
        "- Perek 3 internal protected-preview packet report: `data/gate_2_protected_preview_packets/reports/bereishis_perek_3_internal_protected_preview_packet_report.md`",
        "- Perek 3 internal protected-preview review checklist: `data/gate_2_protected_preview_packets/reports/bereishis_perek_3_internal_protected_preview_review_checklist.md`",
        "- Source audit report: `data/curriculum_extraction/reports/audits/AUDIT_OVERNIGHT_CURRICULUM_QUALITY_REVIEW.md`",
        "",
        "## Use guidance",
        "",
        "- Safe for decision-making: source integrity status, validator pass/fail status, closed-gate confirmations, and explicit review-status counts.",
        "- Requires teacher review before acting: standards grouping, suffix-safe examples, translation/context expansion, and any row marked revision/follow-up.",
        "- Reports are evidence aids only. They do not activate runtime, reviewed bank, protected preview, or student-facing content.",
    ]
    write_text(repo_path(CONTROL_INDEX_PATH), "\n".join(lines) + "\n")


def generate_all_reports(payload: dict[str, Any], summary_md: Path, summary_json: Path) -> None:
    write_json(repo_path(summary_json), payload)
    write_text(repo_path(summary_md), render_summary_markdown(payload))
    write_perek3_status_index()
    write_lineage_reports()
    write_diagnostic_coverage_reports()
    write_runtime_exposure_reports()
    write_standards_gap_reports()
    write_question_quality_risk_reports()
    write_control_index(payload["output_paths"])


def print_console_summary(payload: dict[str, Any]) -> None:
    print(f"Curriculum quality checks: {payload['overall_status']}")
    print(f"Branch: {payload['branch']}")
    for key, value in payload["counts"].items():
        print(f"{key}: {value}")
    for result in payload["checks"]:
        print(f"[{result['status']}] {result['category']} - {result['label']}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run non-runtime curriculum quality checks and reports.")
    parser.add_argument("--summary-md", default=repo_relative(DEFAULT_SUMMARY_MD))
    parser.add_argument("--summary-json", default=repo_relative(DEFAULT_SUMMARY_JSON))
    parser.add_argument("--strict", action="store_true", help="Return nonzero on warnings as well as required failures.")
    parser.add_argument("--list-checks", action="store_true", help="List planned checks without running them.")
    parser.add_argument("--no-write", action="store_true", help="Run checks but do not write summaries or reports.")
    parser.add_argument("--include-slow", action="store_true", help="Reserved for future slow checks.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    checks = build_checks(include_slow=args.include_slow)
    if args.list_checks:
        for check in checks:
            required = "required" if check.required else "optional"
            command = format_command(check.args)
            print(f"{check.category}\t{check.label}\t{required}\t{command}")
        return 0

    results = [run_check(check) for check in checks]
    summary_md = Path(args.summary_md)
    summary_json = Path(args.summary_json)
    payload = build_summary_payload(results, strict=args.strict, summary_md=summary_md, summary_json=summary_json)
    print_console_summary(payload)
    if not args.no_write:
        generate_all_reports(payload, summary_md, summary_json)
    if payload["overall_status"] == "FAIL":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
