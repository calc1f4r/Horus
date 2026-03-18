<!-- AUTO-GENERATED from `.claude/resources/inter-agent-data-format.md`; source_sha256=8471c8d3aa2ca1b90d9b9ffb3a5b2962a1504ba722e22ccee99bc37f0dfbf129 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/resources/inter-agent-data-format.md`.
> This mirrored resource preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

# Inter-Agent Data Format

> **Purpose**: Defines the standardized data contracts between pipeline phases so the `audit-orchestrator` can reliably pass data between specialized sub-agents.
> **Audience**: All agents in the audit pipeline — producers write in this format, consumers parse it.

---

## Output Directory Structure

All pipeline artifacts go into `audit-output/` at the project root:

```
audit-output/
├── pipeline-state.md                  ← Pipeline tracker (updated after every phase)
├── memory-state.md                    ← Cross-cutting: Accumulated agent knowledge (Mem0-inspired)
├── memory-state.json                  ← Cross-cutting: Structured memory entries (machine-readable)
├── 00-scope.md                        ← Phase 1: Reconnaissance
├── context/                           ← Phase 2: Per-contract context (sharded)
│   ├── 00-orientation.md              ←   System map & contract inventory
│   ├── Pool.md                        ←   Per-contract function analysis
│   ├── OracleAdapter.md               ←   Per-contract function analysis
│   ├── ShareMath.md                   ←   Per-contract function analysis
│   └── ...                            ←   One file per contract
├── 01-context.md                      ← Phase 2: Compact global synthesis
├── 02-invariants.md                   ← Phase 3: Invariant extraction (Step 3A)
├── 02-invariants-reviewed.md          ← Phase 3: Reviewed & hardened invariants (Step 3B)
├── hunt-card-hits.json                ← Phase 4: Grep-prune results (4A prep)
├── hunt-card-shards.json              ← Phase 4: Partition plan (4A prep)
├── reasoning-seeds.md                 ← Phase 4: Reasoning seeds extracted from manifests (4B prep)
├── 03-findings-shard-*.md             ← Phase 4A: Per-shard findings (temporary)
├── 03-findings-raw.md                 ← Phase 4A: Merged findings (final)
├── 03-merge-log.md                    ← Phase 4A: Shard merge deduplication log
├── 04a-reasoning-findings.md          ← Phase 4B: Reasoning-based discovery
├── 04c-persona-findings.md            ← Phase 4C: Multi-persona audit findings
├── personas/                          ← Phase 4C: Per-persona working files
│   ├── round-1/                       ←   Round 1 individual persona findings
│   │   ├── bfs.md
│   │   ├── dfs.md
│   │   ├── backward.md
│   │   ├── state-machine.md
│   │   ├── mirror.md
│   │   └── reimpl.md
│   ├── shared-knowledge-round-1.md    ←   Cross-pollinated knowledge per round
│   └── ...
├── 04d-validation-findings.md         ← Phase 4D: Validation gap analysis
├── discovery-state-round-1.md         ← Phase 4: Cross-pollination state (round 1)
├── discovery-state-round-2.md         ← Phase 4: Cross-pollination state (round 2)
├── 05-findings-triaged.md             ← Phase 5: Merge, deduplicate & triage
├── pocs/                              ← Phase 6: PoC exploit tests [CONDITIONAL]
│   ├── F-001-poc.{ext}
│   ├── F-001-poc.log                  ←   Execution log
│   └── ...
├── 06-poc-results.md                  ← Phase 6: PoC execution results [CONDITIONAL]
├── fuzzing/                           ← Phase 7: Medusa harnesses [CONDITIONAL]
│   ├── medusa.json
│   └── ...
├── certora/                           ← Phase 7: Certora specs [CONDITIONAL]
│   ├── spec.conf
│   └── ...
├── halmos/                            ← Phase 7: Halmos symbolic tests [CONDITIONAL]
│   └── ...
├── 07-fv-results.md                   ← Phase 7: FV execution results [CONDITIONAL]
├── 08-pre-judge-results.md            ← Phase 8: Pre-judging validity screen
├── 08-pre-judge-sherlock.md           ← Phase 8: Per-judge pre-screen (if used)
├── 08-pre-judge-cantina.md            ← Phase 8: Per-judge pre-screen (if used)
├── 08-pre-judge-code4rena.md          ← Phase 8: Per-judge pre-screen (if used)
├── issues/                            ← Phase 9: Polished issue write-ups (valid only)
│   ├── F-001-issue.md
│   └── ...
├── 09-polished-findings.md            ← Phase 9: Index of polished issues
├── 10-deep-review.md                  ← Phase 10: Deep review (line-by-line judge verification)
├── 10-deep-review-sherlock.md         ← Phase 10: Per-judge deep review (if used)
├── 10-deep-review-cantina.md          ← Phase 10: Per-judge deep review (if used)
├── 10-deep-review-code4rena.md        ← Phase 10: Per-judge deep review (if used)
└── CONFIRMED-REPORT.md               ← Phase 11: Final confirmed report
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

