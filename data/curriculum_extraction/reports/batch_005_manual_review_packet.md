# Batch 005 Manual Review Packet

- Batch: `batch_005_linear_bereishis_4_1_to_4_16`
- Source range: `Bereishis 4:1 through Bereishis 4:16`
- Packet purpose: sample inactive Batch 005 extraction and preview artifacts for human review only

## Source Files Inspected

- `data/source/bereishis_4_1_to_4_16.json`
- `local_curriculum_sources/7984C_b_01409_pshat_of_torah.pdf`
- `data/curriculum_extraction/raw_sources/batch_005/linear_chumash_bereishis_4_1_to_4_16_cleaned.md`
- `data/curriculum_extraction/normalized/batch_005_linear_chumash_bereishis_4_1_to_4_16_pasuk_segments.jsonl`
- `data/curriculum_extraction/generated_questions_preview/batch_005_preview.jsonl`

## Record Counts

- `pasuk_segment`: `64`
- `translation_rule`: `0`
- preview questions: `100`

## Preview Question Counts

- `phrase_translation`: `50`
- `hebrew_to_english_match`: `25`
- `english_to_hebrew_match`: `25`

## Watchlist Summary

### Names / Places

- `קַיִן`: preserve the source name rendering. Accepted alias set: `Kayin` / `Cain`. Context note: choose one audience-facing name per prompt and avoid mixing both names inside the same item unless the task is explicitly about aliases.
- `הֶבֶל`: preserve the source name rendering. Accepted alias set: `Hevel` / `Abel`. Context note: choose one audience-facing name per prompt and avoid mixing both names inside the same item unless the task is explicitly about aliases.
- `אֶרֶץ־נוֹד`: preserve the place name as `land of Nod`. Context note: keep this as a proper place name rather than paraphrasing it away.
- `קִדְמַת־עֵדֶן`: preserve the source-facing phrase, but allow smoother student-facing aliases `east of Eden` / `toward the east of Eden`. Student-facing note: prefer `Eden` over the source-literal spelling `Eiden` in future accepted-answer layers.

### Source-Literal Phrases That May Need Smoother Accepted Wording

- `מִנְחָה`: preserve the source wording `present`. Accepted aliases: `offering` / `gift-offering`. Context note: `gift-offering` is safer when the prompt needs to signal sacrificial context without overwriting the source wording.
- `וַיִּשַׁע`: preserve the source wording `turned`. Accepted aliases: `accepted` / `paid attention to`. Context note: future prompts may use smoother accepted wording, but should keep the acceptance/rejection contrast explicit.
- `לֹא שָׁעָה`: preserve the source wording `didn't turn`. Accepted aliases: `did not accept` / `did not pay attention to`. Context note: keep the negative response explicit so it still contrasts clearly with `וַיִּשַׁע`.
- `נָע וָנָד`: preserve the source wording `moving and shaking`. Accepted aliases: `wandering` / `restless wanderer`. Student-facing note: the smoother aliases are clearer for future question generation, but the source wording should remain traceable in review artifacts.
- `אוֹת`: preserve the source wording `sign`. Accepted alias: `mark` when the prompt context is already clearly about the protective sign placed on Kayin.

### Exact-Phrase Watchlist

- `חַטָּאת רֹבֵץ`: preserve the source wording. Accepted aliases may include `sin crouches` / `sin crouches at the opening`, but this phrase should stay exact-phrase-sensitive in future prompts.
- `הֲשֹׁמֵר אָחִי אָנֹכִי`: preserve the source wording `am I the guard of my brother?`. Accepted aliases: `am I my brother's keeper?` / `am I my brother's watchman?`.
- `קוֹל דְּמֵי אָחִיךָ`: preserve the source wording. Accepted aliases may include `your brother's blood` and, for more literal study contexts, `your brother's bloods`.
- `לְבִלְתִּי הַכּוֹת־אֹתוֹ כׇּל־מֹצְאֽוֹ`: keep this phrase exact when surfaced. Context note: future prompts should quote the phrase rather than paraphrasing it loosely.

### Review Questions To Keep In Mind

- Does a later accepted-alias layer need to support `Cain`, `Abel`, `offering`, `accepted`, `watchman`, `bloods`, `restless wanderer`, `mark`, `Nod`, and `east of Eden`?
- Which awkward source-literal phrases should remain visible for fidelity, and which should later gain smoother accepted-answer aliases?
- Which prompts must quote the exact Hebrew phrase rather than a larger pasuk chunk?

