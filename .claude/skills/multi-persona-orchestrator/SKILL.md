name: multi-persona-orchestrator
description: "Multi-persona audit orchestrator that spawns 6 parallel auditing personas (BFS, DFS, Working Backward, State Machine, Mirror, Re-Implementation). Agents share findings between rounds, cross-verify, and converge on unified findings. Use when deep-reasoning audit coverage from multiple perspectives is needed."
context: fork
agent: multi-persona-orchestrator
argument-hint: <codebase-path>
---

Run multi-persona audit on `$ARGUMENTS`.

## Personas

| Persona | Strategy | Spawns |
|---------|----------|--------|
| **BFS** | Maps entry points, then progressively deepens | `persona-bfs` |
| **DFS** | Verifies leaf functions, then works upward | `persona-dfs` |
| **Working Backward** | Traces from critical sinks to attacker sources | `persona-working-backward` |
| **State Machine** | Maps all states/transitions, finds illegal paths | `persona-state-machine` |
| **Mirror** | Analyzes paired/opposite functions for asymmetries | `persona-mirror` |
| **Re-Implementation** | Hypothetically re-implements, then diffs | `persona-reimplementer` |

## Process

1. **Round 1** — All 6 personas analyze independently
2. **Knowledge sharing** — Findings aggregated into `shared-knowledge-round-N.md`
3. **Round 2+** — Personas cross-verify, build on each other's findings
4. **Convergence** — Unified findings document with cross-persona validation

## Output

- `audit-output/04c-persona-findings.md`
- `audit-output/personas/round-N/*.md` — Per-persona per-round findings

## Related skills

- [/persona-bfs](../persona-bfs/SKILL.md) — BFS persona (spawned internally)
- [/persona-dfs](../persona-dfs/SKILL.md) — DFS persona (spawned internally)
- [/persona-working-backward](../persona-working-backward/SKILL.md) — Working Backward persona
- [/persona-state-machine](../persona-state-machine/SKILL.md) — State Machine persona
- [/persona-mirror](../persona-mirror/SKILL.md) — Mirror persona
- [/persona-reimplementer](../persona-reimplementer/SKILL.md) — Re-Implementation persona
- [/audit-orchestrator](../audit-orchestrator/SKILL.md) — Parent pipeline (Phase 4C)
