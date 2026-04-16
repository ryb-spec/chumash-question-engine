import json
import random
import hashlib
from pathlib import Path


WORD_BANK_PATH = Path("data/word_bank.json")
LEGACY_WORD_BANK_PATH = Path("word_bank.json")
OUTPUT_PATH = Path("pasuk_flow_questions.json")
LETTER_MEANING_QUESTIONS_PATH = Path("data/skills/letter_meaning/questions_walder.json")
WORD_STRUCTURE_QUESTIONS_PATH = Path("data/skills/word_structure/questions.json")
NORMALIZED_ALIAS_KEY = "__normalized_alias__"

EXAMPLE_PESUKIM = [
    "וילך האיש מביתו אל העיר",
    "ויתן האב לחם לבנו",
]

EXAMPLE_MULTI_PESUKIM = [
    "וילך האיש מביתו אל העיר",
    "ויתן האב לחם לבנו",
    "וישב האיש בביתו",
]

_ALL_PESUKIM = list(dict.fromkeys(EXAMPLE_PESUKIM + EXAMPLE_MULTI_PESUKIM + [
    "בְּרֵאשִׁית בָּרָא אֱלֹקִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ",
    "וְהָאָרֶץ הָיְתָה תֹהוּ וָבֹהוּ וְחֹשֶׁךְ עַל פְּנֵי תְהוֹם",
    "וַיֹּאמֶר אֱלֹקִים יְהִי אוֹר וַיְהִי אוֹר",
    "וַיַּרְא אֱלֹקִים אֶת הָאוֹר כִּי טוֹב",
    "וַיִּקְרָא אֱלֹקִים לָאוֹר יוֹם וְלַחֹשֶׁךְ קָרָא לָיְלָה",
    "וַיֹּאמֶר ה׳ אֶל אַבְרָם לֶךְ לְךָ מֵאַרְצְךָ",
    "וְאֶעֶשְׂךָ לְגוֹי גָּדוֹל וַאֲבָרֶכְךָ",
    "וַיֵּלֶךְ אַבְרָם כַּאֲשֶׁר דִּבֶּר אֵלָיו ה׳",
    "וַיֹּאמֶר אַבְרָם אֶל לוֹט אַל נָא תְהִי מְרִיבָה בֵּינִי וּבֵינֶךָ",
    "וַיֹּאמֶר יַעֲקֹב אֶל בָּנָיו לָמָּה תִּתְרָאוּ",
    "וַיֹּאמֶר יוֹסֵף אֶל אֶחָיו אֲנִי יוֹסֵף",
    "וַיֹּאמֶר פַּרְעֹה אֶל יוֹסֵף רְאֵה נָתַתִּי אֹתְךָ",
    "וַיֹּאמֶר ה׳ אֶל מֹשֶׁה לֶךְ אֶל פַּרְעֹה",
    "וַיֹּאמֶר מֹשֶׁה אֶל ה׳ מִי אָנֹכִי כִּי אֵלֵךְ",
    "וַיֹּאמֶר אֱלֹקִים אֶהְיֶה אֲשֶׁר אֶהְיֶה",
    "אָנֹכִי ה׳ אֱלֹקֶיךָ אֲשֶׁר הוֹצֵאתִיךָ מֵאֶרֶץ מִצְרַיִם",
    "לֹא תִרְצָח לֹא תִנְאָף לֹא תִגְנֹב",
    "כַּבֵּד אֶת אָבִיךָ וְאֶת אִמֶּךָ",
    "וְאָהַבְתָּ אֵת ה׳ אֱלֹקֶיךָ בְּכָל לְבָבְךָ",
    "וְהָיוּ הַדְּבָרִים הָאֵלֶּה עַל לְבָבֶךָ",
    "וְשִׁנַּנְתָּם לְבָנֶיךָ וְדִבַּרְתָּ בָּם",
    "ה׳ רֹעִי לֹא אֶחְסָר",
    "בִּנְאוֹת דֶּשֶׁא יַרְבִּיצֵנִי עַל מֵי מְנֻחוֹת יְנַהֲלֵנִי",
    "גַּם כִּי אֵלֵךְ בְּגֵיא צַלְמָוֶת לֹא אִירָא רָע",
    "שִׁירוּ לַה׳ שִׁיר חָדָשׁ שִׁירוּ לַה׳ כָּל הָאָרֶץ",
    "הוֹדוּ לַה׳ כִּי טוֹב כִּי לְעוֹלָם חַסְדּוֹ",
    "אֶשָּׂא עֵינַי אֶל הֶהָרִים מֵאַיִן יָבֹא עֶזְרִי",
    "עֶזְרִי מֵעִם ה׳ עֹשֵׂה שָׁמַיִם וָאָרֶץ",
    "אֲנִי לְדוֹדִי וְדוֹדִי לִי",
    "קוֹל דּוֹדִי דּוֹפֵק פִּתְחִי לִי אֲחֹתִי",
]))

CHUMASH_PESUKIM = _ALL_PESUKIM[:24]
OTHER_PESUKIM = _ALL_PESUKIM[24:]
PESUKIM = CHUMASH_PESUKIM

WORD_BANK = []

TRANSLATION_LITERAL = "literal"
TRANSLATION_NATURAL = "natural"

PREFIX_MEANINGS = {
    "\u05d5": "and",
    "\u05d1": "in / with",
    "\u05dc": "to / for",
    "\u05db": "like / as",
    "\u05de": "from",
    "\u05d4": "the",
    "\u05e9": "that / which",
}

KNOWN_PREFIXES = PREFIX_MEANINGS
CONTROLLED_TENSE_CHOICES = [
    "vav_consecutive_past",
    "future_jussive",
    "future",
    "past",
    "present",
    "command",
    "not a verb",
]

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
    "\u05d1": ["in / with", "to / for", "from", "the"],
    "\u05dc": ["to / for", "in / with", "from", "like / as"],
    "\u05de": ["from", "to / for", "in / with", "the"],
    "\u05d5": ["and", "the", "to / for", "from"],
    "\u05db": ["like / as", "in / with", "from", "the"],
    "\u05d4": ["the", "and", "to / for", "from"],
    "\u05e9": ["that / which", "and", "the", "from"],
}

SUFFIX_MEANINGS = {
    "\u05d9": "my",
    "\u05da\u05b8": "your (m)",
    "\u05da\u05b0": "your (f)",
    "\u05da": "your",
    "\u05d5": "his",
    "\u05d4": "her",
    "\u05e0\u05d5": "our",
    "\u05db\u05b6\u05dd": "your (m plural)",
    "\u05db\u05b6\u05df": "your (f plural)",
    "\u05db\u05dd": "your (m plural)",
    "\u05db\u05df": "your (f plural)",
    "\u05dd": "their",
    "\u05df": "their",
    "\u05d9\u05d5": "his",
}


def normalize_hebrew_key(text):
    if not isinstance(text, str):
        return text
    return "".join(
        char
        for char in text
        if not "\u0591" <= char <= "\u05c7"
    )


def old_word_type(part_of_speech):
    return {
        "proper_noun": "noun",
        "preposition": "prep",
    }.get(part_of_speech, part_of_speech or "unknown")


def first_morpheme_value(items, key, default=""):
    if not items:
        return default
    first = items[0] or {}
    return first.get(key, default)


def first_present(*values):
    for value in values:
        if value is not None:
            return value
    return None


def add_legacy_word_bank_aliases(entry):
    entry.setdefault("Word", entry.get("word"))
    entry.setdefault("Shoresh", entry.get("shoresh"))
    entry.setdefault("Prefix", entry.get("prefix", ""))
    entry.setdefault("Prefix Meaning", entry.get("prefix_meaning", ""))
    entry.setdefault("Suffix", entry.get("suffix", ""))
    entry.setdefault("Suffix Meaning", entry.get("suffix_meaning", ""))
    entry.setdefault("Translation", entry.get("translation"))
    entry.setdefault(
        "Context Translation",
        entry.get("context_translation")
        or entry.get("translation_context")
        or entry.get("translation"),
    )
    return entry


def flat_analysis_copy(entry):
    analysis = dict(entry)
    analysis.pop("analyses", None)
    return analysis


def adapt_word_bank_analysis(surface, analysis, analysis_index=0):
    prefixes = analysis.get("prefixes") or []
    suffixes = analysis.get("suffixes") or []
    word = analysis.get("surface") or surface
    normalized = analysis.get("normalized") or normalize_hebrew_key(word)
    translation_literal = first_present(
        analysis.get("translation_literal"),
        analysis.get("translation"),
        analysis.get("Translation"),
    )
    translation_context = first_present(
        analysis.get("translation_context"),
        analysis.get("context_translation"),
        analysis.get("Context Translation"),
    )
    entry = {
        "word": word,
        "Word": word,
        "surface": word,
        "menukad": word,
        "normalized": normalized,
        "lemma": analysis.get("lemma"),
        "shoresh": analysis.get("shoresh") or analysis.get("Shoresh"),
        "Shoresh": analysis.get("shoresh") or analysis.get("Shoresh"),
        "type": old_word_type(analysis.get("part_of_speech")),
        "part_of_speech": analysis.get("part_of_speech"),
        "group": analysis.get("group", "unknown"),
        "translation": translation_context or translation_literal or word,
        "translation_literal": translation_literal,
        "translation_context": translation_context,
        "context_translation": translation_context,
        "base_translation": translation_literal,
        "binyan": analysis.get("binyan"),
        "tense": analysis.get("tense"),
        "person": analysis.get("person"),
        "number": analysis.get("number"),
        "gender": analysis.get("gender"),
        "semantic_group": analysis.get("semantic_group", "unknown"),
        "role_hint": analysis.get("role_hint", "unknown"),
        "entity_type": analysis.get("entity_type", "unknown"),
        "prefixes": prefixes,
        "suffixes": suffixes,
        "prefix": first_morpheme_value(prefixes, "form"),
        "prefix_meaning": first_morpheme_value(prefixes, "translation"),
        "suffix": first_morpheme_value(suffixes, "form"),
        "suffix_meaning": first_morpheme_value(suffixes, "translation"),
        "confidence": analysis.get("confidence"),
        "source_refs": analysis.get("source_refs", []),
        "analysis_index": analysis_index,
    }
    entry["analyses"] = [flat_analysis_copy(entry)]
    return add_legacy_word_bank_aliases(entry)


