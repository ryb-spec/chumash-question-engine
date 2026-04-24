**Status:** Planning-ready roadmap  
**Key Finding:** The extraction pipeline is strong enough to keep producing non-runtime batches, but the generator and skill model now need foundational improvement work rather than more of the same translation-only previews.  
**Top Blocker:** Later batches are extracting clean phrase segments, but the system still lacks reusable alias infrastructure, richer skill tags, and broader preview template families.  
**Recommended Next Action:** Build source, alias, and taxonomy foundations before attempting large-scale question-variety expansion.

**Roadmap Overview**

| Priority | Improvement | Expected Impact | Risk | Likely Files Affected in Future Branch | Test Strategy | Suggested Branch Name |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Canonical Hebrew source-text foundation | Faster, safer extraction beyond ad hoc source-prep blocks | Medium | `data/source_texts/`, `scripts/validate_source_texts.py`, `tests/test_source_texts_validation.py` | dedicated validator plus regression tests | `feature/source-bereishis-hebrew-menukad-canonical` |
| 2 | Review-contract closeout for legacy Batches 002-003 | Uniform batch lifecycle and cleaner planning state | Low | `data/curriculum_extraction/curriculum_extraction_manifest.json`, Batch 002/003 reports | curriculum validation + targeted review-state tests | `feature/curriculum-batch-002-and-003-review-contract-closeout` |
| 3 | Alias registry foundation | Consistent accepted-answer handling and watchlist reuse | Medium | `data/curriculum_extraction/`, new registry file(s), generator tests | registry schema tests + preview edge-case tests | `feature/curriculum-alias-registry-foundation` |
| 4 | Skill taxonomy foundation | Lets future batches tag more than phrase translation | Medium | new taxonomy docs/data, extraction reports, tests | schema tests + batch fixture assertions | `feature/curriculum-skill-taxonomy-foundation` |
| 5 | Preview generator variety improvements | Better question quality and less repetition | Medium | likely preview generation scripts, tests, reports | targeted preview tests + audit report diff | `feature/question-generator-variety-and-alias-safe-prompts` |
| 6 | Standards mapping scaffold | Enables Zekelman-style or local standards alignment without runtime promotion | Low | standards docs/data, tests | mapping schema tests only | `feature/curriculum-standards-mapping-scaffold` |
| 7 | Review packet auto-watchlists | Faster human review and more consistent alias capture | Low | review packet generation/report helpers | report fixture tests | `feature/review-packet-auto-watchlists` |
| 8 | Root/vocabulary reuse tracking | Smarter coverage planning across batches | Medium | new audit/report helper(s), tests | usage-tracking tests + report assertions | `feature/root-and-vocabulary-reuse-tracking` |
| 9 | Source-text lookup integration for extraction prep | Faster batch setup using canonical Hebrew rather than one-off prep | Medium | source-prep helpers, extraction docs/tests | range lookup tests | `feature/canonical-source-lookup-for-extraction` |
| 10 | Controlled runtime promotion readiness review | Keeps runtime safety intact while measuring what would be needed later | Low | reports only | no runtime changes; audit-only tests if any | `feature/runtime-promotion-readiness-review` |

**High-Value Improvements in Detail**

**1. Reduce repetitive question types**
- Behavior to change:
  - break the later-batch 50/25/25 preview pattern by adding a small number of new well-scaffolded lanes
  - rotate source-record usage so the same phrase is not used across all lanes by default
- Likely files:
  - future preview generation script(s)
  - `tests/test_curriculum_question_preview.py`
  - audit/report artifacts
- Test strategy:
  - assert type diversity and bounded reuse
  - add regression tests for lane counts and prompt families
- Risk:
  - medium, because generator changes can accidentally weaken review-safety

**2. Improve phrase-sensitive prompts**
- Behavior to change:
  - special-case risky phrases so prompts explicitly quote the Hebrew segment rather than burying it inside generic framing
- Target phrases:
  - `חַטָּאת רֹבֵץ`
  - `הֲשֹׁמֵר אָחִי אָנֹכִי`
  - `דְּמֵי אָחִיךָ`
  - doubled-verb phrases like `מוֹת תָּמוּת`
- Likely files:
  - preview generation logic
  - review packet helpers
  - preview tests
- Risk:
  - low to medium

**3. Improve alias/context support**
- Behavior to change:
  - move accepted aliases out of prose-only reports and into reusable machine-readable structures
  - keep source translations intact while adding accepted answer alternatives
