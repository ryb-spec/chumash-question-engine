from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import dikduk_rules_loader
import translation_sources_loader
from torah_parser.word_bank_adapter import normalize_hebrew_key


TRANSLATION_USAGE_STATUS = "source_preview_only_license_review_required"
PREVIEW_STATUS = "preview_only"
RUNTIME_STATUS = "not_runtime_active"
PRODUCTION_STATUS = "not_production_ready"
FORBIDDEN_STATUSES = {"active", "runtime_active", "production", "production_ready", "approved", "reviewed"}
DEFAULT_TRANSLATION_SOURCES = ["Koren", "Metsudah"]

REVIEWABLE_PREVIEW_QUESTIONS_RELATIVE = (
    "data/diagnostic_preview/generated_questions/bereishis_1_1_to_2_3_reviewable_preview_questions.jsonl"
)
REVIEWABLE_PREVIEW_PACKET_RELATIVE = (
    "data/diagnostic_preview/reports/bereishis_1_1_to_2_3_reviewable_manual_review_packet.md"
)
REVIEWABLE_PREVIEW_SUMMARY_RELATIVE = (
    "data/diagnostic_preview/reports/bereishis_1_1_to_2_3_reviewable_preview_summary.json"
)
REVIEWABLE_PREVIEW_FINAL_RECOMMENDATION = "Reviewable preview ready for teacher review"
REVIEWABLE_RUNTIME_STATUS = "not_runtime_active"
REVIEWABLE_PRODUCTION_STATUS = "not_production_ready"
REVIEWABLE_DIFFICULTY_VALUES = {"easy", "medium", "hard"}
REVIEWABLE_SKILL_CATEGORIES = {
    "translation",
    "dikduk",
    "shoresh",
    "prefix",
    "suffix",
    "noun",
    "verb",
    "gender",
    "number",
    "phrase_meaning",
    "pasuk_comprehension",
}
REVIEWABLE_TRANSLATION_ALIGNMENT_VALUES = {
    "koren_and_metsudah_align",
    "minor_translation_difference",
    "significant_translation_difference",
    "translation_review_required",
}
REVIEWABLE_REVIEW_PRIORITY_VALUES = {"high", "medium", "low"}
REVIEWABLE_REVIEW_STATUS_VALUES = {"likely_approve", "caution", "likely_rewrite"}
REVIEWABLE_STUDENT_RISK_VALUES = {"low", "medium", "high"}
REVIEWABLE_REVIEW_FLAGS = {
    "duplicate_or_too_similar",
    "translation_sensitive",
    "awkward_wording",
    "too_easy",
    "too_hard",
    "unclear_question",
    "weak_distractors",
    "misleading_distractors",
    "source_support_unclear",
    "dikduk_support_unclear",
    "teacher_facing_not_student_facing",
    "depends_on_unintroduced_knowledge",
    "possible_multiple_correct_answers",
    "good_student_candidate",
}

REVIEWABLE_SELECTED_QUESTION_IDS = [
    "DQ-BER-001-001-001",
    "DQ-BER-001-001-003",
    "DQ-BER-001-001-005",
    "DQ-BER-001-002-001",
    "DQ-BER-001-003-001",
    "DQ-BER-001-004-001",
    "DQ-BER-001-005-001",
    "DQ-BER-001-006-001",
    "DQ-BER-001-009-001",
    "DQ-BER-001-010-001",
    "DQ-BER-001-014-001",
    "DQ-BER-002-002-001",
    "DQ-BER-001-022-001",
    "DQ-BER-001-022-003",
    "DQ-BER-001-001-007",
    "DQ-BER-001-001-009",
    "DQ-BER-001-002-003",
    "DQ-BER-001-002-004",
    "DQ-BER-001-001-011",
    "DQ-BER-001-001-012",
    "DQ-BER-001-001-013",
    "DQ-BER-001-005-003",
    "DQ-BER-001-010-003",
    "DQ-BER-001-010-004",
    "DQ-BER-001-014-003",
    "DQ-BER-001-014-004",
    "DQ-BER-001-003-003",
    "DQ-BER-001-012-001",
    "DQ-BER-001-003-005",
    "DQ-BER-001-004-005",
    "DQ-BER-001-005-005",
    "DQ-BER-001-004-007",
    "DQ-BER-001-015-001",
]

REVIEWABLE_CAUTION_IDS = {
    "DQ-BER-001-002-001",
    "DQ-BER-001-006-001",
    "DQ-BER-001-009-001",
    "DQ-BER-001-003-003",
    "DQ-BER-001-012-001",
    "DQ-BER-001-015-001",
}
REVIEWABLE_HIGH_PRIORITY_IDS = {
    "DQ-BER-001-002-001",
    "DQ-BER-001-006-001",
    "DQ-BER-001-009-001",
    "DQ-BER-001-003-003",
    "DQ-BER-001-012-001",
}
REVIEWABLE_TOO_EASY_IDS = {
    "DQ-BER-001-001-007",
    "DQ-BER-001-001-009",
    "DQ-BER-001-002-003",
    "DQ-BER-001-010-003",
    "DQ-BER-001-014-003",
}
REVIEWABLE_DEPENDS_ON_UNINTRODUCED_KNOWLEDGE_IDS = {
    "DQ-BER-001-003-003",
    "DQ-BER-001-012-001",
    "DQ-BER-001-015-001",
}
REVIEWABLE_POSSIBLE_MULTIPLE_ANSWER_IDS = {
    "DQ-BER-001-002-001",
    "DQ-BER-001-006-001",
    "DQ-BER-001-009-001",
}
REVIEWABLE_TRANSLATION_ALIGNMENT_OVERRIDES = {
    "DQ-BER-001-002-001": "minor_translation_difference",
    "DQ-BER-001-006-001": "significant_translation_difference",
    "DQ-BER-001-009-001": "minor_translation_difference",
}
REVIEWABLE_PRIMARY_RULE_OVERRIDES = {
    "DQ-BER-001-002-001": "DK-NOUN-002",
    "DQ-BER-001-003-003": "DK-WORDORDER-002",
    "DQ-BER-001-012-001": "DK-VERB-001",
    "DQ-BER-001-015-001": "DK-PARSE-002",
}
REVIEWABLE_PRIMARY_ERROR_OVERRIDES = {
    "DQ-BER-001-002-001": "ERR-DK-NOUN-001",
    "DQ-BER-001-003-003": "ERR-DK-WORDORDER-001",
    "DQ-BER-001-012-001": "ERR-DK-GENDER-001",
    "DQ-BER-001-015-001": "ERR-DK-VERB-002",
}

HEBREW_PUNCTUATION_RE = re.compile(r"[\u05be\u05c0\u05c3\u05c6.,;:!?]+")
HEBREW_LATIN_CLEAN_RE = re.compile(r"[^\u0590-\u05ff]+")


TRANSLATION_TARGETS: list[dict[str, Any]] = [
    {
        "ref": "Genesis 1:1",
        "target_hebrew": "בראשית",
        "source_words": ["בראשית"],
        "correct_answer": "in the beginning",
        "accepted_answers": ["in the beginning"],
        "distractors": [
            ("created", "common creation verb distractor"),
            ("the earth", "nearby creation noun distractor"),
            ("night", "high-frequency creation noun distractor"),
        ],
        "rule_ids": ["DK-PREP-004"],
        "mastery_tags": ["basic_translation", "preposition_meaning"],
        "difficulty_level": 1,
    },
    {
        "ref": "Genesis 1:1",
        "target_hebrew": "ברא",
        "source_words": ["ברא"],
        "correct_answer": "created",
        "accepted_answers": ["created"],
        "distractors": [
            ("said", "common high-frequency verb distractor"),
            ("saw", "another nearby creation verb distractor"),
            ("called", "another creation-sequence verb distractor"),
        ],
        "rule_ids": ["DK-VERB-001"],
        "mastery_tags": ["basic_translation", "verb_identification"],
        "difficulty_level": 1,
    },
    {
        "ref": "Genesis 1:1",
        "target_hebrew": "הארץ",
        "source_words": ["הארץ"],
        "correct_answer": "the earth",
        "accepted_answers": ["the earth"],
        "distractors": [
            ("the heavens", "nearby paired noun distractor"),
            ("the light", "other creation noun distractor"),
            ("the waters", "other creation noun distractor"),
        ],
        "rule_ids": ["DK-ARTICLE-001"],
        "mastery_tags": ["basic_translation", "definite_article"],
        "difficulty_level": 1,
    },
    {
        "ref": "Genesis 1:2",
        "target_hebrew": "המים",
        "source_words": ["המים"],
        "correct_answer": "the waters",
        "accepted_answers": ["the waters", "waters", "the water", "water"],
        "distractors": [
            ("the earth", "nearby creation noun distractor"),
            ("the darkness", "other verse noun distractor"),
            ("the wind", "nearby verse noun distractor"),
        ],
        "rule_ids": ["DK-NOUN-002", "DK-ARTICLE-001"],
        "mastery_tags": ["basic_translation", "translation_caution", "definite_article"],
        "difficulty_level": 2,
    },
    {
        "ref": "Genesis 1:3",
        "target_hebrew": "אור",
        "source_words": ["אור"],
        "correct_answer": "light",
        "accepted_answers": ["light"],
        "distractors": [
            ("earth", "nearby creation noun distractor"),
            ("day", "related but later noun distractor"),
            ("darkness", "paired opposite noun distractor"),
        ],
        "rule_ids": [],
        "mastery_tags": ["basic_translation", "word_meaning"],
        "difficulty_level": 1,
    },
    {
        "ref": "Genesis 1:4",
        "target_hebrew": "טוב",
        "source_words": ["טוב"],
        "correct_answer": "good",
        "accepted_answers": ["good"],
        "distractors": [
            ("light", "nearby verse noun distractor"),
            ("dry", "other creation adjective distractor"),
            ("living", "other creation adjective distractor"),
        ],
        "rule_ids": [],
        "mastery_tags": ["basic_translation", "word_meaning"],
        "difficulty_level": 1,
    },
    {
        "ref": "Genesis 1:5",
        "target_hebrew": "לילה",
        "source_words": ["לילה"],
        "correct_answer": "night",
        "accepted_answers": ["night"],
        "distractors": [
            ("day", "paired opposite noun distractor"),
            ("light", "nearby verse noun distractor"),
            ("darkness", "nearby verse noun distractor"),
        ],
        "rule_ids": [],
        "mastery_tags": ["basic_translation", "word_meaning"],
        "difficulty_level": 1,
    },
    {
        "ref": "Genesis 1:9",
        "target_hebrew": "היבשה",
        "source_words": ["היבשה"],
        "correct_answer": "dry land",
        "accepted_answers": ["dry land", "the dry land", "dryness"],
        "distractors": [
            ("the waters", "paired creation noun distractor"),
            ("the heavens", "other creation noun distractor"),
            ("light", "other creation noun distractor"),
        ],
        "rule_ids": ["DK-ARTICLE-001"],
        "mastery_tags": ["basic_translation", "definite_article"],
        "difficulty_level": 2,
    },
    {
        "ref": "Genesis 1:10",
        "target_hebrew": "ימים",
        "source_words": ["ימים"],
        "correct_answer": "seas",
        "accepted_answers": ["seas"],
        "distractors": [
            ("days", "surface-form distractor"),
            ("waters", "nearby creation noun distractor"),
            ("earth", "other nearby creation noun distractor"),
        ],
        "rule_ids": ["DK-PLURAL-001"],
        "mastery_tags": ["basic_translation", "plural_recognition"],
        "difficulty_level": 2,
    },
    {
        "ref": "Genesis 1:14",
        "target_hebrew": "מארת",
        "source_words": ["מארת"],
        "correct_answer": "lights",
        "accepted_answers": ["lights"],
        "distractors": [
            ("waters", "other creation noun distractor"),
            ("days", "nearby verse noun distractor"),
            ("seas", "other creation noun distractor"),
        ],
        "rule_ids": ["DK-PLURAL-002"],
        "mastery_tags": ["basic_translation", "feminine_plural"],
        "difficulty_level": 2,
    },
    {
        "ref": "Genesis 2:2",
        "target_hebrew": "מלאכתו",
        "source_words": ["מלאכתו"],
        "correct_answer": "his work",
        "accepted_answers": ["his work", "His work"],
        "distractors": [
            ("the seventh day", "nearby phrase distractor"),
            ("the earth", "creation noun distractor"),
            ("the heavens", "creation noun distractor"),
        ],
        "rule_ids": [],
        "mastery_tags": ["basic_translation", "word_meaning"],
        "difficulty_level": 2,
    },
    {
        "ref": "Genesis 1:22",
        "target_hebrew": "פרו",
        "source_words": ["פרו"],
        "correct_answer": "be fruitful",
        "accepted_answers": ["be fruitful"],
        "distractors": [
            ("multiply", "nearby imperative distractor"),
            ("fill", "nearby imperative distractor"),
            ("divide", "other creation verb distractor"),
        ],
        "rule_ids": ["DK-VERB-001"],
        "mastery_tags": ["basic_translation", "verb_identification"],
        "difficulty_level": 2,
    },
    {
        "ref": "Genesis 1:22",
        "target_hebrew": "ורבו",
        "source_words": ["ורבו"],
        "correct_answer": "multiply",
        "accepted_answers": ["multiply"],
        "distractors": [
            ("be fruitful", "nearby imperative distractor"),
            ("fill", "nearby imperative distractor"),
            ("gather", "other creation verb distractor"),
        ],
        "rule_ids": ["DK-CONJ-001", "DK-VERB-001"],
        "mastery_tags": ["basic_translation", "verb_identification", "conjunction_recognition"],
        "difficulty_level": 2,
    },
]

