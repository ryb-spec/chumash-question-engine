"""Controlled active-scope expansion helpers.

This module evaluates the next contiguous source block after the current active
runtime scope. Promotion is explicit and guarded by staged-build readiness.
Only ``active_candidate`` chunks may be promoted; ``review_needed`` chunks
remain out of the active runtime until a later explicit step.
"""

import json
from copy import deepcopy
from pathlib import Path

from assessment_scope import (
    CORPUS_MANIFEST_PATH,
    load_corpus_manifest,
    manifest_active_scope_metadata,
    normalize_corpus_status,
    resolve_repo_path,
)
from corpus_metrics import evaluate_staged_corpus_readiness
from torah_parser.export_bank import (
    build_parsed_corpus_artifacts,
    load_source_corpus,
    load_source_corpora,
)


DEFAULT_NEXT_BLOCK_SIZE = 10


def _ref_tuple(ref):
    return (ref.get("sefer"), ref.get("perek"), ref.get("pasuk"))


def _make_scope_id(sefer, start_ref, end_ref):
    return (
        f"local_parsed_{str(sefer or 'unknown').lower()}_"
        f"{start_ref.get('perek')}_{start_ref.get('pasuk')}_to_"
        f"{end_ref.get('perek')}_{end_ref.get('pasuk')}"
    )


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
        else:
            result["reason"] = next_block.get("reason")
        return result

    chunk_corpus = {
        "metadata": {
            "title": source_corpus.get("metadata", {}).get("title"),
            "range": source_corpus.get("metadata", {}).get("range"),
            "format": source_corpus.get("metadata", {}).get("format"),
        },
        "pesukim": list(next_block["records"]),
    }
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
    new_start = active_scope["range"]["start"]
    new_end = next_block["range"]["end"]
    new_count = active_scope.get("pesukim_count", 0) + next_block.get("pesukim_count", 0)
    new_scope_id = _make_scope_id(active_scope.get("sefer"), new_start, new_end)
    new_source_files = list(evaluation.get("source_paths") or active_scope.get("source_files") or [])

    active_scope["scope_id"] = new_scope_id
    active_scope["range"]["end"] = {
        "perek": new_end.get("perek"),
        "pasuk": new_end.get("pasuk"),
    }
    active_scope["pesukim_count"] = new_count
    if new_source_files:
        active_scope["source_files"] = new_source_files

    for parsed_corpus in manifest.get("parsed_corpora", []):
        if parsed_corpus.get("corpus_id") == active_scope.get("parsed_corpus_id"):
            parsed_corpus["range"]["end"] = {
                "perek": new_end.get("perek"),
                "pasuk": new_end.get("pasuk"),
            }
            parsed_corpus["pesukim_count"] = new_count
            parsed_corpus["status"] = "active"
            if new_source_files:
                parsed_corpus["source_files"] = new_source_files

    for source_corpus in manifest.get("source_corpora", []):
        if source_corpus.get("corpus_id") == active_scope.get("source_corpus_id"):
            source_corpus["range"]["end"] = {
                "perek": new_end.get("perek"),
                "pasuk": new_end.get("pasuk"),
            }
            source_corpus["pesukim_count"] = new_count
            if new_source_files:
                source_corpus["source_files"] = new_source_files

    return manifest


def promote_next_source_block_if_ready(source_path=None, block_size=DEFAULT_NEXT_BLOCK_SIZE, manifest_path=CORPUS_MANIFEST_PATH):
    evaluation = evaluate_next_source_block(source_path=source_path, block_size=block_size)
    readiness = evaluation.get("readiness", {})
    if normalize_corpus_status(readiness.get("readiness_recommendation")) != "active_candidate":
        evaluation["manifest_updated"] = False
        return evaluation

    manifest = load_corpus_manifest()
    updated = apply_promotion_to_manifest(manifest, evaluation)
    manifest_file = resolve_repo_path(manifest_path)
    manifest_file.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    evaluation["manifest_updated"] = True
    evaluation["promoted"] = True
    evaluation["updated_manifest"] = updated
    return evaluation
