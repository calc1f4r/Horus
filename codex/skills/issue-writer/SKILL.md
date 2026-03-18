name: issue-writer
description: "Polish a validated vulnerability finding into a submission-ready write-up in Sherlock format. Use after triage to convert raw findings into professional audit report entries or contest submissions."
context: fork
agent: issue-writer
argument-hint: <finding-file-or-description>
---

<!-- AUTO-GENERATED from `.claude/skills/issue-writer/SKILL.md`; source_sha256=6b1f06d81a6420530353bd43f3dbebd072935be17bc38ede8c6be433b8bb3750 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/skills/issue-writer/SKILL.md`.
> The original skill metadata below is preserved verbatim.
> For Codex/GPT use, load `codex/agents/issue-writer.md` as the implementation playbook.
> Follow any linked `codex/resources/*` references from that agent file.
> Relative skill links remain mirrored under `codex/skills/*`.

Polish the finding at `$ARGUMENTS` into a submission-ready write-up.

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

- [/poc-writing](../poc-writing/SKILL.md) — Generates PoCs referenced in the write-up
- [/sherlock-judging](../sherlock-judging/SKILL.md) — Validates the write-up against Sherlock criteria
- [/cantina-judge](../cantina-judge/SKILL.md) — Validates against Cantina criteria
- [/code4rena-judge](../code4rena-judge/SKILL.md) — Validates against Code4rena criteria
