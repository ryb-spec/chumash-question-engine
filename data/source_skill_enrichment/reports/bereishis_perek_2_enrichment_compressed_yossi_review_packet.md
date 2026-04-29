# Bereishis Perek 2 Enrichment Compressed Yossi Review Packet

## A. Executive Summary

- raw candidate count: 1083
- compressed review group count: 167
- purpose: let Yossi make first-pass enrichment decisions by review group instead of row-by-row across 1,083 raw candidates
- no safety gates opened
- clean-group decisions were later applied separately: 91 token-split clean noun standards raw candidates are now verified for enrichment mapping only

## B. Recommended First-Pass Review Strategy

1. Review clean vocabulary/noun groups first.
2. Review clean shoresh groups second.
3. Review token-split standards groups third.
4. Treat phrase-level standards as follow-up/source-only where token-split rows are the preferred path.
5. Defer morphology/verb-form rows by default unless Yossi explicitly routes a group to follow-up with a safe standard.

Allowed recommended decisions in this packet: `verified`, `needs_follow_up`, `source_only`, `block_for_questions`, `fix_vocabulary`, `fix_standard`, `fix_morphology`.

## C. Clean Vocabulary/Noun Groups

| review_group_id | hebrew_token_or_pattern | refs_or_count | representative_candidate_ids | recommended_decision | risk_level |
| --- | --- | --- | --- | --- | --- |
| p2_comp_127 | אביו | 1 candidates; Bereishis 2:24 | p2_vocab_314 | needs_follow_up | medium |
| p2_comp_128 | אבן | 1 candidates; Bereishis 2:12 | p2_vocab_155 | needs_follow_up | medium |
| p2_comp_129 | אדם | 15 candidates; Bereishis 2:5, Bereishis 2:7, Bereishis 2:8, Bereishis 2:15, Bereishis 2:16, Bereishis 2:18, Bereishis 2:19, Bereishis 2:20 (+4 more refs) | p2_vocab_065, p2_vocab_083, p2_vocab_092, p2_vocab_104, p2_vocab_183, p2_vocab_193, p2_vocab_219, p2_vocab_239, p2_vocab_248, p2_vocab_254, +5 more | needs_follow_up | medium |
| p2_comp_130 | אדמה | 5 candidates; Bereishis 2:5, Bereishis 2:6, Bereishis 2:7, Bereishis 2:9, Bereishis 2:19 | p2_vocab_069, p2_vocab_078, p2_vocab_086, p2_vocab_111, p2_vocab_229 | needs_follow_up | medium |
| p2_comp_131 | איש | 1 candidates; Bereishis 2:24 | p2_vocab_312 | needs_follow_up | medium |
| p2_comp_132 | אלה | 1 candidates; Bereishis 2:4 | p2_vocab_036 | needs_follow_up | medium |
| p2_comp_133 | אמו | 1 candidates; Bereishis 2:24 | p2_vocab_316 | needs_follow_up | medium |
| p2_comp_134 | ארץ | 8 candidates; Bereishis 2:1, Bereishis 2:4, Bereishis 2:5, Bereishis 2:6, Bereishis 2:11, Bereishis 2:12, Bereishis 2:13 | p2_vocab_003, p2_vocab_039, p2_vocab_045, p2_vocab_064, p2_vocab_073, p2_vocab_144, p2_vocab_150, p2_vocab_165 | needs_follow_up | medium |
| p2_comp_135 | אשה | 1 candidates; Bereishis 2:23 | p2_vocab_304 | needs_follow_up | medium |
| p2_comp_136 | בדלח | 1 candidates; Bereishis 2:12 | p2_vocab_154 | needs_follow_up | medium |
| p2_comp_137 | בשר | 2 candidates; Bereishis 2:21, Bereishis 2:23 | p2_vocab_279, p2_vocab_300 | needs_follow_up | medium |
| p2_comp_138 | גן | 4 candidates; Bereishis 2:8, Bereishis 2:9, Bereishis 2:10, Bereishis 2:16 | p2_vocab_098, p2_vocab_121, p2_vocab_131, p2_vocab_197 | needs_follow_up | medium |

Yossi decision field: ______

Yossi notes field: ______

## D. Clean Shoresh Groups

