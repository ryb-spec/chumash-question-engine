from __future__ import annotations

import json
from pathlib import Path

from .normalize import normalize_form


NORMALIZED_ALIAS_KEY = "__normalized_alias__"


def normalize_hebrew_key(text):
    if not isinstance(text, str):
        return text
    return normalize_form(text)


def old_word_type(part_of_speech):
    return {
        "proper_noun": "noun",
        "preposition": "prep",
    }.get(part_of_speech, part_of_speech or "unknown")


def first_present(*values):
    for value in values:
        if value is not None:
            return value
    return None


def first_morpheme_value(items, key, default=""):
    if not items:
        return default
    first = items[0] or {}
    return first.get(key, default)


def flat_analysis_copy(entry):
    analysis = dict(entry)
    analysis.pop("analyses", None)
    return analysis


def analysis_copies(entry):
    raw_analyses = entry.get("analyses") or []
    analyses = [flat_analysis_copy(analysis) for analysis in raw_analyses if isinstance(analysis, dict)]
    if analyses:
        return analyses
    return [flat_analysis_copy(entry)]


def _normalize_morpheme_items(raw_items, *, legacy_form="", legacy_translation=""):
    items = []
    for raw in raw_items or []:
        if isinstance(raw, dict):
            item = dict(raw)
            item.setdefault("form", "")
            item.setdefault("translation", "")
            items.append(item)
        elif isinstance(raw, str) and raw:
            items.append({"form": raw, "translation": ""})

    if items:
        return items

    if legacy_form:
        return [{"form": legacy_form, "translation": legacy_translation or ""}]
    return []


def add_legacy_word_bank_aliases(entry):
    entry.setdefault("Word", entry.get("word"))
    entry.setdefault("shoresh", entry.get("Shoresh"))
    entry.setdefault("Shoresh", entry.get("shoresh"))
    entry.setdefault("Prefix", entry.get("prefix", ""))
    entry.setdefault("Prefix Meaning", entry.get("prefix_meaning", ""))
    entry.setdefault("Suffix", entry.get("suffix", ""))
    entry.setdefault("Suffix Meaning", entry.get("suffix_meaning", ""))
    entry.setdefault("Translation", entry.get("translation"))
    entry.setdefault(
        "Context Translation",
        entry.get("context_translation")
        or entry.get("translation_context")
        or entry.get("translation"),
    )
    return entry


def adapt_word_analysis(surface, analysis, analysis_index=0, *, defaults=None):
    analysis = dict(analysis or {})
    defaults = dict(defaults or {})

    word = first_present(
        analysis.get("surface"),
        analysis.get("word"),
        analysis.get("Word"),
        surface,
    )
    translation_literal = first_present(
        analysis.get("translation_literal"),
        analysis.get("translation"),
        analysis.get("Translation"),
    )
    translation_context = first_present(
        analysis.get("translation_context"),
        analysis.get("context_translation"),
        analysis.get("Context Translation"),
    )

    prefixes = _normalize_morpheme_items(
        analysis.get("prefixes"),
        legacy_form=first_present(analysis.get("prefix"), analysis.get("Prefix"), ""),
        legacy_translation=first_present(
            analysis.get("prefix_meaning"),
            analysis.get("Prefix Meaning"),
            "",
        ),
    )
    suffixes = _normalize_morpheme_items(
        analysis.get("suffixes"),
        legacy_form=first_present(analysis.get("suffix"), analysis.get("Suffix"), ""),
        legacy_translation=first_present(
            analysis.get("suffix_meaning"),
            analysis.get("Suffix Meaning"),
            "",
        ),
    )

    entry = {
        "word": word,
        "Word": word,
        "surface": word,
        "menukad": first_present(analysis.get("menukad"), word),
        "normalized": first_present(analysis.get("normalized"), defaults.get("normalized"))
        or normalize_hebrew_key(word),
        "lemma": analysis.get("lemma"),
        "shoresh": first_present(analysis.get("shoresh"), analysis.get("Shoresh")),
        "Shoresh": first_present(analysis.get("shoresh"), analysis.get("Shoresh")),
        "type": old_word_type(analysis.get("part_of_speech")),
        "part_of_speech": analysis.get("part_of_speech"),
        "translation": translation_context or translation_literal or word,
        "translation_literal": translation_literal,
        "translation_context": translation_context,
        "context_translation": translation_context,
        "base_translation": translation_literal,
        "prefixes": prefixes,
        "suffixes": suffixes,
        "prefix": first_morpheme_value(prefixes, "form"),
        "prefix_meaning": first_morpheme_value(prefixes, "translation"),
        "suffix": first_morpheme_value(suffixes, "form"),
        "suffix_meaning": first_morpheme_value(suffixes, "translation"),
        "binyan": analysis.get("binyan"),
        "tense": analysis.get("tense"),
        "person": analysis.get("person"),
        "number": analysis.get("number"),
        "gender": analysis.get("gender"),
        "source_refs": list(analysis.get("source_refs") or []),
        "analysis_index": analysis_index,
    }

    for key, value in defaults.items():
        entry.setdefault(key, value)

    for key in (
        "group",
        "semantic_group",
        "role_hint",
        "entity_type",
        "confidence",
        "instructional_value",
        "base_word",
    ):
        value = analysis.get(key)
        if value is not None:
            entry[key] = value
        elif key in defaults:
            entry.setdefault(key, defaults[key])

    entry["analyses"] = [flat_analysis_copy(entry)]
    return add_legacy_word_bank_aliases(entry)


