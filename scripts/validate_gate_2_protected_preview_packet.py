from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "data" / "gate_2_protected_preview_packets"
REPORTS = DIR / "reports"
README = DIR / "README.md"

TSV = DIR / "bereishis_perek_2_internal_protected_preview_packet.tsv"
PACKET = REPORTS / "bereishis_perek_2_internal_protected_preview_packet.md"
GEN = REPORTS / "bereishis_perek_2_internal_protected_preview_packet_generation_report.md"
COMPLETE = REPORTS / "bereishis_perek_2_round_2_completion_report.md"
EXCLUDED = REPORTS / "bereishis_perek_2_internal_protected_preview_packet_excluded_preserved_report.md"
CAND = ROOT / "data" / "gate_2_protected_preview_candidates" / "bereishis_perek_2_protected_preview_candidates.tsv"

P3_TSV = DIR / "bereishis_perek_3_internal_protected_preview_packet.tsv"
P3_REPORT = REPORTS / "bereishis_perek_3_internal_protected_preview_packet_report.md"
P3_REVIEW_CHECKLIST = REPORTS / "bereishis_perek_3_internal_protected_preview_review_checklist.md"
P3_REVIEW_CHECKLIST_TSV = REPORTS / "bereishis_perek_3_internal_protected_preview_review_checklist.tsv"
P3_REVIEW_DECISIONS_APPLIED = REPORTS / "bereishis_perek_3_internal_protected_preview_review_decisions_applied.md"
P3_REVIEW_DECISIONS_APPLIED_TSV = REPORTS / "bereishis_perek_3_internal_protected_preview_review_decisions_applied.tsv"
P3_ITEM_004_REVISION_PLAN = REPORTS / "bereishis_perek_3_item_004_revision_plan.md"
P3_ITEM_004_REVISION_PLAN_TSV = REPORTS / "bereishis_perek_3_item_004_revision_plan.tsv"
P3_LIMITED_READINESS = REPORTS / "bereishis_perek_3_limited_post_preview_iteration_readiness.md"
P3_LIMITED_READINESS_TSV = REPORTS / "bereishis_perek_3_limited_post_preview_iteration_readiness.tsv"
P3_BLOCKED_REGISTER = REPORTS / "bereishis_perek_3_blocked_from_broader_use_register.md"
P3_BLOCKED_REGISTER_TSV = REPORTS / "bereishis_perek_3_blocked_from_broader_use_register.tsv"
P3_OBSERVATION_TEMPLATE = REPORTS / "bereishis_perek_3_limited_post_preview_observation_template.md"
P3_OBSERVATION_TEMPLATE_TSV = REPORTS / "bereishis_perek_3_limited_post_preview_observation_template.tsv"
P3_CAND = ROOT / "data" / "gate_2_protected_preview_candidates" / "bereishis_perek_3_protected_preview_candidates.tsv"
P3_STATUS_INDEX = (
    ROOT
    / "data"
    / "gate_2_protected_preview_candidates"
    / "reports"
    / "bereishis_perek_3_candidate_status_index.md"
)

