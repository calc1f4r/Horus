---
name: system-synthesizer
description: "Synthesizes per-contract analysis files into a global context document with system-wide invariants, cross-contract flows, trust boundaries, and actor models. Spawned by audit-context-building after all function-analyzers complete."
context: fork
agent: system-synthesizer
user-invocable: false
---

Read all per-contract context files from `audit-output/context/` and synthesize a compact `01-context.md` containing:

1. **System architecture** — How contracts interact, inheritance hierarchy
2. **Cross-contract data flows** — Token flows, callback patterns, delegate calls
3. **Trust boundaries** — Which contracts trust which, admin vs user paths
4. **Actor model** — All roles (admin, user, keeper, liquidator, etc.) and their capabilities
5. **System-wide invariants** — Properties that must hold across all contracts
6. **Attack surface** — External entry points ranked by risk

## Related skills

- [/audit-context-building](../audit-context-building/SKILL.md) — Parent coordinator that spawns this
- [/function-analyzer](../function-analyzer/SKILL.md) — Produces the per-contract files this skill reads
- [/invariant-writer](../invariant-writer/SKILL.md) — Consumes the synthesized context
