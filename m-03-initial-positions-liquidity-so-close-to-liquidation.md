---
# Core Classification
protocol: StakeDAO_2025-07-21
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63602
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/StakeDAO-security-review_2025-07-21.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.20
financial_impact: medium

# Scoring
quality_score: 1
rarity_score: 2

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-03] Initial position's liquidity so close to liquidation

### Overview


This bug report discusses an issue with the Morpho Blue market system, where after deployment, a position is automatically created that is too close to liquidation. This means that the position is at risk of being liquidated immediately, which could result in a loss of funds. The report suggests that the system should create positions at a lower loan-to-value (LTV) point, rather than the current liquidation-to-value (LLTV) point. This will help to reduce the risk of immediate liquidation and protect users' funds.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

Currently, after deployment and creation Morpho Blue market system directly opens a position. But this position is so close to liquidation, and it can be liquidated immediately. 

```solidity
        uint256 collateralToSupply = Math.mulDiv(
            Math.mulDiv(borrowAmount, 10 ** oracle.ORACLE_BASE_EXPONENT(), oracle.price(), Math.Rounding.Ceil),
            1e18,
            lltv,
            Math.Rounding.Ceil
        );
        uint256 buffer = 2 * (10 ** (collateral.decimals() - loan.decimals()));
        collateralToSupply += buffer;
```

In here, only 2 wei of additional collateral is added. Most probably, it can be liquidated in the next block because of interest accrual. 

## Recommendations

As all the lending protocols did, create a position at LTV point not LLTV point. ( We don't have LTV in Morpho ). If 90% is LLTV level, 85% can be a good LTV level for the initial position.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 1/5 |
| Rarity Score | 2/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | StakeDAO_2025-07-21 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/StakeDAO-security-review_2025-07-21.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

