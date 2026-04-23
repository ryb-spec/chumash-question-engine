"""Active local assessment dataset scope.

Runtime assessment content should come from the parsed local Torah dataset only.
Legacy preview/static files may still exist in the repo, but they are not part
of the active assessment scope.
"""

import json
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

from torah_parser.word_bank_adapter import normalize_hebrew_key


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
    "source",
    "staged",
    "review_needed",
    "active_candidate",
    "active",
)
LEGACY_CORPUS_STATUS_ALIASES = {
    "experimental": "source",
    "parsed": "staged",
    "reviewed": "review_needed",
}


def normalize_corpus_status(status):
    if status is None:
        return None
    return LEGACY_CORPUS_STATUS_ALIASES.get(status, status)


def _canonicalize_manifest(manifest):
    canonical = deepcopy(manifest or {})
    metadata = canonical.setdefault("metadata", {})
    metadata["status_values"] = list(CORPUS_STATUS_VALUES)
    for collection_name in ("source_corpora", "parsed_corpora", "scopes", "future_scopes"):
        for item in canonical.get(collection_name, []):
            if isinstance(item, dict):
                item["status"] = normalize_corpus_status(item.get("status"))
    return canonical


def _default_corpus_manifest():
    active_runtime_source_files = [
        "data/source/bereishis_1_1_to_1_30.json",
        "data/source/bereishis_1_31_to_2_9.json",
        "data/source/bereishis_2_10_to_2_17.json",
        "data/source/bereishis_2_18_to_2_25.json",
        "data/source/bereishis_3_1_to_3_8.json",
        "data/source/bereishis_3_9_to_3_16.json",
        "data/source/bereishis_3_17_to_3_24.json",
    ]
    prepared_source_files = [
        "data/source/bereishis_1_1_to_1_30.json",
        "data/source/bereishis_1_31_to_2_9.json",
        "data/source/bereishis_2_10_to_2_17.json",
        "data/source/bereishis_2_18_to_2_25.json",
        "data/source/bereishis_3_1_to_3_8.json",
        "data/source/bereishis_3_9_to_3_16.json",
    ]
    parsed_files = {
        "pesukim": "data/pesukim_100.json",
        "parsed_pesukim": "data/parsed_pesukim.json",
        "word_bank": "data/word_bank.json",
        "word_occurrences": "data/word_occurrences.json",
        "translation_reviews": "data/translation_reviews.json",
    }
    staged_next_chunk_files = {
        "pesukim": "data/staged/parsed_bereishis_3_9_to_3_16_staged/pesukim.json",
        "parsed_pesukim": "data/staged/parsed_bereishis_3_9_to_3_16_staged/parsed_pesukim.json",
        "word_bank": "data/staged/parsed_bereishis_3_9_to_3_16_staged/word_bank.json",
        "word_occurrences": "data/staged/parsed_bereishis_3_9_to_3_16_staged/word_occurrences.json",
        "translation_reviews": "data/staged/parsed_bereishis_3_9_to_3_16_staged/translation_reviews.json",
        "reviewed_questions": "data/staged/parsed_bereishis_3_9_to_3_16_staged/reviewed_questions.json",
    }
    staged_future_chunk_files = {
        "pesukim": "data/staged/parsed_bereishis_3_17_to_3_24_staged/pesukim.json",
        "parsed_pesukim": "data/staged/parsed_bereishis_3_17_to_3_24_staged/parsed_pesukim.json",
        "word_bank": "data/staged/parsed_bereishis_3_17_to_3_24_staged/word_bank.json",
        "word_occurrences": "data/staged/parsed_bereishis_3_17_to_3_24_staged/word_occurrences.json",
        "translation_reviews": "data/staged/parsed_bereishis_3_17_to_3_24_staged/translation_reviews.json",
        "reviewed_questions": "data/staged/parsed_bereishis_3_17_to_3_24_staged/reviewed_questions.json",
    }
    promoted_staged_chunk_files = {
        "pesukim": "data/staged/parsed_bereishis_3_1_to_3_8_staged/pesukim.json",
        "parsed_pesukim": "data/staged/parsed_bereishis_3_1_to_3_8_staged/parsed_pesukim.json",
        "word_bank": "data/staged/parsed_bereishis_3_1_to_3_8_staged/word_bank.json",
        "word_occurrences": "data/staged/parsed_bereishis_3_1_to_3_8_staged/word_occurrences.json",
        "translation_reviews": "data/staged/parsed_bereishis_3_1_to_3_8_staged/translation_reviews.json",
        "reviewed_questions": "data/staged/parsed_bereishis_3_1_to_3_8_staged/reviewed_questions.json",
    }
    return {
        "metadata": {
            "title": "Chumash Corpus Manifest",
            "version": "0.1",
            "status_values": list(CORPUS_STATUS_VALUES),
            "notes": (
                "Registry for source corpora, parsed corpora, and runtime scopes. "
                "Lifecycle states are source -> staged -> review_needed -> "
                "active_candidate -> active. The data/ root files remain the "
                "current blessed runtime layer."
            ),
        },
        "source_corpora": [
            {
                "corpus_id": "source_bereishis_1_1_to_3_16_local",
                "type": "source_corpus",
                "sefer": "Bereishis",
                "range": {
                    "start": {"perek": 1, "pasuk": 1},
                    "end": {"perek": 3, "pasuk": 16},
                },
                "pesukim_count": 72,
                "source_files": list(prepared_source_files),
                "parsed_files": {},
                "status": "source",
                "declared_source_range": "1:1-3:16",
                "notes": [
                    "Current local source corpus is prepared through Bereishis 3:16.",
                    "The active parsed runtime includes Bereishis 3:17-3:24, pending source corpus backfill.",
                ],
            }
        ],
        "parsed_corpora": [
            {
                "corpus_id": "parsed_bereishis_1_1_to_3_24_root",
                "type": "parsed_corpus",
                "sefer": "Bereishis",
                "range": {
                    "start": {"perek": 1, "pasuk": 1},
                    "end": {"perek": 3, "pasuk": 24},
                },
                "pesukim_count": 80,
                "source_files": list(active_runtime_source_files),
                "parsed_files": dict(parsed_files),
                "status": "active",
                "storage_layer": "data_root",
                "notes": [
                    "Current blessed parsed runtime layer stored in data/ root.",
                    "Contains reviewed and parsed-only enrichment used by the active app through Bereishis 3:24.",
                ],
            },
            {
                "corpus_id": "parsed_bereishis_3_1_to_3_8_staged",
                "type": "parsed_corpus",
                "sefer": "Bereishis",
                "range": {
                    "start": {"perek": 3, "pasuk": 1},
                    "end": {"perek": 3, "pasuk": 8},
                },
                "pesukim_count": 8,
                "source_files": ["data/source/bereishis_3_1_to_3_8.json"],
                "parsed_files": dict(promoted_staged_chunk_files),
                "status": "active",
                "storage_layer": "data_staged",
                "readiness_report": "data/validation/bereishis_3_1_to_3_8_readiness.json",
                "notes": [
                    "Promoted contiguous parsed bundle retained as staged-source provenance for Bereishis 3:1-3:8.",
                    "The active runtime now includes this slice via the root parsed runtime corpus.",
                ],
            },
            {
                "corpus_id": "parsed_bereishis_3_17_to_3_24_staged",
                "type": "parsed_corpus",
                "sefer": "Bereishis",
                "range": {
                    "start": {"perek": 3, "pasuk": 17},
                    "end": {"perek": 3, "pasuk": 24},
                },
                "pesukim_count": 8,
                "source_files": ["data/source/bereishis_3_17_to_3_24.json"],
                "parsed_files": dict(staged_future_chunk_files),
                "status": "active",
                "storage_layer": "data_staged",
                "readiness_report": "data/validation/bereishis_3_17_to_3_24_readiness.json",
                "notes": [
                    "Promoted contiguous parsed bundle retained as staged-source provenance for Bereishis 3:17-3:24.",
                    "The active runtime now includes this slice via the root parsed runtime corpus.",
                ],
            },
            {
                "corpus_id": "parsed_bereishis_3_9_to_3_16_staged",
                "type": "parsed_corpus",
                "sefer": "Bereishis",
                "range": {
                    "start": {"perek": 3, "pasuk": 9},
                    "end": {"perek": 3, "pasuk": 16},
                },
                "pesukim_count": 8,
                "source_files": ["data/source/bereishis_3_9_to_3_16.json"],
                "parsed_files": dict(staged_next_chunk_files),
                "status": "active",
                "storage_layer": "data_staged",
                "readiness_report": "data/validation/bereishis_3_9_to_3_16_readiness.json",
                "notes": [
                    "Promoted contiguous parsed bundle retained as staged-source provenance for Bereishis 3:9-3:16.",
                    "The active runtime now includes this slice via the root parsed runtime corpus.",
                ],
            },
        ],
        "scopes": [
            {
                "scope_id": "local_parsed_bereishis_1_1_to_3_24",
                "type": "runtime_scope",
                "sefer": "Bereishis",
                "range": {
                    "start": {"perek": 1, "pasuk": 1},
                    "end": {"perek": 3, "pasuk": 24},
                },
                "pesukim_count": 80,
                "source_corpus_id": "source_bereishis_1_1_to_3_24_local",
                "parsed_corpus_id": "parsed_bereishis_1_1_to_3_24_root",
                "source_files": list(active_runtime_source_files),
                "parsed_files": dict(parsed_files),
                "status": "active",
                "supported_runtime": True,
                "notes": [
                    "Current supported Streamlit runtime scope.",
                    "Backward-compatible with existing data/ root runtime paths while extending through Bereishis 3:24.",
                ],
            }
        ],
        "future_scopes": [],
    }


