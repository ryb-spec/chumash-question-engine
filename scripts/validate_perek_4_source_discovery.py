from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "data/gate_2_source_discovery/bereishis_perek_4_review_only_safe_candidate_inventory.tsv"
SOURCE_DISCOVERY_REPORT = ROOT / "data/gate_2_source_discovery/reports/bereishis_perek_4_source_discovery_report.md"
DUPLICATE_WARNING_REPORT = ROOT / "data/gate_2_source_discovery/reports/bereishis_perek_4_duplicate_session_balance_warnings.md"
DUPLICATE_WARNING_TSV = ROOT / "data/gate_2_source_discovery/reports/bereishis_perek_4_duplicate_session_balance_warnings.tsv"
EXCLUDED_RISK_LANES_REPORT = ROOT / "data/gate_2_source_discovery/reports/bereishis_perek_4_excluded_risk_lanes.md"
STATUS_INDEX = ROOT / "data/gate_2_source_discovery/reports/bereishis_perek_4_source_discovery_status_index.md"
NEXT_PROMPT = ROOT / "data/pipeline_rounds/prompts/bereishis_perek_4_review_checklist_prompt.md"
PROTECTED_PREVIEW_PACKET_DIR = ROOT / "data/gate_2_protected_preview_packets"

GOVERNED_PEREK_4_PACKET_REQUIREMENTS: dict[str, tuple[str, ...]] = {
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_two_item_limited_internal_packet_iteration_2026_04_29.json": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_two_item_limited_internal_packet_iteration_2026_04_29.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_two_item_limited_internal_packet_iteration_2026_04_29.md": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_two_item_limited_internal_packet_iteration_2026_04_29.json",
    ),
    "data/gate_2_protected_preview_packets/bereishis_perek_4_two_item_limited_internal_packet_iteration.tsv": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_two_item_limited_internal_packet_iteration_2026_04_29.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_limited_internal_preview_hold_register_2026_04_29.md": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_limited_internal_preview_decisions_applied_2026_04_29.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_limited_internal_preview_decisions_applied_2026_04_29.json": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_limited_internal_preview_decisions_applied_2026_04_29.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_limited_internal_preview_decisions_applied_2026_04_29.md": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_limited_internal_preview_decisions_applied_2026_04_29.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_limited_internal_preview_observation_template_2026_04_29.md": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_limited_internal_preview_decisions_applied_2026_04_29.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_blocked_revision_register_2026_04_29.md": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_limited_internal_preview_decisions_applied_2026_04_29.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_limited_internal_preview_readiness_2026_04_29.md": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_limited_internal_preview_decisions_applied_2026_04_29.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_internal_protected_preview_review_decisions_applied_2026_04_29.json": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_internal_protected_preview_review_decisions_applied_2026_04_29.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_internal_protected_preview_review_decisions_applied_2026_04_29.md": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_internal_protected_preview_review_decisions_applied_2026_04_29.json",
    ),
    "data/gate_2_protected_preview_packets/bereishis_perek_4_internal_protected_preview_packet.tsv": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_internal_protected_preview_packet_2026_04_29.json",
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_internal_protected_preview_review_decisions_applied_2026_04_29.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_internal_protected_preview_packet_2026_04_29.md": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_internal_protected_preview_packet_2026_04_29.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_internal_protected_preview_packet_2026_04_29.json": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_internal_protected_preview_packet_2026_04_29.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_internal_protected_preview_packet_generation_report_2026_04_29.md": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_internal_protected_preview_packet_2026_04_29.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_internal_protected_preview_packet_planning_2026_04_29.md": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_internal_protected_preview_packet_2026_04_29.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_internal_protected_preview_review_checklist_2026_04_29.md": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_internal_protected_preview_review_decisions_applied_2026_04_29.json",
    ),
    "data/gate_2_protected_preview_packets/bereishis_perek_4_limited_protected_preview_build_gate_2026_04_30.tsv": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_limited_protected_preview_build_gate_2026_04_30.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_limited_protected_preview_build_gate_2026_04_30.md": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_limited_protected_preview_build_gate_2026_04_30.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_limited_protected_preview_build_gate_2026_04_30.json": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_limited_protected_preview_build_gate_2026_04_30.json",
    ),
    "data/gate_2_protected_preview_packets/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.tsv": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.md": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.json": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_review_checklist_2026_04_30.md": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.json",
        "data/pipeline_rounds/perek_4_broad_vocabulary_internal_protected_preview_packet_v1_2026_04_30.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_review_checklist_2026_04_30.tsv": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.json",
        "data/pipeline_rounds/perek_4_broad_vocabulary_internal_protected_preview_packet_v1_2026_04_30.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_review_checklist_yossi_completed_2026_04_30.md": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.json",
        "data/pipeline_rounds/perek_4_broad_vocabulary_internal_protected_preview_packet_v1_2026_04_30.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_review_checklist_yossi_completed_2026_04_30.tsv": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.json",
        "data/pipeline_rounds/perek_4_broad_vocabulary_internal_protected_preview_packet_v1_2026_04_30.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_final_observation_evidence_2026_04_30.json": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_final_observation_evidence_2026_04_30.json",
        "data/pipeline_rounds/perek_4_broad_vocabulary_final_internal_completion_gate_2026_04_30.json",
        "data/pipeline_rounds/perek_4_broad_vocabulary_internal_protected_preview_packet_v1_2026_04_30.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_final_observation_evidence_2026_04_30.tsv": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_final_observation_evidence_2026_04_30.json",
        "data/pipeline_rounds/perek_4_broad_vocabulary_final_internal_completion_gate_2026_04_30.json",
        "data/pipeline_rounds/perek_4_broad_vocabulary_internal_protected_preview_packet_v1_2026_04_30.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_final_readiness_register_2026_04_30.json": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_final_readiness_register_2026_04_30.json",
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_final_observation_evidence_2026_04_30.json",
        "data/pipeline_rounds/perek_4_broad_vocabulary_final_internal_completion_gate_2026_04_30.json",
        "data/pipeline_rounds/perek_4_broad_vocabulary_internal_protected_preview_packet_v1_2026_04_30.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_final_readiness_register_2026_04_30.tsv": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_final_readiness_register_2026_04_30.json",
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_final_observation_evidence_2026_04_30.json",
        "data/pipeline_rounds/perek_4_broad_vocabulary_final_internal_completion_gate_2026_04_30.json",
        "data/pipeline_rounds/perek_4_broad_vocabulary_internal_protected_preview_packet_v1_2026_04_30.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_observation_template_2026_04_30.md": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_observation_template_2026_04_30.tsv": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_packet_excluded_register_2026_04_30.md": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_packet_excluded_register_2026_04_30.json",
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_packet_excluded_register_2026_04_30.json": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_packet_excluded_register_2026_04_30.json",
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_review_decisions_and_next_gate_2026_04_30.json": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.json",
        "data/pipeline_rounds/perek_4_broad_vocabulary_internal_protected_preview_packet_v1_2026_04_30.json",
    ),
    "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_review_decisions_and_next_gate_2026_04_30.md": (
        "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.json",
        "data/pipeline_rounds/perek_4_broad_vocabulary_internal_protected_preview_packet_v1_2026_04_30.json",
    ),
}

