import json
import sys
from pathlib import Path

from assessment_scope import LEGACY_GRAMMAR_QUESTIONS_PREVIEW_PATH


WORD_BANK_PATH = Path("word_bank.json")
OUTPUT_PATH = LEGACY_GRAMMAR_QUESTIONS_PREVIEW_PATH

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


DEFAULT_GRAMMAR_FIELDS = {
    "prefix": "",
    "prefix_meaning": "",
    "suffix": "",
    "suffix_meaning": "",
    "tense": "",
    "person": "",
}


GRAMMAR_WORDS = [
    {
        "word": "וילך",
        "shoresh": "הלך",
        "translation": "and he went",
        "type": "verb",
        "group": "movement",
        "difficulty": 3,
        "source": "בראשית יב:ד",
        "prefix": "ו",
        "prefix_meaning": "and / narrative past",
        "tense": "past narrative",
        "person": "3rd masculine singular",
    },
    {
        "word": "וירא",
        "shoresh": "ראה",
        "translation": "and he saw",
        "type": "verb",
        "group": "perception",
        "difficulty": 3,
        "source": "בראשית א:ד",
        "prefix": "ו",
        "prefix_meaning": "and / narrative past",
        "tense": "past narrative",
        "person": "3rd masculine singular",
    },
    {
        "word": "ויאמר",
        "shoresh": "אמר",
        "translation": "and he said",
        "type": "verb",
        "group": "speech",
        "difficulty": 3,
        "source": "בראשית א:ג",
        "prefix": "ו",
        "prefix_meaning": "and / narrative past",
        "tense": "past narrative",
        "person": "3rd masculine singular",
    },
    {
        "word": "ויבא",
        "shoresh": "בוא",
        "translation": "and he came",
        "type": "verb",
        "group": "movement",
        "difficulty": 3,
        "source": "בראשית יב:ה",
        "prefix": "ו",
        "prefix_meaning": "and / narrative past",
        "tense": "past narrative",
        "person": "3rd masculine singular",
    },
    {
        "word": "ויצא",
        "shoresh": "יצא",
        "translation": "and he went out",
        "type": "verb",
        "group": "movement",
        "difficulty": 3,
        "source": "בראשית כח:י",
        "prefix": "ו",
        "prefix_meaning": "and / narrative past",
        "tense": "past narrative",
        "person": "3rd masculine singular",
    },
    {
        "word": "ויעל",
        "shoresh": "עלה",
        "translation": "and he went up",
        "type": "verb",
        "group": "movement",
        "difficulty": 4,
        "source": "בראשית יג:א",
        "prefix": "ו",
        "prefix_meaning": "and / narrative past",
        "tense": "past narrative",
        "person": "3rd masculine singular",
    },
    {
        "word": "וירד",
        "shoresh": "ירד",
        "translation": "and he went down",
        "type": "verb",
        "group": "movement",
        "difficulty": 4,
        "source": "שמות יט:יד",
        "prefix": "ו",
        "prefix_meaning": "and / narrative past",
        "tense": "past narrative",
        "person": "3rd masculine singular",
    },
    {
        "word": "וישב",
        "shoresh": "ישב",
        "translation": "and he sat/dwelt",
        "type": "verb",
        "group": "movement",
        "difficulty": 4,
        "source": "בראשית יג:יב",
        "prefix": "ו",
        "prefix_meaning": "and / narrative past",
        "tense": "past narrative",
        "person": "3rd masculine singular",
    },
    {
        "word": "ויתן",
        "shoresh": "נתן",
        "translation": "and he gave",
        "type": "verb",
        "group": "transfer",
        "difficulty": 3,
        "source": "בראשית א:כט",
        "prefix": "ו",
        "prefix_meaning": "and / narrative past",
        "tense": "past narrative",
        "person": "3rd masculine singular",
    },
    {
        "word": "ויקח",
        "shoresh": "לקח",
        "translation": "and he took",
        "type": "verb",
        "group": "transfer",
        "difficulty": 3,
        "source": "בראשית ב:טו",
        "prefix": "ו",
        "prefix_meaning": "and / narrative past",
        "tense": "past narrative",
        "person": "3rd masculine singular",
    },
    {
        "word": "וישמע",
        "shoresh": "שמע",
        "translation": "and he heard",
        "type": "verb",
        "group": "perception",
        "difficulty": 3,
        "source": "בראשית ג:ח",
        "prefix": "ו",
        "prefix_meaning": "and / narrative past",
        "tense": "past narrative",
        "person": "3rd masculine singular",
    },
    {
        "word": "בבית",
        "shoresh": "בית",
        "translation": "in the house",
        "type": "prep_form",
        "group": "preposition",
        "difficulty": 3,
        "source": "בראשית ז:א",
        "prefix": "ב",
        "prefix_meaning": "in",
    },
    {
        "word": "לבית",
        "shoresh": "בית",
        "translation": "to the house",
        "type": "prep_form",
        "group": "preposition",
        "difficulty": 3,
        "source": "בראשית יב:א",
        "prefix": "ל",
        "prefix_meaning": "to",
    },
    {
        "word": "מבית",
        "shoresh": "בית",
        "translation": "from the house",
        "type": "prep_form",
        "group": "preposition",
        "difficulty": 3,
        "source": "בראשית ב:ט",
        "prefix": "מ",
        "prefix_meaning": "from",
    },
    {
        "word": "בארץ",
        "shoresh": "ארץ",
        "translation": "in the land",
        "type": "prep_form",
        "group": "preposition",
        "difficulty": 3,
        "source": "בראשית א:א",
        "prefix": "ב",
        "prefix_meaning": "in",
    },
    {
        "word": "לארץ",
        "shoresh": "ארץ",
        "translation": "to the land",
        "type": "prep_form",
        "group": "preposition",
        "difficulty": 3,
        "source": "בראשית יב:א",
        "prefix": "ל",
        "prefix_meaning": "to",
    },
    {
        "word": "מארץ",
        "shoresh": "ארץ",
        "translation": "from the land",
        "type": "prep_form",
        "group": "preposition",
        "difficulty": 3,
        "source": "בראשית יב:א",
        "prefix": "מ",
        "prefix_meaning": "from",
    },
    {
        "word": "אביו",
        "shoresh": "אב",
        "translation": "his father",
        "type": "suffix_form",
        "group": "suffix",
        "difficulty": 3,
        "source": "בראשית כב:ז",
        "suffix": "ו",
        "suffix_meaning": "his",
        "person": "3rd masculine singular",
    },
    {
        "word": "ביתו",
        "shoresh": "בית",
        "translation": "his house",
        "type": "suffix_form",
        "group": "suffix",
        "difficulty": 3,
        "source": "בראשית יט:ג",
        "suffix": "ו",
        "suffix_meaning": "his",
        "person": "3rd masculine singular",
    },
    {
        "word": "בנו",
        "shoresh": "בן",
        "translation": "his son",
        "type": "suffix_form",
        "group": "suffix",
        "difficulty": 3,
        "source": "בראשית כב:ג",
        "suffix": "ו",
        "suffix_meaning": "his",
        "person": "3rd masculine singular",
    },
    {
        "word": "עמו",
        "shoresh": "עם",
        "translation": "his people",
        "type": "suffix_form",
        "group": "suffix",
        "difficulty": 3,
        "source": "בראשית יז:יד",
        "suffix": "ו",
        "suffix_meaning": "his",
        "person": "3rd masculine singular",
    },
    {
        "word": "ארצו",
        "shoresh": "ארץ",
        "translation": "his land",
        "type": "suffix_form",
        "group": "suffix",
        "difficulty": 3,
        "source": "בראשית יב:א",
        "suffix": "ו",
        "suffix_meaning": "his",
        "person": "3rd masculine singular",
    },
    {
        "word": "אמו",
        "shoresh": "אם",
        "translation": "his mother",
        "type": "suffix_form",
        "group": "suffix",
        "difficulty": 3,
        "source": "בראשית כד:סז",
        "suffix": "ו",
        "suffix_meaning": "his",
        "person": "3rd masculine singular",
    },
    {
        "word": "אחיו",
        "shoresh": "אח",
        "translation": "his brother",
        "type": "suffix_form",
        "group": "suffix",
        "difficulty": 3,
        "source": "בראשית ד:ב",
        "suffix": "ו",
        "suffix_meaning": "his",
        "person": "3rd masculine singular",
    },
    {
        "word": "עבדו",
        "shoresh": "עבד",
        "translation": "his servant",
        "type": "suffix_form",
        "group": "suffix",
        "difficulty": 3,
        "source": "בראשית כד:ב",
        "suffix": "ו",
        "suffix_meaning": "his",
        "person": "3rd masculine singular",
    },
    {
        "word": "ידו",
        "shoresh": "יד",
        "translation": "his hand",
        "type": "suffix_form",
        "group": "suffix",
        "difficulty": 3,
        "source": "בראשית כב:י",
        "suffix": "ו",
        "suffix_meaning": "his",
        "person": "3rd masculine singular",
    },
    {
        "word": "שמו",
        "shoresh": "שם",
        "translation": "his name",
        "type": "suffix_form",
        "group": "suffix",
        "difficulty": 3,
        "source": "בראשית ב:יט",
        "suffix": "ו",
        "suffix_meaning": "his",
        "person": "3rd masculine singular",
    },
    {
        "word": "בביתו",
        "shoresh": "בית",
        "translation": "in his house",
        "type": "combined_form",
        "group": "combined_grammar",
        "difficulty": 4,
        "source": "בראשית יט:ג",
        "prefix": "ב",
        "prefix_meaning": "in",
        "suffix": "ו",
        "suffix_meaning": "his",
        "person": "3rd masculine singular",
    },
    {
        "word": "לבנו",
        "shoresh": "בן",
        "translation": "to his son",
        "type": "combined_form",
        "group": "combined_grammar",
        "difficulty": 4,
        "source": "בראשית כב:ז",
        "prefix": "ל",
        "prefix_meaning": "to",
        "suffix": "ו",
        "suffix_meaning": "his",
        "person": "3rd masculine singular",
    },
    {
        "word": "מביתו",
        "shoresh": "בית",
        "translation": "from his house",
        "type": "combined_form",
        "group": "combined_grammar",
        "difficulty": 4,
        "source": "בראשית כד:ז",
        "prefix": "מ",
        "prefix_meaning": "from",
        "suffix": "ו",
        "suffix_meaning": "his",
        "person": "3rd masculine singular",
    },
]


