# Sefaria Bereishis English Translation Source Package

This package stores a source-traceable, license-aware English translation pipeline for Sefer Bereishis.

## Why this exists

- Future translation-skill diagnostics need verse-aligned English text, not chapter blobs.
- The canonical Hebrew TSV is the alignment backbone, so every English row maps to an existing Hebrew ref.
- This package is source-ingestion only. Nothing here is runtime-active or production-approved.

## Which Sefaria endpoints were used

- Version discovery: `https://www.sefaria.org/api/texts/versions/Genesis`
- Chapter text retrieval: `https://www.sefaria.org/api/v3/texts/Genesis.{chapter}` with `version=english|{exact versionTitle}`, `return_format=text_only`, and `fill_in_missing_segments=0`.

## Which target versions were found

- Koren exact match found: `True` (`The Koren Jerusalem Bible`)
- Metsudah exact match found: `True` (`Metsudah Chumash, Metsudah Publications, 2009`)
- Total English Genesis versions discovered: `43`
- Final canonical Hebrew ref count: `1533`

## What was fetched and persisted

- Koren text fetched: `True`
- Koren text persisted: `True`
- Metsudah text fetched: `True`
- Metsudah text persisted: `True`
- Koren final row count: `1533`
- Metsudah final row count: `1533`

## License metadata and review status

- Koren license metadata: `CC-BY-NC`
- Metsudah license metadata: `CC-BY`
- Both versions remain human-review-only for future production use.
- API availability does not equal production reuse approval.
- License review matrix: `data/source_texts/translations/sefaria/bereishis_english_translation_license_review_matrix.json`
- Human review packet: `data/source_texts/translations/sefaria/bereishis_english_translation_human_review_packet.md`

## What happened with Genesis 35:30

- The prior canonical Hebrew TSV incorrectly included an extra row labeled `Bereishis 35:30`.
- Sefaria Hebrew `Miqra according to the Masorah` and both English translations end chapter 35 at verse 29.
- The extra local row duplicated the burial verse of Yitzchak, so the canonical Hebrew TSV was corrected to `1533` refs.
- Reconciliation report: `data/source_texts/reports/bereishis_hebrew_source_reconciliation_report.md`

## How to rerun

```powershell
python scripts/fetch_sefaria_bereishis_translations.py --target koren --target metsudah
python scripts/validate_bereishis_translations.py
```

## What the next branch should do

- Review the fetched translations for pedagogy and licensing, then build a non-runtime translation-review layer or diagnostic integration layer that uses the translation registry without activating runtime.
