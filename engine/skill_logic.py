"""Skill applicability, progress selection, and validation helpers."""

from __future__ import annotations

import random

from torah_parser.word_bank_adapter import normalize_hebrew_key

from .candidate_selection import entry_type, find_first, runtime_tense_label
from .constants import CONTROLLED_TENSE_CHOICES, PREFIX_MEANING_CHOICES, PREFIX_MEANINGS, SUFFIX_MEANINGS
from .token_analysis import (
    WORD_BANK,
    extract_prefix,
    extract_suffix,
    is_suffix_candidate,
    is_verb,
    sync_word_bank_from_progress,
    store_word_bank_in_progress,
    structured_word_to_item,
    with_suffix_metadata,
)


def structured_word_bank_items(predicate, word_bank=None, pasuk_text=None, progress=None):
    sync_word_bank_from_progress(progress)
    recent_words = set((progress or {}).get("recent_words", [])[-5:])
    items = []

    for stored_word in WORD_BANK:
        if stored_word.get("word") in recent_words:
            continue

        item = structured_word_to_item(stored_word, word_bank)
        if item is None or not predicate(item["entry"], item["token"]):
            continue

        source_pesukim = stored_word.get("source_pesukim", [])
        item["source_pasuk"] = find_pasuk_for_word(
            stored_word["word"],
            fallback=pasuk_text,
            progress=progress,
        )
        item["source_pesukim"] = source_pesukim
        items.append(item)

    return items


def skill_applicable(word_data, skill):
    word = word_data.get("word") or word_data.get("token")
    if not word:
        return False

    prefix = extract_prefix(word, None)
    suffix = word_data.get("suffix") or extract_suffix(word)
    is_word_verb = bool(word_data.get("is_verb")) or is_verb(word)

    if skill in {"prefix", "identify_prefix_meaning", "identify_prefix_future", "preposition_meaning"}:
        return bool(prefix)
    if skill in {"suffix", "identify_suffix_meaning", "identify_pronoun_suffix", "identify_suffix_past"}:
        return bool(suffix)
    if skill in {"verb_tense", "identify_tense", "identify_verb_marker"}:
        return is_word_verb and runtime_tense_label(word_data, word) is not None
    if skill == "segment_word_parts":
        return bool(prefix or suffix)
    if skill in {"part_of_speech", "shoresh"}:
        return is_word_verb or bool(prefix or suffix)
    return True


def word_skill_score(word, skill):
    for stored_word in WORD_BANK:
        if stored_word.get("word") == word:
            stored_word.setdefault("skill_scores", {})
            return stored_word["skill_scores"].get(skill, 0)
    return 0


def update_word_skill_score(word, skill, is_correct, progress=None):
    sync_word_bank_from_progress(progress)
    amount = 10 if is_correct else -10

    for stored_word in WORD_BANK:
        if stored_word.get("word") != word:
            continue

        stored_word.setdefault("skill_scores", {})
        current_score = stored_word["skill_scores"].get(skill, 0)
        stored_word["skill_scores"][skill] = max(0, min(100, current_score + amount))
        store_word_bank_in_progress(progress)
        return stored_word["skill_scores"][skill]

    return None


def find_pasuk_for_word(word, fallback=None, progress=None):
    sync_word_bank_from_progress(progress)
    recent_pesukim = set((progress or {}).get("recent_pesukim", [])[-5:])

    for stored_word in WORD_BANK:
        if stored_word.get("word") != word:
            continue

        source_pesukim = [
            pasuk
            for pasuk in stored_word.get("source_pesukim", [])
            if pasuk
        ]
        if not source_pesukim and stored_word.get("source_pasuk"):
            source_pesukim = [stored_word["source_pasuk"]]

        fresh_sources = [pasuk for pasuk in source_pesukim if pasuk not in recent_pesukim]
        return random.choice(fresh_sources or source_pesukim or [fallback])

    return fallback


