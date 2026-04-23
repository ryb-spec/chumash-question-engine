from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from corpus_metrics import (
    bundle_word_bank_lookup,
    load_staged_corpus_bundle,
    parsed_pasuk_to_analyzed,
)
from engine import flow_builder
from torah_parser.word_bank_adapter import normalize_hebrew_key

DEFAULT_STAGED_BUNDLE_DIR = BASE_DIR / "data" / "staged" / "parsed_bereishis_3_1_to_3_8_staged"
DEFAULT_OUTPUT_PATH = DEFAULT_STAGED_BUNDLE_DIR / "reviewed_questions.json"

STAGED_REVIEW_SPECS_BY_CORPUS = {
    "parsed_bereishis_3_1_to_3_8_staged": [
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_1", "target": "עָרוּם"},
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_2", "target": "נֹאכֵל"},
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_5", "target": "טוֹב"},
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_6", "target": "תַּאֲוָה"},
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_7", "target": "עֵירֻמִּם"},
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_8", "target": "קוֹל"},
        {"family": "shoresh", "skill": "shoresh", "pasuk_id": "bereishis_3_1", "target": "עָשָׂה"},
        {"family": "shoresh", "skill": "shoresh", "pasuk_id": "bereishis_3_2", "target": "וַתֹּאמֶר"},
        {"family": "shoresh", "skill": "shoresh", "pasuk_id": "bereishis_3_3", "target": "אָמַר"},
        {"family": "shoresh", "skill": "shoresh", "pasuk_id": "bereishis_3_6", "target": "וַתִּקַּח"},
        {"family": "shoresh", "skill": "shoresh", "pasuk_id": "bereishis_3_7", "target": "וַיִּתְפְּרוּ"},
        {"family": "shoresh", "skill": "shoresh", "pasuk_id": "bereishis_3_8", "target": "וַיִּתְחַבֵּא"},
        {"family": "tense", "skill": "identify_tense", "pasuk_id": "bereishis_3_1", "target": "הָיָה"},
        {"family": "tense", "skill": "identify_tense", "pasuk_id": "bereishis_3_2", "target": "נֹאכֵל"},
        {"family": "tense", "skill": "identify_tense", "pasuk_id": "bereishis_3_5", "target": "יֹדֵעַ"},
        {"family": "tense", "skill": "identify_tense", "pasuk_id": "bereishis_3_6", "target": "וַתֵּרֶא"},
        {"family": "tense", "skill": "identify_tense", "pasuk_id": "bereishis_3_8", "target": "מִתְהַלֵּךְ"},
        {"family": "affix", "skill": "identify_prefix_meaning", "pasuk_id": "bereishis_3_2", "target": "מִפְּרִי", "prefix_level": 2},
        {"family": "affix", "skill": "identify_prefix_meaning", "pasuk_id": "bereishis_3_3", "target": "בְּתוֹךְ", "prefix_level": 2},
        {"family": "affix", "skill": "identify_prefix_meaning", "pasuk_id": "bereishis_3_5", "target": "כֵּאלֹהִים", "prefix_level": 2},
        {"family": "affix", "skill": "identify_prefix_meaning", "pasuk_id": "bereishis_3_6", "target": "לְמַאֲכָל", "prefix_level": 2},
        {"family": "affix", "skill": "identify_prefix_meaning", "pasuk_id": "bereishis_3_8", "target": "בַּגָּן", "prefix_level": 2},
        {"family": "affix", "skill": "identify_pronoun_suffix", "pasuk_id": "bereishis_3_5", "target": "עֵינֵיכֶם"},
        {"family": "affix", "skill": "identify_pronoun_suffix", "pasuk_id": "bereishis_3_8", "target": "וְאִשְׁתּוֹ"},
    ],
    "parsed_bereishis_3_9_to_3_16_staged": [
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_9", "target": "וַיִּקְרָא"},
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_10", "target": "עֵירֹם"},
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_11", "target": "הִגִּיד"},
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_11", "target": "צִוִּיתִיךָ"},
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_12", "target": "נָתְנָה"},
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_13", "target": "הִשִּׁיאַנִי"},
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_14", "target": "אָרוּר"},
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_15", "target": "עָקֵב"},
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_16", "target": "יִמְשָׁל"},
        {"family": "shoresh", "skill": "shoresh", "pasuk_id": "bereishis_3_10", "target": "שָׁמַעְתִּי"},
        {"family": "shoresh", "skill": "shoresh", "pasuk_id": "bereishis_3_12", "target": "נָתְנָה"},
        {"family": "shoresh", "skill": "shoresh", "pasuk_id": "bereishis_3_14", "target": "עָשִׂיתָ"},
        {"family": "shoresh", "skill": "shoresh", "pasuk_id": "bereishis_3_15", "target": "אָשִׁית"},
        {"family": "shoresh", "skill": "shoresh", "pasuk_id": "bereishis_3_16", "target": "אַרְבֶּה"},
        {"family": "tense", "skill": "identify_tense", "pasuk_id": "bereishis_3_10", "target": "שָׁמַעְתִּי"},
        {"family": "tense", "skill": "identify_tense", "pasuk_id": "bereishis_3_11", "target": "אָכָלְתָּ"},
        {"family": "tense", "skill": "identify_tense", "pasuk_id": "bereishis_3_14", "target": "תֵלֵךְ"},
        {"family": "tense", "skill": "identify_tense", "pasuk_id": "bereishis_3_15", "target": "אָשִׁית"},
        {"family": "tense", "skill": "identify_tense", "pasuk_id": "bereishis_3_16", "target": "יִמְשָׁל"},
        {"family": "affix", "skill": "identify_prefix_meaning", "pasuk_id": "bereishis_3_9", "target": "לוֹ", "prefix_level": 2},
        {"family": "affix", "skill": "identify_prefix_meaning", "pasuk_id": "bereishis_3_10", "target": "בַּגָּן", "prefix_level": 2},
        {"family": "affix", "skill": "identify_prefix_meaning", "pasuk_id": "bereishis_3_14", "target": "מִכָּל", "prefix_level": 2},
        {"family": "affix", "skill": "identify_prefix_meaning", "pasuk_id": "bereishis_3_16", "target": "וְאֶל", "prefix_level": 2},
        {"family": "affix", "skill": "identify_pronoun_suffix", "pasuk_id": "bereishis_3_10", "target": "קֹלְךָ"},
        {"family": "affix", "skill": "identify_pronoun_suffix", "pasuk_id": "bereishis_3_14", "target": "גְּחֹנְךָ"},
        {"family": "affix", "skill": "identify_pronoun_suffix", "pasuk_id": "bereishis_3_15", "target": "זַרְעָהּ"},
        {"family": "affix", "skill": "identify_pronoun_suffix", "pasuk_id": "bereishis_3_16", "target": "תְּשׁוּקָתֵךְ"},
        {
            "family": "translation",
            "skill": "phrase_translation",
            "pasuk_id": "bereishis_3_9",
            "target": "וַיִּקְרָא יְהוָה אֱלֹהִים אֶל הָאָדָם",
            "correct_answer": "and the LORD God called to the man",
        },
        {
            "family": "translation",
            "skill": "phrase_translation",
            "pasuk_id": "bereishis_3_10",
            "target": "אֶת קֹלְךָ שָׁמַעְתִּי",
            "correct_answer": "I heard your voice",
        },
        {
            "family": "translation",
            "skill": "phrase_translation",
            "pasuk_id": "bereishis_3_11",
            "target": "מִי הִגִּיד לְךָ",
            "correct_answer": "who told you",
        },
        {
            "family": "translation",
            "skill": "phrase_translation",
            "pasuk_id": "bereishis_3_12",
            "target": "הִוא נָתְנָה לִּי",
            "correct_answer": "she gave me",
        },
        {
            "family": "translation",
            "skill": "phrase_translation",
            "pasuk_id": "bereishis_3_13",
            "target": "הַנָּחָשׁ הִשִּׁיאַנִי",
            "correct_answer": "the snake deceived me",
        },
        {
            "family": "translation",
            "skill": "phrase_translation",
            "pasuk_id": "bereishis_3_14",
            "target": "עַל גְּחֹנְךָ תֵלֵךְ",
            "correct_answer": "on your belly you shall go",
        },
        {
            "family": "translation",
            "skill": "phrase_translation",
            "pasuk_id": "bereishis_3_15",
            "target": "וְאֵיבָה אָשִׁית",
            "correct_answer": "and I will put enmity",
        },
        {
            "family": "translation",
            "skill": "phrase_translation",
            "pasuk_id": "bereishis_3_16",
            "target": "בְּעֶצֶב תֵּלְדִי בָנִים",
            "correct_answer": "in pain you will bear children",
        },
        {
            "family": "role",
            "skill": "subject_identification",
            "pasuk_id": "bereishis_3_9",
            "target": "יְהוָה אֱלֹהִים",
            "correct_answer": "the LORD God",
            "action_token": "וַיִּקְרָא",
            "role_focus": "subject",
            "entry_type": "proper_noun",
            "semantic_group": "divine",
            "entity_type": "divine_name",
            "group": "divine",
        },
        {
            "family": "role",
            "skill": "subject_identification",
            "pasuk_id": "bereishis_3_12",
            "target": "הָאִשָּׁה",
            "correct_answer": "the woman",
            "action_token": "נָתְנָה",
            "role_focus": "subject",
            "entry_type": "noun",
            "semantic_group": "person",
            "entity_type": "person",
            "group": "person",
        },
        {
            "family": "role",
            "skill": "subject_identification",
            "pasuk_id": "bereishis_3_13",
            "target": "הַנָּחָשׁ",
            "correct_answer": "the snake",
            "action_token": "הִשִּׁיאַנִי",
            "role_focus": "subject",
            "entry_type": "noun",
            "semantic_group": "animal",
            "entity_type": "animal",
            "group": "animal",
        },
        {
            "family": "role",
            "skill": "object_identification",
            "pasuk_id": "bereishis_3_9",
            "target": "הָאָדָם",
            "correct_answer": "the man",
            "action_token": "וַיִּקְרָא",
            "role_focus": "recipient",
            "answer_kind": "person",
            "entry_type": "noun",
            "semantic_group": "person",
            "entity_type": "person",
            "group": "person",
        },
        {
            "family": "role",
            "skill": "object_identification",
            "pasuk_id": "bereishis_3_10",
            "target": "קֹלְךָ",
            "correct_answer": "your voice",
            "action_token": "שָׁמַעְתִּי",
            "role_focus": "direct_object",
            "answer_kind": "thing",
            "entry_type": "noun",
            "semantic_group": "sound",
            "entity_type": "thing",
            "group": "sound",
        },
        {
            "family": "role",
            "skill": "object_identification",
            "pasuk_id": "bereishis_3_14",
            "target": "וְעָפָר",
            "correct_answer": "dust",
            "action_token": "תֹּאכַל",
            "role_focus": "direct_object",
            "answer_kind": "thing",
            "entry_type": "noun",
            "semantic_group": "substance",
            "entity_type": "thing",
            "group": "substance",
        },
        {
            "family": "role",
            "skill": "object_identification",
            "pasuk_id": "bereishis_3_15",
            "target": "וְאֵיבָה",
            "correct_answer": "enmity",
            "action_token": "אָשִׁית",
            "role_focus": "direct_object",
            "answer_kind": "thing",
            "entry_type": "noun",
            "semantic_group": "conflict",
            "entity_type": "thing",
            "group": "conflict",
        },
        {
            "family": "role",
            "skill": "object_identification",
            "pasuk_id": "bereishis_3_16",
            "target": "בָנִים",
            "correct_answer": "children",
            "action_token": "תֵּלְדִי",
            "role_focus": "direct_object",
            "answer_kind": "thing",
            "entry_type": "noun",
            "semantic_group": "person",
            "entity_type": "person_group",
            "group": "person",
        },
    ],
    "parsed_bereishis_3_17_to_3_24_staged": [
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_17", "target": "אֲרוּרָה"},
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_18", "target": "עֵשֶׂב"},
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_19", "target": "לֶחֶם"},
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_20", "target": "חָי"},
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_21", "target": "כָּתְנוֹת"},
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_22", "target": "יִשְׁלַח"},
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_23", "target": "לַעֲבֹד"},
        {"family": "translation", "skill": "translation", "pasuk_id": "bereishis_3_24", "target": "דֶּרֶךְ"},
        {"family": "shoresh", "skill": "shoresh", "pasuk_id": "bereishis_3_17", "target": "שָׁמַעְתָּ"},
        {"family": "shoresh", "skill": "shoresh", "pasuk_id": "bereishis_3_18", "target": "תַּצְמִיחַ"},
        {"family": "shoresh", "skill": "shoresh", "pasuk_id": "bereishis_3_19", "target": "תָּשׁוּב"},
        {"family": "shoresh", "skill": "shoresh", "pasuk_id": "bereishis_3_21", "target": "וַיַּלְבִּשֵׁם"},
        {"family": "shoresh", "skill": "shoresh", "pasuk_id": "bereishis_3_23", "target": "וַיְשַׁלְּחֵהוּ"},
        {"family": "shoresh", "skill": "shoresh", "pasuk_id": "bereishis_3_24", "target": "וַיְגָרֶשׁ"},
        {"family": "tense", "skill": "identify_tense", "pasuk_id": "bereishis_3_17", "target": "שָׁמַעְתָּ"},
        {"family": "tense", "skill": "identify_tense", "pasuk_id": "bereishis_3_18", "target": "תַּצְמִיחַ"},
        {"family": "tense", "skill": "identify_tense", "pasuk_id": "bereishis_3_19", "target": "תָּשׁוּב"},
        {"family": "tense", "skill": "identify_tense", "pasuk_id": "bereishis_3_20", "target": "הָיְתָה"},
        {"family": "tense", "skill": "identify_tense", "pasuk_id": "bereishis_3_21", "target": "וַיַּלְבִּשֵׁם"},
        {"family": "tense", "skill": "identify_tense", "pasuk_id": "bereishis_3_22", "target": "יִשְׁלַח"},
        {"family": "tense", "skill": "identify_tense", "pasuk_id": "bereishis_3_23", "target": "וַיְשַׁלְּחֵהוּ"},
        {"family": "tense", "skill": "identify_tense", "pasuk_id": "bereishis_3_24", "target": "וַיְגָרֶשׁ"},
        {"family": "affix", "skill": "identify_prefix_meaning", "pasuk_id": "bereishis_3_17", "target": "לְקוֹל", "prefix_level": 2},
        {"family": "affix", "skill": "identify_prefix_meaning", "pasuk_id": "bereishis_3_19", "target": "בְּזֵעַת", "prefix_level": 2},
        {"family": "affix", "skill": "identify_prefix_meaning", "pasuk_id": "bereishis_3_21", "target": "לְאָדָם", "prefix_level": 2},
        {"family": "affix", "skill": "identify_prefix_meaning", "pasuk_id": "bereishis_3_22", "target": "מֵעֵץ", "prefix_level": 2},
        {"family": "affix", "skill": "identify_prefix_meaning", "pasuk_id": "bereishis_3_23", "target": "מִגַּן", "prefix_level": 2},
        {"family": "affix", "skill": "identify_prefix_meaning", "pasuk_id": "bereishis_3_24", "target": "לְגַן", "prefix_level": 2},
        {"family": "affix", "skill": "identify_pronoun_suffix", "pasuk_id": "bereishis_3_17", "target": "אִשְׁתֶּךָ"},
        {"family": "affix", "skill": "identify_pronoun_suffix", "pasuk_id": "bereishis_3_19", "target": "אַפֶּיךָ"},
        {"family": "affix", "skill": "identify_pronoun_suffix", "pasuk_id": "bereishis_3_20", "target": "אִשְׁתּוֹ"},
        {"family": "affix", "skill": "identify_pronoun_suffix", "pasuk_id": "bereishis_3_22", "target": "יָדוֹ"},
        {
            "family": "translation",
            "skill": "phrase_translation",
            "pasuk_id": "bereishis_3_17",
            "target": "כִּי־שָׁמַעְתָּ לְקוֹל אִשְׁתֶּךָ",
            "correct_answer": "because you listened to the voice of your wife",
        },
        {
            "family": "translation",
            "skill": "phrase_translation",
            "pasuk_id": "bereishis_3_18",
            "target": "וְאָכַלְתָּ אֶת־עֵשֶׂב הַשָּׂדֶה",
            "correct_answer": "and you shall eat the grass of the field",
        },
        {
            "family": "translation",
            "skill": "phrase_translation",
            "pasuk_id": "bereishis_3_19",
            "target": "בְּזֵעַת אַפֶּיךָ",
            "correct_answer": "by the sweat of your brow",
        },
        {
            "family": "translation",
            "skill": "phrase_translation",
            "pasuk_id": "bereishis_3_20",
            "target": "אֵם כָּל־חָי",
            "correct_answer": "mother of all living",
        },
        {
            "family": "translation",
            "skill": "phrase_translation",
            "pasuk_id": "bereishis_3_21",
            "target": "כָּתְנוֹת עוֹר",
            "correct_answer": "garments of skin",
        },
        {
            "family": "translation",
            "skill": "phrase_translation",
            "pasuk_id": "bereishis_3_22",
            "target": "מֵעֵץ הַחַיִּים",
            "correct_answer": "from the tree of life",
        },
        {
            "family": "translation",
            "skill": "phrase_translation",
            "pasuk_id": "bereishis_3_23",
            "target": "מִגַּן־עֵדֶן",
            "correct_answer": "from the Garden of Eden",
        },
        {
            "family": "translation",
            "skill": "phrase_translation",
            "pasuk_id": "bereishis_3_24",
            "target": "לִשְׁמֹר אֶת־דֶּרֶךְ עֵץ הַחַיִּים",
            "correct_answer": "to guard the way to the tree of life",
        },
        {
            "family": "role",
            "skill": "subject_identification",
            "pasuk_id": "bereishis_3_20",
            "target": "הָאָדָם",
            "correct_answer": "the man",
            "action_token": "וַיִּקְרָא",
            "role_focus": "subject",
            "entry_type": "noun",
            "semantic_group": "person",
            "entity_type": "person",
            "group": "person",
        },
        {
            "family": "role",
            "skill": "subject_identification",
            "pasuk_id": "bereishis_3_20",
            "target": "הִוא",
            "correct_answer": "she",
            "action_token": "הָיְתָה",
            "role_focus": "subject",
            "entry_type": "pronoun",
            "semantic_group": "person",
            "entity_type": "pronoun",
            "group": "person",
        },
        {
            "family": "role",
            "skill": "subject_identification",
            "pasuk_id": "bereishis_3_21",
            "target": "יְהוָה אֱלֹהִים",
            "correct_answer": "the LORD God",
            "action_token": "וַיַּעַשׂ",
            "role_focus": "subject",
            "entry_type": "proper_noun",
            "semantic_group": "divine",
            "entity_type": "divine_name",
            "group": "divine",
        },
        {
            "family": "role",
            "skill": "subject_identification",
            "pasuk_id": "bereishis_3_22",
            "target": "הָאָדָם",
            "correct_answer": "the man",
            "action_token": "הָיָה",
            "role_focus": "subject",
            "entry_type": "noun",
            "semantic_group": "person",
            "entity_type": "person",
            "group": "person",
        },
        {
            "family": "role",
            "skill": "subject_identification",
            "pasuk_id": "bereishis_3_23",
            "target": "יְהוָה אֱלֹהִים",
            "correct_answer": "the LORD God",
            "action_token": "וַיְשַׁלְּחֵהוּ",
            "role_focus": "subject",
            "entry_type": "proper_noun",
            "semantic_group": "divine",
            "entity_type": "divine_name",
            "group": "divine",
        },
        {
            "family": "role",
            "skill": "object_identification",
            "pasuk_id": "bereishis_3_18",
            "target": "עֵשֶׂב הַשָּׂדֶה",
            "correct_answer": "the grass of the field",
            "action_token": "וְאָכַלְתָּ",
            "role_focus": "direct_object",
            "answer_kind": "thing",
            "entry_type": "noun",
            "semantic_group": "plant",
            "entity_type": "thing",
            "group": "plant",
        },
        {
            "family": "role",
            "skill": "object_identification",
            "pasuk_id": "bereishis_3_19",
            "target": "לֶחֶם",
            "correct_answer": "bread",
            "action_token": "תֹּאכַל",
            "role_focus": "direct_object",
            "answer_kind": "thing",
            "entry_type": "noun",
            "semantic_group": "food",
            "entity_type": "thing",
            "group": "food",
        },
        {
            "family": "role",
            "skill": "object_identification",
            "pasuk_id": "bereishis_3_21",
            "target": "כָּתְנוֹת עוֹר",
            "correct_answer": "garments of skin",
            "action_token": "וַיַּעַשׂ",
            "role_focus": "direct_object",
            "answer_kind": "thing",
            "entry_type": "noun",
            "semantic_group": "object",
            "entity_type": "thing",
            "group": "object",
        },
        {
            "family": "role",
            "skill": "object_identification",
            "pasuk_id": "bereishis_3_22",
            "target": "יָדוֹ",
            "correct_answer": "his hand",
            "action_token": "יִשְׁלַח",
            "role_focus": "direct_object",
            "answer_kind": "thing",
            "entry_type": "noun",
            "semantic_group": "body",
            "entity_type": "thing",
            "group": "body",
        },
        {
            "family": "role",
            "skill": "object_identification",
            "pasuk_id": "bereishis_3_24",
            "target": "הָאָדָם",
            "correct_answer": "the man",
            "action_token": "וַיְגָרֶשׁ",
            "role_focus": "direct_object",
            "answer_kind": "person",
            "entry_type": "noun",
            "semantic_group": "person",
            "entity_type": "person",
            "group": "person",
        },
    ],
}


