name: persona-mirror
description: "Mirror auditing persona — analyzes paired/opposite functions for asymmetries (deposit/withdraw, mint/burn, stake/unstake, lock/unlock). Language-agnostic. Spawned by multi-persona-orchestrator."
context: fork
agent: persona-mirror
user-invocable: false
argument-hint: <codebase-path>
---

<!-- AUTO-GENERATED from `.claude/skills/persona-mirror/SKILL.md`; source_sha256=7cda8ed1bde5a2de8cef89250b1b8401718dd9a9b615f54002c46bbe790bed08 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/skills/persona-mirror/SKILL.md`.
> The original skill metadata below is preserved verbatim.
> For Codex/GPT use, load `codex/agents/persona-mirror.md` as the implementation playbook.
> Follow any linked `codex/resources/*` references from that agent file.
> Relative skill links remain mirrored under `codex/skills/*`.

Perform Mirror audit on the codebase at `$ARGUMENTS`.

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

- [/multi-persona-orchestrator](../multi-persona-orchestrator/SKILL.md) — Parent orchestrator
- [/persona-reimplementer](../persona-reimplementer/SKILL.md) — Complementary re-implementation approach
