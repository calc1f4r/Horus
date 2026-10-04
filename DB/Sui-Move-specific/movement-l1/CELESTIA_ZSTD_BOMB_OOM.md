---
# Core Classification (Required)
protocol: movement
chain: movement
category: resource_exhaustion
vulnerability_type: decompression_bomb|missing_size_limit|oom_crash

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: unbounded_decompression | celestia_blob_ingress | zstd_decode_all_bomb | node_oom_shutdown

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: cross_protocol
involved_contracts:
  - Celestia DA provider (protocol-units/da/movement/providers/celestia, blob/ir.rs into_da_blob)
  - Movement DA light node / full node blob processing
  - Celestia network (public blob submission, 2MB compressed limit)
path_keys:
  - unbounded_decompression | celestia_blob_stream | into_da_blob_zstd_bomb | light_node_oom
  - unbounded_decompression | direct_blob_publish | crafted_rle_blob | network_wide_oom

# Attack Vector Details (Required)
attack_type: data_manipulation
affected_component: da_blob_deserialization

# Technical Primitives (Required - list all applicable)
primitives:
  - zstd::decode_all
  - into_da_blob
  - CelestiaBlob
  - DaBlob
  - bcs::from_bytes
  - RLE block
  - zstd magic header
  - blob size limit

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - into_da_blob
  - zstd::decode_all
  - decompress
  - CelestiaBlob
  - blob_submit
  - bcs::from_bytes

# Impact Classification
severity: critical
impact: dos
exploitability: 0.9
financial_impact: none

# Context Tags (Optional but recommended)
tags:
  - movement
  - move
  - zstd
  - decompression_bomb
  - dos
  - oom
  - celestia
  - da_layer
  - resource_exhaustion
  - attackathon

# Version Info (Optional)
language: move        # Move-family L1; vulnerable host code is Rust
version: all
---

## References & Source Reports

> Verified: #42233 body contains the exact `into_da_blob` code, a working zstd-bomb PoC (~100GB allocation from <1.4MB input), and a fix sketch. #42143 is the sibling "crafted blob shuts down all DA light nodes" critical.

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [P1] | reports/movement-l1_findings/42233-bc-critical-critical-dos-vulnerability-in-movement-network-s-da-layer-due-to-zstd-bomb-blob-ex.md | CRITICAL | Immunefi (perseverance) | #42233 |
| [P2] | reports/movement-l1_findings/42143-bc-critical-decompressing-a-maliciously-crafted-blob-leads-to-shutting-down-all-movement-da-li.md | CRITICAL | Immunefi (indexed critical) | #42143 |

## Zstd Decompression Bomb in Celestia Blob Ingress Crashes All DA Light Nodes

### Overview

