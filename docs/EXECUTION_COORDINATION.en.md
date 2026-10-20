# Execution wiring and independent review — 2026-10-20

## Problem and cause

In a personal workflow shared by multiple AI workers, message delivery was confused with actual task execution. Incident records and stall detection existed, but the continuous feed of execution observations was missing. If the coordinating worker forgot to request review, review never started.

## Structural changes

An external collector reads newly appended records from designated sessions and feeds the existing manager. A separate review queue was adopted into the manager's SQLite connection; writes to the retired store were blocked. Assignments, claims and verdicts are recorded for the two peers other than the executor. Delivery, tool activity, peer opinion and verified browser persistence remain distinct facts.

Review activity was also being collected as new implementation work. Instead of interpreting command text, the revised code associates actual review-claim timestamps with observed turn intervals for the same actor. Regression cases distinguish nested tool calls, incorrect supplied turn IDs and ordinary work that merely quotes a review command.

A requested correction creates a repair record linked to the original work. Duplicate requests and reuse of old work are rejected. A new observed revision after the claim is linked and requires both independent reviews before reaching review acceptance. Original failure history remains intact. This does not automatically prove semantic correctness or browser completion.

## Verification boundary

The private local runtime received regression tests and independent source review. Adoption into the existing manager and a collector advancing its status and reading new records were observed. The repair path was tested in isolation. Deployment verification of the recursion fix, automatic restart after termination, and a live web workflow completing repair and re-review remain unfinished.

No claim of fully unattended operation or completed automatic recovery is made. Test results and peer opinions apply only to their checked scope.

## Relationship to this public repository

This document generalizes design lessons from a private personal workflow. It does not add a running multi-model service or recruitment-platform automation to this public demo. Real sessions, accounts, application documents, execution logs and local paths are excluded. Executable public-demo scope remains as documented in the README.
