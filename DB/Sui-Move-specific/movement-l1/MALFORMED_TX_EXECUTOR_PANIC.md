---
# Core Classification
protocol: movement
chain: movement
category: input_validation
vulnerability_type: malformed_tx_injection|executor_panic|unrecoverable_block_failure

# Pattern Identity
root_cause_family: unvalidated_deserialization
pattern_key: malformed_aptos_payload | batch_write_to_da | block_read_back | full_node_panic_halt

# Interaction Scope
interaction_scope: cross_protocol
involved_contracts:
  - protocol-units/da/movement/protocol/light-node (sequencer.rs batch_write, unauthenticated)
  - protocol-units/da/movement/protocol/light-node (light_node.rs run_server, 0.0.0.0 bind)
  - movement_full_node::node::tasks::execute_settle (block execution, panic site)
  - movement-aptos-core executor (Aptos tx deserialization)
path_keys:
  - malformed_aptos_payload | batch_write_grpc | light-node -> celestia -> execute_settle panic
  - malformed_aptos_payload | keyless_signature_field | aptos-core keyless_validation -> node panic

# Attack Vector Details
attack_type: data_manipulation
affected_component: block_execution_deserialization

# Technical Primitives
primitives:
  - serde_json::from_slice
  - bcs::from_bytes
  - batch_write
  - execute_block
  - panic_in_tokio_worker
  - KeylessSignature
  - exp_date_secs

# Grep / Hunt-Card Seeds
code_keywords:
  - execute_settle
  - Failed to execute block
  - Cannot drop a runtime in a context where blocking is not allowed
  - batch_write
  - KeylessSignature
  - verify_expiry
  - exp_date_secs
  - seconds_from_epoch

# Impact Classification
severity: critical
impact: dos
financial_impact: none

# Context Tags
tags:
  - l1_node_implementation
  - panic_crash
  - celestia_da
  - rust_host
  - immunefi_attackathon

language: move        # Move-family L1; vulnerable host code is Rust (movement protocol-units + aptos-core fork)
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [R1] | reports/movement-l1_findings/43243-bc-critical-attacker-can-halt-chains-operating-in-sequencer-mode.md | CRITICAL | immunefi | #43243 |
| [R2] | reports/movement-l1_findings/42941-bc-critical-critical-network-wide-denial-of-service-through-unrecoverable-block-execution-fail.md | CRITICAL | immunefi | #42941 |
| [R3] | reports/movement-l1_findings/42934-bc-high-improper-input-validation-in-keylesssignature-causes-full-node-panic.md | HIGH | immunefi | #42941/#42934 |
| [R4] | reports/movement-l1_findings/43322-bc-high-inadequate-transaction-validation-in-da-light-node-allows-unprocessable-block-creation.md | HIGH | immunefi | #43322 |

## Malformed Transaction in DA Becomes Unrecoverable Block: Node Panics on Every Read-Back

### Overview

An unauthenticated `batch_write` lets anyone persist a Movement transaction whose inner `data` field is not a valid Aptos transaction (e.g. `"data":[0]`) to Celestia; it gets sequenced, DA-signed, and persisted — and when honest full nodes read the block back and try to execute it, deserialization fails *inside the block-execution loop* and the node panics (`Cannot drop a runtime in a context where blocking is not allowed`). Because the malformed blob is permanent chain data, every restart hits the same block: **unrecoverable, network-wide crash loop**.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because DA contents are trusted during block execution — a malformed Aptos payload written via unauthenticated `batch_write` (with prevalidation fail-open in default config) becomes a canonical block, and `execute_settle` panics on the deserialization error instead of rejecting/skipping, so every node crashes on the same height forever."
- Pattern key: `malformed_aptos_payload | batch_write_to_da | block_read_back | full_node_panic_halt`
- Interaction scope: `cross_protocol` (Movement node ↔ Celestia DA)
- Primary affected component(s): `execute_settle block-execution task`, `batch_write ingress`, `keyless_validation.rs`
- Contracts / modules involved: `light-node/src/sequencer.rs`, `light_node.rs`, `movement_full_node::node::tasks::execute_settle`, `aptos-move/aptos-vm/src/keyless_validation.rs`, `aptos types/src/keyless/mod.rs`
- Path keys: `malformed_aptos_payload | batch_write_grpc | light-node -> celestia -> execute_settle panic`, `malformed_aptos_payload | keyless_signature_field | aptos-core keyless_validation -> node panic`
- High-signal code keywords: `execute_settle`, `Failed to execute block`, `Cannot drop a runtime`, `batch_write`, `KeylessSignature`, `exp_date_secs`
- Typical sink / impact: `node crash loop at fixed height / total network shutdown / no state-advance`
- Validation strength: `strong` ([R1] includes full PoC: grpcurl call + observed panic log; [R2]/[R3] independently confirm unrecoverable execution-failure halts)

