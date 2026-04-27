from pathlib import Path

import pytest

from scripts import generate_trusted_source_extraction_review_packet as generator


ROOT = Path(__file__).resolve().parents[1]
DIAGNOSTIC_PREVIEW_GENERATOR = ROOT / "scripts" / "generate_diagnostic_preview.py"
MANIFEST_PATH = ROOT / "data" / "curriculum_extraction" / "curriculum_extraction_manifest.json"
SAVED_BATCH_002_PACKET_PATH = (
    ROOT
    / "data"
    / "curriculum_extraction"
    / "reports"
    / "batch_002_trusted_source_extraction_accuracy_review_packet.md"
)
SAVED_BATCH_002_PRINT_PACKET_PATH = (
    ROOT
    / "data"
    / "curriculum_extraction"
    / "reports"
    / "batch_002_trusted_source_extraction_accuracy_review_packet_print.md"
)
SAVED_BATCH_003_PRINT_PACKET_PATH = (
    ROOT
    / "data"
    / "curriculum_extraction"
    / "reports"
    / "batch_003_trusted_source_extraction_accuracy_review_packet_print.md"
)


def test_trusted_source_packet_uses_template_language():
    packet = generator.render_packet(
        source_package_id="linear_chumash_translation_most_parshiyos_in_torah",
        batch_id="batch_002_linear_bereishis",
    )

    assert "trusted teacher-source extraction review template" in packet
    assert "one extraction-accuracy confirmation pass" in packet
    assert "Confirm that the copied or OCRed source text matches the source." in packet
    assert "Confirm that Hebrew spelling, nikud, and table layout are faithful" in packet
    assert "Confirm that translations, explanations, answer keys, or examples were extracted accurately." in packet
    assert "Confirm that classification and standards/skill mapping are reasonable." in packet
    assert "Do not re-approve the educational value" in packet
    assert "## 1. One-Page Review Summary" in packet
    assert "## 5. Expanded Source Evidence Review Samples" in packet
    assert "## 10. Final Decision Page" in packet


def test_saved_batch_002_packet_is_linked_as_review_artifact():
    manifest = generator.load_json(MANIFEST_PATH)
    batch = next(
        item
        for item in manifest["resource_batches"]
        if item["batch_id"] == "batch_002_linear_bereishis"
    )
    relative_packet = "data/curriculum_extraction/reports/batch_002_trusted_source_extraction_accuracy_review_packet.md"
    packet_text = SAVED_BATCH_002_PACKET_PATH.read_text(encoding="utf-8")

    assert SAVED_BATCH_002_PACKET_PATH.exists()
    assert relative_packet in batch["review_artifacts"]
    assert batch["extraction_review_status"] == "pending_yossi_extraction_accuracy_pass"
    assert batch["integration_status"] == "not_runtime_active"
    assert batch["runtime_active"] is False
    assert "one extraction-accuracy confirmation pass" in packet_text
    assert "not broad educational re-approval" in packet_text
    assert "Runtime: blocked" in packet_text
    assert "Question generation: blocked" in packet_text


def test_print_friendly_packet_includes_actual_sampled_records():
    packet = generator.render_packet(
        source_package_id="linear_chumash_translation_most_parshiyos_in_torah",
        batch_id="batch_002_linear_bereishis",
    )

    assert "pasuk_segment_batch_002_bereishis_1_6_001" in packet
    assert "- Source excerpt:" in packet
    assert "- Cleaned source Hebrew side:" in packet
    assert "- Extracted Hebrew:" in packet
    assert "- Source English / Translation side:" in packet
    assert "- Extracted English / Translation:" in packet
    assert "- Why this match is believed correct:" in packet
    assert "Human review question:" in packet
    assert "and Hashem said" in packet
    assert "- [ ] Source match" in packet
    assert "- [ ] English / translation alignment" in packet
    assert "- [ ] Parenthetical explanation alignment" in packet
    assert '<div style="page-break-after: always;"></div>' in packet


def test_print_friendly_packets_are_linked_for_batch_002_and_003():
    manifest = generator.load_json(MANIFEST_PATH)
    batches = {batch["batch_id"]: batch for batch in manifest["resource_batches"]}

    assert SAVED_BATCH_002_PRINT_PACKET_PATH.exists()
    assert SAVED_BATCH_003_PRINT_PACKET_PATH.exists()
    assert (
        "data/curriculum_extraction/reports/batch_002_trusted_source_extraction_accuracy_review_packet_print.md"
        in batches["batch_002_linear_bereishis"]["review_artifacts"]
    )
    assert (
        "data/curriculum_extraction/reports/batch_003_trusted_source_extraction_accuracy_review_packet_print.md"
        in batches["batch_003_linear_bereishis_2_4_to_2_25"]["review_artifacts"]
    )


def test_print_friendly_packets_include_summary_counts_and_final_decision_page():
    for path, expected_count in [
        (SAVED_BATCH_002_PRINT_PACKET_PATH, "Number of extracted records: `123`"),
        (SAVED_BATCH_003_PRINT_PACKET_PATH, "Number of extracted records: `90`"),
    ]:
        packet = path.read_text(encoding="utf-8")
        assert expected_count in packet
        assert "## 7. Extraction Summary Table" in packet
        assert "## 10. Final Decision Page" in packet
        assert "Yossi decision box:" in packet
        assert "Recommended current Yossi decision: Not fully approved yet" in packet
        assert "Runtime: blocked" in packet
        assert "Question generation: blocked" in packet


