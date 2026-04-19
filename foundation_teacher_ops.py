from __future__ import annotations

from functools import lru_cache

from foundation_resources import load_foundation_resource


@lru_cache(maxsize=1)
def load_teacher_ops_workflow():
    return load_foundation_resource("teacher_ops_workflow")


def teacher_readiness_criteria():
    return tuple(load_teacher_ops_workflow().get("readiness_criteria", []))


def teacher_deployment_cycle():
    return tuple(load_teacher_ops_workflow().get("deployment_cycle", []))


def teacher_system_outputs():
    outputs = load_teacher_ops_workflow().get("system_outputs_to_support_teachers", {})
    return dict(outputs)
