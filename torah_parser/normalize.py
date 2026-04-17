"""Hebrew text normalization utilities.

Surface text is preserved for display. Normalized forms are used only for
matching and lookup.
"""

import re
import unicodedata


HEBREW_MARK_RE = re.compile(r"[\u0591-\u05c7]")
BOUNDARY_PUNCTUATION_RE = re.compile(r"^[^\u0590-\u05ff]+|[^\u0590-\u05ff]+$")
PUNCTUATION_TRANSLATION = {
    "\u05be": " ",
    "\u05c0": " ",
    "\u05c3": " ",
    "\u05c6": " ",
    ",": " ",
    ".": " ",
    ";": " ",
    ":": " ",
    "!": " ",
    "?": " ",
    "(": " ",
    ")": " ",
    "[": " ",
    "]": " ",
    "{": " ",
    "}": " ",
    '"': " ",
    "'": " ",
    "-": " ",
    "/": " ",
    "\\": " ",
}


def preserve_surface_text(text):
    return text if isinstance(text, str) else ""


def punctuation_cleaned(text):
    cleaned = preserve_surface_text(text)
    for source, replacement in PUNCTUATION_TRANSLATION.items():
        cleaned = cleaned.replace(source, replacement)
    return cleaned


def strip_boundary_punctuation(token):
    if not isinstance(token, str):
        return ""
    return BOUNDARY_PUNCTUATION_RE.sub("", preserve_surface_text(token))


def undotted_form(text):
    if not isinstance(text, str):
        return ""
    normalized = unicodedata.normalize("NFC", punctuation_cleaned(text))
    return HEBREW_MARK_RE.sub("", normalized)


def normalize_form(text):
    return " ".join(undotted_form(text).split())


def normalize_token(text):
    return normalize_form(text)