@lru_cache(maxsize=1)
def load_corpus_manifest():
    if not CORPUS_MANIFEST_PATH.exists():
        return _canonicalize_manifest(_default_corpus_manifest())
    with CORPUS_MANIFEST_PATH.open("r", encoding="utf-8") as file:
        return _canonicalize_manifest(json.load(file))


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
    "local_parsed_bereishis_1_1_to_3_24",
)

_ACTIVE_PARSED_FILES = _MANIFEST_ACTIVE_SCOPE.get("parsed_files", {})

ACTIVE_PARSED_PESUKIM_PATH = resolve_repo_path(
    _ACTIVE_PARSED_FILES.get("pesukim", "data/pesukim_100.json")
)
ACTIVE_PARSED_ANALYSIS_PATH = resolve_repo_path(
    _ACTIVE_PARSED_FILES.get("parsed_pesukim", "data/parsed_pesukim.json")
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
ACTIVE_SCOPE_OVERRIDES_PATH = resolve_repo_path("data/active_scope_overrides.json")
ACTIVE_SCOPE_GOLD_ANNOTATIONS_PATH = resolve_repo_path("data/active_scope_gold_annotations.json")
ACTIVE_SCOPE_REVIEWED_QUESTIONS_PATH = resolve_repo_path("data/active_scope_reviewed_questions.json")

PREVIEW_ARTIFACTS_DIR = repo_path("artifacts", "preview")
LEGACY_DIR = repo_path("legacy")

LEGACY_GENERATED_QUESTIONS_PREVIEW_PATH = PREVIEW_ARTIFACTS_DIR / "generated_questions_preview.json"
LEGACY_GRAMMAR_QUESTIONS_PREVIEW_PATH = PREVIEW_ARTIFACTS_DIR / "grammar_questions_preview.json"
LEGACY_QUESTIONS_PATH = PREVIEW_ARTIFACTS_DIR / "questions.json"
LEGACY_QUESTIONS_HTML_PATH = PREVIEW_ARTIFACTS_DIR / "questions.html"
LEGACY_ENHANCED_QUIZ_HTML_PATH = PREVIEW_ARTIFACTS_DIR / "enhanced_quiz.html"
LEGACY_PREVIEW_INDEX_PATH = PREVIEW_ARTIFACTS_DIR / "index.html"
LEGACY_ROOT_WORD_BANK_PATH = repo_path("word_bank.json")
LEGACY_PASUK_FLOW_PREVIEW_PATH = PREVIEW_ARTIFACTS_DIR / "pasuk_flow_questions.json"
LEGACY_PASUK_FLOWS_PATH = PREVIEW_ARTIFACTS_DIR / "pasuk_flows.json"
LEGACY_GOOGLE_DOCS_EXPORT_PATH = LEGACY_DIR / "chumash_question_bank_google_docs_export.html"

ACTIVE_DATASET_PATHS = {
    "pesukim": ACTIVE_PARSED_PESUKIM_PATH,
    "parsed_pesukim": ACTIVE_PARSED_ANALYSIS_PATH,
    "word_bank": ACTIVE_WORD_BANK_PATH,
    "word_occurrences": ACTIVE_WORD_OCCURRENCES_PATH,
    "translation_reviews": ACTIVE_TRANSLATION_REVIEWS_PATH,
    "active_scope_overrides": ACTIVE_SCOPE_OVERRIDES_PATH,
    "active_scope_gold_annotations": ACTIVE_SCOPE_GOLD_ANNOTATIONS_PATH,
    "active_scope_reviewed_questions": ACTIVE_SCOPE_REVIEWED_QUESTIONS_PATH,
}


@lru_cache(maxsize=1)
def load_active_pesukim_data():
    with ACTIVE_PARSED_PESUKIM_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


@lru_cache(maxsize=1)
def load_active_parsed_pesukim_data():
    if not ACTIVE_PARSED_ANALYSIS_PATH.exists():
        return {"metadata": {}, "parsed_pesukim": []}
    with ACTIVE_PARSED_ANALYSIS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def active_pesukim_records():
    return tuple(load_active_pesukim_data().get("pesukim", []))


def active_parsed_pesukim_records():
    return tuple(load_active_parsed_pesukim_data().get("parsed_pesukim", []))


@lru_cache(maxsize=1)
def _active_pesukim_by_text():
    return {
        record.get("text"): record
        for record in active_pesukim_records()
        if record.get("text")
    }


@lru_cache(maxsize=1)
def _active_pesukim_by_normalized_text():
    return {
        normalize_hebrew_key(record.get("text")): record
        for record in active_pesukim_records()
        if record.get("text")
    }


@lru_cache(maxsize=1)
def _active_pesukim_by_id():
    return {
        record.get("pasuk_id"): record
        for record in active_pesukim_records()
        if record.get("pasuk_id")
    }


def active_pasuk_record_for_text(text):
    if not text:
        return None
    return _active_pesukim_by_text().get(text) or _active_pesukim_by_normalized_text().get(
        normalize_hebrew_key(text)
    )


def active_pasuk_record_for_pasuk_id(pasuk_id):
    if not pasuk_id:
        return None
    return _active_pesukim_by_id().get(pasuk_id)


def active_pasuk_record_for_question(question, fallback_text=None):
    question = question or {}
    embedded_ref = question.get("pasuk_ref") or {}
    record = active_pasuk_record_for_pasuk_id(
        question.get("pasuk_id")
        or question.get("override_pasuk_id")
        or embedded_ref.get("pasuk_id")
    )
    explicit_pasuk = question.get("pasuk")
    selected_word = question.get("selected_word") or question.get("word")
    if not record and explicit_pasuk:
        record = active_pasuk_record_for_text(explicit_pasuk)
    if (
        not record
        and fallback_text
        and (
            not explicit_pasuk
            or normalize_hebrew_key(explicit_pasuk) == normalize_hebrew_key(selected_word)
        )
    ):
        record = active_pasuk_record_for_text(fallback_text)
    return record


def active_pasuk_ref_payload(record):
    if not record:
        return None
    ref = record.get("ref", {})
    return {
        "sefer": ref.get("sefer"),
        "perek": ref.get("perek"),
        "pasuk": ref.get("pasuk"),
        "label": f"{ref.get('sefer')} {ref.get('perek')}:{ref.get('pasuk')}",
        "pasuk_id": record.get("pasuk_id"),
    }


def bind_question_to_active_scope(question, fallback_text=None):
    record = active_pasuk_record_for_question(question, fallback_text=fallback_text)
    if not question or not record:
        return None
    explicit_pasuk = question.get("pasuk")
    selected_word = question.get("selected_word") or question.get("word")
    if (
        not explicit_pasuk
        or normalize_hebrew_key(explicit_pasuk) == normalize_hebrew_key(selected_word)
    ):
        question["pasuk"] = record.get("text") or fallback_text
    question.setdefault("pasuk_id", record.get("pasuk_id"))
    question.setdefault("pasuk_ref", active_pasuk_ref_payload(record))
    return record


@lru_cache(maxsize=1)
def _active_parsed_pesukim_by_text():
    return {
        record.get("text"): record
        for record in active_parsed_pesukim_records()
        if record.get("text")
    }


def active_parsed_pasuk_record_for_text(text):
    return _active_parsed_pesukim_by_text().get(text)


def active_pasuk_texts():
    return tuple(
        record.get("text", "")
        for record in active_pesukim_records()
        if record.get("text")
    )


@lru_cache(maxsize=1)
def active_pasuk_text_set():
    return frozenset(active_pasuk_texts())


@lru_cache(maxsize=1)
def active_pasuk_id_set():
    return frozenset(
        record.get("pasuk_id")
        for record in active_pesukim_records()
        if record.get("pasuk_id")
    )


def is_active_pasuk_text(text):
    return text in active_pasuk_text_set()


def _default_active_scope_overrides():
    return {
        "metadata": {
            "title": "Active Scope Curated Overrides",
            "scope_id": ACTIVE_ASSESSMENT_SCOPE,
            "status": "active",
        },
        "overrides": {},
    }


def _default_active_scope_gold_annotations():
    return {
        "metadata": {
            "title": "Active Scope Gold Annotations",
            "scope_id": ACTIVE_ASSESSMENT_SCOPE,
            "status": "active",
        },
        "annotations": {},
    }


def _default_active_scope_reviewed_questions():
    return {
        "metadata": {
            "title": "Active Scope Reviewed Questions",
            "scope_id": ACTIVE_ASSESSMENT_SCOPE,
            "status": "active",
        },
        "questions": [],
    }


def _canonicalize_active_scope_overrides(payload):
    canonical = deepcopy(payload or {})
    metadata = canonical.setdefault("metadata", {})
    metadata.setdefault("title", "Active Scope Curated Overrides")
    metadata.setdefault("scope_id", ACTIVE_ASSESSMENT_SCOPE)
    metadata.setdefault("status", "active")

    raw_overrides = canonical.get("overrides", {})
    if not isinstance(raw_overrides, dict):
        raise ValueError("Active scope overrides must store overrides as an object keyed by pasuk_id.")

    normalized = {}
    for pasuk_id, override in raw_overrides.items():
        if not isinstance(override, dict):
            raise ValueError(f"Active scope override for {pasuk_id} must be an object.")
        item = deepcopy(override)
        item.setdefault("skills", {})
        if not isinstance(item["skills"], dict):
            raise ValueError(f"Active scope override skills for {pasuk_id} must be an object.")
        normalized[pasuk_id] = item

    canonical["overrides"] = normalized
    return canonical


def _canonicalize_active_scope_gold_annotations(payload):
    canonical = deepcopy(payload or {})
    metadata = canonical.setdefault("metadata", {})
    metadata.setdefault("title", "Active Scope Gold Annotations")
    metadata.setdefault("scope_id", ACTIVE_ASSESSMENT_SCOPE)
    metadata.setdefault("status", "active")

    raw_annotations = canonical.get("annotations", {})
    if not isinstance(raw_annotations, dict):
        raise ValueError("Active scope gold annotations must store annotations as an object keyed by pasuk_id.")

    normalized = {}
    for pasuk_id, annotation in raw_annotations.items():
        if not isinstance(annotation, dict):
            raise ValueError(f"Gold annotation for {pasuk_id} must be an object.")
        item = deepcopy(annotation)
        item.setdefault("skills", {})
        if not isinstance(item["skills"], dict):
            raise ValueError(f"Gold annotation skills for {pasuk_id} must be an object.")
        for skill_name, skill_record in item["skills"].items():
            if not isinstance(skill_record, dict):
                raise ValueError(f"Gold annotation for {pasuk_id}/{skill_name} must be an object.")
            status = skill_record.get("status")
            if status not in {"approved", "suppressed"}:
                raise ValueError(
                    f"Gold annotation for {pasuk_id}/{skill_name} must have status 'approved' or 'suppressed'."
                )
            if status == "approved":
                approved_targets = skill_record.get("approved_targets")
                if not isinstance(approved_targets, list) or not approved_targets:
                    raise ValueError(
                        f"Gold annotation for {pasuk_id}/{skill_name} must include a non-empty approved_targets list."
                    )
            if status == "suppressed" and not skill_record.get("reason"):
                raise ValueError(
                    f"Gold annotation for {pasuk_id}/{skill_name} must include a suppression reason."
                )
        normalized[pasuk_id] = item

    canonical["annotations"] = normalized
    return canonical


def _canonicalize_active_scope_reviewed_questions(payload):
    canonical = deepcopy(payload or {})
    metadata = canonical.setdefault("metadata", {})
    metadata.setdefault("title", "Active Scope Reviewed Questions")
    metadata.setdefault("scope_id", ACTIVE_ASSESSMENT_SCOPE)
    metadata.setdefault("status", "active")

    raw_questions = canonical.get("questions", [])
    if not isinstance(raw_questions, list):
        raise ValueError("Active scope reviewed questions must store questions as a list.")

    normalized = []
    seen_ids = set()
    for item in raw_questions:
        if not isinstance(item, dict):
            raise ValueError("Each reviewed question must be an object.")
        question = deepcopy(item)
        reviewed_id = str(question.get("reviewed_id") or "").strip()
        if not reviewed_id:
            raise ValueError("Each reviewed question must include reviewed_id.")
        if reviewed_id in seen_ids:
            raise ValueError(f"Duplicate reviewed question id: {reviewed_id}")
        seen_ids.add(reviewed_id)
        skill = str(question.get("skill") or "").strip()
        if not skill:
            raise ValueError(f"Reviewed question {reviewed_id} must include skill.")
        pasuk_id = str(question.get("pasuk_id") or "").strip()
        if not pasuk_id:
            raise ValueError(f"Reviewed question {reviewed_id} must include pasuk_id.")
        alias_skills = question.get("alias_skills") or []
        if not isinstance(alias_skills, list):
            raise ValueError(f"Reviewed question {reviewed_id} alias_skills must be a list.")
        question["alias_skills"] = [str(value).strip() for value in alias_skills if str(value).strip()]
        question["review_family"] = str(question.get("review_family") or skill).strip()
        normalized.append(question)

    canonical["questions"] = normalized
    return canonical


@lru_cache(maxsize=1)
def load_active_scope_overrides_data():
    if not ACTIVE_SCOPE_OVERRIDES_PATH.exists():
        return _canonicalize_active_scope_overrides(_default_active_scope_overrides())
    with ACTIVE_SCOPE_OVERRIDES_PATH.open("r", encoding="utf-8") as file:
        return _canonicalize_active_scope_overrides(json.load(file))


@lru_cache(maxsize=1)
def load_active_scope_gold_annotations_data():
    if not ACTIVE_SCOPE_GOLD_ANNOTATIONS_PATH.exists():
        return _canonicalize_active_scope_gold_annotations(_default_active_scope_gold_annotations())
    with ACTIVE_SCOPE_GOLD_ANNOTATIONS_PATH.open("r", encoding="utf-8-sig") as file:
        return _canonicalize_active_scope_gold_annotations(json.load(file))


@lru_cache(maxsize=1)
def load_active_scope_reviewed_questions_data():
    if not ACTIVE_SCOPE_REVIEWED_QUESTIONS_PATH.exists():
        return _canonicalize_active_scope_reviewed_questions(_default_active_scope_reviewed_questions())
    with ACTIVE_SCOPE_REVIEWED_QUESTIONS_PATH.open("r", encoding="utf-8-sig") as file:
        return _canonicalize_active_scope_reviewed_questions(json.load(file))


def active_scope_override_records():
    return dict(load_active_scope_overrides_data().get("overrides", {}))


def active_scope_gold_annotation_records():
    return dict(load_active_scope_gold_annotations_data().get("annotations", {}))


def active_scope_reviewed_question_records():
    return tuple(load_active_scope_reviewed_questions_data().get("questions", []))


def active_scope_override_for_pasuk_id(pasuk_id):
    if pasuk_id not in active_pasuk_id_set():
        return None
    return active_scope_override_records().get(pasuk_id)


def active_scope_gold_annotation_for_pasuk_id(pasuk_id):
    if pasuk_id not in active_pasuk_id_set():
        return None
    return active_scope_gold_annotation_records().get(pasuk_id)


def active_scope_override_for_text(text):
    record = active_pasuk_record_for_text(text)
    if not record:
        return None
    return active_scope_override_for_pasuk_id(record.get("pasuk_id"))


def active_scope_gold_annotation_for_text(text):
    record = active_pasuk_record_for_text(text)
    if not record:
        return None
    return active_scope_gold_annotation_for_pasuk_id(record.get("pasuk_id"))


def gold_skill_record_for_text(text, skill):
    annotation = active_scope_gold_annotation_for_text(text)
    if not annotation:
        return None
    return (annotation.get("skills") or {}).get(skill)


def active_scope_reviewed_questions_for_pasuk_id(pasuk_id, skill=None):
    if pasuk_id not in active_pasuk_id_set():
        return tuple()
    requested_skill = str(skill or "").strip()
    matches = []
    for question in active_scope_reviewed_question_records():
        if question.get("pasuk_id") != pasuk_id:
            continue
        if not requested_skill:
            matches.append(deepcopy(question))
            continue
        supported_skills = {str(question.get("skill") or "").strip(), *question.get("alias_skills", [])}
        if (
            requested_skill == "translation"
            and str(question.get("review_family") or "").strip() == "translation"
            and str(question.get("skill") or "").strip() == "phrase_translation"
        ):
            supported_skills.add("translation")
        if requested_skill in supported_skills:
            matches.append(deepcopy(question))
    return tuple(matches)


def active_scope_reviewed_questions_for_text(text, skill=None):
    record = active_pasuk_record_for_text(text)
    if not record:
        return tuple()
    return active_scope_reviewed_questions_for_pasuk_id(record.get("pasuk_id"), skill=skill)


def _normalize_gold_translation(text):
    rendered = " ".join(str(text or "").split())
    lower = rendered.lower()
    if lower.startswith("and "):
        rendered = rendered[4:]
        lower = rendered.lower()
    if lower.startswith("he "):
        rendered = rendered[3:]
    return rendered


def question_matches_gold_skill_record(question, gold_skill_record):
    if not question or not gold_skill_record or question.get("status") == "skipped":
        return False

    if gold_skill_record.get("status") != "approved":
        return False

    skill = question.get("skill")
    selected = question.get("selected_word") or question.get("word")
    correct = question.get("correct_answer")
    action_token = question.get("action_token")
    role_focus = question.get("role_focus")

    for target in gold_skill_record.get("approved_targets", []):
        if skill == "subject_identification":
            if (
                target.get("surface") == selected
                and target.get("translation") == correct
                and target.get("main_verb_token") == action_token
            ):
                return True
        elif skill == "object_identification":
            target_role = target.get("role")
            if (
                target.get("surface") == selected
                and target.get("translation") == correct
                and target.get("main_verb_token") == action_token
                and (target_role is None or target_role == role_focus)
            ):
                return True
        elif skill == "phrase_translation":
            if (
                target.get("surface") == selected
                and _normalize_gold_translation(target.get("translation")) == _normalize_gold_translation(correct)
            ):
                return True
    return False


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