#### Contract / Boundary Map

- Entry surface(s): `LightNodeService::batch_write()` gRPC (0.0.0.0), keyless-signed tx submission
- Contract hop(s): `batch_write -> memseq.publish_many -> Celestia -> (DA-signed block) -> full-node stream_read -> execute_settle -> bcs deser failure -> panic`
- Trust boundary crossed: `external gRPC input → canonical chain data (DA-signed) → execution engine`
- Shared state or sync assumption: `all nodes assume DA-returned blocks contain well-formed transactions; one poison blob violates this for every participant simultaneously`

#### Valid Bug Signals

- Signal 1: attacker-controllable bytes reach persistent DA storage without full structural validation (prevalidation absent/fail-open/malformed-passing)
- Signal 2: deserialization/decoding of block contents occurs in a code path where the error path panics (or unwraps) rather than returning an error the node can skip/quarantine
- Signal 3: after the crash, the same height is re-fetched on restart → deterministic crash loop; no manual intervention path defined

#### False Positive Guards

- Not this bug when: execution failures on malformed data are contained (error propagated, block skipped, or node marks data invalid and continues) — verify the panic, not merely the bad data
- Safe if: ingress enforces full Aptos structural validation before DA write AND a malicious-sequencer defense exists (skip-invalid-tx execution policy)
- Requires attacker control of: network access to the gRPC port (default 0.0.0.0) — or, for [R3] variant, a funded account to submit one crafted keyless tx
- Distinct from `CELESTIA_ZSTD_BOMB_OOM.md` (existing): zstd bomb is *decompression-resource* exhaustion of DA payloads; THIS is *semantic* malformation crashing the executor. Different sink (memory vs panic-on-deser).
- Distinct from `DA_BLOB_ID_FORGERY_REPLAY.md` (existing): replay/forgery of blob identity vs malformed payload content.

### Vulnerability Description

#### Root Cause

Two independent failures compose into an unrecoverable halt: (1) **ingress**: `batch_write` accepts arbitrary blobs (no access control) and in default config the prevalidator is disabled or fail-open (see `PREVALIDATOR_WHITELIST_DISABLE_BYPASS.md`), so structurally invalid Aptos payloads are serialized into DA and signed by the DA signer — becoming canonical; (2) **executor**: `execute_settle`'s block execution path hits the deserialization failure and, combined with a runtime-drop invariant violation (`Cannot drop a runtime in a context where blocking is not allowed`), the tokio worker panics and the process dies. Persistence of the poison block makes the crash deterministic across restarts and across all nodes ([R1], [R2]).

#### Attack Scenario / Path Variants

**Path A: poison block via batch_write → network-wide crash loop**
Path key: `malformed_aptos_payload | batch_write_grpc | light-node -> celestia -> execute_settle panic`
Entry surface: `BatchWrite` gRPC on 0.0.0.0:30730
Contracts touched: `light-node -> memseq -> Celestia -> execute_settle`
Boundary crossed: external input → DA-signed canonical block → execution
1. Attacker base64-encodes `{"data":[0],"application_priority":0,"sequence_number":0,"id":[...]}` (invalid Aptos tx)
2. `grpcurl ... LightNodeService/BatchWrite` — no auth; default config prevalidation off/fail-open
3. Blob is sequenced, published to Celestia, DA-signed → canonical block at height H
4. Every full node reading height H panics: `Failed to execute block: unexpected end of input. Retrying` → tokio panic → process exit; restart re-reads H → permanent crash loop ([R1] PoC log)

