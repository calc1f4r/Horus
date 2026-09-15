---
# Core Classification
protocol: generic
chain: polkadot
category: lending
vulnerability_type: liquidation_accounting
root_cause_family: accounting_error

# Pattern Identity
pattern_key: liquidation-accounting-gap | lending pallet | price move + liquidate | bad debt

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - lending pallets and liquidation logic

# Attack Vector Details
attack_type: economic_exploit
affected_component: lending pallets and liquidation logic

# Technical Primitives
primitives:
  - accumulating
  - actionkind
  - adequate
  - allow
  - allows
  - amount

# Grep / Hunt-Card Seeds
code_keywords:
  - accumulating
  - actionkind
  - adequate
  - allow
  - allows
  - amount
  - amounts
  - arbitrary
  - asset
  - assets

severity: critical
impact: fund_loss
language: rust
tags:
  - lending
  - l1
  - cosmos
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [k1] | reports/cosmos-l1-nodes_findings/audit-reports-avail-2026-01-15-audit-report-avail-cosmos-and-backend-changes-v1-0-pdf.md | HIGH | Oak Security | Missing minimum block confirmation margin allows external reorgs to invalidate verified requests |
| [k2] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-11-23-audit-report-comdex-lend-and-liquidation-modules-v1-0-pdf.md | CRITICAL | Oak Security | Input-dependent iteration in Lend module's BeginBlocker may slow down or stop block production |
| [k3] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-11-23-audit-report-comdex-lend-and-liquidation-modules-v1-0-pdf.md | CRITICAL | Oak Security | Batch mechanism in Liquidation module's BeginBlocker may allow malicious manipulations |
| [k4] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-11-23-audit-report-comdex-lend-and-liquidation-modules-v1-0-pdf.md | HIGH | Oak Security | Borrow position's InterestAccumulated is not updated before liquidation, leading to an incorrect interest calculation |
| [k5] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-12-07-audit-report-comdex-v1-0-pdf.md | CRITICAL | Oak Security | Users cannot redeem their collateral assets regardless of the ESM status |
| [k6] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2022-02-17-audit-report-mars-v1-0-pdf.md | CRITICAL | Oak Security | Deactivated market assets would cause forced liquidation on borrowers |
| [k7] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2022-02-17-audit-report-mars-v1-0-pdf.md | CRITICAL | Oak Security | Malicious smart contracts can avoid liquidation attempts |
| [k8] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2022-02-17-audit-report-mars-v1-0-pdf.md | CRITICAL | Oak Security | Disabled collateral assets can be liquidated |
| [k9] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2022-12-09-audit-report-mars-rover-v1-0-pdf.md | CRITICAL | Oak Security | Borrowers can prevent liquidation leading to bad debt accumulating |
| [k10] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2022-12-09-audit-report-mars-rover-v1-0-pdf.md | HIGH | Oak Security | Liquidators can extract a higher value by looping small amounts of liquidations |
| [k11] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-01-13-audit-report-mars-outposts-v1-0-pdf.md | CRITICAL | Oak Security | Disabled collateral can be re-enabled by depositing on behalf of the user |
| [k12] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-02-03-audit-report-mars-periphery-v1-0-pdf.md | CRITICAL | Oak Security | Liquidated and excess funds are stuck in the liquidation filterer contract |
| [k13] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-02-03-audit-report-mars-periphery-v1-0-pdf.md | HIGH | Oak Security | Liquidation filterer contract cannot process multiple liquidations efficiently |
| [k14] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-09-14-audit-report-mars-rover-v2-v1-0-pdf.md | CRITICAL | Oak Security | Lendings in the red bank cannot be liquidated when ActionKind::Default circuit breakers trigger |
| [k15] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-09-14-audit-report-mars-rover-v2-v1-0-pdf.md | HIGH | Oak Security | Incorrect protocol fee calculation during liquidation |
| [k16] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-09-14-audit-report-mars-rover-v2-v1-0-pdf.md | HIGH | Oak Security | Circuit breakers may block liquidations, risking the protocol's solvency |
| [k17] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-09-14-audit-report-mars-rover-v2-v1-0-pdf.md | HIGH | Oak Security | Inaccurate health computation due to default collateral limit |
| [k18] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2024-07-15-audit-report-mars-v2-on-neutron-v1-0-pdf.md | HIGH | Oak Security | Liquidatee's staking rewards are lost |
| [k19] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2024-12-04-audit-report-mars-perps-v1-0-pdf.md | HIGH | Oak Security | Liquidation will fail for zero amounts |
| [k20] | reports/cosmos-l1-nodes_findings/publications-reviews-umee-pdf.md | MEDIUM | Trail of Bits | Lack of user-controlled limits for input amount in LiquidateBorrow |
| [k21] | reports/cosmos-l1-nodes_findings/publications-reviews-umee-pdf.md | MEDIUM | Trail of Bits | Lack of simulation and fuzzing of leverage module invariants |
| [k22] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | LOANS CAN BE REPAID WITHOUT SPENDING COINS |
| [k23] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | ARBITRARY MINTING OF COINS WITHOUT DEPOSITING COLLATERALS |
| [k24] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | COLLATERAL BALANCE OF LIQUIDATED USERS DOES NOT DECREASE |
| [k25] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | LIQUIDATED LOANS WITHOUT AN ADEQUATE REPAYMENT |
| [k56] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | LIQUIDATION CAN TOTALLY CORRUPT THE VALUES OF TOTAL DEBT, INDEXES AND RATES |
| [k57] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | POSSIBILITY TO LIQUIDATE WHEN COLLATERAL ASSET IS UNSET |
| [k58] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | LOAN LIMIT CAN BE UPDATED FOR USERS WITH COLLATERALIZED DEBTS |
| [k59] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | POSSIBILITY TO DEPOSIT, REPAY OR LIQUIDATE WITH NATIVE COINS NOT REGISTERED IN STORAGE |
| [k60] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-nexus-protocol-cosmwasm-smart-contract-security-audit-report-halborn-v1-1-pdf.md | HIGH | Halborn | NO UPDATE OF LOAN REPAYMENT STATE ON REBALANCE FUNCTION |
| [k61] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-valkyrie-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | WITHDRAWAL OF ARBITRARY PARTICIPATION REWARDS WITHOUT DEPOSITING COLLATERALS |
| [k62] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-valkyrie-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | DEPOSITS GET LOCKED IN CAMPAIGN IF COLLATERAL DENOM IS NOT SPECIFIED |

