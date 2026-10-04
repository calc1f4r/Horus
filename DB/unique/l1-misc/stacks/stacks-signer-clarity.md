---
# Core Classification
protocol: generic
chain: stacks
category: stacks
vulnerability_type: stacks_signer_stx
root_cause_family: see pattern_key

# Pattern Identity
pattern_key: stacks-signer-stx | stacks signer stx | varies by finding | see references

# Interaction Scope
interaction_scope: varies
involved_contracts:
  - stacks signer stx

# Attack Vector Details
attack_type: varies
affected_component: stacks signer stx

# Technical Primitives
primitives:
  - accepted
  - advance
  - allows
  - attack
  - attackers
  - badprivateshares

# Grep / Hunt-Card Seeds
code_keywords:
  - accepted
  - advance
  - allows
  - attack
  - attackers
  - badprivateshares
  - batches
  - being

severity: critical
impact: varies
language: varies
tags:
  - stacks
  - l1
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [s1] | reports/stacks-l1_findings/37470-bc-medium-sbtc-signers-do-not-page-through-pending-deposit-requests-making-it-trivially-easy-t.md | MEDIUM | Immunefi (throwing5tone7) | #37470 \[BC-Medium] SBTC Signers do not page through pending deposit requests making it trivially eas |
| [s2] | reports/stacks-l1_findings/37811-bc-high-missing-length-check-when-parsing-signaturesharerequest-in-the-signers-allows-the-coor.md | HIGH | Immunefi (n4nika) | #37811 \[BC-High] Missing length check when parsing \`SignatureShareRequest\` in the signers allows the |
| [s3] | reports/stacks-l1_findings/37861-bc-critical-sbtc-signer-wsts-implementation-allows-nonce-replays-such-that-a-malicious-signer.md | CRITICAL | Immunefi (throwing5tone7) | #37861 \[BC-Critical] SBTC Signer WSTS implementation allows nonce replays such that a malicious sign |
| [s4] | reports/stacks-l1_findings/38111-bc-high-attackers-can-send-a-very-large-event-in-a-stacks-block-so-that-the-signer-can-never-g.md | HIGH | Immunefi (f4lc0n) | #38111 \[BC-High] Attackers can send a very large event in a Stacks block so that the Signer can neve |
| [s5] | reports/stacks-l1_findings/38133-bc-medium-a-rogue-signer-can-censor-any-deposit-request-from-being-processed-and-fullfilled-on.md | MEDIUM | Immunefi (niroh) | #38133 \[BC-Medium] A rogue Signer can censor any deposit request from being processed and fullfilled |
| [s6] | reports/stacks-l1_findings/38270-bc-medium-a-signer-can-send-a-large-number-of-junk-wstsnetmessage-noncerequest-through-p2p-to.md | MEDIUM | Immunefi (f4lc0n) | #38270 \[BC-Medium] A signer can send a large number of junk \`WstsNetMessage::NonceRequest\` through P |
| [s7] | reports/stacks-l1_findings/38551-bc-medium-a-signer-can-request-stacks-tx-nonces-in-batches-in-advance-and-then-dos-other-signe.md | MEDIUM | Immunefi (f4lc0n) | #38551 \[BC-Medium] A signer can request stacks tx nonces in batches in advance and then DoS other si |
| [s8] | reports/stacks-l1_findings/40655-bc-medium-malicious-signers-can-give-different-votes-to-other-signers-to-prevent-sbtc-withdraw.md | MEDIUM | Immunefi (f4lc0n) | #40655 \[BC-Medium] Malicious signers can give different votes to other Signers to prevent sBTC withdrawal |
| [s9] | reports/stacks-l1_findings/40731-bc-medium-a-malicious-signer-can-force-a-panic-in-the-coordinator-by-sending-dkgfailure-badpri.md | MEDIUM | Immunefi (christ0s) | #40731 \[BC-Medium] A malicious signer can force a panic in the coordinator by sending \`DkgFailure::BadPrivateShares\` with an invalid signer ID |
| [s10] | reports/stacks-l1_findings/41111-bc-medium-a-malicious-signer-could-manipulate-withdrawal-decisions-preventing-accepted-and-rej.md | MEDIUM | Immunefi (ZoA) | #41111 \[BC-Medium] A malicious signer could manipulate withdrawal decisions preventing accepted and rejected withdrawals from getting confirmed on St |
| [s11] | reports/stacks-l1_findings/42404-bc-medium-a-signer-can-oom-kill-other-signers-during-dkg-verification.md | MEDIUM | Immunefi (Blobism) | #42404 \[BC-Medium] A signer can OOM kill other signers during DKG verification |
| [s12] | reports/stacks-l1_findings/42752-bc-high-signer-can-be-dosed-through-their-libp2p-component.md | HIGH | Immunefi (leadwiz) | #42752 \[BC-High] Signer can be DOSed through their libp2p component |
| [s13] | reports/stacks-l1_findings/42773-bc-medium-signers-can-be-compromised-by-a-libp2p-dos-attack.md | MEDIUM | Immunefi (Pig46940) | #42773 \[BC-Medium] Signers can be compromised by a libp2p DoS attack |
| [s14] | reports/stacks-l1_findings/37384-bc-medium-attacker-can-front-run-call-to-emily-api-with-incorrect-data-preventing-legit-user-f.md | MEDIUM | Immunefi (n4nika) | #37384 \[BC-Medium] Attacker can front-run call to emily api with incorrect data  preventing legit us |
| [s15] | reports/stacks-l1_findings/38740-bc-high-the-missing-check-in-deposits-depositscriptinputs-parse-permits-losing-funds-by-sendin.md | HIGH | Immunefi (jovemjeune) | #38740 \[BC-High] The missing check in Deposits::DepositScriptInputs::parse() permits losing funds by |
| [q16] | reports/stacks-l1_findings/37530-bc-insight-deposits-can-be-completely-dosed-due-to-incorrect-transaction-construction.md | INFO | Immunefi (n4nika) | #37530 \[BC-Insight] Deposits can be completely DoSed due to incorrect transaction construction |
| [q17] | reports/stacks-l1_findings/38028-bc-low-there-is-a-partial-network-degradation-due-to-dynamodb-gsi-throttling-under-high-traffi.md | LOW | Immunefi (XDZIBECX) | #38028 \[BC-Low] There is a Partial Network Degradation Due to DynamoDB GSI Throttling Under High Tra |
| [q18] | reports/stacks-l1_findings/38030-bc-insight-coordinator-can-be-crashed-by-signers-on-dkg.md | INFO | Immunefi (n4nika) | #38030 \[BC-Insight] Coordinator can be crashed by signers on DKG |
| [q19] | reports/stacks-l1_findings/38223-bc-insight-attackers-can-disrupt-the-tag-order-of-gossip-messages-to-bypass-signature-verifica.md | INFO | Immunefi (f4lc0n) | #38223 \[BC-Insight] Attackers can disrupt the tag order of gossip messages to bypass signature verif |
| [q20] | reports/stacks-l1_findings/38460-bc-low-the-coordinator-can-set-a-higher-btc-tx-fee-than-the-current-network-to-make-users-to-p.md | LOW | Immunefi (f4lc0n) | #38460 \[BC-Low] The coordinator can set a higher BTC tx fee than the current network to make users t |
| [q21] | reports/stacks-l1_findings/38671-bc-insight-signer-key-rotation-is-not-possible-due-to-deadlock-between-submitting-key-rotation.md | INFO | Immunefi (n4nika) | #38671 \[BC-Insight] Signer key rotation is not possible due to deadlock between submitting key rotat |
| [q22] | reports/stacks-l1_findings/38690-bc-insight-a-malicious-coordinator-can-run-multiple-dkg-coordination-in-parallel-and-manipulat.md | INFO | Immunefi (ZoA) | #38690 \[BC-Insight] A malicious coordinator can run multiple DKG coordination in parallel and manipu |
| [q23] | reports/stacks-l1_findings/40770-bc-low-unvalidated-withdrawal-events-allow-data-manipulation-and-denial-of-service-in-emily.md | LOW | Immunefi (Cartel) | #40770 \[BC-Low] Unvalidated withdrawal events allow data manipulation and denial of service in Emily |
| [q24] | reports/stacks-l1_findings/41014-bc-low-the-signer-can-submit-multi-tx-first-to-make-the-coordinators-submission-fail.md | LOW | Immunefi (f4lc0n) | #41014 \[BC-Low] The signer can submit multi-tx first to make the coordinator's submission fail |
| [q25] | reports/stacks-l1_findings/41202-bc-insight-a-malicious-signer-can-force-a-failure-of-the-signature-round-by-providing-a-key-id.md | INFO | Immunefi (christ0s) | #41202 \[BC-Insight] A malicious signer can force a failure of the signature round by providing a key ID they don't own |
| [q26] | reports/stacks-l1_findings/41597-bc-insight-emily-server-can-crash-their-connected-stacks-node-when-processing-a-large-number-o.md | INFO | Immunefi (warden) | #41597 \[BC-Insight] Emily server can crash their connected Stacks node when processing a large number of events |
| [q27] | reports/stacks-l1_findings/42750-bc-insight-subtraction-overflow-risk-in-wsts-fire-coordinator.md | INFO | Immunefi (Blobism) | #42750 \[BC-Insight] Subtraction overflow risk in WSTS FIRE coordinator |
| [q28] | reports/stacks-l1_findings/42764-bc-low-a-btc-wallet-on-signer-blocklists-can-cause-network-dos.md | LOW | Immunefi (Blobism) | #42764 \[BC-Low] A BTC wallet on signer blocklists can cause network DoS |

