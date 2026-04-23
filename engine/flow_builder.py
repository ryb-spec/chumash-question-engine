"""Shared question-generation engine.

This module powers the supported Streamlit runtime from the active parsed
dataset. It still contains a few preview/export helpers for local developer
work, but those helpers are not the supported student-facing runtime.
"""

import json
import random
import hashlib
import re
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

from foundation_dikduk import dikduk_foundation_metadata
from engine.morphology_labels import (
    canonical_tense_code as canonical_morphology_tense_code,
    classify_tense_form,
    student_tense_label as morphology_student_tense_label,
)
from assessment_scope import (
    ACTIVE_ASSESSMENT_SCOPE,
    ACTIVE_WORD_BANK_PATH,
    LEGACY_PASUK_FLOW_PREVIEW_PATH,
    active_parsed_pasuk_record_for_text,
    active_pasuk_ref_payload,
    gold_skill_record_for_text,
    active_scope_override_for_text,
    active_scope_reviewed_questions_for_text,
    active_pasuk_record_for_text,
    active_pasuk_texts,
    data_path,
    repo_path,
    resolve_repo_path,
)
from skill_catalog import (
    resolve_skill_id,
    skill_difficulty_tier,
    skill_ids_in_runtime_order,
    skill_micro_standard,
    skill_standard,
)
from torah_parser.candidate_generator import (
    apply_prefix_metadata as parser_apply_prefix_metadata,
    apply_suffix_metadata as parser_apply_suffix_metadata,
    detect_verb_tense as parser_detect_verb_tense,
    extract_prefix as parser_extract_prefix,
    extract_suffix as parser_extract_suffix,
    generate_candidate_analyses as parser_generate_candidate_analyses,
    prefix_has_known_base as parser_prefix_has_known_base,
    suffix_has_known_base as parser_suffix_has_known_base,
)
from torah_parser.disambiguate import annotate_role_layer
from torah_parser.tokenize import tokenize_pasuk as parser_tokenize_pasuk
from torah_parser.word_bank_adapter import (
    NORMALIZED_ALIAS_KEY,
    adapt_word_analysis,
    adapt_word_bank_data,
    build_word_bank_lookup,
    normalize_hebrew_key,
    old_word_type,
    resolve_surface_for_normalized,
    resolve_word_bank_lookup,
)

WORD_BANK_PATH = ACTIVE_WORD_BANK_PATH
OUTPUT_PATH = LEGACY_PASUK_FLOW_PREVIEW_PATH
LETTER_MEANING_QUESTIONS_PATH = data_path("skills", "letter_meaning", "questions_walder.json")
WORD_STRUCTURE_QUESTIONS_PATH = data_path("skills", "word_structure", "questions.json")

EXAMPLE_PESUKIM = [
    "וילך האיש מביתו אל העיר",
    "ויתן האב לחם לבנו",
]

EXAMPLE_MULTI_PESUKIM = [
    "וילך האיש מביתו אל העיר",
    "ויתן האב לחם לבנו",
    "וישב האיש בביתו",
]

_ALL_PESUKIM = list(dict.fromkeys(EXAMPLE_PESUKIM + EXAMPLE_MULTI_PESUKIM + [
    "בְּרֵאשִׁית בָּרָא אֱלֹקִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ",
    "וְהָאָרֶץ הָיְתָה תֹהוּ וָבֹהוּ וְחֹשֶׁךְ עַל פְּנֵי תְהוֹם",
    "וַיֹּאמֶר אֱלֹקִים יְהִי אוֹר וַיְהִי אוֹר",
    "וַיַּרְא אֱלֹקִים אֶת הָאוֹר כִּי טוֹב",
    "וַיִּקְרָא אֱלֹקִים לָאוֹר יוֹם וְלַחֹשֶׁךְ קָרָא לָיְלָה",
    "וַיֹּאמֶר ה׳ אֶל אַבְרָם לֶךְ לְךָ מֵאַרְצְךָ",
    "וְאֶעֶשְׂךָ לְגוֹי גָּדוֹל וַאֲבָרֶכְךָ",
    "וַיֵּלֶךְ אַבְרָם כַּאֲשֶׁר דִּבֶּר אֵלָיו ה׳",
    "וַיֹּאמֶר אַבְרָם אֶל לוֹט אַל נָא תְהִי מְרִיבָה בֵּינִי וּבֵינֶךָ",
    "וַיֹּאמֶר יַעֲקֹב אֶל בָּנָיו לָמָּה תִּתְרָאוּ",
    "וַיֹּאמֶר יוֹסֵף אֶל אֶחָיו אֲנִי יוֹסֵף",
    "וַיֹּאמֶר פַּרְעֹה אֶל יוֹסֵף רְאֵה נָתַתִּי אֹתְךָ",
    "וַיֹּאמֶר ה׳ אֶל מֹשֶׁה לֶךְ אֶל פַּרְעֹה",
    "וַיֹּאמֶר מֹשֶׁה אֶל ה׳ מִי אָנֹכִי כִּי אֵלֵךְ",
    "וַיֹּאמֶר אֱלֹקִים אֶהְיֶה אֲשֶׁר אֶהְיֶה",
    "אָנֹכִי ה׳ אֱלֹקֶיךָ אֲשֶׁר הוֹצֵאתִיךָ מֵאֶרֶץ מִצְרַיִם",
    "לֹא תִרְצָח לֹא תִנְאָף לֹא תִגְנֹב",
    "כַּבֵּד אֶת אָבִיךָ וְאֶת אִמֶּךָ",
    "וְאָהַבְתָּ אֵת ה׳ אֱלֹקֶיךָ בְּכָל לְבָבְךָ",
    "וְהָיוּ הַדְּבָרִים הָאֵלֶּה עַל לְבָבֶךָ",
    "וְשִׁנַּנְתָּם לְבָנֶיךָ וְדִבַּרְתָּ בָּם",
    "ה׳ רֹעִי לֹא אֶחְסָר",
    "בִּנְאוֹת דֶּשֶׁא יַרְבִּיצֵנִי עַל מֵי מְנֻחוֹת יְנַהֲלֵנִי",
    "גַּם כִּי אֵלֵךְ בְּגֵיא צַלְמָוֶת לֹא אִירָא רָע",
    "שִׁירוּ לַה׳ שִׁיר חָדָשׁ שִׁירוּ לַה׳ כָּל הָאָרֶץ",
    "הוֹדוּ לַה׳ כִּי טוֹב כִּי לְעוֹלָם חַסְדּוֹ",
    "אֶשָּׂא עֵינַי אֶל הֶהָרִים מֵאַיִן יָבֹא עֶזְרִי",
    "עֶזְרִי מֵעִם ה׳ עֹשֵׂה שָׁמַיִם וָאָרֶץ",
    "אֲנִי לְדוֹדִי וְדוֹדִי לִי",
    "קוֹל דּוֹדִי דּוֹפֵק פִּתְחִי לִי אֲחֹתִי",
]))

CHUMASH_PESUKIM = list(active_pasuk_texts())
OTHER_PESUKIM = _ALL_PESUKIM[24:]
PESUKIM = CHUMASH_PESUKIM

WORD_BANK = []

TRANSLATION_LITERAL = "literal"
TRANSLATION_NATURAL = "natural"

PREFIX_MEANINGS = {
    "\u05d5": "and",
    "\u05d1": "in / with",
    "\u05dc": "to / for",
    "\u05db": "like / as",
    "\u05de": "from",
    "\u05d4": "the",
    "\u05e9": "that / which",
}
PREFIX_FORM_BANK = ["\u05d5", "\u05d1", "\u05dc", "\u05de", "\u05db", "\u05d4", "\u05e9"]
PREFIX_MEANING_BANK = [
    "and",
    "in / with",
    "to / for",
    "from",
    "like / as",
    "the",
    "that / which",
]

KNOWN_PREFIXES = PREFIX_MEANINGS
CONTROLLED_TENSE_CHOICES = [
    "vav_consecutive_past",
    "future_jussive",
    "future",
    "past",
    "present",
    "infinitive",
    "command",
]
STUDENT_TENSE_LABELS = {
    "vav_consecutive_past": "past",
    "future_jussive": "future",
    "future": "future",
    "past": "past",
    "present": "present",
    "infinitive": "to do form",
}
COHORT_TAUGHT_TENSE_LABELS = (
    "past",
    "future",
    "present",
    "to do form",
)
COHORT_TAUGHT_TENSE_CANONICAL_CODES = {
    "past": "past",
    "future": "future",
    "present": "present",
    "to do form": "infinitive",
}
STUDENT_PART_OF_SPEECH_LABELS = {
    "noun": "naming word",
    "verb": "action word",
    "particle": "small helper word",
    "prep": "direction word",
}
COHORT_PART_OF_SPEECH_CHOICES = (
    "naming word",
    "action word",
    "small helper word",
    "direction word",
)
TENSE_CODE_BY_LABEL = {
    label: code
    for code, label in STUDENT_TENSE_LABELS.items()
}
DIVINE_NAME_VARIANTS = (
    "the LORD God",
    "the LORD",
    "G-d",
    "God",
)
DIVINE_NAME_PATTERN = re.compile(
    "|".join(re.escape(variant) for variant in sorted(DIVINE_NAME_VARIANTS, key=len, reverse=True))
)
EXPLICIT_SUBJECT_PREFIXES = (
    "he ",
    "she ",
    "it ",
    "they ",
    "there ",
    "god ",
    "the lord ",
    "the lord god ",
    "someone else ",
    "the man ",
    "the woman ",
)

SKILLS = skill_ids_in_runtime_order()

SKILL_GROUP_ORDER = [
    "letter_meaning",
    "word_structure",
    "word_meaning",
    "sentence_structure",
    "pasuk_flow",
]

SKILL_METADATA = {
    skill_id: {
        "standard": skill_standard(skill_id),
        "micro_standard": skill_micro_standard(skill_id),
        "difficulty": skill_difficulty_tier(skill_id),
    }
    for skill_id in SKILLS
}

SUFFIX_MEANINGS = {
    "\u05d9": "my",
    "\u05da\u05b8": "your (m)",
    "\u05da\u05b0": "your (f)",
    "\u05da": "your",
    "\u05d5": "his",
    "\u05d4": "her",
    "\u05e0\u05d5": "our",
    "\u05db\u05b6\u05dd": "your (m plural)",
    "\u05db\u05b6\u05df": "your (f plural)",
    "\u05db\u05dd": "your (m plural)",
    "\u05db\u05df": "your (f plural)",
    "\u05dd": "their",
    "\u05df": "their",
    "\u05d9\u05d5": "his",
}
SUFFIX_FORM_BANK = list(SUFFIX_MEANINGS.keys())

@lru_cache(maxsize=1)
def load_word_bank():
    data = json.loads(Path(WORD_BANK_PATH).read_text(encoding="utf-8")) if Path(WORD_BANK_PATH).exists() else {"words": []}
    entries = adapt_word_bank_data(
        data,
        defaults={
            "group": "unknown",
            "semantic_group": "unknown",
            "role_hint": "unknown",
            "entity_type": "unknown",
        },
    )

    by_word = build_word_bank_lookup(entries)
    by_group = {}
    seen_entries = set()
    for entry in by_word.values():
        if entry.get(NORMALIZED_ALIAS_KEY):
            continue
        marker = id(entry)
        if marker in seen_entries:
            continue
        seen_entries.add(marker)
        by_group.setdefault(entry.get("group", "unknown"), []).append(entry)

    return by_word, by_group


def load_json(path):
    return json.loads(resolve_repo_path(path).read_text(encoding="utf-8"))


def load_letter_meaning_questions():
    return load_json(LETTER_MEANING_QUESTIONS_PATH)


def load_word_structure_questions():
    return load_json(WORD_STRUCTURE_QUESTIONS_PATH)


def format_static_skill_question(question):
    skill = resolve_skill_id(question["skill"]) or question["skill"]
    metadata = SKILL_METADATA[skill]
    choices = question["choices"]
    if len(choices) != 4:
        raise ValueError(f"Static skill question must have 4 choices: {question['id']}")
    if len(set(choices)) != 4:
        raise ValueError(f"Static skill question has duplicate choices: {question['id']}")
    if question["correct"] not in choices:
        raise ValueError(f"Correct answer missing from choices: {question['id']}")

    payload = {
        "id": question["id"],
        "question_text": question["question"],
        "question": question["question"],
        "choices": choices,
        "correct_answer": question["correct"],
        "skill_group": question["skill_group"],
        "skill": skill,
        "question_type": skill,
        "mode": "word",
        "standard": metadata["standard"],
        "micro_standard": metadata["micro_standard"],
        "difficulty": question.get("difficulty", metadata["difficulty"]),
        "word": question["word"],
        "selected_word": question["word"],
        "explanation": f"{question['correct']} is the correct letter.",
        "source": question.get("source", "walder_packet"),
    }
    return validate_question_payload(payload)


def generate_static_skill_question(
    questions,
    skill=None,
    difficulty=None,
    asked_question_ids=None,
):
    asked = set(asked_question_ids or [])
    candidates = [
        question
        for question in questions
        if (skill is None or question["skill"] == skill)
        and (difficulty is None or question.get("difficulty") == difficulty)
    ]
    if not candidates:
        candidates = [
            question
            for question in questions
            if skill is None or question["skill"] == skill
        ]
    if not candidates:
        raise ValueError(f"No static questions found for skill: {skill}")

    unused = [question for question in candidates if question["id"] not in asked]
    selected = random.choice(unused or candidates)
    return format_static_skill_question(selected)


def generate_letter_meaning_question(skill=None, difficulty=None, asked_question_ids=None):
    return generate_static_skill_question(
        load_letter_meaning_questions(),
        skill=skill,
        difficulty=difficulty,
        asked_question_ids=asked_question_ids,
    )


def generate_word_structure_question(skill=None, difficulty=None, asked_question_ids=None):
    return generate_static_skill_question(
        load_word_structure_questions(),
        skill=skill,
        difficulty=difficulty,
        asked_question_ids=asked_question_ids,
    )


def generate_diagnostic_questions():
    required_skills = [
        "identify_prefix_meaning",
        "identify_suffix_meaning",
        "identify_verb_marker",
    ]
    return [
        generate_letter_meaning_question(skill=skill)
        for skill in required_skills
    ]


def tokenize_pasuk(pasuk):
    return parser_tokenize_pasuk(pasuk)


def analyze_word(word):
    analyses = parser_generate_candidate_analyses(word)
    primary = analyses[0] if analyses else {}
    return {
        "word": word,
        "prefix": parser_extract_prefix(word),
        "suffix": parser_extract_suffix(word),
        "is_verb": primary.get("part_of_speech") == "verb",
        "tense": primary.get("tense"),
        "analyses": analyses,
    }


def sync_word_bank_from_progress(progress):
    if not progress:
        return

    existing_by_word = {item["word"]: item for item in WORD_BANK}
    for stored_word in progress.get("word_bank", []):
        word = stored_word.get("word")
        if not word:
            continue

        if word in existing_by_word:
            existing = existing_by_word[word]
            existing.setdefault("skill_scores", {})
            existing["skill_scores"].update(stored_word.get("skill_scores", {}))
        else:
            stored = dict(stored_word)
            stored.setdefault("skill_scores", {})
            WORD_BANK.append(stored)
            existing_by_word[word] = stored


def store_word_bank_in_progress(progress):
    if progress is not None:
        progress["word_bank"] = WORD_BANK


def add_words_from_pasuk(pasuk, progress=None):
    sync_word_bank_from_progress(progress)

    if is_structured_pasuk(pasuk):
        pasuk_text = structured_pasuk_text(pasuk)
        analyzed_words = [
            {
                "word": item.get("word") or item.get("token"),
                "prefix": extract_prefix(item.get("word") or item.get("token")),
                "suffix": item.get("suffix") or extract_suffix(item.get("word") or item.get("token")),
                "is_verb": item.get("is_verb", is_verb(item.get("word") or item.get("token"))),
            }
            for item in pasuk
            if item.get("word") or item.get("token")
        ]
    else:
        pasuk_text = pasuk
        analyzed_words = [analyze_word(word) for word in tokenize_pasuk(pasuk)]

    existing_by_word = {item["word"]: item for item in WORD_BANK}
    for analyzed in analyzed_words:
        word = analyzed["word"]
        if word in existing_by_word:
            existing = existing_by_word[word]
            existing["prefix"] = analyzed.get("prefix") or ""
            existing["prefix_meaning"] = PREFIX_MEANINGS.get(existing["prefix"], "")
            existing["suffix"] = existing.get("suffix") or analyzed.get("suffix")
            existing["is_verb"] = bool(existing.get("is_verb") or analyzed.get("is_verb"))
            existing.setdefault("skill_scores", {})
            existing.setdefault("source_pesukim", [])
            if pasuk_text not in existing["source_pesukim"]:
                existing["source_pesukim"].append(pasuk_text)
            existing.setdefault("source_pasuk", existing["source_pesukim"][0])
            continue

        stored = dict(analyzed)
        stored["source_pasuk"] = pasuk_text
        stored["source_pesukim"] = [pasuk_text]
        stored["skill_scores"] = {}
        WORD_BANK.append(stored)
        existing_by_word[word] = stored

    store_word_bank_in_progress(progress)
    return WORD_BANK


def extract_prefix(word, word_bank=None):
    return parser_extract_prefix(word, word_bank)


def prefix_has_known_base(word, prefix, word_bank):
    return parser_prefix_has_known_base(word, prefix, word_bank)


def apply_prefix_metadata(word, entry, word_bank=None):
    return parser_apply_prefix_metadata(word, entry, word_bank)


def is_prefix_candidate(entry, token, word_bank=None):
    prefix = extract_prefix(token, word_bank)
    if not prefix:
        return False
    if entry.get("prefix") and entry.get("prefix") != prefix:
        return False
    if entry_type(entry) != "verb" and word_bank is not None and not prefix_has_known_base(token, prefix, word_bank):
        return False
    return True


def detect_prefix(token, word_bank):
    if len(token) < 2:
        return None

    prefix = extract_prefix(token, word_bank)
    if prefix is None:
        return None

    normalized_token = normalize_hebrew_key(token)
    base_normalized = normalized_token[len(prefix):]
    base_word = resolve_surface_for_normalized(word_bank, base_normalized)
    if not base_word:
        return None

    source_entry = word_bank[base_word] if base_word in word_bank else word_bank.get(base_normalized)
    entry = resolve_word_bank_lookup(base_word, source_entry)
    entry["word"] = token
    entry["prefix"] = prefix
    entry["base_word"] = base_word
    entry["prefix_meaning"] = PREFIX_MEANINGS[prefix]
    entry["translation"] = f"{PREFIX_MEANINGS[prefix]} {entry['translation']}"
    apply_prefix_metadata(entry["word"], entry, word_bank)
    apply_suffix_metadata(entry["word"], entry, word_bank)
    return {"token": token, "entry": entry, "base": base_word}


def extract_suffix(word):
    return parser_extract_suffix(word)


def suffix_has_known_base(word, suffix, word_bank):
    return parser_suffix_has_known_base(word, suffix, word_bank)


def apply_suffix_metadata(word, entry, word_bank=None):
    return parser_apply_suffix_metadata(word, entry, word_bank)


