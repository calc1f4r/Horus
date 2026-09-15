---
# Core Classification (Required)
protocol: movement
chain: movement
category: input_validation
vulnerability_type: missing_id_binding|replay_attack|dedup_bypass

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: unverified_blob_id | signed_blob_ingress | forged_id_resubmission | blob_replay_re_execution

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: cross_protocol
involved_contracts:
  - movement-da protocol util (protocol-units/da/movement/protocol/util, blob/ir/blob.rs try_verify)
  - movement-full-node execute_settle (process_block_from_da dedup by blob.id)
  - Celestia (public blob reposting)
path_keys:
  - unverified_blob_id | celestia_resubmit | modified_id_valid_signature | replayed_block_execution

# Attack Vector Details (Required)
attack_type: logical_error
affected_component: da_blob_verification

# Technical Primitives (Required - list all applicable)
primitives:
  - InnerSignedBlobV1
  - try_verify
  - compute_id
  - to_signing_bytes
  - C::verify
  - blob_id dedup
  - process_block_from_da
  - timestamp digest

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - try_verify
  - compute_id
  - InnerSignedBlobV1
  - to_signing_bytes
  - blob_id
  - process_block_from_da

# Impact Classification
severity: critical
impact: replay|fund_loss
exploitability: 0.8
financial_impact: high

# Context Tags (Optional but recommended)
tags:
  - movement
  - move
  - blob verification
  - replay
  - id mismatch
  - celestia
  - da_layer
  - dedup bypass
  - attackathon

# Version Info (Optional)
language: move        # Move-family L1; vulnerable host code is Rust
version: all
---

## References & Source Reports

> Verified: #42153 body shows `try_verify` verifying signature over `compute_id` while never comparing the declared `id` field to it, plus the executor's id-based dedup that makes the forged id replayable.

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [P1] | reports/movement-l1_findings/42153-bc-critical-attackers-can-exploit-bug-in-blob-verification-to-execute-replay-attack-by-re-exec.md | CRITICAL | Immunefi (perseverance) | #42153 |

## Blob ID Not Bound to Computed ID — Replay-by-ID-Forgery Re-Executes Blobs

### Overview

`InnerSignedBlobV1::try_verify()` checks the signature against the *computed* id but never checks the *declared* `id` field equals it, so an attacker can copy a valid blob from Celestia, change only its `id`, and repost it — the signature still verifies, and the full node's id-keyed execution dedup treats it as a new blob, re-executing its transactions (replay).

#### Agent Quick View

- Root cause statement: "This vulnerability exists because blob verification proves 'signer signed this data' but not 'this blob is the one it claims to be' — the declared id is unauthenticated, and downstream dedup trusts it."
- Pattern key: `unverified_blob_id | signed_blob_ingress | forged_id_resubmission | blob_replay_re_execution`
- Interaction scope: `cross_protocol` (Celestia repost → Movement execution dedup)
- Primary affected component(s): `try_verify` (protocol/util blob/ir/blob.rs), `process_block_from_da` dedup (execute_settle.rs)
- Contracts / modules involved: `InnerSignedBlobV1` / `InnerSignedBlobV1Data`, Celestia DA, full-node executor
- Path keys: single forged-id replay path (below)
- High-signal code keywords: `try_verify`, `compute_id`, `InnerSignedBlobV1`, `blob_id`, `process_block_from_da`
- Typical sink / impact: `transaction replay / double execution / state divergence`
- Validation strength: `strong` — exact vulnerable and consuming code both quoted

#### Contract / Boundary Map

- Entry surface(s): public `blob_submit` on Celestia (anyone can repost modified blobs)
- Contract hop(s): `attacker -> Celestia (blob with forged id, valid sig) -> light node try_verify (passes) -> execute_settle process_block_from_da (dedup by blob.id → miss) -> execute_block`
- Trust boundary crossed: `public DA store -> execution dedup keyed on unauthenticated field`
- Shared state or sync assumption: `blob.id` is assumed to be the canonical content-addressed identity; only `compute_id` is actually authenticated

#### Valid Bug Signals

- Signal 1: `try_verify` computes `message = self.data.compute_id()?` and verifies the signature over it, with no `if self.id != message { Err } `
- Signal 2: executor dedup uses the blob's declared `blob_id` from the DA response (`SequencedBlobBlock`/`PassedThroughBlob` → `blob.blob_id`)
- Signal 3: Celestia accepts the reposted blob (new tx on their chain) — nothing links blob identity to signer intent

#### False Positive Guards

- Not this bug when: verification includes `assert_eq!(self.id, computed_id)` or dedup recomputes the id instead of trusting the field
- Safe if: execution dedup keyed on `compute_id(data)` (content hash) rather than transported `id`
- Requires attacker control of: ability to read public blobs and submit new Celestia txs (no Movement identity needed)

### Vulnerability Description

#### Root Cause

The blob format separates `data` (signed via `compute_id` over `blob || timestamp`), `signature`, `signer`, and `id`. Verification reconstructs the id from data and checks the signature against it — a scheme that authenticates content but leaves the transported `id` field advisory. The executor's replay protection (`has_executed`-style dedup by `blob_id`) consumes the advisory field. Changing `id` transforms "already executed" into "new" while keeping the signature valid.

#### Attack Scenario / Path Variants