DIKDUK_TARGETS: list[dict[str, Any]] = [
    {
        "ref": "Genesis 1:1",
        "target_hebrew": "הארץ",
        "source_words": ["הארץ"],
        "subtype": "article",
        "rule_ids": ["DK-ARTICLE-001"],
        "mastery_tags": ["definite_article", "prefix_recognition", "noun_translation"],
        "difficulty_level": 1,
        "translation_with_rule": "the earth",
    },
    {
        "ref": "Genesis 1:1",
        "target_hebrew": "השמים",
        "source_words": ["השמים"],
        "subtype": "article",
        "rule_ids": ["DK-ARTICLE-001"],
        "mastery_tags": ["definite_article", "prefix_recognition", "noun_translation"],
        "difficulty_level": 1,
        "translation_with_rule": "the heavens",
    },
    {
        "ref": "Genesis 1:2",
        "target_hebrew": "והארץ",
        "source_words": ["והארץ"],
        "subtype": "conjunction",
        "rule_ids": ["DK-CONJ-001"],
        "mastery_tags": ["conjunction_recognition", "prefix_recognition", "word_connection"],
        "difficulty_level": 1,
        "translation_with_rule": "and the earth",
    },
    {
        "ref": "Genesis 1:1",
        "target_hebrew": "את",
        "source_words": ["את"],
        "subtype": "direct_object_marker",
        "rule_ids": ["DK-ET-001"],
        "mastery_tags": ["direct_object_marker", "function_disambiguation", "phrase_translation"],
        "difficulty_level": 2,
    },
    {
        "ref": "Genesis 1:1",
        "target_hebrew": "בראשית",
        "source_words": ["בראשית"],
        "subtype": "prefix_b",
        "rule_ids": ["DK-PREP-004"],
        "mastery_tags": ["preposition_meaning", "prefix_recognition", "context_sensitivity"],
        "difficulty_level": 1,
        "correct_meaning": "in",
    },
    {
        "ref": "Genesis 1:5",
        "target_hebrew": "לאור",
        "source_words": ["לאור"],
        "subtype": "prefix_l",
        "rule_ids": ["DK-PREP-003"],
        "mastery_tags": ["preposition_meaning", "prefix_recognition", "context_sensitivity"],
        "difficulty_level": 1,
        "correct_meaning": "to / for",
    },
    {
        "ref": "Genesis 1:10",
        "target_hebrew": "ימים",
        "source_words": ["ימים"],
        "subtype": "plural_yim",
        "rule_ids": ["DK-PLURAL-001"],
        "mastery_tags": ["plural_recognition", "masculine_plural", "suffix_recognition"],
        "difficulty_level": 1,
    },
    {
        "ref": "Genesis 1:14",
        "target_hebrew": "מארת",
        "source_words": ["מארת"],
        "subtype": "plural_vav_tav",
        "rule_ids": ["DK-PLURAL-002"],
        "mastery_tags": ["plural_recognition", "feminine_plural", "suffix_recognition"],
        "difficulty_level": 2,
    },
    {
        "ref": "Genesis 1:2",
        "target_hebrew": "המים",
        "source_words": ["המים"],
        "subtype": "irregular_plural_warning",
        "rule_ids": ["DK-NOUN-002"],
        "mastery_tags": ["translation_caution", "noun_translation", "plural_recognition"],
        "difficulty_level": 3,
        "safe_translation": "water",
    },
    {
        "ref": "Genesis 1:3",
        "target_hebrew": "ויאמר אלהים",
        "source_words": ["ויאמר", "אלהים"],
        "subtype": "word_order",
        "rule_ids": ["DK-WORDORDER-001", "DK-WORDORDER-002"],
        "mastery_tags": ["syntax_awareness", "translation_reordering", "verb_identification"],
        "difficulty_level": 2,
        "natural_translation": "God said",
    },
    {
        "ref": "Genesis 2:2",
        "target_hebrew": "ביום",
        "source_words": ["ביום"],
        "subtype": "prefix_b",
        "rule_ids": ["DK-PREP-004"],
        "mastery_tags": ["preposition_meaning", "prefix_recognition", "context_sensitivity"],
        "difficulty_level": 1,
        "correct_meaning": "in",
    },
    {
        "ref": "Genesis 1:4",
        "target_hebrew": "את",
        "source_words": ["את"],
        "subtype": "direct_object_marker",
        "rule_ids": ["DK-ET-001"],
        "mastery_tags": ["direct_object_marker", "function_disambiguation", "phrase_translation"],
        "difficulty_level": 2,
    },
    {
        "ref": "Genesis 1:12",
        "target_hebrew": "ותוצא הארץ",
        "source_words": ["ותוצא", "הארץ"],
        "subtype": "verb_agreement",
        "rule_ids": ["DK-VERB-001"],
        "mastery_tags": ["agreement_features", "subject_tracking", "verb_identification"],
        "difficulty_level": 3,
        "matching_noun": "הארץ",
    },
]

WORD_ANALYSIS_TARGETS: list[dict[str, Any]] = [
    {
        "ref": "Genesis 1:3",
        "target_hebrew": "ויאמר",
        "source_words": ["ויאמר"],
        "rule_ids": ["DK-PARSE-002", "DK-PARSE-003"],
        "mastery_tags": ["shoresh_identification", "word_decomposition", "verb_form_analysis"],
        "difficulty_level": 2,
        "shoresh": "אמר",
        "shoresh_choices": ["אמר", "ראה", "קרא", "ברא"],
        "added_letters": "ו + י",
        "added_letter_choices": ["ו + י", "ה + י", "ל + ה", "מ + י"],
    },
    {
        "ref": "Genesis 1:4",
        "target_hebrew": "וירא",
        "source_words": ["וירא"],
        "rule_ids": ["DK-PARSE-002", "DK-PARSE-003"],
        "mastery_tags": ["shoresh_identification", "word_decomposition", "verb_form_analysis"],
        "difficulty_level": 2,
        "shoresh": "ראה",
        "shoresh_choices": ["ראה", "אמר", "בדל", "קרא"],
        "added_letters": "ו + י",
        "added_letter_choices": ["ו + י", "ל + ה", "ו + ת", "מ + י"],
    },
    {
        "ref": "Genesis 1:5",
        "target_hebrew": "ויקרא",
        "source_words": ["ויקרא"],
        "rule_ids": ["DK-PARSE-002", "DK-PARSE-003"],
        "mastery_tags": ["shoresh_identification", "word_decomposition", "verb_form_analysis"],
        "difficulty_level": 2,
        "shoresh": "קרא",
        "shoresh_choices": ["קרא", "אמר", "ראה", "ברא"],
        "added_letters": "ו + י",
        "added_letter_choices": ["ו + י", "ו + ת", "ל + ה", "ה + מ"],
    },
    {
        "ref": "Genesis 1:4",
        "target_hebrew": "ויבדל",
        "source_words": ["ויבדל"],
        "rule_ids": ["DK-PARSE-002", "DK-PARSE-003"],
        "mastery_tags": ["shoresh_identification", "word_decomposition", "verb_form_analysis"],
        "difficulty_level": 3,
        "shoresh": "בדל",
        "shoresh_choices": ["בדל", "ברא", "אמר", "ראה"],
        "added_letters": "ו + י",
        "added_letter_choices": ["ו + י", "ב + ה", "ל + ה", "ו + ת"],
    },
    {
        "ref": "Genesis 1:15",
        "target_hebrew": "להאיר",
        "source_words": ["להאיר"],
        "rule_ids": ["DK-PREP-003", "DK-PARSE-002", "DK-PARSE-003"],
        "mastery_tags": ["shoresh_identification", "word_decomposition", "prefix_recognition"],
        "difficulty_level": 3,
        "shoresh": "אור",
        "shoresh_choices": ["אור", "קרא", "ראה", "עשה"],
        "added_letters": "ל + ה",
        "added_letter_choices": ["ל + ה", "ו + י", "מ + י", "ה + ת"],
    },
]

