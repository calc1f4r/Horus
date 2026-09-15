---
protocol: aurora-rainbow-bridge
chain: near
category: bridge
vulnerability_type: light_client_stall

root_cause_family: unhandled_error_state
pattern_key: missing_skip_slot_handling | eth2_light_client_relayer | beacon_reorg | relayer_stall

interaction_scope: cross_chain
involved_contracts:
  - eth2-client (NEAR contract)
  - eth2near-block-relay-rs (off-chain relayer)
  - SputnikDAO eth2-validator
path_keys:
  - missing_skip_slot_handling | relayer get_last_slot() | eth2-client.unfinalized_headers
  - stale_block_submission | relayer run() loop | eth2-client.unfinalized_headers -> submission_quota
  - no_stale_header_pruning | unfinalized_headers growth | contract_state_bloat

attack_type: denial_of_service
affected_component: bridge_light_client

primitives:
  - beacon_chain_light_client
  - unfinalized_headers
  - skipped_slot_reorg
  - submission_quota
  - storage_deposit

code_keywords:
  - unfinalized_headers
  - get_last_slot
  - block_known_on_near
  - get_last_submitted_slot
  - max_submitted_blocks_by_account
  - submit_only_finalized_blocks
  - unregister_submitter

severity: high
impact: dos
tags:
  - bridge
  - light_client
  - relayer
  - consensus
language: rust
version: "commits 50427ed (rainbow-bridge), 738833b (eth2-on-near-client-validator)"
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [RBE2] | reports/other-l1_findings/public-audits-reports-aurora-review-pdf.md | HIGH (1), MED (2) | Sigma Prime | Aurora Rainbow Bridge Eth2 Client v2.2, June 2023 |

## Aurora Rainbow Bridge ETH2 Client — Relayer Stall and Unbounded State Growth from Unfinalised Header Handling

### Overview

The NEAR-side Ethereum Beacon Chain light client accepts attested-but-unfinalised headers into `unfinalized_headers`; when the beacon chain re-orgs such a header into a skipped slot, the relayer's `get_last_slot()` search hits an unhandled error and stalls the bridge. Separately, re-orged stale headers are never prunable, causing unbounded contract state growth and permanently locking a relayer's storage deposit.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the relayer queries the light client with a slot that may have been re-orged into a skipped slot, and the resulting error path is not handled; and because stale unfinalised headers can never be removed from contract state."
- Pattern key: `missing_skip_slot_handling | eth2_light_client_relayer | beacon_reorg | relayer_stall`
- Interaction scope: `cross_chain`
- Primary affected component(s): `eth2-client NEAR contract`, `eth2near-block-relay-rs relayer`
- Contracts / modules involved: `eth2-client, eth2near-block-relay-rs, SputnikDAO validator`
- Path keys: see `path_keys` above
- High-signal code keywords: `unfinalized_headers`, `get_last_slot`, `block_known_on_near`, `unregister_submitter`
- Typical sink / impact: `bridge liveness halt (DoS), unbounded state growth, locked storage deposits`
- Validation strength: `strong` (detailed code-level root cause chain in source report)

#### Contract / Boundary Map

- Entry surface(s): relayer `run()` loop submitting headers; `unregister_submitter()` for deposit recovery
- Contract hop(s): `relayer.get_last_slot() -> eth_client_contract.get_last_submitted_slot() -> block_known_on_near(slot) -> beacon RPC get_beacon_block_body_for_block_id()`
- Trust boundary crossed: `off-chain relayer <-> NEAR light client contract <-> Beacon Node RPC`
- Shared state or sync assumption: `unfinalized_headers on NEAR must eventually become canonical-or-prunable; last_submitted_slot must point at a queryable block`

#### Valid Bug Signals

- Signal 1: Light client contract stores attested unfinalised headers keyed by slot, and relayer later queries beacon RPC with that slot
- Signal 2: `block_known_on_near(slot)?` propagates an error instead of handling the skipped-slot case, aborting `get_last_slot()`
- Signal 3: No pruning path exists for non-canonical entries in `unfinalized_headers`, and `unregister_submitter()` requires zero pending submissions — relayer deposit is bricked after one re-orged submission

#### False Positive Guards

- Not this bug when: only finalised headers are submitted (`submit_only_finalized_blocks` enabled post-fix), or the error path for missing blocks is explicitly handled
- Safe if: relayer accounts for skipped slots in its binary/linear search and treats "not found" as a search hint, not a fatal error
- Requires attacker control of: nothing — natural beacon chain re-orgs / late blocks trigger it (no malicious actor needed)

### Vulnerability Description

#### Root Cause

1. `get_last_slot()` finds the last unfinalised slot submitted to NEAR; if that slot was re-orged into a skip slot, `block_known_on_near(slot)?` fails with an unhandled error (RBE2-01, High).
2. The relayer submits every attested head; each re-orged submission burns quota against `max_submitted_blocks_by_account` until the relayer can neither submit nor unregister (RBE2-02, Medium).
3. Non-canonical headers stay in `unfinalized_headers` forever — unbounded state growth; only a fresh relayer keeps the bridge alive (RBE2-03, Medium, closed-wontfix at audit time).

#### Attack Scenario / Path Variants

