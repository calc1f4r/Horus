---
# Core Classification
protocol: EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53548
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
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
  - Sigma Prime
---

## Vulnerability Title

beaconChainETHStrategy Queued Withdrawals Excluded From Slashable Shares

### Overview


This bug report discusses an issue with the DelegationManager contract that results in incorrect calculations of burnable shares during operator slashing events. The `_addQueuedSlashableShares()` function excludes `beaconChainETHStrategy` from cumulative scaled shares tracking, which leads to undercounting of burnable shares. This can cause problems in the future when implementing a feature for burning ETH. The recommended solution is to remove the exclusion and properly handle the slashing factor for beacon chain ETH in `EigenPodManager`. The EigenLayer team has resolved this issue in PR #1087.

### Original Finding Content

## Description

DelegationManager excludes `beaconChainETHStrategy` shares in queued withdrawals when calculating burnable shares. This results in undercounting of burnable shares during operator slashing events. 

The `_addQueuedSlashableShares()` function explicitly excludes `beaconChainETHStrategy` from cumulative scaled shares tracking as shown below:

### DelegationManager.sol::_addQueuedSlashableShares()

```solidity
/// @dev Add to the cumulative withdrawn scaled shares from an operator for a given strategy
function _addQueuedSlashableShares(address operator, IStrategy strategy, uint256 scaledShares) internal {
    // @audit beaconChainETHStrategy is excluded from slashable shares tracking
    if (strategy != beaconChainETHStrategy) {
        uint256 currCumulativeScaledShares = _cumulativeScaledSharesHistory[operator][strategy].latest();
        _cumulativeScaledSharesHistory[operator][strategy].push({
            key: uint32(block.number),
            value: currCumulativeScaledShares + scaledShares
        });
    }
}
```

However, the `slashOperatorShares()` function relies on this tracking to calculate slashable shares in the withdrawal queue through `_getSlashableSharesInQueue()`:

### DelegationManager.sol::_getSlashableSharesInQueue()

```solidity
// We want ALL shares added to the withdrawal queue in the window [block.number - MIN_WITHDRAWAL_DELAY_BLOCKS, block.number]
//
// To get this, we take the current shares in the withdrawal queue and subtract the number of shares
// that were in the queue before MIN_WITHDRAWAL_DELAY_BLOCKS.
uint256 curQueuedScaledShares = _cumulativeScaledSharesHistory[operator][strategy].latest();
uint256 prevQueuedScaledShares = _cumulativeScaledSharesHistory[operator][strategy].upperLookup({
    key: uint32(block.number) - MIN_WITHDRAWAL_DELAY_BLOCKS - 1
});
// The difference between these values is the number of scaled shares that entered the withdrawal queue
// less than or equal to MIN_WITHDRAWAL_DELAY_BLOCKS ago. These shares are still slashable.
uint256 scaledSharesAdded = curQueuedScaledShares - prevQueuedScaledShares;
return SlashingLib.scaleForBurning({
    scaledShares: scaledSharesAdded,
    prevMaxMagnitude: prevMaxMagnitude,
    newMaxMagnitude: newMaxMagnitude
});
```

This omission means that when operators are slashed on the `beaconChainETHStrategy`:
1. Queued beacon chain ETH withdrawals are not included in `scaledSharesAdded` calculation.
2. `totalDepositSharesToBurn` will be undercounted.
3. Less shares will be burnable in `EigenPodManager` than intended.

This issue has a low impact as `beaconChainETHStrategy` currently does not have a mechanism for burning ETH. However, it is still important to correctly account for burnable ETH shares so that this feature can be correctly implemented in the future after the Ethereum Pectra upgrade.

## Recommendations

- Remove the `beaconChainETHStrategy` exclusion in `_addQueuedSlashableShares()`.
- Additionally, consider implementing proper slashing factor handling for beacon chain ETH in `EigenPodManager` to account for any beacon chain slashing that would result in less burnable shares.

## Resolution

The EigenLayer team has removed the `beaconChainETHStrategy` exclusion in `_addQueuedSlashableShares()`. This issue has been resolved in PR #1087.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf

### Keywords for Search

`vulnerability`

