# From written instructions to enforced document review

## Failure and investigation

A document can look complete while losing the reasoning that makes its claims credible.
Written review rules alone did not prevent an author from putting a draft in a final
folder without running the review. These are two separate problems:

- Content failure: weak causal explanation or an inaccurate technical summary.
- Execution failure: a missing review did not prevent artifact generation.

Adding more keywords cannot establish that a document answers the actual requirement.
The design therefore separates editorial judgment from mechanically enforceable integrity.

## Decision

A reviewer reads the requirement and source, records the contribution, causal reasoning
and remaining gaps, and anchors the review in quotations. Reusing a relevant case across
similar requirements is allowed; artificial uniqueness is not a quality goal.

A release manifest binds the company, requirement, resume and portfolio to that review.
The renderer calls the gate itself before writing output. A separate optional check would
leave the original bypass open. All contract paths have one root, and changed inputs
invalidate the recorded hashes. Rejection leaves an existing output untouched.

```text
Requirement + evidence -> draft -> editorial review with quotations
                                      |
                          source hashes + release manifest
                                      |
                          render entry point -> integrity gate
                                      |              |
                                    allow          reject
                                      |              |
                                 HTML preview   preserve previous output
```

## Public reproduction

`src/document_release.py` is a small, independent demonstration, not a copy of the
private production harness. Tests construct fictional records in temporary folders.
HTML is used instead of PDF to require only the Python standard library.

```bash
python -m unittest discover -s tests -v
```

The regression cases cover a valid render, missing manifest, wrong company,
unregistered source, stale hashes for each input, false quotations, escaped paths,
input overwrite and preservation of previous output after rejection.

## What this does not prove

The gate verifies links, hashes and review-record presence. It cannot prove that an
author's claims are true, that the reasoning is persuasive, or that an employer will
select a candidate. A deliberately weak but structurally complete judgment is tested
as an explicit limitation. Human/editorial review and visual review remain necessary.

Hashes are change detection, not authentication or signatures. A party allowed to
rewrite both the source and its review can manufacture a matching record. This demo
does not implement reviewer identity enforcement, concurrent-write protection,
atomic publication or enforcement over arbitrary alternative renderers.

No real applicant data, employer details, private prompts, conversation transcripts,
company assets or production failure logs are published here.