def load_word_bank():
    data = json.loads(WORD_BANK_PATH.read_text(encoding="utf-8"))
    words = data.setdefault("words", [])
    words[:] = [entry for entry in words if "?" not in entry.get("word", "")]
    return data


def normalize_word_bank(data):
    words = data["words"]
    for entry in words:
        entry.setdefault("shoresh", entry.get("word", ""))
        for field, value in DEFAULT_GRAMMAR_FIELDS.items():
            entry.setdefault(field, value)

    existing = {(entry["word"], entry.get("type", "")) for entry in words}
    for entry in GRAMMAR_WORDS:
        for field, value in DEFAULT_GRAMMAR_FIELDS.items():
            entry.setdefault(field, value)
        key = (entry["word"], entry.get("type", ""))
        if key not in existing:
            words.append(entry)
            existing.add(key)


def choices(correct, distractors):
    result = [correct]
    for distractor in distractors:
        if distractor != correct and distractor not in result:
            result.append(distractor)
        if len(result) == 4:
            break
    return result


def make_question(
    skill,
    standard,
    micro_standard,
    word,
    source,
    question,
    answer_choices,
    correct_answer,
    explanation,
    difficulty,
    generation_group,
    question_type,
):
    return {
        "skill": skill,
        "standard": standard,
        "micro_standard": micro_standard,
        "question_type": question_type,
        "word": word,
        "selected_word": word,
        "source": source,
        "question": question,
        "choices": answer_choices,
        "correct_answer": correct_answer,
        "explanation": explanation,
        "difficulty": difficulty,
        "grammar_layer": True,
        "generation_group": generation_group,
    }


