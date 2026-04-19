from __future__ import annotations

from functools import lru_cache

from foundation_resources import load_foundation_resource


@lru_cache(maxsize=1)
def load_assessment_blueprint():
    return load_foundation_resource("assessment_blueprint")


def benchmark_section_weights():
    return tuple(
        dict(item)
        for item in load_assessment_blueprint()["external_benchmark"]["jsat_section_weights"]
    )


def benchmark_section_weight_map():
    return {
        item["section"]: item["weight_percent"]
        for item in benchmark_section_weights()
    }


def benchmark_relevant_focus_sections():
    return tuple(
        load_assessment_blueprint()["external_benchmark"]["relevant_jsat_focus_for_this_system"]
    )


def benchmark_skill_family_coverage():
    return tuple(
        dict(item)
        for item in load_assessment_blueprint()["recommended_local_blueprint"]["mvp_focus"]
    )


def benchmark_question_archetypes():
    return tuple(
        dict(item)
        for item in load_assessment_blueprint()["recommended_local_blueprint"]["question_archetypes"]
    )


@lru_cache(maxsize=1)
def benchmark_question_archetype_map():
    return {
        item["archetype_id"]: dict(item)
        for item in benchmark_question_archetypes()
    }


def get_benchmark_question_archetype(archetype_id):
    return dict(benchmark_question_archetype_map()[archetype_id])


@lru_cache(maxsize=1)
def benchmark_canonical_skill_bucket_map():
    mapping = {}
    for bucket in benchmark_skill_family_coverage():
        bucket_label = bucket["bucket"]
        for canonical_skill_id in bucket.get("canonical_skills", []):
            mapping.setdefault(canonical_skill_id, []).append(bucket_label)
    return {
        canonical_skill_id: tuple(bucket_labels)
        for canonical_skill_id, bucket_labels in mapping.items()
    }

