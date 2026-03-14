---
name: persona-dfs
description: "DFS auditing persona — verifies leaf functions then works upward. Language-agnostic. Applies Feynman questioning at every stack depth. Spawned by multi-persona-orchestrator."
context: fork
agent: persona-dfs
user-invocable: false
---

Perform Depth-First Search audit on the target codebase.

## Strategy

1. **Identify leaf functions** — Functions that make no further internal calls
2. **Verify leaves** — Check each leaf for correctness, edge cases, overflow
3. **Work upward** — Verify callers of verified leaves, checking composition safety
4. **Reach entry points** — Confirm the full stack is sound or find where it breaks

At each stack depth, apply Feynman questioning:
- "If the callee is correct, can the caller still misuse the return value?"
- "Does the caller check all error conditions from the callee?"

## Output format

Write findings to the designated personas output file.

## Related skills

- [/multi-persona-orchestrator](../multi-persona-orchestrator/SKILL.md) — Parent orchestrator
- [/persona-bfs](../persona-bfs/SKILL.md) — Complementary BFS approach
