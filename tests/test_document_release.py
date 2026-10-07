import json
from pathlib import Path
import tempfile
import unittest

from src.document_release import ReleaseBlocked, digest, render, validate


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "release"
        self.root.mkdir()
        self.output = self.root.parent / "preview.html"
        for name, text in {"jd": "Build input validation.", "resume": "Implemented request checks.",
                           "portfolio": "Missing fields caused errors. I inspected requests and added validation."}.items():
            (self.root / (name + ".txt")).write_text(text, encoding="utf-8")
        self.source = self.root / "portfolio.txt"
        self.manifest = {"company": "Example Company", "review": "review.json",
                         **{k: k + ".txt" for k in ("jd", "resume", "portfolio")}}
        self.review = {"company": "Example Company", "reviewer": "Example Reviewer", "status": "PASS",
                       "jd_responsibility": "Input checks directly address the requirement.",
                       "causal_assessment": "Observed missing fields led to validation.",
                       "remaining_gaps": "No scale claim is made.",
                       "sources": {k: {"path": k + ".txt", "sha256": digest(self.root / (k + ".txt"))}
                                   for k in ("jd", "resume", "portfolio")},
                       "anchors": [{"source": "portfolio", "quote": "I inspected requests and added validation."}]}
        self.save()

    def save(self):
        (self.root / "release-manifest.json").write_text(json.dumps(self.manifest), encoding="utf-8")
        (self.root / "review.json").write_text(json.dumps(self.review), encoding="utf-8")

    def blocked(self):
        self.output.write_text("previous approved output", encoding="utf-8")
        before = digest(self.output)
        with self.assertRaises(ReleaseBlocked):
            render(self.root, self.source, self.output)
        self.assertEqual(before, digest(self.output))

    def test_valid_contract_renders(self):
        render(self.root, self.source, self.output)
        self.assertIn("Missing fields", self.output.read_text())

    def test_missing_manifest_preserves_output(self):
        (self.root / "release-manifest.json").unlink()
        self.blocked()

    def test_company_mismatch(self):
        self.review["company"] = "Other Company"
        self.save()
        self.blocked()

    def test_stale_approval_for_each_input(self):
        for kind in ("jd", "resume", "portfolio"):
            with self.subTest(kind=kind):
                file = self.root / (kind + ".txt")
                old = file.read_text()
                file.write_text(old + " changed")
                self.blocked()
                file.write_text(old)

    def test_unregistered_source(self):
        self.source = self.root / "other.txt"
        self.source.write_text("Unreviewed")
        self.blocked()

    def test_fake_quote(self):
        self.review["anchors"][0]["quote"] = "Not in source"
        self.save()
        self.blocked()

    def test_paths_cannot_escape_root(self):
        self.manifest["resume"] = "../preview.html"
        self.save()
        self.blocked()

    def test_output_cannot_replace_input(self):
        before = digest(self.source)
        with self.assertRaises(ReleaseBlocked):
            render(self.root, self.source, self.source)
        self.assertEqual(before, digest(self.source))

    def test_formally_complete_judgment_is_not_semantic_proof(self):
        # Deliberately weak prose still passes integrity checks: a documented limit.
        self.review["causal_assessment"] = "Looks good."
        self.save()
        self.assertEqual(validate(self.root, self.source)["status"], "READY_FOR_RENDER")


if __name__ == "__main__":
    unittest.main()