def get_suffixed_word(analyzed, word_bank=None):
    target = find_first(analyzed, lambda entry, token: is_suffix_candidate(entry, token, word_bank))
    return with_suffix_metadata(target)


def infer_tense(entry, token):
    return runtime_tense_label(entry, token)


def choice_pool(values, correct, fallback):
    choices = []
    for value in [correct] + [item for item in values if item != correct] + list(fallback):
        if value and value not in choices:
            choices.append(value)
    return choices[:4]


def prefix_meaning_choices(prefix):
    options = PREFIX_MEANING_CHOICES.get(prefix)
    if options:
        return options

    correct = PREFIX_MEANINGS.get(prefix, "and")
    choices = []
    for value in [correct, "and", "the", "in / with", "to / for", "from"]:
        if value not in choices:
            choices.append(value)
    return choices[:4]


QUESTION_VALIDATOR_REGISTRY = {}


def validation_result(valid, reason_codes=None, details=None):
    return {
        "valid": bool(valid),
        "reason_codes": list(reason_codes or []),
        "details": dict(details or {}),
    }


def invalid_result(*reason_codes, **details):
    return validation_result(False, reason_codes=reason_codes, details=details)


def register_question_validator(skills, validator):
    if isinstance(skills, str):
        skills = [skills]
    for skill_name in skills:
        QUESTION_VALIDATOR_REGISTRY[skill_name] = validator


def _known_prefix_forms(entry):
    entry = entry or {}
    prefix_forms = []

    for prefix_data in entry.get("prefixes") or []:
        if not isinstance(prefix_data, dict):
            continue
        form = prefix_data.get("form")
        if form in PREFIX_MEANINGS and form not in prefix_forms:
            prefix_forms.append(form)

    legacy_prefix = entry.get("prefix")
    if legacy_prefix in PREFIX_MEANINGS and legacy_prefix not in prefix_forms:
        prefix_forms.insert(0, legacy_prefix)

    return prefix_forms


def _known_suffix_forms(entry):
    entry = entry or {}
    suffix_forms = []

    for suffix_data in entry.get("suffixes") or []:
        if not isinstance(suffix_data, dict):
            continue
        form = suffix_data.get("form")
        if form in SUFFIX_MEANINGS and form not in suffix_forms:
            suffix_forms.append(form)

    legacy_suffix = entry.get("suffix")
    if legacy_suffix in SUFFIX_MEANINGS and legacy_suffix not in suffix_forms:
        suffix_forms.insert(0, legacy_suffix)

    return suffix_forms


def _normalized_match(left, right):
    if left is None or right is None:
        return False
    return normalize_hebrew_key(str(left)) == normalize_hebrew_key(str(right))


def _selection_mode(correct_answer, choice_entries):
    return bool(choice_entries) and correct_answer in choice_entries


def _competing_choice_tokens(choice_entries, token, predicate, *, correct_answer=None):
    competing = []
    for choice_token, choice_entry in (choice_entries or {}).items():
        if choice_token in {token, correct_answer}:
            continue
        if predicate(choice_token, choice_entry):
            competing.append(choice_token)
    return competing


