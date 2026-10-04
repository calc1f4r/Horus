# Mitigation review

A mitigation review is a separate engagement from the original audit: the sponsor shipped fixes, and someone has to say whether each fix works and whether it broke anything else. `mitigation-reviewer` runs that engagement.

## What you give it

- The original findings: `CONFIRMED-REPORT.md` or any structured findings list.
- The fix diff: a base ref and the fixed ref. The agent uses recon's diff mode to compute what changed and the blast radius around it (callers and callees of changed functions).

```
/agent mitigation-reviewer <codebase-path> --findings <report-or-dir> --base <ref> --fixed <ref>
```

## What it does per finding

Re-derives exploitability from the patched code, not from the commit message. Then one of four verdicts:

- `FIXED` — the root cause is gone, with file and line evidence from the patched code.
- `PARTIALLY FIXED` — the reported path is closed but the root cause survives another way.
- `NOT FIXED` — still exploitable. A re-run PoC that still passes is mechanical proof of this.
- `FIXED BUT INTRODUCED NEW ISSUE` — the fix works and created a new bug.

That last verdict is where the regression hunt matters. The fix diff itself gets a discovery pass over its blast radius using the same discovery agents the original audit used. New issues go through the platform judges for severity before they appear in the report.

PoCs from the original audit get re-executed against the patched code when they exist. Passing PoC means NOT FIXED, no argument.

## What you get

`MITIGATION-REVIEW.md`: one verdict per original finding with evidence, plus any new-issue submissions in report format.

## Related but different

`remediation-safety-checker` does the inverse job inside an audit: it checks the fixes your own report recommends, before the report ships. One reviews the sponsor's applied diff after the fact, the other reviews your advice before you give it.
