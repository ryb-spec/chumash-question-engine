from __future__ import annotations

from functools import lru_cache

from foundation_resources import load_foundation_resource


@lru_cache(maxsize=1)
def engine_extension_review_queue():
    return load_foundation_resource("engine_extension_review_queue")


@lru_cache(maxsize=1)
def engine_extension_governance_status_values():
    queue = engine_extension_review_queue()
    return tuple(queue.get("metadata", {}).get("governance_status_values", ()))


@lru_cache(maxsize=1)
def engine_extension_recommended_disposition_values():
    queue = engine_extension_review_queue()
    return tuple(queue.get("metadata", {}).get("recommended_disposition_values", ()))


@lru_cache(maxsize=1)
def engine_extension_review_records():
    queue = engine_extension_review_queue()
    return tuple(queue.get("records", ()))


@lru_cache(maxsize=1)
def engine_extension_review_record_map():
    return {
        record["canonical_skill_id"]: dict(record)
        for record in engine_extension_review_records()
        if record.get("canonical_skill_id")
    }


def engine_extension_review_record(canonical_skill_id):
    record = engine_extension_review_record_map().get(canonical_skill_id)
    return dict(record) if record is not None else None


@lru_cache(maxsize=1)
def crosswalk_engine_extension_rows():
    crosswalk = load_foundation_resource("canonical_skill_crosswalk_json")
    return tuple(
        record
        for record in crosswalk.get("skills", ())
        if record.get("system_layer") == "engine_extension"
    )


def governed_engine_extension_ids():
    return tuple(engine_extension_review_record_map().keys())


def ungoverned_engine_extension_ids():
    governed = set(governed_engine_extension_ids())
    return tuple(
        sorted(
            record["canonical_skill_id"]
            for record in crosswalk_engine_extension_rows()
            if record.get("canonical_skill_id") not in governed
        )
    )
