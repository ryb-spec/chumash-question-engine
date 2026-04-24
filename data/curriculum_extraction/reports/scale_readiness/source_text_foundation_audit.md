**Status:** Not ready for fast scale  
**Key Finding:** This branch still relies on one-off `data/source/*.json` blocks and runtime-limited corpora rather than a canonical per-sefer Hebrew source foundation.  
**Top Blocker:** There is no `data/source_texts/` foundation on this branch, so future extraction past Bereishis 4:16 would still depend on ad hoc source-prep work.  
**Recommended Next Action:** Land a canonical per-sefer Bereishis Hebrew source plus validator/tests before starting Batch 006.

**Scope**
- Evidence sources:
  - `data/source/`
  - `data/pesukim_100.json`
  - `data/parsed_pesukim.json`
  - `data/curriculum_extraction/reports/batch_005_source_gap_request.md`
  - `data/curriculum_extraction/reports/batch_005_hebrew_source_prep.md`

**Current Source Inventory**

| Source Path | What Exists | Scaling Value | Risk | Confidence | Recommended Next Action |
| --- | --- | --- | --- | --- | --- |
| `data/source/` | Block JSON files through `bereishis_4_1_to_4_16.json` | Good for one-off source prep and local alignment | Medium | High | Preserve as block-level helpers, but do not treat them as the long-term canonical source layer. |
| `data/pesukim_100.json` | Active parsed/source scaffold for Bereishis 1:1-3:24 | Useful for current runtime-scoped work only | Medium | High | Leave runtime corpus alone until curriculum source foundation is broader and reviewed. |
| `data/parsed_pesukim.json` | Parsed runtime corpus through Bereishis 3:24 | Useful for current app, not for wider extraction scale | Medium | High | Keep unchanged; do not promote active scope from curriculum work. |
| `data/source_texts/` | Not present on this branch | None yet | High | High | Add canonical per-sefer source files and validator in a dedicated source-foundation branch. |

**What the Batch 005 Source Prep Solved**
- `data/curriculum_extraction/reports/batch_005_source_gap_request.md` documented the original blocker: no safe local Hebrew source for Bereishis 4:1-4:16.
- `data/curriculum_extraction/reports/batch_005_hebrew_source_prep.md` documented the safe local fix: `data/source/bereishis_4_1_to_4_16.json`.
- This was enough to unblock Batch 005, but it did not establish a sefer-wide canonical foundation.

**Scalability Judgment**

| Question | Evidence Source Path | Answer |
| --- | --- | --- |
| Does a full canonical Bereishis TSV exist on this branch? | `data/source_texts/` | No |
| Is the current source structure scalable enough for many more batches? | `data/source/`, `batch_005_hebrew_source_prep.md` | Only partially; it still depends on piecemeal block files |
| Should source files be one sefer per file rather than one giant Chumash file? | repo conventions plus Batch 005 source prep pattern | Yes, one sefer per canonical file is the safest next step |
| Should English translation live in the same source foundation file? | current repo structure | No, Hebrew canonical source and translation sources should stay separate |

**Recommended Future Structure**
- Canonical Hebrew source:
  - `data/source_texts/bereishis_hebrew_menukad_taamim.tsv`
- Separate validation/report layer:
  - `scripts/validate_source_texts.py`
  - `tests/test_source_texts_validation.py`
  - `data/source_texts/reports/...`
- Continue using `data/source/*.json` only as derived or convenience blocks when a batch needs a small aligned slice.

**Tests the Repo Should Have for Source Texts**
- file exists
- UTF-8 validation
- exact header/schema validation
- per-sefer row count and chapter coverage
- duplicate ref rejection
- missing/extra ref rejection
- Hebrew text nonblank
- sof pasuk enforcement
- stable hash reporting for the canonical file

**What Still Blocks Faster Batch Processing**
- No sefer-wide canonical Hebrew file on this branch
- No canonical source-text validator on this branch
- No automatic lookup layer from batch range to canonical Hebrew source
- Runtime corpora still stop at Bereishis 3:24, which is correct for runtime safety but means extraction branches cannot piggyback on runtime data

**Ready / Not Ready Judgment**
- Not ready for faster post-4:16 extraction scale on this branch.
- The source-prep tactic works, but the foundation is still piecemeal.

**Next Branch Recommendation**
- `feature/source-bereishis-hebrew-menukad-canonical`
