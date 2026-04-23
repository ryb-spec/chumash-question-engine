"""Generate conservative candidate analyses for individual tokens."""

from copy import deepcopy

from .normalize import normalize_form, undotted_form
from .torah_rules import (
    PREFIX_TRANSLATIONS,
    PRONOMINAL_SUFFIX_TRANSLATIONS,
    apply_torah_overrides,
    common_possessive_suffix,
    detect_vav_consecutive,
)


def prefix_item(form):
    prefix_type, translation = PREFIX_TRANSLATIONS[form]
    return {"form": form, "type": prefix_type, "translation": translation}


def suffix_item(form, translation=None):
    return {
        "form": form,
        "type": "pronominal_suffix",
        "translation": translation or PRONOMINAL_SUFFIX_TRANSLATIONS.get(form, ""),
    }


def lexical_override(
    lemma,
    translation_literal,
    translation_context=None,
    *,
    part_of_speech="noun",
    shoresh=None,
    semantic_group="unknown",
    role_hint="unknown",
    entity_type="unknown",
    group=None,
    gender=None,
    number=None,
    prefixes=None,
    suffixes=None,
):
    return {
        "lemma": lemma,
        "shoresh": shoresh,
        "part_of_speech": part_of_speech,
        "translation_literal": translation_literal,
        "translation_context": translation_context or translation_literal,
        "semantic_group": semantic_group,
        "role_hint": role_hint,
        "entity_type": entity_type,
        "group": group or semantic_group,
        "gender": gender,
        "number": number,
        "prefixes": list(prefixes or []),
        "suffixes": list(suffixes or []),
        "confidence": "surface_override",
    }


VERB_OVERRIDES = {
    "ויאמר": {
        "lemma": "אמר",
        "shoresh": "אמר",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he said",
        "translation_context": "said",
    },
    "וירא": {
        "lemma": "ראה",
        "shoresh": "ראה",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he saw",
        "translation_context": "saw",
    },
    "ויקרא": {
        "lemma": "קרא",
        "shoresh": "קרא",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he called",
        "translation_context": "called",
    },
    "ויהי": {
        "lemma": "היה",
        "shoresh": "היה",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and it was",
        "translation_context": "and there was",
    },
    "ויעש": {
        "lemma": "עשה",
        "shoresh": "עשה",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he made",
        "translation_context": "made",
    },
    "ויבדל": {
        "lemma": "בדל",
        "shoresh": "בדל",
        "binyan": "hifil",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he separated",
        "translation_context": "separated",
    },
    "יקוו": {
        "lemma": "קוה",
        "shoresh": "קוה",
        "binyan": "nifal",
        "tense": "future_jussive",
        "person": "3",
        "number": "plural",
        "gender": "masculine",
        "translation_literal": "they shall gather",
        "translation_context": "let them be gathered",
    },
    "ותראה": {
        "lemma": "ראה",
        "shoresh": "ראה",
        "binyan": "nifal",
        "tense": "future_jussive",
        "person": "3",
        "number": "singular",
        "gender": "feminine",
        "translation_literal": "and it shall appear",
        "translation_context": "and let it appear",
    },
    "ותצא": {
        "lemma": "יצא",
        "shoresh": "יצא",
        "binyan": "hifil",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "feminine",
        "translation_literal": "and it brought forth",
        "translation_context": "brought forth",
    },
    "ויתן": {
        "lemma": "נתן",
        "shoresh": "נתן",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he placed",
        "translation_context": "placed",
    },
    "ויברא": {
        "lemma": "ברא",
        "shoresh": "ברא",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he created",
        "translation_context": "created",
    },
    "וישבת": {
        "lemma": "שבת",
        "shoresh": "שבת",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he rested",
        "translation_context": "rested",
    },
    "עשות": {
        "lemma": "עשה",
        "shoresh": "עשה",
        "binyan": "qal",
        "tense": "infinitive",
        "translation_literal": "to make",
        "translation_context": "to make",
    },
    "יצמח": {
        "lemma": "צמח",
        "shoresh": "צמח",
        "binyan": "qal",
        "tense": "future",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "it will sprout",
        "translation_context": "will sprout",
    },
    "וייצר": {
        "lemma": "יצר",
        "shoresh": "יצר",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he formed",
        "translation_context": "formed",
    },
    "ויטע": {
        "lemma": "נטע",
        "shoresh": "נטע",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he planted",
        "translation_context": "planted",
    },
    "יפרד": {
        "lemma": "פרד",
        "shoresh": "פרד",
        "binyan": "nifal",
        "tense": "future",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "it will separate",
        "translation_context": "will separate",
    },
    "ויצו": {
        "lemma": "צוה",
        "shoresh": "צוה",
        "binyan": "piel",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he commanded",
        "translation_context": "commanded",
    },
    "אעשה": {
        "lemma": "עשה",
        "shoresh": "עשה",
        "binyan": "qal",
        "tense": "future",
        "person": "1",
        "number": "singular",
        "translation_literal": "I will make",
        "translation_context": "I will make",
    },
    "ויקח": {
        "lemma": "לקח",
        "shoresh": "לקח",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he took",
        "translation_context": "took",
    },
    "ויבן": {
        "lemma": "בנה",
        "shoresh": "בנה",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he built",
        "translation_context": "built",
    },
    "תדשא": {
        "lemma": "דשא",
        "shoresh": "דשא",
        "binyan": "hifil",
        "tense": "future_jussive",
        "person": "3",
        "number": "singular",
        "gender": "feminine",
        "translation_literal": "it shall sprout",
        "translation_context": "let it sprout",
    },
    "ישרצו": {
        "lemma": "שרץ",
        "shoresh": "שרץ",
        "binyan": "qal",
        "tense": "future_jussive",
        "person": "3",
        "number": "plural",
        "gender": "masculine",
        "translation_literal": "they shall swarm",
        "translation_context": "let them swarm",
    },
}


