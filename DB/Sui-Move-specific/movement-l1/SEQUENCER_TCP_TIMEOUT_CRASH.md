---
# Core Classification
protocol: movement
chain: movement
category: resource_exhaustion
vulnerability_type: tcp_timeout_missing|slowloris_fd_exhaustion|healthcheck_cascade_crash

# Pattern Identity
root_cause_family: missing_timeout
pattern_key: missing_tcp_timeout | grpc_service_0.0.0.0 | hanging_connections | sequencer_crash_halt

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - protocol-units/da/movement/protocol/light-node (light_node.rs run_server)
  - movement full node services: opt-executor api_service, indexer service, finality viewer, LightNodeService
  - movement full-node healthchecker (kills light node on failure → cascades into sequencer crash)
path_keys:
  - missing_tcp_timeout | light_node_service_grpc | fd_exhaustion -> healthcheck kill -> sequencer panic
  - missing_tcp_timeout | opt_executor_api | fd_exhaustion -> executor unavailable -> halt
  - missing_tcp_timeout | unbounded_stream_height | stream_read_from_height(0) -> node overwhelm

# Attack Vector Details
attack_type: data_manipulation
affected_component: grpc_server_connection_handling

# Technical Primitives
primitives:
  - TcpListener
  - tonic Server
  - max_frame_size
  - accept_http1
  - file_descriptor_limit
  - healthcheck
  - stream_read_from_height
  - slowloris

# Grep / Hunt-Card Seeds
code_keywords:
  - run_server
  - TcpListener
  - max_frame_size
  - accept_http1
  - stream_read_from_height
  - serve
  - timeout
  - healthcheck

# Impact Classification
severity: critical
impact: dos
financial_impact: none

# Context Tags
tags:
  - l1_node_implementation
  - network_layer
  - slowloris
  - rust_host
  - immunefi_attackathon

language: move        # Move-family L1; vulnerable host code is Rust (movement protocol-units)
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [R1] | reports/movement-l1_findings/43244-bc-critical-lack-of-tcp-timeout-allows-attacker-to-crash-the-sequencer-via-the-light-node-serv.md | CRITICAL | immunefi | #43244 |
| [R2] | reports/movement-l1_findings/43246-bc-critical-lack-of-tcp-timeout-allows-attacker-to-crash-the-sequencer-via-the-maptos-opt-exec.md | CRITICAL | immunefi | #43246 |
| [R3] | reports/movement-l1_findings/43250-bc-critical-excessive-tcp-timeout-allows-attacker-to-crash-the-sequencer-via-the-indexer-servi.md | CRITICAL | immunefi | #43250 |
| [R4] | reports/movement-l1_findings/43251-bc-critical-lack-of-tcp-timeout-allows-attacker-to-crash-the-sequencer-via-the-finality-viewer.md | CRITICAL | immunefi | #43251 |
| [R5] | reports/movement-l1_findings/43177-bc-critical-dos-vulnerability-in-da-light-node-via-unbounded-height-parameter.md | CRITICAL | immunefi | #43177 |

## Missing TCP/gRPC Timeouts on 0.0.0.0-Bound Services: Slowloris FD Exhaustion Crashes the Sequencer

### Overview

Movement's gRPC services (LightNodeService, opt-executor API, indexer, finality viewer) are bound to `0.0.0.0` with no request/connection timeouts. Each accepted connection holds a file descriptor (default process limit ~256); an attacker opens hundreds of connections and leaves them hanging (slowloris), exhausting descriptors so the service can't accept more — and the full node's healthchecker then *kills* the light node, panicking the sequencer process and halting the network. Sibling sink: `stream_read_from_height` accepts `height=0` unbounded, replaying all blobs since genesis in one request.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because gRPC servers are bound to 0.0.0.0 without connect/request timeouts, so hanging connections pin file descriptors until exhaustion, and the healthchecker converts the unavailability into a process kill that cascades into a sequencer panic and network halt."
- Pattern key: `missing_tcp_timeout | grpc_service_0.0.0.0 | hanging_connections | sequencer_crash_halt`
- Interaction scope: `multi_contract`
- Primary affected component(s): `LightNodeService::run_server`, opt-executor `api_service`, indexer service, finality viewer, `stream_read_from_height`
- Contracts / modules involved: `light-node/src/light_node.rs`, `protocol-units/execution/maptos/opt-executor`, movement indexer, finality viewer, full-node healthchecker
- Path keys: `missing_tcp_timeout | light_node_service_grpc | fd_exhaustion -> healthcheck kill -> sequencer panic`, `missing_tcp_timeout | opt_executor_api | fd_exhaustion -> executor unavailable -> halt`, `missing_tcp_timeout | unbounded_stream_height | stream_read_from_height(0) -> node overwhelm`
- High-signal code keywords: `run_server`, `TcpListener`, `max_frame_size`, `accept_http1`, `stream_read_from_height`
- Typical sink / impact: `sequencer crash + network halt / service unavailability / full-history replay DoS`
- Validation strength: `strong` ([R1] includes working Python socket PoC + observed panic log; [R2]-[R4] replicate across three more services; [R5] documents the height=0 variant)

