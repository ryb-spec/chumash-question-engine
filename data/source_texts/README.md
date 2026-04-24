# Source Texts

## Purpose

This folder stores canonical local source-text files that future extraction and source-alignment workflows can rely on directly.

## Bereishis Canonical Hebrew Source

- `bereishis_hebrew_menukad_taamim.tsv` is the canonical local Hebrew source for Sefer Bereishis.
- It includes nekudos and taamim.
- It is Hebrew source only.
- It does not include English translation.

## Usage Expectations

- Future extraction batches should use this file for `hebrew_raw` when the relevant pasuk is present here.
- Future extraction batches should not OCR, reconstruct, or guess Hebrew when this file already contains the pasuk.
- English translation sources should live in separate files, with their own version, translator, source, and license metadata.

## Recommended Structure

- Prefer one canonical source-text file per sefer.
- Do not collapse the entire Chumash into one giant source-text file unless the repo conventions change explicitly.