def stable_fragment(value: str | None) -> str:
    text = str(value or "").strip().lower()
    cleaned = []
    for char in text:
        if char.isalnum():
            cleaned.append(char)
        else:
            cleaned.append("_")
    fragment = "".join(cleaned).strip("_")
    while "__" in fragment:
        fragment = fragment.replace("__", "_")
    return fragment or "unknown"


def write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def staged_target_entry(spec):
    correct = str(spec.get("correct_answer") or "").strip()
    return {
        "word": spec["target"],
        "translation": correct,
        "translation_literal": correct,
        "translation_context": correct,
        "part_of_speech": spec.get("entry_type", "noun"),
        "type": spec.get("entry_type", "noun"),
        "group": spec.get("group", "unknown"),
        "semantic_group": spec.get("semantic_group", "unknown"),
        "role_hint": spec.get("role_focus", "unknown"),
        "entity_type": spec.get("entity_type", "unknown"),
        "prefixes": [],
        "suffixes": [],
        "prefix": "",
        "prefix_meaning": "",
        "suffix": "",
        "suffix_meaning": "",
    }


def staged_choice_pool(correct, other_answers, extra=None):
    distractors = [value for value in other_answers if value and value != correct]
    extras = [value for value in (extra or []) if value and value != correct]
    return flow_builder.build_parallel_choices(
        correct,
        distractors,
        f"staged|{stable_fragment(correct)}",
        extra=extras,
    )


