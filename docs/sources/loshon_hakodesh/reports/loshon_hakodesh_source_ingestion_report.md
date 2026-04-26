# Loshon Hakodesh Source Ingestion Report

## 1. Summary

### What was uploaded

- `Loshon Hakodesh Book OCR.pdf`
- `loshon answe 2-combined.pdf`
- `loshon answe 2.pdf`

### Whether the main textbook was found

Yes.

### Whether the full answer booklet was found

Yes.

### Whether any partial/duplicate answer file was found

Yes.

The file `loshon answe 2.pdf` appears to be a 13-page partial duplicate and is not treated as the canonical answer booklet.

### Whether raw text was extracted

No full extracted text files were committed.

Reason:
- repository visibility could not be verified because `gh` was unavailable
- in a public or unknown-visibility repo, protected PDFs and full extracted source text were withheld

Limited in-memory OCR probing with `pypdf.PdfReader.extract_text()` was used only to classify sources, estimate page counts, and build a conservative lesson crosswalk.

### Whether repo visibility allowed committing PDFs

Visibility could not be verified.

Therefore:
- raw PDFs were not committed
- full raw extracted text was not committed
- only metadata, planning, indexing, and reports were added

Initial pass observed limited OCR in the earlier inspected copy; later reinspection identified a cleaner 33-page answer-booklet scan/OCR and updated the preferred answer-key metadata.

## Cleaner Answer Booklet Reinspection

- Date of reinspection:
  - `2026-04-26`
- Reason for reinspection:
  - a cleaner `loshon answe 2-combined.pdf` was supplied after the initial metadata pass
- Exact local file path inspected:
  - `C:\Users\ybassman\Downloads\loshon answe 2-combined.pdf`

### Old preferred answer booklet metadata snapshot

- original filename:
  - `loshon answe 2-combined.pdf`
- path at initial inspection:
  - `C:/Users/ybassman/Downloads/loshon answe 2-combined.pdf`
- page count:
  - `33`
- OCR coverage:
  - `12 pages with extractable text`
- file size:
  - `7088328` bytes
- checksum:
  - `b85a5e93dfee3110b1e7e28f8d62528ab9fbfa19c7eebdc2123a2c0406ded3e2`
- status:
  - historical metadata record retained as `superseded_by_cleaner_scan`

### New cleaner answer booklet inspection

- original filename:
  - `loshon answe 2-combined.pdf`
- path at reinspection:
  - `C:\Users\ybassman\Downloads\loshon answe 2-combined.pdf`
- page count:
  - `33`
- OCR coverage:
  - `33 pages with extractable text`
- file size:
  - `7074942` bytes
- checksum:
  - `de05e9e542a3d9d012d8282f457fcd139a0ab49e6e021281cdbf2688d931a32d`
- visible structure:
  - contents page visible
  - introduction page visible
  - Lessons `1-16` OCR-visible across the booklet
- status:
  - active `preferred_answer_key`

### Final decision

- The newly supplied file is not identical to the earlier inspected copy.
- It is cleaner for metadata and lesson-alignment work because the entire 33-page booklet is OCR-readable through `pypdf`, including contents, introduction, and lesson pages across Lessons `1-16`.
- The cleaner file is now the single active `preferred_answer_key`.
- The earlier full-booklet metadata record is retained only as historical provenance.
- The 13-page `loshon answe 2.pdf` file remains a `partial_duplicate`, not a canonical answer source.
- Answer content remains teacher-only and protected.

## 2. File Review

### Main textbook/workbook

- Original filename:
  - `Loshon Hakodesh Book OCR.pdf`
- Clean filename if private/internal storage is later approved:
  - `docs/sources/loshon_hakodesh/raw/loshon_hakodesh_mastering_the_basics_textbook_ocr.pdf`
- Title:
  - `Lashon Hakodesh: Mastering The Basics`
- Author:
  - `Nachman Marcuson`
- Type:
  - `main_textbook`
- Scan/OCR quality:
  - `mixed_ocr`
