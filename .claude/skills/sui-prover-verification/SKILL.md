---
name: sui-prover-verification
description: "Convert invariant specifications into Sui Prover formal verification specs for Sui Move contracts. Uses the Asymptotic Sui Prover via requires/ensures/asserts specification style. Produces Move specification modules with ghost variables, loop invariants, and Integer/Real math. Use when setting up Sui Prover for Sui Move verification."
context: fork
agent: sui-prover-verification
argument-hint: <path-to-sui-move-project>
---

Generate Sui Prover specs for the Sui Move project at `$ARGUMENTS`.

## What this produces

1. **Spec modules** — Move modules with `#[spec(prove)]` functions
2. **Ghost variables** — `#[spec(global)]` ghost state for tracking
3. **Pre/post conditions** — `requires` and `ensures` annotations
4. **Loop invariants** — `#[spec(loop_invariant)]` for loop verification
5. **Datatype invariants** — Structural properties on Move objects
6. **Integer/Real math** — Precise arithmetic using `Integer` and `Real` types

## Output

- `spec/` package in the target project

For Sui Prover reference, see [sui-prover-reference.md](../../resources/sui-prover-reference.md).

## Related skills

- [/certora-sui-move-verification](../certora-sui-move-verification/SKILL.md) — Alternative: Certora CVLM
- [/invariant-writer](../invariant-writer/SKILL.md) — Produces invariant specs
