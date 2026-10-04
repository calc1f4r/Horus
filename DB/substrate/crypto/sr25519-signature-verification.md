---
# Core Classification
protocol: edgeware
chain: polkadot
category: crypto
vulnerability_type: signature_verification_bypass
root_cause_family: missing_validation

# Pattern Identity
pattern_key: missing-edge-case-check | sr25519 signature verification | non-canonical / identity-point input | invalid signature accepted

# Interaction Scope
interaction_scope: single_contract
involved_contracts:
  - micro-sr25519 index.ts (verify)
  - scure-sr25519 index.ts (verify)
path_keys:
  - missing-edge-case-check | sr25519_verify | identity-point public key | invalid signature accepted
  - missing-edge-case-check | sr25519_verify | non-canonical signature decode | verification malleability
  - missing-edge-case-check | sr25519_verify | empty transcript label | broken domain separation

# Attack Vector Details
attack_type: input_validation_bypass
affected_component: signature_verification (sr25519_verify)

# Technical Primitives
primitives:
  - schnorrkel_sr25519
  - ristretto255_point
  - point_at_infinity_identity_check
  - scalar_canonicality
  - merlin_transcript_domain_separation
  - ed25519_key_encoding
  - timing_side_channel

# Grep / Hunt-Card Seeds
code_keywords:
  - sr25519_verify
  - pointAtInfinity
  - identity
  - transcript
  - vrfVerify
  - secretKey
  - ed25519
  - Scalar

severity: low
impact: invalid_signature_accepted
language: rust
tags:
  - substrate
  - crypto
  - sr25519
  - schnorrkel
  - signature_verification
  - ristretto255
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [micro1] | reports/substrate-l1_findings/audit-reports-polkadot-2025-06-12-audit-report-polkadot-micro-sr25519-v1-0-pdf.md | MINOR | Oak Security (for Edgeware DAO) | #1 public key point-at-infinity not checked (`index.ts:308-311`) |
| [micro4] | reports/substrate-l1_findings/audit-reports-polkadot-2025-06-12-audit-report-polkadot-micro-sr25519-v1-0-pdf.md | MINOR | Oak Security (for Edgeware DAO) | #4 incomplete signature format validation (`index.ts:301-304`) |
| [micro2] | reports/substrate-l1_findings/audit-reports-polkadot-2025-06-12-audit-report-polkadot-micro-sr25519-v1-0-pdf.md | MINOR | Oak Security (for Edgeware DAO) | #2 empty transcript label breaks domain separation |
| [micro5] | reports/substrate-l1_findings/audit-reports-polkadot-2025-06-12-audit-report-polkadot-micro-sr25519-v1-0-pdf.md | INFO/MINOR | Oak Security (for Edgeware DAO) | #5 timing side-channel in verification |
| [micro9] | reports/substrate-l1_findings/audit-reports-polkadot-2025-06-12-audit-report-polkadot-micro-sr25519-v1-0-pdf.md | INFO | Oak Security (for Edgeware DAO) | #9 unbounded input size → DoS |
| [scure1] | reports/substrate-l1_findings/audit-reports-polkadot-2025-08-22-audit-report-polkadot-scure-sr25519-v1-5-pdf.md | MINOR | Oak Security (for Edgeware DAO) | #1 point-at-infinity not checked on public key (`index.ts:484-487`) |
| [fuzz1] | reports/substrate-l1_findings/audit-reports-polkadot-2025-06-12-differential-fuzz-testing-report-polkadot-micro-sr25519-v1-0-pdf.md | INFO | Oak Security (for Edgeware DAO) | secret keys encoded as ed25519 bytes ≠ schnorrkel default encoding (differential mismatch) |
| [x10] | reports/substrate-l1_findings/chainflip-backend-audits-multisig-kudelski-q1-2022-pdf.md | MEDIUM | Kudelski | Possible DoS Attack in FROST KeyGen |
| [x11] | reports/substrate-l1_findings/starlay-oak-wasm.md | CRITICAL | Oak Security | Unauthorized pool liquidation threshold modiﬁcation |

