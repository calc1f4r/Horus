---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3675
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/21

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

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - 0xRajeev
  - obront
  - hansfriese
---

## Vulnerability Title

H-37: isValidRefinance will approve invalid refinances and reject valid refinances due to buggy math

### Overview


This bug report is about a vulnerability found in the code of AstariaRouter.sol:isValidRefinance(). This function is used to check if the refinance terms are valid when trying to buy out a lien from LienToken.sol:buyoutLien(). The current implementation of the function checks whether the rate increased rather than decreased, resulting in invalid refinances being approved and valid refinances being rejected. This is an issue because it means users can perform invalid refinances with the wrong parameters, and users who should be able to perform refinances at better rates will not be able to. 

The code snippet provided shows the logic used to check the rate, which should be flipped to the following:

```solidity
uint256 maxNewRate = uint256(lien.rate) - minInterestBPS;
return (newLien.rate <= maxNewRate...
```

The bug was found by obront, 0xRajeev, and hansfriese, and the discussion that followed was about whether the issue should be escalated for 1 USDC, which was rejected due to it not being a major loss of funds, but still being a severe flaw that would hurt the protocol.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/21 

## Found by 
obront, 0xRajeev, hansfriese

## Summary

The math in `isValidRefinance()` checks whether the rate increased rather than decreased, resulting in invalid refinances being approved and valid refinances being rejected.

## Vulnerability Detail

When trying to buy out a lien from `LienToken.sol:buyoutLien()`, the function calls `AstariaRouter.sol:isValidRefinance()` to check whether the refi terms are valid.

```solidity
if (!ASTARIA_ROUTER.isValidRefinance(lienData[lienId], ld)) {
  revert InvalidRefinance();
}
```
One of the roles of this function is to check whether the rate decreased by more than 0.5%. From the docs:

> An improvement in terms is considered if either of these conditions is met:
> - The loan interest rate decrease by more than 0.5%.
> - The loan duration increases by more than 14 days.

The current implementation of the function does the opposite. It calculates a `minNewRate` (which should be `maxNewRate`) and then checks whether the new rate is greater than that value.

```solidity
uint256 minNewRate = uint256(lien.rate) - minInterestBPS;
return (newLien.rate >= minNewRate ...
```

The result is that if the new rate has increased (or decreased by less than 0.5%), it will be considered valid, but if it has decreased by more than 0.5% (the ideal behavior) it will be rejected as invalid.

## Impact

- Users can perform invalid refinances with the wrong parameters.
- Users who should be able to perform refinances at better rates will not be able to.

## Code Snippet

https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/AstariaRouter.sol#L482-L491

## Tool used

Manual Review

## Recommendation

Flip the logic used to check the rate to the following:

```solidity
uint256 maxNewRate = uint256(lien.rate) - minInterestBPS;
return (newLien.rate <= maxNewRate...
```

## Discussion

**IAmTurnipBoy**

Escalate for 1 USDC

Should be medium because no funds at risk

**sherlock-admin**

 > Escalate for 1 USDC
> 
> Should be medium because no funds at risk

You've created a valid escalation for 1 USDC!

To remove the escalation from consideration: Delete your comment.
To change the amount you've staked on this escalation: Edit your comment **(do not create a new comment)**.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**Evert0x**

Escalation rejected.

Not a major loss of funds but definitely a severe flaw that will hurt the protocol.

**sherlock-admin**

> Escalation rejected.
> 
> Not a major loss of funds but definitely a severe flaw that will hurt the protocol.

This issue's escalations have been rejected!

Watsons who escalated this issue will have their escalation amount deducted from their next payout.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | 0xRajeev, obront, hansfriese |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/21
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

