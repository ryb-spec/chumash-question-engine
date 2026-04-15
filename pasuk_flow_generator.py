import json
import random
import hashlib
from pathlib import Path


WORD_BANK_PATH = Path("word_bank.json")
OUTPUT_PATH = Path("pasuk_flow_questions.json")
LETTER_MEANING_QUESTIONS_PATH = Path("data/skills/letter_meaning/questions_walder.json")
WORD_STRUCTURE_QUESTIONS_PATH = Path("data/skills/word_structure/questions.json")

EXAMPLE_PESUKIM = [
    "וילך האיש מביתו אל העיר",
    "ויתן האב לחם לבנו",
]

EXAMPLE_MULTI_PESUKIM = [
    "וילך האיש מביתו אל העיר",
    "ויתן האב לחם לבנו",
    "וישב האיש בביתו",
]

KNOWN_PREFIXES = {
    "ה": "the",
}

SKILLS = [
    "identify_prefix_meaning",
    "identify_suffix_meaning",
    "identify_pronoun_suffix",
    "identify_verb_marker",
    "segment_word_parts",
    "identify_tense",
    "identify_prefix_future",
    "identify_suffix_past",
    "identify_present_pattern",
    "convert_future_to_command",
    "match_pronoun_to_verb",
    "shoresh",
    "prefix",
    "suffix",
    "verb_tense",
    "part_of_speech",
    "translation",
    "subject_identification",
    "object_identification",
    "preposition_meaning",
    "phrase_translation",
]

SKILL_GROUP_ORDER = [
    "letter_meaning",
    "word_structure",
    "word_meaning",
    "sentence_structure",
    "pasuk_flow",
]

SKILL_METADATA = {
    "identify_prefix_meaning": {
        "standard": "PR",
        "micro_standard": "PR1",
        "difficulty": 1,
    },
    "identify_suffix_meaning": {
        "standard": "PR",
        "micro_standard": "PR2",
        "difficulty": 1,
    },
    "identify_pronoun_suffix": {
        "standard": "PR",
        "micro_standard": "PR2",
        "difficulty": 1,
    },
    "identify_verb_marker": {
        "standard": "PR",
        "micro_standard": "PR1",
        "difficulty": 1,
    },
    "segment_word_parts": {
        "standard": "PR",
        "micro_standard": "PR5",
        "difficulty": 2,
    },
    "identify_tense": {
        "standard": "PR",
        "micro_standard": "PR5",
        "difficulty": 2,
    },
    "identify_prefix_future": {
        "standard": "PR",
        "micro_standard": "PR1",
        "difficulty": 2,
    },
    "identify_suffix_past": {
        "standard": "PR",
        "micro_standard": "PR2",
        "difficulty": 3,
    },
    "identify_present_pattern": {
        "standard": "PR",
        "micro_standard": "PR5",
        "difficulty": 3,
    },
    "convert_future_to_command": {
        "standard": "PR",
        "micro_standard": "PR5",
        "difficulty": 4,
    },
    "match_pronoun_to_verb": {
        "standard": "PR",
        "micro_standard": "PR5",
        "difficulty": 3,
    },
    "shoresh": {
        "standard": "SR",
        "micro_standard": "SR1",
        "difficulty": 3,
    },
    "prefix": {
        "standard": "PR",
        "micro_standard": "PR1",
        "difficulty": 3,
    },
    "suffix": {
        "standard": "PR",
        "micro_standard": "PR2",
        "difficulty": 3,
    },
    "verb_tense": {
        "standard": "PR",
        "micro_standard": "PR5",
        "difficulty": 3,
    },
    "part_of_speech": {
        "standard": "PS",
        "micro_standard": "PS1",
        "difficulty": 2,
    },
    "translation": {
        "standard": "WM",
        "micro_standard": "WM1",
        "difficulty": 2,
    },
    "subject_identification": {
        "standard": "SS",
        "micro_standard": "SS1",
        "difficulty": 4,
    },
    "object_identification": {
        "standard": "SS",
        "micro_standard": "SS3",
        "difficulty": 4,
    },
    "preposition_meaning": {
        "standard": "PR",
        "micro_standard": "PR1",
        "difficulty": 3,
    },
    "phrase_translation": {
        "standard": "PS",
        "micro_standard": "PS4",
        "difficulty": 4,
    },
}

PREFIX_MEANING_CHOICES = {
    "ב": ["in", "to", "from", "on"],
    "ל": ["to", "in", "from", "with"],
    "מ": ["from", "to", "in", "on"],
    "ו": ["and / narrative past", "the", "to", "from"],
    "ה": ["the", "and", "to", "from"],
}


def load_word_bank():
    data = json.loads(WORD_BANK_PATH.read_text(encoding="utf-8"))
    entries = data.get("words", [])
    by_word = {entry["word"]: entry for entry in entries}
    by_group = {}
    for entry in entries:
        by_group.setdefault(entry.get("group", "unknown"), []).append(entry)
    return by_word, by_group


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_letter_meaning_questions():
    return load_json(LETTER_MEANING_QUESTIONS_PATH)


def load_word_structure_questions():
    return load_json(WORD_STRUCTURE_QUESTIONS_PATH)


def format_static_skill_question(question):
    metadata = SKILL_METADATA[question["skill"]]
    choices = question["choices"]
    if len(choices) != 4:
        raise ValueError(f"Static skill question must have 4 choices: {question['id']}")
    if len(set(choices)) != 4:
        raise ValueError(f"Static skill question has duplicate choices: {question['id']}")
    if question["correct"] not in choices:
        raise ValueError(f"Correct answer missing from choices: {question['id']}")

    payload = {
        "id": question["id"],
        "question_text": question["question"],
        "question": question["question"],
        "choices": choices,
        "correct_answer": question["correct"],
        "skill_group": question["skill_group"],
        "skill": question["skill"],
        "question_type": question["skill"],
        "mode": "word",
        "standard": metadata["standard"],
        "micro_standard": metadata["micro_standard"],
        "difficulty": question.get("difficulty", metadata["difficulty"]),
        "word": question["word"],
        "selected_word": question["word"],
        "explanation": f"{question['correct']} is the correct letter.",
        "source": question.get("source", "walder_packet"),
    }
    return validate_question_payload(payload)


