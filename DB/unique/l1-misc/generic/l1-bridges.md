---
# Core Classification
protocol: generic
chain: generic
category: l1
vulnerability_type: l1_bridge_generic
root_cause_family: see pattern_key

# Pattern Identity
pattern_key: l1-bridge-generic | l1 bridge generic | varies by finding | see references

# Interaction Scope
interaction_scope: varies
involved_contracts:
  - l1 bridge generic

# Attack Vector Details
attack_type: varies
affected_component: l1 bridge generic

# Technical Primitives
primitives:
  - accept
  - action_withdraw
  - address
  - admin
  - arbitrary
  - asset

# Grep / Hunt-Card Seeds
code_keywords:
  - accept
  - action_withdraw
  - address
  - admin
  - arbitrary
  - asset
  - assumptions
  - attacks

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
| [o1] | reports/other-l1_findings/audit-reports-brz-audit-report-brz-bridge-pdf.md | HIGH | Oak Security | Bridge operator has full control over funds and relies on backend service controlling a hot wallet |
| [o2] | reports/other-l1_findings/audit-reports-router-2024-04-30-audit-report-router-asset-bridge-v1-2-pdf.md | CRITICAL | Oak Security | Inability to decode request packet payload due to incorrect indexes results in failed cross-chain requests |
| [o3] | reports/other-l1_findings/audit-reports-router-2024-04-30-audit-report-router-asset-bridge-v1-2-pdf.md | HIGH | Oak Security | Failed cross-chain requests cannot be retried |
| [o4] | reports/other-l1_findings/audit-reports-router-2024-04-30-audit-report-router-asset-bridge-v1-2-pdf.md | HIGH | Oak Security | Unsafe conversion from uint256 to uint128 in asset-bridge middleware |
| [o5] | reports/other-l1_findings/public-audits-reports-omni-network-sigma-prime-omni-network-omni-chain-2-security-assessment-report-v2-1-pdf.md | MEDIUM | auditor | OM2-02 Lost Bridged Funds When Pausing ACTION_WITHDRAW Asset OmniBridgeL1.sol & OmniBridgeNative.sol Status Closed: See Resolution Rating |
| [o6] | reports/other-l1_findings/public-audits-reports-omni-network-sigma-prime-omni-nomina-bridge-contracts-security-assessment-report-v2-1-pdf.md | MEDIUM | NCC Group | Desynchronized Pausing Between Nomina Bridges And Omni Portal Can Lock Funds Asset NominaBridgeL1.sol Status Closed: See Resolution Rating |
| [o7] | reports/other-l1_findings/public-audits-reports-omni-network-sigma-prime-omni-rlusd-brdige-security-assessment-report-v2-0-pdf.md | MEDIUM | NCC Group | Bridge Contract Detailed Findings OMRL- 01 Paused T oken Leads to Loss of Funds Asset Bridge.sol Status Resolved: See Resolution Rating |
| [o8] | reports/other-l1_findings/public-audits-reports-omni-network-sigma-prime-omni-rlusd-brdige-security-assessment-report-v2-0-pdf.md | MEDIUM | NCC Group | Bridge Contract Detailed Findings OMRL- 02 Insu/uniFB03cient Gas ForreceiveToken() Asset Bridge.sol Status Resolved: See Resolution Rating |
| [o9] | reports/other-l1_findings/publications-afx-bridge-zellic-audit-report-pdf.md | HIGH | Zellic | Bridge-address updates can strand pending transfers |
| [o10] | reports/other-l1_findings/publications-afx-bridge-zellic-audit-report-pdf.md | MEDIUM | Zellic | Multiple issues related to the Bridge contract address update functionality |
| [o11] | reports/other-l1_findings/publications-astria-bridge-zellic-audit-report-pdf.md | HIGH | Zellic | Invalid address could break down the bridge withdrawer |
| [o12] | reports/other-l1_findings/publications-astria-bridge-zellic-audit-report-pdf.md | HIGH | Zellic | Arbitrary withdrawal could be executed by bridge admin |
| [o13] | reports/other-l1_findings/publications-astria-bridge-zellic-audit-report-pdf.md | HIGH | Zellic | Withdrawal event could be reused by bridge admin |
| [o14] | reports/other-l1_findings/publications-mina-token-bridge-evm-zellic-audit-report-pdf.md | HIGH | Zellic | The protocol owner can withdraw all funds from the bridge |
| [o15] | reports/other-l1_findings/publications-reviews-2023-12-offchain-labs-arbitrum-token-bridge-creator-securityreview-pdf.md | HIGH | Trail of Bits | L2 token bridge contract deployment can be griefed |
| [o16] | reports/other-l1_findings/publications-reviews-2023-12-offchain-labs-arbitrum-token-bridge-creator-securityreview-pdf.md | MEDIUM | Trail of Bits | Depositing before the token bridge is fully deployed can result in loss of funds |
| [o17] | reports/other-l1_findings/publications-reviews-2026-08-offchain-yield-bearing-bridge-securityreview-pdf.md | HIGH | Trail of Bits | Orbit yield-bearing bridge gateway breaks previous assumptions |
| [o18] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-chiliz-bridge-updates-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | TOKENS CAN BE STUCKED IF THE SAME CHAIN-ID USED IN THE BRIDGE |
| [o19] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-chiliz-bridge-updates-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | HANDLER SHOULD ACCEPT PAYMENTS THROUGH ONLY BRIDGE CONTRACT |
| [o20] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-gains-trade-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | BRIDGENFT CALL CAN BE FRONTRUN |
| [o21] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-unlimited-network-unlimited-leverage-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | UNLIMITEDPRICEFEED IS VULNERABLE TO CROSSCHAIN SIGNATURE REPLAY ATTACKS |
| [o22] | reports/other-l1_findings/publications-reviews-2026-06-telcoin-solanapegstabilityvault-securityreview-pdf.md | MEDIUM | Trail of Bits | Permissionless vault initialization can capture vault control |
| [o23] | reports/other-l1_findings/publications-reviews-2026-06-telcoin-solanapegstabilityvault-securityreview-pdf.md | MEDIUM | Trail of Bits | Closed vault PDA can be reinitialized by an attacker |
| [o24] | reports/other-l1_findings/publicreports-solana-program-audit-goosefx-swap-program-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | TOKENS IN FEE VAULTS LOCKED INDEFINITELY |
| [o25] | reports/other-l1_findings/publicreports-solana-program-audit-phantasia-sports-nft-store-spa-solana-program-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | HARDCODED VAULT ADDRESS |
| [o26] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-haqq-pad-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | TOKEN COUNT INACCURACY IN VAULT FUNDING |
| [o27] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-metapool-staking-pools-aurora-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | VAULT IMPLEMENTATION IS VULNERABLE TO INFLATION ATTACK |
| [q28] | reports/other-l1_findings/audit-reports-asteroid-bridge-2024-06-17-audit-report-asteroid-bridge-v1-0-pdf.md | LOW | Oak Security | Misconfiguration of the bridge chain ID could result in stuck tokens |
| [q29] | reports/other-l1_findings/audit-reports-asteroid-bridge-2024-06-17-audit-report-asteroid-bridge-v1-0-pdf.md | INFO | Oak Security | The protocol owner can arbitrarily disable tokens from being bridged back |
| [q30] | reports/other-l1_findings/audit-reports-helix-bridge-2024-07-04-audit-report-helix-xtoken-v1-0-pdf.md | LOW | Oak Security | Daily limits are not communicated across the bridge  leading to inefficiencies |
| [q31] | reports/other-l1_findings/public-audits-reports-near-review-pdf.md | LOW | NCC Group | Admin T ransfer Pattern Asset rainbow-bridge/contracts/eth/nearbridge/contracts/AdminControlled.sol Status Resolved: See Resolution Rating |
| [q32] | reports/other-l1_findings/public-audits-reports-near-review-pdf.md | LOW | NCC Group | Call Might Change In The Future Asset rainbow-bridge/contracts/eth/nearbridge/contracts/NearBridge.sol Status Resolved: See Resolution Rating |
| [q33] | reports/other-l1_findings/publicauditreports-nm0544b-final-token-bridge-pdf.md | LOW | Nethermind | Missing token balance checks on ERC20 transfer functions (token bridge) |
| [q34] | reports/other-l1_findings/publicauditreports-nm0472-final-renzo-bridge-pdf.md | INFO | Nethermind | Incorrect configuration of token time discount on Arbitrum (Renzo bridge) |
| [q35] | reports/other-l1_findings/publicauditreports-nm0472-final-renzo-bridge-pdf.md | INFO | Nethermind | Incorrect handling of WETH in the sweep() function (Renzo bridge) |
| [q36] | reports/other-l1_findings/publicauditreports-nm0472-final-renzo-bridge-pdf.md | INFO | Nethermind | Incorrect oracle configuration for wstETH token on Base (Renzo bridge) |
| [q37] | reports/other-l1_findings/publicauditreports-nm0472-final-renzo-bridge-pdf.md | INFO | Nethermind | LidoOPValueTransfer unnecessarily grants wstETH allowance to lidoBridge (Renzo bridge) |
## L1 Bridge Generic

