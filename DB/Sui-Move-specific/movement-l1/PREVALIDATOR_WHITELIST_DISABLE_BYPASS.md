---
# Core Classification
protocol: movement
chain: movement
category: access_control
vulnerability_type: prevalidation_disable_bypass|fail_open_config|signature_check_skip

# Pattern Identity
root_cause_family: fail_open_validation
pattern_key: whitelist_optional | light_node_prevalidator | no_whitelist_config | signature_validation_bypass

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - protocol-units/da/movement/protocol/prevalidator (Validator::prevalidate)
  - protocol-units/da/movement/protocol/light-node (sequencer.rs batch_write)
  - protocol-units/da/movement/protocol/light-node (light_node.rs run_server, 0.0.0.0 bind)
path_keys:
  - whitelist_optional | batch_write_grpc_no_whitelist | light-node -> prevalidator(None path)
  - whitelist_optional | full_node_ingress_default_config | opt-executor -> mempool -> DA

# Attack Vector Details
attack_type: data_manipulation
affected_component: transaction_ingress_prevalidation

# Technical Primitives
primitives:
  - prevalidate
  - whitelist_validator
  - verify_signature
  - Option<Prevalidator>
  - 0.0.0.0_bind
  - fail_open

# Grep / Hunt-Card Seeds
code_keywords:
  - whitelist_validator
  - whitelist
  - prevalidator
  - is_some
  - contains
  - Transaction sender not in whitelist
  - run_server
  - accept_http1

# Impact Classification
severity: high
impact: dos
financial_impact: medium

# Context Tags
tags:
  - l1_node_implementation
  - configuration
  - fail_open
  - signature_bypass
  - rust_host
  - immunefi_attackathon

language: move        # Move-family L1; vulnerable host code is Rust (movement protocol-units)
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [R1] | reports/movement-l1_findings/41794-bc-high-not-having-any-whitelisted-account-completely-disables-the-prevalidator-leading-to-tra.md | HIGH | immunefi | #41794 |
| [R2] | reports/movement-l1_findings/41373-bc-high-premature-transaction-acceptance-to-mempool-da-without-signature-validation.md | HIGH | immunefi | #41373 |
| [R3] | reports/movement-l1_findings/41722-bc-high-the-passthrough-da-light-node-does-not-prevalidate-transactions-which-leads-to-non-des.md | HIGH | immunefi | #41722 |
| [R4] | reports/movement-l1_findings/43017-bc-high-prevalidation-does-not-validate-application-priority-sequence-number-and-id.md | HIGH | immunefi | #41794/#43017 |

## Whitelist-Optional Prevalidator Fails Open: No Whitelist ⇒ No Signature Validation

### Overview

Movement's light-node prevalidator runs signature validation *inside* the whitelist component, and the whole prevalidator is an `Option`. When no whitelist accounts are configured (the default and suggested configuration), the `Option` is `None` (or the whitelist arm is skipped) and **all** prevalidation — including `verify_signature()` — is skipped: transactions with invalid or missing signatures from *any* forged sender are accepted into the mempool and published to Celestia DA at sequencer expense.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because signature validation is nested inside the optional whitelist prevalidator, so an empty/unset whitelist disables not just sender filtering but signature verification itself — validation fails open on configuration."
- Pattern key: `whitelist_optional | light_node_prevalidator | no_whitelist_config | signature_validation_bypass`
- Interaction scope: `multi_contract`
- Primary affected component(s): `Validator::prevalidate (prevalidator crate)`, `batch_write Option<Prevalidator> handling`, `run_server 0.0.0.0 bind`
- Contracts / modules involved: `movement-da-light-node-prevalidator`, `light-node/src/sequencer.rs`, `light-node/src/light_node.rs`
- Path keys: `whitelist_optional | batch_write_grpc_no_whitelist | light-node -> prevalidator(None path)`, `whitelist_optional | full_node_ingress_default_config | opt-executor -> mempool -> DA`
- High-signal code keywords: `whitelist_validator`, `prevalidator`, `Transaction sender not in whitelist`, `run_server`, `accept_http1`
- Typical sink / impact: `forged-sender txs accepted to mempool/DA / resource waste / sequencer fee drain / unprocessable blocks downstream`
- Validation strength: `strong` ([R1]+[R2] quote the exact skip logic; [R3] confirms the passthrough variant; PoC-grade tracing throughout)

#### Contract / Boundary Map

- Entry surface(s): `LightNodeService::batch_write()` (0.0.0.0-bound gRPC), full-node tx ingress in default config
- Contract hop(s): `batch_write -> match &self.prevalidator { None => push(transaction) } -> memseq.publish_many -> DA`; and `prevalidate -> AptosTransactionValidator (sig) -> whitelist_validator (optional)`
- Trust boundary crossed: `internet-facing gRPC → mempool/DA pipeline (all validation optional)`
- Shared state or sync assumption: `mempool and DA assume every admitted tx passed signature verification; that assumption silently evaporates in default config`

#### Valid Bug Signals