def make_prefix_questions(entries):
    by_word = {entry["word"]: entry for entry in entries}
    return [
        make_question(
            "prefix_meaning",
            "PR",
            "PR1",
            by_word["בבית"]["word"],
            by_word["בבית"]["source"],
            "What does the prefix ב mean in בבית?",
            ["in", "to", "from", "on"],
            "in",
            "ב means 'in'.",
            3,
            "prefix",
            "direct_identification",
        ),
        make_question(
            "prefix_translation",
            "PR",
            "PR3",
            by_word["לבית"]["word"],
            by_word["לבית"]["source"],
            "What does לבית mean?",
            ["to the house", "in the house", "from the house", "on the house"],
            "to the house",
            "ל means 'to'.",
            3,
            "prefix",
            "application",
        ),
        make_question(
            "prefix_translation",
            "PR",
            "PR3",
            by_word["מבית"]["word"],
            by_word["מבית"]["source"],
            "What does מבית mean?",
            ["from the house", "to the house", "in the house", "on the house"],
            "from the house",
            "מ means 'from'.",
            3,
            "prefix",
            "application",
        ),
        make_question(
            "prefix_comparison",
            "PR",
            "PR3",
            "בית",
            by_word["לבית"]["source"],
            "Which form means 'to the house'?",
            ["לבית", "בבית", "מבית", "בית"],
            "לבית",
            "ל before בית means 'to the house'.",
            3,
            "prefix",
            "comparison",
        ),
        make_question(
            "prefix_comparison",
            "PR",
            "PR3",
            "ארץ",
            by_word["בארץ"]["source"],
            "Which form means 'in the land'?",
            ["בארץ", "לארץ", "מארץ", "ארץ"],
            "בארץ",
            "ב before ארץ means 'in the land'.",
            3,
            "prefix",
            "comparison",
        ),
        make_question(
            "prefix_context",
            "PR",
            "PR3",
            by_word["לבית"]["word"],
            by_word["לבית"]["source"],
            "In וילך האיש לבית, what does לבית show?",
            ["movement toward the house", "location inside the house", "movement from the house", "possession of the house"],
            "movement toward the house",
            "ל shows movement toward the house.",
            4,
            "prefix",
            "contextual_sentence",
        ),
        make_question(
            "prefix_context",
            "PR",
            "PR3",
            by_word["מבית"]["word"],
            by_word["מבית"]["source"],
            "In ויצא האיש מבית, what does מבית show?",
            ["movement from the house", "movement to the house", "location in the house", "ownership of the house"],
            "movement from the house",
            "מ shows movement from the house.",
            4,
            "prefix",
            "contextual_sentence",
        ),
        make_question(
            "prefix_reasoning",
            "PR",
            "PR3",
            "בית",
            by_word["מבית"]["source"],
            "What is the difference between בבית and מבית?",
            ["בבית means in the house; מבית means from the house", "בבית means to the house; מבית means in the house", "בבית means from the house; מבית means to the house", "בבית means his house; מבית means the house"],
            "בבית means in the house; מבית means from the house",
            "ב marks location; מ marks movement from.",
            4,
            "prefix",
            "reasoning",
        ),
        make_question(
            "prefix_reasoning",
            "PR",
            "PR3",
            "בית",
            by_word["לבית"]["source"],
            "What is the difference between לבית and בבית?",
            ["לבית means to the house; בבית means in the house", "לבית means in the house; בבית means to the house", "לבית means from the house; בבית means in the house", "לבית means his house; בבית means from the house"],
            "לבית means to the house; בבית means in the house",
            "ל marks direction toward; ב marks location in.",
            4,
            "prefix",
            "reasoning",
        ),
        make_question(
            "prefix_translation",
            "PR",
            "PR3",
            by_word["ויאמר"]["word"],
            by_word["ויאמר"]["source"],
            "In a narrative sentence, what does ויאמר mean?",
            ["and he said", "and he saw", "and he went", "and he gave"],
            "and he said",
            "ו plus the verb form creates a narrative action: 'and he said'.",
            4,
            "prefix",
            "contextual_sentence",
        ),
    ]


