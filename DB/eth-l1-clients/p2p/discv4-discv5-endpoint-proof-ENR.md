---
vulnerability_class: discovery_endpoint_proof_enr_gaps
title: "discv4/discv5 Discovery: endpoint-proof, packet-expiration, and ENR validation gaps"
protocol: eth-l1-clients
category: P2P Networking / Discovery
vulnerability_type: input_validation
attack_type: packet_replay|endpoint_proof_bypass|enr_oversize|neighbor_flood
affected_component: discv4_packets|discv5_messages|enr_records|bonding_state
chain: ethereum
severity: medium
impact: resource_exhaustion|eclipse_facilitation|peer_table_pollution|spec_divergence
severity_range: "LOW to HIGH"
source: Immunefi Ethereum Protocol Attackathon 2024-2025 + Sigma Prime reth 2024 + LatticeFlow discv5 review

primitives:
  - pong_neighbors_expiration_not_checked
  - endpoint_proof_never_refresh_bonding
  - respond_closest_shares_all_neighbours
  - find_node_invalid_endpoint
  - enr_response_max_size_unchecked
  - enr_responses_not_validated
  - udp_spam_dos
  - kdf_index_out_of_bounds

affected_components:
  - discv4 packet handlers (Ping/Pong/FindNode/Neighbors/ENRRequest/ENRResponse)
  - discv5 message handlers (FindNode/Nodes/TalkReq/PING/PONG)
  - node table / k-buckets
  - bonding state machine

tags:
  - discv4
  - discv5
  - discovery
  - enr
  - endpoint_proof
  - besu
  - reth
  - eclipse
  - attackathon

total_reports_analyzed: 8

# Pattern Identity (Required)
root_cause_family: discovery_protocol_validation_gap
pattern_key: discovery_enr_gap | expiration_proof_size_bypass | peer_table_pollution

# Interaction Scope
interaction_scope: network_facing_udp_service

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - expiration
  - Pong
  - Neighbors
  - pingHash
  - bond
  - ENRRequest
  - ENRResponse
  - respond_closest
  - find_node
  - Nodes
  - kbucket
  - maxPacketSize
---

# discv4/discv5 Endpoint-Proof & ENR Validation Gaps

## Overview

Node discovery (discv4 UDP, discv5) is the entry funnel to Ethereum's P2P network. The devp2p spec
uses packet `expiration` timestamps and an endpoint-proof (ping→pong echo-hash) handshake before
nodes exchange neighbours. Repeated audit findings show clients under-enforcing these:

