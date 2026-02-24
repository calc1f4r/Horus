---
# Core Classification
protocol: Blueberry Update
chain: everychain
category: logic
vulnerability_type: deposit/reward_tokens

# Attack Vector Details
attack_type: deposit/reward_tokens
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18481
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/69
source_link: none
github_link: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/101

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.20
financial_impact: high

# Scoring
quality_score: 1
rarity_score: 0

# Context Tags
tags:
  - deposit/reward_tokens
  - coding-bug
  - business_logic

protocol_categories:
  - lending
  - leveraged_farming
  - options_vault

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Bauer
  - Ch\_301
---

## Vulnerability Title

H-1: attackers will keep stealing the `rewards` from Convex SPELL

### Overview


This bug report is about an issue found in the Convex SPELL code. The code allows users to transfer CRV, CVX, and extra rewards to the SPELL, but only refunds CVX to the user when the position is closed. This means that the extra rewards remain in the SPELL, and can be stolen by attackers if they invoke the same address tokens with the _doRefund() function. This vulnerability can cause the Convex SPELL to steal user rewards, leading to the protocol losing fees, and attackers being able to keep stealing rewards from the SPELL. The code snippet provided in the report shows the WConvexPools.burn() function, which transfers CRV, CVX, and extra rewards, and the ConvexSpell.openPositionFarm() function, which only refunds CVX to the user. The tool used to identify this bug was manual review. The recommendation is to refund all rewards (CRV + CVX + the extra rewards). The discussion that followed included a comment from Ch-301, who suggested escalating the bug for 10 USDC, and Convex docs to confirm the point. Senior Watson's comment pointed to a duplicate issue, and Hrishibhat accepted the escalation. Finally, Sherlock-Admin confirmed that the issue's escalation had been accepted, and that contestants' payouts and scores would be updated accordingly.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/101 

## Found by 
Bauer, Ch\_301
## Summary
On [WConvexPools.burn()](https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/wrapper/WConvexPools.sol#L201-L235) transfer [CRV + CVX + the extra rewards](https://docs.convexfinance.com/convexfinance/general-information/why-convex/convex-for-liquidity-providers) to Convex SPELL 


## Vulnerability Detail
But [ConvexSpell.openPositionFarm()](https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/spell/ConvexSpell.sol#L67-L138) only refund CVX to the user.
So the rest rewards will stay in the SPELL intel if someone (could be an attacker) invokes `_doRefund()` within `closePositionFarm()` with the same address tokens 

## Impact
- Convex SPELL steals the user rewards 
- the protocol will lose some fees 
- attackers will keep stealing the rewards from Convex SPELL

## Code Snippet
`WConvexPools.burn()` transfer CRV + CVX + the extra rewards
https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/wrapper/WConvexPools.sol#L201-L235
```solidity
        // Transfer LP Tokens
        IERC20Upgradeable(lpToken).safeTransfer(msg.sender, amount);

        // Transfer Reward Tokens
        (rewardTokens, rewards) = pendingRewards(id, amount);

        for (uint i = 0; i < rewardTokens.length; i++) {
            IERC20Upgradeable(rewardTokens[i]).safeTransfer(
                msg.sender,
                rewards[i]
            );
        }
```

only refund CVX to the user
https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/spell/ConvexSpell.sol#LL127C1-L138C10
```solidity
        // 6. Take out existing collateral and burn
        IBank.Position memory pos = bank.getCurrentPositionInfo();
        if (pos.collateralSize > 0) {
            (uint256 pid, ) = wConvexPools.decodeId(pos.collId);
            if (param.farmingPoolId != pid)
                revert Errors.INCORRECT_PID(param.farmingPoolId);
            if (pos.collToken != address(wConvexPools))
                revert Errors.INCORRECT_COLTOKEN(pos.collToken);
            bank.takeCollateral(pos.collateralSize);
            wConvexPools.burn(pos.collId, pos.collateralSize);
            _doRefundRewards(CVX);
        }
```

## Tool used

Manual Review

## Recommendation
you should Refund all Rewards (CRV + CVX + the extra rewards)



## Discussion

**Ch-301**

Escalate for 10 USDC

Convex docs are confirming this point 

```diff
Convex allows liquidity providers to earn trading fees and claim boosted CRV without locking CRV themselves. Liquidity providers can receive boosted CRV and liquidity mining rewards with minimal effort:
Earn claimable CRV with a high boost without locking any CRV
Earn CVX rewards
Zero deposit and withdraw fees
Zero fees on extra incentive tokens (SNX, etc)
```
and [WConvexPools.burn()](https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/wrapper/WConvexPools.sol#L201-L235) handle this properly

so Convex SPELL should refund all the rewards

**sherlock-admin**

 > Escalate for 10 USDC
> 
> Convex docs are confirming this point 
> 
> ```diff
> Convex allows liquidity providers to earn trading fees and claim boosted CRV without locking CRV themselves. Liquidity providers can receive boosted CRV and liquidity mining rewards with minimal effort:
> Earn claimable CRV with a high boost without locking any CRV
> Earn CVX rewards
> Zero deposit and withdraw fees
> Zero fees on extra incentive tokens (SNX, etc)
> ```
> and [WConvexPools.burn()](https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/wrapper/WConvexPools.sol#L201-L235) handle this properly
> 
> so Convex SPELL should refund all the rewards

You've created a valid escalation for 10 USDC!

To remove the escalation from consideration: Delete your comment.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**ctf-sec**

Senior watson's comment:

same as
https://github.com/sherlock-audit/2023-05-blueberry-judging/issues/29 

**hrishibhat**

Escalation accepted

Valid high 
This issue is a valid high along with another duplicate #42

**sherlock-admin**

> Escalation accepted
> 
> Valid high 
> This issue is a valid high along with another duplicate #42

    This issue's escalations have been accepted!

    Contestants' payouts and scores will be updated according to the changes made on this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 1/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry Update |
| Report Date | N/A |
| Finders | Bauer, Ch\_301 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/101
- **Contest**: https://app.sherlock.xyz/audits/contests/69

### Keywords for Search

`Deposit/Reward tokens, Coding-Bug, Business Logic`

