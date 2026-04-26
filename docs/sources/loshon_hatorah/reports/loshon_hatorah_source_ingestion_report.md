# Loshon HaTorah Source Ingestion Report

## Current Branch
- `feature/loshon-hatorah-standard-3-enrichment`

## Source Policy
- Zekelman 2025 Version 2.5 remains the canonical authority for Standard 3 wording, numbering, level progression, and scope.
- Loshon HaTorah / Loshon Hakodesh material is supplemental evidence only.
- Nothing in this source layer is runtime-ready or question-ready.

## Sources Found
- `docs/sources/loshon_hatorah/raw/loshon_hakodesh_book_ocr.pdf`: main book PDF, `86` pages, `15218787` bytes, SHA-256 `c4eb6adb3841c6c84f3cf63342044ed8ef7890a9d0f6852ebe5edc041ffab130`, extracted to `docs/sources/loshon_hatorah/extracted/loshon_hakodesh_book_ocr_raw_text.md`.
- `docs/sources/loshon_hatorah/raw/loshon_answe_2_combined.pdf`: answer booklet PDF for source review only, `33` pages, `7074942` bytes, SHA-256 `de05e9e542a3d9d012d8282f457fcd139a0ab49e6e021281cdbf2688d931a32d`, extracted to `docs/sources/loshon_hatorah/extracted/loshon_answe_2_combined_raw_text.md`.
- `data/dikduk_rules/rules_loshon_foundation.jsonl`: existing source-modeled JSONL artifact, `67503` bytes, SHA-256 `91f097d2b4688b1b3356181ade74703ac75b3890eb5c75bffcf9b7599b2c9173`, `37` rule records observed.

## Sources Missing
- No expected Loshon HaTorah / Loshon Hakodesh source files are currently missing from the protected source layer.
- Exact record-to-page alignment between the JSONL file and the raw main book still needs human review.

## Search Locations
- `local_curriculum_sources/`
- `docs/`
- `docs/sources/`
- `data/`
- `incoming_source/`

## Extraction Result
- Created `docs/sources/loshon_hatorah/extracted/loshon_hakodesh_book_ocr_raw_text.md` from `docs/sources/loshon_hatorah/raw/loshon_hakodesh_book_ocr.pdf`.
- Created `docs/sources/loshon_hatorah/extracted/loshon_answe_2_combined_raw_text.md` from `docs/sources/loshon_hatorah/raw/loshon_answe_2_combined.pdf`.
- The main-book OCR/text layer is partial: pypdf extracted usable text from pages 4, 6, 8, 63, and 80-86, while many intervening pages were blank in the embedded text layer.
- The answer booklet produced usable page-delimited text across the 33-page file, but Hebrew, tables, and line layout remain OCR-sensitive.

## Review Warnings
- The raw PDFs are now available, but this does not make any skill runtime-ready or question-ready.
- The answer booklet must not be promoted into an active answer key.
- Hebrew examples, nikud-sensitive details, weak-letter behavior, and table structures require direct human source review.
- Loshon evidence can enrich review questions and crosswalk support, but it cannot resolve teacher decisions or override Zekelman 2025.