SURFACE_OVERRIDES = {
    "וִיהִי": {
        "lemma": "היה",
        "shoresh": "היה",
        "binyan": "qal",
        "tense": "future_jussive",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and it shall be",
        "translation_context": "and let it be",
    },
    "וַתּוֹצֵא": {
        "lemma": "יצא",
        "shoresh": "יצא",
        "binyan": "hifil",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "feminine",
        "translation_literal": "and it brought forth",
        "translation_context": "brought forth",
    },
    "וַיִּתֵּן": {
        "lemma": "נתן",
        "shoresh": "נתן",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he placed",
        "translation_context": "placed",
    },
    "וַיִּבְרָא": {
        "lemma": "ברא",
        "shoresh": "ברא",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he created",
        "translation_context": "created",
    },
    "וַיִּשְׁבֹּת": {
        "lemma": "שבת",
        "shoresh": "שבת",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he rested",
        "translation_context": "rested",
    },
    "עֲשׂוֹת": {
        "lemma": "עשה",
        "shoresh": "עשה",
        "binyan": "qal",
        "tense": "infinitive",
        "translation_literal": "to make",
        "translation_context": "to make",
    },
    "יִצְמָח": {
        "lemma": "צמח",
        "shoresh": "צמח",
        "binyan": "qal",
        "tense": "future",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "it will sprout",
        "translation_context": "will sprout",
    },
    "וַיִּיצֶר": {
        "lemma": "יצר",
        "shoresh": "יצר",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he formed",
        "translation_context": "formed",
    },
    "וַיִּטַּע": {
        "lemma": "נטע",
        "shoresh": "נטע",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he planted",
        "translation_context": "planted",
    },
    "יִפָּרֵד": {
        "lemma": "פרד",
        "shoresh": "פרד",
        "binyan": "nifal",
        "tense": "future",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "it will separate",
        "translation_context": "will separate",
    },
    "וַיְצַו": {
        "lemma": "צוה",
        "shoresh": "צוה",
        "binyan": "piel",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he commanded",
        "translation_context": "commanded",
    },
    "אֶעֱשֶׂה": {
        "lemma": "עשה",
        "shoresh": "עשה",
        "binyan": "qal",
        "tense": "future",
        "person": "1",
        "number": "singular",
        "translation_literal": "I will make",
        "translation_context": "I will make",
    },
    "וַיִּקַּח": {
        "lemma": "לקח",
        "shoresh": "לקח",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he took",
        "translation_context": "took",
    },
    "וַיִּבֶן": {
        "lemma": "בנה",
        "shoresh": "בנה",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he built",
        "translation_context": "built",
    },
    "תַּדְשֵׁא": {
        "lemma": "דשא",
        "shoresh": "דשא",
        "binyan": "hifil",
        "tense": "future_jussive",
        "person": "3",
        "number": "singular",
        "gender": "feminine",
        "translation_literal": "it shall sprout",
        "translation_context": "let it sprout",
    },
    "יִשְׁרְצוּ": {
        "lemma": "שרץ",
        "shoresh": "שרץ",
        "binyan": "qal",
        "tense": "future_jussive",
        "person": "3",
        "number": "plural",
        "gender": "masculine",
        "translation_literal": "they shall swarm",
        "translation_context": "let them swarm",
    },
    "הָיָה": {
        "lemma": "היה",
        "shoresh": "היה",
        "binyan": "qal",
        "tense": "past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "was",
        "translation_context": "was",
    },
    "עָשָׂה": {
        "lemma": "עשה",
        "shoresh": "עשה",
        "binyan": "qal",
        "tense": "past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "made",
        "translation_context": "made",
    },
    "וַתֹּאמֶר": {
        "lemma": "אמר",
        "shoresh": "אמר",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "feminine",
        "translation_literal": "and she said",
        "translation_context": "said",
    },
    "נֹאכֵל": {
        "lemma": "אכל",
        "shoresh": "אכל",
        "binyan": "qal",
        "tense": "future",
        "person": "1",
        "number": "plural",
        "translation_literal": "we will eat",
        "translation_context": "we will eat",
    },
    "אָמַר": {
        "lemma": "אמר",
        "shoresh": "אמר",
        "binyan": "qal",
        "tense": "past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "he said",
        "translation_context": "said",
    },
    "תֹאכְלוּ": {
        "lemma": "אכל",
        "shoresh": "אכל",
        "binyan": "qal",
        "tense": "future",
        "person": "2",
        "number": "plural",
        "gender": "masculine",
        "translation_literal": "you will eat",
        "translation_context": "you will eat",
    },
    "תִגְּעוּ": {
        "lemma": "נגע",
        "shoresh": "נגע",
        "binyan": "qal",
        "tense": "future",
        "person": "2",
        "number": "plural",
        "gender": "masculine",
        "translation_literal": "you will touch",
        "translation_context": "you will touch",
    },
    "תְּמֻתוּן": {
        "lemma": "מות",
        "shoresh": "מות",
        "binyan": "qal",
        "tense": "future",
        "person": "2",
        "number": "plural",
        "gender": "masculine",
        "translation_literal": "you will die",
        "translation_context": "you will die",
    },
    "יֹדֵעַ": {
        "lemma": "ידע",
        "shoresh": "ידע",
        "binyan": "qal",
        "tense": "present",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "knowing",
        "translation_context": "knows",
    },
    "וְנִפְקְחוּ": {
        "lemma": "פקח",
        "shoresh": "פקח",
        "binyan": "nifal",
        "tense": "future",
        "person": "3",
        "number": "plural",
        "translation_literal": "and they will be opened",
        "translation_context": "and they will be opened",
    },
    "וִהְיִיתֶם": {
        "lemma": "היה",
        "shoresh": "היה",
        "binyan": "qal",
        "tense": "future",
        "person": "2",
        "number": "plural",
        "gender": "masculine",
        "translation_literal": "and you will be",
        "translation_context": "and you will be",
    },
    "מוֹת": {
        "lemma": "מות",
        "shoresh": "מות",
        "binyan": "qal",
        "tense": "infinitive",
        "person": None,
        "number": None,
        "gender": None,
        "translation_literal": "to die",
        "translation_context": "surely die",
    },
    "אֲכָלְכֶם": {
        "lemma": "אכל",
        "shoresh": "אכל",
        "binyan": "qal",
        "tense": "infinitive",
        "person": "2",
        "number": "plural",
        "gender": "masculine",
        "translation_literal": "your eating",
        "translation_context": "when you eat",
    },
    "צִוִּיתִיךָ": {
        "lemma": "צוה",
        "shoresh": "צוה",
        "binyan": "piel",
        "tense": "past",
        "person": "1",
        "number": "singular",
        "gender": None,
        "translation_literal": "I commanded you",
        "translation_context": "I commanded you",
    },
    "אֲכָל": {
        "lemma": "אכל",
        "shoresh": "אכל",
        "binyan": "qal",
        "tense": "infinitive",
        "person": None,
        "number": None,
        "gender": None,
        "translation_literal": "to eat",
        "translation_context": "eat",
    },
    "הִשִּׁיאַנִי": {
        "lemma": "השיא",
        "shoresh": None,
        "binyan": None,
        "tense": "past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "deceived me",
        "translation_context": "deceived me",
    },
    "יְשׁוּפְךָ": {
        "lemma": "ישוף",
        "shoresh": None,
        "binyan": None,
        "tense": "future",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "he will bruise you",
        "translation_context": "he will bruise you",
    },
    "תְּשׁוּפֶנּוּ": {
        "lemma": "תשופנו",
        "shoresh": None,
        "binyan": None,
        "tense": "future",
        "person": "2",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "you will bruise him",
        "translation_context": "you will bruise him",
    },
    "וַתֵּרֶא": {
        "lemma": "ראה",
        "shoresh": "ראה",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "feminine",
        "translation_literal": "and she saw",
        "translation_context": "saw",
    },
    "וַתִּקַּח": {
        "lemma": "לקח",
        "shoresh": "לקח",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "feminine",
        "translation_literal": "and she took",
        "translation_context": "took",
    },
    "וַתֹּאכַל": {
        "lemma": "אכל",
        "shoresh": "אכל",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "feminine",
        "translation_literal": "and she ate",
        "translation_context": "ate",
    },
    "וַתִּתֵּן": {
        "lemma": "נתן",
        "shoresh": "נתן",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "feminine",
        "translation_literal": "and she gave",
        "translation_context": "gave",
    },
    "וַיֹּאכַל": {
        "lemma": "אכל",
        "shoresh": "אכל",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he ate",
        "translation_context": "ate",
    },
    "וַתִּפָּקַחְנָה": {
        "lemma": "פקח",
        "shoresh": "פקח",
        "binyan": "nifal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "plural",
        "gender": "feminine",
        "translation_literal": "and they were opened",
        "translation_context": "were opened",
    },
    "וַיֵּדְעוּ": {
        "lemma": "ידע",
        "shoresh": "ידע",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "plural",
        "gender": "masculine",
        "translation_literal": "and they knew",
        "translation_context": "knew",
    },
    "וַיִּתְפְּרוּ": {
        "lemma": "תפר",
        "shoresh": "תפר",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "plural",
        "gender": "masculine",
        "translation_literal": "and they sewed",
        "translation_context": "sewed",
    },
    "וַיַּעֲשׂוּ": {
        "lemma": "עשה",
        "shoresh": "עשה",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "plural",
        "gender": "masculine",
        "translation_literal": "and they made",
        "translation_context": "made",
    },
    "וַיִּשְׁמְעוּ": {
        "lemma": "שמע",
        "shoresh": "שמע",
        "binyan": "qal",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "plural",
        "gender": "masculine",
        "translation_literal": "and they heard",
        "translation_context": "heard",
    },
    "מִתְהַלֵּךְ": {
        "lemma": "הלך",
        "shoresh": "הלך",
        "binyan": "hitpael",
        "tense": "present",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "walking",
        "translation_context": "walking",
    },
    "וַיִּתְחַבֵּא": {
        "lemma": "חבא",
        "shoresh": "חבא",
        "binyan": "hitpael",
        "tense": "vav_consecutive_past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "and he hid himself",
        "translation_context": "hid himself",
    },
    "שָׁמַעְתִּי": {
        "lemma": "שמע",
        "shoresh": "שמע",
        "binyan": "qal",
        "tense": "past",
        "person": "1",
        "number": "singular",
        "translation_literal": "I heard",
        "translation_context": "heard",
    },
    "וָאִירָא": {
        "lemma": "ירא",
        "shoresh": "ירא",
        "binyan": "qal",
        "tense": "past",
        "person": "1",
        "number": "singular",
        "translation_literal": "and I was afraid",
        "translation_context": "I was afraid",
        "prefixes": [prefix_item("ו")],
    },
    "וָאֵחָבֵא": {
        "lemma": "חבא",
        "shoresh": "חבא",
        "binyan": "nifal",
        "tense": "past",
        "person": "1",
        "number": "singular",
        "translation_literal": "and I hid",
        "translation_context": "I hid",
        "prefixes": [prefix_item("ו")],
    },
    "הִגִּיד": {
        "lemma": "נגד",
        "shoresh": "נגד",
        "binyan": "hifil",
        "tense": "past",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "told",
        "translation_context": "told",
    },
    "אָכָלְתָּ": {
        "lemma": "אכל",
        "shoresh": "אכל",
        "binyan": "qal",
        "tense": "past",
        "person": "2",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "you ate",
        "translation_context": "you ate",
    },
    "נָתַתָּה": {
        "lemma": "נתן",
        "shoresh": "נתן",
        "binyan": "qal",
        "tense": "past",
        "person": "2",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "you gave",
        "translation_context": "you gave",
    },
    "נָתְנָה": {
        "lemma": "נתן",
        "shoresh": "נתן",
        "binyan": "qal",
        "tense": "past",
        "person": "3",
        "number": "singular",
        "gender": "feminine",
        "translation_literal": "she gave",
        "translation_context": "she gave",
    },
    "וָאֹכֵל": {
        "lemma": "אכל",
        "shoresh": "אכל",
        "binyan": "qal",
        "tense": "past",
        "person": "1",
        "number": "singular",
        "translation_literal": "and I ate",
        "translation_context": "I ate",
        "prefixes": [prefix_item("ו")],
    },
    "עָשִׂית": {
        "lemma": "עשה",
        "shoresh": "עשה",
        "binyan": "qal",
        "tense": "past",
        "person": "2",
        "number": "singular",
        "gender": "feminine",
        "translation_literal": "you did",
        "translation_context": "you did",
    },
    "עָשִׂיתָ": {
        "lemma": "עשה",
        "shoresh": "עשה",
        "binyan": "qal",
        "tense": "past",
        "person": "2",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "you did",
        "translation_context": "you did",
    },
    "אָשִׁית": {
        "lemma": "שית",
        "shoresh": "שית",
        "binyan": "qal",
        "tense": "future",
        "person": "1",
        "number": "singular",
        "translation_literal": "I will put",
        "translation_context": "I will put",
    },
    "תֵלֵךְ": {
        "lemma": "הלך",
        "shoresh": "הלך",
        "binyan": "qal",
        "tense": "future",
        "person": "2",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "you will go",
        "translation_context": "you will go",
    },
    "תֹּאכַל": {
        "lemma": "אכל",
        "shoresh": "אכל",
        "binyan": "qal",
        "tense": "future",
        "person": "2",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "you will eat",
        "translation_context": "you will eat",
    },
    "אַרְבֶּה": {
        "lemma": "רבה",
        "shoresh": "רבה",
        "binyan": "hifil",
        "tense": "future",
        "person": "1",
        "number": "singular",
        "translation_literal": "I will greatly increase",
        "translation_context": "I will greatly increase",
    },
    "תֵּלְדִי": {
        "lemma": "ילד",
        "shoresh": "ילד",
        "binyan": "qal",
        "tense": "future",
        "person": "2",
        "number": "singular",
        "gender": "feminine",
        "translation_literal": "you will bear",
        "translation_context": "you will bear",
    },
    "יִמְשָׁל": {
        "lemma": "משל",
        "shoresh": "משל",
        "binyan": "qal",
        "tense": "future",
        "person": "3",
        "number": "singular",
        "gender": "masculine",
        "translation_literal": "he will rule",
        "translation_context": "he will rule",
    },
}

