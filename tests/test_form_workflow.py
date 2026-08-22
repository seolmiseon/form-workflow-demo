import unittest

from src.form_workflow import WorkflowError, build_fill_plan, verify_values


PAYLOAD = {
    "candidate_name": "Sample Candidate",
    "target_role": "Workflow Product Engineer",
    "intro": "I turn ambiguous work into observable workflows.",
    "skills": ["Python", "RAG", "Workflow"],
}

SNAPSHOT = {
    "fields": [
        {"key": "candidate_name", "selector": "#candidate-name", "required": True},
        {"key": "target_role", "selector": "#target-role", "required": True},
        {"key": "intro", "selector": "#intro", "kind": "textarea", "required": True},
        {"key": "skills", "selector": "#skills", "kind": "text"},
    ]
}


class WorkflowTests(unittest.TestCase):
    def test_builds_plan_without_side_effects(self):
        plan = build_fill_plan(PAYLOAD, SNAPSHOT)
        self.assertEqual([item.key for item in plan], ["candidate_name", "target_role", "intro", "skills"])

    def test_rejects_duplicate_selector(self):
        snapshot = {"fields": [
            {"key": "candidate_name", "selector": "#same"},
            {"key": "target_role", "selector": "#same"},
        ]}
        with self.assertRaises(WorkflowError):
            build_fill_plan(PAYLOAD, snapshot)

    def test_rejects_missing_required_value(self):
        with self.assertRaises(WorkflowError):
            build_fill_plan({"candidate_name": ""}, SNAPSHOT)

    def test_visible_values_must_match(self):
        verify_values(PAYLOAD, {
            "candidate_name": "Sample Candidate",
            "target_role": "Workflow Product Engineer",
            "intro": "I turn ambiguous work into observable workflows.",
            "skills": "Python, RAG, Workflow",
        }, PAYLOAD.keys())
        with self.assertRaises(WorkflowError):
            verify_values(PAYLOAD, {"candidate_name": "Someone Else"}, ["candidate_name"])


if __name__ == "__main__":
    unittest.main()
