# Perek 1 Protected-Preview Input-List Planning Policy Report

## Why This Policy Exists

The Bereishis Perek 1 audit layer has 133 approved future input candidates and four approved family-level wording policies. This policy defines the constraints a later protected-preview input-list planning task must obey without creating that list.

## Current Approved Input-Candidate Count

- approved input candidates: 133

## Approved Family Counts

- `vocabulary_meaning`: 56
- `basic_noun_recognition`: 60
- `direct_object_marker_recognition`: 14
- `shoresh_identification`: 3

## Deferred Family Count

- `basic_verb_form_recognition`: 25 deferred rows

## What A Future Input-List Planning Task May Do

A future planning task may select a conservative subset of approved input candidates, copy their audit identifiers and source references into a planning-layer candidate file, and assign planning-only review statuses for wording, answer key, distractors, and context display.

## What It May Not Do

A future planning task may not generate questions, answer choices, answer keys, protected-preview content, reviewed-bank entries, runtime data, or student-facing content. It may not include verb-form rows or rows marked source-only, needs-follow-up, or blocked for questions.

## Required Future Fields

The required fields are defined in `data/question_eligibility_audits/protected_preview_input_list_planning_policy.v1.json` and include audit linkage, Hebrew token/phrase, approved family, canonical anchors, risk metadata, review statuses, and closed safety gates.

## First Batch Recommendation

The first planning batch should contain 20-30 input candidates, prioritize low-risk vocabulary/noun rows, include only a small sample of direct-object-marker rows, include only 1-3 shoresh rows, exclude verb-form rows, avoid duplicates unless intentional, avoid sensitive/high-risk/broad phrase-level rows, and preserve perek/pasuk spread if possible.

## Safety Gate Summary

- no questions generated
- no answer choices generated
- no answer keys generated
- no protected-preview input list created
- no protected-preview content created
- no reviewed-bank entries created
- no runtime changes made
- no student-facing use approved

## Recommended Next Task

Yossi reviews `data/question_eligibility_audits/reports/perek_1_protected_preview_input_list_planning_policy_yossi_review_packet.md`. After that, Codex applies only reviewed planning-policy decisions in a separate task.
