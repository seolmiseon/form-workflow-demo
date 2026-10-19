# Human-reviewed form automation and failure improvement loop

[한국어](README.md) | [English](README.en.md)

A public demo of **document → structured payload → form inspection → input plan → value verification → human review**, using synthetic data and a local mock form. A separate **Loop Engineer layer** selects recurring failures for investigation instead of treating every successful run as learning material.

This is not the production job-application automation system. It contains no real applicant data or platform sessions and does not automate saving, submitting applications, or deleting records.

## Run the demos

Python 3.10+ is sufficient.

```bash
python scripts/run_demo.py
python scripts/run_loop_demo.py
python -m unittest discover -s tests -v
```

Open `demo/index.html` in a browser to inspect the local form flow:

1. Read `examples/payload.sample.json`.
2. Map the payload to fields in `examples/form_snapshot.sample.json`.
3. Produce an input plan and report blocked sensitive actions.
4. Fill values in the local form and compare them with the payload.
5. Leave saving and submission disabled for human review.

The loop demo selects `WARN/REVISE/FAIL`, disputed PASS decisions, conflicting model assessments, and repeated revisions as observation candidates. It does not collect ordinary PASS results or change harness rules without a reviewed decision.

## Repository structure

```text
src/form_workflow.py       # Payload/snapshot validation and input planning
src/loop_engineer.py       # Signal selection, deduplication, review classification
src/document_release.py   # Review-record integrity checks before HTML rendering
src/recovery_plan.py      # Bounded decisions for rereading or field repair
scripts/run_demo.py        # Dependency-free CLI demo
scripts/run_loop_demo.py   # Ordinary versus disputed PASS decisions
demo/index.html            # Local mock form, not an external platform
examples/                  # Synthetic company and applicant data
tests/                     # Contract and decision-boundary tests
docs/                      # Architecture, safety, and loop design
```

## From document review to rendering

Requiring review in instructions is different from enforcing review-record checks in an execution path. `src/document_release.py` binds a synthetic document to its company, source, quoted review evidence, and hashes. Its renderer checks that contract before producing HTML.

Missing contracts, company mismatches, and source changes after review are blocked before an existing output is overwritten. This checks the integrity of review records, not the quality or truth of the review itself. See the [document release design (Korean)](docs/DOCUMENT_RELEASE.md) for the failure context, decisions, tests, and limitations.

## Agent instructions and executable checks

- [AGENTS.md (Korean)](AGENTS.md): analysis, writing, review, execution, and disclosure boundaries.
- [Document review skill (Korean)](skills/document-review/SKILL.md): requirement/evidence comparison, example selection, text review, and version binding.
- [Failure review skill (Korean)](skills/failure-review/SKILL.md): disputed PASS investigation, minimal corrections, and regression checks.

These files describe procedures for an agent to read and follow. Their existence does not launch independent agents or guarantee compliance. Code and tests define the mechanically enforced boundaries; instructions define the judgments expected from reviewers. Private writing strategies are not included.

## Recovery decisions after a blocked or incomplete run

The recovery example separates delayed reads from observed missing values. Only mismatches in a fresh observation become field-repair candidates, with bounded reread and repair attempts. It prevents a different target or stale PASS from being treated as completion within the supplied contract.

See [recovery decisions and verification scope](docs/RECOVERY.en.md). Actual browser saving and repair execution are not included.

## Public scope

Included:

- Payload generation and validation.
- Example field contracts for form snapshots.
- Selector mapping and pre-execution dry-run planning.
- Post-input value comparison.
- Policies separating ordinary PASS results from anomalous signals.
- Generalized synthetic records of disputes and repeated revisions.
- Deduplication and `ONE_OFF/PATTERN/EXPECTED/INSUFFICIENT_EVIDENCE` classification.
- Synthetic data and reproducible tests.

Excluded:

- Real recruitment-platform URLs, company names, and applicant information.
- Real payloads, snapshots, execution logs, disputes, or model conversations.
- Cookies, sessions, browser profiles, passwords, and OTPs.
- Private platform selectors or private API calls.
- Code that clicks save or application-submission buttons.

## Design principles

- Inspect the form contract before planning input.
- Stop the plan when fields are missing or ambiguously matched.
- Do not interpret automation output as successful submission.
- Separate value verification from final human review.
- Do not extend a test PASS to meanings or evidence that the test never checked.
- Investigate recurring failures and regression impact before adding rules.
- An observation is not authorization to change the harness.
- Do not present private company assets or real-work metrics as evidence for this public demo.

The demo shows a human-in-the-loop workflow that normalizes unstructured documents, checks form contracts, and blocks unsafe execution plans. Its outer loop questions whether passing checks reflects actual quality, then routes selected failures toward reviewed corrections and regression verification.

Additional design documents are currently in Korean: [architecture](docs/ARCHITECTURE.md), [safety policy](docs/SAFETY_POLICY.md), and [failure improvement loop](docs/LOOP_ENGINEERING.md).
