"""Candidate selection, translation, and question-payload helpers."""

from __future__ import annotations

import hashlib
import random

from torah_parser.candidate_generator import generate_candidate_analyses as parser_generate_candidate_analyses
from torah_parser.word_bank_adapter import NORMALIZED_ALIAS_KEY, normalize_hebrew_key, old_word_type

from .constants import CONTROLLED_TENSE_CHOICES, PREFIX_MEANINGS, SUFFIX_MEANINGS, TRANSLATION_LITERAL, TRANSLATION_NATURAL
from .token_analysis import extract_prefix, extract_suffix, is_prefix_candidate


def stable_rng(key):
    return random.Random(key)


def unique(items):
    result = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result


def build_choices(correct, partials, clear, key, extra=None):
    choices = unique([correct] + list(partials or []) + [clear] + list(extra or []))
    if len(choices) < 4:
        raise ValueError(f"Need 4 unique choices. Got: {choices}")
    choices = choices[:4]
    stable_rng(key).shuffle(choices)
    return choices


def contains_hebrew(text):
    return any("\u0590" <= char <= "\u05ff" for char in str(text or ""))


def is_placeholder_translation(value, token=None):
    if not value:
        return True
    text = str(value).strip()
    if not text:
        return True
    if text.startswith("[") and text.endswith("]"):
        return True
    if "direct object marker" in text.lower():
        return True
    if token and normalize_hebrew_key(text) == normalize_hebrew_key(token):
        return True
    return contains_hebrew(text)


def usable_translation(entry, token=None):
    for key in ("translation_context", "context_translation", "translation", "translation_literal"):
        value = entry.get(key)
        if not is_placeholder_translation(value, token):
            return value
    return None


def instructional_value(entry, question_type=None):
    if not isinstance(entry, dict):
        return "low"
    token = entry.get("word") or entry.get("surface")
    if question_type in {"word_meaning", "translation", "subject_identification"}:
        if usable_translation(entry, token) is None:
            return "low"
        if entry.get("entity_type") == "grammatical_particle":
            return "low"
        if entry.get("part_of_speech") == "particle" or entry.get("type") == "particle":
            return "low"
    if question_type in {"verb_tense", "shoresh"}:
        if entry.get("type") != "verb" or entry.get("confidence") == "generated_alternate":
            return "low"
        if question_type == "shoresh" and not entry.get("shoresh"):
            return "low"
        if question_type == "verb_tense" and not entry.get("tense"):
            return "low"
    if entry.get("confidence") in {"reviewed_starter", "reviewed"}:
        return "high"
    if entry.get("semantic_group") not in {None, "unknown"}:
        return "medium"
    return "low"


def quiz_eligible(entry, token, question_type):
    return instructional_value(entry, question_type) in {"high", "medium"}


def entry_type(entry):
    if (entry or {}).get("type"):
        return entry.get("type")
    return old_word_type((entry or {}).get("part_of_speech"))


def semantic_group(entry):
    return (entry or {}).get("semantic_group") or "unknown"


def role_hint(entry):
    return (entry or {}).get("role_hint") or "unknown"


def entity_type(entry):
    return (entry or {}).get("entity_type") or "unknown"


def is_subject_candidate_entry(entry):
    return (
        role_hint(entry) == "subject_candidate"
        and semantic_group(entry) in {"person", "divine", "animal"}
    )


def is_person_like_entry(entry):
    return semantic_group(entry) in {"person", "divine", "animal"}


def is_object_candidate_entry(entry, token, word_bank=None):
    if entity_type(entry) == "grammatical_particle":
        return False
    if role_hint(entry) == "object_candidate":
        return True
    return (
        entry_type(entry) == "noun"
        and semantic_group(entry) in {"object", "cosmic_entity", "place"}
        and not is_prefix_candidate(entry, token, word_bank)
    )


def confident_verb_tense(entry, token):
    entry = entry or {}
    explicit = entry.get("tense")
    if explicit:
        return explicit

    current_type = entry_type(entry)
    if current_type and current_type not in {"verb", "unknown"}:
        return None

    for analysis in parser_generate_candidate_analyses(token):
        if analysis.get("part_of_speech") != "verb":
            continue
        if analysis.get("confidence") == "generated_alternate":
            continue
        tense = analysis.get("tense")
        if tense:
            return tense
    return None


