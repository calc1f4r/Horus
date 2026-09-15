---
vulnerability_class: p2p_remote_dos_oom
title: "P2P Remote DoS / OOM: unbounded request serving, handshake floods, rate-limit gaps"
protocol: eth-l1-clients
category: P2P Networking
vulnerability_type: denial_of_service
attack_type: resource_exhaustion|oom_crash|connection_flood|request_amplification
affected_component: p2p_request_handlers|connection_setup|rate_limiting|peer_management
chain: ethereum
severity: high
impact: node_crash|network_partition|resource_exhaustion
severity_range: "LOW to MEDIUM (network-partition scoped HIGH)"
source: Immunefi Ethereum Protocol Attackathon 2024-2025 + Sigma Prime reth 2024

primitives:
  - getblockheaders_large_range_oom
  - getreceiptsmsg_amplification
  - handshake_tcp_flood_no_ip_ratelimit
  - evil_client_fast_crash_via_unthrottled_requests
  - ping_spamming_deskew
  - missing_handshake_timeout_holding_sockets
  - ban_logic_incoming_peer_count_exhaustion
  - pending_peer_subtraction_overflow

affected_components:
  - eth/66-68 request serving loop
  - RLPx / libp2p connection acceptance
  - peer scoring / ban lists
  - pending-peer accounting

tags:
  - p2p
  - dos
  - oom
  - reth
  - nethermind
  - geth
  - besu
  - rate_limiting
  - netsplit
  - attackathon

total_reports_analyzed: 10
client_coverage: "reth, nethermind, geth, besu, erigon (Caplin), teku"

# Pattern Identity (Required)
root_cause_family: unbounded_remote_work_without_rate_limit
pattern_key: p2p_remote_dos | request_serving_handshake_flood_oom | node_crash_network_partition

# Interaction Scope
interaction_scope: network_facing_service

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - GetBlockHeaders
  - GetReceiptsMsg
  - handle_request
  - serve_
  - dial / handshake
  - Handshake
  - ping
  - ratelimit
  - incoming_peers
  - ban
  - pending_peers
  - max_peers
  - Buffer
  - spawn
---

# P2P Remote DoS / OOM (request amplification + connection floods)

## Overview

A consensus client's P2P layer must serve honest peer requests while surviving hostile peers.
Repeatedly confirmed weaknesses: (1) serving unbounded-size responses to a single request
(GetBlockHeaders with a huge range, GetReceiptsMsg over many blocks), (2) accepting handshakes /
connections with no per-IP rate limit, so a trivial script OOMs the process, (3) accounting bugs in
peer/ban counters that let one attacker permanently block new inbound peers, and (4) missing
timeouts letting half-open handshakes pin sockets. All are remote, unauthenticated, cheap to run,
and if scaled by a botnet remove an entire client implementation from the network (netsplit).

**Root Cause Statement**: This vulnerability exists because P2P request handlers and connection
setup perform allocation / work proportional to attacker-controlled parameters (block ranges,
receipt counts, connection rates) with no per-request cap, per-IP rate limit, or correct peer
accounting — allowing a single lightweight machine to OOM-crash or wedge remote nodes.

**Observed Frequency**: Very common — 10 accepted Attackathon + audit findings across all major EL
clients (2024-25).
**Consensus Severity**: LOW to MEDIUM per-report (Immunefi DoS caps), network-wide netsplit impact HIGH

---

#### Agent Quick View

- Root cause statement: "This vulnerability exists because of unbounded_remote_work_without_rate_limit (GetBlockHeaders/GetReceipts/handshake flood)"
- Pattern key: `p2p_remote_dos | request_serving_handshake_flood_oom | node_crash_network_partition`
- Interaction scope: `network_facing_service`
- Primary affected component(s): `p2p_request_handlers`, `connection_setup`
- High-signal code keywords: `GetBlockHeaders`, `GetReceiptsMsg`, `handshake`, `ratelimit`, `incoming_peers`
- Typical sink / impact: `node_crash` / `network_partition`
- Validation strength: `high` (multiple reports include working crash scripts + video PoCs)

#### Contract / Boundary Map

- Entry surface(s): TCP 30303 (RLPx), libp2p ports, discovery UDP
- Contract hop(s): `accept -> handshake -> decode request -> allocate response -> serialize`
- Trust boundary crossed: `unauthenticated remote peer`
- Shared state or sync assumption: `peer tables / rate limits assume honest connection churn`

#### Valid Bug Signals

