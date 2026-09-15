---
# Core Classification
protocol: generic
chain: polkadot
category: reliability
vulnerability_type: error_handling_state_divergence
root_cause_family: incomplete_failure_handling

# Pattern Identity
pattern_key: partial-failure | multi-step extrinsic | mid-path error | inconsistent state

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - multi-step extrinsics

# Attack Vector Details
attack_type: logical_error
affected_component: multi-step extrinsics

# Technical Primitives
primitives:
  - acknowledged
  - after
  - agent
  - always
  - case
  - causing

# Grep / Hunt-Card Seeds
code_keywords:
  - acknowledged
  - after
  - agent
  - always
  - case
  - causing
  - code
  - contract
  - critical
  - description

severity: critical
impact: dos
language: rust
tags:
  - reliability
  - l1
  - substrate
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [x1] | reports/substrate-l1_findings/composable-audits-halborn-audit20210229-pallets-core-pdf.md | CRITICAL | Halborn | 3.17 (HAL-17) POSSIBLE ERROR AFTER CRITICAL FUNCTION - INFORMATIONAL 83 Description 83 Code Location 83 Risk Level 84 Recommendation 84 Reme |
| [x2] | reports/substrate-l1_findings/composable-audits-halborn-audit20210229-pallets-core-pdf.md | CRITICAL | Halborn | HAL-17 POSSIBLE ERROR AFTER CRITICAL FUNCTION Informational ACKNOWLEDGED 16 EXECUTIVE OVERVIEW |
| [x3] | reports/substrate-l1_findings/composable-audits-halborn-audit20210229-pallets-core-pdf.md | CRITICAL | Halborn | 3.17 (HAL-17) POSSIBLE ERROR AFTER CRITICAL FUNCTION - INFORMATIONAL Description: Inside mosaic pallet, the transfer_to function can throw a |
| [x4] | reports/substrate-l1_findings/composable-halborn-core.md | CRITICAL | Halborn | 3.17 (HAL-17) POSSIBLE ERROR AFTER CRITICAL FUNCTION - INFORMATIONAL 83 Description 83 Code Location 83 Risk Level 84 Recommendation 84 Reme |
| [x5] | reports/substrate-l1_findings/composable-halborn-core.md | CRITICAL | Halborn | HAL-17 POSSIBLE ERROR AFTER CRITICAL FUNCTION Informational ACKNOWLEDGED 16 EXECUTIVE OVERVIEW |
| [x6] | reports/substrate-l1_findings/composable-halborn-core.md | CRITICAL | Halborn | 3.17 (HAL-17) POSSIBLE ERROR AFTER CRITICAL FUNCTION - INFORMATIONAL Description: Inside mosaic pallet, the transfer_to function can throw a |
| [x7] | reports/substrate-l1_findings/audit-reports-snowbridge-2024-02-12-audit-report-snowbridge-extension-v1-1-pdf.md | HIGH | auditor | Inconsistent state in case agent contract instantiation fails on Ethereum |
| [x8] | reports/substrate-l1_findings/audit-reports-snowbridge-2024-05-24-audit-report-snowbridge-v1-1-pdf.md | CRITICAL | auditor | submit extrinsic always returns Ok , causing stuck funds in the Agent contract in case of errors |
| [x17] | reports/substrate-l1_findings/audit-reports-kilt-2025-03-27-audit-report-kilt-bonding-curve-pallet-v1-0-pdf.md | HIGH | Oak Security | Potential loss of funds due to can_deposit error during the refund process |
| [x18] | reports/substrate-l1_findings/audit-reports-snowbridge-2025-05-29-audit-report-snowbridge-v2-v1-0-pdf.md | HIGH | Oak Security | Digest item validation flaw enables inconsistent commitment verification |
| [x19] | reports/substrate-l1_findings/phala-blockchain-audit-code4rena-phat-contract-runtime-pdf.md | MEDIUM | auditor | Limited availability of balance_of(...) method fn balance_of( &self, account: ext::AccountId, ) -> Result<(pink::Balance, pink::Balance), Self::Error> |
| [x20] | reports/substrate-l1_findings/acala-slowmist-2021.md | MEDIUM | SlowMist | Risk of calculation errors |
| [x21] | reports/substrate-l1_findings/acala-slowmist-2021.md | MEDIUM | SlowMist | URL: https://rustsec.org/advisories/RUSTSEC-2021-0115 Solution: Upgrade to >=1.2.0 Dependency tree: zeroize_derive 1.1.0 5.2 Risk of calculation error |
| [q22] | reports/substrate-l1_findings/audit-reports-snowbridge-2024-08-10-audit-report-snowbridge-updates-2-v1-0-pdf.md | INFO | auditor | 2. Incorrect error message |
| [q23] | reports/substrate-l1_findings/audit-reports-snowbridge-2024-08-16-audit-report-snowbridge-updates-v1-0-pdf.md | LOW | auditor | Missing validation for foreignTokenDecimals could lead to a division by zero error |
| [q24] | reports/substrate-l1_findings/alephbft-tob.md | INFO | Trail of Bits | Use of incorrect loop break to handle add_to_store and handle_events failures (TOB-ALEPH-003) |
| [q25] | reports/substrate-l1_findings/alephbft-tob.md | INFO | Trail of Bits | Incorrect state rollback upon removal of forker's units (TOB-ALEPH-004) |
| [q26] | reports/substrate-l1_findings/alephbft-tob.md | INFO | Trail of Bits | Lack of error handling in Terminal's post-insert hooks (TOB-ALEPH-005) |
| [q27] | reports/substrate-l1_findings/alephbft-tob.md | LOW | Trail of Bits | Errors in async code leave the program in an inconsistent state (TOB-ALEPH-007, low-severity per exec summary) |
| [q28] | reports/substrate-l1_findings/alephbft-tob.md | INFO | Trail of Bits | Inconsistent handling of closed channel errors (TOB-ALEPH-009) |
| [q29] | reports/substrate-l1_findings/publications-reviews-alephbft-pdf.md | INFO | Trail of Bits | Use of incorrect loop break to handle add_to_store and handle_events failures (TOB-ALEPH-003) |
| [q30] | reports/substrate-l1_findings/publications-reviews-alephbft-pdf.md | INFO | Trail of Bits | Incorrect state rollback upon removal of forker's units (TOB-ALEPH-004) |
| [q31] | reports/substrate-l1_findings/publications-reviews-alephbft-pdf.md | INFO | Trail of Bits | Lack of error handling in Terminal's post-insert hooks (TOB-ALEPH-005) |
| [q32] | reports/substrate-l1_findings/publications-reviews-alephbft-pdf.md | LOW | Trail of Bits | Errors in async code leave the program in an inconsistent state (TOB-ALEPH-007, low-severity per exec summary) |
| [q33] | reports/substrate-l1_findings/publications-reviews-alephbft-pdf.md | INFO | Trail of Bits | Inconsistent handling of closed channel errors (TOB-ALEPH-009) |
| [q34] | reports/substrate-l1_findings/composable-audits-picasso-cosmos-picasso-cosmos-audit-pdf.md | HIGH | Oak Security | The mint module address is blacklisted and it is not possible to replenish incentives (picasso-cosmos audit) |
| [q35] | reports/substrate-l1_findings/composable-audits-picasso-cosmos-picasso-cosmos-audit-pdf.md | HIGH | Oak Security | Panics in PrepareProposal when sending a transaction (picasso-cosmos audit) |
| [q36] | reports/substrate-l1_findings/composable-audits-picasso-cosmos-picasso-cosmos-audit-pdf.md | HIGH | Oak Security | The mint module panics if there are no staked coins (picasso-cosmos audit) |
## Error Handling

