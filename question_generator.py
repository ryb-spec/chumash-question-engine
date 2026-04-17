"""Legacy preview question generator.

This script builds static preview artifacts from the legacy root word bank.
It is not the supported runtime; the supported app runtime is
``streamlit_app.py`` using the active parsed dataset.
"""

import argparse
import json
import random
from pathlib import Path

from assessment_scope import LEGACY_ROOT_WORD_BANK_PATH, repo_path

BASE_DIR = repo_path()
WORD_BANK_PATH = LEGACY_ROOT_WORD_BANK_PATH
OUTPUT_PATH = repo_path("generated_questions_preview.json")


def load_word_bank():
    with WORD_BANK_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)["words"]


def by_group(words, group, word_type=None):
    matches = [word for word in words if word["group"] == group]
    if word_type is not None:
        matches = [word for word in matches if word["type"] == word_type]
    return matches


def same_group_choices(correct_word, words, value_key="translation"):
    group_words = [
        word
        for word in words
        if word["group"] == correct_word["group"]
        and word["type"] == correct_word["type"]
        and word["word"] != correct_word["word"]
    ]
    distractors = []
    seen = {correct_word[value_key]}

    for word in group_words:
        value = word[value_key]
        if value not in seen:
            distractors.append(value)
            seen.add(value)
        if len(distractors) == 3:
            break

    choices = [correct_word[value_key]] + distractors
    random.shuffle(choices)
    return choices


def cycle_pick(items, index):
    return items[index % len(items)]


def find_word(words, word_text, word_type=None):
    for word in words:
        if word["word"] == word_text and (word_type is None or word["type"] == word_type):
            return word
    raise KeyError(f"Missing word-bank entry: {word_text}")


def make_ss_question(verb, sentence, words, index):
    return {
        "skill": "sentence_structure",
        "standard": "SS",
        "micro_standard": "SS2",
        "selected_word": verb["word"],
        "word": sentence,
        "source": verb["source"],
        "question": f"What is the action in {sentence}?",
        "choices": same_group_choices(verb, words),
        "correct_answer": verb["translation"],
        "explanation": f"{verb['word']} means '{verb['translation']}'.",
        "difficulty": verb["difficulty"],
        "generated_from": "word_bank.json",
        "generation_group": verb["group"],
        "generation_index": index,
    }


def make_cm_question(verb, sentence, words, index):
    return {
        "skill": "contextual_meaning",
        "standard": "CM",
        "micro_standard": "CM1",
        "selected_word": verb["word"],
        "word": verb["word"],
        "source": verb["source"],
        "question": f"In {sentence}, what does {verb['word']} mean?",
        "choices": same_group_choices(verb, words),
        "correct_answer": verb["translation"],
        "explanation": f"The context points to '{verb['translation']}'.",
        "difficulty": verb["difficulty"],
        "generated_from": "word_bank.json",
        "generation_group": verb["group"],
        "generation_index": index,
    }


def make_ps_question(prep, phrase, object_translation, words, index):
    choices = [f"{choice} {object_translation}" for choice in same_group_choices(prep, words)]
    correct_answer = f"{prep['translation']} {object_translation}"
    return {
        "skill": "phrase_structure",
        "standard": "PS",
        "micro_standard": "PS3",
        "selected_word": prep["word"],
        "word": phrase,
        "source": prep["source"],
        "question": f"What does {phrase} mean?",
        "choices": choices,
        "correct_answer": correct_answer,
        "explanation": f"{prep['word']} means '{prep['translation']}'.",
        "difficulty": prep["difficulty"],
        "generated_from": "word_bank.json",
        "generation_group": prep["group"],
        "generation_index": index,
    }


