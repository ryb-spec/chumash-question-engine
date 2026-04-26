**Status:** Canonical source foundation present  
**Key Finding:** This branch already contains a complete Bereishis canonical TSV and a first-pass validator/test scaffold, but it needed hardening around manifesting, reporting, and byte-level source alignment.  
**Top Blocker:** Compatibility with the curriculum validator is likely incomplete for new source-foundation docs and manifest files because this branch is not allowed to update that separate validator.  
**Recommended Next Action:** Finish validating the Bereishis TSV, ship the source-text manifest and handoff docs, and treat any curriculum-validator allowlist failures as isolated compatibility follow-up work.

**Files Inspected**
- `AGENTS.md`
- `README.md`
- `incoming_source/bereishis_hebrew_menukad_taamim.tsv`
- `data/source/`
- `data/source_texts/`
- `data/pesukim_100.json`
- `data/parsed_pesukim.json`
- `scripts/validate_source_texts.py`
- `tests/test_source_texts_validation.py`

**Existing Source Files Found**

| Source Category | Paths | Classification | Safe for Future Extraction Planning | Should Be Used as Canonical Source | Confidence | Risk |
| --- | --- | --- | --- | --- | --- | --- |
| Canonical sefer-wide Hebrew source | `data/source_texts/bereishis_hebrew_menukad_taamim.tsv` | canonical candidate | Yes | Yes | High | Low |
| Incoming local authoritative source input | `incoming_source/bereishis_hebrew_menukad_taamim.tsv` | local source input | Yes, as provenance/input | No, not as repo canonical location | High | Low |
| Block-based Hebrew helper files | `data/source/bereishis_1_1_to_1_30.json` through `data/source/bereishis_4_1_to_4_16.json` | patch-based / range helpers | Yes, for local extraction prep on covered ranges | No | High | Medium |
| Runtime parsed corpus | `data/pesukim_100.json`, `data/parsed_pesukim.json` | runtime-derived / active-scope data | No, not for canonical expansion | No | High | Medium |

**Current Findings**
- `data/source_texts/` exists.
- The canonical Bereishis TSV exists.
- The incoming TSV exists and has identical text content to the repo TSV.
- The repo TSV had drifted to CRLF line endings even though the incoming authoritative TSV was LF-only.
- `data/source/` remains useful as block-based source prep, but it should not replace a sefer-wide canonical source layer.
- `data/pesukim_100.json` and `data/parsed_pesukim.json` are runtime-side assets and should not be treated as canonical expansion sources.

**Which Files Are Safe for Future Extraction Planning**
- `data/source_texts/bereishis_hebrew_menukad_taamim.tsv`
- `data/source_texts/source_text_manifest.json`
- `data/source_texts/reports/bereishis_hebrew_menukad_taamim_validation.md`
- relevant `data/source/*.json` helper blocks for already-covered ranges, as secondary alignment aids only

**Which Files Should Not Be Used as Canonical Sources**
- `data/pesukim_100.json`
- `data/parsed_pesukim.json`
- English translation artifacts anywhere under curriculum extraction
- review packets and extraction reports

**Initial Risk Classification**
- Canonical source-text layer: low risk once validation passes
- Patch/block source files: medium risk if treated as the only long-term source strategy
- Runtime-derived corpora: medium risk if mistaken for canonical source foundation
- Missing curriculum-validator allowlist coverage for new source docs: medium risk to branch compatibility, low risk to source integrity

**Ready / Not Ready Judgment**
- Ready as a source-foundation candidate, pending full validation and compatibility-check results.

**Next Branch Recommendation**
- `feature/source-text-curriculum-validator-compatibility` only if the source foundation passes but the existing curriculum validator rejects the new source docs/manifest paths