def adapt_word_bank_entry(entry, *, defaults=None):
    adapted = adapt_word_analysis(
        first_present(entry.get("surface"), entry.get("word"), entry.get("Word"), ""),
        entry,
        entry.get("analysis_index", 0),
        defaults=defaults,
    )

    raw_analyses = list(entry.get("analyses") or [])
    if raw_analyses:
        adapted["analyses"] = [
            flat_analysis_copy(
                adapt_word_analysis(
                    adapted["word"],
                    raw_analysis,
                    raw_analysis.get("analysis_index", index),
                    defaults=defaults,
                )
            )
            for index, raw_analysis in enumerate(raw_analyses)
        ]
    return add_legacy_word_bank_aliases(adapted)


def adapt_word_bank_data(data, *, defaults=None):
    words = (data or {}).get("words", [])
    if isinstance(words, list):
        return [adapt_word_bank_entry(entry, defaults=defaults) for entry in words]

    entries = []
    for surface, analyses in words.items():
        for index, analysis in enumerate(analyses or []):
            entries.append(adapt_word_analysis(surface, analysis, index, defaults=defaults))
    return entries


def load_word_bank_entries(path, *, defaults=None):
    file_path = Path(path)
    if not file_path.exists():
        return []
    data = json.loads(file_path.read_text(encoding="utf-8"))
    return adapt_word_bank_data(data, defaults=defaults)


def consolidate_surface_entries(entries):
    by_surface = {}
    ordered = []
    for raw_entry in entries:
        if not isinstance(raw_entry, dict):
            continue
        entry = dict(raw_entry)
        word = entry.get("word")
        if not word:
            continue

        analyses = analysis_copies(entry)
        if word not in by_surface:
            entry["analyses"] = analyses
            by_surface[word] = add_legacy_word_bank_aliases(entry)
            ordered.append(by_surface[word])
            continue

        existing = by_surface[word]
        existing.setdefault("analyses", analysis_copies(existing))
        existing["analyses"].extend(analyses)
    return ordered


def build_word_bank_metadata_index(entries):
    metadata = {}
    for entry in consolidate_surface_entries(entries):
        word = entry.get("word")
        if not word:
            continue
        metadata[word] = entry
        normalized = entry.get("normalized")
        if normalized:
            metadata.setdefault(normalized, metadata[word])
    return metadata


def merge_normalized_alias(by_word, normalized, entry):
    alias = by_word.get(normalized)
    if alias is None:
        alias = {
            NORMALIZED_ALIAS_KEY: True,
            "word": normalized,
            "Word": normalized,
            "surface": normalized,
            "menukad": normalized,
            "normalized": normalized,
            "type": "ambiguous",
            "part_of_speech": "ambiguous",
            "group": "unknown",
            "translation": normalized,
            "translation_context": normalized,
            "context_translation": normalized,
            "prefixes": [],
            "suffixes": [],
            "surface_forms": [],
            "entries": [],
            "analyses": [],
        }
        by_word[normalized] = alias
    elif not alias.get(NORMALIZED_ALIAS_KEY):
        alias.setdefault("normalized_aliases", [])
        alias["normalized_aliases"].append(entry)
        return

    surface = entry.get("word")
    if surface not in alias["surface_forms"]:
        alias["surface_forms"].append(surface)
        alias["entries"].append(entry)
    alias["analyses"].extend(entry.get("analyses", [flat_analysis_copy(entry)]))
    if len(alias["surface_forms"]) == 1:
        for key in (
            "translation",
            "translation_literal",
            "translation_context",
            "context_translation",
            "base_translation",
            "type",
            "part_of_speech",
            "lemma",
            "shoresh",
            "Shoresh",
            "binyan",
            "tense",
            "person",
            "number",
            "gender",
            "semantic_group",
            "role_hint",
            "entity_type",
            "prefixes",
            "suffixes",
            "prefix",
            "prefix_meaning",
            "suffix",
            "suffix_meaning",
        ):
            if key in entry:
                alias[key] = entry[key]


def merge_word_bank_entry(by_word, entry):
    word = entry.get("word")
    if not word:
        return

    if word in by_word:
        existing = by_word[word]
        existing.setdefault("analyses", [flat_analysis_copy(existing)])
        existing["analyses"].extend(entry.get("analyses", [flat_analysis_copy(entry)]))
        existing.update(entry)
    else:
        by_word[word] = entry

    normalized = entry.get("normalized")
    if normalized and normalized != word:
        merge_normalized_alias(by_word, normalized, by_word[word])


def build_word_bank_lookup(entries):
    by_word = {}
    for entry in consolidate_surface_entries(entries):
        merge_word_bank_entry(by_word, entry)
    return by_word


def resolve_word_bank_lookup(token, entry):
    if not entry.get(NORMALIZED_ALIAS_KEY):
        return dict(entry)
    entries = entry.get("entries") or []
    if len(entries) == 1:
        resolved = dict(entries[0])
        resolved["normalized_alias_entry"] = dict(entry)
        return resolved
    resolved = dict(entry)
    resolved["word"] = token
    resolved["Word"] = token
    resolved["surface"] = token
    resolved["menukad"] = token
    return resolved


def resolve_surface_for_normalized(word_bank, normalized_key):
    if not normalized_key:
        return None

    direct = word_bank.get(normalized_key)
    if isinstance(direct, dict) and not direct.get(NORMALIZED_ALIAS_KEY):
        return direct.get("word") or normalized_key
    if isinstance(direct, dict) and direct.get(NORMALIZED_ALIAS_KEY):
        entries = direct.get("entries") or []
        if len(entries) == 1:
            return entries[0].get("word")

    for entry in word_bank.values():
        if not isinstance(entry, dict) or entry.get(NORMALIZED_ALIAS_KEY):
            continue
        if entry.get("normalized") == normalized_key:
            return entry.get("word")
    return None
