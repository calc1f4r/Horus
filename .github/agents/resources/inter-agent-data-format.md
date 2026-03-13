# Inter-Agent Data Format

> **Purpose**: Defines the standardized data contracts between pipeline phases so the `audit-orchestrator` can reliably pass data between specialized sub-agents.
> **Audience**: All agents in the audit pipeline — producers write in this format, consumers parse it.

---

## Output Directory Structure

All pipeline artifacts go into `audit-output/` at the project root:

```
audit-output/
├── 00-scope.md                        ← Phase 1: Reconnaissance
├── context/                           ← Phase 2: Per-contract context (sharded)
│   ├── 00-orientation.md              ←   System map & contract inventory
│   ├── Pool.md                        ←   Per-contract function analysis
│   ├── OracleAdapter.md               ←   Per-contract function analysis
│   ├── ShareMath.md                   ←   Per-contract function analysis
│   └── ...                            ←   One file per contract
├── 01-context.md                      ← Phase 2: Compact global synthesis
├── 02-invariants.md                   ← Phase 3: Invariant extraction
├── 02-invariants-reviewed.md          ← Phase 3a: Reviewed & hardened invariants
├── hunt-card-hits.json                ← Phase 4: Grep-prune results
├── hunt-card-shards.json              ← Phase 4: Partition plan
├── 03-findings-shard-*.md             ← Phase 4: Per-shard findings (temporary)
├── 03-findings-raw.md                 ← Phase 4: Merged findings (final)
├── 03-merge-log.md                    ← Phase 4: Shard merge deduplication log
├── 04a-reasoning-findings.md          ← Phase 4a: Reasoning-based discovery
├── 04-validation-findings.md          ← Phase 5: Validation gap analysis
├── 05-findings-triaged.md             ← Phase 6: Triage & deduplication
├── 06-sherlock-validation.md          ← Phase 7: Sherlock judging
├── 07-cantina-validation.md           ← Phase 7: Cantina judging
├── AUDIT-REPORT.md                    ← Final assembled report
├── pocs/                              ← PoC exploit tests
│   ├── F-001-poc.{ext}
│   └── ...
├── fuzzing/                           ← Medusa harnesses
│   ├── medusa.json
│   └── ...
└── certora/                           ← Certora specs
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
- **Language**: (detected from codebase — e.g., Solidity, Rust, Go, Move, Cairo, Vyper)
- **Framework**: (detected from config files — e.g., Foundry, Hardhat, Anchor, Cosmos SDK, Scarb)
- **Total files**: N
- **Total LOC**: N (estimated)

## Files In Scope
| File | LOC | Description |
|------|-----|-------------|
| src/Pool.ext | 450 | Main lending pool |
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

## Phase 2: Context Output

Produced by `audit-context-building` coordinator using a 3-step pipeline:

### Step 1: Orientation (`context/00-orientation.md`)

Written by the coordinator itself. Compact system map:

```markdown
# Orientation: <Protocol Name>

## Contracts in Scope
| # | Contract | File Path | LOC | Role | Key Entry Points |
|---|----------|-----------|-----|------|------------------|

## Preliminary Actor Model
| Actor | Trust Level | Entry Points | Notes |
|-------|------------|--------------|-------|

## Key State Variables
| Variable | Contract | Type | Role |
|----------|----------|------|------|

## Contract Dependency Map
- Pool → OracleAdapter (price queries)
- ...

## Analysis Order
1. ShareMath (utility, no dependencies)
2. ...
```

### Step 2: Per-Contract Analysis (`context/<ContractName>.md`)

Written by `function-analyzer` sub-agents (one per contract):

```markdown
# Context Analysis: <ContractName>

## Contract Overview
- **File**: <path>
- **LOC**: <count>
- **Entry Points**: <count>
- **State Variables**: <count>

## State Variable Map
| Variable | Type | Visibility | Writers | Readers | Invariants |
|----------|------|------------|---------|---------|------------|

