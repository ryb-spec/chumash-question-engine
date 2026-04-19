from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache


ADAPTIVE_STANDARD_IDS = ("WM", "SR", "PR", "CF", "PC", "PS", "SS", "CM")

STANDARD_LABELS = {
    "WM": "Understanding words",
    "SR": "Finding the root of a word",
    "PR": "How words are built",
    "PS": "How words are built",
    "SS": "Who is doing what",
    "CM": "Understanding meaning from context",
    "CF": "How the sentence works",
    "PC": "Reading short phrases",
}

MICRO_STANDARD_LABELS = {
    "WM1": "Match a Hebrew word to its meaning",
    "WM2": "Recognize the Hebrew word from English",
    "WM3": "Group related meanings",
    "WM4": "Tell close meanings apart",
    "WM5": "Understand abstract words",
    "PR1": "Recognize a prefix",
    "PR2": "Recognize an ending",
    "PR3": "Combine prefix and word",
    "PR4": "Combine word and ending",
    "PR5": "Read the whole word form",
    "PS1": "Find the subject in a phrase",
    "PS2": "Find the action in a phrase",
    "PS3": "Read a prefix inside a phrase",
    "PS4": "Understand a phrase unit",
    "PS5": "Put phrase clues together",
    "SS1": "Find who is doing the action",
    "SS2": "Find the main action",
    "SS3": "Identify each word's role",
    "SS4": "Follow the order of events",
    "SS5": "Explain how the sentence works",
    "CM1": "Use context to choose the meaning",
    "CF1": "Connect root and meaning",
    "CF2": "Connect prefix and meaning",
    "CF3": "Put root, prefix, and meaning together",
    "CF4": "Decode several clues at once",
    "CF5": "Explain a complex form",
}


@dataclass(frozen=True)
class SkillDefinition:
    id: str
    display_label: str
    standard: str
    micro_standard: str
    difficulty_tier: int
    prerequisites: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()


SKILL_CATALOG = (
    SkillDefinition(
        id="identify_prefix_meaning",
        display_label="How words are built",
        standard="PR",
        micro_standard="PR1",
        difficulty_tier=1,
        aliases=(
            "prefix_level_1_identify_prefix_meaning",
            "prefix_level_2_identify_prefix_meaning",
            "prefix_level_3_identify_prefix_meaning",
            "prefix_level_4_identify_prefix_meaning",
            "prefix_level_5_identify_prefix_meaning",
        ),
    ),
    SkillDefinition(
        id="identify_suffix_meaning",
        display_label="How words are built",
        standard="PR",
        micro_standard="PR2",
        difficulty_tier=1,
        prerequisites=("identify_prefix_meaning",),
    ),
    SkillDefinition(
        id="identify_pronoun_suffix",
        display_label="How words are built",
        standard="PR",
        micro_standard="PR2",
        difficulty_tier=1,
        prerequisites=("identify_suffix_meaning",),
    ),
    SkillDefinition(
        id="identify_verb_marker",
        display_label="How words are built",
        standard="PR",
        micro_standard="PR1",
        difficulty_tier=1,
        prerequisites=("identify_prefix_meaning",),
    ),
    SkillDefinition(
        id="segment_word_parts",
        display_label="How words are built",
        standard="PR",
        micro_standard="PR5",
        difficulty_tier=2,
        prerequisites=("identify_prefix_meaning", "identify_suffix_meaning"),
    ),
    SkillDefinition(
        id="identify_tense",
        display_label="How verbs are built",
        standard="PR",
        micro_standard="PR5",
        difficulty_tier=2,
        prerequisites=("identify_verb_marker",),
    ),
    SkillDefinition(
        id="identify_prefix_future",
        display_label="How verbs are built",
        standard="PR",
        micro_standard="PR1",
        difficulty_tier=2,
        prerequisites=("identify_tense",),
    ),
    SkillDefinition(
        id="identify_suffix_past",
        display_label="How verbs are built",
        standard="PR",
        micro_standard="PR2",
        difficulty_tier=3,
        prerequisites=("identify_tense", "identify_suffix_meaning"),
    ),
    SkillDefinition(
        id="identify_present_pattern",
        display_label="How verbs are built",
        standard="PR",
        micro_standard="PR5",
        difficulty_tier=3,
        prerequisites=("identify_tense",),
    ),
    SkillDefinition(
        id="convert_future_to_command",
        display_label="How verbs are built",
        standard="PR",
        micro_standard="PR5",
        difficulty_tier=4,
        prerequisites=("identify_prefix_future",),
    ),
    SkillDefinition(
        id="match_pronoun_to_verb",
        display_label="How verbs are built",
        standard="PR",
        micro_standard="PR5",
        difficulty_tier=3,
        prerequisites=("identify_tense", "identify_pronoun_suffix"),
    ),
    SkillDefinition(
        id="part_of_speech",
        display_label="Parts of speech",
        standard="PS",
        micro_standard="PS1",
        difficulty_tier=2,
        prerequisites=("translation",),
    ),
    SkillDefinition(
        id="shoresh",
        display_label="Finding the root",
        standard="SR",
        micro_standard="SR1",
        difficulty_tier=3,
        prerequisites=("part_of_speech",),
    ),
    SkillDefinition(
        id="prefix",
        display_label="Prefixes",
        standard="PR",
        micro_standard="PR1",
        difficulty_tier=3,
        prerequisites=("identify_prefix_meaning",),
    ),
    SkillDefinition(
        id="suffix",
        display_label="Suffixes",
        standard="PR",
        micro_standard="PR2",
        difficulty_tier=3,
        prerequisites=("identify_suffix_meaning",),
    ),
    SkillDefinition(
        id="translation",
        display_label="Word meaning",
        standard="WM",
        micro_standard="WM1",
        difficulty_tier=2,
        aliases=("word_meaning",),
    ),
    SkillDefinition(
        id="verb_tense",
        display_label="Verb tense",
        standard="PR",
        micro_standard="PR5",
        difficulty_tier=3,
        prerequisites=("identify_tense",),
        aliases=("identify_verb_tense",),
    ),
    SkillDefinition(
        id="subject_identification",
        display_label="Who is doing the action",
        standard="SS",
        micro_standard="SS1",
        difficulty_tier=4,
        prerequisites=("translation", "part_of_speech"),
    ),
    SkillDefinition(
        id="object_identification",
        display_label="What the action happens to",
        standard="SS",
        micro_standard="SS3",
        difficulty_tier=4,
        prerequisites=("subject_identification",),
    ),
    SkillDefinition(
        id="preposition_meaning",
        display_label="Small direction words",
        standard="PR",
        micro_standard="PR1",
        difficulty_tier=3,
        prerequisites=("identify_prefix_meaning", "translation"),
    ),
    SkillDefinition(
        id="phrase_translation",
        display_label="Phrase meaning",
        standard="PS",
        micro_standard="PS4",
        difficulty_tier=4,
        prerequisites=("translation",),
    ),
)

