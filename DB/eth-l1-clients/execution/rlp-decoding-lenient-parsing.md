---
vulnerability_class: rlp_decoding_lenient_parsing
title: "RLP Decoding: Lenient Parsing / Missing Validation (trailing bytes, single-byte, non-canonical encodings)"
protocol: eth-l1-clients
category: Execution / Serialization
vulnerability_type: input_validation
attack_type: lenient_decoding|non_canonical_encoding_acceptance|consensus_divergence
affected_component: rlp_decoders|transaction_decoding|p2p_message_decoding
chain: ethereum
severity: critical
impact: consensus_divergence|chain_split|remote_crash|node_halt
severity_range: "LOW to CRITICAL"
source: Immunefi Ethereum Protocol Attackathon 2024-2025 + Sigma Prime reth 2024

primitives:
  - trailing_bytes_accepted_after_rlp_payload
  - single_byte_prefix_returns_full_input
  - create_tx_accepted_for_eip4844_blob_type
  - rlp_list_header_not_validated
  - nil_pointer_deref_on_nil_to_field

affected_components:
  - core/types transaction decoders
  - p2p eth protocol message decoders
  - txpool serialization validation
  - RPC SendRawTransaction entrypoints

tags:
  - rlp
  - decoding
  - consensus
  - eip-4844
  - erigon
  - besu
  - reth
  - trailing_bytes
  - non_canonical
  - attackathon

total_reports_analyzed: 6
client_coverage: "erigon, besu, reth, bera-reth"

# Pattern Identity (Required)
root_cause_family: missing_input_validation_in_decoder
pattern_key: rlp_lenient_decoding | trailing_bytes_single_byte_create4844 | consensus_divergence

# Interaction Scope
interaction_scope: network_facing_decoder

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - DecodeRLPTransaction
  - UnmarshalTransactionFromBinary
  - s.Remaining()
  - rlp.List
  - DecodeRLP
  - decodeOne
  - BYTE_ELEMENT
  - Kind.of(prefix)
  - TxEip4844
  - TransactionKind
  - encodePayload
  - rlp.EncodeToBytes
  - rlp.ListHeader
  - payloadSize
---

# RLP Decoding: Lenient Parsing / Missing Validation

## Overview

RLP is the base serialization of Ethereum: transactions, blocks, and devp2p messages all pass through
client RLP decoders. Every place where one client accepts a byte string another client rejects is a
latent consensus bug. The recurring root cause: decoders validate only the shape they care about
(fields present, list structure) but skip global checks the reference (geth) enforces — trailing
bytes after the payload, canonical single-byte encoding, list-header sanity, and type-specific
constraints such as "EIP-4844 blob transactions must have a `to` address".

**Root Cause Statement**: This vulnerability exists because RLP decoders accept non-canonical or
over-long inputs — missing trailing-byte checks, returning the full buffer for a single-byte prefix,
not validating list headers, or decoding type-invalid structures (CREATE for EIP-4844) — so a
malicious peer/miner can craft one serialization accepted by one client and rejected by others,
causing consensus divergence or panics.

**Observed Frequency**: Common during the 2024-25 Immunefi Ethereum Protocol Attackathon (6 distinct
accepted reports across 3+ clients) — lenient decoding is the single most-recurring client bug family.
**Consensus Severity**: LOW to CRITICAL (single accepted lenient decode of a consensus object = CRITICAL)

---

#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_input_validation_in_decoder (RLP trailing bytes / single-byte / CREATE-4844)"
- Pattern key: `rlp_lenient_decoding | trailing_bytes_single_byte_create4844 | consensus_divergence`
- Interaction scope: `network_facing_decoder`
- Primary affected component(s): `rlp_decoders`, `transaction_decoding`
- High-signal code keywords: `DecodeRLPTransaction`, `s.Remaining()`, `decodeOne`, `TxEip4844`, `encodePayload`
- Typical sink / impact: `consensus_divergence`
- Validation strength: `high` (every pattern below has a paid, accepted report)

#### Contract / Boundary Map

- Entry surface(s): devp2p eth/66-68 messages, txpool gossip, `eth_sendRawTransaction`, block import
- Contract hop(s): `wire bytes -> RLP decoder -> typed transaction struct -> EVM/consensus`
- Trust boundary crossed: `untrusted peer / RPC caller`
- Shared state or sync assumption: `identical accept/reject decision across all clients`

#### Valid Bug Signals