LEXICAL_SURFACE_OVERRIDES = {
    "וְהַנָּחָשׁ": lexical_override(
        "נחש",
        "and the snake",
        part_of_speech="noun",
        semantic_group="animal",
        role_hint="subject_candidate",
        entity_type="animal",
        prefixes=[prefix_item("ו"), prefix_item("ה")],
    ),
    "הַנָּחָשׁ": lexical_override(
        "נחש",
        "the snake",
        part_of_speech="noun",
        semantic_group="animal",
        role_hint="subject_candidate",
        entity_type="animal",
        prefixes=[prefix_item("ה")],
    ),
    "הָאִשָּׁה": lexical_override(
        "אשה",
        "the woman",
        part_of_speech="noun",
        semantic_group="person",
        role_hint="subject_candidate",
        entity_type="person",
        prefixes=[prefix_item("ה")],
        gender="feminine",
    ),
    "וְאִשְׁתּוֹ": lexical_override(
        "אשה",
        "and his wife",
        part_of_speech="noun",
        semantic_group="person",
        role_hint="subject_candidate",
        entity_type="person",
        prefixes=[prefix_item("ו")],
        suffixes=[suffix_item("ו", "his")],
        gender="feminine",
    ),
    "הָאָדָם": lexical_override(
        "אדם",
        "the man",
        part_of_speech="noun",
        semantic_group="person",
        role_hint="subject_candidate",
        entity_type="person",
        prefixes=[prefix_item("ה")],
        gender="masculine",
    ),
    "יְהוָה": lexical_override(
        "יהוה",
        "the LORD",
        part_of_speech="proper_noun",
        semantic_group="divine",
        role_hint="subject_candidate",
        entity_type="divine_name",
        group="divine",
    ),
    "אֱלֹהִים": lexical_override(
        "אלהים",
        "God",
        part_of_speech="proper_noun",
        semantic_group="divine",
        role_hint="subject_candidate",
        entity_type="divine_name",
        group="divine",
    ),
    "הַמְּאֹרֹת": lexical_override(
        "מָאוֹר",
        "the lights",
        part_of_speech="noun",
        shoresh="אור",
        semantic_group="cosmic_entity",
        role_hint="object_candidate",
        entity_type="natural_feature",
        prefixes=[prefix_item("ה")],
        number="plural",
    ),
    "הָרֹמֶשֶׂת": lexical_override(
        "רמשׂ",
        "that creeps",
        part_of_speech="adjective",
        shoresh="רמשׂ",
        semantic_group="description",
        role_hint="unknown",
        entity_type="description",
        prefixes=[prefix_item("ה")],
        gender="feminine",
    ),
    "למאורות": lexical_override(
        "מאורות",
        "for lights",
        shoresh="מאורות",
        prefixes=[prefix_item("ל")],
    ),
    "לאותות": lexical_override(
        "אותות",
        "for signs",
        shoresh="אותות",
        prefixes=[prefix_item("ל")],
    ),
    "במראות": lexical_override(
        "מראות",
        "in visions",
        shoresh="מראות",
        prefixes=[prefix_item("ב")],
    ),
    "במקומות": lexical_override(
        "מקומות",
        "in places",
        shoresh="מקומות",
        prefixes=[prefix_item("ב")],
    ),
    "בצלמנו": lexical_override(
        "צלם",
        "in our image",
        shoresh="צלם",
        prefixes=[prefix_item("ב")],
        suffixes=[suffix_item("נו", "our")],
    ),
    "בְּצַלְמֵנוּ": lexical_override(
        "צלם",
        "in our image",
        shoresh="צלם",
        prefixes=[prefix_item("ב")],
        suffixes=[suffix_item("נו", "our")],
    ),
    "כדמותנו": lexical_override(
        "דמות",
        "like our likeness",
        shoresh="דמות",
        prefixes=[prefix_item("כ")],
        suffixes=[suffix_item("נו", "our")],
    ),
    "כִּדְמוּתֵנוּ": lexical_override(
        "דמות",
        "like our likeness",
        shoresh="דמות",
        prefixes=[prefix_item("כ")],
        suffixes=[suffix_item("נו", "our")],
    ),
    "למינו": lexical_override(
        "מין",
        "to its kind",
        shoresh="מין",
        prefixes=[prefix_item("ל")],
        suffixes=[suffix_item("ו", "its")],
    ),
    "במינו": lexical_override(
        "מין",
        "in its kind",
        shoresh="מין",
        prefixes=[prefix_item("ב")],
        suffixes=[suffix_item("ו", "its")],
    ),
    "כמינו": lexical_override(
        "מין",
        "like its kind",
        shoresh="מין",
        prefixes=[prefix_item("כ")],
        suffixes=[suffix_item("ו", "its")],
    ),
    "למשלת": lexical_override(
        "ממשלה",
        "for dominion",
        shoresh="ממשלה",
        prefixes=[prefix_item("ל")],
    ),
    "עָרוּם": lexical_override(
        "ערום",
        "crafty",
        part_of_speech="adjective",
        semantic_group="descriptor",
        role_hint="descriptor",
        entity_type="adjective",
        group="descriptor",
    ),
    "טוֹב": lexical_override(
        "טוב",
        "good",
        part_of_speech="adjective",
        semantic_group="descriptor",
        role_hint="descriptor",
        entity_type="adjective",
        group="descriptor",
    ),
    "תַאֲוָה": lexical_override(
        "תאוה",
        "desire",
        part_of_speech="noun",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="common_noun",
        group="abstract",
    ),
    "וְנֶחְמָד": lexical_override(
        "חמד",
        "and delightful",
        part_of_speech="adjective",
        semantic_group="descriptor",
        role_hint="descriptor",
        entity_type="adjective",
        group="descriptor",
        prefixes=[prefix_item("ו")],
    ),
    "עֵירֻמִּם": lexical_override(
        "ערם",
        "naked",
        part_of_speech="adjective",
        semantic_group="descriptor",
        role_hint="descriptor",
        entity_type="adjective",
        group="descriptor",
    ),
    "קוֹל": lexical_override(
        "קול",
        "voice",
        part_of_speech="noun",
        semantic_group="abstract",
        role_hint="object_candidate",
        entity_type="common_noun",
        group="abstract",
    ),
    "עֵץ": lexical_override(
        "עץ",
        "a tree",
        part_of_speech="noun",
        semantic_group="object",
        role_hint="object_candidate",
        entity_type="plant",
        group="object",
    ),
    "הָעֵץ": lexical_override(
        "עץ",
        "the tree",
        part_of_speech="noun",
        semantic_group="object",
        role_hint="object_candidate",
        entity_type="plant",
        group="object",
        prefixes=[prefix_item("ה")],
    ),
    "הַגָּן": lexical_override(
        "גן",
        "the garden",
        part_of_speech="noun",
        semantic_group="place",
        role_hint="location_candidate",
        entity_type="place",
        group="place",
        prefixes=[prefix_item("ה")],
    ),
    "בַּגָּן": lexical_override(
        "גן",
        "in the garden",
        part_of_speech="noun",
        semantic_group="place",
        role_hint="location_candidate",
        entity_type="place",
        group="place",
        prefixes=[prefix_item("ב")],
    ),
    "הַשָּׂדֶה": lexical_override(
        "שדה",
        "the field",
        part_of_speech="noun",
        semantic_group="place",
        role_hint="location_candidate",
        entity_type="place",
        group="place",
        prefixes=[prefix_item("ה")],
    ),
    "חַיַּת": lexical_override(
        "חיה",
        "animal of",
        part_of_speech="noun",
        semantic_group="animal",
        role_hint="object_candidate",
        entity_type="animal",
        group="animal",
    ),
    "מִכֹּל": lexical_override(
        "כל",
        "from all",
        part_of_speech="preposition",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
        prefixes=[prefix_item("מ")],
    ),
    "מִפְּרִי": lexical_override(
        "פרי",
        "from fruit of",
        part_of_speech="noun",
        semantic_group="food",
        role_hint="object_candidate",
        entity_type="food",
        group="food",
        prefixes=[prefix_item("מ")],
    ),
    "וּמִפְּרִי": lexical_override(
        "פרי",
        "and from fruit of",
        part_of_speech="noun",
        semantic_group="food",
        role_hint="object_candidate",
        entity_type="food",
        group="food",
        prefixes=[prefix_item("ו"), prefix_item("מ")],
    ),
    "מִפִּרְיוֹ": lexical_override(
        "פרי",
        "from its fruit",
        part_of_speech="noun",
        semantic_group="food",
        role_hint="object_candidate",
        entity_type="food",
        group="food",
        prefixes=[prefix_item("מ")],
        suffixes=[suffix_item("ו", "his")],
    ),
    "עֵינֵיכֶם": lexical_override(
        "עין",
        "your eyes",
        part_of_speech="noun",
        semantic_group="body_part",
        role_hint="object_candidate",
        entity_type="body_part",
        group="body_part",
        suffixes=[suffix_item("כם", "your (m plural)")],
    ),
    "עֵינֵי": lexical_override(
        "עין",
        "eyes of",
        part_of_speech="noun",
        semantic_group="body_part",
        role_hint="object_candidate",
        entity_type="body_part",
        group="body_part",
    ),
    "לָעֵינַיִם": lexical_override(
        "עין",
        "to the eyes",
        part_of_speech="noun",
        semantic_group="body_part",
        role_hint="object_candidate",
        entity_type="body_part",
        group="body_part",
        prefixes=[prefix_item("ל")],
    ),
    "שְׁנֵיהֶם": lexical_override(
        "שנים",
        "the two of them",
        part_of_speech="noun",
        semantic_group="person",
        role_hint="subject_candidate",
        entity_type="person",
        group="person",
    ),
    "עֲלֵה": lexical_override(
        "עלה",
        "leaf of",
        part_of_speech="noun",
        semantic_group="object",
        role_hint="object_candidate",
        entity_type="plant",
        group="object",
    ),
    "תְאֵנָה": lexical_override(
        "תאנה",
        "fig",
        part_of_speech="noun",
        semantic_group="food",
        role_hint="object_candidate",
        entity_type="food",
        group="food",
    ),
    "חֲגֹרֹת": lexical_override(
        "חגורה",
        "belts",
        part_of_speech="noun",
        semantic_group="object",
        role_hint="object_candidate",
        entity_type="object",
        group="object",
        number="plural",
    ),
    "אֲשֶׁר": lexical_override(
        "אשר",
        "that / which",
        part_of_speech="particle",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
    ),
    "אֶל": lexical_override(
        "אל",
        "to",
        part_of_speech="preposition",
        semantic_group="place",
        role_hint="location_candidate",
        entity_type="grammatical_particle",
        group="helper",
    ),
    "כִּי": lexical_override(
        "כי",
        "that / because",
        part_of_speech="particle",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
    ),
    "לֹא": lexical_override(
        "לא",
        "not",
        part_of_speech="particle",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
    ),
    "וְלֹא": lexical_override(
        "לא",
        "and not",
        part_of_speech="particle",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
        prefixes=[prefix_item("ו")],
    ),
    "אַף": lexical_override(
        "אף",
        "indeed",
        part_of_speech="particle",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
    ),
    "פֶּן": lexical_override(
        "פן",
        "lest",
        part_of_speech="particle",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
    ),
    "אֶת": lexical_override(
        "את",
        "object-marking word",
        part_of_speech="particle",
        semantic_group="abstract",
        role_hint="object_candidate",
        entity_type="grammatical_particle",
        group="helper",
    ),
    "בּוֹ": lexical_override(
        "בו",
        "in it",
        part_of_speech="preposition",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
        prefixes=[prefix_item("ב")],
    ),
    "מִמֶּנּוּ": lexical_override(
        "ממנו",
        "from it",
        part_of_speech="preposition",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
        prefixes=[prefix_item("מ")],
    ),
    "בְּתוֹךְ": lexical_override(
        "תוך",
        "inside",
        part_of_speech="preposition",
        semantic_group="place",
        role_hint="location_candidate",
        entity_type="grammatical_particle",
        group="helper",
        prefixes=[prefix_item("ב")],
    ),
    "בְּיוֹם": lexical_override(
        "יום",
        "on the day",
        part_of_speech="noun",
        semantic_group="time",
        role_hint="time_candidate",
        entity_type="time",
        group="time",
        prefixes=[prefix_item("ב")],
    ),
    "הַיּוֹם": lexical_override(
        "יום",
        "the day",
        part_of_speech="noun",
        semantic_group="time",
        role_hint="time_candidate",
        entity_type="time",
        group="time",
        prefixes=[prefix_item("ה")],
    ),
    "לְמַאֲכָל": lexical_override(
        "מאכל",
        "for food",
        part_of_speech="noun",
        semantic_group="food",
        role_hint="object_candidate",
        entity_type="food",
        group="food",
        prefixes=[prefix_item("ל")],
    ),
    "לְהַשְׂכִּיל": lexical_override(
        "שכל",
        "to make wise",
        part_of_speech="verb",
        shoresh="שכל",
        semantic_group="action",
        role_hint="unknown",
        entity_type="verb",
        group="action",
        prefixes=[prefix_item("ל")],
    ),
    "כֵּאלֹהִים": lexical_override(
        "אלהים",
        "like God",
        part_of_speech="proper_noun",
        semantic_group="divine",
        role_hint="descriptor",
        entity_type="divine_name",
        group="divine",
        prefixes=[prefix_item("כ")],
    ),
    "יֹדְעֵי": lexical_override(
        "ידע",
        "knowers of",
        part_of_speech="adjective",
        semantic_group="descriptor",
        role_hint="descriptor",
        entity_type="adjective",
        group="descriptor",
    ),
    "וָרָע": lexical_override(
        "רע",
        "and evil",
        part_of_speech="noun",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="common_noun",
        group="abstract",
        prefixes=[prefix_item("ו")],
    ),
    "הוּא": lexical_override(
        "הוא",
        "it",
        part_of_speech="noun",
        semantic_group="object",
        role_hint="subject_candidate",
        entity_type="pronoun",
        group="person",
    ),
    "גַּם": lexical_override(
        "גם",
        "also",
        part_of_speech="particle",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
    ),
    "לְאִישָׁהּ": lexical_override(
        "איש",
        "to her husband",
        part_of_speech="noun",
        semantic_group="person",
        role_hint="object_candidate",
        entity_type="person",
        group="person",
        prefixes=[prefix_item("ל")],
        suffixes=[suffix_item("ה", "her")],
    ),
    "עִמָּהּ": lexical_override(
        "עם",
        "with her",
        part_of_speech="preposition",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
        suffixes=[suffix_item("ה", "her")],
    ),
    "לָהֶם": lexical_override(
        "להם",
        "for them",
        part_of_speech="preposition",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
        prefixes=[prefix_item("ל")],
        suffixes=[suffix_item("ם", "their")],
    ),
    "וְכִי": lexical_override(
        "כי",
        "and that",
        part_of_speech="particle",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
        prefixes=[prefix_item("ו")],
    ),
    "הֵם": lexical_override(
        "הם",
        "they",
        part_of_speech="pronoun",
        semantic_group="person",
        role_hint="subject_candidate",
        entity_type="pronoun",
        group="person",
        number="plural",
        gender="masculine",
    ),
    "לְרוּחַ": lexical_override(
        "רוח",
        "to the breeze of",
        "at the breezy time of",
        part_of_speech="noun",
        shoresh="רוח",
        semantic_group="time",
        role_hint="time_candidate",
        entity_type="time",
        group="time",
        prefixes=[prefix_item("ל")],
        gender="feminine",
    ),
    "מִפְּנֵי": lexical_override(
        "פנים",
        "from before",
        part_of_speech="preposition",
        semantic_group="place",
        role_hint="location_candidate",
        entity_type="grammatical_particle",
        group="helper",
        prefixes=[prefix_item("מ")],
    ),
    "לוֹ": lexical_override(
        "לו",
        "to him",
        part_of_speech="preposition",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
        prefixes=[prefix_item("ל")],
    ),
    "אַיֶּכָּה": lexical_override(
        "איכה",
        "where are you",
        part_of_speech="particle",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
    ),
    "קֹלְךָ": lexical_override(
        "קול",
        "your voice",
        part_of_speech="noun",
        semantic_group="abstract",
        role_hint="object_candidate",
        entity_type="common_noun",
        group="abstract",
        suffixes=[suffix_item("ךָ", "your (m)")],
    ),
    "עֵירֹם": lexical_override(
        "עירם",
        "naked",
        part_of_speech="adjective",
        semantic_group="descriptor",
        role_hint="descriptor",
        entity_type="adjective",
        group="descriptor",
    ),
    "אָנֹכִי": lexical_override(
        "אנכי",
        "I",
        part_of_speech="pronoun",
        semantic_group="person",
        role_hint="subject_candidate",
        entity_type="pronoun",
        group="person",
    ),
    "מִי": lexical_override(
        "מי",
        "who",
        part_of_speech="particle",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
    ),
    "לְךָ": lexical_override(
        "לך",
        "to you",
        part_of_speech="preposition",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
        prefixes=[prefix_item("ל")],
    ),
    "אָתָּה": lexical_override(
        "אתה",
        "you",
        part_of_speech="pronoun",
        semantic_group="person",
        role_hint="subject_candidate",
        entity_type="pronoun",
        group="person",
    ),
    "אַתָּה": lexical_override(
        "אתה",
        "you",
        part_of_speech="pronoun",
        semantic_group="person",
        role_hint="subject_candidate",
        entity_type="pronoun",
        group="person",
    ),
    "הֲמִן": lexical_override(
        "מן",
        "from",
        part_of_speech="preposition",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
    ),
    "לְבִלְתִּי": lexical_override(
        "בלתי",
        "so as not to",
        part_of_speech="particle",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
        prefixes=[prefix_item("ל")],
    ),
    "עִמָּדִי": lexical_override(
        "עם",
        "with me",
        part_of_speech="preposition",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
        suffixes=[suffix_item("י", "my")],
    ),
    "לִּי": lexical_override(
        "לי",
        "to me",
        part_of_speech="preposition",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
        prefixes=[prefix_item("ל")],
    ),
    "מִן": lexical_override(
        "מן",
        "from",
        part_of_speech="preposition",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
    ),
    "לָאִשָּׁה": lexical_override(
        "אשה",
        "to the woman",
        part_of_speech="noun",
        semantic_group="person",
        role_hint="object_candidate",
        entity_type="person",
        group="person",
        prefixes=[prefix_item("ל"), prefix_item("ה")],
    ),
    "מַה": lexical_override(
        "מה",
        "what",
        part_of_speech="particle",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
    ),
    "זֹּאת": lexical_override(
        "זאת",
        "this",
        part_of_speech="pronoun",
        semantic_group="descriptor",
        role_hint="descriptor",
        entity_type="pronoun",
        group="descriptor",
    ),
    "אָרוּר": lexical_override(
        "ארור",
        "cursed",
        part_of_speech="adjective",
        semantic_group="descriptor",
        role_hint="descriptor",
        entity_type="adjective",
        group="descriptor",
    ),
    "הַבְּהֵמָה": lexical_override(
        "בהמה",
        "the animal",
        part_of_speech="noun",
        semantic_group="animal",
        role_hint="object_candidate",
        entity_type="animal",
        group="animal",
        prefixes=[prefix_item("ה")],
    ),
    "וּמִכֹּל": lexical_override(
        "כל",
        "and from every",
        part_of_speech="preposition",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
        prefixes=[prefix_item("ו"), prefix_item("מ")],
    ),
    "עַל": lexical_override(
        "על",
        "upon",
        part_of_speech="preposition",
        semantic_group="place",
        role_hint="location_candidate",
        entity_type="grammatical_particle",
        group="helper",
    ),
    "גְּחֹנְךָ": lexical_override(
        "גחון",
        "your belly",
        part_of_speech="noun",
        semantic_group="body",
        role_hint="object_candidate",
        entity_type="common_noun",
        group="body",
        suffixes=[suffix_item("ךָ", "your (m)")],
    ),
    "וְעָפָר": lexical_override(
        "עפר",
        "and dust",
        part_of_speech="noun",
        semantic_group="object",
        role_hint="object_candidate",
        entity_type="common_noun",
        group="object",
        prefixes=[prefix_item("ו")],
    ),
    "כָּל": lexical_override(
        "כל",
        "all",
        part_of_speech="noun",
        semantic_group="descriptor",
        role_hint="descriptor",
        entity_type="common_noun",
        group="descriptor",
    ),
    "יְמֵי": lexical_override(
        "ימים",
        "days of",
        part_of_speech="noun",
        semantic_group="time",
        role_hint="time_candidate",
        entity_type="time",
        group="time",
    ),
    "חַיֶּיךָ": lexical_override(
        "חיים",
        "your life",
        part_of_speech="noun",
        semantic_group="time",
        role_hint="time_candidate",
        entity_type="time",
        group="time",
        suffixes=[suffix_item("ךָ", "your (m)")],
    ),
    "וְאֵיבָה": lexical_override(
        "איבה",
        "and enmity",
        part_of_speech="noun",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="common_noun",
        group="abstract",
        prefixes=[prefix_item("ו")],
    ),
    "וּבֵין": lexical_override(
        "בין",
        "and between",
        part_of_speech="preposition",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
        prefixes=[prefix_item("ו")],
    ),
    "בֵּינְךָ": lexical_override(
        "בין",
        "between you",
        part_of_speech="preposition",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
        suffixes=[suffix_item("ךָ", "your (m)")],
    ),
    "זַרְעֲךָ": lexical_override(
        "זרע",
        "your offspring",
        part_of_speech="noun",
        semantic_group="person",
        role_hint="subject_candidate",
        entity_type="person",
        group="person",
        suffixes=[suffix_item("ךָ", "your (m)")],
    ),
    "זַרְעָהּ": lexical_override(
        "זרע",
        "her offspring",
        part_of_speech="noun",
        semantic_group="person",
        role_hint="subject_candidate",
        entity_type="person",
        group="person",
        suffixes=[suffix_item("ה", "her")],
    ),
    "רֹאשׁ": lexical_override(
        "ראש",
        "head",
        part_of_speech="noun",
        semantic_group="body",
        role_hint="object_candidate",
        entity_type="common_noun",
        group="body",
    ),
    "וְאַתָּה": lexical_override(
        "אתה",
        "and you",
        part_of_speech="pronoun",
        semantic_group="person",
        role_hint="subject_candidate",
        entity_type="pronoun",
        group="person",
        prefixes=[prefix_item("ו")],
    ),
    "עָקֵב": lexical_override(
        "עקב",
        "heel",
        part_of_speech="noun",
        semantic_group="body",
        role_hint="object_candidate",
        entity_type="common_noun",
        group="body",
    ),
    "הַרְבָּה": lexical_override(
        "רבה",
        "greatly",
        part_of_speech="particle",
        semantic_group="descriptor",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
    ),
    "עִצְּבוֹנֵךְ": lexical_override(
        "עצבון",
        "your pain",
        part_of_speech="noun",
        semantic_group="abstract",
        role_hint="object_candidate",
        entity_type="common_noun",
        group="abstract",
        suffixes=[suffix_item("ךְ", "your (f)")],
    ),
    "וְהֵרֹנֵךְ": lexical_override(
        "הריון",
        "and your pregnancy",
        part_of_speech="noun",
        semantic_group="body",
        role_hint="object_candidate",
        entity_type="common_noun",
        group="body",
        prefixes=[prefix_item("ו")],
        suffixes=[suffix_item("ךְ", "your (f)")],
    ),
    "בְּעֶצֶב": lexical_override(
        "עצב",
        "with pain",
        part_of_speech="noun",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="common_noun",
        group="abstract",
        prefixes=[prefix_item("ב")],
    ),
    "בָנִים": lexical_override(
        "בן",
        "children",
        part_of_speech="noun",
        semantic_group="person",
        role_hint="object_candidate",
        entity_type="person",
        group="person",
    ),
    "וְאֶל": lexical_override(
        "אל",
        "and to",
        part_of_speech="preposition",
        semantic_group="place",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
        prefixes=[prefix_item("ו")],
    ),
    "אִישֵׁךְ": lexical_override(
        "איש",
        "your husband",
        part_of_speech="noun",
        semantic_group="person",
        role_hint="subject_candidate",
        entity_type="person",
        group="person",
        suffixes=[suffix_item("ךְ", "your (f)")],
    ),
    "תְּשׁוּקָתֵךְ": lexical_override(
        "תשוקה",
        "your desire",
        part_of_speech="noun",
        semantic_group="abstract",
        role_hint="object_candidate",
        entity_type="common_noun",
        group="abstract",
        suffixes=[suffix_item("ךְ", "your (f)")],
    ),
    "וְהוּא": lexical_override(
        "הוא",
        "and he",
        part_of_speech="pronoun",
        semantic_group="person",
        role_hint="subject_candidate",
        entity_type="pronoun",
        group="person",
        prefixes=[prefix_item("ו")],
    ),
    "בָּךְ": lexical_override(
        "בך",
        "over you",
        part_of_speech="preposition",
        semantic_group="abstract",
        role_hint="descriptor",
        entity_type="grammatical_particle",
        group="helper",
    ),
}

