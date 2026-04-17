"""Active local assessment dataset scope.

Runtime assessment content should come from the parsed local Torah dataset only.
Legacy preview/static files may still exist in the repo, but they are not part
of the active assessment scope.
"""

import json
from functools import lru_cache
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
BASE_DIR = REPO_ROOT


def repo_path(*parts):
    return REPO_ROOT.joinpath(*parts)


def data_path(*parts):
    return repo_path("data", *parts)


def resolve_repo_path(path_like):
    path = Path(path_like)
    if path.is_absolute():
        return path
    return repo_path(*path.parts)


CORPUS_MANIFEST_PATH = data_path("corpus_manifest.json")
CORPUS_STATUS_VALUES = (
    "experimental",
    "parsed",
    "reviewed",
    "active_candidate",
    "active",
)


def _default_corpus_manifest():
    source_file = "data/source/bereishis_1_1_to_4_20.json"
    parsed_files = {
        "pesukim": "data/pesukim_100.json",
        "word_bank": "data/word_bank.json",
        "word_occurrences": "data/word_occurrences.json",
        "translation_reviews": "data/translation_reviews.json",
    }
    return {
        "metadata": {
            "title": "Chumash Corpus Manifest",
            "version": "0.1",
            "status_values": list(CORPUS_STATUS_VALUES),
            "notes": (
                "Registry for source corpora, parsed corpora, and runtime scopes. "
                "The data/ root files remain the current blessed runtime layer."
            ),
        },
        "source_corpora": [
            {
                "corpus_id": "source_bereishis_1_1_to_1_20_local",
                "type": "source_corpus",
                "sefer": "Bereishis",
                "range": {
                    "start": {"perek": 1, "pasuk": 1},
                    "end": {"perek": 1, "pasuk": 20},
                },
                "pesukim_count": 20,
                "source_files": [source_file],
                "parsed_files": {},
                "status": "experimental",
                "declared_source_range": "1:1-4:20",
                "notes": [
                    "Current local source file backing the active parsed dataset.",
                    "Not yet fully reproducible for the active 20-pasuk state.",
                ],
            }
        ],
        "parsed_corpora": [
            {
                "corpus_id": "parsed_bereishis_1_1_to_1_20_root",
                "type": "parsed_corpus",
                "sefer": "Bereishis",
                "range": {
                    "start": {"perek": 1, "pasuk": 1},
                    "end": {"perek": 1, "pasuk": 20},
                },
                "pesukim_count": 20,
                "source_files": [source_file],
                "parsed_files": dict(parsed_files),
                "status": "active_candidate",
                "storage_layer": "data_root",
                "notes": [
                    "Current blessed parsed runtime layer stored in data/ root.",
                    "Contains reviewed and parsed-only enrichment used by the active app.",
                ],
            }
        ],
        "scopes": [
            {
                "scope_id": "local_parsed_bereishis_1_1_to_1_20",
                "type": "runtime_scope",
                "sefer": "Bereishis",
                "range": {
                    "start": {"perek": 1, "pasuk": 1},
                    "end": {"perek": 1, "pasuk": 20},
                },
                "pesukim_count": 20,
                "source_corpus_id": "source_bereishis_1_1_to_1_20_local",
                "parsed_corpus_id": "parsed_bereishis_1_1_to_1_20_root",
                "source_files": [source_file],
                "parsed_files": dict(parsed_files),
                "status": "active",
                "supported_runtime": True,
                "notes": [
                    "Current supported Streamlit runtime scope.",
                    "Backward-compatible with existing data/ root runtime paths.",
                ],
            }
        ],
        "future_scopes": [],
    }


@lru_cache(maxsize=1)
def load_corpus_manifest():
    if not CORPUS_MANIFEST_PATH.exists():
        return _default_corpus_manifest()
    with CORPUS_MANIFEST_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def corpus_manifest_metadata():
    return dict(load_corpus_manifest().get("metadata", {}))


def corpus_source_corpora():
    return tuple(load_corpus_manifest().get("source_corpora", []))


def corpus_parsed_corpora():
    return tuple(load_corpus_manifest().get("parsed_corpora", []))


def corpus_scopes():
    return tuple(load_corpus_manifest().get("scopes", []))


def scope_registry():
    return {
        scope.get("scope_id"): scope
        for scope in corpus_scopes()
        if scope.get("scope_id")
    }


def get_scope_metadata(scope_id):
    return dict(scope_registry().get(scope_id, {}))


def _resolve_manifest_active_scope():
    for scope in corpus_scopes():
        if scope.get("status") == "active" and scope.get("supported_runtime"):
            return dict(scope)
    scopes = corpus_scopes()
    return dict(scopes[0]) if scopes else {}


