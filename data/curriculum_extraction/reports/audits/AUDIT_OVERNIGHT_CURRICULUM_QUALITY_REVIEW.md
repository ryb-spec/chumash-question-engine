# Overnight Curriculum Quality Review Audit

Branch: `audit/overnight-curriculum-quality-review`

Scope: full-repo curriculum-quality, assessment-quality, source-integrity, preview-gate, validator, reporting, and maintainability audit. This audit created documentation only. It does not change runtime behavior, scoring, mastery logic, UI, assessment scope, question generation logic, reviewed-bank data, or protected-preview approval state.

## 1. Executive summary

### Top 10 findings ranked by likely impact

1. **High - Runtime coverage is much broader than reviewed preview coverage.** The active assessment scope is `local_parsed_bereishis_1_1_to_3_24` with 80 pesukim, while protected-preview reviewed packet coverage is currently much narrower and mostly `basic_noun_recognition`. Dynamic runtime generation remains the largest quality surface. Evidence: `assessment_scope.py:308`, `assessment_scope.py:827`, `data/corpus_manifest.json:200`, `engine/flow_builder.py:3444`, `data/gate_2_protected_preview_packets/bereishis_perek_2_internal_protected_preview_packet.tsv`.
2. **High - Translation/context candidates have a low safe-valid rate in the audit output.** `scripts/generate_question_validation_audit.py` reported translation/context validity at 223 valid / 1109 total, or 20.1%, with 440 `placeholder_translation`, 243 `low_instructional_value`, and 203 `grammatical_particle` rejections. This is the clearest signal that many generated candidates are not yet strong mastery evidence.
3. **High - Suffix and compound morphology remain fragile.** The same audit found suffix validity at 94 / 258, or 36.4%, and many failures from compound morphology, no clear suffix, plural endings, or ambiguous morphology. This directly affects whether students are assessed on real skill or surface pattern matching.
4. **High - Standards alignment exists, but standards-based mastery reporting is not yet the organizing product surface.** The canonical skill contract is strong, but many Zekelman mappings are `review_only`, and runtime mastery still primarily flows through runtime skill IDs rather than a teacher-facing standards dashboard. Evidence: `data/standards/canonical_skill_contract.json:8`, `data/standards/canonical_skill_contract.json:1130`, `skill_catalog.py:60`, `docs/runtime_skill_canonical_alignment.md`.
5. **Medium - Diagnostic preview is strong but only covers a limited slice.** The diagnostic preview for Bereishis 1:1-2:3 generated 77 questions, 33 reviewable items, and 6 caution flags. It is teacher-useful, but it does not yet provide comparable review evidence for the full active 1:1-3:24 scope.
6. **Medium - Perek 3 candidate gating is correctly fail-closed, but the pre-decision review packet can become stale after decisions are applied.** The Perek 3 applied-decision report correctly records 4 approved-for-internal-packet, 4 revision, and 2 follow-up decisions; the original packet still contains historical pending language. Evidence: `data/gate_2_protected_preview_candidates/reports/bereishis_perek_3_protected_preview_candidate_yossi_review_applied.md:14`, `data/gate_2_protected_preview_candidates/reports/bereishis_perek_3_protected_preview_candidate_review_packet.md:192`.
7. **Medium - Validator coverage is broad but fragmented.** There are many excellent validators, but CI only runs pytest and report generators. Many fail-closed curriculum validators are manual unless called by tests. Evidence: `.github/workflows/python-tests.yml:25`, `.github/workflows/python-tests.yml:28`, `scripts/validate_*.py`.
8. **Medium - Source integrity is strong, but item-level source lineage is not consistently visible in runtime-like outputs.** Source text validation passed across 1,533 Bereishis rows, and Koren/Metsudah translations both have 1,533 rows. The remaining opportunity is not basic source presence, but explicit lineage from each served item back to source row, translation layer, and review authority.
9. **Medium - Runtime question checks validate structure more than pedagogy.** Tests and final validation enforce four choices, uniqueness, correct answer inclusion, and some family-specific safety, but pedagogical usefulness of explanations and distractor intent is more mature in diagnostic/protected preview artifacts than in dynamic generation.
10. **Low/Medium - Repo instructions and legacy entry points can mislead contributors.** `README.md` still advertises old unittest-style commands while `pytest.ini` and CI use pytest. Legacy files are labeled, but command drift increases the chance of incomplete validation.

