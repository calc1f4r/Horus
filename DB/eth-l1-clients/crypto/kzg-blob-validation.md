---
vulnerability_class: kzg_blob_validation
title: "KZG / Blob Validation: binding panics, point deserialization, param-length and proof checks"
protocol: eth-l1-clients
category: Cryptography / EIP-4844
vulnerability_type: input_validation
attack_type: panic_crash|invalid_proof_acceptance|gas_underflow|trusted_setup_misuse
affected_component: kzg_bindings|blob_tx_validation|precompile_0x0a|trusted_setup
chain: ethereum
severity: medium
impact: remote_crash|consensus_divergence|invalid_blob_acceptance
severity_range: "LOW to MEDIUM (HIGH if proof verification bypassed)"
source: Sigma Prime c-kzg-4844/go-kzg-4844 reviews + Immunefi Attackathon

primitives:
  - panic_on_malformed_hex_or_text_input_in_bindings
  - bls12_381_point_deserialization_not_validated
  - parameter_length_not_validated
  - newdomain_panic_on_certain_input
  - trusted_setup_loading_panics
  - random_oracle_batch_proof_may_be_zero
  - modexp_precompile_gas_overflow_in_eels_reference

affected_components:
  - c-kzg-4844 / go-kzg-4844 bindings (from_hex, UnmarshalText)
  - blob transaction validation (proofs, commitments, versioned hashes)
  - KZG precompile (0x0a)
  - trusted setup loading

tags:
  - kzg
  - blob
  - eip-4844
  - cryptography
  - c-kzg
  - go-kzg
  - panic
  - trusted_setup
  - sigp
  - attackathon

total_reports_analyzed: 5

# Pattern Identity (Required)
root_cause_family: unsafe_input_handling_in_crypto_bindings
pattern_key: kzg_validation_gap | binding_panics_point_deserialization | remote_crash_or_invalid_acceptance

# Interaction Scope
interaction_scope: network_facing_crypto_validation

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - from_hex
  - UnmarshalText
  - blob_to_kzg_commitment
  - verify_blob_kzg_proof
  - verify_blob_kzg_proof_batch
  - compute_cells
  - NewDomain
  - TrustedSetup
  - load_trusted_setup
  - deserialize
  - G1Point / G2Point
  - modexp
---

# KZG / Blob Validation Gaps (c-kzg, go-kzg, blob tx paths)

## Overview

Every EIP-4844 blob transaction carries KZG commitments/proofs validated by c-kzg-4844 bindings in
each EL client, plus a KZG precompile at 0x0a. Sigma Prime reviewed the reference libraries twice
(c-kzg/go-kzg v2.0, KZG Powers of Tau v3.0) and the Attackathon probed client/EELS integration.
Confirmed issues:

- **Incorrect Deserialisation of BLS12-381 Points** — points not subgroup/curve validated on all paths.
- **Panics in `from_hex()` (Rust bindings)** — malformed hex input panics instead of erroring; any
  reachable caller becomes a remote-crash vector.
