"""Controlled active-scope expansion helpers.

This module evaluates the next contiguous source block after the current active
runtime scope. Promotion is explicit and guarded by staged-build readiness.
Only ``active_candidate`` chunks may be promoted; ``review_needed`` chunks
remain out of the active runtime until a later explicit step.
"""

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

from assessment_scope import (
    ACTIVE_PARSED_ANALYSIS_PATH,
    ACTIVE_PARSED_PESUKIM_PATH,
    ACTIVE_SCOPE_GOLD_ANNOTATIONS_PATH,
    ACTIVE_SCOPE_OVERRIDES_PATH,
    ACTIVE_SCOPE_REVIEWED_QUESTIONS_PATH,
    ACTIVE_WORD_BANK_PATH,
    ACTIVE_WORD_OCCURRENCES_PATH,
    CORPUS_MANIFEST_PATH,
    REPO_ROOT,
    load_corpus_manifest,
    manifest_active_scope_metadata,
    normalize_corpus_status,
    resolve_repo_path,
)
from corpus_metrics import evaluate_staged_corpus_readiness, load_staged_corpus_bundle
from torah_parser.export_bank import (
    build_parsed_corpus_artifacts,
    load_source_corpus,
    load_source_corpora,
    write_json,
)


DEFAULT_NEXT_BLOCK_SIZE = 10
POST_PROMOTION_REFRESH_SCRIPTS = (
    REPO_ROOT / "scripts" / "build_reviewed_question_bank.py",
    REPO_ROOT / "scripts" / "audit_role_layer.py",
)


def _ref_tuple(ref):
    return (ref.get("sefer"), ref.get("perek"), ref.get("pasuk"))


def _make_scope_id(sefer, start_ref, end_ref):
    return (
        f"local_parsed_{str(sefer or 'unknown').lower()}_"
        f"{start_ref.get('perek')}_{start_ref.get('pasuk')}_to_"
        f"{end_ref.get('perek')}_{end_ref.get('pasuk')}"
    )


def _format_bereishis_ref(ref):
    return f"{ref.get('perek')}:{ref.get('pasuk')}"


def _format_bereishis_range(sefer, start_ref, end_ref):
    start_label = _format_bereishis_ref(start_ref)
    end_label = _format_bereishis_ref(end_ref)
    if start_label == end_label:
        return f"{sefer} {start_label}"
    return f"{sefer} {start_label}-{end_label}"


def _range_matches(candidate_range, target_range):
    candidate_range = candidate_range or {}
    target_range = target_range or {}
    candidate_start = candidate_range.get("start") or {}
    candidate_end = candidate_range.get("end") or {}
    target_start = target_range.get("start") or {}
    target_end = target_range.get("end") or {}
    return (
        candidate_start.get("perek") == target_start.get("perek")
        and candidate_start.get("pasuk") == target_start.get("pasuk")
        and candidate_end.get("perek") == target_end.get("perek")
        and candidate_end.get("pasuk") == target_end.get("pasuk")
    )


def _existing_staged_bundle_dir_for_next_block(manifest, next_block):
    target_range = (next_block or {}).get("range") or {}
    for parsed_corpus in manifest.get("parsed_corpora", []):
        if not _range_matches(parsed_corpus.get("range"), target_range):
            continue
        files = parsed_corpus.get("files") or parsed_corpus.get("parsed_files") or {}
        parsed_path = files.get("parsed_pesukim")
        if not parsed_path:
            continue
        bundle_dir = resolve_repo_path(parsed_path).parent
        reviewed_path = bundle_dir / "reviewed_questions.json"
        if bundle_dir.exists() and reviewed_path.exists():
            return bundle_dir
    return None


def _manifest_repo_path(path_like):
    path = resolve_repo_path(path_like)
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _write_scope_bound_metadata(path: Path, scope_id: str):
    if not path.exists():
        return False
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        return False
    metadata = payload.setdefault("metadata", {})
    metadata["scope_id"] = scope_id
    metadata["status"] = "active"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