def generate_static_skill_question(
    questions,
    skill=None,
    difficulty=None,
    asked_question_ids=None,
):
    asked = set(asked_question_ids or [])
    candidates = [
        question
        for question in questions
        if (skill is None or question["skill"] == skill)
        and (difficulty is None or question.get("difficulty") == difficulty)
    ]
    if not candidates:
        candidates = [
            question
            for question in questions
            if skill is None or question["skill"] == skill
        ]
    if not candidates:
        raise ValueError(f"No static questions found for skill: {skill}")

    unused = [question for question in candidates if question["id"] not in asked]
    selected = random.choice(unused or candidates)
    return format_static_skill_question(selected)


def generate_letter_meaning_question(skill=None, difficulty=None, asked_question_ids=None):
    return generate_static_skill_question(
        load_letter_meaning_questions(),
        skill=skill,
        difficulty=difficulty,
        asked_question_ids=asked_question_ids,
    )


def generate_word_structure_question(skill=None, difficulty=None, asked_question_ids=None):
    return generate_static_skill_question(
        load_word_structure_questions(),
        skill=skill,
        difficulty=difficulty,
        asked_question_ids=asked_question_ids,
    )


def generate_diagnostic_questions():
    required_skills = [
        "identify_prefix_meaning",
        "identify_suffix_meaning",
        "identify_verb_marker",
    ]
    return [
        generate_letter_meaning_question(skill=skill)
        for skill in required_skills
    ]


def normalize_token(token, word_bank):
    if token in word_bank:
        return {"token": token, "entry": dict(word_bank[token]), "base": token}

    for prefix, meaning in KNOWN_PREFIXES.items():
        if token.startswith(prefix):
            base = token[len(prefix):]
            if base in word_bank:
                entry = dict(word_bank[base])
                entry["word"] = token
                entry["prefix"] = prefix
                entry["prefix_meaning"] = meaning
                entry["translation"] = f"{meaning} {word_bank[base]['translation']}"
                return {"token": token, "entry": entry, "base": base}

    return None


def analyze_pasuk(pasuk, word_bank):
    analyzed = []
    unknown = []
    for token in pasuk.split():
        item = normalize_token(token, word_bank)
        if item is None:
            unknown.append(token)
        else:
            analyzed.append(item)

    if unknown:
        raise ValueError(f"Unknown word(s) not in word bank: {', '.join(unknown)}")

    return analyzed


def stable_rng(key):
    return random.Random(key)


def unique(items):
    result = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result


def build_choices(correct, partials, clear, key):
    choices = unique([correct] + partials[:2] + [clear])
    if len(choices) < 4:
        raise ValueError(f"Need 4 unique choices. Got: {choices}")
    choices = choices[:4]
    stable_rng(key).shuffle(choices)
    return choices


def find_first(analyzed, predicate):
    for item in analyzed:
        if predicate(item["entry"], item["token"]):
            return item
    return None


def find_after(analyzed, start_index, predicate):
    for item in analyzed[start_index + 1:]:
        if predicate(item["entry"], item["token"]):
            return item
    return None


def describe(item):
    return item["entry"]["translation"]


def clean_action(text):
    for lead in ["and he ", "and it "]:
        if text.startswith(lead):
            return text[len(lead):]
    return text


def strip_relation(text):
    for lead in ["from ", "to ", "in ", "on ", "with "]:
        if text.startswith(lead):
            return text[len(lead):]
    return text


def root_meaning(entry):
    text = entry.get("translation", "")
    for lead in [
        "from his ",
        "to his ",
        "in his ",
        "from the ",
        "to the ",
        "in the ",
        "the ",
        "his ",
    ]:
        if text.startswith(lead):
            return text[len(lead):]
    return text


def group_distractors(entry, by_group, limit=3):
    return [
        item["translation"]
        for item in by_group.get(entry.get("group"), [])
        if item["translation"] != entry["translation"]
    ][:limit]


def different_group_distractor(entry, by_group):
    for group, items in by_group.items():
        if group != entry.get("group") and items:
            return items[0]["translation"]
    return "not related"


def question_id_for(question):
    base = "|".join(
        [
            str(question.get("skill", "")),
            str(question.get("question_type", "")),
            str(question.get("word", "")),
            str(question.get("question", "")),
            str(question.get("correct_answer", "")),
        ]
    )
    return hashlib.sha1(base.encode("utf-8")).hexdigest()[:12]


def validate_question_payload(question):
    choices = question.get("choices", [])
    if len(choices) != 4:
        raise ValueError(f"Question must have exactly 4 choices: {question.get('question')}")
    if len(set(choices)) != 4:
        raise ValueError(f"Question choices must be unique: {question.get('question')}")
    if question.get("correct_answer") not in choices:
        raise ValueError(f"Correct answer is missing from choices: {question.get('question')}")
    question.setdefault("id", question_id_for(question))
    return question


def make_question(
    step,
    skill,
    standard,
    micro_standard,
    question_type,
    word,
    text,
    choices,
    correct_answer,
    explanation,
    difficulty,
):
    return validate_question_payload({
        "step": step,
        "skill": skill,
        "mode": "pasuk" if question_type in {"phrase_meaning", "subject_identification"} else "word",
        "standard": standard,
        "micro_standard": micro_standard,
        "question_type": question_type,
        "word": word,
        "selected_word": word,
        "question": text,
        "choices": choices,
        "correct_answer": correct_answer,
        "explanation": explanation,
        "difficulty": difficulty,
        "source": "generated pasuk flow",
    })


