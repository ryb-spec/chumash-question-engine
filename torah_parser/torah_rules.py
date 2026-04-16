"""Conservative Torah-specific parsing rules."""

import unicodedata

from .normalize import undotted_form


PREFIX_TRANSLATIONS = {
    "ו": ("conjunction", "and"),
    "ב": ("preposition_b", "in / with"),
    "ל": ("preposition_l", "to / for"),
    "כ": ("preposition_k", "like / as"),
    "מ": ("preposition_m", "from"),
    "ה": ("definite_article", "the"),
    "ש": ("relative", "that / which"),
}

PRONOMINAL_SUFFIX_TRANSLATIONS = {
    "י": "my",
    "ך": "your",
    "ו": "his",
    "ה": "her",
    "נו": "our",
    "כם": "your (m plural)",
    "כן": "your (f plural)",
    "ם": "their",
    "ן": "their",
    "יו": "his",
}


def _normalized_surface(word):
    return unicodedata.normalize("NFC", word or "")


def detect_vav_consecutive(word):
    surface = _normalized_surface(word)
    plain = undotted_form(surface)
    if len(plain) <= 3:
        return None
    if surface.startswith(("וַי", "וַת")):
        return "vav_consecutive_past"
    return None


def narrative_verb_features(word):
    tense = detect_vav_consecutive(word)
    if not tense:
        return {}
    return {
        "part_of_speech": "verb",
        "tense": tense,
        "prefixes": [
            {
                "form": "ו",
                "type": "verb_prefix_vav_consecutive",
                "translation": "and",
            }
        ],
    }


def common_possessive_suffix(word):
    plain = undotted_form(word)
    for suffix in ["כם", "כן", "נו", "יו", "ך", "ם", "ן", "ה", "ו", "י"]:
        if plain.endswith(suffix) and len(plain) > len(suffix) + 1:
            return {
                "form": suffix,
                "type": "pronominal_suffix",
                "translation": PRONOMINAL_SUFFIX_TRANSLATIONS[suffix],
            }
    return None


def apply_torah_overrides(candidate):
    surface = candidate.get("surface", "")
    narrative = narrative_verb_features(surface)
    if narrative:
        candidate.update({k: v for k, v in narrative.items() if v})
        candidate.setdefault("binyan", "qal")
        candidate.setdefault("confidence", "rule_based")
    return candidate
