---
# Core Classification
protocol: Blueberry Update
chain: everychain
category: uncategorized
vulnerability_type: coding-bug

# Attack Vector Details
attack_type: coding-bug
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18500
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/69
source_link: none
github_link: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/114

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:
  - coding-bug

protocol_categories:
  - lending
  - leveraged_farming
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Ch\_301
---

## Vulnerability Title

M-6: M-03 wrong token address on `ShortLongSpell.sol`

### Overview


This bug report is about an issue found in the ShortLongSpell.sol contract, which is part of the Sherlock Audit 2023-04-blueberry-judging project. The issue is that the wrong token address is being passed to the SoftVault contract. This means that the Short/Long Spell will never work.

The issue was found by Ch_301 and confirmed by hrishibhat. It was then escalated for 10 USDC. The bug was caused because the `uToken` address was being passed instead of the `strategy.vault` address.

The issue can be fixed by changing the code snippet in two places. The first code snippet is located at ShortLongSpell.sol#L128-L141, and the second is located at ShortLongSpell.sol#L229-L234. The changes should be made according to the recommendations given in the report.

After the issue is fixed, the contestants' payouts and scores will be updated according to the changes made.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/114 

## Found by 
Ch\_301
## Summary

## Vulnerability Detail
[ShortLongSpell.openPosition()](https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/spell/ShortLongSpell.sol#LL111C4-L151C6) send `uToken` to SoftVault then deposit it into the Compound protocol to earn a passive yield. In return, SPELL receives share tokes of SoftVault  `address(strategy.vault)`  

`WERC20.sol` should receive `address(strategy.vault)` token, but the logic of `ShortLongSpell.sol` subcall (WERC20.sol) `wrapper.burn()` and pass the `uToken` address (please check the Code Snippet part) instead of `strategy.vault` address

## Impact
Short/Long Spell will never work

## Code Snippet
1- https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/spell/ShortLongSpell.sol#L128-L141
```solidity
            address burnToken = address(ISoftVault(strategy.vault).uToken());
            if (collSize > 0) {
                if (posCollToken != address(wrapper))
                    revert Errors.INCORRECT_COLTOKEN(posCollToken);
                bank.takeCollateral(collSize);
                wrapper.burn(burnToken, collSize);
                _doRefund(burnToken);
            }
```
2- https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/spell/ShortLongSpell.sol#L229-L234
```solidity
        // 1. Take out collateral
        bank.takeCollateral(param.amountPosRemove);
        werc20.burn(
            address(ISoftVault(strategy.vault).uToken()),
            param.amountPosRemove
        );
```

## Tool used

Manual Review

## Recommendation
1- 
```diff
-            address burnToken = address(ISoftVault(strategy.vault).uToken());
+            address burnToken = strategy.vault;
            if (collSize > 0) {
                if (posCollToken != address(wrapper))
                    revert Errors.INCORRECT_COLTOKEN(posCollToken);
                bank.takeCollateral(collSize);
                wrapper.burn(burnToken, collSize);
                _doRefund(burnToken);
            }
```
2- 
```diff
        // 1. Take out collateral
        bank.takeCollateral(param.amountPosRemove);
        werc20.burn(
-            address(ISoftVault(strategy.vault).uToken()),
+            strategy.vault,
            param.amountPosRemove
        );
```



## Discussion

**Ch-301**

Escalate for 10 USDC

The same reason as #116 but in a different implementation and it needs another solution 

**sherlock-admin**

 > Escalate for 10 USDC
> 
> The same reason as #116 but in a different implementation and it needs another solution 

You've created a valid escalation for 10 USDC!

To remove the escalation from consideration: Delete your comment.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**hrishibhat**

Escalation accepted

Valid medium
This is a valid issue


**sherlock-admin**

> Escalation accepted
> 
> Valid medium
> This is a valid issue
> 

    This issue's escalations have been accepted!

    Contestants' payouts and scores will be updated according to the changes made on this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry Update |
| Report Date | N/A |
| Finders | Ch\_301 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/114
- **Contest**: https://app.sherlock.xyz/audits/contests/69

### Keywords for Search

`Coding-Bug`

