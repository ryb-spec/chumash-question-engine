from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "docs" / "sources" / "trusted_teacher_source_policy.md"
TEMPLATE_PATH = ROOT / "docs" / "sources" / "trusted_teacher_source_extraction_review_packet_template.md"
CONFIRMATION_ITEMS_PATH = ROOT / "data" / "source_review_confirmation_items.json"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_trusted_source_policy_requires_extraction_accuracy_not_reapproval():
    policy = read_text(POLICY_PATH)

    assert "one Yossi extraction-accuracy pass" in policy
    assert "not a full educational approval cycle" in policy
    assert "should not ask Yossi to re-approve the educational value" in policy
    assert "source matching, Hebrew fidelity, classification, and mapping" in policy


def test_trusted_source_packet_template_uses_light_review_language():
    template = read_text(TEMPLATE_PATH)

    assert "trusted_source_extraction_accuracy_pass" in template
    assert "Was the source copied or OCRed accurately?" in template
    assert "Is the Hebrew faithful to the source?" in template
    assert "Is the standards or skill mapping reasonable?" in template
    assert "Do you approve this educational source?" in template
    assert "Those are the wrong questions for trusted source extraction packets." in template


def test_packet_template_preserves_separate_review_paths():
    template = read_text(TEMPLATE_PATH)

    required_paths = [
        "Trusted teacher-source extraction",
        "AI-generated questions",
        "Protected preview packet",
        "Reviewed-bank promotion",
        "Runtime activation",
        "Unclear source",
    ]
    for required_path in required_paths:
        assert required_path in template

    assert "AI-generated and system-generated questions still require full review" in template
    assert "does not become runtime-active unless a separate runtime activation gate" in template


def test_targeted_confirmation_items_remain_specific_and_non_runtime():
    confirmation_items = read_text(CONFIRMATION_ITEMS_PATH)

    assert "trusted_teacher_source_extraction_review_packet_template.md" in confirmation_items
    assert "exact_question_for_yossi" in confirmation_items
    assert "needs_specific_confirmation" in confirmation_items
    assert "not_runtime_ready" in confirmation_items
    assert "not_question_ready" in confirmation_items
    assert "targeted confirmation items instead of broad workflow blockers" in confirmation_items