**Path B: malformed KeylessSignature field → all full nodes panic ([R3])**
Path key: `malformed_aptos_payload | keyless_signature_field | aptos-core keyless_validation -> node panic`
Entry surface: ordinary tx submission using Movement SDK (funded account, gas only)
Contracts touched: `aptos-vm keyless_validation.rs -> types/src/keyless/mod.rs`
1. Attacker crafts tx with `KeylessSignature` whose `exp_date_secs` is attacker-controlled
2. `seconds_from_epoch(self.exp_date_secs)` overflows during `verify_expiry` (`keyless_validation.rs#L165`, `mod.rs#L151`, `mod.rs#L369`)
3. Panic during signature validation on every full node
4. Network-wide halt — no privileges required, cost ≈ one tx fee ([R3])

#### Vulnerable Pattern Examples

**Example 1: poison blob submission ([R1] PoC verbatim)** [Approx Vulnerability : CRITICAL]
```bash
# ❌ VULNERABLE: one unauthenticated call plants a permanent crash block
grpcurl -v -plaintext \
  -d '{"blobs":[{"data":"eyJkYX...XX0K"}]}' \
  localhost:30730 movementlabs.protocol_units.da.light_node.v1beta2.LightNodeService/BatchWrite
# data decodes to: {"data":[0],"application_priority":0,"sequence_number":0,"id":[157,21,...]}
#   "data":[0] is NOT a valid Aptos transaction
# Result: block at height H is poison; every node panics on read-back:
#   INFO execute_block{block_id=9c42...}: Failed to execute block: unexpected end of input. Retrying
#   thread 'tokio-runtime-worker' panicked at tokio-1.41.1/src/runtime/blocking/shutdown.rs:51:21:
#   Cannot drop a runtime in a context where blocking is not allowed.
```

**Example 2: crash loop on canonical block read-back ([R1] observed log)** [Approx Vulnerability : CRITICAL]
```text
# ❌ VULNERABLE: deterministic restart crash — the malformed tx is chain data now
2025-04-02T01:18:23.338583Z INFO execute_block{block_id=9c4286604b26de55...}:
    movement_full_node::node::tasks::execute_settle: Failed to execute block:
    unexpected end of input. Retrying
thread 'tokio-runtime-worker' panicked at .../tokio-1.41.1/src/runtime/blocking/shutdown.rs:51:21:
Cannot drop a runtime in a context where blocking is not allowed.
Error: task 61 panicked with message "Cannot drop a runtime in a context where blocking is not allowed."
# restart → same height → same panic → halt forever
```