> Note: `[micro2]` label above uses the same underlying report path — all micro-sr25519 rows cite `audit-reports-polkadot-2025-06-12-audit-report-polkadot-micro-sr25519-v1-0-pdf.md`. Audits were performed by Oak Security for the Edgeware DAO (not SRLabs).

## Missing Point-at-Infinity and Canonicality Checks in sr25519 Signature Verification

**sr25519 (schnorrkel/Ristretto255) verification implementations that skip edge-case validation — identity-point public keys, non-canonical encodings, empty transcript labels — accept inputs the reference schnorrkel implementation rejects, enabling forged/malleable verification results and cross-implementation consensus divergence** - representative of any Substrate-ecosystem reimplementation of sr25519 outside the canonical Rust `schnorrkel` crate.

### Overview

Oak Security's audits of `micro-sr25519` (2025-06-12) and `scure-sr25519` v1.5/1.6 (2025-08-22) — TypeScript sr25519 implementations for the Polkadot ecosystem — found 11 findings, all Minor/Info, dominated by missing edge-case checks in `verify()`: no point-at-infinity check on the public key, incomplete signature format validation, empty transcript label, timing side-channel, and unbounded input size. A differential fuzzing report additionally showed secret keys encoded as ed25519 bytes diverge from the schnorrkel default encoding.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the verification routine decodes points/scalars without enforcing canonicality and identity-point rejection, so inputs the reference schnorrkel implementation rejects (or maps differently) are accepted here."
- Pattern key: `missing-edge-case-check | sr25519 signature verification | non-canonical / identity-point input | invalid signature accepted`
- Interaction scope: `single_contract`
- Primary affected component(s): `sr25519_verify, key/signature decoding, transcript initialization`
- Contracts / modules involved: `micro-sr25519 index.ts, scure-sr25519 index.ts`
- Path keys: `identity-point public key`, `non-canonical signature decode`, `empty transcript label`
- High-signal code keywords: `sr25519_verify, pointAtInfinity, transcript, vrfVerify, secretKey, ed25519`
- Typical sink / impact: `invalid signature accepted / malleability / cross-implementation consensus divergence`
- Validation strength: `moderate` (professional audits; all findings Minor/Info — no exploitable fund-loss path demonstrated)

#### Contract / Boundary Map

- Entry surface(s): `verify(signature, message, publicKey)`, `vrfVerify`, secret-key import/export helpers
- Contract hop(s): `caller -> sr25519_verify -> point decode -> transcript (merlin/STROBE) -> scalar check`
- Trust boundary crossed: `off-chain/off-runtime crypto library boundary — any pallet, bridge, or wallet trusting this verification for authentication`
- Shared state or sync assumption: `verification results must match the reference schnorrkel implementation bit-for-bit or chains/indexers diverge`

#### Valid Bug Signals

- Signal 1: A public key or signature component is decoded to a curve point without checking for the identity/point-at-infinity (`index.ts:308-311`, `index.ts:484-487`).
- Signal 2: Scalar/signature byte strings are accepted without canonical (low-order / high-bit / non-reduced form) validation (`index.ts:301-304`).
- Signal 3: The transcript is initialized with an empty or constant label, so different protocols share a signing domain (cross-protocol signature replay).
- Signal 4: Differential fuzzing against reference schnorrkel produces accept/reject mismatches on any input class.

#### False Positive Guards

- Not this bug when: the implementation delegates all point/scalar arithmetic to a vetted Ristretto255 library that rejects non-canonical encodings by construction.
- Safe if: verification is only used with keys generated in-process and never on attacker-supplied key material (still weak — flag as defense-in-depth gap, not a reportable bug).
- Requires attacker control of: the public key blob, signature blob, or message bytes passed to `verify` (e.g., arbitrary account registration, bridge signature submission).
- Do not over-rate: all findings here are Minor/Info — no direct fund-loss path; severity comes from consensus divergence and malleability in downstream multisig/governance/bridge verification.

