---
# Core Classification
protocol: RegnumAurum_2025-08-12
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63401
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/RegnumAurum-security-review_2025-08-12.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-01] Parameter change skews getters

### Overview


This bug report discusses an issue with the calculation of interest accrual in a program. The problem occurs when the program uses the last calculated variables for updating reserve state, which can result in incorrect values being returned in certain functions. This can have a significant impact on the program and is considered a high severity bug. The report recommends not calculating certain rates in specific functions and instead using a cached version to avoid this issue.

### Original Finding Content


_Resolved_

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

Interest accrual is always calculated using the last calculated variables for updating reserve state. For instance, if interest was 5% lastly and after 1 hour we call `deposit` function, it will use this 5% interest for the last 1 hour. However, `getNormalizedIncome` and `getNormalizedDebt` functions calculate these rates again return value according to that.

This will cause incorrect value to be returned in these functions. It's very critical because `getNormalizedIncome` and `getNormalizedDebt` are used in many important points in the codebase.

```solidity
// Reserve update

        reserve.liquidityIndex = calculateLiquidityIndex( 
            rateData.currentLiquidityRate,
            timeDelta,
            reserve.liquidityIndex
        );

        // Update usage index (debt index) using compounded interest
        reserve.usageIndex = calculateUsageIndex(
            rateData.currentUsageRate,
            timeDelta,
            reserve.usageIndex
        );
```

```solidity
// Normalized income

    function getLiquidityIndex(ReserveData storage reserve, ReserveRateData storage rateData) internal view returns (uint256) {
        uint256 timeDelta = block.timestamp - uint256(reserve.lastUpdateTimestamp);
        if(timeDelta < 1) {
            return reserve.liquidityIndex;
        }

        return calculateLiquidityIndex(
            calculateLiquidityRate(rateData.currentUtilizationRate, rateData.currentUsageRate, rateData.protocolFeeRate, reserve.totalUsage),
            timeDelta,
            reserve.liquidityIndex
        );
    }
```

As you can see, it calculates the liquidity rate again in here. Only `protocolFeeRate` can change and can have different actual value here. It means if protocol changes protocol fee, it will return an incorrect value for normalized income.

> Note: Same situation happens in debt for different parameter changes.


## Recommendations

Do not calculate liquidity rate or usage rate in `getNormalizedIncome` and `getNormalizedDebt` instead, use the cached version.





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | RegnumAurum_2025-08-12 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/RegnumAurum-security-review_2025-08-12.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

