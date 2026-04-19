"""Shared engine constants and metadata."""

from assessment_scope import (
    ACTIVE_ASSESSMENT_SCOPE,
    ACTIVE_WORD_BANK_PATH,
    LEGACY_PASUK_FLOW_PREVIEW_PATH,
    active_pasuk_texts,
    data_path,
    repo_path,
    resolve_repo_path,
)
from skill_catalog import (
    resolve_skill_id,
    skill_difficulty_tier,
    skill_ids_in_runtime_order,
    skill_micro_standard,
    skill_standard,
)

WORD_BANK_PATH = ACTIVE_WORD_BANK_PATH
OUTPUT_PATH = LEGACY_PASUK_FLOW_PREVIEW_PATH
LETTER_MEANING_QUESTIONS_PATH = data_path("skills", "letter_meaning", "questions_walder.json")
WORD_STRUCTURE_QUESTIONS_PATH = data_path("skills", "word_structure", "questions.json")

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
    "בְּרֵאשִׁית בָּרָא אֱלֹקִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ",
    "וְהָאָרֶץ הָיְתָה תֹהוּ וָבֹהוּ וְחֹשֶׁךְ עַל פְּנֵי תְהוֹם",
    "וַיֹּאמֶר אֱלֹקִים יְהִי אוֹר וַיְהִי אוֹר",
    "וַיַּרְא אֱלֹקִים אֶת הָאוֹר כִּי טוֹב",
    "וַיִּקְרָא אֱלֹקִים לָאוֹר יוֹם וְלַחֹשֶׁךְ קָרָא לָיְלָה",
    "וַיֹּאמֶר ה׳ אֶל אַבְרָם לֶךְ לְךָ מֵאַרְצְךָ",
    "וְאֶעֶשְׂךָ לְגוֹי גָּדוֹל וַאֲבָרֶכְךָ",
    "וַיֵּלֶךְ אַבְרָם כַּאֲשֶׁר דִּבֶּר אֵלָיו ה׳",
    "וַיֹּאמֶר אַבְרָם אֶל לוֹט אַל נָא תְהִי מְרִיבָה בֵּינִי וּבֵינֶךָ",
    "וַיֹּאמֶר יַעֲקֹב אֶל בָּנָיו לָמָּה תִּתְרָאוּ",
    "וַיֹּאמֶר יוֹסֵף אֶל אֶחָיו אֲנִי יוֹסֵף",
    "וַיֹּאמֶר פַּרְעֹה אֶל יוֹסֵף רְאֵה נָתַתִּי אֹתְךָ",
    "וַיֹּאמֶר ה׳ אֶל מֹשֶׁה לֶךְ אֶל פַּרְעֹה",
    "וַיֹּאמֶר מֹשֶׁה אֶל ה׳ מִי אָנֹכִי כִּי אֵלֵךְ",
    "וַיֹּאמֶר אֱלֹקִים אֶהְיֶה אֲשֶׁר אֶהְיֶה",
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
    "קוֹל דוֹדִי דוֹפֵק פִּתְחִי לִי אֲחֹתִי",
]))

CHUMASH_PESUKIM = list(active_pasuk_texts())
OTHER_PESUKIM = _ALL_PESUKIM[24:]
PESUKIM = CHUMASH_PESUKIM

TRANSLATION_LITERAL = "literal"
TRANSLATION_NATURAL = "natural"

PREFIX_MEANINGS = {
    "ו": "and",
    "ב": "in / with",
    "ל": "to / for",
    "כ": "like / as",
    "מ": "from",
    "ה": "the",
    "ש": "that / which",
}

KNOWN_PREFIXES = PREFIX_MEANINGS
CONTROLLED_TENSE_CHOICES = [
    "vav_consecutive_past",
    "future_jussive",
    "future",
    "past",
    "present",
    "infinitive",
    "command",
]

SKILLS = skill_ids_in_runtime_order()

SKILL_GROUP_ORDER = [
    "letter_meaning",
    "word_structure",
    "word_meaning",
    "sentence_structure",
    "pasuk_flow",
]

SKILL_METADATA = {
    skill_id: {
        "standard": skill_standard(skill_id),
        "micro_standard": skill_micro_standard(skill_id),
        "difficulty": skill_difficulty_tier(skill_id),
    }
    for skill_id in SKILLS
}

PREFIX_MEANING_CHOICES = {
    "ב": ["in / with", "to / for", "from", "the"],
    "ל": ["to / for", "in / with", "from", "like / as"],
    "מ": ["from", "to / for", "in / with", "the"],
    "ו": ["and", "the", "to / for", "from"],
    "כ": ["like / as", "in / with", "from", "the"],
    "ה": ["the", "and", "to / for", "from"],
    "ש": ["that / which", "and", "the", "from"],
}

SUFFIX_MEANINGS = {
    "י": "my",
    "ךָ": "your (m)",
    "ךְ": "your (f)",
    "ך": "your",
    "ו": "his",
    "ה": "her",
    "נו": "our",
    "כֶם": "your (m plural)",
    "כֶן": "your (f plural)",
    "כם": "your (m plural)",
    "כן": "your (f plural)",
    "ם": "their",
    "ן": "their",
    "יו": "his",
}
