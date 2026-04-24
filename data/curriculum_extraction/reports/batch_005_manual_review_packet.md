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

- `קַיִן`: accepted aliases likely `Kayin` / `Cain`
- `הֶבֶל`: accepted aliases likely `Hevel` / `Abel`
- `אֶרֶץ־נוֹד`: likely `land of Nod`
- `קִדְמַת־עֵדֶן`: likely `east of Eden` / `toward the east of Eden`

### Source-Literal Phrases That May Need Smoother Accepted Wording

- `מִנְחָה`: source keeps `present`; later review may want `offering` / `gift-offering`
- `וַיִּשַׁע`: source keeps `turned`; later review may want `accepted` / `paid attention to`
- `לֹא שָׁעָה`: source keeps `didn't turn`; later review may want `did not accept` / `did not pay attention to`
- `נָע וָנָד`: source keeps `moving and shaking`; later review may want `wandering` / `restless wanderer`
- `אוֹת`: source keeps `sign`; later review may want `mark` depending on prompt context

### Exact-Phrase Watchlist

- `חַטָּאת רֹבֵץ`
- `הֲשֹׁמֵר אָחִי אָנֹכִי`
- `קוֹל דְּמֵי אָחִיךָ`
- `לְבִלְתִּי הַכּוֹת־אֹתוֹ כׇּל־מֹצְאֽוֹ`

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
  - `________________`
- Most urgent alias / wording follow-up:
  - `________________`
- Segments or preview items to revise first:
  - `________________`

## Final Recommendation

- [ ] APPROVE_BATCH_005_FOR_INACTIVE_MERGE
- [x] NEEDS_MANUAL_REVIEW
- [ ] BLOCK_BATCH_005
