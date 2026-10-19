"""Pure recovery decisions for synthetic forms; no browser or saving actions."""
from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class Decision:
    state: str
    fields: tuple[str, ...] = ()


def decide(expected: Mapping[str, str], observed: Mapping[str, str] | None,
           *, target_matches: bool, fresh: bool, read_attempts: int = 0,
           repair_attempts: int = 0) -> Decision:
    """Caller supplies a new post-save observation, never a cached PASS.

    Unknown reads permit another read, not a write. A verified target and fresh
    complete observation are prerequisites for a field-specific repair plan.
    Retry budgets are per task; callers persist them across restarts.
    """
    if not expected or read_attempts < 0 or repair_attempts < 0:
        raise ValueError('Nonempty contract and nonnegative attempt counts required')
    if not target_matches:
        return Decision('BLOCKED_TARGET')
    if observed is None or not fresh:
        return Decision('RETRY_READ' if read_attempts < 2 else 'UNVERIFIED')
    missing = tuple(k for k, v in expected.items() if observed.get(k) != v)
    if not missing:
        return Decision('VERIFIED')
    if repair_attempts >= 1:
        return Decision('INCOMPLETE', missing)
    return Decision('REPAIR_FIELDS', missing)