def with_suffix_metadata(item, word_bank=None):
    if item is None:
        return None

    entry = dict(item["entry"])
    apply_suffix_metadata(item["token"], entry, word_bank)
    updated = dict(item)
    updated["entry"] = entry
    return updated


def is_suffix_candidate(entry, token, word_bank=None):
    if entity_type(entry) in {"pronoun", "grammatical_particle"}:
        return False
    if entry_type(entry) in {"pronoun", "particle"}:
        return False
    suffix = entry.get("suffix") or extract_suffix(token)
    if not suffix:
        return False
    if has_lexical_plural_ending(entry, token, suffix):
        return False
    if entry.get("type") == "suffix_form":
        return True
    if word_bank is None:
        return False
    return suffix_has_known_base(token, suffix, word_bank)


def normalize_token(token, word_bank):
    lookup_token = token
    if lookup_token not in word_bank:
        normalized_token = normalize_hebrew_key(token)
        if normalized_token in word_bank:
            lookup_token = normalized_token

    if lookup_token in word_bank:
        entry = resolve_word_bank_lookup(token, word_bank[lookup_token])
        if entry.get("prefix"):
            entry.setdefault("base_word", token)
        else:
            prefix = extract_prefix(token, word_bank)
            if prefix and prefix_has_known_base(token, prefix, word_bank):
                possible_base = resolve_surface_for_normalized(
                    word_bank,
                    normalize_hebrew_key(token)[len(prefix):],
                )
                entry.setdefault(
                    "base_word",
                    possible_base or token,
                )
                apply_prefix_metadata(token, entry, word_bank)
            else:
                entry["prefix"] = ""
                entry["prefix_meaning"] = ""
                entry.setdefault("base_word", token)
        apply_suffix_metadata(token, entry, word_bank)
        return {"token": token, "entry": entry, "base": token}

    detected = detect_prefix(token, word_bank)
    if detected is not None:
        return detected

    return None
def basic_analyzed_item(word, word_bank=None):
    analyses = parser_generate_candidate_analyses(word)
    primary = dict(analyses[0] if analyses else {})
    primary.setdefault("translation_literal", word)
    primary.setdefault("translation_context", word)
    entry = adapt_word_analysis(
        word,
        primary,
        defaults={
            "group": "unknown",
            "semantic_group": "unknown",
            "role_hint": "unknown",
            "entity_type": "unknown",
            "base_word": word,
        },
    )
    apply_prefix_metadata(word, entry, word_bank)
    apply_suffix_metadata(word, entry, word_bank)
    return {"token": word, "entry": entry, "base": word}


def structured_word_to_item(word_data, word_bank=None):
    word = word_data.get("word") or word_data.get("token")
    if not word:
        return None

    if word_bank:
        item = normalize_token(word, word_bank)
        if item is not None:
            return item

    item = basic_analyzed_item(word, word_bank)
    entry = item["entry"]
    detected_prefix = extract_prefix(word, word_bank)
    if word_data.get("prefix") and word_data["prefix"] == detected_prefix:
        entry["prefix"] = detected_prefix
        entry["prefix_meaning"] = PREFIX_MEANINGS.get(detected_prefix, "")
    if word_data.get("suffix"):
        entry["suffix"] = word_data["suffix"]
        entry["suffix_meaning"] = SUFFIX_MEANINGS.get(word_data["suffix"], "")
    if word_data.get("is_verb"):
        entry["type"] = "verb"
    return item


def is_structured_pasuk(value):
    return isinstance(value, (list, tuple)) and all(
        isinstance(item, dict) and ("word" in item or "token" in item)
        for item in value
    )


def structured_pasuk_text(analyzed_words):
    return " ".join((item.get("word") or item.get("token") or "") for item in analyzed_words)


def normalize_analyzed_pasuk(analyzed_words, word_bank=None):
    items = [
        structured_word_to_item(word_data, word_bank)
        for word_data in analyzed_words
    ]
    annotated, _ = annotate_role_layer([item for item in items if item is not None])
    return annotated


def prebuilt_analyzed_pasuk(analyzed_words):
    items = []
    for item in analyzed_words or []:
        if not isinstance(item, dict):
            continue
        if "entry" in item and "token" in item:
            items.append(item)
            continue
        normalized = normalize_analyzed_pasuk([item], word_bank=None)
        items.extend(normalized)
    annotated, _ = annotate_role_layer(items)
    return annotated


def parsed_token_record_to_item(token_record):
    analysis = dict(token_record.get("selected_analysis") or {})
    token = token_record.get("surface", "")
    analysis.setdefault("normalized", token_record.get("normalized") or analysis.get("normalized"))
    analysis.setdefault("translation_literal", analysis.get("translation") or token)
    analysis.setdefault(
        "translation_context",
        analysis.get("context_translation") or analysis.get("translation") or token,
    )
    entry = adapt_word_analysis(
        token,
        analysis,
        defaults={
            "group": "unknown",
            "semantic_group": "unknown",
            "role_hint": "unknown",
            "entity_type": "unknown",
            "base_word": analysis.get("lemma") or token,
        },
    )
    item = {
        "token": token,
        "entry": entry,
        "base": analysis.get("lemma") or token,
    }
    if token_record.get("role_data"):
        item["role_data"] = dict(token_record.get("role_data") or {})
    return item


def active_scope_parsed_analysis(pasuk):
    parsed_record = active_parsed_pasuk_record_for_text(pasuk)
    if not parsed_record:
        return None
    token_records = parsed_record.get("token_records") or []
    if not token_records:
        return None
    items = [parsed_token_record_to_item(token_record) for token_record in token_records]
    if any(item.get("role_data") for item in items):
        return items
    annotated, _ = annotate_role_layer(items)
    return annotated


def active_scope_skill_override(pasuk_text, skill):
    override = active_scope_override_for_text(pasuk_text)
    if not override:
        return None
    skills = override.get("skills") or {}
    return skills.get(skill)


def reviewed_question_skill_aliases(question):
    return {
        str(question.get("skill") or "").strip(),
        *[str(value).strip() for value in question.get("alias_skills") or [] if str(value).strip()],
    }


def reviewed_question_matches_request(question, skill, *, prefix_level=None):
    requested_skill = str(skill or "").strip()
    supported_skills = reviewed_question_skill_aliases(question)
    if (
        requested_skill == "translation"
        and str(question.get("review_family") or "").strip() == "translation"
        and str(question.get("skill") or "").strip() == "phrase_translation"
    ):
        supported_skills.add("translation")
    if requested_skill not in supported_skills:
        return False
    if requested_skill == "identify_prefix_meaning" and question.get("prefix_level") is not None:
        return int(question.get("prefix_level")) == int(prefix_level or 1)
    return True


def clone_reviewed_question(question, requested_skill):
    cloned = deepcopy(question)
    review_family = str(cloned.get("review_family") or "").strip()
    original_skill = str(cloned.get("skill") or "").strip()
    cloned.pop("reviewed_id", None)
    cloned.pop("review_family", None)
    cloned.pop("alias_skills", None)
    requested_skill = str(requested_skill or "").strip()
    if requested_skill and requested_skill != cloned.get("skill"):
        if (
            requested_skill == "translation"
            and review_family == "translation"
            and original_skill == "phrase_translation"
        ):
            cloned["skill"] = requested_skill
        if {
            requested_skill,
            original_skill,
        }.issubset({"identify_tense", "verb_tense"}):
            cloned["skill"] = requested_skill
            cloned["question_type"] = requested_skill
    cloned["source"] = "active scope reviewed bank"
    cloned["analysis_source"] = "active_scope_reviewed_bank"
    return cloned


REVIEWED_TRANSLATION_SELECTION_WINDOW = 20


def _reviewed_translation_answer_key(text):
    return " ".join(str(text or "").split()).strip().lower()


def _reviewed_translation_recent_penalty(question, recent_questions=None):
    token_key = normalize_hebrew_key(question.get("selected_word") or question.get("word") or "")
    answer_key = _reviewed_translation_answer_key(question.get("correct_answer"))
    penalty = 0
    recent_items = list(recent_questions or [])[-REVIEWED_TRANSLATION_SELECTION_WINDOW:]
    for distance, previous in enumerate(reversed(recent_items), start=1):
        if not isinstance(previous, dict):
            continue
        previous_skill = str(previous.get("repeat_family") or previous.get("skill") or "").strip()
        if previous_skill != "translation":
            continue
        previous_target = normalize_hebrew_key(
            previous.get("target_word") or previous.get("selected_word") or previous.get("word") or ""
        )
        previous_answer = _reviewed_translation_answer_key(previous.get("correct_answer"))
        if token_key and previous_target == token_key:
            penalty += max(0, 100 - distance)
            continue
        if answer_key and previous_answer == answer_key:
            penalty += max(0, 20 - distance)
    return penalty


def _best_reviewed_translation_match(matches, recent_questions=None):
    standalone_matches = [
        question
        for question in matches
        if str(question.get("question_type") or question.get("skill") or "").strip() == "translation"
    ]
    if not standalone_matches:
        return matches[0]

    best_question = standalone_matches[0]
    best_penalty = _reviewed_translation_recent_penalty(best_question, recent_questions)
    for question in standalone_matches[1:]:
        penalty = _reviewed_translation_recent_penalty(question, recent_questions)
        if penalty < best_penalty:
            best_question = question
            best_penalty = penalty
    return best_question


def reviewed_question_for_pasuk_skill(pasuk_text, skill, *, prefix_level=None, recent_questions=None):
    matches = [
        question
        for question in active_scope_reviewed_questions_for_text(pasuk_text, skill=skill)
        if reviewed_question_matches_request(question, skill, prefix_level=prefix_level)
    ]
    if not matches:
        return None
    requested_skill = str(skill or "").strip()
    if requested_skill == "translation":
        selected_match = _best_reviewed_translation_match(matches, recent_questions)
    else:
        selected_match = matches[0]
    question = clone_reviewed_question(selected_match, skill)
    record = active_pasuk_record_for_text(pasuk_text)
    if record:
        question.setdefault("pasuk", record.get("text"))
        question.setdefault("pasuk_id", record.get("pasuk_id"))
        question.setdefault("pasuk_ref", active_pasuk_ref_payload(record))
    return validate_question_payload(question)


def override_distractors(pool, correct):
    return [value for value in pool if value and value != correct]


def override_target_entry(surface, translation, *, semantic_group, role_hint, entity_type):
    return {
        "word": surface,
        "translation": translation,
        "type": "noun",
        "part_of_speech": "noun",
        "semantic_group": semantic_group,
        "role_hint": role_hint,
        "entity_type": entity_type,
    }


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

        fresh_sources = [
            pasuk
            for pasuk in source_pesukim
            if pasuk not in recent_pesukim
        ]
        return random.choice(fresh_sources or source_pesukim or [fallback])

    return fallback


def analyze_pasuk(pasuk, word_bank=None):
    if word_bank is None:
        return [analyze_word(word) for word in tokenize_pasuk(pasuk)]

    parsed_items = active_scope_parsed_analysis(pasuk)
    if parsed_items is not None:
        return parsed_items

    analyzed = []
    unknown = []
    for token in tokenize_pasuk(pasuk):
        item = normalize_token(token, word_bank)
        if item is None:
            unknown.append(token)
        else:
            analyzed.append(item)

    if unknown:
        raise ValueError(f"Unknown word(s) not in word bank: {', '.join(unknown)}")

    annotated, _ = annotate_role_layer(analyzed)
    return annotated


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


def build_parallel_choices(correct, candidates, key, *, extra=None, token=None):
    candidate_pool = [
        item
        for item in list(candidates or []) + list(extra or [])
        if item and item != correct and not is_placeholder_translation(item, token)
    ]
    ranked_candidates = rank_parallel_choice_values(correct, candidate_pool)
    quality_floor = parallel_choice_quality_floor(correct)
    high_quality = [
        item
        for item in ranked_candidates
        if parallel_choice_match_score(correct, item) >= quality_floor
    ]
    if quality_floor > 0 and len(high_quality) >= 3:
        ranked_candidates = high_quality

    choices = unique([correct] + ranked_candidates)
    if len(choices) < 4:
        raise ValueError(f"Need 4 parallel choices. Got: {choices}")
    choices = choices[:4]
    stable_rng(key).shuffle(choices)
    return choices


def contains_hebrew(text):
    return any("\u0590" <= char <= "\u05ff" for char in str(text or ""))


def clean_value_text(value):
    text = str(value or "").strip()
    if not text:
        return None
    if set(text) == {"?"}:
        return None
    if "???" in text:
        return None
    return text


def clean_shoresh_value(value):
    text = clean_value_text(value)
    if not text or "?" in text:
        return None
    return text


def student_tense_label(value):
    return morphology_student_tense_label(value)


def student_part_of_speech_label(value):
    return STUDENT_PART_OF_SPEECH_LABELS.get(str(value or "").strip(), str(value or "").strip())


def part_of_speech_with_article(label):
    rendered = student_part_of_speech_label(label)
    if not rendered:
        return rendered
    article = "an" if rendered[0].lower() in {"a", "e", "i", "o", "u"} else "a"
    return f"{article} {rendered}"


def cohort_safe_part_of_speech_choices(correct):
    correct_label = student_part_of_speech_label(correct)
    if correct_label not in COHORT_PART_OF_SPEECH_CHOICES:
        return None
    return [
        correct_label,
        *[label for label in COHORT_PART_OF_SPEECH_CHOICES if label != correct_label],
    ][:4]


def replace_part_of_speech_terms_in_text(text):
    rendered = str(text or "")
    rendered = rendered.replace("part of speech", "kind of word")
    for raw, label in STUDENT_PART_OF_SPEECH_LABELS.items():
        rendered = re.sub(rf"\b{re.escape(raw)}\b", label, rendered)
    return rendered


def tense_form_phrase(value):
    details = classify_tense_form(value)
    return details.get("display_phrase") or ""


def taught_tense_label(value):
    label = student_tense_label(value)
    if label in COHORT_TAUGHT_TENSE_LABELS:
        return label
    return None


def canonical_tense_code(value):
    return canonical_morphology_tense_code(value)


def fair_tense_choice_codes(correct):
    correct_code = canonical_tense_code(correct)
    correct_label = taught_tense_label(correct_code)
    if not correct_code or not correct_label:
        return None

    distractor_labels = [
        label
        for label in COHORT_TAUGHT_TENSE_LABELS
        if label != correct_label
    ]
    if len(distractor_labels) < 3:
        return None

    distractor_codes = [
        COHORT_TAUGHT_TENSE_CANONICAL_CODES[label]
        for label in distractor_labels[:3]
    ]
    choices = [correct_code] + distractor_codes
    if len({student_tense_label(choice) for choice in choices}) != 4:
        return None
    return choices


def replace_tense_codes_in_text(text):
    rendered = str(text or "")
    for code, label in STUDENT_TENSE_LABELS.items():
        rendered = rendered.replace(code, label)
    return rendered


def has_leading_vav(surface):
    first_token = str(surface or "").strip().split()
    if not first_token:
        return False
    normalized = normalize_hebrew_key(first_token[0])
    return normalized.startswith("ו")


def divine_name_style(text):
    rendered = str(text or "")
    for variant in DIVINE_NAME_VARIANTS:
        if variant in rendered:
            return "God" if variant == "G-d" else variant
    return None


def apply_divine_name_style(text, preferred_style):
    rendered = str(text or "")
    preferred = "God" if preferred_style == "G-d" else preferred_style
    if not preferred:
        return rendered
    return DIVINE_NAME_PATTERN.sub(preferred, rendered)


def has_definite_article_prefix(entry):
    prefixes = (entry or {}).get("prefixes") or []
    return any(
        isinstance(prefix, dict) and prefix.get("type") == "definite_article"
        for prefix in prefixes
    )


def clearly_finite_verb_entry(entry, token):
    if entry_type(entry) != "verb" or (entry or {}).get("confidence") == "generated_alternate":
        return False
    # Narrow pilot guard: article-led forms like הָרֹמֶשֶׂת / הַמְּאֹרֹת may be
    # parser-tagged as verbs, but they are not clean finite-tense quiz targets.
    if has_definite_article_prefix(entry):
        return False
    return True


def weak_surface_only_verb_analysis(entry, token):
    entry = entry or {}
    if entry_type(entry) != "verb":
        return False
    normalized_token = normalize_hebrew_key(token or "")
    normalized_shoresh = normalize_hebrew_key(clean_shoresh_value(entry.get("shoresh")) or "")
    if not normalized_token:
        return False
    if normalized_shoresh and normalized_token != normalized_shoresh:
        return False
    if _known_prefix_forms(entry) or _known_suffix_forms(entry):
        return False
    if any(str(entry.get(field) or "").strip() for field in ("person", "number", "gender")):
        return False
    return usable_translation(entry, token) is None


def low_value_part_of_speech_target(entry, token):
    entry = entry or {}
    if entry_type(entry) != "noun":
        return False
    # Context-heavy noun forms with instructional prefixes/suffixes read more
    # like morphology drills than clean word-kind questions for this cohort.
    return standalone_translation_requires_context(entry, token)


def part_of_speech_target_supported(entry, token):
    kind = entry_type(entry)
    if kind not in {"noun", "verb"}:
        return False
    if (entry or {}).get("confidence") == "generated_alternate":
        return False
    if kind == "noun" and low_value_part_of_speech_target(entry, token):
        return False
    if kind == "verb" and weak_surface_only_verb_analysis(entry, token):
        return False
    return True


def is_student_safe_vav_finite_gloss(text):
    rendered = clean_value_text(text)
    if rendered is None:
        return False
    lower = rendered.lower()
    if lower == "and there was":
        return True
    if not lower.startswith(("and he ", "and she ", "and it ", "and they ")):
        return False
    if any(marker in lower for marker in (" when ", " which ", " that ", " who ", ",")):
        return False
    tail = lower.split(" ", 2)[-1].strip()
    if not tail or tail.endswith("ing"):
        return False
    return True


def complete_subjectless_verb_gloss(text):
    rendered = str(text or "").strip()
    if not rendered:
        return rendered
    lower = rendered.lower()
    nominal_phrase_prefixes = (
        "the ",
        "a ",
        "an ",
        "this ",
        "that ",
        "these ",
        "those ",
        "my ",
        "your ",
        "his ",
        "her ",
        "our ",
        "their ",
    )
    if lower.startswith("and "):
        remainder = rendered[4:]
        if remainder.lower().startswith(EXPLICIT_SUBJECT_PREFIXES):
            return rendered
        if remainder.lower().startswith(nominal_phrase_prefixes):
            return rendered
        if remainder.lower().startswith(("let ", "may ")):
            return rendered
        return f"and he {remainder}"
    if lower.startswith(("let ", "may ")):
        return rendered
    if lower.startswith(EXPLICIT_SUBJECT_PREFIXES):
        return rendered
    return rendered


def tense_form_details(value, token=""):
    return classify_tense_form(value, token=token)


def tense_question_explanation(target, correct):
    details = tense_form_details(correct, target["token"])
    display_phrase = details.get("display_phrase") or tense_form_phrase(correct)
    word_gloss = usable_translation(target["entry"], target["token"])
    if word_gloss:
        return f"{target['token']} means '{word_gloss}', so here it uses {display_phrase}."
    return f"{target['token']} uses {display_phrase}."


