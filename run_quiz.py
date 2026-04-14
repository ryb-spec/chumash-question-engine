import argparse
import json
import random
import re
import sys

STANDARDS = ["WM", "SR", "PR", "CF", "PC", "PS", "SS", "CM"]
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
    for filename in ["pasuk_flow_questions.json", "pasuk_flows.json"]:
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

    progress["words"][selected_word] = max(0, min(100, progress["words"][selected_word]))
    progress["standards"][selected_standard] = max(0, min(100, progress["standards"][selected_standard]))
    progress["micro_standards"][selected_micro_standard] = max(
        0, min(100, progress["micro_standards"][selected_micro_standard])
    )

    print(f"Explanation: {display_text(question['explanation'])}")
    return True


def run_pasuk_flow(progress, source=None, pasuk=None):
    flow = load_pasuk_flow(source, pasuk)
    if flow is None:
        print("\nNo pasuk flow found for that source or pasuk.")
        return

    print(f"\nPasuk Flow: {display_text(flow['pasuk'])}")
    print(f"Source: {display_text(flow.get('source', 'unknown'))}")

    steps = flow.get("questions") or flow.get("steps", [])
    for index, step in enumerate(steps, 1):
        step_number = step.get("step", index)
        print(f"\nStep {step_number}: {step['standard']} / {step['micro_standard']}")
        if not ask_question(step, progress):
            break


# Load questions
args = parse_args()
word_bank_metadata = load_word_bank_metadata()

with open("questions.json", "r", encoding="utf-8") as file:
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
session_stats = {
    "answered": 0,
    "correct": 0,
    "consecutive_correct": 0,
    "wm_correct": 0,
    "level5_answered": 0,
}

while True:
    if args.test:
        max_difficulty = "test"
        allowed_questions = filter_questions_for_test_mode(
            questions,
            standard=args.standard,
            min_difficulty=args.min_difficulty,
            max_difficulty=args.max_difficulty,
        )
    else:
        max_difficulty = get_max_difficulty(progress, session_stats)
        allowed_questions = filter_questions_by_progression(
            questions,
            progress,
            max_difficulty,
            session_stats,
        )
        allowed_questions = filter_questions_by_session_limits(allowed_questions, session_stats)

        challenge_allowed_questions = filter_questions_by_progression(
            questions,
            progress,
            min(5, max_difficulty + 1),
            session_stats,
        )
        challenge_allowed_questions = filter_questions_by_session_limits(
            challenge_allowed_questions,
            session_stats,
        )
        challenge_pool = select_challenge_pool(
            challenge_allowed_questions,
            max_difficulty,
            session_stats,
        )
        if challenge_pool:
            allowed_questions = challenge_pool

    if not allowed_questions:
        print("\nNo questions match the current filters.")
        break

    selected_pool_standard = None
    if args.test:
        question_pool = allowed_questions
    else:
        selected_pool_standard = choose_standard(allowed_questions, progress, recent_standards)
        question_pool = [
            q for q in allowed_questions if q["standard"] == selected_pool_standard
        ]
        question_pool = filter_recent_word_repetition(question_pool, recent_words)
        question_pool = filter_recent_group_and_skill(
            question_pool,
            recent_groups,
            recent_skills,
            word_bank_metadata,
        )

    available_words = {q["word"] for q in question_pool}

    # Pick word using weighted randomness
    selected_word = choose_word(progress, available_words, last_word)

    # Get question
    filtered_questions = [q for q in question_pool if q["word"] == selected_word]
    question = random.choice(filtered_questions)
    selected_standard = question["standard"]
    selected_micro_standard = question["micro_standard"]

    print(f"\nWord focus: {display_text(selected_word)} (Score: {progress['words'][selected_word]})")
    print(f"Standard focus: {selected_standard} (Score: {progress['standards'][selected_standard]})")
    print(f"Micro-standard focus: {selected_micro_standard} (Score: {progress['micro_standards'][selected_micro_standard]})")
    if args.test:
        print("Mode: test")
        if args.standard:
            print(f"Test standard: {args.standard}")
        if args.min_difficulty:
            print(f"Test minimum difficulty: {args.min_difficulty}")
        if args.max_difficulty:
            print(f"Test maximum difficulty: {args.max_difficulty}")
    else:
        print(f"Max difficulty unlocked: {max_difficulty}")
        print(f"PS levels unlocked: {', '.join(get_allowed_ps_micro_standards(progress))}")
        ss_levels = get_allowed_ss_micro_standards(progress, session_stats)
        print(f"SS levels unlocked: {', '.join(ss_levels) if ss_levels else 'locked'}")
        print(
            "Session accuracy: "
            f"{session_stats['correct']}/{session_stats['answered']} "
            f"({get_session_accuracy(session_stats) * 100:.0f}%)"
        )
        print(f"Correct streak: {session_stats['consecutive_correct']}")
        print(f"WM correct this session: {session_stats['wm_correct']}")
        if session_stats["consecutive_correct"] >= CHALLENGE_STREAK:
            print("Challenge spike: active")
        print(
            "Level 5 session use: "
            f"{session_stats['level5_answered']}/{session_stats['answered']} "
            f"(normal unlock after {MIN_QUESTIONS_BEFORE_LEVEL5} answered; early unlock after "
            f"{EARLY_LEVEL5_CORRECT} correct at 80%; max 20%)"
        )
    print_question_debug(question, word_bank_metadata)
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
        if selected_standard == "WM":
            session_stats["wm_correct"] += 1
    else:
        session_stats["consecutive_correct"] = 0

    if question.get("difficulty") == 5:
        session_stats["level5_answered"] += 1

    # Keep score between 0-100
    progress["words"][selected_word] = max(0, min(100, progress["words"][selected_word]))
    progress["standards"][selected_standard] = max(0, min(100, progress["standards"][selected_standard]))
    progress["micro_standards"][selected_micro_standard] = max(
        0, min(100, progress["micro_standards"][selected_micro_standard])
    )
    last_word = selected_word
    recent_standards.append(selected_standard)
    recent_standards = recent_standards[-3:]
    recent_words.append(selected_word)
    recent_words = recent_words[-RECENT_WORD_WINDOW:]
    recent_groups.append(get_question_group(question, word_bank_metadata))
    recent_groups = recent_groups[-5:]
    recent_skills.append(question.get("skill", "unknown"))
    recent_skills = recent_skills[-5:]

    print(f"\nNew Score for {display_text(selected_word)}: {progress['words'][selected_word]}")
    print(f"New Score for {selected_standard}: {progress['standards'][selected_standard]}")
    print(f"New Score for {selected_micro_standard}: {progress['micro_standards'][selected_micro_standard]}")
    print(f"Explanation: {display_text(question['explanation'])}")

# Save progress AFTER loop ends
with open("progress.json", "w", encoding="utf-8") as f:
    json.dump(progress, f, indent=2, ensure_ascii=False)