- Likely files:
  - new alias registry file(s)
  - preview generation tests
  - manual review docs/report helpers
- Risk:
  - medium

**4. Skill tagging and difficulty tagging**
- Behavior to change:
  - let extracted segments and preview questions carry more than `phrase_translation`
  - distinguish translation, vocabulary, morphology, sequence, and actor/action skills
- Likely files:
  - extraction docs and possibly extraction validation
  - preview tests
  - future taxonomy docs/data
- Risk:
  - medium because tagging changes can spread across reports and validators

**5. Zekelman-style standard mapping**
- Behavior to change:
  - allow a later standards layer to map curriculum items to consistent educational buckets without affecting runtime
- Likely files:
  - docs and data-only scaffold
- Risk:
  - low

**6. Source-text lookup from canonical Hebrew**
- Behavior to change:
  - stop treating every Hebrew-extension need as a one-off source-prep event once canonical source files exist
- Likely files:
  - source-text validator
  - source lookup helpers
  - extraction prompt docs
- Risk:
  - low to medium

**7. Review packet auto-watchlists**
- Behavior to change:
  - derive watchlist sections from normalized `extraction_quality_flags` and prior alias decisions
- Likely files:
  - report helpers and docs
- Risk:
  - low

**8. Root/vocabulary reuse tracking**
- Behavior to change:
  - show which words, names, and watchlist items have already been targeted so future batches do not over-drill the same concepts
- Likely files:
  - audit/report helpers
  - possible future preview generation logic
- Risk:
  - medium

**Suggested Codex Prompts**

**Canonical source branch**
```text
You are working in the chumash-question-engine repo.

TASK TYPE:
canonical Hebrew source foundation

Branch required:
feature/source-bereishis-hebrew-menukad-canonical

Mission:
Add a canonical local Hebrew source file for Sefer Bereishis, plus validator/tests, without touching runtime or curriculum extraction JSONL.
```

**Alias registry branch**
```text
You are working in the chumash-question-engine repo.

TASK TYPE:
alias registry foundation

Branch required:
feature/curriculum-alias-registry-foundation

Mission:
Create a machine-readable alias/watchlist foundation using Batch 003-005 review artifacts as evidence, without changing runtime or rewriting extracted JSONL.
```

**Generator variety branch**
```text
You are working in the chumash-question-engine repo.

TASK TYPE:
preview generator variety improvement

Branch required:
feature/question-generator-variety-and-alias-safe-prompts

Mission:
Expand non-runtime preview question variety safely, reduce repetitive 50/25/25 template reuse, and fix quote-handling for apostrophes and source-literal English.
```

**Curriculum Reference Crosswalk**
- Reference-source directories checked for this audit:
  - `docs/curriculum_pipeline/reference_sources/`
  - `data/curriculum_extraction/reference_sources/`
  - `docs/reference_sources/`
  - `data/reference_sources/`
- Result:
  - No planning reference-source files were present in those locations on this branch.
- What should still influence the engine from existing repo evidence:
  - Batch manual review packets should drive alias/watchlist rules.
  - Batch review-resolution reports should drive accepted alias/context decisions.
  - Batch 001 seed previews should influence future vocab/shoresh/affix template design.
- Which ideas should become skill tags:
  - phrase translation
  - vocabulary recognition
  - reverse translation
  - actor/action role
  - sequence/comprehension
  - morphology: prefix, suffix, shoresh
- Which ideas should become question templates:
  - phrase-sensitive translation
  - actor/action identification
  - sequence ordering
  - compact vocabulary match
  - morphology spot checks
- Which ideas should become alias/watchlist rules:
  - names and places with common English equivalents
  - source-literal but awkward student-facing translations
  - doubled-verb emphasis phrases
  - phrases that must not be collapsed into one meaning
- Which ideas should not be implemented yet:
  - runtime-facing mastery or scoring changes
  - broad new skill lanes without validator/distractor/report support
  - standards enforcement that affects runtime question behavior
- Missing reference files that would help in a future branch:
  - a standards-mapping reference note set
  - a Zekelman-style terminology crosswalk
  - a small alias policy note for transliteration choices

**Ready / Not Ready Judgment**
- Ready for planning.
- Not ready to skip the foundation work; source, alias, and taxonomy branches should come before aggressive generator expansion.

**Next Branch Recommendation**
- `feature/source-bereishis-hebrew-menukad-canonical`
