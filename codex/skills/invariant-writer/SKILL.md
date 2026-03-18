name: invariant-writer
description: "Extract and document all system invariants, properties, and constraints from a smart contract codebase. Uses dual-mode analysis: 'What Should Happen' (positive specification from specs/standards) and 'What Must Never Happen' (adversarial multi-call attack sequences). Produces language-agnostic invariants consumed by fuzzing and formal verification tools. Use when preparing invariant suites, writing property specifications, or before fuzzing campaigns."
context: fork
agent: invariant-writer
argument-hint: <codebase-path>
---

<!-- AUTO-GENERATED from `.claude/skills/invariant-writer/SKILL.md`; source_sha256=07bc3b1df1f230ede846f4a01cf7b42a0d7bcf23108a15968ebbc12e95a8a6c3 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/skills/invariant-writer/SKILL.md`.
> The original skill metadata below is preserved verbatim.
> For Codex/GPT use, load `codex/agents/invariant-writer.md` as the implementation playbook.
> Follow any linked `codex/resources/*` references from that agent file.
> Relative skill links remain mirrored under `codex/skills/*`.

Extract all invariants from the codebase at `$ARGUMENTS`.

## What this does

Runs two complementary analysis passes:

### Pass 1: "What Should Happen"
- Reads specs, standards, docs, reference implementations
- Extracts positive properties: conservation laws, ordering guarantees, access control rules

### Pass 2: "What Must Never Happen"
- Adversarial, fear-driven analysis
- Multi-call attack sequences, flash loan scenarios, reentrancy paths
- Identifies properties that, if broken, indicate a vulnerability

## Output

- `audit-output/02-invariants.md` — Structured invariant specification

Each invariant includes: ID, category, property statement, boundary conditions, attack vectors it guards against, and whether it's suitable for fuzzing vs formal verification.

## Related skills

- [/invariant-reviewer](../invariant-reviewer/SKILL.md) — Reviews and hardens the output
- [/audit-context-building](../audit-context-building/SKILL.md) — Produces the context this skill consumes
- [/chimera-setup](../chimera-setup/SKILL.md) — Converts invariants to a multi-tool harness (Medusa + Echidna + Halmos). Preferred for new Solidity suites
- [/medusa-fuzzing](../medusa-fuzzing/SKILL.md) — Converts invariants to Medusa-only harnesses
- [/halmos-verification](../halmos-verification/SKILL.md) — Converts invariants to Halmos symbolic tests
- [/certora-verification](../certora-verification/SKILL.md) — Converts invariants to CVL specs
