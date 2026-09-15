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
solodit_id: 3641
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/245

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
  - bin2chen
---

## Vulnerability Title

H-3: buyoutLien() will cause the vault to fail to processEpoch()

### Overview


This bug report is about an issue found in the LienToken#buyoutLien() function. The issue is that the function does not reduce vault#liensOpenForEpoch when transferring from the vault to another receiver. This means that when vault#processEpoch() checks if vault#liensOpenForEpoch[currentEpoch] is equal to uint256(0), it will fail. This bug was found by bin2chen and was manually reviewed. The code snippet in question can be found at https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L121. The impact of this bug is that processEpoch() may fail. The recommendation is to add a decreaseEpochLienCount() function to the buyoutLien() function. Finally, the escalation of this issue was rejected as the argument was not giving sufficient conviction that it should be tagged as a duplicate.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/245 

## Found by 
bin2chen

## Summary
LienToken#buyoutLien() did not reduce vault#liensOpenForEpoch
when vault#processEpoch()will check vault#liensOpenForEpoch[currentEpoch] == uint256(0)
so processEpoch() will fail

## Vulnerability Detail
when create LienToken , vault#liensOpenForEpoch[currentEpoch] will ++
when repay  or liquidate ,  vault#liensOpenForEpoch[currentEpoch] will --
and LienToken#buyoutLien() will transfer from  vault to to other receiver,so liensOpenForEpoch need reduce 
```solidity
function buyoutLien(ILienToken.LienActionBuyout calldata params) external {
   ....
    /**** tranfer but not liensOpenForEpoch-- *****/
    _transfer(ownerOf(lienId), address(params.receiver), lienId);
  }
```


## Impact
processEpoch() maybe fail

## Code Snippet
https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L121

## Tool used

Manual Review

## Recommendation

```solidity
  function buyoutLien(ILienToken.LienActionBuyout calldata params) external {
....

+   //do decreaseEpochLienCount()
+   address lienOwner = ownerOf(lienId);
+    bool isPublicVault = IPublicVault(lienOwner).supportsInterface(
+      type(IPublicVault).interfaceId
+    );
+    if (isPublicVault && !AUCTION_HOUSE.auctionExists(collateralId)) {      
+        IPublicVault(lienOwner).decreaseEpochLienCount(
+          IPublicVault(lienOwner).getLienEpoch(lienData[lienId].start + lienData[lienId].duration)
+        );
+    }    

    lienData[lienId].last = block.timestamp.safeCastTo32();
    lienData[lienId].start = block.timestamp.safeCastTo32();
    lienData[lienId].rate = ld.rate.safeCastTo240();
    lienData[lienId].duration = ld.duration.safeCastTo32();
    _transfer(ownerOf(lienId), address(params.receiver), lienId);
  }
```

## Discussion

**IAmTurnipBoy**

Escalate for 1 USDC

Duplicate of #194, two sides of the same coin. One points out it that buyout doesn't decrement correctly on one side and the other points out it doesn't increment correctly on the other side

**sherlock-admin**

 > Escalate for 1 USDC
> 
> Duplicate of #194, two sides of the same coin. One points out it that buyout doesn't decrement correctly on one side and the other points out it doesn't increment correctly on the other side

You've created a valid escalation for 1 USDC!

To remove the escalation from consideration: Delete your comment.
To change the amount you've staked on this escalation: Edit your comment **(do not create a new comment)**.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**Evert0x**

Escalation rejected.

The argument is not giving us full conviction this should be tagged as a duplicate.

**sherlock-admin**

> Escalation rejected.
> 
> The argument is not giving us full conviction this should be tagged as a duplicate.

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
| Finders | bin2chen |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/245
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