def format_validation_reason(token, result):
    if not result or result.get("valid", True):
        return ""

    details = result.get("details") or {}
    code = (result.get("reason_codes") or ["invalid_question"])[0]

    if code == "no_clear_prefix":
        return f"No clearly analyzed prefix is available for {token}."
    if code == "multiple_prefixes":
        return f"{token} has multiple defensible prefixes, so the question would be ambiguous."
    if code == "prefix_answer_mismatch":
        return f"{token} does not have one clearly defensible prefix answer."
    if code == "prefix_meaning_mismatch":
        return f"{token} does not have one clearly defensible prefix meaning."
    if code == "prefix_distractor_leak":
        return f"{token} has more than one plausible correct answer in the choice list."
    if code == "no_clear_suffix":
        return f"No clearly analyzed suffix is available for {token}."
    if code == "multiple_suffixes":
        return f"{token} has multiple defensible suffixes, so the question would be ambiguous."
    if code == "suffix_answer_mismatch":
        return f"{token} does not have one clearly defensible suffix answer."
    if code == "suffix_meaning_mismatch":
        return f"{token} does not have one clearly defensible suffix meaning."
    if code == "suffix_distractor_leak":
        return f"{token} has more than one plausible correct answer in the choice list."
    if code == "compound_morphology":
        return f"{token} carries compound morphology, so a simple question would be ambiguous."
    if code == "context_dependent_suffix":
        return f"{token} depends on verb/context morphology, so it is not a safe isolated-word suffix question."
    if code == "no_clear_shoresh":
        return f"No clearly analyzed shoresh is available for {token}."
    if code == "shoresh_not_supported":
        return f"{token} is not a clearly supported shoresh question."
    if code == "shoresh_answer_mismatch":
        return f"{token} does not have one clearly defensible shoresh answer."
    if code == "shoresh_distractor_leak":
        return f"{token} has more than one plausible correct answer in the choice list."
    if code == "no_clear_tense":
        return f"No confidently classified verb tense is available for {token}."
    if code == "tense_not_supported":
        return f"{token} is not a clearly supported tense question."
    if code == "tense_answer_mismatch":
        return f"{token} does not have one clearly defensible tense answer."
    if code == "tense_distractor_leak":
        return f"{token} has more than one plausible correct answer in the choice list."

    return details.get("message", f"{token} is not a safe quiz target.")


def validate_question_candidate(
    skill,
    token,
    entry,
    correct_answer=None,
    choices=None,
    choice_entries=None,
):
    validator = QUESTION_VALIDATOR_REGISTRY.get(skill)
    if validator is None:
        return validation_result(True)
    return validator(
        token,
        entry or {},
        correct_answer=correct_answer,
        choices=choices,
        choice_entries=choice_entries,
    )


def prefix_validation_result(token, entry, correct_answer=None, choices=None, choice_entries=None):
    entry = entry or {}
    prefix_forms = _known_prefix_forms(entry)

    if not prefix_forms:
        return invalid_result("no_clear_prefix", prefix_forms=prefix_forms)

    if len(prefix_forms) > 1:
        return invalid_result("multiple_prefixes", prefix_forms=prefix_forms)

    expected_prefix = prefix_forms[0]
    expected_meaning = PREFIX_MEANINGS.get(expected_prefix, "")

    if correct_answer in PREFIX_MEANINGS and correct_answer != expected_prefix:
        return invalid_result(
            "prefix_answer_mismatch",
            expected_prefix=expected_prefix,
            supplied_answer=correct_answer,
        )

    if correct_answer in PREFIX_MEANINGS.values() and correct_answer != expected_meaning:
        return invalid_result(
            "prefix_meaning_mismatch",
            expected_meaning=expected_meaning,
            supplied_answer=correct_answer,
        )

    if choices:
        plausible_answers = set(prefix_forms + [expected_meaning])
        if choice_entries and _selection_mode(correct_answer, choice_entries):
            competing = _competing_choice_tokens(
                choice_entries,
                token,
                lambda _choice, choice_entry: (
                    expected_prefix in _known_prefix_forms(choice_entry)
                    or expected_meaning in {
                        PREFIX_MEANINGS.get(form, "")
                        for form in _known_prefix_forms(choice_entry)
                    }
                ),
                correct_answer=correct_answer,
            )
        else:
            competing = [
                choice
                for choice in choices
                if choice != correct_answer and choice in plausible_answers
            ]
        if competing:
            return invalid_result(
                "prefix_distractor_leak",
                expected_prefix=expected_prefix,
                expected_meaning=expected_meaning,
                competing_choices=competing,
            )

    return validation_result(True)


