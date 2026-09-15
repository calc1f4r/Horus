---
# Core Classification
protocol: movement
chain: movement
category: input_validation
vulnerability_type: sequence_number_zero_reuse|mempool_dedup_bypass|inflight_limit_exhaustion

# Pattern Identity
root_cause_family: sentinel_value_conflation
pattern_key: missing_zero_sequence_handling | used_sequence_number_pool | seq0_resubmission | duplicate_mempool_acceptance

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - protocol-units/execution/maptos/opt-executor (transaction_pipe.rs, has_invalid_sequence_number)
  - protocol-units/oracle/da/movement/memseq (mempool sequencing)
  - used_sequence_number_pool (per-sender sequence ledger)
path_keys:
  - missing_zero_sequence_handling | TransactionPipe::submit_transaction | opt-executor -> used_sequence_number_pool
  - missing_zero_sequence_handling | gas_increase_resubmission | opt-executor -> mempool inflight counter

# Attack Vector Details
attack_type: logical_error
affected_component: mempool_sequence_number_validation

# Technical Primitives
primitives:
  - sequence_number
  - used_sequence_number_pool
  - unwrap_or_default_sentinel
  - inflight_limit
  - MempoolStatusCode
  - gas_increase_transactions

# Grep / Hunt-Card Seeds
code_keywords:
  - has_invalid_sequence_number
  - used_sequence_number_pool
  - get_sequence_number
  - min_used_sequence_number
  - SequenceNumberValidity
  - InvalidSeqNumber
  - SEQUENCE_NUMBER_TOO_OLD
  - inflight_limit

# Impact Classification
severity: high
impact: dos
financial_impact: none

# Context Tags
tags:
  - l1_node_implementation
  - mempool
  - aptos_fork
  - rust_host
  - immunefi_attackathon

language: move        # Move-family L1; vulnerable host code is Rust (movement protocol-units)
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [R1] | reports/movement-l1_findings/42991-bc-high-user-can-reuse-sequence-number-causing-dos-and-breaking-core-invariant.md | HIGH | immunefi | #42991 |
| [R2] | reports/movement-l1_findings/43222-bc-high-a-transaction-with-sequence-number-0-can-be-submitted-multiple-times.md | HIGH | immunefi | #43222 |
| [R3] | reports/movement-l1_findings/42896-bc-high-attackers-can-exploit-sequence-number-tolerance-mechanism-to-to-cause-movement-network.md | HIGH | immunefi | #42896 |
| [R4] | reports/movement-l1_findings/43323-bc-high-inadequate-sequence-number-validation-in-da-light-node-enables-transaction-censorship.md | HIGH | immunefi | #43323 |

## Sequence Number 0 Reuse in Mempool Acceptance Breaks Tx Uniqueness Invariant

### Overview

Movement's opt-executor mempool conflates "sender has never used a sequence number" with "sender's last used sequence number is 0" (`unwrap_or(0)`), so transactions carrying `sequence_number == 0` pass `has_invalid_sequence_number()` on every resubmission — breaking the one-tx-per-sequence-number core invariant and letting a single sender exhaust the per-account `inflight_limit` to DoS all of that account's (and under gas-increase resubmission, general mempool) transaction flow.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because `used_sequence_number_pool.get_sequence_number(...).unwrap_or(0)` treats a missing entry as `0`, and `min_used_sequence_number = if used > 0 { used + 1 } else { 0 }` never advances past 0, so seq-0 transactions are re-accepted forever."
- Pattern key: `missing_zero_sequence_handling | used_sequence_number_pool | seq0_resubmission | duplicate_mempool_acceptance`
- Interaction scope: `multi_contract`
- Primary affected component(s): `TransactionPipe::submit_transaction -> has_invalid_sequence_number -> used_sequence_number_pool`
- Contracts / modules involved: `opt-executor/src/background/transaction_pipe.rs`, `memseq`, `used_sequence_number_pool`
- Path keys: `missing_zero_sequence_handling | TransactionPipe::submit_transaction | opt-executor -> used_sequence_number_pool`, `missing_zero_sequence_handling | gas_increase_resubmission | opt-executor -> mempool inflight counter`
- High-signal code keywords: `has_invalid_sequence_number`, `used_sequence_number_pool`, `min_used_sequence_number`, `inflight_limit`, `InvalidSeqNumber`
- Typical sink / impact: `duplicate mempool acceptance / broken tx-uniqueness invariant / per-account + mempool-wide DoS via inflight_limit`
- Validation strength: `strong` (working PoC test in [R1] shows seq-0 Accepted repeatedly vs seq-1 rejected as InvalidSeqNumber)