## Stacks Signer Stx

**stacks-signer-stx patterns mined from uncited L1 audit reports** - 13 sec-tier findings (1 critical / 3 high / 9 medium) across 13 files from Immunefi (Blobism), Immunefi (Pig46940), Immunefi (ZoA), Immunefi (christ0s), Immunefi (f4lc0n), Immunefi (leadwiz).

### Overview

Titles in the references table are verbatim from source reports. Route to the exact report file for full PoC detail. Validation strength: `unassessed` (evidence rows only).

### Detection Patterns

#### High-Signal Grep Seeds
```
- accepted
- advance
- allows
- attack
- attackers
- badprivateshares
- batches
- being
```

### Vulnerability Description

#### Root Cause

The cited reports describe stacks signer stx paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `stacks-signer-stx | stacks signer stx | varies by finding | see references`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `stacks-signer-stx | stacks signer stx | varies by finding | see references | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `stacks-signer-stx | stacks signer stx | varies by finding | see references | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: #37861 \[BC-Critical] SBTC Signer WSTS implementation allows nonce replays such that a malicious sign** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// #37861 \[BC-Critical] SBTC Signer WSTS implementation allows nonce replays such that a malicious sign
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: #37861 \[BC-Critical] SBTC Signer WSTS implementation allows nonce replays such that a malicious sig
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: #37811 \[BC-High] Missing length check when parsing \`SignatureShareRequest\` in the signers allows the** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// #37811 \[BC-High] Missing length check when parsing \`SignatureShareRequest\` in the signers allows the
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: #37811 \[BC-High] Missing length check when parsing \`SignatureShareRequest\` in the signers allows 
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: #38111 \[BC-High] Attackers can send a very large event in a Stacks block so that the Signer can neve** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// #38111 \[BC-High] Attackers can send a very large event in a Stacks block so that the Signer can neve
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: #38111 \[BC-High] Attackers can send a very large event in a Stacks block so that the Signer can nev
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

`accepted, advance, allows, attack, attackers, badprivateshares, batches, being, block, censor`

### Related Vulnerabilities

- Sibling entries under the same category folder
