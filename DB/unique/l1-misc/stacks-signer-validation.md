---
# Core Classification
protocol: stacks
chain: stacks
category: access_control
vulnerability_type: replay_and_status_confusion

# Pattern Identity
root_cause_family: missing_validation
pattern_key: missing_nonce_and_status_check | signer_vote_processing | vote_replay | signer_set_corruption

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - Stacks Signer (sBTC signer set, Rust)
  - Stacks chain signer vote aggregation
  - Reward/acknowledgment accounting for signers
path_keys:
  - missing_nonce_and_status_check | vote processing | signer vote | replay
  - status_confusion | acknowledgment flow | signer registry | incorrect rewards

# Attack Vector Details
attack_type: logical_error
affected_component: signer_message_validation

# Technical Primitives
primitives:
  - signer votes (approve/reject)
  - nonce-based replay prevention
  - acknowledgment (ack) status machine
  - signer rotation / signer set updates
  - reward distribution to signers
  - DKG shares

# Grep / Hunt-Card Seeds
code_keywords:
  - signer_vote
  - approve/reject vote
  - nonce
  - acknowledgment
  - acknowledged status
  - signer set
  - rotate_keys
  - reward

# Impact Classification
severity: critical
impact: replay_and_reward_corruption
exploitability: 0.5
financial_impact: high

# Context Tags
tags:
  - l1
  - rust
  - sbtc
  - signer
  - threshold signatures
  - replay

# Version Info
language: rust
version: "Stacks Signer V202411 (Coinfabrik audit, April 2025)"
---

## References & Source Reports

> Reference file verified to exist under `reports/other-l1_findings/`. Bucket also contains a second Stacks audit (stacks sibyl/chainstate, see raw index) — Stacks chosen as the "remaining chain bucket" entry.

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [STX1] | reports/other-l1_findings/audits-stacks-coinfabrik-stacks-signer-audit-2025-04-pdf.md | CRITICAL-class bucket (4 critical, 4 high, 6 medium per report ToC) | Coinfabrik | Coinfabrik Stacks-Signer audit, April 2025, V202411, commit c1a1f50fddcbc11054fae537103423e21221665a (severity counts + HI-01 title verified from report ToC) |
| [STX2] | reports/stacks-l1_findings/audits-stacks-coinfabrik-stacks-libsigner-audit-2025-04-pdf.md | (bucket) | Coinfabrik | Coinfabrik Stacks libsigner audit, April 2025 (signer scope; replacement for the sibyl/chainstate bucket note) |

## Stacks Signer Vote Replay and Status Confusion

### Overview

Coinfabrik's April 2025 audit of the Stacks Signer (the sBTC threshold-signing layer) reported 4 critical, 4 high, and 6 medium issues; the headline high-severity finding is **HI-01: Replay Attack on Vote** — signer votes lack adequate nonce/freshness binding, so a captured vote can be replayed. The surrounding pattern is **status and acknowledgment confusion** in the signer registry (incorrect/acknowledged status handling around rotation and rewards, per the index keyword set: acknowledged, incorrect, insecure, reward, status).

#### Agent Quick View

- Root cause statement: "This vulnerability exists because signer votes and acknowledgment state transitions are processed without a fresh, per-message nonce/identity check, allowing replayed or mis-statused votes to corrupt signer-set decisions and reward accounting."
- Pattern key: `missing_nonce_and_status_check | signer_vote_processing | vote_replay | signer_set_corruption`
- Interaction scope: `multi_contract` (signer clients ↔ Stacks chain aggregation ↔ reward accounting)
- Primary affected component(s): `signer vote processing, acknowledgment state machine, signer rotation, reward distribution`
- Contracts / modules involved: `Stacks Signer (rust), sBTC signer set coordination, reward/ack registry`
- Path keys: `missing_nonce_and_status_check | vote processing | signer vote | replay` · `status_confusion | acknowledgment flow | signer registry | incorrect rewards`
- High-signal code keywords: `signer_vote, nonce, acknowledgment, acknowledged status, signer set, rotate_keys, reward`
- Typical sink / impact: `replayed votes skewing threshold decisions; wrong signer set; incorrect reward distribution`
- Validation strength: `moderate` (severity counts and HI-01 title verified verbatim from report ToC; full finding bodies not extracted)

