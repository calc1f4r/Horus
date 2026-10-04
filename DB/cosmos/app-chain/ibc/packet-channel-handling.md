---
# Core Classification
protocol: generic
chain: cosmos
category: ibc
vulnerability_type: packet_channel_validation
root_cause_family: missing_validation

# Pattern Identity
pattern_key: packet-handling-gap | IBC module | malformed or replayed packet | stuck transfers / chain halt

# Interaction Scope
interaction_scope: cross_chain
involved_contracts:
  - IBC module (ics02/ics20/ics26, ICA host/controller)

# Attack Vector Details
attack_type: input_validation_bypass
affected_component: IBC module (ics02/ics20/ics26, ICA host/controller)

# Technical Primitives
primitives:
  - able
  - accessed
  - account
  - accounts
  - acknowledgement
  - active

# Grep / Hunt-Card Seeds
code_keywords:
  - able
  - accessed
  - account
  - accounts
  - acknowledgement
  - active
  - address
  - arbitrary
  - artifacts
  - astro

severity: critical
impact: fund_loss
language: rust
tags:
  - ibc
  - l1
  - cosmos
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [k1] | reports/cosmos-l1-nodes_findings/audit-reports-amulet-2024-02-07-audit-report-amulet-neutron-pos-strategy-v1-0-pdf.md | CRITICAL | Oak Security | Interchain accounts cannot be accessed if the channel closes |
| [k2] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2023-02-14-audit-report-astroport-ibc-v1-0-pdf.md | HIGH | Oak Security | Incorrect permissioning of IbcExecuteProposal execution leads to failure of proposal execution and elevated owner privileges |
| [k3] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2024-05-22-audit-report-astroport-hub-neutron-migration-v1-0-pdf.md | HIGH | Oak Security | IBC transfers can be grieved, preventing old ASTRO tokens from being burned |
| [k4] | reports/cosmos-l1-nodes_findings/audit-reports-avail-2026-01-15-audit-report-avail-cosmos-and-backend-changes-v1-0-pdf.md | HIGH | Oak Security | Fetching vote extension events without timeouts can stall consensus |
| [k5] | reports/cosmos-l1-nodes_findings/audit-reports-avail-2026-01-15-audit-report-avail-cosmos-and-backend-changes-v1-0-pdf.md | HIGH | Oak Security | Replayed DSG messages crash CA nodes through closed channel writes |
| [k6] | reports/cosmos-l1-nodes_findings/audit-reports-babylon-2025-06-12-audit-report-babylon-v1-0-pdf.md | HIGH | Oak Security | Missing message size enforcement in DeliverTx enables oversized IBC messages payload injection |
| [k7] | reports/cosmos-l1-nodes_findings/audit-reports-cosmos-2023-06-23-audit-report-cosmos-interchain-security-v1-0-pdf.md | HIGH | Oak Security | The provider chain halts on failure to send packets to a single consumer chain |
| [k8] | reports/cosmos-l1-nodes_findings/audit-reports-cosmwasm-2023-10-17-audit-report-wasmd-v1-0-pdf.md | HIGH | Oak Security | IBC Querier plugin's unbounded loop could lead to DoS |
| [k9] | reports/cosmos-l1-nodes_findings/audit-reports-milkyway-2024-12-16-audit-report-milkyway-celestia-restaking-v1-0-pdf.md | CRITICAL | Oak Security | Malicious chains can send malicious packets to steal insurance funds |
| [k10] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2022-12-07-audit-report-neutron-v1-0-pdf.md | CRITICAL | Oak Security | An error triggered during the handling of an Ack IBC message will make the channel unusable and spam the network |
| [k11] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2022-12-07-audit-report-neutron-v1-0-pdf.md | CRITICAL | Oak Security | IBC events loop in Sudo handler could drain relayer's funds |
| [k12] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2022-12-07-audit-report-neutron-v1-0-pdf.md | HIGH | Oak Security | Attackers are able to spam the network with IBC messages using the ibc-transfer module |
| [k13] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2022-12-07-audit-report-neutron-v1-0-pdf.md | HIGH | Oak Security | Unbounded iteration in ValidateBasic may cause node timeout |
| [k14] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2022-12-07-audit-report-neutron-v1-0-pdf.md | HIGH | Oak Security | Attackers could steal funds from the ibc-transfer contract |
| [k15] | reports/cosmos-l1-nodes_findings/audit-reports-persistence-2022-01-20-audit-report-persistence-bridge-v1-0-pdf.md | CRITICAL | Oak Security | TLS connection to CASP is prone to man-in-the-middle attacks |
| [k16] | reports/cosmos-l1-nodes_findings/audit-reports-persistence-2024-01-26-audit-report-pstake-native-auto-compounding-and-rebalancing-v1-0-pdf.md | CRITICAL | Oak Security | Risk of gas exhaustion for unbounded ICA messages |
| [k17] | reports/cosmos-l1-nodes_findings/audit-reports-stride-2022-09-26-audit-report-stride-v1-0-pdf.md | HIGH | Oak Security | RegisterHostZone does not ensure that HostDenom and IbcDenom are unique which may introduce conflicts when returning a hostzone from these values |
| [k18] | reports/cosmos-l1-nodes_findings/audits-anoma-2024-08-16-ibc-and-masp-integrations-final-report-pdf.md | CRITICAL | Informal Systems | Incorrect Balance Updates in IBC Transfer Handling |
| [k19] | reports/cosmos-l1-nodes_findings/audits-cosmos-hub-2023-02-10-audit-report-ics-replicated-security-pdf.md | MEDIUM | Informal Systems | Interchain Security v.1.0 Panics on failure to send IBC packets |
| [k20] | reports/cosmos-l1-nodes_findings/audits-mars-protocol-2023-02-03-audit-report-mars-protocol-envoy-module-pdf.md | HIGH | Informal Systems | Mars Protocol Envoy module Iterate over all Interchain Accounts |
| [k21] | reports/cosmos-l1-nodes_findings/audits-mars-protocol-2023-02-03-audit-report-mars-protocol-envoy-module-pdf.md | MEDIUM | Informal Systems | Mars Protocol Envoy module Mars Hub as Interchain Account Host chain |
| [k22] | reports/cosmos-l1-nodes_findings/audits-neutron-2023-04-06-audit-report-neutron-sdk-dao-wasmd-tge-pdf.md | HIGH | Informal Systems | Neutron Non-validated IBC acknowledgement/timeout fees can lead to drainage of relayers funds and spamming of the network |
| [k23] | reports/cosmos-l1-nodes_findings/audits-neutron-2023-11-11-audit-report-neutron-duality-v0-5-0-integration-of-cosmos-sdk-0-47-pdf.md | CRITICAL | Informal Systems | Stealing of arbitrary funds via IBC swaps |
| [k24] | reports/cosmos-l1-nodes_findings/audits-osmosis-2023-30-10-audit-fee-abstraction-module-by-notional-pdf.md | HIGH | Informal Systems | Outdated Exchange Rate Risk Due to Potential IBC Relayer Delays |
| [k25] | reports/cosmos-l1-nodes_findings/audits-osmosis-2023-30-10-audit-fee-abstraction-module-by-notional-pdf.md | HIGH | Informal Systems | Unspecified recovery address for Crosschain-swaps IBC transfer |
| [k51] | reports/cosmos-l1-nodes_findings/audits-stride-2022-11-30-audit-report-stride-stakeibc-icacallbacks-pdf.md | MEDIUM | Informal Systems | Stride StakeIBC and ICACallbacks Modules Failure to send IBC packets may lead to user funds freeze |
| [k52] | reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-08-wasm-halborn-audit-report-pdf.md | MEDIUM | Halborn | CONSENSUS STATE IS NOT SET IN THE WASM LIGHTCLIENT |
| [k53] | reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-08-wasm-halborn-audit-report-pdf.md | MEDIUM | Halborn | THE STATUS OF CLIENT STATE IS MARKED AS ACTIVE BY DEFAULT |
| [k54] | reports/cosmos-l1-nodes_findings/interchain-security-docs-audits-informal-ics-2023-pdf.md | MEDIUM | Informal Systems | Interchain Security v.1.0 Panics on failure to send IBC packets |
| [k55] | reports/cosmos-l1-nodes_findings/publications-celestia-packet-forward-middleware-zellic-audit-report-pdf.md | MEDIUM | Zellic | There is no upper limit to the time-out on PFM packets |
| [k56] | reports/cosmos-l1-nodes_findings/publications-ibc-eureka-zellic-audit-report-pdf.md | CRITICAL | Zellic | Untrusted input is used as trusted consensus state |
| [k57] | reports/cosmos-l1-nodes_findings/publications-ibc-eureka-zellic-audit-report-pdf.md | CRITICAL | Zellic | IBC does not work with chains that generate subsecond blocks |
| [k58] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-a41-supernova-cosmos-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | MISSING VALIDATION ON THE HOST DENOM AND IBC DENOM |
| [k59] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-a41-supernova-cosmos-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | MISSING FUNCTIONALITY WHEN CONNECTION IS CLOSED |
| [k60] | reports/cosmos-l1-nodes_findings/audits-ibc-go-report-pdf.md | HIGH | auditor | Malicious IBC app module can claim any port or channel capability |
| [k61] | reports/cosmos-l1-nodes_findings/audits-ibc-go-report-pdf.md | HIGH | auditor | Model-based Testing for Token Transfer Set of new artifacts to facilitate rigorous testing Informative Code IF-IBC-14 Panic on receiving multi-chain d |
| [q62] | reports/cosmos-l1-nodes_findings/audit-reports-dymension-2024-04-30-audit-report-dymension-point-1d-stream-2-virtual-frontier-contract-v1-1-pdf.md | LOW | Oak Security | Attackers can DoS the chain by sending multiple IBC coins |
| [q63] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-1-pdf.md | LOW | Oak Security | Burning an IBC voucher does not burn the underlying tokens in escrow on the source chain |
| [q64] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-1-pdf.md | INFO | Oak Security | The current owner proposes a new owner address that is validated and lowercased. 2. The new owner account claims ownership  which applies the configur |
| [q65] | reports/cosmos-l1-nodes_findings/audits-axelar-2023-08-04-audit-report-axelar-axelarnet-pdf.md | INFO | Informal Systems | IF-AXELAR-06: IBC wrapping implementation improvement |

