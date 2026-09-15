---
# Core Classification (Required)
protocol: movement          # Movement Labs L1 (Move/Aptos fork), Immunefi Attackathon
chain: movement
category: access_control
vulnerability_type: missing_access_control|unauthenticated_rpc|operator_fund_drain

# Pattern Identity (Required)
root_cause_family: missing_access_control
pattern_key: missing_access_control | da_light_node_batch_write_rpc | unauthenticated_grpc_call | operator_tia_drain

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: cross_protocol
involved_contracts:
  - LightNodeService (movement-da light-node gRPC server, sequencer.rs)
  - MemSeq sequencer (protocol-units/sequencing/memseq/sequencer)
  - Celestia DA (blob_submit via lumina celestia-rpc client)
path_keys:
  - missing_access_control | batch_write_rpc | LightNodeService->memseq->celestia_blob_submit
  - missing_access_control | stream_write_blob | LightNodeService->celestia_blob_submit

# Attack Vector Details (Required)
attack_type: resource_abuse
affected_component: da_light_node_rpc

# Technical Primitives (Required - list all applicable)
primitives:
  - batch_write
  - StreamWriteBlob
  - LightNodeService
  - grpcurl
  - 0.0.0.0_bind
  - blob_submit
  - celestia_namespace
  - TxConfig
  - prevalidator

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - batch_write
  - LightNodeService
  - BatchWriteRequest
  - blob_submit
  - StreamWriteBlob
  - 0.0.0.0
  - publish_many
  - celestia_namespace

# Impact Classification
severity: critical
impact: fund_loss
exploitability: 0.9
financial_impact: high

# Context Tags (Optional but recommended)
tags:
  - movement
  - move
  - da_layer
  - celestia
  - grpc
  - access_control
  - operator_fund_drain
  - attackathon

# Version Info (Optional)
language: move        # Move-family L1; vulnerable host code is Rust (movement protocol-units)
version: all
---

## References & Source Reports

> Verified against report bodies (severity/read from source files, not just filenames).

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [P1] | reports/movement-l1_findings/43253-bc-critical-attackers-can-drain-tia-from-nodes-in-networks-running-in-sequencer-mode.md | CRITICAL | Immunefi (usmannk) | #43253 |
| [P2] | reports/movement-l1_findings/43330-bc-critical-freezing-new-transaction-processing-by-sending-invalid-requests-to-movement-da-lig.md | CRITICAL | Immunefi (hulkvision) | #43330 |

## Unauthenticated `batch_write` / `StreamWriteBlob` gRPC Drains Node Operator Funds

### Overview

The Movement DA light node's write RPCs (`BatchWrite`, `StreamWriteBlob`) have no authentication, and the service binds to `0.0.0.0` in both default and suggested configs, so any internet host can force the node to submit arbitrary blobs to Celestia — with the node operator paying the TIA gas for every submission.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because a cost-incurring write RPC (`batch_write`) is exposed on all interfaces with no authentication, rate limit, or origin check, and each accepted blob is unconditionally published to Celestia at the operator's expense."
- Pattern key: `missing_access_control | da_light_node_batch_write_rpc | unauthenticated_grpc_call | operator_tia_drain`
- Interaction scope: `cross_protocol` (Movement light node → Celestia DA)
- Primary affected component(s): `LightNodeService.batch_write` (sequencer.rs), `submit_celestia_blob`
- Contracts / modules involved: `LightNodeService`, `memseq.publish_many`, `CelestiaDaBlob`/`blob_submit`
- Path keys: `missing_access_control | batch_write_rpc | LightNodeService->memseq->celestia_blob_submit`, `missing_access_control | stream_write_blob | LightNodeService->celestia_blob_submit`
- High-signal code keywords: `batch_write`, `LightNodeService`, `BatchWriteRequest`, `blob_submit`, `StreamWriteBlob`, `0.0.0.0`, `publish_many`
- Typical sink / impact: `operator TIA drain / arbitrary data publication / node griefing`
- Validation strength: `strong` — verified code paths in report body; mainnet exposure demonstrated

#### Contract / Boundary Map

- Entry surface(s): gRPC `movementlabs.protocol_units.da.light_node.v1beta2.LightNodeService/BatchWrite` (and `StreamWriteBlob`)
- Contract hop(s): `LightNodeService.batch_write -> prevalidator (optional) -> memseq.publish_many -> CelestiaDa blob_submit (Celestia network)`
- Trust boundary crossed: `public internet -> node gRPC endpoint -> external DA chain (Celestia)`
- Shared state or sync assumption: every accepted blob is assumed to originate from the trusted full node mempool; in reality anyone can call