- Signal 1: Decoder returns successfully while `stream.Remaining() != 0` is unchecked after payload
- Signal 2: Single-byte prefix branch (`0x00..0x7f`) returns the whole input buffer, not 1 byte
- Signal 3: Typed-tx struct uses an optional field where the EIP mandates a required one (`to: TransactionKind` vs `to: Address` for 4844)
- Signal 4: RLP list header length not validated before slicing (offset vs payload-size mismatch)
- Signal 5: Nil-able pointer field dereferenced during re-encoding (`encodePayload` on nil `To`)

#### False Positive Guards

- Not this bug when: trailing data is a protocol-defined wrapper (EIP-2718 typed envelope, blob wrapping) that the decoder is expected to consume separately
- Safe if: decoder checks `Remaining() == 0` and rejects, matching geth's `rlp.Decode`
- Requires attacker control of: raw bytes on the P2P wire or in a mined block/RPC submission
- Do not report EIP-2718 envelope tolerance itself as "trailing bytes" — geth intentionally decodes typed txs from a string-kind payload

## Vulnerability Categories

### Category 1: Trailing Bytes Accepted After RLP Payload (erigon) [LOW→CRITICAL]

**Real Report: Immunefi #38828 [BC-Low] — Decode RLP of Legacy Transaction Allows Tailing Bytes (CertiK)**
Report: `reports/eth-l1-clients_findings/38828-bc-low-decode-rlp-of-legacy-transaction-allows-tailing-bytes.md`

`DecodeRLPTransaction()` (erigon v2.61.0 `core/types/transaction.go#L116`) decodes a `rlp.List`-kind
legacy tx via `tx.DecodeRLP(s)` without a `s.Remaining() != 0` check afterwards, while the typed-tx
path (`UnmarshalTransactionFromBinary`) does check. A legacy tx with appended garbage is accepted by
erigon and rejected by other clients → consensus-adjacent divergence.

**Attack Flow**:
1. Craft legacy tx RLP with trailing bytes appended after the tx list
2. Submit via `eth_sendRawTransaction` to an erigon node / include in a block via an erigon miner
3. Other clients reject the block; erigon accepts → local divergence, potential mini-fork

### Category 2: Single-Byte Prefix Returns Full Buffer (besu) [LOW]

**Real Report: Immunefi #37462 [BC-Low] — Invalid RLP decoding for single bytes (Franfran)**
Report: `reports/eth-l1-clients_findings/37462-bc-low-invalid-rlp-decoding-for-single-bytes.md`

Besu `RLP.decodeOne`: when the first prefix byte classifies as `BYTE_ELEMENT` (0x00–0x7f), the
function returns the entire `encodedValue` instead of exactly one byte. Any multi-byte input whose
first byte ≤ 0x7f decodes "successfully" to a wrong value. Called from the p2p layer and RPC paths;
if such a value lands in the MPT/state, clients diverge or consensus objects hash differently.

### Category 3: CREATE Transactions Accepted for EIP-4844 Blob Type (reth) [CRITICAL]

**Real Report: Sigma Prime reth 2024 RETH-03 — RLP Decoding Allows CREATE Transactions For EIP-4844 Types**
Report: `reports/eth-l1-clients_findings/reth-sigp-2024.md` (finding starts ~line 359)

EIP-4844 mandates blob txs carry a non-nil `to`. Reth's `TxEip4844` modeled `to` as
`TransactionKind` (optional) instead of `Address` (required), so the RLP decoder accepted a blob tx
with nil `to` (a CREATE). A block containing such a tx would be accepted by reth and rejected by
geth → immediate chain split. Fixed in reth PR #8291 by making the field type enforce presence.

### Category 4: RLP List Headers Not Validated in P2P Decoders (reth) [LOW]

**Real Reports: Sigma Prime reth 2024 RETH-33 / RETH-34** (`reports/eth-l1-clients_findings/reth-sigp-2024.md`,
~lines 1703/1732): `RequestPair` and `DisconnectReason` decoders did not validate the RLP list header
(size/payload consistency) before reading, enabling malformed-message handling bugs from peers.

### Category 5: Nil-Pointer Panic in Blob Tx Re-Encoding (erigon) [INSIGHT]

**Real Report: Immunefi #38766 [BC-Insight] — Nil Pointer Dereference Panics in encodePayload() of Blob Tx's Encoding (CertiK)**
Report: `reports/eth-l1-clients_findings/38766-bc-insight-nil-pointer-dereference-panics-in-encodepayload-of-blob-txs-encoding.md`