#### Contract / Boundary Map

- Entry surface(s): signer vote submission (approve/reject), acknowledgment messages, key-rotation events from the chain
- Contract hop(s): `Signer client -> Stacks chain vote aggregation -> signer set update -> reward accounting`
- Trust boundary crossed: `p2p signer messages + chain-event-driven state machine — votes must be bound to a unique (signer, message, round/nonce)`
- Shared state or sync assumption: `every signer's view of (current signer set, acknowledged status, reward ledger) must converge after each rotation`

#### Valid Bug Signals

- Signal 1: A vote message can be re-submitted and counted twice — no consumed-nonce/round check at the aggregation point (HI-01 class).
- Signal 2: Acknowledgment transitions accept out-of-order or duplicate acks, leaving status `acknowledged`/`pending` inconsistent across signers.
- Signal 3: Reward accounting reads signer status at the wrong time (pre-rotation vs post-rotation), paying wrong parties.
- Signal 4: The 4 critical issues (per ToC count) concentrate in signer-set integrity — treat any unvalidated signer-set update as same-family.

#### False Positive Guards

- Not this bug when: votes carry a strictly-increasing per-signer nonce consumed atomically at aggregation.
- Not this bug when: ack transitions are idempotent and ordered (round-checked).
- Safe if: reward snapshots bind to an immutable signer-set version hash.
- Requires attacker control of: signer p2p traffic capture/replay (HI-01), or timing around rotation events (status/reward variants).
- Impact requires threshold relevance: a single replayed vote matters only if it flips or blocks a threshold decision.

### Vulnerability Description

#### Root Cause

1. **Missing nonce/freshness on votes** (HI-01): votes are not bound to a unique consumed nonce per (signer, message, round), enabling replay.
2. **Ack/status machine gaps**: acknowledgment handling permits duplicate or out-of-order processing, desynchronizing signer status.
3. **Rotation-time consistency**: signer-set updates and reward reads race, yielding incorrect rewards / insecure states (index-verified keyword cluster: incorrect, insecure, reward, status, acknowledged).

#### Attack Scenario / Path Variants

**Path A: Vote replay**
Path key: `missing_nonce_and_status_check | vote processing | signer vote | replay`
Entry surface: signer vote submission
Contracts touched: `Signer client -> chain vote aggregation`
Boundary crossed: `p2p signer message`
1. Attacker captures a signed approve/reject vote for message M in round R.
2. After the round concludes (or during), the vote is re-submitted.
3. Aggregation counts it again — no consumed nonce.
4. Threshold accounting skews: a rejected decision can pass (or vice versa); signer-set or sBTC operation integrity breaks.

**Path B: Ack status confusion at rotation**
Path key: `status_confusion | acknowledgment flow | signer registry | incorrect rewards`
Entry surface: acknowledgment processing / rotate_keys event
1. Rotation event arrives while acks from the previous set are in flight.
2. Duplicate/out-of-order acks accepted; registry flips to `acknowledged` prematurely or stays stale.
3. Reward accounting reads the wrong set version.
4. Incorrect rewards paid; in the worst case an insecure signer set is treated as valid.

#### Vulnerable Pattern Examples

> Reconstructed from verified ToC facts (4 critical / 4 high / 6 medium; HI-01 "Replay Attack on Vote") and the audited keyword cluster; Rust pseudocode.

