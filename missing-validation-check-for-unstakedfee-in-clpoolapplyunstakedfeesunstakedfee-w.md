---
# Core Classification
protocol: Velodrome Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29643
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review-Nov23.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review-Nov23.pdf
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

protocol_categories:
  - dexes
  - services
  - yield_aggregator
  - synthetics
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Jeiwan
  - Alex The Entreprenerd
  - Optimum
  - D-Nice
---

## Vulnerability Title

Missing validation check for unstakedFee in CLPool.applyUnstakedFees/unstakedFee , which might

### Overview

See description below for full details.

### Original Finding Content

## Vulnerability Report

## Be More Than 100%
**Severity:** Low Risk  
**Context:** CLPool.sol#L919  

### Description
`unstakedFee` returns a value that is used in the context of percentage, i.e., there is an implicit assumption that the return value should be `<= 1_000_000` while in reality, this is not enforced in the code and thus may cause an underflow in the value of `unstakedFeeAmount`, which will totally corrupt the values of `feeGrowthGlobal0X128`, `feeGrowthGlobal1X128`, `gaugeFees.token0`, and `gaugeFees.token1`.

### Recommendation
Consider adding a validation check to ensure `unstakedFee` returns a value that is `<= 1_000_000`; otherwise, either revert or use a default value instead.

### Fix Implementation
**Velodrome:** The fix has been applied in commit `4baded78` and now `getUnstakedFee()` cannot return values greater than `1_000_000`.

**Spearbit:** Fixed in commit `4baded78` by implementing the recommendation and adding a default value.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Velodrome Finance |
| Report Date | N/A |
| Finders | Jeiwan, Alex The Entreprenerd, Optimum, D-Nice |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review-Nov23.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review-Nov23.pdf

### Keywords for Search

`vulnerability`