`into_da_blob()` calls `zstd::decode_all()` on blob data streamed from Celestia with no decompressed-size limit and before any signature verification, so a <2MB blob (Celestia's cap) can decompress to ~100GB and OOM every Movement node processing the DA stream — a network-wide shutdown for cents.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because untrusted DA blobs are decompressed with an unbounded allocator before authentication, and the upstream size limit (Celestia 2MB) applies only to the compressed input."
- Pattern key: `unbounded_decompression | celestia_blob_ingress | zstd_decode_all_bomb | node_oom_shutdown`
- Interaction scope: `cross_protocol` (Celestia public DA → Movement nodes)
- Primary affected component(s): `into_da_blob` (providers/celestia/blob/ir.rs), all blob consumers
- Contracts / modules involved: Celestia DA provider, DA light node blob pipeline
- Path keys: streamed-blob path and direct-publish path (below)
- High-signal code keywords: `into_da_blob`, `zstd::decode_all`, `decompress`, `blob_submit`, `bcs::from_bytes`
- Typical sink / impact: `node OOM crash / total network shutdown`
- Validation strength: `strong` — executable PoC code included in report

#### Contract / Boundary Map

- Entry surface(s): Celestia blob stream (`stream_read_from_height`) consumed by every node; anyone can `blob_submit` to the Movement namespace on Celestia
- Contract hop(s): `attacker -> Celestia blob_submit -> node stream -> into_da_blob (unbounded zstd) -> OOM`
- Trust boundary crossed: `public DA chain -> node memory allocator (pre-authentication)`
- Shared state or sync assumption: assumption that Celestia's 2MB blob limit bounds node work — false for decompression

#### Valid Bug Signals

- Signal 1: `zstd::decode_all(blob.data.as_slice())` with no size cap / ReadDecoder limit
- Signal 2: decompression occurs before `try_verify()` (signature check) on the blob
- Signal 3: attacker needs only a Celestia account + gas for ~1.4MB of data (PoC asserts `< 0x1_500_000` bytes)

#### False Positive Guards

- Not this bug when: decompression uses a bounded reader (e.g. `zstd::stream::read::Decoder` wrapped in `take(limit)`) or validates size before/while decompressing
- Safe if: blobs are authenticated before decompression AND a hard decompressed-size ceiling is enforced
- Requires attacker control of: ability to post a blob to Celestia in Movement's namespace (public permissionless action)

### Vulnerability Description

#### Root Cause

Blob payloads are zstd-compressed inside `CelestiaBlob`; on ingest, `into_da_blob` blindly expands them. zstd RLE blocks can encode huge zero-runs in ~4 bytes each, so a tiny input legitimately expands enormous outputs. Celestia's 2MB cap constrains only the compressed form. Because expansion precedes signature verification, no trust is required — just posting to the namespace.

#### Attack Scenario / Path Variants

**Path A: [Streamed blob → every node OOMs]**
Path key: `unbounded_decompression | celestia_blob_stream | into_da_blob_zstd_bomb | light_node_oom`
1. Craft zstd bomb: magic `28 b5 2f fd 00 7f` + ~5.4M RLE blocks (`02 00 10 ff` = 0xff × 0x8000)
2. Keep total < 1.4MB (under Celestia's 2MB blob limit)
3. `blob_submit` to Movement's Celestia namespace
4. All subscribed nodes call `into_da_blob` → allocate ~100GB → crash/OOM
5. Network cannot confirm transactions (total shutdown impact class)

**Path B: [Sustained shutdown]**
Path key: `unbounded_decompression | direct_blob_publish | crafted_rle_blob | network_wide_oom`
1. Repeat Path A with fresh blobs as nodes restart
2. Nodes crash on restart when they re-stream the same height range
3. Persistent liveness kill until blobs age out / code patched

#### Vulnerable Pattern Examples

**Example 1: Unbounded decode of untrusted input** [Approx Vulnerability : CRITICAL]
```rust
// ❌ VULNERABLE: providers/celestia/src/blob/ir.rs
pub fn into_da_blob<C>(blob: CelestiaBlob) -> Result<DaBlob<C>, anyhow::Error>
where C: Curve + for<'de> Deserialize<'de> {
    // decompress blob.data with zstd
    let decompressed =
        zstd::decode_all(blob.data.as_slice()).context("failed to decompress blob")?; // @audit no size limit
    // deserialize the decompressed data with bcs
    let blob = bcs::from_bytes(decompressed.as_slice()).context("failed to deserialize blob")?;
    Ok(blob)
}
```

**Example 2: Working bomb payload (report PoC)** [Approx Vulnerability : CRITICAL]
```rust
// ❌ VULNERABLE: proof that <1.4MB input → ~100GB output
let mut b: Vec<u8> = vec![0x28, 0xb5, 0x2f, 0xfd, 0x0, 0x7f]; // zstd magic + max window
let n_blocks = 0x530000;
for _ in 0..n_blocks {
    b.extend(&[0x02, 0x00, 0x10, 0xff]); // RLE block: 0xff repeated 0x8000 times
}
b.extend(&[0x01, 0x00, 0x00]);           // finish
assert!(b.len() < 0x1_500_000);          // fits Celestia 2MB limit
let res = zstd::decode_all(b.as_slice()).unwrap(); // ≥100GB allocation, then crash
```

**Example 3: Ordering makes it pre-auth** [Approx Vulnerability : CRITICAL]
```rust
// ❌ VULNERABLE: call order in blob processing
let da_blob = into_da_blob(celestia_blob)?; // 1. unbounded decompression FIRST
da_blob.try_verify()?;                      // 2. signature check AFTER (never reached for bombs)
```

### Impact Analysis

#### Technical Impact
- Every node consuming the stream allocates unbounded memory → OOM kill
- Crash-on-restart loop while malicious blobs remain in the streamed height range
- No privileges, no Movement account, trivially cheap attack

#### Business Impact
- Total network shutdown class (reported as Critical)
- Complete liveness loss for the L1 and anything building on it

#### Affected Scenarios
- All networks reading blobs from public Celestia (mainnet topology at report time)
- Any Celestia namespace that Movement nodes subscribe to

### Secure Implementation

**Fix 1: Bounded decompression (report's fix sketch)**
```rust
// ✅ SECURE: enforce a hard decompressed-size ceiling while streaming
pub fn into_da_blob<C>(blob: CelestiaBlob) -> Result<DaBlob<C>, anyhow::Error> {
    const MAX_DECOMPRESSED: usize = 8 * 1024 * 1024; // protocol max blob size
    let reader = zstd::stream::read::Decoder::new(blob.data.as_slice())?;
    let mut limited = reader.take(MAX_DECOMPRESSED as u64 + 1);
    let mut decompressed = Vec::new();
    limited.read_to_end(&mut decompressed)?;
    if decompressed.len() > MAX_DECOMPRESSED {
        return Err(anyhow!("blob decompresses beyond protocol maximum"));
    }
    Ok(bcs::from_bytes(decompressed.as_slice())?)
}
```

**Fix 2: Authenticate before expanding**
```rust
// ✅ SECURE: verify signer/signature on the compressed bytes before decompression
celestia_blob.verify_compressed_signature()?; // sign over compressed digest
let da_blob = bounded_decompress(celestia_blob)?;
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- decode_all / decompress on data crossing a public-chain boundary
- Size limits applied upstream (DA chain limits) trusted for downstream memory budgets
- Decompression ordered before authentication of the same payload
```

#### High-Signal Grep Seeds
```
- into_da_blob
- zstd::decode_all
- decompress
- bcs::from_bytes
```

#### Code Patterns to Look For
```
- Pattern 1: `zstd::decode_all(...)` / `decompress_to_vec` without a take() limit
- Pattern 2: constants like MAX_BLOB_SIZE checked on compressed bytes only
- Pattern 3: resource-heavy parsing of unauthenticated network input

```

#### Audit Checklist
- [ ] For every deserialization of external-chain data, check decompression bounds
- [ ] Verify authentication ordering relative to expensive parsing
- [ ] Compute worst-case expansion ratio of the codec in use (zstd RLE ≈ 32768:1 per block)

### Real-World Examples

#### Known Exploits
- None public (attackathon finding)

#### Related CVEs/Reports
- #42143 — crafted blob decompression shuts down all DA light nodes (sibling report)
- #41489 / #43114 — unchecked blob *sizes* (post-decompression) causing chain halt

### Prevention Guidelines

#### Development Best Practices
1. Never use unbounded `decode_all` on untrusted input; always pair with `take(limit)`
2. Authenticate before resource-intensive processing
3. Never inherit a foreign chain's size limits as your own resource budget

#### Testing Requirements
- Unit tests for: bomb input rejected at limit boundary (limit, limit+1)
- Integration tests for: node survives bomb blob in stream; restart does not re-crash
- Fuzzing targets: zstd stream structure mutation, maximal-expansion block sequences

### Keywords for Search

`movement`, `zstd`, `decompression bomb`, `zip bomb`, `oom`, `denial of service`, `celestia`, `blob`, `into_da_blob`, `decode_all`, `unbounded decompression`, `resource exhaustion`, `network shutdown`, `da layer`, `rle`, `pre-authentication parsing`

### Related Vulnerabilities

- DB/Sui-Move-specific/movement-l1/DA_BLOB_SIZE_UNCHECKED_CHAIN_HALTS.md (same family, size checks)
- DB/Sui-Move-specific/MOVE_DENIAL_OF_SERVICE_VULNERABILITIES.md (DoS family)
