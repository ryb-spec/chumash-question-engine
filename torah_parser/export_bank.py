"""Build local parser JSON files from stored pesukim."""

import json
from pathlib import Path

from .candidate_generator import generate_candidate_analyses
from .disambiguate import select_best_candidate
from .normalize import normalize_form
from .tokenize import tokenize_pasuk_record


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    return json.loads(file_path.read_text(encoding="utf-8"))


def write_json(path, data):
    Path(path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


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
                "source_pesukim_file": Path(pesukim_path).name,
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
                "source_pesukim_file": Path(pesukim_path).name,
                "source_word_bank_file": Path(word_bank_path).name,
            },
            "occurrences": occurrences,
        },
    )
