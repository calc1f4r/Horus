---
# Core Classification
protocol: generic
chain: polkadot
category: dos
vulnerability_type: unbounded_iteration_halt
root_cause_family: resource_exhaustion

# Pattern Identity
pattern_key: unbounded-iteration | pallet loop | attacker-grown storage | block halt

# Interaction Scope
interaction_scope: single_contract
involved_contracts:
  - pallet loops / weight handling

# Attack Vector Details
attack_type: resource_exhaustion
affected_component: pallet loops / weight handling

# Technical Primitives
primitives:
  - account
  - asset_in
  - asset_out
  - attack
  - attacker
  - attackers

# Grep / Hunt-Card Seeds
code_keywords:
  - account
  - asset_in
  - asset_out
  - attack
  - attacker
  - attackers
  - bloat
  - bloated
  - bridge
  - calculation

severity: critical
impact: dos
language: rust
tags:
  - dos
  - l1
  - substrate
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [x1] | reports/substrate-l1_findings/hydradx-c4-2401.md | HIGH | Code4rena | [H-01] An attacker possesses the capability to exhaust the entirety of liquidity within the stable swap pools by manipulating the buy function, speciﬁ |
| [x2] | reports/substrate-l1_findings/hydradx-c4-2401.md | MEDIUM | Code4rena | [M-08] Storage can be bloated with low value liquidity positions |
| [x3] | reports/substrate-l1_findings/phala-c4-2401.md | MEDIUM | Code4rena | [M-02] An attacker can bloat the Pink runtime storage with zero costs |
| [x4] | reports/substrate-l1_findings/chainflip-backend-audits-multisig-kudelski-q1-2022-pdf.md | MEDIUM | Kudelski | Possible DoS Attack in FROST KeyGen |
| [x5] | reports/substrate-l1_findings/composable-audits-solana-ibc-avs-codezen-pdf.md | MEDIUM | Codezen | The state pruning mechanism can suffer DoS depending on the trusting period length |
| [x6] | reports/substrate-l1_findings/audit-reports-bifrost-2024-03-11-audit-report-bifrost-finance-leveraged-staking-v1-0-pdf.md | HIGH | auditor | Static calculation of weights for the claim_reward extrinsic enables DoS attack vector |
| [x7] | reports/substrate-l1_findings/audit-reports-snowbridge-2024-05-24-audit-report-snowbridge-v1-1-pdf.md | CRITICAL | auditor | Attackers can drain relayer funds and hence DoS the bridge by spamming create_agent transactions |
| [x8] | reports/substrate-l1_findings/audit-reports-snowbridge-2024-05-24-audit-report-snowbridge-v1-1-pdf.md | CRITICAL | auditor | Attackers can drain sovereign funds and hence DoS the bridge by spamming registerToken transactions |
| [x9] | reports/substrate-l1_findings/audit-reports-snowbridge-2024-05-24-audit-report-snowbridge-v1-1-pdf.md | HIGH | auditor | The outbound queue continues processing messages even if PalletOperatingMode is Halted |
| [x10] | reports/substrate-l1_findings/audit-reports-zeitgeist-2025-01-02-audit-report-zeitgeist-combinatorial-betting-and-futarchy-security-audit-v1-0-pdf.md | HIGH | auditor | Insuﬃcient iteration limit in hash point decompression |
| [x11] | reports/substrate-l1_findings/audit-reports-zeitgeist-2025-01-02-audit-report-zeitgeist-combinatorial-betting-and-futarchy-security-audit-v1-0-pdf.md | HIGH | auditor | Low account costs could facilitate the exhaustion of parachain resources |
| [x12] | reports/substrate-l1_findings/bifrost-oak-lev-staking.md | HIGH | Oak Security | Static calculation of weights for the claim_reward extrinsic enables DoS attack vector |
| [x25] | reports/substrate-l1_findings/centrifuge-srl-liquidity-pools-2023.md | MEDIUM | SRLabs | October 3, 2023. Issue title 0-weight for message processing enables DoS Tracking [4] |
| [x26] | reports/substrate-l1_findings/hydradx-srl-2405.md | HIGH | SRLabs | Spam vector: An attacker can use a node to submit a large number of unsigned extrinsics, which will be gossiped across the network. This can lead to:  |
| [x27] | reports/substrate-l1_findings/hydradx-srl-2405.md | MEDIUM | SRLabs | An attacker spams the network with unsigned transactions. Location pallet-transaction-multi-payment Attack impact Slowing down the chain |
| [x28] | reports/substrate-l1_findings/manta-veridise-chain.md | MEDIUM | Veridise | Audit Report: Manta Network 4.1 Detailed Description of Issues 13 4.1.3 V-MANC-VUL-003: MantaPay weights calculated with a small database |
| [x29] | reports/substrate-l1_findings/moonbeam-srl-2401.md | MEDIUM | SRLabs | Attack impact Block production could be entirely halted without remediation since XCM implies forced execution |
| [x30] | reports/substrate-l1_findings/acala-c4-2401.md | MEDIUM | Code4rena | Storage can be bloated with low liquidity positions • Low Risk and Non-Critical Issues • 01 Admin is a single point of failure • 02 Consider adding be |
| [x31] | reports/substrate-l1_findings/acala-c4-2401.md | MEDIUM | Code4rena | Storage can be bloated with low liquidity positions Acala https://code4rena.com/reports/2024-03-acala 22 of 52 09/06/2024, 14:14 Submitted by ZanyBonz |
| [x32] | reports/substrate-l1_findings/phala-blockchain-audit-code4rena-phat-contract-runtime-pdf.md | MEDIUM | auditor | An attacker can bloat the Pink runtime storage with zero costs |
| [x33] | reports/substrate-l1_findings/centrifuge-srl-baseline-2022.md | MEDIUM | SRLabs | Out of bounds access could lead to DoS We discovered one case of out of bounds access in the pools pallet [5] |
| [x34] | reports/substrate-l1_findings/centrifuge-srl-baseline-2022.md | MEDIUM | SRLabs | Potential deadlocks leading to DoS SRLabs discovered a potential deadlock condition in the epoch execution |
| [x35] | reports/substrate-l1_findings/centrifuge-srl-baseline-2022.md | MEDIUM | SRLabs | Proper weight calculation When implementing weights for extrinsics, two things should be kept in mind |
| [x36] | reports/substrate-l1_findings/centrifuge-srl-baseline-2022.md | MEDIUM | SRLabs | Spamming attacks Spamming attacks come from unsigned extrinsics as they don’t require a fee to be called |
| [q37] | reports/substrate-l1_findings/astar-srl-2403.md | LOW | SRLabs | Tracking [3] Attack impact Unbounded call length can aid an attacker to cause heap overflow when call data is moved to the vector |
| [q38] | reports/substrate-l1_findings/audit-reports-snowbridge-2025-05-06-audit-report-snowbridge-updates-4-v1-0-pdf.md | INFO | Oak Security | Outdated weight for the submit extrinsic |
| [q39] | reports/substrate-l1_findings/alephbft-tob.md | INFO | Trail of Bits | Blocking I/O in Network trait implementations will block async runtime threads (TOB-ALEPH-008) |
| [q40] | reports/substrate-l1_findings/publications-reviews-alephbft-pdf.md | INFO | Trail of Bits | Blocking I/O in Network trait implementations will block async runtime threads (TOB-ALEPH-008) |
| [q41] | reports/substrate-l1_findings/acala-trailofbits.md | INFO | Trail of Bits | Providing too small a value renders Acala-dapp unresponsive (TOB-ACA-010, denial of service) |
| [q42] | reports/substrate-l1_findings/publications-reviews-acalanetwork-pdf.md | INFO | Trail of Bits | Providing too small a value renders Acala-dapp unresponsive (TOB-ACA-010, denial of service) |
## Dos Unbounded

