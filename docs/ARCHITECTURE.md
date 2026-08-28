# Architecture

```text
sample payload
    │
    ▼
Form Snapshot ──► Selector Mapping ──► Dry-run Fill Plan
    │                                      │
    └──────────── contract checks ◄────────┘
                                           │
                                           ▼
                              Local visible-value verification
                                           │
                                           ▼
                                    Human final review
```

The execution path emits only anomaly signals to a separate Loop Engineer:

```text
Validation report ──► Signal policy ──► normal/expected ──► skip
                            │
                            └──────────► anomaly ──► deduplicated inbox record
                                                        │
                                                        ▼
                                             reproduce and classify
                                                        │
                                                        ▼
                                              reviewed experiment
                                                        │
                                                        ▼
                                           rule proposal (never automatic)
```

## Components

- **Payload**: a platform-neutral object that represents the fields to fill.
- **Form Snapshot**: a previously captured description of visible fields. It is a contract, not a live platform URL.
- **Selector Mapping**: maps a payload key to one unique local field selector.
- **Dry-run plan**: reports intended writes before any UI mutation.
- **Visible verification**: compares the value visible in the form with the payload.
- **Human gate**: save/apply are intentionally outside the automation boundary.
- **Signal policy**: captures failures, warnings, disputed passes, disagreements, and repeated corrections—not every run.
- **Loop inbox**: stores immutable, deduplicated observations outside the execution path.
- **Reviewed decision**: separates one-off defects from patterns before any harness change is proposed.

The public demo keeps the browser boundary local and dependency-free. A real platform adapter would be private, platform-specific, and subject to the platform's terms and the user's manual confirmation.

The Loop Engineer is not a second application generator or a model with broader authority. It audits the harness, and its observations cannot mutate execution rules by themselves.