ERROR_DIAGNOSIS_TARGETS: list[dict[str, Any]] = [
    {
        "ref": "Genesis 1:1",
        "target_hebrew": "הארץ",
        "source_words": ["הארץ"],
        "correct_error_id": "ERR-DK-ARTICLE-001",
        "distractor_error_ids": ["ERR-DK-CONJ-001", "ERR-DK-PLURAL-001", "ERR-DK-ET-002"],
        "mastery_tags": ["definite_article", "error_diagnosis"],
        "difficulty_level": 1,
        "wrong_answer": "earth",
    },
    {
        "ref": "Genesis 1:1",
        "target_hebrew": "השמים",
        "source_words": ["השמים"],
        "correct_error_id": "ERR-DK-ARTICLE-002",
        "distractor_error_ids": ["ERR-DK-CONJ-002", "ERR-DK-PLURAL-001", "ERR-DK-ET-002"],
        "mastery_tags": ["definite_article", "word_decomposition", "error_diagnosis"],
        "difficulty_level": 2,
        "wrong_answer": "The student says the initial ה is part of the base noun.",
    },
    {
        "ref": "Genesis 1:2",
        "target_hebrew": "והארץ",
        "source_words": ["והארץ"],
        "correct_error_id": "ERR-DK-CONJ-001",
        "distractor_error_ids": ["ERR-DK-ARTICLE-001", "ERR-DK-PLURAL-001", "ERR-DK-ET-002"],
        "mastery_tags": ["conjunction_recognition", "error_diagnosis"],
        "difficulty_level": 1,
        "wrong_answer": "the earth",
    },
    {
        "ref": "Genesis 1:2",
        "target_hebrew": "והארץ",
        "source_words": ["והארץ"],
        "correct_error_id": "ERR-DK-CONJ-002",
        "distractor_error_ids": ["ERR-DK-ARTICLE-002", "ERR-DK-PLURAL-001", "ERR-DK-ET-002"],
        "mastery_tags": ["conjunction_recognition", "word_decomposition", "error_diagnosis"],
        "difficulty_level": 2,
        "wrong_answer": "The student treats ו as part of the noun itself.",
    },
    {
        "ref": "Genesis 1:10",
        "target_hebrew": "ימים",
        "source_words": ["ימים"],
        "correct_error_id": "ERR-DK-PLURAL-001",
        "distractor_error_ids": ["ERR-DK-PLURAL-002", "ERR-DK-ARTICLE-001", "ERR-DK-ET-002"],
        "mastery_tags": ["plural_recognition", "error_diagnosis"],
        "difficulty_level": 1,
        "wrong_answer": "sea",
    },
    {
        "ref": "Genesis 1:14",
        "target_hebrew": "מארת",
        "source_words": ["מארת"],
        "correct_error_id": "ERR-DK-PLURAL-002",
        "distractor_error_ids": ["ERR-DK-PLURAL-001", "ERR-DK-ARTICLE-001", "ERR-DK-ET-002"],
        "mastery_tags": ["plural_recognition", "error_diagnosis"],
        "difficulty_level": 2,
        "wrong_answer": "light",
    },
    {
        "ref": "Genesis 1:1",
        "target_hebrew": "את",
        "source_words": ["את"],
        "correct_error_id": "ERR-DK-ET-002",
        "distractor_error_ids": ["ERR-DK-ET-001", "ERR-DK-ARTICLE-001", "ERR-DK-CONJ-001"],
        "mastery_tags": ["direct_object_marker", "error_diagnosis"],
        "difficulty_level": 2,
        "wrong_answer": "with",
    },
    {
        "ref": "Genesis 1:4",
        "target_hebrew": "את",
        "source_words": ["את"],
        "correct_error_id": "ERR-DK-ET-001",
        "distractor_error_ids": ["ERR-DK-ET-002", "ERR-DK-ARTICLE-001", "ERR-DK-CONJ-001"],
        "mastery_tags": ["function_disambiguation", "error_diagnosis"],
        "difficulty_level": 3,
        "wrong_answer": "The student wants every את-family form to mean 'with'.",
    },
    {
        "ref": "Genesis 1:2",
        "target_hebrew": "המים",
        "source_words": ["המים"],
        "correct_error_id": "ERR-DK-NOUN-001",
        "distractor_error_ids": ["ERR-DK-PLURAL-001", "ERR-DK-ARTICLE-001", "ERR-DK-ET-002"],
        "mastery_tags": ["translation_caution", "error_diagnosis"],
        "difficulty_level": 3,
        "wrong_answer": "waters in every basic context",
    },
    {
        "ref": "Genesis 1:3",
        "target_hebrew": "ויאמר",
        "source_words": ["ויאמר"],
        "correct_error_id": "ERR-DK-VERB-002",
        "distractor_error_ids": ["ERR-DK-VERB-001", "ERR-DK-VERB-003", "ERR-DK-PARSE-001"],
        "mastery_tags": ["verb_tense", "error_diagnosis"],
        "difficulty_level": 3,
        "wrong_answer": "The student notices the root but misses the tense clue.",
    },
]

TRANSLATION_COMPARISON_TARGETS: list[dict[str, Any]] = [
    {
        "ref": "Genesis 1:1",
        "target_hebrew": "אלהים",
        "source_words": ["אלהים"],
        "correct_answer": "God",
        "accepted_answers": ["God", "Elohim"],
        "distractors": [
            ("the heavens", "nearby creation noun distractor"),
            ("the earth", "nearby creation noun distractor"),
            ("light", "other creation noun distractor"),
        ],
        "rule_ids": ["DK-NOUN-001"],
        "mastery_tags": ["mixed_skill", "translation_caution", "noun_translation"],
        "difficulty_level": 2,
    },
    {
        "ref": "Genesis 1:1",
        "target_hebrew": "השמים",
        "source_words": ["השמים"],
        "correct_answer": "the heavens",
        "accepted_answers": ["the heavens", "the heaven"],
        "distractors": [
            ("the earth", "paired creation noun distractor"),
            ("the waters", "other creation noun distractor"),
            ("the night", "other creation noun distractor"),
        ],
        "rule_ids": ["DK-ARTICLE-001", "DK-PLURAL-001"],
        "mastery_tags": ["mixed_skill", "definite_article", "plural_recognition"],
        "difficulty_level": 2,
    },
    {
        "ref": "Genesis 1:6",
        "target_hebrew": "רקיע",
        "source_words": ["רקיע"],
        "correct_answer": "firmament",
        "accepted_answers": ["firmament", "canopy"],
        "distractors": [
            ("the waters", "nearby verse noun distractor"),
            ("light", "other creation noun distractor"),
            ("seas", "other creation noun distractor"),
        ],
        "rule_ids": [],
        "mastery_tags": ["mixed_skill", "translation_caution", "word_meaning"],
        "difficulty_level": 2,
    },
    {
        "ref": "Genesis 1:9",
        "target_hebrew": "היבשה",
        "source_words": ["היבשה"],
        "correct_answer": "dry land",
        "accepted_answers": ["dry land", "dryness"],
        "distractors": [
            ("the waters", "paired creation noun distractor"),
            ("the heavens", "other creation noun distractor"),
            ("night", "other creation noun distractor"),
        ],
        "rule_ids": ["DK-ARTICLE-001"],
        "mastery_tags": ["mixed_skill", "definite_article", "translation_caution"],
        "difficulty_level": 2,
    },
    {
        "ref": "Genesis 1:2",
        "target_hebrew": "המים",
        "source_words": ["המים"],
        "correct_answer": "the waters",
        "accepted_answers": ["the waters", "the water", "waters", "water"],
        "distractors": [
            ("the earth", "nearby creation noun distractor"),
            ("the darkness", "other verse noun distractor"),
            ("the night", "other creation noun distractor"),
        ],
        "rule_ids": ["DK-NOUN-002", "DK-ARTICLE-001"],
        "mastery_tags": ["mixed_skill", "translation_caution", "definite_article"],
        "difficulty_level": 3,
    },
]


@dataclass
class RefContext:
    ref: str
    hebrew_ref: str
    perek: int
    pasuk: int
    hebrew_text: str
    koren_translation: str
    metsudah_translation: str
    source_url: str


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, 1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path.as_posix()} line {line_number}: invalid JSON ({exc})") from exc
            if not isinstance(record, dict):
                raise ValueError(f"{path.as_posix()} line {line_number}: expected JSON object")
            rows.append(record)
    return rows


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def preserved_manual_review_findings(path: Path) -> list[str]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    heading = "## AI-Assisted Review Findings"
    ref_section = "## Genesis 1:1 / Bereishis 1:1"
    start_index = text.find(heading)
    if start_index == -1:
        return []
    end_index = text.find(ref_section, start_index)
    preserved_block = text[start_index:end_index].rstrip() if end_index != -1 else text[start_index:].rstrip()
    if not preserved_block:
        return []
    return preserved_block.splitlines() + [""]


def parse_ref(ref: str) -> tuple[int, int]:
    match = re.search(r"(\d+):(\d+)$", ref)
    if not match:
        raise ValueError(f"Unsupported ref format: {ref}")
    return int(match.group(1)), int(match.group(2))


def ref_in_range(ref: str, start_ref: str, end_ref: str) -> bool:
    perek, pasuk = parse_ref(ref)
    start = parse_ref(start_ref)
    end = parse_ref(end_ref)
    return start <= (perek, pasuk) <= end


def hebrew_tokens(text: str) -> list[str]:
    cleaned = HEBREW_PUNCTUATION_RE.sub(" ", text or "")
    raw_tokens = []
    for token in cleaned.split():
        token = token.replace("\u200f", "").replace("\u200e", "")
        token = token.strip()
        if token:
            raw_tokens.append(token)
    return raw_tokens


def normalized_tokens(text: str) -> list[str]:
    tokens = []
    for token in hebrew_tokens(text):
        normalized = normalize_hebrew_key(token)
        normalized = HEBREW_LATIN_CLEAN_RE.sub("", normalized)
        if normalized:
            tokens.append(normalized)
    return tokens


def load_canonical_hebrew_rows(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader)


def build_ref_contexts(config: dict[str, Any]) -> dict[str, RefContext]:
    hebrew_rows = load_canonical_hebrew_rows(REPO_ROOT / config["source_hebrew_file"])
    koren_rows = load_jsonl(REPO_ROOT / config["koren_translation_file"])
    metsudah_rows = load_jsonl(REPO_ROOT / config["metsudah_translation_file"])
    koren_by_ref = {row["ref"]: row for row in koren_rows}
    metsudah_by_ref = {row["ref"]: row for row in metsudah_rows}

    contexts: dict[str, RefContext] = {}
    for row in hebrew_rows:
        ref = f"Genesis {row['perek']}:{row['pasuk']}"
        if not ref_in_range(ref, config["start_ref"], config["end_ref"]):
            continue
        if ref not in koren_by_ref or ref not in metsudah_by_ref:
            raise ValueError(f"Missing translation alignment for {ref}")
        contexts[ref] = RefContext(
            ref=ref,
            hebrew_ref=row["ref"],
            perek=int(row["perek"]),
            pasuk=int(row["pasuk"]),
            hebrew_text=row["hebrew_menukad_taamim"],
            koren_translation=koren_by_ref[ref]["translation_text"],
            metsudah_translation=metsudah_by_ref[ref]["translation_text"],
            source_url=koren_by_ref[ref]["source_url"],
        )
    return dict(sorted(contexts.items(), key=lambda item: parse_ref(item[0])))


def load_config(path: Path) -> dict[str, Any]:
    config = load_json(path)
    if config.get("status") != PREVIEW_STATUS:
        raise ValueError("Diagnostic preview config must keep status=preview_only.")
    if config.get("runtime_status") != RUNTIME_STATUS:
        raise ValueError("Diagnostic preview config must keep runtime_status=not_runtime_active.")
    if config.get("production_status") != PRODUCTION_STATUS:
        raise ValueError("Diagnostic preview config must keep production_status=not_production_ready.")
    for field in (
        "source_hebrew_file",
        "koren_translation_file",
        "metsudah_translation_file",
        "translation_registry_file",
        "dikduk_rules_file",
        "question_templates_file",
        "error_patterns_file",
    ):
        resolved = REPO_ROOT / config[field]
        if not resolved.exists():
            raise FileNotFoundError(f"Required source file missing: {config[field]}")
    return config


def build_rule_template_map() -> dict[tuple[str, str], str]:
    mapping: dict[tuple[str, str], str] = {}
    for template in dikduk_rules_loader.load_dikduk_question_templates():
        mapping.setdefault((template["rule_id"], template["question_type"]), template["template_id"])
    return mapping


def build_error_index() -> dict[str, dict[str, Any]]:
    return {record["error_id"]: record for record in dikduk_rules_loader.load_dikduk_error_patterns()}


def linked_error_ids(rule_ids: list[str]) -> list[str]:
    linked: list[str] = []
    for error in dikduk_rules_loader.load_dikduk_error_patterns():
        if set(error.get("linked_rule_ids", [])) & set(rule_ids):
            linked.append(error["error_id"])
    return linked


def ensure_source_grounded(context: RefContext, source_words: list[str]) -> None:
    normalized_verse_tokens = set(normalized_tokens(context.hebrew_text))
    for source_word in source_words:
        normalized = normalize_hebrew_key(source_word)
        normalized = HEBREW_LATIN_CLEAN_RE.sub("", normalized)
        if normalized not in normalized_verse_tokens:
            raise ValueError(f"{context.ref}: source word {source_word!r} not found in Hebrew text")