**Dos unbounded patterns mined from uncited L1 audit reports** - representative of 12 findings mined from 8 L1 audit reports (Code4rena, Codezen, Kudelski, Oak Security, unknown).

### Overview

12 sec-tier findings (2 critical, 6 high, 4 medium) from 8 audit reports by Code4rena, Codezen, Kudelski, Oak Security, unknown. Titles in the references table are verbatim from the source reports; use them to route to the exact report for full PoC detail.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the pallet loops / weight handling path lacks the validation/bounding the cited reports identify."
- Pattern key: `unbounded-iteration | pallet loop | attacker-grown storage | block halt`
- Interaction scope: `single_contract`
- Primary affected component(s): `pallet loops / weight handling`
- High-signal code keywords: `account, asset_in, asset_out, attack, attacker, attackers`
- Typical sink / impact: `dos`
- Validation strength: `unassessed` (evidence rows cite source reports; per-finding PoCs not yet re-verified)

#### Valid Bug Signals

- Signal 1: title evidence in cited reports matches the audited component family (pallet loops / weight handling)
- Signal 2: severity consensus across independent auditors (Code4rena, Codezen, Kudelski, Oak Security, unknown)
- Signal 3: impact-producing condition stated in source report (dos)

#### False Positive Guards

- Not this bug when: the target chain/module already enforces explicit bounds/limits on the affected path
- Safe if: audited version postdates the fix noted in the source report status
- Requires attacker control of: the inputs named in the cited finding titles (messages, bids, deposits)

### Detection Patterns

#### High-Signal Grep Seeds
```
- account
- asset_in
- asset_out
- attack
- attacker
- attackers
- bloat
- bloated
- bridge
- calculation
```

#### Audit Checklist
- [ ] Verify bounded iteration/gas on the affected path
- [ ] Check state-consistency guarantees across the failure paths cited above
- [ ] Compare implementation against the source-report recommendation

### Vulnerability Description

#### Root Cause

The cited reports describe pallet loops / weight handling paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `unbounded-iteration | pallet loop | attacker-grown storage | block halt`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `unbounded-iteration | pallet loop | attacker-grown storage | block halt | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `unbounded-iteration | pallet loop | attacker-grown storage | block halt | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: Attackers can drain relayer funds and hence DoS the bridge by spamming create_agent transactions** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Attackers can drain relayer funds and hence DoS the bridge by spamming create_agent transactions
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Attackers can drain relayer funds and hence DoS the bridge by spamming create_agent transactions
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: Attackers can drain sovereign funds and hence DoS the bridge by spamming registerToken transactions** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Attackers can drain sovereign funds and hence DoS the bridge by spamming registerToken transactions
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Attackers can drain sovereign funds and hence DoS the bridge by spamming registerToken transactions
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: [H-01] An attacker possesses the capability to exhaust the entirety of liquidity within the stable swap pools by manipul** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// [H-01] An attacker possesses the capability to exhaust the entirety of liquidity within the stable swap pools by manipulating the buy function, speciﬁ
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: [H-01] An attacker possesses the capability to exhaust the entirety of liquidity within the stable s
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

`account, asset_in, asset_out, attack, attacker, attackers, bloat, bloated, bridge, calculation, cally, capability, cient, claim_reward`

### Related Vulnerabilities

- See references table; sibling entries under the same DB category folder