LEXICAL_NORMALIZED_OVERRIDES = {
    normalize_form(surface): deepcopy(features)
    for surface, features in LEXICAL_SURFACE_OVERRIDES.items()
}

SEMANTIC_OVERRIDES = {
    "אלקים": {
        "semantic_group": "divine",
        "role_hint": "subject_candidate",
        "entity_type": "divine_name",
    },
    "את": {
        "semantic_group": "unknown",
        "role_hint": "object_candidate",
        "entity_type": "grammatical_particle",
    },
    "ואת": {
        "semantic_group": "unknown",
        "role_hint": "object_candidate",
        "entity_type": "grammatical_particle",
    },
    "כי": {
        "semantic_group": "abstract",
        "role_hint": "descriptor",
        "entity_type": "grammatical_particle",
    },
    "אשר": {
        "semantic_group": "abstract",
        "role_hint": "descriptor",
        "entity_type": "grammatical_particle",
    },
    "בין": {
        "semantic_group": "abstract",
        "role_hint": "location_candidate",
        "entity_type": "grammatical_particle",
    },
    "ובין": {
        "semantic_group": "abstract",
        "role_hint": "location_candidate",
        "entity_type": "grammatical_particle",
    },
    "אור": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "האור": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "חשך": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "וחשך": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "החשך": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "שמים": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "השמים": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "ארץ": {
        "semantic_group": "place",
        "role_hint": "location_candidate",
        "entity_type": "natural_feature",
    },
    "הארץ": {
        "semantic_group": "place",
        "role_hint": "location_candidate",
        "entity_type": "natural_feature",
    },
    "והארץ": {
        "semantic_group": "place",
        "role_hint": "location_candidate",
        "entity_type": "natural_feature",
    },
    "מים": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "המים": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "למים": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "רקיע": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "הרקיע": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "לרקיע": {
        "semantic_group": "cosmic_entity",
        "role_hint": "location_candidate",
        "entity_type": "natural_feature",
    },
    "יבשה": {
        "semantic_group": "place",
        "role_hint": "location_candidate",
        "entity_type": "natural_feature",
    },
    "היבשה": {
        "semantic_group": "place",
        "role_hint": "location_candidate",
        "entity_type": "natural_feature",
    },
    "ליבשה": {
        "semantic_group": "place",
        "role_hint": "location_candidate",
        "entity_type": "natural_feature",
    },
    "מקוה": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "ולמקוה": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "ימים": {
        "semantic_group": "cosmic_entity",
        "role_hint": "object_candidate",
        "entity_type": "natural_feature",
    },
    "יום": {
        "semantic_group": "time",
        "role_hint": "time_candidate",
        "entity_type": "common_noun",
    },
    "לילה": {
        "semantic_group": "time",
        "role_hint": "time_candidate",
        "entity_type": "common_noun",
    },
    "ערב": {
        "semantic_group": "time",
        "role_hint": "time_candidate",
        "entity_type": "common_noun",
    },
    "בקר": {
        "semantic_group": "time",
        "role_hint": "time_candidate",
        "entity_type": "common_noun",
    },
    "תהו": {
        "semantic_group": "abstract",
        "role_hint": "descriptor",
        "entity_type": "common_noun",
    },
    "ובהו": {
        "semantic_group": "abstract",
        "role_hint": "descriptor",
        "entity_type": "common_noun",
    },
    "טוב": {
        "semantic_group": "abstract",
        "role_hint": "descriptor",
        "entity_type": "common_noun",
    },
    "אחד": {
        "semantic_group": "abstract",
        "role_hint": "descriptor",
        "entity_type": "common_noun",
    },
    "שני": {
        "semantic_group": "abstract",
        "role_hint": "descriptor",
        "entity_type": "common_noun",
    },
    "כן": {
        "semantic_group": "abstract",
        "role_hint": "descriptor",
        "entity_type": "unknown",
    },
    "מקום": {
        "semantic_group": "place",
        "role_hint": "location_candidate",
        "entity_type": "common_noun",
    },
}

