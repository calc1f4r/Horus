---
# Core Classification
protocol: generic
chain: movement
category: da
vulnerability_type: da_blob_consensus
root_cause_family: see pattern_key

# Pattern Identity
pattern_key: da-blob-consensus | da blob consensus | varies by finding | see references

# Interaction Scope
interaction_scope: varies
involved_contracts:
  - da blob consensus

# Attack Vector Details
attack_type: varies
affected_component: da blob consensus

# Technical Primitives
primitives:
  - added
  - allows
  - attackers
  - availability
  - batch
  - before

# Grep / Hunt-Card Seeds
code_keywords:
  - added
  - allows
  - attackers
  - availability
  - batch
  - before
  - blob
  - blobs

severity: critical
impact: varies
language: varies
tags:
  - movement
  - l1
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [m1] | reports/movement-l1_findings/41437-bc-high-an-edge-case-allows-duplicate-transactions-to-be-added-to-the-mempool-of-the-sequencer.md | HIGH | Immunefi (Capybara) | \[BC-High] an edge case allows duplicate transactions to be added to the mempool of the sequencer |
| [m2] | reports/movement-l1_findings/41489-bc-critical-blob-sizes-remain-unchecked-leading-to-chain-halt.md | CRITICAL | Immunefi (okmxuse) | #41489 \[BC-Critical] Blob sizes remain unchecked leading to chain halt |
| [m3] | reports/movement-l1_findings/41686-bc-high-the-passthrough-da-light-node-streams-transactions-instead-of-blocks-which-means-that.md | HIGH | Immunefi (KlosMitSoss) | #41686 \[BC-High] The passthrough DA light node streams transactions instead of blocks which means that the block cannot be deserialized |
| [m4] | reports/movement-l1_findings/42761-bc-high-memseq-does-not-verify-client-specified-expiration-for-transactions-before-including-t.md | HIGH | Immunefi (ZeroTrust) | #42761 \[BC-High] Memseq does not verify client-specified expiration for transactions before including them in DA (Data Availability). |
| [m5] | reports/movement-l1_findings/43110-bc-critical-validator-can-dos-the-da-layer-by-requesting-a-big-range-of-blobs.md | CRITICAL | Immunefi (br0nz3p1ck4x3) | #43110 \[BC-Critical] Validator can DoS the DA Layer by requesting a big range of blobs |
| [m6] | reports/movement-l1_findings/43114-bc-critical-attackers-can-cause-total-shutdown-network-by-exploiting-missing-of-blob-size-chec.md | CRITICAL | Immunefi (perseverance) | #43114 \[BC-Critical] attackers can cause total shutdown network by exploiting missing of blob size check in da lightnode |
| [m7] | reports/movement-l1_findings/43229-bc-high-there-is-a-bug-can-allows-malicious-data-to-enter-the-da-layer-and-be-signed-by-a-legi.md | HIGH | Immunefi (XDZIBECX) | #43229 \[BC-High] There is a bug can allows malicious data to enter the DA layer and be signed by a legitimate node |
| [m8] | reports/movement-l1_findings/43255-bc-medium-user-transactions-might-be-lost-due-to-missing-error-handling-in-celestia-rpc-client.md | MEDIUM | Immunefi (perseverance) | #43255 \[BC-Medium] user transactions might be lost due to missing error handling in celestia rpc client requests blob submit failure&#x20; |
| [m9] | reports/movement-l1_findings/43315-bc-critical-da-light-node-can-be-dosed-due-to-lack-of-batch-validation.md | CRITICAL | Immunefi (Nirix0x) | #43315 \[BC-Critical] DA Light Node Can Be DoSed Due to Lack of Batch Validation |
| [m10] | reports/movement-l1_findings/41255-bc-medium-blocking-sleep-in-async-context-leads-to-thread-pool-exhaustion-and-dos.md | MEDIUM | Immunefi (Rhaydden) | #41255 \[BC-Medium] Blocking sleep in async context leads to thread pool exhaustion and DoS |
| [m11] | reports/movement-l1_findings/41368-bc-high-rpc-server-takedown.md | HIGH | Immunefi (keizo) | #41368 \[BC-High] RPC server takedown |
| [m12] | reports/movement-l1_findings/41466-bc-medium-incorrect-sequence-number-tracking-in-mempool-commit.md | MEDIUM | Immunefi (Rhaydden) | #41466 \[BC-Medium] Incorrect sequence number tracking in mempool commit |
| [m13] | reports/movement-l1_findings/41669-bc-medium-incorrect-gas-cost-used-for-bls12381-subgroup-check-causes-70-undercharge.md | MEDIUM | Immunefi (Minato7namikazi) | #41669 \[BC-Medium] Incorrect Gas Cost Used for BLS12381 Subgroup Check Causes \~70% Undercharge |
| [m14] | reports/movement-l1_findings/41678-bc-medium-transactions-directly-sent-to-the-passthrough-will-cause-the-mempool-to-accept-more.md | MEDIUM | Immunefi (KlosMitSoss) | #41678 \[BC-Medium] Transactions directly sent to the passthrough will cause the mempool to accept more transactions than the \`inflight\_limit\` |
| [m15] | reports/movement-l1_findings/41714-bc-high-tampering-the-id-of-signed-transactions-to-prevent-others-from-executing.md | HIGH | Immunefi (Capybara) | \[BC-High] tampering the id of signed transactions to prevent others from executing |
| [m16] | reports/movement-l1_findings/41715-bc-high-manipulating-the-sequence-number-of-signed-transactions-to-reorder-them-or-prevent-the.md | HIGH | Immunefi (Capybara) | \[BC-High] manipulating the sequence number of signed transactions to reorder them or prevent their execution |
| [m17] | reports/movement-l1_findings/41864-bc-medium-when-memseq-selects-a-transaction-from-a-particular-user-to-include-in-a-block-it-do.md | MEDIUM | Immunefi (ZeroTrust) | #41864 \[BC-Medium] When Memseq selects a transaction from a particular user to include in a block  it does not remove transactions from Memseq that h |
| [m18] | reports/movement-l1_findings/41878-bc-high-edge-case-allows-replaying-user-transactions-to-fill-the-mempool.md | HIGH | Immunefi (Capybara) | \[BC-High] edge case allows replaying user transactions to fill the mempool |
| [m19] | reports/movement-l1_findings/41987-bc-critical-oversized-blocks-split-the-chain.md | CRITICAL | Immunefi (jovi) | bc critical oversized blocks split the chain |
| [m20] | reports/movement-l1_findings/42011-bc-high-duplicate-tx-ids-in-blockchain-blocks-are-possible.md | HIGH | Immunefi (Rhaydden) | #42011 \[BC-High] Duplicate tx IDs in blockchain blocks are possible |
| [m21] | reports/movement-l1_findings/42535-bc-high-garbage-collecting-in-flight-transactions-can-lead-to-spiraling-network-delays.md | HIGH | Immunefi (HollaDieWaldfee) | #42535 \[BC-High] Garbage collecting in flight transactions can lead to spiraling network delays |
| [m22] | reports/movement-l1_findings/42762-bc-high-new-accounts-break-the-pipe-mempool-invariant-that-prevents-duplicate-transactions-fro.md | HIGH | Immunefi (Capybara) | \[BC-High] new accounts break the pipe mempool invariant that prevents duplicate transactions from filling the mempool |
| [m23] | reports/movement-l1_findings/42837-bc-critical-total-network-shutdown.md | CRITICAL | Immunefi (Capybara) | #42837 \[BC-Critical] total network shutdown |
| [m24] | reports/movement-l1_findings/42903-bc-high-attackers-are-able-to-submit-multiple-dupplicate-transactions-due-to-mismatched-mempoo.md | HIGH | Immunefi (Berserk) | #42903 \[BC-High] Attackers are able to submit multiple dupplicate transactions due to mismatched Mempool Implementation |
| [m25] | reports/movement-l1_findings/42928-bc-medium-depositing-gas-fees-into-the-governed-gas-pool-does-not-work-when-the-coinstore-is-f.md | MEDIUM | Immunefi (HollaDieWaldfee) | #42928 \[BC-Medium] Depositing gas fees into the governed gas pool does not work when the CoinStore is frozen |
| [m26] | reports/movement-l1_findings/42930-bc-high-users-are-unable-to-increase-their-gas-resulting-in-stuck-funds.md | HIGH | Immunefi (okmxuse) | #42930 \[BC-High] Users are unable to increase their gas resulting in stuck funds |
| [m27] | reports/movement-l1_findings/42933-bc-medium-integer-underflow-in-garbage-collection-logic-of-usedsequencenumberpool-disrupting-t.md | MEDIUM | Immunefi (savi0ur) | #42933 \[BC-Medium] Integer Underflow in Garbage Collection Logic of UsedSequenceNumberPool disrupting transaction processing |
| [m28] | reports/movement-l1_findings/42936-bc-critical-potential-deadlock-or-panic-due-to-concurrent-lock-acquisition-in-transactionpipe.md | CRITICAL | Immunefi (savi0ur) | #42936 \[BC-Critical] Potential Deadlock or Panic Due to Concurrent Lock Acquisition in \`TransactionPipe\` |
| [m29] | reports/movement-l1_findings/43054-bc-high-malicious-light-node-can-dos-the-full-node.md | HIGH | Immunefi (Blockian) | #43054 \[BC-High] malicious light node can dos the full node |
| [m30] | reports/movement-l1_findings/43136-bc-high-multiple-transactions-sent-by-the-same-account-in-the-same-block-timeframe-can-get-stu.md | HIGH | Immunefi (niroh) | #43136 \[BC-High] Multiple transactions sent by the same account in the same block timeframe can get stuck in the TranactionPipe core\_mempool |
| [m31] | reports/movement-l1_findings/43137-bc-medium-multiple-transactions-from-the-same-account-with-increasing-sequence-number-and-prio.md | MEDIUM | Immunefi (niroh) | #43137 \[BC-Medium] Multiple Transactions from the same account with increasing sequence number and priorities will be sorted incorrectly in the block |
| [m32] | reports/movement-l1_findings/43148-bc-medium-potential-unhandled-panic-in-protocol-units-execution-maptos-opt-executor-executor-m.md | MEDIUM | Immunefi (p4rsely) | #43148 \[BC-Medium] Potential unhandled panic in protocol-units::execution::maptos::opt-executor::executor/mod::decrement\_transactions\_in\_flight |
| [m33] | reports/movement-l1_findings/43214-bc-critical-unchecked-transaction-size-allows-malicious-users-to-dos-honest-users-transactions.md | CRITICAL | Immunefi (okmxuse) | #43214 \[BC-Critical] Unchecked transaction size allows malicious users to DOS honest users transactions |
| [m34] | reports/movement-l1_findings/43241-bc-high-attackers-can-drain-tia-from-nodes-in-networks-running-in-passthrough-mode.md | HIGH | Immunefi (usmannk) | #43241 \[BC-High] Attackers can drain TIA from nodes in networks running in passthrough mode |
| [m35] | reports/movement-l1_findings/43333-bc-critical-missing-depths-checks-in-cached-typelayout-leads-to-network-divergence.md | CRITICAL | Immunefi (dustincha) | #43333 \[BC-Critical] Missing Depths Checks in Cached TypeLayout leads to Network Divergence |
| [q36] | reports/movement-l1_findings/41023-bc-insight-incomplete-transaction-decrementing-leading-to-undesired-behaviour.md | INFO | Immunefi (okmxuse) | #41023 \[BC-Insight] Incomplete transaction decrementing leading to undesired behaviour |
| [q37] | reports/movement-l1_findings/41235-bc-insight-incorrect-celestia-bridge-keyring-flag-causes-network-partition-in-data-availabilit.md | INFO | Immunefi (Rhaydden) | #41235 \[BC-Insight] Incorrect celestia bridge keyring flag causes network partition in data availability layer |
| [q38] | reports/movement-l1_findings/41243-bc-insight-the-mempool-garbage-collector-doesnt-fully-execute-garbage-collection-on-each-itera.md | INFO | Immunefi (jovi) | #41243 \[BC-Insight] The mempool garbage collector doesn't fully execute garbage collection on each iteration |
| [q39] | reports/movement-l1_findings/41324-bc-insight-celestia-auth-tokens-can-be-stolen-by-sniffing-websocket-requests.md | INFO | Immunefi (jovi) | #41324 \[BC-Insight] Celestia auth tokens can be stolen by sniffing websocket requests |
| [q40] | reports/movement-l1_findings/41560-bc-insight-blobtype-of-blobresponse-can-never-be-sequencedblobblock.md | INFO | Immunefi (KlosMitSoss) | #41560 \[BC-Insight] BlobType of BlobResponse can never be SequencedBlobBlock |
| [q41] | reports/movement-l1_findings/41594-bc-insight-invalid-url-format-in-tcplistener-binding-prevents-rest-api-from-starting.md | INFO | Immunefi (Rhaydden) | #41594 \[BC-Insight] Invalid URL format in TcpListener binding prevents REST API from starting |
| [q42] | reports/movement-l1_findings/41618-bc-insight-timestamp-unit-doesnt-match-in-gccounter-which-causes-premature-transaction-evictio.md | INFO | Immunefi (Rhaydden) | #41618 \[BC-Insight] Timestamp unit doesn't match in GcCounter which causes premature transaction eviction |
| [q43] | reports/movement-l1_findings/41855-sc-insight-user-is-able-to-circumvent-blocklist-check-by-utilizing-soliditys-implementation.md | INFO | Immunefi (okmxuse) | #41855 \[SC-Insight] User is able to circumvent blocklist check by utilizing Solidity's implementation |
| [q44] | reports/movement-l1_findings/41980-bc-insight-full-nodes-panic-in-read-only-mode-whenever-a-transaction-is-sent.md | INFO | Immunefi (HollaDieWaldfee) | #41980 \[BC-Insight] Full nodes panic in read-only mode whenever a transaction is sent |
| [q45] | reports/movement-l1_findings/41985-bc-insight-using-the-test-keyring-backend-is-insecure.md | INFO | Immunefi (KlosMitSoss) | #41985 \[BC-Insight] Using the test keyring backend is insecure |
| [q46] | reports/movement-l1_findings/42557-bc-low-remote-signing-methods-can-fail-which-will-turn-off-the-light-node-block-proposer.md | LOW | Immunefi (Franfran) | #42557 \[BC-Low] Remote signing methods can fail which will turn off the light node block proposer |
| [q47] | reports/movement-l1_findings/42859-bc-insight-pub-key-format-mismatch-in-inknownsignersverifier.md | INFO | Immunefi (Rhaydden) | #42859 \[BC-Insight] Pub key format mismatch in \`InKnownSignersVerifier\` |
| [q48] | reports/movement-l1_findings/42895-bc-insight-misuse-of-error.md | INFO | Immunefi (okmxuse) | #42895 \[BC-Insight] Misuse of error |
| [q49] | reports/movement-l1_findings/42938-bc-insight-inefficient-garbage-collection-implementation-in-usedsequencenumberpool.md | INFO | Immunefi (savi0ur) | #42938 \[BC-Insight] Inefficient Garbage Collection Implementation in \`UsedSequenceNumberPool\` |
| [q50] | reports/movement-l1_findings/42939-bc-insight-transaction-expiration-is-not-validated-correctly-in-mempool-and-sequencer.md | INFO | Immunefi (Berserk) | #42939 \[BC-Insight] Transaction expiration is not validated correctly in mempool and sequencer |
| [q51] | reports/movement-l1_findings/43038-bc-insight-there-is-a-permanent-operator-lockout-came-from-an-unsafe-key-rotation.md | INFO | Immunefi (XDZIBECX) | #43038 \[BC-Insight] There is a permanent operator lockout came from an unsafe key rotation |
| [q52] | reports/movement-l1_findings/43168-bc-insight-under-normal-usage-of-the-blockchain-transactions-will-not-be-persisted.md | INFO | Immunefi (br0nz3p1ck4x3) | #43168 \[BC-Insight] Under normal usage of the blockchain  transactions will not be persisted |
| [q53] | reports/movement-l1_findings/43184-bc-insight-vulnerable-secp256k1-version-allows-validation-of-malformed-signatures.md | INFO | Immunefi (Rhaydden) | #43184 \[BC-Insight] Vulnerable \`Secp256k1\` version allows validation of malformed signatures |
| [q54] | reports/movement-l1_findings/43186-bc-insight-flawed-documentation-when-streaming-da-blobs-leads-to-confusion.md | INFO | Immunefi (okmxuse) | #43186 \[BC-Insight] Flawed documentation when streaming da blobs leads to confusion |
| [q55] | reports/movement-l1_findings/43217-bc-insight-incorrect-public-key-notification-after-key-rotation.md | INFO | Immunefi (Rhaydden) | #43217 \[BC-Insight] Incorrect public key notification after key rotation |
| [q56] | reports/movement-l1_findings/43221-bc-insight-expired-transactions-prevent-new-submissions-due-to-delayed-garbage-collection.md | INFO | Immunefi (KlosMitSoss) | #43221 \[BC-Insight] Expired transactions prevent new submissions due to delayed garbage collection |
| [q57] | reports/movement-l1_findings/43267-bc-insight-potential-indefinite-hang-denial-of-service-in-full-node-da-sync-due-to-missing-str.md | INFO | Immunefi (Nirix0x) | #43267 \[BC-Insight] Potential Indefinite Hang (Denial of Service) in Full Node DA Sync Due to Missing Stream Timeout For Light Node Connection |
| [q58] | reports/movement-l1_findings/43287-bc-low-certain-fees-are-unaccounted-for-causing-failed-transactions.md | LOW | Immunefi (okmxuse) | #43287 \[BC-Low] Certain fees are unaccounted for causing failed transactions |
| [q59] | reports/movement-l1_findings/43326-bc-insight-stale-transaction-state-in-mempool-when-sender-receiver-pipe-fails.md | INFO | Immunefi (Blockian) | #43326 \[BC-Insight] stale transaction state in mempool when sender receiver pipe fails |
| [q60] | reports/movement-l1_findings/43346-bc-insight-transactions-arriving-at-the-node-out-of-sequence-order-will-be-rejected-due-to-the.md | INFO | Immunefi (niroh) | #43346 \[BC-Insight] Transactions arriving at the node out of sequence order will be rejected due to the has\_invalid\_sequence\_number function |