### Biggest opportunity

The biggest opportunity is to create a single teacher-facing standards-and-evidence dashboard/report that joins active runtime questions, the canonical skill contract, source validation, question-validation audit metrics, diagnostic/protected-preview status, and mastery outcomes. Right now the repo has many strong gates, but they are spread across validators, TSVs, reports, and tests. A joined report would let Yossi and engineering choose the next work by highest learning value and highest safety risk: for example, expanding strong noun/vocabulary items, restricting weak translation/context candidates, and building reviewed remediation paths for suffix and compound morphology before those lanes become prominent student-facing assessment evidence.

## 2. System map

### Runtime and active scope

- Supported live runtime: `streamlit_app.py` as documented in `README.md` and `AGENTS.md`.
- Active assessment scope and corpus gates: `assessment_scope.py`.
- Active scope ID found in data: `data/corpus_manifest.json:200` and `data/corpus_manifest.json:264` use `local_parsed_bereishis_1_1_to_3_24`.
- Active scope summary reports 80 pesukim from Bereishis 1:1-3:24 via `assessment_scope.py:827`.
- Dynamic question generation path: `engine/flow_builder.py:3444` defines `generate_question`; reviewed-bank preference appears before dynamic fallback around `engine/flow_builder.py:3531`.
- Mastery / scoring / progress: `skill_tracker.py`, runtime tests under `tests/test_runtime_question_flow.py`, `tests/test_streamlit_quiz_experience.py`, and related files.

### Standards and skill truth

- Runtime skill catalog: `skill_catalog.py`, especially `SKILL_CATALOG` around `skill_catalog.py:60`.
- Canonical skill contract: `data/standards/canonical_skill_contract.json`.
- Contract validation: `scripts/validate_canonical_skill_contract.py`.
- Runtime/canonical alignment documentation: `docs/runtime_skill_canonical_alignment.md`.
- Foundation layering documentation: `docs/foundations_layers.md`.
- Standards data validation: `scripts/validate_standards_data.py`.

### Sources and transformations

- Canonical Hebrew source text: `data/source_texts/bereishis_hebrew_menukad_taamim.tsv`.
- Trusted translations: Koren and Metsudah data validated by `scripts/validate_bereishis_translations.py`.
- Active parsed corpus and word bank: `data/pesukim_100.json`, `data/parsed_pesukim.json`, `data/word_bank.json`, `data/word_occurrences.json`.
- Verified source-to-skill maps: `data/verified_source_skill_maps/`.
- Source validators: `scripts/validate_source_texts.py`, `scripts/validate_verified_source_skill_maps.py`, `scripts/validate_curriculum_extraction.py`.

### Review pipeline and protected previews

- Round pipeline docs and contract: `data/pipeline_rounds/README.md`, `data/pipeline_rounds/round_2_fast_track_pipeline_contract.v1.json`, `scripts/validate_pipeline_rounds.py`.
- Perek 2 Gate 2 layers: `data/gate_2_input_planning/`, `data/gate_2_template_skeleton_planning/`, `data/gate_2_exact_wording_planning/`, `data/gate_2_pre_generation_review/`, `data/gate_2_controlled_draft_generation/`, `data/gate_2_protected_preview_candidates/`, `data/gate_2_protected_preview_packets/`.
- Protected preview candidate validator: `scripts/validate_gate_2_protected_preview_candidates.py`.
- Internal packet validator: `scripts/validate_gate_2_protected_preview_packet.py`.
- Perek 3 currently has protected-preview candidates and applied candidate decisions only; no Perek 3 internal packet was created.

### Diagnostic previews and audit reports

