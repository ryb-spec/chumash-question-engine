import argparse
import json
import random
import re
import sys

from assessment_scope import (
    LEGACY_PASUK_FLOW_PREVIEW_PATH,
    LEGACY_PASUK_FLOWS_PATH,
    LEGACY_QUESTIONS_PATH,
)
from runtime.presentation import get_error_type

try:
    from pasuk_flow_generator import generate_pasuk_flow, generate_question as generate_skill_question
except ImportError:
    generate_pasuk_flow = None
    generate_skill_question = None

from skill_tracker import check_mastery, update_skill_progress

STANDARDS = ["WM", "SR", "PR", "CF", "PC", "PS", "SS", "CM"]
SKILL_ORDER = [
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
    "part_of_speech",
    "shoresh",
    "prefix",
    "suffix",
    "translation",
    "verb_tense",
    "subject_identification",
    "object_identification",
    "preposition_meaning",
    "phrase_translation",
]
PS_MICRO_STANDARDS = ["PS1", "PS2", "PS3", "PS4", "PS5"]
SS_MICRO_STANDARDS = ["SS1", "SS2", "SS3", "SS4", "SS5"]
TARGET_STANDARD_WEIGHTS = {
    "WM": 0.4,
    "SR": 0.15,
    "PR": 0.15,
    "CF": 0.08,
    "PC": 0.03,
    "PS": 0.2,
    "SS": 0.1,
    "CM": 0.03,
}
MAX_SS_IN_A_ROW = 2
MIN_QUESTIONS_BEFORE_LEVEL5 = 10
MAX_LEVEL5_SESSION_RATIO = 0.2
FAST_TRACK_MIN_QUESTIONS = 5
FAST_TRACK_ACCURACY = 0.8
EARLY_LEVEL4_CORRECT = 4
EARLY_LEVEL5_CORRECT = 6
EARLY_SS_WM_CORRECT = 3
MAX_SAME_WORD_RECENT = 2
RECENT_WORD_WINDOW = 10
CHALLENGE_STREAK = 3

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def parse_args():
    parser = argparse.ArgumentParser(description="Run the Chumash quiz.")
    parser.add_argument(
        "--test",
        action="store_true",
        help="Enable test mode and manually filter questions.",
    )
    parser.add_argument(
        "--standard",
        choices=STANDARDS,
        help="In test mode, only show questions from this standard.",
    )
    parser.add_argument(
        "--min-difficulty",
        type=int,
        choices=range(1, 6),
        metavar="1-5",
        help="In test mode, only show questions at this difficulty or higher.",
    )
    parser.add_argument(
        "--max-difficulty",
        type=int,
        choices=range(1, 6),
        metavar="1-5",
        help="In test mode, only show questions at this difficulty or lower.",
    )
    parser.add_argument(
        "--pasuk-flow",
        action="store_true",
        help="Run guided pasuk flow mode instead of adaptive quiz mode.",
    )
    parser.add_argument(
        "--source",
        help="In pasuk flow mode, choose a flow by source, for example בראשית יב:א.",
    )
    parser.add_argument(
        "--pasuk",
        help="In pasuk flow mode, choose a flow by exact pasuk text.",
    )
    args = parser.parse_args()

    if (
        args.min_difficulty is not None
        and args.max_difficulty is not None
        and args.max_difficulty < args.min_difficulty
    ):
        parser.error("--max-difficulty cannot be lower than --min-difficulty.")

    if args.standard or args.min_difficulty is not None or args.max_difficulty is not None:
        args.test = True

    return args


HEBREW_WORD_RE = re.compile(r"[\u0590-\u05ff]+")


def display_text(text):
    if not isinstance(text, str):
        return text

    # Keep Hebrew stored and printed in normal order, but isolate Hebrew runs
    # so mixed English/Hebrew prompts have a better chance of displaying cleanly.
    return HEBREW_WORD_RE.sub(lambda match: f"\u2067{match.group(0)}\u2069", text)


