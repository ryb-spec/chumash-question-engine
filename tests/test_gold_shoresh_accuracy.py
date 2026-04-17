from torah_parser.tokenize import tokenize_pasuk
from torah_parser.candidate_generator import generate_candidate_analyses
from torah_parser.disambiguate import select_best_candidate


def load_gold():
    return [
        # verbs
        {"word": "ויאמר", "shoresh": "אמר"},
        {"word": "ברא", "shoresh": "ברא"},
        {"word": "הלך", "shoresh": "הלך"},
        {"word": "נתן", "shoresh": "נתן"},
        {"word": "ראה", "shoresh": "ראה"},
        {"word": "קרא", "shoresh": "קרא"},
        {"word": "אמר", "shoresh": "אמר"},
        {"word": "עשה", "shoresh": "עשה"},
        {"word": "היה", "shoresh": "היה"},
        {"word": "יצא", "shoresh": "יצא"},
        {"word": "יקרא", "shoresh": "קרא"},
        {"word": "ויקראו", "shoresh": "קרא"},
        {"word": "ויעש", "shoresh": "עשה"},
        {"word": "ויתן", "shoresh": "נתן"},
        # additional verb families
        {"word": "הוציא", "shoresh": "יצא"},
        {"word": "והוציא", "shoresh": "יצא"},
        {"word": "אהיה", "shoresh": "היה"},
        {"word": "יהיה", "shoresh": "היה"},
        {"word": "ויבדל", "shoresh": "בדל"},
        {"word": "יראה", "shoresh": "ראה"},
        {"word": "יאיר", "shoresh": "אור"},
        # nouns
        {"word": "מים", "shoresh": "מים"},
        {"word": "ארץ", "shoresh": "ארץ"},
        {"word": "אור", "shoresh": "אור"},
        {"word": "יום", "shoresh": "יום"},
        {"word": "לילה", "shoresh": "לילה"},
        {"word": "שמים", "shoresh": "שמים"},
        {"word": "רקיע", "shoresh": "רקיע"},
        {"word": "זרע", "shoresh": "זרע"},
        {"word": "פרי", "shoresh": "פרי"},
        {"word": "דשא", "shoresh": "דשא"},
        {"word": "מין", "shoresh": "מין"},
        {"word": "שרץ", "shoresh": "שרץ"},
        {"word": "נפש", "shoresh": "נפש"},
        {"word": "חיה", "shoresh": "חיה"},
        # irregular lexical items
        {"word": "אותם", "shoresh": "אותם"},
        {"word": "הכוכבים", "shoresh": "כוכבים"},
        {"word": "כוכבים", "shoresh": "כוכבים"},
        {"word": "מאורות", "shoresh": "מאורות"},
        {"word": "מועדים", "shoresh": "מועדים"},
        {"word": "אותות", "shoresh": "אותות"},
        # known-risk verb forms
        {"word": "ויהי", "shoresh": "היה"},
        {"word": "וירא", "shoresh": "ראה"},
        {"word": "ויקרא", "shoresh": "קרא"},
        {"word": "ותראה", "shoresh": "ראה"},
        {"word": "תדשא", "shoresh": "דשא"},
        {"word": "ותוצא", "shoresh": "יצא"},
        # tense-sensitive forms
        {"word": "ישרצו", "shoresh": "שרץ"},
        {"word": "יעופף", "shoresh": "עוף"},
        {"word": "והיו", "shoresh": "היה"},
        {"word": "יהיו", "shoresh": "היה"},
        {"word": "להאיר", "shoresh": "אור"},
        {"word": "ולהבדיל", "shoresh": "בדל"},
        {"word": "יתן", "shoresh": "נתן"},
        {"word": "למשלת", "shoresh": "ממשלה"},
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
