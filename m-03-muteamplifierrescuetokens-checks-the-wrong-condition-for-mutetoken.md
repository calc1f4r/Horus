---
# Core Classification
protocol: Mute.io
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16043
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-03-mute-switch-versus-contest
source_link: https://code4rena.com/reports/2023-03-mute
github_link: https://github.com/code-423n4/2023-03-mute-findings/issues/32

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
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - evan
  - hansfriese
---

## Vulnerability Title

[M-03] `MuteAmplifier.rescueTokens()` checks the wrong condition for `muteToken`

### Overview


This bug report is about a vulnerability in the MuteAmplifier.sol contract, which is a reward system. The vulnerability exists in the `rescueTokens()` function, which is responsible for rescuing tokens. The bug can lead to two impacts: the reward system can be broken as rewards can be withdrawn before starting staking, and some rewards can be locked inside the contract forever.

The bug can be exploited by checking the condition in the `rescueTokens()` function, which does not check `totalReclaimed` when `totalStakers == 0`. This means that some parts or all of the rewards can be withdrawn before the staking period, which will lead to the reward system not working properly.

The recommended mitigation steps for this bug are to modify the `rescueTokens()` function so that it checks `totalReclaimed` when `totalStakers > 0` and checks `totalRewards` when `totalStakers == 0` and the staking period is still active.

### Original Finding Content


There will be 2 impacts.

*   The reward system would be broken as the rewards can be withdrawn before starting staking.
*   Some rewards would be locked inside the contract forever as it doesn't check `totalReclaimed`

### Proof of Concept

`rescueTokens()` checks the below condition to rescue `muteToken`.

```solidity
else if (tokenToRescue == muteToken) {
    if (totalStakers > 0) {
        require(amount <= IERC20(muteToken).balanceOf(address(this)).sub(totalRewards.sub(totalClaimedRewards)),
            "MuteAmplifier::rescueTokens: that muteToken belongs to stakers"
        );
    }
}
```

But there are 2 problems.

1.  Currently, it doesn't check anything when `totalStakers == 0`. So some parts(or 100%) of rewards can be withdrawn before the staking period. In this case, the reward system won't work properly due to the lack of rewards.
2.  It checks the wrong condition when `totalStakers > 0` as well. As we can see [here](https://github.com/code-423n4/2023-03-mute/blob/4d8b13add2907b17ac14627cfa04e0c3cc9a2bed/contracts/amplifier/MuteAmplifier.sol#L241), some remaining rewards are tracked using `totalReclaimed` and transferred to treasury directly. So we should consider this amount as well.

### Recommended Mitigation Steps

It should be modified like the below.

```solidity
else if (tokenToRescue == muteToken) {
    if (totalStakers > 0) { //should check totalReclaimed as well
        require(amount <= IERC20(muteToken).balanceOf(address(this)).sub(totalRewards.sub(totalClaimedRewards).sub(totalReclaimed)),
            "MuteAmplifier::rescueTokens: that muteToken belongs to stakers"
        );
    }
    else if(block.timestamp <= endTime) { //no stakers but staking is still active, should maintain totalRewards
        require(amount <= IERC20(muteToken).balanceOf(address(this)).sub(totalRewards),
            "MuteAmplifier::rescueTokens: that muteToken belongs to stakers"
        );
    }
}
```

**[mattt21 (Mute Switch) confirmed](https://github.com/code-423n4/2023-03-mute-findings/issues/32#issuecomment-1500388417)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Mute.io |
| Report Date | N/A |
| Finders | evan, hansfriese |

### Source Links

- **Source**: https://code4rena.com/reports/2023-03-mute
- **GitHub**: https://github.com/code-423n4/2023-03-mute-findings/issues/32
- **Contest**: https://code4rena.com/contests/2023-03-mute-switch-versus-contest

### Keywords for Search

`vulnerability`