FUTURE_PREFIX_SURFACES = (
    "\u05d9\u05b4",
    "\u05d9\u05b0",
    "\u05ea\u05b4",
    "\u05ea\u05b0",
    "\u05d0\u05b6",
    "\u05d0\u05b2",
    "\u05e0\u05b4",
    "\u05e0\u05b0",
)


def extract_inseparable_prefixes(word):
    plain = undotted_form(word)
    prefixes = []

    if plain.startswith("ו") and len(plain) > 2:
        prefix_type, translation = PREFIX_TRANSLATIONS["ו"]
        prefixes.append({"form": "ו", "type": prefix_type, "translation": translation})
        plain = plain[1:]

    if plain.startswith("ה") and len(plain) > 2:
        prefix_type, translation = PREFIX_TRANSLATIONS["ה"]
        prefixes.append({"form": "ה", "type": prefix_type, "translation": translation})
    elif plain[:1] in {"ב", "ל", "כ", "מ", "ש"} and len(plain) > 3:
        form = plain[0]
        prefix_type, translation = PREFIX_TRANSLATIONS[form]
        prefixes.append({"form": form, "type": prefix_type, "translation": translation})

    return prefixes


def extract_prefix(word, word_bank=None):
    features = verb_features(word)
    if features:
        for prefix in features.get("prefixes", []):
            form = prefix.get("form")
            if form in PREFIX_TRANSLATIONS:
                return form

    for prefix in extract_inseparable_prefixes(word):
        form = prefix.get("form")
        if form == "ש":
            continue
        if word_bank is not None and not prefix_has_known_base(word, form, word_bank):
            continue
        if form in PREFIX_TRANSLATIONS:
            return form

    return None