| review_group_id | hebrew_token_or_pattern | refs_or_count | representative_candidate_ids | recommended_decision | risk_level |
| --- | --- | --- | --- | --- | --- |
| p2_comp_120 | ברא | 1 candidates; Bereishis 2:3 | p2_vocab_033 | needs_follow_up | medium |
| p2_comp_121 | הלך | 1 candidates; Bereishis 2:14 | p2_vocab_172 | needs_follow_up | medium |
| p2_comp_122 | חיה | 2 candidates; Bereishis 2:7, Bereishis 2:19 | p2_vocab_094, p2_vocab_250 | needs_follow_up | medium |
| p2_comp_123 | יצר | 2 candidates; Bereishis 2:8, Bereishis 2:19 | p2_vocab_106, p2_vocab_225 | needs_follow_up | medium |
| p2_comp_124 | לקח | 1 candidates; Bereishis 2:22 | p2_vocab_287 | needs_follow_up | medium |
| p2_comp_125 | מות | 1 candidates; Bereishis 2:17 | p2_vocab_211 | needs_follow_up | medium |
| p2_comp_126 | עשה | 2 candidates; Bereishis 2:2 | p2_vocab_012, p2_vocab_019 | needs_follow_up | medium |

Yossi decision field: ______

Yossi notes field: ______

## E. Token-Split Standards Groups

