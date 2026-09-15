---
# Core Classification
protocol: Elfi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34789
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/329
source_link: none
github_link: https://github.com/sherlock-audit/2024-05-elfi-protocol-judging/issues/146

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
  - mstpr-brainbot
  - KrisRenZo
  - dany.armstrong90
---

## Vulnerability Title

H-27: Attacker can inflate stake rewards as he wants.

### Overview


The bug report discusses an issue with the `FeeRewardsProcess.sol` function in the ELF Protocol. This function uses the balance of an account as the amount of stake tokens, which can be transferred to any account. This allows an attacker to inflate stake rewards by flash loaning tokens. The impact of this vulnerability is that the attacker can manipulate stake rewards as they wish. The recommendation is to use the `stakingAccount.stakeTokenBalances[stakeToken].stakeAmount` instead of the stake token balance. The protocol team has already fixed this issue in a recent commit.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-05-elfi-protocol-judging/issues/146 

## Found by 
KrisRenZo, dany.armstrong90, mstpr-brainbot
## Summary
`FeeRewardsProcess.sol#updateAccountFeeRewards` function uses balance of account as amount of stake tokens.
Since it is possible to transfer stake tokens to any accounts, attacker can flash loan other's stake tokens to inflate stake rewards.

## Vulnerability Detail
`FeeRewardsProcess.sol#updateAccountFeeRewards` function is the following.
```solidity
    function updateAccountFeeRewards(address account, address stakeToken) public {
        StakingAccount.Props storage stakingAccount = StakingAccount.load(account);
        StakingAccount.FeeRewards storage accountFeeRewards = stakingAccount.getFeeRewards(stakeToken);
        FeeRewards.MarketRewards storage feeProps = FeeRewards.loadPoolRewards(stakeToken);
        if (accountFeeRewards.openRewardsPerStakeToken == feeProps.getCumulativeRewardsPerStakeToken()) {
            return;
        }
63:     uint256 stakeTokens = IERC20(stakeToken).balanceOf(account);
        if (
            stakeTokens > 0 &&
            feeProps.getCumulativeRewardsPerStakeToken() - accountFeeRewards.openRewardsPerStakeToken >
            feeProps.getPoolRewardsPerStakeTokenDeltaLimit()
        ) {
            accountFeeRewards.realisedRewardsTokenAmount += (
                stakeToken == CommonData.getStakeUsdToken()
                    ? CalUtils.mul(
                        feeProps.getCumulativeRewardsPerStakeToken() - accountFeeRewards.openRewardsPerStakeToken,
                        stakeTokens
                    )
                    : CalUtils.mulSmallRate(
                        feeProps.getCumulativeRewardsPerStakeToken() - accountFeeRewards.openRewardsPerStakeToken,
                        stakeTokens
                    )
            );
        }
        accountFeeRewards.openRewardsPerStakeToken = feeProps.getCumulativeRewardsPerStakeToken();
        stakingAccount.emitFeeRewardsUpdateEvent(stakeToken);
    }
```
Balance of account is used as amount of stake tokens in `L63`.
But since the stake tokens can be transferred to any other account, attacker can inflate stake token rewards by flash loan.

Example:
1. User has two account: `account1`, `account2`.
2. User has staked 1000 ETH in `account1` and 1000 ETH in `account2`.
3. After a period of time, user transfer 1000 xETH from `account2` to `account1` and claim rewards for `account1`.
4. Now, attacker can claim rewards twice for `account1`.
5. In the same way, attacker can claim rewards twice for `account2` too.

## Impact
Attacker can inflate stake rewards as he wants using this vulnerability.

## Code Snippet
https://github.com/sherlock-audit/2024-05-elfi-protocol/blob/main/elfi-perp-contracts/contracts/process/FeeRewardsProcess.sol#L63

## Tool used

Manual Review

## Recommendation
Use `stakingAccount.stakeTokenBalances[stakeToken].stakeAmount` instead of stake token balance as follows.
```solidity
    function updateAccountFeeRewards(address account, address stakeToken) public {
        StakingAccount.Props storage stakingAccount = StakingAccount.load(account);
        StakingAccount.FeeRewards storage accountFeeRewards = stakingAccount.getFeeRewards(stakeToken);
        FeeRewards.MarketRewards storage feeProps = FeeRewards.loadPoolRewards(stakeToken);
        if (accountFeeRewards.openRewardsPerStakeToken == feeProps.getCumulativeRewardsPerStakeToken()) {
            return;
        }
--      uint256 stakeTokens = IERC20(stakeToken).balanceOf(account);
++      uint256 stakeTokens = stakingAccount.stakeTokenBalances[stakeToken].stakeAmount;
        if (
            stakeTokens > 0 &&
            feeProps.getCumulativeRewardsPerStakeToken() - accountFeeRewards.openRewardsPerStakeToken >
            feeProps.getPoolRewardsPerStakeTokenDeltaLimit()
        ) {
            accountFeeRewards.realisedRewardsTokenAmount += (
                stakeToken == CommonData.getStakeUsdToken()
                    ? CalUtils.mul(
                        feeProps.getCumulativeRewardsPerStakeToken() - accountFeeRewards.openRewardsPerStakeToken,
                        stakeTokens
                    )
                    : CalUtils.mulSmallRate(
                        feeProps.getCumulativeRewardsPerStakeToken() - accountFeeRewards.openRewardsPerStakeToken,
                        stakeTokens
                    )
            );
        }
        accountFeeRewards.openRewardsPerStakeToken = feeProps.getCumulativeRewardsPerStakeToken();
        stakingAccount.emitFeeRewardsUpdateEvent(stakeToken);
    }
```



## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/0xCedar/elfi-perp-contracts/pull/19

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Elfi |
| Report Date | N/A |
| Finders | mstpr-brainbot, KrisRenZo, dany.armstrong90 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-05-elfi-protocol-judging/issues/146
- **Contest**: https://app.sherlock.xyz/audits/contests/329

### Keywords for Search

`vulnerability`

