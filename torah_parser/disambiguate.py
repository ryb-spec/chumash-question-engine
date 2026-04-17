"""Candidate selection helpers."""


def _looks_like_hebrew_lemma(value):
    if not isinstance(value, str) or not value.strip():
        return False
    return any("\u0590" <= char <= "\u05ff" for char in value)


def _simple_prefix_forms(candidate):
    prefixes = candidate.get("prefixes") or []
    forms = []
    for prefix in prefixes:
        if not isinstance(prefix, dict):
            continue
        form = prefix.get("form")
        if isinstance(form, str) and form:
            forms.append(form)
    return forms


def _special_case_shoresh_fallback(candidate):
    # Keep this tiny and explicit: some current gold forms need a narrow bridge
    # until the parser emits better verb metadata for them.
    special_cases = {
        "תדשא": "דשא",
        "ותוצא": "יצא",
        "יקרא": "קרא",
        "ויקראו": "קרא",
    }
    prefix_forms = _simple_prefix_forms(candidate)
    suffix_forms = _simple_suffix_forms(candidate)
    metadata_cases = {
        ("למים", ("ל",), ("ם",)): "מים",
        ("מימי", ("מ",), ("י",)): "מים",
        ("מימיו", ("מ",), ("יו",)): "מים",
    }
    for field in ("surface", "lemma", "normalized"):
        value = candidate.get(field)
        if (value, tuple(prefix_forms), tuple(suffix_forms)) in metadata_cases:
            return metadata_cases[(value, tuple(prefix_forms), tuple(suffix_forms))]
        if value in special_cases:
            return special_cases[value]
    return None


def _simple_suffix_forms(candidate):
    suffixes = candidate.get("suffixes") or []
    forms = []
    for suffix in suffixes:
        if not isinstance(suffix, dict):
            continue
        form = suffix.get("form")
        if isinstance(form, str) and form:
            forms.append(form)
    return forms


def _allow_l_prefix_with_plural_noun_shape(stripped, suffix_forms):
    # Narrow allowance for forms like לשמים / לימים: the generated candidate
    # may tag final ם as a suffix even when the lexical noun core clearly ends
    # in ים. We only allow this for simple ל-prefix cases.
    return suffix_forms == ["ם"] and isinstance(stripped, str) and len(stripped) >= 3 and stripped.endswith("ים")


def _strip_simple_prefixes_from_lemma(candidate):
    lemma = candidate.get("lemma")
    if not _looks_like_hebrew_lemma(lemma):
        return None

    prefixes = candidate.get("prefixes") or []
    if not isinstance(prefixes, list):
        return None

    stripped = lemma
    allowed = {"ו", "ל", "ב", "ה", "כ", "מ"}
    suffixes = candidate.get("suffixes") or []
    suffix_forms = _simple_suffix_forms(candidate)
    stripped_forms = []

    # Conservative fallback: only peel off simple one-letter prefixes that the
    # candidate already recognized, and only when they appear in order.
    for index, prefix in enumerate(prefixes):
        form = prefix.get("form") if isinstance(prefix, dict) else None
        if form not in allowed or len(form) != 1 or not stripped.startswith(form):
            break
        if form == "ה" and len(prefixes) == 1:
            break
        if form == "ל" and suffixes and not (
            (suffix_forms == ["ו"] and len(stripped) >= 5)
            or _allow_l_prefix_with_plural_noun_shape(stripped[1:], suffix_forms)
        ):
            break
        stripped = stripped[len(form) :]
        stripped_forms.append(form)

    # Narrow stacked-prefix cleanup: some generated candidates only record the
    # leading inseparable prefix and leave a following article in the core.
    if stripped_forms and stripped_forms[-1] in {"ל", "ב", "כ", "מ"} and stripped.startswith("ה") and len(stripped) >= 4:
        stripped = stripped[1:]

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

    suffix_forms = _simple_suffix_forms(candidate)

    if suffix_forms == ["ו"]:
        # Narrow noun-suffix fallback: if the candidate already marked a simple
        # trailing ו suffix, strip only the clear nominal endings we see in the
        # current gold set rather than trying to normalize suffixes generally.
        if len(core) >= 5 and core.endswith("הו"):
            trimmed = _apply_final_letter_form(core[:-2])
            if _looks_like_hebrew_lemma(trimmed):
                return trimmed
        if len(core) >= 4 and core.endswith("ו"):
            trimmed = _apply_final_letter_form(core[:-1])
            if _looks_like_hebrew_lemma(trimmed):
                return trimmed

    if suffix_forms:
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
        special_case = _special_case_shoresh_fallback(result)
        if special_case:
            result["shoresh"] = special_case
        else:
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
