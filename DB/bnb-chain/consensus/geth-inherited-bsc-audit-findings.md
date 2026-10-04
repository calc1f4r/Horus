---
# Core Classification
protocol: go-ethereum              # BSC's execution client (bsc) is a go-ethereum fork; these findings are inherited surface
chain: bsc
category: client_security
vulnerability_type: insecure_default_config

# Pattern Identity
root_cause_family: insecure_defaults_and_missing_defensive_checks
pattern_key: insecure_default | rpc_http_cors | regression_commit | browser_same_origin_bypass

# Interaction Scope
interaction_scope: cross_boundary
involved_contracts:
  - go-ethereum rpc/http.go (newCorsHandler)
  - vendor/github.com/rs/cors middleware
  - p2p rlpx.go (rlpxFrameRW.ReadMsg, readHandshakeMsg)
  - eth/downloader.go (qosReduceConfidence)
  - core/evm.go (Transfer) + core/tx_pool.go (validateTx)
  - internal/jsre/jsre.go (randomSource)
  - consensus/ethash (dataset timestamping)
path_keys:
  - insecure_default | --rpc HTTP endpoint | rs/cors empty AllowedOrigins -> allow-all
  - unbounded_allocation | rlpx frame read | attacker-controlled fsize -> 16.8MB make()
  - missing_zero_check | downloader QoS | peers==0 -> panic divide-by-zero
  - implicit_validation | block processing | negative tx value only blocked by RLP encoding

# Attack Vector Details
attack_type: configuration_bypass
affected_component: rpc_http_interface|p2p_networking|evm_interpreter|block_processing

# Technical Primitives
primitives:
  - cors_default_allow_all
  - empty_slice_vs_empty_string_default
  - user_controlled_memory_allocation
  - unbounded_object_pool (intPool)
  - divide_by_zero_panic
  - implicit_serialization_validation
  - weak_prng_seed_fallback
  - data_race_mutex_gap

# Grep / Hunt-Card Seeds
code_keywords:
  - newCorsHandler
  - AllowedOrigins
  - rpccorsdomain
  - rlpxFrameRW
  - readInt24
  - readHandshakeMsg
  - qosReduceConfidence
  - rttConfidence
  - ErrNegativeValue
  - tx.Value().Sign()
  - intPool
  - randomSource
  - crand.Read
  - dataset(block uint64)

# Impact Classification
severity: high
impact: node_compromise|remote_rpc_abuse|dos
financial_impact: none

# Context Tags
tags:
  - geth
  - bsc-geth
  - inherited_code
  - cors
  - same_origin_policy
  - rpc
  - p2p
  - evm
  - dos
  - regression

# Version Info
language: go
version: "go-ethereum <=1.6.x (audited Apr 2017); classes recur in forks incl. bsc"
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [truesec] | reports/bnb-chain_findings/bsc-docs-audits-2017-04-25-geth-audit-truesec-pdf.md | HIGH | TrueSec (for Ethereum Foundation) | https://github.com/ethereum/go-ethereum/commit/5e29f4be935ff227bbf07a0c6e80e8809f5e0202 |

> BSC's execution layer is a go-ethereum fork, so pre-fork geth audit findings are directly
> relevant when auditing bsc / bsc-geth derivatives: fork drift can reintroduce or fail to
> inherit fixes for every class below.

## Geth-Inherited Audit Findings Relevant to BSC Clients

**Insecure defaults and missing defensive checks inherited from go-ethereum (TrueSec 2017 audit)** — a cluster of client-level issues where correctness relies on fragile implicit guarantees (empty-slice CORS default, caller-side zero checks, RLP encoding as the only negative-value guard, unbounded pools).

### Overview

