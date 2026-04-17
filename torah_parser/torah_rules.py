"""Conservative Torah-specific parsing rules."""

import unicodedata

from .normalize import undotted_form


PREFIX_TRANSLATIONS = {
    "\u05d5": ("conjunction", "and"),
    "\u05d1": ("preposition_b", "in / with"),
    "\u05dc": ("preposition_l", "to / for"),
    "\u05db": ("preposition_k", "like / as"),
    "\u05de": ("preposition_m", "from"),
    "\u05d4": ("definite_article", "the"),
    "\u05e9": ("relative", "that / which"),
}

PRONOMINAL_SUFFIX_TRANSLATIONS = {
    "\u05d9": "my",
    "\u05da": "your",
    "\u05d5": "his",
    "\u05d4": "her",
    "\u05e0\u05d5": "our",
    "\u05db\u05dd": "your (m plural)",
    "\u05db\u05df": "your (f plural)",
    "\u05dd": "their",
    "\u05df": "their",
    "\u05d9\u05d5": "his",
}


def _normalized_surface(word):
    return unicodedata.normalize("NFC", word or "")


def detect_vav_consecutive(word):
    surface = _normalized_surface(word)
    plain = undotted_form(surface)
    if len(plain) <= 3:
        return None
    if surface.startswith(("\u05d5\u05b7\u05d9", "\u05d5\u05b7\u05ea")) and plain[1:2] in {"\u05d9", "\u05ea"}:
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
                "form": "\u05d5",
                "type": "verb_prefix_vav_consecutive",
                "translation": "and",
            }
        ],
    }


def common_possessive_suffix(word):
    plain = undotted_form(word)
    if detect_vav_consecutive(word):
        return None
    if plain.startswith(("\u05d9", "\u05ea", "\u05d0", "\u05e0")) and len(plain) >= 4:
        return None
    for suffix in ["\u05db\u05dd", "\u05db\u05df", "\u05e0\u05d5", "\u05d9\u05d5", "\u05da", "\u05dd", "\u05df", "\u05d4", "\u05d5", "\u05d9"]:
        if len(suffix) == 1 and len(plain) <= len(suffix) + 2:
            continue
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
