---
# Core Classification (Required)
protocol: movement
chain: movement
category: input_validation
vulnerability_type: unsigned_metadata_field_mismatch|ordering_field_forgery|tx_id_collision

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: unsigned_wrapper_mismatch | da_transaction_envelope | client_controlled_priority_or_seqnum | censorship_and_priority_inflation

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract
involved_contracts:
  - movement-da light-node prevalidator (prevalidate: Transaction -> Prevalidated<Transaction>)
  - DA Transaction envelope (data / application_priority / sequence_number / id fields)
  - mempool ordering logic (application_priority queue)
path_keys:
  - unsigned_wrapper_mismatch | batch_write_grpc | forged_application_priority | unfair_ordering
  - unsigned_wrapper_mismatch | batch_write_grpc | forged_sequence_number | targeted_censorship
  - unsigned_wrapper_mismatch | batch_write_grpc | forged_tx_id | mempool_slot_collision

# Attack Vector Details (Required)
attack_type: data_manipulation
affected_component: da_light_node_prevalidator

# Technical Primitives (Required - list all applicable)
primitives:
  - application_priority
  - sequence_number
  - transaction_id
  - prevalidate
  - bcs::to_bytes
  - BTreeSet
  - pop_transactions
  - mempool_queue

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - application_priority
  - prevalidate
  - Transaction::new
  - bcs::to_bytes
  - sequence_number
  - pop_transactions
  - Prevalidated

# Impact Classification
severity: high
impact: tx_censorship|fee_manipulation|griefing
exploitability: 0.85
financial_impact: medium

# Context Tags (Optional but recommended)
tags:
  - movement
  - move
  - transaction_ordering
  - censorship
  - priority_inflation
  - mempool
  - da_layer
  - unsigned_field
  - attackathon

# Version Info (Optional)
language: move        # Move-family L1; vulnerable host code is Rust
version: all
---

## References & Source Reports

> Verified: #43324/#43323 bodies show the prevalidator round-tripping the wrapper fields without checking them against the signed inner payload; #43017 generalizes to all three fields.

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [P1] | reports/movement-l1_findings/43324-bc-high-insufficient-validation-in-da-light-node-allows-malicious-override-of-application-prio.md | HIGH | Immunefi (Blockian) | #43324 |
| [P2] | reports/movement-l1_findings/43323-bc-high-inadequate-sequence-number-validation-in-da-light-node-enables-transaction-censorship.md | HIGH | Immunefi (Blockian) | #43323 |
| [P3] | reports/movement-l1_findings/43017-bc-high-prevalidation-does-not-validate-application-priority-sequence-number-and-id.md | HIGH | Immunefi (HollaDieWaldfee) | #43017 |

## Unsigned Envelope Fields (`application_priority`, `sequence_number`, `id`) Never Checked Against Signed Payload

### Overview

The DA light node's `Transaction` envelope carries `application_priority`, `sequence_number`, and `id` as *unsigned* sidecar fields outside the signed inner `SignedTransaction`; the prevalidator validates only the signed `data` and then re-attaches the attacker-supplied sidecar values verbatim, letting anyone forge priority, sequence number, or transaction ID for ordering, censorship, and mempool-collision attacks.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because ordering/dedup metadata travels outside the signed payload and the prevalidator reconstructs the transaction with those unverified client-supplied fields instead of deriving them from the signed inner transaction."
- Pattern key: `unsigned_wrapper_mismatch | da_transaction_envelope | client_controlled_priority_or_seqnum | censorship_and_priority_inflation`
- Interaction scope: `multi_contract` (DA ingress → prevalidator → mempool ordering/dedup)
- Primary affected component(s): `prevalidator::prevalidate`, DA `Transaction` envelope, mempool priority queue
- Contracts / modules involved: `Validator` (prevalidator), `AptosTransactionValidator`, `whitelist_validator`, mempool `pop_transactions`
- Path keys: forged priority / forged sequence number / forged tx id (below)
- High-signal code keywords: `application_priority`, `prevalidate`, `Transaction::new`, `bcs::to_bytes`, `pop_transactions`
- Typical sink / impact: `priority inflation / targeted censorship / fee-model bypass / mempool slot collision`
- Validation strength: `strong` — exact vulnerable code quoted in reports; PoCs given per field

#### Contract / Boundary Map