def load_word_bank_entries(path):
    if not path.exists():
        return []

    data = json.loads(path.read_text(encoding="utf-8"))
    words = data.get("words", [])
    if isinstance(words, list):
        entries = []
        for entry in words:
            adapted = dict(entry)
            adapted.setdefault("word", adapted.get("Word") or adapted.get("surface"))
            adapted.setdefault("Word", adapted.get("word"))
            adapted.setdefault("surface", adapted.get("word"))
            adapted.setdefault("menukad", adapted.get("surface") or adapted.get("word"))
            adapted.setdefault("normalized", normalize_hebrew_key(adapted.get("word", "")))
            adapted.setdefault("shoresh", adapted.get("Shoresh"))
            adapted.setdefault("Shoresh", adapted.get("shoresh"))
            adapted.setdefault("type", old_word_type(adapted.get("part_of_speech")))
            adapted.setdefault("prefix", adapted.get("Prefix", ""))
            adapted.setdefault("prefix_meaning", adapted.get("Prefix Meaning", ""))
            adapted.setdefault("suffix", adapted.get("Suffix", ""))
            adapted.setdefault("suffix_meaning", adapted.get("Suffix Meaning", ""))
            adapted.setdefault("translation_literal", adapted.get("translation") or adapted.get("Translation"))
            adapted.setdefault(
                "translation_context",
                adapted.get("context_translation") or adapted.get("Context Translation"),
            )
            adapted.setdefault(
                "translation",
                adapted.get("translation_context") or adapted.get("translation_literal") or adapted.get("word"),
            )
            adapted.setdefault("context_translation", adapted.get("translation_context"))
            adapted.setdefault("base_translation", adapted.get("translation_literal"))
            adapted.setdefault("semantic_group", "unknown")
            adapted.setdefault("role_hint", "unknown")
            adapted.setdefault("entity_type", "unknown")
            adapted.setdefault("prefixes", [])
            adapted.setdefault("suffixes", [])
            adapted = add_legacy_word_bank_aliases(adapted)
            adapted.setdefault("analyses", [dict(adapted)])
            entries.append(adapted)
        return entries

    entries = []
    for surface, analyses in words.items():
        adapted_analyses = [
            adapt_word_bank_analysis(surface, analysis, index)
            for index, analysis in enumerate(analyses)
        ]
        if not adapted_analyses:
            continue
        default_entry = dict(adapted_analyses[0])
        default_entry["analyses"] = [
            flat_analysis_copy(analysis)
            for analysis in adapted_analyses
        ]
        entries.append(add_legacy_word_bank_aliases(default_entry))
    return entries


def merge_word_bank_entry(by_word, entry):
    word = entry.get("word")
    if not word:
        return

    if word in by_word:
        existing = by_word[word]
        existing.setdefault("analyses", [existing])
        existing["analyses"].extend(entry.get("analyses", [entry]))
        existing.update(entry)
    else:
        by_word[word] = entry

    normalized = entry.get("normalized")
    if normalized and normalized != word:
        merge_normalized_alias(by_word, normalized, by_word[word])


def merge_normalized_alias(by_word, normalized, entry):
    alias = by_word.get(normalized)
    if alias is None:
        alias = {
            NORMALIZED_ALIAS_KEY: True,
            "word": normalized,
            "Word": normalized,
            "surface": normalized,
            "menukad": normalized,
            "normalized": normalized,
            "type": "ambiguous",
            "part_of_speech": "ambiguous",
            "group": "unknown",
            "translation": normalized,
            "translation_context": normalized,
            "context_translation": normalized,
            "prefixes": [],
            "suffixes": [],
            "surface_forms": [],
            "entries": [],
            "analyses": [],
        }
        by_word[normalized] = alias
    elif not alias.get(NORMALIZED_ALIAS_KEY):
        alias.setdefault("normalized_aliases", [])
        alias["normalized_aliases"].append(entry)
        return

    surface = entry.get("word")
    if surface not in alias["surface_forms"]:
        alias["surface_forms"].append(surface)
        alias["entries"].append(entry)
    alias["analyses"].extend(entry.get("analyses", [entry]))
    if len(alias["surface_forms"]) == 1:
        for key in (
            "translation",
            "translation_literal",
            "translation_context",
            "context_translation",
            "base_translation",
            "type",
            "part_of_speech",
            "lemma",
            "shoresh",
            "binyan",
            "tense",
            "person",
            "number",
            "gender",
            "semantic_group",
            "role_hint",
            "entity_type",
            "prefixes",
            "suffixes",
            "prefix",
            "prefix_meaning",
            "suffix",
            "suffix_meaning",
        ):
            if key in entry:
                alias[key] = entry[key]


def load_word_bank():
    entries = []
    entries.extend(load_word_bank_entries(LEGACY_WORD_BANK_PATH))
    entries.extend(load_word_bank_entries(WORD_BANK_PATH))

    by_word = {}
    by_group = {}
    for entry in entries:
        merge_word_bank_entry(by_word, entry)

    seen_entries = set()
    for entry in by_word.values():
        if entry.get(NORMALIZED_ALIAS_KEY):
            continue
        marker = id(entry)
        if marker in seen_entries:
            continue
        seen_entries.add(marker)
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


def tokenize_pasuk(pasuk):
    return pasuk.replace("\u05be", " ").split()


def analyze_word(word):
    return {
        "word": word,
        "prefix": extract_prefix(word),
        "suffix": extract_suffix(word),
        "is_verb": is_verb(word),
    }


def sync_word_bank_from_progress(progress):
    if not progress:
        return

    existing_by_word = {item["word"]: item for item in WORD_BANK}
    for stored_word in progress.get("word_bank", []):
        word = stored_word.get("word")
        if not word:
            continue

        if word in existing_by_word:
            existing = existing_by_word[word]
            existing.setdefault("skill_scores", {})
            existing["skill_scores"].update(stored_word.get("skill_scores", {}))
        else:
            stored = dict(stored_word)
            stored.setdefault("skill_scores", {})
            WORD_BANK.append(stored)
            existing_by_word[word] = stored


def store_word_bank_in_progress(progress):
    if progress is not None:
        progress["word_bank"] = WORD_BANK


def add_words_from_pasuk(pasuk, progress=None):
    sync_word_bank_from_progress(progress)

    if is_structured_pasuk(pasuk):
        pasuk_text = structured_pasuk_text(pasuk)
        analyzed_words = [
            {
                "word": item.get("word") or item.get("token"),
                "prefix": extract_prefix(item.get("word") or item.get("token")),
                "suffix": item.get("suffix") or extract_suffix(item.get("word") or item.get("token")),
                "is_verb": item.get("is_verb", is_verb(item.get("word") or item.get("token"))),
            }
            for item in pasuk
            if item.get("word") or item.get("token")
        ]
    else:
        pasuk_text = pasuk
        analyzed_words = [analyze_word(word) for word in tokenize_pasuk(pasuk)]

    existing_by_word = {item["word"]: item for item in WORD_BANK}
    for analyzed in analyzed_words:
        word = analyzed["word"]
        if word in existing_by_word:
            existing = existing_by_word[word]
            existing["prefix"] = analyzed.get("prefix") or ""
            existing["prefix_meaning"] = PREFIX_MEANINGS.get(existing["prefix"], "")
            existing["suffix"] = existing.get("suffix") or analyzed.get("suffix")
            existing["is_verb"] = bool(existing.get("is_verb") or analyzed.get("is_verb"))
            existing.setdefault("skill_scores", {})
            existing.setdefault("source_pesukim", [])
            if pasuk_text not in existing["source_pesukim"]:
                existing["source_pesukim"].append(pasuk_text)
            existing.setdefault("source_pasuk", existing["source_pesukim"][0])
            continue

        stored = dict(analyzed)
        stored["source_pasuk"] = pasuk_text
        stored["source_pesukim"] = [pasuk_text]
        stored["skill_scores"] = {}
        WORD_BANK.append(stored)
        existing_by_word[word] = stored

    store_word_bank_in_progress(progress)
    return WORD_BANK


def extract_prefix(word):
    if not word:
        return None

    plain_word = "".join(
        char
        for char in word
        if not "\u0591" <= char <= "\u05c7"
    )
    prefixes = ["\u05d5", "\u05d1", "\u05dc", "\u05db", "\u05de", "\u05d4"]

    for prefix in prefixes:
        if not plain_word.startswith(prefix) or len(plain_word) <= 3:
            continue

        remainder = plain_word[1:]
        if len(remainder) < 2:
            continue
        if remainder[0] == prefix:
            continue

        return prefix

    return None


def prefix_has_known_base(word, prefix, word_bank):
    if not prefix or not word_bank:
        return False

    base = word[len(prefix):] if prefix else word
    return base in word_bank


