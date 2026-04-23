# Hand Audit

Generated: 2026-04-22T16:18:32.666984+00:00
Scope: local_parsed_bereishis_1_1_to_3_8

## Evidence Used
- Fresh current-build hand audit packet: 25 questions generated at 2026-04-22T16:18:34.540149+00:00.
- Historical real pilot log: `data\pilot\runs\pilot_session_events_20260422T113750Z_release-check.jsonl`.
- Latest included real session started at: 2026-04-22T11:38:56.930709+00:00.

## Overall Read
Mixed. Reviewed translation and reviewed shoresh items feel mostly strong, but generated tense and part-of-speech items still leak obviously weak or wrong material.

## Strong Served Items
- Bereishis 1:1 `phrase_translation` on `בָּרָא אֱלֹקִים` -> `God created` (reviewed).
- Bereishis 1:3 `phrase_translation` on `וַיֹּאמֶר אֱלֹקִים` -> `and God said` (reviewed).
- Bereishis 1:4 `shoresh` on `וַיַּבְדֵּל` -> `בדל` (reviewed).
- Bereishis 1:11 `shoresh` on `תַּדְשֵׁא` -> `דשא` (reviewed).
- Bereishis 1:12 `shoresh` on `וַתּוֹצֵא` -> `יצא` (reviewed).

## Thin or Wrong Items
- Bereishis 1:1 `verb_tense` on `בְּרֵאשִׁית`: non-verb served as a single-answer tense item.
- Bereishis 1:1 `part_of_speech` on `בְּרֵאשִׁית`: served as an action word; this looks wrong rather than merely thin.
- Bereishis 1:2 `identify_tense` on `מְרַחֶפֶת`: served as a past-only tense item; this looks structurally weak.
- Bereishis 1:3 `prefix_level_2_identify_prefix_meaning` on `וַיְהִי`: flattens a vav-hahipuch form into a simple prefix-meaning item.

## Repeated-Target Feel
- Fresh hand audit duplicate-feel warnings: 0.
- Historical pilot repeated-target warnings: 0.
- The selector looks fairly good at avoiding repeated feel in the sampled packet, but the reviewed bank still has some repeated targets on paper, so this cleanliness looks selector-driven rather than bank-intrinsic.

## Log Cleanliness
- Historical pilot log shows 0 trusted-scope violations and 0 served-without-validation events.
- That is structurally clean on scope and validation gates, but it is not enough by itself to call the runtime broadly clean because the fresh hand audit still surfaces weak generated grammar items.

## Ambiguity Handling
- Earlier live unclear flags were a weak standalone translation (`????`) and a low-value bare-form shoresh item (`?????`).
- Those exact weak classes did not reappear in the fresh hand audit packet, which is encouraging.
- Even so, the generated grammar lanes still feel only partially fail-closed: some items that look weak or wrong are still being served instead of blocked or reshaped.

## Recommendation
- Ready to stay in cleanup mode: yes.
- Ready to promote the staged slice: no.
- Ready to expand to the next controlled slice: no.
- Stop and gather more evidence: yes, but specifically by running a new isolated pilot on the current build after the next grammar-lane cleanup.
