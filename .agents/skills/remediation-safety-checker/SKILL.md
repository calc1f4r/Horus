---
name: "remediation-safety-checker"
description: "Report gate that validates the remediations Horus itself recommends before the report ships. Per remediation checks root-cause coverage, blast radius, honest-flow impact, cross-fix interactions, invariant compliance, and whether the recommended pattern is itself a known-vulnerable DB pattern; optionally patches a copy and re-runs PoCs and fuzz suites. Returns SAFE / RISKY / UNSAFE with rewritten text. Use between Phase 9 and Phase 11."
---
Use the [remediation-safety-checker subagent](../../../.codex/agents/remediation-safety-checker.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `[audit-output-dir]`.

Validate the recommended remediations in `<arguments>`.

## Six checks per remediation

| ID | Check |
|----|-------|
| C1 | Root-cause coverage — every path in the cluster, not just the reported one |
| C2 | Blast radius — callers, callees, readers of changed state |
| C3 | Honest-flow — does the fix DoS legitimate users? |
| C4 | Fix interactions — evaluated across the **combined** set, never in isolation |
| C5 | Invariant compliance against `02-invariants-reviewed.md` |
| C6 | DB anti-pattern query — is the recommended fix itself a known-vulnerable pattern? |

## Verdicts

`SAFE` / `RISKY` / `UNSAFE`. RISKY and UNSAFE must ship **rewritten, ship-ready remediation text**; a verdict without a corrected recommendation is half the job. No `UNSAFE` remediation reaches Phase 11.

## Mechanical mode

When the target builds: patch a **copy**, rebuild, re-run the finding's PoC (expect neutralised) and any invariant/fuzz suites (expect still passing). Results reported as they happened; skips logged with reasons.

## Output

- `audit-output/10b-remediation-safety.md` + updated remediation text in the report draft

## Related skills

- [mitigation-reviewer](../mitigation-reviewer/SKILL.md) — reviews the sponsor's *applied* diff later
- [report-aggregator](../report-aggregator/SKILL.md) — downstream, refuses UNSAFE remediations
- [issue-writer](../issue-writer/SKILL.md) — upstream prose polishing