Mirror of RETH-03: erigon's `BlobTx` embeds `DynamicFeeTransaction` whose `To *Address` is nil-able.
Accepting a blob tx with nil `To` and re-encoding via `encodePayload()` dereferences nil → node panic
(remote DoS vector if reachable through tx gossip/decoding paths).

### Category 6: Missing RLP Length Validation in Fork Transaction Decoding (bera-reth) [CRITICAL]

**Real Report: Sigma Prime Berachain bera-reth/geth 2025 BRG4-03 — bera-reth Missing RLP Length Validation During PoL Transaction Decoding**
Report: `reports/eth-l1-clients_findings/berachain-reth-geth-sigp-2025.md` (findings table ~line 154)

## Vulnerable Code Patterns (generic)

```go
// VULNERABLE: legacy path skips trailing-byte check (erigon #38828)
if rlp.List == kind {
    tx := &LegacyTx{}
    if err = tx.DecodeRLP(s); err != nil { return nil, err }
    return tx, nil // no s.Remaining() == 0 check
}
```

```java
// VULNERABLE: single-byte kind returns whole buffer (besu #37462)
if (kind == RLPDecodingHelpers.Kind.BYTE_ELEMENT) {
    return encodedValue; // must be encodedValue.slice(0, 1)
}
```

```rust
// VULNERABLE: optional field where EIP requires presence (reth RETH-03)
pub struct TxEip4844 {
    pub to: TransactionKind, // spec: Address; nil accepted => CREATE blob tx
}
```

## Similar Reports

| Client | Report ID | Pattern | Severity |
|--------|-----------|---------|----------|
| erigon | #38828 | trailing bytes after legacy tx | Low (consensus-adjacent) |
| besu | #37462 | single-byte prefix full-buffer return | Low |
| reth | RETH-03 (Sigma Prime) | CREATE allowed for 4844 | Critical |
| reth | RETH-33/34 (Sigma Prime) | RLP header not validated in p2p msgs | Low |
| erigon | #38766 | nil To blob tx panic in encodePayload | Insight |
| bera-reth | BRG4-03 (Sigma Prime) | RLP length validation missing | Critical |

## Detection & Hunt Strategy

1. For every `Decode*` / `decodeOne` / `Unmarshal*` on consensus objects, diff the accept-set
   against geth's `rlp` package: trailing bytes, canonical integer encodings, list headers.
2. Fuzz decoder pairs (target client vs geth) on raw tx/block bytes; any accept/reject mismatch is a finding.
3. For typed txs, compare struct field types against each EIP's MUST-level requirements (nilable vs required).
4. Cross-check every category against EELS/exec-spec reference acceptance tests.

## References

- `reports/eth-l1-clients_findings/38828-bc-low-decode-rlp-of-legacy-transaction-allows-tailing-bytes.md`
- `reports/eth-l1-clients_findings/37462-bc-low-invalid-rlp-decoding-for-single-bytes.md`
- `reports/eth-l1-clients_findings/38766-bc-insight-nil-pointer-dereference-panics-in-encodepayload-of-blob-txs-encoding.md`
- `reports/eth-l1-clients_findings/reth-sigp-2024.md`
- `reports/eth-l1-clients_findings/berachain-reth-geth-sigp-2025.md`
- `reports/eth-l1-clients_findings/chainsafe-gossamer-sigp.md`- `reports/eth-l1-clients_findings/public-audits-reports-berachain-sigma-prime-berachain-reth-geth-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-gossamer-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-obol-sigma-prime-obol-network-charon-security-assessment-report-v2-1-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-reth-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-reth-review-pdf.md`
- EIP-4844 (`to` MUST be present), EIP-2718 (typed envelope), devp2p RLP specs
- Immunefi/audit `37186` [BC-Insight] (erigon, INFO): Missing validation for fixed-size bytes types in ABI parsing — `reports/eth-l1-clients_findings/37186-bc-insight-missing-validation-for-fixed-size-bytes-types-in-abi-parsing.md` (Immunefi (CertiK))
- Immunefi/audit `37359` [BC-Insight] (erigon, INFO): Failure to generate ABI binding in Golang — `reports/eth-l1-clients_findings/37359-bc-insight-failure-to-generate-abi-binding-in-golang.md` (Immunefi (CertiK))
- Immunefi/audit `38277` [BC-Insight] (erigon, INFO): Potential out-of-range panic in UnmarshalJSON() of HexOrDecimal256 — `reports/eth-l1-clients_findings/38277-bc-insight-potential-out-of-range-panic-in-unmarshaljson-of-hexordecimal256.md` (Immunefi (CertiK))