## Phase 8: Pre-Judge Results (`08-pre-judge-results.md`)

```markdown
# Pre-Judge Results (Validity Screen)

## Configuration
- Judge Mode: <all | sherlock | cantina | code4rena>
- Pipeline Mode: <full | static-only>
- Consensus Threshold: <1/1 | 2/3>

## Verdict Summary
| Finding | <Judge 1> | <Judge 2> | <Judge 3> | Consensus | Proceed to Polish |
|---------|-----------|-----------|-----------|-----------|-------------------|
| F-001 | VALID (HIGH) | VALID (HIGH) | VALID (HIGH) | VALID | YES |
| F-002 | VALID (MED) | VALID (MED) | — | VALID | YES |
| F-003 | INVALID | VALID (LOW) | INVALID | INVALID | NO |

## Findings Proceeding to Phase 9
F-001, F-002, F-004, ...

## Findings Rejected at Pre-Judge
### F-003
- Judge verdicts: INVALID / VALID(LOW) / INVALID
- Rejection reason: Failed consensus — 1/3 valid, threshold 2/3
```

### Per-Judge Pre-Screen (`08-pre-judge-<judge-name>.md`)

```markdown
# <Judge Name> Pre-Judge Screen

| Finding | Valid? | Preliminary Severity | Rationale |
|---------|--------|---------------------|-----------|
| F-001 | VALID | HIGH | Definite loss of funds > $10K |
| F-002 | VALID | MEDIUM | Moderate impact, realistic path |
| F-003 | INVALID | — | Requires admin action (trusted role) |
```

---

## Phase 9: Polished Findings (`09-polished-findings.md`)

```markdown
# Polished Findings

## Summary
| Finding | Severity | Execution Evidence | Status |
|---------|----------|-------------------|--------|
| F-001 | HIGH | PoC PASS + FV VIOLATED | Execution-verified |
| F-002 | MEDIUM | N/A (static-only) | Static analysis only |

## F-001: [Title]
(Full submission-ready write-up from issue-writer)
See audit-output/issues/F-001-issue.md for full detail.
```

---

## Phase 10: Deep Review (`10-deep-review.md`)