def apply_prefix_metadata(word, entry, word_bank=None):
    prefix = extract_prefix(word)
    if prefix is None:
        entry["prefix"] = ""
        entry["prefix_meaning"] = ""
        return entry

    entry["prefix"] = prefix
    entry["prefix_meaning"] = PREFIX_MEANINGS[prefix]
    return entry


def is_prefix_candidate(entry, token, word_bank=None):
    prefix = extract_prefix(token)
    if not prefix:
        return False
    if entry.get("prefix") and entry.get("prefix") != prefix:
        return False
    return True


def detect_prefix(token, word_bank):
    if len(token) < 2:
        return None

    prefix = extract_prefix(token)
    if prefix is None:
        return None

    base_word = token[len(prefix):]
    if base_word not in word_bank:
        return None

    entry = dict(word_bank[base_word])
    entry["word"] = token
    entry["prefix"] = prefix
    entry["base_word"] = base_word
    entry["prefix_meaning"] = PREFIX_MEANINGS[prefix]
    entry["translation"] = f"{PREFIX_MEANINGS[prefix]} {word_bank[base_word]['translation']}"
    apply_prefix_metadata(entry["word"], entry, word_bank)
    apply_suffix_metadata(entry["word"], entry, word_bank)
    return {"token": token, "entry": entry, "base": base_word}


def extract_suffix(word):
    if word.endswith("\u05db\u05b6\u05dd"):
        return "\u05db\u05b6\u05dd"
    if word.endswith("\u05db\u05b6\u05df"):
        return "\u05db\u05b6\u05df"
    if word.endswith("\u05db\u05dd"):
        return "\u05db\u05dd"
    if word.endswith("\u05db\u05df"):
        return "\u05db\u05df"
    if word.endswith("\u05e0\u05d5"):
        return "\u05e0\u05d5"
    if word.endswith("\u05d9\u05d5"):
        return "\u05d9\u05d5"
    if word.endswith("\u05da\u05b8"):
        return "\u05da\u05b8"
    if word.endswith("\u05da\u05b0"):
        return "\u05da\u05b0"
    if word.endswith("\u05da"):
        return "\u05da"
    if word.endswith("\u05dd"):
        return "\u05dd"
    if word.endswith("\u05df"):
        return "\u05df"
    if word.endswith("\u05d4"):
        return "\u05d4"
    if word.endswith("\u05d5"):
        return "\u05d5"
    if word.endswith("\u05d9"):
        return "\u05d9"
    return None


def suffix_has_known_base(word, suffix, word_bank):
    if not word_bank:
        return False

    base = word[:-len(suffix)] if suffix else word
    if base in word_bank:
        return True

    prefix = extract_prefix(base)
    if prefix and base[len(prefix):] in word_bank:
        return True

    return False


def apply_suffix_metadata(word, entry, word_bank=None):
    suffix = extract_suffix(word)
    if suffix is None:
        return entry

    already_marked = bool(entry.get("suffix")) or entry.get("type") == "suffix_form"
    if already_marked and entry.get("suffix") in SUFFIX_MEANINGS:
        suffix = entry["suffix"]

    if not already_marked and not suffix_has_known_base(word, suffix, word_bank):
        return entry

    entry["suffix"] = suffix
    entry["suffix_meaning"] = SUFFIX_MEANINGS[suffix]
    return entry


def with_suffix_metadata(item, word_bank=None):
    if item is None:
        return None

    entry = dict(item["entry"])
    apply_suffix_metadata(item["token"], entry, word_bank)
    updated = dict(item)
    updated["entry"] = entry
    return updated


def is_suffix_candidate(entry, token, word_bank=None):
    suffix = entry.get("suffix") or extract_suffix(token)
    if not suffix:
        return False
    return bool(entry.get("suffix")) or entry.get("type") == "suffix_form" or suffix_has_known_base(
        token,
        suffix,
        word_bank,
    )


def normalize_token(token, word_bank):
    lookup_token = token
    if lookup_token not in word_bank:
        normalized_token = normalize_hebrew_key(token)
        if normalized_token in word_bank:
            lookup_token = normalized_token

    if lookup_token in word_bank:
        entry = resolve_word_bank_lookup(token, word_bank[lookup_token])
        if entry.get("prefix"):
            entry.setdefault("base_word", token)
        else:
            prefix = extract_prefix(token)
            if prefix and prefix_has_known_base(token, prefix, word_bank):
                possible_base = token[len(prefix):]
                entry.setdefault(
                    "base_word",
                    possible_base if possible_base in word_bank else token,
                )
                apply_prefix_metadata(token, entry, word_bank)
            else:
                entry["prefix"] = ""
                entry["prefix_meaning"] = ""
                entry.setdefault("base_word", token)
        apply_suffix_metadata(token, entry, word_bank)
        return {"token": token, "entry": entry, "base": token}

    detected = detect_prefix(token, word_bank)
    if detected is not None:
        return detected

    return None


def resolve_word_bank_lookup(token, entry):
    if not entry.get(NORMALIZED_ALIAS_KEY):
        return dict(entry)
    entries = entry.get("entries") or []
    if len(entries) == 1:
        resolved = dict(entries[0])
        resolved["normalized_alias_entry"] = dict(entry)
        return resolved
    resolved = dict(entry)
    resolved["word"] = token
    resolved["Word"] = token
    resolved["surface"] = token
    resolved["menukad"] = token
    return resolved


def basic_analyzed_item(word, word_bank=None):
    basic = analyze_word(word)
    entry = {
        "word": word,
        "translation": word,
        "type": "verb" if basic["is_verb"] else "unknown",
        "group": "unknown",
        "shoresh": word,
        "prefix": basic["prefix"] or "",
        "prefix_meaning": PREFIX_MEANINGS.get(basic["prefix"], ""),
        "suffix": basic["suffix"] or "",
        "suffix_meaning": SUFFIX_MEANINGS.get(basic["suffix"], ""),
        "base_word": word,
    }
    apply_prefix_metadata(word, entry, word_bank)
    apply_suffix_metadata(word, entry, word_bank)
    return {"token": word, "entry": entry, "base": word}


def structured_word_to_item(word_data, word_bank=None):
    word = word_data.get("word") or word_data.get("token")
    if not word:
        return None

    if word_bank:
        item = normalize_token(word, word_bank)
        if item is not None:
            return item

    item = basic_analyzed_item(word, word_bank)
    entry = item["entry"]
    detected_prefix = extract_prefix(word)
    if word_data.get("prefix") and word_data["prefix"] == detected_prefix:
        entry["prefix"] = detected_prefix
        entry["prefix_meaning"] = PREFIX_MEANINGS.get(detected_prefix, "")
    if word_data.get("suffix"):
        entry["suffix"] = word_data["suffix"]
        entry["suffix_meaning"] = SUFFIX_MEANINGS.get(word_data["suffix"], "")
    if word_data.get("is_verb"):
        entry["type"] = "verb"
    return item


def is_structured_pasuk(value):
    return isinstance(value, (list, tuple)) and all(
        isinstance(item, dict) and ("word" in item or "token" in item)
        for item in value
    )


def structured_pasuk_text(analyzed_words):
    return " ".join((item.get("word") or item.get("token") or "") for item in analyzed_words)


def normalize_analyzed_pasuk(analyzed_words, word_bank=None):
    items = [
        structured_word_to_item(word_data, word_bank)
        for word_data in analyzed_words
    ]
    return [item for item in items if item is not None]


def structured_word_bank_items(predicate, word_bank=None, pasuk_text=None, progress=None):
    sync_word_bank_from_progress(progress)
    recent_words = set((progress or {}).get("recent_words", [])[-5:])
    items = []

    for stored_word in WORD_BANK:
        if stored_word.get("word") in recent_words:
            continue

        item = structured_word_to_item(stored_word, word_bank)
        if item is None or not predicate(item["entry"], item["token"]):
            continue

        source_pesukim = stored_word.get("source_pesukim", [])
        item["source_pasuk"] = find_pasuk_for_word(
            stored_word["word"],
            fallback=pasuk_text,
            progress=progress,
        )
        item["source_pesukim"] = source_pesukim
        items.append(item)

    return items


def skill_applicable(word_data, skill):
    word = word_data.get("word") or word_data.get("token")
    if not word:
        return False

    prefix = extract_prefix(word)
    suffix = word_data.get("suffix") or extract_suffix(word)
    is_word_verb = bool(word_data.get("is_verb")) or is_verb(word)

    if skill in {"prefix", "identify_prefix_meaning", "identify_prefix_future", "preposition_meaning"}:
        return bool(prefix)
    if skill in {"suffix", "identify_suffix_meaning", "identify_pronoun_suffix", "identify_suffix_past"}:
        return bool(suffix)
    if skill in {"verb_tense", "identify_tense", "identify_verb_marker"}:
        return is_word_verb and confident_verb_tense(word_data, word) is not None
    if skill == "segment_word_parts":
        return bool(prefix or suffix)
    if skill in {"part_of_speech", "shoresh"}:
        return is_word_verb or bool(prefix or suffix)
    return True


def word_skill_score(word, skill):
    for stored_word in WORD_BANK:
        if stored_word.get("word") == word:
            stored_word.setdefault("skill_scores", {})
            return stored_word["skill_scores"].get(skill, 0)
    return 0


