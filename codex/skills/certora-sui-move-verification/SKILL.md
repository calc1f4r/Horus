name: certora-sui-move-verification
description: "Convert invariant specifications into Certora Sui Prover Move specs using the CVLM library. Handles installation, Sui CLI setup, Move.toml configuration, and platform summaries. Produces Move-based specification modules. Use when setting up Certora formal verification for Sui Move contracts."
context: fork
agent: certora-sui-move-verification
argument-hint: <path-to-sui-move-project>
---

<!-- AUTO-GENERATED from `.claude/skills/certora-sui-move-verification/SKILL.md`; source_sha256=9dab240465dd31cf0a90bbf38b28ee701d7c8e85d8907700347344b5ddd4d52f -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/skills/certora-sui-move-verification/SKILL.md`.
> The original skill metadata below is preserved verbatim.
> For Codex/GPT use, load `codex/agents/certora-sui-move-verification.md` as the implementation playbook.
> Follow any linked `codex/resources/*` references from that agent file.
> Relative skill links remain mirrored under `codex/skills/*`.

Generate Certora CVLM specs for the Sui Move project at `$ARGUMENTS`.

## What this produces

1. **CVLM spec modules** — Move modules with `#[spec]` annotations using the CVLM library
2. **Rules** — Verification rules using MathInt arithmetic
3. **Ghosts and shadows** — State tracking across function calls
4. **Parametric rules** — Rules that verify properties across all entry points
5. **Platform summaries** — Summaries for Sui framework functions
6. **Move.toml updates** — Dependency configuration for the CVLM library

## Output

- `spec/` package in the target project

For CVLM reference, see [certora-sui-move-reference.md](../../resources/certora-sui-move-reference.md).
For templates, see [certora-sui-move-templates.md](../../resources/certora-sui-move-templates.md).

## Related skills

- [/certora-verification](../certora-verification/SKILL.md) — Certora for Solidity (CVL)
- [/sui-prover-verification](../sui-prover-verification/SKILL.md) — Alternative Sui prover
- [/invariant-writer](../invariant-writer/SKILL.md) — Produces invariant specs