#### Contract / Boundary Map

- Entry surface(s): any TCP connect to 0.0.0.0-bound gRPC ports (light node 30730; executor/indexer/finality ports); `stream_read_from_height(height=0)`
- Contract hop(s): `socket connect -> tonic Server (no timeout) -> fd pinned -> healthchecker detects unavailability -> kills light node -> sequencer panic`
- Trust boundary crossed: `raw internet TCP → process liveness (healthchecker + supervisor chain)`
- Shared state or sync assumption: `healthchecker assumes service unavailability means the child is dead-worthy-of-kill; supervisor assumes light node is restartable without sequencer state loss — both false under fd exhaustion`

#### Valid Bug Signals

- Signal 1: service binds 0.0.0.0 and the server builder chain has no `timeout`/`connect_timeout`/`concurrency_limit` (only `max_frame_size` + `accept_http1`)
- Signal 2: opening ≤ fd-limit (≈256) idle connections renders the port unresponsive to new connects
- Signal 3: the deployment's healthcheck reacts to the induced unavailability by killing the service, and the parent (sequencer/full node) then panics — observed `Cannot drop a runtime...` tokio panic

#### False Positive Guards

- Not this bug when: server applies per-request timeouts, connection idle timeouts, or connection limits (check the builder chain, not OS defaults)
- Safe if: service binds loopback only AND fronted by a limiting proxy; or fd limit raised with cgroup-backed supervision that restarts cleanly without parent panic
- Requires attacker control of: network access to the exposed port only — no keys, no funds, no privileges
- Distinct from `CELESTIA_ZSTD_BOMB_OOM.md` (existing): that is *payload* decompression OOM; this is *connection-level* fd exhaustion. Different resource, different code locus.
- [R3] is the inverted variant (excessive/overlong timeout on indexer) — same sink, cite together rather than as separate DB patterns.

### Vulnerability Description

#### Root Cause

`run_server` builds the tonic server with only `max_frame_size(16MB-1)` and `accept_http1(true)`, then `serve(address)` — no `timeout`, `connect_timeout`, `concurrency_limit`, or `max_frame_size`-adjacent liveness guard. Combined with `0.0.0.0` binding (default + suggested configs), any remote host can hold sockets open. Each gRPC connection pins an fd; Nix default soft limit is 256/process. Once descriptors run out, `accept()` fails; the healthchecker (default setup) interprets this as a dead light node and kills it; the sequencer full node then hits the tokio runtime-drop panic and crashes ([R1] trace + PoC). The same builder pattern repeats across opt-executor API, indexer, and finality viewer ([R2], [R3], [R4]), so the entire service surface shares the hole.

#### Attack Scenario / Path Variants

**Path A: slowloris on LightNodeService → healthcheck kill → sequencer crash**
Path key: `missing_tcp_timeout | light_node_service_grpc | fd_exhaustion -> healthcheck kill -> sequencer panic`
Entry surface: TCP connect to 0.0.0.0:30730
Contracts touched: `light_node.rs run_server -> full-node healthchecker -> sequencer process`
1. Attacker opens ~256+ sockets and sends nothing (or partial headers)
2. No timeout exists to reap them; fd table fills; port stops accepting
3. Healthcheck fails → kills light node
4. Sequencer cannot submit DA batches, panics (`Cannot drop a runtime...`), network halts ([R1] PoC log)

**Path B: same attack on executor/indexer/finality services ([R2]/[R3]/[R4])**
Path key: `missing_tcp_timeout | opt_executor_api | fd_exhaustion -> executor unavailable -> halt`
Entry surface: executor `api_service` / indexer / finality viewer ports
1. Same slowloris pattern against each service in turn
2. Each service independently exhausts fds (no cross-service fd isolation)
3. Executor unavailability halts tx processing; indexer/finality loss degrades the stack
4. Single attacker, no resources, rotates targets for persistent outage

