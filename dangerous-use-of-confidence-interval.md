---
# Core Classification
protocol: Tsunami GMX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47810
audit_firm: OtterSec
contest_link: https://tsunami.finance/
source_link: https://tsunami.finance/
github_link: https://github.com/Tsunami-Finance/tsunami-contracts

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
finders_count: 3
finders:
  - Robert Chen
  - Woosun Song
  - OtterSec
---

## Vulnerability Title

Dangerous Use Of Confidence Interval

### Overview

See description below for full details.

### Original Finding Content

## Vulnerability Analysis: Pyth Oracle Prices

## Overview
The vulnerability concerns the utilization of Pyth oracle prices and their associated confidence intervals within the `getPrice` function. In Pyth, prices are reported with an associated confidence interval, which reflects the degree of uncertainty. A wider confidence interval indicates a higher level of uncertainty in the reported price data.

## Affected Code

### Solidity Code
```solidity
contracts/core/VaultPriceFeed.sol
function getPrice(address _token, bool _maximise) public override view returns (uint256) {
    uint256 price = getPrimaryPrice(_token, _maximise);
    /* .. */
    return price;
}

function getPrimaryPrice(address _token, bool _maximise) public override view returns (uint256) {
    /* ... */
    uint256 price = 0;
    if (_maximise) {
        price = uint256(priceStruct.price).add(uint256(priceStruct.conf));
    } else {
        price = uint256(priceStruct.price).sub(uint256(priceStruct.conf));
    }
    // normalise price precision
    return price.mul(PRICE_PRECISION).div(10 ** uint256(-priceStruct.expo));
}
```

## Problem Description
The `getPrice` function calculates two adjusted prices, where `priceStruct.conf` is either added or subtracted from the base price. The issue arises when the difference between the maximum and minimum prices is significantly large due to a wide confidence interval. Thus, a user’s position may experience loss or liquidation even if the index price has not decreased, as it will incur a deterministic loss of `conf * 2 * position size`, resulting in unnecessary loss of assets for the user.

## Remediation
To mitigate this issue, incorporate a mechanism to reject prices with excessively wide confidence intervals.

## Patch
The issue is fixed in commit `18460e8`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Tsunami GMX |
| Report Date | N/A |
| Finders | Robert Chen, Woosun Song, OtterSec |

### Source Links

- **Source**: https://tsunami.finance/
- **GitHub**: https://github.com/Tsunami-Finance/tsunami-contracts
- **Contest**: https://tsunami.finance/

### Keywords for Search

`vulnerability`

