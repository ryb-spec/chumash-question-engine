"""Hebrew text normalization utilities.

Surface text is preserved for display. Normalized forms are used only for
matching and lookup.
"""

import re
import unicodedata


HEBREW_MARK_RE = re.compile(r"[\u0591-\u05c7]")
HEBREW_PUNCTUATION = {
    "\u05be": " ",
    "\u05c0": " ",
    "\u05c3": "",
    "\u05c6": "",
}


def preserve_surface_text(text):
    return text if isinstance(text, str) else ""


def undotted_form(text):
    if not isinstance(text, str):
        return ""
    normalized = unicodedata.normalize("NFC", text)
    for source, replacement in HEBREW_PUNCTUATION.items():
        normalized = normalized.replace(source, replacement)
    return HEBREW_MARK_RE.sub("", normalized)


def normalize_form(text):
    return " ".join(undotted_form(text).split())


def normalize_token(text):
    return normalize_form(text)