def runtime_tense_label(entry, token):
    explicit = (entry or {}).get("tense")
    if explicit in CONTROLLED_TENSE_CHOICES:
        return explicit
    return confident_verb_tense(entry, token)


def skip_question_payload(skill, pasuk, reason, *, source="generated skill question", details=None):
    payload = {
        "status": "skipped",
        "skipped": True,
        "supported": False,
        "skill": skill,
        "question_type": skill,
        "pasuk": pasuk,
        "reason": reason,
        "source": source,
    }
    if details:
        payload["details"] = details
    return payload


def is_skip_payload(payload):
    return isinstance(payload, dict) and payload.get("status") == "skipped"


def strip_surface_family_prefixes(value):
    text = normalize_hebrew_key(value or "")
    if len(text) > 3 and text.startswith("ו"):
        text = text[1:]
    if len(text) > 3 and text.startswith(("ה", "ל")):
        text = text[1:]
    return text


def distractor_key(entry):
    if not isinstance(entry, dict):
        return None

    explicit = (
        entry.get("distractor_key")
        or entry.get("display_lemma")
        or entry.get("surface_family")
    )
    if explicit:
        return normalize_hebrew_key(explicit)

    word = entry.get("word") or entry.get("surface") or entry.get("menukad")
    normalized_word = normalize_hebrew_key(word)
    lemma = entry.get("lemma") or entry.get("shoresh") or entry.get("Shoresh")
    key = normalize_hebrew_key(lemma) if lemma else normalized_word

    if key and key == normalized_word:
        key = strip_surface_family_prefixes(key)
    return key or normalized_word


def filtered_translation_values(entries, correct, correct_entry=None, question_type="translation"):
    values = []
    seen_values = {correct}
    seen_keys = set()
    correct_key = distractor_key(correct_entry)
    if correct_key:
        seen_keys.add(correct_key)

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        if not quiz_eligible(entry, entry.get("word"), question_type):
            continue
        value = usable_translation(entry, entry.get("word"))
        if not value or value in seen_values:
            continue
        key = distractor_key(entry)
        if key and key in seen_keys:
            continue
        values.append(value)
        seen_values.add(value)
        if key:
            seen_keys.add(key)
    return values


def word_bank_entries(word_bank, source_derived_only=False):
    seen = set()
    for entry in (word_bank or {}).values():
        if not isinstance(entry, dict) or entry.get(NORMALIZED_ALIAS_KEY):
            continue
        if source_derived_only and not entry.get("source_refs"):
            continue
        marker = id(entry)
        if marker in seen:
            continue
        seen.add(marker)
        yield entry


def valid_shorashim(word_bank):
    return unique(
        entry.get("shoresh")
        for entry in word_bank_entries(word_bank, source_derived_only=True)
        if entry.get("type") == "verb" and entry.get("shoresh")
    )


def translation_distractors(correct, target_entry, by_group, word_bank=None):
    same_semantic_group = [
        entry
        for entry in word_bank_entries(word_bank, source_derived_only=True)
        if entry.get("semantic_group") == target_entry.get("semantic_group")
    ]
    same_entity_type = [
        entry
        for entry in word_bank_entries(word_bank, source_derived_only=True)
        if entry.get("entity_type") == target_entry.get("entity_type")
    ]
    same_group = [entry for entry in by_group.get(target_entry.get("group"), [])]
    same_type = [
        entry
        for entry in word_bank_entries(word_bank, source_derived_only=True)
        if entry.get("type") == target_entry.get("type")
    ]
    all_translations = [entry for entry in word_bank_entries(word_bank, source_derived_only=True)]
    return filtered_translation_values(
        same_semantic_group + same_entity_type + same_group + same_type + all_translations,
        correct,
        target_entry,
        question_type="word_meaning",
    )


