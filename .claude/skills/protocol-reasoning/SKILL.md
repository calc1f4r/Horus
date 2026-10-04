---
name: protocol-reasoning
description: "Deep reasoning-based vulnerability discovery. Decomposes codebases into domains, spawns specialized sub-agents per domain, and uses DB vulnerability root causes as reasoning seeds. Iterates 4 rounds: standard → cross-domain → edge cases → completeness. Requires reachability proofs. Focuses on MEDIUM/HIGH/CRITICAL severity. Use for reasoning-first vulnerability discovery beyond pattern matching."
context: fork
agent: protocol-reasoning
argument-hint: <codebase-path>
---

Perform deep reasoning-based vulnerability discovery on `$ARGUMENTS`.

## What this does

Unlike pattern-matching (`invariant-catcher`), this skill reasons from first principles about how the protocol can be broken.

### Round 1: Standard analysis
- Decomposes the codebase into domains (e.g., lending, oracle, liquidation)
- Spawns one sub-agent per domain with relevant DB root causes as reasoning seeds

### Round 2: Cross-domain
- Looks for vulnerabilities that span multiple domains (e.g., oracle + liquidation)

### Round 3: Edge cases
- Explores boundary conditions, overflow/underflow, rounding, empty states

### Round 4: Completeness
- Reviews coverage gaps, checks for missed attack vectors

Every finding requires a **reachability proof** — a concrete call chain from a public function to the vulnerable code.

## Output

- `audit-output/04a-reasoning-findings.md`

## Related skills

- [/invariant-catcher](../invariant-catcher/SKILL.md) — Complementary pattern-based hunting
- [/multi-persona-orchestrator](../multi-persona-orchestrator/SKILL.md) — Complementary persona-based hunting
- [/missing-validation-reasoning](../missing-validation-reasoning/SKILL.md) — Complementary input validation scanning
- [/audit-orchestrator](../audit-orchestrator/SKILL.md) — Parent pipeline (Phase 4B)
