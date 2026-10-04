---
name: "invariant-writer"
description: "Extract and document all system invariants, properties, and constraints from a smart contract codebase. Uses dual-mode analysis: 'What Should Happen' (positive specification from specs/standards) and 'What Must Never Happen' (adversarial multi-call attack sequences). Produces language-agnostic invariants consumed by fuzzing and formal verification tools. Use when preparing invariant suites, writing property specifications, or before fuzzing campaigns."
---
Use the [invariant-writer subagent](../../../.codex/agents/invariant-writer.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `<codebase-path>`.

Extract all invariants from the codebase at `<codebase-path>`.

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

- [invariant-reviewer](../invariant-reviewer/SKILL.md) — Reviews and hardens the output
- [audit-context-building](../audit-context-building/SKILL.md) — Produces the context this skill consumes
- [chimera-setup](../chimera-setup/SKILL.md) — Converts invariants to a multi-tool harness (Medusa + Echidna + Halmos). Preferred for new Solidity suites
- [medusa-fuzzing](../medusa-fuzzing/SKILL.md) — Converts invariants to Medusa-only harnesses
- [halmos-verification](../halmos-verification/SKILL.md) — Converts invariants to Halmos symbolic tests
- [certora-verification](../certora-verification/SKILL.md) — Converts invariants to CVL specs