def make_suffix_questions(entries):
    by_word = {entry["word"]: entry for entry in entries}
    return [
        make_question(
            "suffix_meaning",
            "PR",
            "PR2",
            by_word["אביו"]["word"],
            by_word["אביו"]["source"],
            "What does the suffix ו mean in אביו?",
            ["his", "her", "my", "their"],
            "his",
            "ו at the end means 'his'.",
            3,
            "suffix",
            "direct_identification",
        ),
        make_question(
            "suffix_translation",
            "PR",
            "PR4",
            by_word["ביתו"]["word"],
            by_word["ביתו"]["source"],
            "What does ביתו mean?",
            ["his house", "her house", "my house", "their house"],
            "his house",
            "בית means house; ו at the end means his.",
            3,
            "suffix",
            "application",
        ),
        make_question(
            "suffix_translation",
            "PR",
            "PR4",
            by_word["בנו"]["word"],
            by_word["בנו"]["source"],
            "What does בנו mean?",
            ["his son", "her son", "my son", "their son"],
            "his son",
            "בן means son; ו at the end means his.",
            3,
            "suffix",
            "application",
        ),
        make_question(
            "suffix_comparison",
            "PR",
            "PR4",
            "בן",
            by_word["בנו"]["source"],
            "Which form means 'his son'?",
            ["בנו", "אביו", "ביתו", "שמו"],
            "בנו",
            "בנו is בן with the suffix ו, meaning 'his son'.",
            3,
            "suffix",
            "comparison",
        ),
        make_question(
            "suffix_comparison",
            "PR",
            "PR4",
            "שם",
            by_word["שמו"]["source"],
            "Which form means 'his name'?",
            ["שמו", "בנו", "אביו", "ארצו"],
            "שמו",
            "שמו is שם with the suffix ו, meaning 'his name'.",
            3,
            "suffix",
            "comparison",
        ),
        make_question(
            "suffix_context",
            "PR",
            "PR4",
            by_word["ביתו"]["word"],
            by_word["ביתו"]["source"],
            "In וילך האיש אל ביתו, what does ביתו mean?",
            ["his house", "her house", "my house", "their house"],
            "his house",
            "ביתו means 'his house' in the phrase.",
            4,
            "suffix",
            "contextual_sentence",
        ),
        make_question(
            "suffix_context",
            "PR",
            "PR4",
            by_word["אביו"]["word"],
            by_word["אביו"]["source"],
            "In וירא הבן את אביו, what does אביו mean?",
            ["his father", "her father", "my father", "their father"],
            "his father",
            "אביו means 'his father'.",
            4,
            "suffix",
            "contextual_sentence",
        ),
        make_question(
            "suffix_reasoning",
            "PR",
            "PR4",
            "בית",
            by_word["ביתו"]["source"],
            "What is the difference between בית and ביתו?",
            ["בית means house; ביתו means his house", "בית means his house; ביתו means house", "בית means to the house; ביתו means in the house", "בית means from the house; ביתו means his house"],
            "בית means house; ביתו means his house",
            "The suffix ו adds the meaning 'his'.",
            4,
            "suffix",
            "reasoning",
        ),
        make_question(
            "suffix_reasoning",
            "PR",
            "PR4",
            "אב",
            by_word["אביו"]["source"],
            "What changes when אב becomes אביו?",
            ["father becomes his father", "father becomes her father", "father becomes my father", "father becomes their father"],
            "father becomes his father",
            "The suffix ו makes the noun possessive: his father.",
            4,
            "suffix",
            "reasoning",
        ),
        make_question(
            "suffix_translation",
            "PR",
            "PR4",
            by_word["ארצו"]["word"],
            by_word["ארצו"]["source"],
            "What does ארצו mean?",
            ["his land", "her land", "my land", "their land"],
            "his land",
            "ארץ means land; ו at the end means his.",
            3,
            "suffix",
            "application",
        ),
    ]