def get_verb(analyzed):
    return find_first(analyzed, lambda entry, _token: entry.get("type") == "verb") or analyzed[0]


def get_prefixed_word(analyzed):
    return find_first(analyzed, lambda entry, _token: bool(entry.get("prefix")))


def get_suffixed_word(analyzed):
    return find_first(analyzed, lambda entry, _token: bool(entry.get("suffix")))


def get_translatable_word(analyzed):
    return (
        find_first(analyzed, lambda entry, _token: bool(entry.get("translation")))
        or analyzed[0]
    )


def get_part_of_speech_word(analyzed):
    return (
        find_first(analyzed, lambda entry, _token: entry.get("type") in {"verb", "noun"})
        or analyzed[0]
    )


def infer_tense(entry, token):
    if entry.get("tense"):
        return entry["tense"]
    if entry.get("type") == "verb" and token.startswith("וי"):
        return "past"
    return "not a verb"


def choice_pool(values, correct, fallback):
    choices = unique([correct] + [value for value in values if value != correct] + fallback)
    return choices[:4]


def skill_question_payload(skill, target, question_text, choices, correct_answer, explanation):
    metadata = SKILL_METADATA[skill]
    return validate_question_payload({
        "question_text": question_text,
        "question": question_text,
        "choices": choices,
        "correct_answer": correct_answer,
        "skill": skill,
        "mode": "pasuk" if skill in {"subject_identification", "phrase_translation"} else "word",
        "standard": metadata["standard"],
        "micro_standard": metadata["micro_standard"],
        "difficulty": metadata["difficulty"],
        "word": target["token"],
        "selected_word": target["token"],
        "explanation": explanation,
        "source": "generated skill question",
    })


