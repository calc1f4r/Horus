---
name: "persona-mirror"
description: "Mirror auditing persona — analyzes paired/opposite functions for asymmetries (deposit/withdraw, mint/burn, stake/unstake, lock/unlock). Language-agnostic. Spawned by multi-persona-orchestrator."
---
Use the [persona-mirror subagent](../../../.codex/agents/persona-mirror.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `<codebase-path>`.

Perform Mirror audit on the codebase at `<codebase-path>`.

## Strategy

1. **Identify function pairs** — deposit/withdraw, mint/burn, stake/unstake, open/close, lock/unlock, borrow/repay
2. **Compare semantics** — For each pair, check:
   - Do they handle fees symmetrically?
   - Do they update the same state variables in reverse?
   - Do they have matching access control?
   - Do they handle edge cases (zero, max, dust) the same way?
3. **Check roundtrip** — Does `action → reverse_action` return to the exact original state?
4. **Find asymmetries** — Any difference is a potential vulnerability

## Output format

Write findings to the designated personas output file.

## Related skills

- [multi-persona-orchestrator](../multi-persona-orchestrator/SKILL.md) — Parent orchestrator
- [persona-reimplementer](../persona-reimplementer/SKILL.md) — Complementary re-implementation approach
