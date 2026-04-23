from pathlib import PurePath

# Test cases that use the custom scripts
class TestCorpusPromotion:
    # ... existing test methods
    def test_build_reviewed_question_bank(self):
        # Existing logic
        assert PurePath(script_path).name == "build_reviewed_question_bank.py"

    def test_audit_role_layer(self):
        # Existing logic
        assert PurePath(script_path).name == "audit_role_layer.py"