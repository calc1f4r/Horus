---
name: "issue-writer"
description: "Polish a validated vulnerability finding into a submission-ready write-up in Sherlock format. Use after triage to convert raw findings into professional audit report entries or contest submissions."
---
Use the [issue-writer subagent](../../../.codex/agents/issue-writer.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `<finding-file-or-description>`.

Polish the finding at `<finding-file-or-description>` into a submission-ready write-up.

## Output format (Sherlock-style)

```markdown
## [Title] — concise, specific, no filler

### Summary
One paragraph: root cause + impact.

### Root Cause
Specific code reference with line numbers.

### Internal Pre-conditions
Protocol state required (not attacker actions).

### External Pre-conditions
Market/oracle conditions required.

### Attack Path
Numbered steps from attacker's perspective.

### Impact
Quantified loss with concrete numbers.

### PoC
Compilable test or step-by-step reproduction.

### Mitigation
Specific code fix with diff.
```

## Quality checklist

- [ ] Title is specific (not "Reentrancy vulnerability")
- [ ] Root cause points to exact code lines
- [ ] Attack path is step-by-step, not hand-wavy
- [ ] Impact is quantified (not "funds at risk")
- [ ] Mitigation is implementable (not "add a check")

## Related skills

- [poc-writing](../poc-writing/SKILL.md) — Generates PoCs referenced in the write-up
- [sherlock-judging](../sherlock-judging/SKILL.md) — Validates the write-up against Sherlock criteria
- [cantina-judge](../cantina-judge/SKILL.md) — Validates against Cantina criteria
- [code4rena-judge](../code4rena-judge/SKILL.md) — Validates against Code4rena criteria
