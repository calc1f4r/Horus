---
# Core Classification
protocol: sbtc
chain: stacks
category: dos
vulnerability_type: threshold_signing_liveness_sabotage

# Pattern Identity
root_cause_family: unvalidated_peer_input
pattern_key: missing_peer_message_integrity_checks | wsts_signing_rounds | malformed_nonce_or_packet | signing_halt

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - sBTC signer (transaction_coordinator, coordinator_state_machine)
  - wsts library (fire.rs gather_nonces / gather_sig_shares, process_message)
  - transaction_signer (handle_wsts_message, DkgPrivateShares handling)
  - signer request-decider + Emily API deposit storage
path_keys:
  - nonce_without_sig_share | coordinator nonce gathering | wsts threshold lock-in | round timeout loop
  - malformed_packet_abort | wsts process_message | SigShareGather error propagation | all-rounds abort
  - unvalidated_dkg_shares | handle_wsts_message | wsts OOB read | signer crash
  - unbounded_deposit_burst | new_block / request-decider | db + memory exhaustion | signer halt loop

# Attack Vector Details
attack_type: resource_exhaustion
affected_component: sbtc_threshold_signing_liveness

# Technical Primitives
primitives:
  - wsts coordinator state machine (nonce request → sig share request)
  - threshold nonce gathering (nonce_recv_key_ids >= config.threshold)
  - signature share gathering
  - DKG private shares relay
  - libp2p signer p2p mesh
  - Emily API deposit request storage
  - Stacks /new_block event ingestion (axum 2MB body limit)

# Grep / Hunt-Card Seeds
code_keywords:
  - gather_nonces
  - gather_sig_shares
  - nonce_responses
  - signature_shares
  - transaction_coordinator
  - drive_wsts_state_machine
  - DkgPrivateShares
  - request_decider
  - new_block

# Impact Classification
severity: high
impact: total_network_shutdown
exploitability: 0.7
financial_impact: medium

# Context Tags
tags:
  - l1
  - rust
  - sbtc
  - wsts
  - threshold-signatures
  - liveness
  - dos
  - bitcoin-bridge

# Version Info
language: rust
version: "stacks-network/sbtc signer, immunefi_attackaton_0.9 and _1.0 (Stacks Attackathon I & II, Dec 2024 - Mar 2025)"
---

## References & Source Reports

> All paths verified to exist under `reports/stacks-l1_findings/`. Largest high-severity cluster in the Stacks index (8 of 13 highs): a single malicious signer or a cheap unprivileged attacker can halt sBTC signing network-wide.

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [SX1] | reports/stacks-l1_findings/38053-bc-high-a-single-signer-can-continuously-prevent-signatures-from-being-finalized-halting-netwo.md | HIGH | Immunefi (Stacks Attackathon I) | Report #38053, signer, immunefi_attackaton_0.9 |
| [SX2] | reports/stacks-l1_findings/38477-bc-high-a-single-signer-can-abort-every-attempted-signing-round-by-providing-an-invalid-packet.md | HIGH | Immunefi | Report #38477, wsts::process_message error propagation |
| [SX3] | reports/stacks-l1_findings/38516-bc-high-signer-can-censor-transactions-and-halt-the-network-by-providing-an-invalid-nonce-or-t.md | HIGH | Immunefi | Report #38516, wsts::fire::gather_nonces |
| [SX4] | reports/stacks-l1_findings/37814-bc-high-signers-can-crash-other-signers-by-sending-an-invalid-dkgprivateshares-due-to-missing.md | HIGH | Immunefi | Report #37814, DkgPrivateShares OOB crash in wsts |
| [SX5] | reports/stacks-l1_findings/40692-bc-high-calling-multiple-withdrawals-on-a-single-transaction-causes-signers-to-halt-and-the-ne.md | HIGH | Immunefi (Stacks Attackathon II) | Report #40692, request-decider FK violation halt |
| [SX6] | reports/stacks-l1_findings/42747-bc-high-large-btc-transactions-with-many-sbtc-deposits-can-permanently-crash-halt-all-signers.md | HIGH | Immunefi | Report #42747, 1000+ deposits per BTC tx memory exhaustion |