def make_tense_questions(entries):
    tenses = ["past narrative", "present", "future", "command"]
    questions = []
    for entry in entries[:10]:
        questions.append(
            {
                "skill": "tense_identification",
                "standard": "CF",
                "micro_standard": "CF3",
                "word": entry["word"],
                "selected_word": entry["word"],
                "source": entry["source"],
                "question": f"What tense/form is {entry['word']}?",
                "choices": choices(entry["tense"], tenses),
                "correct_answer": entry["tense"],
                "explanation": f"{entry['word']} is a {entry['tense']} form.",
                "difficulty": 4,
                "grammar_layer": True,
                "generation_group": "tense",
            }
        )
    return questions


def make_shoresh_questions(entries):
    roots = ["הלך", "ראה", "אמר", "נתן", "לקח", "בוא", "יצא", "עלה", "ירד", "שמע"]
    questions = []
    for entry in entries[:10]:
        questions.append(
            {
                "skill": "shoresh_identification",
                "standard": "SR",
                "micro_standard": "SR3",
                "word": entry["word"],
                "selected_word": entry["word"],
                "source": entry["source"],
                "question": f"What is the shoresh of {entry['word']}?",
                "choices": choices(entry["shoresh"], roots),
                "correct_answer": entry["shoresh"],
                "explanation": f"{entry['word']} has shoresh {entry['shoresh']}.",
                "difficulty": 3,
                "grammar_layer": True,
                "generation_group": "shoresh",
            }
        )
    return questions


