---
# Core Classification
protocol: DRAFT
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29881
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/report-blast-contracts-review-draft.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/report-blast-contracts-review-draft.pdf
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
finders_count: 4
finders:
  - Milo Truck
  - Christoph Michel
  - Csanuragjain
  - Desmond Ho
---

## Vulnerability Title

Non-zero Maker's PSM buyGem() fee will cause DAI !USDC swaps to fail

### Overview

See description below for full details.

### Original Finding Content

## Security Risk Report

## Severity
**Low Risk**

## Context
`USDConversions.sol#L78`

## Description
Maker's PSM has a fee mechanism (currently zero both ways). The amount specified for `PSM.buyGem()` is the USDC receivable, but the fee charged out is in DAI. Hence, the amount of DAI pulled will be greater than `inputAmount` if `tout` is non-zero. This could pose an issue for `YieldManager.convert()` that might perform DAI to USDC swaps, where the requested USDC amount will be too high since it assumes a 1:1 conversion with zero fee.

## Recommendation
Swap to using `minOutputAmount` instead of `inputAmount`. The drawback with this method is that there could be remaining `inputAmount` since one is specifying exact output instead of expending the entire input.

```diff
- PSM.buyGem(address(this), _wadToUSD(inputAmount));
+ PSM.buyGem(address(this), minOutputAmount);
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | DRAFT |
| Report Date | N/A |
| Finders | Milo Truck, Christoph Michel, Csanuragjain, Desmond Ho |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/report-blast-contracts-review-draft.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/report-blast-contracts-review-draft.pdf

### Keywords for Search

`vulnerability`

