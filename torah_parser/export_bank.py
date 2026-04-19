"""Build local parser JSON files from stored pesukim or source corpus chunks."""

import json
from pathlib import Path

from assessment_scope import resolve_repo_path

from .candidate_generator import generate_candidate_analyses
from .disambiguate import select_best_candidate
from .normalize import normalize_form, preserve_surface_text
from .tokenize import tokenize_pasuk_record


PARSED_CORPUS_SCHEMA_VERSION = "0.1"
DEFAULT_REVIEW_STATUS = "needs_review"


def load_json(path, default):
    file_path = resolve_repo_path(path)
    if not file_path.exists():
        return default
    return json.loads(file_path.read_text(encoding="utf-8"))


def write_json(path, data):
    resolve_repo_path(path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def pasuk_id_from_ref(ref):
    sefer = str(ref.get("sefer", "unknown")).strip().lower().replace(" ", "_")
    perek = ref.get("perek", "x")
    pasuk = ref.get("pasuk", "x")
    return f"{sefer}_{perek}_{pasuk}"


def source_record_to_runtime_pasuk(source_record):
    ref = {
        "sefer": source_record.get("sefer"),
        "perek": source_record.get("perek"),
        "pasuk": source_record.get("pasuk"),
    }
    text = preserve_surface_text(source_record.get("text", ""))
    return {
        "pasuk_id": pasuk_id_from_ref(ref),
        "ref": ref,
        "text": text,
        "tokens": [item["surface"] for item in tokenize_pasuk_record({"pasuk_id": pasuk_id_from_ref(ref), "text": text})],
    }


def source_records_to_runtime_pesukim(source_records):
    return [source_record_to_runtime_pasuk(record) for record in source_records]


def _range_metadata(pesukim):
    refs = [pasuk.get("ref", {}) for pasuk in pesukim if pasuk.get("ref")]
    first = refs[0] if refs else {}
    last = refs[-1] if refs else {}
    sefarim = {ref.get("sefer") for ref in refs if ref.get("sefer")}
    return {
        "sefer": next(iter(sefarim)) if len(sefarim) == 1 else "mixed",
        "range": {
            "start": {
                "sefer": first.get("sefer"),
                "perek": first.get("perek"),
                "pasuk": first.get("pasuk"),
            },
            "end": {
                "sefer": last.get("sefer"),
                "perek": last.get("perek"),
                "pasuk": last.get("pasuk"),
            },
        },
    }


def _artifact_metadata(title, artifact_type, pesukim, source_files=None, corpus_id=None, status="parsed", extra=None):
    range_data = _range_metadata(pesukim)
    metadata = {
        "title": title,
        "version": PARSED_CORPUS_SCHEMA_VERSION,
        "artifact_type": artifact_type,
        "corpus_id": corpus_id,
        "status": status,
        "pesukim_count": len(pesukim),
        "sefer": range_data["sefer"],
        "range": range_data["range"],
        "source_files": list(source_files or []),
    }
    if extra:
        metadata.update(extra)
    return metadata


def build_word_bank(pesukim):
    words = {}
    for pasuk in pesukim:
        pasuk_id = pasuk["pasuk_id"]
        for occurrence in tokenize_pasuk_record(pasuk):
            surface = occurrence["surface"]
            if surface in words:
                for analysis in words[surface]:
                    refs = analysis.setdefault("source_refs", [])
                    if pasuk_id not in refs:
                        refs.append(pasuk_id)
                continue

            analyses = generate_candidate_analyses(surface)
            for analysis in analyses:
                analysis["source_refs"] = [pasuk_id]
            words[surface] = analyses
    return words


def build_occurrences(pesukim, word_bank):
    occurrences = []
    for pasuk in pesukim:
        for occurrence in tokenize_pasuk_record(pasuk):
            surface = occurrence["surface"]
            analyses = word_bank.get(surface, [])
            selected = select_best_candidate(analyses)
            analysis_index = analyses.index(selected) if selected in analyses else 0
            occurrences.append(
                {
                    "pasuk_id": occurrence["pasuk_id"],
                    "token_index": occurrence["token_index"],
                    "surface": surface,
                    "normalized": normalize_form(surface),
                    "analysis_index": analysis_index,
                }
            )
    return occurrences


def build_parsed_pesukim(pesukim, word_bank, occurrences):
    occurrence_index = {
        (item["pasuk_id"], item["token_index"]): item
        for item in occurrences
    }
    parsed_pesukim = []
    for pasuk in pesukim:
        token_records = []
        for occurrence in tokenize_pasuk_record(pasuk):
            key = (occurrence["pasuk_id"], occurrence["token_index"])
            occurrence_record = occurrence_index.get(key, occurrence)
            analyses = word_bank.get(occurrence["surface"], [])
            selected = select_best_candidate(analyses, occurrence_record)
            selected_index = occurrence_record.get("analysis_index", 0)
            token_records.append(
                {
                    "pasuk_id": occurrence["pasuk_id"],
                    "source_ref": dict(pasuk.get("ref", {})),
                    "token_index": occurrence["token_index"],
                    "surface": occurrence["surface"],
                    "normalized": occurrence_record.get("normalized", normalize_form(occurrence["surface"])),
                    "analysis_index": selected_index,
                    "analysis_count": len(analyses),
                    "selected_analysis": dict(selected) if selected else None,
                }
            )
        parsed_pesukim.append(
            {
                "pasuk_id": pasuk.get("pasuk_id"),
                "ref": dict(pasuk.get("ref", {})),
                "source_ref": dict(pasuk.get("ref", {})),
                "text": preserve_surface_text(pasuk.get("text", "")),
                "tokens": list(pasuk.get("tokens", [])),
                "token_records": token_records,
            }
        )
    return parsed_pesukim


def build_translation_reviews_stub(pesukim, source_files=None, corpus_id=None, status="parsed"):
    return {
        "metadata": _artifact_metadata(
            title="Generated Torah Translation Reviews",
            artifact_type="translation_reviews",
            pesukim=pesukim,
            source_files=source_files,
            corpus_id=corpus_id,
            status=status,
            extra={
                "notes": (
                    "Stub review artifact created during parsed corpus ingestion. "
                    "Human review records can be added incrementally."
                ),
            },
        ),
        "reviews": [],
    }


def build_parsed_corpus_artifacts(source_corpus, corpus_id=None, status="parsed", source_files=None):
    source_metadata = source_corpus.get("metadata", {}) if isinstance(source_corpus, dict) else {}
    source_records = source_corpus.get("pesukim", []) if isinstance(source_corpus, dict) else list(source_corpus or [])
    runtime_pesukim = source_records_to_runtime_pesukim(source_records)
    word_bank = build_word_bank(runtime_pesukim)
    occurrences = build_occurrences(runtime_pesukim, word_bank)
    parsed_pesukim = build_parsed_pesukim(runtime_pesukim, word_bank, occurrences)
    declared_range = source_metadata.get("range")

    return {
        "metadata": {
            "schema_version": PARSED_CORPUS_SCHEMA_VERSION,
            "corpus_id": corpus_id,
            "status": status,
            "source_metadata": source_metadata,
            "source_files": list(source_files or []),
        },
        "pesukim": {
            "metadata": _artifact_metadata(
                title="Generated Torah Runtime Pesukim",
                artifact_type="runtime_pesukim",
                pesukim=runtime_pesukim,
                source_files=source_files,
                corpus_id=corpus_id,
                status=status,
                extra={"declared_source_range": declared_range},
            ),
            "pesukim": runtime_pesukim,
        },
        "parsed_pesukim": {
            "metadata": _artifact_metadata(
                title="Generated Parsed Torah Pesukim",
                artifact_type="parsed_pesukim",
                pesukim=runtime_pesukim,
                source_files=source_files,
                corpus_id=corpus_id,
                status=status,
                extra={"declared_source_range": declared_range},
            ),
            "parsed_pesukim": parsed_pesukim,
        },
        "word_bank": {
            "metadata": _artifact_metadata(
                title="Generated Torah Word Bank",
                artifact_type="word_bank",
                pesukim=runtime_pesukim,
                source_files=source_files,
                corpus_id=corpus_id,
                status=status,
                extra={"declared_source_range": declared_range},
            ),
            "words": word_bank,
        },
        "word_occurrences": {
            "metadata": _artifact_metadata(
                title="Generated Torah Word Occurrences",
                artifact_type="word_occurrences",
                pesukim=runtime_pesukim,
                source_files=source_files,
                corpus_id=corpus_id,
                status=status,
                extra={"declared_source_range": declared_range},
            ),
            "occurrences": occurrences,
        },
        "translation_reviews": build_translation_reviews_stub(
            runtime_pesukim,
            source_files=source_files,
            corpus_id=corpus_id,
            status=status,
        ),
    }


def write_parsed_corpus_artifacts(output_dir, artifacts):
    output_path = resolve_repo_path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    write_json(output_path / "pesukim.json", artifacts["pesukim"])
    write_json(output_path / "parsed_pesukim.json", artifacts["parsed_pesukim"])
    write_json(output_path / "word_bank.json", artifacts["word_bank"])
    write_json(output_path / "word_occurrences.json", artifacts["word_occurrences"])
    write_json(output_path / "translation_reviews.json", artifacts["translation_reviews"])


def load_source_corpus(path):
    return load_json(path, {"metadata": {}, "pesukim": []})


def merge_source_corpora(source_corpora):
    corpora = [corpus for corpus in (source_corpora or []) if corpus]
    if not corpora:
        return {"metadata": {}, "pesukim": []}

    records = []
    for corpus in corpora:
        records.extend(corpus.get("pesukim", []))

    if not records:
        metadata = dict(corpora[0].get("metadata", {}))
        return {"metadata": metadata, "pesukim": []}

    first = records[0]
    last = records[-1]
    first_metadata = corpora[0].get("metadata", {})
    return {
        "metadata": {
            "title": first_metadata.get("title"),
            "range": f"{first.get('perek')}:{first.get('pasuk')}-{last.get('perek')}:{last.get('pasuk')}",
            "format": first_metadata.get("format"),
        },
        "pesukim": records,
    }


def load_source_corpora(paths):
    path_list = list(paths or [])
    corpora = [load_source_corpus(path) for path in path_list]
    return merge_source_corpora(corpora)


def build_staged_corpus_from_source(
    source_path,
    output_dir=None,
    corpus_id=None,
    status="parsed",
):
    source_corpus = load_source_corpus(source_path)
    artifacts = build_parsed_corpus_artifacts(
        source_corpus,
        corpus_id=corpus_id,
        status=status,
        source_files=[str(Path(source_path).as_posix())],
    )
    if output_dir is not None:
        write_parsed_corpus_artifacts(output_dir, artifacts)
    return artifacts


def build_local_bank(
    pesukim_path="data/pesukim_100.json",
    word_bank_path="data/word_bank.json",
    occurrences_path="data/word_occurrences.json",
):
    pesukim_data = load_json(pesukim_path, {"pesukim": []})
    word_bank = build_word_bank(pesukim_data.get("pesukim", []))
    occurrences = build_occurrences(pesukim_data.get("pesukim", []), word_bank)

    write_json(
        word_bank_path,
        {
            "metadata": {
                "title": "Generated Torah Word Bank",
                "version": "0.1",
                "source_pesukim_file": resolve_repo_path(pesukim_path).name,
            },
            "words": word_bank,
        },
    )
    write_json(
        occurrences_path,
        {
            "metadata": {
                "title": "Generated Torah Word Occurrences",
                "version": "0.1",
                "source_pesukim_file": resolve_repo_path(pesukim_path).name,
                "source_word_bank_file": resolve_repo_path(word_bank_path).name,
            },
            "occurrences": occurrences,
        },
    )
