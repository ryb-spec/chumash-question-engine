import json
from pathlib import Path


QUESTIONS_PATH = Path("questions.json")
NEW_QUESTIONS_PATH = Path("new_questions.json")

DEFAULTS = {
    "difficulty": 1,
    "tier": "standard",
    "mode": "practice",
}

REQUIRED_FIELDS = {
    "question",
    "choices",
    "correct_answer",
    "explanation",
    "skill",
    "standard",
    "micro_standard",
}


def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path, data):
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.write("\n")


def get_question_list(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("questions"), list):
        return data["questions"]
    raise ValueError("questions.json must be a list or an object with a questions list.")


def validate_question(question, existing_texts):
    missing = sorted(field for field in REQUIRED_FIELDS if field not in question)
    if missing:
        raise ValueError(f"Question is missing required fields: {missing}")

    choices = question["choices"]
    if not isinstance(choices, list) or len(choices) != 4:
        raise ValueError(f"Question must have exactly 4 choices: {question['question']}")
    if len(set(choices)) != 4:
        raise ValueError(f"Question choices must be unique: {question['question']}")
    if question["correct_answer"] not in choices:
        raise ValueError(f"Correct answer missing from choices: {question['question']}")
    if question["question"] in existing_texts:
        return False

    return True


def normalize_question(question):
    normalized = dict(question)
    for key, value in DEFAULTS.items():
        normalized.setdefault(key, value)
    normalized.setdefault("question_type", normalized["skill"])
    normalized.setdefault("word", "")
    normalized.setdefault("selected_word", normalized["word"])
    normalized.setdefault("source", "new_questions.json")
    return normalized


def import_new_questions():
    main_data = load_json(QUESTIONS_PATH)
    questions = get_question_list(main_data)
    new_questions = load_json(NEW_QUESTIONS_PATH)

    if not isinstance(new_questions, list):
        raise ValueError("new_questions.json must contain a list of questions.")

    existing_texts = {question["question"] for question in questions}
    added = []
    skipped = []

    for raw_question in new_questions:
        question = normalize_question(raw_question)
        should_add = validate_question(question, existing_texts)
        if should_add:
            questions.append(question)
            existing_texts.add(question["question"])
            added.append(question["question"])
        else:
            skipped.append(question["question"])

    save_json(QUESTIONS_PATH, main_data)

    print(f"Added: {len(added)}")
    print(f"Skipped duplicates: {len(skipped)}")
    print(f"New total: {len(questions)}")
    if added:
        print("Added questions:")
        for text in added:
            print(f"- {text}")
    if skipped:
        print("Skipped questions:")
        for text in skipped:
            print(f"- {text}")


if __name__ == "__main__":
    import_new_questions()