TrueSec's April 2017 review of go-ethereum found no critical bugs but surfaced a family of insecure-default/fragile-check patterns — most seriously an unintentional CORS allow-all default on the HTTP RPC that bypasses browser same-origin policy. BSC inherits the geth codebase; each pattern below is a checklist item for any bsc-geth fork audit.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because secure behavior depends on implicit/external guarantees (middleware defaults, caller-side checks, serialization format properties) instead of explicit validation at the point of use"
- Pattern key: `insecure_default | rpc_http_cors | regression_commit | browser_same_origin_bypass`
- Interaction scope: `cross_boundary` (browser→local RPC; peer→p2p stack; miner→block processor)
- Primary affected component(s): `rpc/http.go, p2p/rlpx.go, eth/downloader.go, core/evm.go, core/intpool.go, internal/jsre`
- Contracts / modules involved: `newCorsHandler, rlpxFrameRW, qosReduceConfidence, Transfer/validateTx, intPool, randomSource, ethash.dataset`
- Path keys: see frontmatter `path_keys`
- High-signal code keywords: `newCorsHandler`, `AllowedOrigins`, `qosReduceConfidence`, `intPool`, `ErrNegativeValue`
- Typical sink / impact: `remote RPC abuse from any website / node panic / memory-exhaustion DoS / peer resource drain`
- Validation strength: `strong` (PoC JavaScript + curl evidence in source report for the CORS issue)

#### Contract / Boundary Map

- Entry surface(s): `--rpc` HTTP endpoint (port 8545), RLPx peer connections, mined block ingestion, JS console
- Contract hop(s): `browser JS -> HTTP RPC -> cors middleware -> JSON-RPC handlers`; `peer -> rlpx ReadMsg -> make([]byte, rsize)`; `miner block -> block processing -> Transfer()`
- Trust boundary crossed: `browser same-origin policy → local node control plane`; `untrusted peer → node memory`
- Shared state or sync assumption: `default config values must fail closed; validation done in one layer must be repeated where the invariant is consumed`

#### Valid Bug Signals

- Signal 1: A regression commit changes the *type* of a security-relevant default (string → slice) so the "empty" value takes a different code path in downstream middleware (empty array → rs/cors `allowedOriginsAll = true`)
- Signal 2: Peer-controlled length fields feed `make([]byte, n)` without a protocol-level cap applied *before* allocation (16.8MB frame alloc vs 10MB protocol max; 65KB handshake alloc)
- Signal 3: Division by non-constant divisors with the zero-check delegated to callers (`(peers - 1) / peers`)
- Signal 4: A consensus-critical invariant (non-negative tx value) enforced only in the mempool path (`validateTx`) and implicitly via RLP during block processing
- Signal 5: Unbounded reuse pools (intPool) that let cheap opcodes accumulate memory far beyond gas-priced cost (10GB for ~3.3e9 gas vs intended 1.95e14 gas)

#### False Positive Guards

- Not this bug when: CORS default explicitly fails closed (no headers emitted unless configured) — verify with `curl -i -X OPTIONS -H "Origin: attacker"` before/after the suspected commit
- Not this bug when: frame-size caps are checked before buffer allocation and handshake sizes are bounds-checked against the spec
- Safe if: divisors are constants or immediately zero-checked; block-processing re-validates `tx.Value().Sign() >= 0` explicitly
- intPool memory abuse is *contained* while consensus gas-limit growth rules (1/1024 per block) hold — treat as hardening, not exploitable, unless the client relaxes gas caps or cheaper pool-filling opcode sequences exist
- Two-time-pad / replay-protection weaknesses in RLPx were known-and-accepted (public chain data only) at audit time — cite as context, not fresh findings

### Vulnerability Description

#### Root Cause

Security properties delegated to defaults, callers, or serialization rather than enforced locally:

