import unittest

import dikduk_rules_loader as loader


class DikdukRuleLoaderTests(unittest.TestCase):
    def test_manifest_loads_expected_counts(self):
        manifest = loader.load_dikduk_rules_manifest()
        self.assertEqual(manifest["counts"]["rule_groups"], 15)
        self.assertEqual(manifest["counts"]["rules"], 37)
        self.assertEqual(manifest["counts"]["question_templates"], 47)
        self.assertEqual(manifest["counts"]["student_error_patterns"], 25)

    def test_loader_reads_all_records(self):
        self.assertEqual(len(loader.load_dikduk_rule_groups()), 15)
        self.assertEqual(len(loader.load_dikduk_rules()), 37)
        self.assertEqual(len(loader.load_dikduk_question_templates()), 47)
        self.assertEqual(len(loader.load_dikduk_error_patterns()), 25)

    def test_get_rules_by_group_returns_expected_rule(self):
        article_rules = loader.get_rules_by_group("articles")
        rule_ids = {record["rule_id"] for record in article_rules}
        self.assertEqual(rule_ids, {"DK-ARTICLE-001"})

    def test_get_rules_by_mastery_tag_finds_definite_article_rule(self):
        rules = loader.get_rules_by_mastery_tag("definite_article")
        rule_ids = {record["rule_id"] for record in rules}
        self.assertIn("DK-ARTICLE-001", rule_ids)

    def test_get_templates_for_rule_returns_linked_templates(self):
        templates = loader.get_templates_for_rule("DK-ARTICLE-001")
        template_ids = {record["template_id"] for record in templates}
        self.assertEqual(template_ids, {"QT-DK-ARTICLE-001-A", "QT-DK-ARTICLE-001-B"})

    def test_get_errors_for_rule_returns_linked_error_patterns(self):
        errors = loader.get_errors_for_rule("DK-ARTICLE-001")
        error_ids = {record["error_id"] for record in errors}
        self.assertEqual(error_ids, {"ERR-DK-ARTICLE-001", "ERR-DK-ARTICLE-002"})

    def test_utf8_hebrew_survives_load(self):
        article_rule = loader.dikduk_rule_index()["DK-ARTICLE-001"]
        self.assertEqual(article_rule["examples"][1]["hebrew"], "הבן")
        sacred_rule = loader.dikduk_rule_index()["DK-SACRED-001"]
        self.assertEqual(sacred_rule["examples"][0]["hebrew"], "יְהֹוָה")

    def test_all_records_remain_non_runtime_draft_status(self):
        forbidden_statuses = {"reviewed", "approved", "production", "runtime_active", "active"}
        for collection in (
            loader.load_dikduk_rules(),
            loader.load_dikduk_question_templates(),
            loader.load_dikduk_error_patterns(),
        ):
            for record in collection:
                self.assertNotIn(record["status"], forbidden_statuses)


if __name__ == "__main__":
    unittest.main()
