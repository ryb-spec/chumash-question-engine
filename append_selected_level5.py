import copy
import json

from assessment_scope import LEGACY_GRAMMAR_QUESTIONS_PREVIEW_PATH, LEGACY_QUESTIONS_PATH

SOURCE_PATH = LEGACY_GRAMMAR_QUESTIONS_PREVIEW_PATH
TARGET_PATH = LEGACY_QUESTIONS_PATH

WANTED_QUESTIONS = [
    "Why does מביתו mean 'from his house' instead of 'in his house'?",
    "How does לבנו show both direction and possession?",
    "Why does וילך האיש לביתו mean the man went to his house?",
    "How do the grammar clues show that וישב האיש בביתו describes location, not movement?",
    "How do the grammar clues show who receives the bread?",
    "Why does עלה best mean 'went up' in האיש עלה אל ההר?",
    "Why does ירד best mean 'went down' in האיש ירד מן ההר?",
    "Why does וישב fit better than וילך in וישב האיש בביתו?",
    "Why does ויצא fit better than וילך in ויצא האיש מביתו?",
    "How do the grammar clues show that the son saw his father?",
]


LEVEL5_FALLBACKS = [
    {
        "skill": "combined_reasoning",
        "standard": "CF",
        "micro_standard": "CF4",
        "question_type": "reasoning",
        "word": "מביתו",
        "selected_word": "מביתו",
        "source": "בראשית כד:ז",
        "question": "Why does מביתו mean 'from his house' instead of 'in his house'?",
        "choices": [
            "מ marks movement from, while ו marks his possession",
            "מ marks location in, while ו marks his possession",
            "מ marks direction toward, while ו marks his possession",
            "מ marks possession, while ו marks movement from",
        ],
        "correct_answer": "מ marks movement from, while ו marks his possession",
        "explanation": "מ means 'from'; ו at the end means 'his'.",
        "difficulty": 5,
        "grammar_layer": True,
        "generation_group": "combined_grammar",
    },
    {
        "skill": "combined_reasoning",
        "standard": "CF",
        "micro_standard": "CF4",
        "question_type": "reasoning",
        "word": "לבנו",
        "selected_word": "לבנו",
        "source": "בראשית כב:ז",
        "question": "How does לבנו show both direction and possession?",
        "choices": [
            "ל marks direction toward and ו marks his possession",
            "ל marks location in and ו marks his possession",
            "ל marks movement from and ו marks her possession",
            "ל marks possession and ו marks direction toward",
        ],
        "correct_answer": "ל marks direction toward and ו marks his possession",
        "explanation": "ל means 'to'; ו at the end means 'his'.",
        "difficulty": 5,
        "grammar_layer": True,
        "generation_group": "combined_grammar",
    },
    {
        "skill": "sentence_structure",
        "standard": "SS",
        "micro_standard": "SS5",
        "question_type": "reasoning",
        "word": "וילך האיש לביתו",
        "selected_word": "וילך האיש לביתו",
        "source": "בראשית יב:ד",
        "question": "Why does וילך האיש לביתו mean the man went to his house?",
        "choices": [
            "וילך gives the action, האיש gives the subject, and לביתו gives the destination",
            "וילך gives the subject, האיש gives the action, and לביתו gives the object",
            "וילך gives possession, האיש gives the destination, and לביתו gives the action",
            "וילך gives location, האיש gives possession, and לביתו gives movement away",
        ],
        "correct_answer": "וילך gives the action, האיש gives the subject, and לביתו gives the destination",
        "explanation": "וילך = went, האיש = the man, לביתו = to his house.",
        "difficulty": 5,
        "grammar_layer": True,
        "generation_group": "sentence_reasoning",
    },
    {
        "skill": "sentence_structure",
        "standard": "SS",
        "micro_standard": "SS5",
        "question_type": "reasoning",
        "word": "וישב האיש בביתו",
        "selected_word": "וישב האיש בביתו",
        "source": "בראשית יג:יב",
        "question": "How do the grammar clues show that וישב האיש בביתו describes location, not movement?",
        "choices": [
            "וישב describes staying/dwelling and בביתו marks location in his house",
            "וישב describes leaving and בביתו marks movement from his house",
            "וישב describes going and בביתו marks movement toward his house",
            "וישב describes giving and בביתו marks the object being given",
        ],
        "correct_answer": "וישב describes staying/dwelling and בביתו marks location in his house",
        "explanation": "וישב fits location; ב means 'in'.",
        "difficulty": 5,
        "grammar_layer": True,
        "generation_group": "sentence_reasoning",
    },
    {
        "skill": "sentence_structure",
        "standard": "SS",
        "micro_standard": "SS5",
        "question_type": "reasoning",
        "word": "ויתן האב לחם לבנו",
        "selected_word": "ויתן האב לחם לבנו",
        "source": "בראשית א:כט",
        "question": "How do the grammar clues show who receives the bread?",
        "choices": [
            "ל in לבנו marks the receiver: to his son",
            "ו in ויתן marks the receiver: his son",
            "ה in האב marks the receiver: the father",
            "לחם marks the receiver because it follows the verb",
        ],
        "correct_answer": "ל in לבנו marks the receiver: to his son",
        "explanation": "ל marks 'to'; לבנו means 'to his son'.",
        "difficulty": 5,
        "grammar_layer": True,
        "generation_group": "sentence_reasoning",
    },
    {
        "skill": "contextual_meaning",
        "standard": "CM",
        "micro_standard": "CM1",
        "question_type": "reasoning",
        "word": "עלה",
        "selected_word": "עלה",
        "source": "בראשית יג:א",
        "question": "Why does עלה best mean 'went up' in האיש עלה אל ההר?",
        "choices": [
            "אל ההר gives a mountain context, so movement upward fits",
            "אל ההר shows leaving a house, so movement away fits",
            "אל ההר shows giving to a person, so transfer fits",
            "אל ההר shows sitting in a place, so dwelling fits",
        ],
        "correct_answer": "אל ההר gives a mountain context, so movement upward fits",
        "explanation": "A mountain context supports the meaning 'went up'.",
        "difficulty": 5,
        "grammar_layer": True,
        "generation_group": "context_reasoning",
    },
    {
        "skill": "contextual_meaning",
        "standard": "CM",
        "micro_standard": "CM1",
        "question_type": "reasoning",
        "word": "ירד",
        "selected_word": "ירד",
        "source": "שמות יט:יד",
        "question": "Why does ירד best mean 'went down' in האיש ירד מן ההר?",
        "choices": [
            "מן ההר shows movement from a mountain, so downward movement fits",
            "מן ההר shows movement toward a mountain, so upward movement fits",
            "מן ההר shows staying on a mountain, so dwelling fits",
            "מן ההר shows giving a mountain, so transfer fits",
        ],
        "correct_answer": "מן ההר shows movement from a mountain, so downward movement fits",
        "explanation": "Coming from a mountain fits 'went down'.",
        "difficulty": 5,
        "grammar_layer": True,
        "generation_group": "context_reasoning",
    },
    {
        "skill": "contextual_meaning",
        "standard": "CM",
        "micro_standard": "CM1",
        "question_type": "reasoning",
        "word": "וישב",
        "selected_word": "וישב",
        "source": "בראשית יג:יב",
        "question": "Why does וישב fit better than וילך in וישב האיש בביתו?",
        "choices": [
            "בביתו shows location, so וישב describes staying/dwelling there",
            "בביתו shows movement away, so וישב means he left",
            "בביתו shows direction toward, so וישב means he went",
            "בביתו shows giving, so וישב means he gave something",
        ],
        "correct_answer": "בביתו shows location, so וישב describes staying/dwelling there",
        "explanation": "בביתו means 'in his house', which fits sitting or dwelling.",
        "difficulty": 5,
        "grammar_layer": True,
        "generation_group": "context_reasoning",
    },
    {
        "skill": "contextual_meaning",
        "standard": "CM",
        "micro_standard": "CM1",
        "question_type": "reasoning",
        "word": "ויצא",
        "selected_word": "ויצא",
        "source": "בראשית כח:י",
        "question": "Why does ויצא fit better than וילך in ויצא האיש מביתו?",
        "choices": [
            "מביתו shows movement from a place, so ויצא describes leaving",
            "מביתו shows movement toward a place, so ויצא describes arriving",
            "מביתו shows location in a place, so ויצא describes dwelling",
            "מביתו shows possession only, so ויצא describes owning",
        ],
        "correct_answer": "מביתו shows movement from a place, so ויצא describes leaving",
        "explanation": "מ means 'from', which fits ויצא.",
        "difficulty": 5,
        "grammar_layer": True,
        "generation_group": "context_reasoning",
    },
    {
        "skill": "sentence_structure",
        "standard": "SS",
        "micro_standard": "SS5",
        "question_type": "reasoning",
        "word": "וירא הבן את אביו",
        "selected_word": "וירא הבן את אביו",
        "source": "בראשית כב:ז",
        "question": "How do the grammar clues show that the son saw his father?",
        "choices": [
            "הבן is the subject, וירא is the action, and את אביו marks the object",
            "אביו is the subject, וירא is the object, and הבן marks the action",
            "את marks the subject, אביו marks the action, and הבן marks possession",
            "וירא marks possession, הבן marks direction, and אביו marks location",
        ],
        "correct_answer": "הבן is the subject, וירא is the action, and את אביו marks the object",
        "explanation": "הבן does the seeing; את אביו is what he sees.",
        "difficulty": 5,
        "grammar_layer": True,
        "generation_group": "sentence_reasoning",
    },
]


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def question_list(container):
    if isinstance(container, list):
        return container
    if isinstance(container, dict) and isinstance(container.get("questions"), list):
        return container["questions"]
    raise TypeError(f"{TARGET_PATH} must be a list or a dict with a questions list")