def verb_prefixes(word, tense):
    plain = undotted_form(word)
    prefixes = []
    if tense == "vav_consecutive_past":
        return [
            {
                "form": "ו",
                "type": "verb_prefix_vav_consecutive",
                "translation": "and",
            }
        ]
    if plain.startswith("ו") and len(plain) > 2:
        prefix_type, translation = PREFIX_TRANSLATIONS["ו"]
        prefixes.append({"form": "ו", "type": prefix_type, "translation": translation})
        plain = plain[1:]
    if plain[:1] in {"י", "ת", "א", "נ"} and len(plain) >= 3:
        prefixes.append(
            {
                "form": plain[0],
                "type": "verb_prefix_future",
                "translation": "future / jussive marker",
            }
        )
    return prefixes


def extract_suffix(word):
    if detect_verb_tense(word):
        return None
    suffix = common_possessive_suffix(word)
    return suffix.get("form") if suffix else None


def _word_bank_contains(word_bank, surface):
    if not word_bank or not surface:
        return False
    if surface in word_bank:
        return True
    normalized = normalize_form(surface)
    if normalized in word_bank:
        return True
    for entry in word_bank.values():
        if not isinstance(entry, dict):
            continue
        if entry.get("normalized") == normalized:
            return True
    return False


def prefix_has_known_base(word, prefix, word_bank):
    if not prefix or not word_bank:
        return False
    normalized = normalize_form(word)
    if not normalized.startswith(prefix):
        return False
    base = normalized[len(prefix):]
    return _word_bank_contains(word_bank, base)


