"""Controlled active-scope expansion helpers.

This module evaluates the next contiguous source block after the current active
runtime scope. Promotion is explicit and guarded by staged-build readiness.
"""

import json
from copy import deepcopy
from pathlib import Path

from assessment_scope import (
    CORPUS_MANIFEST_PATH,
    load_corpus_manifest,
    manifest_active_scope_metadata,
    resolve_repo_path,
)
from corpus_metrics import evaluate_staged_corpus_readiness
from torah_parser.export_bank import build_parsed_corpus_artifacts, load_source_corpus


DEFAULT_NEXT_BLOCK_SIZE = 10


def _ref_tuple(ref):
    return (ref.get("sefer"), ref.get("perek"), ref.get("pasuk"))


def _make_scope_id(sefer, start_ref, end_ref):
    return (
        f"local_parsed_{str(sefer or 'unknown').lower()}_"
        f"{start_ref.get('perek')}_{start_ref.get('pasuk')}_to_"
        f"{end_ref.get('perek')}_{end_ref.get('pasuk')}"
    )


def primary_source_path_for_active_scope(manifest=None):
    scope = manifest_active_scope_metadata() if manifest is None else next(
        (
            scope for scope in manifest.get("scopes", [])
            if scope.get("status") == "active" and scope.get("supported_runtime")
        ),
        {},
    )
    source_files = scope.get("source_files") or []
    return resolve_repo_path(source_files[0]) if source_files else None


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
    active_scope = manifest_active_scope_metadata()
    source_path = resolve_repo_path(source_path) if source_path else primary_source_path_for_active_scope()
    source_corpus = load_source_corpus(source_path)
    next_block = find_next_source_block(source_corpus, active_scope=active_scope, block_size=block_size)

    result = {
        "current_active_scope": active_scope.get("scope_id"),
        "current_active_range": active_scope.get("range"),
        "source_path": str(source_path) if source_path else None,
        "next_block": next_block,
        "promoted": False,
    }
    if next_block.get("status") != "found":
        result["status"] = next_block.get("status")
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
        status="parsed",
        source_files=[Path(source_path).as_posix()],
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
    if readiness.get("readiness_recommendation") != "active_candidate":
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

    active_scope["scope_id"] = new_scope_id
    active_scope["range"]["end"] = {
        "perek": new_end.get("perek"),
        "pasuk": new_end.get("pasuk"),
    }
    active_scope["pesukim_count"] = new_count

    for parsed_corpus in manifest.get("parsed_corpora", []):
        if parsed_corpus.get("corpus_id") == active_scope.get("parsed_corpus_id"):
            parsed_corpus["range"]["end"] = {
                "perek": new_end.get("perek"),
                "pasuk": new_end.get("pasuk"),
            }
            parsed_corpus["pesukim_count"] = new_count
            parsed_corpus["status"] = "active"

    for source_corpus in manifest.get("source_corpora", []):
        if source_corpus.get("corpus_id") == active_scope.get("source_corpus_id"):
            source_corpus["range"]["end"] = {
                "perek": new_end.get("perek"),
                "pasuk": new_end.get("pasuk"),
            }
            source_corpus["pesukim_count"] = new_count

    return manifest


def promote_next_source_block_if_ready(source_path=None, block_size=DEFAULT_NEXT_BLOCK_SIZE, manifest_path=CORPUS_MANIFEST_PATH):
    evaluation = evaluate_next_source_block(source_path=source_path, block_size=block_size)
    readiness = evaluation.get("readiness", {})
    if readiness.get("readiness_recommendation") != "active_candidate":
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
