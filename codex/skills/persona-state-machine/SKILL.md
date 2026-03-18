name: persona-state-machine
description: "State Machine auditing persona — maps all protocol states, transitions, and cross-contract interactions to find illegal state paths. Specializes in finding unique exploits through exhaustive state-transition analysis. Language-agnostic. Spawned by multi-persona-orchestrator."
context: fork
agent: persona-state-machine
user-invocable: false
argument-hint: <codebase-path>
---

<!-- AUTO-GENERATED from `.claude/skills/persona-state-machine/SKILL.md`; source_sha256=edc16483d37ea2198f8a375e096ad10c11a9e29d6d2d79b61b298ea33119ee42 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/skills/persona-state-machine/SKILL.md`.
> The original skill metadata below is preserved verbatim.
> For Codex/GPT use, load `codex/agents/persona-state-machine.md` as the implementation playbook.
> Follow any linked `codex/resources/*` references from that agent file.
> Relative skill links remain mirrored under `codex/skills/*`.

Perform State Machine audit on the codebase at `$ARGUMENTS`.

## Strategy

1. **Map states** — Identify all protocol states (stored in state variables, enums, booleans, phases)
2. **Map transitions** — For each state, identify which functions cause transitions and their conditions
3. **Build transition graph** — Draw the complete state machine
4. **Find illegal paths** — Look for:
   - Transitions that skip required intermediate states
   - States that should be unreachable but aren't
   - Circular transitions that drain value
   - Race conditions between transitions

## Output format

Write findings to the designated personas output file.

## Related skills

- [/multi-persona-orchestrator](../multi-persona-orchestrator/SKILL.md) — Parent orchestrator
- [/persona-working-backward](../persona-working-backward/SKILL.md) — Complementary backward tracing
