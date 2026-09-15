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
solodit_id: 21368
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

Underconstrained carry value in the binary state machine

### Overview


This bug report is about an issue with the zkevm-proverjs:binary.pil program, which is a critical risk. The problem is that the value of cIn can be set arbitrarily by the prover when RESET is 1, allowing the prover to prove that 0 + 0 == 1 by setting cInto 1. The issue can be exploited by changing the PIL constraint over cIn in the binary.pil file. The new constraint is that cIn equals cOut multiplied by 1 minus RESET. This change will ensure that when RESET is 1, cIn will be 0. The bug has been fixed in PR #137 and acknowledged by Spearbit.

### Original Finding Content

## Severity: Critical Risk

### Context
zkevm-proverjs:binary.pil

### Description
The value of `cIn` can be set arbitrarily by the prover when `RESET` is `1`. As a result, the prover can prove that `0 + 0 == 1` by setting `cIn` to `1`.

The issue can be exploited as follows, for example for the first operation in the binary state machine:

```javascript
// sm_binary.js:337
+ pols.cIn[0] = 1n;
```

### Recommendation
Change the PIL constraint over `cIn`:

```pil
// binary.pil:82
- cIn '* (1 - RESET) = cOut * ( 1 - RESET ')
+ cIn '= cOut * ( 1 - RESET ')
```

With this change `(RESET == 1) => (cIn == 0)`.

### Acknowledgment
- Polygon-Hermez: Fixed in PR #137.
- Spearbit: Acknowledged.

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

