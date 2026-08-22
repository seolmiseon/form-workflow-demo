"""Public, platform-neutral form workflow primitives.

The module intentionally contains no browser, network, credential, or platform
integration code. It only validates a payload against a local form snapshot and
creates a safe fill plan.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class Field:
    key: str
    selector: str
    kind: str
    required: bool = False


@dataclass(frozen=True)
class PlanItem:
    key: str
    selector: str
    value: str


class WorkflowError(ValueError):
    """Raised when the local screen contract is unsafe to fill."""


def snapshot_fields(snapshot: dict[str, Any]) -> list[Field]:
    fields = snapshot.get("fields")
    if not isinstance(fields, list):
        raise WorkflowError("snapshot.fields must be a list")

    result: list[Field] = []
    seen_keys: set[str] = set()
    seen_selectors: set[str] = set()
    for raw in fields:
        if not isinstance(raw, dict):
            raise WorkflowError("every snapshot field must be an object")
        key = str(raw.get("key", "")).strip()
        selector = str(raw.get("selector", "")).strip()
        kind = str(raw.get("kind", "text")).strip()
        if not key or not selector:
            raise WorkflowError("a field needs both key and selector")
        if key in seen_keys or selector in seen_selectors:
            raise WorkflowError(f"ambiguous field mapping: {key}")
        seen_keys.add(key)
        seen_selectors.add(selector)
        result.append(Field(key, selector, kind, bool(raw.get("required", False))))
    return result


def _as_text(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item).strip() for item in value)
    if value is None:
        return ""
    return str(value).strip()


def build_fill_plan(payload: dict[str, Any], snapshot: dict[str, Any]) -> list[PlanItem]:
    """Create a deterministic plan; does not touch a browser or persist data."""

    fields = snapshot_fields(snapshot)
    plan: list[PlanItem] = []
    for field in fields:
        value = _as_text(payload.get(field.key))
        if field.required and not value:
            raise WorkflowError(f"required payload value is missing: {field.key}")
        if value:
            plan.append(PlanItem(field.key, field.selector, value))
    return plan


def verify_values(payload: dict[str, Any], observed: dict[str, Any], keys: Iterable[str]) -> None:
    """Verify visible values after a fill; mismatches fail closed."""

    for key in keys:
        expected = _as_text(payload.get(key))
        actual = _as_text(observed.get(key))
        if expected != actual:
            raise WorkflowError(f"visible value mismatch: {key}")


def summarize_plan(plan: list[PlanItem]) -> str:
    lines = ["DRY-RUN: no save/apply action is allowed"]
    lines.extend(f"- {item.key} -> {item.selector}: {item.value!r}" for item in plan)
    return "\n".join(lines)
