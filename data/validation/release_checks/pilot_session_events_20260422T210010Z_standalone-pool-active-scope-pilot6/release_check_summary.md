# Release Check Summary

Generated: 2026-04-22T21:01:08.188629+00:00
Scope: local_parsed_bereishis_1_1_to_3_8
Pilot log: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\pilot\runs\pilot_session_events_20260422T210010Z_standalone-pool-active-scope-pilot6.jsonl

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
- Top served question families: {'translation': 25}
- Top rejection codes: [{'code': 'feature_repeat_blocked', 'count': 1080}, {'code': 'recent_exact_word_repeat', 'count': 86}, {'code': 'recent_exact_repeat', 'count': 30}]
- Warning codes: ['latest_session_only_applied', 'review_filters_applied']

## Hand Audit
- Question count: 25 requested 25
- Counts by lane: {'translation': 5, 'shoresh': 5, 'tense': 5, 'affix': 5, 'part_of_speech': 5}
- Counts by provenance: {'reviewed': 17, 'generated': 8}
- Duplicate-feel warnings: 0

## Artifact Paths
- pilot_review_json: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\validation\release_checks\pilot_session_events_20260422T210010Z_standalone-pool-active-scope-pilot6\pilot_review.json
- hand_audit_json: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\validation\release_checks\pilot_session_events_20260422T210010Z_standalone-pool-active-scope-pilot6\hand_audit.json
- hand_audit_markdown: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\validation\release_checks\pilot_session_events_20260422T210010Z_standalone-pool-active-scope-pilot6\hand_audit.md
- summary_json: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\validation\release_checks\pilot_session_events_20260422T210010Z_standalone-pool-active-scope-pilot6\release_check_summary.json
- summary_markdown: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\validation\release_checks\pilot_session_events_20260422T210010Z_standalone-pool-active-scope-pilot6\release_check_summary.md
