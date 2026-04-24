**Status:** Partial vocabulary foundation  
**Key Finding:** The repo already contains strong human review evidence for alias-heavy Bereishis terms, but that knowledge is spread across batch reports instead of a reusable registry or watchlist system.  
**Top Blocker:** Alias/context decisions are documented in prose only, which makes them hard to reuse consistently across future batches and question families.  
**Recommended Next Action:** Build a machine-readable alias and watchlist foundation before widening skill lanes.

**Scope**
- Evidence sources:
  - `data/curriculum_extraction/reports/batch_002_manual_review_packet.md`
  - `data/curriculum_extraction/reports/batch_003_manual_review_packet.md`
  - `data/curriculum_extraction/reports/batch_004_summary.md`
  - `data/curriculum_extraction/reports/batch_004_manual_review_packet.md`
  - `data/curriculum_extraction/reports/batch_004_review_resolution.md`
  - `data/curriculum_extraction/reports/batch_005_summary.md`
  - `data/curriculum_extraction/reports/batch_005_manual_review_packet.md`
  - `data/curriculum_extraction/reports/batch_005_review_resolution.md`
  - `data/curriculum_extraction/normalized/batch_004_*.jsonl`
  - `data/curriculum_extraction/normalized/batch_005_*.jsonl`

**Recurring Watchlist Themes**

| Theme | Evidence Source Path | Affected Batch or File | Risk | Confidence | Recommended Next Action |
| --- | --- | --- | --- | --- | --- |
| Names students may know differently (`Kayin/Cain`, `Hevel/Abel`, `Chava/Eve`) | `data/curriculum_extraction/reports/batch_004_review_resolution.md`, `data/curriculum_extraction/reports/batch_005_review_resolution.md` | Batches 004-005 | Medium | High | Add a dedicated alias registry for names and accepted alternates. |
| Place names with transliteration drift (`Eden`, `Gan Eden`, `land of Nod`, `east of Eden`) | same as above | Batches 003-005 | Medium | High | Separate place-name aliases from ordinary vocabulary aliases. |
| Source-literal phrases that are accurate but awkward for students (`you may surely eat`, `moving and shaking`, `present`, `turned to`) | `data/curriculum_extraction/reports/batch_003_manual_review_packet.md`, `data/curriculum_extraction/reports/batch_005_review_resolution.md` | Batches 003 and 005 | High | High | Add accepted-answer layers without overwriting source-backed translations. |
| Terms that must not be collapsed into one meaning (`עָרוּם` vs `עֵירֹם`, `tree of knowledge` wording, `blood/bloods`) | `data/curriculum_extraction/reports/batch_004_review_resolution.md`, `data/curriculum_extraction/reports/batch_005_review_resolution.md` | Batches 004-005 | High | High | Introduce ambiguity notes and anti-collapse rules in a future alias/watchlist registry. |
| Generator phrases needing exact quotation rather than generic paraphrase (`חַטָּאת רֹבֵץ`, `הֲשֹׁמֵר אָחִי אָנֹכִי`) | `data/curriculum_extraction/reports/batch_005_manual_review_packet.md` | Batch 005 | Medium | High | Add phrase-sensitive prompt templates that keep the risky Hebrew phrase visible. |

**Current Alias/Watchlist Inventory**

| Term or Phrase | Current Repo Decision | Evidence Source Path | Risk | Confidence | Recommended Next Action |
| --- | --- | --- | --- | --- | --- |
| `רָקִיעַ` | keep source-backed wording; later accepted answers may include `firmament`, `expanse`, `sky` | `data/curriculum_extraction/reports/batch_002_manual_review_packet.md` | Medium | High | Carry into a reusable accepted-answer registry. |
| `אֶרֶץ וְשָׁמָיִם` | consider `land and sky` and `earth and heavens` as future aliases | `data/curriculum_extraction/reports/batch_003_manual_review_packet.md` | Low | High | Place in geography/cosmos alias list. |
| `וְאֵד יַעֲלֶה מִן הָאָרֶץ` | `cloud`, `mist`, `vapor` are future accepted answers | same as above | Medium | High | Mark as source-literal phrase requiring accepted-answer flexibility. |
| `עֵדֶן / Eiden` | accepted student-facing alias should prefer `Eden` | same as above | Medium | High | Normalize transliteration policy for names and places. |
| `אָכֹל תֹּאכֵל` / `מוֹת תָּמוּת` | preserve source wording but allow smoother accepted forms like `you may surely eat` and `you will surely die` | `data/curriculum_extraction/reports/batch_003_manual_review_packet.md`, `data/curriculum_extraction/reports/batch_004_review_resolution.md` | Medium | High | Add doubled-verb emphasis rule in alias registry. |
| `עָרוּם / עֵירֹם / עֵירֻמִּם` | keep `cunning/crafty` distinct from `naked/unclothed` | `data/curriculum_extraction/reports/batch_004_review_resolution.md` | High | High | Add anti-collapse rule for same-surface/similar-surface ambiguity. |
| `עֵץ הַדַּעַת טוֹב וָרָע` | allow both `good and bad` and `good and evil` as accepted phrasing | same as above | Medium | High | Add accepted alias set for fixed phrases. |
| `קַיִן / הֶבֶל` | one prompt should use one name form consistently | `data/curriculum_extraction/reports/batch_005_review_resolution.md` | Medium | High | Add name alias policy to generator watchlists. |
| `מִנְחָה` | preserve source `present`; accept `offering` / `gift-offering` where appropriate | same as above | Medium | High | Add source-literal vs student-facing synonym support. |
| `וַיִּשַׁע / לֹא שָׁעָה` | keep source `turned / did not turn`; accept `accepted / did not accept`, `paid attention to / did not pay attention to` | same as above | Medium | High | Add phrase-level accepted-answer mapping. |
| `חַטָּאת רֹבֵץ` | keep phrase visible; accepted explanation may use `sin crouches` | same as above | High | High | Treat as exact-phrase prompt candidate, not plain loose translation. |
| `הֲשֹׁמֵר אָחִי אָנֹכִי` | preserve source `guard of my brother`; accept `my brother's keeper/watchman` | same as above | High | High | Add phrase-specific accepted aliases. |
| `דְּמֵי אָחִיךָ` | allow `blood`; reserve `bloods` for literal-study context | same as above | Medium | High | Separate literal-study aliases from student-default aliases. |
| `נָע וָנָד` | preserve source-literal phrasing; accept `wandering` / `restless wanderer` | same as above | Medium | High | Add motion-state alias set. |
| `אוֹת` | preserve `sign`; allow `mark` when context is explicit | same as above | Medium | High | Context-sensitive alias handling needed. |

**What Is Missing Today**
- No machine-readable alias registry.
- No reusable watchlist taxonomy across batches.
- No explicit anti-collapse rule file for dangerous near-equivalents.
- No vocabulary reuse tracker that tells the generator which watchlist terms have already been surfaced.
- No standards-aligned skill tags linking watchlist items to question families.

**Practical Follow-Up Design**
- One machine-readable alias registry for names, places, fixed phrases, and source-literal alternates.
- One watchlist taxonomy keyed by risk:
  - alias required
  - exact phrase required
  - ambiguity do not collapse
  - source-literal wording review
- One batch-report helper that auto-surfaces watchlist terms already present in normalized quality flags.

**Ready / Not Ready Judgment**
- Not ready for reliable scale yet.
- The review intelligence exists, but it is trapped in prose instead of reusable data structures.

**Next Branch Recommendation**
- `feature/curriculum-alias-registry-foundation`
