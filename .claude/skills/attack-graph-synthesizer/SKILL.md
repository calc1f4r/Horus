---
name: attack-graph-synthesizer
description: Systematically searches for multi-step and cross-contract attack chains by walking the codebase knowledge graph against the invariant suite. Produces attack-candidates.json for protocol-reasoning to validate.
argument-hint: "[audit-output-dir]"
user-invocable: false
context: fork
agent: attack-graph-synthesizer
---

# Attack-Graph Synthesizer Skill

Invokes the `attack-graph-synthesizer` agent.

## Task

$ARGUMENTS

## Requirements

- `audit-output/graph/graph.json` must exist (Phase 0 of audit-orchestrator must have completed)
- `audit-output/02-invariants-reviewed.md` must exist (Phase 3 must have completed)
- `audit-output/00-scope.md` must exist (Phase 1 must have completed)

## Outputs

- `audit-output/attack-candidates.json`
- `audit-output/attack-candidates.md`
- `audit-output/attack-proofs/atk-NNN.md` (one per candidate)
