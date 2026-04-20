import unittest

from assessment_scope import (
    active_pasuk_id_set,
    active_pesukim_records,
    active_scope_gold_annotation_records,
    gold_skill_record_for_text,
    load_active_scope_gold_annotations_data,
    question_matches_gold_skill_record,
)
from pasuk_flow_generator import generate_question
from scripts.audit_role_layer import build_role_layer_audit


SKILLS = (
    "subject_identification",
    "object_identification",
    "phrase_translation",
)


def pasuk_by_ref(perek, pasuk):
    for record in active_pesukim_records():
        ref = record.get("ref", {})
        if ref.get("perek") == perek and ref.get("pasuk") == pasuk:
            return record["text"]
    raise AssertionError(f"Missing active pasuk {perek}:{pasuk}")


class ActiveScopeGoldAnnotationTests(unittest.TestCase):
    def test_gold_annotations_cover_the_entire_active_scope(self):
        data = load_active_scope_gold_annotations_data()

        self.assertEqual(
            data.get("metadata", {}).get("scope_id"),
            "local_parsed_bereishis_1_1_to_2_9",
        )
        self.assertEqual(
            set(active_scope_gold_annotation_records().keys()),
            set(active_pasuk_id_set()),
        )

    def test_live_questions_only_serve_gold_approved_targets(self):
        for record in active_pesukim_records():
            text = record["text"]
            for skill in SKILLS:
                question = generate_question(skill, text)
                gold_skill = gold_skill_record_for_text(text, skill)

                self.assertIsNotNone(gold_skill)
                if question.get("status") == "skipped":
                    continue

                self.assertTrue(
                    question_matches_gold_skill_record(question, gold_skill),
                    f"{skill} served a non-gold target for {record.get('pasuk_id')}: {question}",
                )

    def test_known_gold_suppressions_stay_skipped(self):
        cases = [
            ("subject_identification", pasuk_by_ref(1, 2)),
            ("object_identification", pasuk_by_ref(1, 5)),
            ("phrase_translation", pasuk_by_ref(2, 1)),
        ]

        for skill, pasuk in cases:
            question = generate_question(skill, pasuk)
            gold_skill = gold_skill_record_for_text(pasuk, skill)

            self.assertEqual(gold_skill.get("status"), "suppressed")
            self.assertEqual(question.get("status"), "skipped")

    def test_audit_compares_runtime_against_gold_truth(self):
        audit = build_role_layer_audit()

        self.assertIn("1:3", audit["parser_vs_gold"]["subject_identification"]["missed_gold_refs"])
        self.assertIn("1:3", audit["override_vs_gold"]["subject_identification"]["matched_approved_refs"])
        self.assertEqual(
            audit["override_vs_gold"]["object_identification"]["matched_approved_count"],
            11,
        )
        self.assertIn("1:17", audit["override_vs_gold"]["object_identification"]["matched_approved_refs"])
        self.assertIn("1:21", audit["override_vs_gold"]["object_identification"]["missed_gold_refs"])
        self.assertIn("1:31", audit["override_vs_gold"]["phrase_translation"]["missed_gold_refs"])
        self.assertIn("1:2", audit["override_vs_gold"]["subject_identification"]["unsupported_in_gold_refs"])
        self.assertIn("2:1", audit["override_vs_gold"]["phrase_translation"]["unsupported_in_gold_refs"])


if __name__ == "__main__":
    unittest.main()
