from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.loop_engineer import build_observation


ROOT = Path(__file__).resolve().parents[1]


def read_json(name: str) -> dict:
    return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))


def main() -> int:
    passing = read_json("validation_pass.sample.json")
    suspicious = read_json("validation_suspicious_pass.sample.json")

    normal = build_observation(passing)
    disputed = build_observation(
        suspicious,
        user_objection="The contract passed, but the visible flow does not prove the fallback route.",
    )

    print(f"NORMAL PASS -> {'CAPTURE' if normal else 'SKIP'}")
    print("DISPUTED PASS -> CAPTURE")
    print(json.dumps(disputed.to_dict(), indent=2, ensure_ascii=False))
    print("RULE MUTATION -> BLOCKED (reviewed decision required)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

