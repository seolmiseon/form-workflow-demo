import unittest

from src.loop_engineer import build_observation, classify, deduplicate


PASS_REPORT = {
    "run_id": "sample-run",
    "decision": "PASS",
    "summary": "Configured checks passed.",
    "failed_checks": [],
}


class LoopEngineerTests(unittest.TestCase):
    def test_normal_pass_is_not_captured(self):
        self.assertIsNone(build_observation(PASS_REPORT))

    def test_expected_manual_review_is_not_captured(self):
        report = {**PASS_REPORT, "decision": "MANUAL_REVIEW"}
        self.assertIsNone(build_observation(report))

    def test_warn_is_captured(self):
        report = {**PASS_REPORT, "decision": "WARN", "failed_checks": ["evidence_scope"]}
        observation = build_observation(report)
        self.assertEqual(observation.kind, "validation-anomaly")
        self.assertEqual(observation.failed_checks, ("evidence_scope",))

    def test_user_can_dispute_a_pass(self):
        observation = build_observation(PASS_REPORT, user_objection="The rendered flow is incomplete.")
        self.assertEqual(observation.kind, "user-objection")
        self.assertEqual(observation.status, "UNTRIAGED")

    def test_duplicate_signals_collapse(self):
        first = build_observation(PASS_REPORT, user_objection="The rendered flow is incomplete.")
        second = build_observation(PASS_REPORT, user_objection="The rendered flow is incomplete.")
        self.assertEqual(len(deduplicate([first, second])), 1)

    def test_classification_does_not_mutate_original(self):
        observation = build_observation(PASS_REPORT, repeated_correction=True)
        reviewed = classify(observation, "pattern")
        self.assertEqual(observation.classification, "UNTRIAGED")
        self.assertEqual(reviewed.classification, "PATTERN")

    def test_rejects_unknown_classification(self):
        observation = build_observation(PASS_REPORT, repeated_correction=True)
        with self.assertRaises(ValueError):
            classify(observation, "add-a-rule-now")


if __name__ == "__main__":
    unittest.main()