- Diagnostic preview generator: `scripts/generate_diagnostic_preview.py`.
- Diagnostic preview validator: `scripts/validate_diagnostic_preview.py`.
- Question validation audit generator: `scripts/generate_question_validation_audit.py` using `question_validation_audit.py`.
- Generated validation artifacts: `data/validation/`.
- CI test/report workflow: `.github/workflows/python-tests.yml` runs pytest twice and writes validation summaries, but does not directly run most standalone validators.

## 3. Ranked findings

### Finding 1 - Dynamic runtime generation is the broadest quality risk

- Severity: High
- Category: item quality / validation / reporting
- Evidence: `assessment_scope.py:827`, `data/corpus_manifest.json:200`, `engine/flow_builder.py:3444`, `engine/flow_builder.py:3531`, `data/gate_2_protected_preview_packets/bereishis_perek_2_internal_protected_preview_packet.tsv`
- Educational why it matters: A mastery engine should infer skill mastery from items whose skill target, answer key, and distractors have been reviewed. If dynamic generation spans far beyond protected preview coverage, a student can be assessed on items whose educational validity is less proven.
- Technical why it matters: The runtime has strong safety tests, but the protected-preview pipeline and runtime dynamic generator are not the same artifact stream. Reviewed-bank preference helps, but dynamic fallback remains large.
- Recommended action: Build a runtime exposure report that groups every active generator path by reviewed-bank/protected-preview/diagnostic-review status and by canonical skill. Add a fail-closed threshold for newly introduced skill families before they become prominent in runtime.
- Status: Needs engineering review.

### Finding 2 - Translation/context candidates are not yet reliable enough for broad mastery evidence

- Severity: High
- Category: item quality / curriculum alignment
- Evidence: `question_validation_audit.py`; generated audit command showed translation/context 223 valid / 1109 total, 20.1% valid, with 440 `placeholder_translation`, 243 `low_instructional_value`, and 203 `grammatical_particle` rejections.
- Educational why it matters: Translation questions can look authentic while actually rewarding guessing, isolated phrase memory, or placeholder artifacts. That undermines standards-based mastery.
- Technical why it matters: The rejection taxonomy is already exposing actionable failure modes. The system should use these metrics to restrict weak lanes and prioritize review.
- Recommended action: Treat translation/context generation as review-required unless the item has reviewed translation evidence, deterministic answer key, and plausible distractor rationale. Expand diagnostic preview review before runtime expansion.
- Status: Teacher review required.

### Finding 3 - Suffix and compound morphology need a narrower reviewed lane

- Severity: High
- Category: item quality / source integrity
- Evidence: `question_validation_audit.py`; generated audit showed suffix validity 94 / 258, 36.4%, with failures from `compound_morphology`, `no_clear_suffix`, and `lexical_plural_ending`.
- Educational why it matters: Confusing lexical plural endings, construct forms, or compound morphology with suffix decoding teaches the wrong mental model.
- Technical why it matters: Validators catch many unsafe candidates, but low safe-valid rate means future candidate expansion could waste review effort unless pre-filtered.
- Recommended action: Create a suffix-safe source pool with explicit teacher-reviewed examples and block all other suffix-like surface forms from basic suffix questions.
- Status: Needs teacher review.

### Finding 4 - Canonical standards exist, but teacher-facing mastery grouping is incomplete

- Severity: High
- Category: curriculum alignment / reporting
- Evidence: `data/standards/canonical_skill_contract.json:8`, `data/standards/canonical_skill_contract.json:36`, `data/standards/canonical_skill_contract.json:1130`, `skill_catalog.py:60`, `docs/runtime_skill_canonical_alignment.md`.
- Educational why it matters: Zekelman-style standards are benchmarks for mastery, not a syllabus. Teachers need analysis by standard, not just item correctness.
- Technical why it matters: Runtime skills map to canonical skills, but many Zekelman mappings are still `review_only`, and there is no single report that shows mastery evidence by standard plus review status.
- Recommended action: Generate a standards evidence matrix from runtime skill attempts, canonical contract, reviewed-bank status, and preview gate status.
- Status: Safe now for reporting; teacher review required for final standard grouping.

