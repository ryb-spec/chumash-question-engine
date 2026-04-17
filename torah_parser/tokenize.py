"""Conservative pasuk tokenization."""

from .normalize import (
    normalize_form,
    preserve_surface_text,
    punctuation_cleaned,
    strip_boundary_punctuation,
)


def tokenize_pasuk(text):
    if not isinstance(text, str):
        return []
    cleaned = punctuation_cleaned(text)
    tokens = []
    for raw in preserve_surface_text(cleaned).split():
        token = strip_boundary_punctuation(raw)
        if token:
            tokens.append(token)
    return tokens


def tokenize_pasuk_record(pasuk_record):
    tokens = pasuk_record.get("tokens")
    if tokens is None:
        tokens = tokenize_pasuk(pasuk_record.get("text", ""))

    pasuk_id = pasuk_record.get("pasuk_id")
    return [
        {
            "pasuk_id": pasuk_id,
            "token_index": index,
            "surface": preserve_surface_text(token),
            "normalized": normalize_form(token),
        }
        for index, token in enumerate(tokens)
    ]
