---
vulnerability_class: gossipsub_malformed_message
title: "Gossipsub Malformed Messages: zero topic weight disables peer penalties (nimbus-eth2)"
protocol: eth-l1-clients
category: P2P Networking / PubSub
vulnerability_type: peer_scoring_misconfiguration
attack_type: penalty_bypass|invalid_message_spam|resource_exhaustion
affected_component: gossipsub_topic_params|peer_scoring|invalid_message_handling
chain: ethereum
severity: low
impact: wasted_compute_bandwidth|degraded_attestation_flow|node_desync
severity_range: "LOW to MEDIUM"
source: Immunefi Ethereum Protocol Attackathon 2024-2025

primitives:
  - topic_weight_zero_invalid_messages_unpenalized
  - malformed_snappy_ssz_gossip_survives_scoring
  - waste_compute_deserializing_undecodable_messages

affected_components:
  - gossipsub topic params (topic_params.nim)
  - libp2p peer scoring (scoring.nim)
  - beacon block/attestation gossip pipelines

tags:
  - gossipsub
  - libp2p
  - peer_scoring
  - nimbus
  - spam
  - dos
  - attackathon

total_reports_analyzed: 1 (+1 related)

# Pattern Identity (Required)
root_cause_family: scoring_misconfiguration_zero_default_weight
pattern_key: gossipsub_penalty_bypass | zero_topic_weight_invalid_message | spam_enabler

# Interaction Scope
interaction_scope: network_facing_pubsub

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - basicParams
  - TopicParam.init
  - topic_weight
  - invalidMessageDeliveries
  - penalties
  - scoring.nim
  - gossipsub
  - validate
---

# Gossipsub Malformed Message Spam (zero-weight topic penalty bypass)

## Overview

libp2p gossipsub peer scoring is the only backpressure against peers that flood invalid messages:
a peer's score is decremented by `topicWeight × invalidMessageDeliveries`. In nimbus-eth2, most
topic subscriptions are configured via `basicParams` → `TopicParam.init`, which **defaults the
topic weight to zero**. The product of zero weight and any number of invalid messages is zero —
so a malicious peer can gossip corrupted snappy data or non-SSZ garbage on those topics forever,
never accrue a penalty, and never get disconnected/banned by the score system.

**Root Cause Statement**: This vulnerability exists because gossipsub topic parameters are
initialized with a zero default topic weight, making the invalid-message penalty term identically
zero for all topics except `AggregateAndProofsTopic` and `BeaconBlocksTopic` — so malformed-message
spam is free for the attacker.

**Observed Frequency**: 1 accepted Attackathon report (config-class bug, likely present in any
fork/default-config audit of gossipsub clients)
**Consensus Severity**: LOW (DoS/degradation), MEDIUM when combined with a decode-cost amplifier

---

#### Agent Quick View

- Root cause statement: "This vulnerability exists because of scoring_misconfiguration_zero_default_weight (gossipsub topic weight = 0)"
- Pattern key: `gossipsub_penalty_bypass | zero_topic_weight_invalid_message | spam_enabler`
- Interaction scope: `network_facing_pubsub`
- Primary affected component(s): `gossipsub_topic_params`, `peer_scoring`
- High-signal code keywords: `basicParams`, `TopicParam.init`, `topic_weight`, `invalidMessageDeliveries`
- Typical sink / impact: `wasted_compute_bandwidth` / degraded chain-following ability
- Validation strength: `high` (code-line citations in nim-libp2p scoring.nim L75-77, L209-216)

#### Contract / Boundary Map

- Entry surface(s): all gossipsub topic subscriptions using `basicParams`
- Contract hop(s): `peer message -> topic validation fails -> scoring penalty(=0) -> peer stays`
- Trust boundary crossed: `unauthenticated gossip peer`
- Shared state or sync assumption: `peer scoring deters invalid-message flooding`

#### Valid Bug Signals

