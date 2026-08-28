# Loop Engineering extension

The form workflow harness answers a local question: **did this run satisfy the contract it was given?** Loop Engineering asks a different question: **why do similar failures or suspicious passes keep recurring, and should the harness change?**

These concerns are deliberately separated.

```text
Execution harness
payload -> contract checks -> dry-run plan -> visible verification -> human gate
                                  │
                     only anomaly signals
                                  ▼
Loop Engineer inbox -> reproduce -> classify -> experiment -> reviewed decision
                                                        │
                                      no automatic rule mutation
```

## Capture policy

The demo captures:

- `WARN`, `REVISE`, or `FAIL` validation results;
- a user objection to an apparent PASS;
- a model disagreement;
- an explicitly identified repeated correction.

It skips:

- ordinary PASS runs;
- expected `MANUAL_REVIEW` states;
- duplicate fingerprints.

## Why the loop is outside the harness

Adding a rule after every failure makes an execution skill larger and more rigid. An outside loop preserves the raw signal, tests whether it is a one-off or a pattern, compares retaining, revising, deleting, and adding a rule, and requires regression evidence before recommending a change.

An observation is not authorization. The public demo can classify a signal as `ONE_OFF`, `PATTERN`, `EXPECTED`, or `INSUFFICIENT_EVIDENCE`, but it never edits execution rules automatically.

## Public boundary

The examples use fake run IDs and generic failures. They contain no resumes, employers, job URLs, platform selectors, model transcripts, personal objections, or private validation logs.

