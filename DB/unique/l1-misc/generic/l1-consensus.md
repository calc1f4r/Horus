---
# Core Classification
protocol: generic
chain: generic
category: l1
vulnerability_type: l1_consensus_generic
root_cause_family: see pattern_key

# Pattern Identity
pattern_key: l1-consensus-generic | l1 consensus generic | varies by finding | see references

# Interaction Scope
interaction_scope: varies
involved_contracts:
  - l1 consensus generic

# Attack Vector Details
attack_type: varies
affected_component: l1 consensus generic

# Technical Primitives
primitives:
  - adjusted
  - after
  - agreement
  - amounts
  - asset
  - being

# Grep / Hunt-Card Seeds
code_keywords:
  - adjusted
  - after
  - agreement
  - amounts
  - asset
  - being
  - between
  - block

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
| [o1] | reports/other-l1_findings/audit-reports-dusk-2024-09-20-audit-report-rusk-consensus-pdf.md | HIGH | Oak Security | Committee members can vote multiple times |
| [o2] | reports/other-l1_findings/audit-reports-dusk-2024-09-20-audit-report-rusk-consensus-pdf.md | HIGH | Oak Security | Committee members can submit conflicting votes |
| [o3] | reports/other-l1_findings/audit-reports-dusk-2024-09-20-audit-report-rusk-consensus-pdf.md | HIGH | Oak Security | Slashing for block generator is disabled after 10 iterations |
| [o4] | reports/other-l1_findings/audit-reports-milkyway-2023-12-12-audit-report-milkyway-staking-v1-0-pdf.md | HIGH | Oak Security | The exchange rate between milkTIA and osmoTIA cannot be adjusted in the event of a slashing incident |
| [o5] | reports/other-l1_findings/audit-reports-router-2024-05-29-audit-report-router-evm-and-near-gateway-contracts-and-wasm-bindings-v1-0-pdf.md | HIGH | Oak Security | Validator set supermajority threshold discrepancy between the gateway contracts and Router Chain |
| [o6] | reports/other-l1_findings/public-audits-reports-mantle-review-pdf.md | HIGH | NCC Group | Detailed Findings MNT-05 TSS Nodes Set Includes Slashed Node By Default Asset tss/manager/agreement.go Status Closed: See Resolution Rating |
| [o7] | reports/other-l1_findings/public-audits-reports-omni-network-sigma-prime-omni-network-omni-portal-security-assessment-report-v2-1-pdf.md | HIGH | NCC Group | Findings OMP-05 Old Validator Set Can Sign Newly Supported Chains Asset protocol/OmniPortal.sol Status Resolved: See Resolution Rating |
| [o8] | reports/other-l1_findings/publications-afx-bridge-zellic-audit-report-pdf.md | HIGH | Zellic | Partially voted withdrawals can stay stuck in the pending state indefinitely |
| [o9] | reports/other-l1_findings/publications-afx-bridge-zellic-audit-report-pdf.md | HIGH | Zellic | Validator rotation can double-count bridge votes |
| [o10] | reports/other-l1_findings/publications-afx-bridge-zellic-audit-report-pdf.md | MEDIUM | Zellic | Relayer vote caches grow without bound |
| [o11] | reports/other-l1_findings/publications-mina-token-bridge-evm-zellic-audit-report-pdf.md | CRITICAL | Zellic | Validator public key is not checked |
| [o12] | reports/other-l1_findings/publications-mina-token-bridge-evm-zellic-audit-report-pdf.md | CRITICAL | Zellic | Function getValidatorIndex returns index of first validator for every public key |
| [o13] | reports/other-l1_findings/publications-mina-token-bridge-evm-zellic-audit-report-pdf.md | MEDIUM | Zellic | Validators cannot be removed |
| [o14] | reports/other-l1_findings/publications-mina-token-bridge-evm-zellic-audit-report-pdf.md | HIGH | Zellic | No domain separation for validator signatures |
| [o15] | reports/other-l1_findings/publications-reviews-dfinityconsensus-pdf.md | HIGH | Trail of Bits | Invalid notarizations cause the validator to skip block validation |
| [o16] | reports/other-l1_findings/publicreports-l1-audits-taraxa-node-evm-l1-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | VOTES - DENIAL OF SERVICE |
| [o17] | reports/other-l1_findings/publicreports-near-smart-contract-audits-octopus-network-near-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | REGISTRY OWNER CAN SET ITSELF AS VOTER OPERATOR |
| [o18] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-meld-staking-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | WEIGHTED AMOUNTS ARE NOT BEING REMOVED ON SLASHING |
| [o19] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-thorstarter-governance-smart-contract-security-audit-report-halborn-v1-1-pdf.md | CRITICAL | Halborn | USER CAN VOTE MULTIPLE TIMES THROUGH DELEGATION |
| [q20] | reports/other-l1_findings/audit-reports-asteroid-bridge-2024-06-17-audit-report-asteroid-bridge-v1-0-pdf.md | LOW | Oak Security | Message verification does not require the supermajority of signers |
| [q21] | reports/other-l1_findings/audit-reports-asteroid-bridge-2024-06-17-audit-report-asteroid-bridge-v1-0-pdf.md | LOW | Oak Security | Signers can replay transactions |
| [q22] | reports/other-l1_findings/publications-springsui-zellic-audit-report-pdf.md | INFO | Zellic | Refreshing validator updates |
| [q23] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-pocket-network-wrapped-pocket-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | SAFE SIGNER NUMBER THRESHOLD NOT ENFORCED |

## L1 Consensus Generic

**l1-consensus-generic patterns mined from uncited L1 audit reports** - 19 sec-tier findings (5 critical / 11 high / 3 medium) across 12 files from Halborn, NCC Group, Oak Security, Trail of Bits, Zellic.

### Overview

Titles in the references table are verbatim from source reports. Route to the exact report file for full PoC detail. Validation strength: `unassessed` (evidence rows only).

### Detection Patterns

#### High-Signal Grep Seeds
```
- adjusted
- after
- agreement
- amounts
- asset
- being
- between
- block
```

### Vulnerability Description

#### Root Cause

The cited reports describe l1 consensus generic paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `l1-consensus-generic | l1 consensus generic | varies by finding | see references`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `l1-consensus-generic | l1 consensus generic | varies by finding | see references | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `l1-consensus-generic | l1 consensus generic | varies by finding | see references | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: Validator public key is not checked** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Validator public key is not checked
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Validator public key is not checked
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: Function getValidatorIndex returns index of first validator for every public key** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Function getValidatorIndex returns index of first validator for every public key
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Function getValidatorIndex returns index of first validator for every public key
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: VOTES - DENIAL OF SERVICE** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// VOTES - DENIAL OF SERVICE
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: VOTES - DENIAL OF SERVICE
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

`adjusted, after, agreement, amounts, asset, being, between, block, bound, bridge`

### Related Vulnerabilities

- Sibling entries under the same category folder
