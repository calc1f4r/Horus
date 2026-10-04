---
# Core Classification
protocol: UXD Protocol
chain: everychain
category: uncategorized
vulnerability_type: overflow/underflow

# Attack Vector Details
attack_type: overflow/underflow
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6270
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/33
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-uxd-judging/issues/97

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - overflow/underflow
  - don't_update_state

protocol_categories:
  - liquid_staking
  - services
  - derivatives
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - rvierdiiev
---

## Vulnerability Title

M-12: PerpDepository.netAssetDeposits variable can prevent users to withdraw with underflow error

### Overview


This bug report is about the PerpDepository.netAssetDeposits variable, which can prevent users from withdrawing their funds due to an underflow error. This variable is increased when users deposit base assets and decreased when users withdraw UXD tokens. The problem is that when the user redeems their UXD tokens, they may receive more or less than the base assets they deposited, leading to a negative value for the netAssetDeposits variable and a transaction revert. This issue is considered to be of medium severity, as it only occurs under certain specific conditions and can correct itself. The recommended solution is to remove the variable, or to use two variables (totalDeposited and totalWithdrawn) instead. If accepted, contestants' payouts and scores will be updated accordingly.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-uxd-judging/issues/97 

## Found by 
rvierdiiev

## Summary
PerpDepository.netAssetDeposits variable can prevent users to withdraw with underflow error
## Vulnerability Detail
When user deposits using PerpDepository, then `netAssetDeposits` variable is increased with the base assets amount, provided by depositor.
https://github.com/sherlock-audit/2023-01-uxd/blob/main/contracts/integrations/perp/PerpDepository.sol#L283-L288
```solidity
    function _depositAsset(uint256 amount) private {
        netAssetDeposits += amount;


        IERC20(assetToken).approve(address(vault), amount);
        vault.deposit(assetToken, amount);
    }
```

Also when user withdraws, this `netAssetDeposits` variable is decreased with base amount that user has received for redeeming his UXD tokens.
https://github.com/sherlock-audit/2023-01-uxd/blob/main/contracts/integrations/perp/PerpDepository.sol#L294-L302
```solidity
    function _withdrawAsset(uint256 amount, address to) private {
        if (amount > netAssetDeposits) {
            revert InsufficientAssetDeposits(netAssetDeposits, amount);
        }
        netAssetDeposits -= amount;


        vault.withdraw(address(assetToken), amount);
        IERC20(assetToken).transfer(to, amount);
    }
```

The problem here is that when user deposits X assets, then he receives Y UXD tokens. And when later he redeems his Y UXD tokens he can receive more or less than X assets. This can lead to situation when netAssetDeposits variable will be seting to negative value which will revert tx.

Example.
1.User deposits 1 WETH when it costs 1200$. As result 1200 UXD tokens were minted and netAssetDeposits was set to 1.
2.Price of WETH has decreased and now it costs 1100.
3.User redeem his 1200 UXD tokens and receives from perp protocol 1200/1100=1.09 WETH. But because netAssetDeposits is 1, then transaction will revert inside `_withdrawAsset` function with underflow error.
## Impact
User can't redeem all his UXD tokens.
## Code Snippet
https://github.com/sherlock-audit/2023-01-uxd/blob/main/contracts/integrations/perp/PerpDepository.sol#L264-L278
https://github.com/sherlock-audit/2023-01-uxd/blob/main/contracts/integrations/perp/PerpDepository.sol#L294-L302
https://github.com/sherlock-audit/2023-01-uxd/blob/main/contracts/integrations/perp/PerpDepository.sol#L240-L253
https://github.com/sherlock-audit/2023-01-uxd/blob/main/contracts/integrations/perp/PerpDepository.sol#L283-L288
## Tool used

Manual Review

## Recommendation
As you don't use this variable anywhere else, you can remove it.
Otherwise you need to have 2 variables instead: totalDeposited and totalWithdrawn. 

## Discussion

**WarTech9**

One fix: `netAssetDeposits` should be updated during rebalancing.

**WarTech9**

@acamill This _can only be partially fixed_ by updating `netAssetsDeposits` while rebalancing but that's only resolves the issue if rebalancing has occurred. It would still be possible to run into this if rebalancing has not yet occurred so its not a full fix. 
We could use 2 variables as suggested but due to changes in asset values between mints and redeems, those would diverge and would be meaningless. 
We already have the position size which tells us this information, thus removing this field is the better option.

**0x00052**

Escalate for 25 USDC

This should only be medium severity because it is an edge case for the following reasons:
1) It can only occur if the average withdraw price is chronically under the average deposit price.
2) It only affects the tail end of withdraws, requiring a majority of the depository to be withdrawn
3) This state is not permanent because later deposits/withdraws can function in reverse (i.e. deposited at 1100 and withdraw at 1200) to cause netAssetsDeposits to go back up and free stuck assets

**sherlock-admin**

 > Escalate for 25 USDC
> 
> This should only be medium severity because it is an edge case for the following reasons:
> 1) It can only occur if the average withdraw price is chronically under the average deposit price.
> 2) It only affects the tail end of withdraws, requiring a majority of the depository to be withdrawn
> 3) This state is not permanent because later deposits/withdraws can function in reverse (i.e. deposited at 1100 and withdraw at 1200) to cause netAssetsDeposits to go back up and free stuck assets

You've created a valid escalation for 25 USDC!

To remove the escalation from consideration: Delete your comment.
To change the amount you've staked on this escalation: Edit your comment **(do not create a new comment)**.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**hrishibhat**

Escalation accepted

Given the certain specific requirements for the issue to occur, also note that there the condition can correct itself to free stuck assets.
Considering this issue as medium

**sherlock-admin**

> Escalation accepted
> 
> Given the certain specific requirements for the issue to occur, also note that there the condition can correct itself to free stuck assets.
> Considering this issue as medium

This issue's escalations have been accepted!

Contestants' payouts and scores will be updated according to the changes made on this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | UXD Protocol |
| Report Date | N/A |
| Finders | rvierdiiev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-uxd-judging/issues/97
- **Contest**: https://app.sherlock.xyz/audits/contests/33

### Keywords for Search

`Overflow/Underflow, Don't update state`

