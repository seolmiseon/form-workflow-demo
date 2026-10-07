"""Synthetic document release contract; not a semantic quality evaluator."""
import hashlib
import html
import json
from pathlib import Path


class ReleaseBlocked(ValueError):
    pass


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def local_file(root, name):
    if not isinstance(name, str) or not name:
        raise ReleaseBlocked("Missing artifact path")
    candidate = (root / name).resolve()
    if not candidate.is_relative_to(root) or not candidate.is_file():
        raise ReleaseBlocked("Artifact must be a file inside the release folder")
    return candidate


def validate(folder, source):
    """All contract paths are relative to one release root, regardless of cwd."""
    root = Path(folder).resolve()
    try:
        manifest = json.loads(local_file(root, "release-manifest.json").read_text(encoding="utf-8"))
        review = json.loads(local_file(root, manifest["review"]).read_text(encoding="utf-8"))
        if not manifest.get("company") or review["company"] != manifest["company"]:
            raise ReleaseBlocked("Company mismatch")
        if review["status"] != "PASS" or not review.get("reviewer"):
            raise ReleaseBlocked("Explicit review required")
        for decision in ("jd_responsibility", "causal_assessment", "remaining_gaps"):
            if not isinstance(review.get(decision), str) or not review[decision].strip():
                raise ReleaseBlocked("Missing reviewer judgment: " + decision)
        texts = {}
        for kind in ("jd", "resume", "portfolio"):
            artifact = local_file(root, manifest[kind])
            evidence = review["sources"][kind]
            if local_file(root, evidence["path"]) != artifact or digest(artifact) != evidence["sha256"]:
                raise ReleaseBlocked("Changed or mismatched artifact: " + kind)
            texts[kind] = artifact.read_text(encoding="utf-8")
        if Path(source).resolve() not in {local_file(root, manifest[k]) for k in ("resume", "portfolio")}:
            raise ReleaseBlocked("Source is not registered")
        anchors = review.get("anchors")
        if not isinstance(anchors, list) or not anchors:
            raise ReleaseBlocked("Review quotations required")
        for anchor in anchors:
            quote = anchor["quote"]
            if not isinstance(quote, str) or not quote.strip() or quote not in texts.get(anchor["source"], ""):
                raise ReleaseBlocked("Quotation absent from reviewed source")
        return {"status": "READY_FOR_RENDER", "company": manifest["company"]}
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ReleaseBlocked("Invalid release contract") from exc


def render(folder, source, output):
    """Gate before output writes. HTML keeps this public demo dependency-free."""
    validate(folder, source)
    destination = Path(output).resolve()
    if destination.is_relative_to(Path(folder).resolve()):
        raise ReleaseBlocked("Output must not overwrite release inputs")
    text = Path(source).read_text(encoding="utf-8")
    document = '<!doctype html><meta charset="utf-8"><pre>' + html.escape(text) + '</pre>'
    destination.write_text(document, encoding="utf-8")
    return destination
