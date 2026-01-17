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
solodit_id: 63405
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/RegnumAurum-security-review_2025-08-12.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
rarity_score: 1

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-03] Protocol misses fees from borrowing positions

### Overview


The bug report states that there is an issue with the protocol always subtracting a protocol fee rate when calculating interest rates for liquidity providers. However, these funds are never minted or allocated, meaning that borrowers are paying for these fees but nobody is receiving them, including lenders. This can result in a situation where there are funds in the system even if all borrowers pay for their positions and lenders withdraw all their funds. The report recommends allocating or minting these funds to the fee recipient in order to properly gather fees from borrowing positions.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

Protocol always subtracts protocol fee rate while calculation of interest rate for liquidity providers, but it never mints or allocate these funds. It means borrowers pay for these fees too, but nobody receives these funds, including lenders.

It means even if all the borrowers pay for their positions and then lenders withdraw 100% of the funds, there will be funds in the system.

```solidity
    function calculateLiquidityRate(uint256 utilizationRate, uint256 usageRate, uint256 protocolFeeRate, uint256 totalDebt) internal pure returns (uint256) {
        if (totalDebt < 1) {
            return 0;
        }

        uint256 grossLiquidityRate = utilizationRate.rayMul(usageRate);
        uint256 protocolFeeAmount = grossLiquidityRate.rayMul(protocolFeeRate);
@>      uint256 netLiquidityRate = grossLiquidityRate - protocolFeeAmount;

        return netLiquidityRate;
    }
```

## Recommendations

Allocate/mint these funds to the fee recipient in order to gather fees from borrowing positions.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 1/5 |
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