def suffix_validation_result(token, entry, correct_answer=None, choices=None, choice_entries=None):
    entry = entry or {}
    suffix_forms = _known_suffix_forms(entry)

    if not suffix_forms:
        return invalid_result("no_clear_suffix", suffix_forms=suffix_forms)

    if len(suffix_forms) > 1:
        return invalid_result("multiple_suffixes", suffix_forms=suffix_forms)

    prefix_forms = _known_prefix_forms(entry)
    if len(prefix_forms) > 1:
        return invalid_result(
            "compound_morphology",
            prefix_forms=prefix_forms,
            suffix_forms=suffix_forms,
        )

    if entry_type(entry) == "verb" or entry.get("tense"):
        return invalid_result(
            "context_dependent_suffix",
            entry_type=entry_type(entry),
            tense=entry.get("tense"),
        )

    expected_suffix = suffix_forms[0]
    canonical_meaning = SUFFIX_MEANINGS.get(expected_suffix, "")
    entry_meaning = entry.get("suffix_meaning", "")
    if entry_meaning and canonical_meaning and entry_meaning != canonical_meaning:
        return invalid_result(
            "suffix_meaning_mismatch",
            expected_meaning=canonical_meaning,
            supplied_meaning=entry_meaning,
        )

    expected_meaning = entry_meaning or canonical_meaning

    if correct_answer in SUFFIX_MEANINGS and correct_answer != expected_suffix:
        return invalid_result(
            "suffix_answer_mismatch",
            expected_suffix=expected_suffix,
            supplied_answer=correct_answer,
        )

    if correct_answer in SUFFIX_MEANINGS.values() and correct_answer != expected_meaning:
        return invalid_result(
            "suffix_meaning_mismatch",
            expected_meaning=expected_meaning,
            supplied_answer=correct_answer,
        )

    if choices:
        plausible_answers = set(suffix_forms + [expected_meaning])
        plausible_answers.update(
            form
            for form, meaning in SUFFIX_MEANINGS.items()
            if meaning == expected_meaning
        )
        if choice_entries and _selection_mode(correct_answer, choice_entries):
            competing = _competing_choice_tokens(
                choice_entries,
                token,
                lambda _choice, choice_entry: (
                    expected_suffix in _known_suffix_forms(choice_entry)
                    or expected_meaning in {
                        SUFFIX_MEANINGS.get(form, "")
                        for form in _known_suffix_forms(choice_entry)
                    }
                ),
                correct_answer=correct_answer,
            )
        else:
            competing = [
                choice
                for choice in choices
                if choice != correct_answer and choice in plausible_answers
            ]
        if competing:
            return invalid_result(
                "suffix_distractor_leak",
                expected_suffix=expected_suffix,
                expected_meaning=expected_meaning,
                competing_choices=competing,
            )

    return validation_result(True)


def shoresh_validation_result(token, entry, correct_answer=None, choices=None, choice_entries=None):
    entry = entry or {}
    expected_shoresh = entry.get("shoresh")
    if not expected_shoresh:
        return invalid_result("no_clear_shoresh")

    if entry_type(entry) != "verb" or entry.get("confidence") == "generated_alternate":
        return invalid_result(
            "shoresh_not_supported",
            entry_type=entry_type(entry),
            confidence=entry.get("confidence"),
        )

    if len(_known_prefix_forms(entry)) > 1 or _known_suffix_forms(entry):
        return invalid_result(
            "compound_morphology",
            prefix_forms=_known_prefix_forms(entry),
            suffix_forms=_known_suffix_forms(entry),
        )

    if not _selection_mode(correct_answer, choice_entries) and correct_answer is not None:
        if not _normalized_match(correct_answer, expected_shoresh):
            return invalid_result(
                "shoresh_answer_mismatch",
                expected_shoresh=expected_shoresh,
                supplied_answer=correct_answer,
            )

    if choices:
        if choice_entries and _selection_mode(correct_answer, choice_entries):
            competing = _competing_choice_tokens(
                choice_entries,
                token,
                lambda _choice, choice_entry: _normalized_match(choice_entry.get("shoresh"), expected_shoresh),
                correct_answer=correct_answer,
            )
        else:
            competing = [
                choice
                for choice in choices
                if choice != correct_answer and _normalized_match(choice, expected_shoresh)
            ]
        if competing:
            return invalid_result(
                "shoresh_distractor_leak",
                expected_shoresh=expected_shoresh,
                competing_choices=competing,
            )

    return validation_result(True)


