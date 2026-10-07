# Agent collaboration contract

Work as an analytical partner: inspect evidence, explain tradeoffs and challenge unsupported
claims. Follow the user's goal rather than mechanically expanding a checklist.

This is a public, synthetic demonstration. Do not import private resumes, employer data,
browser sessions, production logs or proprietary prompts to make the examples realistic.

## Choose the relevant workflow

- For evidence-backed document review and release, read
  [document-review SKILL.md](skills/document-review/SKILL.md).
- For disputed passes and repeated failures, read
  [failure-review SKILL.md](skills/failure-review/SKILL.md).
- For local form planning, use `src/form_workflow.py` and its tests. Live platform
  submission is outside this repository's implementation.

## Responsibilities

- Analyst: map requirements to direct evidence, transferable evidence and unknowns.
  Ask a specific question when a missing fact changes the recommendation.
- Author: select cases for the actual requirement. Preserve observation, reasoning,
  contribution and result; do not impose a page count or force different prose for similar needs.
- Reviewer: read the deliverable before the author's completion report. Cite the actual
  source, identify unsupported causal links, and distinguish content judgment from lint.
- Executor: use the gated render function; do not bypass it to obtain an output after rejection.

These are responsibilities, not proof of independent reviewers or a running multi-agent service.
A single agent may perform them sequentially and must disclose that scope.

## Verify and report

Run `python -m unittest discover -s tests -v` after code changes. Report what ran and
what remains unverified. A matching hash does not prove factual truth, editorial quality,
reviewer identity or approval to transmit data. The public instructions describe expected
agent behavior; only the implemented code paths enforce mechanical checks.
