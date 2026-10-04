---
# Core Classification
protocol: generic
chain: polkadot
category: arithmetic
vulnerability_type: rounding_precision_error
root_cause_family: rounding_error

# Pattern Identity
pattern_key: rounding-drift | fixed-point math | repeated ops | value leak

# Interaction Scope
interaction_scope: single_contract
involved_contracts:
  - balance/issuance computation paths

# Attack Vector Details
attack_type: logical_error
affected_component: balance/issuance computation paths

# Technical Primitives
primitives:
  - account
  - allows
  - amounts
  - arbitrarily
  - assets
  - because

# Grep / Hunt-Card Seeds
code_keywords:
  - account
  - allows
  - amounts
  - arbitrarily
  - assets
  - because
  - beginblocker
  - being
  - between
  - calculation

severity: critical
impact: fund_loss
language: rust
tags:
  - arithmetic
  - l1
  - cosmos
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [k1] | reports/cosmos-l1-nodes_findings/audit-reports-amulet-2024-02-07-audit-report-amulet-neutron-pos-strategy-v1-0-pdf.md | HIGH | Oak Security | Rewards are not increased for zero fees or empty fee recipient |
| [k2] | reports/cosmos-l1-nodes_findings/audit-reports-amulet-2024-02-07-audit-report-amulet-neutron-pos-strategy-v1-0-pdf.md | HIGH | Oak Security | Delegation rewards computed will be zero if MsgUndelegate is called |
| [k3] | reports/cosmos-l1-nodes_findings/audit-reports-apollo-2024-09-04-audit-report-apollo-osmosis-fixed-width-range-vault-v1-0-pdf.md | HIGH | Oak Security | The contract's position can arbitrarily be set to zero |
| [k4] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-10-28-audit-report-comdex-locking-and-vesting-contracts-v1-0-pdf.md | CRITICAL | Oak Security | Multiple rounding issues may cause zero rewards being distributed |
| [k5] | reports/cosmos-l1-nodes_findings/audit-reports-ibcx-2023-04-29-audit-report-ibcx-v1-0-pdf.md | CRITICAL | Oak Security | Rebalance may not be finalizable because of rounding error |
| [k6] | reports/cosmos-l1-nodes_findings/audit-reports-injective-2023-01-20-audit-report-injective-v1-0-pdf.md | CRITICAL | Oak Security | Contract creators can update the gas price into invalid integer value in order to disable the wasmx 's BeginBlocker execution |
| [k7] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2024-12-04-audit-report-mars-perps-v1-0-pdf.md | HIGH | Oak Security | Liquidation will fail for zero amounts |
| [k8] | reports/cosmos-l1-nodes_findings/audit-reports-milkyway-2024-12-16-audit-report-milkyway-celestia-restaking-v1-0-pdf.md | CRITICAL | Oak Security | Incorrect rounding direction when decreasing insurance fund |
| [k9] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2025-03-25-audit-report-neutron-independent-chain-v1-0-pdf.md | HIGH | Oak Security | Incorrect stake retrieval for LST protocols leads to zero rewards |
| [k10] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2024-05-15-audit-report-osmosis-transmuter-v3-v1-0-pdf.md | HIGH | Oak Security | Corrupted assets may not be removed when liquidity reaches zero |
| [k11] | reports/cosmos-l1-nodes_findings/audit-reports-persistence-2022-01-20-audit-report-persistence-bridge-v1-0-pdf.md | HIGH | Oak Security | Transaction page calculation using floating point numbers could be off by one, causing transactions to be missed |
| [k12] | reports/cosmos-l1-nodes_findings/audits-duality-2023-05-16-audit-report-duality-dex-and-incentives-modules-pdf.md | CRITICAL | Informal Systems | Loss of user funds via shares rounding with large ticks |
| [k13] | reports/cosmos-l1-nodes_findings/audits-osmosis-2023-06-23-audit-report-osmosis-q2-pdf.md | HIGH | Informal Systems | Division by zero protection in distribute.go |
| [k14] | reports/cosmos-l1-nodes_findings/gaia-contrib-audits-liquid-zellic-audit-25-pdf.md | MEDIUM | Informal Systems | Missing enforcement of MinSelfDelegation allows zero self-delegation for validators |
| [k15] | reports/cosmos-l1-nodes_findings/publications-reviews-umee-pdf.md | HIGH | Trail of Bits | Validators can crash other nodes by triggering an integer overflow |
| [k16] | reports/cosmos-l1-nodes_findings/publications-reviews-umee-pdf.md | HIGH | Trail of Bits | Rounding errors may cause the module to incur losses |
| [k17] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-a41-supernova-cosmos-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | FUNDS CAN BE LOCKED IF THE ZONE DECIMAL IS HIGHER THAN 18 |
| [k18] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-pocket-network-validator-wpokt-golang-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | POTENTIAL RISK OF int64 Nonce OVERFLOW IN FINDNONCE FUNCTION OF MintSignerRunner |
| [k19] | reports/cosmos-l1-nodes_findings/v4-chain-audits-informal-systems-audit-report-phase-i-ii-pdf.md | HIGH | Informal Systems | Division by Zero Issue in GetBankruptcyPriceInQuoteQuantums Function |
| [k20] | reports/cosmos-l1-nodes_findings/audits-anoma-namada-q2-2025-e2e-shielded-transaction-balance-consistency-audit-report-final-pdf.md | MEDIUM | Informal Systems | Inconsistent handling of overflowing transactions between prepare and process proposal |
| [k21] | reports/cosmos-l1-nodes_findings/audits-neutron-2025-07-18-neutron-timewave-q2-2025-valence-protocol-audit-report-final-pdf.md | MEDIUM | Informal Systems | Neutron & Timewave Q2 2025 Valence Protocol target lacks zero-check in Account execute() function Implementation High Patched Without Reaudit Unexpect |
| [q22] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2023-07-13-audit-report-astroport-concentrated-liquidity-pool-with-injective-orderbook-integration-v1-0-pdf.md | INFO | Oak Security | Overflow checks not enabled for release profile |
| [q23] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-1-pdf.md | LOW | Oak Security | Leftover USDC due to rounding will be irrecoverable |
| [q24] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-astroport-fi-maker-contract-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | OVERFLOW CHECKS NOT SET FOR PROFILE RELEASE |