def tense_validation_result(token, entry, correct_answer=None, choices=None, choice_entries=None):
    entry = entry or {}
    expected_tense = runtime_tense_label(entry, token)
    if not expected_tense:
        return invalid_result("no_clear_tense")

    if entry_type(entry) != "verb" or entry.get("confidence") == "generated_alternate":
        return invalid_result(
            "tense_not_supported",
            entry_type=entry_type(entry),
            confidence=entry.get("confidence"),
        )

    if len(_known_prefix_forms(entry)) > 1 or _known_suffix_forms(entry):
        return invalid_result(
            "compound_morphology",
            prefix_forms=_known_prefix_forms(entry),
            suffix_forms=_known_suffix_forms(entry),
        )

    explicit_tense = entry.get("tense")
    if explicit_tense and explicit_tense in CONTROLLED_TENSE_CHOICES and explicit_tense != expected_tense:
        return invalid_result(
            "tense_not_supported",
            expected_tense=expected_tense,
            explicit_tense=explicit_tense,
        )

    if not _selection_mode(correct_answer, choice_entries) and correct_answer is not None:
        if correct_answer != expected_tense:
            return invalid_result(
                "tense_answer_mismatch",
                expected_tense=expected_tense,
                supplied_answer=correct_answer,
            )

    if choices:
        if choice_entries and _selection_mode(correct_answer, choice_entries):
            competing = _competing_choice_tokens(
                choice_entries,
                token,
                lambda _choice, choice_entry: runtime_tense_label(choice_entry, _choice) == expected_tense,
                correct_answer=correct_answer,
            )
        else:
            competing = [
                choice
                for choice in choices
                if choice != correct_answer and choice == expected_tense
            ]
        if competing:
            return invalid_result(
                "tense_distractor_leak",
                expected_tense=expected_tense,
                competing_choices=competing,
            )

    return validation_result(True)


register_question_validator(["identify_prefix_meaning", "prefix"], prefix_validation_result)
register_question_validator(
    ["identify_suffix_meaning", "identify_pronoun_suffix", "suffix"],
    suffix_validation_result,
)
register_question_validator("shoresh", shoresh_validation_result)
register_question_validator(["verb_tense", "identify_tense"], tense_validation_result)


def prefix_question_validation(token, entry, correct_answer=None, choices=None, choice_entries=None):
    result = validate_question_candidate(
        "identify_prefix_meaning",
        token,
        entry,
        correct_answer=correct_answer,
        choices=choices,
        choice_entries=choice_entries,
    )
    return result["valid"], format_validation_reason(token, result)


def suffix_question_validation(token, entry, correct_answer=None, choices=None, choice_entries=None):
    result = validate_question_candidate(
        "identify_suffix_meaning",
        token,
        entry,
        correct_answer=correct_answer,
        choices=choices,
        choice_entries=choice_entries,
    )
    return result["valid"], format_validation_reason(token, result)


def shoresh_question_validation(token, entry, correct_answer=None, choices=None, choice_entries=None):
    result = validate_question_candidate(
        "shoresh",
        token,
        entry,
        correct_answer=correct_answer,
        choices=choices,
        choice_entries=choice_entries,
    )
    return result["valid"], format_validation_reason(token, result)