- Contents:
  - lesson sequence
  - rule explanations
  - vocabulary and grammar exercises
  - later summary pages showing rules through Lesson 16
- Project relevance:
  - rule extraction
  - dikduk skill taxonomy
  - lesson-to-skill mapping
  - exercise-to-skill mapping
- Warnings:
  - OCR is sparse
  - many pages returned no extractable text through `pypdf`
  - copied source text must remain protected
- Canonical/supplemental/archive decision:
  - `preferred_instructional_source`

### Full answer booklet

- Original filename:
  - `loshon answe 2-combined.pdf`
- Clean filename if private/internal storage is later approved:
  - `docs/sources/loshon_hakodesh/raw/loshon_hakodesh_mastering_the_basics_answer_booklet_full.pdf`
- Title:
  - `Answer Booklet to Lashon Hakodesh: Mastering The Basics`
- Author:
  - `Nachman Marcuson`
- Type:
  - `answer_booklet`
- Scan/OCR quality:
  - `improved_ocr`
- Contents:
  - exercise answers
  - teacher-key explanations
  - contents page, introduction, and lesson answer pages that align to textbook parsing work through Lessons 1-16
- Project relevance:
  - answer validation
  - teacher review
  - generated-question QA
  - lesson-to-exercise mapping
- Warnings:
  - must never become student-facing runtime content
  - full answer content was intentionally not committed
  - OCR should not be treated as final answer truth without human review
- Canonical/supplemental/archive decision:
  - `preferred_answer_key`
- Historical note:
  - the initial pass only observed limited OCR in an earlier inspected copy of this same filename
  - later reinspection identified a cleaner 33-page answer-booklet scan/OCR and updated the preferred answer-key metadata

### Partial/duplicate answer file

- Original filename:
  - `loshon answe 2.pdf`
- Clean filename if private/internal storage is later approved:
  - `docs/sources/loshon_hakodesh/raw/archive/loshon_hakodesh_answer_booklet_partial_duplicate.pdf`
- Title:
  - `Lashon Hakodesh answer booklet partial duplicate`
- Author:
  - `Nachman Marcuson`
- Type:
  - `partial_answer_booklet`
- Scan/OCR quality:
  - `image_only`
- Contents:
  - thirteen-page non-canonical slice
- Project relevance:
  - provenance
  - source-quality comparison only
- Warnings:
  - not the canonical answer booklet source
  - no extractable text was returned by `pypdf`
- Canonical/supplemental/archive decision:
  - `partial_duplicate`

## 3. Source-Pair Diagnosis

- Textbook and answer booklet appear matched:
  - yes
- Lesson numbering aligns:
  - yes, with remaining caution
  - textbook OCR visibly reaches Lesson 16
  - cleaner answer booklet OCR visibly shows contents, introduction, and Lessons 1-16 across the full 33-page booklet
  - some textbook-side rule anchors still require human review because the textbook OCR remains sparse
- Answer booklet references textbook exercises/pages:
  - yes
  - OCR-visible answer pages repeatedly refer back to page numbers and textbook rule locations
- Partial/duplicate diagnosis:
  - `loshon answe 2.pdf` is a 13-page partial duplicate candidate, not the full answer source

## 4. Why Both Sources Matter

- The textbook contains the instructional rule sequence and exercises.
- The answer booklet contains expected answers and explanatory validation.
- The answer booklet references lesson structure and rule usage from the textbook.
- They should be treated as one matched protected source pair for downstream extraction and QA.

## 5. Project Use

This source pair supports:
- skill taxonomy
- dikduk rule extraction
- question template design
- answer validation
- teacher review
- automated QA
- Zekelman Standard 3 alignment

## 6. Restrictions

- Do not expose answer booklet content to students.
- Do not create public answer banks from this file.
- Do not rely on OCR without human review.
- Do not modify production or runtime behavior from this ingestion task.

## 7. Recommended Next Branch

`feature/loshon-hakodesh-rule-extraction`
