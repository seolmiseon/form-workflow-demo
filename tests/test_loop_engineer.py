import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.loop_engineer import (
    ArtifactEvidence,
    ResolutionError,
    build_observation,
    classify,
    deduplicate,
    file_sha256,
    resolve,
    start_review,
)


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

    def test_resolution_requires_explicit_review_first(self):
        observation = build_observation(PASS_REPORT, repeated_correction=True)
        with self.assertRaises(ResolutionError):
            resolve(
                observation,
                decision_accepted=True,
                authorization="Approved after review.",
                checks=[True],
                artifacts=[],
            )

    def test_resolution_rejects_incomplete_evidence(self):
        observation = start_review(build_observation(PASS_REPORT, repeated_correction=True))
        with self.assertRaises(ResolutionError):
            resolve(
                observation,
                decision_accepted=False,
                authorization="",
                checks=[False],
                artifacts=[],
            )

    def test_resolution_requires_hash_matched_artifacts(self):
        observation = start_review(build_observation(PASS_REPORT, repeated_correction=True))
        with TemporaryDirectory() as directory:
            artifact = Path(directory) / "verified-output.txt"
            artifact.write_text("verified", encoding="utf-8")
            evidence = ArtifactEvidence(str(artifact), file_sha256(artifact))
            resolved = resolve(
                observation,
                decision_accepted=True,
                authorization="Approved after review.",
                checks=[True, True],
                artifacts=[evidence],
            )
            self.assertEqual(resolved.status, "RESOLVED")
            self.assertEqual(observation.status, "IN_REVIEW")

    def test_stale_artifact_cannot_inherit_an_old_pass(self):
        observation = start_review(build_observation(PASS_REPORT, repeated_correction=True))
        with TemporaryDirectory() as directory:
            artifact = Path(directory) / "verified-output.txt"
            artifact.write_text("before", encoding="utf-8")
            evidence = ArtifactEvidence(str(artifact), file_sha256(artifact))
            artifact.write_text("after", encoding="utf-8")
            with self.assertRaises(ResolutionError):
                resolve(
                    observation,
                    decision_accepted=True,
                    authorization="Approved after review.",
                    checks=[True],
                    artifacts=[evidence],
                )


if __name__ == "__main__":
    unittest.main()
