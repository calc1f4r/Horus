---
vulnerability_class: snappy_decompression_dos
title: "Snappy Compression/Framing: checksum skipping and non-minimal-length divergence (Lodestar / Nimbus)"
protocol: eth-l1-clients
category: P2P Networking / Compression
vulnerability_type: input_validation
attack_type: integrity_check_bypass|spec_divergence|resource_waste
affected_component: reqresp_encoding|gossip_decoding|snappy_framing
chain: ethereum
severity: medium
impact: corrupted_message_acceptance|peer_eclipse|wasted_compute|network_partition
severity_range: "LOW to MEDIUM"
source: Immunefi Ethereum Protocol Attackathon 2024-2025

primitives:
  - uncompressed_chunk_checksum_not_verified
  - non_minimal_varint_length_accepted_or_rejected
  - corrupted_gossip_deserialization_cost

affected_components:
  - ssz_snappy req/resp encoding strategies
  - gossipsub message decoders
  - snappy frame reader

tags:
  - snappy
  - compression
  - lodestar
  - nimbus
  - consensus
  - p2p
  - integrity
  - attackathon

total_reports_analyzed: 2

# Pattern Identity (Required)
root_cause_family: missing_integrity_check_in_decoder
pattern_key: snappy_framing_gap | checksum_or_canonical_length_gap | corrupted_message_acceptance

# Interaction Scope
interaction_scope: network_facing_decoder

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - uncompress
  - getChunkType
  - getFrameSize
  - checksumSize
  - crc
  - chunkTypeUncompressedData
  - varint
  - minEnc
  - decodeFramed
---

# Snappy Decompression DoS / Divergence (Lodestar / Nimbus)

## Overview

All eth2 req/resp and gossip messages are ssz_snappy-encoded: snappy framing compression over SSZ.
Two Attackathon findings show the same class from opposite directions:

