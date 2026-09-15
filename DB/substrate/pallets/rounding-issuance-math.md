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
  - arithmetic
  - asset
  - could
  - currencies
  - defined
  - description

# Grep / Hunt-Card Seeds
code_keywords:
  - arithmetic
  - asset
  - could
  - currencies
  - defined
  - description
  - dispatchable
  - happens
  - integer
  - issuance

severity: high
impact: fund_loss
language: rust
tags:
  - arithmetic
  - l1
  - substrate
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [x1] | reports/substrate-l1_findings/acala-srl-2021-12.md | HIGH | SRLabs | Integer overflow in the xcm::v1 pallet could result in loss of asset tokens |
| [x2] | reports/substrate-l1_findings/publicreports-substrate-audits-reef-chain-substrate-security-audit-report-halborn-v1-1-pdf.md | MEDIUM | Halborn | 3.1 (HAL-01) INTEGER OVERFLOW - MEDIUM Description: An overflow happens when an arithmetic operation reaches the maximum size of a type |
| [x3] | reports/substrate-l1_findings/publicreports-substrate-audits-reef-chain-substrate-security-audit-report-halborn-v1-1-pdf.md | MEDIUM | Halborn | 3.2 (HAL-02) TOTAL ISSUANCE NOT UPDATED ON MINT - MEDIUM Description: The update_balance dispatchable defined in modules/currencies/src/lib. |
| [x4] | reports/substrate-l1_findings/reef-halborn.md | MEDIUM | Halborn | 3.1 (HAL-01) INTEGER OVERFLOW - MEDIUM Description: An overflow happens when an arithmetic operation reaches the maximum size of a type |
| [x5] | reports/substrate-l1_findings/reef-halborn.md | MEDIUM | Halborn | 3.2 (HAL-02) TOTAL ISSUANCE NOT UPDATED ON MINT - MEDIUM Description: The update_balance dispatchable defined in modules/currencies/src/lib. |
| [x11] | reports/substrate-l1_findings/manta-veridise-chain.md | MEDIUM | Veridise | Manta Network ©2023 Veridise Inc. 14 4 Vulnerability Report 4.1.4 V-MANC-VUL-004: Total supply of native assets can exceed the set limit |
| [x12] | reports/substrate-l1_findings/acala-c4-2401.md | HIGH | Code4rena | transfer_share_and_rewards can be used to transfer out shares without transferring reward debt due to rounding • Medium Risk Findings (4) |
| [x13] | reports/substrate-l1_findings/centrifuge-srl-baseline-2022.md | MEDIUM | SRLabs | Integer overflows could invert state of a loan Integer overflows are common in Rust, they are also easy to prevent |
| [q14] | reports/substrate-l1_findings/acala-slowmist-2020.md | LOW | SlowMist | Tokens transfer does not use overflow prevention methods to calculate the amount |
| [q15] | reports/substrate-l1_findings/composable-audits-solana-restaking-v2-composable-audit-draft-v2-pdf.md | MEDIUM | OtterSec | Point precision loss (OS-CFI-ADV-006) (composable solana restaking v2 draft) |
| [q16] | reports/substrate-l1_findings/composable-audits-solana-restaking-v2-composable-audit-draft-v2-pdf.md | LOW | OtterSec | Rounding error on integer division (OS-CFI-ADV-008) (composable solana restaking v2 draft) |
## Arith Rounding

**Arith rounding patterns mined from uncited L1 audit reports** - representative of 5 findings mined from 3 L1 audit reports (Halborn, SRLabs).

### Overview

5 sec-tier findings (0 critical, 1 high, 4 medium) from 3 audit reports by Halborn, SRLabs. Titles in the references table are verbatim from the source reports; use them to route to the exact report for full PoC detail.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the balance/issuance computation paths path lacks the validation/bounding the cited reports identify."
- Pattern key: `rounding-drift | fixed-point math | repeated ops | value leak`
- Interaction scope: `single_contract`
- Primary affected component(s): `balance/issuance computation paths`
- High-signal code keywords: `arithmetic, asset, could, currencies, defined, description`
- Typical sink / impact: `fund_loss`
- Validation strength: `unassessed` (evidence rows cite source reports; per-finding PoCs not yet re-verified)

#### Valid Bug Signals

- Signal 1: title evidence in cited reports matches the audited component family (balance/issuance computation paths)
- Signal 2: severity consensus across independent auditors (Halborn, SRLabs)
- Signal 3: impact-producing condition stated in source report (fund_loss)

#### False Positive Guards

- Not this bug when: the target chain/module already enforces explicit bounds/limits on the affected path
- Safe if: audited version postdates the fix noted in the source report status
- Requires attacker control of: the inputs named in the cited finding titles (messages, bids, deposits)

### Detection Patterns

#### High-Signal Grep Seeds
```
- arithmetic
- asset
- could
- currencies
- defined
- description
- dispatchable
- happens
- integer
- issuance
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

**Example 1: Integer overflow in the xcm::v1 pallet could result in loss of asset tokens** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Integer overflow in the xcm::v1 pallet could result in loss of asset tokens
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Integer overflow in the xcm::v1 pallet could result in loss of asset tokens
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: transfer_share_and_rewards can be used to transfer out shares without transferring reward debt due to rounding • Medium ** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// transfer_share_and_rewards can be used to transfer out shares without transferring reward debt due to rounding • Medium Risk Findings (4)
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: transfer_share_and_rewards can be used to transfer out shares without transferring reward debt due t
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: 3.1 (HAL-01) INTEGER OVERFLOW - MEDIUM Description: An overflow happens when an arithmetic operation reaches the maximum** [Approx Vulnerability : MEDIUM]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// 3.1 (HAL-01) INTEGER OVERFLOW - MEDIUM Description: An overflow happens when an arithmetic operation reaches the maximum size of a type
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: 3.1 (HAL-01) INTEGER OVERFLOW - MEDIUM Description: An overflow happens when an arithmetic operation
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

`arithmetic, asset, could, currencies, defined, description, dispatchable, happens, integer, issuance, loss, maximum, medium, mint`

### Related Vulnerabilities

- See references table; sibling entries under the same DB category folder