**Path C: unbounded history replay via height=0 ([R5])**
Path key: `missing_tcp_timeout | unbounded_stream_height | stream_read_from_height(0) -> node overwhelm`
Entry surface: `stream_read_from_height(height: u64)` gRPC
Contracts touched: `light-node DA stream -> celestia certificate/blob streams`
1. Attacker calls `stream_read_from_height(0)` — no lower-bound validation
2. Node attempts to stream all blobs since genesis (`stream_da_blobs_between_heights(last_height, height)` walk)
3. As chain history grows, request cost grows unboundedly
4. Node overwhelmed → DoS that worsens over time ([R5])

#### Vulnerable Pattern Examples

**Example 1: no-timeout server builder ([R1] verbatim)** [Approx Vulnerability : CRITICAL]
```rust
// ❌ VULNERABLE: light_node.rs run_server — no timeout, no conn limit, 0.0.0.0
async fn run_server(&self) -> Result<(), anyhow::Error> {
    let reflection = tonic_reflection::server::Builder::configure()
        .register_encoded_file_descriptor_set(movement_da_light_node_proto::FILE_DESCRIPTOR_SET)
        .build_v1()?;
    let address = self.try_service_address()?;
    info!("Server listening on: {}", address);
    Server::builder()
        .max_frame_size(1024 * 1024 * 16 - 1)   // size guard only
        .accept_http1(true)
        .add_service(LightNodeServiceServer::new(self.clone()))
        .add_service(reflection)
        .serve(address.parse()?)                 // ← no .timeout(), no .connect_timeout(),
        .await?;                                 //   no concurrency limit; binds 0.0.0.0
    Ok(())
}
```

**Example 2: slowloris PoC ([R1] verbatim)** [Approx Vulnerability : CRITICAL]
```python
# ❌ VULNERABLE: ~256 idle sockets kill the network (no timeout reaps them)
import socket
server_address = ('localhost', 30730)
arr = []
for _ in range(9999):  # adjust for fd limit, likely 256 will suffice
    arr.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    arr[-1].connect(server_address)
# observe: light node unavailable → healthchecker kills it → sequencer panics:
#   thread 'tokio-runtime-worker' panicked at tokio-1.41.1/src/runtime/blocking/shutdown.rs:51:21:
#   Cannot drop a runtime in a context where blocking is not allowed.
```

**Example 3: unbounded height parameter ([R5] verbatim structure)** [Approx Vulnerability : CRITICAL]
```rust
// ❌ VULNERABLE: height=0 replays all history; no validation on start_height
fn stream_da_blobs_from_height(
    &self,
    start_height: u64,                     // ← attacker sets 0; no lower bound check
) -> Pin<Box<dyn Future<Output = Result<DaBlobStream<C>, DaError>> + Send + '_>> {
    let certificate_stream = self.stream_certificates().await?;
    let mut last_height = start_height;
    while let Some(certificate) = certificate_stream.next().await {
        match certificate {
            Ok(Certificate::Height(height)) if height > last_height => {
                let blob_stream = self
                    .stream_da_blobs_between_heights(last_height, height)  // genesis→now
                    .await?;
                // ...streams every blob ever published
```

### Impact Analysis

#### Technical Impact
- File-descriptor exhaustion → service unavailability on five distinct services (light node, executor API, indexer, finality viewer, DA stream)
- Healthchecker converts DoS into process kill; tokio runtime-drop panic crashes the sequencer
- height=0 replay cost grows with chain age — permanent worsening DoS surface

#### Business Impact
- Total network shutdown from a laptop and a socket loop; zero attacker cost
- Immunefi Critical impact: "Network not being able to confirm new transactions (total network shutdown)"

#### Affected Scenarios
- All default/suggested Movement deployments (0.0.0.0 binds, no proxy, default healthchecker)
- Any long-running network (Path C strengthens with history depth)

### Secure Implementation

