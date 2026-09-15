---
name: "persona-reimplementer"
description: "Re-Implementation auditing persona — hypothetically re-implements functions then diffs against actual code. Requires deep protocol intuition. Language-agnostic. Spawned by multi-persona-orchestrator."
---
Use the [persona-reimplementer subagent](../../../.codex/agents/persona-reimplementer.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `<codebase-path>`.

Perform Re-Implementation audit on the codebase at `<codebase-path>`.

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

- [multi-persona-orchestrator](../multi-persona-orchestrator/SKILL.md) — Parent orchestrator
- [persona-mirror](../persona-mirror/SKILL.md) — Complementary symmetry analysis