def update_word_skill_score(word, skill, is_correct, progress=None):
    sync_word_bank_from_progress(progress)
    amount = 10 if is_correct else -10

    for stored_word in WORD_BANK:
        if stored_word.get("word") != word:
            continue

        stored_word.setdefault("skill_scores", {})
        current_score = stored_word["skill_scores"].get(skill, 0)
        stored_word["skill_scores"][skill] = max(0, min(100, current_score + amount))
        store_word_bank_in_progress(progress)
        return stored_word["skill_scores"][skill]

    return None


def find_pasuk_for_word(word, fallback=None, progress=None):
    sync_word_bank_from_progress(progress)
    recent_pesukim = set((progress or {}).get("recent_pesukim", [])[-5:])

    for stored_word in WORD_BANK:
        if stored_word.get("word") != word:
            continue

        source_pesukim = [
            pasuk
            for pasuk in stored_word.get("source_pesukim", [])
            if pasuk
        ]
        if not source_pesukim and stored_word.get("source_pasuk"):
            source_pesukim = [stored_word["source_pasuk"]]

        fresh_sources = [
            pasuk
            for pasuk in source_pesukim
            if pasuk not in recent_pesukim
        ]
        return random.choice(fresh_sources or source_pesukim or [fallback])

    return fallback


def analyze_pasuk(pasuk, word_bank=None):
    if word_bank is None:
        return [analyze_word(word) for word in tokenize_pasuk(pasuk)]

    analyzed = []
    unknown = []
    for token in tokenize_pasuk(pasuk):
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


def build_choices(correct, partials, clear, key, extra=None):
    choices = unique([correct] + list(partials or []) + [clear] + list(extra or []))
    if len(choices) < 4:
        raise ValueError(f"Need 4 unique choices. Got: {choices}")
    choices = choices[:4]
    stable_rng(key).shuffle(choices)
    return choices


def contains_hebrew(text):
    return any("\u0590" <= char <= "\u05ff" for char in str(text or ""))


def is_placeholder_translation(value, token=None):
    if not value:
        return True
    text = str(value).strip()
    if not text:
        return True
    if text.startswith("[") and text.endswith("]"):
        return True
    if "direct object marker" in text.lower():
        return True
    if token and normalize_hebrew_key(text) == normalize_hebrew_key(token):
        return True
    return contains_hebrew(text)


def usable_translation(entry, token=None):
    for key in ("translation_context", "context_translation", "translation", "translation_literal"):
        value = entry.get(key)
        if not is_placeholder_translation(value, token):
            return value
    return None


def instructional_value(entry, question_type=None):
    if not isinstance(entry, dict):
        return "low"
    token = entry.get("word") or entry.get("surface")
    if question_type in {"word_meaning", "translation", "subject_identification"}:
        if usable_translation(entry, token) is None:
            return "low"
        if entry.get("entity_type") == "grammatical_particle":
            return "low"
        if entry.get("part_of_speech") == "particle" or entry.get("type") == "particle":
            return "low"
    if question_type in {"verb_tense", "shoresh"}:
        if entry.get("type") != "verb" or entry.get("confidence") == "generated_alternate":
            return "low"
        if question_type == "shoresh" and not entry.get("shoresh"):
            return "low"
        if question_type == "verb_tense" and not entry.get("tense"):
            return "low"
    if entry.get("confidence") in {"reviewed_starter", "reviewed"}:
        return "high"
    if entry.get("semantic_group") not in {None, "unknown"}:
        return "medium"
    return "low"


def quiz_eligible(entry, token, question_type):
    return instructional_value(entry, question_type) in {"high", "medium"}


def strip_surface_family_prefixes(value):
    text = normalize_hebrew_key(value or "")
    if len(text) > 3 and text.startswith("\u05d5"):
        text = text[1:]
    if len(text) > 3 and text.startswith(("\u05d4", "\u05dc")):
        text = text[1:]
    return text


def distractor_key(entry):
    if not isinstance(entry, dict):
        return None

    explicit = (
        entry.get("distractor_key")
        or entry.get("display_lemma")
        or entry.get("surface_family")
    )
    if explicit:
        return normalize_hebrew_key(explicit)

    word = entry.get("word") or entry.get("surface") or entry.get("menukad")
    normalized_word = normalize_hebrew_key(word)
    lemma = entry.get("lemma") or entry.get("shoresh") or entry.get("Shoresh")
    key = normalize_hebrew_key(lemma) if lemma else normalized_word

    if key and key == normalized_word:
        key = strip_surface_family_prefixes(key)
    return key or normalized_word


def filtered_translation_values(entries, correct, correct_entry=None, question_type="translation"):
    values = []
    seen_values = {correct}
    seen_keys = set()
    correct_key = distractor_key(correct_entry)
    if correct_key:
        seen_keys.add(correct_key)

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        if not quiz_eligible(entry, entry.get("word"), question_type):
            continue
        value = usable_translation(entry, entry.get("word"))
        if not value or value in seen_values:
            continue
        key = distractor_key(entry)
        if key and key in seen_keys:
            continue
        values.append(value)
        seen_values.add(value)
        if key:
            seen_keys.add(key)
    return values


def word_bank_entries(word_bank, source_derived_only=False):
    seen = set()
    for entry in (word_bank or {}).values():
        if not isinstance(entry, dict) or entry.get(NORMALIZED_ALIAS_KEY):
            continue
        if source_derived_only and not entry.get("source_refs"):
            continue
        marker = id(entry)
        if marker in seen:
            continue
        seen.add(marker)
        yield entry


def valid_shorashim(word_bank):
    return unique(
        entry.get("shoresh")
        for entry in word_bank_entries(word_bank, source_derived_only=True)
        if entry.get("type") == "verb" and entry.get("shoresh")
    )


def translation_distractors(correct, target_entry, by_group, word_bank=None):
    same_semantic_group = [
        entry
        for entry in word_bank_entries(word_bank, source_derived_only=True)
        if entry.get("semantic_group") == target_entry.get("semantic_group")
    ]
    same_entity_type = [
        entry
        for entry in word_bank_entries(word_bank, source_derived_only=True)
        if entry.get("entity_type") == target_entry.get("entity_type")
    ]
    same_group = [
        entry
        for entry in by_group.get(target_entry.get("group"), [])
    ]
    same_type = [
        entry
        for entry in word_bank_entries(word_bank, source_derived_only=True)
        if entry.get("type") == target_entry.get("type")
    ]
    all_translations = [
        entry
        for entry in word_bank_entries(word_bank, source_derived_only=True)
    ]
    return filtered_translation_values(
        same_semantic_group + same_entity_type + same_group + same_type + all_translations,
        correct,
        target_entry,
        question_type="word_meaning",
    )


def quiz_ready(entry, token, question_type):
    if question_type == "translation":
        return quiz_eligible(entry, token, "word_meaning")
    if question_type == "shoresh":
        return quiz_eligible(entry, token, "shoresh")
    if question_type == "verb_tense":
        return quiz_eligible(entry, token, "verb_tense")
    if question_type == "prefix_suffix":
        prefix = extract_prefix(token) or entry.get("prefix")
        suffix = entry.get("suffix")
        return bool(
            (prefix and PREFIX_MEANINGS.get(prefix))
            or (suffix and (entry.get("suffix_meaning") or SUFFIX_MEANINGS.get(suffix)))
        )
    if question_type == "subject_identification":
        return (
            entry.get("role_hint") == "subject_candidate"
            and entry.get("semantic_group") in {"person", "divine"}
            and quiz_eligible(entry, token, "subject_identification")
        )
    return True


def first_ready(analyzed, question_type):
    return find_first(
        analyzed,
        lambda entry, token: quiz_ready(entry, token, question_type),
    )


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


def describe(item, mode=TRANSLATION_LITERAL):
    return item["entry"]["translation"]


def naturalize_subject_action(action_text, subject_text):
    replacements = [
        ("and he ", "and "),
        ("and it ", "and "),
        ("he ", ""),
        ("it ", ""),
    ]
    for prefix, replacement in replacements:
        if action_text.startswith(prefix):
            return f"{replacement}{subject_text} {action_text[len(prefix):]}"
    return f"{subject_text} {action_text}"


def format_translation(items, mode=TRANSLATION_LITERAL):
    if mode == TRANSLATION_LITERAL:
        return " ".join(describe(item) for item in items)

    if len(items) >= 2:
        first, second = items[0], items[1]
        if (
            first["entry"].get("type") == "verb"
            and second["entry"].get("group") == "people"
        ):
            translated = naturalize_subject_action(describe(first), describe(second))
            rest = [describe(item) for item in items[2:]]
            return " ".join([translated] + rest)

    return " ".join(describe(item) for item in items)


def varied_phrase_window(analyzed, target_token=None, recent_phrases=None, key="phrase"):
    recent_phrases = list(recent_phrases or [])
    recent_block = set(recent_phrases[-5:])
    options = []
    max_length = min(4, len(analyzed))

    for length in range(2, max_length + 1):
        for start in range(0, len(analyzed) - length + 1):
            phrase_items = analyzed[start:start + length]
            phrase = " ".join(item["token"] for item in phrase_items)
            if phrase_items[-1]["entry"].get("type") == "prep":
                continue
            if target_token and target_token not in [item["token"] for item in phrase_items]:
                continue
            options.append((phrase, phrase_items))

    unused = [option for option in options if option[0] not in recent_block]
    pool = unused
    attempts = 0
    while not pool and attempts < 10:
        attempts += 1
        pool = [option for option in options if option[0] not in recent_block]

    if not pool:
        pool = options

    if not pool:
        return " ".join(item["token"] for item in analyzed[:2]), analyzed[:2]

    return stable_rng(f"{key}|{len(recent_phrases)}").choice(pool)


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
    choices = list(question.get("choices", []))
    if len(choices) != 4:
        raise ValueError(f"Question must have exactly 4 choices: {question.get('question')}")
    if len(set(choices)) != 4:
        raise ValueError(f"Question choices must be unique: {question.get('question')}")
    if question.get("correct_answer") not in choices:
        raise ValueError(f"Correct answer is missing from choices: {question.get('question')}")
    random.shuffle(choices)
    question["choices"] = choices
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
        "translation_mode": (
            TRANSLATION_NATURAL
            if question_type in {"phrase_meaning", "subject_identification"}
            else TRANSLATION_LITERAL
        ),
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
    return find_first(analyzed, lambda entry, token: is_prefix_candidate(entry, token))


