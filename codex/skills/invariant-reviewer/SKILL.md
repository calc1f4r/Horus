name: invariant-reviewer
description: "Review and harden invariant specifications produced by invariant-writer. Re-understands the protocol, researches canonical invariants for the protocol type, enforces multi-step attack vector coverage, calibrates bounds, and produces a revised invariant file ready for formal verification. Use after invariant-writer or when invariant quality is suspect."
context: fork
agent: invariant-reviewer
argument-hint: <path-to-invariants-file>
---

<!-- AUTO-GENERATED from `.claude/skills/invariant-reviewer/SKILL.md`; source_sha256=3c96a8eeedc3fa4700d32946e4ebf9f6627a828a55758cfcfd78a3479301e749 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/skills/invariant-reviewer/SKILL.md`.
> The original skill metadata below is preserved verbatim.
> For Codex/GPT use, load `codex/agents/invariant-reviewer.md` as the implementation playbook.
> Follow any linked `codex/resources/*` references from that agent file.
> Relative skill links remain mirrored under `codex/skills/*`.

Review and harden the invariant specification at `$ARGUMENTS`.

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

- [/invariant-writer](../invariant-writer/SKILL.md) — Produces the invariants this skill reviews
- [/medusa-fuzzing](../medusa-fuzzing/SKILL.md) — Consumes reviewed invariants
- [/halmos-verification](../halmos-verification/SKILL.md) — Consumes reviewed invariants
- [/certora-verification](../certora-verification/SKILL.md) — Consumes reviewed invariants
- [/invariant-indexer](../invariant-indexer/SKILL.md) — Provides canonical invariant references