def generate_question(
    skill,
    pasuk,
    mode="direct",
    asked_tokens=None,
    asked_question_types=None,
):
    if skill not in SKILLS:
        raise ValueError(f"Unknown skill: {skill}. Expected one of: {', '.join(SKILLS)}")
    if mode not in {"direct", "context", "selection"}:
        raise ValueError("mode must be one of: direct, context, selection")
    if skill in {
        "identify_prefix_meaning",
        "identify_suffix_meaning",
        "identify_pronoun_suffix",
        "identify_verb_marker",
        "segment_word_parts",
    }:
        return generate_letter_meaning_question(skill=skill, asked_question_ids=asked_tokens)
    if skill in {
        "identify_tense",
        "identify_prefix_future",
        "identify_suffix_past",
        "identify_present_pattern",
        "convert_future_to_command",
        "match_pronoun_to_verb",
    }:
        return generate_word_structure_question(skill=skill, asked_question_ids=asked_tokens)

    word_bank, by_group = load_word_bank()
    analyzed = analyze_pasuk(pasuk, word_bank)
    asked_set = set(asked_tokens or [])
    used_types = set(asked_question_types or [])

    def finish(question):
        if mode == "selection":
            question["hide_focus_word"] = True
        return validate_question_payload(question)

    def clean_choices(correct, candidates):
        choices = unique([correct] + [item for item in candidates if item and item != correct])
        if len(choices) < 4:
            choices = unique(
                choices
                + [
                    entry.get("translation")
                    for entry in word_bank.values()
                    if entry.get("translation") != correct
                ]
            )
        if len(choices) < 4:
            raise ValueError(f"Could not build 4 clean choices for {skill}: {choices}")
        choices = choices[:4]
        stable_rng(f"{pasuk}|{skill}|choices").shuffle(choices)
        return choices

    def same_group_translation_choices(target_entry, correct):
        same_group = [
            entry.get("translation")
            for entry in by_group.get(target_entry.get("group"), [])
            if entry.get("translation") != correct
        ]
        same_type = [
            entry.get("translation")
            for entry in word_bank.values()
            if entry.get("type") == target_entry.get("type")
            and entry.get("translation") != correct
        ]
        return clean_choices(correct, same_group + same_type)

    def pasuk_word_choices(correct_token):
        return clean_choices(
            correct_token,
            [item["token"] for item in analyzed if item["token"] != correct_token],
        )

    def prompt(direct_text, context_text, selection_text):
        if mode == "context":
            return context_text
        if mode == "selection":
            return selection_text
        return direct_text

    def choose_target(predicate, fallback=None):
        candidates = [item for item in analyzed if predicate(item["entry"], item["token"])]
        if not candidates and fallback is not None:
            return fallback()
        if not candidates:
            return analyzed[0]

        unused = [item for item in candidates if item["token"] not in asked_set]
        return (unused or candidates)[0]

    def people_translation_choices(correct):
        return clean_choices(
            correct,
            [
                entry["translation"]
                for entry in by_group.get("people", [])
                if entry.get("translation") != correct
            ],
        )

    def noun_translation_choices(correct):
        return clean_choices(
            correct,
            [
                entry["translation"]
                for entry in word_bank.values()
                if entry.get("type") == "noun"
                and entry.get("translation") != correct
            ],
        )

    def phrase_parts():
        source = get_source(analyzed)
        marker, destination = get_destination(analyzed)
        recipient = get_recipient(analyzed)
        direct_object = get_direct_object(analyzed)
        phrase_options = []

        if source and marker and destination:
            phrase = f"{source['token']} {marker['token']} {destination['token']}"
            source_text = strip_relation(describe(source))
            destination_text = strip_relation(describe(destination))
            correct = f"from {source_text} to {destination_text}"
            candidates = [
                f"in {source_text} to {destination_text}",
                f"from {destination_text} to {source_text}",
                f"from {source_text} in {destination_text}",
                f"to {source_text} from {destination_text}",
            ]
            phrase_options.append((phrase, correct, candidates))

        if direct_object and recipient:
            phrase = f"{direct_object['token']} {recipient['token']}"
            recipient_text = strip_relation(describe(recipient))
            correct = f"{describe(direct_object)} to {recipient_text}"
            candidates = [
                f"{describe(direct_object)} from {recipient_text}",
                f"{describe(direct_object)} in {recipient_text}",
                f"{recipient_text} to {describe(direct_object)}",
                f"{describe(direct_object)} with {recipient_text}",
            ]
            phrase_options.append((phrase, correct, candidates))

        phrase_items = analyzed[:2]
        phrase = " ".join(item["token"] for item in phrase_items)
        correct = " ".join(describe(item) for item in phrase_items)
        candidates = [
            " ".join(reversed([describe(item) for item in phrase_items])),
            f"{describe(phrase_items[0])} in {describe(phrase_items[-1])}",
            f"{describe(phrase_items[0])} from {describe(phrase_items[-1])}",
            f"{describe(phrase_items[-1])} to {describe(phrase_items[0])}",
        ]
        phrase_options.append((phrase, correct, candidates))

        unused = [item for item in phrase_options if item[0] not in asked_set]
        return (unused or phrase_options)[0]

    if skill == "shoresh":
        target = choose_target(
            lambda entry, _token: entry.get("type") == "verb",
            lambda: get_verb(analyzed),
        )
        correct = target["entry"].get("shoresh", target["token"])
        if mode == "selection":
            return finish(skill_question_payload(
                skill,
                target,
                f"Which word has shoresh {correct}?",
                pasuk_word_choices(target["token"]),
                target["token"],
                f"{target['token']} has shoresh {correct}.",
            ))
        choices = clean_choices(
            correct,
            [
                entry.get("shoresh")
                for entry in word_bank.values()
                if entry.get("type") == "verb"
            ],
        )
        return skill_question_payload(
            skill,
            target,
            prompt(
                f"What is the shoresh of {target['token']}?",
                f"What is the shoresh of {target['token']}?",
                "",
            ),
            choices,
            correct,
            f"The shoresh of {target['token']} is {correct}.",
        )

    if skill == "prefix":
        target = choose_target(
            lambda entry, _token: bool(entry.get("prefix")),
            lambda: get_prefixed_word(analyzed),
        )
        if target is None:
            raise ValueError("No prefixed word found in this pasuk.")
        prefix = target["entry"].get("prefix", "")
        correct = target["entry"].get("prefix_meaning", "")
        if mode == "selection":
            return finish(skill_question_payload(
                skill,
                target,
                f"Which word contains a prefix meaning \"{correct}\"?",
                pasuk_word_choices(target["token"]),
                target["token"],
                f"{target['token']} contains the prefix {prefix}, meaning '{correct}'.",
            ))
        choices = clean_choices(
            correct,
            PREFIX_MEANING_CHOICES.get(prefix, [])
            + ["and / narrative past", "the", "in", "to", "from", "on"],
        )
        return skill_question_payload(
            skill,
            target,
            prompt(
                f"What does the prefix {prefix} add?",
                f"What does the prefix {prefix} add?",
                "",
            ),
            choices,
            correct,
            f"In {target['token']}, the prefix {prefix} means '{correct}'.",
        )

    if skill == "suffix":
        target = choose_target(
            lambda entry, _token: bool(entry.get("suffix")),
            lambda: get_suffixed_word(analyzed),
        )
        if target is None:
            raise ValueError("No suffixed word found in this pasuk.")
        suffix = target["entry"].get("suffix", "")
        correct = target["entry"].get("suffix_meaning", "")
        if mode == "selection":
            return finish(skill_question_payload(
                skill,
                target,
                f"Which word contains a suffix meaning \"{correct}\"?",
                pasuk_word_choices(target["token"]),
                target["token"],
                f"{target['token']} contains the suffix {suffix}, meaning '{correct}'.",
            ))
        choices = clean_choices(correct, ["my", "your", "his", "her", "our", "their"])
        return skill_question_payload(
            skill,
            target,
            prompt(
                f"What does the suffix {suffix} add?",
                f"What does the suffix {suffix} add?",
                "",
            ),
            choices,
            correct,
            f"In {target['token']}, the suffix {suffix} means '{correct}'.",
        )

    if skill == "verb_tense":
        target = choose_target(
            lambda entry, _token: entry.get("type") == "verb",
            lambda: get_verb(analyzed),
        )
        correct = infer_tense(target["entry"], target["token"])
        if mode == "selection":
            return finish(skill_question_payload(
                skill,
                target,
                f"Which word shows {correct} tense?",
                pasuk_word_choices(target["token"]),
                target["token"],
                f"{target['token']} shows {correct} tense.",
            ))
        choices = clean_choices(correct, ["past", "future", "basic command", "not a verb"])
        return skill_question_payload(
            skill,
            target,
            prompt(
                "What verb tense is shown?",
                "What verb tense is shown?",
                "",
            ),
            choices,
            correct,
            f"{target['token']} is read as {correct}.",
        )

    if skill == "part_of_speech":
        target = choose_target(
            lambda entry, _token: entry.get("type") in {"verb", "noun"},
            lambda: get_part_of_speech_word(analyzed),
        )
        correct = target["entry"].get("type", "unknown")
        student_correct = "action" if correct == "verb" else "person/thing"
        if mode == "selection":
            return finish(skill_question_payload(
                skill,
                target,
                f"Which word is an {student_correct}?",
                pasuk_word_choices(target["token"]),
                target["token"],
                f"{target['token']} is a {student_correct}.",
            ))
        choices = ["person/thing", "action"]
        return skill_question_payload(
            skill,
            target,
            prompt(
                f"Is {target['token']} a person/thing or an action?",
                f"Is {target['token']} a person/thing or an action?",
                "",
            ),
            choices,
            student_correct,
            f"{target['token']} is an {student_correct}.",
        )

    if skill == "subject_identification":
        target = choose_target(
            lambda entry, _token: entry.get("group") == "people",
            lambda: get_subject(analyzed),
        )
        correct = target["entry"]["translation"]
        if mode == "selection":
            return finish(skill_question_payload(
                skill,
                target,
                "Which word is doing the action?",
                pasuk_word_choices(target["token"]),
                target["token"],
                f"{target['token']} is doing the action.",
            ))
        choices = people_translation_choices(correct)
        return skill_question_payload(
            skill,
            target,
            prompt(
                "Who is doing the action?",
                "Who is doing the action?",
                "",
            ),
            choices,
            correct,
            f"{target['token']} is the one doing the action.",
        )

    if skill == "object_identification":
        target = (
            get_direct_object(analyzed)
            or choose_target(
                lambda entry, _token: entry.get("type") == "noun"
                and entry.get("group") != "people"
                and not entry.get("prefix"),
            )
        )
        correct = target["entry"]["translation"]
        choices = noun_translation_choices(correct)
        return skill_question_payload(
            skill,
            target,
            "What did the action happen to?",
            choices,
            correct,
            f"The action happened to {correct}.",
        )

    if skill == "preposition_meaning":
        target = choose_target(
            lambda entry, _token: entry.get("type") == "prep"
            or entry.get("prefix") in {"ב", "ל", "מ"},
        )
        prefix = target["entry"].get("prefix", "")
        correct = target["entry"].get("prefix_meaning") or target["entry"].get("translation")
        display_word = prefix or target["token"]
        choices = clean_choices(correct, ["to", "from", "in", "on"])
        return skill_question_payload(
            skill,
            target,
            f"What does {display_word} mean?",
            choices,
            correct,
            f"{display_word} means '{correct}'.",
        )

    if skill == "phrase_translation":
        phrase, correct, candidates = phrase_parts()
        if mode == "selection":
            phrase_tokens = phrase.split()
            distractors = []
            for index in range(len(analyzed) - 1):
                candidate = " ".join(item["token"] for item in analyzed[index:index + 2])
                if candidate != phrase:
                    distractors.append(candidate)
            choices = clean_choices(phrase, distractors)
            return finish(skill_question_payload(
                skill,
                {"token": phrase, "entry": {"translation": correct}},
                "Which phrase has this meaning?",
                choices,
                phrase,
                f"{phrase} means '{correct}'.",
            ))
        choices = clean_choices(correct, candidates)
        return skill_question_payload(
            skill,
            {"token": phrase, "entry": {"translation": correct}},
            prompt(
                "What does this phrase mean?",
                "What does this phrase mean?",
                "",
            ),
            choices,
            correct,
            f"{phrase} means '{correct}'.",
        )

    target = choose_target(
        lambda entry, _token: bool(entry.get("translation")),
        lambda: get_translatable_word(analyzed),
    )
    correct = target["entry"]["translation"]
    if mode == "selection":
        question = finish(skill_question_payload(
            skill,
            target,
            f"Which Hebrew word means \"{correct}\"?",
            pasuk_word_choices(target["token"]),
            target["token"],
            f"{target['token']} means '{correct}'.",
        ))
        question["hide_pasuk"] = True
        question["hide_focus_word"] = True
        return question
    choices = same_group_translation_choices(target["entry"], correct)
    return skill_question_payload(
        skill,
        target,
        prompt(
            f"What does {target['token']} mean?",
            f"What does {target['token']} mean?",
            "",
        ),
        choices,
        correct,
        f"{target['token']} means '{correct}'.",
    )