### Finding 5 - Diagnostic previews are promising but under-scoped

- Severity: Medium
- Category: preview workflow
- Evidence: `scripts/generate_diagnostic_preview.py`, `scripts/validate_diagnostic_preview.py`; command output for `data/diagnostic_preview/configs/bereishis_1_1_to_2_3_dikduk_translation_preview.json` produced 77 questions, 33 reviewable items, 27 likely approve, 6 caution.
- Educational why it matters: This is one of the best teacher-facing artifacts because it exposes caution flags, translation alignment, and reviewable items.
- Technical why it matters: The validator is strong but config-driven; coverage does not automatically extend to the full active runtime scope.
- Recommended action: Add an active-scope diagnostic-preview index that reports which pesukim/skills have diagnostic preview evidence and which do not.
- Status: Safe now.

### Finding 6 - Perek 3 review packet can become stale after decision application

- Severity: Medium
- Category: preview workflow / maintainability
- Evidence: `data/gate_2_protected_preview_candidates/reports/bereishis_perek_3_protected_preview_candidate_yossi_review_applied.md:14`, `data/gate_2_protected_preview_candidates/reports/bereishis_perek_3_protected_preview_candidate_review_packet.md:192`.
- Educational why it matters: A teacher reading both files could be unsure whether rows are still pending or have decisions applied.
- Technical why it matters: The validator checks the applied report, but the review packet remains a historical artifact without a status banner.
- Recommended action: Add a small post-decision banner or companion status field to candidate review packets after decisions are applied, without rewriting history.
- Status: Safe now.

### Finding 7 - Validators are excellent but manual orchestration is fragile

- Severity: Medium
- Category: validation / maintainability
- Evidence: `.github/workflows/python-tests.yml:25`, `.github/workflows/python-tests.yml:28`, `scripts/validate_*.py`.
- Educational why it matters: Safety gates only protect learning quality if they are reliably run.
- Technical why it matters: CI runs pytest and generated reports, but not the full standalone validator suite directly. Some validators are covered by tests, others are manually invoked in task prompts.
- Recommended action: Create `scripts/run_curriculum_quality_checks.py` as a non-runtime orchestrator that runs source, standards, pipeline, preview, and protected packet validators with a clear summary.
- Status: Safe now.

### Finding 8 - Source text integrity is strong, but item-level lineage should be more visible

- Severity: Medium
- Category: source integrity / reporting
- Evidence: `scripts/validate_source_texts.py` passed 1,533 Bereishis source rows with no missing/duplicate/malformed rows; `scripts/validate_bereishis_translations.py` passed 1,533 Koren and 1,533 Metsudah rows.
- Educational why it matters: Teachers need confidence that a question’s Hebrew and translation evidence are anchored in trusted text, not generated text.
- Technical why it matters: Source validators are strong, but many item reports do not show full lineage through source row, source-to-skill row, enrichment row, and review decision.
- Recommended action: Add an optional provenance section to preview packets and runtime audit rows: source row ID, source-to-skill ID, enrichment/review ID, translation authority.
- Status: Safe now for audit/reporting.

### Finding 9 - Some runtime tests prove structure, not enough instructional quality

- Severity: Medium
- Category: item quality / validation
- Evidence: `engine/flow_builder.py:3564`, `engine/flow_builder.py:5823`, `tests/test_question_types_contract.py`, `tests/test_runtime_question_flow.py`.
- Educational why it matters: Four unique choices and a deterministic key are necessary but not sufficient; distractors should reveal misconceptions, and explanations should teach the intended skill.
- Technical why it matters: Diagnostic preview artifacts already have richer review fields. Runtime dynamic generation could benefit from similar explanation/distractor rubrics.
- Recommended action: Add an audit-only explanation/distractor rubric for each active question family, then decide which families need teacher review before expansion.
- Status: Needs teacher review.

### Finding 10 - Documentation command drift can cause incomplete validation

