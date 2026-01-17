---
# Core Classification
protocol: Gooserun V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44073
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/GooseRun-V1-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[M-01] Short Lookback Period in `createTokenManager()` Function

### Overview


This bug report discusses an issue with the `createTokenManager` function in the `LaunchFactory.sol` file. The function specifies a 30-second lookback period for calculating the Time-Weighted Average Price (TWAP), which can lead to unstable TWAP values and potential price manipulation. The team has fixed the issue by increasing the lookback period to 2 minutes. 

### Original Finding Content

## Severity

Medium Risk

## Description

The `createTokenManager` function specifies a **30-seconds lookback period** for calculating the Time-Weighted Average Price (TWAP) when creating a new pool through the `createPermissioned` function.

```solidity
IMaverickV2Pool pool = factory.createPermissioned(
    0,
    0,
    TICK_SPACING,
    uint32(30 seconds), seconds
    tokenIsA ? _tempLaunchData.token : quoteToken,
    tokenIsA ? quoteToken : _tempLaunchData.token,
    tokenIsA ? lens.lastTick() : -lens.lastTick(),
    1, // 1 => only mode static in pool
    address(swapper),
    false,
    true
);
```

The lookback period is critical in determining TWAP, which smooths price volatility and helps ensure price accuracy over time. A 30-second lookback period is excessively short and can lead to unstable TWAP values.

## Impact

A short TWAP lookback window heightens exposure to rapid price changes, enabling potential price manipulation.

## Location of Affected Code

File: [`src/LaunchFactory.sol#L143`](https://github.com/fairlaunchrc/fairlaunch_contracts/blob/cb3b10370a029e39694dde45c51027bfb5b1cf75/src/LaunchFactory.sol#L143)

## Recommendation

Consider increasing the lookback period.

## Team Response

Fixed, the lookback period was set to 2 minutes.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Gooserun V1 |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/GooseRun-V1-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

