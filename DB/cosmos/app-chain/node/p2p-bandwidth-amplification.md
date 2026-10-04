---
protocol: generic
chain: cosmos
category: node
vulnerability_type: p2p_bandwidth_amplification

# Pattern Identity
root_cause_family: resource_exhaustion
pattern_key: resource_exhaustion | p2p_gossip_amplification | p2p_bandwidth_amplification

# Interaction Scope
interaction_scope: multi_component
involved_contracts:
  - P2P Switch (peer routing)
  - ConsensusReactor (BlockPart / Vote gossip)
  - MempoolReactor (Txs gossip)
  - PeerSet / per-peer send queues
path_keys:
  - unbounded_fanout | BlockPart gossip | N-peer re-send | egress amplification
  - unbounded_mempool_broadcast | Txs message | full-mempool broadcast | ingress flood
  - missing_rate_limit | per-peer send queue | queue bloat | OOM/drop
  - sentry_topology_amplification | multiple nodes per operator | terabyte/day egress

# Attack Vector Details
attack_type: dos|resource_exhaustion
affected_component: p2p_networking|consensus_gossip|mempool_gossip

# Technical Primitives
primitives:
  - gossip_fanout
  - block_part_retransmission
  - mempool_broadcast
  - per_peer_queueing
  - sentry_architecture
  - bandwidth_economics

# Grep / Hunt-Card Seeds
code_keywords:
  - consensus.BlockPart
  - mempool.Txs
  - consensus.Vote
  - MaxNumInboundPeers
  - MaxNumOutboundPeers
  - FlushThrottleTimeout
  - SendQueueCapacity
  - broadcastNewRoundStepMessage
  - gossipDataForCatchup
  - trySendTicker
  - PeerSendQueue
  - SeedMode
  - sentry

# Impact Classification
severity: medium
impact: dos|node_degradation|validator_downtime_slashing
exploitability: 0.7
financial_impact: medium

# Context Tags
tags:
  - cosmos
  - cometbft
  - tendermint
  - p2p
  - networking
  - dos
  - bandwidth
  - node-operators

language: go
version: Tendermint/CometBFT (RFC-027, Nov 2022; applies to current CometBFT)

---

## References & Source Reports

> **For Agents**: If you need detailed information, read the referenced report file.

### Bandwidth Amplification RFC
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| RFC 27: P2P Message Bandwidth Report — BlockPart/Txs/Vote = 98% of bandwidth; Osmosis validator measured 366 GB/day sent, 208 GB/day received | `reports/cosmos-l1-nodes_findings/cometbft-docs-references-rfc-tendermint-core-rfc-027-p2p-message-bandwidth-report-md.md` | DESIGN | CometBFT (williambanfield) |
| Tendermint copy of RFC-027 | `reports/cosmos-l1-nodes_findings/tendermint-docs-rfc-rfc-027-p2p-message-bandwidth-report-md.md` | DESIGN | Tendermint |

---

## P2P Bandwidth Amplification (CometBFT Gossip) [MEDIUM]

### Overview

Tendermint/CometBFT's gossip reactors amplify bandwidth by design: each `consensus.BlockPart`, `mempool.Txs`, and `consensus.Vote` message received from one peer is re-sent to many others; with default peer counts (10–50 inbound/outbound) a single observed Osmosis validator pushed ~366 GB/day egress. RFC-027 quantifies that 3 message types account for 98% of all bandwidth. This is a *design-level* resource-exhaustion surface: peers or transaction submitters can modulate the amplification factor (tx size, block part churn, peer churn) to degrade validators — and validator downtime converts directly into slashing.

#### Agent Quick View

- Root cause statement: "Gossip reactors re-broadcast consensus/mempool messages to all connected peers without global egress budgeting — per-peer send queues and fanout defaults multiply attacker-influenced input into terabyte-scale output, degrading or disconnecting validators."
- Pattern key: `resource_exhaustion | p2p_gossip_amplification | p2p_bandwidth_amplification`
- Interaction scope: `multi_component`
- Primary affected component(s): `p2p switch, consensus reactor (BlockPart/Vote), mempool reactor (Txs), per-peer send queues`
- High-signal code keywords: `consensus.BlockPart`, `mempool.Txs`, `consensus.Vote`, `SendQueueCapacity`, `FlushThrottleTimeout`, `MaxNumInboundPeers`, `gossipDataForCatchup`
- Typical sink / impact: `validator bandwidth exhaustion → missed votes → downtime slashing; node egress cost ($18–44/day on GCP per RFC); peer churn / partition`
- Validation strength: `strong (instrumented production measurements)`

