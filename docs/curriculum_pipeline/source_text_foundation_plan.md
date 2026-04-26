**Status:** Foundation plan ready  
**Key Finding:** The repo now has a path toward scalable extraction only if canonical source texts are treated as a dedicated per-sefer layer rather than as a side effect of runtime data or one-off batch patches.  
**Top Blocker:** The source foundation must stay isolated from runtime and from curriculum extraction validators that were originally built for batch-only work.  
**Recommended Next Action:** Use Bereishis as the canonical pattern, then repeat the same source-text contract sefer by sefer.

**Current State**
- `data/source/` contains range-based helper files through `Bereishis 4:1-4:16`.
- `data/source_texts/bereishis_hebrew_menukad_taamim.tsv` is the canonical sefer-wide Bereishis source candidate.
- Runtime corpora under `data/pesukim_100.json` and `data/parsed_pesukim.json` remain bounded to the active app scope and should stay separate.

**Target Architecture**
- One canonical TSV per sefer under `data/source_texts/`
- One machine-readable source-text manifest
- One validator script for canonical source files
- One report set for inventory, validation, and gaps
- Optional block helpers under `data/source/` derived later for convenience, not as the primary canonical layer

**Per-Sefer Source Strategy**
- `data/source_texts/bereishis_hebrew_menukad_taamim.tsv`
- future:
  - `data/source_texts/shemos_hebrew_menukad_taamim.tsv`
  - `data/source_texts/vayikra_hebrew_menukad_taamim.tsv`
  - `data/source_texts/bamidbar_hebrew_menukad_taamim.tsv`
  - `data/source_texts/devarim_hebrew_menukad_taamim.tsv`

**TSV Schema**
- `sefer`
- `perek`
- `pasuk`
- `ref`
- `hebrew_menukad_taamim`
- `source`
- `url`
- `source_note`

**Validation Strategy**
- exact header and tab delimiter
- UTF-8 readability
- one row per pasuk
- full per-sefer coverage where expected counts are known
- duplicate/malformed row detection
- nonblank source provenance fields
- no runtime activation or corpus promotion implied by source presence

**Future Expansion Strategy**
- Add one sefer at a time.
- Validate each sefer independently.
- Keep Hebrew-only source texts separate from translation sources.
- Do not reuse runtime parsed corpora as automatic canonical expansion input.

**How Canonical Source Files Should Interact With Curriculum Extraction**
- Future extraction branches should use canonical source files for `hebrew_raw` when the requested range is present.
- Source-text manifest and validation reports should be checked before new extraction batches start.
- Block helpers in `data/source/` can still be generated for local range-focused work if needed.

**How Canonical Source Files Should Not Interact With Runtime Yet**
- They should not change active runtime scope.
- They should not automatically update `data/pesukim_100.json` or `data/parsed_pesukim.json`.
- They should not trigger runtime promotion or reviewed-bank changes.

**Next Branch Recommendation**
- `feature/curriculum-batch-006-bereishis-4-17-to-4-26` only after this source foundation validates cleanly and the handoff report says it is safe
