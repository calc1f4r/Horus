name: persona-reimplementer
description: "Re-Implementation auditing persona — hypothetically re-implements functions then diffs against actual code. Requires deep protocol intuition. Language-agnostic. Spawned by multi-persona-orchestrator."
context: fork
agent: persona-reimplementer
user-invocable: false
argument-hint: <codebase-path>
---

<!-- AUTO-GENERATED from `.claude/skills/persona-reimplementer/SKILL.md`; source_sha256=75ed9a6618a153057b7116c8ca4af2cdd522491dca7956b6ed0e5d8f0ffeb823 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/skills/persona-reimplementer/SKILL.md`.
> The original skill metadata below is preserved verbatim.
> For Codex/GPT use, load `codex/agents/persona-reimplementer.md` as the implementation playbook.
> Follow any linked `codex/resources/*` references from that agent file.
> Relative skill links remain mirrored under `codex/skills/*`.

Perform Re-Implementation audit on the codebase at `$ARGUMENTS`.

## Strategy

1. **Read the spec** — Understand what each function SHOULD do from docs, comments, interfaces
2. **Mentally re-implement** — Write pseudocode for what a correct implementation would look like
3. **Diff against actual** — Compare your re-implementation with the actual code
4. **Flag divergences** — Any difference between "what it should do" and "what it does" is a finding candidate

Focus on:
- Missing checks your implementation would include
- Different ordering of operations
- Missing event emissions
- Incorrect math formulas vs specification

## Output format

Write findings to the designated personas output file.

## Related skills

- [/multi-persona-orchestrator](../multi-persona-orchestrator/SKILL.md) — Parent orchestrator
- [/persona-mirror](../persona-mirror/SKILL.md) — Complementary symmetry analysis