def get_subject(analyzed):
    verb = get_verb(analyzed)
    verb_index = analyzed.index(verb)
    return (
        find_after(analyzed, verb_index, lambda entry, _token: entry.get("group") == "people")
        or find_first(analyzed, lambda entry, _token: entry.get("group") == "people")
        or analyzed[0]
    )


def get_source(analyzed):
    return find_first(analyzed, lambda entry, _token: entry.get("prefix") == "מ")


def get_recipient(analyzed):
    return find_first(analyzed, lambda entry, _token: entry.get("prefix") == "ל")


def get_destination(analyzed):
    marker = find_first(
        analyzed,
        lambda entry, token: token == "אל" or entry.get("prefix") == "ל",
    )
    if marker is None:
        return None, None

    marker_index = analyzed.index(marker)
    obj = find_after(
        analyzed,
        marker_index,
        lambda entry, _token: entry.get("group") in {"place", "people"},
    )
    return marker, obj


def get_direct_object(analyzed):
    return find_first(
        analyzed,
        lambda entry, _token: entry.get("group") in {"object", "place"}
        and not entry.get("prefix"),
    )


def get_prefixed_or_suffixed(analyzed):
    return (
        find_first(analyzed, lambda entry, _token: entry.get("prefix") and entry.get("suffix"))
        or find_first(
            analyzed,
            lambda entry, _token: (entry.get("prefix") or entry.get("suffix"))
            and entry.get("type") != "verb",
        )
        or find_first(analyzed, lambda entry, _token: entry.get("prefix") or entry.get("suffix"))
        or analyzed[0]
    )


def build_translation_question(step, pasuk, analyzed, by_group):
    target = get_verb(analyzed)
    entry = target["entry"]
    choices = build_choices(
        entry["translation"],
        group_distractors(entry, by_group, 2),
        different_group_distractor(entry, by_group),
        f"{pasuk}|wm",
    )
    return make_question(
        step,
        "translation",
        "WM",
        "WM1",
        "word_meaning",
        target["token"],
        f"What does {target['token']} mean?",
        choices,
        entry["translation"],
        f"{target['token']} means '{entry['translation']}'.",
        2,
    )


