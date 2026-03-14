name: audit-context-building
description: "Build deep architectural context for a smart contract codebase before vulnerability hunting. Distributes per-contract analysis across sub-agents, then synthesizes a global context document. Use when preparing for a security audit, architecture review, threat modeling, or when bottom-up codebase comprehension is needed."
context: fork
agent: audit-context-building
argument-hint: <codebase-path>
---

Build deep architectural context for the codebase at `$ARGUMENTS`.

## What this does

1. **Scoping** — Identifies all in-scope contract files, their dependencies, and the protocol type
2. **Per-contract analysis** — Spawns one `function-analyzer` sub-agent per contract for line-by-line micro-analysis
3. **Synthesis** — Spawns `system-synthesizer` to produce a unified `01-context.md` with:
   - System-wide invariants and trust boundaries
   - Cross-contract data flows and call graphs
   - Actor models and privilege hierarchies
   - Storage layout and upgrade patterns

## Output

- `audit-output/context/*.md` — Per-contract analysis files
- `audit-output/01-context.md` — Global context document

## Related skills

- [/function-analyzer](../function-analyzer/SKILL.md) — Per-contract function analysis (spawned internally)
- [/system-synthesizer](../system-synthesizer/SKILL.md) — Global context synthesis (spawned internally)
- [/audit-orchestrator](../audit-orchestrator/SKILL.md) — Parent pipeline that invokes this skill
- [/invariant-writer](../invariant-writer/SKILL.md) — Consumes the context output
