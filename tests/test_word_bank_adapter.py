import unittest

from torah_parser.word_bank_adapter import (
    adapt_word_bank_data,
    build_word_bank_lookup,
    build_word_bank_metadata_index,
    normalize_hebrew_key,
    resolve_surface_for_normalized,
    resolve_word_bank_lookup,
)


class WordBankAdapterTests(unittest.TestCase):
    def test_old_schema_entry_stays_compatible_and_uses_structured_morphemes(self):
        data = {
            "words": [
                {
                    "Word": "בָּאָרֶץ",
                    "Shoresh": "ארץ",
                    "part_of_speech": "proper_noun",
                    "Prefix": "ב",
                    "Prefix Meaning": "in / with",
                    "Suffix": "",
                    "Suffix Meaning": "",
                    "translation": "land",
                }
            ]
        }

        entries = adapt_word_bank_data(data)
        entry = entries[0]

        self.assertEqual(entry["word"], "בָּאָרֶץ")
        self.assertEqual(entry["Word"], "בָּאָרֶץ")
        self.assertEqual(entry["shoresh"], "ארץ")
        self.assertEqual(entry["Shoresh"], "ארץ")
        self.assertEqual(entry["type"], "noun")
        self.assertEqual(entry["translation"], "land")
        self.assertEqual(entry["prefixes"], [{"form": "ב", "translation": "in / with"}])
        self.assertEqual(entry["suffixes"], [])
        self.assertEqual(entry["prefix"], "ב")
        self.assertEqual(entry["prefix_meaning"], "in / with")

    def test_exact_surface_lookup_is_preserved_in_metadata_index(self):
        entries = adapt_word_bank_data(
            {
                "words": {
                    "בְּמַיִם": [
                        {
                            "surface": "בְּמַיִם",
                            "normalized": "במים",
                            "part_of_speech": "noun",
                            "translation_literal": "water",
                            "translation_context": "in the water",
                            "prefixes": [{"form": "ב", "translation": "in / with"}],
                            "suffixes": [],
                        }
                    ]
                }
            }
        )

        metadata = build_word_bank_metadata_index(entries)
        self.assertIn("בְּמַיִם", metadata)
        self.assertEqual(metadata["בְּמַיִם"]["menukad"], "בְּמַיִם")
        self.assertEqual(metadata["בְּמַיִם"]["translation"], "in the water")

    def test_normalized_lookup_resolves_back_to_surface_entry(self):
        entries = adapt_word_bank_data(
            {
                "words": {
                    "בְּמַיִם": [
                        {
                            "surface": "בְּמַיִם",
                            "normalized": "במים",
                            "part_of_speech": "noun",
                            "translation_literal": "water",
                            "translation_context": "in the water",
                            "prefixes": [{"form": "ב", "translation": "in / with"}],
                            "suffixes": [],
                        }
                    ]
                }
            }
        )

        lookup = build_word_bank_lookup(entries)
        normalized = normalize_hebrew_key("בְּמַיִם")

        self.assertIn(normalized, lookup)
        self.assertEqual(resolve_surface_for_normalized(lookup, normalized), "בְּמַיִם")
        resolved = resolve_word_bank_lookup("במים", lookup[normalized])
        self.assertEqual(resolved["word"], "בְּמַיִם")
        self.assertEqual(resolved["translation"], "in the water")

    def test_missing_field_fallbacks_stay_honest_and_usable(self):
        entries = adapt_word_bank_data(
            {
                "words": {
                    "אוֹר": [
                        {
                            "surface": "אוֹר",
                            "part_of_speech": "noun",
                        }
                    ]
                }
            }
        )

        entry = entries[0]
        self.assertEqual(entry["word"], "אוֹר")
        self.assertEqual(entry["menukad"], "אוֹר")
        self.assertEqual(entry["translation"], "אוֹר")
        self.assertIsNone(entry["translation_literal"])
        self.assertIsNone(entry["translation_context"])
        self.assertEqual(entry["prefixes"], [])
        self.assertEqual(entry["suffixes"], [])
        self.assertEqual(entry["prefix"], "")
        self.assertEqual(entry["suffix"], "")
    def test_multi_analysis_surface_keeps_first_analysis_as_default_entry(self):
        entries = adapt_word_bank_data(
            {
                "words": {
                    "וַיְהִי": [
                        {
                            "surface": "וַיְהִי",
                            "normalized": "ויהי",
                            "part_of_speech": "verb",
                            "shoresh": "היה",
                            "tense": "vav_consecutive_past",
                            "translation_literal": "and it was",
                            "translation_context": "and there was",
                        },
                        {
                            "surface": "וַיְהִי",
                            "normalized": "ויהי",
                            "translation": "וַיְהִי",
                        },
                    ]
                }
            }
        )

        lookup = build_word_bank_lookup(entries)
        metadata = build_word_bank_metadata_index(entries)

        self.assertEqual(lookup["וַיְהִי"]["part_of_speech"], "verb")
        self.assertEqual(lookup["וַיְהִי"]["shoresh"], "היה")
        self.assertEqual(lookup["וַיְהִי"]["tense"], "vav_consecutive_past")
        self.assertEqual(metadata["וַיְהִי"]["translation"], "and there was")
        self.assertEqual(len(lookup["וַיְהִי"]["analyses"]), 2)


if __name__ == "__main__":
    unittest.main()