**Example 3: KeylessSignature overflow panic ([R3] cited lines)** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: attacker-controlled field, unchecked arithmetic, panic on all nodes
// aptos-move/aptos-vm/src/keyless_validation.rs#L165
sig.verify_expiry(&onchain_timestamp_obj).map_err(|_| { ... });
// types/src/keyless/mod.rs#L151
let expiry_time = seconds_from_epoch(self.exp_date_secs);  // exp_date_secs fully attacker-controlled
// types/src/keyless/mod.rs#L369 → integer overflow during the calculation → panic
```

### Impact Analysis

#### Technical Impact
- Deterministic process crash at a fixed block height for every full node; no recovery without intervention
- Attacker写入 canonical chain data signed by the DA signer — persistent, replicated poison
- [R2] generalizes: any unrecoverable block execution failure → network-wide DoS

#### Business Impact
- Total network shutdown (consensus/execution halt) from a single unauthenticated call ([R1]) or one funded tx ([R3])
- Immunefi Critical impact: "Network not being able to confirm new transactions (total network shutdown)"

#### Affected Scenarios
- Chains in sequencer mode with default/suggested configs (0.0.0.0, no whitelist prevalidation)
- Any deployment where DA read-back feeds directly into execution without containment

### Secure Implementation

**Fix 1: validate-before-DA + contained execution failures ([R1]/[R2] recommendations, combined)**
```rust
// ✅ SECURE: two independent fixes required
// (a) Ingress: full structural validation before any DA write; fail closed
async fn batch_write(&self, request: tonic::Request<grpc::BatchWriteRequest>)
    -> Result<tonic::Response<grpc::BatchWriteResponse>, tonic::Status> {
    let blobs = request.into_inner().blobs;
    let mut transactions = Vec::new();
    for blob in blobs {
        let tx: Transaction = serde_json::from_slice(&blob.data)
            .map_err(|e| tonic::Status::invalid_argument(e.to_string()))?;  // reject, don't forward
        let aptos: AptosTransaction = bcs::from_bytes(&tx.data()).map_err(|e| {
            tonic::Status::invalid_argument(format!("Malformed AptosTransaction: {e}")) // ← the [0] case
        })?;
        aptos.verify_signature().map_err(|e| {
            tonic::Status::invalid_argument(format!("Bad signature: {e}"))
        })?;
        transactions.push(tx);
    }
    self.memseq.publish_many(transactions).await
        .map_err(|e| tonic::Status::internal(e.to_string()))?;
    Ok(tonic::Response::new(grpc::BatchWriteResponse { blobs: vec![] }))
}
// (b) Executor: never panic on block contents — contain, mark, skip
match execute_block(&block) {
    Err(BlockError::MalformedTransaction(idx)) => {
        error!("block {} contains malformed tx at {}; quarantining", block.id(), idx);
        self.quarantine_block(block.id());   // record & skip — do NOT unwrap/panic/retry-loop
        continue;
    }
    Err(e) => return Err(e),
}
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- External bytes → persistent storage → execution-engine deserialization without full validation at write time
- Error paths in block execution that panic/unwrap/retry-loop instead of quarantining
- "Retrying" + panic pairs in execution task logs (crash-loop signature)
- Attacker-controlled integer fields (exp_date_secs) reaching unchecked arithmetic in validation code
```

#### High-Signal Grep Seeds
```
- execute_settle
- Failed to execute block
- Cannot drop a runtime
- KeylessSignature
- exp_date_secs
```

#### Code Patterns to Look For
```
- Pattern 1: serde_json::from_slice(&blob.data)? forwarding raw user data to publish_many
- Pattern 2: bcs::from_bytes inside execution loop with ?/unwrap on block contents
- Pattern 3: seconds_from_epoch(attacker_field) with no bounds check
```

#### Audit Checklist
- [ ] Submit structurally invalid Aptos payloads through every ingress; assert rejection before DA write
- [ ] Force a malformed block; assert nodes quarantine/skip rather than panic
- [ ] Fuzz KeylessSignature (and every signature variant) field bounds against validation arithmetic

### Real-World Examples

#### Known Exploits
- None public on Movement; the poison-block crash-loop class parallels Bitcoin's 2010 value-overflow (contained via fork) and various L1 deserialization halts

#### Related CVEs/Reports
- Immunefi Movement Labs Attackathon: #43243, #42941, #42934, #43322 (sources)
- Adjacent: #43315 (DA light node DoS via lack of batch validation — same trust-DA-blindly theme)

### Prevention Guidelines

#### Development Best Practices
1. Validate fully at the trust boundary (before persistence), not at read-back
2. Block execution must treat contents as hostile: errors → quarantine/skip policies, never panics
3. Bound-check every attacker-controlled integer before arithmetic in consensus-critical validation

#### Testing Requirements
- Unit tests for: `"data":[0]` blob rejected at ingress; malformed block quarantined without crash
- Integration tests for: poison-block injection → network keeps executing subsequent heights
- Fuzzing targets: BCS/JSON deserialization of every tx/signature variant in the execution path

### References

#### Technical Documentation
- BCS (Binary Canonical Serialization): https://github.com/aptos-labs/bcs
- Tokio runtime-drop constraint (the panic site): tokio docs, `runtime/blocking/shutdown.rs`

#### Security Research
- Immunefi Movement Labs Attackathon (Mar–Apr 2025): #43243, #42941, #42934, #43322

### Keywords for Search

`malformed transaction`, `poison block`, `crash loop`, `node panic`, `batch_write`, `deserialization failure`, `unexpected end of input`, `Cannot drop a runtime`, `execute_settle`, `unrecoverable block`, `network halt`, `KeylessSignature`, `exp_date_secs`, `integer overflow validation`, `DA read-back trust`, `quarantine block`, `unauthenticated DA write`, `Celestia poison blob`, `sequencer mode halt`, `movement executor`, `block execution failure`

### Related Vulnerabilities

- `PREVALIDATOR_WHITELIST_DISABLE_BYPASS.md` (why ingress validation is absent in default config)
- `LIGHTNODE_BATCH_WRITE_UNAUTHENTICATED.md` (existing — the auth hole on the entry RPC)
- `CELESTIA_ZSTD_BOMB_OOM.md` (existing — resource rather than semantic malformation)
- `SEQUENCER_TCP_TIMEOUT_CRASH.md` (this directory — sibling crash vector on the same service)