def make_combined_questions(entries):
    by_word = {entry["word"]: entry for entry in entries}
    return [
        make_question(
            "full_grammar_meaning",
            "CF",
            "CF4",
            by_word["בביתו"]["word"],
            by_word["בביתו"]["source"],
            "What does בביתו mean?",
            ["in his house", "from his house", "his house", "in the house"],
            "in his house",
            "ב = in, בית = house, ו = his.",
            4,
            "combined_grammar",
            "application",
        ),
        make_question(
            "full_grammar_meaning",
            "CF",
            "CF4",
            by_word["מביתו"]["word"],
            by_word["מביתו"]["source"],
            "What does מביתו mean?",
            ["from his house", "in his house", "to his house", "his house"],
            "from his house",
            "מ = from, בית = house, ו = his.",
            4,
            "combined_grammar",
            "application",
        ),
        make_question(
            "full_grammar_meaning",
            "CF",
            "CF4",
            by_word["לבנו"]["word"],
            by_word["לבנו"]["source"],
            "What does לבנו mean?",
            ["to his son", "his son", "from his son", "to the son"],
            "to his son",
            "ל = to, בן = son, ו = his.",
            4,
            "combined_grammar",
            "application",
        ),
        make_question(
            "word_decomposition",
            "CF",
            "CF4",
            by_word["בביתו"]["word"],
            by_word["בביתו"]["source"],
            "Which choice correctly decomposes בביתו?",
            ["ב = in; בית = house; ו = his", "ב = from; בית = house; ו = his", "ב = in; בית = house; ו = her", "ב = to; בית = house; ו = his"],
            "ב = in; בית = house; ו = his",
            "בביתו has prefix ב and suffix ו.",
            4,
            "combined_grammar",
            "word_decomposition",
        ),
        make_question(
            "word_decomposition",
            "CF",
            "CF4",
            by_word["לבנו"]["word"],
            by_word["לבנו"]["source"],
            "Which choice correctly decomposes לבנו?",
            ["ל = to; בן = son; ו = his", "ל = in; בן = son; ו = his", "ל = to; בן = son; ו = her", "ל = from; בן = son; ו = his"],
            "ל = to; בן = son; ו = his",
            "לבנו has prefix ל and suffix ו.",
            4,
            "combined_grammar",
            "word_decomposition",
        ),
        make_question(
            "combined_comparison",
            "CF",
            "CF4",
            "בית",
            by_word["בביתו"]["source"],
            "Which form means 'in his house'?",
            ["בביתו", "מביתו", "ביתו", "בבית"],
            "בביתו",
            "בביתו combines ב = in with ו = his.",
            4,
            "combined_grammar",
            "comparison",
        ),
        make_question(
            "combined_comparison",
            "CF",
            "CF4",
            "בית",
            by_word["מביתו"]["source"],
            "Which form means 'from his house'?",
            ["מביתו", "בביתו", "ביתו", "מבית"],
            "מביתו",
            "מביתו combines מ = from with ו = his.",
            4,
            "combined_grammar",
            "comparison",
        ),
        make_question(
            "combined_context",
            "CF",
            "CF4",
            by_word["בביתו"]["word"],
            by_word["בביתו"]["source"],
            "How do the grammar clues in וישב האיש בביתו show that the man is located in his own house?",
            [
                "וישב signals staying, ב marks location, and ו marks his possession",
                "וישב signals movement, ב marks direction, and ו marks the object",
                "וישב signals giving, ב marks source, and ו marks her possession",
                "וישב signals seeing, ב marks comparison, and ו marks plural possession",
            ],
            "וישב signals staying, ב marks location, and ו marks his possession",
            "וישב gives the action, ב gives location, and ו gives possession.",
            5,
            "combined_grammar",
            "contextual_sentence",
        ),
        make_question(
            "combined_context",
            "CF",
            "CF4",
            by_word["מביתו"]["word"],
            by_word["מביתו"]["source"],
            "Why does מביתו in ויצא האיש מביתו mean movement away from his house?",
            [
                "ויצא signals leaving, מ marks from, and ו marks his possession",
                "ויצא signals staying, מ marks in, and ו marks his possession",
                "ויצא signals going toward, מ marks to, and ו marks the object",
                "ויצא signals seeing, מ marks with, and ו marks plural possession",
            ],
            "ויצא signals leaving, מ marks from, and ו marks his possession",
            "ויצא gives the action of leaving, מ gives 'from', and ו gives 'his'.",
            5,
            "combined_grammar",
            "contextual_sentence",
        ),
        make_question(
            "combined_reasoning",
            "CF",
            "CF4",
            "בית",
            by_word["בביתו"]["source"],
            "How does adding ו to בבית change the meaning?",
            [
                "It keeps the location meaning and adds possession: in the house becomes in his house",
                "It changes location into movement: in the house becomes from the house",
                "It removes the prefix meaning: in the house becomes his house only",
                "It changes the owner and direction: in the house becomes to her house",
            ],
            "It keeps the location meaning and adds possession: in the house becomes in his house",
            "Both forms keep ב = in; בביתו adds ו = his.",
            5,
            "combined_grammar",
            "reasoning",
        ),
    ]