**Fix 1: timeouts + limits + loopback ([R1]/[R5] recommendations combined)**
```rust
// ✅ SECURE: bound every dimension of a connection; validate stream bounds
use std::time::Duration;
use tonic::transport::Server;

Server::builder()
    .timeout(Duration::from_secs(30))               // per-request deadline
    .connect_timeout(Duration::from_secs(5))        // handshake must complete
    .concurrency_limit_per_connection(32)           // cap in-flight requests
    .max_concurrent_connections(1024)               // cap total sockets — slowloris ceiling
    .tcp_keepalive(Some(Duration::from_secs(15)))   // reap dead peers
    .max_frame_size(1024 * 1024 * 16 - 1)
    .accept_http1(true)
    .add_service(LightNodeServiceServer::new(self.clone()))
    .add_service(reflection)
    .serve(address.parse()?)                        // address = 127.0.0.1, not 0.0.0.0
    .await?;

// And for stream endpoints: validate and bound the range
fn stream_read_from_height(&self, start_height: u64) -> ... {
    let tip = self.latest_height().await?;
    if start_height < tip.saturating_sub(MAX_LOOKBACK) {     // e.g. MAX_LOOKBACK = 10_000
        return Err(DaError::InvalidRequest(
            "height too far in the past; use paginated queries"));   // reject height=0 genesis replay
    }
    ...
}
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Server builder chain lacking timeout/connect_timeout/concurrency knobs
- 0.0.0.0 or wildcard bind in default + suggested configs
- Healthchecker wired to kill supervised services on unavailability
- Unbounded u64 parameters feeding range/stream constructors
```

#### High-Signal Grep Seeds
```
- run_server
- max_frame_size
- accept_http1
- stream_read_from_height
- Server::builder()
```

#### Code Patterns to Look For
```
- Pattern 1: Server::builder().max_frame_size(..).serve(..) with nothing between
- Pattern 2: stream_read_from_height(start_height: u64) with no bounds check
- Pattern 3: healthcheck → kill chains where DoS transmutes into crash
```

#### Audit Checklist
- [ ] For every exposed service: open fd-limit idle connections, assert service still accepts and no process dies
- [ ] Verify builder chain includes timeout + connect_timeout + connection caps
- [ ] Call stream endpoints with 0 / u64::MAX bounds; assert rejection or pagination

### Real-World Examples

#### Known Exploits
- Slowloris-class attacks are ubiquitous web-infrastructure history (2009–present); L1-node exposure makes it chain-fatal here

#### Related CVEs/Reports
- Immunefi Movement Labs Attackathon: #43244, #43246, #43250, #43251, #43177 (sources)
- Adjacent in corpus: #43330 (freezing tx processing via invalid requests to DA light node), #43110 (validator DoS via big blob ranges)

### Prevention Guidelines

#### Development Best Practices
1. Every internet-facing server gets: request timeout, connect timeout, concurrency limit, connection cap, keepalive — by policy, not per-service choice
2. Never bind 0.0.0.0 in shipped defaults; loopback + explicit exposure
3. Bound all range/stream query parameters against a maximum window
4. Healthcheck responses to resource exhaustion should restart *safe*, never kill parents

#### Testing Requirements
- Unit tests for: server config asserts (timeout present); height bounds validation
- Integration tests for: slowloris simulation below/above limits; healthcheck behavior under induced exhaustion
- Fuzzing targets: u64 parameter edges on all streaming endpoints

### References

#### Technical Documentation
- tonic transport server options: https://docs.rs/tonic/latest/tonic/transport/struct.Server.html
- Slowloris: https://en.wikipedia.org/wiki/Slowloris_(cyberattack)

#### Security Research
- Immunefi Movement Labs Attackathon (Mar–Apr 2025): #43244, #43246, #43250, #43251, #43177

### Keywords for Search

`TCP timeout`, `slowloris`, `file descriptor exhaustion`, `fd limit`, `0.0.0.0 bind`, `gRPC timeout`, `tonic server`, `connection limit`, `healthcheck kill`, `sequencer crash`, `network halt`, `stream_read_from_height`, `unbounded height`, `genesis replay`, `DoS`, `resource exhaustion`, `concurrency limit`, `connect_timeout`, `keepalive`, `movement light node`, `service liveness`, `crash cascade`, `opt-executor api`, `indexer service`, `finality viewer`

### Related Vulnerabilities

- `MALFORMED_TX_EXECUTOR_PANIC.md` (this directory — same tokio panic sink, data-triggered)
- `CELESTIA_ZSTD_BOMB_OOM.md` (existing — payload-resource exhaustion sibling)
- `LIGHTNODE_BATCH_WRITE_UNAUTHENTICATED.md` (existing — same 0.0.0.0 exposure, logic exploit)