def _refresh_active_sidecar_metadata(scope_id: str):
    refreshed = []
    for path in (
        ACTIVE_SCOPE_OVERRIDES_PATH,
        ACTIVE_SCOPE_GOLD_ANNOTATIONS_PATH,
        ACTIVE_SCOPE_REVIEWED_QUESTIONS_PATH,
    ):
        if _write_scope_bound_metadata(path, scope_id):
            refreshed.append(str(path))
    return refreshed


def refresh_post_promotion_artifacts():
    refreshed = []
    for script_path in POST_PROMOTION_REFRESH_SCRIPTS:
        command = [sys.executable, str(script_path)]
        completed = subprocess.run(
            command,
            cwd=str(REPO_ROOT),
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        refreshed.append(
            {
                "script": str(script_path),
                "command": command,
                "stdout": completed.stdout.strip(),
                "stderr": completed.stderr.strip(),
            }
        )
    return refreshed


def _promoted_active_scope(manifest):
    return next(
        scope
        for scope in manifest.get("scopes", [])
        if scope.get("status") == "active" and scope.get("supported_runtime")
    )


def _write_live_root_artifacts(manifest, evaluation):
    active_scope = _promoted_active_scope(manifest)
    source_paths = evaluation.get("source_paths") or active_scope.get("source_files") or []
    resolved_source_paths = [resolve_repo_path(path) for path in source_paths]
    source_corpus = (
        load_source_corpora(resolved_source_paths)
        if len(resolved_source_paths) > 1
        else load_source_corpus(resolved_source_paths[0])
    )
    artifacts = build_parsed_corpus_artifacts(
        source_corpus,
        corpus_id=active_scope.get("parsed_corpus_id"),
        status="active",
        source_files=[_manifest_repo_path(path) for path in resolved_source_paths],
    )
    write_json(ACTIVE_PARSED_PESUKIM_PATH, artifacts["pesukim"])
    write_json(ACTIVE_PARSED_ANALYSIS_PATH, artifacts["parsed_pesukim"])
    write_json(ACTIVE_WORD_BANK_PATH, artifacts["word_bank"])
    write_json(ACTIVE_WORD_OCCURRENCES_PATH, artifacts["word_occurrences"])
    return {
        "pesukim": str(ACTIVE_PARSED_PESUKIM_PATH),
        "parsed_pesukim": str(ACTIVE_PARSED_ANALYSIS_PATH),
        "word_bank": str(ACTIVE_WORD_BANK_PATH),
        "word_occurrences": str(ACTIVE_WORD_OCCURRENCES_PATH),
    }


def source_corpus_actual_summary(source_corpus):
    records = list((source_corpus or {}).get("pesukim", []))
    if not records:
        return {
            "pesukim_count": 0,
            "range": {
                "start": {"sefer": None, "perek": None, "pasuk": None},
                "end": {"sefer": None, "perek": None, "pasuk": None},
            },
        }
    first = records[0]
    last = records[-1]
    return {
        "pesukim_count": len(records),
        "range": {
            "start": {"sefer": first.get("sefer"), "perek": first.get("perek"), "pasuk": first.get("pasuk")},
            "end": {"sefer": last.get("sefer"), "perek": last.get("perek"), "pasuk": last.get("pasuk")},
        },
    }


def _promotion_blocker(code, message, *, active_scope=None, source_actual_end=None):
    active_scope = active_scope or {}
    active_range = active_scope.get("range") or {}
    return {
        "code": code,
        "message": message,
        "active_scope": active_scope.get("scope_id"),
        "active_scope_range": active_range,
        "active_scope_end": active_range.get("end") or {},
        "source_actual_end": source_actual_end or {},
    }


def _active_scope_from_manifest(manifest):
    return next(
        (
            scope for scope in manifest.get("scopes", [])
            if scope.get("status") == "active" and scope.get("supported_runtime")
        ),
        {},
    )


def source_paths_for_active_scope(manifest=None):
    manifest = manifest or load_corpus_manifest()
    scope = manifest_active_scope_metadata() if manifest is None else _active_scope_from_manifest(manifest)
    source_corpus_id = scope.get("source_corpus_id")
    source_corpus = next(
        (row for row in manifest.get("source_corpora", []) if row.get("corpus_id") == source_corpus_id),
        {},
    )
    source_files = source_corpus.get("source_files") or scope.get("source_files") or []
    return [resolve_repo_path(path) for path in source_files]


def find_next_source_block(source_corpus, active_scope=None, block_size=DEFAULT_NEXT_BLOCK_SIZE):
    active_scope = active_scope or manifest_active_scope_metadata()
    source_records = source_corpus.get("pesukim", [])
    current_end = {
        "sefer": active_scope.get("sefer"),
        "perek": (active_scope.get("range") or {}).get("end", {}).get("perek"),
        "pasuk": (active_scope.get("range") or {}).get("end", {}).get("pasuk"),
    }

    end_index = None
    for index, record in enumerate(source_records):
        if _ref_tuple(record) == _ref_tuple(current_end):
            end_index = index
            break

    if end_index is None:
        return {
            "status": "no_next_block",
            "reason": "Active scope end reference was not found in the source corpus.",
            "records": [],
            "current_end": current_end,
        }

    next_records = source_records[end_index + 1:end_index + 1 + block_size]
    if not next_records:
        return {
            "status": "no_next_block",
            "reason": "The source corpus does not contain a contiguous block after the current active scope.",
            "records": [],
            "current_end": current_end,
        }

    first = next_records[0]
    last = next_records[-1]
    return {
        "status": "found",
        "records": next_records,
        "current_end": current_end,
        "range": {
            "start": {"sefer": first.get("sefer"), "perek": first.get("perek"), "pasuk": first.get("pasuk")},
            "end": {"sefer": last.get("sefer"), "perek": last.get("perek"), "pasuk": last.get("pasuk")},
        },
        "pesukim_count": len(next_records),
    }


def evaluate_next_source_block(source_path=None, block_size=DEFAULT_NEXT_BLOCK_SIZE):
    manifest = load_corpus_manifest()
    active_scope = manifest_active_scope_metadata()
    if source_path is None:
        source_paths = source_paths_for_active_scope(manifest)
    elif isinstance(source_path, (list, tuple)):
        source_paths = [resolve_repo_path(path) for path in source_path]
    else:
        source_paths = [resolve_repo_path(source_path)]

    source_corpus = load_source_corpora(source_paths) if len(source_paths) > 1 else load_source_corpus(source_paths[0])
    source_summary = source_corpus_actual_summary(source_corpus)
    next_block = find_next_source_block(source_corpus, active_scope=active_scope, block_size=block_size)

    result = {
        "current_active_scope": active_scope.get("scope_id"),
        "current_active_range": active_scope.get("range"),
        "source_path": str(source_paths[0]) if source_paths else None,
        "source_paths": [str(path) for path in source_paths],
        "source_declared_range": source_corpus.get("metadata", {}).get("range"),
        "source_actual_range": source_summary["range"],
        "source_pesukim_count": source_summary["pesukim_count"],
        "next_block": next_block,
        "promoted": False,
    }
    if next_block.get("status") != "found":
        actual_end = (source_summary.get("range") or {}).get("end", {})
        active_end = (active_scope.get("range") or {}).get("end", {})
        result["status"] = next_block.get("status")
        if (
            next_block.get("status") == "no_next_block"
            and active_scope.get("sefer") == actual_end.get("sefer")
            and active_end.get("perek") == actual_end.get("perek")
            and active_end.get("pasuk") == actual_end.get("pasuk")
        ):
            result["reason"] = (
                "The local source corpus ends at the current active scope, so no next contiguous block is available."
            )
            result["blocking_stage"] = "source_material"
            result["blockers"] = [
                _promotion_blocker(
                    "source_corpus_exhausted_at_active_scope",
                    result["reason"],
                    active_scope=active_scope,
                    source_actual_end=actual_end,
                )
            ]
        else:
            result["reason"] = next_block.get("reason")
            result["blocking_stage"] = "source_material"
            result["blockers"] = [
                _promotion_blocker(
                    "next_source_block_unavailable",
                    result["reason"],
                    active_scope=active_scope,
                    source_actual_end=actual_end,
                )
            ]
        return result

    chunk_corpus = {
        "metadata": {
            "title": source_corpus.get("metadata", {}).get("title"),
            "range": source_corpus.get("metadata", {}).get("range"),
            "format": source_corpus.get("metadata", {}).get("format"),
        },
        "pesukim": list(next_block["records"]),
    }
    existing_bundle_dir = _existing_staged_bundle_dir_for_next_block(manifest, next_block)
    if existing_bundle_dir is not None:
        staged = load_staged_corpus_bundle(existing_bundle_dir)
        readiness = evaluate_staged_corpus_readiness(existing_bundle_dir)
        result.update(
            {
                "status": "evaluated",
                "staged_chunk": staged,
                "readiness": readiness,
                "evaluation_source": "existing_staged_bundle",
                "staged_bundle_dir": str(existing_bundle_dir),
            }
        )
        return result

    corpus_id = _make_scope_id(
        active_scope.get("sefer"),
        next_block["range"]["start"],
        next_block["range"]["end"],
    )
    staged = build_parsed_corpus_artifacts(
        chunk_corpus,
        corpus_id=corpus_id,
        status="staged",
        source_files=[Path(path).as_posix() for path in source_paths],
    )
    readiness = evaluate_staged_corpus_readiness(staged)
    result.update(
        {
            "status": "evaluated",
            "staged_chunk": staged,
            "readiness": readiness,
            "evaluation_source": "fresh_source_rebuild",
        }
    )
    return result


def apply_promotion_to_manifest(manifest, evaluation):
    readiness = evaluation.get("readiness", {})
    if normalize_corpus_status(readiness.get("readiness_recommendation")) != "active_candidate":
        raise ValueError("Cannot promote a chunk that is not an active_candidate.")

    manifest = deepcopy(manifest)
    next_block = evaluation["next_block"]
    active_scope = next(
        scope for scope in manifest.get("scopes", [])
        if scope.get("status") == "active" and scope.get("supported_runtime")
    )
    previous_scope_id = active_scope.get("scope_id")
    previous_parsed_corpus_id = active_scope.get("parsed_corpus_id")
    new_start = active_scope["range"]["start"]
    new_end = next_block["range"]["end"]
    sefer = active_scope.get("sefer") or next_block["range"]["start"].get("sefer") or "Bereishis"
    promoted_slice_label = _format_bereishis_range(sefer, next_block["range"]["start"], next_block["range"]["end"])
    promoted_scope_end_label = _format_bereishis_range(sefer, new_end, new_end)
    new_count = active_scope.get("pesukim_count", 0) + next_block.get("pesukim_count", 0)
    new_scope_id = _make_scope_id(active_scope.get("sefer"), new_start, new_end)
    new_parsed_corpus_id = f"parsed_{new_scope_id.removeprefix('local_parsed_')}_root"
    new_source_files = [
        _manifest_repo_path(path)
        for path in (evaluation.get("source_paths") or active_scope.get("source_files") or [])
    ]

    active_scope["scope_id"] = new_scope_id
    active_scope["range"]["end"] = {
        "perek": new_end.get("perek"),
        "pasuk": new_end.get("pasuk"),
    }
    active_scope["pesukim_count"] = new_count
    active_scope["parsed_corpus_id"] = new_parsed_corpus_id
    if new_source_files:
        active_scope["source_files"] = new_source_files
    active_scope["notes"] = [
        "Current supported Streamlit runtime scope.",
        f"Backward-compatible with existing data/ root runtime paths while extending through {promoted_scope_end_label}.",
    ]

    for parsed_corpus in manifest.get("parsed_corpora", []):
        if parsed_corpus.get("corpus_id") == previous_parsed_corpus_id:
            parsed_corpus["corpus_id"] = new_parsed_corpus_id
            parsed_corpus["range"]["end"] = {
                "perek": new_end.get("perek"),
                "pasuk": new_end.get("pasuk"),
            }
            parsed_corpus["pesukim_count"] = new_count
            parsed_corpus["status"] = "active"
            if new_source_files:
                parsed_corpus["source_files"] = new_source_files
            parsed_corpus["notes"] = [
                "Current blessed parsed runtime layer stored in data/ root.",
                f"Contains reviewed and parsed-only enrichment used by the active app through {promoted_scope_end_label}.",
            ]
    for source_corpus in manifest.get("source_corpora", []):
        if source_corpus.get("corpus_id") == active_scope.get("source_corpus_id"):
            source_corpus["range"]["end"] = {
                "perek": new_end.get("perek"),
                "pasuk": new_end.get("pasuk"),
            }
            source_corpus["pesukim_count"] = new_count
            if new_source_files:
                source_corpus["source_files"] = new_source_files
            source_corpus["notes"] = [
                f"Current local source corpus is prepared through {promoted_scope_end_label}.",
                f"The active parsed runtime now includes {promoted_slice_label}.",
            ]

    staged_chunk_corpus_id = None
    for future_scope in manifest.get("future_scopes", []):
        if future_scope.get("scope_id") == new_scope_id:
            staged_chunk_corpus_id = future_scope.get("staged_next_chunk_corpus_id")
            break

    for parsed_corpus in manifest.get("parsed_corpora", []):
        if parsed_corpus.get("corpus_id") == staged_chunk_corpus_id:
            parsed_corpus["status"] = "active"
            parsed_corpus["notes"] = [
                f"Promoted contiguous parsed bundle retained as staged-source provenance for {promoted_slice_label}.",
                "The active runtime now includes this slice via the root parsed runtime corpus.",
            ]

    manifest["future_scopes"] = [
        future_scope
        for future_scope in manifest.get("future_scopes", [])
        if future_scope.get("scope_id") != new_scope_id
    ]

    return manifest


def promote_next_source_block_if_ready(source_path=None, block_size=DEFAULT_NEXT_BLOCK_SIZE, manifest_path=CORPUS_MANIFEST_PATH):
    evaluation = evaluate_next_source_block(source_path=source_path, block_size=block_size)
    readiness = evaluation.get("readiness", {})
    if normalize_corpus_status(readiness.get("readiness_recommendation")) != "active_candidate":
        evaluation["manifest_updated"] = False
        evaluation["live_root_artifacts_updated"] = False
        return evaluation

    manifest = load_corpus_manifest()
    updated = apply_promotion_to_manifest(manifest, evaluation)
    manifest_file = resolve_repo_path(manifest_path)
    manifest_file.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written_artifacts = _write_live_root_artifacts(updated, evaluation)
    sidecars = _refresh_active_sidecar_metadata(_promoted_active_scope(updated).get("scope_id"))
    refreshed_artifacts = refresh_post_promotion_artifacts()
    evaluation["manifest_updated"] = True
    evaluation["promoted"] = True
    evaluation["updated_manifest"] = updated
    evaluation["live_root_artifacts_updated"] = True
    evaluation["written_root_artifacts"] = written_artifacts
    evaluation["refreshed_sidecar_metadata"] = sidecars
    evaluation["refreshed_post_promotion_artifacts"] = refreshed_artifacts
    return evaluation
