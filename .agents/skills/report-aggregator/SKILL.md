---
name: "report-aggregator"
description: "Aggregate judge-verified findings into a final Sherlock-format audit report with verified code citations. Reads confirmed findings, resolves severity consensus, verifies all line numbers against the codebase, generates GitHub permalinks, and produces CONFIRMED-REPORT.md. Use after judging completes (Phase 10) or standalone to compile findings from any source into a publication-ready report."
---
Use the [report-aggregator subagent](../../../.codex/agents/report-aggregator.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `<audit-output-dir-or-findings-path> [--repo-url=<github-url>] [--commit=<hash>] [--static-only]`.

Aggregate findings into a Sherlock-format report from `<audit-output-dir-or-findings-path>`.

## What this does

1. **Collects** all CONFIRMED findings from the judging phase
2. **Resolves** severity consensus across judges (2-of-3 rule)
3. **Verifies** every code citation against the actual codebase — fixes stale line numbers
4. **Generates** GitHub permalinks for all in-repo code references
5. **Assembles** the final report in Sherlock submission format

## Sherlock finding format

Each finding in the report follows this structure:

```markdown
## [Title]

### Summary
[What's wrong, where, and impact]

### Root Cause
In [`file.sol:42`](https://github.com/org/repo/blob/<commit>/src/file.sol#L42), ...

### Internal Pre-conditions
1. [Protocol state required]

### External Pre-conditions
1. [External conditions required]

### Attack Path
1. Attacker calls [`function()`](permalink) with ...
2. This causes ... because [code citation] ...

### Impact
[Concrete quantified impact]

### PoC
[Inline code block — no GitHub links]

### Mitigation
[Inline recommended fix — no GitHub links]
```

## Flags

- `--repo-url=<url>` — GitHub repo URL for generating permalinks
- `--commit=<hash>` — Commit hash for permalinks (auto-detected from git if omitted)
- `--static-only` — Mark execution evidence as "skipped (static-only mode)"

## Output

- `audit-output/CONFIRMED-REPORT.md` — Final publication-quality report

## Related skills

- [judge-orchestrator](../judge-orchestrator/SKILL.md) — Produces the judged verdicts this skill consumes
- [issue-writer](../issue-writer/SKILL.md) — Produces polished individual findings used as input
- [audit-orchestrator](../audit-orchestrator/SKILL.md) — Parent pipeline (Phase 11)
- [poc-writing](../poc-writing/SKILL.md) — Produces PoCs inlined in the final report