- Entry surface(s): `LightNodeService/BatchWrite` gRPC carrying `Transaction { data, application_priority, sequence_number, id }`
- Contract hop(s): `attacker -> batch_write -> prevalidate (only data verified) -> mempool (orders by application_priority, dedups by id, gates by sequence_number) -> block`
- Trust boundary crossed: `client-supplied envelope metadata -> consensus-relevant ordering state`
- Shared state or sync assumption: envelope sidecar fields are assumed to mirror the signed inner transaction; nothing enforces it

#### Valid Bug Signals

- Signal 1: prevalidator reads `transaction.application_priority()` / `.sequence_number()` before inner validation and re-attaches them in `Transaction::new(...)` after — no equality check against `aptos_transaction`
- Signal 2: `application_priority` is not covered by the signature (not part of signed payload)
- Signal 3: mempool ordering and dedup consume the envelope fields (priority queue, id-keyed slots), producing ordering/censorship impact

#### False Positive Guards

- Not this bug when: priority/seqnum/id are derived server-side from the deserialized signed transaction (or moved inside the signed payload), or the ingress is authenticated and trusted
- Safe if: `prevalidate` asserts `outer.sequence_number == inner.raw_txn.sequence_number` and computes priority from gas price
- Requires attacker control of: a gRPC request to the light node write endpoint (any observer can copy a victim tx's `data`)

### Vulnerability Description

#### Root Cause

The DA `Transaction` type is a wrapper: signed bytes (`data`) plus three plaintext fields. The prevalidator flow deserializes and signature-verifies only `data`, then rebuilds the envelope with `Transaction::new(bcs::to_bytes(&aptos_transaction)?, application_priority, sequence_number)` — propagating whatever the caller sent. Since ordering (`application_priority`, lower = earlier), account sequencing (outer `sequence_number`), and dedup (`id`) all read the envelope, a malicious submitter controls consensus-adjacent metadata of *other users'* transactions.

#### Attack Scenario / Path Variants

**Path A: [Priority inflation / demotion]**
Path key: `unsigned_wrapper_mismatch | batch_write_grpc | forged_application_priority | unfair_ordering`
1. Copy victim tx `data`/`sequence_number`/`id`, set `application_priority: 9999` (or 0 for self)
2. Submit via `write_batch` gRPC
3. Victim tx demoted → starvation/targeted delay; attacker txs jump the queue for free
4. Fee-based ordering broken: low-gas txs execute before high-gas txs

**Path B: [Sequence-number censorship]**
Path key: `unsigned_wrapper_mismatch | batch_write_grpc | forged_sequence_number | targeted_censorship`
1. Clone a victim's valid signed tx; set outer `sequence_number = victim + 1000`
2. Signature still valid (inner untouched), so it passes prevalidation
3. Executor skips/rejects on mismatch → victim's real tx silently fails or is delayed; account liveness lost

**Path C: [Transaction-ID collision]**
Path key: `unsigned_wrapper_mismatch | batch_write_grpc | forged_tx_id | mempool_slot_collision`
1. Submit a fake tx whose `id` equals the victim's legitimate tx id
2. Mempool dedups/slots by id — the legitimate transaction gets skipped
3. Cheap targeted DoS of arbitrary pending transactions (#43017)

#### Vulnerable Pattern Examples

**Example 1: Sidecar fields round-tripped unvalidated** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: prevalidator/src — only `data` is verified
async fn prevalidate(&self, transaction: Transaction)
    -> Result<Prevalidated<Transaction>, Error> {
    let application_priority = transaction.application_priority(); // @audit unsigned
    let sequence_number = transaction.sequence_number();           // @audit unsigned
    let aptos_transaction = AptosTransactionValidator.prevalidate(transaction).await?;
    let aptos_transaction = self.whitelist_validator
        .prevalidate(aptos_transaction.into_inner()).await?.into_inner();
    Ok(Prevalidated(Transaction::new(
        bcs::to_bytes(&aptos_transaction)?,  // signed payload re-serialized
        application_priority,                // @audit attacker value re-attached verbatim
        sequence_number,                     // @audit attacker value re-attached verbatim
    )))
}
```

**Example 2: Priority forgery PoC** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: attacker-side (from report #43324 PoC)
let manipulated_tx = Transaction {
    data: original_tx.data.clone(),        // valid signature preserved
    application_priority: 9999,            // arbitrary priority
    sequence_number: original_tx.sequence_number,
    id: original_tx.id,
};
// sent to LightNode write_batch endpoint
```

**Example 3: Sequence-number censorship PoC** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: attacker-side (from report #43323 PoC)
let censored_tx = Transaction {
    data: original_tx.data.clone(),               // same signed inner payload
    application_priority: original_tx.application_priority,
    sequence_number: original_tx.sequence_number + 1000, // breaks execution
    id: original_tx.id,
};
```

### Impact Analysis

#### Technical Impact
- Deterministic ordering broken: priority is a client-controlled string on a signed tx
- Targeted censorship and account-liveness loss via outer-seqnum mismatch
- Mempool slot exhaustion / collision via forged ids
- Fee-market bypass: high priority without paying the corresponding gas price

#### Business Impact
- Tx-fee modification outside design parameters + censorship (reported impact classes)
- MEV/ordering fairness guarantees collapse; predictable sandwiching of victims

#### Affected Scenarios
- Any light node accepting external `batch_write` calls
- Compounds with blob-ordering bugs (#42298): two independent orderings can be broken

### Secure Implementation

**Fix 1: Derive all metadata from the signed transaction**
```rust
// ✅ SECURE: compute envelope fields server-side, ignore client values
let inner: SignedTransaction = bcs::from_bytes(&transaction.data())?;
inner.verify_signature()?;
let priority = derive_priority(&inner);            // from gas_price, not client
let seq = inner.sequence_number();                 // from signed payload
Ok(Prevalidated(Transaction::new(bcs::to_bytes(&inner)?, priority, seq)))
```

**Fix 2: If envelope fields must stay, verify equality**
```rust
// ✅ SECURE: reject mismatches between outer envelope and inner signed values
if transaction.sequence_number() != inner.sequence_number() {
    return Err(Error::Validation("outer seqnum != signed seqnum"));
}
// and move application_priority into the signed payload or sign over it
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Envelope/wrapper struct where consensus-relevant fields sit outside the signed bytes
- Validator that validates inner payload but reconstructs the wrapper with pre-validation captures
- Ordering or dedup logic reading fields that no validator checked
```

#### High-Signal Grep Seeds
```
- application_priority
- prevalidate
- Transaction::new
- bcs::to_bytes
- pop_transactions
```

#### Code Patterns to Look For
```
- Pattern 1: `let x = transaction.field(); ... Transaction::new(..., x)` round-trip in a validator
- Pattern 2: priority/seqnum/id not present in the signing bytes of the payload
- Pattern 3: mempool keyed or ordered by envelope fields arriving from an RPC

```

#### Audit Checklist
- [ ] List every field of the wire envelope; mark which are signature-covered
- [ ] For each uncovered field, trace where it is consumed (ordering, dedup, accounting)
- [ ] Verify server-side derivation or equality checks for each uncovered field
- [ ] Test cloned valid tx with mutated metadata through the full pipeline

### Real-World Examples

#### Known Exploits
- None public (attackathon findings)

#### Related CVEs/Reports
- #42648 — altering `application_priority` variant (same root cause, different report)
- #42298 / #42749 — independent DA-side ordering breaks

### Prevention Guidelines

#### Development Best Practices
1. Anything that influences ordering, dedup, or fees must be signed or server-derived
2. Validators should never echo client input into validated output
3. Reject on any inner/outer mismatch rather than defaulting to outer values

#### Testing Requirements
- Unit tests for: outer≠inner seqnum rejection; priority derived from gas price
- Integration tests for: clone-and-mutate attacks on each envelope field
- Fuzzing targets: envelope field mutation against prevalidator invariants

### Keywords for Search

`movement`, `application_priority`, `unsigned field`, `envelope mismatch`, `sequence number`, `transaction id`, `censorship`, `priority inflation`, `prevalidate`, `mempool ordering`, `transaction wrapper`, `da light node`, `fee bypass`, `forged priority`, `write_batch`

### Related Vulnerabilities

- DB/Sui-Move-specific/movement-l1/CELESTIA_BLOB_ORDER_MANIPULATION.md (independent ordering break)
- DB/Sui-Move-specific/movement-l1/MEMPOOL_SEQUENCE_NUMBER_VALIDATION.md
- DB/Sui-Move-specific/SUI_MOVE_ACCESS_CONTROL_VALIDATION_VULNERABILITIES.md (input-validation family)
