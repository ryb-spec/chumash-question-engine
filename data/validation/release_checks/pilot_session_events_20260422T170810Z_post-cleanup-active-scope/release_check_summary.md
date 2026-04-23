# Release Check Summary

Generated: 2026-04-22T17:33:14.383073+00:00
Scope: local_parsed_bereishis_1_1_to_3_8
Pilot log: data\pilot\runs\pilot_session_events_20260422T170810Z_post-cleanup-active-scope.jsonl

## Gate Checks
- PASS `fresh_run_only`: True
- PASS `mixed_log_clear`: True
- PASS `trusted_scope_violations_clear`: 0
- PASS `served_without_validation_clear`: 0
- WARN `unclear_flags_clear`: 2

## Pilot Review
- Session count: 1
- Substantive vs shell: 1 substantive / 0 shell
- Trusted-scope violations: 0
- Served without validation: 0
- Top unclear items: [{'pasuk_ref': 'Bereishis 2:7', 'question_type': 'phrase_translation', 'question_text': 'What does this phrase mean?', 'selected_word': 'וַיִּיצֶר יְהוָה אֱלֹהִים אֶת הָאָדָם', 'repeat_count': 1, 'teacher_label': 'unclear wording'}, {'pasuk_ref': 'Bereishis 3:1', 'question_type': 'translation', 'question_text': 'What does עָרוּם mean?', 'selected_word': 'עָרוּם', 'repeat_count': 1, 'teacher_label': None}]
- Top served question families: {'shoresh': 5, 'translation': 3, 'phrase_translation': 3, 'identify_tense': 3, 'prefix_level_1_identify_prefix_letter': 1, 'verb_tense': 1}
- Top rejection codes: [{'code': 'feature_repeat_blocked', 'count': 410}, {'code': 'recent_surface_pattern_repeat', 'count': 17}, {'code': 'diversity_redirect', 'count': 9}, {'code': 'recent_exact_word_repeat', 'count': 3}]
- Warning codes: ['latest_session_only_applied', 'review_filters_applied']

## Hand Audit
- Question count: 25 requested 25
- Counts by lane: {'translation': 5, 'shoresh': 5, 'tense': 5, 'affix': 5, 'part_of_speech': 5}
- Counts by provenance: {'reviewed': 10, 'generated': 15}
- Duplicate-feel warnings: 0

## Artifact Paths
- pilot_review_json: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\validation\release_checks\pilot_session_events_20260422T170810Z_post-cleanup-active-scope\pilot_review.json
- hand_audit_json: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\validation\release_checks\pilot_session_events_20260422T170810Z_post-cleanup-active-scope\hand_audit.json
- hand_audit_markdown: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\validation\release_checks\pilot_session_events_20260422T170810Z_post-cleanup-active-scope\hand_audit.md
- summary_json: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\validation\release_checks\pilot_session_events_20260422T170810Z_post-cleanup-active-scope\release_check_summary.json
- summary_markdown: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\validation\release_checks\pilot_session_events_20260422T170810Z_post-cleanup-active-scope\release_check_summary.md