#### Contract / Boundary Map

- Entry surface(s): `TransactionPipe::submit_transaction()` (full-node tx ingress), gas-increase resubmission path
- Contract hop(s): `transaction_pipe.rs -> used_sequence_number_pool.get_sequence_number() -> mempool (memseq) inflight accounting`
- Trust boundary crossed: `user-submitted SignedTransaction -> node-internal sequence ledger`
- Shared state or sync assumption: `used_sequence_number_pool must advance monotonically per sender; inflight counter must reflect only unexecuted live transactions`

#### Valid Bug Signals

- Signal 1: `get_sequence_number()` result is combined with `unwrap_or(0)` (or similar Option::None == 0 conflation) before the min-sequence check
- Signal 2: the same validly-signed `sequence_number == 0` transaction is accepted twice (`MempoolStatusCode::Accepted` both times) by the same node
- Signal 3: repeated acceptance drives the sender's (or mempool's) `inflight_limit` to capacity, blocking honest transactions — invariant "each sequence number processed at most once per account" observably broken

#### False Positive Guards

- Not this bug when: rejections occur because `transaction.sequence_number() < min_sequence_number` triggers `SEQUENCE_NUMBER_TOO_OLD` — that is the guard working; the bug is only when seq 0 *passes* repeatedly
- Safe if: the pool distinguishes `None` (never used → allow 0) from `Some(0)` (0 used → min becomes 1), e.g. `Option` propagated into the min computation
- Requires attacker control of: a funded (gas-paying) account only — any normal user; no whitelist/privilege needed on default configs
- Distinct from [R3]/[R4]: those exploit *tolerance windows* and DA-light-node-side sequence gaps (censorship), not the seq-0 sentinel bug — verify which mechanism fires before merging findings

### Vulnerability Description

#### Root Cause

`has_invalid_sequence_number()` reads the sender's last-used sequence number from `used_sequence_number_pool` with `unwrap_or(0)`. `None` (sender unknown) and `Some(0)` (sender genuinely consumed seq 0) both yield `0`, and the subsequent `if used_sequence_number > 0 { used + 1 } else { 0 }` keeps `min_used_sequence_number` at 0 in both cases. A seq-0 transaction therefore always satisfies `sequence_number >= min_used_sequence_number` and is re-accepted on every submission ([R2] pins this at `transaction_pipe.rs#L164-L218`).

#### Attack Scenario / Path Variants

**Path A: Seq-0 duplicate acceptance (invariant break)**
Path key: `missing_zero_sequence_handling | TransactionPipe::submit_transaction | opt-executor -> used_sequence_number_pool`
Entry surface: `submit_transaction()` on the full node
Contracts touched: `transaction_pipe.rs -> used_sequence_number_pool -> mempool`
Boundary crossed: user tx ingress into node-internal sequence ledger
1. Fresh (or seq-0-only) sender account exists; pool returns `None` → treated as 0
2. Attacker submits the identical signed seq-0 transaction N times
3. Each submission returns `Accepted`; duplicates occupy mempool slots
4. Core invariant "one transaction per (sender, sequence_number)" is broken; downstream consumers (dedup, replays, accounting) see conflicting state

