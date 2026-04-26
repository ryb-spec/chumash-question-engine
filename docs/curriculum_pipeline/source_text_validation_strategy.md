**Status:** Validation strategy defined  
**Key Finding:** Canonical source texts need their own validator and manifest because batch validators and runtime validators solve different problems.  
**Top Blocker:** Source-text files can be structurally sound while still falling outside the curriculum batch validator allowlist.  
**Recommended Next Action:** Treat source validation as a first-class lane, with compatibility checks reported separately rather than folding them into runtime logic.

**Validation Goals**
- confirm canonical file presence
- confirm schema correctness
- confirm expected Bereishis coverage
- confirm source provenance fields are populated
- confirm the file is safe for extraction planning
- confirm the file is not treated as runtime data

**Structural Checks**
- exact column order
- tab delimiter only
- UTF-8 readability
- one row per pasuk
- valid integer `perek` and `pasuk`
- valid `Bereishis {perek}:{pasuk}` ref pattern
- no duplicate refs
- no duplicate perek/pasuk pairs
- no missing refs across known chapter counts
- no extra refs outside the known Bereishis structure
- nonblank Hebrew/source/source_note fields
- sof pasuk termination

**Status Model**
- `complete`: structurally valid full canonical file
- `partial`: file exists but full expected scope is missing
- `malformed`: file exists but has structural problems
- `missing`: canonical file not present

**Testing Strategy**
- synthetic malformed TSV tests in temporary files
- canonical-file happy-path test
- manifest shape test
- source validator should remain standard-library only

**Compatibility Strategy**
- Run source validation independently first.
- Run curriculum validation separately and report any allowlist mismatch as a compatibility issue.
- Do not change runtime or curriculum extraction data just to make source foundation work pass.

**Next Branch Recommendation**
- `feature/source-text-curriculum-validator-compatibility` only if this branch’s source foundation passes source validation but fails curriculum compatibility checks