SKILL_IDS_IN_RUNTIME_ORDER = tuple(skill.id for skill in SKILL_CATALOG)


@lru_cache(maxsize=1)
def skill_catalog_by_id():
    return {skill.id: skill for skill in SKILL_CATALOG}


@lru_cache(maxsize=1)
def skill_alias_map():
    alias_map = {}
    for skill in SKILL_CATALOG:
        alias_map[skill.id] = skill.id
        for alias in skill.aliases:
            alias_map[alias] = skill.id
    return alias_map


def resolve_skill_id(skill_or_alias):
    if not skill_or_alias:
        return None
    return skill_alias_map().get(skill_or_alias)


def get_skill_definition(skill_or_alias):
    skill_id = resolve_skill_id(skill_or_alias)
    if skill_id is None:
        return None
    return skill_catalog_by_id()[skill_id]


def skill_ids_in_runtime_order():
    return list(SKILL_IDS_IN_RUNTIME_ORDER)


def adaptive_standard_ids():
    return list(ADAPTIVE_STANDARD_IDS)


def next_skill_id(current_skill, steps=1):
    skill_id = resolve_skill_id(current_skill)
    if not SKILL_IDS_IN_RUNTIME_ORDER:
        return skill_id or current_skill
    if skill_id is None:
        return SKILL_IDS_IN_RUNTIME_ORDER[0]
    index = SKILL_IDS_IN_RUNTIME_ORDER.index(skill_id)
    target_index = min(len(SKILL_IDS_IN_RUNTIME_ORDER) - 1, index + max(0, steps))
    return SKILL_IDS_IN_RUNTIME_ORDER[target_index]


def skill_display_label(skill_or_alias, default=None):
    skill = get_skill_definition(skill_or_alias)
    if skill is None:
        return default
    return skill.display_label


def skill_standard(skill_or_alias, default=None):
    skill = get_skill_definition(skill_or_alias)
    if skill is None:
        return default
    return skill.standard


def skill_micro_standard(skill_or_alias, default=None):
    skill = get_skill_definition(skill_or_alias)
    if skill is None:
        return default
    return skill.micro_standard


def skill_difficulty_tier(skill_or_alias, default=None):
    skill = get_skill_definition(skill_or_alias)
    if skill is None:
        return default
    return skill.difficulty_tier


def skill_prerequisites(skill_or_alias):
    skill = get_skill_definition(skill_or_alias)
    if skill is None:
        return []
    return list(skill.prerequisites)


def standard_display_label(standard_id, default=None):
    return STANDARD_LABELS.get(standard_id, default)


def micro_standard_display_label(micro_standard_id, default=None):
    return MICRO_STANDARD_LABELS.get(micro_standard_id, default)


def skill_metadata_record(skill_or_alias):
    skill = get_skill_definition(skill_or_alias)
    if skill is None:
        return None
    return {
        "id": skill.id,
        "display_label": skill.display_label,
        "aliases": list(skill.aliases),
        "difficulty_tier": skill.difficulty_tier,
        "prerequisites": list(skill.prerequisites),
        "standard": skill.standard,
        "micro_standard": skill.micro_standard,
    }