def build_pr_question(step, pasuk, analyzed):
    target = get_prefixed_or_suffixed(analyzed)
    entry = target["entry"]
    prefix = entry.get("prefix", "")
    suffix = entry.get("suffix", "")
    prefix_meaning = entry.get("prefix_meaning", "")
    suffix_meaning = entry.get("suffix_meaning", "")

    if prefix and suffix:
        base = root_meaning(entry)
        correct = f"{prefix} = {prefix_meaning}, {entry['shoresh']} = {base}, {suffix} = {suffix_meaning}"
        partials = [
            f"{prefix} = in, {entry['shoresh']} = {base}, {suffix} = {suffix_meaning}",
            f"{prefix} = {prefix_meaning}, {entry['shoresh']} = {base}, {suffix} = her",
        ]
        clear = f"{prefix} = and, {entry['shoresh']} = action, {suffix} = plural"
        micro_standard = "PR5"
    elif prefix:
        correct = prefix_meaning
        partials = [item for item in PREFIX_MEANING_CHOICES.get(prefix, []) if item != correct][:2]
        clear = "possession"
        micro_standard = "PR1"
    elif suffix:
        correct = suffix_meaning
        partials = ["her", "their"]
        clear = "and"
        micro_standard = "PR2"
    else:
        correct = entry["translation"]
        partials = ["to", "from"]
        clear = "not a grammar clue"
        micro_standard = "PR1"

    choices = build_choices(correct, partials, clear, f"{pasuk}|pr")
    prompt = stable_rng(f"{pasuk}|pr_prompt").choice(
        [
            f"What does {target['token']} add?",
            f"What does {target['token']} add?",
            f"What does {target['token']} add?",
        ]
    )
    return make_question(
        step,
        "prefix_suffix",
        "PR",
        micro_standard,
        "prefix_suffix",
        target["token"],
        prompt,
        choices,
        correct,
        f"{target['token']} is read as '{entry['translation']}'.",
        3,
    )


def build_phrase_question(step, pasuk, analyzed):
    source = get_source(analyzed)
    marker, destination = get_destination(analyzed)
    recipient = get_recipient(analyzed)
    direct_object = get_direct_object(analyzed)
    subject = get_subject(analyzed)

    if source and marker and destination:
        phrase = f"{source['token']} {marker['token']} {destination['token']}"
        source_text = strip_relation(describe(source))
        destination_text = strip_relation(describe(destination))
        correct = f"from {source_text} to {destination_text}"
        partials = [
            f"from {source_text} in {destination_text}",
            f"from {destination_text} to {source_text}",
        ]
        clear = f"from {source_text} to {strip_relation(describe(subject))}"
    elif recipient and direct_object:
        phrase = f"{direct_object['token']} {recipient['token']}"
        recipient_text = strip_relation(describe(recipient))
        correct = f"{describe(direct_object)} to {recipient_text}"
        partials = [
            f"{describe(direct_object)} from {recipient_text}",
            f"{describe(direct_object)} with {recipient_text}",
        ]
        clear = f"{describe(direct_object)} to {strip_relation(describe(subject))}"
    else:
        phrase_items = analyzed[:2]
        phrase = " ".join(item["token"] for item in phrase_items)
        correct = " ".join(describe(item) for item in phrase_items)
        partials = [
            " ".join(reversed([describe(item) for item in phrase_items])),
            f"{describe(phrase_items[0])} in {describe(phrase_items[-1])}",
        ]
        clear = f"{describe(phrase_items[-1])} from {describe(phrase_items[0])}"

    choices = build_choices(correct, partials, clear, f"{pasuk}|phrase")
    return make_question(
        step,
        "phrase",
        "PS",
        "PS4",
        "phrase_meaning",
        phrase,
        "What does this phrase mean?",
        choices,
        correct,
        f"{phrase} functions as a combined phrase unit in the pasuk.",
        4,
    )


def build_subject_question(step, pasuk, analyzed, by_group):
    subject = get_subject(analyzed)
    correct = subject["entry"]["translation"]
    distractors = [
        entry["translation"]
        for entry in by_group.get("people", [])
        if entry.get("translation") != correct
    ]
    choices = build_choices(
        correct,
        distractors[:2],
        distractors[2] if len(distractors) > 2 else "servant",
        f"{pasuk}|subject",
    )
    return make_question(
        step,
        "subject_identification",
        "SS",
        "SS1",
        "subject_identification",
        subject["token"],
        "Who is doing the action?",
        choices,
        correct,
        f"{subject['token']} is doing the action.",
        4,
    )


def build_flow_question(step, pasuk, analyzed):
    source = get_source(analyzed)
    marker, destination = get_destination(analyzed)
    recipient = get_recipient(analyzed)
    direct_object = get_direct_object(analyzed)
    subject = get_subject(analyzed)
    verb = get_verb(analyzed)

    if source and marker and destination:
        source_text = strip_relation(describe(source))
        destination_text = strip_relation(describe(destination))
        correct = f"{source['token']} must be read as the starting point before {marker['token']} {destination['token']} can be read as the destination"
        partials = [
            f"{marker['token']} {destination['token']} must be read as the starting point before {source['token']} can be read as the destination",
            f"{source['token']} gives possession, while {marker['token']} {destination['token']} alone gives the full movement",
        ]
        clear = f"{subject['token']} must be read as the destination before {verb['token']} gives the action"
        explanation = "The flow depends on reading source and destination together."
        prompt = "What comes first?"
    elif recipient and direct_object:
        recipient_text = strip_relation(describe(recipient))
        correct = f"{direct_object['token']} must be read as the object before {recipient['token']} can mark the receiver"
        partials = [
            f"{recipient['token']} must be read as the object before {direct_object['token']} can mark the receiver",
            f"{verb['token']} shows transfer, but {recipient['token']} only shows possession and not receiver",
        ]
        clear = f"{subject['token']} must be read as the receiver before {direct_object['token']} gives the object"
        explanation = "The flow depends on distinguishing the object from the receiver."
        prompt = "Who gets the action?"
    else:
        correct = f"{verb['token']} must be read as the action before {subject['token']} can be understood as the performer"
        partials = [
            f"{subject['token']} must be read as the action before {verb['token']} can be understood as the performer",
            f"{verb['token']} gives the action, but {subject['token']} only gives a location",
        ]
        clear = f"{subject['token']} gives the receiver, and {verb['token']} gives the object"
        explanation = "The flow begins with the action and is anchored by the subject."
        prompt = "What is the action?"

    choices = build_choices(correct, partials, clear, f"{pasuk}|flow")
    return make_question(
        step,
        "flow",
        "SS",
        "SS5",
        "flow_dependency",
        pasuk,
        prompt,
        choices,
        correct,
        explanation,
        5,
    )


