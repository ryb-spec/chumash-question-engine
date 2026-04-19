from __future__ import annotations

from functools import lru_cache

from foundation_resources import load_foundation_resource
from torah_parser.word_bank_adapter import normalize_hebrew_key


_TIER_PRIORITY_METADATA = {
    "A": {
        "mastery_priority": "highest",
        "review_priority": "highest",
        "priority_rank": 4,
    },
    "B": {
        "mastery_priority": "high",
        "review_priority": "high",
        "priority_rank": 3,
    },
    "C": {
        "mastery_priority": "medium",
        "review_priority": "medium",
        "priority_rank": 2,
    },
    "D": {
        "mastery_priority": "contextual",
        "review_priority": "contextual",
        "priority_rank": 1,
    },
}


@lru_cache(maxsize=1)
def load_high_frequency_lexicon():
    return load_foundation_resource("high_frequency_lexicon")


def high_frequency_priority_tiers():
    return tuple(load_high_frequency_lexicon().get("priority_tiers", []))


def high_frequency_seed_entries():
    return tuple(load_high_frequency_lexicon().get("seed_entries", []))


def _lexicon_variants(term):
    if not isinstance(term, str):
        return []
    return [part.strip() for part in term.split("/") if part.strip()]


@lru_cache(maxsize=1)
def high_frequency_lexicon_lookup():
    lookup = {}
    for entry in high_frequency_seed_entries():
        variants = _lexicon_variants(entry.get("hebrew", ""))
        if not variants:
            continue
        for variant in variants:
            lookup.setdefault(variant, dict(entry))
            normalized_variant = normalize_hebrew_key(variant)
            lookup.setdefault(normalized_variant, dict(entry))
    return lookup


def get_high_frequency_lexicon_entry(term):
    if term is None:
        return None
    exact = high_frequency_lexicon_lookup().get(term)
    if exact is not None:
        return dict(exact)
    normalized = high_frequency_lexicon_lookup().get(normalize_hebrew_key(term))
    return dict(normalized) if normalized is not None else None


def lexicon_priority_profile(term):
    entry = get_high_frequency_lexicon_entry(term)
    if entry is None:
        return {
            "frequency_tier": None,
            "mastery_priority": "unknown",
            "review_priority": "unknown",
            "priority_rank": 0,
            "entry": None,
        }
    tier = entry.get("tier")
    priorities = dict(_TIER_PRIORITY_METADATA.get(tier, {}))
    return {
        "frequency_tier": tier,
        "mastery_priority": priorities.get("mastery_priority", "unknown"),
        "review_priority": priorities.get("review_priority", "unknown"),
        "priority_rank": priorities.get("priority_rank", 0),
        "entry": entry,
    }

