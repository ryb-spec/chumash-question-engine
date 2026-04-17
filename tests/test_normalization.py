import unittest

from torah_parser.normalize import normalize_form, undotted_form


class NormalizationTests(unittest.TestCase):
    def test_normalize_form_removes_nekudos_and_preserves_letters(self):
        dotted = "\u05d1\u05bc\u05b0\u05e8\u05b5\u05d0\u05e9\u05c1\u05b4\u05d9\u05ea"
        undotted = "\u05d1\u05e8\u05d0\u05e9\u05d9\u05ea"

        self.assertEqual(undotted_form(dotted), undotted)
        self.assertEqual(normalize_form(dotted), undotted)
        self.assertEqual(normalize_form(undotted), undotted)

    def test_normalize_form_cleans_maqaf_and_punctuation(self):
        text = "\u05d5\u05b7\u05d9\u05bc\u05b9\u05d0\u05de\u05b6\u05e8,\u05d0\u05b1\u05dc\u05b9\u05e7\u05b4\u05d9\u05dd\u05be\u05d9\u05b0\u05d4\u05b4\u05d9 \u05d0\u05d5\u05b9\u05e8\u05c3"

        self.assertEqual(
            normalize_form(text),
            "\u05d5\u05d9\u05d0\u05de\u05e8 \u05d0\u05dc\u05e7\u05d9\u05dd \u05d9\u05d4\u05d9 \u05d0\u05d5\u05e8",
        )


if __name__ == "__main__":
    unittest.main()
