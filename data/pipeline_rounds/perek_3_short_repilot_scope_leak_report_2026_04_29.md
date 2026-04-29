# Perek 3 Short Re-Pilot Scope Leak Report - 2026-04-29

## Purpose

This report records scope-control findings from the short Perek 3 re-pilot raw logs. It does not change runtime behavior, activate Perek 4, promote content, or apply any new review decision.

## Expected short re-pilot scope

The short re-pilot was intended to test only:

- revised tense/form wording
- revised prefix prompt wording
- `דֶּרֶךְ` translation distractor repair
- `אֲרוּרָה` translation distractor repair

The short re-pilot was intended to exclude:

- `אָשִׁית` / `שית` beginner shoresh identification
- unverified `phrase_translation`
- Perek 4 content
- runtime expansion

## Scope-control outcome

Manual-only scope control did not produce a fully clean short re-pilot.

| Leak ID | Type | Evidence | Why it matters | Required follow-up |
| --- | --- | --- | --- | --- |
| p3_short_repilot_leak_001 | Excluded question family served | `phrase_translation` for `בְּעֶצֶב תֵּלְדִי בָנִים` | Unverified phrase_translation was explicitly excluded from the short re-pilot scope. | Do not count as clean closure evidence; add pilot-only filtering or manual skip instruction before the next clean run. |
| p3_short_repilot_leak_002 | Excluded question family served | `phrase_translation` for `וְאֵיבָה אָשִׁית` | Unverified phrase_translation was excluded, and this phrase includes `אָשִׁית`, which remains a source/teacher follow-up context. | Do not count as clean closure evidence; keep `אָשִׁית` / `שית` beginner shoresh unresolved and keep phrase_translation audit open. |
| p3_short_repilot_wording_001 | Old wording served | `What is the prefix in בְּאִשְׁתּוֹ?` | The short re-pilot was intended to test revised prefix wording. This served event suggests an active reviewed-bank row still carries old wording. | Locate and repair the stored prompt or add a targeted reviewed-bank wording check in a later task. |

## Non-leak findings

- Perek 4 content was not observed in the reviewed raw evidence.
- The blocked `אָשִׁית` / `שית` beginner shoresh question was not observed as a shoresh-identification item.
- A non-blocked shoresh question for `וַיְגָרֶשׁ` was answered correctly.

## Gate implication

The short re-pilot results are useful but not clean enough to close Perek 3 or to justify moving on as if all unresolved Perek 3 issues are settled. Perek 4 remains inactive.

## Safety boundary confirmation

- No runtime behavior change.
- No active scope expansion.
- No Perek 4 activation.
- No reviewed-bank/runtime promotion.
- No source-truth change.
- No fake data.
- Raw logs were not edited manually by this task.
