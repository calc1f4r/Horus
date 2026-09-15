---
# Core Classification (Required)
protocol: movement
chain: movement
category: signature_validation
vulnerability_type: missing_signature_verification|trust_boundary_confusion|replay

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: missing_signature_verification | block_execution_pipeline | unsigned_da_transaction | forged_tx_execution

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: cross_protocol
involved_contracts:
  - movement-full-node execute_settle task (execute_settle.rs execute_block)
  - movement-da light-node passthrough (batch_write / passthrough.rs)
  - movement-aptos-core VM (execute_single_transaction expectation)
path_keys:
  - missing_signature_verification | passthrough_batch_write | light_node->execute_settle->vm_execution
  - missing_signature_verification | whitelist_gap_prevalidation | sequencer_batch_write->da->executor

# Attack Vector Details (Required)
attack_type: logical_error
affected_component: block_execution_pipeline

# Technical Primitives (Required - list all applicable)
primitives:
  - SignatureVerifiedTransaction
  - execute_block
  - bcs::from_bytes
  - verify_signature
  - has_executed_transaction_opt
  - committed_hash
  - prevalidate
  - whitelist_validator
  - SIG_VERIFY_POOL

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - SignatureVerifiedTransaction::Valid
  - execute_block
  - verify_signature
  - bcs::from_bytes
  - prevalidate
  - execute_settle.rs
  - passthrough.rs

# Impact Classification
severity: high
impact: fund_loss
exploitability: 0.8
financial_impact: high

# Context Tags (Optional but recommended)
tags:
  - movement
  - move
  - signature
  - execution_pipeline
  - da_layer
  - aptos_core_integration
  - trust_boundary
  - attackathon

# Version Info (Optional)
language: move        # Move-family L1; vulnerable host code is Rust
version: all
---

## References & Source Reports

> Verified: #43307 body shows the `SignatureVerifiedTransaction::Valid` wrap without verification; #41373 body shows the whitelist-gated prevalidation variant.

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [P1] | reports/movement-l1_findings/43307-bc-high-not-verifying-the-signatures-upon-execution-leads-to-direct-loss-of-funds.md | HIGH | Immunefi (HollaDieWaldfee) | #43307 |
| [P2] | reports/movement-l1_findings/41373-bc-high-premature-transaction-acceptance-to-mempool-da-without-signature-validation.md | HIGH | Immunefi (Cartel) | #41373 |
| [P3] | reports/movement-l1_findings/41794-bc-high-not-having-any-whitelisted-account-completely-disables-the-prevalidator-leading-to-tra.md | HIGH | Immunefi (HollaDieWaldfee) | #41794 |

## Signatures Not Verified at Execution — Forged Transactions Execute as `SignatureVerifiedTransaction::Valid`

### Overview

Movement's block executor wraps every deserialized DA transaction in `SignatureVerifiedTransaction::Valid` without ever checking the signature, importing Aptos Core's execution types but not its signature verification step — so transactions injected directly at the DA layer execute as if properly signed, enabling direct loss of funds.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the execution pipeline assumes signature verification happened upstream (at mempool admission) and blindly marks DA-sourced transactions `Valid`, while the DA ingress path either never verifies (passthrough) or skips verification entirely when no whitelist is configured."
- Pattern key: `missing_signature_verification | block_execution_pipeline | unsigned_da_transaction | forged_tx_execution`
- Interaction scope: `cross_protocol` (DA light node → full-node executor → Aptos VM)
- Primary affected component(s): `execute_settle.rs::execute_block`, `passthrough.rs::batch_write`, prevalidator wiring in `sequencer.rs::try_from_config`
- Contracts / modules involved: movement-full-node execute_settle task, movement-da light-node (passthrough + sequencer modes), movement-aptos-core VM
- Path keys: `missing_signature_verification | passthrough_batch_write | light_node->execute_settle->vm_execution`, `missing_signature_verification | whitelist_gap_prevalidation | sequencer_batch_write->da->executor`
- High-signal code keywords: `SignatureVerifiedTransaction::Valid`, `execute_block`, `verify_signature`, `bcs::from_bytes`, `prevalidate`
- Typical sink / impact: `forged transaction execution / spend from any address / direct fund loss`
- Validation strength: `strong` — code-anchored, PoC steps provided, Aptos Core contrast shown

#### Contract / Boundary Map