- Severity: Low/Medium
- Category: maintainability
- Evidence: `README.md` test instructions reference older unittest-style commands while `pytest.ini` and `.github/workflows/python-tests.yml` use pytest.
- Educational why it matters: Contributors may think they validated a change when they did not run the relevant test/validator path.
- Technical why it matters: Command drift is low risk per item but high friction over time.
- Recommended action: Update developer docs to point to pytest and the future curriculum-quality check orchestrator.
- Status: Safe now.

## 4. Skill coverage matrix

| Skill or standard area | Source of truth | Current implementation | Question types / artifacts | Validators / tests | Preview coverage | Risk level | Recommended next action |
|---|---|---|---|---|---|---|---|
| Vocabulary / word meaning | `skill_catalog.py`, `data/standards/canonical_skill_contract.json`, word bank, translations | Runtime and diagnostic preview support basic word translation; Perek 2/Perek 3 candidates mostly noun recognition | translation, vocabulary meaning, protected preview noun rows | `validate_question_eligibility_audit.py`, runtime tests, diagnostic preview validator | Diagnostic preview has translation lanes; protected preview narrow | Medium | Expand only reviewed vocabulary pools with authority notes and deterministic answer keys |
| Basic noun / part of speech | Canonical contract `WORD.PART_OF_SPEECH_BASIC`; reviewed Gate 2 layers | Strongest current protected-preview path | `basic_noun_recognition` | Gate 2 validators and tests | Perek 2 internal packet 10; Perek 3 candidates 10 | Low/Medium | Keep expanding cautiously; add duplicate-token balance checks |
| Shoresh identification | Canonical `ROOT.IDENTIFY`, gold annotations | Runtime supports; Perek 2 clean shoresh groups stayed follow-up | shoresh questions | gold shoresh tests, question validation audit | Limited protected preview | Medium | Teacher-confirm high-frequency roots before new reviewed packets |
| Prefix / article / preposition | Canonical prefix rows; word-bank prefix metadata | Runtime supports prefix lanes; Perek 3 decisions flagged article/prefix risks | prefix questions; possible revision-only candidates | prefix tests, question validation audit | Diagnostic preview has prefix items | Medium | Separate base noun recognition from prefix recognition in templates and reports |
| Suffix / possession / construct-like forms | Canonical suffix rows mostly review-only | Runtime has suffix questions but audit validity is low | suffix questions | suffix tests, question validation audit | Limited | High | Create a teacher-reviewed safe suffix pool; block lexical plural/construct confusion |
| Verb tense/person/gender/number | canonical verb rows and dikduk foundations | Runtime supports tense; advanced forms require caution | tense / verb form analysis | tense tests, diagnostic preview, dikduk validators | Diagnostic preview has verb form analysis | Medium/High | Keep advanced verb clues diagnostic/review-only until teacher-scored examples exist |
| Vav hahipuch / narrative forms | dikduk foundations / canonical review-only lanes | Mentioned in materials; not a broad reviewed runtime lane | limited diagnostics | dikduk validators | limited | High | Do not expand until classifier, detector, distractors, display policy, and review rubric exist |
| Direct-object marker / function words | canonical review-only rows | Some eligible/approved input candidates exist, but high caution | direct_object_marker_recognition | question eligibility validator | not broad | Medium/High | Keep review-only and require wording review because particles can be low instructional value |
| Phrase translation | translations and source-to-skill maps | Diagnostic preview and extraction layers exist | phrase meaning / translation | diagnostic preview validator, translation validators | present in diagnostics | High | Avoid runtime expansion until phrase-level answer keys and distractors are teacher-reviewed |
| Pasuk comprehension / context | translation reviews and diagnostic preview | limited reviewable preview | pasuk comprehension | diagnostic preview validator | sparse | High | Keep teacher-review only; avoid inference-heavy templates |
| Rashi / commentary / higher-order comprehension | not active in discovered runtime gates | intentionally absent | none active | none | none | High | Do not add until source authority, standards, review workflow, and item templates exist |

## 5. Question type quality matrix