def build_phrase_translation_question(record, spec, choice_pools):
    correct = spec["correct_answer"]
    phrase = spec["target"]
    target = {
        "token": phrase,
        "entry": staged_target_entry(spec),
        "source_pasuk": record["text"],
    }
    choices = staged_choice_pool(correct, choice_pools["phrase_translation"])
    return flow_builder.skill_question_payload(
        "phrase_translation",
        target,
        "What does this phrase mean?",
        choices,
        correct,
        f"Here, {phrase} means '{correct}'.",
    )


def build_role_question(record, spec, choice_pools):
    skill = spec["skill"]
    correct = spec["correct_answer"]
    target = {
        "token": spec["target"],
        "entry": staged_target_entry(spec),
        "source_pasuk": record["text"],
    }
    if skill == "subject_identification":
        choices = staged_choice_pool(correct, choice_pools["subject_identification"], extra=["someone else"])
        question_text = f"Who is doing the action in {spec['action_token']}?"
        explanation = f"In {spec['action_token']}, {spec['target']} is doing the action."
    else:
        answer_kind = spec.get("answer_kind", "thing")
        if answer_kind == "person":
            choices = staged_choice_pool(correct, choice_pools["object_identification"], extra=["someone else"])
            question_text = f"Who receives the action in {spec['action_token']}?"
            explanation = f"In {spec['action_token']}, {spec['target']} is the one receiving the action."
        else:
            choices = staged_choice_pool(correct, choice_pools["object_identification"], extra=["something else"])
            question_text = f"What receives the action in {spec['action_token']}?"
            explanation = f"In {spec['action_token']}, {spec['target']} is what receives the action."
    return flow_builder.skill_question_payload(
        skill,
        target,
        question_text,
        choices,
        correct,
        explanation,
        action_token=spec["action_token"],
        role_focus=spec["role_focus"],
    )


