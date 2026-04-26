# Bereishis Hebrew Menukad + Taamim TSV Validation

- Status: `ready`
- Key finding: the canonical Bereishis Hebrew TSV now has `1533` rows and chapter 35 correctly ends at `Bereishis 35:29`
- Top blocker: none at the source-structure level after the chapter-35 reconciliation
- Recommended next action: use this corrected TSV as the canonical ref backbone for non-runtime English translation alignment and future extraction planning

## File checked

- Path: `data/source_texts/bereishis_hebrew_menukad_taamim.tsv`
- Exists: `true`
- Encoding: `UTF-8`
- Delimiter: `tab-separated`
- Coverage: `Bereishis 1:1` through `Bereishis 50:26`

## Summary

- Rows excluding header: `1533`
- Chapters: `50`
- Chapter 35 pasuk rows: `29`
- First ref: `Bereishis 1:1`
- Last ref: `Bereishis 50:26`
- SHA-256: `0dedb854e1e8b59fa5dc08f93be5baffe4c1faaa09d00c148c8ef3113b065913`
- Empty Hebrew cells: `0`
- Hebrew cells with embedded tab characters: `0`
- Rows missing final sof pasuk `׃`: `0`
- Duplicate refs: `0`
- Contains `Bereishis 35:30`: `false`

## Source attribution

- Source label: `Sefaria`
- Hebrew version note: `Miqra according to the Masorah`
- Content scope: Hebrew-only source text with nekudos and taamim
- English translation included: `false`

## Chapter counts

| Perek | Pasuk rows |
|---:|---:|
| 1 | 31 |
| 2 | 25 |
| 3 | 24 |
| 4 | 26 |
| 5 | 32 |
| 6 | 22 |
| 7 | 24 |
| 8 | 22 |
| 9 | 29 |
| 10 | 32 |
| 11 | 32 |
| 12 | 20 |
| 13 | 18 |
| 14 | 24 |
| 15 | 21 |
| 16 | 16 |
| 17 | 27 |
| 18 | 33 |
| 19 | 38 |
| 20 | 18 |
| 21 | 34 |
| 22 | 24 |
| 23 | 20 |
| 24 | 67 |
| 25 | 34 |
| 26 | 35 |
| 27 | 46 |
| 28 | 22 |
| 29 | 35 |
| 30 | 43 |
| 31 | 54 |
| 32 | 33 |
| 33 | 20 |
| 34 | 31 |
| 35 | 29 |
| 36 | 43 |
| 37 | 36 |
| 38 | 30 |
| 39 | 23 |
| 40 | 23 |
| 41 | 57 |
| 42 | 38 |
| 43 | 34 |
| 44 | 34 |
| 45 | 28 |
| 46 | 34 |
| 47 | 31 |
| 48 | 22 |
| 49 | 33 |
| 50 | 26 |

## Reconciliation note

- Prior branch state incorrectly included an extra row labeled `Bereishis 35:30`.
- The removed row duplicated the burial verse of Yitzchak that Sefaria serves as `Bereishis 35:29`.
- See `data/source_texts/reports/bereishis_hebrew_source_reconciliation_report.md` for the decision trail and preserved removed-row content.

## Validation checklist summary

- Required columns present: `true`
- One pasuk per row: `true`
- Stable ref pattern: `true`
- Positive integer `perek` and `pasuk`: `true`
- No duplicate refs: `true`
- No unexpected extra ref after chapter 35: `true`
- Hebrew-only file: `true`
- No OCR used in this branch: `true`
- English translations belong in separate source files: `true`

## Ready judgment

- Judgment: `ready`
- Next branch recommendation: `feature/source-bereishis-english-translations-sefaria`