| Question type / family | Claimed skill | Actual assessed skill | Level appropriateness | Distractor quality | Answer determinism | Explanation quality | Hebrew/source risk | Recommended status |
|---|---|---|---|---|---|---|---|
| Basic noun recognition | part of speech / noun recognition | Usually identifies a visible noun token | Good for early mastery when token is simple | Simple category labels; adequate for first pass | High for reviewed rows | Controlled drafts explain teacher-review status | Low when base noun is unambiguous | keep and expand through review gates |
| Vocabulary meaning / basic translation | word meaning | Often isolated vocabulary; can drift into context translation | Good only when vocabulary is taught and unambiguous | Variable; needs teacher review | Medium; low if placeholder/context-dependent | Better in preview packets than dynamic runtime | Medium/High | teacher review required |
| Shoresh identification | root recognition | Root recall/recognition | Appropriate for reviewed roots | Can be plausible if generated from known root sets | Medium/High with gold annotations | Needs explicit root evidence | Medium | improve with reviewed root pools |
| Prefix recognition | prefix/article/preposition recognition | Surface prefix recognition; sometimes base word confusion | Good if the question target is explicit | Strong if distractors are prefixes only | Medium/High for simple forms | Needs caution for article/base noun distinction | Medium | keep with stricter target wording |
| Suffix recognition | suffix/person/possession decoding | Often ambiguous with construct/plural/lexical endings | Risky for early layers | Weak unless suffix class is teacher-reviewed | Low/Medium per audit | Needs strong explanation | High | restrict to reviewed bank until safe pool exists |
| Verb tense / verb form | tense/person clues | Verb morphology recognition | Appropriate only after explicit instruction | Can be plausible but needs grammar control | Medium | Needs teacher wording | Medium/High | teacher review required |
| Direct-object marker/function word | particle recognition | Recognizes grammar particle rather than meaning | Useful but easy to overuse | Distractors can be weak | Medium | Needs explanation of function | Medium | review-only, expand cautiously |
| Phrase meaning / translation | phrase comprehension | Often translation memory or context matching | Good for reviewed phrases only | Hard to make plausible without ambiguity | Low/Medium unless reviewed | Diagnostic preview is helpful | High | restrict to reviewed packets |
| Diagnostic error diagnosis | misconception recognition | Identifies likely error pattern | Potentially excellent for teachers | Strong if tied to misconceptions | Medium | Can be pedagogically rich | Medium | improve and expand after review |
| Word order / syntax grouping | syntax/phrase structure | Can become broad syntax | Advanced | Variable | Medium/Low | Needs careful explanation | Medium/High | teacher review required |

## 6. Validator coverage matrix

| Validator / test area | What it checks | What it misses | Run mode found | Failure mode | Recommended strengthening |
|---|---|---|---|---|---|
| `scripts/validate_source_texts.py` | canonical source rows, refs, missing/malformed/duplicate source text | item-level source lineage | manual / test-linked | hard fail | Add source-row hash to item review packets |
| `scripts/validate_bereishis_translations.py` | Koren/Metsudah coverage against canonical refs | translation educational appropriateness | manual | hard fail | Include translation authority in generated review packets |
| `scripts/validate_verified_source_skill_maps.py` | verified source-to-skill rows and closed safety gates | whether skill is pedagogically useful | manual | hard fail | Add source-to-skill usage coverage matrix |
| `scripts/validate_canonical_skill_contract.py` | statuses, runtime mapping consistency, non-runtime gates | teacher-facing mastery grouping | manual/test-linked | hard fail | Generate standards evidence report |
| `scripts/validate_source_skill_enrichment.py` | Perek 2 enrichment artifacts, crosswalks, decisions, closed gates | future Perek expansion unless added | manual/test-linked | hard fail | Parameterize per Perek to reduce copy checks |
| `scripts/validate_question_eligibility_audit.py` | eligibility recommendations, counts, gate closure | actual runtime exposure | manual | hard fail | Join with runtime generation audit |
| `scripts/validate_gate_2_*` | Gate 2 layer counts, statuses, closed gates, packet/report presence | content quality beyond encoded statuses | manual/test-linked | hard fail | Add stale packet/status consistency checks |
| `scripts/validate_diagnostic_preview.py` | config outputs, reviewable packets, closed runtime/production statuses | full active-scope coverage | manual config required | hard fail | Add discover-all-configs mode |
| `scripts/validate_curriculum_extraction.py` | extraction artifacts and git diff guard | broad validator orchestration | manual | hard fail | Include generated churn guidance in summary |
| `question_validation_audit.py` / `scripts/generate_question_validation_audit.py` | candidate validity/rejection reasons across active scope | does not fail build by itself | manual/CI artifact potential | report-only | Promote selected thresholds to warning/fail gates after baseline |
| Pytest suite | runtime behavior, contract checks, validators under tests | not all standalone validators directly | CI via `.github/workflows/python-tests.yml` | hard fail | Add a curriculum validator aggregate test |
| `scripts/release_check.py` | pilot/release-check workflow | needs pilot log input for finalize | manual | hard fail/usage | Document when release checks should run |