**Path B: inflight_limit exhaustion DoS via gas-increase resubmissions**
Path key: `missing_zero_sequence_handling | gas_increase_resubmission | opt-executor -> mempool inflight counter`
Entry surface: gas-increase resubmission flow
Contracts touched: `opt-executor -> mempool inflight tracking`
1. Attacker repeatedly submits gas-increase variants anchored on seq-0 transactions ([R1])
2. Each passes the (broken) seq check and is counted as in-flight
3. `inflight_limit` for the account/mempool fills with attacker entries that never clear
4. Honest transactions are rejected/blocked → network-wide processing stall on that path; [R1] maps this to "process transactions beyond set parameters / total network shutdown"

#### Vulnerable Pattern Examples

**Example 1: seq-0 sentinel conflation** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: transaction_pipe.rs — None (never used) and Some(0) are indistinguishable
let used_sequence_number = self
    .used_sequence_number_pool
    .get_sequence_number(&transaction.sender())
    .unwrap_or(0);                        // sentinel conflation: "unknown" == "used 0"

let min_used_sequence_number =
    if used_sequence_number > 0 { used_sequence_number + 1 } else { 0 };
// seq-0 tx always satisfies: 0 >= 0 → accepted forever
if transaction.sequence_number() < min_sequence_number {
    return Ok(SequenceNumberValidity::Invalid((
        MempoolStatus::new(MempoolStatusCode::InvalidSeqNumber),
        Some(DiscardedVMStatus::SEQUENCE_NUMBER_TOO_OLD),
    )));
}
```

**Example 2: PoC demonstrating repeated Acceptance ([R1], verbatim test)** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: seq 0 accepted 4x; seq 1 accepted once then rejected
let user_transaction = create_signed_transaction(0, &maptos_config);
let (mempool_status, _) = transaction_pipe.submit_transaction(user_transaction).await?;
assert_eq!(mempool_status.code, MempoolStatusCode::Accepted); // 1st
// ...identical resubmissions of seq 0 → Accepted, Accepted, Accepted
let user_transaction = create_signed_transaction(1, &maptos_config);
let (mempool_status, _) = transaction_pipe.submit_transaction(user_transaction).await?;
assert_eq!(mempool_status.code, MempoolStatusCode::Accepted);
let user_transaction = create_signed_transaction(1, &maptos_config);
let (mempool_status, _) = transaction_pipe.submit_transaction(user_transaction).await?;
assert_eq!(mempool_status.code, MempoolStatusCode::InvalidSeqNumber); // guard works only for seq > 0
```

**Example 3: adjacent sequence-validation gaps in the same family ([R3] tolerance window, [R4] DA-light-node censorship)** [Approx Vulnerability : HIGH]
```text
// ❌ VULNERABLE (family variants, different code paths):
// [R3] memseq/sequence tolerance mechanism lets committed_sequence_number /
//      min_sequence_number windows be exploited so reused numbers wedge the network
// [R4] DA light node prevalidate does not reconcile aptos_transaction.sequence_number
//      against committed state → attacker occupies future sequence numbers and
//      censors a victim's transactions
```

### Impact Analysis

#### Technical Impact
- Per-sender transaction uniqueness invariant broken; mempool holds multiple valid entries for one (sender, seq) pair
- `inflight_limit` exhaustion blocks all future submissions for the account and degrades mempool throughput network-wide
- Downstream dedup/indexers/execution observe contradictory sequence state ([R1] explicitly flags "breaking core invariant")

#### Business Impact
- Cheap DoS (only gas for the first tx; resubmissions of the same signed blob are near-free per [R1])
- Chain liveness degradation maps to Immunefi attackathon High impacts: processing beyond set parameters; potential total shutdown

#### Affected Scenarios
- Any account whose next legitimate sequence number is 0 (new accounts) — the most common onboarding case
- Aggravated on default configs with no whitelist prevalidation (see `PREVALIDATOR_WHITELIST_DISABLE_BYPASS.md`)

### Secure Implementation