def build_question(record, analyzed, word_bank, by_group, spec, choice_pools):
    token = spec["target"]
    target_item = next((item for item in analyzed if item["token"] == token), None)
    skill = spec["skill"]

    if skill == "phrase_translation":
        if normalize_hebrew_key(token) not in normalize_hebrew_key(record["text"]):
            return None
        question = build_phrase_translation_question(record, spec, choice_pools)
    elif skill in {"subject_identification", "object_identification"}:
        if normalize_hebrew_key(token) not in normalize_hebrew_key(record["text"]):
            return None
        question = build_role_question(record, spec, choice_pools)
    elif target_item is None:
        return None
    else:
        target = {
            "token": target_item["token"],
            "entry": deepcopy(target_item["entry"]),
            "source_pasuk": record["text"],
        }

        if skill == "translation":
            if not flow_builder.quiz_ready(target["entry"], token, "translation", word_bank):
                return None
            correct = flow_builder.usable_translation(target["entry"], token)
            distractors = flow_builder.translation_distractors(
                correct,
                target["entry"],
                by_group,
                word_bank,
                require_quality_count=3,
            )
            choices = flow_builder.build_parallel_choices(correct, distractors, f"{record['pasuk_id']}|translation|{token}", token=token)
            question = flow_builder.skill_question_payload(
                "translation",
                target,
                f"What does {token} mean?",
                choices,
                correct,
                f"{token} means '{correct}'.",
            )
        elif skill == "shoresh":
            validation = flow_builder.validate_question_candidate("shoresh", token, target["entry"])
            if not validation["valid"]:
                return None
            correct = flow_builder.clean_shoresh_value(target["entry"].get("shoresh"))
            distractors = [
                value for value in flow_builder.shoresh_distractors(correct, word_bank)
                if normalize_hebrew_key(value) != normalize_hebrew_key(correct)
            ]
            if len(distractors) < 3:
                return None
            choices = [correct] + distractors[:3]
            validation = flow_builder.validate_question_candidate(
                "shoresh",
                token,
                target["entry"],
                correct_answer=correct,
                choices=choices,
            )
            if not validation["valid"]:
                return None
            question = flow_builder.skill_question_payload(
                "shoresh",
                target,
                f"What is the shoresh of {token}?",
                choices,
                correct,
                f"The shoresh of {token} is {correct}.",
            )
        elif skill == "identify_tense":
            correct = flow_builder.runtime_tense_label(target["entry"], token)
            if not correct:
                return None
            choices = flow_builder.fair_tense_choice_codes(correct)
            if not choices:
                return None
            details = flow_builder.tense_form_details(correct, token)
            validation = flow_builder.validate_question_candidate(
                "verb_tense",
                token,
                target["entry"],
                correct_answer=correct,
                choices=choices,
            )
            if not validation["valid"]:
                return None
            question = flow_builder.skill_question_payload(
                "identify_tense",
                target,
                "What form is shown?",
                choices,
                correct,
                flow_builder.tense_question_explanation(target, correct),
                tense_display_phrase=details.get("display_phrase"),
                base_conjugation=details.get("base_conjugation"),
                vav_prefix_type=details.get("vav_prefix_type"),
                accepted_answer_aliases=details.get("accepted_answer_aliases"),
                tense_code=details.get("canonical_code"),
                tense=correct,
            )
        elif skill == "identify_prefix_meaning":
            level = int(spec.get("prefix_level") or 2)
            flow_builder.apply_prefix_metadata(token, target["entry"], word_bank)
            prefix = flow_builder.extract_prefix(token, word_bank) or target["entry"].get("prefix")
            correct = flow_builder.PREFIX_MEANINGS.get(prefix)
            if not prefix or not correct:
                return None
            choices = flow_builder.unique(
                [correct] + [value for value in flow_builder.PREFIX_MEANING_BANK if value != correct]
            )[:4]
            validation = flow_builder.validate_question_candidate(
                "identify_prefix_meaning",
                token,
                target["entry"],
                correct_answer=correct,
                choices=choices,
            )
            if not validation["valid"]:
                return None
            question = flow_builder.prefix_level_question_payload(
                "identify_prefix_meaning",
                target,
                level,
                "identify_prefix_meaning",
                f"What does the prefix {prefix} mean in {token}?",
                choices,
                correct,
                f"In {token}, the prefix {prefix} means '{correct}'.",
            )
        elif skill == "identify_pronoun_suffix":
            flow_builder.apply_suffix_metadata(token, target["entry"], word_bank)
            suffix = target["entry"].get("suffix")
            correct = target["entry"].get("suffix_meaning") or flow_builder.SUFFIX_MEANINGS.get(suffix)
            if not suffix or not correct:
                return None
            choices = flow_builder.unique(
                [correct] + [value for value in flow_builder.SUFFIX_MEANINGS.values() if value != correct]
            )[:4]
            validation = flow_builder.validate_question_candidate(
                "identify_pronoun_suffix",
                token,
                target["entry"],
                correct_answer=correct,
                choices=choices,
            )
            if not validation["valid"]:
                return None
            question = flow_builder.skill_question_payload(
                "identify_pronoun_suffix",
                target,
                f"What does the suffix {suffix} mean in {token}?",
                choices,
                correct,
                f"In {token}, the suffix {suffix} means '{correct}'.",
            )
        else:
            return None

    if not question or question.get("status") == "skipped":
        return None
    item = deepcopy(question)
    item["pasuk"] = record["text"]
    item["pasuk_id"] = record["pasuk_id"]
    item["pasuk_ref"] = {
        **dict(record.get("ref") or {}),
        "label": f"{(record.get('ref') or {}).get('sefer')} {(record.get('ref') or {}).get('perek')}:{(record.get('ref') or {}).get('pasuk')}",
        "pasuk_id": record["pasuk_id"],
    }
    item["review_family"] = spec["family"]
    item["reviewed_id"] = (
        f"staged_{spec['family']}_{spec['skill']}_{record['pasuk_id']}"
        f"_{normalize_hebrew_key(spec['target'])}_{stable_fragment(item.get('correct_answer'))}"
    )
    item["analysis_source"] = "staged_reviewed_support"
    item["source"] = "staged reviewed support"
    return item