## Ibc Packet Channel Handling

**Ibc packet channel handling patterns mined from uncited L1 audit reports** - representative of 36 findings mined from 25 L1 audit reports (Halborn, Informal Systems, Oak Security, Zellic, unknown).

### Overview

36 sec-tier findings (10 critical, 17 high, 9 medium) from 25 audit reports by Halborn, Informal Systems, Oak Security, Zellic, unknown. Titles in the references table are verbatim from the source reports; use them to route to the exact report for full PoC detail.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the IBC module (ics02/ics20/ics26, ICA host/controller) path lacks the validation/bounding the cited reports identify."
- Pattern key: `packet-handling-gap | IBC module | malformed or replayed packet | stuck transfers / chain halt`
- Interaction scope: `cross_chain`
- Primary affected component(s): `IBC module (ics02/ics20/ics26, ICA host/controller)`
- High-signal code keywords: `able, accessed, account, accounts, acknowledgement, active`
- Typical sink / impact: `fund_loss`
- Validation strength: `unassessed` (evidence rows cite source reports; per-finding PoCs not yet re-verified)

#### Valid Bug Signals

- Signal 1: title evidence in cited reports matches the audited component family (IBC module (ics02/ics20/ics26, ICA host/controller))
- Signal 2: severity consensus across independent auditors (Halborn, Informal Systems, Oak Security, Zellic, unknown)
- Signal 3: impact-producing condition stated in source report (fund_loss)