def get_suffixed_word(analyzed, word_bank=None):
    target = find_first(analyzed, lambda entry, token: is_suffix_candidate(entry, token, word_bank))
    return with_suffix_metadata(target)


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
    return confident_verb_tense(entry, token)


def choice_pool(values, correct, fallback):
    choices = unique([correct] + [value for value in values if value != correct] + fallback)
    return choices[:4]


def prefix_meaning_choices(prefix):
    options = PREFIX_MEANING_CHOICES.get(prefix)
    if options:
        return options

    correct = PREFIX_MEANINGS.get(prefix, "and")
    return unique([correct, "and", "the", "in / with", "to / for", "from"])[:4]


def has_prefix(word):
    return extract_prefix(word) is not None


def has_suffix(word):
    return extract_suffix(word) is not None


def strip_hebrew_marks(word):
    return "".join(
        char
        for char in word
        if not "\u0591" <= char <= "\u05c7"
    )


def detect_verb_tense(word):
    w = strip_hebrew_marks(word)

    if w.endswith("\u05ea\u05d9"):
        return "past"
    if w.endswith("\u05ea"):
        return "past"
    if w.endswith("\u05ea\u05dd") or w.endswith("\u05ea\u05df"):
        return "past"
    if w.endswith("\u05e0\u05d5"):
        return "past"
    if w.endswith("\u05d5") and len(w) > 3:
        return "past"

    if w.startswith(("\u05d9", "\u05ea", "\u05d0", "\u05e0")):
        if len(w) >= 3:
            return "future"

    if len(w) <= 4 and not w.startswith(("\u05d9", "\u05ea", "\u05d0", "\u05e0", "\u05d5")):
        return "command"

    if w.startswith("\u05d5") and len(w) > 3:
        second = w[1]
        if second in ["\u05d9", "\u05ea"]:
            return "past"

    return None


def is_verb(word):
    plain = strip_hebrew_marks(word)
    if plain.startswith(("\u05d9", "\u05ea", "\u05d0", "\u05e0")):
        return True
    if plain.endswith(("\u05ea\u05d9", "\u05ea", "\u05e0\u05d5", "\u05d5")):
        return True
    if plain.startswith("\u05d5") and len(plain) > 3 and plain[1] in ["\u05d9", "\u05ea"]:
        return True
    if len(plain) >= 3:
        return True
    return False


def confident_verb_tense(entry, token):
    if not is_verb(token):
        return None

    tense = detect_verb_tense(token)
    if tense is None:
        return None

    entry = entry or {}
    entry_type = entry.get("type")
    if entry_type and entry_type not in {"verb", "unknown"}:
        return None

    plain = strip_hebrew_marks(token)
    is_basic_guess = (
        entry_type == "verb"
        and entry.get("group") == "unknown"
        and entry.get("translation") == token
    )
    if tense == "command" and entry.get("tense") != "command":
        return None
    if tense == "past" and is_basic_guess:
        if plain.endswith("\u05d5"):
            return None
        if plain.endswith("\u05ea") and not plain.endswith(("\u05ea\u05d9", "\u05ea\u05dd", "\u05ea\u05df")):
            return None

    if tense == "past" and plain.endswith("\u05d5") and entry_type != "verb":
        return None

    return tense


def pick_word_for_skill(words=None, skill=None, progress=None):
    if skill is None:
        skill = words
        words = None

    progress = progress or {}
    sync_word_bank_from_progress(progress)
    allowed_words = set(words) if words is not None else None
    recent_words = set(progress.get("recent_words", [])[-5:])

    candidates = [
        stored_word
        for stored_word in WORD_BANK
        if skill_applicable(stored_word, skill)
        and (allowed_words is None or stored_word.get("word") in allowed_words)
        and stored_word.get("word") not in recent_words
    ]

    if not candidates:
        candidates = [
            stored_word
            for stored_word in WORD_BANK
            if skill_applicable(stored_word, skill)
            and (allowed_words is None or stored_word.get("word") in allowed_words)
        ]

    if not candidates and words is not None:
        candidates = [
            {"word": word, "skill_scores": {}}
            for word in words
            if word not in recent_words
        ] or [{"word": word, "skill_scores": {}} for word in words]

    if not candidates:
        raise ValueError(f"No words available for skill: {skill}")

    recent_prefixes = progress.get("recent_prefixes", [])[-5:]
    if skill in {"prefix", "identify_prefix_meaning", "identify_prefix_future", "preposition_meaning"}:
        varied_prefixes = [
            candidate
            for candidate in candidates
            if not extract_prefix(candidate["word"])
            or extract_prefix(candidate["word"]) not in recent_prefixes
        ]
        if recent_prefixes.count("\u05d5") >= 2:
            candidates = [
                candidate
                for candidate in varied_prefixes or candidates
                if extract_prefix(candidate["word"]) != "\u05d5"
            ] or varied_prefixes or candidates
        else:
            non_vav = [
                candidate
                for candidate in varied_prefixes or candidates
                if not candidate["word"].startswith("\u05d5")
            ]
            candidates = non_vav or varied_prefixes or candidates

    recent_suffixes = progress.get("recent_suffixes", [])[-5:]
    if skill in {"suffix", "identify_suffix_meaning", "identify_pronoun_suffix", "identify_suffix_past"}:
        non_vav_suffixes = [
            candidate
            for candidate in candidates
            if not candidate["word"].endswith("\u05d5")
        ]
        varied_suffixes = [
            candidate
            for candidate in candidates
            if not has_suffix(candidate["word"])
            or extract_suffix(candidate["word"]) not in recent_suffixes
        ]
        if recent_suffixes.count("\u05d5") >= 2:
            candidates = [
                candidate
                for candidate in varied_suffixes or candidates
                if not candidate["word"].endswith("\u05d5")
            ] or non_vav_suffixes or varied_suffixes or candidates
        else:
            candidates = non_vav_suffixes or varied_suffixes or candidates

    candidates.sort(
        key=lambda word_data: (
            word_data.setdefault("skill_scores", {}).get(skill, 0),
            progress.get("recent_words", []).count(word_data["word"]),
            word_data["word"],
        )
    )
    return candidates[0]["word"]


def remember_selected_word(progress, word, entry=None):
    progress.setdefault("recent_words", []).append(word)
    progress["recent_words"] = progress["recent_words"][-10:]

    prefix = extract_prefix(word) or ""
    if prefix:
        progress.setdefault("recent_prefixes", []).append(prefix)
        progress["recent_prefixes"] = progress["recent_prefixes"][-10:]

    suffix = (entry or {}).get("suffix") or (extract_suffix(word) if entry is None else "") or ""
    if suffix:
        progress.setdefault("recent_suffixes", []).append(suffix)
        progress["recent_suffixes"] = progress["recent_suffixes"][-10:]


def skill_question_payload(skill, target, question_text, choices, correct_answer, explanation):
    metadata = SKILL_METADATA[skill]
    payload = {
        "question_text": question_text,
        "question": question_text,
        "choices": choices,
        "correct_answer": correct_answer,
        "skill": skill,
        "mode": "pasuk" if skill in {"subject_identification", "phrase_translation"} else "word",
        "translation_mode": (
            TRANSLATION_NATURAL
            if skill in {"subject_identification", "phrase_translation"}
            else TRANSLATION_LITERAL
        ),
        "standard": metadata["standard"],
        "micro_standard": metadata["micro_standard"],
        "difficulty": metadata["difficulty"],
        "word": target["token"],
        "selected_word": target["token"],
        "explanation": explanation,
        "source": "generated skill question",
    }
    if target.get("source_pasuk"):
        payload["pasuk"] = target["source_pasuk"]
    return validate_question_payload(payload)


def prefix_level_question_payload(
    skill,
    target,
    level,
    question_format,
    question_text,
    choices,
    correct_answer,
    explanation,
):
    choices = unique([correct_answer] + [choice for choice in choices if choice != correct_answer])
    choices = choices[:4]
    question = skill_question_payload(
        skill,
        target,
        question_text,
        choices,
        correct_answer,
        explanation,
    )
    question["prefix_level"] = level
    question["prefix"] = extract_prefix(target["token"]) or target["entry"].get("prefix")
    question["question_format"] = question_format
    question["question_type"] = f"prefix_level_{level}_{question_format}"
    question["difficulty"] = level
    return validate_question_payload(question)


def choose_prefix_question_level(prefix_level, recent_question_formats):
    level = max(1, min(5, int(prefix_level or 1)))
    formats_by_level = {
        1: ["identify_prefix_letter"],
        2: ["identify_prefix_meaning"],
        3: ["apply_prefix_meaning"],
        4: ["distinguish_prefixes"],
        5: ["explain_prefix_function"],
    }
    formats = formats_by_level[level]
    recent = set((recent_question_formats or [])[-3:])
    available = [item for item in formats if item not in recent]
    return level, (available or formats)[0]


