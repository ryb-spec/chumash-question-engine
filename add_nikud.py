import json

# Hebrew words dictionary with their nikud versions
hebrew_words_with_nikud = {
    "ארץ": "אָרֶץ",
    "בית": "בַּיִת",
    "מים": "מַיִם",
    "מלך": "מֶלֶךְ",
    "יום": "יוֹם",
    "לילה": "לַיְלָה",
    "איש": "אִישׁ",
    "אשה": "אִשָּׁה",
    "בן": "בֵּן",
    "בת": "בַּת",
    "עם": "עַם",
    "עיר": "עִיר",
    "שדה": "שָׂדֶה",
    "הר": "הַר",
    "ים": "יָם",
    "עץ": "עֵץ",
    "אכל": "אָכַל",
    "הלך": "הָלַךְ",
    "ראה": "רָאָה",
    "אמר": "אָמַר",
    "שמע": "שָׁמַע",
    "נתן": "נָתַן",
    "גבר": "גִּבּוֹר",
    "דבר": "דָּבָר",
    "עשה": "עָשָׂה",
}

# Load questions
with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update all questions with nikud
for question in data.get('questions', []):
    word = question.get('word', '')
    if word in hebrew_words_with_nikud:
        question['word_with_nikud'] = hebrew_words_with_nikud[word]
    else:
        question['word_with_nikud'] = word

# Save updated questions
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Updated {len(data.get('questions', []))} questions with nikud!")
print(f"Added nikud for {len(hebrew_words_with_nikud)} unique words")