#### False Positive Guards

- Not this bug when: the target chain/module already enforces explicit bounds/limits on the affected path
- Safe if: audited version postdates the fix noted in the source report status
- Requires attacker control of: the inputs named in the cited finding titles (messages, bids, deposits)

### Detection Patterns

#### High-Signal Grep Seeds
```
- able
- accessed
- account
- accounts
- acknowledgement
- active
- address
- arbitrary
- artifacts
- astro
```

#### Audit Checklist
- [ ] Verify bounded iteration/gas on the affected path
- [ ] Check state-consistency guarantees across the failure paths cited above
- [ ] Compare implementation against the source-report recommendation

### Vulnerability Description

#### Root Cause

The cited reports describe IBC module (ics02/ics20/ics26, ICA host/controller) paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `packet-handling-gap | IBC module | malformed or replayed packet | stuck transfers / chain halt`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `packet-handling-gap | IBC module | malformed or replayed packet | stuck transfers / chain halt | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `packet-handling-gap | IBC module | malformed or replayed packet | stuck transfers / chain halt | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: Interchain accounts cannot be accessed if the channel closes** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Interchain accounts cannot be accessed if the channel closes
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Interchain accounts cannot be accessed if the channel closes
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: Malicious chains can send malicious packets to steal insurance funds** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Malicious chains can send malicious packets to steal insurance funds
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Malicious chains can send malicious packets to steal insurance funds
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: An error triggered during the handling of an Ack IBC message will make the channel unusable and spam the network** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// An error triggered during the handling of an Ack IBC message will make the channel unusable and spam the network
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: An error triggered during the handling of an Ack IBC message will make the channel unusable and spam
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

`able, accessed, account, accounts, acknowledgement, active, address, arbitrary, artifacts, astro, attackers, attacks, balance, based`

### Related Vulnerabilities

- See references table; sibling entries under the same DB category folder
