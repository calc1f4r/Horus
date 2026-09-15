---
# Core Classification
protocol: generic
chain: polkadot
category: fees
vulnerability_type: fee_handling_error
root_cause_family: missing_validation

# Pattern Identity
pattern_key: fee-handling-gap | fee path | payment or refund | value leak or griefing

# Interaction Scope
interaction_scope: single_contract
involved_contracts:
  - fee collection paths

# Attack Vector Details
attack_type: logical_error
affected_component: fee collection paths

# Technical Primitives
primitives:
  - accesses
  - actual
  - amount
  - attacks
  - broker
  - called

# Grep / Hunt-Card Seeds
code_keywords:
  - accesses
  - actual
  - amount
  - attacks
  - broker
  - called
  - case
  - change
  - charged
  - come

severity: critical
impact: fund_loss
language: rust
tags:
  - fees
  - l1
  - substrate
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [x1] | reports/substrate-l1_findings/chainflip-backend-audits-chainflip-backend-zellic-audit-report-pdf.md | CRITICAL | Zellic | Broker fees are not taken from swap amount |
| [x2] | reports/substrate-l1_findings/audit-reports-snowbridge-2024-02-12-audit-report-snowbridge-extension-v1-1-pdf.md | CRITICAL | auditor | Potential locked funds in case the user-deﬁned destinationFee does not cover the actual fee |
| [x3] | reports/substrate-l1_findings/starlay-oak-wasm.md | HIGH | Oak Security | Flash loans can be initiated without paying fee premiums |
| [x4] | reports/substrate-l1_findings/manta-veridise-chain.md | MEDIUM | Veridise | Inc. 10 4 Vulnerability Report 4.1 Detailed Description of Issues 4.1.1 V-MANC-VUL-001: Static fee charged despite dynamic storage accesses |
| [x5] | reports/substrate-l1_findings/acala-c4-2401.md | MEDIUM | Code4rena | Unbond_instant removes incorrect amount of shares let amount = change.change; let fee = fee_ratio.mul_ceil(amount); let final_amount = amount.saturati |
| [x6] | reports/substrate-l1_findings/centrifuge-srl-baseline-2022.md | MEDIUM | SRLabs | Spamming attacks Spamming attacks come from unsigned extrinsics as they don’t require a fee to be called |
| [q7] | reports/substrate-l1_findings/audit-reports-snowbridge-2024-08-16-audit-report-snowbridge-updates-v1-0-pdf.md | LOW | auditor | Missing validation for the fee multiplier |
| [q8] | reports/substrate-l1_findings/acala-trailofbits.md | LOW | Trail of Bits | Transferring "max" ACA tokens through Acala-dapp fails and only burns the fees (TOB-ACA-004) |
| [q9] | reports/substrate-l1_findings/publications-reviews-acalanetwork-pdf.md | LOW | Trail of Bits | Transferring "max" ACA tokens through Acala-dapp fails and only burns the fees (TOB-ACA-004) |
## Fee Handling

**Fee handling patterns mined from uncited L1 audit reports** - representative of 6 findings mined from 6 L1 audit reports (Code4rena, Oak Security, SRLabs, Veridise, Zellic, unknown).

### Overview

6 sec-tier findings (2 critical, 1 high, 3 medium) from 6 audit reports by Code4rena, Oak Security, SRLabs, Veridise, Zellic, unknown. Titles in the references table are verbatim from the source reports; use them to route to the exact report for full PoC detail.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the fee collection paths path lacks the validation/bounding the cited reports identify."
- Pattern key: `fee-handling-gap | fee path | payment or refund | value leak or griefing`
- Interaction scope: `single_contract`
- Primary affected component(s): `fee collection paths`
- High-signal code keywords: `accesses, actual, amount, attacks, broker, called`
- Typical sink / impact: `fund_loss`
- Validation strength: `unassessed` (evidence rows cite source reports; per-finding PoCs not yet re-verified)

#### Valid Bug Signals

- Signal 1: title evidence in cited reports matches the audited component family (fee collection paths)
- Signal 2: severity consensus across independent auditors (Code4rena, Oak Security, SRLabs, Veridise, Zellic, unknown)
- Signal 3: impact-producing condition stated in source report (fund_loss)

#### False Positive Guards

- Not this bug when: the target chain/module already enforces explicit bounds/limits on the affected path
- Safe if: audited version postdates the fix noted in the source report status
- Requires attacker control of: the inputs named in the cited finding titles (messages, bids, deposits)

### Detection Patterns

#### High-Signal Grep Seeds
```
- accesses
- actual
- amount
- attacks
- broker
- called
- case
- change
- charged
- come
```

#### Audit Checklist
- [ ] Verify bounded iteration/gas on the affected path
- [ ] Check state-consistency guarantees across the failure paths cited above
- [ ] Compare implementation against the source-report recommendation

### Vulnerability Description

#### Root Cause

The cited reports describe fee collection paths paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `fee-handling-gap | fee path | payment or refund | value leak or griefing`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `fee-handling-gap | fee path | payment or refund | value leak or griefing | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `fee-handling-gap | fee path | payment or refund | value leak or griefing | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: Broker fees are not taken from swap amount** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Broker fees are not taken from swap amount
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Broker fees are not taken from swap amount
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: Potential locked funds in case the user-deﬁned destinationFee does not cover the actual fee** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Potential locked funds in case the user-deﬁned destinationFee does not cover the actual fee
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Potential locked funds in case the user-deﬁned destinationFee does not cover the actual fee
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: Flash loans can be initiated without paying fee premiums** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Flash loans can be initiated without paying fee premiums
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Flash loans can be initiated without paying fee premiums
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

`accesses, actual, amount, attacks, broker, called, case, change, charged, come, cover, description, despite, destinationfee`

### Related Vulnerabilities

- See references table; sibling entries under the same DB category folder