def no_duplicate_objects(items):
    serialized = [
        json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        for item in items
    ]
    return len(serialized) == len(set(serialized))


def main():
    target_data = load_json(TARGET_PATH)
    target_questions = question_list(target_data)
    before_count = len(target_questions)

    source_data = load_json(SOURCE_PATH)
    source_questions = question_list(source_data)
    source_by_text = {item.get("question"): item for item in source_questions}
    fallback_by_text = {item["question"]: item for item in LEVEL5_FALLBACKS}

    selected = []
    missing_from_source = []
    for text in WANTED_QUESTIONS:
        item = source_by_text.get(text)
        if item is None:
            missing_from_source.append(text)
            item = copy.deepcopy(fallback_by_text[text])
            source_questions.append(item)
            source_by_text[text] = item
        item = copy.deepcopy(item)
        item["difficulty"] = 5
        item["tier"] = "advanced"
        item["mode"] = "reasoning"
        selected.append(item)

    existing_texts = {item.get("question") for item in target_questions}
    duplicate_texts = [item["question"] for item in selected if item["question"] in existing_texts]
    if duplicate_texts:
        raise ValueError(f"Questions already exist in target: {duplicate_texts}")

    target_questions.extend(selected)
    after_count = len(target_questions)
    if after_count != before_count + 10:
        raise AssertionError(f"Expected count {before_count + 10}, got {after_count}")
    if not no_duplicate_objects(target_questions):
        raise AssertionError("Duplicate question objects found after append")

    if missing_from_source:
        SOURCE_PATH.write_text(
            json.dumps(source_data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    TARGET_PATH.write_text(
        json.dumps(target_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # Re-load to prove the saved JSON is valid.
    saved_questions = question_list(load_json(TARGET_PATH))
    if len(saved_questions) != after_count:
        raise AssertionError("Saved question count does not match expected count")

    print(f"before_count={before_count}")
    print(f"appended_count={len(selected)}")
    print(f"after_count={after_count}")
    print(f"missing_from_source_count={len(missing_from_source)}")
    if missing_from_source:
        print("used_fallback_questions=")
        for text in missing_from_source:
            print(f"- {text}")


if __name__ == "__main__":
    main()