def sanitize_entry_translation(value, entry=None, token=None):
    rendered = clean_value_text(value)
    if rendered is None:
        return None
    rendered = apply_divine_name_style(rendered, divine_name_style(rendered))
    if entry_type(entry) == "verb":
        if has_leading_vav(token) and not rendered.lower().startswith("and "):
            rendered = f"and {rendered}"
        rendered = complete_subjectless_verb_gloss(rendered)
    return " ".join(rendered.split())


def sanitize_question_translation_text(
    text,
    *,
    question_type="",
    surface="",
    part_of_speech="",
    preferred_divine_style=None,
):
    rendered = clean_value_text(text)
    if rendered is None:
        return None
    if preferred_divine_style:
        rendered = apply_divine_name_style(rendered, preferred_divine_style)
    elif "G-d" in rendered:
        rendered = rendered.replace("G-d", "God")
    if question_type in {"translation", "phrase_translation"} and has_leading_vav(surface):
        if not rendered.lower().startswith("and "):
            rendered = f"and {rendered}"
    if part_of_speech == "verb" and question_type == "translation":
        rendered = complete_subjectless_verb_gloss(rendered)
    return " ".join(rendered.split())


def non_divine_phrase_fallback(text):
    rendered = " ".join(str(text or "").split())
    replacements = (
        ("and the LORD God ", "and someone else "),
        ("and the LORD ", "and someone else "),
        ("and God ", "and someone else "),
        ("the LORD God ", "someone else "),
        ("the LORD ", "someone else "),
        ("God ", "someone else "),
    )
    for prefix, replacement in replacements:
        if rendered.startswith(prefix):
            return f"{replacement}{rendered[len(prefix):]}".strip()
    return None


def is_placeholder_translation(value, token=None):
    rendered = clean_value_text(value)
    if not rendered:
        return True
    text = rendered
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
            return sanitize_entry_translation(value, entry, token)
    return None


AMBIGUOUS_STANDALONE_HAYAH_GLOSSES = {
    "and it was",
    "it was",
    "and there was",
    "there was",
}


def _standalone_affix_forms(entry, key, legacy_key):
    forms = []
    for item in (entry or {}).get(key) or []:
        if not isinstance(item, dict):
            continue
        form = item.get("form")
        if form and form not in forms:
            forms.append(form)
    legacy_form = (entry or {}).get(legacy_key)
    if legacy_form and legacy_form not in forms:
        forms.append(legacy_form)
    return forms


def low_value_standalone_translation_class(entry, token=None):
    entry = entry or {}
    normalized_surface = normalize_hebrew_key(
        token
        or entry.get("surface")
        or entry.get("word")
        or entry.get("menukad")
        or ""
    )
    if normalized_surface in {
        normalize_hebrew_key("אֱלֹהִים"),
        normalize_hebrew_key("אֱלֹקִים"),
        normalize_hebrew_key("יְהוָה"),
    }:
        return True
    if (entry.get("semantic_group") or "") == "divine" or entity_type(entry) == "divine_being":
        return True
    if entity_type(entry) in {"pronoun", "grammatical_particle"}:
        return True
    kind = entry_type(entry)
    return kind == "particle" or str(entry.get("part_of_speech") or "").strip() == "particle"


CONTEXT_DEPENDENT_STANDALONE_TRANSLATION_FORMS = {
    normalize_hebrew_key("אֲכָל"),
    normalize_hebrew_key("יְשׁוּפְךָ"),
    normalize_hebrew_key("תְּשׁוּפֶנּוּ"),
}


def standalone_translation_requires_context(entry, token=None):
    kind = entry_type(entry)
    normalized_surface = normalize_hebrew_key(
        token
        or entry.get("surface")
        or entry.get("word")
        or entry.get("menukad")
        or ""
    )
    prefix_forms = _standalone_affix_forms(entry, "prefixes", "prefix")
    suffix_forms = _standalone_affix_forms(entry, "suffixes", "suffix")
    normalized_prefixes = {normalize_hebrew_key(form) for form in prefix_forms if form}
    non_conjunction_prefixes = {
        form
        for form in normalized_prefixes
        if form != normalize_hebrew_key("ו")
    }

    if kind == "noun" and normalize_hebrew_key("ה") in normalized_prefixes:
        return True
    if kind != "verb" and (non_conjunction_prefixes or suffix_forms):
        return True
    if normalized_surface in CONTEXT_DEPENDENT_STANDALONE_TRANSLATION_FORMS:
        return True
    if low_value_standalone_translation_class(entry, token):
        return True
    gloss = usable_translation(entry, token)
    if kind != "verb" and gloss and gloss.lower().endswith(" of"):
        return True
    foundation = dikduk_foundation_metadata(
        token,
        entry,
        skill="translation",
        question_type="translation",
    )
    if foundation.get("weak_standalone_translation") or foundation.get("ambiguous_without_context"):
        return True
    return False


def standalone_translation_target(entry, token=None):
    if usable_translation(entry, token) is None:
        return False
    if standalone_translation_requires_context(entry, token):
        return False
    if entry_type(entry) != "verb" or not has_leading_vav(token):
        return True
    if normalize_hebrew_key((entry or {}).get("shoresh") or "") != normalize_hebrew_key("היה"):
        return True

    literal = entry.get("translation_literal")
    context = entry.get("translation_context") or entry.get("context_translation")
    if is_placeholder_translation(literal, token) or is_placeholder_translation(context, token):
        return True

    literal = sanitize_entry_translation(literal, entry, token)
    context = sanitize_entry_translation(context, entry, token)
    if literal == context:
        return True
    if {literal.lower(), context.lower()}.issubset(AMBIGUOUS_STANDALONE_HAYAH_GLOSSES):
        return False
    return True


def instructional_value(entry, question_type=None):
    if not isinstance(entry, dict):
        return "low"
    token = entry.get("word") or entry.get("surface")
    if question_type in {
        "word_meaning",
        "translation",
        "subject_identification",
        "object_identification",
    }:
        if question_type in {"word_meaning", "translation"}:
            if not standalone_translation_target(entry, token):
                return "low"
        elif usable_translation(entry, token) is None:
            return "low"
        if entry.get("entity_type") == "grammatical_particle":
            return "low"
        if entry.get("part_of_speech") == "particle" or entry.get("type") == "particle":
            return "low"
    if question_type in {"verb_tense", "shoresh"}:
        if entry.get("type") != "verb" or entry.get("confidence") == "generated_alternate":
            return "low"
        if question_type == "shoresh" and not clean_shoresh_value(entry.get("shoresh")):
            return "low"
        if question_type == "shoresh" and low_value_shoresh_target(entry, token):
            return "low"
        if question_type == "verb_tense" and not runtime_tense_label(entry, token):
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


def runtime_tense_label(entry, token):
    if not clearly_finite_verb_entry(entry, token):
        return None
    if weak_surface_only_verb_analysis(entry, token):
        return None
    if not clean_shoresh_value(entry.get("shoresh")) and usable_translation(entry, token) is None:
        return None
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
    if len(text) > 3 and text.startswith("\u05d5"):
        text = text[1:]
    if len(text) > 3 and text.startswith(("\u05d4", "\u05dc")):
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


PARALLEL_RELATION_PREFIXES = ("from", "to", "in", "on", "with")
PARALLEL_SUBJECT_PREFIXES = (
    "and the lord god ",
    "and the lord ",
    "and god ",
    "and someone else ",
    "and he ",
    "and she ",
    "and it ",
    "and they ",
    "the lord god ",
    "the lord ",
    "god ",
    "someone else ",
)
PARALLEL_PRONOUN_CHOICES = {
    "him",
    "her",
    "them",
    "me",
    "us",
    "you",
    "someone else",
    "something else",
}


def normalized_parallel_text(value):
    cleaned = clean_value_text(value)
    if cleaned is None:
        return ""
    return " ".join(str(cleaned).split()).lower()


def parallel_text_profile(text):
    lowered = normalized_parallel_text(text)
    words = lowered.split()
    subject_prefix = ""
    for prefix in PARALLEL_SUBJECT_PREFIXES:
        if lowered.startswith(prefix):
            subject_prefix = prefix.strip().replace(" ", "_")
            break

    relation_prefix = ""
    for prefix in PARALLEL_RELATION_PREFIXES:
        if lowered.startswith(f"{prefix} "):
            relation_prefix = prefix
            break

    if lowered.startswith("to "):
        leading_form = "to_form"
    elif lowered in PARALLEL_PRONOUN_CHOICES:
        leading_form = "pronoun"
    elif words[:1] and words[0] in {"the", "a", "an"}:
        leading_form = "article_noun"
    elif len(words) == 1:
        leading_form = "single_word"
    else:
        leading_form = words[0] if words else ""

    return {
        "word_count": min(len(words), 4),
        "starts_with_and": lowered.startswith("and "),
        "subject_prefix": subject_prefix,
        "relation_prefix": relation_prefix,
        "leading_form": leading_form,
        "divine_style": divine_name_style(text) or "",
    }


def parallel_choice_match_score(correct, candidate):
    correct_profile = parallel_text_profile(correct)
    candidate_profile = parallel_text_profile(candidate)
    score = 0.0

    if correct_profile["subject_prefix"]:
        if candidate_profile["subject_prefix"] == correct_profile["subject_prefix"]:
            score += 4.0
    elif candidate_profile["starts_with_and"] == correct_profile["starts_with_and"]:
        score += 1.5

    if correct_profile["relation_prefix"]:
        if candidate_profile["relation_prefix"] == correct_profile["relation_prefix"]:
            score += 3.0
    elif not candidate_profile["relation_prefix"]:
        score += 1.0

    if correct_profile["leading_form"] and candidate_profile["leading_form"] == correct_profile["leading_form"]:
        score += 3.0

    if correct_profile["divine_style"]:
        if candidate_profile["divine_style"] == correct_profile["divine_style"]:
            score += 2.0
    elif not candidate_profile["divine_style"]:
        score += 0.5

    word_gap = abs(correct_profile["word_count"] - candidate_profile["word_count"])
    if word_gap == 0:
        score += 2.0
    elif word_gap == 1:
        score += 1.0

    return round(score, 2)


def parallel_choice_quality_floor(correct):
    profile = parallel_text_profile(correct)
    if profile["subject_prefix"] or profile["relation_prefix"]:
        return 5.0
    if profile["leading_form"] in {"article_noun", "to_form"} or profile["word_count"] >= 2:
        return 4.0
    return 0.0


def rank_parallel_choice_values(correct, candidates):
    scored = [
        (
            parallel_choice_match_score(correct, candidate),
            abs(parallel_text_profile(correct)["word_count"] - parallel_text_profile(candidate)["word_count"]),
            candidate,
        )
        for candidate in unique(candidates)
    ]
    scored.sort(key=lambda item: (-item[0], item[1], item[2]))
    return [item[2] for item in scored]


def translation_entry_family_score(entry, correct_entry):
    if not isinstance(entry, dict) or not isinstance(correct_entry, dict):
        return 0.0

    score = 0.0
    if entry_type(entry) == entry_type(correct_entry):
        score += 4.0
    if semantic_group(entry) != "unknown" and semantic_group(entry) == semantic_group(correct_entry):
        score += 3.0
    if entity_type(entry) != "unknown" and entity_type(entry) == entity_type(correct_entry):
        score += 2.0
    if is_person_like_entry(entry) and is_person_like_entry(correct_entry):
        score += 1.0
    return score


def translation_distractor_quality_floor(correct_entry, question_type):
    kind = entry_type(correct_entry)
    if question_type in {"word_meaning", "translation"}:
        if kind == "verb":
            return 9.0
        if kind == "noun":
            return 6.0
    if question_type in {"subject_identification", "object_identification"}:
        return 5.0
    return 0.0


def is_vav_led_finite_translation_target(entry):
    token = (entry or {}).get("word") or (entry or {}).get("surface") or ""
    return has_leading_vav(token) and runtime_tense_label(entry, token) == "vav_consecutive_past"


def filtered_translation_values(
    entries,
    correct,
    correct_entry=None,
    question_type="translation",
    require_quality_count=0,
):
    scored_values = []
    seen_values = {correct}
    seen_keys = set()
    correct_key = distractor_key(correct_entry)
    preferred_divine_style = divine_name_style(correct)
    require_vav_finite_style = is_vav_led_finite_translation_target(correct_entry)
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
        if preferred_divine_style and divine_name_style(value) and divine_name_style(value) != preferred_divine_style:
            continue
        if require_vav_finite_style and not is_student_safe_vav_finite_gloss(value):
            continue
        key = distractor_key(entry)
        if key and key in seen_keys:
            continue
        shape_score = parallel_choice_match_score(correct, value)
        family_score = translation_entry_family_score(entry, correct_entry)
        total_score = round(family_score + shape_score, 2)
        scored_values.append((total_score, family_score, shape_score, value))
        seen_values.add(value)
        if key:
            seen_keys.add(key)

    scored_values.sort(key=lambda item: (-item[0], -item[1], -item[2], item[3]))
    if require_quality_count and correct_entry is not None:
        quality_floor = translation_distractor_quality_floor(correct_entry, question_type)
        high_quality = [value for score, _family, _shape, value in scored_values if score >= quality_floor]
        if len(high_quality) >= require_quality_count:
            return high_quality
    return [value for _score, _family, _shape, value in scored_values]


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


def shoresh_similarity_score(correct, candidate):
    correct_key = normalize_hebrew_key(correct or "")
    candidate_key = normalize_hebrew_key(candidate or "")
    if not correct_key or not candidate_key or correct_key == candidate_key:
        return -1.0

    score = 0.0
    if len(correct_key) == len(candidate_key):
        score += 2.0
    shared_letters = len(set(correct_key) & set(candidate_key))
    score += float(shared_letters)
    same_positions = sum(1 for left, right in zip(correct_key, candidate_key) if left == right)
    score += same_positions * 2.0
    return score


def shoresh_distractors(correct, word_bank):
    scored = []
    for shoresh in valid_shorashim(word_bank):
        score = shoresh_similarity_score(correct, shoresh)
        if score < 0:
            continue
        scored.append((score, shoresh))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [shoresh for _score, shoresh in scored]


def translation_distractors(correct, target_entry, by_group, word_bank=None, require_quality_count=0):
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
    same_group = [
        entry
        for entry in by_group.get(target_entry.get("group"), [])
    ]
    same_type = [
        entry
        for entry in word_bank_entries(word_bank, source_derived_only=True)
        if entry.get("type") == target_entry.get("type")
    ]
    all_translations = [
        entry
        for entry in word_bank_entries(word_bank, source_derived_only=True)
    ]
    return filtered_translation_values(
        same_semantic_group + same_entity_type + same_group + same_type + all_translations,
        correct,
        target_entry,
        question_type="word_meaning",
        require_quality_count=require_quality_count,
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
        return (
            is_subject_candidate_entry(entry)
            and quiz_eligible(entry, token, "subject_identification")
        )
    return True


def first_ready(analyzed, question_type, word_bank=None):
    return find_first(
        analyzed,
        lambda entry, token: quiz_ready(entry, token, question_type, word_bank),
    )


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
        ("he ", ""),
        ("it ", ""),
        ("they ", ""),
        ("and they ", "and "),
    ]
    for prefix, replacement in replacements:
        if action_text.startswith(prefix):
            return f"{replacement}{subject_text} {action_text[len(prefix):]}"
    return f"{subject_text} {action_text}"


PHRASE_ACTION_DISTRACTOR_POOL = (
    "said",
    "made",
    "blessed",
    "finished",
    "created",
    "saw",
    "called",
    "gave",
    "separated",
    "caused to grow",
)

PHRASE_SUBJECT_DISTRACTOR_POOL = (
    "God",
    "the LORD",
    "someone else",
    "they",
)

PHRASE_OBJECT_DISTRACTOR_POOL = (
    "something else",
    "someone else",
    "them",
    "the earth",
    "the heavens",
)

PHRASE_RECIPIENT_DISTRACTOR_POOL = (
    "them",
    "him",
    "her",
    "someone else",
)

PHRASE_DIRECT_OBJECT_ACTION_BLACKLIST = {
    "said",
    "called",
}

SUBJECT_OVERRIDE_DISTRACTOR_POOL = (
    "God",
    "the LORD",
    "the LORD God",
    "someone else",
    "the man",
    "they",
)

OBJECT_OVERRIDE_DISTRACTOR_POOL = (
    "the man",
    "a garden",
    "the earth",
    "the heavens",
    "the seventh day",
    "something else",
)

RECIPIENT_OVERRIDE_DISTRACTOR_POOL = (
    "them",
    "him",
    "her",
    "someone else",
    "the man",
)


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
    for lead in ["and he ", "and it ", "and they ", "he ", "it ", "they ", "and "]:
        if text.startswith(lead):
            return text[len(lead):]
    return text


def strip_relation(text):
    for lead in ["from ", "to ", "in ", "on ", "with "]:
        if text.startswith(lead):
            return text[len(lead):]
    return text


def normalize_role_translation(text):
    text = strip_relation(str(text or "").strip())
    if text.startswith("and "):
        return text[4:]
    return text


def phrase_surface_text(items):
    ordered = sorted(
        (item for item in items if item),
        key=lambda item: (item.get("role_data") or {}).get("token_index", 10**6),
    )
    if not ordered:
        return None
    return " ".join(item["token"] for item in ordered)


def phrase_distractor_pool(pool, correct):
    return [value for value in pool if value and value != correct]


def quiz_ready_phrase_option(phrase, correct, candidates):
    clean_candidates = filtered_phrase_candidates(candidates, phrase)
    if not phrase or not correct or is_placeholder_translation(correct, phrase):
        return None
    if len(clean_candidates) < 3:
        return None
    return {
        "phrase": phrase,
        "correct": correct,
        "candidates": clean_candidates,
    }


def choose_phrase_option(options, recent_phrases=None):
    recent_block = set(list(recent_phrases or [])[-5:])
    for option in options:
        if option["phrase"] not in recent_block:
            return option
    return options[0] if options else None


