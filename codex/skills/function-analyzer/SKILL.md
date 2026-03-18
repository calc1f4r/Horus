name: function-analyzer
description: "Per-contract ultra-granular function analysis. Performs line-by-line micro-analysis of every non-trivial function in a single contract file. Pure context building — no vulnerability identification. Spawned by audit-context-building."
context: fork
agent: function-analyzer
user-invocable: false
argument-hint: <contract-file-path>
---

<!-- AUTO-GENERATED from `.claude/skills/function-analyzer/SKILL.md`; source_sha256=0aee6b6614b7f697ddb6997af7daeafbfa117349aa08b542895a7529ab6047f2 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/skills/function-analyzer/SKILL.md`.
> The original skill metadata below is preserved verbatim.
> For Codex/GPT use, load `codex/agents/function-analyzer.md` as the implementation playbook.
> Follow any linked `codex/resources/*` references from that agent file.
> Relative skill links remain mirrored under `codex/skills/*`.

Analyze every function in the contract at `$ARGUMENTS`. For each non-trivial function, produce:

1. **Signature** — Full function signature with visibility and modifiers
2. **Purpose** — One-line description of what the function does
3. **State reads/writes** — Which storage slots are read and written
4. **External calls** — All cross-contract calls with target and selector
5. **Access control** — Guards, modifiers, role checks
6. **Math operations** — Arithmetic with precision/rounding analysis
7. **Edge cases** — Boundary conditions, zero inputs, max values

Write output to the designated per-contract file in `audit-output/context/`.

## Related skills

- [/audit-context-building](../audit-context-building/SKILL.md) — Parent coordinator that spawns this
- [/system-synthesizer](../system-synthesizer/SKILL.md) — Consumes the output of all function-analyzers
