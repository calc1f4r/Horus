---
name: "mitigation-reviewer"
description: "Run a fix-verification engagement — given prior findings and the sponsor's fix diff, verify each fix works and introduces nothing new. Produces a four-value verdict per finding backed by re-derived evidence from patched code, re-runs original PoCs, and hunts regressions across the fix blast radius. Use for mitigation review engagements after fixes ship."
---
Use the [mitigation-reviewer subagent](../../../.codex/agents/mitigation-reviewer.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `<target-path> <base-ref> <fixed-ref> [original-report-path]`.

Review the fixes in `<target-path>`.

## Verdicts

| Verdict | Criterion |
|---------|-----------|
| `FIXED` | Root cause addressed, no sibling path, no new issue |
| `PARTIALLY FIXED` | Reported path blocked, sibling path to the same root cause remains |
| `NOT FIXED` | Original attack path still executes |
| `FIXED BUT INTRODUCED NEW ISSUE` | Path blocked, new issue created |

Exactly one verdict per original finding, each citing patched-code `file:line`. A passing original PoC is mechanical proof of `NOT FIXED`.

## Passes

1. Diff scope + blast radius (callers, callees, shared state, depth 2)
2. Per-finding re-derivation from patched code, including sibling-path analysis
3. PoC re-execution against the fixed ref
4. Regression hunt on the blast radius
5. New issues routed through the platform judges

## Output

- `MITIGATION-REVIEW.md`

## Related skills

- [recon-specialist](../recon-specialist/SKILL.md) — diff scoping (`--diff`)
- [remediation-safety-checker](../remediation-safety-checker/SKILL.md) — validates *our* advice, pre-ship
- [judge-orchestrator](../judge-orchestrator/SKILL.md) — severity for new issues
- [poc-writing](../poc-writing/SKILL.md) — PoC re-execution conventions