| review_group_id | hebrew_token_or_pattern | refs_or_count | representative_candidate_ids | recommended_decision | risk_level |
| --- | --- | --- | --- | --- | --- |
| p2_comp_014 | אביו | 1 candidates; Bereishis 2:24 | p2_tstd_314 | needs_follow_up | medium |
| p2_comp_015 | אבן | 1 candidates; Bereishis 2:12 | p2_tstd_155 | needs_follow_up | medium |
| p2_comp_016 | אדם | 15 candidates; Bereishis 2:5, Bereishis 2:7, Bereishis 2:8, Bereishis 2:15, Bereishis 2:16, Bereishis 2:18, Bereishis 2:19, Bereishis 2:20 (+4 more refs) | p2_tstd_065, p2_tstd_083, p2_tstd_092, p2_tstd_104, p2_tstd_183, p2_tstd_193, p2_tstd_219, p2_tstd_239, p2_tstd_248, p2_tstd_254, +5 more | needs_follow_up | medium |
| p2_comp_017 | אדמה | 5 candidates; Bereishis 2:5, Bereishis 2:6, Bereishis 2:7, Bereishis 2:9, Bereishis 2:19 | p2_tstd_069, p2_tstd_078, p2_tstd_086, p2_tstd_111, p2_tstd_229 | needs_follow_up | medium |
| p2_comp_018 | איש | 1 candidates; Bereishis 2:24 | p2_tstd_312 | needs_follow_up | medium |
| p2_comp_019 | אלה | 1 candidates; Bereishis 2:4 | p2_tstd_036 | needs_follow_up | medium |
| p2_comp_020 | אמו | 1 candidates; Bereishis 2:24 | p2_tstd_316 | needs_follow_up | medium |
| p2_comp_021 | ארץ | 8 candidates; Bereishis 2:1, Bereishis 2:4, Bereishis 2:5, Bereishis 2:6, Bereishis 2:11, Bereishis 2:12, Bereishis 2:13 | p2_tstd_003, p2_tstd_039, p2_tstd_045, p2_tstd_064, p2_tstd_073, p2_tstd_144, p2_tstd_150, p2_tstd_165 | needs_follow_up | medium |
| p2_comp_022 | אשה | 1 candidates; Bereishis 2:23 | p2_tstd_304 | needs_follow_up | medium |
| p2_comp_023 | בדלח | 1 candidates; Bereishis 2:12 | p2_tstd_154 | needs_follow_up | medium |
| p2_comp_024 | בשר | 2 candidates; Bereishis 2:21, Bereishis 2:23 | p2_tstd_279, p2_tstd_300 | needs_follow_up | medium |
| p2_comp_025 | גן | 4 candidates; Bereishis 2:8, Bereishis 2:9, Bereishis 2:10, Bereishis 2:16 | p2_tstd_098, p2_tstd_121, p2_tstd_131, p2_tstd_197 | needs_follow_up | medium |
| p2_comp_046 | אחד | 1 candidates; Bereishis 2:24 | p2_tstd_321 | needs_follow_up | medium |
| p2_comp_047 | אחת | 1 candidates; Bereishis 2:21 | p2_tstd_276 | needs_follow_up | medium |
| p2_comp_048 | אין | 1 candidates; Bereishis 2:5 | p2_tstd_066 | needs_follow_up | medium |
| p2_comp_049 | אכל | 2 candidates; Bereishis 2:16, Bereishis 2:17 | p2_tstd_198, p2_tstd_209 | needs_follow_up | medium |
| p2_comp_050 | אלה | 14 candidates; Bereishis 2:2, Bereishis 2:3, Bereishis 2:4, Bereishis 2:5, Bereishis 2:7, Bereishis 2:8, Bereishis 2:9, Bereishis 2:15 (+5 more refs) | p2_tstd_007, p2_tstd_021, p2_tstd_034, p2_tstd_044, p2_tstd_062, p2_tstd_081, p2_tstd_097, p2_tstd_109, p2_tstd_181, p2_tstd_191, +4 more | needs_follow_up | medium |
| p2_comp_051 | אעש | 1 candidates; Bereishis 2:18 | p2_tstd_221 | needs_follow_up | medium |
| p2_comp_052 | אשו | 1 candidates; Bereishis 2:14 | p2_tstd_174 | needs_follow_up | medium |
| p2_comp_053 | אתו | 1 candidates; Bereishis 2:3 | p2_tstd_026 | needs_follow_up | medium |
| p2_comp_054 | גיח | 1 candidates; Bereishis 2:13 | p2_tstd_160 | needs_follow_up | medium |
| p2_comp_055 | זאת | 2 candidates; Bereishis 2:23 | p2_tstd_296, p2_tstd_308 | needs_follow_up | medium |
| p2_comp_056 | חדק | 1 candidates; Bereishis 2:14 | p2_tstd_170 | needs_follow_up | medium |
| p2_comp_057 | חית | 2 candidates; Bereishis 2:19, Bereishis 2:20 | p2_tstd_231, p2_tstd_261 | needs_follow_up | medium |
| p2_comp_072 | א | 9 candidates; Bereishis 2:2, Bereishis 2:3, Bereishis 2:8, Bereishis 2:11, Bereishis 2:19, Bereishis 2:22 | p2_tstd_011, p2_tstd_018, p2_tstd_032, p2_tstd_105, p2_tstd_146, p2_tstd_238, p2_tstd_245, p2_tstd_286, p2_tstd_292 | needs_follow_up | high |
| p2_comp_073 | ב | 13 candidates; Bereishis 2:2, Bereishis 2:3, Bereishis 2:4, Bereishis 2:5, Bereishis 2:7, Bereishis 2:8, Bereishis 2:9, Bereishis 2:15 (+2 more refs) | p2_tstd_008, p2_tstd_014, p2_tstd_028, p2_tstd_033, p2_tstd_040, p2_tstd_041, p2_tstd_052, p2_tstd_088, p2_tstd_099, p2_tstd_120, +3 more | needs_follow_up | high |
| p2_comp_074 | ה | 21 candidates; Bereishis 2:5, Bereishis 2:9, Bereishis 2:11, Bereishis 2:12, Bereishis 2:13, Bereishis 2:14, Bereishis 2:17, Bereishis 2:18 (+3 more refs) | p2_tstd_060, p2_tstd_123, p2_tstd_138, p2_tstd_140, p2_tstd_141, p2_tstd_145, p2_tstd_151, p2_tstd_156, p2_tstd_159, p2_tstd_161, +11 more | needs_follow_up | high |
| p2_comp_075 | ו | 17 candidates; Bereishis 2:1, Bereishis 2:5, Bereishis 2:6, Bereishis 2:10, Bereishis 2:15, Bereishis 2:17, Bereishis 2:19, Bereishis 2:20 (+2 more refs) | p2_tstd_004, p2_tstd_047, p2_tstd_053, p2_tstd_070, p2_tstd_074, p2_tstd_132, p2_tstd_134, p2_tstd_188, p2_tstd_200, p2_tstd_244, +7 more | needs_follow_up | high |
| p2_comp_076 | כ | 14 candidates; Bereishis 2:3, Bereishis 2:5, Bereishis 2:6, Bereishis 2:9, Bereishis 2:11, Bereishis 2:13, Bereishis 2:17, Bereishis 2:18 (+4 more refs) | p2_tstd_027, p2_tstd_058, p2_tstd_076, p2_tstd_112, p2_tstd_143, p2_tstd_164, p2_tstd_166, p2_tstd_207, p2_tstd_224, p2_tstd_230, +4 more | needs_follow_up | high |
| p2_comp_077 | ל | 24 candidates; Bereishis 2:3, Bereishis 2:5, Bereishis 2:7, Bereishis 2:9, Bereishis 2:10, Bereishis 2:15, Bereishis 2:16, Bereishis 2:17 (+6 more refs) | p2_tstd_035, p2_tstd_059, p2_tstd_067, p2_tstd_093, p2_tstd_115, p2_tstd_117, p2_tstd_129, p2_tstd_135, p2_tstd_187, p2_tstd_194, +14 more | needs_follow_up | high |
| p2_comp_078 | מ | 18 candidates; Bereishis 2:2, Bereishis 2:3, Bereishis 2:6, Bereishis 2:7, Bereishis 2:8, Bereishis 2:9, Bereishis 2:10, Bereishis 2:16 (+6 more refs) | p2_tstd_016, p2_tstd_030, p2_tstd_072, p2_tstd_085, p2_tstd_100, p2_tstd_110, p2_tstd_128, p2_tstd_195, p2_tstd_206, p2_tstd_210, +8 more | needs_follow_up | high |
| p2_comp_079 | ע | 4 candidates; Bereishis 2:5, Bereishis 2:16, Bereishis 2:21, Bereishis 2:24 | p2_tstd_063, p2_tstd_192, p2_tstd_272, p2_tstd_309 | needs_follow_up | high |
| p2_comp_080 | ש | 5 candidates; Bereishis 2:3, Bereishis 2:5, Bereishis 2:19, Bereishis 2:20, Bereishis 2:25 | p2_tstd_029, p2_tstd_048, p2_tstd_252, p2_tstd_255, p2_tstd_323 | needs_follow_up | high |
| p2_comp_045 | את / direct-object marker | 13 candidates; Bereishis 2:3, Bereishis 2:5, Bereishis 2:6, Bereishis 2:7, Bereishis 2:8, Bereishis 2:10, Bereishis 2:11, Bereishis 2:13 (+4 more refs) | p2_tstd_022, p2_tstd_068, p2_tstd_075, p2_tstd_082, p2_tstd_103, p2_tstd_130, p2_tstd_142, p2_tstd_163, p2_tstd_182, p2_tstd_233, +3 more | needs_follow_up | high |
| p2_comp_081 | verb-form-sensitive token-split rows | 55 candidates; Bereishis 2:1, Bereishis 2:2, Bereishis 2:3, Bereishis 2:4, Bereishis 2:5, Bereishis 2:6, Bereishis 2:7, Bereishis 2:8 (+13 more refs) | p2_tstd_001, p2_tstd_006, p2_tstd_013, p2_tstd_020, p2_tstd_023, p2_tstd_025, p2_tstd_037, p2_tstd_043, p2_tstd_051, p2_tstd_057, +45 more | needs_follow_up | high |

