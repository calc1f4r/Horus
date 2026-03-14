name: missing-validation-reasoning
description: "Specialized reasoning-based auditor for input validation and hygiene vulnerabilities. Scans for zero-address checks, stale oracle data, array length mismatches, numeric bounds, arbitrary calldata forwarding, unvalidated token/callback addresses, and access control gaps. Use when reviewing constructors, initialize functions, admin setters, oracle integrations, or batch operations."
context: fork
agent: missing-validation-reasoning
argument-hint: <codebase-path>
---

Scan for missing input validation vulnerabilities in `$ARGUMENTS`.

## What this checks

| Category | Examples |
|----------|----------|
| Zero-address | Missing `address(0)` checks on token/receiver/admin params |
| Stale data | No freshness validation on oracle prices, no heartbeat checks |
| Array mismatches | `arrays.length != otherArrays.length` without require |
| Numeric bounds | Missing min/max checks, uncapped slippage, zero-amount |
| Arbitrary forwarding | Unvalidated calldata in `.call()`, delegate patterns |
| Token validation | Unvalidated token addresses in multi-token systems |
| Access control | Missing modifiers on state-changing functions, constructor gaps |

## Output

- `audit-output/04d-validation-findings.md`

## Related skills

- [/protocol-reasoning](../protocol-reasoning/SKILL.md) — Broader reasoning-based discovery
- [/invariant-catcher](../invariant-catcher/SKILL.md) — Pattern-based hunting
- [/audit-orchestrator](../audit-orchestrator/SKILL.md) — Parent pipeline (Phase 4D)
