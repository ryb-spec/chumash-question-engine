"""Candidate selection helpers."""


def _looks_like_hebrew_lemma(value):
    if not isinstance(value, str) or not value.strip():
        return False
    return any("\u0590" <= char <= "\u05ff" for char in value)


def _strip_simple_prefixes_from_lemma(candidate):
    lemma = candidate.get("lemma")
    if not _looks_like_hebrew_lemma(lemma):
        return None

    prefixes = candidate.get("prefixes") or []
    if not isinstance(prefixes, list):
        return None

    stripped = lemma
    allowed = {"ו", "ל", "ב", "ה"}
    suffixes = candidate.get("suffixes") or []

    # Conservative fallback: only peel off simple one-letter prefixes that the
    # candidate already recognized, and only when they appear in order.
    for index, prefix in enumerate(prefixes):
        form = prefix.get("form") if isinstance(prefix, dict) else None
        if form not in allowed or len(form) != 1 or not stripped.startswith(form):
            break
        if form == "ה" and len(prefixes) == 1:
            break
        if form == "ל" and suffixes:
            break
        stripped = stripped[len(form) :]

    return stripped if _looks_like_hebrew_lemma(stripped) else None


def _apply_final_letter_form(value):
    if not _looks_like_hebrew_lemma(value):
        return None

    finals = {"כ": "ך", "מ": "ם", "נ": "ן", "פ": "ף", "צ": "ץ"}
    tail = finals.get(value[-1])
    if tail is None:
        return value
    return value[:-1] + tail


def _strip_simple_suffix_from_core(candidate, core):
    if not _looks_like_hebrew_lemma(core):
        return None

    suffixes = candidate.get("suffixes") or []
    if suffixes:
        return None

    # Very narrow follow-up: after a simple prefix has already been peeled off,
    # allow a trailing ו to drop as a likely attached nominal ending. This is
    # intentionally limited and not a general suffix analyzer.
    if len(core) >= 4 and core.endswith("ו"):
        trimmed = _apply_final_letter_form(core[:-1])
        if _looks_like_hebrew_lemma(trimmed):
            return trimmed

    return None


def _with_fallback_shoresh(candidate):
    if candidate is None:
        return None

    result = dict(candidate)
    # Conservative fallback: prefer a prefix-stripped lemma when the candidate
    # already recognized simple detachable prefixes; otherwise reuse the lemma
    # itself so base-form Hebrew words do not return None.
    if result.get("shoresh") is None:
        stripped = _strip_simple_prefixes_from_lemma(result)
        if stripped:
            suffix_stripped = _strip_simple_suffix_from_core(result, stripped)
            result["shoresh"] = suffix_stripped or stripped
        elif _looks_like_hebrew_lemma(result.get("lemma")):
            result["shoresh"] = result["lemma"]
    return result


def select_best_candidate(candidates, occurrence=None):
    if not candidates:
        return None

    if occurrence is not None:
        index = occurrence.get("analysis_index")
        if isinstance(index, int) and 0 <= index < len(candidates):
            return _with_fallback_shoresh(candidates[index])

    ranked = sorted(
        candidates,
        key=lambda item: (
            item.get("confidence") not in {"reviewed_starter", "reviewed"},
            item.get("part_of_speech") == "unknown",
        ),
    )
    return _with_fallback_shoresh(ranked[0])


def preserve_alternates(selected, candidates):
    if selected is None:
        return None
    result = dict(selected)
    result["alternate_analyses"] = [
        candidate for candidate in candidates if candidate is not selected
    ]
    return result
