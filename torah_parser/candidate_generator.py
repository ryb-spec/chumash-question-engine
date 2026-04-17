"""Generate conservative candidate analyses for individual tokens."""

from copy import deepcopy

from .normalize import normalize_form, undotted_form
from .torah_rules import (
    PREFIX_TRANSLATIONS,
    apply_torah_overrides,
    common_possessive_suffix,
    detect_vav_consecutive,
)


VERB_OVERRIDES = {
    "ויאמר": {
        "lemma": "אמר",
        "shoresh": "אמר",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he said",
        "translation_context": "said",
    },
    "וירא": {
        "lemma": "ראה",
        "shoresh": "ראה",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he saw",
        "translation_context": "saw",
    },
    "ויקרא": {
        "lemma": "קרא",
        "shoresh": "קרא",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he called",
        "translation_context": "called",
    },
    "ויהי": {
        "lemma": "היה",
        "shoresh": "היה",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and it was",
        "translation_context": "and there was",
    },
    "ויעש": {
        "lemma": "עשה",
        "shoresh": "עשה",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he made",
        "translation_context": "made",
    },
    "ויבדל": {
        "lemma": "בדל",
        "shoresh": "בדל",
        "binyan": "hifil",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he separated",
        "translation_context": "separated",
    },
    "יקוו": {
        "lemma": "קוה",
        "shoresh": "קוה",
        "binyan": "nifal",
        "tense": "future_jussive",
        "person": "3",
        "number": "plural",
        "gender": "masculine",
        "translation_literal": "they shall gather",
        "translation_context": "let them be gathered",
    },
    "ותראה": {
        "lemma": "ראה",
        "shoresh": "ראה",
        "binyan": "nifal",
        "tense": "future_jussive",
        "person": "3",
        "number": "singular",
        "gender": "feminine",
        "translation_literal": "and it shall appear",
        "translation_context": "and let it appear",
    },
}


SURFACE_OVERRIDES = {
    "וִיהִי": {
        "lemma": "היה",
        "shoresh": "היה",
        "binyan": "qal",
        "tense": "future_jussive",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and it shall be",
        "translation_context": "and let it be",
    },
}

SEMANTIC_OVERRIDES = {
    "אלקים": {
        "semantic_group": "divine",
        "role_hint": "subject_candidate",
        "entity_type": "divine_name",
    },
    "את": {
        "semantic_group": "unknown",
        "role_hint": "object_candidate",
        "entity_type": "grammatical_particle",
    },
    "ואת": {
        "semantic_group": "unknown",
        "role_hint": "object_candidate",
        "entity_type": "grammatical_particle",
    },
    "כי": {
        "semantic_group": "abstract",
        "role_hint": "descriptor",
        "entity_type": "grammatical_particle",
    },
    "אשר": {
        "semantic_group": "abstract",
        "role_hint": "descriptor",
        "entity_type": "grammatical_particle",
    },
    "בין": {
        "semantic_group": "abstract",
        "role_hint": "location_candidate",
        "entity_type": "grammatical_particle",
    },
    "ובין": {
        "semantic_group": "abstract",
        "role_hint": "location_candidate",
        "entity_type": "grammatical_particle",
    },
    "אור": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "האור": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "חשך": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "וחשך": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "החשך": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "שמים": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "השמים": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "ארץ": {
        "semantic_group": "place",
        "role_hint": "location_candidate",
        "entity_type": "natural_feature",
    },
    "הארץ": {
        "semantic_group": "place",
        "role_hint": "location_candidate",
        "entity_type": "natural_feature",
    },
    "והארץ": {
        "semantic_group": "place",
        "role_hint": "location_candidate",
        "entity_type": "natural_feature",
    },
    "מים": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "המים": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "למים": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "רקיע": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "הרקיע": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "לרקיע": {
        "semantic_group": "cosmic_entity",
        "role_hint": "location_candidate",
        "entity_type": "natural_feature",
    },
    "יבשה": {
        "semantic_group": "place",
        "role_hint": "location_candidate",
        "entity_type": "natural_feature",
    },
    "היבשה": {
        "semantic_group": "place",
        "role_hint": "location_candidate",
        "entity_type": "natural_feature",
    },
    "ליבשה": {
        "semantic_group": "place",
        "role_hint": "location_candidate",
        "entity_type": "natural_feature",
    },
    "מקוה": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "ולמקוה": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "ימים": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "יום": {
        "semantic_group": "time",
        "role_hint": "time_candidate",
        "entity_type": "common_noun",
    },
    "לילה": {
        "semantic_group": "time",
        "role_hint": "time_candidate",
        "entity_type": "common_noun",
    },
    "ערב": {
        "semantic_group": "time",
        "role_hint": "time_candidate",
        "entity_type": "common_noun",
    },
    "בקר": {
        "semantic_group": "time",
        "role_hint": "time_candidate",
        "entity_type": "common_noun",
    },
    "תהו": {
        "semantic_group": "abstract",
        "role_hint": "descriptor",
        "entity_type": "common_noun",
    },
    "ובהו": {
        "semantic_group": "abstract",
        "role_hint": "descriptor",
        "entity_type": "common_noun",
    },
    "טוב": {
        "semantic_group": "abstract",
        "role_hint": "descriptor",
        "entity_type": "common_noun",
    },
    "אחד": {
        "semantic_group": "abstract",
        "role_hint": "descriptor",
        "entity_type": "common_noun",
    },
    "שני": {
        "semantic_group": "abstract",
        "role_hint": "descriptor",
        "entity_type": "common_noun",
    },
    "כן": {
        "semantic_group": "abstract",
        "role_hint": "descriptor",
        "entity_type": "unknown",
    },
    "מקום": {
        "semantic_group": "place",
        "role_hint": "location_candidate",
        "entity_type": "common_noun",
    },
}

