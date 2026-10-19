# Recovery decisions: failed reads versus missing values

[한국어](RECOVERY.md) | [English](RECOVERY.en.md)

A delayed page load does not prove that saving failed. Likewise, processing a save button does not prove that values persisted. This example distinguishes an unknown state from an observed mismatch and identifies only the fields requiring repair on the same target.

`src/recovery_plan.py` makes decisions from synthetic observations without accessing or writing to an external site.

| Observation | Decision | Next step |
|---|---|---|
| Target mismatch | BLOCKED_TARGET | Do not write to a different target |
| Failed read or stale observation | RETRY_READ / UNVERIFIED | Bounded rereads; no writes |
| Some values differ in a fresh observation | REPAIR_FIELDS | Plan repairs for those fields only |
| Values still differ after the repair budget is exhausted | INCOMPLETE | Do not report completion |
| All expected values match in a fresh observation | VERIFIED | Synthetic contract comparison complete |

A real adapter must supply target binding, fresh observations after saving, and per-task retry counters. This function does not authenticate those inputs. VERIFIED does not establish semantic correctness or successful submission.

Repair execution, saving, and browser rereading are outside this public example. Failed task states can be retained while other tasks are evaluated independently.

Run the tests with `python -m unittest discover -s tests -v`.

These synthetic tests do not demonstrate successful execution on a live site or measured time savings.