def validate_payload(payload, records_by_id):
    duplicate_keys = Counter()
    issues = []
    for item in payload.get("questions", []):
        record = records_by_id.get(item.get("pasuk_id"))
        token = item.get("selected_word") or item.get("word") or ""
        choices = list(item.get("choices") or [])
        correct_answer = item.get("correct_answer")
        duplicate_keys[
            (
                item.get("review_family"),
                item.get("skill"),
                item.get("pasuk_id"),
                normalize_hebrew_key(token),
                stable_fragment(correct_answer),
            )
        ] += 1
        if not record:
            issues.append({"reviewed_id": item.get("reviewed_id"), "code": "missing_pasuk"})
            continue
        if token and normalize_hebrew_key(token) not in normalize_hebrew_key(record["text"]):
            issues.append({"reviewed_id": item.get("reviewed_id"), "code": "target_not_in_pasuk"})
        if len(choices) != 4 or len(set(choices)) != 4:
            issues.append({"reviewed_id": item.get("reviewed_id"), "code": "duplicate_or_short_choices"})
        if correct_answer not in choices:
            issues.append({"reviewed_id": item.get("reviewed_id"), "code": "correct_not_in_choices"})
    duplicate_items = [
        {"key": list(key), "count": count}
        for key, count in duplicate_keys.items()
        if count > 1
    ]
    return {
        "valid": not issues and not duplicate_items,
        "issues": issues,
        "duplicate_items": duplicate_items,
    }