- Signal 1: signature verification call site is lexically/statically inside the whitelist validation component (or gated on whitelist being `Some`)
- Signal 2: with whitelist unset, a transaction with an invalid signature is accepted (`MempoolStatusCode::Accepted`) into the mempool
- Signal 3: forged-sender transactions reach Celestia DA and downstream execution fails on them, degrading nodes ([R1] impact: transactions unprocessable, resource waste)

#### False Positive Guards

- Not this bug when: signature validation is an unconditional step in the pipeline independent of whitelist configuration (check call-site placement, not config docs)
- Safe if: `prevalidator` is guaranteed `Some` in all shipped configs AND signature check precedes any whitelist short-circuit
- Requires attacker control of: network access only (gRPC bound 0.0.0.0 in default/suggested configs per [R2]/#43253 lineage)
- Distinct from `EXECUTION_SIGNATURE_BYPASS.md` (existing): that entry covers the *executor* trusting unverified txs read back from DA; THIS entry covers *ingress* skipping verification at submission time. Different component, different fix locus.
- Distinct from `LIGHTNODE_BATCH_WRITE_UNAUTHENTICATED.md` (existing): that is missing authN on the RPC; this is missing validation logic inside an authenticated-enough path. Both needed.

### Vulnerability Description

#### Root Cause

`Validator::prevalidate` composes two stages: `AptosTransactionValidator.prevalidate` (deserialize + `verify_signature`) then `whitelist_validator.prevalidate` (sender ∈ whitelist). But the whitelist is a deployment choice, and when it is not configured, the code path skips validation entirely — `match &self.prevalidator { ... None => transactions.push(transaction) }` in `batch_write` forwards the raw deserialized transaction with zero checks ([R2]). [R1] further shows the "no whitelisted accounts" state disables the prevalidator wholesale. The design error is coupling mandatory validation (signatures) to optional policy (whitelisting), i.e., fail-open composition.

#### Attack Scenario / Path Variants

**Path A: default-config signature bypass via batch_write**
Path key: `whitelist_optional | batch_write_grpc_no_whitelist | light-node -> prevalidator(None path)`
Entry surface: `batch_write` gRPC on 0.0.0.0:30730
Contracts touched: `light-node -> (no prevalidation) -> memseq -> Celestia`
Boundary crossed: internet gRPC → DA pipeline
1. Node runs default/suggested config: no whitelist ⇒ prevalidator disabled
2. Attacker submits transactions with invalid/missing signatures, arbitrary forged `sender`
3. `None => transactions.push(transaction)` — no checks at all
4. Forged txs flood mempool and DA; sequencer pays TIA; executor chokes on junk ([R1]: "leading to transactions being unprocessable")

**Path B: passthrough DA light node without prevalidation ([R3])**
Path key: `whitelist_optional | full_node_ingress_default_config | opt-executor -> mempool -> DA`
Entry surface: passthrough-mode light node streams
Contracts touched: passthrough light-node → mempool/DA
1. Passthrough node (no prevalidator attached) forwards transactions
2. Non-deserializable / invalid transactions enter DA streams
3. Downstream full nodes fail on deserialization → degraded/stalled processing
4. Same fail-open root: absence of optional policy disables mandatory checks

#### Vulnerable Pattern Examples

**Example 1: batch_write None-arm skips everything ([R2] verbatim)** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: prevalidation is optional; absent config ⇒ zero validation
match &self.prevalidator {
    Some(prevalidator) => {
        match prevalidator.prevalidate(transaction).await {
            Ok(prevalidated) => { transactions.push(prevalidated.into_inner()); }
            Err(e) => { /* discard or internal error */ }
        }
    }
    None => transactions.push(transaction),   // ← raw attacker blob straight to DA
}
```

**Example 2: signature check nested inside optional whitelist stage ([R1]/[R2] structure)** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: mandatory check (signature) coupled to optional policy (whitelist)
impl PrevalidatorOperations<Transaction, Transaction> for Validator {
    async fn prevalidate(&self, transaction: Transaction) -> Result<Prevalidated<Transaction>, Error> {
        let aptos_transaction = AptosTransactionValidator.prevalidate(transaction).await?; // sig
        let aptos_transaction = self
            .whitelist_validator                       // ← whole stage vanishes when
            .prevalidate(aptos_transaction.into_inner())//   whitelist is unconfigured,
            .await?.into_inner();                      //   taking sig-check path with it
        Ok(Prevalidated(/* re-serialize */))
    }
}
// With no whitelisted accounts the prevalidator is disabled entirely ([R1]):
// signature verification never runs → txs with invalid signatures accepted.
```

**Example 3: 0.0.0.0 bind makes the fail-open path internet-reachable ([R2]/#43244 config)** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: default/suggested configs bind all interfaces
Server::builder()
    .max_frame_size(1024 * 1024 * 16 - 1)
    .accept_http1(true)
    .add_service(LightNodeServiceServer::new(self.clone()))
    .add_service(reflection)
    .serve(address.parse()?)     // address = 0.0.0.0 in default + suggested config
```

### Impact Analysis

#### Technical Impact
- Any party can inject arbitrary forged-sender transactions into mempool + Celestia DA
- Downstream nodes waste deserialization/execution effort on invalid txs; unprocessable blocks ([R1])
- Compounds with every downstream trust assumption (execution sig bypass, replay, censorship entries)

#### Business Impact
- Sequencer TIA drain (publishing junk), node resource +30% consumption class impacts
- Trust failure: mempool guarantees (authenticated senders) silently absent in default config

#### Affected Scenarios
- Default and suggested deployments (no whitelist) — i.e., the common case, not an exotic misconfig
- Passthrough-mode networks ([R3])

### Secure Implementation

**Fix 1: decouple mandatory validation from optional policy (fail closed)**
```rust
// ✅ SECURE: signature validation is unconditional; whitelist is additive policy
impl PrevalidatorOperations<Transaction, Transaction> for Validator {
    async fn prevalidate(&self, transaction: Transaction) -> Result<Prevalidated<Transaction>, Error> {
        // 1. ALWAYS run structural + signature validation, regardless of config
        let aptos_transaction: AptosTransaction =
            bcs::from_bytes(&transaction.data()).map_err(|e| {
                Error::Validation(format!("Failed to deserialize AptosTransaction: {e}"))
            })?;
        aptos_transaction.verify_signature().map_err(|e| {
            Error::Validation(format!("Failed to prevalidate signature: {e}"))
        })?;
        // 2. Whitelist applies ONLY if configured — it filters, never gates the sig check
        if let Some(whitelist) = &self.whitelist_validator {
            if !whitelist.contains(&aptos_transaction.sender()) {
                return Err(Error::Validation("Transaction sender not in whitelist".to_string()));
            }
        }
        Ok(Prevalidated(aptos_transaction))
    }
}
// And at the call site: make the prevalidator non-optional (type-level guarantee),
// failing startup if not configured — never `None => push(transaction)`.
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Optional validator component (Option<T> or cfg flag) guarding a mandatory security property
- Validation stage composition where one stage's absence disables earlier stages
- Internet-bound service (0.0.0.0) whose input validation depends on deployment config
- Fail-open match arms: None => accept
```

#### High-Signal Grep Seeds
```
- whitelist_validator
- prevalidator
- Transaction sender not in whitelist
- None => transactions.push
- run_server
```

#### Code Patterns to Look For
```
- Pattern 1: match &self.prevalidator { Some(..) => validate, None => accept }
- Pattern 2: verify_signature() reachable only through a configurable component
- Pattern 3: config defaults (0.0.0.0 bind, empty whitelist) that disable security stages
```

#### Audit Checklist
- [ ] Disable whitelist in config; submit invalid-signature tx; must be rejected
- [ ] Verify signature verification is unconditional in every ingress path (batch_write, full-node, passthrough)
- [ ] Check bind address defaults for every internet-exposed service

### Real-World Examples

#### Known Exploits
- None public; fail-open validation composition is a recurring L1-client audit theme (cf. geth CORS allow-all default in the bnb-chain corpus)

#### Related CVEs/Reports
- Immunefi Movement Labs Attackathon: #41794, #41373, #41722, #43017 (sources)
- Related prevalidation gaps: #43017 (application_priority/sequence/id fields not validated — same prevalidator, additional unchecked fields)

### Prevention Guidelines

#### Development Best Practices
1. Separate mandatory validation (signatures, structure) from optional policy (whitelists, rate limits); mandatory checks must be unconditional
2. Fail closed: refuse to start (or reject all input) when a required validator is unconfigured
3. Audit shipped default configs as attack surface, not conveniences

#### Testing Requirements
- Unit tests for: empty-whitelist + invalid-signature ⇒ reject; None prevalidator ⇒ startup failure
- Integration tests for: batch_write with forged signatures across all config permutations
- Fuzzing targets: signature field mutations under every config combination

### References

#### Technical Documentation
- Movement suggested config (0.0.0.0 binds): https://docs.movementnetwork.xyz/assets/files/config-4551e1260977506ebb8dcdea19b254ed.json (cited in #43253/#43244)

#### Security Research
- Immunefi Movement Labs Attackathon (Mar–Apr 2025): #41794, #41373, #41722, #43017

### Keywords for Search

`fail open`, `whitelist optional`, `prevalidator disabled`, `signature validation bypass`, `invalid signature accepted`, `forged sender`, `batch_write`, `0.0.0.0 bind`, `default configuration`, `Option<Prevalidator>`, `passthrough light node`, `mempool acceptance`, `verify_signature skipped`, `configuration-dependent security`, `movement prevalidator`, `tx ingress`, `fail-open validation`, `optional security stage`, `mempool flooding`, `DA pollution`

### Related Vulnerabilities

- `EXECUTION_SIGNATURE_BYPASS.md` (existing — downstream executor variant)
- `LIGHTNODE_BATCH_WRITE_UNAUTHENTICATED.md` (existing — RPC authN hole)
- `SEQUENCER_UNFUNDED_TX_FUND_DRAIN.md` (economic sink reachable once validation fails open)
- `MALFORMED_TX_EXECUTOR_PANIC.md` (this directory — what the junk txs do at execution)
