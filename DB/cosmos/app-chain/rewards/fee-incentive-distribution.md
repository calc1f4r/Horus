---
# Core Classification
protocol: generic
chain: cosmos
category: rewards
vulnerability_type: fee_distribution_error
root_cause_family: accounting_error

# Pattern Identity
pattern_key: fee-distribution-gap | distributor module | epoch/settlement | wrong fee split

# Interaction Scope
interaction_scope: single_contract
involved_contracts:
  - fee/incentive distributor modules

# Attack Vector Details
attack_type: logical_error
affected_component: fee/incentive distributor modules

# Technical Primitives
primitives:
  - account
  - acknowledgement
  - adding
  - address
  - allowance
  - allows

# Grep / Hunt-Card Seeds
code_keywords:
  - account
  - acknowledgement
  - adding
  - address
  - allowance
  - allows
  - amount
  - amounts
  - ante
  - apis

severity: critical
impact: fund_loss
language: rust
tags:
  - rewards
  - l1
  - cosmos
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [k1] | reports/cosmos-l1-nodes_findings/audit-reports-amulet-2024-02-07-audit-report-amulet-neutron-pos-strategy-v1-0-pdf.md | HIGH | Oak Security | Potential reconciliation failure due to uncapped fee amount |
| [k2] | reports/cosmos-l1-nodes_findings/audit-reports-amulet-2024-02-07-audit-report-amulet-neutron-pos-strategy-v1-0-pdf.md | HIGH | Oak Security | Rewards are not increased for zero fees or empty fee recipient |
| [k3] | reports/cosmos-l1-nodes_findings/audit-reports-avail-2026-01-15-audit-report-avail-cosmos-and-backend-changes-v1-0-pdf.md | HIGH | Oak Security | Incomplete fee grant implementation |
| [k4] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-12-07-audit-report-comdex-v1-0-pdf.md | HIGH | Oak Security | Base gas fee is insufficient for functions with iteration |
| [k5] | reports/cosmos-l1-nodes_findings/audit-reports-croncat-2023-03-14-audit-report-croncat-cosmwasm-v1-0-pdf.md | HIGH | Oak Security | Updating fees may cause ongoing tasks to error during execution |
| [k6] | reports/cosmos-l1-nodes_findings/audit-reports-dorahacks-2024-03-04-audit-report-dorahacks-quadratic-grant-injective-v1-0-pdf.md | HIGH | Oak Security | Quadratic funding taxation is not incentive-compatible |
| [k7] | reports/cosmos-l1-nodes_findings/audit-reports-dymension-2024-03-08-audit-report-dymension-point-0d-v1-0-pdf.md | CRITICAL | Oak Security | MsgEthereumTx EVM messages can be nested within a MsgExec message to bypass Ante handlers and steal transaction fees or perform a Denial-of-Service at |
| [k8] | reports/cosmos-l1-nodes_findings/audit-reports-ibcx-2023-04-29-audit-report-ibcx-v1-0-pdf.md | CRITICAL | Oak Security | Rebalance finalization may become unachievable due to streaming fee collection |
| [k9] | reports/cosmos-l1-nodes_findings/audit-reports-ibcx-2023-04-29-audit-report-ibcx-v1-0-pdf.md | HIGH | Oak Security | The streaming fee calculation formula returns wrong results for some input values |
| [k10] | reports/cosmos-l1-nodes_findings/audit-reports-ibcx-2023-04-29-audit-report-ibcx-v1-0-pdf.md | HIGH | Oak Security | Streaming fee realization mechanism can be manipulated by the fee collector to maximize profit |
| [k11] | reports/cosmos-l1-nodes_findings/audit-reports-injective-2023-01-20-audit-report-ninja-v1-0-pdf.md | CRITICAL | Oak Security | Fees held by spot vault are locked forever |
| [k12] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-08-01-audit-report-mars-red-bank-updates-v1-0-pdf.md | CRITICAL | Oak Security | Missing denom validation when adding incentives could lead to insufficient funds error |
| [k13] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-08-01-audit-report-mars-red-bank-updates-v1-0-pdf.md | HIGH | Oak Security | Incentive rewards might be distributed to depositors outside the epoch period |
| [k14] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-09-14-audit-report-mars-rover-v2-v1-0-pdf.md | HIGH | Oak Security | Incorrect protocol fee calculation during liquidation |
| [k15] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2022-12-07-audit-report-neutron-v1-0-pdf.md | HIGH | Oak Security | Fee struct could be simplified to avoid manipulations |
| [k16] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2025-03-25-audit-report-neutron-independent-chain-v1-0-pdf.md | HIGH | Oak Security | Failure to update user stake may cause excess reward distribution |
| [k17] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2024-07-03-audit-report-osmosis-smart-accounts-v1-0-pdf.md | HIGH | Oak Security | Excessive transaction fees are incurred |
| [k18] | reports/cosmos-l1-nodes_findings/audit-reports-persistence-2022-01-20-audit-report-persistence-bridge-v1-0-pdf.md | CRITICAL | Oak Security | Retry logic can cause unlimited fees and potentially spend user funds |
| [k19] | reports/cosmos-l1-nodes_findings/audit-reports-structured-2025-12-24-audit-report-structured-cosmwasm-and-solana-updates-v1-0-pdf.md | HIGH | Oak Security | Minted fee amount can be manipulated in both directions |
| [k20] | reports/cosmos-l1-nodes_findings/audit-reports-structured-2025-12-24-audit-report-structured-cosmwasm-and-solana-updates-v1-0-pdf.md | HIGH | Oak Security | Using the vault account as the Wormhole bridge fee payer allows griefing by fee draining |
| [k21] | reports/cosmos-l1-nodes_findings/audit-reports-volta-2024-09-18-audit-report-volta-cosmwasm-v1-0-pdf.md | HIGH | Oak Security | Griefing risk due to unlimited fee grant allowance |
| [k22] | reports/cosmos-l1-nodes_findings/audit-reports-yieldmos-2024-05-17-audit-report-yieldmos-outposts-osmosis-v1-0-pdf.md | CRITICAL | Oak Security | Users can manipulate fee amounts in their favor |
| [k23] | reports/cosmos-l1-nodes_findings/audit-reports-yieldmos-2024-05-17-audit-report-yieldmos-outposts-osmosis-v1-0-pdf.md | CRITICAL | Oak Security | Users can redirect tax fees to their address |
| [k24] | reports/cosmos-l1-nodes_findings/audits-duality-2023-05-16-audit-report-duality-dex-and-incentives-modules-pdf.md | HIGH | Informal Systems | Tick and Fee inputs are not validated |
| [k25] | reports/cosmos-l1-nodes_findings/audits-neutron-2023-04-06-audit-report-neutron-sdk-dao-wasmd-tge-pdf.md | HIGH | Informal Systems | Neutron Non-validated IBC acknowledgement/timeout fees can lead to drainage of relayers funds and spamming of the network |
| [k51] | reports/cosmos-l1-nodes_findings/audits-neutron-2023-11-11-audit-report-neutron-duality-v0-5-0-integration-of-cosmos-sdk-0-47-pdf.md | CRITICAL | Informal Systems | Unbounded iteration over Incentives stakes may lead to chain halt |
| [k52] | reports/cosmos-l1-nodes_findings/audits-neutron-2023-11-11-audit-report-neutron-duality-v0-5-0-integration-of-cosmos-sdk-0-47-pdf.md | HIGH | Informal Systems | Misleading Incentives module user-facing and developer documentation |
| [k53] | reports/cosmos-l1-nodes_findings/audits-neutron-2023-11-11-audit-report-neutron-duality-v0-5-0-integration-of-cosmos-sdk-0-47-pdf.md | HIGH | Informal Systems | Tick and Fee inputs are not completely validated |
| [k54] | reports/cosmos-l1-nodes_findings/publications-reviews-umee-pdf.md | HIGH | Trail of Bits | Oracle price-feeder is vulnerable to manipulation by a single malicious price feed |
| [k55] | reports/cosmos-l1-nodes_findings/publications-reviews-umee-pdf.md | MEDIUM | Trail of Bits | price-feeder is at risk of rate limiting by public APIs |
| [k56] | reports/cosmos-l1-nodes_findings/publications-reviews-umee-pdf.md | MEDIUM | Trail of Bits | Insecure storage of price-feeder keyring passwords |
| [k57] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-boostylabs-tricorn-bridge-server-golang-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | USERS CANNOT WITHDRAW FUNDS DUE TO HARD-CODED COMMISSION VALUES |
| [k58] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | BID FEE IS NOT SENT |
| [k59] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | LIQUIDATOR FEE IS NOT SENT |
| [k60] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-sienna-network-amm-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | UNRESTRICTED CHANGES IN FEE RATES LEAD TO TOKENS LOSS / DOS |
| [k61] | reports/cosmos-l1-nodes_findings/audits-anoma-namada-q2-2025-e2e-shielded-transaction-balance-consistency-audit-report-final-pdf.md | MEDIUM | Informal Systems | Namada T ransactions doing masp fee payment may be executed an unbounded number of times for free |
| [k62] | reports/cosmos-l1-nodes_findings/audits-injective-informal-report-injective-audit-202106-pdf.md | HIGH | Informal Systems | Injective Protocol Audit IF-INJECTIVE-11 Price feed does not validate prices, may crash consensus #331 Status: resolved (as of June 15, 2021) |
| [q63] | reports/cosmos-l1-nodes_findings/audits-axelar-2023-08-04-audit-report-axelar-axelarnet-pdf.md | LOW | Informal Systems | IF-AXELAR-03: Simplify Relayers setup using FeeGrant |