def manifest_active_scope_metadata():
    return _resolve_manifest_active_scope()

SUPPORTED_RUNTIME_NAME = "streamlit_app"
SUPPORTED_RUNTIME_ENTRYPOINT = "streamlit_app.py"
SUPPORTED_PRACTICE_TYPES = (
    "Learn Mode",
    "Practice Mode",
    "Pasuk Flow",
)

_MANIFEST_ACTIVE_SCOPE = _resolve_manifest_active_scope()

ACTIVE_ASSESSMENT_SCOPE = _MANIFEST_ACTIVE_SCOPE.get(
    "scope_id",
    "local_parsed_bereishis_1_1_to_1_20",
)

_ACTIVE_PARSED_FILES = _MANIFEST_ACTIVE_SCOPE.get("parsed_files", {})

ACTIVE_PARSED_PESUKIM_PATH = resolve_repo_path(
    _ACTIVE_PARSED_FILES.get("pesukim", "data/pesukim_100.json")
)
ACTIVE_WORD_BANK_PATH = resolve_repo_path(
    _ACTIVE_PARSED_FILES.get("word_bank", "data/word_bank.json")
)
ACTIVE_WORD_OCCURRENCES_PATH = resolve_repo_path(
    _ACTIVE_PARSED_FILES.get("word_occurrences", "data/word_occurrences.json")
)
ACTIVE_TRANSLATION_REVIEWS_PATH = resolve_repo_path(
    _ACTIVE_PARSED_FILES.get("translation_reviews", "data/translation_reviews.json")
)

LEGACY_QUESTIONS_PATH = repo_path("questions.json")
LEGACY_ROOT_WORD_BANK_PATH = repo_path("word_bank.json")
LEGACY_PASUK_FLOW_PREVIEW_PATH = repo_path("pasuk_flow_questions.json")
LEGACY_PASUK_FLOWS_PATH = repo_path("pasuk_flows.json")

ACTIVE_DATASET_PATHS = {
    "pesukim": ACTIVE_PARSED_PESUKIM_PATH,
    "word_bank": ACTIVE_WORD_BANK_PATH,
    "word_occurrences": ACTIVE_WORD_OCCURRENCES_PATH,
    "translation_reviews": ACTIVE_TRANSLATION_REVIEWS_PATH,
}


@lru_cache(maxsize=1)
def load_active_pesukim_data():
    with ACTIVE_PARSED_PESUKIM_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def active_pesukim_records():
    return tuple(load_active_pesukim_data().get("pesukim", []))


def active_pasuk_texts():
    return tuple(
        record.get("text", "")
        for record in active_pesukim_records()
        if record.get("text")
    )


@lru_cache(maxsize=1)
def active_pasuk_text_set():
    return frozenset(active_pasuk_texts())


def is_active_pasuk_text(text):
    return text in active_pasuk_text_set()


def active_pasuk_refs():
    refs = []
    for record in active_pesukim_records():
        ref = record.get("ref", {})
        refs.append(
            {
                "pasuk_id": record.get("pasuk_id"),
                "sefer": ref.get("sefer"),
                "perek": ref.get("perek"),
                "pasuk": ref.get("pasuk"),
            }
        )
    return tuple(refs)


def active_scope_metadata():
    metadata = get_scope_metadata(ACTIVE_ASSESSMENT_SCOPE)
    if not metadata:
        metadata = dict(_MANIFEST_ACTIVE_SCOPE)
    return metadata


def active_scope_summary():
    scope_metadata = active_scope_metadata()
    refs = active_pasuk_refs()
    return {
        "scope": ACTIVE_ASSESSMENT_SCOPE,
        "sefer": scope_metadata.get("sefer"),
        "range": scope_metadata.get("range"),
        "status": scope_metadata.get("status"),
        "pesukim_count": len(refs),
        "first_ref": refs[0] if refs else None,
        "last_ref": refs[-1] if refs else None,
        "paths": {key: str(path) for key, path in ACTIVE_DATASET_PATHS.items()},
    }


def active_runtime_contract():
    return {
        "supported_runtime": SUPPORTED_RUNTIME_NAME,
        "runtime_entrypoint": SUPPORTED_RUNTIME_ENTRYPOINT,
        "supported_practice_types": SUPPORTED_PRACTICE_TYPES,
        "active_scope": ACTIVE_ASSESSMENT_SCOPE,
        "active_scope_status": active_scope_metadata().get("status"),
        "active_dataset_paths": {key: str(path) for key, path in ACTIVE_DATASET_PATHS.items()},
        "active_pesukim_count": len(active_pasuk_refs()),
    }
