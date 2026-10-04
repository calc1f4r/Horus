---
# Core Classification
protocol: Blueberry Update
chain: everychain
category: uncategorized
vulnerability_type: vault

# Attack Vector Details
attack_type: vault
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18502
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/69
source_link: none
github_link: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/116

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
  - vault
  - configuration
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

M-8: asking for the wrong address for `balanceOf()`

### Overview


This bug report is about an issue found in the code of the ShortLongSpell contract in the 2023-04-blueberry-judging Github repository. The issue is that the wrong address is being asked for the `balanceOf()` function. This issue was found by Ch_301 and was escalated for 10 USDC. 

The vulnerability detail is that the `openPosition()` function passes the wrong value of `balanceOf()` to the `_doPutCollateral()` function. The impact of this issue is that `openPosition()` will never work. The code snippet of the issue is provided in the report. The tool used to find the issue was Manual Review. 

The recommendation for the issue is to change the code snippet as shown in the report. The discussion section shows that the issue was accepted as a valid medium as the issue does not clearly identify the impact where the tokens can be stolen, but still correctly recognizes the underlying issue. 

Thus, this bug report is about an issue found in the code of the ShortLongSpell contract in the 2023-04-blueberry-judging Github repository. The issue was found by Ch_301 and was accepted as a valid medium. The impact of this issue is that `openPosition()` will never work. The recommendation is to change the code snippet as shown in the report.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/116 

## Found by 
Ch\_301
## Summary

## Vulnerability Detail
ShortLongSpell.[openPosition()](https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/spell/ShortLongSpell.sol#L143-L150) pass to `_doPutCollateral()` wrong value of `balanceOf()`
```solidity
        // 5. Put collateral - strategy token
        address vault = strategies[param.strategyId].vault;
        _doPutCollateral(
            vault,
            IERC20Upgradeable(ISoftVault(vault).uToken()).balanceOf(
                address(this)
            )
        );
```
the balance should be of `address(vault)`

## Impact
- `openPosition()` will never work

## Code Snippet

## Tool used

Manual Review

## Recommendation
```diff
        // 5. Put collateral - strategy token
        address vault = strategies[param.strategyId].vault;
        _doPutCollateral(
            vault,
-            IERC20Upgradeable(ISoftVault(vault).uToken()).balanceOf(
-                address(this)
+                IERC20Upgradeable(vault).balanceOf(address(this))
            )
        );
```



## Discussion

**Ch-301**

Escalate for 10 USDC

This is a simple finding when you know that `SoftVault` is transferring all `uToken` to Compound to generate yield 

Also of wonder the judge set this as invalid but he submitted both this and #114  in the next contest **Blueberry Update 2**

**sherlock-admin**

 > Escalate for 10 USDC
> 
> This is a simple finding when you know that `SoftVault` is transferring all `uToken` to Compound to generate yield 
> 
> Also of wonder the judge set this as invalid but he submitted both this and #114  in the next contest **Blueberry Update 2**

You've created a valid escalation for 10 USDC!

To remove the escalation from consideration: Delete your comment.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**hrishibhat**

Escalation accepted

Valid medium
Since the issue does not clearly identify the impact where the tokens can be stolen, but still correctly recognizes the underlying issue considering this a valid medium. 



**sherlock-admin**

> Escalation accepted
> 
> Valid medium
> Since the issue does not clearly identify the impact where the tokens can be stolen, but still correctly recognizes the underlying issue considering this a valid medium. 
> 
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
- **GitHub**: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/116
- **Contest**: https://app.sherlock.xyz/audits/contests/69

### Keywords for Search

`Vault, Configuration, Coding-Bug`

