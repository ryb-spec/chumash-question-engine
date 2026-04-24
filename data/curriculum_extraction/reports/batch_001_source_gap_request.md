# Batch 001 Source Gap Request

## Stop Reason

Phase 3C cannot continue in this worktree because the required source PDFs are not present in the repo/worktree.

Search results:

- `13726D_g_01023_first_150_shorashim_and_keywords_in_chumash.pdf` — not found
- `12944_b_01757_01_parshas_shemos_shorashim_prefix_suffix.pdf` — not found
- `14016C_b_01758_01_text_skills.pdf` — not found
- `7984C_b_01409_pshat_of_torah.pdf` — not found

No local PDF files were found anywhere under this repository checkout.

## Exact Source Material Needed

### 1. First 150 Shorashim and Keywords in Bereishis

Expected file:

- `13726D_g_01023_first_150_shorashim_and_keywords_in_chumash.pdf`

Needed content:

- the glossary/keyword entries that could provide source-backed English glosses for:
  - `ארץ`
  - `אדם`
  - `אשה`
  - `בית`
  - `בן`
  - `יום`
  - `מים`
  - `עץ`

Needed proof shape:

- exact page(s)
- exact keyword/gloss line(s)
- enough source snippet to support copying the gloss into the normalized `vocab_entry` records

### 2. Bacharach Shemos Shorashim, Prefix and Suffix Skills

Expected file:

- `12944_b_01757_01_parshas_shemos_shorashim_prefix_suffix.pdf`

Needed content:

- the answer-key page(s) for the 8 blocked Batch 001 task rows so the following can be filled from source:
  - `expected_word_in_pasuk`
  - `prefixes`
  - `suffixes`
  - `contextual_translation` or equivalent source-backed translation field

Blocked task targets:

- Shemos 1:1 — `בוא` (first occurrence)
- Shemos 1:1 — `בוא` (second occurrence)
- Shemos 1:6 — `מות`
- Shemos 1:7 — `פרה`
- Shemos 1:7 — `שרץ`
- Shemos 1:7 — `רבה`
- Shemos 1:7 — `עצם`
- Shemos 1:7 — `מלא`

Needed proof shape:

- exact answer-key page(s)
- exact word-in-pasuk / prefix / suffix / translation entries for each blocked task row

### 3. Bacharach Va’eira Textual Skills

Expected file:

- `14016C_b_01758_01_text_skills.pdf`

Needed content:

- the answer-key page(s) for the 10 blocked comprehension prompts so `expected_answer` can be filled only where explicitly provided

Blocked comprehension rows:

- `comp_question_vaeira_6_3_001`
- `comp_question_vaeira_6_3_002`
- `comp_question_vaeira_6_4_003`
- `comp_question_vaeira_6_5_004`
- `comp_question_vaeira_6_6_005`
- `comp_question_vaeira_6_6_006`
- `comp_question_vaeira_6_6_007`
- `comp_question_vaeira_6_7_008`
- `comp_question_vaeira_6_8_009`
- `comp_question_vaeira_6_9_010`

Needed proof shape:

- exact answer-key page(s)
- exact answer lines for each `מי אמר אל מי` / `על מי נאמר` prompt

### 4. Linear Chumash Translation

Expected file:

- `7984C_b_01409_pshat_of_torah.pdf`

Needed content:

- fallback source-backed translation lines only if used to support blocked vocab entries that are not covered by the primary Bereishis keyword/glossary source

Needed proof shape:

- exact page(s)
- exact Hebrew phrase/word and English translation line(s)
- enough context to show the gloss is truly source-backed rather than inferred

## Recommendation

- Provide the missing PDF files, or provide cleaned answer-bearing excerpts from those files under `data/curriculum_extraction/raw_sources/batch_001/`.
- After those source files or cleaned answer-key excerpts are available, rerun Phase 3C on `isolated/curriculum-extraction-factory`.
