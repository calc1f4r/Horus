---
name: "certora-sui-move-verification"
description: "Convert invariant specifications into Certora Sui Prover Move specs using the CVLM library. Handles installation, Sui CLI setup, Move.toml configuration, and platform summaries. Produces Move-based specification modules. Use when setting up Certora formal verification for Sui Move contracts."
---
Use the [certora-sui-move-verification subagent](../../../.codex/agents/certora-sui-move-verification.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `<path-to-sui-move-project>`.

Generate Certora CVLM specs for the Sui Move project at `<path-to-sui-move-project>`.

## What this produces

1. **CVLM spec modules** — Move modules with `#[spec]` annotations using the CVLM library
2. **Rules** — Verification rules using MathInt arithmetic
3. **Ghosts and shadows** — State tracking across function calls
4. **Parametric rules** — Rules that verify properties across all entry points
5. **Platform summaries** — Summaries for Sui framework functions
6. **Move.toml updates** — Dependency configuration for the CVLM library

## Output

- `spec/` package in the target project

For CVLM reference, see [certora-sui-move-reference.md](../../../.codex/resources/certora-sui-move-reference.md).
For templates, see [certora-sui-move-templates.md](../../../.codex/resources/certora-sui-move-templates.md).

## Related skills

- [certora-verification](../certora-verification/SKILL.md) — Certora for Solidity (CVL)
- [sui-prover-verification](../sui-prover-verification/SKILL.md) — Alternative Sui prover
- [invariant-writer](../invariant-writer/SKILL.md) — Produces invariant specs
