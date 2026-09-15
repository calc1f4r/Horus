---
# Core Classification
protocol: generic
chain: generic
category: polygon
vulnerability_type: polygon_bor
root_cause_family: see pattern_key

# Pattern Identity
pattern_key: polygon-bor | polygon bor | varies by finding | see references

# Interaction Scope
interaction_scope: varies
involved_contracts:
  - polygon bor

# Attack Vector Details
attack_type: varies
affected_component: polygon bor

# Technical Primitives
primitives:
  - abused
  - across
  - address
  - aggregator
  - asset
  - authority

# Grep / Hunt-Card Seeds
code_keywords:
  - abused
  - across
  - address
  - aggregator
  - asset
  - authority
  - averaged
  - batch

severity: critical
impact: varies
language: varies
tags:
  - generic
  - l1
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [o1] | reports/other-l1_findings/public-audits-reports-polygon-sigma-prime-polygon-lxly-bridge-security-assessment-report-v2-1-pdf.md | MEDIUM | NCC Group | LXL Y-02 Aggregator Rewards Are Averaged Across Forced Batches & Rollups Asset PolygonRollupBase.sol Status Closed: See Resolution Rating |
| [o2] | reports/other-l1_findings/public-audits-reports-polygon-sigma-prime-polygon-lxly-bridge-security-assessment-report-v2-1-pdf.md | MEDIUM | NCC Group | Findings LXL Y-03 Batch Fees Multiplier Cap Bypassed With Multiple Calls Asset PolygonRollupManager.sol Status Closed: See Resolution Rating |
| [o3] | reports/other-l1_findings/public-audits-reports-polygon-sigma-prime-polygon-lxly-bridge-security-assessment-report-v2-1-pdf.md | MEDIUM | NCC Group | Bridge Detailed Findings LXL Y-04 Missing ifNotEmergencyState Modifier Asset PolygonZkEVMBridgeV2.sol Status Resolved: See Resolution Rating |
| [o4] | reports/other-l1_findings/public-audits-reports-polygon-sigma-prime-polygon-lxly-bridge-security-assessment-report-v2-1-pdf.md | MEDIUM | NCC Group | Detailed Findings LXL Y-05 Rollups Can Be Overwritten Without Checks Asset PolygonRollupManager.sol Status Resolved: See Resolution Rating |
| [o5] | reports/other-l1_findings/public-audits-reports-polygon-sigma-prime-polygon-lxly-bridge-security-assessment-report-v2-1-pdf.md | MEDIUM | NCC Group | Batch Event Will Look Like It Came From An EOA Asset PolygonRollupBase.sol  PolygonRollupBaseEtrog.sol Status Closed: See Resolution Rating |
| [o6] | reports/other-l1_findings/public-audits-reports-polygon-sigma-prime-polygon-lxly-bridge-security-assessment-report-v2-1-pdf.md | MEDIUM | NCC Group | Findings LXL Y-07 T oken Wrapped Creation Code Is Not Deterministic Asset PolygonZkEVMBridgeV2.sol Status Resolved: See Resolution Rating |
| [o7] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-debt-dao-p2p-loan-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | WITHDRAWING ALL LIQUIDITY BEFORE BORROWING CAN DEADLOCK CONTRACT |
| [o8] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-debt-dao-p2p-loan-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | BORROWING FROM NON-FIRST POSITION CAN DEADLOCK CONTRACT |
| [o9] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-debt-dao-p2p-loan-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | UPDATEOWNERSPLIT FUNCTION CAN BE ABUSED BY LENDER OR BORROWER |
| [o10] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-debt-dao-p2p-loan-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | BORROWER CAN CLAIM REVENUE WHILE LOAN IS LIQUIDATABLE |
| [o11] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-moonwell-finance-compound-vault-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | INCORRECT USE OF BORROW CAP INSTEAD OF SUPPLY CAP IN MAXMINT FUNCTION |
| [o12] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-tribal-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | BORROWER ADDRESS NOT ENFORCED TO BE WHITELISTED IN AUTHORITY |
| [o13] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-tribal-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | BORROWER CAN NOT RECOVER DEPOSIT IN FUNDING FAILED STAGE |
| [q14] | reports/other-l1_findings/public-audits-reports-near-review-pdf.md | LOW | NCC Group | PR #202. Page   11 NEAR Protocol Detailed Findings NSS-05 Free Memory Pointer Overflow Asset Borsh.sol Status Resolved: See Resolution Rating |
| [q15] | reports/other-l1_findings/public-audits-reports-near-review-pdf.md | LOW | NCC Group | Findings NSS-06 Borsh Decoding Does Not Call done() Asset eNear.sol ERC20Locker.sol &EthCustodian.sol Status Resolved: See Resolution Rating |
| [q16] | reports/other-l1_findings/publicreports-solana-program-audit-clone-protocol-solana-program-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | LIQUIDATING A BORROW POSITION WITH PARTIAL DEBT SETTLEMENT |