### Vulnerability Description

#### Root Cause

Reimplementing schnorrkel verification requires rejecting degenerate inputs the math library tolerates. The audited implementations (a) never checked whether the decoded public key is the point at infinity (identity element) — so an identity-point "public key" verifies without possession of any secret key ([micro1], [scure1]); (b) accepted non-canonical signature encodings ([micro4]); (c) initialized the transcript with an empty label, removing domain separation between protocols ([micro2]); (d) leaked timing information ([micro5]); (e) performed no length bounds on inputs, allowing DoS ([micro9]).

#### Attack Scenario / Path Variants

**Path A: Identity-point public key verifies without a secret key**
Path key: `missing-edge-case-check | sr25519_verify | identity-point public key | invalid signature accepted`
Entry surface: `verify(signature, message, publicKey)`
Contracts touched: `sr25519_verify -> point decode`
1. Attacker submits the identity point (point at infinity) as a public key to whatever registration/verification surface consumes the library.
2. Verification succeeds for crafted signatures without the attacker holding any secret scalar.
3. Any account/bridge/multisig auth built on this verify accepts the attacker as valid.

**Path B: Non-canonical signature malleability**
Path key: `missing-edge-case-check | sr25519_verify | non-canonical signature decode | verification malleability`
Entry surface: `verify(signature, message, publicKey)` with `index.ts:301-304` decode path
1. Attacker takes a valid signature and produces non-canonical variants (non-reduced scalars, non-canonical point encodings).
2. Each variant verifies as a "distinct" signature.
3. Signature-uniqueness assumptions (replay protection, nonce tracking) break.

**Path C: Cross-implementation divergence via key encoding**
Path key: `missing-edge-case-check | secret key import | ed25519-encoded secret key | consensus divergence`
Entry surface: secret-key serialization helpers ([fuzz1])
1. A key is exported/imported as raw ed25519 bytes instead of schnorrkel's `SecretKey` encoding (or vice versa).
2. The two implementations derive different public keys / verification results for the "same" key material.
3. Chains, indexers, or bridges using different implementations disagree on validity.

#### Vulnerable Pattern Examples

**Example 1: No point-at-infinity check on the public key (from [micro1], [scure1])** [Approx Vulnerability : LOW]
```rust
// ❌ VULNERABLE: index.ts:308-311 (micro-sr25519) / index.ts:484-487 (scure-sr25519)
// Public key decoded to a point, identity element never rejected
pub fn sr25519_verify(signature: &[u8; 64], message: &[u8], public_key: &[u8; 32]) -> bool {
    let pk_point = decompress_point(public_key); // accepts identity point
    // MISSING: if pk_point.is_identity() { return false; }
    verify_inner(signature, message, &pk_point) // identity point verifies without secret key
}
```

**Example 2: Incomplete signature format validation (from [micro4])** [Approx Vulnerability : LOW]
```rust
// ❌ VULNERABLE: index.ts:301-304 — non-canonical components accepted
pub fn decode_signature(sig: &[u8]) -> Option<Signature> {
    let r = decompress_point(&sig[..32])?;          // no canonicality enforcement
    let s = Scalar::from_bytes_mod_order(&sig[32..]); // wraps non-reduced scalars instead of rejecting
    Some(Signature { r, s })                          // malleable: non-canonical s accepted
}
```

**Example 3: Empty transcript label kills domain separation (from [micro2])** [Approx Vulnerability : LOW]
```rust
// ❌ VULNERABLE: transcript initialized with empty/constant label
let mut transcript = Transcript::new(b""); // empty label — all protocols share one domain
transcript.append_message(b"", payload);    // signature valid across otherwise-distinct protocols
```

