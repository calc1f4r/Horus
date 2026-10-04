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
  - accrued
  - accruing
  - allow
  - asset
  - assets
  - attackers

# Grep / Hunt-Card Seeds
code_keywords:
  - accrued
  - accruing
  - allow
  - asset
  - assets
  - attackers
  - auto
  - before
  - behalf
  - borrow

severity: critical
impact: fund_loss
language: rust
tags:
  - lending
  - l1
  - substrate
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [x1] | reports/substrate-l1_findings/composable-audits-halborn-audit20210229-pallets-core-pdf.md | CRITICAL | Halborn | 3.3 (HAL-03) IMPROPER LENDING MARKET CONFIGURATION - CRITICAL Description: Inside the lending pallet, using the update_market function, mark |
| [x2] | reports/substrate-l1_findings/composable-audits-halborn-audit20210229-pallets-core-pdf.md | MEDIUM | Halborn | 3.6 (HAL-06) COLLATERAL FACTOR CAN BE SET SMALLER THAN TWO - MEDIUM Description: Inside the lending pallet, the update_market function allow |
| [x3] | reports/substrate-l1_findings/composable-halborn-core.md | CRITICAL | Halborn | 3.3 (HAL-03) IMPROPER LENDING MARKET CONFIGURATION - CRITICAL Description: Inside the lending pallet, using the update_market function, mark |
| [x4] | reports/substrate-l1_findings/composable-halborn-core.md | MEDIUM | Halborn | 3.6 (HAL-06) COLLATERAL FACTOR CAN BE SET SMALLER THAN TWO - MEDIUM Description: Inside the lending pallet, the update_market function allow |
| [x5] | reports/substrate-l1_findings/starlay-oak-wasm.md | CRITICAL | Oak Security | Attackers can increase users' debt by repaying a loan on their behalf |
| [x6] | reports/substrate-l1_findings/starlay-oak-wasm.md | CRITICAL | Oak Security | Unauthorized pool liquidation threshold modiﬁcation |
| [x7] | reports/substrate-l1_findings/starlay-oak-wasm.md | CRITICAL | Oak Security | Disabled collateral assets can be liquidated |
| [x8] | reports/substrate-l1_findings/starlay-oak-wasm.md | CRITICAL | Oak Security | Disabled collaterals can be seized during liquidation |
| [x9] | reports/substrate-l1_findings/starlay-oak-wasm.md | CRITICAL | Oak Security | Accruing interest does not update total borrows and reserves |
| [x10] | reports/substrate-l1_findings/starlay-oak-wasm.md | HIGH | Oak Security | Interest not accrued before rate computations |
| [x11] | reports/substrate-l1_findings/starlay-oak-wasm.md | HIGH | Oak Security | Flash loans can be initiated without paying fee premiums |
| [x12] | reports/substrate-l1_findings/starlay-oak-wasm.md | HIGH | Oak Security | Protocol reserves are incorrectly scaled with borrow index |
| [x13] | reports/substrate-l1_findings/starlay-oak-wasm.md | HIGH | Oak Security | Incorrect interest and reserves accrued when updating the interest rate model contract and reserve factors |
| [x14] | reports/substrate-l1_findings/starlay-oak-wasm.md | HIGH | Oak Security | Potential incorrect logic for ﬂash loan implementation |
| [x15] | reports/substrate-l1_findings/starlay-oak-wasm.md | HIGH | Oak Security | Incorrect logic for auto-enabling the recipient’s asset as collateral |
| [x16] | reports/substrate-l1_findings/starlay-oak-wasm.md | HIGH | Oak Security | Controllers can seize collaterals governed by other controllers |
| [x33] | reports/substrate-l1_findings/audits-interlay-informal-report-interlay-audit-2021q2-pdf.md | MEDIUM | Informal Systems | Informal Systems InterBTC Parachain IF-INTERLAY-LIQUIDATION: Liquidation event incen- tives unclear |
| [x34] | reports/substrate-l1_findings/interlay-informal-2021q2.md | MEDIUM | Informal Systems | Informal Systems InterBTC Parachain IF-INTERLAY-LIQUIDATION: Liquidation event incen- tives unclear |
| [x35] | reports/substrate-l1_findings/centrifuge-srl-baseline-2022.md | MEDIUM | SRLabs | Integer overflows could invert state of a loan Integer overflows are common in Rust, they are also easy to prevent |

## Lending Liquidation

**Lending liquidation patterns mined from uncited L1 audit reports** - representative of 16 findings mined from 3 L1 audit reports (Halborn, Oak Security).

### Overview

16 sec-tier findings (7 critical, 7 high, 2 medium) from 3 audit reports by Halborn, Oak Security. Titles in the references table are verbatim from the source reports; use them to route to the exact report for full PoC detail.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the lending pallets and liquidation logic path lacks the validation/bounding the cited reports identify."
- Pattern key: `liquidation-accounting-gap | lending pallet | price move + liquidate | bad debt`
- Interaction scope: `multi_contract`
- Primary affected component(s): `lending pallets and liquidation logic`
- High-signal code keywords: `accrued, accruing, allow, asset, assets, attackers`
- Typical sink / impact: `fund_loss`
- Validation strength: `unassessed` (evidence rows cite source reports; per-finding PoCs not yet re-verified)

#### Valid Bug Signals

- Signal 1: title evidence in cited reports matches the audited component family (lending pallets and liquidation logic)
- Signal 2: severity consensus across independent auditors (Halborn, Oak Security)
- Signal 3: impact-producing condition stated in source report (fund_loss)

#### False Positive Guards

- Not this bug when: the target chain/module already enforces explicit bounds/limits on the affected path
- Safe if: audited version postdates the fix noted in the source report status
- Requires attacker control of: the inputs named in the cited finding titles (messages, bids, deposits)

### Detection Patterns

#### High-Signal Grep Seeds
```
- accrued
- accruing
- allow
- asset
- assets
- attackers
- auto
- before
- behalf
- borrow
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

**Example 1: 3.3 (HAL-03) IMPROPER LENDING MARKET CONFIGURATION - CRITICAL Description: Inside the lending pallet, using the update_m** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// 3.3 (HAL-03) IMPROPER LENDING MARKET CONFIGURATION - CRITICAL Description: Inside the lending pallet, using the update_market function, mark
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: 3.3 (HAL-03) IMPROPER LENDING MARKET CONFIGURATION - CRITICAL Description: Inside the lending pallet
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: 3.3 (HAL-03) IMPROPER LENDING MARKET CONFIGURATION - CRITICAL Description: Inside the lending pallet, using the update_m** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// 3.3 (HAL-03) IMPROPER LENDING MARKET CONFIGURATION - CRITICAL Description: Inside the lending pallet, using the update_market function, mark
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: 3.3 (HAL-03) IMPROPER LENDING MARKET CONFIGURATION - CRITICAL Description: Inside the lending pallet
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: Attackers can increase users' debt by repaying a loan on their behalf** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Attackers can increase users' debt by repaying a loan on their behalf
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Attackers can increase users' debt by repaying a loan on their behalf
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

`accrued, accruing, allow, asset, assets, attackers, auto, before, behalf, borrow, borrows, cation, collateral, collaterals`

### Related Vulnerabilities

- See references table; sibling entries under the same DB category folder
