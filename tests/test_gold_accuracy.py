from torah_parser.tokenize import tokenize_pasuk
from torah_parser.candidate_generator import generate_candidate_analyses
from torah_parser.disambiguate import select_best_candidate


def load_gold():
    return [
        # simple verbs
        {"word": "ויאמר", "shoresh": "אמר"},
        {"word": "ברא", "shoresh": "ברא"},
        {"word": "הלך", "shoresh": "הלך"},
        {"word": "נתן", "shoresh": "נתן"},
        {"word": "ראה", "shoresh": "ראה"},
        {"word": "קרא", "shoresh": "קרא"},
        # simple nouns
        {"word": "מים", "shoresh": "מים"},
        {"word": "ארץ", "shoresh": "ארץ"},
        {"word": "אור", "shoresh": "אור"},
        {"word": "יום", "shoresh": "יום"},
        {"word": "לילה", "shoresh": "לילה"},
        # prefixed forms
        {"word": "והארץ", "shoresh": "ארץ"},
        {"word": "לאור", "shoresh": "אור"},
        {"word": "במים", "shoresh": "מים"},
        {"word": "לרקיע", "shoresh": "רקיע"},
        {"word": "למינו", "shoresh": "מין"},
        # known-risk forms
        {"word": "ויהי", "shoresh": "היה"},
        {"word": "וירא", "shoresh": "ראה"},
        {"word": "ויקרא", "shoresh": "קרא"},
        {"word": "ותראה", "shoresh": "ראה"},
    ]


def extract_shoresh(word):
    tokens = tokenize_pasuk(word)
    if not tokens:
        return None

    candidates = generate_candidate_analyses(tokens[0])
    if not candidates:
        return None

    best = select_best_candidate(candidates)
    if not best:
        return None

    return best.get("shoresh")


def test_gold_shoresh_accuracy():
    failures = []

    for item in load_gold():
        word = item["word"]
        expected = item["shoresh"]
        actual = extract_shoresh(word)

        if actual != expected:
            failures.append(f"{word}: expected {expected}, got {actual}")

    assert not failures, "\n".join(failures)
