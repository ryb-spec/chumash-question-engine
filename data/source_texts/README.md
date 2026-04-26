# Source Texts

## Purpose

This folder stores canonical local source-text files that future extraction and source-alignment workflows can rely on directly.

## Why TSV Instead Of CSV

- TSV is safer for Hebrew text because commas in notes or metadata do not risk breaking column structure.
- One pasuk must appear on exactly one row.
- Files should be UTF-8 encoded.

## Required Columns

Canonical source-text TSV files must use these columns in this exact order:

1. `sefer`
2. `perek`
3. `pasuk`
4. `ref`
5. `hebrew_menukad_taamim`
6. `source`
7. `url`
8. `source_note`

## Bereishis Canonical Hebrew Source

- `bereishis_hebrew_menukad_taamim.tsv` is the canonical local Hebrew source for Sefer Bereishis.
- It includes nekudos and taamim.
- It is Hebrew source only.
- It does not include English translation.

## Provenance Expectations

- `source` should identify the source label clearly.
- `source_note` should explain provenance and any relevant text-tradition details.
- Do not invent missing pesukim.
- Do not silently alter Hebrew wording.

## Usage Expectations

- Future extraction batches should use canonical source-text files here for `hebrew_raw` when the relevant pasuk is present.
- Future extraction batches should not OCR, reconstruct, or guess Hebrew when a canonical file already contains the pasuk.
- Runtime parsed files are not canonical expansion sources.
- English translation sources should live in separate files, with their own version, translator, source, and license metadata.

## Validation

Run:

```powershell
python scripts/validate_source_texts.py
python -m pytest tests/test_source_texts_validation.py
```

## Future Sefarim

- Prefer one canonical source-text file per sefer.
- Do not collapse the entire Chumash into one giant source-text file unless repo conventions change explicitly.
- Add each sefer with the same TSV schema, manifest entry, validation report, and tests.

## Runtime Boundary

- This source-text layer does not make anything runtime active.
- It exists to support safer future extraction planning, not runtime promotion.