**Example 4: Unbounded input size (from [micro9])** [Approx Vulnerability : LOW]
```rust
// ❌ VULNERABLE: no length cap before hashing/processing
pub fn verify(signature: &[u8], message: &[u8], public_key: &[u8]) -> bool {
    // attacker submits multi-MB messages; per-call cost unbounded -> DoS on APIs/indexers
    process_without_bound(message)
}
```

### Impact Analysis

#### Technical Impact

- Verification bypass primitives: identity-point keys verify without secret keys; malleable signatures break uniqueness assumptions.
- Cross-implementation divergence (Rust `schnorrkel` vs TS reimplementation) → chain/indexer/bridge disagreement on validity ([fuzz1]).
- Timing side-channel leaks secret-dependent computation shape ([micro5]); unbounded inputs enable resource-exhaustion ([micro9]).

#### Business Impact

- All 11 findings Minor/Info: no direct fund-loss exploit demonstrated. The risk is concentrated in downstream systems (multisig wallets, bridge relayer auth, governance identity) that treat `verify() == true` as proof of key possession.

#### Affected Scenarios

- Any parachain tooling, wallet, or bridge verifying sr25519 signatures outside the canonical Rust `schnorrkel` crate.
- Systems that import/export sr25519 key material using ed25519 byte encodings ([fuzz1]).
- Signature-uniqueness / replay-protection logic layered on a malleable verify.

### Secure Implementation

**Fix 1: Reject degenerate and non-canonical inputs explicitly**
```rust
// ✅ SECURE: mirror schnorrkel's own edge-case checks
pub fn sr25519_verify(signature: &[u8; 64], message: &[u8], public_key: &[u8; 32]) -> bool {
    let Ok(pk) = PublicKey::from_bytes(public_key) else { return false };
    if pk.point().is_identity() { return false; }        // point-at-infinity check (fixes #1)
    let Ok(sig) = Signature::from_bytes(signature) else { return false };
    if !sig.s.is_canonical() { return false; }           // canonical scalar (fixes #4)
    schnorrkel::verify(&sig, message, &pk).is_ok()
}
```

**Fix 2: Domain-separated transcript + bounded inputs + constant-time paths**
```rust
// ✅ SECURE: per-protocol label, length caps, constant-time verification
let mut transcript = Transcript::new(b"my-protocol-sr25519-v1"); // non-empty unique label (fixes #2)
ensure!(message.len() <= MAX_MSG_LEN, Error::MessageTooLarge);   // bound work (fixes #9)
constant_time_verify(&sig, message, &pk, &mut transcript);       // no secret-dependent branches (fixes #5)
```

### Detection Patterns

#### High-Signal Grep Seeds
```
- sr25519_verify
- pointAtInfinity
- identity
- transcript
- vrfVerify
- secretKey
- ed25519
```

#### Code Patterns to Look For
```
- Pattern 1: point decompression whose result is never checked against the identity element
- Pattern 2: Scalar::from_bytes_mod_order-style wraps on attacker-supplied signature halves
- Pattern 3: Transcript::new(b"") or a constant label shared by multiple protocols
- Pattern 4: verification entry points with no input length ceiling
```

#### Audit Checklist
- [ ] Does verify() reject the identity point as a public key? (compare against schnorrkel tests)
- [ ] Are non-canonical scalar/point encodings rejected, not normalized?
- [ ] Is the transcript label unique per protocol and non-empty?
- [ ] Differential fuzz against reference schnorrkel: zero accept/reject mismatches?

### Keywords for Search

`sr25519`, `schnorrkel`, `signature verification`, `point at infinity`, `identity point`, `ristretto255`, `signature malleability`, `canonical encoding`, `transcript domain separation`, `merlin`, `vrf verify`, `differential fuzzing`, `ed25519 key encoding`, `timing side channel`, `polkadot cryptography`, `micro-sr25519`, `scure-sr25519`

### Related Vulnerabilities

- DB/substrate/bridges/grandpa-light-client-validation.md (consensus verification edge cases)
- DB/substrate/pallets/origin-authorization-bypass.md (what a broken verify unlocks)