1. **CORS allow-all default (most serious)** — commit `5e29f4b` (2017-04-12) changed `newCorsHandler` from splitting a comma string to receiving `[]string`. The old default (`""`) split into `[""]` which rs/cors treated as one (invalid) origin; the new default (`[]`) hits rs/cors's own fallback: `if len(options.AllowedOrigins) == 0 { c.allowedOriginsAll = true }`. Net effect: `geth --rpc` with no `--rpccorsdomain` answers `Access-Control-Allow-Origin: <any origin>` — same-origin policy bypassed for every browser.
2. **Unnecessarily large peer-controlled allocations** — `rlpxFrameRW.ReadMsg` computes `rsize` from the 24-bit frame header and allocates up to 16.8MB before any protocol cap (10MB) is applied; `readHandshakeMsg` extends a buffer by an attacker-chosen 16-bit size up to 65KB.
3. **Divide-by-zero fragility** — `qosReduceConfidence` computes `atomic.LoadUint64(&d.rttConfidence) * (peers - 1) / peers` relying on the caller to guarantee `peers != 0`; Go panics on integer division by zero.
4. **Fragile negative-value protection** — `validateTx` rejects `tx.Value().Sign() < 0` for mempool admission, but block processing has no explicit check; negative amounts are only impossible because RLP cannot encode them. An evil miner crafting an alternate serialization path (or a fork changing decoders) would let `Transfer()` with negative `amount` move Ether from recipient to sender.
5. **Weak PRNG seed fallback** — `randomSource()` seeds `math/rand` with `time.Now().UnixNano()` when `crypto/rand.Read` errors, instead of failing; errors from crypto/rand usually indicate deeper problems.
6. **Ethash dataset race** — first `current.used = time.Now()` write outside `current.lock` in `dataset()`.
7. **Known/accepted** — RLPx two-time-pad confidentiality flaw and missing secure-channel replay protection (documented upstream issues at audit time).

#### Attack Scenario / Path Variants

**Path A: Browser → HTTP RPC same-origin bypass** [HIGH]
Path key: `insecure_default | --rpc HTTP endpoint | rs/cors empty AllowedOrigins -> allow-all`
1. Victim runs `geth --rpc` (any bsc-geth fork with the same default) with default CORS config
2. Victim visits attacker-controlled page (any origin, even `file://` with null Origin)
3. Page JS issues `XMLHttpRequest` POST to `http://localhost:8545` — CORS preflight now succeeds because rs/cors reflects the origin
4. RPC responses (e.g. `rpc_modules`) readable cross-origin; public-API data exfiltration and any locally-exposed namespace reachable

**Path B: Peer → memory pressure via RLPx allocations** [LOW/INFO]
Path key: `unbounded_allocation | rlpx frame read | attacker-controlled fsize -> 16.8MB make()`
1. Attacker opens RLPx connections and sends frames with maximal 24-bit size fields
2. Node allocates 16.8MB per frame regardless of the 10MB protocol message cap
3. Many parallel connections multiply allocations; TrueSec found no crash path but flags resource-exhaustion potential