#### Valid Bug Signals

- Signal 1: write RPC (`batch_write` / `StreamWriteBlob`) reachable from non-localhost (bound `0.0.0.0`, verified in default + docs-suggested config)
- Signal 2: no auth token, TLS client cert, allowlist, or rate limit on the RPC handler
- Signal 3: handler ends in `memseq.publish_many` / `blob_submit` which spends operator TIA — attacker cost is zero, operator cost is per-call

#### False Positive Guards

- Not this bug when: the endpoint is bound to `127.0.0.1`/unix socket behind an authenticating proxy, or write RPCs are disabled in the deployed profile
- Safe if: per-caller quotas + authentication + spending caps are enforced before any Celestia submission
- Requires attacker control of: only network reachability to the gRPC port (no keys, no stake, no whitelisting)

### Vulnerability Description

#### Root Cause

`batch_write` treats the gRPC request as trusted input: it deserializes each blob into a `Transaction`, optionally prevalidates, then unconditionally publishes via `memseq.publish_many` → Celestia `blob_submit`. There is no authentication layer and the tonic service is bound to `0.0.0.0` (default and suggested config), so the "trusted internal API" assumption is false on any publicly routed host. Even with all prevalidators enabled, an attacker can replay previously-signed valid blobs to pass validation and still force paid submissions.

#### Attack Scenario / Path Variants

**Path A: [Arbitrary data → operator pays]**
Path key: `missing_access_control | batch_write_rpc | LightNodeService->memseq->celestia_blob_submit`
Entry surface: `LightNodeService/BatchWrite` from any host
Contracts touched: `LightNodeService -> memseq -> Celestia`
Boundary crossed: public internet → node gRPC → external DA
1. Attacker runs `grpcurl -plaintext -d '{"blobs":[{"data":"..."}]}' host:30730 .../LightNodeService/BatchWrite` with megabytes of arbitrary data
2. `batch_write` deserializes and pushes transactions; when no prevalidator is configured they are accepted as-is
3. `publish_many` submits to Celestia; the node's Celestia account pays gas
4. Repeat → operator TIA balance drains; node eventually can no longer publish (liveness loss)

**Path B: [Valid-blob replay through prevalidators]**
Path key: `missing_access_control | batch_write_rpc | replay_signed_blob`
Entry surface: same RPC, but prevalidators enabled
1. Attacker copies old, validly-signed blobs already on Celestia
2. Resubmits them via `batch_write`; signature checks pass
3. Node re-publishes, paying again per submission — drain persists despite validation

