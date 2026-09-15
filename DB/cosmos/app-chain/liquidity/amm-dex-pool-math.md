---
# Core Classification
protocol: generic
chain: cosmos
category: amm
vulnerability_type: pool_math_error
root_cause_family: arithmetic_error

# Pattern Identity
pattern_key: pool-math-error | AMM/DEX pool | swap or liquidity op | mispriced execution

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - AMM/DEX modules and pool contracts

# Attack Vector Details
attack_type: economic_exploit
affected_component: AMM/DEX modules and pool contracts

# Technical Primitives
primitives:
  - accrued
  - actionamount
  - adding
  - address
  - after
  - allow

# Grep / Hunt-Card Seeds
code_keywords:
  - accrued
  - actionamount
  - adding
  - address
  - after
  - allow
  - allowing
  - allows
  - already
  - amount

severity: critical
impact: fund_loss
language: rust
tags:
  - amm
  - l1
  - cosmos
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [k1] | reports/cosmos-l1-nodes_findings/audit-reports-apollo-2024-09-04-audit-report-apollo-osmosis-fixed-width-range-vault-v1-0-pdf.md | HIGH | Oak Security | Slippage is not correctly applied during liquidity balancing |
| [k2] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2024-01-29-audit-report-astroport-on-osmosis-v1-0-pdf.md | CRITICAL | Oak Security | Double refunds on excess offer assets allow draining pools |
| [k3] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2024-01-29-audit-report-astroport-on-osmosis-v1-0-pdf.md | CRITICAL | Oak Security | Attackers can swap any token and drain funds from pools |
| [k4] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2025-03-17-audit-report-astroport-pcl-neutron-duality-orderbook-integration-v1-0-pdf.md | CRITICAL | Oak Security | Missing ob_state persistence causes incorrect pool repeg |
| [k5] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2025-03-17-audit-report-astroport-pcl-neutron-duality-orderbook-integration-v1-0-pdf.md | HIGH | Oak Security | Excessive gas consumption in pool operations |
| [k6] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2025-03-17-audit-report-astroport-pcl-neutron-duality-orderbook-integration-v1-0-pdf.md | HIGH | Oak Security | Disabling of Neutron order book causes pool operations failure |
| [k7] | reports/cosmos-l1-nodes_findings/audit-reports-avail-2026-01-15-audit-report-avail-cosmos-and-backend-changes-v1-0-pdf.md | CRITICAL | Oak Security | Refund logic allows already fulfilled requests to be reimbursed, allowing double spends and prematurely refunded deposits, resulting in locked liquidi |
| [k8] | reports/cosmos-l1-nodes_findings/audit-reports-ibcx-2023-04-29-audit-report-ibcx-v1-0-pdf.md | CRITICAL | Oak Security | Inability to inflate an asset caused by using the wrong coin denomination for swapping the reserve to asset |
| [k9] | reports/cosmos-l1-nodes_findings/audit-reports-ibcx-2023-04-29-audit-report-ibcx-v1-0-pdf.md | CRITICAL | Oak Security | Asset deflation uses wrong swap direction by swapping the reserve to the asset |
| [k10] | reports/cosmos-l1-nodes_findings/audit-reports-ibcx-2023-04-29-audit-report-ibcx-v1-0-pdf.md | HIGH | Oak Security | Asset inflation simulates the swap incorrectly and expands by the wrong amount |
| [k11] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-01-13-audit-report-mars-outposts-v1-0-pdf.md | HIGH | Oak Security | Swapping assets in the reward collector contract are vulnerable to sandwich attack |
| [k12] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2024-07-15-audit-report-mars-v2-on-neutron-v1-0-pdf.md | CRITICAL | Oak Security | Total liquidity tokens are incorrectly increased, causing lower rewards |
| [k13] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2024-07-15-audit-report-mars-v2-on-neutron-v1-0-pdf.md | HIGH | Oak Security | Users cannot stake new liquidity tokens on Astroport |
| [k14] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2024-07-15-audit-report-mars-v2-on-neutron-v1-0-pdf.md | HIGH | Oak Security | Incorrect liquidity tokens unstaked for ActionAmount::Exact |
| [k15] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2024-12-04-audit-report-mars-perps-v1-0-pdf.md | CRITICAL | Oak Security | Users will lose accrued rewards when withdrawing liquidity |
| [k16] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2024-05-15-audit-report-osmosis-transmuter-v3-v1-0-pdf.md | HIGH | Oak Security | Corrupted assets may not be removed when liquidity reaches zero |
| [k17] | reports/cosmos-l1-nodes_findings/audit-reports-sei-2023-05-19-audit-report-sei-chain-and-cosmwasm-v1-0-pdf.md | HIGH | Oak Security | Tick sizes are wrongly updated when a newly registered pair already exists |
| [k18] | reports/cosmos-l1-nodes_findings/audit-reports-terra-liquidity-bootstrapping-pool-2021-12-23-audit-report-terra-liquidity-bootstrapping-pool-v1-0-pdf.md | CRITICAL | Oak Security | Pools with big but different token amounts allow attackers to extract free value with minimal cost |
| [k19] | reports/cosmos-l1-nodes_findings/audit-reports-yieldmos-2024-05-17-audit-report-yieldmos-outposts-osmosis-v1-0-pdf.md | CRITICAL | Oak Security | Swap operations are vulnerable to sandwich attack |
| [k20] | reports/cosmos-l1-nodes_findings/audits-duality-2023-05-16-audit-report-duality-dex-and-incentives-modules-pdf.md | CRITICAL | Informal Systems | A byzantine consumer can cause chain halt via pricing tick |
| [k21] | reports/cosmos-l1-nodes_findings/audits-duality-2023-05-16-audit-report-duality-dex-and-incentives-modules-pdf.md | CRITICAL | Informal Systems | Loss of user funds via shares rounding with large ticks |
| [k22] | reports/cosmos-l1-nodes_findings/audits-duality-2023-05-16-audit-report-duality-dex-and-incentives-modules-pdf.md | HIGH | Informal Systems | Tick and Fee inputs are not validated |
| [k23] | reports/cosmos-l1-nodes_findings/audits-duality-2023-05-16-audit-report-duality-dex-and-incentives-modules-pdf.md | MEDIUM | Informal Systems | Invalid Multi Hop Swap routes cause panic |
| [k24] | reports/cosmos-l1-nodes_findings/audits-neutron-2023-11-11-audit-report-neutron-duality-v0-5-0-integration-of-cosmos-sdk-0-47-pdf.md | CRITICAL | Informal Systems | Stealing of arbitrary funds via IBC swaps |
| [k25] | reports/cosmos-l1-nodes_findings/audits-neutron-2023-11-11-audit-report-neutron-duality-v0-5-0-integration-of-cosmos-sdk-0-47-pdf.md | HIGH | Informal Systems | Tick and Fee inputs are not completely validated |
| [k51] | reports/cosmos-l1-nodes_findings/audits-osmosis-2023-30-10-audit-fee-abstraction-module-by-notional-pdf.md | HIGH | Informal Systems | Lack of Frozen Status Check in Cross-chain Swap Execution |
| [k52] | reports/cosmos-l1-nodes_findings/audits-osmosis-2023-30-10-audit-fee-abstraction-module-by-notional-pdf.md | HIGH | Informal Systems | Unspecified recovery address for Crosschain-swaps IBC transfer |
| [k53] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-a41-supernova-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | SLIPPAGE NOT ENFORCED |
| [k54] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-astroport-fi-amm-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | POSSIBILITY TO CREATE POOLS WITH THE SAME PAIR |
| [k55] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-astroport-fi-amm-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | REPEATED POOLS CAN BE CREATED |
| [k56] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-astroport-fi-amm-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | ADDING LIQUIDITY TO NEW POOLS DOES NOT WORK PROPERLY |
| [k57] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-astroport-fi-amm-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | MAXIMUM THRESHOLD FOR SLIPPAGE IS NOT ENFORCED WHEN ADDING LIQUIDITY OR SWAPPING |
| [k58] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-astroport-fi-periphery-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | POSSIBILITY TO WITHDRAW TERRASWAP LP TOKENS AFTER CLAIMING REWARDS |
| [k59] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | WITHOUT POSSIBILITY TO SWAP ALL NATIVE TOKENS TO REWARD DENOMINATION |
| [k60] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | INADEQUATE TRACKING OF SWAPPED AMOUNTS |
| [k61] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | RESTRICTION TO NOT SWAP MARS TOKENS CAN BE BYPASSED |
| [k62] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-nolus-money-market-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | NO SLIPPAGE PROTECTION |
| [k63] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-sienna-network-amm-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | POSSIBILITY TO CREATE POOLS WITH THE SAME PAIR |
| [k64] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-sienna-network-amm-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | ADDING LIQUIDITY TO NEW POOLS DOES NOT WORK PROPERLY |
| [k65] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-sienna-network-amm-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | MAXIMUM THRESHOLD FOR SLIPPAGE IS NOT ENFORCED WHEN ADDING LIQUIDITY OR SWAPPING |
| [k66] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-sienna-network-amm-protocol-updated-code-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | POSSIBILITY TO CREATE POOLS WITH THE SAME PAIR |
| [k67] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-sienna-network-rewards-v3-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | REWARDS CANNOT BE CLAIMED WHEN REWARD POOLS ARE CLOSED |
| [k68] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-sienna-network-rewards-v3-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | POSSIBILITY TO TRANSFER AN ARBITRARY AMOUNT OF TOKENS OUT OF REWARD POOLS |
| [k69] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-valkyrie-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | NOT ENFORCING SLIPPAGE TOLERANCE COULD LEAD TOKENS LOSS |
| [k70] | reports/cosmos-l1-nodes_findings/audits-neutron-2025-07-30-neutron-q3-2025-dex-fractional-banking-audit-report-final-pdf.md | MEDIUM | Informal Systems | DEX Fractional Banking Audit Migrate5to6 not registered |
| [k71] | reports/cosmos-l1-nodes_findings/audits-neutron-2025-07-30-neutron-q3-2025-dex-fractional-banking-audit-report-final-pdf.md | MEDIUM | Informal Systems | DEX Fractional Banking Audit Inefficient fractional balance loading |
| [q72] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2023-07-13-audit-report-astroport-concentrated-liquidity-pool-with-injective-orderbook-integration-v1-0-pdf.md | LOW | Oak Security | Lack of orderbook state validation upon update |
| [q73] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2023-10-09-audit-report-osmosis-transmuter-v1-0-pdf.md | INFO | Oak Security | Zero-value swaps are allowed and introduce inefficiencies |
| [q74] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2023-10-09-audit-report-osmosis-transmuter-v1-0-pdf.md | INFO | Oak Security | Lack of limiters could result in uncontrolled pool imbalance |

