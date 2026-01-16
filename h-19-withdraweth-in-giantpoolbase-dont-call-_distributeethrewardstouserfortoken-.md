---
# Core Classification
protocol: Stakehouse Protocol
chain: everychain
category: uncategorized
vulnerability_type: don't_update_state

# Attack Vector Details
attack_type: don't_update_state
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5906
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest
source_link: https://code4rena.com/reports/2022-11-stakehouse
github_link: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/260

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - don't_update_state

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
  - unforgiven
  - 0x4non
---

## Vulnerability Title

[H-19] withdrawETH() in GiantPoolBase don’t call _distributeETHRewardsToUserForToken() or _onWithdraw() which would make users to lose their remaining rewards 

### Overview


This bug report is about a vulnerability in the code of a contract called "GiantPoolBase" that is used to distribute rewards to users. The vulnerability is that when a user withdraws their funds, their unclaimed rewards are not transferred to them before their balance is set to zero. This means that when they try to claim their rewards, they will receive nothing. 

The code of the vulnerability can be found at two links, both of which are provided in the report. The code of the "withdrawETH()" function in "GiantPoolBase" is also provided in the report. This code shows that when a user withdraws their funds, their balance is set to zero without any transfer of unclaimed rewards. 

The steps that this bug happens are also provided in the report. It explains that if a user has unclaimed rewards, they will lose them when they withdraw their funds.

The report also mentions the tools used to identify the bug, which is VIM.

Finally, the report provides a recommended mitigation step, which is that user's unclaimed funds should be calculated and transferred before any actions that change user's balance.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/GiantPoolBase.sol#L50-L64
https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/GiantMevAndFeesPool.sol#L180-L193


## Vulnerability details

## Impact
Function `_distributeETHRewardsToUserForToken()` is used to distribute remaining reward of user and it's called in `_onWithdraw()` of `GiantMevAndFeesPool`. but function `withdrawETH()` in `GiantPoolBase` don't call either of them and burn user giant LP token balance so if user withdraw his funds and has some remaining ETH rewards he would lose those rewards because his balance set to zero.

## Proof of Concept
This is `withdrawETH()` code in `GiantPoolBase`:
```
    /// @notice Allow a user to chose to burn their LP tokens for ETH only if the requested amount is idle and available from the contract
    /// @param _amount of LP tokens user is burning in exchange for same amount of ETH
    function withdrawETH(uint256 _amount) external nonReentrant {
        require(_amount >= MIN_STAKING_AMOUNT, "Invalid amount");
        require(lpTokenETH.balanceOf(msg.sender) >= _amount, "Invalid balance");
        require(idleETH >= _amount, "Come back later or withdraw less ETH");

        idleETH -= _amount;

        lpTokenETH.burn(msg.sender, _amount);
        (bool success,) = msg.sender.call{value: _amount}("");
        require(success, "Failed to transfer ETH");

        emit LPBurnedForETH(msg.sender, _amount);
    }
```
As you can see it burn user `lpTokenETH` balance and don't call either `_distributeETHRewardsToUserForToken()` or `_onWithdraw()`. and in function `claimRewards()` uses `lpTokenETH.balanceOf(msg.sender)` to calculate user rewards so if user balance get to `0` user won't get the remaining rewards.
These are steps that this bug happens:
1. `user1` deposit `10` ETH into the giant pool and `claimed[user1][lpTokenETH]` is `20` and `accumulatedETHPerLPShare` is `2`.
2. some time passes and `accumulatedETHPerLPShare` set to `3`.
3. `user1` unclaimed rewards are `10 * 3 - 20 = 10` ETH.
4. `user1` withdraw his `10` ETH by calling `withdrawETH(10)` and contract set `lpTokenETH` balance of `user1`  to `0` and transfer `10` ETH to user.
5. now if `user1` calls `claimRewards()` he would get `0` reward as his `lpTokenETH` balance is `0`.

so users lose their unclaimed rewards by withdrawing their funds.

## Tools Used
VIM

## Recommended Mitigation Steps
user's unclaimed funds should be calculated and transferred before any actions that change user's balance.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Stakehouse Protocol |
| Report Date | N/A |
| Finders | unforgiven, 0x4non |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-stakehouse
- **GitHub**: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/260
- **Contest**: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest

### Keywords for Search

`Don't update state`

