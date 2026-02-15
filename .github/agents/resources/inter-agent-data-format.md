# Inter-Agent Data Format

> **Purpose**: Defines the standardized data contracts between pipeline phases so the `audit-orchestrator` can reliably pass data between specialized sub-agents.
> **Audience**: All agents in the audit pipeline — producers write in this format, consumers parse it.

---

## Output Directory Structure

All pipeline artifacts go into `audit-output/` at the project root:

```
audit-output/
├── 00-scope.md              ← Phase 1: Reconnaissance
├── 01-context.md            ← Phase 2: Context building
├── 02-invariants.md         ← Phase 3: Invariant extraction This should be a folder as there are many invariants, e.g. `02-invariants/INV-001.md`, `02-invariants/INV-002.md`, etc. 
├── 03-findings-raw.md       ← Phase 4: DB-powered hunting
├── 04a-reasoning-findings.md ← Phase 4a: Reasoning-based discovery
├── 04-validation-findings.md ← Phase 5: Validation gap analysis
├── 05-findings-triaged.md   ← Phase 6: Triage & deduplication
├── 06-sherlock-validation.md ← Phase 7: Sherlock judging
├── 07-cantina-validation.md ← Phase 7: Cantina judging
├── AUDIT-REPORT.md          ← Final assembled report
├── pocs/                    ← PoC exploit tests
│   ├── F-001-poc.t.sol
│   └── ...
├── fuzzing/                 ← Medusa harnesses
│   ├── medusa.json
│   └── ...
└── certora/                 ← Certora specs
    ├── spec.conf
    └── ...
```

---

## Phase 1: Scope Document (`00-scope.md`)

```markdown
# Audit Scope

## Protocol Classification
- **Detected types**: [lending_protocol, vault_yield]
- **User hint**: lending (if provided)
- **Confidence**: HIGH | MEDIUM | LOW

## Codebase Summary
- **Language**: Solidity | Rust | Go | Move
- **Framework**: Foundry | Hardhat | Anchor | Cosmos SDK
- **Total files**: N
- **Total LOC**: N (estimated)

## Files In Scope
| File | LOC | Description |
|------|-----|-------------|
| src/Pool.sol | 450 | Main lending pool |
| ... | ... | ... |

## Resolved Manifests
| Manifest | Reason |
|----------|--------|
| oracle | Protocol uses Chainlink for price feeds |
| general-defi | Lending/borrowing math, flash loans |
| tokens | ERC20 token interactions |
| general-security | Access control, input validation |
| unique | Protocol-specific patterns |

## Focus Patterns (from protocolContext)
- staleness, price manipulation, liquidation, flash loan, ...
```

---

## Phase 2: Context Output (`01-context.md`)

Produced by `audit-context-building`. Must contain these sections:

```markdown
# Audit Context

## Contract Inventory
| Contract | Purpose | LOC | Entry Points | State Variables |
|----------|---------|-----|--------------|-----------------|
| Pool.sol | Main lending pool | 450 | 12 | 8 |
| ... | ... | ... | ... | ... |

## Actor Model
| Actor | Trust Level | Can Call | Notes |
|-------|------------|---------|-------|
| User (EOA) | Untrusted | deposit, withdraw, borrow | Any EOA |
| Admin | Trusted | setFee, pause | Multi-sig |
| Oracle | Semi-trusted | updatePrice | Chainlink |
| Liquidator | Untrusted | liquidate | Any EOA |

## State Variable Map
| Variable | Type | Writers | Readers | Invariants |
|----------|------|---------|---------|------------|
| totalDeposits | uint256 | deposit, withdraw | borrow, getRate | >= sum of user balances |
| ... | ... | ... | ... | ... |

## Function Analysis
### Contract.functionName()
- **Purpose**: ...
- **Inputs & Assumptions**: ...
- **Outputs & Effects**: ...
- **Block-by-Block Analysis**: ...
- **Cross-Function Dependencies**: ...
- **Invariants Identified**: ...
(repeat for every non-trivial function)

## Cross-Function Flows
### Flow: Deposit → Borrow → Repay → Withdraw
1. deposit() → updates totalDeposits, mints shares
2. borrow() → checks collateral via oracle, transfers tokens
...

## Trust Boundaries
| Boundary | From | To | Risk |
|----------|------|----|------|
| User → Pool | Untrusted input | State changes | Input validation required |
| Pool → Oracle | Contract call | Price data | Staleness, manipulation |

## Invariant Candidates
1. `totalDeposits >= totalBorrowed` (solvency)
2. `sharePrice * totalShares == totalAssets` (accounting)
...

## Assumption Register
1. Oracle returns prices within 1 hour freshness
2. Admin multi-sig has 3/5 threshold
...
```

