---
name: "invariant-reviewer"
description: "Review and harden invariant specifications produced by invariant-writer. Re-understands the protocol, researches canonical invariants for the protocol type, enforces multi-step attack vector coverage, calibrates bounds, and produces a revised invariant file ready for formal verification. Use after invariant-writer or when invariant quality is suspect."
---
Use the [invariant-reviewer subagent](../../../.codex/agents/invariant-reviewer.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `<path-to-invariants-file>`.

Review and harden the invariant specification at `<path-to-invariants-file>`.

## What this does

1. **Re-understanding** — Reads the protocol independently (does not trust the writer's framing)
2. **Canonical research** — Looks up known invariants for this protocol type from `invariants/` reference files
3. **Gap analysis** — Checks for missing invariant categories: conservation, ordering, access control, timing, cross-contract
4. **Multi-step coverage** — Ensures invariants cover 2-step and 3-step attack sequences, not just single-call
5. **Bound calibration** — Tightens or loosens numerical bounds to avoid over/under-specification
6. **FV readiness** — Reformulates invariants for formal verification tool consumption

## Output

- `audit-output/02-invariants-reviewed.md` — Hardened invariant specification

## Related skills

- [invariant-writer](../invariant-writer/SKILL.md) — Produces the invariants this skill reviews
- [medusa-fuzzing](../medusa-fuzzing/SKILL.md) — Consumes reviewed invariants
- [halmos-verification](../halmos-verification/SKILL.md) — Consumes reviewed invariants
- [certora-verification](../certora-verification/SKILL.md) — Consumes reviewed invariants
- [invariant-indexer](../invariant-indexer/SKILL.md) — Provides canonical invariant references
