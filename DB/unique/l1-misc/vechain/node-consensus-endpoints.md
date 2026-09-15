---
# Core Classification
protocol: generic
chain: vechain
category: vechain
vulnerability_type: vechain_consensus_nodes
root_cause_family: see pattern_key

# Pattern Identity
pattern_key: vechain-consensus-nodes | vechain consensus nodes | varies by finding | see references

# Interaction Scope
interaction_scope: varies
involved_contracts:
  - vechain consensus nodes

# Attack Vector Details
attack_type: varies
affected_component: vechain consensus nodes

# Technical Primitives
primitives:
  - accounting
  - after
  - another
  - attacker
  - both
  - bricked

# Grep / Hunt-Card Seeds
code_keywords:
  - accounting
  - after
  - another
  - attacker
  - both
  - bricked
  - broken
  - case

severity: high
impact: varies
language: varies
tags:
  - vechain
  - l1
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [v1] | reports/vechain-l1_findings/59386-sc-high-fund-freeze-from-double-stake-subtraction-when-validator-exits.md | HIGH | Immunefi (humanitia) | sc high fund freeze from double stake subtraction when validator exits&#x20; |
| [v2] | reports/vechain-l1_findings/59723-sc-high-double-decrease-after-exit-validator-exited-leads-to-underflow-and-permanent-freeze.md | HIGH | Immunefi (yesofcourse) | sc high double decrease after exit validator exited leads to underflow and permanent freeze |
| [v3] | reports/vechain-l1_findings/59742-sc-high-user-funds-get-stucked-in-the-contract-when-validators-exits.md | HIGH | Immunefi (warden) | sc high user funds get stucked in the contract when validators exits&#x20; |
| [v4] | reports/vechain-l1_findings/59756-sc-high-exiting-delegators-stakes-can-be-bricked-permanently-by-the-validator-signaling-an-exi.md | HIGH | Immunefi (flacko) | sc high exiting delegators stakes can be bricked permanently by the validator signaling an exit after them in the same period |
| [v5] | reports/vechain-l1_findings/60080-sc-high-unstake-exit-requests-can-either-lock-funds-or-silently-double-deduct-effective-stake.md | HIGH | Immunefi (n0fr33w1f14u) | sc high unstake exit requests can either lock funds or silently double deduct effective stake after validator exit |
| [v6] | reports/vechain-l1_findings/60125-sc-high-moving-delegations-from-one-validator-to-another-validator-will-not-be-possible-in-exi.md | HIGH | Immunefi (oxrex) | sc high moving delegations from one validator to another validator will not be possible in exit case for validator 1 |
| [v7] | reports/vechain-l1_findings/60210-sc-high-during-a-validator-exit-users-will-be-unable-to-unstake-due-to-underflow.md | HIGH | Immunefi (oxrex) | sc high during a validator exit users will be unable to unstake due to underflow |
| [v8] | reports/vechain-l1_findings/60265-sc-high-the-attacker-can-still-claim-rewards-after-exiting-from-validator.md | HIGH | Immunefi (aman) | sc high the attacker can still claim rewards after exiting from validator |
| [v9] | reports/vechain-l1_findings/60282-sc-high-last-delegators-for-an-exited-validator-may-be-dosed-from-re-delegating-or-unstaking-d.md | HIGH | Immunefi (prk0) | sc high last delegators for an exited validator may be dosed from re delegating or unstaking due to incorrect accounting of period effective stake |
| [v10] | reports/vechain-l1_findings/60334-sc-high-unstake-permanently-reverts-when-validator-exits-after-delegator-exit-double-decrease.md | HIGH | Immunefi (Diavol0) | sc high unstake permanently reverts when validator exits after delegator exit double decrease of effective stake&#x20; |
| [v11] | reports/vechain-l1_findings/60373-sc-high-incorrect-effective-stake-decrement-when-validator-exits-causes-permanent-freezing-of.md | HIGH | Immunefi (x0xmechanic) | sc high incorrect effective stake decrement when validator exits causes permanent freezing of user stake |
| [v12] | reports/vechain-l1_findings/60470-sc-high-double-decrease-of-validator-stake-in-stargate-sol.md | HIGH | Immunefi (FrontRunner) | sc high double decrease of validator stake in stargate sol |
| [v13] | reports/vechain-l1_findings/60534-sc-high-a-delegator-who-signals-exit-and-waits-for-the-validator-to-finish-its-period-can-no-l.md | HIGH | Immunefi (demonhat) | sc high a delegator who signals exit and waits for the validator to finish its period can no longer withdraw in the unstake function causing permanent |
| [v14] | reports/vechain-l1_findings/60539-sc-medium-critical-withdraw-dos-zero-reward-validators-cause-permanent-user-fund-lock-via-brok.md | MEDIUM | Immunefi (uzemy) | sc medium critical withdraw dos zero reward validators cause permanent user fund lock via broken reward claim logic |
| [v15] | reports/vechain-l1_findings/60548-sc-high-an-exited-delegator-who-has-not-unstaked-or-delegated-to-a-validator-will-be-dos-ed-if.md | HIGH | Immunefi (HalalAudits) | sc high an exited delegator who has not unstaked or delegated to a validator will be dos ed if a validator exits&#x20; |
| [v16] | reports/vechain-l1_findings/60553-sc-high-the-delegator-and-the-validator-both-exiting-consecutively-could-lead-to-underflow-in.md | HIGH | Immunefi (frolic) | sc high the delegator and the validator both exiting consecutively could lead to underflow in the unstake and delegate and stuck staked vet&#x20; |
| [q17] | reports/vechain-l1_findings/56362-bc-insight-during-addvalidation-if-pos-not-active-authority-native-env-state-get-should-consum.md | INFO | Immunefi (emarai) | bc insight during addvalidation if pos not active authority native env state get should consume double the gas |
| [q18] | reports/vechain-l1_findings/56367-sc-insight-staker-gas-optimization-public-to-external-visibility.md | INFO | Immunefi (caslo) | sc insight staker gas optimization public to external visibility |
| [q19] | reports/vechain-l1_findings/56657-bc-insight-inactive-validator-scheduling-bypass-in-vechain-thor-pos-consensus-mechanism.md | INFO | Immunefi (warden) | bc insight inactive validator scheduling bypass in vechain thor pos consensus mechanism |
| [q20] | reports/vechain-l1_findings/57179-bc-insight-during-the-call-to-native-totalsupply-there-s-missing-gas-charges.md | INFO | Immunefi (emarai) | bc insight during the call to native totalsupply there s missing gas charges |
| [q21] | reports/vechain-l1_findings/57412-sc-insight-gas-optimization-insight-improve-gas-cost-efficiency-by-the-use-of-custom-errors-in.md | INFO | Immunefi (warden) | sc insight gas optimization insight improve gas cost efficiency by the use of custom errors in staker sol contract |
| [q22] | reports/vechain-l1_findings/60023-sc-insight-unchecked-address-0-validator-in-unstake.md | INFO | Immunefi (Oxb4b) | sc insight unchecked address 0 validator in unstake&#x20; |
| [q23] | reports/vechain-l1_findings/60450-sc-insight-code-optimizations-and-enhancemets-for-efficient-gas-usage-in-several-functions.md | INFO | Immunefi (KKam86) | sc insight code optimizations and enhancemets for efficient gas usage in several functions |
| [q24] | reports/vechain-l1_findings/57136-bc-low-txpool-priority-cache-lets-base-fee-swings-reduce-proposers-tips.md | LOW | Immunefi (warden) | Txpool priority cache lets base fee swings reduce proposers tips |
| [q25] | reports/vechain-l1_findings/56345-bc-insight-there-is-an-issue-related-to-strict-threshold-breaks-exact-2-3-and-is-causing-final.md | INFO | Immunefi (warden) | Strict threshold breaks exact 2/3 and is causing finality freeze |
## Vechain Consensus Nodes

