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
solodit_id: 21366
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

Incorrect SARimplementation

### Overview


This bug report is about an incorrect implementation of the opSAR command in zkevm-rom:comparison.zkasm#L488. In the case where A is negative (sign bit is 1), the result from SHRarithBit is incorrectly corrected by negation (0 - A). A counter example of this bug is sar(0x80...01, 1) which should give 0xc0..00 but instead gives 0xc0..01. Tests have been disabled to uncover this bug. 

The correct implementation of SAR in the case of A being negative would be NOT(SHR(NOT(A), D)) (A is the number to shift, D is the amount of bits to shift by), where NOT is bitwise negation, not arithmetic negation as in the current implementation. The implementation could use XOR and the sign bit to conditionally negate.

The bug has been fixed in PR #211 and a test has been added in PR #165. The bug has been acknowledged by Spearbit.

### Original Finding Content

## Severity: Critical Risk

## Context
`zkevm-rom:comparison.zkasm#L488`

## Description
The implementation of `opSAR` is incorrect. In case `A` is "negative" (sign bit is 1), the correction of the result from `SHRarithBit` is incorrectly done by negation (`0 - A`).

### Counter Example
`sar(0x80...01, 1)` gives `0xc0..01` instead of `0xc0..00`:
- `sign(A) == 1`
- `abs(A) == 0x7f..ff`
- `abs(A) >> 1 == 0x3f..ff`
- `0 - (abs(A) >> 1) == 0xc0..01`

These tests should uncover the bug, but they are disabled:
- [ FAILED ] `stShift.shiftCombinations`
- [ FAILED ] `stShift.shiftSignedCombinations`

## Recommendation
The correct implementation of `SAR` in the case of `A` being negative would be:
```
NOT(SHR(NOT(A), D))
```
where `NOT` is bitwise negation, not arithmetic negation as in the current implementation.

We could use `XOR` and the sign bit to conditionally negate. If `E` contains the sign bit, then this would be (using functional and assignment notation):
```
MASK = SUB(0, E)
RESULT = XOR(SHR(XOR(A, MASK), D), MASK)
```

## Acknowledgments
- **Polygon-Hermez**: Fixed in PR #211 and test added in PR #165.
- **Spearbit**: Acknowledged.

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