def generate_question(
    skill,
    pasuk=None,
    mode="direct",
    asked_tokens=None,
    asked_question_types=None,
    prefix_level=1,
    recent_question_formats=None,
    recent_prefixes=None,
    progress=None,
):
    if pasuk is None or (isinstance(pasuk, (list, tuple)) and not is_structured_pasuk(pasuk)):
        pasuk_pool = list(pasuk or CHUMASH_PESUKIM)
        if not pasuk_pool:
            raise ValueError("No pesukim available for question generation.")

        shuffled_pasuks = pasuk_pool[:]
        random.shuffle(shuffled_pasuks)
        last_error = None
        for selected_pasuk in shuffled_pasuks:
            try:
                question = generate_question(
                    skill,
                    selected_pasuk,
                    mode=mode,
                    asked_tokens=asked_tokens,
                    asked_question_types=asked_question_types,
                    prefix_level=prefix_level,
                    recent_question_formats=recent_question_formats,
                    recent_prefixes=recent_prefixes,
                    progress=progress,
                )
                question.setdefault("pasuk", selected_pasuk)
                return question
            except ValueError as error:
                last_error = error

        raise ValueError(f"No usable pasuk found for skill '{skill}': {last_error}")

    if skill not in SKILLS:
        raise ValueError(f"Unknown skill: {skill}. Expected one of: {', '.join(SKILLS)}")
    if mode not in {"direct", "context", "selection"}:
        raise ValueError("mode must be one of: direct, context, selection")
    if skill in {
        "identify_prefix_future",
        "identify_suffix_past",
        "identify_present_pattern",
        "convert_future_to_command",
        "match_pronoun_to_verb",
    }:
        return generate_word_structure_question(skill=skill, asked_question_ids=asked_tokens)

    word_bank, by_group = load_word_bank()
    if is_structured_pasuk(pasuk):
        pasuk_text = structured_pasuk_text(pasuk)
        analyzed = normalize_analyzed_pasuk(pasuk, word_bank)
    else:
        pasuk_text = pasuk
        try:
            analyzed = analyze_pasuk(pasuk, word_bank)
        except ValueError:
            analyzed = normalize_analyzed_pasuk(analyze_pasuk(pasuk), word_bank)
    pasuk = pasuk_text
    asked_set = set(asked_tokens or [])
    used_types = set(asked_question_types or [])
    asked_suffixes = [
        suffix
        for suffix in (extract_suffix(token) for token in (asked_tokens or []))
        if suffix
    ]
    if progress is None:
        progress = {
            "recent_words": list(asked_tokens or []),
            "recent_suffixes": asked_suffixes,
        }
    else:
        progress.setdefault("recent_words", list(asked_tokens or []))
        progress.setdefault("recent_suffixes", asked_suffixes)
    if recent_prefixes is not None:
        progress.setdefault("recent_prefixes", list(recent_prefixes))
    add_words_from_pasuk(pasuk_text, progress)

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
        stable_rng(f"{pasuk_text}|{skill}|choices").shuffle(choices)
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
        candidates = structured_word_bank_items(
            predicate,
            word_bank=word_bank,
            pasuk_text=pasuk_text,
            progress=progress,
        )
        if not candidates:
            candidates = [item for item in analyzed if predicate(item["entry"], item["token"])]
        if not candidates and fallback is not None:
            target = fallback()
            if target is not None:
                target.setdefault(
                    "source_pasuk",
                    find_pasuk_for_word(
                        target["token"],
                        fallback=pasuk_text,
                        progress=progress,
                    ),
                )
                remember_selected_word(progress, target["token"], target["entry"])
            return target
        if not candidates:
            target = analyzed[0]
            target.setdefault(
                "source_pasuk",
                find_pasuk_for_word(
                    target["token"],
                    fallback=pasuk_text,
                    progress=progress,
                ),
            )
            remember_selected_word(progress, target["token"], target["entry"])
            return target

        unused = [item for item in candidates if item["token"] not in asked_set]
        pool = unused or candidates
        selected_word = pick_word_for_skill(
            [item["token"] for item in pool],
            skill,
            progress,
        )
        target = next((item for item in pool if item["token"] == selected_word), pool[0])
        target.setdefault(
            "source_pasuk",
            find_pasuk_for_word(
                target["token"],
                fallback=pasuk_text,
                progress=progress,
            ),
        )
        remember_selected_word(progress, target["token"], target["entry"])
        return target

    def grammar_choice_payload(target, question_text, correct, choices, explanation):
        return skill_question_payload(
            skill,
            target,
            question_text,
            clean_choices(correct, choices),
            correct,
            explanation,
        )

    def build_prefix_level_question():
        recent_prefixes_window = list(recent_prefixes or [])[-5:]
        prefix_candidates = structured_word_bank_items(
            lambda entry, token: is_prefix_candidate(entry, token, word_bank),
            word_bank=word_bank,
            pasuk_text=pasuk_text,
            progress=progress,
        )
        if not prefix_candidates:
            prefix_candidates = [
                item
                for item in analyzed
                if is_prefix_candidate(item["entry"], item["token"], word_bank)
            ]
        available_prefix_candidates = [
            item
            for item in prefix_candidates
            if recent_prefixes_window.count(item["entry"].get("prefix") or extract_prefix(item["token"])) < 2
        ]

        target = None
        if available_prefix_candidates:
            selected_word = pick_word_for_skill(
                [item["token"] for item in available_prefix_candidates],
                "prefix",
                progress,
            )
            target = next(
                (
                    item
                    for item in available_prefix_candidates
                    if item["token"] == selected_word
                ),
                available_prefix_candidates[0],
            )

        if target is None:
            raise ValueError("No usable prefixed word found in this pasuk.")
        target.setdefault(
            "source_pasuk",
            find_pasuk_for_word(
                target["token"],
                fallback=pasuk_text,
                progress=progress,
            ),
        )
        remember_selected_word(progress, target["token"], target["entry"])

        level, question_format = choose_prefix_question_level(
            prefix_level,
            recent_question_formats,
        )
        apply_prefix_metadata(target["token"], target["entry"], word_bank)
        prefix = extract_prefix(target["token"])
        prefix_meaning = PREFIX_MEANINGS.get(prefix)
        base_word = target["entry"].get("base_word") or target.get("base") or target["token"]
        word_meaning = target["entry"].get("translation")

        if level == 1:
            return prefix_level_question_payload(
                skill,
                target,
                level,
                question_format,
                f"What is the prefix in {target['token']}?",
                [prefix, "ו", "ב", "ל", "מ", "כ", "ה", "ש"],
                prefix,
                f"The prefix in {target['token']} is {prefix}.",
            )

        if level == 2:
            return prefix_level_question_payload(
                skill,
                target,
                level,
                question_format,
                f"What does the prefix {prefix} add?",
                prefix_meaning_choices(prefix),
                prefix_meaning,
                f"In {target['token']}, {prefix} means '{prefix_meaning}'.",
            )

        if level == 3:
            base_translation = root_meaning(target["entry"])
            return prefix_level_question_payload(
                skill,
                target,
                level,
                question_format,
                f"What does {target['token']} mean?",
                [
                    word_meaning,
                    base_translation,
                    f"from {base_translation}",
                    f"to {base_translation}",
                    f"in {base_translation}",
                ],
                word_meaning,
                f"{prefix} adds '{prefix_meaning}' to {base_word}.",
            )

        if level == 4:
            return prefix_level_question_payload(
                skill,
                target,
                level,
                question_format,
                f"Which prefix means '{prefix_meaning}' here?",
                ["ו", "ב", "ל", "מ", "כ", "ה", "ש"],
                prefix,
                f"The word {target['token']} uses {prefix} for '{prefix_meaning}'.",
            )

        return prefix_level_question_payload(
            skill,
            target,
            level,
            question_format,
            f"What job does {prefix} do in {target['token']}?",
            [
                f"adds '{prefix_meaning}' to the word",
                "marks ownership at the end",
                "changes the word into a noun",
                "removes the base word meaning",
            ],
            f"adds '{prefix_meaning}' to the word",
            f"The prefix {prefix} helps show '{prefix_meaning}' in {target['token']}.",
        )

    if skill == "identify_prefix_meaning":
        return build_prefix_level_question()

    if skill == "identify_suffix_meaning":
        target = choose_target(lambda entry, token: is_suffix_candidate(entry, token, word_bank))
        target = with_suffix_metadata(target, word_bank)
        if target is None:
            raise ValueError("No suffixed word found in this pasuk.")
        suffix = target["entry"].get("suffix")
        correct = SUFFIX_MEANINGS.get(suffix)
        return grammar_choice_payload(
            target,
            f"What does the suffix {suffix} add?",
            correct,
            list(SUFFIX_MEANINGS.values()),
            f"In {target['token']}, {suffix} means '{correct}'.",
        )

    if skill == "identify_pronoun_suffix":
        target = choose_target(lambda entry, token: is_suffix_candidate(entry, token, word_bank))
        target = with_suffix_metadata(target, word_bank)
        if target is None:
            raise ValueError("No pronoun suffix found in this pasuk.")
        suffix = target["entry"].get("suffix")
        correct = SUFFIX_MEANINGS.get(suffix)
        return grammar_choice_payload(
            target,
            f"What does the ending {suffix} mean?",
            correct,
            list(SUFFIX_MEANINGS.values()),
            f"The ending {suffix} in {target['token']} means '{correct}'.",
        )

    if skill == "identify_verb_marker":
        target = choose_target(
            lambda entry, token: entry.get("type") == "verb" and is_prefix_candidate(entry, token, word_bank)
        )
        if target is None:
            raise ValueError("No prefixed verb found in this pasuk.")
        apply_prefix_metadata(target["token"], target["entry"], word_bank)
        prefix = extract_prefix(target["token"])
        correct = PREFIX_MEANINGS.get(prefix)
        return grammar_choice_payload(
            target,
            f"What does the first letter {prefix} add?",
            correct,
            prefix_meaning_choices(prefix),
            f"In {target['token']}, {prefix} marks '{correct}'.",
        )

    if skill == "segment_word_parts":
        target = choose_target(
            lambda entry, token: bool(is_prefix_candidate(entry, token, word_bank) or is_suffix_candidate(entry, token, word_bank)),
        )
        if target is None:
            raise ValueError("No word with a prefix or suffix found in this pasuk.")
        target = with_suffix_metadata(target, word_bank)
        apply_prefix_metadata(target["token"], target["entry"], word_bank)
        prefix = extract_prefix(target["token"])
        suffix = target["entry"].get("suffix")
        if prefix:
            correct = prefix
            meaning = PREFIX_MEANINGS.get(prefix)
            question_text = f"Which part means '{meaning}'?"
            choices = [prefix, target["entry"].get("shoresh"), suffix, target["token"]]
            explanation = f"In {target['token']}, {prefix} means '{meaning}'."
        else:
            correct = suffix
            meaning = SUFFIX_MEANINGS.get(suffix)
            question_text = f"Which part means '{meaning}'?"
            choices = [suffix, target["entry"].get("shoresh"), target["token"][:1], target["token"]]
            explanation = f"In {target['token']}, {suffix} means '{meaning}'."
        return grammar_choice_payload(target, question_text, correct, choices, explanation)

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
        target_item = (
            find_first(analyzed, lambda _entry, token: token not in asked_set)
            or get_verb(analyzed)
        )
        target_token = target_item["token"] if target_item else None

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
            if target_token in phrase.split():
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
            if target_token in phrase.split():
                phrase_options.append((phrase, correct, candidates))

        phrase, phrase_items = varied_phrase_window(
            analyzed,
            target_token=target_token,
            recent_phrases=asked_set,
            key=f"{pasuk}|phrase_parts",
        )
        correct = format_translation(phrase_items, TRANSLATION_NATURAL)
        literal = format_translation(phrase_items, TRANSLATION_LITERAL)
        candidates = [
            literal,
            " ".join(reversed([describe(item) for item in phrase_items])),
            f"{describe(phrase_items[0])} in {describe(phrase_items[-1])}",
            f"{describe(phrase_items[0])} from {describe(phrase_items[-1])}",
            f"{describe(phrase_items[-1])} to {describe(phrase_items[0])}",
        ]
        phrase_options.append((phrase, correct, candidates))

        unused = [item for item in phrase_options if item[0] not in asked_set]
        return stable_rng(f"{pasuk}|phrase_choice|{len(asked_set)}").choice(
            unused or phrase_options
        )

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
        if mode == "selection":
            recent_prefixes_window = list(recent_prefixes or [])[-5:]
            prefix_pool = structured_word_bank_items(
                lambda entry, token: is_prefix_candidate(entry, token, word_bank),
                word_bank=word_bank,
                pasuk_text=pasuk_text,
                progress=progress,
            )
            if not prefix_pool:
                prefix_pool = analyzed
            candidates = [
                item
                for item in prefix_pool
                if is_prefix_candidate(item["entry"], item["token"], word_bank)
                and item["token"] not in asked_set
                and recent_prefixes_window.count(item["entry"].get("prefix") or extract_prefix(item["token"])) < 2
            ]
            fallback_candidates = [
                item
                for item in prefix_pool
                if is_prefix_candidate(item["entry"], item["token"], word_bank)
                and recent_prefixes_window.count(item["entry"].get("prefix") or extract_prefix(item["token"])) < 2
            ]
            pool = candidates or fallback_candidates
            if pool:
                selected_word = pick_word_for_skill(
                    [item["token"] for item in pool],
                    "prefix",
                    progress,
                )
                target = next((item for item in pool if item["token"] == selected_word), pool[0])
                target.setdefault(
                    "source_pasuk",
                    find_pasuk_for_word(
                        target["token"],
                        fallback=pasuk_text,
                        progress=progress,
                    ),
                )
                remember_selected_word(progress, target["token"], target["entry"])
            else:
                target = None
            if target is None:
                raise ValueError("No usable prefixed word found in this pasuk.")
            apply_prefix_metadata(target["token"], target["entry"], word_bank)
            prefix = extract_prefix(target["token"])
            correct = PREFIX_MEANINGS.get(prefix, "")
            return finish(skill_question_payload(
                skill,
                target,
                f"Which word contains a prefix meaning \"{correct}\"?",
                pasuk_word_choices(target["token"]),
                target["token"],
                f"{target['token']} contains the prefix {prefix}, meaning '{correct}'.",
            ))
        return build_prefix_level_question()

    if skill == "suffix":
        target = choose_target(
            lambda entry, token: is_suffix_candidate(entry, token, word_bank),
            lambda: get_suffixed_word(analyzed, word_bank),
        )
        target = with_suffix_metadata(target, word_bank)
        if target is None:
            raise ValueError("No suffixed word found in this pasuk.")
        suffix = target["entry"].get("suffix", "")
        correct = SUFFIX_MEANINGS.get(suffix, "")
        if mode == "selection":
            return finish(skill_question_payload(
                skill,
                target,
                f"Which word contains a suffix meaning \"{correct}\"?",
                pasuk_word_choices(target["token"]),
                target["token"],
                f"{target['token']} contains the suffix {suffix}, meaning '{correct}'.",
            ))
        choices = clean_choices(correct, list(SUFFIX_MEANINGS.values()))
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

    if skill in {"verb_tense", "identify_tense"}:
        target = choose_target(
            lambda entry, token: confident_verb_tense(entry, token) is not None,
        )
        correct = infer_tense(target["entry"], target["token"])
        if correct is None:
            raise ValueError("No confidently classified verb tense found in this pasuk.")
        if mode == "selection":
            return finish(skill_question_payload(
                skill,
                target,
                f"Which word shows {correct} tense?",
                pasuk_word_choices(target["token"]),
                target["token"],
                f"{target['token']} shows {correct} tense.",
            ))
        choices = clean_choices(correct, ["past", "future", "command", "not a verb"])
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
            get_recipient(analyzed)
            or get_direct_object(analyzed)
            or find_first(
                analyzed,
                lambda entry, _token: entry.get("type") == "noun"
                and entry.get("group") != "people"
                and not is_prefix_candidate(entry, _token, word_bank),
            )
        )
        if target is None:
            raise ValueError("No object found in this pasuk.")
        remember_selected_word(progress, target["token"], target["entry"])

        is_person_object = target["entry"].get("group") == "people"
        correct = (
            strip_relation(target["entry"]["translation"])
            if is_person_object or is_suffix_candidate(target["entry"], target["token"], word_bank)
            else target["entry"]["translation"]
        )
        choices = (
            people_translation_choices(correct)
            if is_person_object
            else noun_translation_choices(correct)
        )
        question_text = (
            "Who is the action done to?"
            if is_person_object or is_suffix_candidate(target["entry"], target["token"], word_bank)
            else "What does this word mean?"
        )
        return skill_question_payload(
            skill,
            target,
            question_text,
            choices,
            correct,
            f"{target['token']} means '{correct}'.",
        )

    if skill == "preposition_meaning":
        target = choose_target(
            lambda entry, _token: entry.get("type") == "prep"
            or (
                is_prefix_candidate(entry, _token, word_bank)
                and extract_prefix(_token) in {"\u05d1", "\u05dc", "\u05de"}
            ),
        )
        apply_prefix_metadata(target["token"], target["entry"], word_bank)
        prefix = extract_prefix(target["token"]) or target["entry"].get("prefix", "")
        correct = PREFIX_MEANINGS.get(prefix) or target["entry"].get("translation")
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
        find_after(
            analyzed,
            verb_index,
            lambda entry, _token: entry.get("role_hint") == "subject_candidate"
            and entry.get("semantic_group") in {"person", "divine"},
        )
        or find_first(
            analyzed,
            lambda entry, _token: entry.get("role_hint") == "subject_candidate"
            and entry.get("semantic_group") in {"person", "divine"},
        )
        or find_after(analyzed, verb_index, lambda entry, _token: entry.get("group") == "people")
        or find_first(analyzed, lambda entry, _token: entry.get("group") == "people")
        or analyzed[0]
    )


