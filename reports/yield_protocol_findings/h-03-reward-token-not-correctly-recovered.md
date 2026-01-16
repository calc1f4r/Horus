---
# Core Classification
protocol: Streaming Protocol
chain: everychain
category: uncategorized
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1128
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-streaming-protocol-contest
source_link: https://code4rena.com/reports/2021-11-streaming
github_link: https://github.com/code-423n4/2021-11-streaming-findings/issues/214

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 2

# Context Tags
tags:
  - wrong_math

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - cmichel
  - pedroais
  - GeekyLumberjack
  - hyh
  - kenzo
---

## Vulnerability Title

[H-03] Reward token not correctly recovered

### Overview


This bug report concerns the `Streaming` contract, which allows users to recover their reward tokens by calling `recoverTokens(rewardToken, recipient)`. The issue is that the excess amount is computed incorrectly, resulting in reward token recovery not working.

The problem is that `rewardTokenAmount` only ever increases (when calling `fundStream`) but it never decreases when claiming the rewards through `claimReward`. As a result, the `rewardTokenAmount` never tracks the contract's reward balance and the excess cannot be computed that way.

To illustrate the issue, consider a situation with no reward fees and a single user staking. When someone funds `1000` reward tokens through `fundStream(1000)`, the `rewardTokenAmount` is set to `1000`. After the stream and reward lock period is over, the user claims their full reward and receives `1000` reward tokens by calling `claimReward()`. The reward contract balance is now `0` but `rewardTokenAmount` remains `1000`. If someone then sends 1000 reward tokens to the contract by accident, these cannot be recovered as the `excess = balance - rewardTokenAmount = 0`.

The recommended mitigation steps are that the claimed rewards need to be tracked, just like the claimed deposits are tracked. Additionally, `rewardTokenAmount` can be decreased in `claimReward` as it is no longer used to update the `cumulativeRewardPerToken`.

### Original Finding Content

_Submitted by cmichel, also found by GeekyLumberjack, kenzo, pedroais, and hyh_

The `Streaming` contract allows recovering the reward token by calling `recoverTokens(rewardToken, recipient)`.

However, the excess amount is computed incorrectly as `ERC20(token).balanceOf(address(this)) - (rewardTokenAmount + rewardTokenFeeAmount)`:

```solidity
function recoverTokens(address token, address recipient) public lock {
    if (token == rewardToken) {
        require(block.timestamp > endRewardLock, "time");

        // check what isnt claimable by depositors and governance
        // @audit-issue rewardTokenAmount increased on fundStream, but never decreased! this excess underflows
        uint256 excess = ERC20(token).balanceOf(address(this)) - (rewardTokenAmount + rewardTokenFeeAmount);
        ERC20(token).safeTransfer(recipient, excess);

        emit RecoveredTokens(token, recipient, excess);
        return;
    }
    // ...
```

Note that `rewardTokenAmount` only ever *increases* (when calling `fundStream`) but it never decreases when claiming the rewards through `claimReward`.
However, `claimReward` transfers out the reward token.

Therefore, the `rewardTokenAmount` never tracks the contract's reward balance and the excess cannot be computed that way.

#### Proof Of Concept

Assume no reward fees for simplicity and only a single user staking.

*   Someone funds `1000` reward tokens through `fundStream(1000)`. Then `rewardTokenAmount = 1000`
*   The stream and reward lock period is over, i.e. `block.timestamp > endRewardLock`
*   The user claims their full reward and receives `1000` reward tokens by calling `claimReward()`. The reward contract balance is now `0` but `rewardTokenAmount = 1000`
*   Some fool sends 1000 reward tokens to the contract by accident. These cannot be recovered as the `excess = balance - rewardTokenAmount = 0`

#### Impact

Reward token recovery does not work.

#### Recommended Mitigation Steps

The claimed rewards need to be tracked as well, just like the claimed deposits are tracked.
I think you can even decrease `rewardTokenAmount` in `claimReward` because at this point `rewardTokenAmount` is not used to update the `cumulativeRewardPerToken` anymore.

**[brockelmore (Streaming Protocol) confirmed](https://github.com/code-423n4/2021-11-streaming-findings/issues/214#issuecomment-989285321)**





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 2/5 |
| Audit Firm | Code4rena |
| Protocol | Streaming Protocol |
| Report Date | N/A |
| Finders | cmichel, pedroais, GeekyLumberjack, hyh, kenzo |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-streaming
- **GitHub**: https://github.com/code-423n4/2021-11-streaming-findings/issues/214
- **Contest**: https://code4rena.com/contests/2021-11-streaming-protocol-contest

### Keywords for Search

`Wrong Math`

