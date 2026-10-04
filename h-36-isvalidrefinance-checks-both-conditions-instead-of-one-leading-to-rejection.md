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
solodit_id: 3674
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/22

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
finders_count: 1
finders:
  - obront
---

## Vulnerability Title

H-36: isValidRefinance checks both conditions instead of one, leading to rejection of valid refinances

### Overview


This bug report is about the `isValidRefinance()` function in the AstariaRouter.sol file of the Sherlock-Audit project. This function is intended to check whether either (a) the loan interest rate decreased sufficiently or (b) the loan duration increased sufficiently when trying to buy out a lien. However, the current implementation requires both of these conditions to be met, leading to the rejection of valid refinances. The code snippet and recommendation for fixing this issue have been included in the report. The issue has been discussed and an escalation for 1 USDC was rejected.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/22 

## Found by 
obront

## Summary

`isValidRefinance()` is intended to check whether either (a) the loan interest rate decreased sufficiently or (b) the loan duration increased sufficiently. Instead, it requires both of these to be true, leading to the rejection of valid refinances.

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

The currently implementation of the code requires both of these conditions to be met:

```solidity
return (
    newLien.rate >= minNewRate &&
    ((block.timestamp + newLien.duration - lien.start - lien.duration) >= minDurationIncrease)
);
```

## Impact

Valid refinances that meet one of the two criteria will be rejected.

## Code Snippet

https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/AstariaRouter.sol#L488-L490

## Tool used

Manual Review

## Recommendation

Change the AND in the return statement to an OR:

```solidity
return (
    newLien.rate >= minNewRate ||
    ((block.timestamp + newLien.duration - lien.start - lien.duration) >= minDurationIncrease)
);
```

## Discussion

**SantiagoGregory**

Independently fixed during our own review so there's no PR specifically for this, but this is now updated to an or.

**IAmTurnipBoy**

Escalate for 1 USDC

Should be medium because there are no funds at risk

**sherlock-admin**

 > Escalate for 1 USDC
> 
> Should be medium because there are no funds at risk

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
| Finders | obront |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/22
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

