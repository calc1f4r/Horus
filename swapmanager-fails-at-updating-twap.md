---
# Core Classification
protocol: Morpho
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6926
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - validation

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - hack3r-0m
  - Jay Jonah
  - Christoph Michel
  - Emanuele Ricci
---

## Vulnerability Title

SwapManager fails at updating TWAP

### Overview


This bug report is related to the SwapManagerUniV2.sol file, lines 83-85. The bug is that the update function returns early without updating the TWAP (Time Weighted Average Price) if the elapsed time is past the TWAP period, meaning that the TWAP will forever represent an old value. This could lead to a denial of service attack when claiming rewards, as the wrongly calculated expected amount slippage check will revert.

The recommendation to fix this code is to ensure that at least one full period has passed since the last update. This can be done by changing the "if (timeElapsed >= PERIOD) {" line to "if (timeElapsed < PERIOD) {", and adding "return;" after that. Morpho has fixed this in PR #550, and Spearbit has acknowledged the fix.

### Original Finding Content

## Severity: High Risk

## Context
`SwapManagerUniV2.sol#L83-L85`

## Description
The update function returns early without updating the TWAP if the elapsed time is past the TWAP period. Meaning, once the TWAP period passes, the TWAP is stale and forever represents an old value. This could lead to a denial of service attack when claiming rewards as the wrongly calculated expected amount slippage check reverts.

## Recommendation
Fix the code:

```solidity
// ensure that at least one full period has passed since the last update
- if (timeElapsed >= PERIOD) {
+ if (timeElapsed < PERIOD) {
return;
}
```

## Morpho
Fixed in PR #550

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | hack3r-0m, Jay Jonah, Christoph Michel, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation`

