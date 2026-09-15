---
# Core Classification
protocol: Polygon zkEVM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21363
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/PolygonzkEVM-Protocol/zkEVM-engagement-1-Spearbit-27-March.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/PolygonzkEVM-Protocol/zkEVM-engagement-1-Spearbit-27-March.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 8
finders:
  - Thibaut Schaeffer
  - Alex Beregszaszi
  - Lucas Vella
  - Miguel Palhas
  - Paweł Bylica
---

## Vulnerability Title

Memory alignment malleability

### Overview


This bug report is about the constant polynomial BYTE_C4096 not wrapping around after value 255. This could allow inVto have values above a byte, which may carry over and cause an MSTORE8 to write a 1 before the given byte in memory. This could be exploited by malicious block builders to cause users to lose or gain value in transactions such as AMM transactions or other kinds of swaps.

The recommendation to fix this bug is to wrap around after value 255. This was fixed in PR #116, which was acknowledged.

In summary, this bug report is about the constant polynomial BYTE_C4096 not wrapping around after value 255, which could be exploited by malicious block builders to cause users to lose or gain value in transactions. The recommendation to fix this bug is to wrap around after value 255, which was fixed in PR #116 and acknowledged.

### Original Finding Content

## Severity: Critical Risk

## Context
`zkevm-proverjs:sm_mem_align.js#L14`

## Description
The constant polynomial `BYTE_C4096` does not wrap around after value 255 as it should, allowing `inV` to have values above a byte, which may carry over and cause an `MSTORE8` to write a 1 before the given byte in memory.

## Background
Solidity code generation always tries to align memory offsets (such as allocation is done at word-boundaries) and many other projects writing inline assembly are encouraged to do so. However, some people optimizing for gas do not adhere to this, and it cannot be known for certain that no unaligned case exists in Solidity’s code generator.

Now imagine if "fake value" insertion is possible in unaligned `MLOAD`s; that means a malicious block builder could make a user lose or gain value in, for example, an AMM transaction or other kinds of swaps. Such transactions could be sandwiches to extract value. Cases of unaligned reads could be easily mapped out by transaction tracing, and "searchers" could build up a database of proof patterns to modify for the automatic execution of such malicious trades.

## Recommendation
Wrap around after value 255.

```javascript
@@ -11,7 +11,7 @@ const CONST_F = {
BYTE2B: (i) => (i & 0xFF), // [0..255]
// 0 (x4096), 1 (x4096), ..., 255 (x4096), 0 (x4096),
- BYTE_C4096: (i) => (i >> 12), // [0:4096..255:4096]
+ BYTE_C4096: (i) => (i >> 12) & 0xFF, // [0:4096..255:4096]
// 0 - 1023 WR256 = 0 WR8 = 0 i & 0xC00 = 0x000
// 1024 - 2047 WR256 = 0 WR8 = 0 i & 0xC00 = 0x400
```

## Polygon-Hermez
Fixed in PR #116.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Polygon zkEVM |
| Report Date | N/A |
| Finders | Thibaut Schaeffer, Alex Beregszaszi, Lucas Vella, Miguel Palhas, Paweł Bylica, Christian Reitwiessner, Andrei Maiboroda, Leo Alt |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/PolygonzkEVM-Protocol/zkEVM-engagement-1-Spearbit-27-March.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/PolygonzkEVM-Protocol/zkEVM-engagement-1-Spearbit-27-March.pdf

### Keywords for Search

`vulnerability`

