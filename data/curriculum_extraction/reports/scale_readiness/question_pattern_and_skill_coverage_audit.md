**Status:** Not ready for generator scale  
**Key Finding:** Batches 002-005 currently collapse to three translation-heavy preview families with identical skill tagging, which is fast for extraction previewing but too narrow for a scalable skill-driven curriculum engine.  
**Top Blocker:** The preview generator is repetitive across later batches and still brittle around source-literal English strings with apostrophes or awkward phrasing.  
**Recommended Next Action:** Split the next generator branch into two focused goals: prompt-family variety and alias-safe phrase rendering.

**Scope**
- Evidence sources:
  - `data/curriculum_extraction/generated_questions_preview/batch_001_preview.jsonl`
  - `data/curriculum_extraction/generated_questions_preview/batch_001_preview_v2.jsonl`
  - `data/curriculum_extraction/generated_questions_preview/batch_002_preview.jsonl`
  - `data/curriculum_extraction/generated_questions_preview/batch_003_preview.jsonl`
  - `data/curriculum_extraction/generated_questions_preview/batch_004_preview.jsonl`
  - `data/curriculum_extraction/generated_questions_preview/batch_005_preview.jsonl`
  - `data/curriculum_extraction/normalized/batch_00*_*.jsonl`

**Question Type Counts by Batch**

| Batch | Phrase Translation | Hebrew to English Match | English to Hebrew Match | Prefix Identification | Suffix Identification | Shoresh Identification | Other Preview Families |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Batch 001 preview | 50 | 25 | 25 | 15 | 15 | 25 | none beyond seed preview families |
| Batch 001 preview v2 | 50 | 25 | 25 | 15 | 15 | 25 | none beyond seed preview families |
| Batch 002 | 50 | 25 | 25 | 0 | 0 | 0 | none |
| Batch 003 | 50 | 25 | 25 | 0 | 0 | 0 | none |
| Batch 004 | 50 | 25 | 25 | 0 | 0 | 0 | none |
| Batch 005 | 50 | 25 | 25 | 0 | 0 | 0 | none |

**Skill Coverage Snapshot**

| Evidence Source Path | Affected Batch or File | Finding | Risk | Confidence | Recommended Next Action |
| --- | --- | --- | --- | --- | --- |
| `data/curriculum_extraction/normalized/batch_002_linear_chumash_bereishis_1_6_to_2_3_pasuk_segments.jsonl` through `batch_005_linear_chumash_bereishis_4_1_to_4_16_pasuk_segments.jsonl` | Batches 002-005 | All normalized records are tagged only with `phrase_translation`. | Medium | High | Add explicit skill taxonomy and multi-skill extraction targets before scaling more batches. |
| `data/curriculum_extraction/generated_questions_preview/batch_002_preview.jsonl` through `batch_005_preview.jsonl` | Batches 002-005 | All preview questions are variants of translation or matching rather than actor/action, sequence, role, or comprehension lanes. | High | High | Add new preview families only after each has validator, distractor policy, watchlist logic, and tests. |
| `data/curriculum_extraction/generated_questions_preview/batch_001_preview*.jsonl` | Batch 001 | Seed previews show prefix, suffix, shoresh, and vocabulary families already exist as isolated ideas, but they are not part of the current extraction path. | Medium | High | Reuse Batch 001 as a design seed, not as direct pipeline proof. |

**Pattern Reuse Findings**

| Pattern | Evidence Source Path | Affected Batch or File | Risk | Confidence | Recommended Next Action |
| --- | --- | --- | --- | --- | --- |
| Exact three-family distribution of 50/25/25 repeats in every later batch. | `data/curriculum_extraction/generated_questions_preview/batch_002_preview.jsonl` through `batch_005_preview.jsonl` | Batches 002-005 | High | High | Add at least two new non-translation preview families before continuing many more batches. |
| The same source record is reused across multiple preview lanes in a narrow pool. Batch 002 and Batch 003 each have 25 source records reused three times. | same as above | Batches 002-003 | Medium | High | Add source-record rotation or lane balancing to reduce repetitive drilling on the same phrases. |
| Preview skill tags are effectively frozen at `translation_context` and `phrase_translation`. | preview files above | Batches 002-005 | High | High | Introduce a machine-readable skill taxonomy before expanding question variety. |
| English-to-Hebrew prompts become awkward when English contains apostrophes or source-literal phrasing. Examples: `Hashem's making of`, `isn't (available)`, `He (Hashem) didn't turn`. | `data/curriculum_extraction/generated_questions_preview/batch_003_preview.jsonl`, `data/curriculum_extraction/generated_questions_preview/batch_005_preview.jsonl` | Batch 003 and Batch 005 | Medium | High | Escape or reshape quoted English phrases before prompt assembly; add regression tests for apostrophes and contractions. |
| Watchlist-heavy phrases appear more often in Batch 005 but still use the same generic prompt shells. | `data/curriculum_extraction/generated_questions_preview/batch_005_preview.jsonl`, `data/curriculum_extraction/reports/batch_005_manual_review_packet.md` | Batch 005 | Medium | High | Add phrase-sensitive prompt variants that explicitly highlight the risky Hebrew phrase instead of treating it as ordinary translation content. |

**Coverage Judgment**
- `phrase_translation`: strong coverage across all later batches, but highly repetitive.
- `hebrew_to_english_match`: present and stable, but currently too similar to phrase translation to add much skill diversity.
- `english_to_hebrew_match`: present and useful, but currently the most exposed to awkward English quoting.
- `role/action/comprehension`: effectively absent in the later batch pipeline.
- `prefix/suffix/shoresh`: present only in legacy seed previews, not in the current batch extraction pipeline.

**Where Questions Quote Too Much or Too Little**
- Too little Hebrew:
  - English-to-Hebrew prompts often rely on English alone, which is risky when the English is source-literal or alias-sensitive.
- Too much generic framing:
  - Later prompts repeat `In Bereishis X:Y segment N...` so often that the batch previews look mechanically uniform.
- Exact phrase highlighting needed:
  - `חַטָּאת רֹבֵץ`
  - `הֲשֹׁמֵר אָחִי אָנֹכִי`
  - `דְּמֵי אָחִיךָ`
  - `נָע וָנָד`
  - `אוֹת`
  - `קִדְמַת־עֵדֶן`

**Practical Improvement Targets**
- Add phrase-sensitive prompt shells for alias-heavy phrases.
- Add at least one actor/action lane and one sequence/comprehension lane, but only with full validator and distractor support.
- Add quote-safe prompt rendering for apostrophes and contractions.
- Add reuse-balancing so one source phrase is not automatically used in all three lanes.
- Add skill tags beyond `translation_context` / `phrase_translation` before scaling more batches.

**Ready / Not Ready Judgment**
- Not ready for large-scale skill-driven generation yet.
- The current preview generator is sufficient for review previews, but not yet for broader curriculum intelligence.

**Next Branch Recommendation**
- `feature/question-generator-variety-and-alias-safe-prompts`