**Example 1: Vote without consumed nonce** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: replayable signer vote ([STX1] HI-01 class)
fn handle_vote(&mut self, v: SignedVote) {
    // no check that (v.signer, v.msg_id, v.round) nonce is fresh/consumed
    self.votes[v.msg_id].push(v);          // same vote counts twice on replay
}
```

**Example 2: Non-idempotent acknowledgment transition** [Approx Vulnerability : MEDIUM]
```rust
// ❌ VULNERABLE: duplicate/out-of-order ack corrupts status
fn handle_ack(&mut self, ack: Ack) {
    self.status[ack.signer] = Status::Acknowledged;  // no round/ordering check;
    self.rewards.credit(ack.signer, self.current_set_reward()); // wrong set version possible
}
```

**Example 3: Reward read racing rotation** [Approx Vulnerability : MEDIUM]
```rust
// ❌ VULNERABLE: snapshot after rotation uses new set for old round
fn payout(&self, round: Round) {
    let set = self.current_signer_set();   // post-rotation set
    for s in set { self.rewards.credit(s, round.reward); } // old-round signers unpaid
}
```

### Impact Analysis

#### Technical Impact
- Replayed votes flip or block threshold decisions (signer-set updates, sBTC operations)
- Status desync across signers halts coordination liveness
- Reward misallocation to wrong/non-signers

#### Business Impact
- sBTC (Bitcoin bridge on Stacks) depends on signer-set integrity — replay-class criticals here are bridge-trust criticals
- Reward corruption erodes signer participation incentives

#### Affected Scenarios
- Key rotation windows (highest confusion risk)
- Network partitions healing (delayed vote/ack delivery = natural replay carrier)
- Any aggregator change that touches vote storage without nonce bookkeeping

### Secure Implementation

**Fix 1: Consumed nonces, idempotent acks, versioned reward snapshots**
```rust
// ✅ SECURE: replay-proof vote, ordered ack, immutable reward binding
fn handle_vote(&mut self, v: SignedVote) -> Result<(), Error> {
    let key = (v.signer, v.msg_id, v.round);
    if !self.consumed_nonces.insert(key) {      // atomic consume-once
        return Err(Error::ReplayedVote);
    }
    self.votes[v.msg_id].insert(v.signer, v);   // set semantics: one vote per signer
    Ok(())
}
fn handle_ack(&mut self, ack: Ack) -> Result<(), Error> {
    if ack.round != self.current_round { return Err(Error::StaleAck); }  // ordering
    self.status[ack.signer] = Status::Acknowledged;                      // idempotent
    Ok(())
}
fn payout(&self, round: Round) {
    let set = self.signer_set_at(round.set_version_hash);  // immutable snapshot
    for s in set { self.rewards.credit(s, round.reward_split(s)); }
}
```

### Detection Patterns

#### High-Signal Grep Seeds
```
- signer_vote
- nonce
- acknowledgment
- acknowledged
- rotate_keys
- signer set
- reward
```

#### Code Patterns to Look For
```
- vote vectors keyed by message only (not by (signer, round))
- Option/BTreeMap status flips without round comparison
- reward reads from current_set instead of a versioned snapshot
- ack handlers that cannot reject duplicates
```

#### Audit Checklist
- [ ] Is every signer vote bound to a consume-once nonce (signer, msg, round)?
- [ ] Are ack transitions round-ordered and idempotent?
- [ ] Do reward payouts bind to an immutable signer-set version?
- [ ] During rotation, are in-flight votes/acks expired explicitly?

### Real-World Examples

#### Known Exploits
- None cited in [STX1] (acknowledged/fixed status per report keywords).

#### Related CVEs/Reports
- [STX1] Coinfabrik, Stacks Signer audit, April 2025, V202411 (4 critical / 4 high / 6 medium; HI-01 Replay Attack on Vote)
- [STX2] Coinfabrik, Stacks sibyl audit, Feb 2025 (stackslib chainstate, bitcoin signers)

### Keywords for Search

`stacks`, `stacks signer`, `sbtc`, `signer set`, `vote replay`, `nonce`, `replay attack`, `acknowledgment`, `status confusion`, `key rotation`, `rotate keys`, `threshold signature`, `reward distribution`, `rust`, `coinfabrik`, `signer coordination`, `DKG`

### Related Vulnerabilities

- DB/unique/l1-misc/polygon-bor-heimdall-validation.md (validator-set change integrity at consensus boundary)
- DB/unique/l1-misc/near-aurora-rainbow-bridge-light-client.md (signature/replay validation on bridge messages)