**Path C: Miner → negative-value transfer (defense-in-depth gap)** [INFO]
Path key: `implicit_validation | block processing | negative tx value only blocked by RLP encoding`
1. Evil miner constructs blocks containing negative-valued transactions (requires bypassing RLP's unsigned encoding — currently impossible)
2. If any fork introduces an alternate tx encoding/decoding path, `Transfer(db, sender, recipient, negativeAmount)` moves funds recipient→sender
3. Severity is latent: protection is a property of the serialization format, not of the processing rule

#### Vulnerable Pattern Examples

**Example 1: CORS empty-array default flows into allow-all middleware** [Approx Vulnerability : HIGH]
```go
// ❌ VULNERABLE (rpc/http.go after commit 5e29f4b): empty AllowedOrigins is
// interpreted by rs/cors as "allow all origins", silently defeating SOP
func newCorsHandler(srv *Server, allowedOrigins []string) http.Handler {
    c := cors.New(cors.Options{
        AllowedOrigins: allowedOrigins, // [] on default config
        AllowedMethods: []string{"POST", "GET"},
        MaxAge:         600,
        AllowedHeaders: []string{"*"},
    })
    return c.Handler(srv)
}
// vendor/github.com/rs/cors/cors.go:
// if len(options.AllowedOrigins) == 0 { c.allowedOriginsAll = true }
```

**Example 2: peer-sized allocation before protocol cap** [Approx Vulnerability : LOW]
```go
// ❌ VULNERABLE (p2p/rlpx.go): fsize is peer-controlled; allocate happens
// before the 10MB protocol-message limit is applied
fsize := readInt24(headbuf)
var rsize = fsize
if padding := fsize % 16; padding > 0 {
    rsize += 16 - padding
}
framebuf := make([]byte, rsize) // TRUESEC: user-controlled allocation of 16.8MB
```

**Example 3: caller-trusted divisor and serialization-trusted sign** [Approx Vulnerability : LOW]
```go
// ❌ FRAGILE (eth/downloader.go): panics if caller lets peers hit 0
func (d *Downloader) qosReduceConfidence() {
    peers := uint64(d.peers.Len())
    conf := atomic.LoadUint64(&d.rttConfidence) * (peers - 1) / peers // no zero-check
    _ = conf
}

// ❌ FRAGILE (core): block processing relies on RLP's inability to encode
// negatives instead of re-checking; only tx_pool validates explicitly:
// if tx.Value().Sign() < 0 { return ErrNegativeValue }
```

### Impact Analysis

#### Technical Impact
- Any website can read responses from a locally running node's HTTP RPC (default `--rpc`), enabling info disclosure and driving whatever namespaces are exposed on the port
- Peer-driven oversized allocations multiply per-connection memory cost ~1.7x beyond the protocol message cap
- Latent consensus hazard: negative-value protection is a serialization artifact, not a processing rule — fragile for any fork touching tx decoding (directly relevant to bsc-geth evolution, e.g. new tx types)

#### Business Impact
- Node operators unknowingly expose RPC to every origin → eclipse/peer-manipulation and debug-endpoint abuse become browser-driveable
- Fork maintainers (BSC included) inherit silent regressions when rebasing over upstream refactors that change default-value types

#### Affected Scenarios
- Auditing any bsc-geth / geth fork: diff `newCorsHandler` and middleware defaults against upstream fix history; verify frame caps before allocation; grep divisions by peer/counter variables; confirm block-processing re-validates tx value sign
- Any client upgrade that changes tx envelope formats (new transaction types) — re-check negative/overflow value guards in block processing, not just mempool

### Secure Implementation

**Fix 1: fail-closed CORS default**
```go
// ✅ SECURE: default emits no CORS headers (browser blocks cross-origin);
// explicit configuration required to open access
func newCorsHandler(srv *Server, allowedOrigins []string) http.Handler {
    opts := cors.Options{AllowedMethods: []string{"POST", "GET"}, MaxAge: 600,
        AllowedHeaders: []string{"*"}}
    if len(allowedOrigins) > 0 { // explicit only
        opts.AllowedOrigins = allowedOrigins
    } else {
        opts.SkipCors = true // serve without CORS headers: SOP applies
    }
    return cors.New(opts).Handler(srv)
}
```

**Fix 2: cap before allocate; check before divide; validate at consumption**
```go
// ✅ SECURE: apply protocol max before allocating
const maxProtocolMsg = 10 * 1024 * 1024
if fsize > maxProtocolMsg { return msg, errors.New("frame too large") }
framebuf := make([]byte, rsize)

// ✅ SECURE: zero-check non-constant divisors immediately
peers := uint64(d.peers.Len())
if peers == 0 { return }
conf := atomic.LoadUint64(&d.rttConfidence) * (peers - 1) / peers

// ✅ SECURE: explicit sign validation in block processing too
if tx.Value().Sign() < 0 { return core.ErrNegativeValue }
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Security-relevant config defaults flowing into third-party middleware whose "empty" semantics differ from the producer's
- Peer-controlled length/size integers reaching make()/append() before spec caps
- Division or modulo by any runtime-variable without a preceding zero-check
- Validation present on the mempool/admission path but absent on the processing path for the same field
- Unbounded sync.Pool-style reuse pools reachable from priced-but-cheap operations
```

#### High-Signal Grep Seeds
```
- newCorsHandler
- AllowedOrigins
- rpccorsdomain
- readInt24
- qosReduceConfidence
- ErrNegativeValue
- intPool
- randomSource
```

#### Code Patterns to Look For
```
- Pattern 1: `if len(x.AllowedOrigins) == 0 { allowAll = true }` in vendored CORS libs
- Pattern 2: `make([]byte, <peer-controlled>)` in frame/handshake readers
- Pattern 3: `(peers - 1) / peers` style trust-the-caller arithmetic
- Pattern 4: `time.Now().UnixNano()` fallback seed after crypto/rand error
- Pattern 5: unlocked first write of shared timestamp (`current.used`) before generate/wait lock acquisition
```

#### Audit Checklist
- [ ] OPTIONS-probe the HTTP RPC with an arbitrary Origin on default config (expect no ACAO header)
- [ ] Trace every refactor commit that changes a default value's type (string→slice, int→pointer)
- [ ] Verify frame-size caps precede buffer allocation in p2p read paths
- [ ] Confirm block processing re-validates transaction value sign independent of serialization
- [ ] Grep all divisions by non-constant expressions for zero-checks
- [ ] Check intPool-like reuse pools for size bounds if gas schedule changes

### Real-World Examples

#### Known Exploits
- No public exploit from this report; the CORS default is the same *class* as later MetaMask/wallet local-RPC drive-by attacks (browser → localhost JSON-RPC).

#### Related CVEs/Reports
- TrueSec Go Ethereum Security Review (2017-04-25), commissioned by Ethereum Foundation — see [truesec] reference
- Upstream follow-ups: geth `--http.virtualhosts` Host-header check line of defense (see DB/eth-l1-clients/execution/rpc-dns-rebinding.md for the related DNS-rebinding class)

### Prevention Guidelines

#### Development Best Practices
1. Fail-closed defaults: absence of configuration must never widen access in downstream middleware
2. Validate at the point of consumption (block processing), not only at admission (mempool)
3. Zero-check every non-constant divisor immediately before division
4. Bound all reuse pools and apply protocol size caps before allocation

#### Testing Requirements
- Unit tests: default-config CORS probe (OPTIONS with foreign Origin must NOT return ACAO header); zero-peer downloader paths
- Integration tests: regression test per security-relevant default after any config-type refactor
- Fuzzing targets: RLPx frame readers (size fields), tx decoders with adversarial encodings

### Keywords for Search

`geth`, `bsc`, `bsc-geth`, `go-ethereum`, `fork inheritance`, `cors`, `same-origin policy`, `rpccorsdomain`, `AllowedOrigins`, `rs/cors`, `rpc http`, `default configuration`, `regression`, `rlpx`, `frame size`, `memory allocation`, `unbounded allocation`, `divide by zero`, `panic`, `negative value transaction`, `ErrNegativeValue`, `RLP encoding`, `implicit validation`, `intPool`, `evm memory dos`, `gas limit`, `prng seed`, `crypto/rand`, `math/rand`, `race condition`, `ethash`, `known issues`, `two-time-pad`, `replay protection`

### Related Vulnerabilities

- DB/eth-l1-clients/execution/rpc-dns-rebinding.md (same local-RPC browser boundary; works regardless of CORS)
- DB/eth-l1-clients/execution/rlp-decoding-lenient-parsing.md (serialization-trust family)
- DB/eth-l1-clients/p2p/snappy-decompression-DoS.md (peer-driven resource exhaustion family)