def corpus_title(corpus_id):
    titles = {
        "parsed_bereishis_3_1_to_3_8_staged": "Bereishis 3:1-3:8 staged reviewed support",
        "parsed_bereishis_3_9_to_3_16_staged": "Bereishis 3:9-3:16 staged reviewed support",
        "parsed_bereishis_3_17_to_3_24_staged": "Bereishis 3:17-3:24 staged reviewed support",
    }
    return titles.get(corpus_id, "Bereishis staged reviewed support")


def scope_candidate(corpus_id):
    candidates = {
        "parsed_bereishis_3_1_to_3_8_staged": "local_parsed_bereishis_1_1_to_3_8",
        "parsed_bereishis_3_9_to_3_16_staged": "local_parsed_bereishis_1_1_to_3_16",
        "parsed_bereishis_3_17_to_3_24_staged": "local_parsed_bereishis_1_1_to_3_24",
    }
    return candidates.get(corpus_id, "local_parsed_bereishis_1_1_to_3_16")


def build_payload(bundle_dir):
    bundle = load_staged_corpus_bundle(bundle_dir)
    word_bank, by_group = bundle_word_bank_lookup(bundle)
    records = bundle["parsed_pesukim"]["parsed_pesukim"]
    records_by_id = {record["pasuk_id"]: record for record in records}
    corpus_id = str((bundle.get("pesukim", {}).get("metadata") or {}).get("corpus_id") or "")
    specs = STAGED_REVIEW_SPECS_BY_CORPUS.get(corpus_id)
    if not specs:
        raise SystemExit(f"No staged reviewed-support spec set is defined for {corpus_id or 'unknown_corpus'}.")
    choice_pools = {
        "phrase_translation": [
            spec["correct_answer"]
            for spec in specs
            if spec.get("skill") == "phrase_translation"
        ],
        "subject_identification": [
            spec["correct_answer"]
            for spec in specs
            if spec.get("skill") == "subject_identification"
        ],
        "object_identification": [
            spec["correct_answer"]
            for spec in specs
            if spec.get("skill") == "object_identification"
        ],
    }
    questions = []
    family_counts = Counter()
    skill_counts = Counter()

    for spec in specs:
        record = records_by_id[spec["pasuk_id"]]
        analyzed = parsed_pasuk_to_analyzed(record)
        question = build_question(record, analyzed, word_bank, by_group, spec, choice_pools)
        if question is None:
            raise SystemExit(
                f"Could not build staged reviewed support item for "
                f"{spec['pasuk_id']} {spec['skill']} {spec['target']}"
            )
        questions.append(question)
        family_counts[spec["family"]] += 1
        skill_counts[spec["skill"]] += 1

    payload = {
        "metadata": {
            "title": corpus_title(corpus_id),
            "corpus_id": corpus_id,
            "status": "staged",
            "scope_candidate": scope_candidate(corpus_id),
            "notes": [
                "This file is a curated staged reviewed-support seed bank for the next contiguous slice.",
                "It is not active runtime content yet; it exists to strengthen future promotion readiness.",
            ],
            "lane_counts": dict(family_counts),
            "skill_counts": dict(skill_counts),
        },
        "questions": questions,
    }
    summary = validate_payload(payload, records_by_id)
    if not summary["valid"]:
        raise SystemExit(json.dumps(summary, ensure_ascii=False, indent=2))
    return payload, summary


def main():
    parser = argparse.ArgumentParser(description="Build the staged reviewed-support seed bank for a staged Bereishis bundle.")
    parser.add_argument("--bundle-dir", default=str(DEFAULT_STAGED_BUNDLE_DIR), help="Staged bundle directory to use.")
    parser.add_argument("--validate-only", action="store_true", help="Validate the existing staged reviewed-support file.")
    parser.add_argument("--output", help="Output path for the staged reviewed-support JSON.")
    args = parser.parse_args()

    bundle_dir = Path(args.bundle_dir)
    output_path = Path(args.output) if args.output else bundle_dir / "reviewed_questions.json"
    if args.validate_only:
        payload = json.loads(output_path.read_text(encoding="utf-8"))
        bundle = load_staged_corpus_bundle(bundle_dir)
        records_by_id = {
            record["pasuk_id"]: record
            for record in bundle["parsed_pesukim"]["parsed_pesukim"]
        }
        summary = validate_payload(payload, records_by_id)
    else:
        payload, summary = build_payload(bundle_dir)
        write_json(output_path, payload)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if not summary["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
