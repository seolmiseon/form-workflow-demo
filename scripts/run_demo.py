from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.form_workflow import WorkflowError, build_fill_plan, summarize_plan, verify_values


ROOT = Path(__file__).resolve().parents[1]


def read_json(name: str) -> dict:
    return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))


def main() -> int:
    payload = read_json("payload.sample.json")
    snapshot = read_json("form_snapshot.sample.json")
    try:
        plan = build_fill_plan(payload, snapshot)
        print(summarize_plan(plan))
        observed = {item.key: item.value for item in plan}
        verify_values(payload, observed, (item.key for item in plan))
        print("VISIBLE-VERIFY: PASS")
        print("HUMAN-CHECK: required before any save/apply action")
        print("SAVE/APPLY: BLOCKED")
        return 0
    except WorkflowError as exc:
        print(f"FAIL-CLOSED: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
