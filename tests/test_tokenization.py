import unittest

from torah_parser.tokenize import tokenize_pasuk


class TokenizationTests(unittest.TestCase):
    def test_tokenize_pasuk_splits_maqaf_and_punctuation(self):
        text = "\u05d5\u05b7\u05d9\u05bc\u05b9\u05d0\u05de\u05b6\u05e8, \u05d0\u05b1\u05dc\u05b9\u05e7\u05b4\u05d9\u05dd\u05be\u05d9\u05b0\u05d4\u05b4\u05d9 \u05d0\u05d5\u05b9\u05e8\u05c3"

        self.assertEqual(
            tokenize_pasuk(text),
            [
                "\u05d5\u05b7\u05d9\u05bc\u05b9\u05d0\u05de\u05b6\u05e8",
                "\u05d0\u05b1\u05dc\u05b9\u05e7\u05b4\u05d9\u05dd",
                "\u05d9\u05b0\u05d4\u05b4\u05d9",
                "\u05d0\u05d5\u05b9\u05e8",
            ],
        )

    def test_tokenize_pasuk_strips_boundary_quotes(self):
        text = "\"\u05d1\u05bc\u05b0\u05e8\u05b5\u05d0\u05e9\u05c1\u05b4\u05d9\u05ea\" \u05d1\u05bc\u05b8\u05e8\u05b8\u05d0"

        self.assertEqual(
            tokenize_pasuk(text),
            [
                "\u05d1\u05bc\u05b0\u05e8\u05b5\u05d0\u05e9\u05c1\u05b4\u05d9\u05ea",
                "\u05d1\u05bc\u05b8\u05e8\u05b8\u05d0",
            ],
        )


if __name__ == "__main__":
    unittest.main()