## Sample Pasuk Segment Review Table

| Ref | Hebrew phrase | Source translation | Skill target | Concern flag | Reviewer notes | Alias / context notes |
|---|---|---|---|---|---|---|
| `4:1` | `וַתַּ֙הַר֙ וַתֵּ֣לֶד אֶת־קַ֔יִן` | `and she conceived and she bore (a son whom she named) Kayin` | `phrase_translation` | `name_alias_review` | `________________` | `Kayin / Cain?` |
| `4:2` | `וַֽיְהִי־הֶ֙בֶל֙ רֹ֣עֵה צֹ֔אן` | `and Hevel was a shepherd of sheep and goats` | `phrase_translation` | `name_alias_review` | `________________` | `Hevel / Abel?` |
| `4:3` | `מִנְחָ֖ה לַֽיהֹוָֽה` | `a present to Hashem` | `phrase_translation` | `source_literal_wording` | `________________` | `present / offering / gift-offering?` |
| `4:4` | `וַיִּ֣שַׁע יְהֹוָ֔ה` | `and Hashem turned` | `phrase_translation` | `source_literal_wording` | `________________` | `turned / accepted / paid attention to?` |
| `4:5` | `לֹ֣א שָׁעָ֑ה` | `He (Hashem) didn't turn` | `phrase_translation` | `source_literal_wording` | `________________` | `didn't turn / did not accept?` |
| `4:7` | `לַפֶּ֖תַח חַטָּ֣את רֹבֵ֑ץ` | `to the opening of your heart the sin (yetzer hara) crouches` | `phrase_translation` | `phrase_sensitive` | `________________` | `sin crouches / rests at the opening?` |
| `4:8` | `וַיָּ֥קׇם קַ֛יִן אֶל־הֶ֥בֶל אָחִ֖יו` | `and Kayin got up to Hevel his brother` | `phrase_translation` | `actor_action_wording` | `________________` | `rise up against?` |
| `4:9` | `הֲשֹׁמֵ֥ר אָחִ֖י אָנֹֽכִי` | `am I the guard of my brother?` | `phrase_translation` | `phrase_sensitive` | `________________` | `guard / keeper / watchman?` |
| `4:10` | `ק֚וֹל דְּמֵ֣י אָחִ֔יךָ` | `the voice of the blood of your brother` | `phrase_translation` | `phrase_sensitive` | `________________` | `blood / bloods?` |
| `4:12` | `נָ֥ע וָנָ֖ד תִּֽהְיֶ֥ה בָאָֽרֶץ` | `moving and shaking you will be in the land` | `phrase_translation` | `source_literal_wording` | `________________` | `wandering / restless wanderer?` |
| `4:15` | `וַיָּ֨שֶׂם יְהֹוָ֤ה לְקַ֙יִן֙ א֔וֹת` | `and Hashem placed a sign for Kayin` | `phrase_translation` | `alias_review` | `________________` | `sign / mark?` |
| `4:16` | `וַיֵּ֥שֶׁב בְּאֶֽרֶץ־נ֖וֹד` | `and he sat (settled) in the land of Nod` | `phrase_translation` | `name_place_alias_review` | `________________` | `Nod?` |
| `4:16` | `קִדְמַת־עֵֽדֶן` | `East of Eiden` | `phrase_translation` | `name_place_alias_review` | `________________` | `east of Eden / toward the east of Eden?` |

## Sample Preview Review Table