## Polygon Bor

**polygon-bor patterns mined from uncited L1 audit reports** - 13 sec-tier findings (1 critical / 3 high / 9 medium) across 4 files from Halborn, NCC Group.

### Overview

Titles in the references table are verbatim from source reports. Route to the exact report file for full PoC detail. Validation strength: `unassessed` (evidence rows only).

### Detection Patterns

#### High-Signal Grep Seeds
```
- abused
- across
- address
- aggregator
- asset
- authority
- averaged
- batch
```

### Vulnerability Description

#### Root Cause

The cited reports describe polygon bor paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `polygon-bor | polygon bor | varies by finding | see references`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `polygon-bor | polygon bor | varies by finding | see references | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `polygon-bor | polygon bor | varies by finding | see references | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: WITHDRAWING ALL LIQUIDITY BEFORE BORROWING CAN DEADLOCK CONTRACT** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// WITHDRAWING ALL LIQUIDITY BEFORE BORROWING CAN DEADLOCK CONTRACT
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: WITHDRAWING ALL LIQUIDITY BEFORE BORROWING CAN DEADLOCK CONTRACT
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: BORROWING FROM NON-FIRST POSITION CAN DEADLOCK CONTRACT** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// BORROWING FROM NON-FIRST POSITION CAN DEADLOCK CONTRACT
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: BORROWING FROM NON-FIRST POSITION CAN DEADLOCK CONTRACT
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: UPDATEOWNERSPLIT FUNCTION CAN BE ABUSED BY LENDER OR BORROWER** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// UPDATEOWNERSPLIT FUNCTION CAN BE ABUSED BY LENDER OR BORROWER
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: UPDATEOWNERSPLIT FUNCTION CAN BE ABUSED BY LENDER OR BORROWER
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```

### Impact Analysis

#### Technical Impact
- Wrong accounting / reward misallocation / stuck or double-counted funds (fund-loss class rows above)
- State inconsistency after partial failure (see error-handling references)
- Chain halt or node crash from unbounded work (see DoS rows)

#### Business Impact
- User fund loss and withdrawal freezes; validator downtime; consensus/partition risk for client-level bugs.

### Secure Implementation

**Fix 1: [Bound and validate at the entry surface]**
```rust
// ✅ SECURE: explicit bounds + validation before state mutation
fn handler(input: UntrustedInput) -> Result<(), Error> {
    ensure!(input.len() <= T::MaxInput::get(), Error::TooLarge);
    ensure!(is_valid(&input), Error::Invalid);
    state.update_checked(&input)?;
    Ok(())
}
```

**Fix 2: [Aggregate instead of iterate; cap growth]**
```rust
// ✅ SECURE: keep block-time work O(1) and cap attacker growth
fn on_block_end() {
    let aggregate = Aggregates::get();          // maintained incrementally
    distribute(&aggregate);                      // no unbounded iteration
}
fn create_plan(p: Plan) -> Result<(), Error> {
    ensure!(PlansCount::get() < T::MaxPlans::get(), Error::TooManyPlans);
    Ok(())
}
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Entry surface writes state before validating attacker-controlled fields
- Block-time hooks iterate collections whose size is attacker-influenceable
- Multi-step handlers where a mid-step failure leaves earlier writes committed
- Config setters without role checks or bounds
```

#### Audit Checklist
- [ ] Verify every attacker-reachable input is length/bounds-checked before state writes
- [ ] Verify block-time (end-blocker / on_finalize) iteration is O(1) or capped
- [ ] Verify failure paths roll back partial state mutations
- [ ] Cross-check the cited reports' fix status before re-reporting

### Keywords for Search

`abused, across, address, aggregator, asset, authority, averaged, batch, batches, before`

### Related Vulnerabilities

- Sibling entries under the same category folder