## 7. Protected preview findings

- Trustworthiness: Strong. Gate 2 candidate and packet validators enforce row counts, required columns, links to prior approved artifacts, and closed downstream gates. Perek 2 internal packet rows have `reviewed_bank_allowed=false`, `runtime_allowed=false`, and `student_facing_allowed=false`.
- Reproducibility: Good for validation, mixed for creation. TSVs and Markdown reports are deterministic once written, but manual review packets can become historical snapshots unless explicitly labeled after decisions are applied.
- Teacher readability: Strong in protected-preview packets and diagnostic preview review packets. The best artifacts show prompt, answer choices, expected answer, explanation, source evidence, caution note, and decision fields.
- Leak prevention: Strong for reviewed-bank/runtime/student-facing gates. Perek 3 currently has candidate decisions but no Perek 3 final/internal packet, and validators explicitly check that no final Perek 3 packet exists.
- Main improvement: Add a small status index for each candidate layer showing current stage: pre-decision packet, decisions applied, internal packet created, post-preview review not started. This would prevent stale packet confusion without opening any gate.

## 8. Recommended next work plan

### Safe now

1. Add a non-runtime `scripts/run_curriculum_quality_checks.py` that runs the core source, standards, pipeline, diagnostic, protected preview, and question-audit checks and writes one summary.
2. Add a status banner/update to Perek 3 candidate review packet or README indicating decisions have been applied and the original packet is a pre-decision snapshot.
3. Update `README.md` test commands to align with `pytest.ini` and CI.
4. Add an audit-only source lineage matrix for protected preview/internal packet items.
5. Add a diagnostic preview coverage index by active scope, pasuk, lane, skill, and review status.

### Teacher review required

1. Review translation/context rejection families and decide which translation question shapes should remain teacher-only.
2. Approve a suffix-safe pool with examples that avoid construct, plural-ending, and compound morphology confusion.
3. Decide Zekelman reporting groups that should be visible to teachers first.
4. Review diagnostic preview caution rows before converting any to protected-preview candidates.
5. Decide whether repeated noun-recognition items should be balanced by pasuk, token, or target standard.

### Engineering review required

1. Decide whether dynamic runtime generation should have per-skill exposure caps based on reviewed evidence coverage.
2. Integrate canonical skill contract, runtime skill catalog, and mastery reporting into a standards evidence dashboard.
3. Parameterize Gate 2 validators by Perek so new Perakim do not require duplicated hardcoded checks.
4. Add CI or scheduled job coverage for standalone validators, not only pytest.
5. Add provenance fields to runtime audit traces without changing student-facing behavior.

### Do not touch yet

1. Do not activate Perek 3 runtime scope.
2. Do not create Perek 3 reviewed-bank entries.
3. Do not create a Perek 3 internal protected-preview packet until a later explicit packet-creation task.
4. Do not broaden vav hahipuch / advanced verb-form assessment without full classifier, detector, validator, distractor rules, display policy, audit visibility, and tests.
5. Do not add Rashi/commentary or higher-order inference items until source authority and review workflow are designed.

## 9. Completion report

### Branch name