FUTURE_PREFIX_SURFACES = (
    "\u05d9\u05b4",
    "\u05d9\u05b0",
    "\u05ea\u05b4",
    "\u05ea\u05b0",
    "\u05d0\u05b6",
    "\u05d0\u05b2",
    "\u05e0\u05b4",
    "\u05e0\u05b0",
)


def extract_inseparable_prefixes(word):
    plain = undotted_form(word)
    prefixes = []

    if plain.startswith("ו") and len(plain) > 2:
        prefix_type, translation = PREFIX_TRANSLATIONS["ו"]
        prefixes.append({"form": "ו", "type": prefix_type, "translation": translation})
        plain = plain[1:]

    if plain.startswith("ה") and len(plain) > 2:
        prefix_type, translation = PREFIX_TRANSLATIONS["ה"]
        prefixes.append({"form": "ה", "type": prefix_type, "translation": translation})
    elif plain[:1] in {"ב", "ל", "כ", "מ", "ש"} and len(plain) > 3:
        form = plain[0]
        prefix_type, translation = PREFIX_TRANSLATIONS[form]
        prefixes.append({"form": form, "type": prefix_type, "translation": translation})

    return prefixes


def extract_prefix(word, word_bank=None):
    features = verb_features(word)
    if features:
        for prefix in features.get("prefixes", []):
            form = prefix.get("form")
            if form in PREFIX_TRANSLATIONS:
                return form

    for prefix in extract_inseparable_prefixes(word):
        form = prefix.get("form")
        if form == "ש":
            continue
        if word_bank is not None and not prefix_has_known_base(word, form, word_bank):
            continue
        if form in PREFIX_TRANSLATIONS:
            return form

    return None


def verb_prefixes(word, tense):
    plain = undotted_form(word)
    prefixes = []
    if tense == "vav_consecutive_past":
        return [
            {
                "form": "ו",
                "type": "verb_prefix_vav_consecutive",
                "translation": "and",
            }
        ]
    if plain.startswith("ו") and len(plain) > 2:
        prefix_type, translation = PREFIX_TRANSLATIONS["ו"]
        prefixes.append({"form": "ו", "type": prefix_type, "translation": translation})
        plain = plain[1:]
    if plain[:1] in {"י", "ת", "א", "נ"} and len(plain) >= 3:
        prefixes.append(
            {
                "form": plain[0],
                "type": "verb_prefix_future",
                "translation": "future / jussive marker",
            }
        )
    return prefixes


def extract_suffix(word):
    if detect_verb_tense(word):
        return None
    suffix = common_possessive_suffix(word)
    return suffix.get("form") if suffix else None


def _word_bank_contains(word_bank, surface):
    if not word_bank or not surface:
        return False
    if surface in word_bank:
        return True
    normalized = normalize_form(surface)
    if normalized in word_bank:
        return True
    for entry in word_bank.values():
        if not isinstance(entry, dict):
            continue
        if entry.get("normalized") == normalized:
            return True
    return False


def prefix_has_known_base(word, prefix, word_bank):
    if not prefix or not word_bank:
        return False
    normalized = normalize_form(word)
    if not normalized.startswith(prefix):
        return False
    base = normalized[len(prefix):]
    return _word_bank_contains(word_bank, base)


def suffix_has_known_base(word, suffix, word_bank):
    if not suffix or not word_bank:
        return False
    plain = undotted_form(word)
    if not plain.endswith(suffix):
        return False
    base = plain[:-len(suffix)]
    if _word_bank_contains(word_bank, base):
        return True
    prefix = extract_prefix(base, word_bank)
    if prefix and base.startswith(prefix):
        return _word_bank_contains(word_bank, base[len(prefix):])
    return False


def apply_prefix_metadata(word, entry, word_bank=None):
    prefix = extract_prefix(word, word_bank)
    if not prefix:
        entry["prefix"] = ""
        entry["prefix_meaning"] = ""
        return entry

    prefix_type, translation = PREFIX_TRANSLATIONS[prefix]
    if word_bank is not None and not prefix_has_known_base(word, prefix, word_bank) and prefix != "\u05d5":
        entry["prefix"] = ""
        entry["prefix_meaning"] = ""
        return entry

    entry["prefix"] = prefix
    entry["prefix_meaning"] = translation
    entry.setdefault("prefixes", [])
    if not any(item.get("form") == prefix for item in entry["prefixes"]):
        entry["prefixes"] = [{"form": prefix, "type": prefix_type, "translation": translation}] + list(entry["prefixes"])
    return entry