PEREK_4_GOVERNANCE_FALSE_GATE_ALIASES: dict[str, tuple[str, ...]] = {
    "runtime_scope_widened": ("runtime_scope_widened",),
    "perek_activated": ("perek_activated", "perek_4_activated"),
    "reviewed_bank_promoted": ("reviewed_bank_promoted",),
    "runtime_questions_created": ("runtime_questions_created",),
    "student_facing_content_created": ("student_facing_content_created", "student_facing_created"),
    "fake_observation_evidence_created": ("fake_observation_evidence_created", "fake_observations_created"),
}

def _read_json_contract(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, OSError):
        return {}


def _contract_gates_are_closed(payload: dict[str, object]) -> bool:
    for key, aliases in PEREK_4_GOVERNANCE_FALSE_GATE_ALIASES.items():
        found = False
        for alias in aliases:
            if alias not in payload:
                continue
            if payload[alias] is not False:
                return False
            found = True
            break
        if not found:
            continue
    return True


def _is_governed_downstream_perek4_packet(path_text: str) -> bool:
    contract_paths = GOVERNED_PEREK_4_PACKET_REQUIREMENTS.get(path_text)
    if not contract_paths:
        return False
    for contract_path in contract_paths:
        full_path = ROOT / contract_path
        payload = _read_json_contract(full_path)
        if not payload or not _contract_gates_are_closed(payload):
            return False
    return True