## Function Analysis

### <functionName>(<params>)
#### Purpose
...
#### Inputs & Assumptions
...
#### Outputs & Effects
...
#### Block-by-Block Analysis
...
#### Cross-Function Dependencies
...
#### Invariants
...

(repeat for every non-trivial function)

## Contract-Level Invariant Candidates
1. ...

## Contract-Level Assumptions
1. ...

## Open Questions
- ...
```

### Step 3: Global Synthesis (`01-context.md`)

Written by `system-synthesizer` sub-agent. Compact summary referencing per-contract files:

```markdown
# Audit Context

## Contract Inventory
| Contract | Purpose | LOC | Entry Points | State Variables |
|----------|---------|-----|--------------|-----------------|

## Actor Model
| Actor | Trust Level | Can Call | Notes |
|-------|------------|---------|-------|

## State Variable Map
| Variable | Contract | Type | Writers | Readers | Invariants |
|----------|----------|------|---------|---------|------------|

## Function Analysis
> Per-contract analysis files in `audit-output/context/`:
> - `Pool.md` — Core lending pool (12 functions)
> - `OracleAdapter.md` — Price feed adapter (5 functions)
> - ...

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
1. INV-S-001: `totalDeposits >= totalBorrowed` (solvency)
2. INV-A-001: `sharePrice * totalShares == totalAssets` (accounting)
...

## Assumption Register
1. ASM-001: Oracle returns prices within 1 hour freshness
2. ASM-002: Admin multi-sig has 3/5 threshold
...

## Fragility Clusters
| Cluster | Contracts | Functions | Risk Factors |
|---------|-----------|-----------|--------------|
```

> **Note**: The Function Analysis section in `01-context.md` references per-contract files rather than duplicating block-by-block analysis. Downstream agents needing function-level detail should read the individual `context/<ContractName>.md` files.

---

## Phase 3: Invariant Spec (`02-invariants.md`)

Produced by `invariant-writer`. Must use this category structure:

```markdown
# Invariant Specifications

## Solvency Invariants
### INV-S-001: Total deposits cover total borrows
- **Property**: `totalDeposits >= totalBorrowed`
- **Scope**: Pool module/contract
- **Why**: If violated, protocol is insolvent
- **Testable**: YES — check after every deposit/withdraw/borrow/repay

## Access Control Invariants
### INV-AC-001: Only admin can pause
- **Property**: `pause() reverts if caller != admin`
- **Scope**: Pool module/contract
- **Why**: Unauthorized pause = DoS

## State Machine Invariants
### INV-SM-001: Cannot borrow when paused
- **Property**: `paused == true → borrow() reverts`
- **Scope**: Pool module/contract

## Arithmetic Invariants
### INV-A-001: Share price monotonically increases (absent losses)
- **Property**: `sharePriceAfter >= sharePriceBefore` for deposits
- **Scope**: Pool + ShareMath modules

## Oracle Invariants
### INV-O-001: Price feed freshness
- **Property**: `currentTime - updatedAt < STALENESS_THRESHOLD`
- **Scope**: OracleAdapter module

## Cross-Contract Invariants
### INV-CC-001: Token balance matches accounting
- **Property**: `token.balanceOf(pool) >= totalDeposits - totalBorrowed`
- **Scope**: Pool + token modules
```

Each invariant MUST have: ID, Property (concrete expression), Scope (files), Why (impact if broken), Testable (YES/NO).

---

## Phase 3a: Reviewed Invariant Spec (`02-invariants-reviewed.md`)

Produced by `invariant-reviewer`. Uses the same category structure as Phase 3 with added review annotations:

```markdown
# Invariant Specifications (Reviewed)

