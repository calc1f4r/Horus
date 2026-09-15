---
# Core Classification
protocol: Ouroboros_2024-12-06
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45949
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Ouroboros-security-review_2024-12-06.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

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

[M-01] TCR is overestimated on redemptions

### Overview


This bug report discusses a problem with the system's use of different price types for different operations. Specifically, the report highlights an issue with the use of the highest price for redemptions, which can result in an overestimation of the Total Collateral Ratio (TCR) and allow redemptions even when the real TCR is below the Minimum Collateral Ratio (MCR). The report recommends using the lowest or weighted average price instead to calculate the TCR. This bug is considered to have a medium impact and likelihood.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The system uses different price types (lowest, highest, and weighted average) depending on the nature of the operation. As such, in some operations, the most conservative price from the point of view of the protocol safety is used.

For example, using the lowest price for debt creation makes sure that the amount of debt created is not higher than it should be.

In the same way, using the highest price for redemptions makes sure that the amount of collateral withdrawn from the protocol is not higher than it should be. However, on `redeemCollateral` this same price is also used to check if the TCR is above the MCR. So using the highest price can overestimate the TCR and, consequently, allow redemptions when the real TCR is below the MCR.

```solidity
File: PositionManager.sol

423:  @>    (totals.price, totals.suggestedAdditiveFeePCT) = priceFeed.fetchHighestPriceWithFeeSuggestion(
424:            totals.loadIncrease,
425:            totals.utilizationPCT,
426:            true,
427:            true
428:        );
429:
430:        _requireValidMaxFeePercentage(totals.maxFeePCT, totals.suggestedAdditiveFeePCT);
431:
432:        uint MCR = collateralController.getMCR(address(collateralToken), totals.version);
433:  @>    _requireTCRoverMCR(totals.price, MCR);
```

## Recommendations

Use the lowest or weighted average price to calculate the TCR.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ouroboros_2024-12-06 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Ouroboros-security-review_2024-12-06.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