- **Panics in `UnmarshalText()` (Go bindings)** — same class for go-kzg-4844 consumers (geth family).
- **Potential Panics Loading Trusted Setup** — malformed setup files crash node startup/validation paths.
- **Lack of Validation of Parameter Length** — functions trusting caller-provided lengths (blob/commitment sizes).
- **NewDomain() Will Panic for Certain Input** — domain construction not input-safe.
- **Random Oracle for Batch Proofs may be Zero** — batch-verification challenge edge case.
- **EELS reference gap (#38958)**: EELS cannot handle overflow gas calculation in the modexp
  precompile like geth/Nethermind — reference-vs-client divergence in precompile gas (adjacent class:
  consensus-relevant crypto precompile math).

**Root Cause Statement**: This vulnerability exists because KZG library bindings trust input
formats (hex/text encoding, point bytes, parameter lengths, setup files) without full validation
and panic instead of returning errors — and reference implementations diverge on precompile edge
handling — so malformed peer/RPC input can crash nodes or, in verification bypass cases, let
invalid proofs through.

**Observed Frequency**: 8 distinct findings in two Sigma Prime reviews + 1 Attackathon EELS report
**Consensus Severity**: LOW to MEDIUM (proof-verification bypass would be HIGH/CRITICAL — none found in scope)

---

#### Agent Quick View

- Root cause statement: "This vulnerability exists because of unsafe_input_handling_in_crypto_bindings (kzg from_hex/UnmarshalText/point/length panics)"
- Pattern key: `kzg_validation_gap | binding_panics_point_deserialization | remote_crash_or_invalid_acceptance`
- Interaction scope: `network_facing_crypto_validation`
- Primary affected component(s): `kzg_bindings`, `blob_tx_validation`
- High-signal code keywords: `from_hex`, `UnmarshalText`, `verify_blob_kzg_proof`, `TrustedSetup`, `NewDomain`
- Typical sink / impact: `remote_crash` / `consensus_divergence`
- Validation strength: `high` (two commercial audits with per-finding code citations)

#### Contract / Boundary Map

- Entry surface(s): blob tx gossip/RPC (commitments, versioned hashes, proofs), precompile 0x0a calls, node startup (trusted setup)
- Contract hop(s): `raw bytes -> binding decode (panic?) -> c library verify -> accept/reject`
- Trust boundary crossed: `untrusted peer/RPC caller`
- Shared state or sync assumption: `all clients embed the same audited c-kzg core with equally safe bindings (often false)`

#### Valid Bug Signals

- Signal 1: Binding exposes `from_hex`/`UnmarshalText`/`FromString` that `unwrap()`/`panic!` on odd-length, non-hex, or oversized input
- Signal 2: G1/G2 point parsing without subgroup check (small-subgroup / invalid-curve attacks)
- Signal 3: Length parameters taken from caller and passed to unsafe copies/slices without cap (BLOB_SIZE = 131072, commitment 48, proof 48)
- Signal 4: Batch verify challenge derived from a hash that can produce zero (degenerate challenge breaks soundness argument)
- Signal 5: Domain separation string length unbounded into `NewDomain` (panic on certain lengths)

#### False Positive Guards

- Not this bug when: panicking function is only invoked on trusted/config-sourced input (trusted setup from pinned file, domain from constants) — downgrade to hardening
- Safe if: all binding entrypoints return `Result`/`error` and the c-core API contract (lengths fixed by type) is enforced
- Requires attacker control of: blob tx fields (network/RPC) — trivial post-4844
- `verify_blob_kzg_proof` correctness itself was NOT found bypassed — findings are panic/validation hygiene, not soundness breaks

## Real Reports

### 1. Sigma Prime — c-kzg & go-kzg Security Assessment v2.0 (Ethereum Foundation)

Report: `reports/eth-l1-clients_findings/eth-c-kzg-libs-sigp.md` (16 pages; findings TOC at top)
Findings: Incorrect Deserialisation of BLS12-381 Points; Panics in from_hex() (Rust); Panics in
UnmarshalText() (Go); Potential Panics Loading Trusted Setup; Lack of Validation of Parameter
Length; NewDomain() Panic; Random Oracle for Batch Proofs may be Zero.

### 2. Sigma Prime — KZG Powers Of Tau Ceremony Review v3.0

Report: `reports/eth-l1-clients_findings/eth-kzg-libs-sigp.md` (30 pages) — ceremony-side trust
root for the setup the clients load.

### 3. Immunefi #38958 [BC-Low] — EELS can't handle overflow gas calculation in modexp precompile

Report: `reports/eth-l1-clients_findings/38958-bc-low-eels-cant-handle-overflow-gas-calculation-in-modexp-precompile.md`
Reference/EELS divergence on very large base length vs geth/Nethermind — cross-client
crypto-precompile gas class.

### 4. Related blob-encoding crash: Immunefi #38766 [BC-Insight] — erigon nil-pointer panic in encodePayload() of blob tx encoding

Report: `reports/eth-l1-clients_findings/38766-bc-insight-nil-pointer-dereference-panics-in-encodepayload-of-blob-txs-encoding.md`
(blob-tx encode path panic — see also `DB/eth-l1-clients/execution/rlp-decoding-lenient-parsing.md` Category 5)

### 5. Upstream EF reviews (reference corpus)

- `reports/eth-l1-clients_findings/public-audits-reports-ethereum-foundation-c-kzg-review-pdf.md`
- `reports/eth-l1-clients_findings/public-audits-reports-ethereum-foundation-ef-kzg-review-pdf.md`

## Vulnerable Code Pattern (generic)

```go
// VULNERABLE: panic on malformed input in binding (go-kzg UnmarshalText pattern)
func (c *KZGCommitment) UnmarshalText(text []byte) error {
    b, err := hex.DecodeString(strings.TrimPrefix(string(text), "0x"))
    if err != nil { panic(err) }        // must return err
    copy(c[:], b)                        // no len(b) == 48 check (param length class)
    return nil
}
```

## Detection & Hunt Strategy

1. In each EL client, locate the go-kzg/c-kzg/ckzg_natives binding version; diff against upstream
   for the audited fixes (from_hex/UnmarshalText error handling, length checks).
2. Fuzz every public binding entrypoint reachable from blob tx decode: odd hex, 0x-prefix, empty,
   47/49-byte commitment, 131071/131073-byte blob. Expect errors, not panics.
3. Verify subgroup checks on parsed points (`CheckG1`, `CheckG2` or blst `SubgroupCheck`).
4. Test `NewDomain` / domain strings at boundary lengths; `load_trusted_setup` with truncated files.
5. Cross-run precompile 0x0a + modexp gas tests through EELS vs geth vs Nethermind at extreme sizes.

## References

- `reports/eth-l1-clients_findings/eth-c-kzg-libs-sigp.md`
- `reports/eth-l1-clients_findings/eth-kzg-libs-sigp.md`
- `reports/eth-l1-clients_findings/38958-bc-low-eels-cant-handle-overflow-gas-calculation-in-modexp-precompile.md`
- `reports/eth-l1-clients_findings/38766-bc-insight-nil-pointer-dereference-panics-in-encodepayload-of-blob-txs-encoding.md`
- `reports/eth-l1-clients_findings/public-audits-reports-ethereum-foundation-c-kzg-review-pdf.md`
- `reports/eth-l1-clients_findings/audit-reports-anoma-2023-03-28-audit-report-namada-ethereum-bridge-v1-0-pdf.md`- `reports/eth-l1-clients_findings/audit-reports-nawa-2026-07-16-audit-report-nawa-usdt-stable-vault-ethereum-v1-0-pdf.md`- `reports/eth-l1-clients_findings/chainsafe-gossamer-sigp.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-forest-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-forest-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-gossamer-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-commitboost-sigma-prime-commit-boost-client-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-commitboost-sigma-prime-commitboost-multiplexer-signer-security-assessment-report-v2-1-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-drand-2-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-drand-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-drand-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-drand-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-lotus-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-risc-zero-sigma-prime-risc-zero-the-signal-ethereum-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/publications-audit-reports-peckshield-audit-report-pinksale-subscriptionpool-v1-0-pdf.md`- `reports/eth-l1-clients_findings/publications-reviews-dfinityconsensus-pdf.md`- `reports/eth-l1-clients_findings/publications-reviews-eth2depositcli-pdf.md`
- EIP-4844 (blob tx validation, KZG precompile 0x0a)
- Immunefi/audit `37134` [BC-Insight] (prysm, INFO): Improper secp256k sanitization — `reports/eth-l1-clients_findings/37134-bc-insight-improper-secp256k-sanitization.md` (Immunefi (br0nz3p1ck4x3))
- Immunefi/audit `GR-CR-24-101` [severity: none] (grandine, INFO): RSA library has timing side channel on private keys — `reports/eth-l1-clients_findings/grandine-audit-x41-code-review-grandine-final-report-2024-11-29-pdf.md` (X41)
- Immunefi/audit `GR-CR-24-102` [severity: none] (grandine, INFO): Inconsistent verifier implementations — `reports/eth-l1-clients_findings/grandine-audit-x41-code-review-grandine-final-report-2024-11-29-pdf.md` (X41)