**l1-bridge-generic patterns mined from uncited L1 audit reports** - 21 sec-tier findings (3 critical / 11 high / 7 medium) across 13 files from Halborn, NCC Group, Oak Security, Trail of Bits, Zellic, unknown.

### Overview

Titles in the references table are verbatim from source reports. Route to the exact report file for full PoC detail. Validation strength: `unassessed` (evidence rows only).

### Detection Patterns

#### High-Signal Grep Seeds
```
- accept
- action_withdraw
- address
- admin
- arbitrary
- asset
- assumptions
- attacks
```

### Vulnerability Description

#### Root Cause

The cited reports describe l1 bridge generic paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `l1-bridge-generic | l1 bridge generic | varies by finding | see references`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `l1-bridge-generic | l1 bridge generic | varies by finding | see references | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `l1-bridge-generic | l1 bridge generic | varies by finding | see references | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: Inability to decode request packet payload due to incorrect indexes results in failed cross-chain requests** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Inability to decode request packet payload due to incorrect indexes results in failed cross-chain requests
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Inability to decode request packet payload due to incorrect indexes results in failed cross-chain re
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: TOKENS CAN BE STUCKED IF THE SAME CHAIN-ID USED IN THE BRIDGE** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// TOKENS CAN BE STUCKED IF THE SAME CHAIN-ID USED IN THE BRIDGE
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: TOKENS CAN BE STUCKED IF THE SAME CHAIN-ID USED IN THE BRIDGE
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: BRIDGENFT CALL CAN BE FRONTRUN** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// BRIDGENFT CALL CAN BE FRONTRUN
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: BRIDGENFT CALL CAN BE FRONTRUN
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

`accept, action_withdraw, address, admin, arbitrary, asset, assumptions, attacks, backend, bearing`

### Related Vulnerabilities

- Sibling entries under the same category folder
