---
# Core Classification
protocol: generic
chain: generic
category: near
vulnerability_type: near_novel
root_cause_family: see pattern_key

# Pattern Identity
pattern_key: near-novel | near novel | varies by finding | see references

# Interaction Scope
interaction_scope: varies
involved_contracts:
  - near novel

# Attack Vector Details
attack_type: varies
affected_component: near novel

# Technical Primitives
primitives:
  - abused
  - adding
  - allows
  - asset
  - assetbridge
  - available

# Grep / Hunt-Card Seeds
code_keywords:
  - abused
  - adding
  - allows
  - asset
  - assetbridge
  - available
  - balance
  - being

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
| [o1] | reports/other-l1_findings/audit-reports-router-2024-04-30-audit-report-router-asset-bridge-v1-2-pdf.md | CRITICAL | Oak Security | NEAR tokens are incorrectly transferred to the gateway contract instead of being escrowed in the AssetBridge contract |
| [o2] | reports/other-l1_findings/audit-reports-router-2024-04-30-audit-report-router-asset-bridge-v1-2-pdf.md | HIGH | Oak Security | The reentrancy lock mechanism in the NEAR AssetBridge contract can be abused to grief the contract |
| [o3] | reports/other-l1_findings/audit-reports-router-2024-04-30-audit-report-router-asset-bridge-v1-2-pdf.md | HIGH | Oak Security | Callback functions may run out of gas  resulting in inconsistent states of the NEAR asset-bridge contract |
| [o4] | reports/other-l1_findings/audit-reports-router-2024-04-30-audit-report-router-asset-bridge-v1-2-pdf.md | HIGH | Oak Security | Incorrectly determining the available NEAR balance of the AssetBridge contract causes transactions to fail |
| [o5] | reports/other-l1_findings/audit-reports-router-2024-05-29-audit-report-router-evm-and-near-gateway-contracts-and-wasm-bindings-v1-0-pdf.md | CRITICAL | Oak Security | Duplicate IReceiveEvent event nonces in the NEAR gateway contract resulting in stuck cross-chain requests |
| [o6] | reports/other-l1_findings/audit-reports-router-2024-05-29-audit-report-router-evm-and-near-gateway-contracts-and-wasm-bindings-v1-0-pdf.md | HIGH | Oak Security | The reentrancy lock mechanism in the NEAR GatewayUpgradeable contract can be abused to grief the contract |
| [o7] | reports/other-l1_findings/audits-avalaunch-2021-11-allocationstaking-cooldown-feature-pdf.md | CRITICAL | CoinFabrik | Yes Immediately Medium In the near future Yes As soon as possible Minor Unlikely No Eventually Enhancement No No Eventually Issues Found by |
| [o8] | reports/other-l1_findings/publicreports-near-smart-contract-audits-octopus-network-anchor-near-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | CASE SENSITIVE CHECK ALLOWS ADDING THE SAME NEAR FUNGIBLE TOKEN MORE THAN ONCE |

## Near Novel

**near-novel patterns mined from uncited L1 audit reports** - 8 sec-tier findings (3 critical / 4 high / 1 medium) across 4 files from CoinFabrik, Halborn, Oak Security.

### Overview

Titles in the references table are verbatim from source reports. Route to the exact report file for full PoC detail. Validation strength: `unassessed` (evidence rows only).

### Detection Patterns

#### High-Signal Grep Seeds
```
- abused
- adding
- allows
- asset
- assetbridge
- available
- balance
- being
```

### Vulnerability Description

#### Root Cause

The cited reports describe near novel paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `near-novel | near novel | varies by finding | see references`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `near-novel | near novel | varies by finding | see references | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `near-novel | near novel | varies by finding | see references | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: NEAR tokens are incorrectly transferred to the gateway contract instead of being escrowed in the AssetBridge contract** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// NEAR tokens are incorrectly transferred to the gateway contract instead of being escrowed in the AssetBridge contract
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: NEAR tokens are incorrectly transferred to the gateway contract instead of being escrowed in the Ass
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: Duplicate IReceiveEvent event nonces in the NEAR gateway contract resulting in stuck cross-chain requests** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Duplicate IReceiveEvent event nonces in the NEAR gateway contract resulting in stuck cross-chain requests
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Duplicate IReceiveEvent event nonces in the NEAR gateway contract resulting in stuck cross-chain req
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: Yes Immediately Medium In the near future Yes As soon as possible Minor Unlikely No Eventually Enhancement No No Eventua** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Yes Immediately Medium In the near future Yes As soon as possible Minor Unlikely No Eventually Enhancement No No Eventually Issues Found by
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Yes Immediately Medium In the near future Yes As soon as possible Minor Unlikely No Eventually Enhan
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

`abused, adding, allows, asset, assetbridge, available, balance, being, bridge, callback`

### Related Vulnerabilities

- Sibling entries under the same category folder