- Signal 1: Request handler allocates from a header field without clamping (e.g., `limit` or `count` beyond max-headers)
- Signal 2: Connection accept path has no per-IP/token-bucket limiter (geth enforces 1 handshake/30s/IP; if target doesn't, flag)
- Signal 3: Response assembled fully in memory before send (no streaming, no size cap)
- Signal 4: Peer counter decremented on disconnect can underflow (`checked_sub` panic / permanent negative)
- Signal 5: Handshake await has no timeout, holding a task+socket per half-open connection

#### False Positive Guards

- Not this bug when: request caps match devp2p soft limits and response streaming is bounded (e.g., 1024 headers chunked)
- Safe if: per-IP connection rate limit + global pending-peer cap enforced before handshake crypto
- Requires attacker control of: network reachability to p2p port only — no keys, no stake
- Local-only (IPC/unix socket) request paths are NOT remotely reachable — check bind flags in the PoC

## Vulnerability Categories & Real Reports

### Category 1: GetBlockHeaders Range OOM (reth) [LOW per report, netsplit if scaled]

**Real Report: Immunefi #38850 [BC-Low] — Remote P2P OOM Crash (GetBlockHeaders) / Reth**
Report: `reports/eth-l1-clients_findings/38850-bc-low-remote-p2p-oom-crash-getblockheaders-reth.md`

Reth v1.1.5: a single GetBlockHeaders P2P request for a huge block range makes the victim
allocate the entire response in memory → fast OOM kill, "regardless of server specs". Author
demonstrated remote crash of a sepolia reth+lighthouse stack from one attacking machine.

### Category 2: Evil-Client Fast OOM via Unthrottled Receipts (nethermind) [MEDIUM]

**Real Report: Immunefi #37466 [BC-Medium] — Evil-client OOM crash (fast P2P crash)**
Report: `reports/eth-l1-clients_findings/37466-bc-medium-evil-client-oom-crash-fast-p2p-crash.md`

Nethermind 1.29.1: block-receipts serving is not sufficiently rate-limited; a modified light
client (1000+ line Go "evil client", receipts.go) completes handshakes and peers in, then crashes
any nethermind node in 30–60s. Nethermind's handshake path notably lacks geth's 1-per-30s-per-IP rule.

### Category 3: Handshake TCP/30303 Flood OOM (nethermind) [INSIGHT]

**Real Report: Immunefi #37120 [BC-Insight] — Remote handshake-based TCP/30303 flooding leads to an out-of-memory crash**
Report: `reports/eth-l1-clients_findings/37120-bc-insight-remote-handshake-based-tcp-30303-flooding-leads-to-an-out-of-memory-crash.md`

Multithreaded open/close of blank TCP connections to 30303 (telnet-like, no data) OOMs
nethermind. Same netsplit impact as #37466; requires no protocol-level handshaking at all.

### Category 4: GetReceiptsMsg Abuse Across EL Clients [INSIGHT]

**Real Report: Immunefi #38598 [BC-Insight] — GetReceiptsMsg abuse leads to the DoS and/or crash of every EL client**
Report: `reports/eth-l1-clients_findings/38598-bc-insight-getreceiptsmsg-abuse-leads-to-the-dos-and-or-crash-of-every-el-client-in-the-ethere.md`

>100% CPU/MEM and OOM crashes demonstrated against latest Geth, Nethermind and Besu by abusing
receipts requests. Confirms this is a client-ecosystem class, not a single-vendor bug.

### Category 5: Peer/Ban Accounting Exhaustion (reth) [LOW]

**Real Report: Immunefi #38807 [BC-Low] — DoS any reth node via ban logic exploit**
Report: `reports/eth-l1-clients_findings/38807-bc-low-dos-any-reth-node-via-ban-logic-exploit.md`
Reth v1.1.5: attacker gets self-banned via a specific path, then a counting bug in incoming-peer
bookkeeping blocks ALL new inbound peers — persistent, remote, cheap wedge (no crash needed).

**Related: Immunefi #38686 [BC-Low]** — `reports/eth-l1-clients_findings/38686-bc-low-nodes-with-trusted-peers-vulnerable-to-pending-peer-flooding-and-dos.md`
Reth: unlimited pending peers + disconnect-after-limit → pending counter subtraction overflow →
pending limit permanently exceeded; new peers can never connect (nodes with trusted peers).

### Category 6: CL-side variants (teku/lighthouse/nimbus/erigon-Caplin)

- **#38920 [BC-Medium]** Teku remote DoS: unvalidated BlobSidecarsByRange params — `reports/eth-l1-clients_findings/38920-bc-medium-teku-remote-dos.md`
- **#38948 [BC-Low]** Lighthouse remote DoS (same family as #38920) — `reports/eth-l1-clients_findings/38948-bc-low-lighthouse-remote-dos.md`
- **#37505 [BC-Insight]** Teku 24.10.3: 1-byte spam over raw tcp/9000 → full peer removal + desync — `reports/eth-l1-clients_findings/37505-bc-insight-remotely-spamming-1-byte-leads-to-full-peer-removal-and-desync-in-both-execution-an.md`
- **#38459 [BC-Low]** Erigon embedded-Caplin remote DoS — `reports/eth-l1-clients_findings/38459-bc-low-erigon-remote-dos.md`

### Category 7: Sigma Prime reth 2024 audit anchors

From `reports/eth-l1-clients_findings/reth-sigp-2024.md`:
- RETH-07 **Lack of Timeout in EthStream Handshake** (High) — half-open handshakes pin resources
- RETH-11 **DoS Through PING Spamming** (Medium) — deskew/ping handling
- RETH-24 **Unbounded Channels** (Low), RETH-25 **Connection DoS Via Invalid TCP Packets** (Low), RETH-27 **UDP Spamming DoS** (Low)

## Vulnerable Code Pattern (generic)

```rust
// VULNERABLE: response size driven by peer-controlled range, fully buffered
async fn handle_get_block_headers(req: GetBlockHeaders) -> Response {
    let mut headers = Vec::new();
    let mut num = req.start;                       // attacker-controlled
    while num < req.start + req.limit {            // no clamp to MAX_HEADERSserve
        headers.push(db.header(num));              // unbounded allocation
        num += 1;
    }
    Response::new(headers)                         // serialized in-memory
}
```

## Similar Reports

| Client | Report | Vector | Reported Sev |
|--------|--------|--------|--------------|
| reth | #38850 | GetBlockHeaders OOM | Low |
| nethermind | #37466 | evil client, receipts | Medium |
| nethermind | #37120 | TCP handshake flood | Insight |
| geth/nethermind/besu | #38598 | GetReceiptsMsg | Insight |
| reth | #38807 | ban logic peer exhaustion | Low |
| reth | #38686 | pending peer overflow | Low |
| teku | #38920 | BlobSidecarsByRange params | Medium |
| teku | #37505 | 1-byte tcp/9000 spam | Insight |
| reth | RETH-07/11/24/25/27 | handshake timeout / PING / channels / TCP / UDP | High/Med/Low |
| prysm | #37148 | wantedPeerDials() dead branch (dial logic gap) | Insight |
| prysm | #37153 | malicious validator brings down honest nodes | Insight |
| besu | #38275 | evil-client headers-traversal DoS + total peer removal | Low |

## Detection & Hunt Strategy

1. Enumerate every devp2p/libp2p request message the client serves; for each, find the size/bound
   source and verify a hard cap independent of peer input.
2. Compare connection-accept path against geth's `dialer`/`setupIncomingPeers` rate limits
   (1 handshake per IP / 30s) — absence in another client is reportable.
3. Check every peer-counter mutation for underflow on disconnect (`checked_sub` vs `-`).
4. Load test: single machine, one p2p connection, max-legal-range requests; watch RSS.

## References

- `reports/eth-l1-clients_findings/38850-bc-low-remote-p2p-oom-crash-getblockheaders-reth.md`
- `reports/eth-l1-clients_findings/37466-bc-medium-evil-client-oom-crash-fast-p2p-crash.md`
- `reports/eth-l1-clients_findings/37120-bc-insight-remote-handshake-based-tcp-30303-flooding-leads-to-an-out-of-memory-crash.md`
- `reports/eth-l1-clients_findings/38598-bc-insight-getreceiptsmsg-abuse-leads-to-the-dos-and-or-crash-of-every-el-client-in-the-ethere.md`
- `reports/eth-l1-clients_findings/38807-bc-low-dos-any-reth-node-via-ban-logic-exploit.md`
- `reports/eth-l1-clients_findings/38686-bc-low-nodes-with-trusted-peers-vulnerable-to-pending-peer-flooding-and-dos.md`
- `reports/eth-l1-clients_findings/38920-bc-medium-teku-remote-dos.md`
- `reports/eth-l1-clients_findings/38948-bc-low-lighthouse-remote-dos.md`
- `reports/eth-l1-clients_findings/37505-bc-insight-remotely-spamming-1-byte-leads-to-full-peer-removal-and-desync-in-both-execution-an.md`
- `reports/eth-l1-clients_findings/38459-bc-low-erigon-remote-dos.md`
- `reports/eth-l1-clients_findings/reth-sigp-2024.md`
- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-forest-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-forest-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-forest-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-lotus-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-obol-sigma-prime-obol-network-charon-security-assessment-report-v2-1-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-reth-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-reth-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-reth-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-reth-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-reth-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-reth-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-reth-review-pdf.md`
- Immunefi/audit `37148` [BC-Insight] (prysm, INFO): wantedPeerDials() branch will never be executed — `reports/eth-l1-clients_findings/37148-bc-insight-wantedpeerdials-branch-will-never-be-executed.md` (Immunefi (br0nz3p1ck4x3))
- Immunefi/audit `37153` [BC-Insight] (prysm, INFO): Malicious validator can bring down honest nodes — `reports/eth-l1-clients_findings/37153-bc-insight-malicious-validator-can-bring-down-honest-nodes.md` (Immunefi (br0nz3p1ck4x3))
- Immunefi/audit `38275` [BC-Low] (besu, LOW): Evil-client P2P headers-traversal leads to D/DoS and total peer removal — `reports/eth-l1-clients_findings/38275-bc-low-evil-client-p2p-headers-traversal-leads-to-d-dos-and-total-peer-removal.md` (Immunefi (warden))
