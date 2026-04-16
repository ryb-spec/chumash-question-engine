import json
from pathlib import Path


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


def get_questions(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data["questions"] if isinstance(data, dict) else data


questions = get_questions("questions.json")
by_text = {question.get("question"): question for question in questions}
selected = [by_text[text] for text in WANTED_QUESTIONS]
serialized = [
    json.dumps(question, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    for question in questions
]

print(f"total={len(questions)}")
print(f"selected={len(selected)}")
print(f"all_difficulty_5={all(question.get('difficulty') == 5 for question in selected)}")
print(f"all_tier_advanced={all(question.get('tier') == 'advanced' for question in selected)}")
print(f"all_mode_reasoning={all(question.get('mode') == 'reasoning' for question in selected)}")
print(f"duplicate_objects={len(serialized) - len(set(serialized))}")
