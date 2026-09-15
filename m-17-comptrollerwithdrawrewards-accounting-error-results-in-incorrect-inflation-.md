---
# Core Classification
protocol: Union Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3588
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/11
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-union-finance-judging/issues/26

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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - lemonmon
  - Lambda
  - dipp
  - Jeiwan
---

## Vulnerability Title

M-17: `Comptroller::withdrawRewards` accounting error results in incorrect inflation index

### Overview


This bug report is about the accounting error in `Comptroller::withdrawRewards` which results in incorrect inflation index. It was found by Jeiwan, Lambda, dipp, and lemonmon using manual review. The issue is that in `Comptroller:withdrawRewards` calls `_getUserManagerState` and saves it as `userManagerState` which returns the value of `userManager.totalStaked() - userManager.totalFrozen()`, however, in the `Comptroller::withdrawRewards` function, the returned value `userManagerState.totalStaked` is subtracted by totalFrozen again. This results in an incorrect update of the `gInflationIndex`. Additionally, if more than half of total staked values are frozen, the line 260 in Comptroller.sol will revert from underflow. The impact of this issue is an updated incorrect `gInflationIndex` and a revert when more than half of total staked is frozen. The recommendation is to change the code snippet to `uint256 totalStaked_ = userManagerState.totalStaked;` to fix the issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-union-finance-judging/issues/26 

## Found by 
Jeiwan, Lambda, dipp, lemonmon

## Summary

In `Comptroller::withdrawRewards`, `totalFrozen` was subtracted twice from `totalStaked`, which will update `Comptroller::gInflationIndex` based on incorrect information.
Also, if more than half of `totalStaked` is frozen, the `Comptroller::withdrawRewards` will revert, so no one can call `UserManager::stake` or `UserManager::unstake`.

## Vulnerability Detail

In `Comptroller:withdrawRewards` calls `_getUserManagerState` and saves it as `userManagerState`:

https://github.com/sherlock-audit/2022-10-union-finance/blob/main/union-v2-contracts/contracts/token/Comptroller.sol?plain=1#L248

Note that returned value of `userManagerState.totalStaked` is equivalent to `userManager.totalStaked() - userManager.totalFrozen()`:

https://github.com/sherlock-audit/2022-10-union-finance/blob/main/union-v2-contracts/contracts/token/Comptroller.sol?plain=1#L306-L317

However, in the `Comptroller::withdrawRewards` function, the returned value `userManagerState.totalStaked` will be subtracted by totalFrozen again:

https://github.com/sherlock-audit/2022-10-union-finance/blob/main/union-v2-contracts/contracts/token/Comptroller.sol?plain=1#L260-L261

So, the `totalStaked_` is equivalent to `userManager.totalStaked() - 2 * userManager.totalFrozen()`, which was used to calculate `gInflationIndex` in the line 261 of `Comptroller.sol`. It will result in incorrect update of the `gInflationIndex`.

Moreover, if more than half of total staked values are frozen, the line 260 in Comptroller.sol will revert from underflow. The `Comptroller::withdrawRewards` function is used in `UserManager::stake`, `UserManager::unstake` and `UserManager::withdrawRewards`, thus all of these function will stop working when the condition is met.

## Impact

- Updated to incorrect `gInflationIndex`
- Revert when more than half of total staked is frozen

## Code Snippet

https://github.com/sherlock-audit/2022-10-union-finance/blob/main/union-v2-contracts/contracts/token/Comptroller.sol?plain=1#L248
https://github.com/sherlock-audit/2022-10-union-finance/blob/main/union-v2-contracts/contracts/token/Comptroller.sol?plain=1#L306-L317
https://github.com/sherlock-audit/2022-10-union-finance/blob/main/union-v2-contracts/contracts/token/Comptroller.sol?plain=1#L260-L261

## Tool used

Manual Review

## Recommendation

the following line 

https://github.com/sherlock-audit/2022-10-union-finance/blob/main/union-v2-contracts/contracts/token/Comptroller.sol?plain=1#L248

should be:

```solidity
        uint256 totalStaked_ = userManagerState.totalStaked;
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Union Finance |
| Report Date | N/A |
| Finders | lemonmon, Lambda, dipp, Jeiwan |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-union-finance-judging/issues/26
- **Contest**: https://app.sherlock.xyz/audits/contests/11

### Keywords for Search

`vulnerability`