def get_source(analyzed):
    return find_first(analyzed, lambda entry, token: extract_prefix(token) == "\u05de")


def get_recipient(analyzed):
    return find_first(analyzed, lambda entry, token: extract_prefix(token) == "\u05dc")


def get_destination(analyzed):
    marker = find_first(
        analyzed,
        lambda entry, token: token == "\u05d0\u05dc" or extract_prefix(token) == "\u05dc",
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
        lambda entry, token: entry.get("group") in {"object", "place"}
        and not is_prefix_candidate(entry, token),
    )


def get_prefixed_or_suffixed(analyzed, word_bank=None):
    target = (
        find_first(analyzed, lambda entry, token: is_prefix_candidate(entry, token) and entry.get("suffix"))
        or find_first(
            analyzed,
            lambda entry, token: (is_prefix_candidate(entry, token, word_bank) or is_suffix_candidate(entry, token, word_bank))
            and entry.get("type") != "verb",
        )
        or find_first(analyzed, lambda entry, token: is_prefix_candidate(entry, token, word_bank) or is_suffix_candidate(entry, token, word_bank))
        or analyzed[0]
    )
    return with_suffix_metadata(target, word_bank)


def build_translation_question(step, pasuk, analyzed, by_group, word_bank=None):
    target = first_ready(analyzed, "translation")
    if target is None:
        raise ValueError("No quiz-ready translation target found in this pasuk.")
    entry = target["entry"]
    correct = usable_translation(entry, target["token"])
    distractors = translation_distractors(correct, entry, by_group, word_bank)
    choices = build_choices(
        correct,
        distractors,
        "not the meaning here",
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
        correct,
        f"{target['token']} means '{correct}'.",
        2,
    )