REQUIRED_COLUMNS = [
    "protected_preview_packet_item_id",
    "protected_preview_candidate_id",
    "controlled_draft_item_id",
    "source_ref",
    "approved_family",
    "hebrew_token",
    "hebrew_phrase",
    "prompt",
    "answer_choices",
    "expected_answer",
    "correct_answer",
    "explanation",
    "source_evidence_note",
    "caution_note",
    "internal_packet_status",
    "internal_preview_review_status",
    "reviewed_bank_allowed",
    "runtime_allowed",
    "student_facing_allowed",
    "post_preview_review_status",
    "yossi_internal_preview_decision",
    "yossi_internal_preview_notes",
]
GATES = ["reviewed_bank_allowed", "runtime_allowed", "student_facing_allowed"]
REVISION = {"g2p2_001", "g2p2_010", "g2p2_012", "g2p2_013"}
FOLLOWUP = {"g2p2_011", "g2p2_015"}
EXCLUDED_GATE2 = REVISION | FOLLOWUP | {"g2p2_004", "g2p2_005", "g2p2_008", "g2p2_018"}
EXPECTED_P3_APPROVED = {
    "g2ppcand_p3_003",
    "g2ppcand_p3_004",
    "g2ppcand_p3_007",
    "g2ppcand_p3_008",
}
P3_REVISION = {"g2ppcand_p3_001", "g2ppcand_p3_005", "g2ppcand_p3_009", "g2ppcand_p3_010"}
P3_FOLLOWUP = {"g2ppcand_p3_002", "g2ppcand_p3_006"}
P3_EXCLUDED = P3_REVISION | P3_FOLLOWUP
DECISION = "approve_for_internal_protected_preview_packet"
STATUS = "yossi_approved_for_internal_protected_preview_packet"
HEBREW_RE = re.compile(r"[\u0590-\u05FF]")
REVIEW_CHECKLIST_COLUMNS = [
    "packet_item_id",
    "candidate_id",
    "ref",
    "hebrew_token",
    "hebrew_phrase",
    "skill_family",
    "current_review_status",
    "runtime_allowed",
    "reviewed_bank_allowed",
    "student_facing_allowed",
    "reviewer_decision",
    "issue_category",
    "revision_required",
    "reviewer_notes",
    "reviewer_name",
    "review_date",
]
APPLIED_REVIEW_COLUMNS = [
    "packet_item_id",
    "candidate_id",
    "ref",
    "hebrew_token",
    "hebrew_phrase",
    "skill_family",
    "reviewer_decision",
    "reviewer_note",
    "required_revision",
    "runtime_allowed",
    "reviewed_bank_allowed",
    "student_facing_allowed",
    "broader_use_allowed",
    "reviewed_bank_promotion_allowed",
    "runtime_activation_allowed",
]
APPLIED_REVIEW_GATE_COLUMNS = [
    "runtime_allowed",
    "reviewed_bank_allowed",
    "student_facing_allowed",
    "broader_use_allowed",
    "reviewed_bank_promotion_allowed",
    "runtime_activation_allowed",
]
EXPECTED_P3_INTERNAL_REVIEW_COUNTS = {
    "approve_for_limited_post_preview_iteration": 3,
    "approve_with_revision": 1,
    "needs_follow_up": 0,
    "reject_for_broader_use": 0,
    "source_only": 0,
}
EXPECTED_P3_LIMITED_READINESS = {
    "g2ppcand_p3_003",
    "g2ppcand_p3_007",
    "g2ppcand_p3_008",
}
P3_BLOCKED_FROM_BROADER_USE = {"g2ppcand_p3_004"}
REVISION_PLAN_COLUMNS = [
    "packet_item_id",
    "candidate_id",
    "ref",
    "hebrew_token",
    "current_decision",
    "revision_issue",
    "recommended_path",
    "broader_use_blocked",
    "runtime_allowed",
    "reviewed_bank_allowed",
    "student_facing_allowed",
    "future_acceptance_criteria",
]
LIMITED_READINESS_COLUMNS = [
    "packet_item_id",
    "candidate_id",
    "ref",
    "hebrew_token",
    "hebrew_phrase",
    "skill_family",
    "applied_review_decision",
    "limited_iteration_ready",
    "readiness_reason",
    "runtime_allowed",
    "reviewed_bank_allowed",
    "student_facing_allowed",
    "broader_use_allowed",
    "reviewed_bank_promotion_allowed",
    "runtime_activation_allowed",
    "next_review_focus",
    "post_iteration_decision",
]
LIMITED_READINESS_GATE_COLUMNS = [
    "runtime_allowed",
    "reviewed_bank_allowed",
    "student_facing_allowed",
    "broader_use_allowed",
    "reviewed_bank_promotion_allowed",
    "runtime_activation_allowed",
]
BLOCKED_REGISTER_COLUMNS = [
    "packet_item_id",
    "candidate_id",
    "ref",
    "hebrew_token",
    "current_decision",
    "block_reason",
    "related_duplicate_item",
    "broader_use_blocked",
    "runtime_allowed",
    "reviewed_bank_allowed",
    "student_facing_allowed",
    "future_resolution_required",
]
OBSERVATION_TEMPLATE_COLUMNS = [
    "packet_item_id",
    "candidate_id",
    "ref",
    "hebrew_token",
    "reviewer_name",
    "review_date",
    "observed_student_confusion",
    "prompt_clarity_rating",
    "distractor_fairness_rating",
    "explanation_accuracy_rating",
    "too_easy_too_hard",
    "repetition_or_fatigue_note",
    "source_confidence",
    "recommended_next_decision",
    "notes",
]
OBSERVATION_BLANK_COLUMNS = [
    "reviewer_name",
    "review_date",
    "observed_student_confusion",
    "prompt_clarity_rating",
    "distractor_fairness_rating",
    "explanation_accuracy_rating",
    "too_easy_too_hard",
    "repetition_or_fatigue_note",
    "source_confidence",
    "recommended_next_decision",
    "notes",
]


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def load_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def has_hebrew(value: str) -> bool:
    return bool(HEBREW_RE.search(value or ""))