```markdown
# Deep Review Results (Line-by-Line Verification)

## Configuration
- Judge Mode: <all | sherlock | cantina | code4rena>
- Pipeline Mode: <full | static-only>
- Consensus Threshold: <1/1 | 2/3>

## Deep Review Summary
| Finding | <Judge 1> | <Judge 2> | <Judge 3> | Final Verdict | Final Severity |
|---------|-----------|-----------|-----------|---------------|----------------|
| F-001 | CONFIRMED (HIGH) | CONFIRMED (HIGH) | CONFIRMED (HIGH) | CONFIRMED | HIGH |
| F-002 | CONFIRMED (MED) | CONFIRMED-DOWNGRADED (LOW) | CONFIRMED (MED) | CONFIRMED | MEDIUM |
| F-004 | REJECTED | REJECTED | — | REJECTED | — |

## Confirmed Findings (passed both pre-judge and deep review)
### F-001: [Title]
- Pre-Judge: VALID (3/3)
- Deep-Review: CONFIRMED (3/3)
- Final Severity: HIGH
- Execution Evidence: PoC PASS, FV VIOLATED (INV-S-001)

## Rejected at Deep Review
### F-004: [Title]
- Pre-Judge: VALID (2/3)
- Deep-Review: REJECTED (2/3)
- Rejection Reason: Code reference at line 142 was hallucinated — function doesn't exist
```

### Per-Judge Deep Review (`10-deep-review-<judge-name>.md`)

```markdown
# <Judge Name> Deep Review

| Finding | Code Refs | Claims | Severity | Attack Path | Root Cause | Verdict |
|---------|-----------|--------|----------|-------------|-----------|---------|
| F-001 | ✓ All verified | ✓ All substantiated | ✓ Justified | ✓ Executable | ✓ Correct | CONFIRMED (HIGH) |
| F-004 | ✗ Line 142 not found | ✗ Claim unverifiable | — | ✗ Blocked by guard | — | REJECTED |
```
- **Code4rena**: 2 (High) — [full rationale]
- **Consensus**: 3/3 VALID
- **PoC Status**: PASS (see pocs/F-001-poc.sol)
- **FV Status**: VIOLATED INV-S-001 (see halmos/)
```

---

## Phase 4C: Persona Findings (`04c-persona-findings.md`)

Produced by `multi-persona-orchestrator`. Aggregated findings from 6 independent auditing personas.

```markdown
# Multi-Persona Audit Findings

## Persona Coverage Summary
| Persona | Findings | Unique | Confirmed by Others |
|---------|----------|--------|---------------------|
| BFS | N | N | N |
| DFS | N | N | N |
| Working Backward | N | N | N |
| State Machine | N | N | N |
| Mirror | N | N | N |
| Re-Implementation | N | N | N |

## Cross-Verified Findings
(Findings confirmed by 2+ personas — highest confidence)

### F-4C-001: [Title]
| Field | Value |
|-------|-------|
| **ID** | F-4C-001 |
| **Severity** | HIGH |
| **Confidence** | HIGH (confirmed by BFS + DFS + State Machine) |
| **Root Cause** | ... |
| **Impact** | ... |
| **Discovered By** | BFS (Round 1), confirmed by DFS (Round 2), State Machine (Round 2) |

## Single-Persona Findings
(Findings from only 1 persona — lower confidence, needs triage verification)
```

---

## Phase 6: PoC Results (`06-poc-results.md`)

Produced by orchestrator after spawning `poc-writing` and executing the PoCs.

```markdown
# PoC Execution Results

## Summary
| Status | Count |
|--------|-------|
| PASS | N |
| COMPILE_FAIL | N |
| ASSERT_FAIL | N |
| REVERT | N |
| TIMEOUT | N |
| SKIP | N |

## Results
| Finding | PoC File | Status | Attempts | Notes |
|---------|----------|--------|----------|-------|
| F-001 | pocs/F-001-poc.sol | PASS | 1 | Exploit confirmed, stole 100 ETH in test |
| F-002 | pocs/F-002-poc.sol | COMPILE_FAIL | 2 | Import resolution failed after retry |
| F-003 | — | SKIP | 0 | MEDIUM severity, no PoC generated |

## Execution Logs
### F-001 (PASS)
```
forge test --match-test test_F001_exploit -vvv
[PASS] test_F001_exploit() (gas: 245891)
Logs:
  Attacker balance before: 0
  Attacker balance after: 100000000000000000000
```

### F-002 (COMPILE_FAIL — Attempt 2)
```
forge build
Error: ...
```
```

---

## Phase 7: FV Results (`07-fv-results.md`)

Produced by orchestrator after spawning FV generators and executing the suites.

```markdown
# Formal Verification Execution Results