## Fee Incentive Distribution

**Fee incentive distribution patterns mined from uncited L1 audit reports** - representative of 36 findings mined from 25 L1 audit reports (Halborn, Informal Systems, Oak Security, Trail of Bits).

### Overview

36 sec-tier findings (8 critical, 24 high, 4 medium) from 25 audit reports by Halborn, Informal Systems, Oak Security, Trail of Bits. Titles in the references table are verbatim from the source reports; use them to route to the exact report for full PoC detail.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the fee/incentive distributor modules path lacks the validation/bounding the cited reports identify."
- Pattern key: `fee-distribution-gap | distributor module | epoch/settlement | wrong fee split`
- Interaction scope: `single_contract`
- Primary affected component(s): `fee/incentive distributor modules`
- High-signal code keywords: `account, acknowledgement, adding, address, allowance, allows`
- Typical sink / impact: `fund_loss`
- Validation strength: `unassessed` (evidence rows cite source reports; per-finding PoCs not yet re-verified)

#### Valid Bug Signals

- Signal 1: title evidence in cited reports matches the audited component family (fee/incentive distributor modules)
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
- acknowledgement
- adding
- address
- allowance
- allows
- amount
- amounts
- ante
- apis
```

#### Audit Checklist
- [ ] Verify bounded iteration/gas on the affected path
- [ ] Check state-consistency guarantees across the failure paths cited above
- [ ] Compare implementation against the source-report recommendation

### Vulnerability Description

#### Root Cause

The cited reports describe fee/incentive distributor modules paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `fee-distribution-gap | distributor module | epoch/settlement | wrong fee split`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `fee-distribution-gap | distributor module | epoch/settlement | wrong fee split | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `fee-distribution-gap | distributor module | epoch/settlement | wrong fee split | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: MsgEthereumTx EVM messages can be nested within a MsgExec message to bypass Ante handlers and steal transaction fees or ** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// MsgEthereumTx EVM messages can be nested within a MsgExec message to bypass Ante handlers and steal transaction fees or perform a Denial-of-Service at
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: MsgEthereumTx EVM messages can be nested within a MsgExec message to bypass Ante handlers and steal 
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: Rebalance finalization may become unachievable due to streaming fee collection** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Rebalance finalization may become unachievable due to streaming fee collection
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Rebalance finalization may become unachievable due to streaming fee collection
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: Fees held by spot vault are locked forever** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Fees held by spot vault are locked forever
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Fees held by spot vault are locked forever
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

`account, acknowledgement, adding, address, allowance, allows, amount, amounts, ante, apis, attack, avoid, base, become`

### Related Vulnerabilities

- See references table; sibling entries under the same DB category folder
