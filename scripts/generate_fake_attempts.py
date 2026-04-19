from __future__ import annotations

import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

from skill_catalog import skill_standard

BASE_DIR = Path(__file__).resolve().parents[1]
ATTEMPT_LOG_PATH = BASE_DIR / "data" / "attempt_log.jsonl"


COMMONLY_MISSED = [
    {
        "word": "למינו",
        "selected_word": "למינו",
        "pasuk_ref": "Bereishis 1:11",
        "source": "local_parsed_bereishis_1_1_to_1_20:Bereishis 1:11",
        "focus": "affix",
    },
    {
        "word": "והארץ",
        "selected_word": "והארץ",
        "pasuk_ref": "Bereishis 1:2",
        "source": "local_parsed_bereishis_1_1_to_1_20:Bereishis 1:2",
        "focus": "prefix",
    },
    {
        "word": "לאור",
        "selected_word": "לאור",
        "pasuk_ref": "Bereishis 1:4",
        "source": "local_parsed_bereishis_1_1_to_1_20:Bereishis 1:4",
        "focus": "prefix",
    },
    {
        "word": "במים",
        "selected_word": "במים",
        "pasuk_ref": "Bereishis 1:6",
        "source": "local_parsed_bereishis_1_1_to_1_20:Bereishis 1:6",
        "focus": "suffix",
    },
]

MOSTLY_CORRECT = [
    {
        "word": "ברא",
        "selected_word": "ברא",
        "pasuk_ref": "Bereishis 1:1",
        "source": "local_parsed_bereishis_1_1_to_1_20:Bereishis 1:1",
    },
    {
        "word": "ויאמר",
        "selected_word": "ויאמר",
        "pasuk_ref": "Bereishis 1:3",
        "source": "local_parsed_bereishis_1_1_to_1_20:Bereishis 1:3",
    },
    {
        "word": "אור",
        "selected_word": "אור",
        "pasuk_ref": "Bereishis 1:3",
        "source": "local_parsed_bereishis_1_1_to_1_20:Bereishis 1:3",
    },
    {
        "word": "יום",
        "selected_word": "יום",
        "pasuk_ref": "Bereishis 1:5",
        "source": "local_parsed_bereishis_1_1_to_1_20:Bereishis 1:5",
    },
]

GENERAL_POOL = [
    {
        "word": "מים",
        "selected_word": "מים",
        "pasuk_ref": "Bereishis 1:2",
        "source": "local_parsed_bereishis_1_1_to_1_20:Bereishis 1:2",
    },
    {
        "word": "שמים",
        "selected_word": "שמים",
        "pasuk_ref": "Bereishis 1:1",
        "source": "local_parsed_bereishis_1_1_to_1_20:Bereishis 1:1",
    },
    {
        "word": "ויקרא",
        "selected_word": "ויקרא",
        "pasuk_ref": "Bereishis 1:5",
        "source": "local_parsed_bereishis_1_1_to_1_20:Bereishis 1:5",
    },
    {
        "word": "וירא",
        "selected_word": "וירא",
        "pasuk_ref": "Bereishis 1:4",
        "source": "local_parsed_bereishis_1_1_to_1_20:Bereishis 1:4",
    },
    {
        "word": "רקיע",
        "selected_word": "רקיע",
        "pasuk_ref": "Bereishis 1:7",
        "source": "local_parsed_bereishis_1_1_to_1_20:Bereishis 1:7",
    },
    {
        "word": "תדשא",
        "selected_word": "תדשא",
        "pasuk_ref": "Bereishis 1:11",
        "source": "local_parsed_bereishis_1_1_to_1_20:Bereishis 1:11",
    },
]

QUESTION_TYPES = [
    {
        "skill": "shoresh",
        "question_type": "shoresh",
        "standard": skill_standard("shoresh"),
        "accuracy": 0.84,
        "expected": lambda row: shoresh_answer(row["word"]),
        "wrong": lambda row, expected: expected[:-1] if len(expected) > 2 else row["word"],
    },
    {
        "skill": "translation",
        "question_type": "word_meaning",
        "standard": skill_standard("translation"),
        "accuracy": 0.72,
        "expected": lambda row: translation_answer(row["word"]),
        "wrong": lambda row, expected: wrong_translation(row["word"], expected),
    },
    {
        "skill": "verb_tense",
        "question_type": "verb_tense",
        "standard": skill_standard("verb_tense"),
        "accuracy": 0.67,
        "expected": lambda row: tense_answer(row["word"]),
        "wrong": lambda row, expected: wrong_tense(expected),
    },
    {
        "skill": "identify_prefix_meaning",
        "question_type": "prefix",
        "standard": skill_standard("identify_prefix_meaning"),
        "accuracy": 0.45,
        "expected": lambda row: prefix_answer(row["word"]),
        "wrong": lambda row, expected: wrong_prefix(expected),
    },
    {
        "skill": "identify_suffix_meaning",
        "question_type": "suffix",
        "standard": skill_standard("identify_suffix_meaning"),
        "accuracy": 0.38,
        "expected": lambda row: suffix_answer(row["word"]),
        "wrong": lambda row, expected: wrong_suffix(expected),
    },
]


