---
# Core Classification
protocol: generic
chain: cosmos
category: access_control
vulnerability_type: key_signature_handling
root_cause_family: missing_validation

# Pattern Identity
pattern_key: signature-validation-gap | signer verification | crafted tx | unauthorized action

# Interaction Scope
interaction_scope: single_contract
involved_contracts:
  - keys/signature verification paths

# Attack Vector Details
attack_type: spoofing
affected_component: keys/signature verification paths

# Technical Primitives
primitives:
  - across
  - adaptor
  - addresses
  - allowing
  - allows
  - already

# Grep / Hunt-Card Seeds
code_keywords:
  - across
  - adaptor
  - addresses
  - allowing
  - allows
  - already
  - argument
  - attacks
  - backend
  - before

severity: critical
impact: fund_loss
language: rust
tags:
  - access_control
  - l1
  - cosmos
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [k1] | reports/cosmos-l1-nodes_findings/audit-reports-avail-2026-01-15-audit-report-avail-cosmos-and-backend-changes-v1-0-pdf.md | CRITICAL | Oak Security | Refund logic allows already fulfilled requests to be reimbursed, allowing double spends and prematurely refunded deposits, resulting in locked liquidi |
| [k2] | reports/cosmos-l1-nodes_findings/audit-reports-avail-2026-01-15-audit-report-avail-cosmos-and-backend-changes-v1-0-pdf.md | HIGH | Oak Security | Transient DSG send failures slip through retries and stall key operations |
| [k3] | reports/cosmos-l1-nodes_findings/audit-reports-avail-2026-01-15-audit-report-avail-cosmos-and-backend-changes-v1-0-pdf.md | HIGH | Oak Security | Compromised SIWE signature enables permanent theft of derived Cosmos and ephemeral wallets |
| [k4] | reports/cosmos-l1-nodes_findings/audit-reports-axelar-audit-report-axelar-pdf.md | HIGH | Oak Security | Non-unique key for identifying voting topics implementations may lead to lost proposals |
| [k5] | reports/cosmos-l1-nodes_findings/audit-reports-babylon-2025-06-12-audit-report-babylon-v1-0-pdf.md | HIGH | Oak Security | Missing TLS credentials and HMAC key in gRPC client enables credential compromise and MITM attacks |
| [k6] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-10-28-audit-report-comdex-locking-and-vesting-contracts-v1-0-pdf.md | HIGH | Oak Security | Incorrect key results in incorrect calculations in calculate_bribe_reward function |
| [k7] | reports/cosmos-l1-nodes_findings/audit-reports-cosmos-2023-06-23-audit-report-cosmos-interchain-security-v1-0-pdf.md | CRITICAL | Oak Security | A validator updating its ConsumerKey to the same key causes a panic in the related consumer chain |
| [k8] | reports/cosmos-l1-nodes_findings/audit-reports-dorahacks-2024-03-04-audit-report-dorahacks-quadratic-grant-injective-v1-0-pdf.md | CRITICAL | Oak Security | Signatures can be replayed across different chains, networks, and contract addresses |
| [k9] | reports/cosmos-l1-nodes_findings/audit-reports-dorahacks-2024-03-04-audit-report-dorahacks-quadratic-grant-injective-v1-0-pdf.md | HIGH | Oak Security | Signatures can be replayed within one hour before expiration |
| [k10] | reports/cosmos-l1-nodes_findings/audit-reports-interchain-foundation-2022-07-20-audit-report-liquidity-staking-cosmos-sdk-modules-v1-0-pdf.md | CRITICAL | Oak Security | Using non-prefixed addresses in storage keys can lead to key collisions, allowing exploits to overwrite data |
| [k11] | reports/cosmos-l1-nodes_findings/audit-reports-persistence-2022-01-20-audit-report-persistence-bridge-v1-0-pdf.md | CRITICAL | Oak Security | Retry logic can cause unlimited fees and potentially spend user funds |
| [k12] | reports/cosmos-l1-nodes_findings/audits-anoma-2024-12-11-namada-governance-pgf-pdf.md | CRITICAL | Informal Systems | Proposal type key modification |
| [k13] | reports/cosmos-l1-nodes_findings/audits-anoma-2024-12-11-namada-governance-pgf-pdf.md | CRITICAL | Informal Systems | Proposal funds key modification |
| [k14] | reports/cosmos-l1-nodes_findings/audits-osmosis-2023-30-10-audit-fee-abstraction-module-by-notional-pdf.md | CRITICAL | Informal Systems | Critical Risk of Non-Uniqueness in KVStore Keys |
| [k15] | reports/cosmos-l1-nodes_findings/publications-babylon-genesis-chain-zellic-audit-report-pdf.md | CRITICAL | Zellic | Nonce reuse in adaptor signatures allows recovering signing key |
| [k16] | reports/cosmos-l1-nodes_findings/publications-babylon-genesis-chain-zellic-audit-report-pdf.md | CRITICAL | Zellic | Incorrect parity check in adaptor signatures |
| [k17] | reports/cosmos-l1-nodes_findings/publications-babylon-genesis-chain-zellic-audit-report-pdf.md | HIGH | Zellic | BLS keystore password is stored as plaintext |
| [k18] | reports/cosmos-l1-nodes_findings/publications-babylon-genesis-chain-zellic-audit-report-pdf.md | MEDIUM | Zellic | The test keyring backend is used |
| [k19] | reports/cosmos-l1-nodes_findings/publications-reviews-umee-pdf.md | MEDIUM | Trail of Bits | Insecure storage of price-feeder keyring passwords |
| [k20] | reports/cosmos-l1-nodes_findings/publications-reviews-umee-pdf.md | MEDIUM | Trail of Bits | Peggo takes an Ethereum private key as a command-line argument |
| [k21] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-boostylabs-tricorn-bridge-server-golang-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | PRIVATE SSH KEYS COMMITTED TO GIT REPOSITORY |
| [k22] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | LOANS CAN BE REPAID WITHOUT SPENDING COINS |
| [k23] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-sienna-network-amm-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | SIGNATURE VALIDATION CAN BE BYPASSED |
| [k47] | reports/cosmos-l1-nodes_findings/publications-osmosis-authentication-abstraction-zellic-audit-report-pdf.md | CRITICAL | Zellic | Signatureauthenticatorauthenticationbypass • Target:x/authenticator/authenticator/ante.go • Category:CodingMistakes • Likelihood:High • |
| [w48] | reports/cosmos-l1-nodes_findings/audits-anoma-anoma-q3-2025-token-token-distributor-audit-report-final-v3-pdf.md | MEDIUM | Immunefi (warden) | audits-anoma-anoma-q3-2025-token-token-distributor-audit-report-final-v3 |
| [w49] | reports/cosmos-l1-nodes_findings/audits-anoma-anoma-q4-2025-risc-zero-rm-evm-protocol-adapter-audit-final-report-v2-pdf.md | MEDIUM | Immunefi (warden) | audits-anoma-anoma-q4-2025-risc-zero-rm-evm-protocol-adapter-audit-final-report-v2 |
| [w50] | reports/cosmos-l1-nodes_findings/audits-espresso-espresso-q1-2025-epoch-change-protocol-audit-report-final-pdf.md | CRITICAL | Immunefi (warden) | audits-espresso-espresso-q1-2025-epoch-change-protocol-audit-report-final |
| [w51] | reports/cosmos-l1-nodes_findings/audits-interlay-informal-report-interlay-audit-2021q2-pdf.md | MEDIUM | Immunefi (warden) | audits-interlay-informal-report-interlay-audit-2021q2 |
| [w52] | reports/cosmos-l1-nodes_findings/publications-cosmos-sdk-sign-mode-textual-zellic-audit-report-pdf.md | CRITICAL | Immunefi (warden) | publications-cosmos-sdk-sign-mode-textual-zellic-audit-report |
| [q53] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2023-08-18-audit-report-cosmwasm-wbtc-v1-0-pdf.md | INFO | Oak Security | Storage entries spread across multiple files increase the chances of storage key collision |
| [q54] | reports/cosmos-l1-nodes_findings/publicauditreports-nm0405-final-gaia-network-token-pdf.md | LOW | Nethermind | Signers cannot cancel permit signatures before the deadline in GaiaToken |

