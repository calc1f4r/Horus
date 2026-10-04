---
# Core Classification
protocol: generic
chain: polkadot
category: tokens
vulnerability_type: issuance_balance_accounting
root_cause_family: accounting_error

# Pattern Identity
pattern_key: issuance-accounting-gap | token pallet | mint/burn/transfer | supply mismatch

# Interaction Scope
interaction_scope: single_contract
involved_contracts:
  - token/issuance pallet paths

# Attack Vector Details
attack_type: logical_error
affected_component: token/issuance pallet paths

# Technical Primitives
primitives:
  - addition
  - addressed
  - amounts
  - asset
  - assets
  - availability

# Grep / Hunt-Card Seeds
code_keywords:
  - addition
  - addressed
  - amounts
  - asset
  - assets
  - availability
  - balance
  - balance_of
  - causes
  - certain

severity: critical
impact: fund_loss
language: rust
tags:
  - tokens
  - l1
  - substrate
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [x1] | reports/substrate-l1_findings/hydradx-c4-2401.md | MEDIUM | Code4rena | [M-06] complete liquidity removal will result in permanent disable of the liquidity addition and prevent minting shares for the liquidity providers. |
| [x2] | reports/substrate-l1_findings/chainflip-backend-audits-2023-04-trailofbits-securityreview-pdf.md | HIGH | Trail of Bits | ERC-20 token transfer fails for certain tokens |
| [x3] | reports/substrate-l1_findings/chainflip-backend-audits-2023-04-trailofbits-securityreview-pdf.md | HIGH | Trail of Bits | Nonstandard ERC-20 tokens get stuck when depositing |
| [x4] | reports/substrate-l1_findings/acala-srl-2021-12.md | HIGH | SRLabs | Integer overflow in the xcm::v1 pallet could result in loss of asset tokens |
| [x5] | reports/substrate-l1_findings/phala-c4-2401.md | MEDIUM | Code4rena | [M-01] Limited availability of balance_of(...) method |
| [x6] | reports/substrate-l1_findings/composable-audits-solana-restaking-vaults-restaking-vaults-audit-pdf.md | CRITICAL | auditor | Missing Receipt Token Balance Check |
| [x7] | reports/substrate-l1_findings/composable-audits-solana-restaking-vaults-restaking-vaults-audit-pdf.md | HIGH | auditor | Stake Mint Differentiation |
| [x8] | reports/substrate-l1_findings/audit-reports-snowbridge-2025-01-07-audit-report-snowbridge-updates-3-v1-0-pdf.md | HIGH | auditor | Unauthorized minting of PNA assets due to missing origin validation |
| [x9] | reports/substrate-l1_findings/centrifuge-chainbridge-2020.md | CRITICAL | auditor | 4.2 Transfer functions of ERC20 tokens may return false Critical ✓ Addressed Resolution Addressed in https://github.com/ChainSafe/chainb |
| [x10] | reports/substrate-l1_findings/publicreports-substrate-audits-reef-chain-substrate-security-audit-report-halborn-v1-1-pdf.md | MEDIUM | Halborn | 3.2 (HAL-02) TOTAL ISSUANCE NOT UPDATED ON MINT - MEDIUM Description: The update_balance dispatchable defined in modules/currencies/src/lib. |
| [x11] | reports/substrate-l1_findings/reef-halborn.md | MEDIUM | Halborn | 3.2 (HAL-02) TOTAL ISSUANCE NOT UPDATED ON MINT - MEDIUM Description: The update_balance dispatchable defined in modules/currencies/src/lib. |
| [x12] | reports/substrate-l1_findings/t3rn-docs-main-static-halborn-sc-security-audit-pdf.md | HIGH | Halborn | 4.5 (HAL-05) POTENTIAL ERC20 TOKEN EXPLOIT - HIGH (7.5) Description: The LocalExchange contract’s localOrder function presents a potential v |
| [x13] | reports/substrate-l1_findings/starlay-oak-wasm.md | CRITICAL | Oak Security | Unnecessary underlying token conversion causes a loss of funds for the sender |
| [x14] | reports/substrate-l1_findings/starlay-oak-wasm.md | CRITICAL | Oak Security | Incorrect token denominations result in inaccurate amounts transacted |
| [x15] | reports/substrate-l1_findings/starlay-oak-wasm.md | HIGH | Oak Security | Double deduction of protocol seized tokens |
| [x16] | reports/substrate-l1_findings/starlay-oak-wasm.md | HIGH | Oak Security | Supporting markets with existing underlying tokens overwrites market pair |
| [x33] | reports/substrate-l1_findings/audits-interlay-informal-report-interlay-audit-2021q3-pdf.md | MEDIUM | Informal Systems | Systems InterBTC Parachain Modules and Vault Client IF-INTERLAY2-MINTING: Vault not banned precondition not enforced on minting tokens |
| [x34] | reports/substrate-l1_findings/hydradx-rv-stableswap-2023.md | HIGH | auditor | The asset balance of a pool can drop below the existential deposit |
| [x35] | reports/substrate-l1_findings/interlay-informal-2021q3.md | MEDIUM | Informal Systems | Systems InterBTC Parachain Modules and Vault Client IF-INTERLAY2-MINTING: Vault not banned precondition not enforced on minting tokens |
| [x36] | reports/substrate-l1_findings/manta-veridise-chain.md | MEDIUM | Veridise | Manta Network ©2023 Veridise Inc. 14 4 Vulnerability Report 4.1.4 V-MANC-VUL-004: Total supply of native assets can exceed the set limit |
| [x37] | reports/substrate-l1_findings/phala-blockchain-audit-code4rena-phat-contract-runtime-pdf.md | MEDIUM | auditor | Limited availability of balance_of(...) method |
| [x38] | reports/substrate-l1_findings/phala-blockchain-audit-code4rena-phat-contract-runtime-pdf.md | MEDIUM | auditor | Limited availability of balance_of(...) method fn balance_of( &self, account: ext::AccountId, ) -> Result<(pink::Balance, pink::Balance), Self::Error> |
| [q39] | reports/substrate-l1_findings/acala-slowmist-2020.md | LOW | SlowMist | Tokenstransferdoesnotuseoverflowpreventionmethods to calculate the amount |

