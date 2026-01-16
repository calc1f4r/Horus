---
# Core Classification
protocol: Peapods_2024-11-16
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45984
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Peapods-security-review_2024-11-16.md
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

[C-02] For self-lending pairs rewards will be stuck

### Overview


This bug report discusses a problem with self-lending pods, which are used for lending and borrowing assets. The bug causes rewards to be lost because the underlying token is not being correctly converted to the paired LP token for the pod. This issue occurs when the rewarded token is different from the pod's LP rewards token. A proof of concept has been provided to demonstrate the bug, and a recommendation is made to deposit the underlying asset into the lending pair to fix the issue.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** High

## Description

For self-lending pods, the paired LP token of the pod is a fToken, which is a share of a lending pair.

In the `AutoCompoundingPodLp`, it converts the reward token into the paired LP token. However for self-lending pods, instead of converting to the fToken, it converts to the underlying token since it is a more liquid asset. (With the intention of later depositing the asset into the lending pair to receive the fToken)

```solidity
// if self lending pod, we need to swap for the lending pair borrow token,
// then deposit into the lending pair which is the paired LP token for the pod
if (IS_PAIRED_LENDING_PAIR) {
    _swapOutputTkn = IFraxlendPair(_pairedLpToken).asset();
}
```

This is handled correctly when the rewarded token is the same as the pod's LP rewards token:

```solidity
try DEX_ADAPTER.swapV3Single(
    /* PARAMS */
) returns (uint256 __amountOut) {
    ...
    // if this is a self-lending pod, convert the received borrow token
    // into fTKN shares and use as the output since it's the pod paired LP token
    if (IS_PAIRED_LENDING_PAIR) {
        IERC20(_swapOutputTkn).safeIncreaseAllowance(address(_pairedLpToken), _amountOut);
        _amountOut = IFraxlendPair(_pairedLpToken).deposit(_amountOut, address(this));
    }
}
```

However when the rewarded token is NOT the same as the pod's LP reward token, the deposit does not occur:

```solidity
address _rewardsToken = pod.lpRewardsToken();
if (_token != _rewardsToken) {
    return _swap(_token, _swapOutputTkn, _amountIn, 0); //@audit only swap occurs to token, not converting to fToken!
}
```

As a result, the later swaps within the `_processRewardsToPodLp()` will fail (not revert, due to try-catch) due to having zero balance of the fToken which is the actual paired LP token of the pod.

The underlying token of the fToken will be stuck in the aspTKN contract and cannot be redeemed, so rewards are lost.

## Proof of Concept

The PoC requires a large setup with multiple files so I have added it to a gist [here](https://gist.github.com/0xjuaan/0567324d0dd7e36f29bf0ea809389b1c)

It requires a mainnet RPC url in the `.env` file. `RPC="<insert-url>"`

## Recommendations

Within `_tokenToPairedLpToken()`, when `_token != _rewardsToken`, deposit the underlying asset into the lending pair before returning.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Peapods_2024-11-16 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Peapods-security-review_2024-11-16.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

