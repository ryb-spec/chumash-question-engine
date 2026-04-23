# Release Check Summary

Generated: 2026-04-22T18:58:52.773113+00:00
Scope: local_parsed_bereishis_1_1_to_3_8
Pilot log: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\pilot\runs\pilot_session_events_20260422T185453Z_current-scope-branch-evidence_1.jsonl

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
- Top served question families: {'phrase_translation': 13, 'part_of_speech': 4, 'object_identification': 4, 'subject_identification': 3, 'shoresh': 2, 'prefix_level_1_identify_prefix_letter': 1}
- Top rejection codes: [{'code': 'feature_repeat_blocked', 'count': 331}, {'code': 'recent_exact_word_repeat', 'count': 33}, {'code': 'recent_prompt_repeat', 'count': 16}, {'code': 'diversity_redirect', 'count': 5}]
- Warning codes: ['review_filters_applied']

## Hand Audit
- Question count: 25 requested 25
- Counts by lane: {'translation': 5, 'shoresh': 5, 'tense': 5, 'affix': 5, 'part_of_speech': 5}
- Counts by provenance: {'reviewed': 10, 'generated': 15}
- Duplicate-feel warnings: 0

## Artifact Paths
- pilot_review_json: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\validation\release_checks\pilot_session_events_20260422T185453Z_current-scope-branch-evidence_1\pilot_review.json
- hand_audit_json: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\validation\release_checks\pilot_session_events_20260422T185453Z_current-scope-branch-evidence_1\hand_audit.json
- hand_audit_markdown: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\validation\release_checks\pilot_session_events_20260422T185453Z_current-scope-branch-evidence_1\hand_audit.md
- summary_json: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\validation\release_checks\pilot_session_events_20260422T185453Z_current-scope-branch-evidence_1\release_check_summary.json
- summary_markdown: C:\Users\ybassman\Documents\GitHub\chumash-question-engine\data\validation\release_checks\pilot_session_events_20260422T185453Z_current-scope-branch-evidence_1\release_check_summary.md
