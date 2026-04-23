# Release Check Summary

Generated: 2026-04-22T20:05:21.241757+00:00
Scope: local_parsed_bereishis_1_1_to_3_8
Pilot log: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\pilot\runs\pilot_session_events_20260422T200346Z_quality-hardening-active-scope-pilot3.jsonl

## Gate Checks
- PASS `fresh_run_only`: True
- PASS `mixed_log_clear`: True
- PASS `trusted_scope_violations_clear`: 0
- PASS `served_without_validation_clear`: 0
- PASS `unclear_flags_clear`: 0

## Pilot Review
- Session count: 1
- Substantive vs shell: 1 substantive / 0 shell
- Trusted-scope violations: 0
- Served without validation: 0
- Top unclear items: []
- Top served question families: {'phrase_translation': 10, 'part_of_speech': 6, 'translation': 3, 'subject_identification': 3, 'prefix_level_1_identify_prefix_letter': 2, 'object_identification': 2}
- Top rejection codes: [{'code': 'feature_repeat_blocked', 'count': 559}, {'code': 'recent_exact_word_repeat', 'count': 73}, {'code': 'recent_prompt_repeat', 'count': 34}, {'code': 'recent_exact_repeat', 'count': 6}, {'code': 'diversity_redirect', 'count': 5}, {'code': 'recent_target_family_repeat', 'count': 1}]
- Warning codes: ['latest_session_only_applied', 'review_filters_applied']

## Hand Audit
- Question count: 25 requested 25
- Counts by lane: {'translation': 5, 'shoresh': 5, 'tense': 5, 'affix': 5, 'part_of_speech': 5}
- Counts by provenance: {'reviewed': 17, 'generated': 8}
- Duplicate-feel warnings: 0

## Artifact Paths
- pilot_review_json: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\validation\release_checks\pilot_session_events_20260422T200346Z_quality-hardening-active-scope-pilot3\pilot_review.json
- hand_audit_json: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\validation\release_checks\pilot_session_events_20260422T200346Z_quality-hardening-active-scope-pilot3\hand_audit.json
- hand_audit_markdown: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\validation\release_checks\pilot_session_events_20260422T200346Z_quality-hardening-active-scope-pilot3\hand_audit.md
- summary_json: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\validation\release_checks\pilot_session_events_20260422T200346Z_quality-hardening-active-scope-pilot3\release_check_summary.json
- summary_markdown: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\validation\release_checks\pilot_session_events_20260422T200346Z_quality-hardening-active-scope-pilot3\release_check_summary.md
