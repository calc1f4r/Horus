---
# Core Classification
protocol: zcash
chain: zcash
category: transaction_construction
vulnerability_type: silent_data_mangling

# Pattern Identity
root_cause_family: encoding_semantic_gap
pattern_key: serialization_ambiguity_and_version_gaps | tx_builder_serialization | unvalidated_bundle_fields | txid_mismatch_or_fund_divergence

# Interaction Scope
interaction_scope: cross_protocol
involved_contracts:
  - librustzcash transaction builder (value balancing, burn amounts)
  - Orchard / transparent bundle serialization
  - PCZT verifier/signer role adapters
path_keys:
  - serialization_ambiguity_and_version_gaps | tx_builder | transparent bundle encode | txid_divergence
  - zip233_burn_bypass | tx_builder | value balancing | miner_payment
  - version_check_bypass | orchard change output | V4 txid computation | panic

# Attack Vector Details
attack_type: data_manipulation
affected_component: transaction_serialization_and_builder

# Technical Primitives
primitives:
  - transparent bundle serialization
  - txid / sighash computation
  - ZIP 233 burn amounts
  - Orchard note construction
  - version gating (V4/V5/V6, nu7, zip-233 feature flags)
  - merkle_path_from_slice witness parsing
  - PCZT role adapters

# Grep / Hunt-Card Seeds
code_keywords:
  - merkle_path_from_slice
  - zip233
  - burn_amount
  - transparent bundle
  - txid
  - sighash
  - V4 V5 V6 transaction version
  - nu7

# Impact Classification
severity: medium
impact: fund_divergence_and_panic
exploitability: 0.5
financial_impact: medium

# Context Tags
tags:
  - l1
  - rust
  - privacy chain
  - transaction builder
  - serialization
  - consensus adjacency

# Version Info
language: rust
version: "librustzcash, Zellic assessment June 22–July 2 2026"
---

## References & Source Reports

> All reference files verified to exist under `reports/other-l1_findings/`. The Zcash bucket is the largest non-EVM bucket in the raw index (8 findings): librustzcash, Ironwood upgrade, Sapling, Zakura, plus three Trail of Bits reviews and the security-warnings doc.

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [Z1] | reports/other-l1_findings/publications-zcash-librustzcash-zellic-audit-report-pdf.md | LOW ×4 + INFO | Zellic | Zellic for Valar Group, July 13 2026 — findings list verified verbatim from report contents (§3.1–3.5) |
| [Z2] | reports/other-l1_findings/publications-zcash-ironwood-upgrade-zellic-audit-report-pdf.md | (bucket) | Zellic | Index-verified; Ironwood bundle-encoding scope overlaps [Z1] §4.1 |
| [Z3] | reports/other-l1_findings/publications-zcash-sapling-zellic-audit-report-pdf.md | (bucket) | Zellic | Index-verified |
| [Z4] | reports/other-l1_findings/publications-reviews-zcash-pdf.md | (bucket) | Trail of Bits | Index-verified (one of three ToB zcash reviews: zcash, zcash2, zcashwp) |

## librustzcash Transaction Builder: Silent Mangling, Burn Bypass, and Version-Gate Gaps

### Overview

Zellic's librustzcash assessment found a coherent family of **encoding/semantic gaps in the transaction builder and serialization layer**: ZIP-233 burn amounts can be silently dropped and paid to the miner instead of burned ([Z1] §3.1); an empty witness slice panics in `merkle_path_from_slice` ([Z1] §3.2); an **empty transparent bundle serializes identically to an absent one but yields a different txid and sighash** ([Z1] §3.3); an Orchard change output bypasses the version check and panics while computing a V4 transaction's txid ([Z1] §3.4); and building with `nu7` but without `zip-233` produces invalid V6 transactions ([Z1] §3.5).

#### Agent Quick View

- Root cause statement: "This vulnerability exists because serialization treats distinct logical states (empty vs absent bundle, burn vs transfer) as equivalent on the wire while txid/sighash and value-balancing treat them differently — and feature flags (nu7, zip-233) are not cross-validated."
- Pattern key: `serialization_ambiguity_and_version_gaps | tx_builder_serialization | unvalidated_bundle_fields | txid_mismatch_or_fund_divergence`
- Interaction scope: `cross_protocol` (library ↔ consensus rules ↔ downstream wallets/exchanges)
- Primary affected component(s): `transaction builder, transparent/Orchard bundle encoding, txid & sighash computation, value balancing`
- Contracts / modules involved: `librustzcash builder, Orchard/Ironwood bundle encoding, PCZT adapters, merkle witness parsing`
- Path keys: `serialization_ambiguity_and_version_gaps | tx_builder | transparent bundle encode | txid_divergence` · `zip233_burn_bypass | tx_builder | value balancing | miner_payment`
- High-signal code keywords: `merkle_path_from_slice, zip233, burn_amount, txid, sighash, nu7, transparent bundle`
- Typical sink / impact: `funds paid to miner instead of burned; wallet/exchange txid mismatches; panics in integrator codebases; invalid V6 txs`
- Validation strength: `strong` (all five findings verified verbatim from [Z1] report contents)

