---
name: "function-analyzer"
description: "Per-contract ultra-granular function analysis. Performs line-by-line micro-analysis of every non-trivial function in a single contract file. Pure context building — no vulnerability identification. Spawned by audit-context-building."
---
Use the [function-analyzer subagent](../../../.codex/agents/function-analyzer.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `<contract-file-path>`.

Analyze every function in the contract at `<contract-file-path>`. For each non-trivial function, produce:

1. **Signature** — Full function signature with visibility and modifiers
2. **Purpose** — One-line description of what the function does
3. **State reads/writes** — Which storage slots are read and written
4. **External calls** — All cross-contract calls with target and selector
5. **Access control** — Guards, modifiers, role checks
6. **Math operations** — Arithmetic with precision/rounding analysis
7. **Edge cases** — Boundary conditions, zero inputs, max values

Write output to the designated per-contract file in `audit-output/context/`.

## Related skills

- [audit-context-building](../audit-context-building/SKILL.md) — Parent coordinator that spawns this
- [system-synthesizer](../system-synthesizer/SKILL.md) — Consumes the output of all function-analyzers