def suffix_has_known_base(word, suffix, word_bank):
    if not suffix or not word_bank:
        return False
    plain = undotted_form(word)
    if not plain.endswith(suffix):
        return False
    base = plain[:-len(suffix)]
    if _word_bank_contains(word_bank, base):
        return True
    prefix = extract_prefix(base, word_bank)
    if prefix and base.startswith(prefix):
        return _word_bank_contains(word_bank, base[len(prefix):])
    return False


def apply_prefix_metadata(word, entry, word_bank=None):
    explicit_prefix = entry.get("prefix") or next(
        (item.get("form") for item in (entry.get("prefixes") or []) if item.get("form")),
        "",
    )
    if explicit_prefix and explicit_prefix not in PREFIX_TRANSLATIONS:
        explicit_prefix = ""
    prefix = explicit_prefix or extract_prefix(word, word_bank)
    if not prefix:
        entry["prefix"] = ""
        entry["prefix_meaning"] = ""
        return entry

    prefix_type, translation = PREFIX_TRANSLATIONS[prefix]
    if (
        word_bank is not None
        and not prefix_has_known_base(word, prefix, word_bank)
        and prefix != "\u05d5"
        and prefix != explicit_prefix
    ):
        entry["prefix"] = ""
        entry["prefix_meaning"] = ""
        return entry

    entry["prefix"] = prefix
    entry["prefix_meaning"] = translation
    entry.setdefault("prefixes", [])
    if not any(item.get("form") == prefix for item in entry["prefixes"]):
        entry["prefixes"] = [{"form": prefix, "type": prefix_type, "translation": translation}] + list(entry["prefixes"])
    return entry


