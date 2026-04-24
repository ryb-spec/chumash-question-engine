**Status:** Inventory complete, revision needed  
**Key Finding:** The repo already shows a small, identifiable set of preview-template families, but the later curriculum batches overuse three translation-focused families and underuse the more diagnostic seed templates.  
**Top Blocker:** Template diversity is too low in Batches 002-005 to support a more powerful skill-driven curriculum engine.  
**Recommended Next Action:** Keep the three current non-runtime preview families, revise them for phrase safety, and add carefully scoped new families rather than inventing a wide template explosion.

**Scope**
- Evidence sources:
  - `data/curriculum_extraction/generated_questions_preview/batch_001_preview.jsonl`
  - `data/curriculum_extraction/generated_questions_preview/batch_001_preview_v2.jsonl`
  - `data/curriculum_extraction/generated_questions_preview/batch_002_preview.jsonl`
  - `data/curriculum_extraction/generated_questions_preview/batch_003_preview.jsonl`
  - `data/curriculum_extraction/generated_questions_preview/batch_004_preview.jsonl`
  - `data/curriculum_extraction/generated_questions_preview/batch_005_preview.jsonl`

| Template Family | Example Question or ID | Skill Assessed | Batches Where It Appears | Overuse Risk | Weakness | Improvement Idea | Needs Hebrew Phrase Highlighting | Needs Alias Support | Recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Context phrase translation | `generated_preview.batch_002_linear_bereishis.002` style: `Translate segment N from Bereishis X:Y into English: ...` | phrase translation | Batches 002-005 | High | Very repetitive; does not distinguish easy vs risky phrases | Add phrase-sensitive variant for watchlist-heavy segments | Sometimes | Yes for risky phrases | Revise |
| Hebrew phrase to English match | `generated_preview.batch_005_linear_bereishis_4_1_to_4_16.hebrew_to_english_match.007` style | recognition of source-backed translation | Batches 002-005 | Medium | Too similar to plain translation; distractors are same-lane only | Vary distractor style and add explicit phrase focus for risky terms | Sometimes | Yes | Revise |
| English phrase to Hebrew match | `generated_preview.batch_003_linear_bereishis_2_4_to_2_25.english_to_hebrew_match.005` | reverse translation | Batches 002-005 | High | Most exposed to awkward English quoting and alias drift | Sanitize quote handling and use alias-aware English stems | Often | Yes | Revise |
| Segment meaning in context | `What does this segment mean in context? בראשית` | context translation | Batch 001 previews | Medium | Prompt is short and useful, but not standardized with later batches | Bring back as a compact variant for brief phrases | Yes | Sometimes | Keep and modernize |
| Compact Hebrew-to-English vocab match | `Which English gloss best matches the Hebrew word אכל?` | vocabulary recognition | Batch 001 previews | Low | Strong for isolated words, but absent from current extraction pipeline | Reintroduce once vocab-entry extraction exists for later batches | No | Sometimes | Keep |
| Compact English-to-Hebrew vocab match | `Which Hebrew word best matches the English gloss 'eat'?` | vocabulary recall | Batch 001 previews | Low | Useful but currently disconnected from later batch records | Reuse after alias registry and vocabulary extraction foundation exist | No | Yes | Keep |
| Prefix identification | `In the word ולא, which prefix is present?` | prefix recognition | Batch 001 previews | Low | Seed-only; no later extraction support | Reintroduce only with validated affix-safe candidate detection | No | No | Keep, later |
| Suffix identification | `Look at עליו. What suffix can you identify?` | suffix recognition | Batch 001 previews | Low | Seed-only; no later extraction support | Same as prefix lane: only with full safety rails | No | No | Keep, later |
| Shoresh identification | `What is the shoresh of ולא?` | shoresh recognition | Batch 001 previews | Medium | One seed phrasing is noisy (`in Vayeishev sample answer key`) and needs cleanup | Rebuild from clean seed rules before reuse | No | No | Revise before reuse |

**Inventory Notes**
- The current engine already hints at a wider template future, but only the three translation families have an active curriculum-batch path.
- Template quality is strongest when the prompt is compact and the risky phrase is visible.
- Template quality is weakest when English phrasing is quoted mechanically from source-literal wording.

**Ready / Not Ready Judgment**
- Not ready to scale template variety automatically yet.
- The current family inventory is good enough to plan from, but not yet broad enough to support a richer curriculum engine.

**Next Branch Recommendation**
- `feature/question-template-variety-foundation`