## Token Issuance

**Token issuance patterns mined from uncited L1 audit reports** - representative of 16 findings mined from 11 L1 audit reports (Code4rena, Halborn, Oak Security, SRLabs, Trail of Bits, unknown).

### Overview

16 sec-tier findings (4 critical, 8 high, 4 medium) from 11 audit reports by Code4rena, Halborn, Oak Security, SRLabs, Trail of Bits, unknown. Titles in the references table are verbatim from the source reports; use them to route to the exact report for full PoC detail.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the token/issuance pallet paths path lacks the validation/bounding the cited reports identify."
- Pattern key: `issuance-accounting-gap | token pallet | mint/burn/transfer | supply mismatch`
- Interaction scope: `single_contract`
- Primary affected component(s): `token/issuance pallet paths`
- High-signal code keywords: `addition, addressed, amounts, asset, assets, availability`
- Typical sink / impact: `fund_loss`
- Validation strength: `unassessed` (evidence rows cite source reports; per-finding PoCs not yet re-verified)

#### Valid Bug Signals

- Signal 1: title evidence in cited reports matches the audited component family (token/issuance pallet paths)
- Signal 2: severity consensus across independent auditors (Code4rena, Halborn, Oak Security, SRLabs, Trail of Bits, unknown)
- Signal 3: impact-producing condition stated in source report (fund_loss)

#### False Positive Guards

- Not this bug when: the target chain/module already enforces explicit bounds/limits on the affected path
- Safe if: audited version postdates the fix noted in the source report status
- Requires attacker control of: the inputs named in the cited finding titles (messages, bids, deposits)

### Detection Patterns

#### High-Signal Grep Seeds
```
- addition
- addressed
- amounts
- asset
- assets
- availability
- balance
- balance_of
- causes
- certain
```

#### Audit Checklist
- [ ] Verify bounded iteration/gas on the affected path
- [ ] Check state-consistency guarantees across the failure paths cited above
- [ ] Compare implementation against the source-report recommendation

### Vulnerability Description

#### Root Cause

The cited reports describe token/issuance pallet paths paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `issuance-accounting-gap | token pallet | mint/burn/transfer | supply mismatch`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `issuance-accounting-gap | token pallet | mint/burn/transfer | supply mismatch | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `issuance-accounting-gap | token pallet | mint/burn/transfer | supply mismatch | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: Missing Receipt Token Balance Check** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Missing Receipt Token Balance Check
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Missing Receipt Token Balance Check
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: 4.2 Transfer functions of ERC20 tokens may return false Critical ✓ Addressed Resolution Addressed in https://github.com/** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// 4.2 Transfer functions of ERC20 tokens may return false Critical ✓ Addressed Resolution Addressed in https://github.com/ChainSafe/chainb
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: 4.2 Transfer functions of ERC20 tokens may return false Critical ✓ Addressed Resolution Addressed in
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: Unnecessary underlying token conversion causes a loss of funds for the sender** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Unnecessary underlying token conversion causes a loss of funds for the sender
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Unnecessary underlying token conversion causes a loss of funds for the sender
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

`addition, addressed, amounts, asset, assets, availability, balance, balance_of, causes, certain, chainb, chainsafe, check, complete`

### Related Vulnerabilities

- See references table; sibling entries under the same DB category folder