#### Contract / Boundary Map

- Entry surface(s): `Builder::build()`, bundle serialization (`to_bytes`/`from_slice`), PCZT verifier/signer adapters, `merkle_path_from_slice`
- Contract hop(s): `wallet/integrator -> librustzcash builder -> consensus encoding -> network & miners`
- Trust boundary crossed: `library API boundary — integrators assume builder output is canonical and burn-safe`
- Shared state or sync assumption: `wire bytes must uniquely determine txid/sighash; value balance must account burns as burns, not transfers`

#### Valid Bug Signals

- Signal 1: A burn output ([Z1] §3.1, ZIP 233) can be represented as an ordinary output during building → value balancing routes it to the miner rather than removing it from circulation.
- Signal 2: Two logically distinct states (empty transparent bundle vs absent bundle, §3.3) serialize to identical bytes but compute different txids/sighashes → integrators tracking by txid diverge from consensus.
- Signal 3: Library features (`nu7`, `zip-233`) can be enabled independently (§3.5) → builder produces transactions invalid under consensus.
- Signal 4: Empty input slices reach `merkle_path_from_slice` (§3.2) or Orchard change reaches a V4 txid computation (§3.4) → panic in integrator process.

#### False Positive Guards

- Not this bug when: the builder explicitly rejects empty transparent bundles or normalizes them to `None` with a single canonical encoding.
- Not this bug when: burn semantics are enforced by a dedicated type (e.g., a `Burn` variant distinct from `Transfer`) that value-balancing handles separately.
- Safe if: feature flags have compile-time mutual-exclusion (e.g., `nu7` implies `zip-233` via cfg constraint) and version checks run before any txid computation.
- Requires attacker control of: transaction inputs to the library (malicious or buggy integrator), empty/malformed witness slices — panics require only malformed data, not an adversary.
- Findings are low/info severity per Zellic: no consensus break of Zcash itself; impact lands on integrators using the library incorrectly-but-plausibly.

### Vulnerability Description

#### Root Cause

1. **Burn semantics not type-enforced** (§3.1): ZIP-233 burn amounts flow through the same value-balancing as transfers, so a burn can be silently dropped and redirected to the miner.
2. **Missing empty-slice guard** (§3.2): `merkle_path_from_slice(&[])` panics instead of returning an error.
3. **Encoding ambiguity empty-vs-absent** (§3.3): an empty transparent bundle and an absent one serialize identically but produce different txid/sighash — a consensus-adjacent identity mismatch.
4. **Version check bypass for Orchard change** (§3.4): an Orchard change output on a V4 transaction bypasses the version gate and panics inside txid computation.
5. **Independent feature flags** (§3.5): `nu7` without `zip-233` builds invalid V6 transactions.

#### Attack Scenario / Path Variants

**Path A: ZIP-233 burn redirected to miner**
Path key: `zip233_burn_bypass | tx_builder | value balancing | miner_payment`
Entry surface: builder API with burn output
1. Integrator constructs a tx with a ZIP-233 burn amount.
2. Burn is dropped from the burn accounting path during building.
3. Value balancing still balances, but the amount lands as miner fee/payment.
4. Supply is not reduced; "burned" funds are instead collected by the miner — silent divergence from the user's intent.

**Path B: txid divergence via empty-vs-absent transparent bundle**
Path key: `serialization_ambiguity_and_version_gaps | tx_builder | transparent bundle encode | txid_divergence`
Entry surface: builder producing an empty transparent bundle
1. Integrator builds a tx where the transparent bundle ends up empty rather than absent.
2. Wire bytes are identical to the absent case.
3. txid/sighash computed by the library differ from what other implementations compute for the same bytes.
4. Wallets/exchanges track a different txid → confirmation tracking, replay checks, and signing break.

**Path C: Panics and invalid versions from unvalidated inputs**
Path key: `version_check_bypass | orchard change output | V4 txid computation | panic`
1. Empty witness slice → `merkle_path_from_slice` panic (§3.2); or Orchard change output on V4 tx bypasses the version check → panic in txid computation (§3.4); or `nu7` without `zip-233` → invalid V6 tx accepted by builder (§3.5).
2. Integrator process crashes or broadcasts an invalid transaction.
3. Liveness/integrity issue for the integrator, not for consensus.

#### Vulnerable Pattern Examples

> Reconstructed from [Z1] §3.1–3.5 finding descriptions; Rust pseudocode preserving audited identifiers.

**Example 1: Burn dropped in value balancing** [Approx Vulnerability : LOW-MEDIUM]
```rust
// ❌ VULNERABLE: ZIP-233 burn treated like any other output ([Z1] §3.1)
let tx = builder.build(StandardFee::new(fee))?; // burn amount in outputs
// value balancing sums transparent+sapling+orchard; a dropped burn entry
// is silently compensated by a higher miner payment:
//   intended: 10 ZEC burned  ->  actual: 10 ZEC to miner, nothing burned
```