#### Component / Boundary Map

- Entry surface(s): inbound peer connections (unauthenticated until handshake), tx submission (RPC → mempool → gossip), block part requests from catch-up peers
- Component hop(s): `peer A → reactor receive → internal state → per-peer send queues of all other peers (fanout × message size)`; catch-up path: `gossipDataForCatchup` sends stored block parts to lagging peers on demand
- Trust boundary crossed: `any network peer (no stake required) → validator's egress budget`
- Shared state or sync assumption: `send queues are per-peer but CPU/egress NIC is global — no cross-peer budget`

#### Valid Bug Signals

- Signal 1: Per-peer send queue capacity unbounded or set high (`SendQueueCapacity`) with no global egress rate limiter — one slow peer forces queueing for all
- Signal 2: Mempool reactor broadcasts full tx batches to all peers on `Txs` receive (no dedup/sampling) — attacker spams one large tx set, network multiplies it
- Signal 3: Catch-up (`gossipDataForCatchup`) serves arbitrary old block parts with no rate limit — free historical data amplification
- Signal 4: Config defaults unchanged from upstream (peers 50+ inbound) while block size/gas limits were raised by the chain — amplification factor scales with chain params
- Signal 5: Sentry topology (validator + N sentries) multiplies the same gossip stream per operator — RFC's "terabytes per day" scenario

#### False Positive Guards

- Not this bug when: egress is inherently bounded by config (small peer counts, rate-limited NIC) and the chain runs default block sizes — then it is cost, not vulnerability
- Safe if: reactors implement the RFC's suggested mitigations (message coalescing, peer-pair sharding for BlockPart gossip, mempool sampling)
- Requires attacker control of: network peers (cheap) or tx submission (depends on fees) — exploitability high for degradation, low for full halt

### Vulnerable Pattern Examples

**Example 1: Measured amplification baseline** [DESIGN]
> 📖 Reference: `reports/cosmos-l1-nodes_findings/cometbft-docs-references-rfc-tendermint-core-rfc-027-p2p-message-bandwidth-report-md.md`
"Node operators... report that operators running on a network with hundreds of validators consumes multiple terabytes of bandwidth per day... In the nearly three hours of observation, Tendermint sent nearly 42 gigabytes and received about 26 gigabytes... three message types account for 98% of the total bandwidth consumed: consensus.BlockPart, mempool.Txs, consensus.Vote."

**Example 2: Cost/slashing conversion**
> 📖 Reference: same RFC — "$.05 to $.12 per gigabyte [GCP egress]... a single node on Google cloud may cost $18 to $44 a day" — bandwidth exhaustion is a direct path to validator missed-height slashing and operator exit.

### Secure Implementation

```go
// ✅ SECURE: budgeted gossip (RFC-027 mitigation directions)
// 1. Global egress budget shared across per-peer queues:
if sw.TotalEgressRate() > cfg.GlobalEgressBudget { throttleLowPriority(consensusCatchup, mempool) }
// 2. Mempool gossip sampling instead of full broadcast:
peers := sample(sw.Peers(), cfg.MempoolFanoutSample)   // not all peers
// 3. Rate-limit catch-up block part serving per peer:
if peer.CatchupBytesThisWindow() > cfg.CatchupQuota { defer(peer) }
// 4. Alert when egress > baseline: validator health hook
```

### Impact Analysis

- **Frequency**: 1 instrumentation RFC + recurring operator reports
- **Severity Distribution**: DESIGN/MEDIUM (availability + economic)
- **Affected Protocols**: all Tendermint/CometBFT chains; high-block-volume chains (Osmosis-class) worst
- **Validation Strength**: Strong (production Prometheus instrumentation)

**Cross-references**: `dos/gas-resource-exhaustion.md` (on-chain resource exhaustion), `dos/chain-halt-consensus-dos.md`, `node-operator/minipool-node-vulnerabilities.md`.
