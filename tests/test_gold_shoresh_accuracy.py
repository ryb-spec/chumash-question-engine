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
        {"word": "יבדיל", "shoresh": "בדל"},
        {"word": "תראה", "shoresh": "ראה"},
        {"word": "תאיר", "shoresh": "אור"},
        {"word": "יוציא", "shoresh": "יצא"},
        {"word": "תוציא", "shoresh": "יצא"},
        {"word": "תהיה", "shoresh": "היה"},
        {"word": "תתן", "shoresh": "נתן"},
        {"word": "תבדיל", "shoresh": "בדל"},
        {"word": "תוציאו", "shoresh": "יצא"},
        {"word": "יראו", "shoresh": "ראה"},
        {"word": "יתנו", "shoresh": "נתן"},
        {"word": "תבדילו", "shoresh": "בדל"},
        {"word": "יוציאם", "shoresh": "יצא"},
        {"word": "תצא", "shoresh": "יצא"},
        {"word": "יצאו", "shoresh": "יצא"},
        {"word": "תאמר", "shoresh": "אמר"},
        {"word": "יאמרו", "shoresh": "אמר"},
        {"word": "תתנו", "shoresh": "נתן"},
        {"word": "יבדילו", "shoresh": "בדל"},
        {"word": "תבדל", "shoresh": "בדל"},
        {"word": "יאמר", "shoresh": "אמר"},
        {"word": "תאמרו", "shoresh": "אמר"},
        {"word": "תצאו", "shoresh": "יצא"},
        {"word": "יבדל", "shoresh": "בדל"},
        {"word": "תבדילו", "shoresh": "בדל"},
        # common Bereishis root relatives
        {"word": "תקרא", "shoresh": "קרא"},
        {"word": "יקראו", "shoresh": "קרא"},
        {"word": "יבדלו", "shoresh": "בדל"},
        {"word": "תקראו", "shoresh": "קרא"},
        # future / imperfect plural-style variants
        {"word": "תאמרנה", "shoresh": "אמר"},
        {"word": "תראינה", "shoresh": "ראה"},
        {"word": "תצאנה", "shoresh": "יצא"},
        {"word": "תהיינה", "shoresh": "היה"},
        # future / imperfect feminine-singular drill forms
        {"word": "תאמרי", "shoresh": "אמר"},
        {"word": "תראי", "shoresh": "ראה"},
        {"word": "תצאי", "shoresh": "יצא"},
        {"word": "תהיי", "shoresh": "היה"},
        {"word": "תקראי", "shoresh": "קרא"},
        {"word": "תתני", "shoresh": "נתן"},
        # common Bereishis root relatives
        {"word": "ויאמרו", "shoresh": "אמר"},
        {"word": "ויראו", "shoresh": "ראה"},
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
        {"word": "מאור", "shoresh": "מאור"},
        {"word": "מקום", "shoresh": "מקום"},
        {"word": "ממשלה", "shoresh": "ממשלה"},
        {"word": "מועד", "shoresh": "מועד"},
        {"word": "מבול", "shoresh": "מבול"},
        {"word": "מאכל", "shoresh": "מאכל"},
        {"word": "מראות", "shoresh": "מראות"},
        {"word": "מאכלים", "shoresh": "מאכלים"},
        {"word": "מוצא", "shoresh": "מוצא"},
        {"word": "מבוא", "shoresh": "מבוא"},
        {"word": "מעמד", "shoresh": "מעמד"},
        {"word": "מלאך", "shoresh": "מלאך"},
        {"word": "מאמר", "shoresh": "מאמר"},
        {"word": "מזבח", "shoresh": "מזבח"},
        {"word": "מחנה", "shoresh": "מחנה"},
        {"word": "מראה", "shoresh": "מראה"},
        {"word": "מנורה", "shoresh": "מנורה"},
        {"word": "מקנה", "shoresh": "מקנה"},
        {"word": "מצבה", "shoresh": "מצבה"},
        {"word": "מכתב", "shoresh": "מכתב"},
        {"word": "מזל", "shoresh": "מזל"},
        # curriculum-shaped lexical nouns
        {"word": "מקוה", "shoresh": "מקוה"},
        {"word": "מקומות", "shoresh": "מקומות"},
        {"word": "מינים", "shoresh": "מינים"},
        {"word": "מראים", "shoresh": "מראים"},
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
        {"word": "להבדיל", "shoresh": "בדל"},
        {"word": "יוציאו", "shoresh": "יצא"},
        {"word": "תהיו", "shoresh": "היה"},
        {"word": "תראו", "shoresh": "ראה"},
        {"word": "תאירו", "shoresh": "אור"},
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
