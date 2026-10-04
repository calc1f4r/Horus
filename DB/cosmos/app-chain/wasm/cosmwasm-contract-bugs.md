---
# Core Classification
protocol: generic
chain: cosmos
category: cosmwasm
vulnerability_type: contract_logic_error
root_cause_family: logic_error

# Pattern Identity
pattern_key: handler-logic-gap | cosmwasm contract | user message | wrong state transition

# Interaction Scope
interaction_scope: single_contract
involved_contracts:
  - CosmWasm smart contracts (ExecuteMsg handlers)

# Attack Vector Details
attack_type: logical_error
affected_component: CosmWasm smart contracts (ExecuteMsg handlers)

# Technical Primitives
primitives:
  - airdrop
  - antehandler
  - arbitrary
  - attempts
  - authorization
  - avoid

# Grep / Hunt-Card Seeds
code_keywords:
  - airdrop
  - antehandler
  - arbitrary
  - attempts
  - authorization
  - avoid
  - aware
  - beginblocker
  - binaries
  - binding

severity: critical
impact: fund_loss
language: rust
tags:
  - cosmwasm
  - l1
  - cosmos
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [k1] | reports/cosmos-l1-nodes_findings/audit-reports-autonomy-2023-03-06-audit-report-autonomy-osmosis-v1-1-pdf.md | HIGH | Oak Security | stakes vector could exceed the CosmWasm VM memory limit when loaded |
| [k2] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-12-07-audit-report-comdex-v1-0-pdf.md | CRITICAL | Oak Security | CosmWasm - State query binding can perform a GRPC call to an arbitrary URL |
| [k3] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-12-07-audit-report-comdex-v1-0-pdf.md | CRITICAL | Oak Security | CosmWasm - Deposited funds of other denom will be stuck in the contract |
| [k4] | reports/cosmos-l1-nodes_findings/audit-reports-cosmwasm-2023-10-17-audit-report-wasmd-v1-0-pdf.md | CRITICAL | Oak Security | Gzipped wasm binaries with invalid CRC could be used to DOS the chain |
| [k5] | reports/cosmos-l1-nodes_findings/audit-reports-injective-2023-01-20-audit-report-injective-v1-0-pdf.md | CRITICAL | Oak Security | Contract creators can update the gas price into invalid integer value in order to disable the wasmx 's BeginBlocker execution |
| [k6] | reports/cosmos-l1-nodes_findings/audit-reports-injective-2023-01-20-audit-report-injective-v1-0-pdf.md | HIGH | Oak Security | registry contract and wasmx module are not aware of registered contract migrations |
| [k7] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2022-02-17-audit-report-mars-v1-0-pdf.md | CRITICAL | Oak Security | Malicious smart contracts can avoid liquidation attempts |
| [k8] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-02-03-audit-report-mars-periphery-v1-0-pdf.md | HIGH | Oak Security | Smart contracts holding tokens on Terra classic cannot claim their airdrop |
| [k9] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-2-pdf.md | HIGH | Oak Security | Any CosmWasm contract can add cron schedules, bypassing authorization |
| [k10] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-2-pdf.md | HIGH | Oak Security | nil DistributionKeeper passed to the wasm keeper prevents distribution messages in CosmWasm contracts |
| [k11] | reports/cosmos-l1-nodes_findings/audit-reports-structured-2025-12-24-audit-report-structured-cosmwasm-and-solana-updates-v1-0-pdf.md | HIGH | Oak Security | Existing MaxBTC issuer contract migration does not transfer current deposits |
| [k12] | reports/cosmos-l1-nodes_findings/audits-neutron-2023-04-06-audit-report-neutron-sdk-dao-wasmd-tge-pdf.md | CRITICAL | Informal Systems | Neutron Interchain Queries register and remove logic can be exploited to steal smart contract's deposit and stop it from creating the queries |
| [k13] | reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-08-wasm-halborn-audit-report-pdf.md | MEDIUM | Halborn | CONSENSUS STATE IS NOT SET IN THE WASM LIGHTCLIENT |
| [k14] | reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-08-wasm-halborn-audit-report-pdf.md | MEDIUM | Halborn | WASMVM PARAMETERS ARE NOT SET IN THE CONTRACT INTERACTIONS |
| [k15] | reports/cosmos-l1-nodes_findings/publications-babylon-genesis-chain-zellic-audit-report-pdf.md | CRITICAL | Zellic | CosmWasm Stargate/Any messages bypass AnteHandler checks |
| [k16] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-umee-wasm-integration-cosmos-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | VULNERABLE WASM SMART CONTRACT LEADS TO CHAIN HALT |
| [z17] | reports/cosmos-l1-nodes_findings/audits-agoric-informal-agoric-report-phase1-pdf.md | MEDIUM | Informal Systems | Unrestricted number of vat slots per vat |
| [z18] | reports/cosmos-l1-nodes_findings/audits-agoric-informal-agoric-report-phase1-pdf.md | MEDIUM | Informal Systems | Possible cycles in promise resolutions |
| [z19] | reports/cosmos-l1-nodes_findings/audits-agoric-informal-agoric-report-phase1-pdf.md | MEDIUM | Informal Systems | Possible loss of vat termination events |
| [z20] | reports/cosmos-l1-nodes_findings/audits-agoric-informal-agoric-report-phase1-pdf.md | MEDIUM | Informal Systems | Inconsistencies in vat bookkeeping |
| [z21] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | SOME PRICE SOURCES DO NOT PREVENT MANIPULATION OF ASSETS PRICE IN THE ORACLE |
| [z22] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | LIQUIDATION CAN TOTALLY CORRUPT THE VALUES OF TOTAL DEBT  INDEXES AND RATES |
| [z23] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | SLASH EVENTS CAN BE OVERWRITTEN WHEN TRANSFERRING MARS TOKENS |
| [z24] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | MARS TOKENS CAN GET LOCKED IN CONTRACT WHEN UNSTAKING |
| [z25] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | TOTAL MARS FOR CLAIMERS IS MISCALCULATED WHEN TRANSFERRING MARS TOKENS |
| [z26] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | TOKENS GET LOCKED WHEN TRANSFERRING TO UPPER-CASE ADDRESSES |
| [z27] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | POSSIBILITY TO LIQUIDATE WHEN COLLATERAL ASSET IS UNSET |
| [z28] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | NO MINIMUM THRESHOLD FOR SOME PARAMETERS OF COUNCIL CONFIGURATION |
| [z29] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | LOAN LIMIT CAN BE UPDATED FOR USERS WITH COLLATERALIZED DEBTS |
| [z30] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | RESTRICTION TO NOT SWAP MARS TOKENS CAN BE BYPASSED |
| [z31] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | POSSIBILITY TO DEPOSIT  REPAY OR LIQUIDATE WITH NATIVE COINS NOT REGISTERED IN STORAGE |
| [z32] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-fields-of-mars-cosmwasm-smart-contract-security-audit-final-pdf.md | MEDIUM | Halborn | CONFIG PARAMETERS VALUE CAN BE CHANGED UNRESTRICTEDLY |
| [q33] | reports/cosmos-l1-nodes_findings/publications-pyth-network-cosmwasm-zellic-audit-report-pdf.md | LOW | Zellic | DetailedFindings 3.1 Newgovernancesourcemaybreaktransferfunctionality • Target:CosmWasm • Category:CodingMistakes • Likelihood:Low • |
| [q34] | reports/cosmos-l1-nodes_findings/publications-pyth-network-cosmwasm-zellic-audit-report-pdf.md | INFO | Zellic | Zellic 9 PythDataAssociation 3.2 OpenTODOsshouldbeaddressed • Target:CosmWasm • Category:CodingMistakes • Likelihood:N/A • |