def quiz_ready_phrase_options(analyzed):
    verb = get_verb(analyzed)
    subject = get_subject(analyzed)
    direct_object = get_direct_object(analyzed)
    recipient_phrase = get_phrase_role(analyzed, "recipient")
    recipient = recipient_phrase["object"] if recipient_phrase else get_recipient(analyzed)
    source_phrase = get_phrase_role(analyzed, "source")
    destination_phrase = get_phrase_role(analyzed, "destination")

    action_text = translated_item_text(verb)
    action = clean_action(action_text or "")
    subject_text = strip_relation(translated_item_text(subject) or "")
    direct_object_text = normalize_role_translation(translated_item_text(direct_object) or "")
    recipient_text = strip_relation(translated_item_text(recipient) or "")

    action_distractors = phrase_distractor_pool(PHRASE_ACTION_DISTRACTOR_POOL, action)
    object_action_distractors = [
        candidate
        for candidate in action_distractors
        if candidate not in PHRASE_DIRECT_OBJECT_ACTION_BLACKLIST
    ]
    subject_distractors = phrase_distractor_pool(PHRASE_SUBJECT_DISTRACTOR_POOL, subject_text)
    object_distractors = phrase_distractor_pool(PHRASE_OBJECT_DISTRACTOR_POOL, direct_object_text)
    recipient_distractors = phrase_distractor_pool(PHRASE_RECIPIENT_DISTRACTOR_POOL, recipient_text)

    options = []

    if (
        verb
        and subject
        and direct_object
        and action
        and action not in PHRASE_DIRECT_OBJECT_ACTION_BLACKLIST
        and subject_text
        and direct_object_text
    ):
        subject_action_text = naturalize_subject_action(action_text or action, subject_text)
        option = quiz_ready_phrase_option(
            phrase_surface_text([verb, direct_object, subject]),
            f"{subject_action_text} {direct_object_text}",
            [
                f"{naturalize_subject_action(object_action_distractors[0], subject_text)} {direct_object_text}",
                f"{subject_distractors[0]} {action} {direct_object_text}",
                f"{subject_action_text} {object_distractors[0]}",
                f"{naturalize_subject_action(object_action_distractors[1], subject_text)} {direct_object_text}",
            ],
        )
        if option:
            options.append(option)

    if verb and subject and recipient and action and subject_text and recipient_text:
        subject_action_text = naturalize_subject_action(action_text or action, subject_text)
        option = quiz_ready_phrase_option(
            phrase_surface_text([verb, recipient, subject]),
            f"{subject_action_text} to {recipient_text}",
            [
                f"{naturalize_subject_action(action_distractors[0], subject_text)} to {recipient_text}",
                f"{subject_distractors[0]} {action} to {recipient_text}",
                f"{subject_action_text} from {recipient_text}",
                f"{subject_action_text} to {recipient_distractors[0]}",
            ],
        )
        if option:
            options.append(option)

    if source_phrase and destination_phrase:
        source_text = translated_item_text(source_phrase["object"])
        destination_text = translated_item_text(destination_phrase["object"])
        if source_text and destination_text:
            source_text = strip_relation(source_text)
            destination_text = strip_relation(destination_text)
            option = quiz_ready_phrase_option(
                f"{source_phrase['text']} {destination_phrase['text']}",
                f"from {source_text} to {destination_text}",
                [
                    f"from {destination_text} to {source_text}",
                    f"from {source_text} in {destination_text}",
                    f"to {source_text} from {destination_text}",
                    f"in {source_text} to {destination_text}",
                ],
            )
            if option:
                options.append(option)

    if (
        verb
        and direct_object
        and action
        and action not in PHRASE_DIRECT_OBJECT_ACTION_BLACKLIST
        and direct_object_text
    ):
        option = quiz_ready_phrase_option(
            phrase_surface_text([verb, direct_object]),
            f"{action} {direct_object_text}",
            [
                f"{object_action_distractors[0]} {direct_object_text}",
                f"{action} {object_distractors[0]}",
                f"{object_action_distractors[1]} {direct_object_text}",
                f"{action} {object_distractors[1]}",
            ],
        )
        if option:
            options.append(option)

    if verb and recipient and action and recipient_text:
        option = quiz_ready_phrase_option(
            phrase_surface_text([verb, recipient]),
            f"{action} to {recipient_text}",
            [
                f"{action_distractors[0]} to {recipient_text}",
                f"{action} from {recipient_text}",
                f"{action_distractors[1]} to {recipient_text}",
                f"{action} to {recipient_distractors[0]}",
            ],
        )
        if option:
            options.append(option)

    if verb and subject and action_text and subject_text:
        option = quiz_ready_phrase_option(
            phrase_surface_text([verb, subject]),
            naturalize_subject_action(action_text, subject_text),
            [
                f"{subject_text} {action_distractors[0]}",
                f"{subject_distractors[0]} {action}",
                f"{subject_text} {action_distractors[1]}",
                f"{subject_distractors[1]} {action}",
            ],
        )
        if option:
            options.append(option)

    return options


def root_meaning(entry):
    text = entry.get("translation", "")
    for lead in [
        "from his ",
        "to his ",
        "in his ",
        "from the ",
        "to the ",
        "in the ",
        "the ",
        "his ",
    ]:
        if text.startswith(lead):
            return text[len(lead):]
    return text


def group_distractors(entry, by_group, limit=3):
    return [
        item["translation"]
        for item in by_group.get(entry.get("group"), [])
        if item["translation"] != entry["translation"]
    ][:limit]


def different_group_distractor(entry, by_group):
    for group, items in by_group.items():
        if group != entry.get("group") and items:
            return items[0]["translation"]
    return "not related"


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


def normalize_student_facing_question(question):
    question_type = str(question.get("question_type", ""))
    skill = str(question.get("skill", ""))

    if question_type in {"verb_tense", "identify_tense"} or skill in {"verb_tense", "identify_tense"}:
        raw_correct = canonical_tense_code(question.get("correct_answer"))
        question["correct_answer"] = student_tense_label(raw_correct)
        question["choices"] = [student_tense_label(canonical_tense_code(choice)) for choice in question.get("choices", [])]
        question["question"] = replace_tense_codes_in_text(question.get("question"))
        if "question_text" in question:
            question["question_text"] = replace_tense_codes_in_text(question.get("question_text"))
        question["explanation"] = replace_tense_codes_in_text(question.get("explanation"))
        if raw_correct:
            question.setdefault("tense_code", raw_correct)
        question["question"] = question["question"].replace("What verb tense is shown?", "What form is shown?")
        if "question_text" in question:
            question["question_text"] = question["question_text"].replace("What verb tense is shown?", "What form is shown?")
        question["question"] = question["question"].replace("Which word shows the to do form form?", "Which word shows the 'to do' form?")
        if "question_text" in question:
            question["question_text"] = question["question_text"].replace("Which word shows the to do form form?", "Which word shows the 'to do' form?")

    if question_type == "part_of_speech" or skill == "part_of_speech":
        question["correct_answer"] = student_part_of_speech_label(question.get("correct_answer"))
        question["choices"] = [student_part_of_speech_label(choice) for choice in question.get("choices", [])]
        question["question"] = replace_part_of_speech_terms_in_text(question.get("question"))
        if "question_text" in question:
            question["question_text"] = replace_part_of_speech_terms_in_text(question.get("question_text"))
        question["explanation"] = replace_part_of_speech_terms_in_text(question.get("explanation"))

    translation_like = question_type in {
        "translation",
        "phrase_translation",
        "subject_identification",
        "object_identification",
    } or skill in {
        "translation",
        "phrase_translation",
        "subject_identification",
        "object_identification",
    }
    if translation_like:
        surface = question.get("selected_word") or question.get("word") or ""
        part_of_speech = str(question.get("part_of_speech", ""))
        raw_correct = clean_value_text(question.get("correct_answer")) or str(question.get("correct_answer", "")).strip()
        if raw_correct:
            sanitized_correct = sanitize_question_translation_text(
                raw_correct,
                question_type=question_type,
                surface=surface,
                part_of_speech=part_of_speech,
            )
            preferred_style = divine_name_style(sanitized_correct)
            original_choices = list(question.get("choices", []))
            choice_style = preferred_style if question_type in {"translation", "phrase_translation"} else preferred_style
            sanitized_choices = unique(
                sanitize_question_translation_text(
                    choice,
                    question_type=question_type,
                    surface=surface,
                    part_of_speech=part_of_speech,
                    preferred_divine_style=choice_style,
                )
                for choice in original_choices
            )
            if sanitized_correct not in sanitized_choices:
                sanitized_choices = [sanitized_correct] + sanitized_choices
            while question_type == "phrase_translation" and len(sanitized_choices) < len(original_choices):
                fallback = non_divine_phrase_fallback(sanitized_correct)
                if not fallback or fallback in sanitized_choices:
                    break
                sanitized_choices.append(fallback)
            if len(sanitized_choices) >= len(original_choices):
                question["choices"] = sanitized_choices
            question["correct_answer"] = sanitized_correct
            explanation = str(question.get("explanation", ""))
            if raw_correct and sanitized_correct and raw_correct in explanation:
                question["explanation"] = explanation.replace(raw_correct, sanitized_correct)

    return question


def validate_question_payload(question):
    attach_dikduk_foundation_metadata(question)
    normalize_student_facing_question(question)
    choices = list(question.get("choices", []))
    question_type = str(question.get("question_type", ""))
    skill = str(question.get("skill", ""))
    if question_type.startswith("prefix_level_") or skill == "identify_prefix_meaning":
        if len(choices) < 4:
            raise ValueError(f"Prefix question must have at least 4 choices: {question.get('question')}")
    elif len(choices) != 4:
        raise ValueError(f"Question must have exactly 4 choices: {question.get('question')}")
    if len(set(choices)) != len(choices):
        raise ValueError(f"Question choices must be unique: {question.get('question')}")
    if question.get("correct_answer") not in choices:
        raise ValueError(f"Correct answer is missing from choices: {question.get('question')}")
    if skill == "segment_word_parts":
        morpheme_type = question.get("morpheme_type")
        if morpheme_type == "prefix":
            allowed_choices = set(PREFIX_FORM_BANK)
        elif morpheme_type == "suffix":
            allowed_choices = set(SUFFIX_FORM_BANK)
        else:
            allowed_choices = set()
        if not morpheme_type or any(choice not in allowed_choices for choice in choices):
            raise ValueError(
                f"segment_word_parts choices must be lane-consistent affix units: {question.get('question')}"
            )
    random.shuffle(choices)
    question["choices"] = choices
    question.setdefault("id", question_id_for(question))
    return question


def foundation_entry_hint(question):
    entry = {}
    part_of_speech = question.get("part_of_speech")
    if part_of_speech:
        entry["type"] = part_of_speech
        entry["part_of_speech"] = part_of_speech
    for field in ("prefix", "suffix", "shoresh", "tense", "person", "gender", "number"):
        value = question.get(field)
        if value:
            entry[field] = value
    return entry


def attach_dikduk_foundation_metadata(question):
    if not isinstance(question, dict) or question.get("status") == "skipped":
        return question
    token = question.get("selected_word") or question.get("word")
    if not token:
        return question
    entry = foundation_entry_hint(question)
    question["dikduk_foundation"] = dikduk_foundation_metadata(
        token,
        entry or None,
        skill=question.get("skill"),
        question_type=question.get("question_type"),
    )
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
    **extra_fields,
):
    payload = {
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
    }
    payload.update({
        key: value
        for key, value in extra_fields.items()
        if value is not None and value != ""
    })
    return validate_question_payload(payload)


def role_data(item):
    return (item or {}).get("role_data") or {}


def role_status(analyzed):
    if not analyzed:
        return "no_tokens"
    return role_data(analyzed[0]).get("role_status", "unresolved")


def get_verb(analyzed):
    return next(
        (
            item
            for item in analyzed
            if role_data(item).get("clause_role") == "verb"
        ),
        None,
    )


def get_prefixed_word(analyzed):
    return find_first(analyzed, lambda entry, token: is_prefix_candidate(entry, token))


def get_suffixed_word(analyzed, word_bank=None):
    target = find_first(analyzed, lambda entry, token: is_suffix_candidate(entry, token, word_bank))
    return with_suffix_metadata(target)


def get_translatable_word(analyzed):
    return find_first(analyzed, lambda entry, token: standalone_translation_target(entry, token))


def get_part_of_speech_word(analyzed):
    return find_first(analyzed, lambda entry, _token: entry_type(entry) in {"verb", "noun"})


def infer_tense(entry, token):
    return runtime_tense_label(entry, token)


def choice_pool(values, correct, fallback):
    choices = unique([correct] + [value for value in values if value != correct] + fallback)
    return choices[:4]


def prefix_meaning_choices(prefix):
    correct = PREFIX_MEANINGS.get(prefix, "and")
    return unique([correct] + [value for value in PREFIX_MEANING_BANK if value != correct])


def suffix_form_choices(suffix):
    correct_meaning = SUFFIX_MEANINGS.get(suffix)
    distractors = [
        form
        for form in SUFFIX_FORM_BANK
        if form != suffix and SUFFIX_MEANINGS.get(form) != correct_meaning
    ]
    return unique([suffix] + distractors)


def has_lexical_plural_ending(entry, token, suffix):
    normalized = normalize_hebrew_key(token or "")
    if suffix not in {"\u05dd", "\u05df"}:
        return False
    if not normalized.endswith(("ים", "ין")):
        return False
    if (entry or {}).get("type") == "suffix_form":
        return False
    return entry_type(entry) in {"noun", "adj", "unknown"}


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


