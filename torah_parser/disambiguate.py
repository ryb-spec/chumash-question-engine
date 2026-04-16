"""Candidate selection helpers."""


def select_best_candidate(candidates, occurrence=None):
    if not candidates:
        return None

    if occurrence is not None:
        index = occurrence.get("analysis_index")
        if isinstance(index, int) and 0 <= index < len(candidates):
            return candidates[index]

    ranked = sorted(
        candidates,
        key=lambda item: (
            item.get("confidence") not in {"reviewed_starter", "reviewed"},
            item.get("part_of_speech") == "unknown",
        ),
    )
    return ranked[0]


def preserve_alternates(selected, candidates):
    if selected is None:
        return None
    result = dict(selected)
    result["alternate_analyses"] = [
        candidate for candidate in candidates if candidate is not selected
    ]
    return result