## Tool Summary
| Tool | Specs Generated | Compiled | Executed | Violations Found |
|------|----------------|----------|----------|-----------------|
| Medusa | N | Y/N | Y/N | N |
| Certora | N | Y/N | Y/N | N |
| Halmos | N | Y/N | Y/N | N |

## Invariant → Finding Mapping
| Invariant | Tool | Result | Maps to Finding |
|-----------|------|--------|-----------------|
| INV-S-001 | Halmos | VIOLATED | F-001 (existing) |
| INV-A-003 | Medusa | VIOLATED | F-NEW-001 (new finding) |
| INV-AC-001 | Certora | VERIFIED | — (property holds) |

## New Findings from FV
(Findings created from FV violations that don't match existing Phase 5 findings)

### F-NEW-001: [Title from FV violation]
(Standard Finding Schema)

## Execution Logs
### Medusa
```
medusa fuzz --config medusa.json
...
```

### Halmos
```
halmos --function check_INV_S_001
...
```
```

---

## Pipeline State (`pipeline-state.md`)

Updated by orchestrator after every phase. Central tracking file.

```markdown
# Pipeline State

## Metadata
- **Target**: <codebase path>
- **Protocol**: <detected types>
- **Started**: <timestamp>
- **Current Phase**: <N>

## Configuration
- **Mode**: full | static-only
- **Judge Mode**: full (all 3) | single (<name>)
- **Discovery Rounds**: <N>

## Phase Status
| Phase | Status | Started | Completed | Output File |
|-------|--------|---------|-----------|-------------|
| 1 | COMPLETED | T1 | T2 | 00-scope.md |
| 2 | COMPLETED | T3 | T4 | 01-context.md |
| 3 | COMPLETED | T5 | T6 | 02-invariants-reviewed.md |
| 4-R1 | COMPLETED | T7 | T8 | (round 1 outputs) |
| 4-R2 | COMPLETED | T9 | T10 | (round 2 outputs) |
| 5 | COMPLETED | T11 | T12 | 05-findings-triaged.md |
| 6 | COMPLETE/SKIPPED | T13 | T14 | 06-poc-results.md / — |
| 7 | COMPLETE/SKIPPED | T15 | T16 | 07-fv-results.md / — |
| 8 | COMPLETED | T17 | T18 | 08-pre-judge-results.md |
| 9 | COMPLETED | T19 | T20 | 09-polished-findings.md |
| 10 | COMPLETED | T21 | T22 | 10-deep-review.md |
| 11 | IN_PROGRESS | T23 | — | — |

## Finding Tracker
| ID | Title | Source | Severity | PoC | FV | Pre-Judge | Polished | Deep-Review | Final Status |
|----|-------|--------|----------|-----|-----|-----------|----------|-------------|--------------|
| F-001 | Missing staleness check | 4A-R1 | HIGH | PASS | VIOLATED | VALID | ✓ | CONFIRMED | CONFIRMED |
| F-002 | Reentrancy in withdraw | 4B-R2 | HIGH | PASS | — | VALID | ✓ | CONFIRMED | CONFIRMED |
| F-003 | Zero-address admin | 4D-R1 | MEDIUM | SKIP | — | VALID | ✓ | NEEDS-REVISION | DEMOTED |
| F-004 | False positive | 4C-R1 | LOW | — | — | INVALID | — | — | REJECTED |
```

---

## Cross-Phase Data Flow Summary

```
Phase 1 (Scope) ──→ protocolTypes, manifestList, filesInScope
                       │ + pipeline-state.md initialized (with Configuration)
                       │
Phase 2 (Context) ←───┘ reads filesInScope
         │──→ architecture, functions, invariantCandidates, assumptions
         │
Phase 3 (Invariants: 3A→3B) ←── reads invariantCandidates
         │  3A: invariant-writer → 02-invariants.md
         │  3B: invariant-reviewer → 02-invariants-reviewed.md
         │──→ reviewed invariant specs (INV-*)
         │
         ╔══════════════════════════════════════════════════════════╗
         ║  Phase 4 — ITERATIVE DISCOVERY (N rounds)              ║
         ║                                                         ║
         ║  Round 1:                                               ║
         ║  ├──4A (DB Hunt) ──→ 03-findings-raw.md                ║
         ║  ├──4B (Reasoning) ──→ 04a-reasoning-findings.md       ║
         ║  ├──4C (Personas) ──→ 04c-persona-findings.md          ║
         ║  └──4D (Validation) ──→ 04d-validation-findings.md     ║
         ║       │                                                 ║
         ║  Orchestrator writes discovery-state-round-1.md         ║
         ║  (cumulative findings + cross-check requests +          ║
         ║   unexplored areas + variant suggestions)               ║
         ║       │                                                 ║
         ║  Round 2+ (reads discovery-state-round-(N-1).md):       ║
         ║  ├──4A ──→ 03-findings-raw-round-N.md                  ║
         ║  ├──4B ──→ 04a-reasoning-round-N.md                    ║
         ║  ├──4C ──→ 04c-persona-round-N.md                      ║
         ║  └──4D ──→ 04d-validation-round-N.md                   ║
         ║       │                                                 ║
         ║  Orchestrator writes discovery-state-round-N.md         ║
         ╚══════════════════════════════════════════════════════════╝
                                     │
Phase 5 (Merge & Triage) ←──────────┘ reads ALL rounds of Phase 4 outputs
         │  Cross-source correlation → dedup → falsification → severity
         │  Assign stable IDs: F-001, F-002, ...
         │──→ 05-findings-triaged.md
         │
         ┌─────────── if --static-only: SKIP Phases 6-7 ───────────┐
         │                                                          │
Phase 6 (PoC Gen + EXECUTION) [CONDITIONAL]                        │
         │  Per CRIT/HIGH: poc-writing spawn → compile → RUN        │
         │──→ pocs/F-NNN-poc.* + 06-poc-results.md                 │
         │                                                          │
Phase 7 (FV Gen + EXECUTION) [CONDITIONAL]                         │
         │  Parallel: medusa + certora + halmos → compile → RUN     │
         │──→ fuzzing/ + certora/ + halmos/ + 07-fv-results.md     │
         └──────────────────────────────────────────────────────────┘
         │
         ╔══════════════════════════════════════════════════════════╗
         ║  Phases 8-10 — JUDGING SELF-LOOP                       ║
         ║                                                         ║
         ║  Phase 8 (Pre-Judging) ←── reads 05-findings-triaged   ║
         ║  │  Judge(s) screen all findings: VALID / INVALID       ║
         ║  │  (--judge=X: single judge; default: all 3 parallel)  ║
         ║  │──→ 08-pre-judge-results.md                           ║
         ║  │                                                      ║
         ║  Phase 9 (Issue Polishing) ←── reads VALID findings     ║
         ║  │  issue-writer per finding (with execution evidence   ║
         ║  │  if available, or static-only annotation)            ║
         ║  │──→ issues/F-NNN-issue.md + 09-polished-findings.md  ║
         ║  │                                                      ║
         ║  Phase 10 (Deep Review) ←── reads polished findings     ║
         ║  │  Same judge(s) do line-by-line deep review           ║
         ║  │  CONFIRMED / NEEDS-REVISION / REJECTED               ║
         ║  │  NEEDS-REVISION → loop back to Phase 9 (max 1 retry)║
         ║  │──→ 10-deep-review.md                                 ║
         ╚══════════════════════════════════════════════════════════╝
         │
Phase 11 (Report) ←── reads ALL pipeline artifacts
         │  Mode-aware: includes/omits execution evidence sections
         │  Includes judging self-loop summary + discovery rounds record
         └──→ CONFIRMED-REPORT.md
```