def low_value_shoresh_target(entry, token):
    entry = entry or {}
    normalized_token = normalize_hebrew_key(token or "")
    normalized_shoresh = normalize_hebrew_key(clean_shoresh_value(entry.get("shoresh")) or "")
    if not normalized_token or not normalized_shoresh:
        return False
    if normalized_token != normalized_shoresh:
        return False
    if _known_prefix_forms(entry) or _known_suffix_forms(entry):
        return False
    return (
        str(entry.get("tense") or "").strip() == "past"
        and str(entry.get("person") or "").strip() == "3"
        and str(entry.get("number") or "").strip() == "singular"
        and str(entry.get("gender") or "").strip() == "masculine"
    )


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
    if code == "low_value_shoresh_target":
        return f"{token} is already a bare past form, so this shoresh question would add little."
    if code == "suffix_meaning_mismatch":
        return f"{token} does not have one clearly defensible suffix meaning."
    if code == "suffix_distractor_leak":
        return f"{token} has more than one plausible correct answer in the choice list."
    if code == "compound_morphology":
        return f"{token} carries compound morphology, so a simple question would be ambiguous."
    if code == "context_dependent_suffix":
        return f"{token} depends on verb/context morphology, so it is not a safe isolated-word suffix question."
    if code == "lexical_plural_ending":
        return f"{token} ends with a normal plural/lexical ending, not a possessive suffix."
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
    prefix_types = {
        prefix_data.get("type")
        for prefix_data in (entry.get("prefixes") or [])
        if isinstance(prefix_data, dict) and prefix_data.get("type")
    }

    if "verb_prefix_vav_consecutive" in prefix_types:
        return invalid_result(
            "compound_morphology",
            prefix_forms=prefix_forms,
            prefix_types=sorted(prefix_types),
            tense=entry.get("tense"),
        )

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
    if entity_type(entry) in {"pronoun", "grammatical_particle"}:
        return invalid_result(
            "non_suffix_lexical_form",
            entry_type=entry_type(entry),
            entity_type=entity_type(entry),
        )
    if entry_type(entry) in {"pronoun", "particle"}:
        return invalid_result(
            "non_suffix_lexical_form",
            entry_type=entry_type(entry),
            entity_type=entity_type(entry),
        )
    suffix_forms = _known_suffix_forms(entry)

    if not suffix_forms:
        return invalid_result("no_clear_suffix", suffix_forms=suffix_forms)

    if len(suffix_forms) > 1:
        return invalid_result("multiple_suffixes", suffix_forms=suffix_forms)

    prefix_forms = _known_prefix_forms(entry)

    # A single clean suffix is fine even with one attached prefix, but once the
    # form stacks multiple prefixes the suffix meaning stops being a simple quiz.
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
    if has_lexical_plural_ending(entry, token, expected_suffix):
        return invalid_result(
            "lexical_plural_ending",
            expected_suffix=expected_suffix,
            normalized_token=normalize_hebrew_key(token),
        )
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
    expected_shoresh = clean_shoresh_value(entry.get("shoresh"))
    if not expected_shoresh:
        return invalid_result("no_clear_shoresh")

    prefix_types = [
        prefix.get("type")
        for prefix in (entry.get("prefixes") or [])
        if isinstance(prefix, dict) and prefix.get("type")
    ]
    allowed_prefix_types = {
        "conjunction",
        "verb_prefix_vav_consecutive",
        "verb_prefix_future",
    }

    if not clearly_finite_verb_entry(entry, token):
        return invalid_result(
            "shoresh_not_supported",
            entry_type=entry_type(entry),
            confidence=entry.get("confidence"),
        )

    if any(prefix_type not in allowed_prefix_types for prefix_type in prefix_types):
        return invalid_result(
            "shoresh_not_supported",
            prefix_types=prefix_types,
            entry_type=entry_type(entry),
        )

    if runtime_tense_label(entry, token) is None:
        return invalid_result(
            "shoresh_not_supported",
            entry_type=entry_type(entry),
            confidence=entry.get("confidence"),
            tense=entry.get("tense"),
        )

    if low_value_shoresh_target(entry, token):
        return invalid_result(
            "low_value_shoresh_target",
            token=token,
            expected_shoresh=expected_shoresh,
            tense=entry.get("tense"),
            person=entry.get("person"),
            number=entry.get("number"),
            gender=entry.get("gender"),
        )

    normalized_token = normalize_hebrew_key(token or "")
    normalized_shoresh = normalize_hebrew_key(expected_shoresh or "")
    if "verb_prefix_future" in prefix_types:
        stripped_future_surface = (
            normalized_token[1:]
            if normalized_token[:1] in {"י", "ת", "א", "נ"}
            else normalized_token
        )
        if (
            len(stripped_future_surface) < 2
            or (
                stripped_future_surface != normalized_shoresh
                and not stripped_future_surface.startswith(normalized_shoresh[:2])
                and not normalized_shoresh.startswith(stripped_future_surface[:2])
            )
        ):
            return invalid_result(
                "shoresh_not_supported",
                prefix_types=prefix_types,
                token=token,
                expected_shoresh=expected_shoresh,
            )

    if len(normalized_shoresh) > 4:
        return invalid_result(
            "shoresh_not_supported",
            token=token,
            expected_shoresh=expected_shoresh,
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
                lambda _choice, choice_entry: _normalized_match(
                    clean_shoresh_value(choice_entry.get("shoresh")),
                    expected_shoresh,
                ),
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

    if not clearly_finite_verb_entry(entry, token):
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


def strip_hebrew_marks(word):
    return "".join(
        char
        for char in word
        if not "\u0591" <= char <= "\u05c7"
    )


def detect_verb_tense(word):
    return parser_detect_verb_tense(word)


def is_verb(word):
    analyses = parser_generate_candidate_analyses(word)
    return any(
        analysis.get("part_of_speech") == "verb"
        and analysis.get("confidence") != "generated_alternate"
        for analysis in analyses
    )


def confident_verb_tense(entry, token):
    entry = entry or {}
    explicit = entry.get("tense")
    if explicit:
        return explicit

    if not clearly_finite_verb_entry(entry, token):
        return None

    for analysis in parser_generate_candidate_analyses(token):
        if analysis.get("part_of_speech") != "verb":
            continue
        if analysis.get("confidence") == "generated_alternate":
            continue
        if has_definite_article_prefix(analysis):
            continue
        tense = analysis.get("tense")
        if tense:
            return tense
    return None


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
        if recent_prefixes.count("\u05d5") >= 2:
            candidates = [
                candidate
                for candidate in varied_prefixes or candidates
                if extract_prefix(candidate["word"]) != "\u05d5"
            ] or varied_prefixes or candidates
        else:
            non_vav = [
                candidate
                for candidate in varied_prefixes or candidates
                if not candidate["word"].startswith("\u05d5")
            ]
            candidates = non_vav or varied_prefixes or candidates

    recent_suffixes = progress.get("recent_suffixes", [])[-5:]
    if skill in {"suffix", "identify_suffix_meaning", "identify_pronoun_suffix", "identify_suffix_past"}:
        non_vav_suffixes = [
            candidate
            for candidate in candidates
            if not candidate["word"].endswith("\u05d5")
        ]
        varied_suffixes = [
            candidate
            for candidate in candidates
            if not has_suffix(candidate["word"])
            or extract_suffix(candidate["word"]) not in recent_suffixes
        ]
        if recent_suffixes.count("\u05d5") >= 2:
            candidates = [
                candidate
                for candidate in varied_suffixes or candidates
                if not candidate["word"].endswith("\u05d5")
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


def skill_question_payload(
    skill,
    target,
    question_text,
    choices,
    correct_answer,
    explanation,
    **extra_fields,
):
    skill = resolve_skill_id(skill) or skill
    entry = target.get("entry") or {}
    metadata = SKILL_METADATA[skill]
    payload = {
        "question_text": question_text,
        "question": question_text,
        "choices": choices,
        "correct_answer": correct_answer,
        "skill": skill,
        "mode": "pasuk" if skill in {"subject_identification", "phrase_translation"} else "word",
        "translation_mode": (
            TRANSLATION_NATURAL
            if skill in {"subject_identification", "phrase_translation"}
            else TRANSLATION_LITERAL
        ),
        "standard": metadata["standard"],
        "micro_standard": metadata["micro_standard"],
        "difficulty": metadata["difficulty"],
        "question_type": skill,
        "word": target["token"],
        "selected_word": target["token"],
        "prefix": entry.get("prefix", ""),
        "prefix_meaning": entry.get("prefix_meaning", ""),
        "suffix": entry.get("suffix", ""),
        "suffix_meaning": entry.get("suffix_meaning", ""),
        "shoresh": clean_shoresh_value(entry.get("shoresh")) or "",
        "tense": entry.get("tense", ""),
        "part_of_speech": entry_type(entry),
        "explanation": explanation,
        "word_gloss": usable_translation(entry, target["token"]) or "",
        "source": "generated skill question",
    }
    if target.get("source_pasuk"):
        payload["pasuk"] = target["source_pasuk"]
    payload.update({
        key: value
        for key, value in extra_fields.items()
        if value is not None and value != ""
    })
    return validate_question_payload(payload)


def prefix_level_question_payload(
    skill,
    target,
    level,
    question_format,
    question_text,
    choices,
    correct_answer,
    explanation,
):
    choices = unique([correct_answer] + [choice for choice in choices if choice != correct_answer])
    question = skill_question_payload(
        skill,
        target,
        question_text,
        choices,
        correct_answer,
        explanation,
    )
    question["prefix_level"] = level
    question["prefix"] = extract_prefix(target["token"]) or target["entry"].get("prefix")
    question["question_format"] = question_format
    question["question_type"] = f"prefix_level_{level}_{question_format}"
    question["difficulty"] = level
    return validate_question_payload(question)


def choose_prefix_question_level(prefix_level, recent_question_formats):
    level = max(1, min(5, int(prefix_level or 1)))
    formats_by_level = {
        1: ["identify_prefix_letter"],
        2: ["identify_prefix_meaning"],
        3: ["apply_prefix_meaning"],
        4: ["distinguish_prefixes"],
        5: ["explain_prefix_function"],
    }
    formats = formats_by_level[level]
    recent = set((recent_question_formats or [])[-3:])
    available = [item for item in formats if item not in recent]
    return level, (available or formats)[0]


def generate_question(
    skill,
    pasuk=None,
    mode="direct",
    asked_tokens=None,
    asked_question_types=None,
    prefix_level=1,
    recent_question_formats=None,
    recent_prefixes=None,
    recent_questions=None,
    progress=None,
    analyzed_override=None,
    word_bank_override=None,
    by_group_override=None,
):
    skill = resolve_skill_id(skill) or skill
    if pasuk is None or (isinstance(pasuk, (list, tuple)) and not is_structured_pasuk(pasuk)):
        pasuk_pool = list(pasuk or CHUMASH_PESUKIM)
        if not pasuk_pool:
            raise ValueError("No pesukim available for question generation.")

        shuffled_pasuks = pasuk_pool[:]
        random.shuffle(shuffled_pasuks)
        last_error = None
        for selected_pasuk in shuffled_pasuks:
            try:
                question = generate_question(
                    skill,
                    selected_pasuk,
                    mode=mode,
                    asked_tokens=asked_tokens,
                    asked_question_types=asked_question_types,
                    prefix_level=prefix_level,
                    recent_question_formats=recent_question_formats,
                    recent_prefixes=recent_prefixes,
                    recent_questions=recent_questions,
                    progress=progress,
                    analyzed_override=None,
                    word_bank_override=word_bank_override,
                    by_group_override=by_group_override,
                )
                if is_skip_payload(question):
                    last_error = ValueError(question.get("reason", f"{skill} skipped"))
                    continue
                question.setdefault("pasuk", selected_pasuk)
                return question
            except ValueError as error:
                last_error = error

        raise ValueError(f"No usable pasuk found for skill '{skill}': {last_error}")

    if skill not in SKILLS:
        raise ValueError(f"Unknown skill: {skill}. Expected one of: {', '.join(SKILLS)}")
    if mode not in {"direct", "context", "selection"}:
        raise ValueError("mode must be one of: direct, context, selection")
    if skill in {
        "identify_prefix_future",
        "identify_suffix_past",
        "identify_present_pattern",
        "convert_future_to_command",
        "match_pronoun_to_verb",
    }:
        raise ValueError(
            f"{skill} is not quiz-ready in the active parsed dataset scope: "
            f"{ACTIVE_ASSESSMENT_SCOPE}"
        )

    if word_bank_override is None and by_group_override is None:
        word_bank, by_group = load_word_bank()
    else:
        word_bank = word_bank_override or {}
        by_group = by_group_override or {}
    if analyzed_override is not None:
        pasuk_text = pasuk or structured_pasuk_text(analyzed_override)
        analyzed = prebuilt_analyzed_pasuk(analyzed_override)
    elif is_structured_pasuk(pasuk):
        pasuk_text = structured_pasuk_text(pasuk)
        analyzed = normalize_analyzed_pasuk(pasuk, word_bank)
    else:
        pasuk_text = pasuk
        try:
            analyzed = analyze_pasuk(pasuk, word_bank)
        except ValueError:
            analyzed = normalize_analyzed_pasuk(analyze_pasuk(pasuk), word_bank)
    pasuk = pasuk_text

    if mode in {"direct", "context"} and analyzed_override is None:
        reviewed_question = reviewed_question_for_pasuk_skill(
            pasuk_text,
            skill,
            prefix_level=prefix_level,
            recent_questions=recent_questions,
        )
        if reviewed_question is not None:
            return reviewed_question

    asked_set = set(asked_tokens or [])
    used_types = set(asked_question_types or [])
    asked_suffixes = [
        suffix
        for suffix in (extract_suffix(token) for token in (asked_tokens or []))
        if suffix
    ]
    if progress is None:
        progress = {
            "recent_words": list(asked_tokens or []),
            "recent_suffixes": asked_suffixes,
        }
    else:
        progress.setdefault("recent_words", list(asked_tokens or []))
        progress.setdefault("recent_suffixes", asked_suffixes)
    if recent_prefixes is not None:
        progress.setdefault("recent_prefixes", list(recent_prefixes))
    add_words_from_pasuk(pasuk_text, progress)

    def finish(question):
        if mode == "selection":
            question["hide_focus_word"] = True
        return validate_question_payload(question)

    def clean_choices(correct, candidates):
        choices = unique([correct] + [item for item in candidates if item and item != correct])
        if len(choices) < 4:
            raise ValueError(f"Could not build 4 clean choices for {skill}: {choices}")
        choices = choices[:4]
        stable_rng(f"{pasuk_text}|{skill}|choices").shuffle(choices)
        return choices

    def same_group_translation_choices(target_entry, correct):
        distractors = translation_distractors(
            correct,
            target_entry,
            by_group,
            word_bank,
            require_quality_count=3,
        )
        return build_parallel_choices(
            correct,
            distractors,
            f"{pasuk_text}|{skill}|translation",
            token=target_entry.get("word"),
        )

    def pasuk_word_choices(correct_token):
        return clean_choices(
            correct_token,
            [item["token"] for item in analyzed if item["token"] != correct_token],
        )

    def prompt(direct_text, context_text, selection_text):
        if mode == "context":
            return context_text
        if mode == "selection":
            return selection_text
        return direct_text

    def target_preference_score(item):
        token = item["token"]
        entry = item["entry"]
        kind = entry_type(entry)

        if skill == "translation":
            score = 0.0
            if standalone_translation_requires_context(entry, token):
                score -= 3.0
            if semantic_group(entry) == "unknown":
                score -= 0.5
            return score

        if skill == "shoresh":
            normalized = normalize_hebrew_key(token)
            score = 0.0
            if not normalized.startswith("ו"):
                score += 2.0
            elif normalized.startswith(("וי", "ות")):
                score -= 1.5
            else:
                score -= 1.0
            if normalize_hebrew_key(entry.get("shoresh") or "") == normalize_hebrew_key("היה"):
                score -= 1.0
            return score

        return 0.0

    def preferred_target_pool(items):
        if not items:
            return []
        scores = [target_preference_score(item) for item in items]
        best_score = max(scores)
        return [item for item, score in zip(items, scores) if score == best_score]

    def choose_target(predicate, fallback=None):
        candidates = [item for item in analyzed if predicate(item["entry"], item["token"])]
        if not candidates and fallback is not None:
            target = fallback()
            if target is not None and predicate(target["entry"], target["token"]):
                target.setdefault("source_pasuk", pasuk_text)
                remember_selected_word(progress, target["token"], target["entry"])
            return target
        if not candidates:
            return None

        unused = [item for item in candidates if item["token"] not in asked_set]
        pool = preferred_target_pool(unused or candidates) or (unused or candidates)
        selected_word = pick_word_for_skill(
            [item["token"] for item in pool],
            skill,
            progress,
        )
        target = next((item for item in pool if item["token"] == selected_word), pool[0])
        target.setdefault("source_pasuk", pasuk_text)
        remember_selected_word(progress, target["token"], target["entry"])
        return target

    def prepare_candidate_item(item, *, add_prefix=False, add_suffix=False):
        candidate_entry = dict(item["entry"])
        if add_prefix:
            apply_prefix_metadata(item["token"], candidate_entry, word_bank)
        if add_suffix:
            apply_suffix_metadata(item["token"], candidate_entry, word_bank)
        return {**item, "entry": candidate_entry}

    def validation_choice_entries(choices=None, *, add_prefix=False, add_suffix=False):
        requested = set(choices or [])
        choice_entries = {}
        for item in analyzed:
            token = item["token"]
            if requested and token not in requested:
                continue
            prepared = prepare_candidate_item(item, add_prefix=add_prefix, add_suffix=add_suffix)
            choice_entries[token] = prepared["entry"]
        return choice_entries

    def collect_validated_candidates(
        validation_skill,
        predicate,
        *,
        add_prefix=False,
        add_suffix=False,
    ):
        candidates = []
        selection_choice_entries = None
        selection_choices = None
        if mode == "selection":
            selection_choice_entries = validation_choice_entries(
                None,
                add_prefix=add_prefix,
                add_suffix=add_suffix,
            )
            selection_choices = list(selection_choice_entries.keys())
        for item in analyzed:
            if not predicate(item["entry"], item["token"]):
                continue
            prepared = prepare_candidate_item(item, add_prefix=add_prefix, add_suffix=add_suffix)
            result = validate_question_candidate(
                validation_skill,
                prepared["token"],
                prepared["entry"],
                correct_answer=prepared["token"] if mode == "selection" else None,
                choices=selection_choices,
                choice_entries=selection_choice_entries,
            )
            if not result["valid"]:
                continue
            candidates.append(prepared)
        return candidates

    def choose_validated_target(
        validation_skill,
        predicate,
        *,
        add_prefix=False,
        add_suffix=False,
    ):
        candidates = collect_validated_candidates(
            validation_skill,
            predicate,
            add_prefix=add_prefix,
            add_suffix=add_suffix,
        )
        if not candidates:
            return None

        unused = [item for item in candidates if item["token"] not in asked_set]
        pool = preferred_target_pool(unused or candidates) or (unused or candidates)
        selected_word = pick_word_for_skill(
            [item["token"] for item in pool],
            skill,
            progress,
        )
        target = next((item for item in pool if item["token"] == selected_word), pool[0])
        target.setdefault("source_pasuk", pasuk_text)
        remember_selected_word(progress, target["token"], target["entry"])
        return target

    def validated_question_payload(
        validation_skill,
        target,
        question_text,
        correct,
        choices,
        explanation,
        *,
        add_prefix=False,
        add_suffix=False,
        **extra_fields,
    ):
        cleaned_choices = clean_choices(correct, choices)
        choice_entries = None
        if mode == "selection":
            choice_entries = validation_choice_entries(
                cleaned_choices,
                add_prefix=add_prefix,
                add_suffix=add_suffix,
            )
        result = validate_question_candidate(
            validation_skill,
            target["token"],
            target["entry"],
            correct_answer=correct,
            choices=cleaned_choices,
            choice_entries=choice_entries,
        )
        if not result["valid"]:
            return skip_question_payload(
                skill,
                pasuk_text,
                format_validation_reason(target["token"], result),
                details=result,
            )
        return skill_question_payload(
            skill,
            target,
            question_text,
            cleaned_choices,
            correct,
            explanation,
            **extra_fields,
        )

    def grammar_choice_payload(target, question_text, correct, choices, explanation, **extra_fields):
        return validated_question_payload(
            skill,
            target,
            question_text,
            correct,
            choices,
            explanation,
            **extra_fields,
        )

    def choose_validated_suffix_target():
        return choose_validated_target(
            "identify_suffix_meaning",
            lambda entry, token: is_suffix_candidate(entry, token, word_bank),
            add_prefix=True,
            add_suffix=True,
        )

    def build_prefix_level_question():
        recent_prefixes_window = list(recent_prefixes or [])[-5:]
        prefix_candidates = collect_validated_candidates(
            "identify_prefix_meaning",
            lambda entry, token: is_prefix_candidate(entry, token, word_bank),
            add_prefix=True,
            add_suffix=True,
        )
        available_prefix_candidates = [
            item
            for item in prefix_candidates
            if recent_prefixes_window.count(item["entry"].get("prefix") or extract_prefix(item["token"])) < 2
        ]

        target = None
        if available_prefix_candidates:
            selected_word = pick_word_for_skill(
                [item["token"] for item in available_prefix_candidates],
                "prefix",
                progress,
            )
            target = next(
                (
                    item
                    for item in available_prefix_candidates
                    if item["token"] == selected_word
                ),
                available_prefix_candidates[0],
            )

        if target is None:
            return skip_question_payload(skill, pasuk_text, "No usable prefixed word found in this pasuk.")
        target.setdefault("source_pasuk", pasuk_text)
        remember_selected_word(progress, target["token"], target["entry"])

        level, question_format = choose_prefix_question_level(
            prefix_level,
            recent_question_formats,
        )
        apply_prefix_metadata(target["token"], target["entry"], word_bank)
        prefix = extract_prefix(target["token"], word_bank)
        prefix_meaning = PREFIX_MEANINGS.get(prefix)
        base_word = target["entry"].get("base_word") or target.get("base") or target["token"]
        word_meaning = target["entry"].get("translation")

        def validated_prefix_payload(question_text, choices, correct_answer, explanation):
            result = validate_question_candidate(
                "identify_prefix_meaning",
                target["token"],
                target["entry"],
                correct_answer=correct_answer,
                choices=choices,
            )
            if not result["valid"]:
                return skip_question_payload(
                    skill,
                    pasuk_text,
                    format_validation_reason(target["token"], result),
                    details=result,
                )
            return prefix_level_question_payload(
                skill,
                target,
                level,
                question_format,
                question_text,
                choices,
                correct_answer,
                explanation,
            )

        if level == 1:
            return validated_prefix_payload(
                f"What is the prefix in {target['token']}?",
                PREFIX_FORM_BANK,
                prefix,
                f"The prefix in {target['token']} is {prefix}.",
            )

        if level == 2:
            return validated_prefix_payload(
                f"What does the prefix {prefix} add?",
                prefix_meaning_choices(prefix),
                prefix_meaning,
                f"In {target['token']}, {prefix} means '{prefix_meaning}'.",
            )

        if level == 3:
            base_translation = root_meaning(target["entry"])
            return validated_prefix_payload(
                f"What does {target['token']} mean?",
                [
                    word_meaning,
                    base_translation,
                    f"from {base_translation}",
                    f"to {base_translation}",
                    f"in {base_translation}",
                ],
                word_meaning,
                f"{prefix} adds '{prefix_meaning}' to {base_word}.",
            )

        if level == 4:
            return validated_prefix_payload(
                f"Which prefix means '{prefix_meaning}' here?",
                PREFIX_FORM_BANK,
                prefix,
                f"The word {target['token']} uses {prefix} for '{prefix_meaning}'.",
            )

        return validated_prefix_payload(
            f"What job does {prefix} do in {target['token']}?",
            [
                f"adds '{prefix_meaning}' to the word",
                "marks ownership at the end",
                "changes the word into a noun",
                "removes the base word meaning",
            ],
            f"adds '{prefix_meaning}' to the word",
            f"The prefix {prefix} helps show '{prefix_meaning}' in {target['token']}.",
        )

    if skill == "identify_prefix_meaning":
        return build_prefix_level_question()

    if skill == "identify_suffix_meaning":
        target = choose_validated_suffix_target()
        if target is None:
            return skip_question_payload(skill, pasuk_text, "No suffixed word found in this pasuk.")
        suffix = target["entry"].get("suffix")
        correct = SUFFIX_MEANINGS.get(suffix)
        return validated_question_payload(
            "identify_suffix_meaning",
            target,
            f"What does the suffix {suffix} add?",
            correct,
            list(SUFFIX_MEANINGS.values()),
            f"In {target['token']}, {suffix} means '{correct}'.",
            add_prefix=True,
            add_suffix=True,
        )

    if skill == "identify_pronoun_suffix":
        target = choose_validated_suffix_target()
        if target is None:
            return skip_question_payload(skill, pasuk_text, "No pronoun suffix found in this pasuk.")
        suffix = target["entry"].get("suffix")
        correct = SUFFIX_MEANINGS.get(suffix)
        return validated_question_payload(
            "identify_pronoun_suffix",
            target,
            f"What does the ending {suffix} mean?",
            correct,
            list(SUFFIX_MEANINGS.values()),
            f"The ending {suffix} in {target['token']} means '{correct}'.",
            add_prefix=True,
            add_suffix=True,
        )

    if skill == "identify_verb_marker":
        target = choose_target(
            lambda entry, token: entry_type(entry) == "verb" and is_prefix_candidate(entry, token, word_bank)
        )
        if target is None:
            return skip_question_payload(skill, pasuk_text, "No prefixed verb found in this pasuk.")
        apply_prefix_metadata(target["token"], target["entry"], word_bank)
        prefix = extract_prefix(target["token"], word_bank)
        correct = PREFIX_MEANINGS.get(prefix)
        return grammar_choice_payload(
            target,
            f"What does the first letter {prefix} add?",
            correct,
            prefix_meaning_choices(prefix),
            f"In {target['token']}, {prefix} marks '{correct}'.",
        )

    if skill == "segment_word_parts":
        target = choose_target(
            lambda entry, token: bool(is_prefix_candidate(entry, token, word_bank) or is_suffix_candidate(entry, token, word_bank)),
        )
        if target is None:
            return skip_question_payload(skill, pasuk_text, "No word with a prefix or suffix found in this pasuk.")
        target = with_suffix_metadata(target, word_bank)
        apply_prefix_metadata(target["token"], target["entry"], word_bank)
        prefix = extract_prefix(target["token"], word_bank)
        suffix = target["entry"].get("suffix")
        if prefix:
            correct = prefix
            meaning = PREFIX_MEANINGS.get(prefix)
            question_text = f"Which part means '{meaning}'?"
            choices = [prefix] + [form for form in PREFIX_FORM_BANK if form != prefix]
            explanation = f"In {target['token']}, {prefix} means '{meaning}'."
            morpheme_type = "prefix"
        else:
            if has_lexical_plural_ending(target["entry"], target["token"], suffix):
                return skip_question_payload(
                    skill,
                    pasuk_text,
                    "No word with a prefix or suffix found in this pasuk.",
                )
            correct = suffix
            meaning = SUFFIX_MEANINGS.get(suffix)
            question_text = f"Which part means '{meaning}'?"
            choices = suffix_form_choices(suffix)
            explanation = f"In {target['token']}, {suffix} means '{meaning}'."
            morpheme_type = "suffix"
        if len(unique(choices)) < 4:
            return skip_question_payload(
                skill,
                pasuk_text,
                "No clean affix-unit choices found in this pasuk.",
            )
        return grammar_choice_payload(
            target,
            question_text,
            correct,
            choices[:4],
            explanation,
            morpheme_type=morpheme_type,
            morpheme_form=correct,
        )

    def people_translation_choices(
        correct,
        correct_entry=None,
        question_type="subject_identification",
        key="people",
    ):
        distractors = filtered_translation_values(
            [
                entry
                for entry in word_bank_entries(word_bank, source_derived_only=True)
                if is_person_like_entry(entry)
            ],
            correct,
            correct_entry,
            question_type=question_type,
        )
        extra = (
            ["someone else", "the man", "they"]
            if question_type in {"subject_identification", "object_identification"}
            else []
        )
        if question_type == "object_identification":
            distractors = unique(
                normalize_role_translation(value)
                for value in distractors
                if normalize_role_translation(value) and normalize_role_translation(value) != correct
            )
        return build_parallel_choices(
            correct,
            distractors,
            f"{pasuk_text}|{skill}|{key}",
            extra=extra,
            token=(correct_entry or {}).get("word"),
        )

    def noun_translation_choices(
        correct,
        correct_entry=None,
        question_type="object_identification",
        key="nouns",
    ):
        distractors = filtered_translation_values(
            [
                entry
                for entry in word_bank_entries(word_bank, source_derived_only=True)
                if entry_type(entry) == "noun" and not is_person_like_entry(entry)
            ],
            correct,
            correct_entry,
            question_type=question_type,
        )
        if question_type == "object_identification":
            distractors = unique(
                normalize_role_translation(value)
                for value in distractors
                if normalize_role_translation(value) and normalize_role_translation(value) != correct
            )
        return build_parallel_choices(
            correct,
            distractors,
            f"{pasuk_text}|{skill}|{key}",
            extra=["something else"],
            token=(correct_entry or {}).get("word"),
        )

    def phrase_parts():
        option = choose_phrase_option(
            quiz_ready_phrase_options(analyzed),
            recent_phrases=asked_set,
        )
        if not option:
            return None, None, []
        return option["phrase"], option["correct"], option["candidates"]

    if skill == "shoresh":
        target = choose_validated_target(
            "shoresh",
            lambda entry, _token: entry_type(entry) == "verb" and bool(entry.get("shoresh")),
        )
        if target is None:
            return skip_question_payload(skill, pasuk_text, "No supported shoresh target found in this pasuk.")
        correct = target["entry"].get("shoresh", target["token"])
        if mode == "selection":
            return finish(validated_question_payload(
                "shoresh",
                target,
                f"Which word has shoresh {correct}?",
                target["token"],
                pasuk_word_choices(target["token"]),
                f"{target['token']} has shoresh {correct}.",
            ))
        choices = shoresh_distractors(correct, word_bank)
        return validated_question_payload(
            "shoresh",
            target,
            prompt(
                f"What is the shoresh of {target['token']}?",
                f"What is the shoresh of {target['token']}?",
                "",
            ),
            correct,
            choices,
            f"The shoresh of {target['token']} is {correct}.",
        )

    if skill == "prefix":
        if mode == "selection":
            recent_prefixes_window = list(recent_prefixes or [])[-5:]
            prefix_pool = structured_word_bank_items(
                lambda entry, token: is_prefix_candidate(entry, token, word_bank),
                word_bank=word_bank,
                pasuk_text=pasuk_text,
                progress=progress,
            )
            if not prefix_pool:
                prefix_pool = analyzed
            candidates = [
                prepare_candidate_item(item, add_prefix=True, add_suffix=True)
                for item in prefix_pool
                if is_prefix_candidate(item["entry"], item["token"], word_bank)
                and validate_question_candidate(
                    "prefix",
                    item["token"],
                    prepare_candidate_item(item, add_prefix=True, add_suffix=True)["entry"],
                )["valid"]
                and item["token"] not in asked_set
                and recent_prefixes_window.count(item["entry"].get("prefix") or extract_prefix(item["token"])) < 2
            ]
            fallback_candidates = [
                prepare_candidate_item(item, add_prefix=True, add_suffix=True)
                for item in prefix_pool
                if is_prefix_candidate(item["entry"], item["token"], word_bank)
                and validate_question_candidate(
                    "prefix",
                    item["token"],
                    prepare_candidate_item(item, add_prefix=True, add_suffix=True)["entry"],
                )["valid"]
                and recent_prefixes_window.count(item["entry"].get("prefix") or extract_prefix(item["token"])) < 2
            ]
            pool = candidates or fallback_candidates
            if pool:
                selected_word = pick_word_for_skill(
                    [item["token"] for item in pool],
                    "prefix",
                    progress,
                )
                target = next((item for item in pool if item["token"] == selected_word), pool[0])
                target.setdefault(
                    "source_pasuk",
                    find_pasuk_for_word(
                        target["token"],
                        fallback=pasuk_text,
                        progress=progress,
                    ),
                )
                remember_selected_word(progress, target["token"], target["entry"])
            else:
                target = None
            if target is None:
                raise ValueError("No usable prefixed word found in this pasuk.")
            apply_prefix_metadata(target["token"], target["entry"], word_bank)
            prefix = extract_prefix(target["token"], word_bank)
            correct = PREFIX_MEANINGS.get(prefix, "")
            return finish(validated_question_payload(
                "prefix",
                target,
                f"Which word contains a prefix meaning \"{correct}\"?",
                target["token"],
                pasuk_word_choices(target["token"]),
                f"{target['token']} contains the prefix {prefix}, meaning '{correct}'.",
                add_prefix=True,
                add_suffix=True,
            ))
        return build_prefix_level_question()

    if skill == "suffix":
        target = choose_validated_suffix_target()
        if target is None:
            raise ValueError("No suffixed word found in this pasuk.")
        suffix = target["entry"].get("suffix", "")
        correct = SUFFIX_MEANINGS.get(suffix, "")
        if mode == "selection":
            return finish(validated_question_payload(
                "suffix",
                target,
                f"Which word contains a suffix meaning \"{correct}\"?",
                target["token"],
                pasuk_word_choices(target["token"]),
                f"{target['token']} contains the suffix {suffix}, meaning '{correct}'.",
                add_prefix=True,
                add_suffix=True,
            ))
        return validated_question_payload(
            "suffix",
            target,
            prompt(
                f"What does the suffix {suffix} add?",
                f"What does the suffix {suffix} add?",
                "",
            ),
            correct,
            list(SUFFIX_MEANINGS.values()),
            f"In {target['token']}, the suffix {suffix} means '{correct}'.",
            add_prefix=True,
            add_suffix=True,
        )

    if skill in {"verb_tense", "identify_tense"}:
        target = choose_validated_target(
            "verb_tense",
            lambda entry, token: runtime_tense_label(entry, token) is not None,
        )
        if target is None:
            return skip_question_payload(skill, pasuk_text, "No confidently classified verb tense found in this pasuk.")
        correct = infer_tense(target["entry"], target["token"])
        if correct is None:
            return skip_question_payload(skill, pasuk_text, "No confidently classified verb tense found in this pasuk.")
        tense_details = tense_form_details(correct, target["token"])
        display_phrase = tense_details.get("display_phrase") or tense_form_phrase(correct)
        fair_choices = fair_tense_choice_codes(correct)
        if fair_choices is None:
            return skip_question_payload(
                skill,
                pasuk_text,
                "No fair taught-label verb tense bank is available for this pasuk.",
            )
        if mode == "selection":
            prompt_text = (
                "Which word shows the 'to do' form?"
                if tense_details.get("displayed_label") == "to do form"
                else f"Which word shows {display_phrase}?"
            )
            return finish(validated_question_payload(
                "verb_tense",
                target,
                prompt_text,
                target["token"],
                pasuk_word_choices(target["token"]),
                tense_question_explanation(target, correct),
                tense_display_phrase=display_phrase,
                base_conjugation=tense_details.get("base_conjugation"),
                vav_prefix_type=tense_details.get("vav_prefix_type"),
                accepted_answer_aliases=tense_details.get("accepted_answer_aliases"),
            ))
        return validated_question_payload(
            "verb_tense",
            target,
            prompt(
                "What form is shown?",
                "What form is shown?",
                "",
            ),
            correct,
            fair_choices,
            tense_question_explanation(target, correct),
            tense_display_phrase=display_phrase,
            base_conjugation=tense_details.get("base_conjugation"),
            vav_prefix_type=tense_details.get("vav_prefix_type"),
            accepted_answer_aliases=tense_details.get("accepted_answer_aliases"),
        )

    if skill == "part_of_speech":
        target = choose_target(
            lambda entry, token: part_of_speech_target_supported(entry, token),
        )
        if target is None:
            return skip_question_payload(skill, pasuk_text, "No noun or verb target found in this pasuk.")
        correct = entry_type(target["entry"])
        student_correct = student_part_of_speech_label(correct)
        choices = cohort_safe_part_of_speech_choices(correct)
        if not student_correct or choices is None:
            return skip_question_payload(skill, pasuk_text, "No cohort-safe word-kind target found in this pasuk.")
        word_gloss = usable_translation(target["entry"], target["token"])
        explanation = (
            f"{target['token']} means '{word_gloss}', so here it is {part_of_speech_with_article(student_correct)}."
            if word_gloss
            else f"{target['token']} is {part_of_speech_with_article(student_correct)}."
        )
        if mode == "selection":
            return finish(skill_question_payload(
                skill,
                target,
                f"Which word is {part_of_speech_with_article(student_correct)}?",
                pasuk_word_choices(target["token"]),
                target["token"],
                explanation,
            ))
        return skill_question_payload(
            skill,
            target,
            prompt(
                f"What kind of word is {target['token']}?",
                f"What kind of word is {target['token']}?",
                "",
            ),
            choices,
            student_correct,
            explanation,
        )

    if skill == "subject_identification":
        override = subject_override_components(pasuk_text)
        gold_skill = gold_skill_record_for_text(pasuk_text, "subject_identification")
        if gold_skill and gold_skill.get("status") == "suppressed" and override is None:
            return skip_question_payload(
                skill,
                pasuk_text,
                gold_skill.get("reason") or "No subject candidate is supported by this pasuk.",
                source="active scope gold suppression",
            )
        if override is not None:
            return skill_question_payload(
                skill,
                override["target"],
                override["question"],
                override["choices"],
                override["correct_answer"],
                override["explanation"],
                action_token=override["action_token"],
                role_focus=override["role_focus"],
                source="active scope override",
                analysis_source="active_scope_override",
                override_pasuk_id=override["pasuk_id"],
            )
        target = choose_target(
            lambda entry, _token: is_subject_candidate_entry(entry),
            lambda: get_subject(analyzed),
        )
        if target is None:
            return skip_question_payload(skill, pasuk_text, "No subject candidate is supported by this pasuk.")
        correct = usable_translation(target["entry"], target["token"])
        if correct is None:
            return skip_question_payload(skill, pasuk_text, "No usable subject translation is available for this pasuk.")
        action = get_action_anchor(analyzed, target)
        if action is None:
            return skip_question_payload(skill, pasuk_text, "No clear action anchor is available for this pasuk.")
        if mode == "selection":
            return finish(skill_question_payload(
                skill,
                target,
                f"Which word is doing the action in {action['token']}?",
                pasuk_word_choices(target["token"]),
                target["token"],
                f"In {action['token']}, {target['token']} is doing the action.",
                action_token=action["token"],
                role_focus="subject",
            ))
        try:
            choices = people_translation_choices(
                correct,
                target["entry"],
                question_type="subject_identification",
            )
        except ValueError:
            return skip_question_payload(
                skill,
                pasuk_text,
                "No quiz-ready subject choices are available for this pasuk.",
            )
        return skill_question_payload(
            skill,
            target,
            prompt(
                f"Who is doing the action in {action['token']}?",
                f"Who is doing the action in {action['token']}?",
                "",
            ),
            choices,
            correct,
            f"In {action['token']}, {target['token']} is doing the action.",
            action_token=action["token"],
            role_focus="subject",
        )

    if skill == "object_identification":
        override = object_override_components(pasuk_text)
        gold_skill = gold_skill_record_for_text(pasuk_text, "object_identification")
        if gold_skill and gold_skill.get("status") == "suppressed" and override is None:
            return skip_question_payload(
                skill,
                pasuk_text,
                gold_skill.get("reason") or "No supported object target found in this pasuk.",
                source="active scope gold suppression",
            )
        if override is not None:
            return skill_question_payload(
                skill,
                override["target"],
                override["question"],
                override["choices"],
                override["correct_answer"],
                override["explanation"],
                action_token=override["action_token"],
                role_focus=override["role_focus"],
                source="active scope override",
                analysis_source="active_scope_override",
                override_pasuk_id=override["pasuk_id"],
            )
        target = get_action_recipient(analyzed, word_bank) or get_direct_object(analyzed)
        if target is None:
            return skip_question_payload(skill, pasuk_text, "No supported object target found in this pasuk.")
        target.setdefault("source_pasuk", pasuk_text)
        remember_selected_word(progress, target["token"], target["entry"])
        action = get_action_anchor(analyzed, target)
        if action is None:
            return skip_question_payload(skill, pasuk_text, "No clear action anchor is available for this pasuk.")

        is_person_object = is_person_like_entry(target["entry"])
        correct = usable_translation(target["entry"], target["token"])
        if correct is None:
            return skip_question_payload(skill, pasuk_text, "No usable object translation is available for this pasuk.")
        correct = normalize_role_translation(correct)
        if is_person_object:
            try:
                choices = people_translation_choices(
                    correct,
                    target["entry"],
                    question_type="object_identification",
                    key="object_people",
                )
            except ValueError:
                return skip_question_payload(
                    skill,
                    pasuk_text,
                    "No quiz-ready object choices are available for this pasuk.",
                )
            question_text = f"Who receives the action in {action['token']}?"
            explanation = f"In {action['token']}, {target['token']} is the one receiving the action."
            role_focus = "recipient"
        else:
            if role_hint(target["entry"]) != "object_candidate":
                return skip_question_payload(
                    skill,
                    pasuk_text,
                    "No clearly supported direct object target found in this pasuk.",
                )
            try:
                choices = noun_translation_choices(
                    correct,
                    target["entry"],
                    question_type="object_identification",
                    key="object_nouns",
                )
            except ValueError:
                return skip_question_payload(
                    skill,
                    pasuk_text,
                    "No quiz-ready object choices are available for this pasuk.",
                )
            question_text = f"What receives the action in {action['token']}?"
            explanation = f"In {action['token']}, {target['token']} is what receives the action."
            role_focus = "direct_object"
        return skill_question_payload(
            skill,
            target,
            question_text,
            choices,
            correct,
            explanation,
            action_token=action["token"],
            role_focus=role_focus,
        )

    if skill == "preposition_meaning":
        target = choose_target(
            lambda entry, _token: entry_type(entry) == "prep"
            or (
                is_prefix_candidate(entry, _token, word_bank)
                and extract_prefix(_token, word_bank) in {"\u05d1", "\u05dc", "\u05de"}
            ),
        )
        if target is None:
            return skip_question_payload(skill, pasuk_text, "No supported preposition target found in this pasuk.")
        apply_prefix_metadata(target["token"], target["entry"], word_bank)
        prefix = extract_prefix(target["token"], word_bank) or target["entry"].get("prefix", "")
        correct = PREFIX_MEANINGS.get(prefix) or target["entry"].get("translation")
        display_word = prefix or target["token"]
        choices = clean_choices(correct, ["to", "from", "in", "on"])
        return skill_question_payload(
            skill,
            target,
            f"What does {display_word} mean?",
            choices,
            correct,
            f"{display_word} means '{correct}'.",
        )

    if skill == "phrase_translation":
        override = phrase_override_components(pasuk_text)
        if override and override.get("suppress"):
            return skip_question_payload(
                skill,
                pasuk_text,
                override["reason"],
                source="active scope override",
            )
        gold_skill = gold_skill_record_for_text(pasuk_text, "phrase_translation")
        if gold_skill and gold_skill.get("status") == "suppressed" and not override:
            return skip_question_payload(
                skill,
                pasuk_text,
                gold_skill.get("reason") or "No quiz-ready phrase target found in this pasuk.",
                source="active scope gold suppression",
            )
        if override:
            phrase = override["phrase"]
            correct = override["correct_answer"]
            candidates = [choice for choice in override["choices"] if choice != correct]
        else:
            phrase, correct, candidates = phrase_parts()
            if not phrase or not correct:
                return skip_question_payload(
                    skill,
                    pasuk_text,
                    "No quiz-ready phrase target found in this pasuk.",
                )
        if mode == "selection":
            phrase_tokens = phrase.split()
            distractors = []
            for index in range(len(analyzed) - 1):
                candidate = " ".join(item["token"] for item in analyzed[index:index + 2])
                if candidate != phrase:
                    distractors.append(candidate)
            choices = clean_choices(phrase, distractors)
            return finish(skill_question_payload(
                skill,
                {"token": phrase, "entry": {"translation": correct}, "source_pasuk": pasuk_text},
                "Which phrase has this meaning?",
                choices,
                phrase,
                f"{phrase} means '{correct}'.",
                source="active scope override" if override and phrase == override.get("phrase") else "generated skill question",
                analysis_source="active_scope_override" if override and phrase == override.get("phrase") else None,
                override_pasuk_id=override.get("pasuk_id") if override and phrase == override.get("phrase") else None,
            ))
        if override and phrase == override.get("phrase"):
            choices = override["choices"]
        else:
            try:
                choices = build_parallel_choices(
                    correct,
                    candidates,
                    f"{pasuk_text}|phrase_translation",
                    token=phrase,
                )
            except ValueError:
                if override:
                    choices = override["choices"]
                    phrase = override["phrase"]
                    correct = override["correct_answer"]
                else:
                    return skip_question_payload(
                        skill,
                        pasuk_text,
                        "No quiz-ready phrase target found in this pasuk.",
                    )
        return skill_question_payload(
            skill,
            {"token": phrase, "entry": {"translation": correct}, "source_pasuk": pasuk_text},
            prompt(
                "What does this phrase mean?",
                "What does this phrase mean?",
                "",
            ),
            choices,
            correct,
            (
                override["explanation"]
                if override and phrase == override.get("phrase")
                else f"{phrase} means '{correct}'."
            ),
            source="active scope override" if override and phrase == override.get("phrase") else "generated skill question",
            analysis_source="active_scope_override" if override and phrase == override.get("phrase") else None,
            override_pasuk_id=override.get("pasuk_id") if override and phrase == override.get("phrase") else None,
        )

    target = choose_target(
        lambda entry, token: standalone_translation_target(entry, token),
        lambda: get_translatable_word(analyzed),
    )
    if target is None:
        return skip_question_payload(skill, pasuk_text, "No usable translation target found in this pasuk.")
    correct = usable_translation(target["entry"], target["token"])
    if mode == "selection":
        question = finish(skill_question_payload(
            skill,
            target,
            f"Which Hebrew word means \"{correct}\"?",
            pasuk_word_choices(target["token"]),
            target["token"],
            f"{target['token']} means '{correct}'.",
        ))
        question["hide_pasuk"] = True
        question["hide_focus_word"] = True
        return question
    try:
        choices = same_group_translation_choices(target["entry"], correct)
    except ValueError:
        return skip_question_payload(
            skill,
            pasuk_text,
            "No quiz-ready translation choices found in this pasuk.",
        )
    return skill_question_payload(
        skill,
        target,
        prompt(
            f"What does {target['token']} mean?",
            f"What does {target['token']} mean?",
            "",
        ),
        choices,
        correct,
        f"{target['token']} means '{correct}'.",
    )


def get_subject(analyzed):
    return next(
        (
            item
            for item in analyzed
            if role_data(item).get("clause_role") == "subject"
        ),
        None,
    )


def get_source(analyzed):
    phrase = get_phrase_role(analyzed, "source")
    if phrase is None:
        return None
    return phrase.get("object")


def get_recipient(analyzed):
    return next(
        (
            item
            for item in analyzed
            if role_data(item).get("clause_role") == "recipient"
        ),
        None,
    )


def get_destination(analyzed):
    phrase = get_phrase_role(analyzed, "destination")
    if phrase is None:
        return None, None
    return phrase.get("marker"), phrase.get("object")


def get_direct_object(analyzed):
    return next(
        (
            item
            for item in analyzed
            if role_data(item).get("clause_role") == "direct_object"
        ),
        None,
    )


def get_phrase_role(analyzed, phrase_role):
    marker = next(
        (
            item
            for item in analyzed
            if role_data(item).get("clause_role") == "prep_marker"
            and role_data(item).get("phrase_role") == phrase_role
        ),
        None,
    )
    obj = next(
        (
            item
            for item in analyzed
            if role_data(item).get("phrase_role") == phrase_role
            and role_data(item).get("clause_role") in {"recipient", "prepositional_object"}
        ),
        None,
    )
    if obj is None:
        return None
    details = role_data(obj)
    span = details.get("phrase_span") or [analyzed.index(obj), analyzed.index(obj)]
    text = " ".join(analyzed[index]["token"] for index in range(span[0], span[1] + 1))
    return {
        "marker": marker,
        "object": obj,
        "span": span,
        "text": text,
        "phrase_role": phrase_role,
        "preposition_form": details.get("preposition_form"),
        "preposition_meaning": details.get("preposition_meaning"),
    }


def subject_override_components(pasuk_text):
    spec = active_scope_skill_override(pasuk_text, "subject_identification")
    if not spec or spec.get("suppress"):
        return None

    subject_spec = spec.get("subject") or {}
    action_token = spec.get("main_verb_token")
    surface = subject_spec.get("surface")
    translation = subject_spec.get("translation")
    if not action_token or not surface or not translation:
        return None

    record = active_pasuk_record_for_text(pasuk_text) or {}
    target = {
        "token": surface,
        "entry": override_target_entry(
            surface,
            translation,
            semantic_group=subject_spec.get("semantic_group", "person"),
            role_hint="subject_candidate",
            entity_type=subject_spec.get("entity_type", "person"),
        ),
        "source_pasuk": pasuk_text,
    }
    choices = build_parallel_choices(
        translation,
        override_distractors(SUBJECT_OVERRIDE_DISTRACTOR_POOL, translation),
        f"{pasuk_text}|subject_override",
        token=surface,
    )
    return {
        "pasuk_id": record.get("pasuk_id"),
        "target": target,
        "question": f"Who is doing the action in {action_token}?",
        "choices": choices,
        "correct_answer": translation,
        "explanation": f"In {action_token}, {surface} is doing the action.",
        "action_token": action_token,
        "role_focus": "subject",
    }


def object_override_components(pasuk_text):
    spec = active_scope_skill_override(pasuk_text, "object_identification")
    if not spec or spec.get("suppress"):
        return None

    action_token = spec.get("main_verb_token")
    if not action_token:
        return None

    record = active_pasuk_record_for_text(pasuk_text) or {}
    recipient_spec = spec.get("recipient")
    object_spec = spec.get("direct_object")

    if recipient_spec:
        surface = recipient_spec.get("surface")
        translation = recipient_spec.get("translation")
        if not surface or not translation:
            return None
        target = {
            "token": surface,
            "entry": override_target_entry(
                surface,
                translation,
                semantic_group=recipient_spec.get("semantic_group", "person"),
                role_hint="subject_candidate",
                entity_type=recipient_spec.get("entity_type", "person"),
            ),
            "source_pasuk": pasuk_text,
        }
        choices = build_parallel_choices(
            translation,
            override_distractors(RECIPIENT_OVERRIDE_DISTRACTOR_POOL, translation),
            f"{pasuk_text}|recipient_override",
            token=surface,
        )
        return {
            "pasuk_id": record.get("pasuk_id"),
            "target": target,
            "question": f"Who receives the action in {action_token}?",
            "choices": choices,
            "correct_answer": translation,
            "explanation": f"In {action_token}, {surface} is the one receiving the action.",
            "action_token": action_token,
            "role_focus": "recipient",
        }

    if not object_spec:
        return None

    surface = object_spec.get("surface")
    translation = object_spec.get("translation")
    if not surface or not translation:
        return None

    target = {
        "token": surface,
        "entry": override_target_entry(
            surface,
            translation,
            semantic_group=object_spec.get("semantic_group", "object"),
            role_hint="object_candidate",
            entity_type=object_spec.get("entity_type", "common_noun"),
        ),
        "source_pasuk": pasuk_text,
    }
    choices = build_parallel_choices(
        translation,
        override_distractors(OBJECT_OVERRIDE_DISTRACTOR_POOL, translation),
        f"{pasuk_text}|object_override",
        token=surface,
    )
    return {
        "pasuk_id": record.get("pasuk_id"),
        "target": target,
        "question": f"What receives the action in {action_token}?",
        "choices": choices,
        "correct_answer": translation,
        "explanation": f"In {action_token}, {surface} is what receives the action.",
        "action_token": action_token,
        "role_focus": "direct_object",
    }


def phrase_override_components(pasuk_text):
    spec = active_scope_skill_override(pasuk_text, "phrase_translation")
    if not spec:
        return None
    if spec.get("suppress"):
        return {
            "suppress": True,
            "reason": (spec.get("suppress") or {}).get("reason")
            or "No quiz-ready phrase target found in this pasuk.",
        }

    phrase_spec = spec.get("preferred_phrase") or {}
    surface = phrase_spec.get("surface")
    translation = phrase_spec.get("translation")
    distractors = phrase_spec.get("distractors") or []
    if not surface or not translation:
        return None

    record = active_pasuk_record_for_text(pasuk_text) or {}
    choices = build_parallel_choices(
        translation,
        distractors,
        f"{pasuk_text}|phrase_override",
        token=surface,
    )
    return {
        "pasuk_id": record.get("pasuk_id"),
        "phrase": surface,
        "question": "What does this phrase mean?",
        "choices": choices,
        "correct_answer": translation,
        "explanation": f"Here, {surface} is the curated quiz-ready phrase and means '{translation}'.",
    }


def is_action_anchor_candidate(item):
    if not item:
        return False
    entry = item["entry"]
    token = item["token"]
    if entity_type(entry) == "grammatical_particle":
        return False
    if entry_type(entry) in {"prep", "particle"}:
        return False
    if normalize_hebrew_key(token) in {"את", "ואת"}:
        return False
    if is_subject_candidate_entry(entry) or is_person_like_entry(entry):
        return False
    return True


def get_action_anchor(analyzed, target=None):
    return get_verb(analyzed)


def get_action_recipient(analyzed, word_bank=None):
    return get_recipient(analyzed)


def get_prefixed_or_suffixed(analyzed, word_bank=None):
    target = (
        find_first(analyzed, lambda entry, token: is_prefix_candidate(entry, token) and entry.get("suffix"))
        or find_first(
            analyzed,
            lambda entry, token: (is_prefix_candidate(entry, token, word_bank) or is_suffix_candidate(entry, token, word_bank))
            and entry_type(entry) != "verb",
        )
        or find_first(analyzed, lambda entry, token: is_prefix_candidate(entry, token, word_bank) or is_suffix_candidate(entry, token, word_bank))
    )
    return with_suffix_metadata(target, word_bank)


def build_translation_question(step, pasuk, analyzed, by_group, word_bank=None):
    target = first_ready(analyzed, "translation")
    if target is None:
        return skip_question_payload(
            "translation",
            pasuk,
            "No quiz-ready translation target found in this pasuk.",
            source="generated pasuk flow",
        )
    entry = target["entry"]
    correct = usable_translation(entry, target["token"])
    distractors = translation_distractors(
        correct,
        entry,
        by_group,
        word_bank,
        require_quality_count=3,
    )
    try:
        choices = build_parallel_choices(
            correct,
            distractors,
            f"{pasuk}|wm",
            token=target["token"],
        )
    except ValueError:
        return skip_question_payload(
            "translation",
            pasuk,
            "No quiz-ready translation choices found in this pasuk.",
            source="generated pasuk flow",
        )
    return make_question(
        step,
        "translation",
        "WM",
        "WM1",
        "word_meaning",
        target["token"],
        f"What does {target['token']} mean?",
        choices,
        correct,
        f"{target['token']} means '{correct}'.",
        2,
    )


def build_pr_question(step, pasuk, analyzed, word_bank=None):
    target = first_ready(analyzed, "prefix_suffix", word_bank) or get_prefixed_or_suffixed(analyzed, word_bank)
    if target is None:
        return skip_question_payload(
            "prefix_suffix",
            pasuk,
            "No quiz-ready prefix or suffix target found in this pasuk.",
            source="generated pasuk flow",
        )
    entry = target["entry"]
    apply_prefix_metadata(target["token"], entry, word_bank)
    prefix = extract_prefix(target["token"], word_bank) or entry.get("prefix", "")
    suffix = entry.get("suffix", "")
    prefix_meaning = PREFIX_MEANINGS.get(prefix, entry.get("prefix_meaning", ""))
    suffix_meaning = SUFFIX_MEANINGS.get(suffix, entry.get("suffix_meaning", ""))

    if prefix and prefix_meaning:
        correct = prefix_meaning
        partials = [item for item in prefix_meaning_choices(prefix) if item != correct]
        extra = [value for value in PREFIX_MEANINGS.values() if value != correct]
        micro_standard = "PR1"
        prompt = f"What does the prefix {prefix} add in {target['token']}?"
        explanation = f"In {target['token']}, the prefix {prefix} adds '{correct}'."
        morpheme_type = "prefix"
        morpheme_form = prefix
    elif suffix and suffix_meaning:
        correct = suffix_meaning
        partials = [value for value in SUFFIX_MEANINGS.values() if value != correct]
        extra = []
        micro_standard = "PR2"
        prompt = f"What does the suffix {suffix} add in {target['token']}?"
        explanation = f"In {target['token']}, the suffix {suffix} adds '{correct}'."
        morpheme_type = "suffix"
        morpheme_form = suffix
    else:
        raise ValueError("No quiz-ready prefix or suffix target found in this pasuk.")

    try:
        choices = build_parallel_choices(
            correct,
            partials,
            f"{pasuk}|pr",
            extra=extra,
            token=target["token"],
        )
    except ValueError:
        return skip_question_payload(
            "prefix_suffix",
            pasuk,
            "No quiz-ready morpheme choices found in this pasuk.",
            source="generated pasuk flow",
        )
    return make_question(
        step,
        "prefix_suffix",
        "PR",
        micro_standard,
        "prefix_suffix",
        target["token"],
        prompt,
        choices,
        correct,
        explanation,
        3,
        morpheme_type=morpheme_type,
        morpheme_form=morpheme_form,
    )


def build_phrase_question(step, pasuk, analyzed, recent_phrases=None):
    override = phrase_override_components(pasuk)
    if override and override.get("suppress"):
        return skip_question_payload(
            "phrase_meaning",
            pasuk,
            override["reason"],
            source="active scope override",
        )
    option = choose_phrase_option(
        quiz_ready_phrase_options(analyzed),
        recent_phrases=recent_phrases,
    )
    if not option and override:
        option = {
            "phrase": override["phrase"],
            "correct": override["correct_answer"],
            "candidates": [choice for choice in override["choices"] if choice != override["correct_answer"]],
        }
    if not option:
        return skip_question_payload(
            "phrase_meaning",
            pasuk,
            "No quiz-ready phrase target found in this pasuk.",
            source="generated pasuk flow",
        )
    phrase = option["phrase"]
    correct = option["correct"]
    if override and phrase == override.get("phrase"):
        choices = override["choices"]
    else:
        try:
            choices = build_parallel_choices(
                correct,
                option["candidates"],
                f"{pasuk}|phrase",
                token=phrase,
            )
        except ValueError:
            if override:
                phrase = override["phrase"]
                correct = override["correct_answer"]
                choices = override["choices"]
            else:
                return skip_question_payload(
                    "phrase_meaning",
                    pasuk,
                    "No quiz-ready phrase target found in this pasuk.",
                    source="generated pasuk flow",
                )
    return make_question(
        step,
        "phrase",
        "PS",
        "PS4",
        "phrase_meaning",
        phrase,
        "What does this phrase mean?",
        choices,
        correct,
        (
            override["explanation"]
            if override and phrase == override.get("phrase")
            else f"Here, {phrase} works together as one phrase and means '{correct}'."
        ),
        4,
        source="active scope override" if override and phrase == override.get("phrase") else "generated pasuk flow",
        analysis_source="active_scope_override" if override and phrase == override.get("phrase") else None,
        override_pasuk_id=override.get("pasuk_id") if override and phrase == override.get("phrase") else None,
    )


def build_subject_question(step, pasuk, analyzed, by_group, word_bank=None):
    override = subject_override_components(pasuk)
    subject = first_ready(analyzed, "subject_identification")
    if subject is None:
        if override is not None:
            return make_question(
                step,
                "subject_identification",
                "SS",
                "SS1",
                "subject_identification",
                override["target"]["token"],
                override["question"],
                override["choices"],
                override["correct_answer"],
                override["explanation"],
                4,
                action_token=override["action_token"],
                role_focus=override["role_focus"],
                source="active scope override",
                analysis_source="active_scope_override",
                override_pasuk_id=override["pasuk_id"],
            )
        return skip_question_payload(
            "subject_identification",
            pasuk,
            "No quiz-ready subject found in this pasuk.",
            source="generated pasuk flow",
        )
    correct = usable_translation(subject["entry"], subject["token"])
    if correct is None:
        if override is not None:
            return make_question(
                step,
                "subject_identification",
                "SS",
                "SS1",
                "subject_identification",
                override["target"]["token"],
                override["question"],
                override["choices"],
                override["correct_answer"],
                override["explanation"],
                4,
                action_token=override["action_token"],
                role_focus=override["role_focus"],
                source="active scope override",
                analysis_source="active_scope_override",
                override_pasuk_id=override["pasuk_id"],
            )
        return skip_question_payload(
            "subject_identification",
            pasuk,
            "No usable subject translation found in this pasuk.",
            source="generated pasuk flow",
        )
    action = get_action_anchor(analyzed, subject)
    if action is None:
        if override is not None:
            return make_question(
                step,
                "subject_identification",
                "SS",
                "SS1",
                "subject_identification",
                override["target"]["token"],
                override["question"],
                override["choices"],
                override["correct_answer"],
                override["explanation"],
                4,
                action_token=override["action_token"],
                role_focus=override["role_focus"],
                source="active scope override",
                analysis_source="active_scope_override",
                override_pasuk_id=override["pasuk_id"],
            )
        return skip_question_payload(
            "subject_identification",
            pasuk,
            "No clear action anchor is available for this subject question.",
            source="generated pasuk flow",
        )
    distractor_entries = [
        entry
        for entry in word_bank_entries(word_bank, source_derived_only=True)
        if is_person_like_entry(entry)
    ]
    distractors = filtered_translation_values(
        distractor_entries,
        correct,
        subject["entry"],
        question_type="subject_identification",
    )
    try:
        choices = build_parallel_choices(
            correct,
            distractors,
            f"{pasuk}|subject",
            token=subject["token"],
        )
    except ValueError:
        if override is not None:
            return make_question(
                step,
                "subject_identification",
                "SS",
                "SS1",
                "subject_identification",
                override["target"]["token"],
                override["question"],
                override["choices"],
                override["correct_answer"],
                override["explanation"],
                4,
                action_token=override["action_token"],
                role_focus=override["role_focus"],
                source="active scope override",
                analysis_source="active_scope_override",
                override_pasuk_id=override["pasuk_id"],
            )
        return skip_question_payload(
            "subject_identification",
            pasuk,
            "No quiz-ready subject choices found in this pasuk.",
            source="generated pasuk flow",
        )
    return make_question(
        step,
        "subject_identification",
        "SS",
        "SS1",
        "subject_identification",
        subject["token"],
        f"Who is doing the action in {action['token']}?",
        choices,
        correct,
        f"In {action['token']}, {subject['token']} is doing the action.",
        4,
        action_token=action["token"],
        role_focus="subject",
    )


def build_shoresh_question(step, pasuk, analyzed, word_bank=None):
    target = find_first(
        analyzed,
        lambda entry, token: validate_question_candidate("shoresh", token, entry)["valid"],
    )
    if target is None:
        return skip_question_payload(
            "shoresh",
            pasuk,
            "No quiz-ready shoresh target found in this pasuk.",
            source="generated pasuk flow",
        )
    correct = target["entry"].get("shoresh")
    distractors = shoresh_distractors(correct, word_bank)
    try:
        choices = build_parallel_choices(
            correct,
            distractors,
            f"{pasuk}|shoresh",
            token=target["token"],
        )
    except ValueError:
        return skip_question_payload(
            "shoresh",
            pasuk,
            "No quiz-ready shoresh choices found in this pasuk.",
            source="generated pasuk flow",
        )
    validation = validate_question_candidate(
        "shoresh",
        target["token"],
        target["entry"],
        correct_answer=correct,
        choices=choices,
    )
    if not validation["valid"]:
        return skip_question_payload(
            "shoresh",
            pasuk,
            format_validation_reason(target["token"], validation),
            source="generated pasuk flow",
            details=validation,
        )
    return make_question(
        step,
        "shoresh",
        "SR",
        "SR1",
        "shoresh",
        target["token"],
        f"What is the shoresh of {target['token']}?",
        choices,
        correct,
        f"The shoresh of {target['token']} is {correct}.",
        3,
    )


def build_tense_question(step, pasuk, analyzed):
    target = find_first(
        analyzed,
        lambda entry, token: validate_question_candidate("verb_tense", token, entry)["valid"],
    )
    if target is None:
        return skip_question_payload(
            "verb_tense",
            pasuk,
            "No quiz-ready verb tense target found in this pasuk.",
            source="generated pasuk flow",
        )
    correct = runtime_tense_label(target["entry"], target["token"])
    if correct is None:
        return skip_question_payload(
            "verb_tense",
            pasuk,
            "No runtime verb tense label found in this pasuk.",
            source="generated pasuk flow",
        )
    choices = fair_tense_choice_codes(correct)
    if choices is None:
        return skip_question_payload(
            "verb_tense",
            pasuk,
            "No fair taught-label verb tense bank is available for this pasuk.",
            source="generated pasuk flow",
        )
    validation = validate_question_candidate(
        "verb_tense",
        target["token"],
        target["entry"],
        correct_answer=correct,
        choices=choices,
    )
    if not validation["valid"]:
        return skip_question_payload(
            "verb_tense",
            pasuk,
            format_validation_reason(target["token"], validation),
            source="generated pasuk flow",
            details=validation,
        )
    tense_details = tense_form_details(correct, target["token"])
    return make_question(
        step,
        "verb_tense",
        "PR",
        "PR5",
        "verb_tense",
        target["token"],
        "What form is shown?",
        choices,
        correct,
        tense_question_explanation(target, correct),
        3,
        tense_display_phrase=tense_details.get("display_phrase"),
        base_conjugation=tense_details.get("base_conjugation"),
        vav_prefix_type=tense_details.get("vav_prefix_type"),
        accepted_answer_aliases=tense_details.get("accepted_answer_aliases"),
    )


def build_flow_question(step, pasuk, analyzed):
    source_phrase = get_phrase_role(analyzed, "source")
    destination_phrase = get_phrase_role(analyzed, "destination")
    recipient_phrase = get_phrase_role(analyzed, "recipient")
    source = source_phrase["object"] if source_phrase else None
    destination = destination_phrase["object"] if destination_phrase else None
    recipient = recipient_phrase["object"] if recipient_phrase else get_recipient(analyzed)
    direct_object = get_direct_object(analyzed)
    subject = get_subject(analyzed)
    verb = get_verb(analyzed)

    if verb is None or subject is None:
        return skip_question_payload(
            "flow",
            pasuk,
            "No role-resolved clause is available for this flow question.",
            source="generated pasuk flow",
        )

    if source_phrase and destination_phrase and source and destination:
        source_text = strip_relation(describe(source))
        destination_text = strip_relation(describe(destination))
        correct = f"{source_phrase['text']} must be read as the starting point before {destination_phrase['text']} can be read as the destination"
        partials = [
            f"{destination_phrase['text']} must be read as the starting point before {source_phrase['text']} can be read as the destination",
            f"{source_phrase['text']} gives possession, while {destination_phrase['text']} alone gives the full movement",
        ]
        clear = f"{subject['token']} must be read as the destination before {verb['token']} gives the action"
        explanation = "The flow depends on reading source and destination together."
        prompt = "What comes first?"
    elif recipient and direct_object:
        recipient_text = strip_relation(describe(recipient))
        recipient_label = (recipient_phrase or {"text": recipient["token"]})["text"]
        correct = f"{direct_object['token']} must be read as the object before {recipient_label} can mark the receiver"
        partials = [
            f"{recipient_label} must be read as the object before {direct_object['token']} can mark the receiver",
            f"{verb['token']} shows transfer, but {recipient_label} only shows possession and not receiver",
        ]
        clear = f"{subject['token']} must be read as the receiver before {direct_object['token']} gives the object"
        explanation = "The flow depends on distinguishing the object from the receiver."
        prompt = "Who gets the action?"
    else:
        correct = f"{verb['token']} must be read as the action before {subject['token']} can be understood as the performer"
        partials = [
            f"{subject['token']} must be read as the action before {verb['token']} can be understood as the performer",
            f"{verb['token']} gives the action, but {subject['token']} only gives a location",
        ]
        clear = f"{subject['token']} gives the receiver, and {verb['token']} gives the object"
        explanation = "The flow begins with the action and is anchored by the subject."
        prompt = "What is the action?"

    choices = build_choices(correct, partials, clear, f"{pasuk}|flow")
    return make_question(
        step,
        "flow",
        "SS",
        "SS5",
        "flow_dependency",
        pasuk,
        prompt,
        choices,
        correct,
        explanation,
        5,
    )


def build_substitution_question(step, pasuk, analyzed):
    source_phrase = get_phrase_role(analyzed, "source")
    recipient_phrase = get_phrase_role(analyzed, "recipient")
    destination_phrase = get_phrase_role(analyzed, "destination")
    source = source_phrase["object"] if source_phrase else None
    recipient = recipient_phrase["object"] if recipient_phrase else get_recipient(analyzed)
    destination = destination_phrase["object"] if destination_phrase else None

    if source:
        prompt_variant = "impossible"
        old = source_phrase["text"] if source_phrase else source["token"]
        replacement = (
            f"ב{source['token'][1:]}"
            if source["token"].startswith("מ")
            else f"ב{source['token']}"
        )
        correct = "movement away from that place would no longer be possible"
        partials = [
            "movement toward the destination would no longer be possible",
            "possession by the same person would no longer be possible",
        ]
        clear = "the source clue would turn into a location-inside clue"
    elif recipient:
        prompt_variant = "new_meaning"
        old = recipient_phrase["text"] if recipient_phrase else recipient["token"]
        replacement = (
            f"מ{recipient['token'][1:]}"
            if recipient["token"].startswith("ל")
            else f"מ{recipient['token']}"
        )
        correct = "movement away from that person would be introduced"
        partials = [
            "movement toward that person would become stronger",
            "possession by that person would become the main meaning",
        ]
        clear = "the receiver clue would become a source clue"
    elif destination_phrase and destination:
        prompt_variant = "breaks"
        old = destination_phrase["text"]
        replacement = "מן"
        correct = "the direction would change from toward to away from"
        partials = [
            "the same place would remain important, but it would no longer work as the destination",
            "the movement would still be present, but its direction would reverse",
        ]
        clear = "the destination clue would break because the new word marks source instead"
    else:
        prompt_variant = "change"
        verb = get_verb(analyzed)
        if verb is None:
            return skip_question_payload(
                "substitution",
                pasuk,
                "No role-resolved clause is available for this substitution question.",
                source="generated pasuk flow",
            )
        old = verb["token"]
        replacement = "וישב"
        correct = "the action would change while the subject could stay the same"
        partials = [
            "the same subject would remain, but movement would no longer be the best reading",
            "the action would stay active, but the direction clues would become weaker",
        ]
        clear = "the action clue would break because the replacement gives a different action"

    choices = build_choices(correct, partials, clear, f"{pasuk}|substitution")
    prompts = {
        "change": "What changes?",
        "impossible": "What no longer works?",
        "new_meaning": "What new meaning appears?",
        "breaks": "What changes?",
    }
    return make_question(
        step,
        "substitution",
        "CM",
        "CM1",
        "substitution",
        old,
        prompts[prompt_variant],
        choices,
        correct,
        "Changing one grammar clue changes how the phrase or sentence functions.",
        5,
    )


def build_reasoning_question(step, pasuk, analyzed):
    verb = get_verb(analyzed)
    subject = get_subject(analyzed)
    source_phrase = get_phrase_role(analyzed, "source")
    destination_phrase = get_phrase_role(analyzed, "destination")
    recipient_phrase = get_phrase_role(analyzed, "recipient")
    source = source_phrase["object"] if source_phrase else None
    recipient = recipient_phrase["object"] if recipient_phrase else get_recipient(analyzed)
    direct_object = get_direct_object(analyzed)
    destination = destination_phrase["object"] if destination_phrase else None

    if verb is None or subject is None:
        return skip_question_payload(
            "reasoning",
            pasuk,
            "No role-resolved clause is available for this reasoning question.",
            source="generated pasuk flow",
        )

    if source_phrase and destination_phrase and source and destination:
        correct = (
            f"{verb['token']} gives the action, {subject['token']} gives the subject, "
            f"{source_phrase['text']} gives the source, and {destination_phrase['text']} gives the destination"
        )
        partials = [
            f"{verb['token']} gives the action and {subject['token']} gives the subject, but the direction is only implied",
            f"{source_phrase['text']} gives the destination and {destination_phrase['text']} gives the starting point",
        ]
        clear = f"{verb['token']} means gave, and {destination['token']} is the object being given"
        prompt = "Choose the best answer."
    elif recipient and direct_object:
        recipient_label = (recipient_phrase or {"text": recipient["token"]})["text"]
        correct = (
            f"{verb['token']} gives the action, {subject['token']} gives the giver, "
            f"{direct_object['token']} gives the object, and {recipient_label} gives the receiver"
        )
        partials = [
            f"{verb['token']} gives the action and {subject['token']} gives the giver, but the receiver is not marked",
            f"{recipient_label} gives the object, and {direct_object['token']} gives the receiver",
        ]
        clear = f"{verb['token']} means went, and {recipient_label} gives the destination city"
        prompt = "Who gets the action?"
    else:
        correct = f"{verb['token']} gives the action, and {subject['token']} gives the subject"
        partials = [
            f"{subject['token']} gives the action, and {verb['token']} gives the subject",
            f"{verb['token']} gives the action, but the subject is not stated",
        ]
        clear = f"{subject['token']} is a place and {verb['token']} is a noun"
        prompt = "Choose the best answer."

    choices = build_choices(correct, partials, clear, f"{pasuk}|reasoning")
    return make_question(
        step,
        "reasoning",
        "CM",
        "CM1",
        "reasoning",
        pasuk,
        prompt,
        choices,
        correct,
        "The strongest answer accounts for the action, roles, and grammar clues together.",
        5,
    )


def generate_pasuk_flow(
    pasuk: str,
    asked_question_types=None,
    recent_phrases=None,
    analyzed_override=None,
    word_bank_override=None,
    by_group_override=None,
):
    if word_bank_override is None and by_group_override is None:
        word_bank, by_group = load_word_bank()
    else:
        word_bank = word_bank_override or {}
        by_group = by_group_override or {}
    analyzed = (
        prebuilt_analyzed_pasuk(analyzed_override)
        if analyzed_override is not None
        else analyze_pasuk(pasuk, word_bank)
    )
    used_types = set(asked_question_types or [])

    builders = [
        ("word_meaning", lambda step: build_translation_question(step, pasuk, analyzed, by_group, word_bank)),
        ("prefix_suffix", lambda step: build_pr_question(step, pasuk, analyzed, word_bank)),
        ("subject_identification", lambda step: build_subject_question(step, pasuk, analyzed, by_group, word_bank)),
        ("verb_tense", lambda step: build_tense_question(step, pasuk, analyzed)),
        ("shoresh", lambda step: build_shoresh_question(step, pasuk, analyzed, word_bank)),
        (
            "phrase_meaning",
            lambda step: build_phrase_question(
                step,
                pasuk,
                analyzed,
                recent_phrases=recent_phrases,
            ),
        ),
    ]
    active_builders = [item for item in builders if item[0] not in used_types]
    if len(active_builders) < 3:
        active_builders = builders
    questions = []
    errors = []
    skipped = []
    for kind, builder in active_builders:
        try:
            result = builder(len(questions) + 1)
        except ValueError as error:
            errors.append(f"{kind}: {error}")
            continue
        if is_skip_payload(result):
            skipped.append(result)
            errors.append(f"{kind}: {result.get('reason')}")
            continue
        questions.append(result)
        if len(questions) >= 4:
            break
    if len(questions) < 3 and active_builders is not builders:
        for kind, builder in builders:
            if kind in {question.get("question_type") for question in questions}:
                continue
            try:
                result = builder(len(questions) + 1)
            except ValueError as error:
                errors.append(f"{kind}: {error}")
                continue
            if is_skip_payload(result):
                skipped.append(result)
                errors.append(f"{kind}: {result.get('reason')}")
                continue
            questions.append(result)
            if len(questions) >= 3:
                break
    if len(questions) < 3:
        raise ValueError(
            "Could not build enough quiz-ready pasuk flow questions: "
            + "; ".join(errors)
        )
    questions = sorted(questions, key=lambda item: item.get("difficulty", 0))
    for index, question in enumerate(questions, 1):
        question["step"] = index
    flow = {
        "mode": "pasuk_flow",
        "pasuk": pasuk,
        "source": "generated",
        "questions": questions,
    }
    if skipped:
        flow["skipped"] = skipped
    validate_flow(flow)
    return flow


def summarize_pasuk(analyzed):
    verb = get_verb(analyzed)
    subject = get_subject(analyzed)
    source = get_source(analyzed)
    recipient = get_recipient(analyzed)
    direct_object = get_direct_object(analyzed)
    marker, destination = get_destination(analyzed)
    return {
        "verb": verb,
        "subject": subject,
        "source": source,
        "recipient": recipient,
        "direct_object": direct_object,
        "marker": marker,
        "destination": destination,
    }


def build_multi_sequence_question(step, pesukim, summaries):
    first = summaries[0]
    second = summaries[1]
    correct = f"first {first['verb']['token']} happens, then {second['verb']['token']} happens"
    partials = [
        f"first {second['verb']['token']} happens, then {first['verb']['token']} happens",
        f"both actions happen at the same time because both begin with ו",
    ]
    clear = "there is no action in either pasuk"
    choices = build_choices(correct, partials, clear, "multi|sequence")
    return make_question(
        step,
        "multi_pasuk_flow",
        "SS",
        "SS4",
        "multi_pasuk_sequence",
        " / ".join(pesukim),
        "What happens first?",
        choices,
        correct,
        "The order of the pesukim controls the sequence of actions.",
        4,
    )


def build_multi_dependency_question(step, pesukim, summaries):
    movement = next((item for item in summaries if item["source"] or item["destination"]), summaries[0])
    transfer = next((item for item in summaries if item["recipient"]), summaries[-1])

    correct = f"the movement phrase sets location or direction before the later action is understood"
    partials = [
        "the later action changes the earlier subject into an object",
        "the receiver phrase explains where the earlier movement began",
    ]
    clear = "the two pesukim are unrelated because they share no grammar"
    choices = build_choices(correct, partials, clear, "multi|dependency")
    return make_question(
        step,
        "multi_pasuk_flow",
        "CM",
        "CM1",
        "multi_pasuk_dependency",
        " / ".join(pesukim),
        "How are they connected?",
        choices,
        correct,
        "A multi-pasuk flow asks how one action prepares the next.",
        5,
    )


def build_multi_substitution_question(step, pesukim, summaries):
    target = summaries[0]["source"] or summaries[-1]["recipient"] or summaries[0]["verb"]
    old = target["token"]
    if old.startswith("מ"):
        replacement = f"ב{old[1:]}"
        correct = "the first pasuk would shift from leaving a place to being in a place"
    elif old.startswith("ל"):
        replacement = f"מ{old[1:]}"
        correct = "the phrase would shift from receiver/direction to movement away"
    else:
        replacement = "וישב"
        correct = "the action would shift and the later flow would no longer depend on the same movement"

    partials = [
        "only the spelling would change, but the flow would stay identical",
        "the subject would become the receiver in every pasuk",
    ]
    clear = "all words would become nouns"
    choices = build_choices(correct, partials, clear, "multi|substitution")
    return make_question(
        step,
        "multi_pasuk_flow",
        "CM",
        "CM1",
        "multi_pasuk_substitution",
        old,
        "What changes?",
        choices,
        correct,
        "A substitution can change how one pasuk connects to the next.",
        5,
    )


def generate_multi_pasuk_flow(pesukim):
    if len(pesukim) < 2 or len(pesukim) > 3:
        raise ValueError("Multi-pasuk flow requires 2-3 pesukim.")

    word_bank, _by_group = load_word_bank()
    analyzed_flows = [analyze_pasuk(pasuk, word_bank) for pasuk in pesukim]
    questions = [
        build_translation_question(1, pesukim[0], analyzed_flows[0], _by_group),
        build_phrase_question(2, pesukim[0], analyzed_flows[0]),
        build_subject_question(3, pesukim[0], analyzed_flows[0], _by_group, word_bank),
    ]
    flow = {
        "mode": "multi_pasuk_flow",
        "pasuk": " / ".join(pesukim),
        "source": "generated multi-pasuk",
        "questions": questions,
    }
    validate_flow(flow, allow_short=True)
    return flow


def validate_flow(flow, allow_short=False):
    questions = flow["questions"]
    texts = [item["question"] for item in questions]
    if len(texts) != len(set(texts)):
        raise ValueError("Duplicate questions found in pasuk flow.")
    if len(questions) < 3:
        raise ValueError("Pasuk flow must include at least 3 atomic questions.")
    difficulties = [item["difficulty"] for item in questions]
    if difficulties != sorted(difficulties):
        raise ValueError("Pasuk flow difficulty must build step-by-step.")
    for item in questions:
        if len(item["question"].split()) > 12:
            raise ValueError(f"Question is too long: {item['question']}")
        if len(item["choices"]) != 4:
            raise ValueError(f"Question does not have 4 choices: {item['question']}")
        if len(set(item["choices"])) != 4:
            raise ValueError(f"Question has duplicate choices: {item['question']}")
        if item["correct_answer"] not in item["choices"]:
            raise ValueError(f"Correct answer missing from choices: {item['question']}")


def write_examples(pesukim=None):
    """Write preview flow artifacts for local inspection.

    This is a developer helper, not the supported runtime path.
    """
    pesukim = pesukim or EXAMPLE_PESUKIM
    flows = [generate_pasuk_flow(pasuk) for pasuk in pesukim]
    flows.append(generate_multi_pasuk_flow(EXAMPLE_MULTI_PESUKIM))
    data = {"flows": flows}
    OUTPUT_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT_PATH} with {len(flows)} flows.")
    for flow in flows:
        print(f"- {flow['pasuk']}: {len(flow['questions'])} questions")


if __name__ == "__main__":
    write_examples()