REQUIRED_COLUMNS = [
    "candidate_id",
    "perek",
    "ref",
    "pasuk_number",
    "hebrew_token",
    "hebrew_phrase",
    "skill_family",
    "canonical_skill_id",
    "candidate_type",
    "source_row_id",
    "source_artifact",
    "provenance_status",
    "source_confidence",
    "review_status",
    "review_required",
    "duplicate_token_warning",
    "session_balance_warning",
    "risk_flags",
    "exclusion_reason",
    "runtime_allowed",
    "reviewed_bank_allowed",
    "protected_preview_allowed",
    "student_facing_allowed",
    "broader_use_allowed",
    "notes",
]

FALSE_GATE_COLUMNS = [
    "runtime_allowed",
    "reviewed_bank_allowed",
    "protected_preview_allowed",
    "student_facing_allowed",
    "broader_use_allowed",
]

STATUS_REQUIRED_PHRASES = [
    "No Perek 4 protected-preview packet exists.",
    "No runtime activation.",
    "No Perek 4 runtime activation.",
    "No reviewed-bank promotion.",
    "No student-facing content.",
]

REPORT_REQUIRED_SAFETY_PHRASES = [
    "No runtime activation.",
    "No Perek 4 runtime activation.",
    "No reviewed-bank promotion.",
    "No protected-preview packet creation.",
    "No student-facing content.",
]

PROMPT_GUARDRAIL_PHRASES = [
    "Do not create a Perek 4 protected-preview packet.",
    "Do not activate runtime.",
    "Do not promote anything to reviewed bank.",
    "Do not create student-facing content.",
]


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def perek4_packet_paths() -> list[Path]:
    if not PROTECTED_PREVIEW_PACKET_DIR.exists():
        return []
    packet_paths: list[Path] = []
    for path in sorted(PROTECTED_PREVIEW_PACKET_DIR.rglob("*perek_4*")):
        if not path.is_file():
            continue
        path_text = repo_relative(path)
        if "packet_planning" in path.name or "planning-only" in read_text(path):
            continue
        if _is_governed_downstream_perek4_packet(path_text):
            continue
        packet_paths.append(path)
    return packet_paths