def build_pr_question(step, pasuk, analyzed, word_bank=None):
    target = first_ready(analyzed, "prefix_suffix") or get_prefixed_or_suffixed(analyzed, word_bank)
    entry = target["entry"]
    apply_prefix_metadata(target["token"], entry, word_bank)
    prefix = extract_prefix(target["token"]) or entry.get("prefix", "")
    suffix = entry.get("suffix", "")
    prefix_meaning = PREFIX_MEANINGS.get(prefix, entry.get("prefix_meaning", ""))
    suffix_meaning = SUFFIX_MEANINGS.get(suffix, entry.get("suffix_meaning", ""))

    if prefix and prefix_meaning:
        correct = prefix_meaning
        partials = [
            item
            for item in prefix_meaning_choices(prefix)
            if item != correct
        ]
        extra = [
            value
            for value in PREFIX_MEANINGS.values()
            if value != correct
        ]
        clear = "possessive suffix"
        micro_standard = "PR1"
    elif suffix and suffix_meaning:
        correct = suffix_meaning
        partials = [
            value
            for value in SUFFIX_MEANINGS.values()
            if value != correct
        ]
        extra = ["and", "the", "to / for"]
        clear = "prefix meaning"
        micro_standard = "PR2"
    else:
        raise ValueError("No quiz-ready prefix or suffix target found in this pasuk.")

    choices = build_choices(correct, partials, clear, f"{pasuk}|pr", extra=extra)
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


def build_phrase_question(step, pasuk, analyzed, recent_phrases=None):
    source = get_source(analyzed)
    marker, destination = get_destination(analyzed)
    recipient = get_recipient(analyzed)
    direct_object = get_direct_object(analyzed)
    subject = get_subject(analyzed)
    phrase_options = []

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
        phrase_options.append((phrase, correct, partials, clear))

    if recipient and direct_object:
        phrase = f"{direct_object['token']} {recipient['token']}"
        recipient_text = strip_relation(describe(recipient))
        correct = f"{describe(direct_object)} to {recipient_text}"
        partials = [
            f"{describe(direct_object)} from {recipient_text}",
            f"{describe(direct_object)} with {recipient_text}",
        ]
        clear = f"{describe(direct_object)} to {strip_relation(describe(subject))}"
        phrase_options.append((phrase, correct, partials, clear))

    target_token = get_verb(analyzed)["token"] if get_verb(analyzed) else None
    phrase, phrase_items = varied_phrase_window(
        analyzed,
        target_token=target_token,
        recent_phrases=recent_phrases,
        key=f"{pasuk}|build_phrase",
    )
    correct = format_translation(phrase_items, TRANSLATION_NATURAL)
    literal = format_translation(phrase_items, TRANSLATION_LITERAL)
    partials = [
        literal,
        " ".join(reversed([describe(item) for item in phrase_items])),
        f"{describe(phrase_items[0])} in {describe(phrase_items[-1])}",
    ]
    clear = f"{describe(phrase_items[-1])} from {describe(phrase_items[0])}"
    extra = phrase_choice_fallbacks(analyzed, phrase_items, correct)
    phrase_options.append((phrase, correct, partials, clear))

    phrase, correct, partials, clear = stable_rng(f"{pasuk}|phrase_question|{step}").choice(
        phrase_options
    )

    choices = build_choices(correct, partials, clear, f"{pasuk}|phrase", extra=extra)
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


def build_subject_question(step, pasuk, analyzed, by_group, word_bank=None):
    subject = first_ready(analyzed, "subject_identification")
    if subject is None:
        raise ValueError("No quiz-ready subject found in this pasuk.")
    correct = usable_translation(subject["entry"], subject["token"])
    distractor_entries = [
        item["entry"]
        for item in analyzed
        if item is not subject
        and item["entry"].get("semantic_group") in {"cosmic_entity", "place", "time", "object"}
    ]
    distractor_entries.extend(
        entry
        for entry in word_bank_entries(word_bank, source_derived_only=True)
        if entry.get("semantic_group") in {"divine", "person", "cosmic_entity", "place"}
    )
    distractor_entries.extend(
        entry
        for entry in by_group.get("people", [])
    )
    distractors = filtered_translation_values(
        distractor_entries,
        correct,
        subject["entry"],
        question_type="subject_identification",
    )
    choices = build_choices(
        correct,
        distractors,
        "someone else",
        f"{pasuk}|subject",
        extra=["not the subject", "the action", "the time"],
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


def phrase_choice_fallbacks(analyzed, phrase_items, correct):
    fallbacks = []
    for length in range(2, min(4, len(analyzed)) + 1):
        for start in range(0, len(analyzed) - length + 1):
            items = analyzed[start:start + length]
            text = format_translation(items, TRANSLATION_NATURAL)
            if text != correct:
                fallbacks.append(text)
            reversed_text = " ".join(reversed([describe(item) for item in items]))
            if reversed_text != correct:
                fallbacks.append(reversed_text)
    if phrase_items:
        fallbacks.extend(
            [
                f"{describe(phrase_items[0])} after {describe(phrase_items[-1])}",
                f"{describe(phrase_items[-1])} before {describe(phrase_items[0])}",
                "not a connected phrase",
            ]
        )
    return unique(fallbacks)


def build_shoresh_question(step, pasuk, analyzed, word_bank=None):
    target = first_ready(analyzed, "shoresh")
    if target is None:
        raise ValueError("No quiz-ready shoresh target found in this pasuk.")
    correct = target["entry"].get("shoresh")
    distractors = [
        shoresh
        for shoresh in valid_shorashim(word_bank)
        if shoresh != correct
    ]
    choices = build_choices(
        correct,
        distractors,
        "not a verb",
        f"{pasuk}|shoresh",
    )
    return make_question(
        step,
        "shoresh",
        "SR",
        "SR1",
        "shoresh",
        target["token"],
        f"What is the shoresh of {target['token']}?",
        choices,
        correct,
        f"The shoresh of {target['token']} is {correct}.",
        3,
    )


def build_tense_question(step, pasuk, analyzed):
    target = first_ready(analyzed, "verb_tense")
    if target is None:
        raise ValueError("No quiz-ready verb tense target found in this pasuk.")
    correct = target["entry"].get("tense")
    choices = build_choices(
        correct,
        [item for item in CONTROLLED_TENSE_CHOICES if item != correct],
        "not a verb",
        f"{pasuk}|tense",
    )
    return make_question(
        step,
        "verb_tense",
        "PR",
        "PR5",
        "verb_tense",
        target["token"],
        "What verb tense is shown?",
        choices,
        correct,
        f"{target['token']} is read as {correct}.",
        3,
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


def generate_pasuk_flow(pasuk: str, asked_question_types=None, recent_phrases=None):
    word_bank, by_group = load_word_bank()
    analyzed = analyze_pasuk(pasuk, word_bank)
    used_types = set(asked_question_types or [])

    builders = [
        ("word_meaning", lambda step: build_translation_question(step, pasuk, analyzed, by_group, word_bank)),
        ("prefix_suffix", lambda step: build_pr_question(step, pasuk, analyzed, word_bank)),
        ("subject_identification", lambda step: build_subject_question(step, pasuk, analyzed, by_group, word_bank)),
        ("verb_tense", lambda step: build_tense_question(step, pasuk, analyzed)),
        ("shoresh", lambda step: build_shoresh_question(step, pasuk, analyzed, word_bank)),
        (
            "phrase_meaning",
            lambda step: build_phrase_question(
                step,
                pasuk,
                analyzed,
                recent_phrases=recent_phrases,
            ),
        ),
    ]
    active_builders = [item for item in builders if item[0] not in used_types]
    if len(active_builders) < 3:
        active_builders = builders
    questions = []
    errors = []
    for kind, builder in active_builders:
        try:
            questions.append(builder(len(questions) + 1))
        except ValueError as error:
            errors.append(f"{kind}: {error}")
        if len(questions) >= 4:
            break
    if len(questions) < 3 and active_builders is not builders:
        for kind, builder in builders:
            if kind in {question.get("question_type") for question in questions}:
                continue
            try:
                questions.append(builder(len(questions) + 1))
            except ValueError as error:
                errors.append(f"{kind}: {error}")
            if len(questions) >= 3:
                break
    if len(questions) < 3:
        raise ValueError(
            "Could not build enough quiz-ready pasuk flow questions: "
            + "; ".join(errors)
        )
    questions = sorted(questions, key=lambda item: item.get("difficulty", 0))
    for index, question in enumerate(questions, 1):
        question["step"] = index
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
        build_subject_question(3, pesukim[0], analyzed_flows[0], _by_group, word_bank),
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
