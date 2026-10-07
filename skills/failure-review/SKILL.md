---
name: failure-review
description: Investigate a disputed PASS, repeated correction or workflow failure and test a scoped remedy in this repository. Use for regression analysis, not routine successful runs.
---

# Failure review loop

Read [loop lifecycle](../../docs/LOOP_ENGINEERING.md) when recording an observation
or resolution through `src/loop_engineer.py`.

1. Preserve the failing artifact and expected behavior. Separate the observation from
   hypotheses about its cause. A complaint is a signal to investigate, not an instruction
   to apply the same rewrite everywhere.
2. Trace both the content decision and the execution path. A skipped review explains why
   a defect escaped; it does not necessarily explain why the content was poor.
3. Compare retaining, narrowing, revising or adding a rule. Prefer the smallest change
   addressing the reproduced cause. Do not introduce company-specific keywords as a
   universal content gate.
4. Test the failing case, a valid case with a different structure, and a stale or mismatched
   artifact. For enforcement defects, invoke the real entry point rather than testing only
   its helper. Ensure rejection preserves any prior output.
5. Inspect the resulting content separately from test results. Record whether verification
   was mechanical, editorial or visual. State any untested scope.

Use the existing lifecycle's reviewed decision and authorization fields when resolving a
signal. An observation alone does not authorize changing production rules. Authorization
already supplied by the user may cover the agreed remedy; do not ask for it repeatedly.

Keep real case records private. Public reproductions use fictional data and explain the
general failure, investigation, decision, regression evidence and remaining limitation.
