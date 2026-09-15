---
# Core Classification
protocol: Biconomy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42511
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-03-biconomy
source_link: https://code4rena.com/reports/2022-03-biconomy
github_link: https://github.com/code-423n4/2022-03-biconomy-findings/issues/136

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
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-14] `LiquidityFarming.sol` Unbounded for loops can potentially freeze users' funds in edge cases

### Overview


The bug report is about an issue with the `withdraw()` function in the `LiquidityFarming.sol` contract. The function calls other functions, one of which has a loop that can become too expensive if a certain condition is met. This can cause the transaction to fail due to running out of gas. The suggested solution is to remove a variable and change the code in a specific function. The severity of the bug has been decreased to medium.

### Original Finding Content

_Submitted by WatchPug_

In the current implementation of `withdraw()`, it calls `_sendRewardsForNft()` at L243 which calls `updatePool()` at L129 which calls `getUpdatedAccTokenPerShare()` at L319.

`getUpdatedAccTokenPerShare()` will loop over `rewardRateLog` to calculate an up to date value of accTokenPerShare.

[LiquidityFarming.sol#L270-L285](https://github.com/code-423n4/2022-03-biconomy/blob/db8a1fdddd02e8cc209a4c73ffbb3de210e4a81a/contracts/hyphen/LiquidityFarming.sol#L270-L285)<br>

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

*   the `rewardPerSecond` get updated quite frequently;
*   the liquidityProviders are inactive (no deposits / withdrawals for a period of time)

Then by the time one of the `liquidityProviders` come to `withdraw()`, the tx may revert due to out-of-gas.

As the `rewardRateLog` is now accumulated to a large size that causes the loop costs more gas than the block gas limit.

There is a really easy fix for this, it will also make the code simpler:

### Recommended Mitigation Steps

Consider removing `rewardRateLog` and change `setRewardPerSecond()` to:

```solidity
function setRewardPerSecond(address _baseToken, uint256 _rewardPerSecond) public onlyOwner {
    updatePool(baseToken);
    rewardRate[_baseToken] = RewardsPerSecondEntry(_rewardPerSecond, block.timestamp);
    emit LogRewardPerSecond(_baseToken, _rewardPerSecond);
}
```

**[ankurdubey521 (Biconomy) acknowledged](https://github.com/code-423n4/2022-03-biconomy-findings/issues/136)**

**[pauliax (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-03-biconomy-findings/issues/136#issuecomment-1114779005):**
 > A valid concern, but I think it should be of Medium severity: _"Assets not at direct risk, but the function of the protocol or its availability could be impacted, or leak value with a hypothetical attack path with stated assumptions, but external requirements."_



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Biconomy |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-biconomy
- **GitHub**: https://github.com/code-423n4/2022-03-biconomy-findings/issues/136
- **Contest**: https://code4rena.com/reports/2022-03-biconomy

### Keywords for Search

`vulnerability`

