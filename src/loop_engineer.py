"""Public, dependency-free Loop Engineer primitives.

The execution harness validates one workflow run. This module sits outside that
path and captures only anomaly signals that may justify later rule analysis.
It never edits the harness or promotes an observation into a rule by itself.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any


AUTO_CAPTURE = frozenset({"WARN", "REVISE", "FAIL"})
CLASSIFICATIONS = frozenset({"ONE_OFF", "PATTERN", "EXPECTED", "INSUFFICIENT_EVIDENCE"})
UNTRIAGED = "UNTRIAGED"
IN_REVIEW = "IN_REVIEW"
RESOLVED = "RESOLVED"


@dataclass(frozen=True)
class Observation:
    fingerprint: str
    status: str
    kind: str
    run_id: str
    validation_decision: str
    summary: str
    failed_checks: tuple[str, ...]
    classification: str = UNTRIAGED

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["failed_checks"] = list(self.failed_checks)
        return data


@dataclass(frozen=True)
class ArtifactEvidence:
    """One reviewed output and the digest observed during verification."""

    path: str
    sha256: str


class ResolutionError(ValueError):
    """Raised when an observation is resolved without reproducible evidence."""


def _clean_list(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(str(item).strip() for item in value if str(item).strip())


def should_capture(
    report: dict[str, Any],
    *,
    user_objection: str = "",
    model_disagreement: str = "",
    repeated_correction: bool = False,
) -> bool:
    """Return True only for an anomaly signal, not for every workflow run."""

    if user_objection.strip() or model_disagreement.strip() or repeated_correction:
        return True
    decision = str(report.get("decision", "")).strip().upper()
    return decision in AUTO_CAPTURE


def build_observation(
    report: dict[str, Any],
    *,
    user_objection: str = "",
    model_disagreement: str = "",
    repeated_correction: bool = False,
) -> Observation | None:
    """Build an immutable inbox record; return None for a normal/expected run."""

    if not should_capture(
        report,
        user_objection=user_objection,
        model_disagreement=model_disagreement,
        repeated_correction=repeated_correction,
    ):
        return None

    run_id = str(report.get("run_id", "unknown-run")).strip() or "unknown-run"
    decision = str(report.get("decision", "UNKNOWN")).strip().upper() or "UNKNOWN"
    failed_checks = _clean_list(report.get("failed_checks"))
    if user_objection.strip():
        kind, summary = "user-objection", user_objection.strip()
    elif model_disagreement.strip():
        kind, summary = "model-disagreement", model_disagreement.strip()
    elif repeated_correction:
        kind, summary = "repeated-correction", "The same correction recurred."
    else:
        kind = "validation-anomaly"
        summary = str(report.get("summary", "Validation reported an anomaly.")).strip()

    fingerprint_input = json.dumps(
        {"kind": kind, "run_id": run_id, "summary": summary, "failed_checks": failed_checks},
        ensure_ascii=False,
        sort_keys=True,
    )
    fingerprint = hashlib.sha256(fingerprint_input.encode("utf-8")).hexdigest()[:12]
    return Observation(
        fingerprint=fingerprint,
        status=UNTRIAGED,
        kind=kind,
        run_id=run_id,
        validation_decision=decision,
        summary=summary,
        failed_checks=failed_checks,
    )


def deduplicate(observations: list[Observation]) -> list[Observation]:
    """Keep the first observation for each stable fingerprint."""

    seen: set[str] = set()
    result: list[Observation] = []
    for observation in observations:
        if observation.fingerprint in seen:
            continue
        seen.add(observation.fingerprint)
        result.append(observation)
    return result


def classify(observation: Observation, classification: str) -> Observation:
    """Apply a reviewed classification without changing any harness rule."""

    normalized = classification.strip().upper()
    if normalized not in CLASSIFICATIONS:
        raise ValueError(f"unsupported classification: {classification}")
    return Observation(**{**asdict(observation), "classification": normalized, "failed_checks": observation.failed_checks})


def start_review(observation: Observation) -> Observation:
    """Move an unresolved signal into explicit human/agent review."""

    if observation.status == RESOLVED:
        raise ResolutionError("a resolved observation cannot be reopened by this helper")
    return replace(observation, status=IN_REVIEW)


def file_sha256(path: str | Path) -> str:
    """Return the SHA-256 digest of a reviewed artifact."""

    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def resolve(
    observation: Observation,
    *,
    decision_accepted: bool,
    authorization: str,
    checks: list[bool],
    artifacts: list[ArtifactEvidence],
) -> Observation:
    """Resolve only after an accepted, authorized, reproducibly verified change.

    The function intentionally does not edit a workflow.  It only records that a
    previously captured signal has passed the review gate.  Every listed artifact
    must still match the digest that was inspected, which prevents a later file
    change from inheriting an earlier PASS result.
    """

    if observation.status != IN_REVIEW:
        raise ResolutionError("start review before resolving an observation")
    if not decision_accepted:
        raise ResolutionError("an accepted review decision is required")
    if not authorization.strip():
        raise ResolutionError("human authorization is required")
    if not checks or not all(checks):
        raise ResolutionError("all verification checks must pass")
    if not artifacts:
        raise ResolutionError("at least one verified artifact is required")

    for artifact in artifacts:
        path = Path(artifact.path)
        if not path.is_file():
            raise ResolutionError(f"artifact does not exist: {path}")
        if file_sha256(path) != artifact.sha256:
            raise ResolutionError(f"artifact changed after verification: {path}")

    return replace(observation, status=RESOLVED)