## Solvency Invariants
### INV-S-001: Total deposits cover total borrows
- **Property**: `totalDeposits >= totalBorrowed`
- **Scope**: Pool module/contract
- **Why**: If violated, protocol is insolvent
- **Testable**: YES — check after every deposit/withdraw/borrow/repay
- **Review**: UNCHANGED — matches canonical lending solvency property

### INV-S-002: Share price monotonicity
- **Property**: `sharePrice(t) <= sharePrice(t+1)` in absence of realized losses
- **Scope**: Vault module/contract
- **Why**: Share price decrease without loss event indicates value extraction
- **Testable**: YES — ghost variable tracking sharePrice across calls
- **Review**: TIGHTENED — original was `sharePrice >= 0` (tautological). Source: ERC4626 canonical properties.
- **Bound Rationale**: Rounding tolerance: ±1 wei per operation due to integer division.

### INV-S-010: Flash-loan-resistant solvency [ADDED]
- **Property**: `solvencyRatio() >= MIN_RATIO` at END of every transaction
- **Scope**: Pool module/contract
- **Why**: Flash loans can temporarily inflate collateral to borrow and default
- **Testable**: YES — post-condition on every public function
- **Review**: ADDED — not in original spec. Source: [canonical lending properties]
- **Multi-step**: deposit(flash) → borrow(max) → repay(flash) → default
```

Every invariant MUST have the standard fields (ID, Property, Scope, Why, Testable) PLUS:
- **Review**: Action tag — `UNCHANGED | TIGHTENED | LOOSENED | SPLIT | COMPOSED | ADDED | REMOVED | PARAMETERIZED`
- **Bound Rationale** (if TIGHTENED/LOOSENED): Derivation of the correct bound
- **Multi-step** (if COMPOSED/ADDED): The attack sequence it was designed to survive
- **Source** (if ADDED): Research URL, EIP, audit report, or DB pattern reference

Must include a Review Summary section at the end:

```markdown
## Review Summary

### Statistics
| Action | Count |
|---|---|
| UNCHANGED | N |
| TIGHTENED | N |
| ... | ... |

### Canonical Coverage
| Canonical Invariant | Status |
|---|---|
| Solvency | COVERED by INV-S-001 |
| ... | ... |

### Multi-Step Coverage
| Attack Sequence | Invariants Covering |
|---|---|
| deposit→borrow→oracle_crash→liquidate | INV-S-001, INV-ORA-001 |
| ... | ... |

### Remaining Gaps
| Gap | Risk | Recommendation |
|---|---|---|
| ... | ... | ... |
```

---

## Phase 4a: Reasoning Findings (`04a-reasoning-findings.md`)

Produced by `protocol-reasoning`. Extends the standard Finding Schema with reasoning-specific fields.

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
- **Files**: [file1.ext, file2.ext]
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
| **Affected Code** | `src/Pool.ext` L123-L145 |
| **DB Pattern Ref** | `oracle-staleness-001` from `DB/manifests/oracle.json` → `DB/oracle/pyth/PYTH_ORACLE_VULNERABILITIES.md` L93-L248 (or "Novel — no DB match") |
| **Attack Scenario** | Step-by-step exploit path |

#### Vulnerable Code
```
// src/Pool L123-L145 (use target language)
function getPrice() returns price:
    price = priceFeed.latestRoundData()
    return price  // ❌ No staleness check
```

#### Recommended Fix
```
// src/Pool L123-L145 (use target language)
function getPrice() returns price:
    (price, updatedAt) = priceFeed.latestRoundData()
    require(currentTime - updatedAt < STALENESS_THRESHOLD, "Stale price")
    require(price > 0, "Invalid price")
    return price  // ✅ Validated
```

#### PoC Reference
See `audit-output/pocs/F-001-poc.{ext}` (if generated)
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
         │  Self: grep-prune → partition into shards → spawn N sub-agents
         │  N × invariant-catcher: per-shard findings → 03-findings-shard-*.md
         │  Self: merge shards → deduplicate → 03-findings-raw.md
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