def test_expanded_packets_include_deterministic_sample_buckets_and_batch_specific_checks():
    packet_002 = SAVED_BATCH_002_PRINT_PACKET_PATH.read_text(encoding="utf-8")
    packet_003 = SAVED_BATCH_003_PRINT_PACKET_PATH.read_text(encoding="utf-8")

    assert packet_002.count("### Item ") == 37
    assert packet_003.count("### Item ") == 32
    assert "Samples included in this packet: `37`" in packet_002
    assert "Samples included in this packet: `32`" in packet_003
    packet = packet_002
    assert "First records: first 5 records" in packet
    assert "Last records: last 5 records" in packet
    assert "Deterministic random records: 10 records selected by stable SHA-256 ordering" in packet
    assert "Longest English / explanatory records: top 10 by extracted English length" in packet
    assert "Long parenthetical records: all records with substantial parenthetical or explanatory text" in packet
    assert "Long Hebrew records: top 10 by extracted Hebrew phrase length" in packet
    assert "Sample bucket counts:" in packet
    assert "`confirm_hebrew_english_phrase_matching`" in packet
    assert "`confirm_parenthetical_explanation_alignment`" in packet
    assert "`confirm_long_phrase_boundary_accuracy`" in packet
    assert "`confirm_source_wording_not_generated`" in packet
    assert "`confirm_cleanup_normalization_acceptable`" in packet
    assert "`confirm_segment_order_matches_pasuk_flow`" in packet


def test_unrelated_global_confirmation_items_are_omitted_from_batch_packets():
    packet = SAVED_BATCH_002_PRINT_PACKET_PATH.read_text(encoding="utf-8")

    assert "Batch-specific targeted confirmation items:" in packet
    assert "Unrelated global confirmation items were intentionally omitted from this batch packet." in packet
    assert "### Global Confirmation Items Not Specific To This Batch" not in packet
    assert "confirm_loshon_foundation_rules_jsonl_source_alignment" not in packet


def test_batch_002_and_003_remain_pending_after_expanded_packets():
    manifest = generator.load_json(MANIFEST_PATH)
    batches = {batch["batch_id"]: batch for batch in manifest["resource_batches"]}
    for batch_id in ["batch_002_linear_bereishis", "batch_003_linear_bereishis_2_4_to_2_25"]:
        batch = batches[batch_id]
        assert batch["extraction_review_status"] == "pending_yossi_extraction_accuracy_pass"
        assert batch["integration_status"] == "not_runtime_active"
        assert batch["runtime_active"] is False


def test_trusted_source_packet_keeps_runtime_and_question_generation_blocked():
    packet = generator.render_packet(source_package_id="vocabulary_priority_pack")

    assert "Runtime: blocked" in packet
    assert "Question generation: blocked" in packet
    assert "Reviewed bank: blocked" in packet
    assert "Student-facing use: blocked" in packet
    assert "Runtime status: `not_runtime_ready`" in packet
    assert "Question-generation status: `not_question_ready`" in packet


def test_batch_specific_confirmation_items_are_rendered_without_global_noise():
    packet = generator.render_packet(source_package_id="first_150_shorashim_and_keywords_bereishis")

    assert "## 8. Targeted Confirmation Items" in packet
    assert "Exact Question For Yossi" in packet
    assert "pending_yossi_extraction_accuracy_pass" in packet
    assert "confirm_hebrew_english_phrase_matching" in packet
    assert "confirm_parenthetical_explanation_alignment" in packet
    assert "confirm_loshon_foundation_rules_jsonl_source_alignment" not in packet


def test_generated_question_packet_generator_does_not_use_trusted_source_review_path():
    script_text = DIAGNOSTIC_PREVIEW_GENERATOR.read_text(encoding="utf-8")

    assert "write_manual_review_packet" in script_text
    assert "Teacher checkbox" in script_text
    assert "trusted_source_extraction_accuracy_pass" not in script_text
    assert "generate_trusted_source_extraction_review_packet" not in script_text


def test_runtime_promotion_language_remains_separate_in_template():
    template = generator.load_template_text()

    assert "Runtime activation | Runtime activation gate" in template
    assert "reviewed-bank promotion" in template
    assert "does not become runtime-active unless a separate runtime activation gate" in template


def test_historical_reports_are_not_generator_inputs():
    packet = generator.render_packet(source_package_id="linear_chumash_translation_most_parshiyos_in_torah")

    assert "data/curriculum_extraction/reports/batch_004_manual_review_packet.md" not in packet
    assert "data/diagnostic_preview/reports/bereishis_1_1_to_2_3_manual_review_packet.md" not in packet


def test_non_trusted_source_package_is_rejected():
    registry = generator.load_json(generator.REGISTRY_PATH)
    registry = {
        **registry,
        "source_packages": [
            {
                **registry["source_packages"][0],
                "source_package_id": "unclear_package",
                "teacher_source_status": "needs_specific_confirmation",
            }
        ],
    }

    with pytest.raises(ValueError, match="may only be generated for trusted teacher-source packages"):
        generator.render_packet(source_package_id="unclear_package", registry=registry)