def apply_suffix_metadata(word, entry, word_bank=None):
    suffix = entry.get("suffix") or extract_suffix(word)
    if not suffix:
        entry.setdefault("suffix", "")
        entry.setdefault("suffix_meaning", "")
        return entry
    if word_bank is not None and not suffix_has_known_base(word, suffix, word_bank):
        return entry

    translation = common_possessive_suffix(word) or {}
    entry["suffix"] = suffix
    entry["suffix_meaning"] = translation.get("translation", entry.get("suffix_meaning", ""))
    entry.setdefault("suffixes", [])
    if not any(item.get("form") == suffix for item in entry["suffixes"]):
        entry["suffixes"] = list(entry["suffixes"]) + [{
            "form": suffix,
            "type": "pronominal_suffix",
            "translation": entry["suffix_meaning"],
        }]
    return entry


def detect_verb_tense(word):
    normalized = normalize_form(word)
    if word in SURFACE_OVERRIDES:
        return SURFACE_OVERRIDES[word]["tense"]
    if normalized in VERB_OVERRIDES:
        return VERB_OVERRIDES[normalized]["tense"]
    surface = word or ""
    plain = undotted_form(word)
    consecutive = detect_vav_consecutive(word)
    if consecutive:
        return consecutive
    if plain.startswith("ו") and len(plain) > 3:
        plain = plain[1:]
    if plain.endswith(("תי", "תם", "תן", "נו")) and len(plain) > 4:
        return "past"
    if plain.endswith("ת") and len(plain) > 4:
        return "past"
    if (
        plain.startswith(("י", "ת", "א", "נ"))
        and len(plain) >= 4
        and surface.startswith(FUTURE_PREFIX_SURFACES)
    ):
        return "future"
    return None


def verb_features(word):
    normalized = normalize_form(word)
    features = dict(VERB_OVERRIDES.get(normalized, {}))
    features.update(SURFACE_OVERRIDES.get(word, {}))
    tense = features.get("tense") or detect_verb_tense(word)
    if not tense:
        return None
    return {
        "lemma": features.get("lemma", normalized),
        "shoresh": features.get("shoresh"),
        "part_of_speech": "verb",
        "binyan": features.get("binyan", "qal"),
        "tense": tense,
        "person": features.get("person"),
        "number": features.get("number"),
        "gender": features.get("gender"),
        "prefixes": verb_prefixes(word, tense),
        "suffixes": [],
        "translation_literal": features.get("translation_literal", word),
        "translation_context": features.get("translation_context", word),
        "confidence": "rule_based",
        "semantic_group": "action",
        "role_hint": "unknown",
        "entity_type": "verb",
    }


def semantic_features(token, part_of_speech):
    normalized = normalize_form(token)
    if part_of_speech == "verb":
        return {
            "semantic_group": "action",
            "role_hint": "unknown",
            "entity_type": "verb",
        }
    return dict(
        SEMANTIC_OVERRIDES.get(
            normalized,
            {
                "semantic_group": "unknown",
                "role_hint": "unknown",
                "entity_type": "unknown",
            },
        )
    )


def likely_part_of_speech(word):
    tense = detect_verb_tense(word)
    if tense:
        return "verb"
    return "unknown"


def generate_candidate_analyses(token):
    normalized = normalize_form(token)
    features = verb_features(token)
    part_of_speech = features["part_of_speech"] if features else likely_part_of_speech(token)
    suffix = None if features else common_possessive_suffix(token)

    candidate = {
        "surface": token,
        "normalized": normalized,
        "lemma": normalized,
        "shoresh": None,
        "part_of_speech": part_of_speech,
        "binyan": "qal" if part_of_speech == "verb" else None,
        "tense": detect_verb_tense(token) if part_of_speech == "verb" else None,
        "person": None,
        "number": None,
        "gender": None,
        "semantic_group": "unknown",
        "role_hint": "unknown",
        "entity_type": "unknown",
        "prefixes": extract_inseparable_prefixes(token),
        "suffixes": [suffix] if suffix else [],
        "translation_literal": token,
        "translation_context": token,
        "confidence": "generated_candidate",
        "source_refs": [],
    }
    if features:
        candidate.update(features)
    candidate.update(semantic_features(token, candidate.get("part_of_speech")))
    apply_prefix_metadata(token, candidate)
    apply_suffix_metadata(token, candidate)
    primary = apply_torah_overrides(candidate)
    analyses = [primary]
    if primary.get("part_of_speech") == "verb":
        alternate = deepcopy(primary)
        alternate.update(
            {
                "lemma": normalized,
                "shoresh": None,
                "part_of_speech": "unknown",
                "binyan": None,
                "tense": None,
                "person": None,
                "number": None,
                "gender": None,
                "semantic_group": "unknown",
                "role_hint": "unknown",
                "entity_type": "unknown",
                "prefixes": extract_inseparable_prefixes(token),
                "suffixes": [],
                "translation_literal": token,
                "translation_context": token,
                "confidence": "generated_alternate",
            }
        )
        analyses.append(alternate)
    return analyses
