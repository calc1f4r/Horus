---
# Core Classification
protocol: Initia_2025-06-17
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61450
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Initia-security-review_2025-06-17.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-20] Missing curve validation in `encodeEthSecp256k1Pubkey`

### Overview

See description below for full details.

### Original Finding Content


In packages/widget-react/src/data/patches/encoding.ts, the function `encodeEthSecp256k1Pubkey` function performs basic structural validation (33-byte length and `0x02/0x03` prefix) but does not cryptographically verify that the public key represents a valid point on the secp256k1 curve. While this doesn't pose an immediate security risk in the current implementation, it could lead to:

- Downstream Processing Issues: Some libraries may behave unpredictably when given invalid curve points.
- UI Confusion: Wallet interfaces might display incorrect derived addresses for malformed keys.

```
// packages/widget-react/src/data/patches/encoding.ts
export function encodeEthSecp256k1Pubkey(pubkey: Uint8Array): EthSecp256k1Pubkey {
  if (pubkey.length !== 33 || (pubkey[0] !== 0x02 && pubkey[0] !== 0x03)) {
    throw new Error(
      "Public key must be compressed secp256k1, i.e. 33 bytes starting with 0x02 or 0x03",
    )
  }
  return {
    type: pubkeyTypeInitia.ethsecp256k1,
    value: toBase64(pubkey),
  }
}
```
Risk Context
This is primarily a defensive improvement rather than a critical fix.
The current implementation is safe when:
Keys come from trusted sources (wallets/key generators).
Downstream systems properly validate keys.

The main benefits are:
Earlier detection of malformed keys.
More predictable behavior across different client implementations.

**Recommendation** 
For defense-in-depth, consider adding cryptographic validation using `@noble/secp256k1`:
```
import { Point } from "@noble/secp256k1";
import { toBase64 } from "@cosmjs/encoding";

export function encodeEthSecp256k1Pubkey(pubkey: Uint8Array): EthSecp256k1Pubkey {
  // 1. Structural checks
  if (pubkey.length !== 33 || (pubkey[0] !== 0x02 && pubkey[0] !== 0x03)) {
    throw new Error("Invalid compressed secp256k1 key format");
  }

  // 2. Cryptographic validation
  try {
    // Throws if:
    // - X-coordinate is >= curve field size
    // - Point is not on the curve
    // - Point is at infinity
    Point.fromHex(pubkey);
  } catch (err) {
    throw new Error(`Invalid secp256k1 public key: ${err.message}`);
  }

  return {
    type: pubkeyTypeInitia.ethsecp256k1,
    value: toBase64(pubkey),
  };
}
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Initia_2025-06-17 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Initia-security-review_2025-06-17.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