## Da Blob Consensus

**da-blob-consensus patterns mined from uncited L1 audit reports** - 9 sec-tier findings (4 critical / 4 high / 1 medium) across 9 files from Immunefi (Capybara), Immunefi (KlosMitSoss), Immunefi (Nirix0x), Immunefi (XDZIBECX), Immunefi (ZeroTrust), Immunefi (br0nz3p1ck4x3).

### Overview

Titles in the references table are verbatim from source reports. Route to the exact report file for full PoC detail. Validation strength: `unassessed` (evidence rows only).

### Detection Patterns

#### High-Signal Grep Seeds
```
- added
- allows
- attackers
- availability
- batch
- before
- blob
- blobs
```

### Vulnerability Description

#### Root Cause

The cited reports describe da blob consensus paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `da-blob-consensus | da blob consensus | varies by finding | see references`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `da-blob-consensus | da blob consensus | varies by finding | see references | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `da-blob-consensus | da blob consensus | varies by finding | see references | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: #41489 \[BC-Critical] Blob sizes remain unchecked leading to chain halt** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// #41489 \[BC-Critical] Blob sizes remain unchecked leading to chain halt
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: #41489 \[BC-Critical] Blob sizes remain unchecked leading to chain halt
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: #43110 \[BC-Critical] Validator can DoS the DA Layer by requesting a big range of blobs** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// #43110 \[BC-Critical] Validator can DoS the DA Layer by requesting a big range of blobs
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: #43110 \[BC-Critical] Validator can DoS the DA Layer by requesting a big range of blobs
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: #43114 \[BC-Critical] attackers can cause total shutdown network by exploiting missing of blob size check in da lightnod** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// #43114 \[BC-Critical] attackers can cause total shutdown network by exploiting missing of blob size check in da lightnode
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: #43114 \[BC-Critical] attackers can cause total shutdown network by exploiting missing of blob size 
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```

### Impact Analysis

#### Technical Impact
- Wrong accounting / reward misallocation / stuck or double-counted funds (fund-loss class rows above)
- State inconsistency after partial failure (see error-handling references)
- Chain halt or node crash from unbounded work (see DoS rows)

#### Business Impact
- User fund loss and withdrawal freezes; validator downtime; consensus/partition risk for client-level bugs.

### Secure Implementation

**Fix 1: [Bound and validate at the entry surface]**
```rust
// ✅ SECURE: explicit bounds + validation before state mutation
fn handler(input: UntrustedInput) -> Result<(), Error> {
    ensure!(input.len() <= T::MaxInput::get(), Error::TooLarge);
    ensure!(is_valid(&input), Error::Invalid);
    state.update_checked(&input)?;
    Ok(())
}
```

**Fix 2: [Aggregate instead of iterate; cap growth]**
```rust
// ✅ SECURE: keep block-time work O(1) and cap attacker growth
fn on_block_end() {
    let aggregate = Aggregates::get();          // maintained incrementally
    distribute(&aggregate);                      // no unbounded iteration
}
fn create_plan(p: Plan) -> Result<(), Error> {
    ensure!(PlansCount::get() < T::MaxPlans::get(), Error::TooManyPlans);
    Ok(())
}
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Entry surface writes state before validating attacker-controlled fields
- Block-time hooks iterate collections whose size is attacker-influenceable
- Multi-step handlers where a mid-step failure leaves earlier writes committed
- Config setters without role checks or bounds
```

#### Audit Checklist
- [ ] Verify every attacker-reachable input is length/bounds-checked before state writes
- [ ] Verify block-time (end-blocker / on_finalize) iteration is O(1) or capped
- [ ] Verify failure paths roll back partial state mutations
- [ ] Cross-check the cited reports' fix status before re-reporting

### Keywords for Search

`added, allows, attackers, availability, batch, before, blob, blobs, block, blocks`

### Related Vulnerabilities

- Sibling entries under the same category folder
