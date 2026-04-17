from torah_parser.tokenize import tokenize_pasuk
from torah_parser.candidate_generator import generate_candidate_analyses
from torah_parser.disambiguate import select_best_candidate


def load_gold():
    return [
        # prefixed
        {"word": "והארץ", "shoresh": "ארץ"},
        {"word": "לאור", "shoresh": "אור"},
        {"word": "לרקיע", "shoresh": "רקיע"},
        {"word": "כמלאך", "shoresh": "מלאך"},
        {"word": "כאור", "shoresh": "אור"},
        {"word": "מהארץ", "shoresh": "ארץ"},
        {"word": "ממלך", "shoresh": "מלך"},
        {"word": "לשמים", "shoresh": "שמים"},
        {"word": "בשמים", "shoresh": "שמים"},
        {"word": "והמים", "shoresh": "מים"},
        {"word": "למים", "shoresh": "מים"},
        {"word": "מפרי", "shoresh": "פרי"},
        {"word": "לימים", "shoresh": "ימים"},
        {"word": "לזרע", "shoresh": "זרע"},
        {"word": "לדשא", "shoresh": "דשא"},
        {"word": "כדשא", "shoresh": "דשא"},
        {"word": "למאורות", "shoresh": "מאורות"},
        {"word": "ברקיע", "shoresh": "רקיע"},
        {"word": "ולמועדים", "shoresh": "מועדים"},
        {"word": "ולימים", "shoresh": "ימים"},
        {"word": "ושנים", "shoresh": "שנים"},
        {"word": "והמאורות", "shoresh": "מאורות"},
        {"word": "ובמאורות", "shoresh": "מאורות"},
        {"word": "ולכוכבים", "shoresh": "כוכבים"},
        {"word": "בכוכבים", "shoresh": "כוכבים"},
        # repeated trouble words and related noun forms
        {"word": "לאותות", "shoresh": "אותות"},
        {"word": "לכוכבים", "shoresh": "כוכבים"},
        {"word": "מהכוכבים", "shoresh": "כוכבים"},
        {"word": "במועדים", "shoresh": "מועדים"},
        {"word": "לזרעים", "shoresh": "זרעים"},
        {"word": "ובמועדים", "shoresh": "מועדים"},
        {"word": "ולאותות", "shoresh": "אותות"},
        {"word": "ולמאור", "shoresh": "מאור"},
        {"word": "ובמקום", "shoresh": "מקום"},
        # prefix+suffix
        {"word": "במים", "shoresh": "מים"},
        {"word": "למינו", "shoresh": "מין"},
        {"word": "במינו", "shoresh": "מין"},
        {"word": "כמינו", "shoresh": "מין"},
        {"word": "ממים", "shoresh": "מים"},
        {"word": "מימי", "shoresh": "מים"},
        {"word": "מימיו", "shoresh": "מים"},
        {"word": "זרעו", "shoresh": "זרע"},
        {"word": "לזרעו", "shoresh": "זרע"},
        {"word": "למינהו", "shoresh": "מין"},
        {"word": "מזרעו", "shoresh": "זרע"},
        {"word": "ולמינהו", "shoresh": "מין"},
        {"word": "ובזרעו", "shoresh": "זרע"},
        {"word": "כזרעו", "shoresh": "זרע"},
        {"word": "ובמינהו", "shoresh": "מין"},
        {"word": "כמינהו", "shoresh": "מין"},
        # additional stacked prefix+suffix noun forms
        {"word": "ובמימיו", "shoresh": "מים"},
        {"word": "למימיו", "shoresh": "מים"},
        {"word": "כמימיו", "shoresh": "מים"},
        {"word": "ולמאורות", "shoresh": "מאורות"},
        {"word": "ולזרעו", "shoresh": "זרע"},
        {"word": "ובמועדהו", "shoresh": "מועד"},
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


def test_gold_affix_handling():
    failures = []

    for item in load_gold():
        word = item["word"]
        expected = item["shoresh"]
        actual = extract_shoresh(word)

        if actual != expected:
            failures.append(f"{word}: expected {expected}, got {actual}")

    assert not failures, "\n".join(failures)