def load_word_bank_metadata():
    try:
        with open("word_bank.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return {}

    metadata = {}
    for entry in data.get("words", []):
        metadata.setdefault(entry["word"], entry)
    return metadata


def get_question_debug(question, word_bank_metadata):
    group = question.get("generation_group")
    selected_word = question.get("selected_word") or question.get("word", "")
    word_entry = None

    if selected_word in word_bank_metadata:
        word_entry = word_bank_metadata[selected_word]
    else:
        for token in selected_word.split():
            if token in word_bank_metadata:
                word_entry = word_bank_metadata[token]
                break

    if group is None and word_entry is not None:
        group = word_entry.get("group")

    difficulty = question.get("difficulty")
    if difficulty is None and word_entry is not None:
        difficulty = word_entry.get("difficulty")

    distractor_group = question.get("generation_group")

    return {
        "word": selected_word,
        "group": group or "unknown",
        "difficulty": difficulty if difficulty is not None else "unknown",
        "distractors_from": f"{distractor_group} group" if distractor_group else "unknown",
    }


def print_question_debug(question, word_bank_metadata):
    debug = get_question_debug(question, word_bank_metadata)
    print(f"Word: {display_text(debug['word'])}")
    print(f"Group: {debug['group']}")
    print(f"Difficulty: {debug['difficulty']}")
    print(f"Distractors from: {debug['distractors_from']}")


def get_session_accuracy(session_stats):
    answered = session_stats.get("answered", 0)
    if answered == 0:
        return 0
    return session_stats.get("correct", 0) / answered


def get_max_difficulty(progress, session_stats=None):
    session_stats = session_stats or {}
    standards = progress["standards"]
    max_difficulty = 1

    if standards["WM"] >= 60:
        max_difficulty = 2
    if standards["SR"] >= 60:
        max_difficulty = 3
    if standards["PR"] >= 60:
        max_difficulty = 4
    if standards["CF"] >= 70:
        max_difficulty = 5

    session_accuracy = get_session_accuracy(session_stats)
    session_correct = session_stats.get("correct", 0)
    session_answered = session_stats.get("answered", 0)

    if session_answered >= FAST_TRACK_MIN_QUESTIONS and session_accuracy >= FAST_TRACK_ACCURACY:
        max_difficulty = min(5, max_difficulty + 1)
    if session_correct >= EARLY_LEVEL4_CORRECT:
        max_difficulty = max(max_difficulty, 4)
    if session_correct >= EARLY_LEVEL5_CORRECT and session_accuracy >= FAST_TRACK_ACCURACY:
        max_difficulty = 5

    return max_difficulty


def get_allowed_ps_micro_standards(progress):
    standards = progress["standards"]
    micro_standards = progress["micro_standards"]
    allowed = ["PS1", "PS2"]

    ps_foundation_score = (
        micro_standards.get("PS1", 0) + micro_standards.get("PS2", 0)
    ) / 2

    if ps_foundation_score >= 70:
        allowed.append("PS3")
    if standards.get("PR", 0) >= 60:
        allowed.append("PS4")
    if standards.get("CF", 0) >= 65:
        allowed.append("PS5")

    return allowed


def get_allowed_ss_micro_standards(progress, session_stats=None):
    session_stats = session_stats or {}
    standards = progress["standards"]
    micro_standards = progress["micro_standards"]

    if (
        session_stats.get("wm_correct", 0) < EARLY_SS_WM_CORRECT
        and (standards.get("PS", 0) < 60 or standards.get("PR", 0) < 60)
    ):
        return []

    allowed = ["SS1", "SS2"]
    ss_foundation_score = (
        micro_standards.get("SS1", 0) + micro_standards.get("SS2", 0)
    ) / 2

    if ss_foundation_score >= 70:
        allowed.append("SS3")
    if micro_standards.get("SS3", 0) >= 70:
        allowed.append("SS4")
    if micro_standards.get("SS4", 0) >= 70:
        allowed.append("SS5")

    return allowed


def get_standard_group(standard):
    if standard in {"SR", "PR"}:
        return "SR_PR"
    return standard


def filter_questions_by_progression(questions, progress, max_difficulty, session_stats=None):
    allowed_ps_micro_standards = set(get_allowed_ps_micro_standards(progress))
    allowed_ss_micro_standards = set(get_allowed_ss_micro_standards(progress, session_stats))

    return [
        question
        for question in questions
        if question["difficulty"] <= max_difficulty
        and (
            question["standard"] != "PS"
            or question["micro_standard"] in allowed_ps_micro_standards
        )
        and (
            question["standard"] != "SS"
            or question["micro_standard"] in allowed_ss_micro_standards
        )
    ]


def filter_questions_by_session_limits(questions, session_stats):
    questions_answered = session_stats.get("answered", 0)
    level5_answered = session_stats.get("level5_answered", 0)
    session_accuracy = get_session_accuracy(session_stats)
    session_correct = session_stats.get("correct", 0)
    allow_level5_by_count = questions_answered >= MIN_QUESTIONS_BEFORE_LEVEL5
    allow_level5_by_early_challenge = (
        session_correct >= EARLY_LEVEL5_CORRECT
        and session_accuracy >= FAST_TRACK_ACCURACY
    )
    allow_level5_by_ratio = (
        (level5_answered + 1) / (questions_answered + 1)
        <= MAX_LEVEL5_SESSION_RATIO
    )

    if (allow_level5_by_count or allow_level5_by_early_challenge) and allow_level5_by_ratio:
        return questions

    return [question for question in questions if question.get("difficulty") != 5]


def get_question_group(question, word_bank_metadata):
    group = question.get("generation_group")
    if group:
        return group

    selected_word = question.get("selected_word") or question.get("word", "")
    if selected_word in word_bank_metadata:
        return word_bank_metadata[selected_word].get("group", "unknown")

    for token in selected_word.split():
        if token in word_bank_metadata:
            return word_bank_metadata[token].get("group", "unknown")

    return "unknown"


def filter_recent_word_repetition(question_pool, recent_words):
    recent_window = recent_words[-RECENT_WORD_WINDOW:]
    filtered = [
        question
        for question in question_pool
        if recent_window.count(question["word"]) < MAX_SAME_WORD_RECENT
    ]
    return filtered or question_pool


def filter_recent_group_and_skill(question_pool, recent_groups, recent_skills, word_bank_metadata):
    filtered = question_pool

    if recent_groups:
        recent_group = recent_groups[-1]
        group_filtered = [
            question
            for question in filtered
            if get_question_group(question, word_bank_metadata) != recent_group
        ]
        if group_filtered:
            filtered = group_filtered

    if recent_skills:
        recent_skill = recent_skills[-1]
        skill_filtered = [
            question
            for question in filtered
            if question.get("skill") != recent_skill
        ]
        if skill_filtered:
            filtered = skill_filtered

    return filtered


def select_challenge_pool(allowed_questions, max_difficulty, session_stats):
    if session_stats.get("consecutive_correct", 0) < CHALLENGE_STREAK:
        return None

    target_difficulty = min(5, max_difficulty + 1)
    challenge_pool = [
        question
        for question in allowed_questions
        if question.get("difficulty") == target_difficulty
    ]
    return challenge_pool or None


def get_question_id(question):
    return question.get("id") or question.get("question")


def get_next_skill(current_skill):
    try:
        index = SKILL_ORDER.index(current_skill)
    except ValueError:
        return SKILL_ORDER[0]

    if index + 1 >= len(SKILL_ORDER):
        return current_skill

    return SKILL_ORDER[index + 1]
def get_current_focus_skill(progress):
    return progress.get("current_skill", SKILL_ORDER[0])


def get_target_difficulty(progress, session_stats):
    target_difficulty = get_max_difficulty(progress, session_stats)

    if (
        get_session_accuracy(session_stats) >= FAST_TRACK_ACCURACY
        and session_stats.get("answered", 0) >= FAST_TRACK_MIN_QUESTIONS
    ):
        target_difficulty = min(5, target_difficulty + 1)

    if session_stats.get("correct", 0) >= EARLY_LEVEL4_CORRECT:
        target_difficulty = max(target_difficulty, 4)

    if (
        session_stats.get("correct", 0) >= EARLY_LEVEL5_CORRECT
        and get_session_accuracy(session_stats) >= FAST_TRACK_ACCURACY
    ):
        target_difficulty = 5

    if session_stats.get("consecutive_correct", 0) >= CHALLENGE_STREAK:
        target_difficulty = min(5, target_difficulty + 1)

    return target_difficulty


def level5_allowed(question, session_stats):
    if question.get("difficulty") != 5:
        return True

    questions_answered = session_stats.get("answered", 0)
    level5_answered = session_stats.get("level5_answered", 0)
    early_level5 = (
        session_stats.get("correct", 0) >= EARLY_LEVEL5_CORRECT
        and get_session_accuracy(session_stats) >= FAST_TRACK_ACCURACY
    )
    normal_level5 = questions_answered >= MIN_QUESTIONS_BEFORE_LEVEL5
    ratio_ok = (
        (level5_answered + 1) / (questions_answered + 1)
        <= MAX_LEVEL5_SESSION_RATIO
    )

    return (early_level5 or normal_level5) and ratio_ok


def score_question(
    question,
    target_difficulty,
    current_skill,
    recent_questions,
    recent_words,
    recent_standards,
    recent_skills,
    recent_groups,
    last_word,
    word_bank_metadata,
    session_stats,
):
    score = 0
    difficulty = question.get("difficulty", 1)
    difficulty_gap = abs(difficulty - target_difficulty)

    # Prefer target difficulty.
    if difficulty == target_difficulty:
        score += 5
    elif difficulty_gap == 1:
        score += 2
    elif difficulty > target_difficulty:
        score -= 4 * (difficulty - target_difficulty)
    else:
        score -= target_difficulty - difficulty

    # Prefer current focus skill.
    if question.get("skill") == current_skill or question.get("standard") == current_skill:
        score += 3

    # Unlock SS earlier after vocabulary success.
    if question.get("standard") == "SS":
        if session_stats.get("wm_correct", 0) >= EARLY_SS_WM_CORRECT:
            score += 3
        else:
            score -= 4

    # Penalize recently used questions.
    if get_question_id(question) in recent_questions:
        score -= 5

    # Penalize same word repetition.
    if question.get("word") == last_word:
        score -= 3

    recent_window = recent_words[-RECENT_WORD_WINDOW:]
    if recent_window.count(question.get("word")) >= MAX_SAME_WORD_RECENT:
        score -= 100

    # Rotate across groups and skills.
    question_group = get_question_group(question, word_bank_metadata)
    if recent_groups and question_group == recent_groups[-1]:
        score -= 2
    if recent_standards and question.get("standard") == recent_standards[-1]:
        score -= 2
    if recent_skills and question.get("skill") == recent_skills[-1]:
        score -= 2

    return score


def select_question_by_score(
    questions,
    progress,
    session_stats,
    recent_questions,
    recent_words,
    recent_standards,
    recent_skills,
    recent_groups,
    last_word,
    word_bank_metadata,
):
    target_difficulty = get_target_difficulty(progress, session_stats)
    current_skill = get_current_focus_skill(progress)

    candidates = [
        question
        for question in questions
        if level5_allowed(question, session_stats)
        and question.get("skill") == current_skill
    ]

    strict_word_candidates = [
        question
        for question in candidates
        if recent_words[-RECENT_WORD_WINDOW:].count(question.get("word")) < MAX_SAME_WORD_RECENT
    ]
    if strict_word_candidates:
        candidates = strict_word_candidates

    if not candidates:
        return None, target_difficulty, current_skill

    scored = [
        (
            score_question(
                question,
                target_difficulty,
                current_skill,
                recent_questions,
                recent_words,
                recent_standards,
                recent_skills,
                recent_groups,
                last_word,
                word_bank_metadata,
                session_stats,
            ),
            -recent_questions.count(get_question_id(question)),
            -recent_words.count(question.get("word")),
            question.get("difficulty", 1),
            question.get("question", ""),
            question,
        )
        for question in candidates
    ]
    scored.sort(reverse=True, key=lambda item: item[:-1])
    return scored[0][-1], target_difficulty, current_skill


def get_standard_weight(standard, progress, recent_standards):
    standards = progress["standards"]
    weight = TARGET_STANDARD_WEIGHTS.get(standard, 0)

    if weight == 0:
        return 0

    score = standards.get(standard, 0)

    if score < 40:
        weight *= 1.7
    elif score < 60:
        weight *= 1.35
    elif score >= 85:
        weight *= 0.55

    if standards.get("WM", 0) < 60 and standard != "WM":
        weight *= 0.35

    if standard == "SS":
        if standards.get("PS", 0) < 60 or standards.get("PR", 0) < 60:
            return 0
        if score < 50:
            weight *= 0.45
        if len(recent_standards) >= MAX_SS_IN_A_ROW and all(
            item == "SS" for item in recent_standards[-MAX_SS_IN_A_ROW:]
        ):
            return 0

    if standard == "PS" and standards.get("SS", 0) < 50:
        weight *= 1.2

    if standard == "PR" and standards.get("SS", 0) < 50:
        weight *= 1.2

    return weight


def choose_standard(question_pool, progress, recent_standards):
    available_standards = sorted({q["standard"] for q in question_pool})
    weighted_standards = []
    weights = []

    for standard in available_standards:
        weight = get_standard_weight(standard, progress, recent_standards)
        if weight > 0:
            weighted_standards.append(standard)
            weights.append(weight)

    if not weighted_standards:
        return random.choice(available_standards)

    return random.choices(weighted_standards, weights=weights, k=1)[0]


def choose_word(progress, available_words, last_word=None):
    sorted_words = sorted(
        [(word, score) for word, score in progress["words"].items() if word in available_words],
        key=lambda x: x[1],
    )

    low_words = [word for word, score in sorted_words if score < 50]
    mid_words = [word for word, score in sorted_words if 50 <= score <= 79]
    high_words = [word for word, score in sorted_words if score >= 80]

    groups = [
        (low_words, 0.6),
        (mid_words, 0.3),
        (high_words, 0.1),
    ]

    available_groups = [(words, weight) for words, weight in groups if words]
    available_words = [word for words, _ in available_groups for word in words]

    if last_word is not None and len(available_words) > 1:
        available_groups = [
            ([word for word in words if word != last_word], weight)
            for words, weight in available_groups
        ]
        available_groups = [(words, weight) for words, weight in available_groups if words]

    group_choices = [words for words, _ in available_groups]
    group_weights = [weight for _, weight in available_groups]
    selected_group = random.choices(group_choices, weights=group_weights, k=1)[0]

    return random.choice(selected_group)


def filter_questions_for_test_mode(
    questions,
    standard=None,
    min_difficulty=None,
    max_difficulty=None,
):
    filtered_questions = questions

    if standard is not None:
        filtered_questions = [
            question for question in filtered_questions if question["standard"] == standard
        ]

    if min_difficulty is not None:
        filtered_questions = [
            question
            for question in filtered_questions
            if question["difficulty"] >= min_difficulty
        ]

    if max_difficulty is not None:
        filtered_questions = [
            question
            for question in filtered_questions
            if question["difficulty"] <= max_difficulty
        ]

    return filtered_questions


def load_pasuk_flow(source=None, pasuk=None):
    flows = []
    for filename in [LEGACY_PASUK_FLOW_PREVIEW_PATH, LEGACY_PASUK_FLOWS_PATH]:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            continue
        flows.extend(data.get("flows", []))

    if not flows:
        return None

    if source is None and pasuk is None:
        return flows[0]

    for flow in flows:
        if pasuk is not None and flow.get("pasuk") == pasuk:
            return flow
        if source is not None and flow.get("source") == source:
            return flow

    return None


def get_pasuk_flow(source=None, pasuk=None):
    if pasuk is not None and generate_pasuk_flow is not None:
        try:
            flow = generate_pasuk_flow(pasuk)
            flow["source"] = "generated live"
            return flow
        except Exception as error:
            print(
                "\nCould not generate that pasuk live. "
                f"Falling back to saved flows. Reason: {error}"
            )

    return load_pasuk_flow(source, pasuk)


def ask_question(question, progress):
    selected_word = question["word"]
    selected_standard = question["standard"]
    selected_micro_standard = question["micro_standard"]

    progress["words"].setdefault(selected_word, 0)
    progress["standards"].setdefault(selected_standard, 0)
    progress["micro_standards"].setdefault(selected_micro_standard, 0)

    print_question_debug(question, word_bank_metadata)
    print(f"\nStandard: {selected_standard}")
    print(f"Micro-standard: {selected_micro_standard}")
    print(f"Difficulty: {question['difficulty']}")
    print("\nQuestion:")
    print(display_text(question["question"]))

    for i, choice in enumerate(question["choices"], 1):
        print(f"{i}. {display_text(choice)}")

    user_input = input("\nEnter your answer (1-4) or 'q' to quit: ")

    if user_input.lower() == "q":
        return False

    try:
        selected = question["choices"][int(user_input) - 1]
    except:
        print("Invalid input.")
        return True

    if selected == question["correct_answer"]:
        print("\nCorrect!")
        progress["words"][selected_word] += 10
        progress["standards"][selected_standard] += 10
        progress["micro_standards"][selected_micro_standard] += 10
    else:
        print("\nIncorrect.")
        print(f"Correct answer: {display_text(question['correct_answer'])}")
        progress["words"][selected_word] -= 10
        progress["standards"][selected_standard] -= 10
        progress["micro_standards"][selected_micro_standard] -= 10

    skill = question.get("skill", selected_standard)
    is_correct = selected == question["correct_answer"]
    skill_state = update_skill_progress(
        skill,
        is_correct,
        None if is_correct else get_error_type(skill),
    )
    if skill == progress.get("current_skill") and skill_state["mastered"]:
        progress["current_skill"] = get_next_skill(skill)
        print(f"Skill mastered: {skill}")
        print(f"Next skill unlocked: {progress['current_skill']}")
    elif check_mastery(skill):
        print(f"Skill mastered: {skill}")

    progress["words"][selected_word] = max(0, min(100, progress["words"][selected_word]))
    progress["standards"][selected_standard] = max(0, min(100, progress["standards"][selected_standard]))
    progress["micro_standards"][selected_micro_standard] = max(
        0, min(100, progress["micro_standards"][selected_micro_standard])
    )

    print(f"Explanation: {display_text(question['explanation'])}")
    return True


def run_pasuk_flow(progress, source=None, pasuk=None, flow=None):
    def skill_name(standard):
        names = {
            "WM": "understanding words",
            "PR": "how words are built",
            "PS": "how words work together",
            "SS": "who is doing what",
            "CM": "meaning from context",
            "CF": "how the sentence works",
            "PC": "reading short phrases",
            "SR": "finding the root",
        }
        return names.get(standard, standard)

    def update_flow_progress(question, is_correct):
        selected_word = question["word"]
        selected_standard = question["standard"]
        selected_micro_standard = question["micro_standard"]
        amount = 10 if is_correct else -10

        progress["words"].setdefault(selected_word, 0)
        progress["standards"].setdefault(selected_standard, 0)
        progress["micro_standards"].setdefault(selected_micro_standard, 0)

        progress["words"][selected_word] += amount
        progress["standards"][selected_standard] += amount
        progress["micro_standards"][selected_micro_standard] += amount

        progress["words"][selected_word] = max(0, min(100, progress["words"][selected_word]))
        progress["standards"][selected_standard] = max(0, min(100, progress["standards"][selected_standard]))
        progress["micro_standards"][selected_micro_standard] = max(
            0, min(100, progress["micro_standards"][selected_micro_standard])
        )

    def ask_flow_question(question, label="Question"):
        selected_standard = question["standard"]
        selected_micro_standard = question["micro_standard"]

        print_question_debug(question, word_bank_metadata)
        print(f"\n{label}")
        print(f"Focus: {skill_name(selected_standard)}")
        print(f"Skill step: {selected_micro_standard}")
        print(f"Difficulty: {question['difficulty']}")
        print("\nQuestion:")
        print(display_text(question["question"]))

        for i, choice in enumerate(question["choices"], 1):
            print(f"{i}. {display_text(choice)}")

        user_input = input("\nEnter your answer (1-4) or 'q' to quit: ")
        if user_input.lower() == "q":
            return False, None

        try:
            selected = question["choices"][int(user_input) - 1]
        except:
            print("Invalid input.")
            return True, None

        is_correct = selected == question["correct_answer"]
        if is_correct:
            print("\nCorrect.")
            print(f"Clue used: {display_text(question['explanation'])}")
        else:
            print("\nNot quite.")
            print(f"Correct answer: {display_text(question['correct_answer'])}")
            print(f"Explanation: {display_text(question['explanation'])}")

        update_flow_progress(question, is_correct)
        return True, is_correct

    def build_follow_up(question):
        return {
            "skill": question["skill"],
            "standard": question["standard"],
            "micro_standard": question["micro_standard"],
            "question_type": question.get("question_type", "follow_up"),
            "word": question["word"],
            "selected_word": question.get("selected_word", question["word"]),
            "question": (
                "Follow-up: which answer best matches the clue from the last question?"
            ),
            "choices": question["choices"],
            "correct_answer": question["correct_answer"],
            "explanation": (
                "This review uses the same clue in a simpler way: "
                + question["explanation"]
            ),
            "difficulty": max(1, question.get("difficulty", 1) - 1),
        }

    if flow is None:
        flow = get_pasuk_flow(source, pasuk)
    if flow is None:
        print("\nNo pasuk flow found for that source or pasuk.")
        return

    print(f"\nPasuk Flow: {display_text(flow['pasuk'])}")
    print(f"Source: {display_text(flow.get('source', 'unknown'))}")

    flow_stats = {}
    challenge_adjustment = 0
    steps = flow.get("questions") or flow.get("steps", [])
    for index, step in enumerate(steps, 1):
        step_number = step.get("step", index)
        print(f"\nStep {step_number}: {step['standard']} / {step['micro_standard']}")
        should_continue, is_correct = ask_flow_question(step)
        if not should_continue:
            break

        standard = step["standard"]
        flow_stats.setdefault(standard, {"correct": 0, "incorrect": 0})
        if is_correct is True:
            flow_stats[standard]["correct"] += 1
            challenge_adjustment += 1
            print("Nice. The next step can stretch a little more.")
        elif is_correct is False:
            flow_stats[standard]["incorrect"] += 1
            challenge_adjustment = max(0, challenge_adjustment - 1)
            print("\nLet's reinforce that before moving on.")
            follow_up = build_follow_up(step)
            should_continue, follow_up_correct = ask_flow_question(
                follow_up,
                label="Follow-up practice",
            )
            if not should_continue:
                break
            if follow_up_correct is True:
                flow_stats[standard]["correct"] += 1
            elif follow_up_correct is False:
                flow_stats[standard]["incorrect"] += 1

    if flow_stats:
        print("\nFlow Summary")
        strengths = [
            skill_name(standard)
            for standard, stats in flow_stats.items()
            if stats["correct"] >= stats["incorrect"]
        ]
        weak_areas = [
            skill_name(standard)
            for standard, stats in flow_stats.items()
            if stats["incorrect"] > stats["correct"]
        ]

        if strengths:
            print("Strengths: " + ", ".join(strengths))
        else:
            print("Strengths: still building")

        if weak_areas:
            print("Needs more practice: " + ", ".join(weak_areas))
        else:
            print("Needs more practice: nothing stood out in this flow")


# Load questions
args = parse_args()
word_bank_metadata = load_word_bank_metadata()

with open(LEGACY_QUESTIONS_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)

questions = data["questions"]

# Load progress
try:
    with open("progress.json", "r", encoding="utf-8") as file:
        progress = json.load(file)
except FileNotFoundError:
    progress = {"words": {}, "standards": {}}

progress.setdefault("words", {})
progress.setdefault("standards", {})
progress.setdefault("micro_standards", {})
progress.setdefault("current_skill", SKILL_ORDER[0])

for question_data in questions:
    progress["words"].setdefault(question_data["word"], 0)
    progress["micro_standards"].setdefault(question_data["micro_standard"], 0)

for micro_standard in PS_MICRO_STANDARDS:
    progress["micro_standards"].setdefault(micro_standard, 0)

for micro_standard in SS_MICRO_STANDARDS:
    progress["micro_standards"].setdefault(micro_standard, 0)

for standard in STANDARDS:
    progress["standards"].setdefault(standard, 0)

if args.pasuk_flow:
    run_pasuk_flow(progress, args.source, args.pasuk)
    with open("progress.json", "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)
    sys.exit()

last_word = None
recent_standards = []
recent_words = []
recent_groups = []
recent_skills = []
recent_questions = []
session_stats = {
    "answered": 0,
    "correct": 0,
    "consecutive_correct": 0,
    "wm_correct": 0,
    "level5_answered": 0,
}

while True:
    current_skill = progress["current_skill"]

    # =========================
    # 🔧 PASUK-BASED GENERATION
    # =========================
    if args.pasuk and not args.pasuk_flow and generate_skill_question is not None:
        try:
            valid_question = None

            # Initialize tracking
            progress.setdefault("recent_features", [])
            progress.setdefault("recent_prefix_values", [])
            progress.setdefault("recent_suffix_values", [])

            for _ in range(10):
                q = generate_skill_question(current_skill, args.pasuk)
                feature = q.get("skill")

                # 🔴 PREFIX CONTROL
                if feature == "prefix":
                    prefix_value = q.get("prefix") or q.get("target_prefix")

                    if prefix_value and progress["recent_prefix_values"].count(prefix_value) >= 2:
                        continue

                    if progress["recent_features"][-5:].count("prefix") >= 2:
                        continue

                # 🔴 SUFFIX CONTROL
                if feature == "suffix":
                    suffix_value = q.get("suffix") or q.get("target_suffix")

                    if suffix_value and progress["recent_suffix_values"].count(suffix_value) >= 2:
                        continue

                    if progress["recent_features"][-5:].count("suffix") >= 2:
                        continue

                # ✅ ACCEPT
                valid_question = q
                break

            if not valid_question:
                valid_question = q

            questions = [valid_question]

            # 🔵 TRACK
            feature = valid_question.get("skill")

            progress["recent_features"].append(feature)
            progress["recent_features"] = progress["recent_features"][-10:]

            if feature == "prefix":
                prefix_value = valid_question.get("prefix") or valid_question.get("target_prefix")
                if prefix_value:
                    progress["recent_prefix_values"].append(prefix_value)
                    progress["recent_prefix_values"] = progress["recent_prefix_values"][-10:]

            if feature == "suffix":
                suffix_value = valid_question.get("suffix") or valid_question.get("target_suffix")
                if suffix_value:
                    progress["recent_suffix_values"].append(suffix_value)
                    progress["recent_suffix_values"] = progress["recent_suffix_values"][-10:]

        except Exception as error:
            print(f"\nCould not generate a question for skill '{current_skill}': {error}")
            break

    # =========================
    # 🧪 TEST MODE
    # =========================
    if args.test:
        max_difficulty = "test"
        allowed_questions = filter_questions_for_test_mode(
            questions,
            standard=args.standard,
            min_difficulty=args.min_difficulty,
            max_difficulty=args.max_difficulty,
        )
        allowed_questions = [
            question
            for question in allowed_questions
            if question.get("skill") == current_skill
        ]
    else:
        max_difficulty = get_max_difficulty(progress, session_stats)
        allowed_questions = questions

    if not allowed_questions:
        print("\nNo questions match the current filters.")
        break

    # =========================
    # 🎯 QUESTION SELECTION
    # =========================
    if args.test:
        question = random.choice(allowed_questions)
        target_difficulty = "test"
    else:
        question, target_difficulty, current_skill = select_question_by_score(
            questions,
            progress,
            session_stats,
            recent_questions,
            recent_words,
            recent_standards,
            recent_skills,
            recent_groups,
            last_word,
            word_bank_metadata,
        )

        if question is None:
            print("\nNo questions match the current filters.")
            break

    selected_word = question["word"]
    selected_standard = question["standard"]
    selected_micro_standard = question["micro_standard"]

    print(f"\nWord focus: {display_text(selected_word)}")
    print(f"Skill: {current_skill}")
    print(f"Difficulty: {question['difficulty']}")
    print("\nQuestion:")
    print(display_text(question["question"]))

    for i, choice in enumerate(question["choices"], 1):
        print(f"{i}. {display_text(choice)}")

    user_input = input("\nEnter your answer (1-4) or 'q' to quit: ")

    if user_input.lower() == "q":
        break

    try:
        selected = question["choices"][int(user_input) - 1]
    except:
        print("Invalid input.")
        continue

    is_correct = selected == question["correct_answer"]

    if is_correct:
        print("\nCorrect!")
        progress["words"][selected_word] += 10
        progress["standards"][selected_standard] += 10
        progress["micro_standards"][selected_micro_standard] += 10
    else:
        print("\nIncorrect.")
        print(f"Correct answer: {display_text(question['correct_answer'])}")
        progress["words"][selected_word] -= 10
        progress["standards"][selected_standard] -= 10
        progress["micro_standards"][selected_micro_standard] -= 10

    session_stats["answered"] += 1
    if is_correct:
        session_stats["correct"] += 1
        session_stats["consecutive_correct"] += 1
    else:
        session_stats["consecutive_correct"] = 0

    print(f"Explanation: {display_text(question['explanation'])}")
# Save progress AFTER loop ends
with open("progress.json", "w", encoding="utf-8") as f:
    json.dump(progress, f, indent=2, ensure_ascii=False)
