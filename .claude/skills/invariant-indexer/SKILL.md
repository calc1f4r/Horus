name: invariant-indexer
description: "Index canonical invariants from major DeFi protocol repositories, formal verification specs, fuzzing harnesses, and documented properties. Writes structured reference files into invariants/<category>/. Use when building protocol-level invariant reference libraries, studying how top protocols specify formal properties, or bootstrapping invariant suites."
context: fork
agent: invariant-indexer
argument-hint: <protocol-name-or-github-url>
---

Index invariants from `$ARGUMENTS`.

## What this does

1. **Source discovery** — Finds formal specs, fuzzing harnesses, property tests, and documented invariants in the target repository
2. **Extraction** — Pulls out each invariant with its category, property statement, and source reference
3. **Classification** — Tags invariants by type: conservation, ordering, access control, timing, liveness, safety
4. **Deduplication** — Merges equivalent invariants across sources
5. **Output** — Writes structured reference files to `invariants/<category>/`

## Sources it searches

- Certora CVL specs (`*.spec`)
- Echidna/Medusa harnesses (`property_*`, `invariant_*`)
- Halmos symbolic tests (`check_*`)
- Foundry invariant tests
- Scribble annotations
- Documented properties in READMEs and audits

## Related skills

- [/invariant-writer](../invariant-writer/SKILL.md) — Consumes indexed invariants as seed context
- [/invariant-reviewer](../invariant-reviewer/SKILL.md) — Uses indexed invariants for gap analysis
- [/medusa-fuzzing](../medusa-fuzzing/SKILL.md) — Targets protocols whose invariants were indexed