## Amm Dex Liquidity

**Amm dex liquidity patterns mined from uncited L1 audit reports** - representative of 46 findings mined from 26 L1 audit reports (Halborn, Informal Systems, Oak Security).

### Overview

46 sec-tier findings (13 critical, 21 high, 12 medium) from 26 audit reports by Halborn, Informal Systems, Oak Security. Titles in the references table are verbatim from the source reports; use them to route to the exact report for full PoC detail.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the AMM/DEX modules and pool contracts path lacks the validation/bounding the cited reports identify."
- Pattern key: `pool-math-error | AMM/DEX pool | swap or liquidity op | mispriced execution`
- Interaction scope: `multi_contract`
- Primary affected component(s): `AMM/DEX modules and pool contracts`
- High-signal code keywords: `accrued, actionamount, adding, address, after, allow`
- Typical sink / impact: `fund_loss`
- Validation strength: `unassessed` (evidence rows cite source reports; per-finding PoCs not yet re-verified)

#### Valid Bug Signals

- Signal 1: title evidence in cited reports matches the audited component family (AMM/DEX modules and pool contracts)
- Signal 2: severity consensus across independent auditors (Halborn, Informal Systems, Oak Security)
- Signal 3: impact-producing condition stated in source report (fund_loss)

#### False Positive Guards