## Lending Liquidation

**Lending liquidation patterns mined from uncited L1 audit reports** - representative of 37 findings mined from 15 L1 audit reports (Halborn, Oak Security, Trail of Bits).

### Overview

37 sec-tier findings (17 critical, 15 high, 5 medium) from 15 audit reports by Halborn, Oak Security, Trail of Bits. Titles in the references table are verbatim from the source reports; use them to route to the exact report for full PoC detail.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the lending pallets and liquidation logic path lacks the validation/bounding the cited reports identify."
- Pattern key: `liquidation-accounting-gap | lending pallet | price move + liquidate | bad debt`
- Interaction scope: `multi_contract`
- Primary affected component(s): `lending pallets and liquidation logic`
- High-signal code keywords: `accumulating, actionkind, adequate, allow, allows, amount`
- Typical sink / impact: `fund_loss`
- Validation strength: `unassessed` (evidence rows cite source reports; per-finding PoCs not yet re-verified)

#### Valid Bug Signals

- Signal 1: title evidence in cited reports matches the audited component family (lending pallets and liquidation logic)
- Signal 2: severity consensus across independent auditors (Halborn, Oak Security, Trail of Bits)
- Signal 3: impact-producing condition stated in source report (fund_loss)

#### False Positive Guards

- Not this bug when: the target chain/module already enforces explicit bounds/limits on the affected path
- Safe if: audited version postdates the fix noted in the source report status
- Requires attacker control of: the inputs named in the cited finding titles (messages, bids, deposits)

### Detection Patterns

#### High-Signal Grep Seeds
```
- accumulating
- actionkind
- adequate
- allow
- allows
- amount
- amounts
- arbitrary
- asset
- assets
```

#### Audit Checklist
- [ ] Verify bounded iteration/gas on the affected path
- [ ] Check state-consistency guarantees across the failure paths cited above
- [ ] Compare implementation against the source-report recommendation

### Vulnerability Description

#### Root Cause

The cited reports describe lending pallets and liquidation logic paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `liquidation-accounting-gap | lending pallet | price move + liquidate | bad debt`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `liquidation-accounting-gap | lending pallet | price move + liquidate | bad debt | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `liquidation-accounting-gap | lending pallet | price move + liquidate | bad debt | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: Input-dependent iteration in Lend module's BeginBlocker may slow down or stop block production** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Input-dependent iteration in Lend module's BeginBlocker may slow down or stop block production
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Input-dependent iteration in Lend module's BeginBlocker may slow down or stop block production
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: Batch mechanism in Liquidation module's BeginBlocker may allow malicious manipulations** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Batch mechanism in Liquidation module's BeginBlocker may allow malicious manipulations
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Batch mechanism in Liquidation module's BeginBlocker may allow malicious manipulations
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: Users cannot redeem their collateral assets regardless of the ESM status** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Users cannot redeem their collateral assets regardless of the ESM status
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Users cannot redeem their collateral assets regardless of the ESM status
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

`accumulating, actionkind, adequate, allow, allows, amount, amounts, arbitrary, asset, assets, attempts, available, avoid, balance`

### Related Vulnerabilities

- See references table; sibling entries under the same DB category folder
