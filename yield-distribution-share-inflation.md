---
# Core Classification
protocol: Plume Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53271
audit_firm: OtterSec
contest_link: https://plumenetwork.xyz/
source_link: https://plumenetwork.xyz/
github_link: https://github.com/plumenetwork/contracts

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
finders_count: 3
finders:
  - Nicholas R. Putra
  - Robert Chen
  - Renato Eugenio Maria Marziano
---

## Vulnerability Title

Yield Distribution Share Inflation

### Overview


The bug report is about an issue with the receiveYield function in the YieldToken contract. This function increases the yieldPerTokenStored and the total currencyToken held by the contract. However, there is a problem with this mechanism, as it causes unintended share value inflation when users deposit currencyToken as yield. This means that users receive more value than they should. To fix this issue, the yield distribution process needs to be separated to prevent direct inflation of share value. This has been resolved in the latest patch.

### Original Finding Content

## Issue Overview

The issue concerns how `receiveYield` in `YieldToken` interacts with the contract’s accounting, specifically the mechanism used to track user share values relative to the underlying assets. In the current implementation, when `receiveYield` is called, it increases both the `yieldPerTokenStored` and the total `currencyToken` held by the `YieldToken` contract.

## Code Snippet

```solidity
> _ smart-wallets/src/token/YieldToken.sol solidity
function receiveYield(IAssetToken assetToken, IERC20 currencyToken, uint256 currencyTokenAmount) external {
    [...]
    _depositYield(currencyTokenAmount);
}
```

```solidity
> _ smart-wallets/src/token/YieldDistributionToken.sol solidity
function _depositYield(uint256 currencyTokenAmount) internal {
    [...]
    if (currentSupply > 0) {
        [...]
        $.yieldPerTokenStored += currencyTokenAmount.mulDiv(SCALE, divisor);
    }
    [...]
    $.currencyToken.safeTransferFrom(_msgSender(), address(this), currencyTokenAmount);
    emit Deposited(_msgSender(), currencyTokenAmount);
}
```

## Problem Description

However, there is an oversight in this mechanism. When depositing `currencyTokenAmount` as yield, the `totalAssets` held by the contract increase. This creates a dual effect where users not only receive their intended yield but also experience unintended share value inflation due to the share-to-asset conversion dependency. As a result, users receive more value than they are entitled to.

## Remediation

Separate the yield distribution process to prevent direct inflation of share value.

## Patch

Resolved in commit `223af8d`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Plume Network |
| Report Date | N/A |
| Finders | Nicholas R. Putra, Robert Chen, Renato Eugenio Maria Marziano |

### Source Links

- **Source**: https://plumenetwork.xyz/
- **GitHub**: https://github.com/plumenetwork/contracts
- **Contest**: https://plumenetwork.xyz/

### Keywords for Search

`vulnerability`

