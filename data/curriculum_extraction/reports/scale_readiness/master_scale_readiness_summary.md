**Status:** Partial readiness for scale planning  
**Key Finding:** The project has a working non-runtime curriculum extraction pipeline through Bereishis 4:16, but scale is now limited more by review-contract consistency, source foundation, alias reuse, and generator variety than by raw extraction mechanics.  
**Top Blocker:** The branch can safely produce planning artifacts, but it should not start Batch 006 here because the scalable source-text foundation and generator/alias infrastructure are still incomplete.  
**Recommended Next Action:** Land the canonical Bereishis source-text foundation, then close the Batch 002/003 review contract gap, then move into Batch 006 with improved planning discipline.

**1. What stage is the project in now?**
- The project is in a non-runtime curriculum scaling transition stage.
- Contiguous curriculum extraction coverage exists from Bereishis 1:1 through 4:16.
- Batches 004 and 005 already use the reviewed non-runtime contract.
- Runtime remains intentionally limited to the older active corpus through Bereishis 3:24.

**2. What is safely completed?**
- Batch extraction infrastructure exists and is validated.
- Manual review packet and review-resolution patterns exist and work for Batches 004 and 005.
- Source-prep tactics can safely unblock a batch when local Hebrew is missing.
- Preview generation works deterministically for review previews.
- Runtime and curriculum extraction remain correctly separated.

**3. What is the next highest-value branch?**
- `feature/source-bereishis-hebrew-menukad-canonical`

**4. What are the top 5 blockers to scaling?**

| Blocker | Evidence Source Path | Risk | Confidence | Recommended Next Action |
| --- | --- | --- | --- | --- |
| No canonical per-sefer Bereishis Hebrew source on this branch | `data/source/`, missing `data/source_texts/` | High | High | Add canonical source-text foundation and validator/tests. |
| Batch 002 and Batch 003 still have manifest/review-state mismatch | `data/curriculum_extraction/curriculum_extraction_manifest.json`, `batch_002_manual_review_packet.md`, `batch_003_manual_review_packet.md` | Medium | High | Close out both legacy batches with review-resolution reports. |
| Generator variety is too narrow across Batches 002-005 | preview JSONL files | High | High | Add carefully scoped preview families and quote-safe prompt handling. |
| Alias/context decisions are prose-only and not reusable | Batch 003-005 review packets and resolutions | High | High | Build a machine-readable alias registry. |
| Skill tags are too shallow for a true curriculum engine | normalized JSONL and preview JSONL | Medium | High | Add skill taxonomy and standards-mapping scaffold before major generator expansion. |

**5. What are the top 5 opportunities to improve question quality?**
- Add phrase-sensitive templates for watchlist-heavy phrases.
- Add alias-aware accepted-answer handling without overwriting source translations.
- Reintroduce compact vocab/shoresh/affix lanes from the seed layer only with full safety rails.
- Add source-record rotation so the same phrase is not automatically used in all preview lanes.
- Add automated watchlist extraction from normalized quality flags and manual review packet themes.

**6. What should not be touched yet?**
- Runtime scope and active corpus promotion
- `streamlit_app.py`
- `runtime/`
- `engine/`
- scoring/mastery/UI layers
- reviewed production question-bank files
- existing extracted JSONL and preview JSONL for Batches 001-005

**7. What is the best Monday morning action after this audit?**
- Merge the report set from this branch.
- Then start `feature/source-bereishis-hebrew-menukad-canonical`.
- After that, close out Batch 002 and Batch 003 review-state drift before widening question-template or alias infrastructure.

**Ready / Not Ready Judgment**
- Ready for planning, not ready for uncontrolled scale.
- The project can move forward safely, but the next branches need to strengthen source, alias, and generator foundations before any runtime-adjacent work.

**Next Branch Recommendation**
- `feature/source-bereishis-hebrew-menukad-canonical`