def pick_words(words, word_list):
    by_word = {entry["word"]: entry for entry in words}
    return [by_word[word] for word in word_list if word in by_word]


def build_grammar_questions(words):
    prefix_entries = pick_words(
        words,
        ["וילך", "וירא", "ויאמר", "ויתן", "ויקח", "בבית", "לבית", "מבית", "בארץ", "לארץ", "מארץ"],
    )
    suffix_entries = [entry for entry in words if entry.get("suffix") and entry.get("suffix_meaning")]
    tense_entries = pick_words(
        words,
        ["וילך", "וירא", "ויאמר", "ויבא", "ויצא", "ויעל", "וירד", "וישב", "ויתן", "ויקח"],
    )
    shoresh_entries = pick_words(
        words,
        ["וילך", "וירא", "ויאמר", "ויבא", "ויצא", "ויעל", "וירד", "וישב", "ויתן", "ויקח"],
    )
    combined_entries = pick_words(
        words,
        ["בביתו", "לבנו", "מביתו"],
    )

    return (
        make_prefix_questions(prefix_entries)
        + make_suffix_questions(suffix_entries)
        + make_tense_questions(tense_entries)
        + make_shoresh_questions(shoresh_entries)
        + make_combined_questions(combined_entries)
    )


def integration_test(words):
    selected = next(entry for entry in words if entry["word"] == "עלה")
    distractors = [
        entry
        for entry in words
        if entry["group"] == selected["group"] and entry["word"] != selected["word"]
    ][:3]
    question = {
        "skill": "sentence_structure",
        "standard": "SS",
        "micro_standard": "SS2",
        "word": "איש עלה אל הר",
        "selected_word": selected["word"],
        "question": "What is the action in איש עלה אל הר?",
        "choices": [selected["translation"]] + [entry["translation"] for entry in distractors],
        "correct_answer": selected["translation"],
        "difficulty": 3,
        "generation_group": selected["group"],
    }

    print("Integration test")
    print(f"Word: {selected['word']}")
    print(f"Group: {selected['group']}")
    print(f"Translation: {selected['translation']}")
    print("Choices built from: " + ", ".join(entry["word"] for entry in distractors))
    print(json.dumps(question, indent=2, ensure_ascii=False))


def main():
    data = load_word_bank()
    normalize_word_bank(data)
    WORD_BANK_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    questions = build_grammar_questions(data["words"])
    OUTPUT_PATH.write_text(
        json.dumps({"questions": questions}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    integration_test(data["words"])
    print(f"Grammar questions written: {len(questions)}")


if __name__ == "__main__":
    main()