def make_choice_list(correct_answer: str, distractors: list[tuple[str, str]]) -> tuple[list[str], list[dict[str, str]]]:
    seen = {correct_answer}
    choices = [correct_answer]
    distractor_rows: list[dict[str, str]] = []
    for text, reason in distractors:
        if text in seen:
            continue
        seen.add(text)
        choices.append(text)
        distractor_rows.append({"text": text, "reason": reason})
        if len(choices) == 4:
            break
    if len(choices) < 4:
        raise ValueError(f"Not enough unique choices to build multiple-choice item for {correct_answer!r}")
    return choices, distractor_rows


def default_source_evidence(rule_ids: list[str]) -> dict[str, Any]:
    return {
        "hebrew_source": "canonical Bereishis Hebrew TSV",
        "translation_sources": DEFAULT_TRANSLATION_SOURCES,
        "translation_usage_status": TRANSLATION_USAGE_STATUS,
        "dikduk_sources": rule_ids,
    }


def build_blueprint_and_question(
    *,
    context: RefContext,
    index_within_ref: int,
    lane: str,
    skill_focus: str,
    question_type: str,
    target_hebrew: str,
    source_words: list[str],
    prompt: str,
    choices: list[str],
    correct_answer: str,
    accepted_answers: list[str],
    distractor_rows: list[dict[str, str]],
    feedback_correct: str,
    feedback_incorrect: str,
    rule_ids: list[str],
    mastery_tags: list[str],
    difficulty_level: int,
    student_error_pattern_ids: list[str],
    template_id: str | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    blueprint_id = f"DP-BER-{context.perek:03d}-{context.pasuk:03d}-{index_within_ref:03d}"
    question_id = f"DQ-BER-{context.perek:03d}-{context.pasuk:03d}-{index_within_ref:03d}"
    source_evidence = default_source_evidence(rule_ids)
    blueprint = {
        "blueprint_id": blueprint_id,
        "ref": context.ref,
        "hebrew_ref": context.hebrew_ref,
        "hebrew_text": context.hebrew_text,
        "koren_translation": context.koren_translation,
        "metsudah_translation": context.metsudah_translation,
        "diagnostic_lane": lane,
        "skill_focus": skill_focus,
        "dikduk_rule_ids": rule_ids,
        "mastery_tags": mastery_tags,
        "source_words": source_words,
        "student_error_patterns": student_error_pattern_ids,
        "question_types_allowed": [question_type],
        "difficulty_level": difficulty_level,
        "translation_usage_status": TRANSLATION_USAGE_STATUS,
        "question_template_ids": [template_id] if template_id else [],
        "status": PREVIEW_STATUS,
    }
    question = {
        "question_id": question_id,
        "blueprint_id": blueprint_id,
        "ref": context.ref,
        "hebrew_ref": context.hebrew_ref,
        "prompt": prompt,
        "question_type": question_type,
        "choices": choices,
        "correct_answer": correct_answer,
        "accepted_answers": accepted_answers,
        "distractors": distractor_rows,
        "feedback_correct": feedback_correct,
        "feedback_incorrect": feedback_incorrect,
        "dikduk_rule_ids": rule_ids,
        "mastery_tags": mastery_tags,
        "student_error_pattern_ids": student_error_pattern_ids,
        "question_template_id": template_id,
        "source_evidence": source_evidence,
        "translation_usage_status": TRANSLATION_USAGE_STATUS,
        "skill_focus": skill_focus,
        "diagnostic_lane": lane,
        "difficulty_level": difficulty_level,
        "status": PREVIEW_STATUS,
    }
    return blueprint, question


def translation_variants_for_seed(seed: dict[str, Any]) -> list[tuple[str, str]]:
    return [
        ("choose_translation", f"What does {seed['target_hebrew']} mean in this pasuk?"),
        ("identify_word_meaning", f"Which English meaning best fits {seed['target_hebrew']} in {seed['ref']}?"),
    ]


def build_translation_rows(
    contexts: dict[str, RefContext],
    template_map: dict[tuple[str, str], str],
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    rows = []
    counters: defaultdict[str, int] = defaultdict(int)
    for seed in TRANSLATION_TARGETS:
        context = contexts[seed["ref"]]
        ensure_source_grounded(context, seed["source_words"])
        for question_type, prompt in translation_variants_for_seed(seed):
            counters[seed["ref"]] += 1
            choices, distractor_rows = make_choice_list(seed["correct_answer"], seed["distractors"])
            rule_ids = list(seed["rule_ids"])
            student_error_ids = linked_error_ids(rule_ids)
            template_id = None
            for rule_id in rule_ids:
                template_id = template_map.get((rule_id, "choose_translation")) or template_map.get((rule_id, "translate_word"))
                if template_id:
                    break
            blueprint, question = build_blueprint_and_question(
                context=context,
                index_within_ref=counters[seed["ref"]],
                lane="translation",
                skill_focus="basic_word_translation",
                question_type=question_type,
                target_hebrew=seed["target_hebrew"],
                source_words=seed["source_words"],
                prompt=prompt,
                choices=choices,
                correct_answer=seed["correct_answer"],
                accepted_answers=seed["accepted_answers"],
                distractor_rows=distractor_rows,
                feedback_correct=f"Correct. {seed['target_hebrew']} fits {seed['correct_answer']} here.",
                feedback_incorrect=(
                    f"Check {seed['target_hebrew']} against the source translations. "
                    f"The preview supports {', '.join(seed['accepted_answers'])} here."
                ),
                rule_ids=rule_ids,
                mastery_tags=list(seed["mastery_tags"]),
                difficulty_level=seed["difficulty_level"],
                student_error_pattern_ids=student_error_ids,
                template_id=template_id,
            )
            rows.append((blueprint, question))
    return rows


def dikduk_variants_for_seed(seed: dict[str, Any]) -> list[dict[str, Any]]:
    subtype = seed["subtype"]
    if subtype == "article":
        return [
            {
                "question_type": "identify_marker",
                "prompt": f"In the word {seed['target_hebrew']}, which letter adds the meaning 'the'?",
                "correct_answer": "ה",
                "accepted_answers": ["ה"],
                "distractors": [("א", "nearby letter distractor"), ("ר", "middle-letter distractor"), ("ץ", "final-letter distractor")],
            },
            {
                "question_type": "choose_translation",
                "prompt": f"Which translation best fits {seed['target_hebrew']}?",
                "correct_answer": seed["translation_with_rule"],
                "accepted_answers": [seed["translation_with_rule"]],
                "distractors": [
                    (seed["translation_with_rule"].replace("the ", "", 1), "drops the definite article"),
                    ("and " + seed["translation_with_rule"], "adds a conjunction that is not the target here"),
                    ("created", "unrelated creation verb distractor"),
                ],
            },
        ]
    if subtype == "conjunction":
        return [
            {
                "question_type": "identify_marker",
                "prompt": f"In the word {seed['target_hebrew']}, which letter adds the meaning 'and'?",
                "correct_answer": "ו",
                "accepted_answers": ["ו"],
                "distractors": [("ה", "article distractor"), ("א", "base-letter distractor"), ("ץ", "final-letter distractor")],
            },
            {
                "question_type": "translate_word",
                "prompt": f"Translate {seed['target_hebrew']} accurately, including any added conjunction meaning.",
                "correct_answer": seed["translation_with_rule"],
                "accepted_answers": [seed["translation_with_rule"]],
                "distractors": [
                    (seed["translation_with_rule"].replace("and ", "", 1), "omits the conjunction"),
                    ("earth", "drops both the conjunction and the article"),
                    ("with the earth", "turns the prefix into the wrong function"),
                ],
            },
        ]
    if subtype == "direct_object_marker":
        return [
            {
                "question_type": "identify_direct_object_marker",
                "prompt": f"What is the job of {seed['target_hebrew']} in this phrase?",
                "correct_answer": "It marks the direct object.",
                "accepted_answers": ["It marks the direct object."],
                "distractors": [
                    ("It means with.", "common function confusion distractor"),
                    ("It is the main noun.", "role confusion distractor"),
                    ("It means from.", "rare-sense distractor"),
                ],
            },
            {
                "question_type": "explain_rule",
                "prompt": f"Why is {seed['target_hebrew']} not translated as a separate English word here?",
                "correct_answer": "Because it marks the direct object instead of adding its own main English meaning.",
                "accepted_answers": ["Because it marks the direct object instead of adding its own main English meaning."],
                "distractors": [
                    ("Because it is always silent and can be ignored in every context.", "overbroad rule distractor"),
                    ("Because it always means with, even in direct-object phrases.", "function confusion distractor"),
                    ("Because it is part of the next noun itself.", "boundary confusion distractor"),
                ],
            },
        ]
    if subtype in {"prefix_b", "prefix_l"}:
        marker = "ב" if subtype == "prefix_b" else "ל"
        meaning_choices = ["in", "to / for", "from", "like"]
        correct_meaning = seed["correct_meaning"]
        distractors = [(choice, "other common prefix-preposition meaning") for choice in meaning_choices if choice != correct_meaning]
        letter_distractors = [("ב", "common prefix-preposition letter"), ("ל", "common prefix-preposition letter"), ("מ", "common prefix-preposition letter"), ("ו", "common conjunction letter")]
        return [
            {
                "question_type": "identify_preposition_meaning",
                "prompt": f"What does the prefixed {marker} add in {seed['target_hebrew']} here?",
                "correct_answer": correct_meaning,
                "accepted_answers": [correct_meaning],
                "distractors": distractors,
            },
            {
                "question_type": "identify_added_letters",
                "prompt": f"Which added letter should you notice first in {seed['target_hebrew']}?",
                "correct_answer": marker,
                "accepted_answers": [marker],
                "distractors": [item for item in letter_distractors if item[0] != marker],
            },
        ]
    if subtype == "plural_yim":
        return [
            {
                "question_type": "singular_or_plural",
                "prompt": f"Is {seed['target_hebrew']} singular or plural on the surface?",
                "correct_answer": "plural",
                "accepted_answers": ["plural"],
                "distractors": [
                    ("singular", "misses the plural ending"),
                    ("not a noun", "part-of-speech distractor"),
                    ("not enough information", "over-cautious distractor"),
                ],
            },
            {
                "question_type": "explain_rule",
                "prompt": f"Which ending in {seed['target_hebrew']} helps signal a common masculine plural?",
                "correct_answer": "ים",
                "accepted_answers": ["ים"],
                "distractors": [("ות", "feminine plural ending distractor"), ("ה", "article-like distractor"), ("את", "object marker distractor")],
            },
        ]
    if subtype == "plural_vav_tav":
        return [
            {
                "question_type": "singular_or_plural",
                "prompt": f"Is {seed['target_hebrew']} singular or plural on the surface?",
                "correct_answer": "plural",
                "accepted_answers": ["plural"],
                "distractors": [
                    ("singular", "misses the plural ending"),
                    ("not a noun", "part-of-speech distractor"),
                    ("not enough information", "over-cautious distractor"),
                ],
            },
            {
                "question_type": "explain_rule",
                "prompt": f"Which ending in {seed['target_hebrew']} helps signal a common feminine plural?",
                "correct_answer": "ות",
                "accepted_answers": ["ות"],
                "distractors": [("ים", "masculine plural ending distractor"), ("ה", "article-like distractor"), ("את", "object marker distractor")],
            },
        ]
    if subtype == "irregular_plural_warning":
        return [
            {
                "question_type": "choose_translation",
                "prompt": f"What is the safest basic translation for {seed['target_hebrew']} here?",
                "correct_answer": seed["safe_translation"],
                "accepted_answers": [seed["safe_translation"], "the water", "water"],
                "distractors": [
                    ("waters everywhere", "over-literal plural-only distractor"),
                    ("faces", "other classic caution-word distractor"),
                    ("lands", "ordinary English plural distractor"),
                ],
            },
            {
                "question_type": "explain_rule",
                "prompt": f"What caution should you remember when you translate {seed['target_hebrew']}?",
                "correct_answer": "It looks plural on the surface, but the English idea may still be singular in a simple context.",
                "accepted_answers": ["It looks plural on the surface, but the English idea may still be singular in a simple context."],
                "distractors": [
                    ("Every word ending in ים must always become a normal English plural.", "overgeneralization distractor"),
                    ("The word stops being a noun once it ends in ים.", "part-of-speech confusion distractor"),
                    ("The article ה cancels any translation caution.", "article overreach distractor"),
                ],
            },
        ]
    if subtype == "word_order":
        return [
            {
                "question_type": "reorder_translation",
                "prompt": f"Which English order sounds natural for {seed['target_hebrew']}?",
                "correct_answer": seed["natural_translation"],
                "accepted_answers": [seed["natural_translation"]],
                "distractors": [
                    ("said God", "too literal Hebrew-order distractor"),
                    ("God light", "broken clause distractor"),
                    ("light said God", "word-order confusion distractor"),
                ],
            },
            {
                "question_type": "explain_rule",
                "prompt": "What should you do when the Hebrew word order sounds unnatural in English?",
                "correct_answer": "Translate the meaning naturally after you identify the verb and the noun.",
                "accepted_answers": ["Translate the meaning naturally after you identify the verb and the noun."],
                "distractors": [
                    ("Copy the Hebrew order exactly, even when the English sounds unnatural.", "too literal distractor"),
                    ("Change the meaning freely so the English sounds smoother.", "overcorrection distractor"),
                    ("Ignore the verb and translate only the nouns.", "structure-loss distractor"),
                ],
            },
        ]
    if subtype == "verb_agreement":
        return [
            {
                "question_type": "explain_rule",
                "prompt": f"Which noun is {seed['target_hebrew'].split()[0]} matching in this clause?",
                "correct_answer": seed["matching_noun"],
                "accepted_answers": [seed["matching_noun"]],
                "distractors": [
                    ("המים", "other nearby creation noun distractor"),
                    ("האור", "other creation noun distractor"),
                    ("הלילה", "other creation noun distractor"),
                ],
            },
            {
                "question_type": "classify_part_of_speech",
                "prompt": f"What kind of clue does {seed['target_hebrew'].split()[0]} give you here?",
                "correct_answer": "It helps show a verb agreeing with its subject.",
                "accepted_answers": ["It helps show a verb agreeing with its subject."],
                "distractors": [
                    ("It is only a direct-object marker.", "function-word distractor"),
                    ("It is only a noun with no agreement clue.", "part-of-speech distractor"),
                    ("It is only a conjunction with no verb meaning.", "conjunction distractor"),
                ],
            },
        ]
    raise ValueError(f"Unsupported dikduk subtype: {subtype}")


def build_dikduk_rows(
    contexts: dict[str, RefContext],
    template_map: dict[tuple[str, str], str],
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    rows = []
    counters: defaultdict[str, int] = defaultdict(int)
    for seed in DIKDUK_TARGETS:
        context = contexts[seed["ref"]]
        ensure_source_grounded(context, seed["source_words"])
        variants = dikduk_variants_for_seed(seed)
        for variant in variants:
            counters[seed["ref"]] += 1
            choices, distractor_rows = make_choice_list(variant["correct_answer"], variant["distractors"])
            template_id = None
            for rule_id in seed["rule_ids"]:
                template_id = template_map.get((rule_id, variant["question_type"]))
                if template_id:
                    break
            blueprint, question = build_blueprint_and_question(
                context=context,
                index_within_ref=counters[seed["ref"]],
                lane="dikduk",
                skill_focus=seed["subtype"],
                question_type=variant["question_type"],
                target_hebrew=seed["target_hebrew"],
                source_words=seed["source_words"],
                prompt=variant["prompt"],
                choices=choices,
                correct_answer=variant["correct_answer"],
                accepted_answers=variant["accepted_answers"],
                distractor_rows=distractor_rows,
                feedback_correct=f"Correct. {seed['target_hebrew']} fits this rule clue.",
                feedback_incorrect="Look at the Hebrew form carefully. The preview is testing the added marker or form clue, not just a loose English gloss.",
                rule_ids=list(seed["rule_ids"]),
                mastery_tags=list(seed["mastery_tags"]),
                difficulty_level=seed["difficulty_level"],
                student_error_pattern_ids=linked_error_ids(seed["rule_ids"]),
                template_id=template_id,
            )
            rows.append((blueprint, question))
    return rows


def build_word_analysis_rows(
    contexts: dict[str, RefContext],
    template_map: dict[tuple[str, str], str],
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    rows = []
    counters: defaultdict[str, int] = defaultdict(int)
    for seed in WORD_ANALYSIS_TARGETS:
        context = contexts[seed["ref"]]
        ensure_source_grounded(context, seed["source_words"])
        variants = [
            {
                "question_type": "identify_shoresh",
                "prompt": f"What is the shoresh of {seed['target_hebrew']}?",
                "correct_answer": seed["shoresh"],
                "accepted_answers": [seed["shoresh"]],
                "distractors": [(choice, "other creation-verb shoresh distractor") for choice in seed["shoresh_choices"] if choice != seed["shoresh"]],
            },
            {
                "question_type": "identify_added_letters",
                "prompt": f"Which added letters should you notice in {seed['target_hebrew']} before you parse the whole form?",
                "correct_answer": seed["added_letters"],
                "accepted_answers": [seed["added_letters"]],
                "distractors": [(choice, "other prefix-pattern distractor") for choice in seed["added_letter_choices"] if choice != seed["added_letters"]],
            },
        ]
        for variant in variants:
            counters[seed["ref"]] += 1
            choices, distractor_rows = make_choice_list(variant["correct_answer"], variant["distractors"])
            template_id = None
            for rule_id in seed["rule_ids"]:
                template_id = template_map.get((rule_id, variant["question_type"]))
                if template_id:
                    break
            blueprint, question = build_blueprint_and_question(
                context=context,
                index_within_ref=counters[seed["ref"]],
                lane="word_analysis",
                skill_focus="verb_form_analysis",
                question_type=variant["question_type"],
                target_hebrew=seed["target_hebrew"],
                source_words=seed["source_words"],
                prompt=variant["prompt"],
                choices=choices,
                correct_answer=variant["correct_answer"],
                accepted_answers=variant["accepted_answers"],
                distractor_rows=distractor_rows,
                feedback_correct=f"Correct. {seed['target_hebrew']} needs both its shoresh and its added letters for a full parse.",
                feedback_incorrect="Start with the shoresh, then check the added letters before deciding what the full form means.",
                rule_ids=list(seed["rule_ids"]),
                mastery_tags=list(seed["mastery_tags"]),
                difficulty_level=seed["difficulty_level"],
                student_error_pattern_ids=linked_error_ids(seed["rule_ids"]),
                template_id=template_id,
            )
            rows.append((blueprint, question))
    return rows


def build_error_diagnosis_rows(
    contexts: dict[str, RefContext],
    error_index: dict[str, dict[str, Any]],
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    rows = []
    counters: defaultdict[str, int] = defaultdict(int)
    for seed in ERROR_DIAGNOSIS_TARGETS:
        context = contexts[seed["ref"]]
        ensure_source_grounded(context, seed["source_words"])
        correct_error = error_index[seed["correct_error_id"]]
        distractors = [
            (error_index[error_id]["diagnosis"], f"distractor from {error_id}")
            for error_id in seed["distractor_error_ids"]
        ]
        counters[seed["ref"]] += 1
        choices, distractor_rows = make_choice_list(correct_error["diagnosis"], distractors)
        blueprint, question = build_blueprint_and_question(
            context=context,
            index_within_ref=counters[seed["ref"]],
            lane="error_diagnosis",
            skill_focus="error_diagnosis",
            question_type="choose_feedback",
            target_hebrew=seed["target_hebrew"],
            source_words=seed["source_words"],
            prompt=(
                f"A student answered {seed['wrong_answer']!r} for {seed['target_hebrew']} in {seed['ref']}. "
                "Which diagnostic note fits best?"
            ),
            choices=choices,
            correct_answer=correct_error["diagnosis"],
            accepted_answers=[correct_error["diagnosis"]],
            distractor_rows=distractor_rows,
            feedback_correct=f"Correct. The linked error pattern is {seed['correct_error_id']}.",
            feedback_incorrect=correct_error["remediation_hint"],
            rule_ids=list(correct_error["linked_rule_ids"]),
            mastery_tags=list(seed["mastery_tags"]),
            difficulty_level=seed["difficulty_level"],
            student_error_pattern_ids=[seed["correct_error_id"], *seed["distractor_error_ids"]],
            template_id=None,
        )
        rows.append((blueprint, question))
    return rows


def build_translation_comparison_rows(
    contexts: dict[str, RefContext],
    template_map: dict[tuple[str, str], str],
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    rows = []
    counters: defaultdict[str, int] = defaultdict(int)
    for seed in TRANSLATION_COMPARISON_TARGETS:
        context = contexts[seed["ref"]]
        ensure_source_grounded(context, seed["source_words"])
        counters[seed["ref"]] += 1
        choices, distractor_rows = make_choice_list(seed["correct_answer"], seed["distractors"])
        rule_ids = list(seed["rule_ids"])
        template_id = None
        for rule_id in rule_ids:
            template_id = template_map.get((rule_id, "choose_translation"))
            if template_id:
                break
        blueprint, question = build_blueprint_and_question(
            context=context,
            index_within_ref=counters[seed["ref"]],
            lane="translation_comparison",
            skill_focus="mixed_skill_translation_rule",
            question_type="choose_translation",
            target_hebrew=seed["target_hebrew"],
            source_words=seed["source_words"],
            prompt=(
                f"Which translation best fits {seed['target_hebrew']} here while staying consistent "
                "with the source translations used in this preview?"
            ),
            choices=choices,
            correct_answer=seed["correct_answer"],
            accepted_answers=seed["accepted_answers"],
            distractor_rows=distractor_rows,
            feedback_correct=f"Correct. The preview will accept {', '.join(seed['accepted_answers'])} for this source-backed item.",
            feedback_incorrect="Use the Hebrew form together with the two source translations. The preview is preserving allowed English variants, not promoting a runtime answer key yet.",
            rule_ids=rule_ids,
            mastery_tags=list(seed["mastery_tags"]),
            difficulty_level=seed["difficulty_level"],
            student_error_pattern_ids=linked_error_ids(rule_ids),
            template_id=template_id,
        )
        rows.append((blueprint, question))
    return rows


def build_preview_records(config: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    contexts = build_ref_contexts(config)
    template_map = build_rule_template_map()
    error_index = build_error_index()
    registry = translation_sources_loader.load_translation_registry()
    available_versions = set(translation_sources_loader.get_available_translation_versions())
    if {"koren", "metsudah"} - available_versions:
        raise ValueError("Translation registry must expose both koren and metsudah.")

    blueprint_question_pairs: list[tuple[dict[str, Any], dict[str, Any]]] = []
    blueprint_question_pairs.extend(build_translation_rows(contexts, template_map))
    blueprint_question_pairs.extend(build_dikduk_rows(contexts, template_map))
    blueprint_question_pairs.extend(build_word_analysis_rows(contexts, template_map))
    blueprint_question_pairs.extend(build_error_diagnosis_rows(contexts, error_index))
    blueprint_question_pairs.extend(build_translation_comparison_rows(contexts, template_map))

    blueprints = [pair[0] for pair in blueprint_question_pairs]
    questions = [pair[1] for pair in blueprint_question_pairs]
    reassign_preview_ids(blueprints, questions)
    summary = build_summary_payload(config, contexts, blueprints, questions, registry)
    return blueprints, questions, summary


def reassign_preview_ids(blueprints: list[dict[str, Any]], questions: list[dict[str, Any]]) -> None:
    counters: defaultdict[str, int] = defaultdict(int)
    for blueprint, question in zip(blueprints, questions):
        ref = question["ref"]
        perek, pasuk = parse_ref(ref)
        counters[ref] += 1
        index_within_ref = counters[ref]
        blueprint_id = f"DP-BER-{perek:03d}-{pasuk:03d}-{index_within_ref:03d}"
        question_id = f"DQ-BER-{perek:03d}-{pasuk:03d}-{index_within_ref:03d}"
        blueprint["blueprint_id"] = blueprint_id
        question["blueprint_id"] = blueprint_id
        question["question_id"] = question_id


def build_summary_payload(
    config: dict[str, Any],
    contexts: dict[str, RefContext],
    blueprints: list[dict[str, Any]],
    questions: list[dict[str, Any]],
    registry: dict[str, Any],
) -> dict[str, Any]:
    lane_counts = Counter(question["diagnostic_lane"] for question in questions)
    skill_counts = Counter(question["skill_focus"] for question in questions)
    mastery_counts: Counter[str] = Counter()
    difficulty_counts: Counter[str] = Counter()
    used_rule_ids: set[str] = set()
    for question in questions:
        mastery_counts.update(question["mastery_tags"])
        difficulty_counts[str(question["difficulty_level"])] += 1
        used_rule_ids.update(question["dikduk_rule_ids"])

    selected_versions = registry.get("available_translation_versions", [])
    translations_used = [
        {
            "translation_version_key": entry["translation_version_key"],
            "translation_version_title": entry["translation_version_title"],
            "license": entry["license"],
            "license_status": entry["license_status"],
        }
        for entry in selected_versions
        if entry["translation_version_key"] in {"koren", "metsudah"}
    ]
    warnings = [
        "Preview questions use English translations only in a non-runtime source-preview layer.",
        "All translation-backed questions remain source_preview_only_license_review_required.",
        "Nothing in this preview is production-approved or runtime-active.",
    ]
    blocked_items: list[str] = []
    return {
        "schema_version": "1.0",
        "preview_id": config["preview_id"],
        "range_covered": {
            "sefer": config["sefer"],
            "start_ref": config["start_ref"],
            "end_ref": config["end_ref"],
            "pesukim_covered": len(contexts),
        },
        "total_blueprints": len(blueprints),
        "total_questions": len(questions),
        "question_count_by_lane": dict(sorted(lane_counts.items())),
        "question_count_by_skill": dict(sorted(skill_counts.items())),
        "question_count_by_mastery_tag": dict(sorted(mastery_counts.items())),
        "question_count_by_difficulty": dict(sorted(difficulty_counts.items(), key=lambda item: int(item[0]))),
        "rules_used": sorted(used_rule_ids),
        "translations_used": translations_used,
        "warnings": warnings,
        "blocked_items": blocked_items,
        "ready_for_human_review": [
            "blueprint JSONL",
            "preview question JSONL",
            "manual review packet",
            "summary reports",
        ],
        "not_ready_for_runtime": [
            "translation content still requires human license review",
            "questions remain preview_only and not runtime_active",
            "no reviewed-bank promotion or student-facing runtime integration has been done",
        ],
        "generated_at": utc_now_iso(),
        "status": PREVIEW_STATUS,
        "runtime_status": RUNTIME_STATUS,
        "production_status": PRODUCTION_STATUS,
    }


def write_manual_review_packet(
    path: Path,
    questions: list[dict[str, Any]],
    blueprints_by_id: dict[str, dict[str, Any]],
    error_index: dict[str, dict[str, Any]],
) -> None:
    lines = [
        "# Bereishis 1:1-2:3 Diagnostic Preview Manual Review Packet",
        "",
        f"Status: `{PREVIEW_STATUS}`",
        f"Runtime status: `{RUNTIME_STATUS}`",
        f"Production status: `{PRODUCTION_STATUS}`",
        f"Translation usage status: `{TRANSLATION_USAGE_STATUS}`",
        "",
        "Reviewer recommendation options:",
        "- `accept`",
        "- `accept_with_edit`",
        "- `reject`",
        "- `needs_source_review`",
        "- `needs_translation_review`",
        "- `needs_dikduk_review`",
        "",
    ]
    lines.extend(preserved_manual_review_findings(path))
    questions_by_ref: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for question in questions:
        questions_by_ref[question["ref"]].append(question)

    for ref in sorted(questions_by_ref, key=parse_ref):
        questions_for_ref = sorted(
            questions_by_ref[ref],
            key=lambda item: (item["diagnostic_lane"], item["skill_focus"], item["question_id"]),
        )
        blueprint = blueprints_by_id[questions_for_ref[0]["blueprint_id"]]
        lines.extend(
            [
                f"## {ref} / {blueprint['hebrew_ref']}",
                "",
                f"Hebrew source: {blueprint['hebrew_text']}",
                f"Koren: {blueprint['koren_translation']}",
                f"Metsudah: {blueprint['metsudah_translation']}",
                "",
            ]
        )
        for question in questions_for_ref:
            blueprint = blueprints_by_id[question["blueprint_id"]]
            error_notes = [
                error_index[error_id]["diagnosis"]
                for error_id in question.get("student_error_pattern_ids", [])
                if error_id in error_index
            ]
            likely_mistake = error_notes[0] if error_notes else "No explicit linked student error pattern."
            lines.extend(
                [
                    f"### {question['question_id']}",
                    f"- Skill: `{question['skill_focus']}`",
                    f"- Diagnostic lane: `{question['diagnostic_lane']}`",
                    f"- Difficulty: `{question['difficulty_level']}`",
                    f"- Mastery tags: {', '.join(question['mastery_tags'])}",
                    f"- Rule IDs: {', '.join(question['dikduk_rule_ids']) if question['dikduk_rule_ids'] else 'None'}",
                    f"- Prompt: {question['prompt']}",
                    f"- Choices: {', '.join(question['choices'])}",
                    f"- Correct answer: {question['correct_answer']}",
                    f"- Accepted answers: {', '.join(question['accepted_answers'])}",
                    f"- Likely student mistake if wrong: {likely_mistake}",
                    "- Reviewer comment:",
                    "- Recommendation:",
                    "",
                ]
            )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_summary_markdown(path: Path, summary: dict[str, Any]) -> None:
    lines = [
        "# Bereishis 1:1-2:3 Diagnostic Preview Summary",
        "",
        f"Range covered: {summary['range_covered']['start_ref']} to {summary['range_covered']['end_ref']}",
        f"Pesukim covered: {summary['range_covered']['pesukim_covered']}",
        f"Total blueprints: {summary['total_blueprints']}",
        f"Total questions: {summary['total_questions']}",
        "",
        "Question count by lane:",
    ]
    for key, value in summary["question_count_by_lane"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "Question count by skill:"])
    for key, value in summary["question_count_by_skill"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "Question count by mastery tag:"])
    for key, value in summary["question_count_by_mastery_tag"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "Question count by difficulty:"])
    for key, value in summary["question_count_by_difficulty"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "Rules used:",
            *[f"- {rule_id}" for rule_id in summary["rules_used"]],
            "",
            "Translations used:",
        ]
    )
    for translation in summary["translations_used"]:
        lines.append(
            f"- {translation['translation_version_key']}: {translation['translation_version_title']} "
            f"({translation['license']}, {translation['license_status']})"
        )
    lines.extend(["", "Warnings:"])
    for warning in summary["warnings"]:
        lines.append(f"- {warning}")
    lines.extend(["", "Blocked items:"])
    if summary["blocked_items"]:
        for item in summary["blocked_items"]:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.extend(["", "Ready for human review:"])
    for item in summary["ready_for_human_review"]:
        lines.append(f"- {item}")
    lines.extend(["", "Not ready for runtime:"])
    for item in summary["not_ready_for_runtime"]:
        lines.append(f"- {item}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def reviewable_preview_paths() -> dict[str, Path]:
    return {
        "questions": REPO_ROOT / REVIEWABLE_PREVIEW_QUESTIONS_RELATIVE,
        "manual_review_packet": REPO_ROOT / REVIEWABLE_PREVIEW_PACKET_RELATIVE,
        "summary_json": REPO_ROOT / REVIEWABLE_PREVIEW_SUMMARY_RELATIVE,
    }


def reviewable_difficulty_label(difficulty_level: int) -> str:
    if difficulty_level <= 1:
        return "easy"
    if difficulty_level == 2:
        return "medium"
    return "hard"


def reviewable_skill_category(question: dict[str, Any]) -> str:
    question_type = question["question_type"]
    skill_focus = question["skill_focus"]
    if question["diagnostic_lane"] == "translation_comparison" or skill_focus == "mixed_skill_translation_rule":
        return "translation"
    if question_type == "identify_shoresh":
        return "shoresh"
    if skill_focus in {"article", "conjunction", "prefix_b", "prefix_l"} or question_type == "identify_marker":
        return "prefix"
    if skill_focus in {"plural_yim", "plural_vav_tav", "irregular_plural_warning"} or question_type == "singular_or_plural":
        return "number"
    if skill_focus == "direct_object_marker":
        return "phrase_meaning"
    if skill_focus == "word_order":
        return "pasuk_comprehension"
    if skill_focus == "verb_agreement":
        return "verb"
    if skill_focus == "basic_word_translation":
        return "translation"
    return "dikduk"


def reviewable_translation_alignment_status(question_id: str) -> str:
    return REVIEWABLE_TRANSLATION_ALIGNMENT_OVERRIDES.get(question_id, "koren_and_metsudah_align")


def reviewable_primary_rule_id(question: dict[str, Any]) -> str | None:
    if question["question_id"] in REVIEWABLE_PRIMARY_RULE_OVERRIDES:
        return REVIEWABLE_PRIMARY_RULE_OVERRIDES[question["question_id"]]
    rule_ids = question.get("dikduk_rule_ids", [])
    return rule_ids[0] if rule_ids else None


def reviewable_primary_error_id(
    question: dict[str, Any],
    error_index: dict[str, dict[str, Any]],
    primary_rule_id: str | None,
) -> str | None:
    if question["question_id"] in REVIEWABLE_PRIMARY_ERROR_OVERRIDES:
        return REVIEWABLE_PRIMARY_ERROR_OVERRIDES[question["question_id"]]
    error_ids = question.get("student_error_pattern_ids", [])
    if error_ids:
        return error_ids[0]
    if primary_rule_id:
        for error_id, error_record in error_index.items():
            if primary_rule_id in error_record.get("linked_rule_ids", []):
                return error_id
    return None


def reviewable_flags(question_id: str) -> list[str]:
    flags: list[str] = []
    if question_id in REVIEWABLE_TOO_EASY_IDS:
        flags.append("too_easy")
    if question_id in REVIEWABLE_CAUTION_IDS:
        if question_id in REVIEWABLE_TRANSLATION_ALIGNMENT_OVERRIDES:
            flags.append("translation_sensitive")
        if question_id in REVIEWABLE_POSSIBLE_MULTIPLE_ANSWER_IDS:
            flags.append("possible_multiple_correct_answers")
    if question_id in REVIEWABLE_DEPENDS_ON_UNINTRODUCED_KNOWLEDGE_IDS:
        flags.append("depends_on_unintroduced_knowledge")
    if question_id == "DQ-BER-001-012-001":
        flags.append("too_hard")
    if question_id not in REVIEWABLE_CAUTION_IDS:
        flags.append("good_student_candidate")
    return sorted(dict.fromkeys(flags))


def reviewable_priority(question_id: str) -> str:
    if question_id in REVIEWABLE_HIGH_PRIORITY_IDS:
        return "high"
    if question_id in REVIEWABLE_CAUTION_IDS:
        return "medium"
    return "low"


def reviewable_likely_status(question_id: str) -> str:
    if question_id in REVIEWABLE_CAUTION_IDS:
        return "caution"
    return "likely_approve"


def reviewable_student_risk(question_id: str) -> str:
    if question_id in {"DQ-BER-001-006-001", "DQ-BER-001-012-001"}:
        return "high"
    if question_id in REVIEWABLE_CAUTION_IDS:
        return "medium"
    return "low"


def reviewable_teacher_note(question_id: str, hebrew_word_or_phrase: str) -> str:
    special_notes = {
        "DQ-BER-001-002-001": "Keep the accepted-answer policy broad enough to cover water/waters before using this outside adult review.",
        "DQ-BER-001-006-001": "Review whether the packet should allow firmament, canopy, or both before carrying this item into any locked subset.",
        "DQ-BER-001-009-001": "Decide whether dry land and dryness should both remain acceptable at preview stage.",
        "DQ-BER-001-003-003": "Use only if the teacher wants students to practice natural English reordering explicitly.",
        "DQ-BER-001-012-001": "Check that subject-verb agreement has already been introduced before using this with learners.",
        "DQ-BER-001-015-001": "Confirm that parsing להאיר as a shoresh item fits the class level before moving it forward.",
    }
    if question_id in special_notes:
        return special_notes[question_id]
    return f"This is a strong review-first candidate for {hebrew_word_or_phrase} because the answer is direct and the support is easy to verify."


def reviewable_generation_reason(question_id: str, hebrew_word_or_phrase: str) -> str:
    if question_id in REVIEWABLE_CAUTION_IDS:
        return (
            f"This question was kept because {hebrew_word_or_phrase} is instructionally valuable, "
            "but it needs teacher review before any locked subset because the wording or support is more delicate."
        )
    return (
        f"This question was kept because it gives one clear, student-facing check on {hebrew_word_or_phrase} "
        "without the weaker duplicate prompt from the larger preview set."
    )


def reviewable_test_summary(question: dict[str, Any], hebrew_word_or_phrase: str) -> str:
    category = reviewable_skill_category(question)
    if category == "translation":
        return f"This tests whether the student can translate {hebrew_word_or_phrase} correctly in the pasuk."
    if category == "prefix":
        return f"This tests whether the student notices how an added letter changes the meaning of {hebrew_word_or_phrase}."
    if category == "number":
        return f"This tests whether the student can recognize the number clue inside {hebrew_word_or_phrase}."
    if category == "shoresh":
        return f"This tests whether the student can identify the shoresh inside {hebrew_word_or_phrase}."
    if category == "phrase_meaning":
        return f"This tests whether the student can explain the function of {hebrew_word_or_phrase} inside the phrase."
    if category == "pasuk_comprehension":
        return "This tests whether the student can translate the clause naturally rather than copying Hebrew order mechanically."
    if category == "verb":
        return f"This tests whether the student can track what {hebrew_word_or_phrase} is doing in the clause."
    return f"This tests a focused grammar skill connected to {hebrew_word_or_phrase}."


def reviewable_student_explanation(
    question: dict[str, Any],
    hebrew_word_or_phrase: str,
    correct_answer: str,
    primary_rule: dict[str, Any] | None,
) -> str:
    question_type = question["question_type"]
    if question_type in {"choose_translation", "identify_word_meaning", "translate_word"}:
        return f"In this pasuk, {hebrew_word_or_phrase} means {correct_answer}."
    if question_type == "identify_marker":
        return f"The letter {correct_answer} is the added marker the question is asking about."
    if question_type == "identify_direct_object_marker":
        return f"Here {hebrew_word_or_phrase} marks the direct object instead of naming a separate thing."
    if question_type == "identify_preposition_meaning":
        return f"In this pasuk, the added letter contributes the meaning {correct_answer}."
    if question_type == "singular_or_plural":
        return f"The form of {hebrew_word_or_phrase} shows {correct_answer} on the surface."
    if question_type == "explain_rule":
        return correct_answer
    if question_type == "identify_shoresh":
        return f"The base shoresh inside {hebrew_word_or_phrase} is {correct_answer}."
    if question_type == "reorder_translation":
        return f"Hebrew says the clause in a different order, but natural English here is {correct_answer}."
    if question_type == "classify_part_of_speech":
        return correct_answer
    if primary_rule:
        return primary_rule["student_facing_rule"]
    return f"The correct answer fits the Hebrew word or phrase {hebrew_word_or_phrase} in this pasuk."


def reviewable_correct_answer_note(
    question: dict[str, Any],
    hebrew_word_or_phrase: str,
    translation_alignment_status: str,
    primary_rule: dict[str, Any] | None,
) -> str:
    if translation_alignment_status == "koren_and_metsudah_align":
        return (
            f"The exact Hebrew target {hebrew_word_or_phrase} appears in the pasuk, and both Koren and Metsudah "
            f"support the keyed answer {question['correct_answer']!r}."
        )
    if translation_alignment_status == "minor_translation_difference":
        return (
            f"The Hebrew target {hebrew_word_or_phrase} is clear, but Koren and Metsudah use slightly different "
            "English wording, so the reviewer should confirm that the accepted-answer list stays broad enough."
        )
    if translation_alignment_status == "significant_translation_difference":
        return (
            f"The Hebrew target {hebrew_word_or_phrase} is present, but Koren and Metsudah diverge more sharply here, "
            "so the item stays in review even though it may still be instructionally useful."
        )
    if primary_rule:
        return (
            f"The Hebrew target {hebrew_word_or_phrase} appears in the pasuk and the keyed answer matches the linked "
            f"rule {primary_rule['rule_id']} ({primary_rule['skill_name']})."
        )
    return f"The Hebrew target {hebrew_word_or_phrase} appears directly in the pasuk and supports the keyed answer."


def reviewable_source_support_note(
    hebrew_word_or_phrase: str,
    translation_alignment_status: str,
) -> str:
    if translation_alignment_status == "koren_and_metsudah_align":
        return (
            f"The exact Hebrew target {hebrew_word_or_phrase} is present in the verse, and both translation sources "
            "support the same classroom-level meaning."
        )
    if translation_alignment_status == "minor_translation_difference":
        return (
            f"The exact Hebrew target {hebrew_word_or_phrase} is present in the verse, but Koren and Metsudah vary "
            "slightly in English wording, so the item is flagged for review."
        )
    if translation_alignment_status == "significant_translation_difference":
        return (
            f"The Hebrew target {hebrew_word_or_phrase} is present in the verse, but the two translations differ "
            "enough that this question must remain teacher-reviewed."
        )
    return (
        f"The exact Hebrew target {hebrew_word_or_phrase} is present in the verse, but the English support should be "
        "checked by a teacher before any tighter answer policy is locked."
    )


def reviewable_distractor_explanation(
    distractor_text: str,
    reason: str,
    hebrew_word_or_phrase: str,
) -> str:
    reason_map = {
        "common creation verb distractor": "This is a different verb from the creation story, not the meaning of the tested word.",
        "another nearby creation verb distractor": "This is a different nearby creation verb, not the tested word in this pasuk.",
        "another creation-sequence verb distractor": "This is a different action from the creation sequence, not the target word here.",
        "nearby creation noun distractor": "This is a different nearby creation noun, not the tested word in this pasuk.",
        "high-frequency creation noun distractor": "This is a common creation noun from the wider narrative, not the meaning of the tested word here.",
        "paired creation noun distractor": "This is the paired noun in the verse, not the target being tested.",
        "nearby paired noun distractor": "This names the paired noun nearby, not the Hebrew target the question asks about.",
        "other creation noun distractor": "This is another creation noun, but it is not the meaning or function of the tested word.",
        "other verse noun distractor": "This appears elsewhere in the verse, but it is not the target word being asked about.",
        "nearby verse noun distractor": "This noun belongs to the same verse, but not to the tested Hebrew word.",
        "paired opposite noun distractor": "This is the opposite or paired term, not the meaning of the target word.",
        "other creation adjective distractor": "This adjective belongs elsewhere in the creation story, not to the tested word.",
        "surface-form distractor": "This follows the outer look of the letters, but not the real meaning in this pasuk.",
        "nearby imperative distractor": "This is a different nearby command, not the target command here.",
        "other prefix-pattern distractor": "These letters do not match the actual added letters in the form being analyzed.",
        "other creation-verb shoresh distractor": "This is the shoresh of a different nearby verb, not the base root of the tested form.",
        "other nearby creation noun distractor": "This is a different nearby creation noun, not the target meaning.",
    }
    explanation = reason_map.get(reason, f"This choice is not supported by the Hebrew target {hebrew_word_or_phrase} in this pasuk.")
    return f"{distractor_text}: {explanation}"


def build_reviewable_preview_records(
    blueprints: list[dict[str, Any]],
    questions: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    blueprint_by_id = {record["blueprint_id"]: record for record in blueprints}
    question_by_id = {record["question_id"]: record for record in questions}
    rule_index = dikduk_rules_loader.dikduk_rule_index()
    error_index = build_error_index()
    reviewable_questions: list[dict[str, Any]] = []

    for original_question_id in REVIEWABLE_SELECTED_QUESTION_IDS:
        question = question_by_id[original_question_id]
        blueprint = blueprint_by_id[question["blueprint_id"]]
        hebrew_word_or_phrase = blueprint["source_words"][0]
        perek, pasuk = parse_ref(question["ref"])
        difficulty_level = reviewable_difficulty_label(int(question["difficulty_level"]))
        skill_category = reviewable_skill_category(question)
        translation_alignment_status = reviewable_translation_alignment_status(original_question_id)
        primary_rule_id = reviewable_primary_rule_id(question)
        primary_rule = rule_index.get(primary_rule_id) if primary_rule_id else None
        primary_error_id = reviewable_primary_error_id(question, error_index, primary_rule_id)
        primary_error = error_index.get(primary_error_id) if primary_error_id else None
        distractor_note_map = {
            item["text"]: reviewable_distractor_explanation(item["text"], item["reason"], hebrew_word_or_phrase)
            for item in question.get("distractors", [])
        }
        reviewable_questions.append(
            {
                "question_id": question["question_id"].replace("DQ-", "RVP-"),
                "source_preview_question_id": question["question_id"],
                "source_blueprint_id": question["blueprint_id"],
                "sefer": "Bereishis",
                "perek": perek,
                "pasuk": pasuk,
                "ref": question["ref"],
                "question_text": question["prompt"],
                "answer_choices": list(question["choices"]),
                "correct_answer": question["correct_answer"],
                "student_explanation": reviewable_student_explanation(
                    question,
                    hebrew_word_or_phrase,
                    question["correct_answer"],
                    primary_rule,
                ),
                "difficulty_level": difficulty_level,
                "skill_category": skill_category,
                "hebrew_word_or_phrase": hebrew_word_or_phrase,
                "hebrew_context": blueprint["hebrew_text"],
                "koren_translation_support": blueprint["koren_translation"],
                "metsudah_translation_support": blueprint["metsudah_translation"],
                "translation_alignment_status": translation_alignment_status,
                "source_support_note": reviewable_source_support_note(
                    hebrew_word_or_phrase,
                    translation_alignment_status,
                ),
                "dikduk_rule_id": primary_rule_id,
                "dikduk_rule_name": primary_rule["skill_name"] if primary_rule else None,
                "dikduk_rule_summary": primary_rule["student_facing_rule"] if primary_rule else "No direct dikduk rule linkage; this item is kept for source-backed reviewable meaning work.",
                "student_error_pattern_id": primary_error_id,
                "student_error_pattern_summary": primary_error["diagnosis"] if primary_error else "No single linked student error pattern; this item is mainly checking direct comprehension or vocabulary accuracy.",
                "review_priority": reviewable_priority(original_question_id),
                "likely_review_status": reviewable_likely_status(original_question_id),
                "review_flags": reviewable_flags(original_question_id),
                "why_this_question_was_generated": reviewable_generation_reason(
                    original_question_id,
                    hebrew_word_or_phrase,
                ),
                "what_the_question_tests": reviewable_test_summary(question, hebrew_word_or_phrase),
                "why_the_correct_answer_is_correct": reviewable_correct_answer_note(
                    question,
                    hebrew_word_or_phrase,
                    translation_alignment_status,
                    primary_rule,
                ),
                "why_each_distractor_is_wrong": {
                    choice: distractor_note_map.get(
                        choice,
                        f"{choice}: This option is not supported by the Hebrew target {hebrew_word_or_phrase} in this pasuk.",
                    )
                    for choice in question["choices"]
                    if choice != question["correct_answer"]
                },
                "possible_alternate_answers": [
                    answer for answer in question.get("accepted_answers", []) if answer != question["correct_answer"]
                ],
                "teacher_review_note": reviewable_teacher_note(original_question_id, hebrew_word_or_phrase),
                "student_readiness_risk": reviewable_student_risk(original_question_id),
                "status": PREVIEW_STATUS,
                "runtime_status": REVIEWABLE_RUNTIME_STATUS,
                "production_status": REVIEWABLE_PRODUCTION_STATUS,
                "translation_usage_status": TRANSLATION_USAGE_STATUS,
            }
        )

    summary = build_reviewable_preview_summary(reviewable_questions)
    return reviewable_questions, summary


def build_reviewable_preview_summary(reviewable_questions: list[dict[str, Any]]) -> dict[str, Any]:
    skill_counts = Counter(question["skill_category"] for question in reviewable_questions)
    difficulty_counts = Counter(question["difficulty_level"] for question in reviewable_questions)
    likely_review_status_counts = Counter(question["likely_review_status"] for question in reviewable_questions)
    review_flag_counts: Counter[str] = Counter()
    for question in reviewable_questions:
        review_flag_counts.update(question["review_flags"])
    translation_alignment_counts = Counter(
        question["translation_alignment_status"] for question in reviewable_questions
    )
    risk_counts = Counter(question["student_readiness_risk"] for question in reviewable_questions)
    unique_refs = sorted({question["ref"] for question in reviewable_questions}, key=parse_ref)
    top_review_risks = [
        "Translation-sensitive English wording around המים, היבשה, and רקיע.",
        "A few grammar questions still assume lesson context, especially subject-verb agreement and abstract word-order awareness.",
        "Some beginner items may be too easy and should stay warm-up only if they remain in the packet.",
    ]
    strongest_patterns = [
        "Direct word meaning questions with one clearly supported answer.",
        "Definite-article and conjunction recognition with exact Hebrew support.",
        "Simple shoresh-identification questions on common creation verbs.",
        "Plural-recognition questions where the surface ending is easy for a teacher to verify.",
    ]
    weakest_patterns = [
        "Translation-sensitive words with legitimate English variation.",
        "Questions that require more lesson context than a standalone preview should assume.",
    ]
    return {
        "schema_version": "1.0",
        "preview_id": "bereishis_1_1_to_2_3_reviewable_preview",
        "range": {
            "sefer": "Bereishis",
            "start_ref": "Genesis 1:1",
            "end_ref": "Genesis 2:3",
            "refs_with_questions": unique_refs,
            "pesukim_with_questions": len(unique_refs),
        },
        "total_questions": len(reviewable_questions),
        "skill_counts": dict(sorted(skill_counts.items())),
        "difficulty_counts": {
            key: difficulty_counts.get(key, 0) for key in ("easy", "medium", "hard")
        },
        "likely_review_status_counts": {
            key: likely_review_status_counts.get(key, 0) for key in ("likely_approve", "caution", "likely_rewrite")
        },
        "review_flag_counts": dict(sorted(review_flag_counts.items())),
        "translation_alignment_counts": {
            key: translation_alignment_counts.get(key, 0)
            for key in (
                "koren_and_metsudah_align",
                "minor_translation_difference",
                "significant_translation_difference",
                "translation_review_required",
            )
        },
        "low_risk_student_candidate_count": risk_counts.get("low", 0),
        "medium_risk_count": risk_counts.get("medium", 0),
        "high_risk_count": risk_counts.get("high", 0),
        "top_review_risks": top_review_risks,
        "strongest_question_patterns": strongest_patterns,
        "weakest_question_patterns": weakest_patterns,
        "recommended_next_step": (
            "Teacher-review the high-priority caution items first, then lock the likely_approve subset "
            "into a non-runtime candidate packet."
        ),
        "final_recommendation": REVIEWABLE_PREVIEW_FINAL_RECOMMENDATION,
        "status": PREVIEW_STATUS,
        "runtime_status": REVIEWABLE_RUNTIME_STATUS,
        "production_status": REVIEWABLE_PRODUCTION_STATUS,
        "translation_usage_status": TRANSLATION_USAGE_STATUS,
        "generated_at": utc_now_iso(),
    }


def write_reviewable_manual_review_packet(path: Path, reviewable_questions: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    lines = [
        "# Bereishis 1:1-2:3 Reviewable Diagnostic Preview Manual Review Packet",
        "",
        f"Final recommendation: `{summary['final_recommendation']}`",
        f"Status: `{summary['status']}`",
        f"Runtime status: `{summary['runtime_status']}`",
        f"Production status: `{summary['production_status']}`",
        f"Translation usage status: `{summary['translation_usage_status']}`",
        "",
        "## Packet Snapshot",
        f"- Total generated questions: {summary['total_questions']}",
        f"- Count by skill category: {json.dumps(summary['skill_counts'], ensure_ascii=False, sort_keys=True)}",
        f"- Count by difficulty: {json.dumps(summary['difficulty_counts'], ensure_ascii=False, sort_keys=True)}",
        f"- Count by likely review status: {json.dumps(summary['likely_review_status_counts'], ensure_ascii=False, sort_keys=True)}",
        f"- Count by review flag: {json.dumps(summary['review_flag_counts'], ensure_ascii=False, sort_keys=True)}",
        "",
        "Top review risks:",
        *[f"- {item}" for item in summary["top_review_risks"]],
        "",
        "Strongest question patterns:",
        *[f"- {item}" for item in summary["strongest_question_patterns"]],
        "",
        "Weakest question patterns:",
        *[f"- {item}" for item in summary["weakest_question_patterns"]],
        "",
        "Recommendation for next step:",
        f"- {summary['recommended_next_step']}",
        "",
    ]

    high_priority = [
        question for question in reviewable_questions if question["review_priority"] == "high"
    ]
    likely_approve = [
        question
        for question in reviewable_questions
        if question["review_priority"] != "high" and question["likely_review_status"] == "likely_approve"
    ]
    caution = [
        question for question in reviewable_questions if question["likely_review_status"] != "likely_approve"
    ]
    sections = [
        ("High-priority review", high_priority),
        ("Likely approve", likely_approve),
        ("Caution / likely rewrite", caution),
    ]
    for section_title, items in sections:
        lines.extend([f"## {section_title}", ""])
        if not items:
            lines.extend(["- none", ""])
            continue
        for question in sorted(items, key=lambda row: (parse_ref(row["ref"]), row["question_id"])):
            lines.extend(
                [
                    f"### {question['question_id']}",
                    f"- Ref: {question['ref']}",
                    f"- Hebrew tested: {question['hebrew_word_or_phrase']}",
                    f"- Skill: {question['skill_category']}",
                    f"- Difficulty: {question['difficulty_level']}",
                    f"- Student question: {question['question_text']}",
                    f"- Choices: {', '.join(question['answer_choices'])}",
                    f"- Correct answer: {question['correct_answer']}",
                    f"- Student explanation: {question['student_explanation']}",
                    f"- Source support: {question['source_support_note']}",
                    f"- Koren support: {question['koren_translation_support']}",
                    f"- Metsudah support: {question['metsudah_translation_support']}",
                    f"- Dikduk rule: {question['dikduk_rule_id'] or 'None'} - {question['dikduk_rule_name'] or 'No direct dikduk rule linkage'}",
                    f"- Error pattern: {question['student_error_pattern_id'] or 'None'} - {question['student_error_pattern_summary']}",
                    f"- Why generated: {question['why_this_question_was_generated']}",
                    f"- Reviewer concern flags: {', '.join(question['review_flags']) if question['review_flags'] else 'none'}",
                    f"- Suggested review status: {question['likely_review_status']}",
                    "- Teacher checkbox:",
                    "  - [ ] Approve as-is",
                    "  - [ ] Approve with caution",
                    "  - [ ] Rewrite",
                    "  - [ ] Reject",
                    "- Teacher notes:",
                    "",
                ]
            )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_reviewable_preview_artifacts(blueprints: list[dict[str, Any]], questions: list[dict[str, Any]]) -> dict[str, Any]:
    reviewable_questions, summary = build_reviewable_preview_records(blueprints, questions)
    paths = reviewable_preview_paths()
    write_jsonl(paths["questions"], reviewable_questions)
    write_reviewable_manual_review_packet(paths["manual_review_packet"], reviewable_questions, summary)
    write_json(paths["summary_json"], summary)
    return summary


def validate_generation_targets(summary: dict[str, Any], config: dict[str, Any]) -> None:
    minimums = config["minimum_question_counts"]
    if summary["total_questions"] < minimums["total_questions"]:
        raise ValueError("Generated question count did not meet minimum total_questions target.")
    if summary["question_count_by_lane"].get("translation", 0) < minimums["translation"]:
        raise ValueError("Generated question count did not meet translation minimum.")
    if summary["question_count_by_lane"].get("dikduk", 0) < minimums["dikduk"]:
        raise ValueError("Generated question count did not meet dikduk minimum.")
    if summary["question_count_by_lane"].get("word_analysis", 0) < minimums["word_analysis"]:
        raise ValueError("Generated question count did not meet word_analysis minimum.")
    if summary["question_count_by_lane"].get("error_diagnosis", 0) < minimums["error_diagnosis"]:
        raise ValueError("Generated question count did not meet error_diagnosis minimum.")
    if summary["question_count_by_skill"].get("mixed_skill_translation_rule", 0) < minimums["mixed_skill"]:
        raise ValueError("Generated mixed-skill preview question count did not meet minimum.")


def generate_preview(config_path: Path) -> dict[str, Any]:
    config = load_config(config_path)
    blueprints, questions, summary = build_preview_records(config)
    validate_generation_targets(summary, config)
    reviewable_summary = write_reviewable_preview_artifacts(blueprints, questions)

    outputs = config["output_files"]
    blueprints_path = REPO_ROOT / outputs["blueprints"]
    questions_path = REPO_ROOT / outputs["questions"]
    review_packet_path = REPO_ROOT / outputs["manual_review_packet"]
    summary_md_path = REPO_ROOT / outputs["summary_markdown"]
    summary_json_path = REPO_ROOT / outputs["summary_json"]

    write_jsonl(blueprints_path, blueprints)
    write_jsonl(questions_path, questions)
    write_manual_review_packet(
        review_packet_path,
        questions,
        {record["blueprint_id"]: record for record in blueprints},
        build_error_index(),
    )
    summary["reviewable_preview"] = {
        "total_questions": reviewable_summary["total_questions"],
        "final_recommendation": reviewable_summary["final_recommendation"],
        "likely_review_status_counts": reviewable_summary["likely_review_status_counts"],
    }
    write_summary_markdown(summary_md_path, summary)
    write_json(summary_json_path, summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate non-runtime diagnostic preview artifacts.")
    parser.add_argument("--config", required=True, help="Path to the diagnostic preview config JSON file.")
    args = parser.parse_args()
    summary = generate_preview((REPO_ROOT / args.config).resolve() if not Path(args.config).is_absolute() else Path(args.config))
    print(
        json.dumps(
            {
                "preview_id": summary["preview_id"],
                "total_blueprints": summary["total_blueprints"],
                "total_questions": summary["total_questions"],
                "question_count_by_lane": summary["question_count_by_lane"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