**Error handling patterns mined from uncited L1 audit reports** - representative of 8 findings mined from 4 L1 audit reports (Halborn, unknown).

### Overview

8 sec-tier findings (7 critical, 1 high, 0 medium) from 4 audit reports by Halborn, unknown. Titles in the references table are verbatim from the source reports; use them to route to the exact report for full PoC detail.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the multi-step extrinsics path lacks the validation/bounding the cited reports identify."
- Pattern key: `partial-failure | multi-step extrinsic | mid-path error | inconsistent state`
- Interaction scope: `multi_contract`
- Primary affected component(s): `multi-step extrinsics`
- High-signal code keywords: `acknowledged, after, agent, always, case, causing`
- Typical sink / impact: `dos`
- Validation strength: `unassessed` (evidence rows cite source reports; per-finding PoCs not yet re-verified)

#### Valid Bug Signals

- Signal 1: title evidence in cited reports matches the audited component family (multi-step extrinsics)
- Signal 2: severity consensus across independent auditors (Halborn, unknown)
- Signal 3: impact-producing condition stated in source report (dos)

#### False Positive Guards

- Not this bug when: the target chain/module already enforces explicit bounds/limits on the affected path
- Safe if: audited version postdates the fix noted in the source report status
- Requires attacker control of: the inputs named in the cited finding titles (messages, bids, deposits)

