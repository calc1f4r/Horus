---
# Core Classification
protocol: Biconomy
chain: everychain
category: uncategorized
vulnerability_type: array_bound

# Attack Vector Details
attack_type: array_bound
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1642
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-03-biconomy-hyphen-20-contest
source_link: https://code4rena.com/reports/2022-03-biconomy
github_link: https://github.com/code-423n4/2022-03-biconomy-findings/issues/136

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
rarity_score: 0

# Context Tags
tags:
  - array_bound

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - WatchPug
---

## Vulnerability Title

[M-14] LiquidityFarming.sol Unbounded for loops can potentially freeze users’ funds in edge cases

### Overview


This bug report is about a vulnerability in the code of the LiquidityFarming.sol contract, which is part of the biconomy project. The vulnerability is caused by the implementation of the withdraw() function, which calls the _sendRewardsForNft() function at line 243, which in turn calls the updatePool() function at line 129, which calls the getUpdatedAccTokenPerShare() function at line 319. This function loops over the rewardRateLog to calculate an up-to-date value of accTokenPerShare. 

The problem arises when the rewardPerSecond is updated frequently, and the liquidityProviders are inactive for a period of time. When one of the liquidityProviders comes to withdraw, the transaction may revert due to out-of-gas, as the rewardRateLog has accumulated to a large size, causing the loop to cost more gas than the block gas limit.

The recommended fix is to remove the rewardRateLog and change the setRewardPerSecond() function to the code provided in the report. This will make the code simpler and avoid the out-of-gas issue.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-03-biconomy/blob/db8a1fdddd02e8cc209a4c73ffbb3de210e4a81a/contracts/hyphen/LiquidityFarming.sol#L270-L285


## Vulnerability details

In the current implementation of `withdraw()`, it calls `_sendRewardsForNft()` at L243 which calls `updatePool()` at L129 which calls `getUpdatedAccTokenPerShare()` at L319.

`getUpdatedAccTokenPerShare()` will loop over `rewardRateLog` to calculate an up to date value of accTokenPerShare.

https://github.com/code-423n4/2022-03-biconomy/blob/db8a1fdddd02e8cc209a4c73ffbb3de210e4a81a/contracts/hyphen/LiquidityFarming.sol#L270-L285

```solidity
while (true) {
    if (lastUpdatedTime >= counter) {
        break;
    }
    unchecked {
        accumulator +=
            rewardRateLog[_baseToken][i].rewardsPerSecond *
            (counter - max(lastUpdatedTime, rewardRateLog[_baseToken][i].timestamp));
    }
    counter = rewardRateLog[_baseToken][i].timestamp;
    if (i == 0) {
        break;
    }
    --i;
}
```

This won't be a problem in the usual cases, however, if there is a baseToken that:

- the `rewardPerSecond` get updated quite frequently;
- the liquidityProviders are inactive (no deposits / withdrawals for a period of time)

Then by the time one of the `liquidityProviders` come to `withdraw()`, the tx may revert due to out-of-gas.

As the `rewardRateLog` is now accumulated to a large size that causes the loop costs more gas than the block gas limit.

There is a really easy fix for this, it will also make the code simpler:

### Recommendation

Consider removing `rewardRateLog` and change `setRewardPerSecond()` to:

```solidity
function setRewardPerSecond(address _baseToken, uint256 _rewardPerSecond) public onlyOwner {
    updatePool(baseToken);
    rewardRate[_baseToken] = RewardsPerSecondEntry(_rewardPerSecond, block.timestamp);
    emit LogRewardPerSecond(_baseToken, _rewardPerSecond);
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Biconomy |
| Report Date | N/A |
| Finders | WatchPug |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-biconomy
- **GitHub**: https://github.com/code-423n4/2022-03-biconomy-findings/issues/136
- **Contest**: https://code4rena.com/contests/2022-03-biconomy-hyphen-20-contest

### Keywords for Search

`Array Bound`