**Path A: [Replay by id forgery]**
Path key: `unverified_blob_id | celestia_resubmit | modified_id_valid_signature | replayed_block_execution`
1. Read a valid sequenced blob B (id = X) from Celestia
2. Construct B' with identical `data`/`signature`/`signer`, but `id = X' ≠ X`
3. Submit B' to Celestia (attacker pays a small Celestia fee)
4. `try_verify` recomputes `compute_id(data)` = X → signature over X valid → passes
5. `process_block_from_da` sees blob_id X' — not in executed set → re-executes B's transactions
6. Transactions replay (double spends/double effects); classified direct loss of funds (Critical)

#### Vulnerable Pattern Examples

**Example 1: Signature verified, identity not** [Approx Vulnerability : CRITICAL]
```rust
// ❌ VULNERABLE: protocol/util/src/blob/ir/blob.rs
pub fn try_verify(&self) -> Result<(), anyhow::Error> {
    let public_key = C::PublicKey::try_from_bytes(self.signer.as_slice())?;
    let signature = C::Signature::try_from_bytes(self.signature.as_slice())?;
    let message = self.data.compute_id()?;            // @audit id recomputed from data
    if !C::verify(message.as_slice(), &signature, &public_key)? {
        return Err(anyhow::anyhow!("signature verification failed"))?;
    }
    Ok(())                                             // @audit self.id never compared to message
}
```

**Example 2: Id derivation (what should be bound)** [Approx Vulnerability : reference]
```rust
// The authenticated identity is:
fn to_signing_bytes(&self) -> Vec<u8> {
    [self.blob.as_slice(), &self.timestamp.to_be_bytes()].concat()
}
pub fn compute_id(&self) -> Result<Id, anyhow::Error> {
    Ok(Id::new(C::digest(&self.to_signing_bytes())?.to_bytes()))
}
// The transported `id` field is NOT covered by the signature and NOT checked.
```

**Example 3: Dedup keyed on the forged field** [Approx Vulnerability : CRITICAL]
```rust
// ❌ VULNERABLE: execute_settle.rs::process_block_from_da
BlobType::SequencedBlobBlock(blob) => {
    (blob.data, blob.timestamp, blob.blob_id, blob.height)  // @audit blob_id trusted from wire
}
// ... later: executed-if-not-seen logic keyed on blob_id → forged id = "never seen"
```

### Impact Analysis

#### Technical Impact
- Full replay of previously executed blobs (all transaction effects re-applied)
- Double-application of any non-sequence-number-protected effect (e.g., passed-through blobs, messages without per-account sequencing)
- State divergence risk across nodes if some see the original and replay ordering differs

#### Business Impact
- Direct loss of funds impact class (reported Critical)
- Breaks the "execute once" guarantee the DA layer exists to provide

#### Affected Scenarios
- Any blob type whose inner transactions aren't fully protected by Move VM sequence numbers (e.g. passed-through blobs, heartbeat-adjacent logic)
- Multi-blob replay amplification (each repost = new id)

### Secure Implementation

**Fix 1: Bind the id field**
```rust
// ✅ SECURE: reject any blob whose declared id != computed id
pub fn try_verify(&self) -> Result<(), anyhow::Error> {
    let computed = self.data.compute_id()?;
    if self.id != computed {
        return Err(anyhow::anyhow!("blob id does not match computed id"));
    }
    // ... existing signature verification over computed ...
}
```

**Fix 2: Content-addressed dedup (defense in depth)**
```rust
// ✅ SECURE: executor dedups on recomputed hash, never on transported id
let computed_id = blob.data.compute_id()?;
if self.executed_blob_ids.contains(&computed_id) { return Ok(()); }
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- A struct carrying both a content-hash field and the raw content, with verification hashing the content but not comparing the field
- Dedup/replay-protection keyed on a transported identifier rather than a recomputed one
- Public repost surface (permissionless DA) upstream of the dedup
```

#### High-Signal Grep Seeds
```
- try_verify
- compute_id
- blob_id
- process_block_from_da
- has_executed
```

#### Code Patterns to Look For
```
- Pattern 1: verify(signature, hash(data)) with an unchecked parallel id/data-hash field
- Pattern 2: "already executed" sets keyed by values read off the wire
- Pattern 3: signing bytes that omit struct fields used elsewhere as identity

```

#### Audit Checklist
- [ ] For every signed message struct, enumerate fields NOT covered by the signature
- [ ] Trace each uncovered field to its consumers; flag identity/dedup/ordering uses
- [ ] Test: resubmit valid message with mutated uncovered identity field

### Real-World Examples

#### Known Exploits
- None public (attackathon finding)

#### Related CVEs/Reports
- #43307 — replay guard (`has_executed_transaction_opt`) is content-keyed but the same pipeline skips signature checks
- DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md (id/proof binding family)

### Prevention Guidelines

#### Development Best Practices
1. Authenticate every field used as identity: sign over the id or compare id == hash(data)
2. Key replay protection on recomputed content hashes, not transported ids
3. Assume permissionless DA layers will deliver attacker-resubmitted data

#### Testing Requirements
- Unit tests for: id≠computed rejection; dedup hit on recomputed id
- Integration tests for: copy-mutate-resubmit of a sequenced blob
- Fuzzing targets: all unsigned struct fields of blob types

### Keywords for Search

`movement`, `blob verification`, `blob id`, `compute_id`, `try_verify`, `replay attack`, `id mismatch`, `dedup bypass`, `celestia`, `re-execute blob`, `double execution`, `signed blob`, `unsigned field`, `da layer`, `content addressed`

### Related Vulnerabilities

- DB/Sui-Move-specific/movement-l1/EXECUTION_SIGNATURE_BYPASS.md (same pipeline, signatures)
- DB/Sui-Move-specific/movement-l1/UNSIGNED_ENVELOPE_METADATA_FORGERY.md (unsigned envelope fields)
- DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md