---

## Phase 3: Invariant Spec (`02-invariants.md`)

Produced by `invariant-writer`. Must use this category structure:

```markdown
# Invariant Specifications

## Solvency Invariants
### INV-S-001: Total deposits cover total borrows
- **Property**: `totalDeposits >= totalBorrowed`
- **Scope**: Pool.sol
- **Why**: If violated, protocol is insolvent
- **Testable**: YES — check after every deposit/withdraw/borrow/repay

## Access Control Invariants
### INV-AC-001: Only admin can pause
- **Property**: `pause() reverts if msg.sender != admin`
- **Scope**: Pool.sol
- **Why**: Unauthorized pause = DoS

## State Machine Invariants
### INV-SM-001: Cannot borrow when paused
- **Property**: `paused == true → borrow() reverts`
- **Scope**: Pool.sol

## Arithmetic Invariants
### INV-A-001: Share price monotonically increases (absent losses)
- **Property**: `sharePriceAfter >= sharePriceBefore` for deposits
- **Scope**: Pool.sol, ShareMath.sol

## Oracle Invariants
### INV-O-001: Price feed freshness
- **Property**: `block.timestamp - updatedAt < STALENESS_THRESHOLD`
- **Scope**: OracleAdapter.sol

## Cross-Contract Invariants
### INV-CC-001: Token balance matches accounting
- **Property**: `token.balanceOf(pool) >= totalDeposits - totalBorrowed`
- **Scope**: Pool.sol + ERC20 token
```

Each invariant MUST have: ID, Property (concrete expression), Scope (files), Why (impact if broken), Testable (YES/NO).

---

## Phase 4a: Reasoning Findings (`04a-reasoning-findings.md`)

Produced by `protocol-reasoning-agent`. Extends the standard Finding Schema with reasoning-specific fields.

```markdown
# Reasoning-Based Findings (Phase 4a)

## Summary
| Severity | Count |
|----------|-------|
| CRITICAL | N |
| HIGH | N |
| MEDIUM | N |
| **Total** | **N** |

## Domain Map
### Domain: [Name]
- **Files**: [contract1.sol, contract2.sol]
- **Functions**: [function list]
- **Key State**: [state variables]
- **Interfaces**: [cross-domain connections]

## Reasoning Seed Catalog (Summary)
### Input Seeds: N seeds applied
### State Seeds: N seeds applied
### Ordering Seeds: N seeds applied
### Economic Seeds: N seeds applied
### Environmental Seeds: N seeds applied

## Findings
(Each finding uses the extended Finding Schema below)
```

### Extended Finding Schema for Phase 4a

Phase 4a findings use the standard Finding Schema (below) PLUS these additional fields:

```markdown
| **Reasoning Type** | standard / cross-domain / edge-case / completeness |
| **Round Discovered** | 1 / 2 / 3 / 4 |
| **Assumption Violated** | Layer N — [Input/State/Ordering/Economic/Environmental] |
| **DB Seed Reference** | SEED-X-NNN (generalized from <pattern-id>) or "Novel — no seed" |

#### Reachability Proof
Step 1: [Actor] calls [function(args)] → state S_0 transitions to S_1
  WHY: [function is externally callable, args are controllable]
Step 2: [Actor] calls [function(args)] → S_1 transitions to S_2
  WHY: [precondition met because of S_1]
...
Step N: State is now S_vulnerable
  VERIFICATION: S_vulnerable violates [invariant/assumption]
  IMPACT: [concrete quantified damage]
```

---

## Finding Schema (Phases 3-6)

Every finding across all phases MUST use this format:

```markdown
### F-NNN: [Title]

| Field | Value |
|-------|-------|
| **ID** | F-NNN |
| **Severity** | CRITICAL / HIGH / MEDIUM / LOW |
| **Confidence** | HIGH / MEDIUM / LOW |
| **Root Cause** | [One sentence: "This vulnerability exists because..."] |
| **Impact** | [Concrete impact: "$X stolen", "DoS for Y blocks", "Z% loss"] |
| **Affected Code** | `src/Pool.sol` L123-L145 |
| **DB Pattern Ref** | `oracle-staleness-001` from `DB/manifests/oracle.json` → `DB/oracle/pyth/PYTH_ORACLE_VULNERABILITIES.md` L93-L248 (or "Novel — no DB match") |
| **Attack Scenario** | Step-by-step exploit path |

#### Vulnerable Code
```solidity
// src/Pool.sol L123-L145
function getPrice() external view returns (uint256) {
    (, int256 price,,,) = priceFeed.latestRoundData();
    return uint256(price); // ❌ No staleness check
}
```

#### Recommended Fix
```solidity
function getPrice() external view returns (uint256) {
    (, int256 price,, uint256 updatedAt,) = priceFeed.latestRoundData();
    require(block.timestamp - updatedAt < STALENESS_THRESHOLD, "Stale price");
    require(price > 0, "Invalid price");
    return uint256(price); // ✅ Validated
}
```

#### PoC Reference
See `audit-output/pocs/F-001-poc.t.sol` (if generated)
```

---

## Triage Output (`05-findings-triaged.md`)

```markdown
# Triaged Findings

## Summary
| Severity | Count |
|----------|-------|
| CRITICAL | N |
| HIGH | N |
| MEDIUM | N |
| LOW | N |
| **Total** | **N** |

## Deduplicated Findings
(Each finding in the Finding Schema above, ordered by severity)

## Excluded Findings
### EX-001: [Title]
- **Original ID**: F-NNN
- **Reason for exclusion**: Failed falsification — [specific reason]
```

---

## Severity Validation Output (Phases 7)

### Sherlock Validation (`06-sherlock-validation.md`)

```markdown
# Sherlock Severity Validation

| Finding | Agent Severity | Sherlock Severity | Rationale |
|---------|---------------|-------------------|-----------|
| F-001 | HIGH | HIGH | Definite loss of funds > $10K |
| F-002 | MEDIUM | INVALID | Requires admin action (trusted role) |
| ... | ... | ... | ... |
```

### Cantina Validation (`07-cantina-validation.md`)

```markdown
# Cantina Severity Validation

| Finding | Agent Severity | Cantina Severity | Impact | Likelihood | Rationale |
|---------|---------------|------------------|--------|------------|-----------|
| F-001 | HIGH | HIGH | High | High | Direct fund theft possible |
| F-002 | MEDIUM | LOW | Medium | Low | Requires specific market conditions |
| ... | ... | ... | ... | ... | ... |
```

---

## Cross-Phase Data Flow Summary

```
Phase 1 (Scope) ──→ protocolTypes, manifestList, filesInScope
                       │
Phase 2 (Context) ←───┘ reads filesInScope
         │──→ architecture, functions, invariantCandidates, assumptions
         │
Phase 3 (Invariants) ←── reads invariantCandidates
         │──→ structured invariant specs (INV-*)
         │
Phase 4 (Hunting) ←── reads manifestList + invariant specs
         │──→ raw findings (F-NNN)
         │
Phase 4a (Reasoning) ←── reads context + invariants + raw findings + manifests
         │──→ reasoning findings (F-4a-NNN) with reachability proofs
         │
Phase 5 (Validation) ←── reads filesInScope + context
         │──→ additional findings (F-NNN)
         │
Phase 6 (Triage) ←── reads all findings (03 + 04a + 04)
         │──→ deduplicated, scored findings + PoCs
         │
Phase 7 (Downstream) ←── reads invariant specs + triaged findings
         ├──→ Medusa harnesses
         ├──→ Certora specs
         ├──→ Sherlock validation
         └──→ Cantina validation
         
Final (Report) ←── reads ALL outputs
         └──→ AUDIT-REPORT.md
```