- Entry surface(s): `passthrough::batch_write()` gRPC (direct-to-DA submission), sequencer-mode `batch_write` with empty whitelist config
- Contract hop(s): `attacker -> LightNodeService.batch_write -> Celestia blob -> execute_settle stream -> execute_block -> VM`
- Trust boundary crossed: `public DA ingress -> trusted execution pipeline (signature verification dropped at boundary)`
- Shared state or sync assumption: executor trusts that anything reaching `execute_block` already passed upstream signature checks; that check is bypassable/absent on the DA path

#### Valid Bug Signals

- Signal 1: transactions from `block.transactions()` are wrapped `SignatureVerifiedTransaction::Valid(Transaction::UserTransaction(...))` with no `verify_signature()` call in `execute_block`
- Signal 2: a direct-to-light-node ingress path (`passthrough::batch_write`) exists that does not enforce signature validation
- Signal 3: in sequencer mode, `Option<Prevalidator>` is `None` when `whitelisted_accounts` is empty → no signature check at all before DA publication

#### False Positive Guards

- Not this bug when: the deployment always configures a non-empty whitelist AND the passthrough ingress is disabled/firewalled AND execution re-verifies signatures (Aptos-style `SIG_VERIFY_POOL` / `Invalid(_)` discard path)
- Safe if: executor treats DA transactions as `Unverified` and verifies before execution, rejecting `Invalid`
- Requires attacker control of: network access to the DA light-node gRPC endpoint (no keys required)

### Vulnerability Description

#### Root Cause

Aptos Core's contract is: transactions enter execution as `SignatureVerifiedTransaction`, and `execute_single_transaction` discards `Invalid(_)` entries — verification happens in `prepare_block` (`SIG_VERIFY_POOL.install(...)`). Movement reuses the executor but feeds it DA blobs it never verified: `execute_block` does `bcs::from_bytes(transaction.data())`, checks only replay (`has_executed_transaction_opt(committed_hash())`), then wraps in `Valid`. Upstream, the prevalidator (signature + whitelist) is optional and is not even constructed when no whitelist is configured — so "verified upstream" is either bypassable (passthrough) or entirely absent (empty whitelist).

#### Attack Scenario / Path Variants

**Path A: [Passthrough direct injection]**
Path key: `missing_signature_verification | passthrough_batch_write | light_node->execute_settle->vm_execution`
Entry surface: `passthrough::batch_write()` gRPC on the DA light node
Contracts touched: `LightNodeService -> Celestia -> execute_settle -> VM`
Boundary crossed: public gRPC → DA → trusted executor
1. Attacker crafts a `SignedTransaction` spending a victim's funds with an invalid/garbage signature
2. Submits directly via `passthrough::batch_write()` — no signature validation on this path
3. Blob lands in DA; executor streams it, wraps as `Valid`, VM executes
4. Victim's funds move; report classifies as direct loss of funds (HIGH)

