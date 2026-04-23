# Release Check Summary

Generated: 2026-04-22T11:55:59.883072+00:00
Scope: local_parsed_bereishis_1_1_to_3_8
Pilot log: data\pilot\runs\pilot_session_events_20260422T113750Z_release-check.jsonl

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
- Top unclear items: [{'pasuk_ref': 'Bereishis 3:3', 'question_type': 'shoresh', 'question_text': 'What is the shoresh of אָמַר?', 'selected_word': 'אָמַר', 'repeat_count': 1, 'teacher_label': None}, {'pasuk_ref': 'Bereishis 2:11', 'question_type': 'translation', 'question_text': 'What does הוּא mean?', 'selected_word': 'הוּא', 'repeat_count': 1, 'teacher_label': None}]
- Top served question families: {'phrase_translation': 5, 'shoresh': 5, 'identify_tense': 3, 'prefix_level_1_identify_prefix_letter': 1, 'translation': 1}
- Top rejection codes: [{'code': 'feature_repeat_blocked', 'count': 366}, {'code': 'recent_surface_pattern_repeat', 'count': 16}, {'code': 'diversity_redirect', 'count': 9}]
- Warning codes: ['latest_session_only_applied', 'review_filters_applied']

## Hand Audit
- Question count: 12 requested 12
- Counts by lane: {'translation': 3, 'shoresh': 3, 'tense': 2, 'affix': 2, 'part_of_speech': 2}
- Counts by provenance: {'reviewed': 5, 'generated': 7}
- Duplicate-feel warnings: 0

## Artifact Paths
- pilot_review_json: data\validation\release_checks\pilot_session_events_20260422T113750Z_release-check_human_feel_cleanup\pilot_review.json
- hand_audit_json: data\validation\release_checks\pilot_session_events_20260422T113750Z_release-check_human_feel_cleanup\hand_audit.json
- hand_audit_markdown: data\validation\release_checks\pilot_session_events_20260422T113750Z_release-check_human_feel_cleanup\hand_audit.md
- summary_json: data\validation\release_checks\pilot_session_events_20260422T113750Z_release-check_human_feel_cleanup\release_check_summary.json
- summary_markdown: data\validation\release_checks\pilot_session_events_20260422T113750Z_release-check_human_feel_cleanup\release_check_summary.md
