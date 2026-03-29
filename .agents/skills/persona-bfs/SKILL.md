---
name: "persona-bfs"
description: "BFS auditing persona — maps entry points then progressively deepens. Language-agnostic. Applies Feynman questioning at every depth layer. Spawned by multi-persona-orchestrator."
---
Use the [persona-bfs subagent](../../../.codex/agents/persona-bfs.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `<codebase-path>`.

Perform Breadth-First Search audit on the codebase at `<codebase-path>`.

## Strategy

1. **Depth 0** — Enumerate all external/public entry points
2. **Depth 1** — For each entry point, map immediate internal calls and state changes
3. **Depth 2** — Follow internal calls one level deeper, check interaction patterns
4. **Depth N** — Continue until leaf functions reached

At each depth layer, apply Feynman questioning:
- "Can I explain exactly what this function does in simple terms?"
- "What would break if this assumption were wrong?"
- "What's the simplest way an attacker could abuse this?"

## Output format

Write findings to the designated personas output file with: finding ID, severity, root cause, affected functions, and reachability proof.

## Related skills

- [multi-persona-orchestrator](../multi-persona-orchestrator/SKILL.md) — Parent orchestrator
- [persona-dfs](../persona-dfs/SKILL.md) — Complementary DFS approach