**Path B: [Empty-whitelist configuration gap]**
Path key: `missing_signature_verification | whitelist_gap_prevalidation | sequencer_batch_write->da->executor`
Entry surface: sequencer-mode `batch_write` on a node configured without whitelisted accounts
1. Operator sets no whitelist (intending "accept everyone")
2. `try_from_config()` returns no prevalidator → `batch_write` pushes all transactions unvalidated (`None => transactions.push(transaction)`)
3. Invalid-signature transactions are sequenced into blocks and published to DA
4. Executor (Path A sink) executes them; also enables mempool flooding and deserialization-failure liveness bugs (#41794)

#### Vulnerable Pattern Examples

**Example 1: Executor trusts DA blindly** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: execute_settle.rs::execute_block
for transaction in block.transactions() {
    let signed_transaction: SignedTransaction = bcs::from_bytes(transaction.data())?;
    if self.executor.has_executed_transaction_opt(signed_transaction.committed_hash())? {
        continue; // replay check only — NOT a signature check
    }
    // @audit wrapped as Valid without any verify_signature() call
    let signature_verified_transaction = SignatureVerifiedTransaction::Valid(
        Transaction::UserTransaction(signed_transaction),
    );
    block_transactions.push(signature_verified_transaction);
}
```

**Example 2: Optional prevalidator collapses to none** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: prevalidation is gated on whitelist configuration
match &self.prevalidator {
    Some(prevalidator) => { match prevalidator.prevalidate(transaction).await { /* ... */ } }
    None => transactions.push(transaction), // @audit no signature check at all
}
```

**Example 3: The missing contrast (Aptos Core, secure)** [Approx Vulnerability : N/A — reference]
```rust
// ✅ Reference behavior Movement failed to import:
if let SignatureVerifiedTransaction::Invalid(_) = txn {
    let vm_status = VMStatus::error(StatusCode::INVALID_SIGNATURE, None);
    return Ok((vm_status, discarded_output(vm_status.status_code())));
}
// and, before execution: SIG_VERIFY_POOL.install(|| txns.map(|t| t.into()) ...)
```

### Impact Analysis

#### Technical Impact
- Any forged transaction executes as long as it reaches the DA — spend from arbitrary addresses
- Replay check (`has_executed_transaction_opt`) is keyed on content hash, not authenticity, so first-seen forgeries always run
- Combined with #41794: non-deserializable transactions on the same path halt block execution entirely

#### Business Impact
- Direct loss of user funds (reported impact class)
- Total trust failure in the chain's signature guarantee

#### Affected Scenarios
- Any deployment where the DA light node ingress is reachable and the executor runs stock `execute_block`
- Empty-whitelist sequencer configs (both sequencer and passthrough modes affected)

### Secure Implementation

**Fix 1: Verify at the execution boundary**
```rust
// ✅ SECURE: verify DA-sourced transactions before wrapping
let signed = bcs::from_bytes::<SignedTransaction>(transaction.data())?;
signed.verify_signature()?;   // fail → discard as Invalid, do not halt the block
let sv = SignatureVerifiedTransaction::Valid(Transaction::UserTransaction(signed));
```

**Fix 2: Unconditional prevalidation (decouple from whitelist)**
```rust
// ✅ SECURE: always construct signature/deserialization prevalidator; whitelist is an ADDITIONAL filter
let prevalidator = Prevalidator::new(
    AptosTransactionValidator,                      // always on
    whitelist.map(WhitelistValidator::new).unwrap_or(AcceptAll), // optional layer
);
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Executor consumes a trusted wrapper type (SignatureVerifiedTransaction::Valid) built from untrusted input
- Verification component optional (Option<...>) on the ingress path that feeds the executor
- "Verify upstream" assumption spanning a network/persistence boundary (DA blob store)
```

#### High-Signal Grep Seeds
```
- SignatureVerifiedTransaction::Valid
- execute_block
- verify_signature
- bcs::from_bytes
- prevalidate
```

#### Code Patterns to Look For
```
- Pattern 1: `SignatureVerifiedTransaction::Valid(` constructed without a preceding verify call
- Pattern 2: `None => transactions.push(transaction)` in an ingress handler
- Pattern 3: verification logic gated on an unrelated config (whitelist) rather than always-on

```

#### Audit Checklist
- [ ] Trace every ingress that feeds the executor; confirm signature verification on each
- [ ] Check whether wrapper types (`Valid`) are constructed from raw deserialization
- [ ] Verify what happens when whitelist/prevalidation config is empty vs unset
- [ ] Confirm invalid transactions are discarded (not block-halting) after verification is added

### Real-World Examples

#### Known Exploits
- None public at report time (attackathon finding, fixed post-report)

#### Related CVEs/Reports
- #41794 — empty whitelist also removes deserialization prevalidation → unexecutable blocks
- DB/Sui-Move-specific/movement-l1/LIGHTNODE_BATCH_WRITE_UNAUTHENTICATED.md — same ingress, unauthenticated

### Prevention Guidelines

#### Development Best Practices
1. Never carry a "verified" type across a trust boundary; re-verify at the consuming boundary
2. Make cryptographic validation unconditional; configuration may only add restrictions
3. When forking (Aptos Core), audit which pipeline stages were dropped in the integration

#### Testing Requirements
- Unit tests for: executor receives invalid-signature tx → discarded, block continues
- Integration tests for: direct-to-DA submission with forged signature; empty-whitelist config
- Fuzzing targets: signature field mutation across valid/invalid boundary

### Keywords for Search

`movement`, `signature verification`, `SignatureVerifiedTransaction`, `execute_block`, `forged transaction`, `invalid signature`, `passthrough`, `batch_write`, `prevalidator`, `whitelist`, `aptos core fork`, `trust boundary`, `direct loss of funds`, `da layer`, `transaction execution`

### Related Vulnerabilities

- DB/Sui-Move-specific/movement-l1/LIGHTNODE_BATCH_WRITE_UNAUTHENTICATED.md
- DB/Sui-Move-specific/movement-l1/PREVALIDATOR_WHITELIST_GATING_BYPASS.md
- DB/Sui-Move-specific/movement-l1/DA_BLOB_ID_FORGERY_REPLAY.md