**Path A: Relayer stall on skipped slot** [HIGH]
Path key: `missing_skip_slot_handling | relayer get_last_slot() | eth2-client.unfinalized_headers`
1. Beacon head proposed late; validators attest a skip slot; next proposer forks out the late block
2. Relayer had already submitted the late header into `unfinalized_headers`
3. `get_last_submitted_slot()` returns the skipped slot; `block_known_on_near(slot)` errors; error propagates unhandled
4. `eth2_to_near_relay` stalls until NEAR-side finalised slot exceeds the submitted slot — Eth2→NEAR bridging halts

**Path B: Submission quota exhaustion via routine re-orgs** [MEDIUM]
Path key: `stale_block_submission | relayer run() loop | submission_quota`
1. Relayer submits unfinalised heads as part of normal operation
2. Any re-org turns a submission stale, permanently consuming quota
3. Relayer hits `max_submitted_blocks_by_account`, cannot submit or `unregister_submitter()` (requires zero pending)
4. If it is the only relayer, bridge stalls; storage deposit stranded

**Path C: Unbounded state growth** [MEDIUM]
Path key: `no_stale_header_pruning | unfinalized_headers growth | contract_state_bloat`
1. Stale entries accumulate in `unfinalized_headers` with no removal API
2. Each new relayer repeats the cycle; contract state grows indefinitely or bridge operation halts

#### Vulnerable Pattern Examples

**Example 1: Unhandled error in slot search** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: block_known_on_near(slot)? errors when slot was re-orged to a skip slot;
// get_last_slot() does not handle it and the relay loop stalls
let last_submitted_slot = self.eth_client_contract.get_last_submitted_slot();
let slot = max(finalized_slot, last_submitted_slot);
// linear or binary search both reach:
if self.block_known_on_near(slot)? { /* ... */ } // error propagates, relay halts
```

**Example 2: Submitting unfinalised heads burns quota** [Approx Vulnerability : MEDIUM]
```rust
// ❌ VULNERABLE: submits current (unfinalised) head; re-orgs make submissions stale
// and irreversibly consume max_submitted_blocks_by_account quota
let last_eth2_slot_on_eth_chain: u64 = match self.beacon_rpc_client.get_last_slot_number() {
    Ok(slot) => slot.as_u64(), // head, not finalised checkpoint
    // ...
};
```

**Example 3: No pruning for stale unfinalised headers** [Approx Vulnerability : MEDIUM]
```text
// ❌ VULNERABLE: unfinalized_headers has no clean-up entry point for non-canonical
// entries; unregister_submitter() requires zero pending submissions, so a relayer
// that ever submitted a re-orged block can never recover its storage deposit
```

### Impact Analysis

#### Technical Impact
- Eth2→NEAR bridge liveness halt (single-relayer deployments)
- Irreversible contract state bloat on NEAR
- Stranded storage deposits for relayers

#### Business Impact
- Bridge outages block all ETH→NEAR transfers and Rainbow Bridge-dependent flows (Aurora)

#### Affected Scenarios
- Any beacon chain re-org / late block during routine relayer operation
- Compounded by low relayer count (centralisation noted as RBE2-18)

### Secure Implementation

**Fix 1: Handle skipped slots and submit only finalised headers (applied upstream)**
```rust
// ✅ SECURE: search logic accounts for skipped slots (PRs #800, #832);
// configurable submit_only_finalized_blocks makes last_eth2_slot_on_eth_chain
// the last FINALISED slot, keeping quota consumption deterministic (commit 2198169)
let last_eth2_slot_on_eth_chain = if self.config.submit_only_finalized_blocks {
    self.beacon_rpc_client.get_last_finalized_slot()?
} else { /* legacy path */ };
```

**Fix 2: Prune stale headers**
```text
// ✅ SECURE: expose an API to remove unfinalized_headers entries whose block
// number is below the current finalised block, and allow unregister_submitter()
// once pending stale entries are cleared
```

### Detection Patterns

#### High-Signal Grep Seeds
```
- unfinalized_headers
- get_last_slot
- block_known_on_near
- max_submitted_blocks_by_account
- unregister_submitter
- submit_only_finalized_blocks
```

#### Code Patterns to Look For
```
- Light-client contracts storing attested/unfinalised consensus data without a pruning path
- Off-chain relayers propagating `?` errors from RPC queries for slots that may be re-orged
- Storage-deposit refund gated on "zero pending entries" with no way to clear stale entries
- Quota accounting that never refunds re-orged submissions
```

#### Audit Checklist
- [ ] Can every header/slot accepted by the on-chain client later become non-canonical? If yes, is there a pruning/removal path?
- [ ] Do relayer error paths distinguish "slot re-orged/skipped" from fatal errors?
- [ ] Does submission quota survive worst-case re-org rates?
- [ ] Is `unregister`/deposit-recovery blocked by state the operator cannot clear?

### Real-World Examples

#### Related Reports
- Sigma Prime, Aurora Rainbow Bridge Eth2 Client v2.2 (June 2023): RBE2-01 (High, resolved), RBE2-02 (Medium, resolved), RBE2-03 (Medium, closed — team relied on controlling relayers and cheap storage)

### Keywords for Search

`near`, `aurora`, `rainbow bridge`, `eth2 client`, `light client`, `beacon chain`, `skipped slot`, `reorg`, `unfinalized_headers`, `relayer stall`, `submission quota`, `storage deposit`, `state growth`, `bridge dos`, `finality gap`, `bls signature verification`

### Related Vulnerabilities

- DB/unique/l1-misc/avalanche-warp-messaging-replay.md (cross-chain message trust assumptions)
- DB/bridge/ entries on light-client finality handling