Yossi decision field: ______

Yossi notes field: ______

## F. Phrase-Level Standards

| review_group_id | hebrew_token_or_pattern | refs_or_count | representative_candidate_ids | recommended_decision | risk_level |
| --- | --- | --- | --- | --- | --- |
| p2_comp_013 | phrase-level standards parent rows | 99 candidates; Bereishis 2:1, Bereishis 2:2, Bereishis 2:3, Bereishis 2:4, Bereishis 2:5, Bereishis 2:6, Bereishis 2:7, Bereishis 2:8 (+17 more refs) | p2_std_001, p2_std_002, p2_std_003, p2_std_004, p2_std_005, p2_std_006, p2_std_007, p2_std_008, p2_std_009, p2_std_010, +89 more | source_only | medium |

Yossi decision field: ______

Yossi notes field: ______

## G. Morphology / Verb Forms

| review_group_id | hebrew_token_or_pattern | refs_or_count | representative_candidate_ids | recommended_decision | risk_level |
| --- | --- | --- | --- | --- | --- |
| p2_comp_011 | future / jussive / imperfect-looking form | 29 candidates; Bereishis 2:3, Bereishis 2:4, Bereishis 2:5, Bereishis 2:6, Bereishis 2:7, Bereishis 2:8, Bereishis 2:9, Bereishis 2:10 (+10 more refs) | p2_morph_023, p2_morph_037, p2_morph_043, p2_morph_051, p2_morph_057, p2_morph_061, p2_morph_071, p2_morph_080, p2_morph_096, p2_morph_106, +19 more | needs_follow_up | high |
| p2_comp_012 | vav narrative / vav hahipuch | 26 candidates; Bereishis 2:1, Bereishis 2:2, Bereishis 2:3, Bereishis 2:7, Bereishis 2:8, Bereishis 2:9, Bereishis 2:15, Bereishis 2:16 (+7 more refs) | p2_morph_001, p2_morph_006, p2_morph_013, p2_morph_020, p2_morph_025, p2_morph_079, p2_morph_087, p2_morph_091, p2_morph_095, p2_morph_101, +16 more | needs_follow_up | high |
| p2_comp_009 | heh/article or stem-sensitive form | 55 candidates; Bereishis 2:1, Bereishis 2:2, Bereishis 2:3, Bereishis 2:4, Bereishis 2:5, Bereishis 2:6, Bereishis 2:7, Bereishis 2:8 (+15 more refs) | p2_morph_002, p2_morph_009, p2_morph_015, p2_morph_024, p2_morph_038, p2_morph_049, p2_morph_055, p2_morph_060, p2_morph_064, p2_morph_069, +45 more | needs_follow_up | high |
| p2_comp_010 | suffix / construct / number-sensitive form | 84 candidates; Bereishis 2:1, Bereishis 2:2, Bereishis 2:3, Bereishis 2:4, Bereishis 2:5, Bereishis 2:6, Bereishis 2:7, Bereishis 2:8 (+17 more refs) | p2_morph_005, p2_morph_007, p2_morph_008, p2_morph_010, p2_morph_012, p2_morph_014, p2_morph_017, p2_morph_019, p2_morph_021, p2_morph_026, +74 more | needs_follow_up | high |
| p2_comp_001 | אל | 2 candidates; Bereishis 2:19, Bereishis 2:22 | p2_morph_238, p2_morph_292 | source_only | medium |
| p2_comp_002 | אשר | 7 candidates; Bereishis 2:2, Bereishis 2:3, Bereishis 2:8, Bereishis 2:11, Bereishis 2:19, Bereishis 2:22 | p2_morph_011, p2_morph_018, p2_morph_032, p2_morph_105, p2_morph_146, p2_morph_245, p2_morph_286 | source_only | medium |
| p2_comp_003 | את | 11 candidates; Bereishis 2:3, Bereishis 2:5, Bereishis 2:6, Bereishis 2:7, Bereishis 2:8, Bereishis 2:10, Bereishis 2:11, Bereishis 2:13 (+3 more refs) | p2_morph_022, p2_morph_068, p2_morph_075, p2_morph_082, p2_morph_103, p2_morph_130, p2_morph_142, p2_morph_163, p2_morph_182, p2_morph_284, +1 more | source_only | medium |
| p2_comp_004 | כל | 6 candidates; Bereishis 2:6, Bereishis 2:9, Bereishis 2:11, Bereishis 2:13, Bereishis 2:19 | p2_morph_076, p2_morph_112, p2_morph_143, p2_morph_164, p2_morph_230, p2_morph_234 | source_only | medium |
| p2_comp_005 | לא | 4 candidates; Bereishis 2:5, Bereishis 2:17, Bereishis 2:18, Bereishis 2:20 | p2_morph_059, p2_morph_204, p2_morph_216, p2_morph_264 | source_only | medium |
| p2_comp_006 | מן | 5 candidates; Bereishis 2:6, Bereishis 2:7, Bereishis 2:9, Bereishis 2:19, Bereishis 2:22 | p2_morph_072, p2_morph_085, p2_morph_110, p2_morph_228, p2_morph_288 | source_only | medium |
| p2_comp_007 | על | 4 candidates; Bereishis 2:5, Bereishis 2:16, Bereishis 2:21, Bereishis 2:24 | p2_morph_063, p2_morph_192, p2_morph_272, p2_morph_309 | source_only | medium |
| p2_comp_008 | general morphology deferred | 95 candidates; Bereishis 2:1, Bereishis 2:2, Bereishis 2:3, Bereishis 2:4, Bereishis 2:5, Bereishis 2:6, Bereishis 2:7, Bereishis 2:8 (+17 more refs) | p2_morph_003, p2_morph_004, p2_morph_016, p2_morph_029, p2_morph_030, p2_morph_033, p2_morph_035, p2_morph_039, p2_morph_042, p2_morph_045, +85 more | needs_follow_up | high |

Yossi decision field: ______

Yossi notes field: ______

## H. Safety Statement

This is enrichment review only. It is not question approval, protected-preview approval, reviewed-bank approval, runtime approval, or student-facing approval.
This is enrichment review only: not question approval, not protected-preview approval, not reviewed-bank approval, not runtime approval, and not student-facing approval.

Raw Perek 2 enrichment rows outside the clean-group decision crosswalk remain review-only with closed gates; clean-group decisions are documented separately and do not approve questions or preview/runtime use.

## Clean-Group Decision Application Note

Yossi clean-group decisions were later applied through the clean-group crosswalk: 31 token-split clean noun standards groups / 91 raw candidates were verified for enrichment mapping only, and 38 clean vocabulary/shoresh groups / 100 raw candidates remain needs_follow_up. This does not approve questions, protected-preview use, reviewed-bank use, runtime use, or student-facing use.