**vechain-consensus-nodes patterns mined from uncited L1 audit reports** - 16 sec-tier findings (0 critical / 15 high / 1 medium) across 16 files from Immunefi (Diavol0), Immunefi (FrontRunner), Immunefi (HalalAudits), Immunefi (aman), Immunefi (demonhat), Immunefi (flacko).

### Overview

Titles in the references table are verbatim from source reports. Route to the exact report file for full PoC detail. Validation strength: `unassessed` (evidence rows only).

### Detection Patterns

#### High-Signal Grep Seeds
```
- accounting
- after
- another
- attacker
- both
- bricked
- broken
- case
```

### Vulnerability Description

#### Root Cause

The cited reports describe vechain consensus nodes paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `vechain-consensus-nodes | vechain consensus nodes | varies by finding | see references`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `vechain-consensus-nodes | vechain consensus nodes | varies by finding | see references | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `vechain-consensus-nodes | vechain consensus nodes | varies by finding | see references | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: sc high fund freeze from double stake subtraction when validator exits&#x20;** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// sc high fund freeze from double stake subtraction when validator exits&#x20;
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: sc high fund freeze from double stake subtraction when validator exits&#x20;
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: sc high double decrease after exit validator exited leads to underflow and permanent freeze** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// sc high double decrease after exit validator exited leads to underflow and permanent freeze
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: sc high double decrease after exit validator exited leads to underflow and permanent freeze
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: sc high user funds get stucked in the contract when validators exits&#x20;** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// sc high user funds get stucked in the contract when validators exits&#x20;
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: sc high user funds get stucked in the contract when validators exits&#x20;
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

`accounting, after, another, attacker, both, bricked, broken, case, cause, causes`

### Related Vulnerabilities

- Sibling entries under the same category folder