## Cosmwasm Contract

**Cosmwasm contract patterns mined from uncited L1 audit reports** - representative of 16 findings mined from 12 L1 audit reports (Halborn, Informal Systems, Oak Security, Zellic).

### Overview

16 sec-tier findings (8 critical, 6 high, 2 medium) from 12 audit reports by Halborn, Informal Systems, Oak Security, Zellic. Titles in the references table are verbatim from the source reports; use them to route to the exact report for full PoC detail.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the CosmWasm smart contracts (ExecuteMsg handlers) path lacks the validation/bounding the cited reports identify."
- Pattern key: `handler-logic-gap | cosmwasm contract | user message | wrong state transition`
- Interaction scope: `single_contract`
- Primary affected component(s): `CosmWasm smart contracts (ExecuteMsg handlers)`
- High-signal code keywords: `airdrop, antehandler, arbitrary, attempts, authorization, avoid`
- Typical sink / impact: `fund_loss`
- Validation strength: `unassessed` (evidence rows cite source reports; per-finding PoCs not yet re-verified)

#### Valid Bug Signals

- Signal 1: title evidence in cited reports matches the audited component family (CosmWasm smart contracts (ExecuteMsg handlers))
- Signal 2: severity consensus across independent auditors (Halborn, Informal Systems, Oak Security, Zellic)
- Signal 3: impact-producing condition stated in source report (fund_loss)

#### False Positive Guards

- Not this bug when: the target chain/module already enforces explicit bounds/limits on the affected path
- Safe if: audited version postdates the fix noted in the source report status
- Requires attacker control of: the inputs named in the cited finding titles (messages, bids, deposits)

### Detection Patterns

#### High-Signal Grep Seeds
```
- airdrop
- antehandler
- arbitrary
- attempts
- authorization
- avoid
- aware
- beginblocker
- binaries
- binding
```

#### Audit Checklist
- [ ] Verify bounded iteration/gas on the affected path
- [ ] Check state-consistency guarantees across the failure paths cited above
- [ ] Compare implementation against the source-report recommendation

### Vulnerability Description

#### Root Cause

The cited reports describe CosmWasm smart contracts (ExecuteMsg handlers) paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `handler-logic-gap | cosmwasm contract | user message | wrong state transition`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `handler-logic-gap | cosmwasm contract | user message | wrong state transition | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `handler-logic-gap | cosmwasm contract | user message | wrong state transition | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: CosmWasm - State query binding can perform a GRPC call to an arbitrary URL** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// CosmWasm - State query binding can perform a GRPC call to an arbitrary URL
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: CosmWasm - State query binding can perform a GRPC call to an arbitrary URL
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: CosmWasm - Deposited funds of other denom will be stuck in the contract** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// CosmWasm - Deposited funds of other denom will be stuck in the contract
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: CosmWasm - Deposited funds of other denom will be stuck in the contract
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: Gzipped wasm binaries with invalid CRC could be used to DOS the chain** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Gzipped wasm binaries with invalid CRC could be used to DOS the chain
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Gzipped wasm binaries with invalid CRC could be used to DOS the chain
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

`airdrop, antehandler, arbitrary, attempts, authorization, avoid, aware, beginblocker, binaries, binding, bypass, bypassing, call, cannot`

### Related Vulnerabilities

- See references table; sibling entries under the same DB category folder