def quiz_ready(entry, token, question_type, word_bank=None):
    if question_type == "translation":
        return quiz_eligible(entry, token, "word_meaning")
    if question_type == "shoresh":
        return quiz_eligible(entry, token, "shoresh")
    if question_type == "verb_tense":
        return quiz_eligible(entry, token, "verb_tense")
    if question_type == "prefix_suffix":
        prefix = extract_prefix(token, word_bank) or entry.get("prefix")
        suffix = entry.get("suffix")
        return bool(
            (prefix and PREFIX_MEANINGS.get(prefix))
            or (suffix and (entry.get("suffix_meaning") or SUFFIX_MEANINGS.get(suffix)))
        )
    if question_type == "subject_identification":
        return is_subject_candidate_entry(entry) and quiz_eligible(entry, token, "subject_identification")
    return True


def find_first(analyzed, predicate):
    for item in analyzed:
        if predicate(item["entry"], item["token"]):
            return item
    return None


def find_after(analyzed, start_index, predicate):
    for item in analyzed[start_index + 1:]:
        if predicate(item["entry"], item["token"]):
            return item
    return None


def first_ready(analyzed, question_type, word_bank=None):
    return find_first(
        analyzed,
        lambda entry, token: quiz_ready(entry, token, question_type, word_bank),
    )


def describe(item, mode=TRANSLATION_LITERAL):
    return item["entry"]["translation"]


def translated_item_text(item):
    if not item:
        return None
    return usable_translation(item["entry"], item.get("token"))


def phrase_items_are_translatable(items):
    return bool(items) and all(translated_item_text(item) for item in items)


def filtered_phrase_candidates(candidates, token=None):
    return unique(
        candidate
        for candidate in candidates
        if candidate and not is_placeholder_translation(candidate, token)
    )


def naturalize_subject_action(action_text, subject_text):
    replacements = [
        ("and he ", "and "),
        ("and it ", "and "),
        ("and ", ""),
        ("he ", ""),
        ("it ", ""),
    ]
    for prefix, replacement in replacements:
        if action_text.startswith(prefix):
            return f"{replacement}{subject_text} {action_text[len(prefix):]}"
    return f"{subject_text} {action_text}"


def format_translation(items, mode=TRANSLATION_LITERAL):
    if mode == TRANSLATION_LITERAL:
        return " ".join(describe(item) for item in items)

    if len(items) >= 2:
        first = items[0]
        if entry_type(first["entry"]) == "verb" and is_subject_candidate_entry(items[1]["entry"]):
            subject_items = []
            index = 1
            while index < len(items) and is_subject_candidate_entry(items[index]["entry"]):
                subject_items.append(items[index])
                index += 1
            subject_text = " ".join(describe(item) for item in subject_items)
            translated = naturalize_subject_action(describe(first), subject_text)
            rest = [describe(item) for item in items[index:]]
            return " ".join([translated] + rest)

    return " ".join(describe(item) for item in items)


def varied_phrase_window(
    analyzed,
    target_token=None,
    recent_phrases=None,
    key="phrase",
    require_translatable=False,
):
    recent_phrases = list(recent_phrases or [])
    recent_block = set(recent_phrases[-5:])
    options = []
    max_length = min(4, len(analyzed))

    for length in range(2, max_length + 1):
        for start in range(0, len(analyzed) - length + 1):
            phrase_items = analyzed[start:start + length]
            phrase = " ".join(item["token"] for item in phrase_items)
            if phrase_items[-1]["entry"].get("type") == "prep":
                continue
            if require_translatable and not phrase_items_are_translatable(phrase_items):
                continue
            if target_token and target_token not in [item["token"] for item in phrase_items]:
                continue
            options.append((phrase, phrase_items))

    unused = [option for option in options if option[0] not in recent_block]
    pool = unused
    attempts = 0
    while not pool and attempts < 10:
        attempts += 1
        pool = [option for option in options if option[0] not in recent_block]

    if not pool:
        pool = options

    if not pool:
        if require_translatable:
            return None, []
        return " ".join(item["token"] for item in analyzed[:2]), analyzed[:2]

    return stable_rng(f"{key}|{len(recent_phrases)}").choice(pool)


def clean_action(text):
    for lead in ["and he ", "and it "]:
        if text.startswith(lead):
            return text[len(lead):]
    return text


def strip_relation(text):
    for lead in ["from ", "to ", "in ", "on ", "with "]:
        if text.startswith(lead):
            return text[len(lead):]
    return text


