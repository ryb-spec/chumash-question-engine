"""Validate Content Expansion Planning Gate V1 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PLANNING_MD = ROOT / "data/pipeline_rounds/content_expansion_planning_gate_2026_04_30.md"
PLANNING_JSON = ROOT / "data/pipeline_rounds/content_expansion_planning_gate_2026_04_30.json"
INVENTORY_TSV = ROOT / "data/content_expansion_planning/content_expansion_inventory_2026_04_30.tsv"
INVENTORY_JSON = ROOT / "data/content_expansion_planning/content_expansion_inventory_2026_04_30.json"
GAP_MD = ROOT / "data/content_expansion_planning/content_expansion_gap_map_2026_04_30.md"
GAP_JSON = ROOT / "data/content_expansion_planning/content_expansion_gap_map_2026_04_30.json"
PLAN_MD = ROOT / "data/content_expansion_planning/content_expansion_candidate_plan_2026_04_30.md"
PLAN_JSON = ROOT / "data/content_expansion_planning/content_expansion_candidate_plan_2026_04_30.json"
NEXT_PROMPT = ROOT / "data/pipeline_rounds/next_codex_prompt_content_build_candidate_2026_04_30.md"
DOC = ROOT / "docs/content_expansion_planning_gate_v1.md"
DOCS_README = ROOT / "docs/README.md"
PIPELINE_README = ROOT / "data/pipeline_rounds/README.md"

SAFETY_FALSE_KEYS = [
    "content_expansion_performed",
    "runtime_scope_widened",
    "perek_activated",
    "reviewed_bank_promoted",
    "runtime_content_promoted",
    "question_generation_changed",
    "question_selection_changed",
    "question_selection_weighting_changed",
    "scoring_mastery_changed",
    "source_truth_changed",
    "fake_teacher_approval_created",
    "fake_student_data_created",
    "raw_logs_exposed",
    "validators_weakened",
    "ready_for_runtime_activation",
    "runtime_activation_authorized",
]

REQUIRED_COLUMNS = [
    "source_area",
    "source_file",
    "perek",
    "pasuk_start",
    "pasuk_end",
    "skill",
    "question_type",
    "source_status",
    "extraction_status",
    "teacher_review_status",
    "protected_preview_status",
    "reviewed_bank_status",
    "runtime_status",
    "blocker_reason",
    "safe_next_use",
    "recommended_next_gate",
]

FORBIDDEN_CLAIMS = [
    "activated runtime scope",
    "perek activated",
    "promoted to reviewed bank",
    "approved for runtime",
    "teacher approved",
    "mastery proven",
    "fake student data created: yes",
    "raw JSONL",
    "scope widened",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def validate() -> list[str]:
    errors: list[str] = []
    required = [
        PLANNING_MD,
        PLANNING_JSON,
        INVENTORY_TSV,
        INVENTORY_JSON,
        GAP_MD,
        GAP_JSON,
        PLAN_MD,
        PLAN_JSON,
        NEXT_PROMPT,
        DOC,
        DOCS_README,
        PIPELINE_README,
    ]
    for path in required:
        if not path.exists():
            errors.append(f"missing required artifact: {path.relative_to(ROOT)}")
    if errors:
        return errors

    try:
        planning = _json(PLANNING_JSON)
        inventory = _json(INVENTORY_JSON)
        gap = _json(GAP_JSON)
        plan = _json(PLAN_JSON)
    except Exception as exc:  # pragma: no cover
        return [f"JSON parse failed: {exc}"]

    if planning.get("planning_only") is not True:
        errors.append("planning JSON must say planning_only true")
    for key in SAFETY_FALSE_KEYS:
        if planning.get(key) is not False:
            errors.append(f"planning JSON {key} must be false")
    for key in [
        "active_runtime_scope_detected",
        "primary_recommended_candidate",
        "blocked_items_summary",
        "review_needed_summary",
    ]:
        if not planning.get(key):
            errors.append(f"planning JSON missing {key}")
    if planning.get("ready_for_content_build_planning") is not True:
        errors.append("planning JSON must be ready for content build planning")

    primary = planning.get("primary_recommended_candidate") or {}
    if primary.get("candidate_id") != "cepg_primary_bereishis_perek_4_limited_protected_preview_build":
        errors.append("primary candidate must be the Perek 4 protected-preview build")
    if primary.get("future_branch_name") != "feature/perek-4-limited-protected-preview-build-gate":
        errors.append("future branch recommendation mismatch")

    with INVENTORY_TSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if not rows:
        errors.append("inventory TSV must contain rows")
    for column in REQUIRED_COLUMNS:
        if column not in (rows[0].keys() if rows else []):
            errors.append(f"inventory TSV missing column {column}")
    if inventory.get("planning_only") is not True or inventory.get("content_expansion_performed") is not False:
        errors.append("inventory JSON must be planning-only and non-expansion")
    classifications = set(inventory.get("classification_counts") or {})
    if "blocked" not in classifications or "pending_teacher_review" not in classifications:
        errors.append("inventory must include fail-closed blocked and pending review classifications")

    if not gap.get("slice_summaries"):
        errors.append("gap map JSON must include slice summaries")
    if not plan.get("primary_recommended_candidate"):
        errors.append("candidate plan must include primary recommendation")
    if not plan.get("alternate_candidates"):
        errors.append("candidate plan must include alternates")

    report_text = _read(PLANNING_MD)
    if "## Safety confirmation" not in report_text:
        errors.append("planning report must include safety confirmation section")

    docs_text = _read(DOC) + _read(DOCS_README) + _read(PIPELINE_README)
    for fragment in [
        "planning-only",
        "Extraction verification is not approval",
        "Protected preview is not reviewed bank",
        "Runtime activation is blocked",
        "data/content_expansion_planning/",
    ]:
        if fragment not in docs_text:
            errors.append(f"docs/index missing fragment: {fragment}")

    combined = "\n".join(
        _read(path)
        for path in [PLANNING_MD, GAP_MD, PLAN_MD, NEXT_PROMPT, DOC]
    ) + json.dumps({"planning": planning, "inventory": inventory, "gap": gap, "plan": plan}, ensure_ascii=False)
    for phrase in FORBIDDEN_CLAIMS:
        if phrase in combined:
            errors.append(f"forbidden claim found: {phrase}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Content expansion planning gate validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