def generate_questions(ss_count=20, cm_count=15, ps_count=10):
    words = load_word_bank()
    preposition = lambda text: find_word(words, text, "prep")
    verb = lambda text: find_word(words, text, "verb")

    ss_templates = [
        ("הלך", "איש הלך אל בית"),
        ("בא", "עבד בא אל עיר"),
        ("יצא", "נער יצא מן בית"),
        ("עמד", "כהן עמד לפני מלך"),
        ("רץ", "איש רץ אל שדה"),
        ("נתן", "אב נתן לחם"),
        ("לקח", "עבד לקח כסף"),
        ("שלח", "מלך שלח עבד"),
        ("פתח", "איש פתח בית"),
        ("סגר", "עבד סגר בית"),
        ("מצא", "נער מצא כסף"),
        ("בנה", "מלך בנה עיר"),
        ("הלך", "אב הלך אל הר"),
        ("בא", "בן בא אל בית"),
        ("יצא", "איש יצא מן עיר"),
        ("עמד", "נער עמד לפני אב"),
        ("רץ", "עבד רץ אל נהר"),
        ("נתן", "מלך נתן זהב"),
        ("לקח", "איש לקח אבן"),
        ("שלח", "אב שלח בן"),
    ]

    cm_templates = [
        ("עלה", "איש עלה אל הר"),
        ("ירד", "איש ירד מן הר"),
        ("עבר", "איש עבר מן עיר אל שדה"),
        ("שב", "נער שב אל בית"),
        ("ישב", "עבד ישב תחת עץ"),
        ("ראה", "נביא ראה איש"),
        ("שמע", "עם שמע מלך"),
        ("ידע", "איש ידע דבר"),
        ("זכר", "אב זכר בן"),
        ("שכח", "בן שכח דבר"),
        ("חשב", "איש חשב דבר"),
        ("אהב", "אב אהב בן"),
        ("שנא", "אח שנא אח"),
        ("ירא", "עבד ירא מלך"),
        ("הביא", "עבד הביא לחם"),
    ]

    ps_templates = [
        ("אל", "אל בית", "the house"),
        ("מן", "מן בית", "the house"),
        ("על", "על הר", "the mountain"),
        ("עם", "עם עבד", "the servant"),
        ("לפני", "לפני מלך", "the king"),
        ("אחרי", "אחרי נער", "the youth"),
        ("תחת", "תחת עץ", "the tree"),
        ("אל", "אל עיר", "the city"),
        ("מן", "מן שדה", "the field"),
        ("על", "על אבן", "the stone"),
    ]

    generated = []

    for index in range(ss_count):
        verb_text, sentence = cycle_pick(ss_templates, index)
        generated.append(
            make_ss_question(
                verb(verb_text),
                sentence,
                words,
                index + 1,
            )
        )

    for index in range(cm_count):
        verb_text, sentence = cycle_pick(cm_templates, index)
        generated.append(
            make_cm_question(
                verb(verb_text),
                sentence,
                words,
                index + 1,
            )
        )

    for index in range(ps_count):
        prep_text, phrase, object_translation = cycle_pick(ps_templates, index)
        generated.append(
            make_ps_question(
                preposition(prep_text),
                phrase,
                object_translation,
                words,
                index + 1,
            )
        )

    return generated


def validate_generated_questions(questions):
    errors = []
    seen_questions = set()

    for question in questions:
        if question["question"] in seen_questions:
            errors.append(f"Duplicate question: {question['question']}")
        seen_questions.add(question["question"])

        if len(question["choices"]) != 4:
            errors.append(f"Question does not have 4 choices: {question['question']}")

        if question["correct_answer"] not in question["choices"]:
            errors.append(f"Correct answer is missing from choices: {question['question']}")

        if question["standard"] == "PS" and question["difficulty"] not in {1, 2}:
            errors.append(f"PS difficulty should be 1-2: {question['question']}")
        if question["standard"] == "SS" and question["difficulty"] != 3:
            errors.append(f"SS difficulty should be 3: {question['question']}")
        if question["standard"] == "CM" and question["difficulty"] not in {4, 5}:
            errors.append(f"CM difficulty should be 4-5: {question['question']}")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Generate preview Chumash questions.")
    parser.add_argument("--ss", type=int, default=20)
    parser.add_argument("--cm", type=int, default=15)
    parser.add_argument("--ps", type=int, default=10)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()

    questions = generate_questions(ss_count=args.ss, cm_count=args.cm, ps_count=args.ps)
    errors = validate_generated_questions(questions)
    if errors:
        raise SystemExit("\n".join(errors))

    payload = {"questions": questions}
    args.output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Wrote {len(questions)} questions to {args.output}")


if __name__ == "__main__":
    main()