def root_meaning(entry):
    text = entry.get("translation", "")
    for lead in [
        "from his ",
        "to his ",
        "from her ",
        "to her ",
        "from the ",
        "to the ",
        "from ",
        "to ",
        "with ",
        "in ",
        "and ",
        "the ",
    ]:
        if text.startswith(lead):
            return text[len(lead):]
    return text


def group_distractors(entry, by_group, limit=3):
    group = entry.get("group")
    if not group:
        return []
    distractors = [
        root_meaning(candidate)
        for candidate in by_group.get(group, [])
        if candidate is not entry and root_meaning(candidate) != root_meaning(entry)
    ]
    return unique(distractors)[:limit]


def different_group_distractor(entry, by_group):
    for group, candidates in by_group.items():
        if group == entry.get("group"):
            continue
        for candidate in candidates:
            value = root_meaning(candidate)
            if value and value != root_meaning(entry):
                return value
    return "something else"


def question_id_for(question):
    base = "|".join(
        [
            str(question.get("skill", "")),
            str(question.get("question_type", "")),
            str(question.get("word", "")),
            str(question.get("question", "")),
            str(question.get("correct_answer", "")),
        ]
    )
    return hashlib.sha1(base.encode("utf-8")).hexdigest()[:12]


def validate_question_payload(question):
    choices = list(question.get("choices", []))
    if len(choices) != 4:
        raise ValueError(f"Question must have exactly 4 choices: {question.get('question')}")
    if len(set(choices)) != 4:
        raise ValueError(f"Question choices must be unique: {question.get('question')}")
    if question.get("correct_answer") not in choices:
        raise ValueError(f"Correct answer is missing from choices: {question.get('question')}")
    random.shuffle(choices)
    question["choices"] = choices
    question.setdefault("id", question_id_for(question))
    return question


def make_question(
    step,
    skill,
    standard,
    micro_standard,
    question_type,
    word,
    text,
    choices,
    correct_answer,
    explanation,
    difficulty,
):
    return validate_question_payload({
        "step": step,
        "skill": skill,
        "mode": "pasuk" if question_type in {"phrase_meaning", "subject_identification"} else "word",
        "standard": standard,
        "micro_standard": micro_standard,
        "question_type": question_type,
        "translation_mode": (
            TRANSLATION_NATURAL
            if question_type in {"phrase_meaning", "subject_identification"}
            else TRANSLATION_LITERAL
        ),
        "word": word,
        "selected_word": word,
        "question": text,
        "choices": choices,
        "correct_answer": correct_answer,
        "explanation": explanation,
        "difficulty": difficulty,
        "source": "generated pasuk flow",
    })


def get_verb(analyzed):
    return find_first(analyzed, lambda entry, _token: entry_type(entry) == "verb")


def get_prefixed_word(analyzed):
    return find_first(analyzed, lambda entry, token: is_prefix_candidate(entry, token))


def get_translatable_word(analyzed):
    return find_first(analyzed, lambda entry, token: usable_translation(entry, token) is not None)


def get_part_of_speech_word(analyzed):
    return find_first(analyzed, lambda entry, _token: entry_type(entry) in {"verb", "noun"})


def get_subject(analyzed):
    verb = get_verb(analyzed)
    if verb is None:
        return None
    verb_index = analyzed.index(verb)
    return (
        find_after(
            analyzed,
            verb_index,
            lambda entry, _token: is_subject_candidate_entry(entry),
        )
        or find_first(
            analyzed,
            lambda entry, _token: is_subject_candidate_entry(entry),
        )
    )


def get_source(analyzed):
    return find_first(analyzed, lambda entry, token: extract_prefix(token) == "מ")


def get_recipient(analyzed):
    return find_first(analyzed, lambda entry, token: extract_prefix(token) == "ל")


def get_destination(analyzed):
    marker = find_first(
        analyzed,
        lambda entry, token: token == "אל" or extract_prefix(token) == "ל",
    )
    if marker is None:
        return None, None

    marker_index = analyzed.index(marker)
    obj = find_after(
        analyzed,
        marker_index,
        lambda entry, _token: semantic_group(entry) in {"place", "person", "divine", "animal"},
    )
    return marker, obj


def get_direct_object(analyzed):
    return find_first(
        analyzed,
        lambda entry, token: is_object_candidate_entry(entry, token)
        and not is_prefix_candidate(entry, token),
    )