def tense_question_validation(token, entry, correct_answer=None, choices=None, choice_entries=None):
    result = validate_question_candidate(
        "verb_tense",
        token,
        entry,
        correct_answer=correct_answer,
        choices=choices,
        choice_entries=choice_entries,
    )
    return result["valid"], format_validation_reason(token, result)


def has_prefix(word):
    return extract_prefix(word) is not None


def has_suffix(word):
    return extract_suffix(word) is not None


def pick_word_for_skill(words=None, skill=None, progress=None):
    if skill is None:
        skill = words
        words = None

    progress = progress or {}
    sync_word_bank_from_progress(progress)
    allowed_words = set(words) if words is not None else None
    recent_words = set(progress.get("recent_words", [])[-5:])

    candidates = [
        stored_word
        for stored_word in WORD_BANK
        if skill_applicable(stored_word, skill)
        and (allowed_words is None or stored_word.get("word") in allowed_words)
        and stored_word.get("word") not in recent_words
    ]

    if not candidates:
        candidates = [
            stored_word
            for stored_word in WORD_BANK
            if skill_applicable(stored_word, skill)
            and (allowed_words is None or stored_word.get("word") in allowed_words)
        ]

    if not candidates and words is not None:
        candidates = [
            {"word": word, "skill_scores": {}}
            for word in words
            if word not in recent_words
        ] or [{"word": word, "skill_scores": {}} for word in words]

    if not candidates:
        raise ValueError(f"No words available for skill: {skill}")

    recent_prefixes = progress.get("recent_prefixes", [])[-5:]
    if skill in {"prefix", "identify_prefix_meaning", "identify_prefix_future", "preposition_meaning"}:
        varied_prefixes = [
            candidate
            for candidate in candidates
            if not extract_prefix(candidate["word"])
            or extract_prefix(candidate["word"]) not in recent_prefixes
        ]
        if recent_prefixes.count("ו") >= 2:
            candidates = [
                candidate
                for candidate in varied_prefixes or candidates
                if extract_prefix(candidate["word"]) != "ו"
            ] or varied_prefixes or candidates
        else:
            non_vav = [
                candidate
                for candidate in varied_prefixes or candidates
                if not candidate["word"].startswith("ו")
            ]
            candidates = non_vav or varied_prefixes or candidates

    recent_suffixes = progress.get("recent_suffixes", [])[-5:]
    if skill in {"suffix", "identify_suffix_meaning", "identify_pronoun_suffix", "identify_suffix_past"}:
        non_vav_suffixes = [
            candidate
            for candidate in candidates
            if not candidate["word"].endswith("ו")
        ]
        varied_suffixes = [
            candidate
            for candidate in candidates
            if not has_suffix(candidate["word"])
            or extract_suffix(candidate["word"]) not in recent_suffixes
        ]
        if recent_suffixes.count("ו") >= 2:
            candidates = [
                candidate
                for candidate in varied_suffixes or candidates
                if not candidate["word"].endswith("ו")
            ] or non_vav_suffixes or varied_suffixes or candidates
        else:
            candidates = non_vav_suffixes or varied_suffixes or candidates

    candidates.sort(
        key=lambda word_data: (
            word_data.setdefault("skill_scores", {}).get(skill, 0),
            progress.get("recent_words", []).count(word_data["word"]),
            word_data["word"],
        )
    )
    return candidates[0]["word"]


def remember_selected_word(progress, word, entry=None):
    progress.setdefault("recent_words", []).append(word)
    progress["recent_words"] = progress["recent_words"][-10:]

    prefix = extract_prefix(word) or ""
    if prefix:
        progress.setdefault("recent_prefixes", []).append(prefix)
        progress["recent_prefixes"] = progress["recent_prefixes"][-10:]

    suffix = (entry or {}).get("suffix") or (extract_suffix(word) if entry is None else "") or ""
    if suffix:
        progress.setdefault("recent_suffixes", []).append(suffix)
        progress["recent_suffixes"] = progress["recent_suffixes"][-10:]