## Arith Rounding

**Arith rounding patterns mined from uncited L1 audit reports** - representative of 21 findings mined from 19 L1 audit reports (Halborn, Informal Systems, Oak Security, Trail of Bits).

### Overview

21 sec-tier findings (6 critical, 11 high, 4 medium) from 19 audit reports by Halborn, Informal Systems, Oak Security, Trail of Bits. Titles in the references table are verbatim from the source reports; use them to route to the exact report for full PoC detail.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the balance/issuance computation paths path lacks the validation/bounding the cited reports identify."
- Pattern key: `rounding-drift | fixed-point math | repeated ops | value leak`
- Interaction scope: `single_contract`
- Primary affected component(s): `balance/issuance computation paths`
- High-signal code keywords: `account, allows, amounts, arbitrarily, assets, because`
- Typical sink / impact: `fund_loss`
- Validation strength: `unassessed` (evidence rows cite source reports; per-finding PoCs not yet re-verified)

#### Valid Bug Signals

- Signal 1: title evidence in cited reports matches the audited component family (balance/issuance computation paths)
- Signal 2: severity consensus across independent auditors (Halborn, Informal Systems, Oak Security, Trail of Bits)
- Signal 3: impact-producing condition stated in source report (fund_loss)

#### False Positive Guards

- Not this bug when: the target chain/module already enforces explicit bounds/limits on the affected path
- Safe if: audited version postdates the fix noted in the source report status
- Requires attacker control of: the inputs named in the cited finding titles (messages, bids, deposits)

### Detection Patterns

#### High-Signal Grep Seeds
```
- account
- allows
- amounts
- arbitrarily
- assets
- because
- beginblocker
- being
- between
- calculation
```

#### Audit Checklist
- [ ] Verify bounded iteration/gas on the affected path
- [ ] Check state-consistency guarantees across the failure paths cited above
- [ ] Compare implementation against the source-report recommendation

### Vulnerability Description

#### Root Cause

The cited reports describe balance/issuance computation paths paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `rounding-drift | fixed-point math | repeated ops | value leak`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `rounding-drift | fixed-point math | repeated ops | value leak | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `rounding-drift | fixed-point math | repeated ops | value leak | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: Multiple rounding issues may cause zero rewards being distributed** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Multiple rounding issues may cause zero rewards being distributed
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Multiple rounding issues may cause zero rewards being distributed
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: Rebalance may not be finalizable because of rounding error** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Rebalance may not be finalizable because of rounding error
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Rebalance may not be finalizable because of rounding error
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: Contract creators can update the gas price into invalid integer value in order to disable the wasmx 's BeginBlocker exec** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Contract creators can update the gas price into invalid integer value in order to disable the wasmx 's BeginBlocker execution
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Contract creators can update the gas price into invalid integer value in order to disable the wasmx 
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

`account, allows, amounts, arbitrarily, assets, because, beginblocker, being, between, calculation, called, cause, causing, check`

### Related Vulnerabilities

- See references table; sibling entries under the same DB category folder
