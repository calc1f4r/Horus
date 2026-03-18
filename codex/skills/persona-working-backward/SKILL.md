name: persona-working-backward
description: "Working Backward auditing persona — traces from critical sinks to attacker-controllable sources. Optimized for speedrun/bug-bounty style hunting. Language-agnostic. Spawned by multi-persona-orchestrator."
context: fork
agent: persona-working-backward
user-invocable: false
argument-hint: <codebase-path>
---

<!-- AUTO-GENERATED from `.claude/skills/persona-working-backward/SKILL.md`; source_sha256=6fedbcda2a3b9ddcb9a9d4eb783380201f79f462798828c326bdbd8755c7e9e5 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/skills/persona-working-backward/SKILL.md`.
> The original skill metadata below is preserved verbatim.
> For Codex/GPT use, load `codex/agents/persona-working-backward.md` as the implementation playbook.
> Follow any linked `codex/resources/*` references from that agent file.
> Relative skill links remain mirrored under `codex/skills/*`.

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