| Preview ID | Type | Prompt / target | Answer | Concern flag | Reviewer notes | Alias / context notes |
|---|---|---|---|---|---|---|
| `phrase_translation.002` | `phrase_translation` | `4:1 seg 2 - וַתַּ֙הַר֙ וַתֵּ֣לֶד אֶת־קַ֔יִן` | `and she conceived and she bore (a son whom she named) Kayin` | `name_alias_review` | `________________` | `Kayin / Cain?` |
| `phrase_translation.015` | `phrase_translation` | `4:5 seg 2 - לֹא שָׁעָ֑ה` | `He (Hashem) didn't turn` | `source_literal_wording` | `________________` | `didn't turn / did not accept?` |
| `phrase_translation.023` | `phrase_translation` | `4:7 seg 4 - לַפֶּ֖תַח חַטָּ֣את רֹבֵ֑ץ` | `to the opening of your heart the sin (yetzer hara) crouches` | `phrase_sensitive` | `________________` | `sin crouches?` |
| `phrase_translation.032` | `phrase_translation` | `4:9 seg 2 - אֵ֖י הֶ֣בֶל אָחִ֑יךָ` | `where is Hevel your brother` | `name_alias_review` | `________________` | `Hevel / Abel?` |
| `phrase_translation.047` | `phrase_translation` | `4:14 seg 4 - וְהָיִ֜יתִי נָ֤ע וָנָד֙ בָּאָ֔רֶץ` | `and I will be moving and shaking in the land` | `source_literal_wording` | `________________` | `wandering / restless?` |
| `hebrew_to_english_match.004` | `hebrew_to_english_match` | `4:3 seg 3 - מִנְחָ֖ה לַֽיהֹוָֽה` | `a present to Hashem` | `alias_review` | `________________` | `present / offering?` |
| `hebrew_to_english_match.009` | `hebrew_to_english_match` | `4:7 seg 4 - לַפֶּ֖תַח חַטָּ֣את רֹבֵ֑ץ` | `to the opening of your heart the sin (yetzer hara) crouches` | `phrase_sensitive` | `________________` | `sin crouches?` |
| `hebrew_to_english_match.014` | `hebrew_to_english_match` | `4:9 seg 4 - הֲשֹׁמֵ֥ר אָחִ֖י אָנֹֽכִי` | `am I the guard of my brother?` | `phrase_sensitive` | `________________` | `guard / keeper / watchman?` |
| `english_to_hebrew_match.017` | `english_to_hebrew_match` | `moving and shaking you will be in the land` | `נָ֥ע וָנָ֖ד תִּֽהְיֶ֥ה בָאָֽרֶץ` | `source_literal_wording` | `________________` | `wandering / restless?` |
| `english_to_hebrew_match.022` | `english_to_hebrew_match` | `and Hashem placed a sign for Kayin` | `וַיָּ֨שֶׂם יְהֹוָ֤ה לְקַ֙יִן֙ א֔וֹת` | `alias_review` | `________________` | `sign / mark?` |

## Reviewer Notes Summary

- Overall extraction quality:
  - `Batch 005 is usable as an inactive reviewed-for-planning packet. The source trace is consistent, the Hebrew alignment source is explicit, and the extracted payload remains clearly isolated from runtime.`
- Most urgent alias / wording follow-up:
  - `Keep the source translations, but allow accepted-answer aliases for Kayin/Cain, Hevel/Abel, minchah as offering/gift-offering, וַיִּשַׁע / לֹא שָׁעָה as accepted-rejected phrasing, חַטָּאת רֹבֵץ as sin crouches wording, הֲשֹׁמֵר אָחִי אָנֹכִי as keeper/watchman wording, דְּמֵי אָחִיךָ as blood/bloods, נָע וָנָד as wandering/restless, אוֹת as sign/mark, and קִדְמַת־עֵדֶן as east of Eden.`
- Segments or preview items to revise first:
  - `Prioritize future accepted-alias handling for 4:3 seg 3, 4:4 seg 4, 4:5 seg 2, 4:7 seg 4, 4:9 seg 4, 4:10 seg 3, 4:12 seg 3, 4:15 seg 4, and 4:16 seg 3, since those are the main places where source-faithful wording is correct but potentially awkward or ambiguous for students.`
- Source preservation decision:
  - `Original source translations should remain unchanged in the extraction artifacts. The review resolution here is about accepted alias/context guidance only, not about rewriting the underlying Batch 005 JSONL or preview data.`
- Preview quality note:
  - `The preview set is suitable for inactive review use. Phrase-translation items intentionally behave like flashcard-style prompts, while the match lanes already carry usable same-batch distractors.`
- Runtime boundary:
  - `This manual review approves Batch 005 for future curriculum planning only. It does not make Batch 005 runtime active, and it does not promote any reviewed production question-bank data.`

## Final Recommendation

- Approval note: Batch 005 is approved for inactive merge and for future Batch 006 planning. This approval does not promote any extraction data into runtime. The extracted JSONL payload remains unchanged and still carries record-level `needs_review` flags.

- [x] APPROVE_BATCH_005_FOR_INACTIVE_MERGE
- [ ] NEEDS_MANUAL_REVIEW
- [ ] BLOCK_BATCH_005