**Example 2: Empty vs absent transparent bundle txid mismatch** [Approx Vulnerability : LOW-MEDIUM]
```rust
// ❌ VULNERABLE: two states, same wire bytes, different txid ([Z1] §3.3)
let tx_a = TxData { transparent: Some(Bundle::empty()), .. }; // "empty"
let tx_b = TxData { transparent: None, .. };                   // "absent"
assert_eq!(tx_a.to_bytes(), tx_b.to_bytes());  // identical serialization
// but compute_txid(tx_a) != compute_txid(tx_b) per audited finding — sighash too
```

**Example 3: Panic paths on unvalidated input** [Approx Vulnerability : LOW]
```rust
// ❌ VULNERABLE: panics instead of errors ([Z1] §3.2, §3.4)
let path = merkle_path_from_slice(&witness_bytes)?; // panics on empty slice
let txid = v4_txid(&tx_with_orchard_change);         // version check bypassed -> panic
```

### Impact Analysis

#### Technical Impact
- Burned funds silently redirected to miners (supply integrity for asset issuers relying on ZIP-233)
- txid/sighash divergence across implementations → double-spend-detection and replay-protection confusion in integrators
- Panics crash wallets/exchange signing services (DoS on the integrator)
- Invalid V6 transactions built under mismatched feature flags

#### Business Impact
- Zellic rated all findings low/info — impact concentrates on integrators, not the chain
- Exchange txid-tracking mismatches can misreport deposits/withdrawals

#### Affected Scenarios
- Wallets/exchanges building zcash transactions via librustzcash with edge-case bundles
- Issuers using ZIP-233 burns for supply control
- Builds combining feature flags inconsistently (`nu7` on, `zip-233` off)

### Secure Implementation

**Fix 1: Canonical states, typed burns, cross-checked flags, errors over panics**
```rust
// ✅ SECURE: enforce one canonical representation, typed burn, flag implication, Result-based parsing
impl Builder {
    pub fn build(self) -> Result<Transaction, BuildError> {
        // §3.3 fix: normalize — never emit an empty bundle
        let transparent = match self.transparent {
            Some(b) if b.is_empty() => None,
            other => other,
        };
        // §3.1 fix: burns are a distinct typed output participating in value balance
        let value_balance = self.outputs.iter()
            .map(|o| match o { Out::Burn(v) => -v, Out::Transfer(v) => *v })
            .sum::<i64>();
        // §3.5 fix: compile-time flag implication
        #[cfg(all(feature = "nu7", not(feature = "zip-233")))]
        compile_error!("nu7 requires zip-233");
        ...
    }
}
// §3.2/§3.4 fix: parse/verify before compute, return errors
pub fn merkle_path_from_slice(bytes: &[u8]) -> Result<MerklePath, ParseError> {
    if bytes.is_empty() { return Err(ParseError::EmptyWitness); } // no panic
    ...
}
pub fn compute_txid(tx: &TxData) -> Result<TxId, BuildError> {
    if tx.version == V4 && tx.orchard_change.is_some() {
        return Err(BuildError::OrchardChangeOnV4); // version gate before computation
    }
    ...
}
```

### Detection Patterns

#### High-Signal Grep Seeds
```
- merkle_path_from_slice
- zip233
- burn_amount
- txid
- sighash
- nu7
```

#### Code Patterns to Look For
```
- Option<Bundle> where Some(empty) and None both serialize (no normalization)
- burn values stored in the same field/variant as transfers
- unwrap()/expect()/panic! reachable from deserialization or tx building
- independent feature flags that consensus couples (cfg nu7 vs cfg zip-233)
```

#### Audit Checklist
- [ ] Does every logically distinct tx state have a unique canonical encoding?
- [ ] Are burn outputs a distinct type in value balancing?
- [ ] Can any empty slice or wrong-version bundle reach a computation before validation?
- [ ] Do consensus-coupled feature flags have compile-time mutual constraints?

### Real-World Examples

#### Known Exploits
- None cited in [Z1]; class is integrator-impact (silent misrouting, panics), not chain exploits.

#### Related CVEs/Reports
- [Z1] Zellic, librustzcash Application Security Assessment, 13 July 2026 (findings §3.1–3.5)
- [Z2] Zellic, Zcash Ironwood upgrade audit (bundle-encoding overlap)
- [Z3] Zellic, Zcash Sapling audit
- [Z4] Trail of Bits zcash reviews (publications-reviews-zcash{,2,wp})

### Keywords for Search

`zcash`, `librustzcash`, `sapling`, `orchard`, `ironwood`, `transparent bundle`, `txid`, `sighash`, `zip 233`, `burn amount`, `value balancing`, `merkle path`, `witness slice`, `V4 transaction`, `V6 transaction`, `nu7`, `feature flag`, `serialization ambiguity`, `PCZT`, `transaction builder`, `rust`

### Related Vulnerabilities

- DB/unique/l1-misc/avalanche-node-validation.md (encoding/validation gaps at protocol boundaries)
- DB/tokens/ burn-semantics entries (burn vs transfer confusion)