def build_substitution_question(step, pasuk, analyzed):
    source = get_source(analyzed)
    recipient = get_recipient(analyzed)
    marker, destination = get_destination(analyzed)

    if source:
        prompt_variant = "impossible"
        old = source["token"]
        replacement = f"ב{source['token'][1:]}" if old.startswith("מ") else f"ב{old}"
        correct = "movement away from that place would no longer be possible"
        partials = [
            "movement toward the destination would no longer be possible",
            "possession by the same person would no longer be possible",
        ]
        clear = "the source clue would turn into a location-inside clue"
    elif recipient:
        prompt_variant = "new_meaning"
        old = recipient["token"]
        replacement = f"מ{recipient['token'][1:]}" if old.startswith("ל") else f"מ{old}"
        correct = "movement away from that person would be introduced"
        partials = [
            "movement toward that person would become stronger",
            "possession by that person would become the main meaning",
        ]
        clear = "the receiver clue would become a source clue"
    elif marker and destination:
        prompt_variant = "breaks"
        old = marker["token"]
        replacement = "מן"
        correct = "the direction would change from toward to away from"
        partials = [
            "the same place would remain important, but it would no longer work as the destination",
            "the movement would still be present, but its direction would reverse",
        ]
        clear = "the destination clue would break because the new word marks source instead"
    else:
        prompt_variant = "change"
        verb = get_verb(analyzed)
        old = verb["token"]
        replacement = "וישב"
        correct = "the action would change while the subject could stay the same"
        partials = [
            "the same subject would remain, but movement would no longer be the best reading",
            "the action would stay active, but the direction clues would become weaker",
        ]
        clear = "the action clue would break because the replacement gives a different action"

    choices = build_choices(correct, partials, clear, f"{pasuk}|substitution")
    prompts = {
        "change": "What changes?",
        "impossible": "What no longer works?",
        "new_meaning": "What new meaning appears?",
        "breaks": "What changes?",
    }
    return make_question(
        step,
        "substitution",
        "CM",
        "CM1",
        "substitution",
        old,
        prompts[prompt_variant],
        choices,
        correct,
        "Changing one grammar clue changes how the phrase or sentence functions.",
        5,
    )


def build_reasoning_question(step, pasuk, analyzed):
    verb = get_verb(analyzed)
    subject = get_subject(analyzed)
    source = get_source(analyzed)
    recipient = get_recipient(analyzed)
    direct_object = get_direct_object(analyzed)
    marker, destination = get_destination(analyzed)

    if source and marker and destination:
        correct = f"{verb['token']} gives the action, {subject['token']} gives the subject, {source['token']} gives the source, and {marker['token']} {destination['token']} gives the destination"
        partials = [
            f"{verb['token']} gives the action and {subject['token']} gives the subject, but the direction is only implied",
            f"{source['token']} gives the destination and {marker['token']} {destination['token']} gives the starting point",
        ]
        clear = f"{verb['token']} means gave, and {destination['token']} is the object being given"
        prompt = "Choose the best answer."
    elif recipient and direct_object:
        correct = f"{verb['token']} gives the action, {subject['token']} gives the giver, {direct_object['token']} gives the object, and {recipient['token']} gives the receiver"
        partials = [
            f"{verb['token']} gives the action and {subject['token']} gives the giver, but the receiver is not marked",
            f"{recipient['token']} gives the object, and {direct_object['token']} gives the receiver",
        ]
        clear = f"{verb['token']} means went, and {recipient['token']} gives the destination city"
        prompt = "Who gets the action?"
    else:
        correct = f"{verb['token']} gives the action, and {subject['token']} gives the subject"
        partials = [
            f"{subject['token']} gives the action, and {verb['token']} gives the subject",
            f"{verb['token']} gives the action, but the subject is not stated",
        ]
        clear = f"{subject['token']} is a place and {verb['token']} is a noun"
        prompt = "Choose the best answer."

    choices = build_choices(correct, partials, clear, f"{pasuk}|reasoning")
    return make_question(
        step,
        "reasoning",
        "CM",
        "CM1",
        "reasoning",
        pasuk,
        prompt,
        choices,
        correct,
        "The strongest answer accounts for the action, roles, and grammar clues together.",
        5,
    )


def generate_pasuk_flow(pasuk: str, asked_question_types=None):
    word_bank, by_group = load_word_bank()
    analyzed = analyze_pasuk(pasuk, word_bank)
    used_types = set(asked_question_types or [])

    builders = [
        ("word_meaning", lambda step: build_translation_question(step, pasuk, analyzed, by_group)),
        ("prefix_suffix", lambda step: build_pr_question(step, pasuk, analyzed)),
        ("subject_identification", lambda step: build_subject_question(step, pasuk, analyzed, by_group)),
        ("phrase_meaning", lambda step: build_phrase_question(step, pasuk, analyzed)),
    ]
    active_builders = [item for item in builders if item[0] not in used_types]
    if len(active_builders) < 3:
        active_builders = builders
    questions = [builder(step) for step, (_kind, builder) in enumerate(active_builders, 1)]
    flow = {
        "mode": "pasuk_flow",
        "pasuk": pasuk,
        "source": "generated",
        "questions": questions,
    }
    validate_flow(flow)
    return flow