- Signal 1: `TopicParam.init` / equivalent constructor called without explicit topic weight for a validated topic
- Signal 2: Peer score does not decrease after sending N invalid messages on affected topic (observable in metrics/behavior)
- Signal 3: `invalidMessageDeliveries` increment exists but its penalty term multiplies by topic weight 0

#### False Positive Guards

- Not this bug when: topic explicitly sets positive weight (AggregateAndProofs, BeaconBlocks in nimbus are exempt)
- Safe if: global peer-score penalties (not topic-scoped) still trigger disconnect/ban on invalid messages
- Requires attacker control of: gossipsub peer connection only
- Correlated-but-distinct: snappy CRC bypass (#37246) enables *silent* corruption; this finding is about *cost-free spam* even when validation correctly rejects

## Real Report

### Immunefi #38318 [BC-Low] — nimbus-eth2: Gossipsub misconfiguration allows malicious peers gossip malformed data without penalization (alpharush)

Report: `reports/eth-l1-clients_findings/38318-bc-low-nimbus-eth2-gossipsub-misconfiguration-allows-malicious-peers-gossip-malformed-data-wit.md`

Evidence lines (from report):
- `beacon_chain/networking/topic_params.nim#L58` — `basicParams` uses `TopicParam.init` (zero weight default)
- `nim-libp2p gossipsub/scoring.nim#L75-L77` and `#L209-L216` — penalty = topicWeight × invalid count
- All topic subscriptions except `AggregateAndProofsTopic` / `BeaconBlocksTopic` affected

Impact: node wastes compute+bandwidth deserializing undecodable data; ability to follow the
network/beacon chain degrades while the spammer is never penalized.

### Related reports (compounding)

- `#37246` Lodestar snappy checksum skip → see `DB/eth-l1-clients/p2p/snappy-decompression-DoS.md`
- `#38146` [BC-Medium] Nimbus-eth2 remote crash via incorrect protobuf parsing — `reports/eth-l1-clients_findings/38146-bc-medium-nimbus-eth2-remote-crash.md` (malformed-message handling reaching a crash, shows gossip-adjacent decode paths can be fatal, not just costly)
- `#38733` [BC-Medium] Nimbus eth2 remote crash — `reports/eth-l1-clients_findings/38733-bc-medium-nibmus-eth2-remote-crash.md`

## Vulnerable Code Pattern (generic)

```nim
# VULNERABLE: default zero weight => invalid-message penalty always 0
proc basicParams(topic: string): TopicParam =
  TopicParam.init(topic)   # topicWeight defaults to 0.0

# scoring.nim: penalty = topicWeight * invalidDeliveries == 0 * N == 0
```

## Detection & Hunt Strategy

1. Grep every gossipsub topic registration in the client for default-initialized `TopicParam` /
   topic-weight arguments; list topics with weight == 0 that also have message validation.
2. Verify the peer-score disconnect threshold can actually be reached via invalid messages on
   each topic (unit test: send N invalid, assert score drop).
3. Audit global (topic-independent) penalties — e.g., `invalidMessageDeliveries` behavior when
   app-specific scoring is disabled.
4. For each CL client (lighthouse, prysm, teku, lodestar, grandine), compare topic-weight matrices
   against the libp2p pubsub scoring spec recommendations.

## References

- `reports/eth-l1-clients_findings/38318-bc-low-nimbus-eth2-gossipsub-misconfiguration-allows-malicious-peers-gossip-malformed-data-wit.md`
- `reports/eth-l1-clients_findings/38146-bc-medium-nimbus-eth2-remote-crash.md`
- `reports/eth-l1-clients_findings/38733-bc-medium-nibmus-eth2-remote-crash.md`
- libp2p pubsub peer-scoring spec (topic scoring parameters)
- Immunefi/audit `37351` [BC-Insight] (erigon, INFO): Resubscribe deadlocks when unsubscribing within an unblock channel — `reports/eth-l1-clients_findings/37351-bc-insight-resubscribe-deadlocks-when-unsubscribing-within-an-unblock-channel.md` (Immunefi (CertiK))