- **Besu accepted expired `Pong`/`Neighbors` packets and never re-bonds** (#38894) — replayed
  packets keep dead/malicious table entries alive; Besu also never initiates re-bonding itself,
  becoming a "bad peer" source for others.
- **reth `respond_closest()` shared ALL neighbours** (RETH-06, High) instead of the bucket-limited
  subset — a single FindNode lets a peer map and eclipse the local table.
- **reth ENR responses not validated** (RETH-42) and **find_node callable with invalid endpoint**
  (RETH-12, Medium) — malformed remote records enter the table.
- **ENR_RESPONSE max size unchecked** (#38902, Low) — oversized ENR records from a peer consume
  unbounded memory/bandwidth.

**Root Cause Statement**: This vulnerability exists because discovery packet handlers skip spec
validation — expiration timestamps, endpoint-proof completion, ENR size limits — or answer FindNode
with the full table instead of the Kademlia-bounded neighbourhood, letting remote attackers replay
packets, pollute peer tables, or map the node for eclipse attacks.

**Observed Frequency**: 8 findings across besu/reth + the dedicated discv5 protocol review.
**Consensus Severity**: LOW to HIGH (RETH-06 table disclosure = High)

---

#### Agent Quick View

- Root cause statement: "This vulnerability exists because of discovery_protocol_validation_gap (expiration/proof/size/table-bounds)"
- Pattern key: `discovery_enr_gap | expiration_proof_size_bypass | peer_table_pollution`
- Interaction scope: `network_facing_udp_service`
- Primary affected component(s): `discv4_packets`, `discv5_messages`
- High-signal code keywords: `expiration`, `respond_closest`, `find_node`, `ENRResponse`, `bond`
- Typical sink / impact: `peer_table_pollution` / `eclipse_facilitation`
- Validation strength: `high`

#### Contract / Boundary Map

- Entry surface(s): UDP discovery port (discv4 30303-udp, discv5)
- Contract hop(s): `packet -> MAC verify -> kind dispatch -> [expiration/proof checks] -> table update / response`
- Trust boundary crossed: `unauthenticated UDP sender` (spoofable pre-proof)
- Shared state or sync assumption: `kbuckets hold only bonded, live endpoints`

#### Valid Bug Signals

- Signal 1: `Pong`/`Neighbors` handler parses `expiration` field but never compares to now
- Signal 2: Endpoint-proof completed once and never re-verified on later FindNode sessions
- Signal 3: FindNode response assembled from all table entries rather than closest-k per bucket
- Signal 4: ENRResponse/ENR record length taken from packet without cap (spec: 300-byte ENR max)
- Signal 5: Remote ENR fields (ip/tcp/udp) not re-validated against observed sender

#### False Positive Guards

- Not this bug when: expiration grace window is spec-permitted and consistent across clients
- Safe if: FindNode requires completed bonding AND response bounded by bucket alpha/k constants
- Requires attacker control of: ability to send UDP to discovery port (no identity needed)
- discv5 encrypts+authenticates handshakes; discv4 findings do not auto-apply — check the stack first

## Real Reports

### 1. Immunefi #38894 [BC-Low] — Missing expiration check for Pong and Neighbors packets and not refreshing the endpoint proof (Franfran, Besu)

Report: `reports/eth-l1-clients_findings/38894-bc-low-missing-expiration-check-for-pong-and-neighbors-packets-and-not-refreshing-the-endpoint.md`

devp2p discv4 spec: "Packets containing a time stamp that lies in the past are expired may not be
processed"; expiration is the only replay protection. Besu ignores it for Pong/Neighbors and never
re-initiates bonding → stale/adversarial peers persist in the table.

### 2. Sigma Prime reth 2024 — RETH-06 (High): respond_closest() Shares All Neighbours

Report: `reports/eth-l1-clients_findings/reth-sigp-2024.md`

A peer sending FindNode received the entire local table (not the Kademlia-limited closest subset),
enabling complete network mapping for eclipse attacks.

### 3. Sigma Prime reth 2024 — RETH-12 (Medium): find_node May Be Called With An Invalid Endpoint; RETH-42 (Info): ENR Responses Are Not Validated

Same report, `reth-sigp-2024.md`.

### 4. Immunefi #38902 [BC-Low] — No check on the maximum size of the encoded ENR on ENR_RESPONSE packet

Report: `reports/eth-l1-clients_findings/38902-bc-low-no-check-on-the-maximum-size-of-the-encoded-enr-on-enr.md`
NOTE: local file is a GitBook 404-stub capture (upstream moved to `...enr_response-packet.md`);
ID/title retained from raw index.

### 5. Supporting: Sigma Prime reth 2024 RETH-27 UDP Spamming DoS (Low), RETH-28 kdf() index-out-of-bounds (Low)

`reports/eth-l1-clients_findings/reth-sigp-2024.md` — UDP-level discovery DoS and crypto-path panics.

### 6. Protocol-level reference: discv5 final review

`reports/eth-l1-clients_findings/eth-node-discovery-la.md` (LatticeFlow/ambire-style final protocol
review PDF-capture, 15pp) — use as the spec ground truth when judging discv5 handler gaps.

## Vulnerable Code Pattern (generic)

```go
// VULNERABLE: expiration parsed but not enforced (besu #38894 pattern)
func handleNeighbors(pkt *NeighborsPacket, from *enode.Node) {
    for _, n := range pkt.Nodes {     // pkt.Expiration never checked vs time.Now()
        table.Add(n)                  // replayed/stale entries accepted
    }
}
```

```rust
// VULNERABLE: full-table disclosure on FindNode (reth RETH-06 pattern)
fn respond_closest(target: NodeId) -> Vec<Node> {
    table.all_entries()               // must be closest_k(target, bucket limits)
}
```

## Detection & Hunt Strategy

1. For each discv4 packet kind, tick the spec checklist: MAC ✓, hash-prev ✓, expiration-enforced?,
   proof-completed-before-Neighbors?
2. Discv5: verify Nodes-message TOTAL_CEILING (udp max ~1280) and node-count caps per response
   batch; oversized/overset responses are the #38902 pattern.
3. Test replay: capture valid Pong/Neighbors, replay after expiry, assert drop.
4. Test table disclosure: from a fresh peer, issue FindNode at distance buckets and count unique
   entries returned; compare against Kademlia k.
5. Check ENR ingress validation: size ≤ 300 bytes, signature over canonical encoding, seq freshness.

## References

- `reports/eth-l1-clients_findings/38894-bc-low-missing-expiration-check-for-pong-and-neighbors-packets-and-not-refreshing-the-endpoint.md`
- `reports/eth-l1-clients_findings/38902-bc-low-no-check-on-the-maximum-size-of-the-encoded-enr-on-enr.md` (404-stub)
- `reports/eth-l1-clients_findings/reth-sigp-2024.md` (RETH-06, RETH-12, RETH-27, RETH-28, RETH-42)
- `reports/eth-l1-clients_findings/eth-node-discovery-la.md`
- devp2p discv4.md (expiration, endpoint proof, known issues), discv5 spec (Nodes message caps)
- Immunefi/audit `37352` [BC-Insight] (erigon, INFO): Missing liveness check in collectTableNodes() — `reports/eth-l1-clients_findings/37352-bc-insight-missing-liveness-check-in-collecttablenodes.md` (Immunefi (CertiK))
