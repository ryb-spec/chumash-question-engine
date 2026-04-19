from __future__ import annotations

from functools import lru_cache

from foundation_resources import load_foundation_resource


_PRONOUN_KINDS = (
    "subject_pronouns",
    "object_pronouns",
    "possessive_pronouns",
)


@lru_cache(maxsize=1)
def load_grammar_paradigms():
    return load_foundation_resource("grammar_paradigms")


def paradigm_instructional_uses():
    return tuple(load_grammar_paradigms().get("instructional_uses", []))


def pronoun_forms(kind, *, number=None, person=None, gender=None):
    if kind not in _PRONOUN_KINDS:
        raise KeyError(f"Unsupported pronoun kind: {kind}")
    data = load_grammar_paradigms()[kind]
    numbers = (number,) if number else tuple(data.keys())
    matches = []
    for number_key in numbers:
        for form in data.get(number_key, []):
            if person is not None and form.get("person") != str(person):
                continue
            if gender is not None and form.get("gender") != gender:
                continue
            matches.append(dict(form))
    return matches


def pronoun_form(kind, *, number, person, gender):
    matches = pronoun_forms(kind, number=number, person=person, gender=gender)
    if not matches:
        return None
    return matches[0]


def verb_paradigm_forms(tense, *, number=None, person=None, gender=None):
    paradigm = load_grammar_paradigms()["verb_paradigm_example"]
    tense_data = paradigm.get(tense, {})
    numbers = (number,) if number else tuple(tense_data.keys())
    matches = []
    for number_key in numbers:
        for form in tense_data.get(number_key, []):
            if person is not None and form.get("person") != str(person):
                continue
            if gender is not None and form.get("gender") != gender:
                continue
            matches.append(dict(form))
    return matches


def verb_paradigm_form(tense, *, number, person, gender):
    matches = verb_paradigm_forms(tense, number=number, person=person, gender=gender)
    if not matches:
        return None
    return matches[0]

