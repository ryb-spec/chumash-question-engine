# Bereishis Hebrew Menukad Taamim Validation

- Source file path: `data/source_texts/bereishis_hebrew_menukad_taamim.tsv`
- Row count: `1534`
- Chapter count: `50`
- SHA-256: `a5fc8a32ff7d01c6c557e361d0c09a5a8d2267140dc4ba2e11a821bac4985f8d`
- First ref: `Bereishis 1:1`
- Last ref: `Bereishis 50:26`

## Source Attribution

- Source: `Sefaria`
- Source note wording present in the TSV: `Generated from Sefaria public export; Hebrew version: Miqra according to the Masorah; includes nekudos and taamim; no English translation included.`
- Repo copy source: copied from a user-provided local TSV into the canonical repo location without OCR or reconstruction.

## Validation Checklist Summary

- File exists in the canonical repo location.
- File is valid UTF-8.
- File is tab-separated.
- Header exactly matches the expected 8-column schema.
- Every data row has exactly 8 columns.
- All rows use `Bereishis` as the sefer value.
- Row count matches the full sefer count of `1534`.
- Perek count matches the full sefer count of `50`.
- Refs begin at `Bereishis 1:1` and end at `Bereishis 50:26`.
- No duplicate refs were found.
- No missing refs were found across the expected Bereishis structure.
- No extra refs were found outside the expected Bereishis structure.
- Every Hebrew text field is nonblank and ends with sof pasuk `׃`.
- Spot checks passed for `Bereishis 1:1`, `Bereishis 4:1`, `Bereishis 4:16`, `Bereishis 4:17`, and `Bereishis 50:26`.

## Hebrew-Only Confirmation

- This canonical TSV is Hebrew-only.
- It includes nekudos and taamim.
- It does not include any English translation column.

## OCR / Translation Separation

- No OCR was used in this branch.
- English translations belong in separate source files with their own source, translator, version, and metadata fields.
