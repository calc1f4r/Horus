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
solodit_id: 21364
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

Incorrect BYTE implementation

### Overview


This bug report discusses an issue with the argument range check for the InopBYTE function in the zkevm-rom:comparison.zkasm code. The check only covers B0, but if any of B1-B7 are non-zero, the result of opBYTE should be 0. This is demonstrated with a counter example, where A is 0xa0a1a2a3a4a5a6a7a8a9b0b1b2b3b4b5b6b7b8b9c0c1c2c3c4c5c6c7c8c9d0d1 and B is 0x100000001, with B0 = 1 and B1 = 1. The result should be 0, but is 0xa0. This case is not covered by the Ethereum State Tests, but is covered in unit tests like evmone. The recommendation is to use SUB, which was fixed in PR #211 and specific tests added in PR #165. Spearbit acknowledged the bug.

### Original Finding Content

## Severity: Critical Risk

## Context
`zkevm-rom:comparison.zkasm#L345`

## Description
InopBYTE, the argument range check `31 - B => D :JMPN(opBYTE0)` is incorrect because this only checks `B0`. If any of `B1–B7` are non-zero, the result of `opBYTE` must be `0` but may be another value in this implementation.

### Counter example:
- A = `0xa0a1a2a3a4a5a6a7a8a9b0b1b2b3b4b5b6b7b8b9c0c1c2c3c4c5c6c7c8c9d0d1`
- B = `0x100000001`, i.e. `B0 = 1`, `B1 = 1`
- The result should be `0` but is `0xa0`.

This case or similar are not covered by the Ethereum State Tests, but various implementations cover it via unit tests (like evmone).

## Recommendation
Use `SUB`.

## Polygon-Hermez
Fixed in PR #211 and specific tests added in PR #165.

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

