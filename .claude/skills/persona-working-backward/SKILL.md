---
name: persona-working-backward
description: "Working Backward auditing persona — traces from critical sinks to attacker-controllable sources. Optimized for speedrun/bug-bounty style hunting. Language-agnostic. Spawned by multi-persona-orchestrator."
context: fork
agent: persona-working-backward
user-invocable: false
argument-hint: <codebase-path>
---

Perform Working Backward audit on the codebase at `$ARGUMENTS`.

## Strategy

1. **Identify critical sinks** — `transfer`, `selfdestruct`, `delegatecall`, storage writes to balances/ownership
2. **Trace backward** — For each sink, follow the data flow backward to its sources
3. **Find attacker control** — Identify which sources are attacker-controllable (function params, `msg.sender`, `msg.value`)
4. **Verify path** — Check if any guards along the path can be bypassed

## Output format

Write findings to the designated personas output file.

## Related skills

- [/multi-persona-orchestrator](../multi-persona-orchestrator/SKILL.md) — Parent orchestrator
- [/persona-state-machine](../persona-state-machine/SKILL.md) — Complementary state analysis
