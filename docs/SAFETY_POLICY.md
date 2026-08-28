# Safety policy

## Allowed in this public demo

- Parse fake, local JSON.
- Validate required fields and unique mappings.
- Produce a dry-run plan.
- Fill a local fake form.
- Verify visible values after filling.
- Build an observation from fake validation reports.
- Deduplicate and classify generic anomaly signals.

## Deliberately excluded

- Network calls to a hiring platform.
- Login, cookies, browser profiles, passwords, OTPs, or API keys.
- CAPTCHA bypass or private endpoint discovery.
- Save, apply, delete, payment, or account-setting actions.
- Real people, employers, job URLs, or application history.
- Raw model transcripts, real user objections, or private failure logs.
- Automatic mutation of harness rules from an observation.

## Fail-closed rules

1. Missing or duplicate selectors stop the plan.
2. Missing required payload values stop the plan.
3. A visible-value mismatch is a verification failure.
4. A passing verification is not a submission; a person must review and act.
5. A validation PASS is limited to the checks performed; a disputed PASS can be observed without being treated as proven failure.
6. An observation cannot directly add, remove, or rewrite a harness rule.