## Key Management

**Key management patterns mined from uncited L1 audit reports** - representative of 23 findings mined from 15 L1 audit reports (Halborn, Informal Systems, Oak Security, Trail of Bits, Zellic).

### Overview

23 sec-tier findings (12 critical, 8 high, 3 medium) from 15 audit reports by Halborn, Informal Systems, Oak Security, Trail of Bits, Zellic. Titles in the references table are verbatim from the source reports; use them to route to the exact report for full PoC detail.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the keys/signature verification paths path lacks the validation/bounding the cited reports identify."
- Pattern key: `signature-validation-gap | signer verification | crafted tx | unauthorized action`
- Interaction scope: `single_contract`
- Primary affected component(s): `keys/signature verification paths`
- High-signal code keywords: `across, adaptor, addresses, allowing, allows, already`
- Typical sink / impact: `fund_loss`
- Validation strength: `unassessed` (evidence rows cite source reports; per-finding PoCs not yet re-verified)

#### Valid Bug Signals

- Signal 1: title evidence in cited reports matches the audited component family (keys/signature verification paths)
- Signal 2: severity consensus across independent auditors (Halborn, Informal Systems, Oak Security, Trail of Bits, Zellic)
- Signal 3: impact-producing condition stated in source report (fund_loss)

#### False Positive Guards

- Not this bug when: the target chain/module already enforces explicit bounds/limits on the affected path
- Safe if: audited version postdates the fix noted in the source report status
- Requires attacker control of: the inputs named in the cited finding titles (messages, bids, deposits)

### Detection Patterns

#### High-Signal Grep Seeds
```
- across
- adaptor
- addresses
- allowing
- allows
- already
- argument
- attacks
- backend
- before
```

#### Audit Checklist
- [ ] Verify bounded iteration/gas on the affected path
- [ ] Check state-consistency guarantees across the failure paths cited above
- [ ] Compare implementation against the source-report recommendation

### Vulnerability Description

#### Root Cause

The cited reports describe keys/signature verification paths paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `signature-validation-gap | signer verification | crafted tx | unauthorized action`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `signature-validation-gap | signer verification | crafted tx | unauthorized action | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `signature-validation-gap | signer verification | crafted tx | unauthorized action | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: Refund logic allows already fulfilled requests to be reimbursed, allowing double spends and prematurely refunded deposit** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Refund logic allows already fulfilled requests to be reimbursed, allowing double spends and prematurely refunded deposits, resulting in locked liquidi
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Refund logic allows already fulfilled requests to be reimbursed, allowing double spends and prematur
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: A validator updating its ConsumerKey to the same key causes a panic in the related consumer chain** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// A validator updating its ConsumerKey to the same key causes a panic in the related consumer chain
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: A validator updating its ConsumerKey to the same key causes a panic in the related consumer chain
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: Signatures can be replayed across different chains, networks, and contract addresses** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Signatures can be replayed across different chains, networks, and contract addresses
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Signatures can be replayed across different chains, networks, and contract addresses
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

`across, adaptor, addresses, allowing, allows, already, argument, attacks, backend, before, bypassed, calculate_bribe_reward, calculations, cause`

### Related Vulnerabilities

- See references table; sibling entries under the same DB category folder