**Path C: [Freeze via flood]**
Path key: `missing_access_control | batch_write_rpc | invalid_request_flood`
Contracts touched: `LightNodeService -> executor state`
1. Send invalid requests for minutes (report #43330 PoC)
2. Node reaches a state where new accounts/transactions cannot be processed even after the flood stops

#### Vulnerable Pattern Examples

**Example 1: Unauthenticated cost-incurring RPC** [Approx Vulnerability : CRITICAL]
```rust
// ❌ VULNERABLE: sequencer.rs — no auth, no rate limit, no caller check
async fn batch_write(
    &self,
    request: tonic::Request<grpc::BatchWriteRequest>,
) -> std::result::Result<tonic::Response<grpc::BatchWriteResponse>, tonic::Status> {
    let blobs_for_submission = request.into_inner().blobs;
    let mut transactions = Vec::new();
    for blob in blobs_for_submission {
        let transaction: Transaction = serde_json::from_slice(&blob.data)
            .map_err(|e| tonic::Status::internal(e.to_string()))?;
        match &self.prevalidator {
            Some(prevalidator) => { /* optional validation */ }
            None => transactions.push(transaction), // @audit unvalidated push
        }
    }
    let memseq = self.memseq.clone();
    memseq.publish_many(transactions).await // @audit operator pays Celestia gas
        .map_err(|e| tonic::Status::internal(e.to_string()))?;
    Ok(tonic::Response::new(grpc::BatchWriteResponse { blobs: vec![] }))
}
```

**Example 2: Wildcard bind in default config** [Approx Vulnerability : CRITICAL]
```rust
// ❌ VULNERABLE: service reachable from any IP; "internal" API exposed publicly
// default + suggested config bind:
service_builder.serve("0.0.0.0:30730")  // @audit docs config.json also 0.0.0.0
```

**Example 3: Attacker one-liner** [Approx Vulnerability : CRITICAL]
```bash
# ❌ VULNERABLE: demonstrated against live mainnet endpoint
grpcurl m1-da-light-node.mainnet.movementnetwork.xyz:443 list \
  movementlabs.protocol_units.da.light_node.v1beta2.LightNodeService
# BatchRead / BatchWrite / ReadAtHeight / StreamReadFromHeight / StreamReadLatest / StreamWriteBlob
```

### Impact Analysis

#### Technical Impact
- Direct, repeatable loss of node operator TIA at zero attacker cost
- Arbitrary data written into the Movement Celestia namespace (pollution/impersonation of DA stream)
- Sequencer wallet depletion → node cannot publish → network liveness degradation
- Flood variant (#43330) freezes new account creation and transaction processing persistently

#### Business Impact
- Continuous operating-cost attack on every exposed operator; mainnet endpoint was confirmed exposed at report time
- Ecosystem trust: unauthenticated write path into consensus-adjacent infrastructure

#### Affected Scenarios
- Any deployment using default/suggested config (0.0.0.0 bind)
- Worse when prevalidator unset (Path A/C), still exploitable via replay when set (Path B)

### Secure Implementation

**Fix 1: Authenticate + restrict bind**
```rust
// ✅ SECURE: loopback bind by default; require auth (mTLS/token) for any remote caller
service_builder
    .serve("127.0.0.1:30730")?;                     // default: local only
// + interceptor rejecting requests without a valid operator-issued credential
```

**Fix 2: Quota + spending cap before publish**
```rust
// ✅ SECURE: bound per-caller submission size/rate and total daily Celestia spend
let budget = self.daily_submit_budget.consume(blob.data.len())?;
if budget.exceeded() { return Err(tonic::Status::resource_exhausted("DA submit budget")); }
memseq.publish_many(transactions).await?;
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Cost-incurring external-side-effect call (blob_submit / publish_many) directly reachable from a network RPC handler
- Config default binding 0.0.0.0 for a service assumed to be node-internal
- Prevalidator optional (Option<Prevalidator>) on a public write path
```

#### High-Signal Grep Seeds
```
- batch_write
- LightNodeService
- BatchWriteRequest
- blob_submit
- StreamWriteBlob
- publish_many
- 0.0.0.0
```

#### Code Patterns to Look For
```
- Pattern 1: `None => transactions.push(transaction)` on a network-exposed write handler
- Pattern 2: tonic service builder with wildcard bind address
- Pattern 3: no per-request size/rate accounting before an external paid submission

```

#### Audit Checklist
- [ ] Enumerate every gRPC/HTTP write endpoint on node services; verify auth + bind address
- [ ] Trace each endpoint to external side effects that cost money (DA submission, signing)
- [ ] Check whether validation is optional (Option-based) and what the None path does
- [ ] Test replay of previously valid blobs through the full validation stack

### Real-World Examples

#### Known Exploits
- **Movement mainnet (report-time demo)** — #43253 listed live `m1-da-light-node.mainnet.movementnetwork.xyz:443` write RPCs — Apr 2025 — no exploitation, exposure proven
  - Root cause: unauthenticated `batch_write` + `0.0.0.0` bind

#### Related CVEs/Reports
- #43330 (freeze via invalid-request flood to the same endpoint)
- #43241 (TIA drain in passthrough mode — same sink, different mode)

### Prevention Guidelines

#### Development Best Practices
1. Never bind cost-incurring services to wildcard addresses by default
2. Treat every gRPC method as public unless authenticated — including "internal" DA services
3. Gate external paid submissions behind quotas and spending caps

#### Testing Requirements
- Unit tests for: auth interceptor rejection paths
- Integration tests for: remote-host write attempt, replay of valid blobs, budget exhaustion
- Fuzzing targets: BatchWriteRequest deserialization + oversized payloads

### Keywords for Search

`movement`, `batch_write`, `light node`, `grpc`, `unauthenticated rpc`, `0.0.0.0 bind`, `celestia`, `blob_submit`, `tia drain`, `operator fund loss`, `memseq publish_many`, `access control`, `da layer`, `resource abuse`, `replay`

### Related Vulnerabilities

- DB/Sui-Move-specific/movement-l1/PREVALIDATOR_WHITELIST_GATING_BYPASS.md (validation optional on same path)
- DB/Sui-Move-specific/movement-l1/UNFUNDED_TX_DA_COST_DRAIN.md (same operator-pays sink, mempool entry)
- DB/Sui-Move-specific/SUI_MOVE_ACCESS_CONTROL_VALIDATION_VULNERABILITIES.md (Move-level access control family)