- Not this bug when: the target chain/module already enforces explicit bounds/limits on the affected path
- Safe if: audited version postdates the fix noted in the source report status
- Requires attacker control of: the inputs named in the cited finding titles (messages, bids, deposits)

### Detection Patterns

#### High-Signal Grep Seeds
```
- accrued
- actionamount
- adding
- address
- after
- allow
- allowing
- allows
- already
- amount
```

#### Audit Checklist
- [ ] Verify bounded iteration/gas on the affected path
- [ ] Check state-consistency guarantees across the failure paths cited above
- [ ] Compare implementation against the source-report recommendation

### Vulnerability Description

#### Root Cause

The cited reports describe AMM/DEX modules and pool contracts paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `pool-math-error | AMM/DEX pool | swap or liquidity op | mispriced execution`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `pool-math-error | AMM/DEX pool | swap or liquidity op | mispriced execution | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `pool-math-error | AMM/DEX pool | swap or liquidity op | mispriced execution | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: Double refunds on excess offer assets allow draining pools** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Double refunds on excess offer assets allow draining pools
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Double refunds on excess offer assets allow draining pools
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: Attackers can swap any token and drain funds from pools** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Attackers can swap any token and drain funds from pools
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Attackers can swap any token and drain funds from pools
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: Missing ob_state persistence causes incorrect pool repeg** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Missing ob_state persistence causes incorrect pool repeg
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Missing ob_state persistence causes incorrect pool repeg
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

`accrued, actionamount, adding, address, after, allow, allowing, allows, already, amount, amounts, applied, arbitrary, asset`

### Related Vulnerabilities

- See references table; sibling entries under the same DB category folder
