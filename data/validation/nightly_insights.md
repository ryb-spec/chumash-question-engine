# Nightly Insights

## Summary

- Total attempts: 928
- Total incorrect: 193

## Most Missed Words

- `לָאוֹר`: 97
- `למינו`: 11
- `וְתֵרָאֶה`: 6
- `וִיהִי`: 6
- `מים`: 4
- `במים`: 4
- `ויקרא`: 4
- `אֱלֹקִים`: 4
- `וַיַּרְא`: 4
- `תדשא`: 3

## Most Missed Skills

- `identify_prefix_meaning`: 122
- `identify_tense`: 24
- `translation`: 15
- `identify_suffix_meaning`: 14
- `verb_tense`: 5
- `subject_identification`: 4
- `shoresh`: 3
- `suffix`: 2
- `phrase_translation`: 2
- `part_of_speech`: 2

## Most Missed Question Types

- `identify_tense`: 24
- `suffix`: 15
- `prefix`: 15
- `prefix_level_1_identify_prefix_letter`: 10
- `translation`: 9
- `word_meaning`: 6
- `verb_tense`: 5
- `subject_identification`: 4
- `shoresh`: 3
- `phrase_translation`: 2

## Most Missed Standards

- `PR`: 163
- `WM`: 15
- `CF`: 4
- `SS`: 4
- `PS`: 4
- `SR`: 3

## Words Missed 3+ Times

- `לָאוֹר`: 97
- `למינו`: 11
- `וְתֵרָאֶה`: 6
- `וִיהִי`: 6
- `מים`: 4
- `במים`: 4
- `ויקרא`: 4
- `אֱלֹקִים`: 4
- `וַיַּרְא`: 4
- `תדשא`: 3
- `וַיְהִי`: 3
- `עֲשׂוֹת`: 3
- `וְהִשְׁקָה`: 3

## Suggested Review Targets

- Review prefix meaning questions.
- Add more gold cases for לָאוֹר, למינו, וְתֵרָאֶה, and related forms.
- Review the identify_tense question type with a few extra examples.
- Revisit standard PR with a short targeted review set.

## Recommended Next Actions

- Prioritize noun suffix fallback fixes.
- Tighten prefix handling and add more prefix review coverage.
- Add reteach practice for PR-standard items.
- Expand gold cases for repeated trouble words.
- Review suffix-bearing noun forms that are still being over-literalized.
- Review prefix meaning distractors and reteach sequencing.

## Gold Failures to Review

- No gold-failure summary is available yet.

## Pilot Repetition Signals

### Top Repeated Prompts

- `prefix_level_3_apply_prefix_meaning` -> `What does לָאוֹר mean?`: 188
- `identify_tense` -> `What form is shown?`: 11
- `phrase_translation` -> `What does this phrase mean?`: 9
- `shoresh` -> `What is the shoresh of וַיַּעַשׂ?`: 4
- `shoresh` -> `What is the shoresh of וַיֹּאמֶר?`: 4

### Top Repeated Target Words

- `prefix_level_3_apply_prefix_meaning` -> `לָאוֹר`: 188
- `shoresh` -> `וַיַּעַשׂ`: 4
- `shoresh` -> `וַיֹּאמֶר`: 4
- `prefix_level_1_identify_prefix_letter` -> `בַּיּוֹם`: 3
- `prefix_level_1_identify_prefix_letter` -> `בְּיוֹם`: 3

### Top Repeated Translation Meanings

- `god`: 2

### Tense-Lane Overlap Targets

- `וְתֵרָאֶה`: identify_tense, verb_tense

### Shoresh Surface Pattern Concentration

- `vav_yod_surface`: 21
- `vav_led_surface`: 2
- `plain_surface`: 2

### Dominant Correct Answer Concentration by Lane

- `prefix_level_3_apply_prefix_meaning` -> `to / for light`: 188/188 (100%)
- `prefix_level_1_identify_prefix_letter` -> `ב`: 6/6 (100%)
- `verb_tense` -> `future`: 3/3 (100%)
- `part_of_speech` -> `naming word`: 2/2 (100%)
- `identify_tense` -> `past`: 6/11 (55%)
- `phrase_translation` -> `God created`: 2/9 (22%)

### Reuse Triggered by Reteach vs Exhaustion

- No reuse events recorded yet.

### Diversity Redirects

- `identify_prefix_meaning`: 38

## Pre-Serve Validation Signals

### Top Rejection Codes

- `feature_repeat_blocked`: 514
- `recent_exact_word_repeat`: 295
- `explanation_target_conflict`: 127
- `invalid_tense_target`: 64
- `invalid_shoresh_target`: 63
- `incompatible_skill_target`: 21
- `diversity_redirect`: 18
- `recent_target_repeat`: 13
- `recent_exact_repeat`: 4
- `recent_same_pasuk_intent_repeat`: 1

### Rejection Counts by Lane

- `shoresh` -> `feature_repeat_blocked`: 216
- `shoresh` -> `recent_exact_word_repeat`: 171
- `identify_tense` -> `feature_repeat_blocked`: 153
- `identify_tense` -> `recent_exact_word_repeat`: 94
- `phrase_translation` -> `feature_repeat_blocked`: 91
- `shoresh` -> `invalid_shoresh_target`: 63
- `shoresh` -> `explanation_target_conflict`: 63
- `identify_tense` -> `invalid_tense_target`: 55
- `identify_tense` -> `explanation_target_conflict`: 55
- `translation` -> `feature_repeat_blocked`: 54

### Served Questions Missing Validation Flag

- Served with validation flag: 42
- Served missing validation flag: 213

### Served Questions Outside Active Scope

- `prefix_level_3_apply_prefix_meaning`: 188
