import json
import unittest
from pathlib import Path
import uuid

import progress_store


class ProgressMigrationTests(unittest.TestCase):
    def temp_path(self, prefix):
        return Path(f"{prefix}_{uuid.uuid4().hex}.json")

    def test_migrates_legacy_progress_and_skill_progress(self):
        progress_path = self.temp_path("progress_migration_test_progress")
        legacy_path = self.temp_path("progress_migration_test_skill")
        try:
            legacy_progress = {
                "words": {"בְּרֵאשִׁית": 30},
                "standards": {"WM": 20},
                "micro_standards": {"WM1": 10},
                "xp": {"WM": 45},
                "current_skill": "translation",
                "prefix_level": 2,
                "word_bank": [{"word": "בְּרֵאשִׁית"}],
            }
            legacy_skill_progress = {
                "translation": {
                    "score": 15,
                    "correct_count": 3,
                    "incorrect_count": 0,
                    "current_streak": 3,
                    "best_streak": 3,
                    "challenge_streak": 0,
                    "last_12_results": [True, True, True],
                    "error_counts": {},
                    "mastered": False,
                    "last_point_change": "+5",
                },
                "word_exposure": {
                    "בְּרֵאשִׁית": {
                        "seen": 5,
                        "correct": 4,
                        "recent_streak": 2,
                        "mastered": False,
                    }
                },
            }

            progress_path.write_text(
                json.dumps(legacy_progress, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            legacy_path.write_text(
                json.dumps(legacy_skill_progress, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            state = progress_store.load_progress_state(progress_path, legacy_path)

            self.assertEqual(state["schema_version"], progress_store.SCHEMA_VERSION)
            self.assertEqual(state["words"]["בְּרֵאשִׁית"], 30)
            self.assertEqual(state["xp"]["WM"], 45)
            self.assertEqual(state["current_skill"], "translation")
            self.assertEqual(state["prefix_level"], 2)
            self.assertIn("translation", state["skills"])
            self.assertIn("בְּרֵאשִׁית", state["word_exposure"])
            self.assertEqual(state["word_bank"], [{"word": "בְּרֵאשִׁית"}])

            persisted = json.loads(progress_path.read_text(encoding="utf-8"))
            self.assertEqual(persisted["schema_version"], progress_store.SCHEMA_VERSION)
            self.assertIn("skills", persisted)
            self.assertIn("word_exposure", persisted)
        finally:
            progress_path.unlink(missing_ok=True)
            legacy_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