def validate_perek_4_source_discovery() -> dict[str, object]:
    errors: list[str] = []
    for path in [
        SOURCE_DISCOVERY_REPORT,
        INVENTORY_PATH,
        DUPLICATE_WARNING_REPORT,
        DUPLICATE_WARNING_TSV,
        EXCLUDED_RISK_LANES_REPORT,
        STATUS_INDEX,
        NEXT_PROMPT,
    ]:
        if not path.exists():
            errors.append(f"missing required artifact: {repo_relative(path)}")

    rows: list[dict[str, str]] = []
    if INVENTORY_PATH.exists():
        rows = read_tsv(INVENTORY_PATH)
        if not rows:
            report_text = read_text(SOURCE_DISCOVERY_REPORT) if SOURCE_DISCOVERY_REPORT.exists() else ""
            if "no safe candidates found" not in report_text.lower():
                errors.append("candidate inventory has zero rows without explicit no-safe-candidates explanation")

        fieldnames = set(rows[0].keys()) if rows else set()
        missing_columns = [column for column in REQUIRED_COLUMNS if column not in fieldnames]
        if missing_columns:
            errors.append(f"candidate inventory missing columns: {missing_columns}")

        candidate_ids = [row.get("candidate_id", "") for row in rows]
        duplicates = [candidate_id for candidate_id, count in Counter(candidate_ids).items() if count > 1]
        if duplicates:
            errors.append(f"duplicate candidate IDs: {duplicates}")

        for index, row in enumerate(rows, start=2):
            context = f"{repo_relative(INVENTORY_PATH)}:{index}"
            if row.get("perek") != "4":
                errors.append(f"{context}: perek must be 4")
            if not re.fullmatch(r"g2srcdisc_p4_\d{3}", row.get("candidate_id", "")):
                errors.append(f"{context}: candidate_id must be Perek 4 scoped")
            if row.get("review_status") != "review_only":
                errors.append(f"{context}: review_status must be review_only")
            if row.get("review_required") != "true":
                errors.append(f"{context}: review_required must be true")
            for column in FALSE_GATE_COLUMNS:
                if row.get(column) != "false":
                    errors.append(f"{context}: {column} must be false")
            for column in [
                "source_artifact",
                "source_row_id",
                "provenance_status",
                "source_confidence",
                "hebrew_token",
                "hebrew_phrase",
            ]:
                if not row.get(column):
                    errors.append(f"{context}: {column} must be populated")
            if row.get("source_artifact") and not (ROOT / row["source_artifact"]).exists():
                errors.append(f"{context}: source_artifact does not exist: {row['source_artifact']}")

    if SOURCE_DISCOVERY_REPORT.exists():
        text = read_text(SOURCE_DISCOVERY_REPORT)
        for phrase in REPORT_REQUIRED_SAFETY_PHRASES:
            if phrase not in text:
                errors.append(f"source discovery report missing safety phrase: {phrase}")
        if "Perek 4 source-to-skill discovery only" not in text:
            errors.append("source discovery report must state source-to-skill discovery only")

    if DUPLICATE_WARNING_REPORT.exists():
        text = read_text(DUPLICATE_WARNING_REPORT)
        if "duplicate עֵץ/session-balance" not in text:
            errors.append("duplicate warning report must explicitly connect to the Perek 3 duplicate-token lesson")
        if "No Perek 4 protected-preview packet was created" not in text:
            errors.append("duplicate warning report must state no Perek 4 protected-preview packet was created")

    if DUPLICATE_WARNING_TSV.exists():
        warning_rows = read_tsv(DUPLICATE_WARNING_TSV)
        if not warning_rows:
            errors.append("duplicate/session-balance warning TSV must have at least one row")
        if not any(row.get("session_balance_warning") == "true" for row in warning_rows):
            errors.append("duplicate/session-balance warning TSV must include true warning rows")

    if EXCLUDED_RISK_LANES_REPORT.exists():
        text = read_text(EXCLUDED_RISK_LANES_REPORT)
        for lane in [
            "Translation/context",
            "Suffix/compound morphology",
            "Advanced verbs",
            "Vav hahipuch",
            "Rashi/commentary",
            "Higher-order comprehension",
        ]:
            if lane not in text:
                errors.append(f"excluded risk lanes report missing lane: {lane}")

    if STATUS_INDEX.exists():
        text = read_text(STATUS_INDEX)
        for phrase in STATUS_REQUIRED_PHRASES:
            if phrase not in text:
                errors.append(f"status index missing safety phrase: {phrase}")
        if "not a protected-preview packet" not in text:
            errors.append("status index must say the inventory is not a protected-preview packet")

    if NEXT_PROMPT.exists():
        prompt = read_text(NEXT_PROMPT)
        for phrase in PROMPT_GUARDRAIL_PHRASES:
            if phrase not in prompt:
                errors.append(f"next prompt missing guardrail phrase: {phrase}")

    packet_paths = perek4_packet_paths()
    if packet_paths:
        errors.append(
            "Perek 4 protected-preview packet artifacts are not allowed in this task: "
            + ", ".join(repo_relative(path) for path in packet_paths)
        )

    skill_counts = dict(sorted(Counter(row.get("skill_family", "") for row in rows).items()))
    duplicate_warning_count = sum(1 for row in rows if row.get("duplicate_token_warning") == "true")
    return {
        "valid": not errors,
        "candidate_count": len(rows),
        "skill_family_counts": skill_counts,
        "candidate_duplicate_warning_count": duplicate_warning_count,
        "checked_paths": [
            repo_relative(SOURCE_DISCOVERY_REPORT),
            repo_relative(INVENTORY_PATH),
            repo_relative(DUPLICATE_WARNING_REPORT),
            repo_relative(EXCLUDED_RISK_LANES_REPORT),
            repo_relative(STATUS_INDEX),
            repo_relative(NEXT_PROMPT),
        ],
        "perek_4_packet_paths": [repo_relative(path) for path in packet_paths],
        "errors": errors,
    }


def main() -> int:
    summary = validate_perek_4_source_discovery()
    print(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True))
    return 0 if summary["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
