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

## Components

- **Payload**: a platform-neutral object that represents the fields to fill.
- **Form Snapshot**: a previously captured description of visible fields. It is a contract, not a live platform URL.
- **Selector Mapping**: maps a payload key to one unique local field selector.
- **Dry-run plan**: reports intended writes before any UI mutation.
- **Visible verification**: compares the value visible in the form with the payload.
- **Human gate**: save/apply are intentionally outside the automation boundary.

The public demo keeps the browser boundary local and dependency-free. A real platform adapter would be private, platform-specific, and subject to the platform's terms and the user's manual confirmation.