1. **Lodestar skips the CRC checksum on uncompressed snappy chunks** (#37246, Low) — a corrupted or
   tampered message decodes without error, breaking message integrity guarantees and enabling
   eclipse-style manipulation (peer feeds subtly corrupted data that other clients would reject).
2. **Nimbus rejects non-minimally-encoded snappy data lengths due to spec ambiguity** (#37594,
   Insight) — over-verbose but semantically valid varint lengths are rejected, a divergence from
   other libp2p stacks; non-minimal encodings from an honest-but-quirky peer cause spurious
   disconnects, and in the mirror direction an accepting client diverges from Nimbus.

**Root Cause Statement**: This vulnerability exists because snappy framing decoders implement the
framing spec asymmetrically — skipping mandatory CRC verification (Lodestar) or enforcing
non-spec-mandated canonical varint lengths (Nimbus) — so corrupted/non-canonical messages are
accepted or valid messages rejected, diverging from the libp2p reference behavior.

**Observed Frequency**: rare-but-recurring (2 accepted reports across the two major alt-language clients)
**Consensus Severity**: LOW to MEDIUM

---

#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_integrity_check_in_decoder (snappy checksum/varint canonicality)"
- Pattern key: `snappy_framing_gap | checksum_or_canonical_length_gap | corrupted_message_acceptance`
- Interaction scope: `network_facing_decoder`
- Primary affected component(s): `reqresp_encoding`, `gossip_decoding`
- High-signal code keywords: `uncompress`, `crc`, `chunkTypeUncompressedData`, `varint`
- Typical sink / impact: `corrupted_message_acceptance` / `spurious_disconnect`
- Validation strength: `high` (reference code diff vs golang/snappy shown in report)

#### Contract / Boundary Map

- Entry surface(s): libp2p req/resp streams, gossipsub topics (ssz_snappy)
- Contract hop(s): `frame -> chunk type -> [checksum] -> decompress -> SSZ decode`
- Trust boundary crossed: `unauthenticated remote peer`
- Shared state or sync assumption: `all clients agree on framing validity`

#### Valid Bug Signals

- Signal 1: Uncompressed-chunk branch (chunk type 0x01) reads payload without comparing stored CRC to `crc(decoded)` (golang/snappy `decode.go#L176` enforces)
- Signal 2: Length varint parser rejects encodings with redundant trailing zero groups that other stacks accept (or vice-versa: accepts what reference rejects)
- Signal 3: Decoder returns success on frames where checksum bytes are absent but chunk length covers them

#### False Positive Guards

- Not this bug when: only *compressed* chunks (type 0x00) are handled leniently AND spec marks checksum optional there (it doesn't — framing checksums are mandatory per snappy framing format §4.2/4.3)
- Safe if: every chunk type path verifies CRC before yielding bytes
- Requires attacker control of: any libp2p connection/topic membership — trivial
- Distinguish from #38318 (gossipsub zero-weight penalty): that's scoring, not decoding

## Real Reports

### 1. Immunefi #37246 [BC-Low] — lodestar snappy checksum issue (gln)

Report: `reports/eth-l1-clients_findings/37246-bc-low-lodestar-snappy-checksum-issue.md`

Lodestar `uncompress()` (`packages/reqresp/src/encodingStrategies/sszSnappy/snappyFrames/uncompress.ts`)
iterates framed chunks but does not verify the CRC-32 checksum prefixed to uncompressed chunks,
unlike the golang/snappy reference which returns `ErrCorrupt` on mismatch. Impact classification
filed under "permanent chain split ≥25% requiring hard fork" — i.e., a peer can feed corrupted
messages that Lodestar accepts and other clients reject.

### 2. Immunefi #37594 [SC-Insight] — Nimbus incorrectly rejects non-minimally encoded snappy data lengths (spec ambiguity)

Report: `reports/eth-l1-clients_findings/37594-sc-insight-nimbus-incorrectly-rejects-non-minimally-encoded-snappy-data-lengths-due-to-spec.md`
NOTE: local file is a GitBook 404-stub capture (content moved to `...spec.-a.md` upstream); title,
ID and classification retained from the raw index. Core claim: Nimbus' snappy length varint parser
requires minimal encodings where the framing spec is ambiguous, rejecting messages other stacks accept.

### Related (decode-cost amplifier)

**#38318** gossipsub zero topic weight (`DB/eth-l1-clients/p2p/gossipsub-malformed-message.md`):
corrupted-snappy gossip is *also* unpenalized in Nimbus, compounding the wasted-deserialization cost.

## Vulnerable Code Pattern (generic)

```ts
// VULNERABLE: no checksum verification on uncompressed chunk (lodestar #37246)
uncompress(chunk: Uint8ArrayList): Uint8ArrayList | null {
  const type = getChunkType(this.buffer.get(0));
  const frameSize = getFrameSize(this.buffer);
  if (type === CHUNK_UNCOMPRESSED) {
    const data = this.buffer.sublist(4, frameSize); // skips 4-byte CRC
    result.append(data);                            // no crc(data) == stored check
  }
}
```

## Detection & Hunt Strategy

1. For each non-Go client, locate the snappy frames decoder and grep the uncompressed-chunk branch
   for CRC verification; compare byte-for-byte with `github.com/golang/snappy` decode.go.
2. Fuzz the length-varint parser with redundant encodings (`0x80 0x00`-style continuations) and
   diff accept/reject across ≥2 clients.
3. Cross-check gossip topic decoders — a checksum-bypassed frame that reaches SSZ decode is
   attacker-compute amplification even when the SSZ layer later rejects it.

## References

- `reports/eth-l1-clients_findings/37246-bc-low-lodestar-snappy-checksum-issue.md`
- `reports/eth-l1-clients_findings/37594-sc-insight-nimbus-incorrectly-rejects-non-minimally-encoded-snappy-data-lengths-due-to-spec.md` (404-stub)
- golang/snappy framing spec §4.2–4.3 (mandatory per-chunk CRC)
- libp2p ssz_snappy encoding notes
