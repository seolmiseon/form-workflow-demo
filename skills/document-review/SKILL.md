---
name: document-review
description: Review an evidence-backed document against its requirements and prepare a version-bound release in this synthetic workflow repository. Use for document review or release tasks, not general prose editing.
---

# Evidence-backed document review

Use the supplied requirement and source evidence as the starting point, not a previous
PASS message. See [release design](../../docs/DOCUMENT_RELEASE.md) for the gate's scope.

## Before writing

For each material requirement, record the evidence and whether it is direct,
transferable, unknown or contradicted. Search available sources before declaring absence.
If an unknown affects the recommendation, ask what happened, who was involved,
what changed and where a record may exist. Do not turn missing records into invented facts.

Choose the smallest set of cases that adequately supports the responsibility. The main
case should explain the observed problem, investigation, choice, personal contribution
and verified outcome. Add another case only when it contributes a missing capability.
Length and visual layout follow the evidence; no fixed number of pages or projects applies.

## Read as a reviewer

Read the document without relying on the author's summary. Reconstruct what changed,
why that approach was chosen and what the result actually establishes. Quote the passages
supporting those answers. Check that diagrams preserve branches and joins, and that a
measurement is not attributed to an unrelated change. Distinguish experiments, deployed
features and future plans. A keyword's presence is not evidence of a coherent explanation.

## Release in this demo

The executable schema is illustrated by `tests/test_document_release.py` at repository root.
Create a release manifest and a review record referencing fictional JD, resume and portfolio
files relative to one release folder. Include company, reviewer, status, source hashes,
quotations and judgments (`jd_responsibility`, `causal_assessment`, `remaining_gaps`).
Record PASS only after actual content review; do not fill fields to satisfy the validator.

Call `src.document_release.render(folder, source, output)` with output outside the input
folder. It performs integrity checks before writing an HTML preview. On rejection, explain
the defect and repair the source or review rather than bypassing the gate. Source changes
require renewed review and hashes. Rendering is not visual approval or external submission.

The code validates record integrity, not the truth or quality of the recorded judgments.