**Fix 1: propagate Option instead of a 0 sentinel ([R2] recommendation)**
```rust
// ✅ SECURE: distinguish "no sequence number used yet" from "0 was used"
let used_sequence_number: Option<u64> = self
    .used_sequence_number_pool
    .get_sequence_number(&transaction.sender());          // keep the Option
let min_used_sequence_number: u64 = match used_sequence_number {
    Some(n) => n + 1,        // 0 was really used → next legal is 1
    None => 0,               // never used → 0 is legal exactly once
};
// A second seq-0 tx now sees min == 1 and is rejected with SEQUENCE_NUMBER_TOO_OLD.
// Additionally: cap per-sender inflight accounting so gas-increase resubmissions
// cannot pin the inflight_limit (defense-in-depth for Path B).
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Tx-ingress path consults a per-sender sequence ledger before mempool insert
- Option lookup flattened with unwrap_or(0)/unwrap_or_default before comparison
- Off-by-one style "if x > 0 { x+1 } else { 0 }" guarding a lower bound
- Inflight/dedup counters keyed on (sender, seq) that assume uniqueness the ingress does not enforce
```

#### High-Signal Grep Seeds
```
- has_invalid_sequence_number
- used_sequence_number_pool
- min_used_sequence_number
- InvalidSeqNumber
- inflight_limit
```

#### Code Patterns to Look For
```
- Pattern 1: .get_sequence_number(...).unwrap_or(0)
- Pattern 2: min computation where the sentinel (0) collides with a legitimate value
- Pattern 3: tests asserting seq N rejected but no test asserting seq 0 resubmission rejected
```

#### Audit Checklist
- [ ] Submit the identical signed seq-0 transaction twice; second must be rejected
- [ ] Verify Option vs sentinel handling for "account never seen" in every sequence-check implementation (executor AND da-light-node prevalidator)
- [ ] Check whether gas-increase resubmission can inflate per-account inflight counts without bound

### Real-World Examples

#### Known Exploits
- None public for Movement seq-0 reuse specifically; the class (sequence-number mishandling enabling mempool DoS) is a recurring L1 client theme

#### Related CVEs/Reports
- Immunefi Attackathon Movement Labs: #42991, #43222, #42896, #43323 (this entry's sources)
- See also `MEMPOOL_*`/sequencer entries in this directory for adjacent inflight/GC failures

### Prevention Guidelines

#### Development Best Practices
1. Never flatten `Option<u64>` domain sentinels into the value domain; carry `None` explicitly
2. Property-test the invariant: for any sender, each sequence number is accepted at most once
3. Treat "new account's first sequence number" as its own test case class

#### Testing Requirements
- Unit tests for: seq-0 first submission, seq-0 resubmission, `Some(0)` vs `None` pool states
- Integration tests for: parallel submission races on the same seq; gas-increase resubmission inflight accounting
- Fuzzing targets: sequence-number bounds at u64 edges (max, wrap)

### References

#### Technical Documentation
- Aptos sequence number semantics (Movement is an Aptos fork): https://github.com/aptos-labs/aptos-core (aptos-types transaction metadata)

#### Security Research
- Immunefi Movement Labs Attackathon (Mar–Apr 2025): reports #42991, #43222, #42896, #43323

### Keywords for Search

`sequence_number`, `seq zero`, `unwrap_or(0)`, `sentinel conflation`, `used_sequence_number_pool`, `has_invalid_sequence_number`, `mempool dedup`, `duplicate transaction`, `inflight_limit`, `gas increase resubmission`, `InvalidSeqNumber`, `SEQUENCE_NUMBER_TOO_OLD`, `transaction uniqueness invariant`, `movement mempool`, `aptos fork mempool`, `transaction_pipe`, `censorship`, `DoS`

### Related Vulnerabilities

- `PREVALIDATOR_WHITELIST_DISABLE_BYPASS.md` (missing ingress validation lets junk reach this path)
- `SEQUENCER_UNFUNDED_TX_FUND_DRAIN.md` (same ingress, economic sink)
- `EXECUTION_SIGNATURE_BYPASS.md` (existing entry — downstream trust of unvalidated tx data)