### Detection Patterns

#### High-Signal Grep Seeds
```
- acknowledged
- after
- agent
- always
- case
- causing
- code
- contract
- critical
- description
```

#### Audit Checklist
- [ ] Verify bounded iteration/gas on the affected path
- [ ] Check state-consistency guarantees across the failure paths cited above
- [ ] Compare implementation against the source-report recommendation

### Vulnerability Description

#### Root Cause

The cited reports describe multi-step extrinsics paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `partial-failure | multi-step extrinsic | mid-path error | inconsistent state`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `partial-failure | multi-step extrinsic | mid-path error | inconsistent state | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `partial-failure | multi-step extrinsic | mid-path error | inconsistent state | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: 3.17 (HAL-17) POSSIBLE ERROR AFTER CRITICAL FUNCTION - INFORMATIONAL 83 Description 83 Code Location 83 Risk Level 84 Re** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// 3.17 (HAL-17) POSSIBLE ERROR AFTER CRITICAL FUNCTION - INFORMATIONAL 83 Description 83 Code Location 83 Risk Level 84 Recommendation 84 Reme
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: 3.17 (HAL-17) POSSIBLE ERROR AFTER CRITICAL FUNCTION - INFORMATIONAL 83 Description 83 Code Location
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: HAL-17 POSSIBLE ERROR AFTER CRITICAL FUNCTION Informational ACKNOWLEDGED 16 EXECUTIVE OVERVIEW** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// HAL-17 POSSIBLE ERROR AFTER CRITICAL FUNCTION Informational ACKNOWLEDGED 16 EXECUTIVE OVERVIEW
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: HAL-17 POSSIBLE ERROR AFTER CRITICAL FUNCTION Informational ACKNOWLEDGED 16 EXECUTIVE OVERVIEW
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: 3.17 (HAL-17) POSSIBLE ERROR AFTER CRITICAL FUNCTION - INFORMATIONAL Description: Inside mosaic pallet, the transfer_to ** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// 3.17 (HAL-17) POSSIBLE ERROR AFTER CRITICAL FUNCTION - INFORMATIONAL Description: Inside mosaic pallet, the transfer_to function can throw a
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: 3.17 (HAL-17) POSSIBLE ERROR AFTER CRITICAL FUNCTION - INFORMATIONAL Description: Inside mosaic pall
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

`acknowledged, after, agent, always, case, causing, code, contract, critical, description, error, errors, ethereum, executive`

### Related Vulnerabilities

- See references table; sibling entries under the same DB category folder
