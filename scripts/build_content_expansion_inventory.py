"""Build planning-only content expansion inventory artifacts.

This script reads existing repo artifacts and writes inventory/gap/candidate
planning files. It never modifies runtime scope, reviewed bank, source truth, or
question generation assets.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
OUT_DIR = ROOT / "data" / "content_expansion_planning"
DATE = "2026_04_30"

INVENTORY_TSV = OUT_DIR / f"content_expansion_inventory_{DATE}.tsv"
INVENTORY_JSON = OUT_DIR / f"content_expansion_inventory_{DATE}.json"
GAP_MD = OUT_DIR / f"content_expansion_gap_map_{DATE}.md"
GAP_JSON = OUT_DIR / f"content_expansion_gap_map_{DATE}.json"
PLAN_MD = OUT_DIR / f"content_expansion_candidate_plan_{DATE}.md"
PLAN_JSON = OUT_DIR / f"content_expansion_candidate_plan_{DATE}.json"

INVENTORY_COLUMNS = [
    "inventory_id",
    "source_area",
    "source_file",
    "parsha",
    "perek",
    "pasuk_start",
    "pasuk_end",
    "pasuk_ref",
    "skill",
    "subskill",
    "question_type",
    "standard_id",
    "source_status",
    "extraction_status",
    "teacher_review_status",
    "protected_preview_status",
    "reviewed_bank_status",
    "runtime_status",
    "evidence_artifacts",
    "blocker_reason",
    "safe_next_use",
    "recommended_next_gate",
]

SAFETY_FLAGS = {
    "planning_only": True,
    "content_expansion_performed": False,
    "runtime_scope_widened": False,
    "perek_activated": False,
    "reviewed_bank_promoted": False,
    "runtime_content_promoted": False,
    "question_generation_changed": False,
    "question_selection_changed": False,
    "question_selection_weighting_changed": False,
    "scoring_mastery_changed": False,
    "source_truth_changed": False,
    "fake_teacher_approval_created": False,
    "fake_student_data_created": False,
    "raw_logs_exposed": False,
    "validators_weakened": False,
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def parse_range_from_name(name: str) -> tuple[str, str, str] | None:
    match = re.search(r"bereishis_(\d+)_(\d+)_to_(\d+)_(\d+)", name)
    if not match:
        match = re.search(r"perek_(\d+)", name)
        if not match:
            return None
        perek = match.group(1)
        return perek, "", ""
    perek_start, pasuk_start, perek_end, pasuk_end = match.groups()
    perek = perek_start if perek_start == perek_end else f"{perek_start}-{perek_end}"
    return perek, pasuk_start, pasuk_end


def active_runtime_scope() -> dict[str, Any]:
    from assessment_scope import active_scope_summary

    return active_scope_summary()


def row_template(**kwargs: Any) -> dict[str, str]:
    row = {key: "" for key in INVENTORY_COLUMNS}
    row.update({key: "" if value is None else str(value) for key, value in kwargs.items()})
    return row


def build_inventory_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    idx = 1

    scope = active_runtime_scope()
    scope_range = scope.get("range") or {}
    start = scope_range.get("start") or {}
    end = scope_range.get("end") or {}
    rows.append(
        row_template(
            inventory_id=f"ceinv_{idx:03d}",
            source_area="active_runtime_scope",
            source_file="assessment_scope.py",
            parsha="Bereishis",
            perek=f"{start.get('perek')}-{end.get('perek')}",
            pasuk_start=start.get("pasuk"),
            pasuk_end=end.get("pasuk"),
            pasuk_ref=f"Bereishis {start.get('perek')}:{start.get('pasuk')}-{end.get('perek')}:{end.get('pasuk')}",
            source_status="active parsed local corpus",
            runtime_status="runtime_active",
            safe_next_use="runtime_active_existing_only",
            recommended_next_gate="do_not_expand_in_planning_gate",
            evidence_artifacts="assessment_scope.py; data/corpus_manifest.json",
        )
    )
    idx += 1

    source_text = ROOT / "data/source_texts/bereishis_hebrew_menukad_taamim.tsv"
    rows.append(
        row_template(
            inventory_id=f"ceinv_{idx:03d}",
            source_area="source_text",
            source_file=rel(source_text),
            parsha="Bereishis",
            perek="1-50",
            pasuk_start="1",
            pasuk_end="26",
            pasuk_ref="Bereishis 1:1-50:26",
            source_status="canonical_source_available",
            runtime_status="source_truth_only",
            safe_next_use="source_support_only",
            recommended_next_gate="candidate_selection_requires_review_artifacts",
            blocker_reason="source text support is not content approval",
        )
    )
    idx += 1

    for path in sorted((ROOT / "data/verified_source_skill_maps").glob("*.tsv")):
        tsv_rows = read_tsv(path)
        rng = parse_range_from_name(path.name) or ("", "", "")
        skills = sorted({row.get("skill_primary", "") for row in tsv_rows if row.get("skill_primary")})
        standards = sorted({row.get("zekelman_standard", "") for row in tsv_rows if row.get("zekelman_standard")})
        question_allowed = sum(1 for row in tsv_rows if str(row.get("question_allowed", "")).lower() == "true")
        preview_allowed = sum(1 for row in tsv_rows if str(row.get("protected_preview_allowed", "")).lower() == "true")
        reviewed_allowed = sum(1 for row in tsv_rows if str(row.get("reviewed_bank_allowed", "")).lower() == "true")
        runtime_allowed = sum(1 for row in tsv_rows if str(row.get("runtime_allowed", "")).lower() == "true")
        safe_next = "teacher_review_ready" if question_allowed or preview_allowed else "extraction_verified_planning_only"
        if reviewed_allowed:
            safe_next = "reviewed_bank_candidate"
        if runtime_allowed:
            safe_next = "blocked"
        rows.append(
            row_template(
                inventory_id=f"ceinv_{idx:03d}",
                source_area="verified_source_skill_map",
                source_file=rel(path),
                parsha="Bereishis",
                perek=rng[0],
                pasuk_start=rng[1],
                pasuk_end=rng[2],
                skill="; ".join(skills[:8]),
                standard_id="; ".join(standards[:5]),
                source_status="source_to_skill_map_present",
                extraction_status="verified_or_review_tracked",
                teacher_review_status="map_verification_artifacts_present",
                protected_preview_status=f"protected_preview_allowed_rows={preview_allowed}",
                reviewed_bank_status=f"reviewed_bank_allowed_rows={reviewed_allowed}",
                runtime_status=f"runtime_allowed_rows={runtime_allowed}",
                evidence_artifacts=rel(path),
                blocker_reason="verification is not question approval",
                safe_next_use=safe_next,
                recommended_next_gate="build_or_review_candidate_packet",
            )
        )
        idx += 1

    for path in sorted((ROOT / "data/gate_2_protected_preview_candidates").glob("*.tsv")):
        tsv_rows = read_tsv(path)
        rng = parse_range_from_name(path.name) or ("", "", "")
        decisions = Counter(row.get("decision") or row.get("review_decision") or row.get("status") or "unknown" for row in tsv_rows)
        rows.append(
            row_template(
                inventory_id=f"ceinv_{idx:03d}",
                source_area="protected_preview_candidates",
                source_file=rel(path),
                parsha="Bereishis",
                perek=rng[0],
                pasuk_start=rng[1],
                pasuk_end=rng[2],
                skill="basic_noun_recognition",
                question_type="source_discovery_or_protected_preview_candidate",
                teacher_review_status="; ".join(f"{key}={value}" for key, value in sorted(decisions.items())[:6]),
                protected_preview_status="candidate_layer_present",
                reviewed_bank_status="not_reviewed_bank",
                runtime_status="not_runtime_active",
                evidence_artifacts=rel(path),
                blocker_reason="protected preview candidate is not reviewed bank or runtime approval",
                safe_next_use="protected_preview_ready",
                recommended_next_gate="build_limited_internal_packet_or_record_observation",
            )
        )
        idx += 1

    for path in sorted((ROOT / "data/gate_2_protected_preview_packets").glob("*.tsv")):
        tsv_rows = read_tsv(path)
        rng = parse_range_from_name(path.name) or ("", "", "")
        rows.append(
            row_template(
                inventory_id=f"ceinv_{idx:03d}",
                source_area="protected_preview_packet",
                source_file=rel(path),
                parsha="Bereishis",
                perek=rng[0],
                pasuk_start=rng[1],
                pasuk_end=rng[2],
                skill="basic_noun_recognition",
                question_type="internal_protected_preview_packet",
                protected_preview_status=f"packet_rows={len(tsv_rows)}",
                reviewed_bank_status="not_reviewed_bank",
                runtime_status="not_runtime_active",
                evidence_artifacts=rel(path),
                blocker_reason="internal protected preview is not runtime activation",
                safe_next_use="protected_preview_ready",
                recommended_next_gate="teacher_observation_or_revision_gate",
            )
        )
        idx += 1

    manifest = read_json(ROOT / "data/curriculum_extraction/curriculum_extraction_manifest.json", {})
    for batch in manifest.get("resource_batches", []):
        rows.append(
            row_template(
                inventory_id=f"ceinv_{idx:03d}",
                source_area="curriculum_extraction_batch",
                source_file="data/curriculum_extraction/curriculum_extraction_manifest.json",
                parsha="Bereishis" if "Bereishis" in str(batch.get("label", "")) or "bereishis" in str(batch).lower() else "mixed",
                perek=_batch_perek_label(batch),
                pasuk_ref=_batch_range_label(batch),
                source_status=batch.get("status"),
                extraction_status=batch.get("review_status") or batch.get("status"),
                teacher_review_status=batch.get("review_status") or "needs_review",
                protected_preview_status="not_protected_preview",
                reviewed_bank_status="not_reviewed_bank",
                runtime_status="not_runtime_active",
                evidence_artifacts="; ".join(batch.get("review_artifacts") or []),
                blocker_reason="extraction verification is not question approval",
                safe_next_use="extraction_verified_planning_only" if batch.get("review_status") == "reviewed" else "pending_teacher_review",
                recommended_next_gate="teacher_review_packet_or_candidate_packet",
            )
        )
        idx += 1

    standard_bank = ROOT / "data/standards/zekelman/reviewed_bank/standard_3_mvp_reviewed_bank.json"
    standard_payload = read_json(standard_bank, {})
    rows.append(
        row_template(
            inventory_id=f"ceinv_{idx:03d}",
            source_area="zekelman_standard_3_reviewed_bank",
            source_file=rel(standard_bank),
            standard_id="Zekelman Standard 3",
            source_status="standard_3_review_artifacts_present",
            teacher_review_status="standard_3_teacher_review_layer_present",
            protected_preview_status="standard_3_protected_preview_review_complete",
            reviewed_bank_status="standard_3_reviewed_bank_artifact_present",
            runtime_status="not_runtime_active_for_content_expansion_gate",
            evidence_artifacts="data/standards/zekelman/reports/standard_3_reviewed_bank_promotion_report.md",
            blocker_reason="standard reviewed-bank planning does not authorize this branch to activate runtime content",
            safe_next_use="reviewed_bank_candidate",
            recommended_next_gate="separate_standard_3_runtime_activation_gate_if_authorized",
            skill=str(len(standard_payload.get("records", []))) + " reviewed-bank records" if isinstance(standard_payload, dict) else "reviewed bank artifact",
        )
    )
    idx += 1

    diag_summary = ROOT / "data/diagnostic_preview/reports/bereishis_1_1_to_2_3_preview_summary.json"
    rows.append(
        row_template(
            inventory_id=f"ceinv_{idx:03d}",
            source_area="diagnostic_preview",
            source_file=rel(diag_summary),
            parsha="Bereishis",
            perek="1-2",
            pasuk_start="1",
            pasuk_end="3",
            question_type="diagnostic_preview",
            source_status="diagnostic_preview_artifacts_present",
            extraction_status="preview_generation_optional_test_has_known_failure",
            teacher_review_status="manual_review_packet_present",
            protected_preview_status="diagnostic_preview_only",
            reviewed_bank_status="not_reviewed_bank",
            runtime_status="not_runtime_active",
            evidence_artifacts="data/diagnostic_preview/reports/bereishis_1_1_to_2_3_manual_review_packet.md",
            blocker_reason="diagnostic preview is not runtime activation; optional generation test failed pre-implementation",
            safe_next_use="blocked",
            recommended_next_gate="fix_diagnostic_preview_generation_idempotency_before_using_as_expansion_basis",
        )
    )
    return rows


def _batch_range_label(batch: dict[str, Any]) -> str:
    text = json.dumps(batch, ensure_ascii=False).lower()
    match = re.search(r"bereishis[_ ](\d+)_(\d+)_to_(\d+)_(\d+)", text)
    if match:
        return f"Bereishis {match.group(1)}:{match.group(2)}-{match.group(3)}:{match.group(4)}"
    match = re.search(r"bereishis (\d+):(\d+) through (\d+):(\d+)", text)
    if match:
        return f"Bereishis {match.group(1)}:{match.group(2)}-{match.group(3)}:{match.group(4)}"
    return ""


def _batch_perek_label(batch: dict[str, Any]) -> str:
    label = _batch_range_label(batch)
    match = re.search(r"Bereishis (\d+):", label)
    if not match:
        return ""
    return match.group(1)


def build_gap_map(rows: list[dict[str, str]]) -> dict[str, Any]:
    by_slice: dict[str, dict[str, Any]] = defaultdict(lambda: {
        "slice": "",
        "source_support": "unknown",
        "skill_map_status": "missing",
        "review_status": "insufficient_evidence",
        "candidate_question_readiness": "insufficient_evidence",
        "runtime_safety_status": "blocked_from_activation",
        "recommended_next_step": "gather_evidence",
        "artifact_count": 0,
    })
    for row in rows:
        slice_key = row.get("pasuk_ref") or f"Bereishis {row.get('perek') or '?'}:{row.get('pasuk_start') or '?'}-{row.get('pasuk_end') or '?'}"
        item = by_slice[slice_key]
        item["slice"] = slice_key
        item["artifact_count"] += 1
        if row["source_area"] in {"source_text", "verified_source_skill_map", "curriculum_extraction_batch"}:
            item["source_support"] = "present"
        if row["source_area"] == "verified_source_skill_map":
            item["skill_map_status"] = "present"
        if row["teacher_review_status"] and row["teacher_review_status"] != "needs_review":
            item["review_status"] = row["teacher_review_status"]
        if row["safe_next_use"] in {"protected_preview_ready", "teacher_review_ready", "reviewed_bank_candidate"}:
            item["candidate_question_readiness"] = row["safe_next_use"]
            item["recommended_next_step"] = row["recommended_next_gate"]
        if row["runtime_status"] == "runtime_active":
            item["runtime_safety_status"] = "already_runtime_active_existing_scope"
    summaries = sorted(by_slice.values(), key=lambda value: value["slice"])
    return {
        "schema_version": "1.0",
        "generated_date": "2026-04-30",
        "current_active_runtime_scope": active_runtime_scope(),
        "slice_summaries": summaries,
        "strongest_gaps": [
            "No runtime activation evidence beyond existing Bereishis 1:1-3:24 active scope.",
            "Diagnostic preview generation has a known optional idempotency test failure and should not drive expansion yet.",
            "Extraction reviewed/planning status is not teacher approval for questions.",
        ],
        "highest_leverage_next_opportunities": [
            "Bereishis Perek 4 limited protected-preview/teacher review build from existing Perek 4 review artifacts.",
            "Bereishis Perek 5-6 clean two-item limited packet continuation for sefer/ben only.",
            "Standard 3 reviewed-bank candidate alignment audit without runtime activation.",
        ],
        "standard_3_coverage_summary": {
            "standards_validator_passed_preflight": True,
            "standard_3_artifacts_present": True,
            "runtime_activation_authorized": False,
        },
    }


def build_candidate_plan() -> dict[str, Any]:
    primary = {
        "candidate_id": "cepg_primary_bereishis_perek_4_limited_protected_preview_build",
        "candidate_type": "protected_preview_candidate_packet_build",
        "perek_or_slice": "Bereishis Perek 4",
        "pasuk_range": "Bereishis 4:1-4:16 planning/review slice",
        "skills": ["basic_noun_recognition", "source_discovery", "teacher-reviewed limited packet selection"],
        "question_types": ["internal protected-preview noun recognition", "teacher review packet"],
        "source_evidence": [
            "data/curriculum_extraction/reports/batch_005_review_resolution.md",
            "data/gate_2_protected_preview_candidates/bereishis_perek_4_protected_preview_candidate_review.tsv",
            "data/gate_2_protected_preview_packets/bereishis_perek_4_internal_protected_preview_packet.tsv",
            "data/gate_2_protected_preview_packets/bereishis_perek_4_two_item_limited_internal_packet_iteration.tsv",
        ],
        "review_status": "review artifacts exist, but runtime activation remains blocked",
        "blockers": [
            "Protected preview is not reviewed bank.",
            "Teacher/internal review artifacts do not authorize runtime activation.",
            "Need a separate build branch to create the next allowed packet/report only.",
        ],
        "next_required_artifacts": [
            "Perek 4 limited protected-preview build or observation packet",
            "machine-readable contract",
            "validator and tests",
            "explicit no-runtime safety gate",
        ],
        "future_branch_name": "feature/perek-4-limited-protected-preview-build-gate",
        "risk_level": "low_to_medium",
        "recommendation_summary": "Use Perek 4 because it is the next contiguous non-runtime Bereishis slice with reviewed planning and protected-preview artifacts, while keeping runtime activation blocked.",
    }
    alternates = [
        {
            "candidate_id": "cepg_alt_perek_5_6_clean_two_item_followup",
            "candidate_type": "limited_packet_followup",
            "perek_or_slice": "Bereishis Perek 5-6",
            "pasuk_range": "clean two-item packet only",
            "skills": ["basic_noun_recognition"],
            "question_types": ["limited internal review packet"],
            "risk_level": "low",
            "recommendation_summary": "Safe but small; useful if the teacher wants a minimal packet continuation rather than a broader contiguous slice.",
        },
        {
            "candidate_id": "cepg_alt_standard_3_reviewed_bank_alignment_audit",
            "candidate_type": "standards_alignment_audit",
            "perek_or_slice": "Standard 3 cross-scope",
            "pasuk_range": "not a pasuk expansion",
            "skills": ["Zekelman Standard 3 mapped language skills"],
            "question_types": ["audit only"],
            "risk_level": "medium",
            "recommendation_summary": "Useful for standards readiness, but not the best immediate content-expansion build because it is less classroom-slice specific.",
        },
    ]
    return {
        "schema_version": "1.0",
        "generated_date": "2026-04-30",
        "primary_recommended_candidate": primary,
        "alternate_candidates": alternates,
        "staged_path": [
            "Stage 1: planning/inventory complete",
            "Stage 2: build candidate packet",
            "Stage 3: teacher review",
            "Stage 4: protected preview only",
            "Stage 5: reviewed-bank promotion only after explicit approval",
            "Stage 6: runtime activation only after explicit gate",
        ],
        "must_not_activate": True,
        "ready_for_content_build_planning": True,
        "ready_for_runtime_activation": False,
    }


def write_outputs() -> dict[str, Any]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = build_inventory_rows()
    with INVENTORY_TSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=INVENTORY_COLUMNS, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    inventory_payload = {
        "schema_version": "1.0",
        "generated_date": "2026-04-30",
        "planning_only": True,
        "row_count": len(rows),
        "columns": INVENTORY_COLUMNS,
        "classification_counts": dict(Counter(row["safe_next_use"] for row in rows)),
        "rows": rows,
        **SAFETY_FLAGS,
    }
    INVENTORY_JSON.write_text(json.dumps(inventory_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    gap = build_gap_map(rows)
    GAP_JSON.write_text(json.dumps(gap, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    GAP_MD.write_text(render_gap_markdown(gap), encoding="utf-8")

    plan = build_candidate_plan()
    PLAN_JSON.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PLAN_MD.write_text(render_plan_markdown(plan), encoding="utf-8")

    return {
        "inventory_tsv": rel(INVENTORY_TSV),
        "inventory_json": rel(INVENTORY_JSON),
        "gap_md": rel(GAP_MD),
        "gap_json": rel(GAP_JSON),
        "candidate_plan_md": rel(PLAN_MD),
        "candidate_plan_json": rel(PLAN_JSON),
        "row_count": len(rows),
        "classification_counts": inventory_payload["classification_counts"],
        "primary_recommended_candidate": plan["primary_recommended_candidate"],
    }


def render_gap_markdown(gap: dict[str, Any]) -> str:
    lines = [
        "# Content Expansion Gap Map",
        "",
        "Planning-only map. Extraction verification is not question approval. Protected preview is not reviewed-bank promotion. Runtime activation is blocked.",
        "",
        "## Active runtime scope",
        "",
        f"- Scope: `{gap['current_active_runtime_scope'].get('scope')}`",
        f"- Status: `{gap['current_active_runtime_scope'].get('status')}`",
        f"- Pesukim count: {gap['current_active_runtime_scope'].get('pesukim_count')}",
        "",
        "## Slice readiness table",
        "",
        "| Slice/range | Source support | Skill-map status | Review status | Candidate readiness | Runtime safety | Recommended next step |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in gap["slice_summaries"]:
        lines.append(
            f"| {item['slice']} | {item['source_support']} | {item['skill_map_status']} | {item['review_status']} | {item['candidate_question_readiness']} | {item['runtime_safety_status']} | {item['recommended_next_step']} |"
        )
    lines += [
        "",
        "## Strongest gaps",
        "",
        *[f"- {gap_item}" for gap_item in gap["strongest_gaps"]],
        "",
        "## Highest-leverage next opportunities",
        "",
        *[f"- {item}" for item in gap["highest_leverage_next_opportunities"]],
    ]
    return "\n".join(lines) + "\n"


def render_plan_markdown(plan: dict[str, Any]) -> str:
    primary = plan["primary_recommended_candidate"]
    lines = [
        "# Content Expansion Candidate Plan",
        "",
        "This is a planning-only candidate recommendation. It does not create questions, widen runtime scope, promote reviewed bank, or activate content.",
        "",
        "## Primary recommended candidate",
        "",
        f"- Candidate id: `{primary['candidate_id']}`",
        f"- Type: `{primary['candidate_type']}`",
        f"- Slice: {primary['perek_or_slice']}",
        f"- Pasuk range: {primary['pasuk_range']}",
        f"- Risk level: {primary['risk_level']}",
        f"- Summary: {primary['recommendation_summary']}",
        "",
        "## Why this is safest/highest leverage",
        "",
        "Perek 4 is the next contiguous non-runtime Bereishis content slice with reviewed planning and protected-preview artifacts already present. It gives the next branch a concrete classroom-useful target while keeping runtime activation blocked.",
        "",
        "## Blockers",
        "",
        *[f"- {item}" for item in primary["blockers"]],
        "",
        "## Staged path",
        "",
        *[f"- {item}" for item in plan["staged_path"]],
        "",
        "## Alternates",
        "",
    ]
    for alt in plan["alternate_candidates"]:
        lines.append(f"- `{alt['candidate_id']}`: {alt['recommendation_summary']}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    print(json.dumps(write_outputs(), ensure_ascii=False, indent=2))