`audit/overnight-curriculum-quality-review`

### Files created

- `AUDIT_OVERNIGHT_CURRICULUM_QUALITY_REVIEW.md`

### Files modified

- None intentionally beyond this audit report.
- `scripts/generate_question_validation_audit.py` temporarily regenerated `data/validation/question_validation_audit.json` and `data/validation/question_validation_audit.md`; those generated files were restored to avoid unrelated report churn.

### Commands run

- `git branch --show-current` - pass; started on `feature/canonical-skill-standards-contract`.
- `git status --short` - pass; starting worktree clean.
- `git checkout -b audit/overnight-curriculum-quality-review` - pass.
- `python scripts/generate_question_validation_audit.py` - pass; produced useful audit metrics, then generated churn was restored.
- `python scripts/generate_diagnostic_preview.py --help` - pass.
- `python scripts/release_check.py --help` - pass; emitted non-blocking Streamlit cache warnings.
- `python scripts/validate_curriculum_extraction.py` - pass.
- `python scripts/validate_standards_data.py` - pass.
- `python scripts/validate_canonical_skill_contract.py` - pass.
- `python scripts/generate_diagnostic_preview.py --config data/diagnostic_preview/configs/bereishis_1_1_to_2_3_dikduk_translation_preview.json` - pass.
- `python scripts/validate_diagnostic_preview.py` - failed as expected during command discovery because `--config` is required.
- `python scripts/validate_diagnostic_preview.py --config data/diagnostic_preview/configs/bereishis_1_1_to_2_3_dikduk_translation_preview.json` - initially failed because generated question-validation audit files dirtied the worktree; passed after restoring generated churn.
- `python scripts/validate_verified_source_skill_maps.py` - pass.
- `python scripts/validate_source_texts.py` - pass.
- `python scripts/validate_gate_2_protected_preview_candidates.py` - pass.
- `python scripts/validate_gate_2_protected_preview_packet.py` - pass.
- `python scripts/validate_source_skill_enrichment.py` - pass.
- `python scripts/validate_pipeline_rounds.py` - pass.
- `python scripts/validate_question_eligibility_audit.py` - pass.
- `python scripts/validate_protected_preview_packet.py` - pass.
- `python scripts/validate_bereishis_translations.py` - pass.
- `python scripts/validate_dikduk_foundations.py` - pass.
- `python scripts/validate_dikduk_rules.py` - pass.
- `python scripts/validate_gate_2_input_planning.py` - pass.
- `python scripts/validate_gate_2_controlled_draft_generation.py` - pass.
- `python scripts/validate_protected_preview_candidates.py` - pass.

### Commands failed

- `python scripts/validate_diagnostic_preview.py` without `--config`: expected argparse usage failure, non-blocking discovery failure.
- First configured diagnostic preview validation failed only because `generate_question_validation_audit.py` had regenerated tracked validation artifacts. After restoring generated churn, the same configured validator passed.

### Tests/validators passed

All targeted validators listed above passed after generated churn was restored. Full pytest was run after this report was created; see final assistant response for the exact result.

### Tests/validators failed

No remaining targeted validator failures at report-writing time.

### Unresolved questions

1. Which Zekelman standard groupings should teachers see first in mastery reports?
2. Which translation/context question shapes should be allowed beyond diagnostic preview?
3. What is the acceptable runtime exposure policy for dynamic generated items before a reviewed-bank or protected-preview equivalent exists?
4. Should Perek 3 candidate review packet be updated as a historical pre-decision snapshot now that decisions are applied, or should the applied report remain the sole current-status source?

### Recommended next Codex prompt

Create a non-runtime curriculum quality check orchestrator and status index:

`Create scripts/run_curriculum_quality_checks.py and a generated data/validation/curriculum_quality_check_summary.md that run/source-link the existing source, standards, Gate 2, protected-preview, diagnostic-preview, and question-validation audit checks without changing runtime behavior. Include a stale-packet/status consistency check for Perek 3 candidate decisions, but do not modify runtime, reviewed bank, or protected-preview packet approvals.`