def apply_suffix_metadata(word, entry, word_bank=None):
    explicit_suffix = entry.get("suffix") or next(
        (item.get("form") for item in (entry.get("suffixes") or []) if item.get("form")),
        "",
    )
    if explicit_suffix and explicit_suffix not in PRONOMINAL_SUFFIX_TRANSLATIONS:
        explicit_suffix = ""
    if (
        not explicit_suffix
        and entry.get("part_of_speech") == "pronoun"
        and entry.get("entity_type") == "pronoun"
    ):
        entry.setdefault("suffix", "")
        entry.setdefault("suffix_meaning", "")
        return entry
    if (
        not explicit_suffix
        and entry.get("entity_type") == "grammatical_particle"
    ):
        entry.setdefault("suffix", "")
        entry.setdefault("suffix_meaning", "")
        return entry
    suffix = explicit_suffix or extract_suffix(word)
    if not suffix:
        entry.setdefault("suffix", "")
        entry.setdefault("suffix_meaning", "")
        return entry
    if word_bank is not None and not suffix_has_known_base(word, suffix, word_bank) and suffix != explicit_suffix:
        return entry

    translation = common_possessive_suffix(word) or {}
    entry["suffix"] = suffix
    entry["suffix_meaning"] = translation.get("translation", entry.get("suffix_meaning", ""))
    entry.setdefault("suffixes", [])
    if not any(item.get("form") == suffix for item in entry["suffixes"]):
        entry["suffixes"] = list(entry["suffixes"]) + [{
            "form": suffix,
            "type": "pronominal_suffix",
            "translation": entry["suffix_meaning"],
        }]
    return entry


def detect_verb_tense(word):
    normalized = normalize_form(word)
    if word in SURFACE_OVERRIDES:
        return SURFACE_OVERRIDES[word]["tense"]
    if normalized in VERB_OVERRIDES:
        return VERB_OVERRIDES[normalized]["tense"]
    surface = word or ""
    plain = undotted_form(word)
    consecutive = detect_vav_consecutive(word)
    if consecutive:
        return consecutive
    if plain.startswith("ו") and len(plain) > 3:
        plain = plain[1:]
    if plain.endswith(("תי", "תם", "תן", "נו")) and len(plain) > 4:
        return "past"
    if plain.endswith("ת") and len(plain) > 4:
        return "past"
    if (
        plain.startswith(("י", "ת", "א", "נ"))
        and len(plain) >= 4
        and surface.startswith(FUTURE_PREFIX_SURFACES)
    ):
        return "future"
    return None


def verb_features(word):
    normalized = normalize_form(word)
    features = dict(VERB_OVERRIDES.get(normalized, {}))
    features.update(SURFACE_OVERRIDES.get(word, {}))
    tense = features.get("tense") or detect_verb_tense(word)
    if not tense:
        return None
    return {
        "lemma": features.get("lemma", normalized),
        "shoresh": features.get("shoresh"),
        "part_of_speech": "verb",
        "binyan": features.get("binyan", "qal"),
        "tense": tense,
        "person": features.get("person"),
        "number": features.get("number"),
        "gender": features.get("gender"),
        "prefixes": (
            list(features.get("prefixes", []))
            if "prefixes" in features
            else ([] if word in SURFACE_OVERRIDES and tense in {"past", "present", "infinitive"} else verb_prefixes(word, tense))
        ),
        "suffixes": [],
        "translation_literal": features.get("translation_literal", word),
        "translation_context": features.get("translation_context", word),
        "confidence": "rule_based",
        "semantic_group": "action",
        "role_hint": "unknown",
        "entity_type": "verb",
    }


def lexical_features(word):
    features = deepcopy(
        LEXICAL_SURFACE_OVERRIDES.get(word)
        or LEXICAL_NORMALIZED_OVERRIDES.get(normalize_form(word))
    )
    if not features:
        return None
    features.setdefault("lemma", normalize_form(word))
    features.setdefault("part_of_speech", "noun")
    features.setdefault("prefixes", [])
    features.setdefault("suffixes", [])
    return features


def semantic_features(token, part_of_speech):
    normalized = normalize_form(token)
    if part_of_speech == "verb":
        return {
            "semantic_group": "action",
            "role_hint": "unknown",
            "entity_type": "verb",
        }
    return dict(
        SEMANTIC_OVERRIDES.get(
            normalized,
            {
                "semantic_group": "unknown",
                "role_hint": "unknown",
                "entity_type": "unknown",
            },
        )
    )


def likely_part_of_speech(word):
    tense = detect_verb_tense(word)
    if tense:
        return "verb"
    return "unknown"


def generate_candidate_analyses(token):
    normalized = normalize_form(token)
    features = lexical_features(token)
    feature_origin = "lexical" if features else None
    if features is None:
        features = verb_features(token)
        feature_origin = "verb" if features else None
    part_of_speech = features["part_of_speech"] if features else likely_part_of_speech(token)
    suffix = None if features else common_possessive_suffix(token)
    prefixes = list(features.get("prefixes", [])) if features else extract_inseparable_prefixes(token)
    suffixes = list(features.get("suffixes", [])) if features else [suffix] if suffix else []

    candidate = {
        "surface": token,
        "normalized": normalized,
        "lemma": normalized,
        "shoresh": None,
        "part_of_speech": part_of_speech,
        "binyan": "qal" if part_of_speech == "verb" else None,
        "tense": detect_verb_tense(token) if part_of_speech == "verb" else None,
        "person": None,
        "number": None,
        "gender": None,
        "semantic_group": "unknown",
        "role_hint": "unknown",
        "entity_type": "unknown",
        "group": "unknown",
        "prefixes": prefixes,
        "suffixes": suffixes,
        "translation_literal": token,
        "translation_context": token,
        "confidence": "generated_candidate",
        "source_refs": [],
    }
    candidate.update(semantic_features(token, part_of_speech))
    if features:
        candidate.update(features)
    if feature_origin is None:
        apply_prefix_metadata(token, candidate)
        apply_suffix_metadata(token, candidate)
    candidate["prefix"] = candidate.get("prefix") or (candidate.get("prefixes") or [{}])[0].get("form", "")
    candidate["prefix_meaning"] = candidate.get("prefix_meaning") or (candidate.get("prefixes") or [{}])[0].get("translation", "")
    candidate["suffix"] = candidate.get("suffix") or (candidate.get("suffixes") or [{}])[0].get("form", "")
    candidate["suffix_meaning"] = candidate.get("suffix_meaning") or (candidate.get("suffixes") or [{}])[0].get("translation", "")
    primary = apply_torah_overrides(candidate)
    analyses = [primary]
    if primary.get("part_of_speech") == "verb":
        alternate = deepcopy(primary)
        alternate.update(
            {
                "lemma": normalized,
                "shoresh": None,
                "part_of_speech": "unknown",
                "binyan": None,
                "tense": None,
                "person": None,
                "number": None,
                "gender": None,
                "semantic_group": "unknown",
                "role_hint": "unknown",
                "entity_type": "unknown",
                "prefixes": extract_inseparable_prefixes(token),
                "suffixes": [],
                "translation_literal": token,
                "translation_context": token,
                "confidence": "generated_alternate",
            }
        )
        analyses.append(alternate)
    return analyses
