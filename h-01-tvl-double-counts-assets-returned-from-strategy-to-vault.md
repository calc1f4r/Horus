---
# Core Classification
protocol: Elytra_2025-07-10
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63544
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Elytra-security-review_2025-07-10.md
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

[H-01] TVL double-counts assets returned from strategy to vault

### Overview


The bug report states that when assets are allocated to a strategy, there is an issue where the same tokens are counted twice in the total value locked (TVL) calculations. This is because the tokens are counted once in the deposit pool's strategy allocation and again in the vault's claimable assets. The report recommends adjusting the values when the receiveFromStrategy function is triggered to avoid this double-counting issue.

### Original Finding Content


_Resolved_

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

When assets are allocated to a strategy, `ElytraDepositPoolV1.assetsAllocatedToStrategies[asset]` is incremented. Later, the strategy can return funds to the unstaking vault via:

```solidity
    /// @notice Receives assets from strategy for withdrawal processing
    /// @param asset Asset address
    /// @param amount Amount received
    function receiveFromStrategy(address asset, uint256 amount) external onlyStrategy {
        claimableAssets[asset] += amount;
        emit AssetsReceivedFromStrategy(asset, amount);
    }
```

However, this would create a double-counting problem in the TVL calculations since the same tokens would end up counted twice 
1. In the deposit pool’s strategy allocation (`assetsAllocatedToStrategies[asset]`).
2. In the vault’s claimable assets (`claimableAssets[asset]`).

Since `getTotalAssetTVL` sums both values, the returned strategy assets inflate TVL improperly.

## Recommendations

Consider decreasing the `assetsAllocatedToStrategies` and the `assetStrategyAllocations` of `ElytraDepositPoolV1`, when `receiveFromStrategy` is being triggered.





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Elytra_2025-07-10 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Elytra-security-review_2025-07-10.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