## sBTC Signer Set Liveness Sabotage via wsts Signing-Round Manipulation

### Overview

The sBTC bridge's Bitcoin↔Stacks operations depend on a rotating coordinator driving FROST-style threshold signing rounds (`wsts` library): request nonces → gather nonces → request signature shares → gather shares. Every stage trusts peer messages: nonces are added to the signer set without integrity checks, the first threshold nonce-providers become a hard dependency for sig shares, malformed packets abort rounds through error propagation, and DKG relay messages are forwarded into `wsts` unvalidated. A **single signer** (or, for the deposit-burst paths, any unprivileged Bitcoin/Stacks user) can therefore stall every signing round, crash peer signers with an out-of-bounds read, or wedge the request-decider database — halting deposits, withdrawals, and the whole sBTC network. This is the dominant high-severity cluster of the Stacks attackathon corpus.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the wsts signing pipeline trusts peer-supplied messages (nonces, sig-share packets, DKG shares) without integrity/completeness validation and hard-depends on exactly the signers who provided nonces to also provide signature shares, so one malicious participant — or one oversized public transaction — can block or crash every signing round."
- Pattern key: `missing_peer_message_integrity_checks | wsts_signing_rounds | malformed_nonce_or_packet | signing_halt`
- Interaction scope: `multi_contract` (coordinator state machine ↔ wsts library ↔ transaction_signer ↔ request-decider/Emily storage)
- Primary affected component(s): `wsts gather_nonces/gather_sig_shares, coordinator_state_machine, handle_wsts_message, request_decider`
- Contracts / modules involved: `transaction_coordinator, wsts (fire.rs), transaction_signer, request-decider, Emily API, libp2p mesh`
- Path keys: `nonce_without_sig_share | coordinator nonce gathering | wsts threshold lock-in | round timeout loop` · `malformed_packet_abort | wsts process_message | SigShareGather error propagation | all-rounds abort` · `unvalidated_dkg_shares | handle_wsts_message | wsts OOB read | signer crash` · `unbounded_deposit_burst | new_block / request-decider | db + memory exhaustion | signer halt loop`
- High-signal code keywords: `gather_nonces, gather_sig_shares, nonce_responses, signature_shares, transaction_coordinator, drive_wsts_state_machine, DkgPrivateShares, request_decider, new_block`
- Typical sink / impact: `total network shutdown — no new sBTC mint/burn transactions can be signed; crash loops; permanently stuck bridge operations`
- Validation strength: `strong` (#38053, #38477, #38516, #37814, #40692, #42747 all read with code excerpts, PoCs, and signer logs)

#### Contract / Boundary Map

- Entry surface(s): wsts peer messages (nonce responses, sig shares, DkgPrivateShares), coordinator rotation, public Stacks transactions with many withdrawal calls (#40692), public BTC transactions with 1000+ deposit outputs (#42747), Stacks blocks with >2MB of events hitting `/new_block` (#38111)
- Contract hop(s): `peer signer -> p2p (libp2p) -> transaction_signer.handle_wsts_message -> wsts state machine -> coordinator drive_wsts_state_machine -> aggregate signature`
- Trust boundary crossed: `p2p signer mesh — every message crosses an unauthenticated-trust boundary into threshold-critical state machines; public chain data crosses into signer storage/memory`
- Shared state or sync assumption: `coordinator and signers must converge on the same round state; the nonce-providing subset must equal the sig-share-providing subset for the round to complete`

#### Valid Bug Signals

- Signal 1: Nonce gathering accepts the first threshold of nonce responses "without checking the integrity of the `nonces` vector" (#38516, `wsts::fire.rs::gather_nonces`) — malformed nonces poison the round.
- Signal 2: Once `nonce_info.nonce_recv_key_ids.len() >= self.config.threshold`, the coordinator "is reliant on exactly the signers who provided a nonce to ALSO provide a signature share" (#38053) — withholding one share times out the round, repeatable forever.
- Signal 3: `wsts::process_message` returns `OperationResult::SignError(Coordinator(e))` on `gather_sig_shares` failure (#38477) — a single invalid packet aborts the whole round instead of excluding the offender.
- Signal 4: `handle_wsts_message` relays `DkgPrivateShares` after only a signature check; a `share` with empty `bytes` causes an OOB read in `wsts` and crashes the receiving signer (#37814).
- Signal 5: One Stacks transaction invoking the sBTC withdrawal 500+ times triggers `withdrawal_signers_request_id_block_hash_fkey` FK violations in request-decider — "DOSes the sbtc network 100%" (#40692); a single BTC tx with 1000+ dust deposits consumes GBs of signer memory and crash-loops on restart (#42747).

#### False Positive Guards

- Not this bug when: nonce and sig-share gathering succeed independently at threshold (parallel gather; round completes with any threshold set that provided BOTH) — the #38053 design flaw is then structurally closed.
- Not this bug when: peer packets are fully validated (length, point encoding, share bytes) before entering wsts state, and invalid senders are excluded + slashed rather than aborting the round.
- Safe if: deposit/withdrawal request ingestion is bounded per block/transaction (rate limits, aggregation caps) with graceful degradation.
- Requires attacker control of: one signer seat (Paths A–C) OR merely transaction fees (Paths D/E — no signer role needed).
- Liveness-only: none of these paths steal funds directly (see companion entry for coordinator theft); impact requires sBTC/bridge operations to depend on timely signing, which they do (mints, burns, sweeps).

### Vulnerability Description

#### Root Cause

1. **Threshold lock-in asymmetry** (#38053): the signing round's participant set is fixed by whoever replied to the *nonce* request first; sig-share collection then requires *all* of them, dropping back below threshold if any one withholds.
2. **No peer-message integrity validation** (#38516, #37814, #37811): nonces enter `public_nonces` unchecked; `DkgPrivateShares` are relayed with only a signature check; `SignatureShareRequest` parsing lacks length checks — malformed inputs reach `wsts` internals that panic/OOB.
3. **Error propagation = round abort** (#38477): `wsts::process_message` maps a single peer's `gather_sig_shares` error to a coordinator-level `SignError` that kills the round for everyone.
4. **Unbounded public inputs** (#40692, #42747, #38111): per-txn withdrawal count, per-BTC-tx deposit output count, and per-block event payload size are unbounded; signers persist/process all of them (DB FK violations, GB-scale memory, 2MB axum body limit).

#### Attack Scenario / Path Variants

**Path A: Nonce-then-withhold round stall**
Path key: `nonce_without_sig_share | coordinator nonce gathering | wsts threshold lock-in | round timeout loop`
Entry surface: signer's nonce response
Contracts touched: `transaction_coordinator -> wsts fire.rs`
Boundary crossed: `p2p signer message`
1. Malicious signer `alice` answers the nonce request promptly (always in the first threshold).
2. Coordinator reaches `nonce_recv_key_ids.len() >= threshold` and starts sig-share gathering locked to that set.
3. `alice` never sends her signature share → round times out.
4. Repeat every round ("with a signer set of 15, this absolutely doable on every signature request" — #38053 PoC via `cargo test ... sign_bitcoin_transaction_poc`).

**Path B: Invalid packet aborts every round**
Path key: `malformed_packet_abort | wsts process_message | SigShareGather error propagation | all-rounds abort`
Entry surface: sig-share packet in `State::SigShareGather`
1. Signer sends a packet that fails `gather_sig_shares` (malformed share).
2. `process_message` returns `Some(OperationResult::SignError(Coordinator(e)))`.
3. Coordinator aborts the round entirely rather than excluding the bad signer.
4. Every attempted round dies the same way; no aggregate signature ever forms.

**Path C: DKG crash via unvalidated private shares**
Path key: `unvalidated_dkg_shares | handle_wsts_message | wsts OOB read | signer crash`
Entry surface: `DkgPrivateShares` p2p message
1. Signer sends `DkgPrivateShares` containing a `share` with an empty `bytes` object (passes signature check — key matches).
2. `transaction_signer.rs::handle_wsts_message` relays it into the wsts state machine.
3. OOB read inside `wsts` panics the receiving signer process.
4. Repeated against rotating DKG rounds, signers crash continuously; key generation halts.

**Path D: Withdrawal-call flood wedges request-decider**
Path key: `unbounded_deposit_burst | new_block / request-decider | db + memory exhaustion | signer halt loop`
Entry surface: one public Stacks transaction
1. Attacker deploys a contract that calls the sBTC `initiate-withdrawal` 500+ times in a single transaction (#40692).
2. Signers' request-decider fails on `withdrawal_signers_request_id_block_hash_fkey` FK violation (verified signer log in report).
3. Signers halt; mining of sBTC operations stops — "effectively DOSes the sbtc network 100%".
4. Variant E: one BTC tx with 1,000+ dust-limit deposit outputs eats GBs of signer memory (#42747); crash persists across restarts because pending deposits remain in the Emily API database.

#### Vulnerable Pattern Examples

> Rust pseudocode reconstructed from verified report excerpts.

**Example 1: Nonce-gathered set hard-wires sig-share dependency** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: #38053 — wsts fire.rs gather semantics
if nonce_info.nonce_recv_key_ids.len() >= self.config.threshold {
    // participant set is now FROZEN as exactly these signers...
    self.state = State::SigShareGather(signature_type);
}
// ...and gather_sig_shares waits for EVERY one of them:
for signer in self.nonce_providers {           // ❌ a single withholder times out the round
    if !shares.contains_key(signer) { return Err(Waiting); }
}
```

**Example 2: One bad packet aborts the round for all** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: #38477 — wsts process_message
State::SigShareGather(signature_type) => {
    if let Err(e) = self.gather_sig_shares(packet, signature_type) {
        return Ok((None, Some(OperationResult::SignError(Coordinator(e))))); // ❌ round-wide abort
    }                                                             // instead of excluding sender
}
```

**Example 3: DKG shares relayed into wsts unvalidated** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: #37814 — transaction_signer.rs handle_wsts_message
WstsNetMessage::DkgPrivateShares(dkg_private_shares) => {
    // only the sender's public key / signature is checked...
    if signer_public_key != msg_public_key { return Err(Error::InvalidSignature); }
    self.relay_message(msg.txid, &msg.inner, bitcoin_chain_tip) // ❌ share bytes never length-checked;
    // wsts indexes into share.bytes -> OOB panic on empty payload
}
```

### Impact Analysis

#### Technical Impact
- No aggregate signatures ⇒ no sBTC mint/burn/sweep transactions can be created (all deposits, withdrawals, and bridge operations stop)
- Signer process crashes (OOB) and crash-loops on restart (persistent DB/memory state)
- Coordinator rotation does not help when the flaw is in the shared wsts round design

#### Business Impact
- Immunefi impact class: "Network not being able to confirm new transactions (total network shutdown)" — applies to every report in this cluster
- Bitcoin↔Stacks bridge unavailability freezes user funds in transit; #42747 additionally flags "Permanent freezing of funds (fix requires hardfork)"
- Attack cost is trivial: one signer seat, or plain transaction fees for paths D/E

#### Affected Scenarios
- Any coordinator round while a malicious signer is in the nonce threshold set
- DKG windows (key rotation, signer set changes)
- Public BTC/Stx spam targeting request ingestion (#40692, #42747, #38111)

### Secure Implementation

**Fix 1: Independent threshold gathering + full peer-message validation + bounded ingestion**
```rust
// ✅ SECURE: parallel gather with per-signer exclusion and validated inputs
fn gather(&mut self, msg: ValidatedPeerMsg) -> RoundProgress {
    // 1. validate EVERYTHING before touching wsts internals
    if !msg.well_formed() {                     // ✅ length/encoding checks (#37814, #38516, #37811)
        self.banlist.record(msg.signer_id);     // ✅ exclude & report the sender, not the round
        return RoundProgress::Continue;
    }
    // 2. succeed only when ONE threshold of signers provided BOTH nonce and sig share
    self.nonces.union(msg.nonces);
    self.shares.union(msg.share);
    let ready: HashSet<_> = self.nonces.keys()
        .filter(|s| self.shares.contains_key(s)).collect();   // ✅ independent of arrival order
    if ready.len() >= self.config.threshold {
        return RoundProgress::Aggregate(ready); // ✅ withholding one share just swaps in a spare signer
    }
    RoundProgress::Continue
}
// ingestion bounds (#40692, #42747):
const MAX_WITHDRAWALS_PER_TX: u32 = 16;   // ✅ reject/defer beyond cap at event-processing time
const MAX_DEPOSIT_OUTPUTS_PER_BTC_TX: u32 = 64; // ✅ cap before persisting to Emily/request-decider
```

### Detection Patterns

#### High-Signal Grep Seeds
```
gather_nonces
gather_sig_shares
nonce_responses
signature_shares
drive_wsts_state_machine
DkgPrivateShares
request_decider
new_block
```

#### Code Patterns to Look For
```
- Participant sets frozen at nonce-threshold then required in full for sig shares
- Peer packets (nonces/shares/DKG) entering state machines with signature-only validation
- Any `OperationResult::SignError(Coordinator(_))` returned from single-peer failures
- Unbounded per-transaction loop ingestion (withdrawal/deposit events) into DB or memory
- Process-wide panics reachable from p2p input (indexing, slicing, unwrap) inside wsts calls
```

#### Audit Checklist
- [ ] Can one withholding signer stall rounds indefinitely (nonce set ≠ sig-share set dependency)?
- [ ] Are all p2p message fields length/encoding-validated before wsts state mutation?
- [ ] Does a single malformed packet abort the round, or just exclude the sender?
- [ ] Are per-txn withdrawal calls, per-BTC-tx deposit outputs, and per-block event sizes bounded?
- [ ] Can attacker-supplied persistent state (DB rows, Emily entries) crash signers on restart?

### Real-World Examples

#### Known Exploits
- None public at time of writing; all findings from Stacks Attackathon I/II (Dec 2024 – Mar 2025), triaged by Immunefi.

#### Related CVEs/Reports
- Immunefi #38053, #38477, #38516, #37814 (Attackathon I, sbtc 0.9); #40692, #42747 (Attackathon II, sbtc 1.0)
- Same-family: #37811 (SignatureShareRequest length check), #38111 (>2MB Stacks event block vs axum body limit), #42752 (libp2p component DoS)

### Prevention Guidelines

#### Development Best Practices
1. Never fix a threshold participant set at an earlier protocol stage than its final use; gather both artifacts independently.
2. Treat every p2p message as hostile input: full structural validation before library calls; ban-and-exclude instead of abort-on-error.
3. Bound all public-chain-derived ingestion (events per block, outputs per tx, calls per tx) with explicit caps.

#### Testing Requirements
- Integration: withholder-signer round test (the #38053 PoC pattern: `sign_bitcoin_transaction_poc`)
- Fuzz: all p2p message types with empty/truncated/jumbo fields — no panics
- Load: 1,000-output BTC tx and 500-call withdrawal tx against request-decider/Emily

### Keywords for Search

`stacks`, `sbtc`, `signer`, `wsts`, `threshold signatures`, `FROST`, `nonce`, `gather_nonces`, `gather_sig_shares`, `signature share`, `signing round`, `coordinator`, `liveness`, `network halt`, `DoS`, `DkgPrivateShares`, `DKG`, `out of bounds`, `request decider`, `deposit burst`, `withdrawal flood`, `libp2p`, `bitcoin bridge`, `rust`, `attackathon`, `immunefi`

### Related Vulnerabilities

- DB/unique/l1-misc/stacks/sbtc-coordinator-unvalidated-transaction-drain.md (companion cluster: same trust model, theft sink)
- DB/unique/l1-misc/stacks-signer-validation.md (Coinfabrik-audited signer vote replay / ack status confusion)
