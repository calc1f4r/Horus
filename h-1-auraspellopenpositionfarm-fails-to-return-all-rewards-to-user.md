---
# Core Classification
protocol: Blueberry Update #2
chain: everychain
category: uncategorized
vulnerability_type: check_return_value

# Attack Vector Details
attack_type: check_return_value
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18508
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/77
source_link: none
github_link: https://github.com/sherlock-audit/2023-05-blueberry-judging/issues/29

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
  - check_return_value
  - missing-logic
  - fund_lock
  - deposit/reward_tokens

protocol_categories:
  - lending
  - leveraged_farming
  - options_vault

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0x52
  - nobody2018
---

## Vulnerability Title

H-1: AuraSpell#openPositionFarm fails to return all rewards to user

### Overview


A bug report has been raised in the Sherlock Audit repository about an issue with the AuraSpell#openPositionFarm contract. It was found by 0x52 and nobody2018 and is related to the WAuraPool contract. The issue is that when a user adds to an existing position on AuraSpell, the contract burns their current position and remints them a new one. However, the WAuraPool contract only sends the Aura token back to the user, causing all other rewards to be lost. 

The vulnerability detail is that inside the WAuraPools#burn function, reward tokens are sent to the user. However, in the AuraSpell#openPositionFarm function, the contract only refunds Aura to the user, causing all other extra reward tokens received by the contract to be lost to the user. 

The impact of this bug is that users will lose all extra reward tokens from their original position.

The tool used to identify this bug was manual review. The recommendation is that WAuraPool should be modified to return the reward tokens it sends. This list should then be used to refund all tokens to the user.

The issue was discussed and it was decided that the issue mentioned previously had been resolved accordingly in the respective contest, so the escalation was rejected. Watsons who escalated this issue will have their escalation amount deducted from their next payout.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-05-blueberry-judging/issues/29 

## Found by 
0x52, nobody2018
## Summary

When a user adds to an existing position on AuraSpell, the contract burns their current position and remints them a new one. The issues is that WAuraPool will send all reward tokens to the contract but it only sends Aura back to the user, causing all other rewards to be lost.

## Vulnerability Detail

https://github.com/sherlock-audit/2023-05-blueberry/blob/main/blueberry-core/contracts/wrapper/WAuraPools.sol#L256-L261

        for (uint i = 0; i < rewardTokens.length; i++) {
            IERC20Upgradeable(rewardTokens[i]).safeTransfer(
                msg.sender,
                rewards[i]
            );
        }

Inside WAuraPools#burn reward tokens are sent to the user.

https://github.com/sherlock-audit/2023-05-blueberry/blob/main/blueberry-core/contracts/spell/AuraSpell.sol#L130-L140

        IBank.Position memory pos = bank.getCurrentPositionInfo();
        if (pos.collateralSize > 0) {
            (uint256 pid, ) = wAuraPools.decodeId(pos.collId);
            if (param.farmingPoolId != pid)
                revert Errors.INCORRECT_PID(param.farmingPoolId);
            if (pos.collToken != address(wAuraPools))
                revert Errors.INCORRECT_COLTOKEN(pos.collToken);
            bank.takeCollateral(pos.collateralSize);
            wAuraPools.burn(pos.collId, pos.collateralSize);
            _doRefundRewards(AURA);
        }

We see above that the contract only refunds Aura to the user causing all other extra reward tokens received by the contract to be lost to the user.

## Impact

User will lose all extra reward tokens from their original position

## Code Snippet

## Tool used

Manual Review

## Recommendation

WAuraPool returns the reward tokens it sends. Use this list to refund all tokens to the user



## Discussion

**sleepriverfish**

Escalate for 10 USDC.
The issue was  excluded from #Blueberry Update, it appears to have been rewarded in #Blueberry Update 2.
https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/42

**sherlock-admin**

 > Escalate for 10 USDC.
> The issue was  excluded from #Blueberry Update, it appears to have been rewarded in #Blueberry Update 2.
> https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/42

You've created a valid escalation for 10 USDC!

To remove the escalation from consideration: Delete your comment.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**securitygrid**

Escalate for 10 USDC
valid H. Nobody escalated [it](https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/42) 

**sherlock-admin**

 > Escalate for 10 USDC
> valid H. Nobody escalated [it](https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/42) 

You've created a valid escalation for 10 USDC!

To remove the escalation from consideration: Delete your comment.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**IAm0x52**

Agreed with second escalation

**sleepriverfish**

So, the issue https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/42 considered invalid? I believe it should be categorized and rewarded in some way.

**hrishibhat**

Escalation rejected

Valid high
The issue mentioned above has been resolved accordingly in the respective contest. 

**sherlock-admin**

> Escalation rejected
> 
> Valid high
> The issue mentioned above has been resolved accordingly in the respective contest. 

    This issue's escalations have been rejected!

    Watsons who escalated this issue will have their escalation amount deducted from their next payout.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 2/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry Update #2 |
| Report Date | N/A |
| Finders | 0x52, nobody2018 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-05-blueberry-judging/issues/29
- **Contest**: https://app.sherlock.xyz/audits/contests/77

### Keywords for Search

`Check Return Value, Missing-Logic, Fund Lock, Deposit/Reward tokens`

