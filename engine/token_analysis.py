"""Token analysis and word-bank loading helpers."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

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
from torah_parser.tokenize import tokenize_pasuk as parser_tokenize_pasuk
from torah_parser.word_bank_adapter import (
    NORMALIZED_ALIAS_KEY,
    adapt_word_analysis,
    adapt_word_bank_data,
    build_word_bank_lookup,
    normalize_hebrew_key,
    resolve_surface_for_normalized,
    resolve_word_bank_lookup,
)

from .constants import PREFIX_MEANINGS, SUFFIX_MEANINGS, WORD_BANK_PATH


WORD_BANK = []


@lru_cache(maxsize=1)
def load_word_bank():
    data = (
        json.loads(Path(WORD_BANK_PATH).read_text(encoding="utf-8"))
        if Path(WORD_BANK_PATH).exists()
        else {"words": []}
    )
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


def extract_prefix(word, word_bank=None):
    return parser_extract_prefix(word, word_bank)


def extract_suffix(word):
    return parser_extract_suffix(word)


def detect_verb_tense(word):
    return parser_detect_verb_tense(word)


def prefix_has_known_base(word, prefix, word_bank):
    return parser_prefix_has_known_base(word, prefix, word_bank)


def suffix_has_known_base(word, suffix, word_bank):
    return parser_suffix_has_known_base(word, suffix, word_bank)


def apply_prefix_metadata(word, entry, word_bank=None):
    return parser_apply_prefix_metadata(word, entry, word_bank)


def apply_suffix_metadata(word, entry, word_bank=None):
    return parser_apply_suffix_metadata(word, entry, word_bank)


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


def is_prefix_candidate(entry, token, word_bank=None):
    prefix = extract_prefix(token, word_bank)
    if not prefix:
        return False
    if entry.get("prefix") and entry.get("prefix") != prefix:
        return False
    if entry.get("type") != "verb" and word_bank is not None and not prefix_has_known_base(token, prefix, word_bank):
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


def with_suffix_metadata(item, word_bank=None):
    if item is None:
        return None

    entry = dict(item["entry"])
    apply_suffix_metadata(item["token"], entry, word_bank)
    updated = dict(item)
    updated["entry"] = entry
    return updated


def is_suffix_candidate(entry, token, word_bank=None):
    suffix = entry.get("suffix") or extract_suffix(token)
    if not suffix:
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
                entry.setdefault("base_word", possible_base or token)
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
    return [item for item in items if item is not None]


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
    return items


def analyze_pasuk(pasuk, word_bank=None):
    if word_bank is None:
        return [analyze_word(word) for word in tokenize_pasuk(pasuk)]

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

    return analyzed


def strip_hebrew_marks(word):
    return "".join(
        char
        for char in word
        if not "\u0591" <= char <= "\u05c7"
    )


def is_verb(word):
    analyses = parser_generate_candidate_analyses(word)
    return any(
        analysis.get("part_of_speech") == "verb"
        and analysis.get("confidence") != "generated_alternate"
        for analysis in analyses
    )