def bad_phrase(text: str, phrase: str) -> bool:
    for line in text.lower().splitlines():
        if phrase in line and not any(
            marker in line
            for marker in (
                "not ",
                "no ",
                "false",
                "closed",
                "does not",
                "still requires",
                "requires post-preview",
                "remain excluded",
                "not reviewed-bank",
                "not runtime",
                "not student-facing",
            )
        ):
            return True
    return False


def approved_candidates(candidate_tsv: Path) -> dict[str, dict[str, str]]:
    _, candidate_rows = load_tsv(candidate_tsv)
    return {
        row["protected_preview_candidate_id"]: row
        for row in candidate_rows
        if row.get("yossi_protected_preview_decision") == DECISION
        and row.get("protected_preview_candidate_status") == STATUS
    }


def validate_packet_spec(
    *,
    name: str,
    packet_tsv: Path,
    candidate_tsv: Path,
    expected_count: int,
    expected_candidate_ids: set[str] | None,
    excluded_gate_ids: set[str],
    excluded_candidate_ids: set[str],
    errors: list[str],
    family_counts: Counter[str],
) -> dict[str, Any]:
    fields, rows = load_tsv(packet_tsv)
    if fields != REQUIRED_COLUMNS:
        errors.append(f"{name}: internal packet TSV columns do not match required schema")
    if len(rows) != expected_count:
        errors.append(f"{name}: internal packet TSV must have exactly {expected_count} rows, found {len(rows)}")

    approved = approved_candidates(candidate_tsv)
    approved_id_set = set(approved)
    expected_ids = expected_candidate_ids if expected_candidate_ids is not None else approved_id_set
    if approved_id_set != expected_ids:
        errors.append(f"{name}: approved candidate ID set does not match expected packet set")

    included: set[str] = set()
    for row in rows:
        rid = row.get("protected_preview_packet_item_id", "?")
        candidate_id = row.get("protected_preview_candidate_id", "")
        included.add(candidate_id)
        family_counts[row.get("approved_family", "")] += 1
        source = approved.get(candidate_id)
        if candidate_id in excluded_candidate_ids:
            errors.append(f"{rid}: revision/follow-up candidate included")
        if not source:
            errors.append(f"{rid}: must link to approved protected-preview candidate")
        else:
            for field in (
                "protected_preview_candidate_id",
                "controlled_draft_item_id",
                "source_ref",
                "approved_family",
                "hebrew_token",
                "hebrew_phrase",
                "prompt",
                "answer_choices",
                "expected_answer",
                "correct_answer",
                "explanation",
                "source_evidence_note",
                "caution_note",
            ):
                if row.get(field, "") != source.get(field, ""):
                    errors.append(f"{rid}: {field} must match source candidate")
            if source.get("gate_2_input_candidate_id") in excluded_gate_ids:
                errors.append(f"{rid}: excluded Gate 2 row included")
        if row.get("approved_family") != "basic_noun_recognition":
            errors.append(f"{rid}: unsafe family included")
        if row.get("internal_packet_status") != "internal_protected_preview_packet_only":
            errors.append(f"{rid}: internal_packet_status must be internal_protected_preview_packet_only")
        if row.get("internal_preview_review_status") != "needs_internal_review":
            errors.append(f"{rid}: internal_preview_review_status must be needs_internal_review")
        if row.get("post_preview_review_status") != "not_started":
            errors.append(f"{rid}: post_preview_review_status must be not_started")
        for gate in GATES:
            if row.get(gate) != "false":
                errors.append(f"{rid}: {gate} must be false")
        if row.get("yossi_internal_preview_decision") or row.get("yossi_internal_preview_notes"):
            errors.append(f"{rid}: internal preview decision fields must be blank")
        if not has_hebrew(row.get("hebrew_token", "")) or not has_hebrew(row.get("hebrew_phrase", "")):
            errors.append(f"{rid}: must contain real Hebrew")
        if any(bad in "\t".join(row.values()) for bad in ("???", "Ã—", "Ã–")):
            errors.append(f"{rid}: contains placeholder corruption")

    if included != expected_ids:
        errors.append(f"{name}: internal packet rows must exactly match expected approved candidates")

    return {
        "packet_path": rel(packet_tsv),
        "row_count": len(rows),
        "candidate_ids": sorted(included),
    }