def shoresh_answer(word: str) -> str:
    return {
        "ברא": "ברא",
        "ויאמר": "אמר",
        "ויקרא": "קרא",
        "וירא": "ראה",
        "לאור": "אור",
        "והארץ": "ארץ",
        "במים": "מים",
        "למינו": "מין",
        "תדשא": "דשא",
        "רקיע": "רקיע",
        "מים": "מים",
        "יום": "יום",
        "אור": "אור",
        "שמים": "שמים",
    }.get(word, word)


def translation_answer(word: str) -> str:
    return {
        "ברא": "created",
        "ויאמר": "and he said",
        "אור": "light",
        "יום": "day",
        "מים": "water",
        "והארץ": "and the earth",
        "לאור": "to the light",
        "במים": "in the water",
        "רקיע": "firmament",
        "למינו": "according to its kind",
        "תדשא": "let sprout",
        "שמים": "heavens",
    }.get(word, word)


def tense_answer(word: str) -> str:
    return {
        "ויאמר": "vav_consecutive_past",
        "ויקרא": "vav_consecutive_past",
        "וירא": "vav_consecutive_past",
        "תדשא": "future_jussive",
        "ברא": "past",
    }.get(word, "not_a_verb")


def prefix_answer(word: str) -> str:
    return {
        "והארץ": "and",
        "לאור": "to / for",
        "למינו": "to / for",
        "במים": "in / with",
    }.get(word, "none")


def suffix_answer(word: str) -> str:
    return {
        "למינו": "his / its",
        "במים": "none",
        "יום": "none",
        "אור": "none",
    }.get(word, "none")


def wrong_translation(word: str, expected: str) -> str:
    options = {
        "ברא": "saw",
        "ויאמר": "and he saw",
        "אור": "day",
        "יום": "light",
        "מים": "earth",
        "והארץ": "the heavens",
        "לאור": "the light",
        "במים": "the water",
        "רקיע": "earth",
        "למינו": "its seed",
        "תדשא": "it came out",
        "שמים": "water",
    }
    return options.get(word, expected)


def wrong_tense(expected: str) -> str:
    options = [
        "past",
        "future",
        "future_jussive",
        "vav_consecutive_past",
        "not_a_verb",
    ]
    for option in options:
        if option != expected:
            return option
    return expected


def wrong_prefix(expected: str) -> str:
    options = ["and", "to / for", "in / with", "the", "none"]
    for option in options:
        if option != expected:
            return option
    return expected


def wrong_suffix(expected: str) -> str:
    options = ["his / its", "their", "your", "none"]
    for option in options:
        if option != expected:
            return option
    return expected


def choose_word(rng: random.Random, question_type: str) -> dict:
    if question_type == "prefix":
        weighted = COMMONLY_MISSED * 3 + GENERAL_POOL + MOSTLY_CORRECT
    elif question_type == "suffix":
        weighted = [
            row for row in COMMONLY_MISSED if row["word"] in {"למינו", "במים"}
        ] * 5 + MOSTLY_CORRECT + GENERAL_POOL
    elif question_type == "shoresh":
        weighted = MOSTLY_CORRECT * 3 + COMMONLY_MISSED + GENERAL_POOL
    else:
        weighted = COMMONLY_MISSED + MOSTLY_CORRECT * 2 + GENERAL_POOL * 2
    return dict(rng.choice(weighted))


def build_attempt(rng: random.Random, index: int) -> dict:
    question = rng.choice(QUESTION_TYPES)
    row = choose_word(rng, question["question_type"])

    expected = question["expected"](row)
    accuracy = question["accuracy"]

    if row["word"] in {entry["word"] for entry in COMMONLY_MISSED}:
        accuracy -= 0.18
    if row["word"] in {entry["word"] for entry in MOSTLY_CORRECT}:
        accuracy += 0.12

    accuracy = max(0.05, min(0.95, accuracy))
    is_correct = rng.random() < accuracy
    user_answer = expected if is_correct else question["wrong"](row, expected)

    timestamp = datetime(2026, 4, 1, 0, 0, tzinfo=timezone.utc) + timedelta(minutes=15 * index)
    return {
        "timestamp_utc": timestamp.isoformat(),
        "word": row["word"],
        "selected_word": row["selected_word"],
        "skill": question["skill"],
        "question_type": question["question_type"],
        "standard": question["standard"],
        "is_correct": is_correct,
        "expected_answer": expected,
        "user_answer": user_answer,
        "pasuk_ref": row["pasuk_ref"],
        "source": row["source"],
    }


def main() -> None:
    rng = random.Random(613)
    attempts = [build_attempt(rng, index) for index in range(100)]
    ATTEMPT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with ATTEMPT_LOG_PATH.open("w", encoding="utf-8") as handle:
        for row in attempts:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