def summarize_pasuk(analyzed):
    verb = get_verb(analyzed)
    subject = get_subject(analyzed)
    source = get_source(analyzed)
    recipient = get_recipient(analyzed)
    direct_object = get_direct_object(analyzed)
    marker, destination = get_destination(analyzed)
    return {
        "verb": verb,
        "subject": subject,
        "source": source,
        "recipient": recipient,
        "direct_object": direct_object,
        "marker": marker,
        "destination": destination,
    }


def build_multi_sequence_question(step, pesukim, summaries):
    first = summaries[0]
    second = summaries[1]
    correct = f"first {first['verb']['token']} happens, then {second['verb']['token']} happens"
    partials = [
        f"first {second['verb']['token']} happens, then {first['verb']['token']} happens",
        f"both actions happen at the same time because both begin with ו",
    ]
    clear = "there is no action in either pasuk"
    choices = build_choices(correct, partials, clear, "multi|sequence")
    return make_question(
        step,
        "multi_pasuk_flow",
        "SS",
        "SS4",
        "multi_pasuk_sequence",
        " / ".join(pesukim),
        "What happens first?",
        choices,
        correct,
        "The order of the pesukim controls the sequence of actions.",
        4,
    )


def build_multi_dependency_question(step, pesukim, summaries):
    movement = next((item for item in summaries if item["source"] or item["destination"]), summaries[0])
    transfer = next((item for item in summaries if item["recipient"]), summaries[-1])

    correct = f"the movement phrase sets location or direction before the later action is understood"
    partials = [
        "the later action changes the earlier subject into an object",
        "the receiver phrase explains where the earlier movement began",
    ]
    clear = "the two pesukim are unrelated because they share no grammar"
    choices = build_choices(correct, partials, clear, "multi|dependency")
    return make_question(
        step,
        "multi_pasuk_flow",
        "CM",
        "CM1",
        "multi_pasuk_dependency",
        " / ".join(pesukim),
        "How are they connected?",
        choices,
        correct,
        "A multi-pasuk flow asks how one action prepares the next.",
        5,
    )


def build_multi_substitution_question(step, pesukim, summaries):
    target = summaries[0]["source"] or summaries[-1]["recipient"] or summaries[0]["verb"]
    old = target["token"]
    if old.startswith("מ"):
        replacement = f"ב{old[1:]}"
        correct = "the first pasuk would shift from leaving a place to being in a place"
    elif old.startswith("ל"):
        replacement = f"מ{old[1:]}"
        correct = "the phrase would shift from receiver/direction to movement away"
    else:
        replacement = "וישב"
        correct = "the action would shift and the later flow would no longer depend on the same movement"

    partials = [
        "only the spelling would change, but the flow would stay identical",
        "the subject would become the receiver in every pasuk",
    ]
    clear = "all words would become nouns"
    choices = build_choices(correct, partials, clear, "multi|substitution")
    return make_question(
        step,
        "multi_pasuk_flow",
        "CM",
        "CM1",
        "multi_pasuk_substitution",
        old,
        "What changes?",
        choices,
        correct,
        "A substitution can change how one pasuk connects to the next.",
        5,
    )


def generate_multi_pasuk_flow(pesukim):
    if len(pesukim) < 2 or len(pesukim) > 3:
        raise ValueError("Multi-pasuk flow requires 2-3 pesukim.")

    word_bank, _by_group = load_word_bank()
    analyzed_flows = [analyze_pasuk(pasuk, word_bank) for pasuk in pesukim]
    questions = [
        build_translation_question(1, pesukim[0], analyzed_flows[0], _by_group),
        build_phrase_question(2, pesukim[0], analyzed_flows[0]),
        build_subject_question(3, pesukim[0], analyzed_flows[0], _by_group),
    ]
    flow = {
        "mode": "multi_pasuk_flow",
        "pasuk": " / ".join(pesukim),
        "source": "generated multi-pasuk",
        "questions": questions,
    }
    validate_flow(flow, allow_short=True)
    return flow


def validate_flow(flow, allow_short=False):
    questions = flow["questions"]
    texts = [item["question"] for item in questions]
    if len(texts) != len(set(texts)):
        raise ValueError("Duplicate questions found in pasuk flow.")
    if len(questions) < 3:
        raise ValueError("Pasuk flow must include at least 3 atomic questions.")
    difficulties = [item["difficulty"] for item in questions]
    if difficulties != sorted(difficulties):
        raise ValueError("Pasuk flow difficulty must build step-by-step.")
    for item in questions:
        if len(item["question"].split()) > 12:
            raise ValueError(f"Question is too long: {item['question']}")
        if len(item["choices"]) != 4:
            raise ValueError(f"Question does not have 4 choices: {item['question']}")
        if len(set(item["choices"])) != 4:
            raise ValueError(f"Question has duplicate choices: {item['question']}")
        if item["correct_answer"] not in item["choices"]:
            raise ValueError(f"Correct answer missing from choices: {item['question']}")


def write_examples(pesukim=None):
    pesukim = pesukim or EXAMPLE_PESUKIM
    flows = [generate_pasuk_flow(pasuk) for pasuk in pesukim]
    flows.append(generate_multi_pasuk_flow(EXAMPLE_MULTI_PESUKIM))
    data = {"flows": flows}
    OUTPUT_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT_PATH} with {len(flows)} flows.")
    for flow in flows:
        print(f"- {flow['pasuk']}: {len(flow['questions'])} questions")


if __name__ == "__main__":
    write_examples()