def validate_gate_2_protected_preview_packet() -> dict[str, object]:
    errors: list[str] = []
    required_artifacts = (
        README,
        TSV,
        PACKET,
        GEN,
        COMPLETE,
        EXCLUDED,
        CAND,
        P3_TSV,
        P3_REPORT,
        P3_REVIEW_CHECKLIST,
        P3_REVIEW_CHECKLIST_TSV,
        P3_REVIEW_DECISIONS_APPLIED,
        P3_REVIEW_DECISIONS_APPLIED_TSV,
        P3_ITEM_004_REVISION_PLAN,
        P3_ITEM_004_REVISION_PLAN_TSV,
        P3_LIMITED_READINESS,
        P3_LIMITED_READINESS_TSV,
        P3_BLOCKED_REGISTER,
        P3_BLOCKED_REGISTER_TSV,
        P3_OBSERVATION_TEMPLATE,
        P3_OBSERVATION_TEMPLATE_TSV,
        P3_CAND,
        P3_STATUS_INDEX,
    )
    for path in required_artifacts:
        if not path.exists():
            errors.append(f"missing internal packet artifact: {rel(path)}")
    if errors:
        return {"valid": False, "errors": errors}

    family_counts: Counter[str] = Counter()
    perek_summaries = {
        "perek_2": validate_packet_spec(
            name="perek_2",
            packet_tsv=TSV,
            candidate_tsv=CAND,
            expected_count=10,
            expected_candidate_ids=None,
            excluded_gate_ids=EXCLUDED_GATE2,
            excluded_candidate_ids=set(),
            errors=errors,
            family_counts=family_counts,
        ),
        "perek_3": validate_packet_spec(
            name="perek_3",
            packet_tsv=P3_TSV,
            candidate_tsv=P3_CAND,
            expected_count=4,
            expected_candidate_ids=EXPECTED_P3_APPROVED,
            excluded_gate_ids=set(),
            excluded_candidate_ids=P3_EXCLUDED,
            errors=errors,
            family_counts=family_counts,
        ),
    }

    p2_text = "\n".join(path.read_text(encoding="utf-8") for path in (README, PACKET, GEN, COMPLETE, EXCLUDED))
    for phrase in (
        "internal protected-preview packet only",
        "Packet item count: 10",
        "Perek 2 is complete",
        "Reviewed-bank entries created: 0",
        "Runtime changes: 0",
        "Student-facing content: 0",
    ):
        if phrase not in p2_text:
            errors.append(f"required phrase missing: {phrase}")
    for gid in REVISION | FOLLOWUP:
        if gid not in p2_text:
            errors.append(f"excluded report missing {gid}")
    for phrase in (
        "reviewed_bank_ready",
        "runtime_ready",
        "approved_for_reviewed_bank",
        "approved_for_runtime",
        "approved_for_student_facing",
    ):
        if bad_phrase(p2_text, phrase):
            errors.append(f"forbidden phrase appears without clear negation: {phrase}")
    if "??" in p2_text or "Ã—" in p2_text or "Ã–" in p2_text:
        errors.append("packet reports contain placeholder corruption")

    readme = README.read_text(encoding="utf-8")
    for path in (
        TSV,
        PACKET,
        GEN,
        COMPLETE,
        EXCLUDED,
        P3_TSV,
        P3_REPORT,
        P3_REVIEW_CHECKLIST,
        P3_REVIEW_CHECKLIST_TSV,
        P3_REVIEW_DECISIONS_APPLIED,
        P3_REVIEW_DECISIONS_APPLIED_TSV,
        P3_ITEM_004_REVISION_PLAN,
        P3_ITEM_004_REVISION_PLAN_TSV,
        P3_LIMITED_READINESS,
        P3_LIMITED_READINESS_TSV,
        P3_BLOCKED_REGISTER,
        P3_BLOCKED_REGISTER_TSV,
        P3_OBSERVATION_TEMPLATE,
        P3_OBSERVATION_TEMPLATE_TSV,
    ):
        if rel(path) not in readme:
            errors.append(f"README must link {rel(path)}")

    p3_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (
            README,
            P3_REPORT,
            P3_STATUS_INDEX,
            P3_REVIEW_CHECKLIST,
            P3_REVIEW_DECISIONS_APPLIED,
            P3_ITEM_004_REVISION_PLAN,
            P3_LIMITED_READINESS,
            P3_BLOCKED_REGISTER,
            P3_OBSERVATION_TEMPLATE,
        )
    )
    for candidate_id in sorted(EXPECTED_P3_APPROVED):
        if candidate_id not in p3_text:
            errors.append(f"Perek 3 packet report/status missing {candidate_id}")
    for phrase in (
        "Included approved rows: 4",
        "Excluded revision rows: 4",
        "Excluded follow-up rows: 2",
        "No Perek 3 runtime activation",
        "No reviewed-bank promotion",
        "No student-facing content",
        "four-item internal protected-preview packet now exists",
        "does not apply decisions",
        "does not activate or promote anything",
        "approve_for_limited_post_preview_iteration",
        "repetition/session-balance",
        "planning artifact only",
        "broader use blocked",
        "limited post-preview iteration readiness",
        "A three-item limited post-preview iteration readiness lane exists",
        "A blocked broader-use register keeps `g2ppcand_p3_004` out of the limited readiness lane",
        "Future observation decisions must be recorded in a later explicit task",
        "No protected-preview packet creation",
    ):
        if phrase not in p3_text:
            errors.append(f"Perek 3 packet/status required phrase missing: {phrase}")
    if EXPECTED_P3_APPROVED.intersection(P3_EXCLUDED):
        errors.append("Perek 3 expected packet IDs overlap excluded IDs")
    for candidate_id in sorted(P3_EXCLUDED):
        if f"### " in P3_REVIEW_CHECKLIST.read_text(encoding="utf-8") and f" / {candidate_id}" in P3_REVIEW_CHECKLIST.read_text(encoding="utf-8"):
            errors.append(f"Perek 3 excluded candidate appears as checklist item card: {candidate_id}")

    checklist_fields, checklist_rows = load_tsv(P3_REVIEW_CHECKLIST_TSV)
    if checklist_fields != REVIEW_CHECKLIST_COLUMNS:
        errors.append("Perek 3 review checklist TSV columns do not match required schema")
    if len(checklist_rows) != 4:
        errors.append(f"Perek 3 review checklist TSV must have exactly 4 rows, found {len(checklist_rows)}")
    checklist_ids = {row.get("candidate_id", "") for row in checklist_rows}
    if checklist_ids != EXPECTED_P3_APPROVED:
        errors.append("Perek 3 review checklist TSV candidate IDs must exactly match approved packet IDs")
    for row in checklist_rows:
        rid = row.get("packet_item_id", "?")
        if row.get("candidate_id") in P3_EXCLUDED:
            errors.append(f"{rid}: excluded Perek 3 candidate included in checklist TSV")
        for gate in GATES:
            if row.get(gate) != "false":
                errors.append(f"{rid}: checklist TSV {gate} must be false")
        if row.get("candidate_id") == "g2ppcand_p3_004":
            if row.get("reviewer_decision") != "approve_with_revision":
                errors.append(f"{rid}: g2ppcand_p3_004 checklist decision must be approve_with_revision")
            if "repetition/session-balance" not in row.get("revision_required", ""):
                errors.append(f"{rid}: g2ppcand_p3_004 checklist revision must mention repetition/session-balance")
        elif row.get("reviewer_decision") != "approve_for_limited_post_preview_iteration":
            errors.append(f"{rid}: checklist approved rows must be approve_for_limited_post_preview_iteration")
        for reviewer_field in ("reviewer_name", "review_date"):
            if row.get(reviewer_field):
                errors.append(f"{rid}: checklist TSV reviewer metadata field must be blank: {reviewer_field}")

    applied_fields, applied_rows = load_tsv(P3_REVIEW_DECISIONS_APPLIED_TSV)
    if applied_fields != APPLIED_REVIEW_COLUMNS:
        errors.append("Perek 3 applied review TSV columns do not match required schema")
    if len(applied_rows) != 4:
        errors.append(f"Perek 3 applied review TSV must have exactly 4 rows, found {len(applied_rows)}")
    applied_ids = {row.get("candidate_id", "") for row in applied_rows}
    if applied_ids != EXPECTED_P3_APPROVED:
        errors.append("Perek 3 applied review TSV candidate IDs must exactly match approved packet IDs")
    applied_counts = Counter(row.get("reviewer_decision", "") for row in applied_rows)
    for decision, expected_count in EXPECTED_P3_INTERNAL_REVIEW_COUNTS.items():
        if applied_counts.get(decision, 0) != expected_count:
            errors.append(f"Perek 3 applied review expected {expected_count} {decision} rows, found {applied_counts.get(decision, 0)}")
    for row in applied_rows:
        rid = row.get("packet_item_id", "?")
        cid = row.get("candidate_id", "")
        if cid in P3_EXCLUDED:
            errors.append(f"{rid}: excluded Perek 3 candidate included in applied review TSV")
        for gate in APPLIED_REVIEW_GATE_COLUMNS:
            if row.get(gate) != "false":
                errors.append(f"{rid}: applied review TSV {gate} must be false")
        if cid == "g2ppcand_p3_004":
            if row.get("reviewer_decision") != "approve_with_revision":
                errors.append(f"{rid}: g2ppcand_p3_004 must be approve_with_revision")
            if "repetition/session-balance" not in row.get("required_revision", ""):
                errors.append(f"{rid}: g2ppcand_p3_004 required revision must mention repetition/session-balance")
        elif row.get("reviewer_decision") != "approve_for_limited_post_preview_iteration":
            errors.append(f"{rid}: non-revision applied review rows must be approve_for_limited_post_preview_iteration")

    revision_plan_text = P3_ITEM_004_REVISION_PLAN.read_text(encoding="utf-8")
    if "g2ppcand_p3_004" not in revision_plan_text or "g2ppacket_p3_002" not in revision_plan_text:
        errors.append("Perek 3 item 004 revision plan must identify g2ppcand_p3_004 / g2ppacket_p3_002")
    for candidate_id in EXPECTED_P3_APPROVED - {"g2ppcand_p3_004"}:
        if f"Candidate: `{candidate_id}`" in revision_plan_text:
            errors.append(f"Perek 3 revision plan targets non-revision candidate: {candidate_id}")
    for phrase in (
        "planning artifact only",
        "It does not revise the item.",
        "It does not apply a new decision.",
        "No runtime activation",
        "No reviewed-bank promotion",
        "No student-facing content creation",
        "broader use blocked",
        "repetition/session-balance",
    ):
        if phrase not in revision_plan_text:
            errors.append(f"Perek 3 item 004 revision plan missing phrase: {phrase}")

    revision_fields, revision_rows = load_tsv(P3_ITEM_004_REVISION_PLAN_TSV)
    if revision_fields != REVISION_PLAN_COLUMNS:
        errors.append("Perek 3 item 004 revision plan TSV columns do not match required schema")
    if len(revision_rows) != 1:
        errors.append(f"Perek 3 item 004 revision plan TSV must have exactly 1 row, found {len(revision_rows)}")
    if revision_rows:
        row = revision_rows[0]
        if row.get("candidate_id") != "g2ppcand_p3_004" or row.get("packet_item_id") != "g2ppacket_p3_002":
            errors.append("Perek 3 item 004 revision plan TSV must target g2ppcand_p3_004 / g2ppacket_p3_002 only")
        if row.get("current_decision") != "approve_with_revision":
            errors.append("Perek 3 item 004 revision plan TSV must preserve approve_with_revision")
        if row.get("broader_use_blocked") != "true":
            errors.append("Perek 3 item 004 revision plan TSV must keep broader_use_blocked=true")
        for gate in GATES:
            if row.get(gate) != "false":
                errors.append(f"Perek 3 item 004 revision plan TSV {gate} must be false")
        if "repetition/session-balance" not in row.get("revision_issue", ""):
            errors.append("Perek 3 item 004 revision plan TSV must mention repetition/session-balance")

    readiness_text = P3_LIMITED_READINESS.read_text(encoding="utf-8")
    for phrase in (
        "Internal-only limited post-preview iteration readiness",
        "This is not runtime content.",
        "This is not reviewed-bank content.",
        "This is not student-facing content.",
        "This does not revise item content.",
        "This does not apply new review decisions.",
        "This does not create a new protected-preview packet.",
        "blocked from broader use",
        "Why only 3 items",
        "No runtime activation",
        "No reviewed-bank promotion",
        "No protected-preview packet creation",
        "No student-facing content creation",
    ):
        if phrase not in readiness_text:
            errors.append(f"Perek 3 limited readiness report missing phrase: {phrase}")
    for candidate_id in EXPECTED_P3_LIMITED_READINESS:
        if candidate_id not in readiness_text:
            errors.append(f"Perek 3 limited readiness report missing included candidate: {candidate_id}")
    if "g2ppcand_p3_004" not in readiness_text or "not rejected, not revised, not promoted" not in readiness_text:
        errors.append("Perek 3 limited readiness report must name item 004 as blocked but not rejected/revised/promoted")

    readiness_fields, readiness_rows = load_tsv(P3_LIMITED_READINESS_TSV)
    if readiness_fields != LIMITED_READINESS_COLUMNS:
        errors.append("Perek 3 limited readiness TSV columns do not match required schema")
    if len(readiness_rows) != 3:
        errors.append(f"Perek 3 limited readiness TSV must have exactly 3 rows, found {len(readiness_rows)}")
    readiness_ids = {row.get("candidate_id", "") for row in readiness_rows}
    if readiness_ids != EXPECTED_P3_LIMITED_READINESS:
        errors.append("Perek 3 limited readiness TSV candidate IDs must exactly match the three clean items")
    if readiness_ids.intersection(P3_BLOCKED_FROM_BROADER_USE):
        errors.append("Perek 3 blocked item appears in limited readiness TSV")
    for row in readiness_rows:
        rid = row.get("packet_item_id", "?")
        if row.get("applied_review_decision") != "approve_for_limited_post_preview_iteration":
            errors.append(f"{rid}: limited readiness row must preserve approve_for_limited_post_preview_iteration")
        if row.get("limited_iteration_ready") != "true":
            errors.append(f"{rid}: limited_iteration_ready must be true")
        if row.get("post_iteration_decision"):
            errors.append(f"{rid}: post_iteration_decision must remain blank")
        for gate in LIMITED_READINESS_GATE_COLUMNS:
            if row.get(gate) != "false":
                errors.append(f"{rid}: limited readiness TSV {gate} must be false")

    blocked_text = P3_BLOCKED_REGISTER.read_text(encoding="utf-8")
    for phrase in (
        "Blocked from broader use register",
        "g2ppcand_p3_004",
        "g2ppacket_p3_002",
        "repetition/session-balance",
        "broader_use_blocked=true",
        "This item is not rejected.",
        "This item is not revised by this task.",
        "This item is not approved for broader use.",
        "This item remains internal evidence only.",
        "No runtime activation",
        "No reviewed-bank promotion",
        "No student-facing content creation",
    ):
        if phrase not in blocked_text:
            errors.append(f"Perek 3 blocked register missing phrase: {phrase}")

    blocked_fields, blocked_rows = load_tsv(P3_BLOCKED_REGISTER_TSV)
    if blocked_fields != BLOCKED_REGISTER_COLUMNS:
        errors.append("Perek 3 blocked register TSV columns do not match required schema")
    if len(blocked_rows) != 1:
        errors.append(f"Perek 3 blocked register TSV must have exactly 1 row, found {len(blocked_rows)}")
    if blocked_rows:
        row = blocked_rows[0]
        if row.get("candidate_id") != "g2ppcand_p3_004" or row.get("packet_item_id") != "g2ppacket_p3_002":
            errors.append("Perek 3 blocked register TSV must target g2ppcand_p3_004 / g2ppacket_p3_002 only")
        if row.get("current_decision") != "approve_with_revision":
            errors.append("Perek 3 blocked register TSV must preserve approve_with_revision")
        if row.get("related_duplicate_item") != "g2ppcand_p3_003":
            errors.append("Perek 3 blocked register TSV must identify g2ppcand_p3_003 as duplicate item")
        if row.get("broader_use_blocked") != "true":
            errors.append("Perek 3 blocked register TSV must keep broader_use_blocked=true")
        if "repetition/session-balance" not in row.get("block_reason", ""):
            errors.append("Perek 3 blocked register TSV must mention repetition/session-balance")
        for gate in GATES:
            if row.get(gate) != "false":
                errors.append(f"Perek 3 blocked register TSV {gate} must be false")

    observation_text = P3_OBSERVATION_TEMPLATE.read_text(encoding="utf-8")
    for phrase in (
        "Limited post-preview observation template",
        "Observation fields are blank",
        "keep_limited_iteration",
        "revise_before_next_iteration",
        "needs_follow_up",
        "reject_for_broader_use",
        "candidate_for_future_reviewed_bank_consideration",
        "No runtime activation",
        "No reviewed-bank promotion",
        "No student-facing content creation",
    ):
        if phrase not in observation_text:
            errors.append(f"Perek 3 observation template missing phrase: {phrase}")
    for candidate_id in EXPECTED_P3_LIMITED_READINESS:
        if candidate_id not in observation_text:
            errors.append(f"Perek 3 observation template missing active candidate: {candidate_id}")
    if "### g2ppacket_p3_002 / g2ppcand_p3_004" in observation_text:
        errors.append("Perek 3 blocked item appears as an active observation card")

    observation_fields, observation_rows = load_tsv(P3_OBSERVATION_TEMPLATE_TSV)
    if observation_fields != OBSERVATION_TEMPLATE_COLUMNS:
        errors.append("Perek 3 observation template TSV columns do not match required schema")
    if len(observation_rows) != 3:
        errors.append(f"Perek 3 observation template TSV must have exactly 3 rows, found {len(observation_rows)}")
    observation_ids = {row.get("candidate_id", "") for row in observation_rows}
    if observation_ids != EXPECTED_P3_LIMITED_READINESS:
        errors.append("Perek 3 observation template TSV candidate IDs must exactly match the three clean items")
    if observation_ids.intersection(P3_BLOCKED_FROM_BROADER_USE):
        errors.append("Perek 3 blocked item appears in observation template TSV")
    for row in observation_rows:
        rid = row.get("packet_item_id", "?")
        for field in OBSERVATION_BLANK_COLUMNS:
            if row.get(field):
                errors.append(f"{rid}: observation template field must be blank: {field}")

    return {
        "valid": not errors,
        "errors": errors,
        "packet_path": rel(TSV),
        "row_count": sum(int(summary["row_count"]) for summary in perek_summaries.values()),
        "family_counts": dict(family_counts),
        "perek_summaries": perek_summaries,
    }


def main() -> int:
    summary = validate_gate_2_protected_preview_packet()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
