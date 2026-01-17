---
# Core Classification
protocol: Blueberry Update #2
chain: everychain
category: uncategorized
vulnerability_type: coding-bug

# Attack Vector Details
attack_type: coding-bug
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18511
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/77
source_link: none
github_link: https://github.com/sherlock-audit/2023-05-blueberry-judging/issues/30

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.40
financial_impact: medium

# Scoring
quality_score: 2
rarity_score: 1

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
  - 0x52
---

## Vulnerability Title

M-2: ShortLongSpell#openPosition attempts to burn wrong token

### Overview


This bug report is about a problem with the ShortLongSpell#openPosition function in the 2023-05-blueberry-judging repository. The issue is that the function attempts to burn vault.uToken when it should be using vault instead, resulting in the function being completely nonfunctional when the user is adding to their position. The code snippet that is causing the issue can be found at https://github.com/sherlock-audit/2023-05-blueberry/blob/main/blueberry-core/contracts/spell/ShortLongSpell.sol#L111-L151. The bug was found by 0x52 using manual review. The recommendation to fix the issue is to burn token should be vault rather than vault.uToken.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-05-blueberry-judging/issues/30 

## Found by 
0x52
## Summary

ShortLongSpell#openPosition attempts to burn vault.uToken when it should be using vault instead. The result is that ShortLongSpell#openPosition will be completely nonfunctional when the user is adding to their position

## Vulnerability Detail

https://github.com/sherlock-audit/2023-05-blueberry/blob/main/blueberry-core/contracts/spell/ShortLongSpell.sol#L133-L140

            address burnToken = address(ISoftVault(strategy.vault).uToken());
            if (collSize > 0) {
                if (posCollToken != address(wrapper))
                    revert Errors.INCORRECT_COLTOKEN(posCollToken);
                bank.takeCollateral(collSize);
                wrapper.burn(burnToken, collSize);
                _doRefund(burnToken);
            }

We see above that the contract attempts to withdraw vault.uToken from the wrapper.

https://github.com/sherlock-audit/2023-05-blueberry/blob/main/blueberry-core/contracts/spell/ShortLongSpell.sol#L145-L150

        _doPutCollateral(
            vault,
            IERC20Upgradeable(ISoftVault(vault).uToken()).balanceOf(
                address(this)
            )
        );

This is in direct conflict with the collateral that is actually deposited which is vault. This will cause the function to always revert when adding to an existing position.

## Impact

ShortLongSpell#openPosition will be completely nonfunctional when the user is adding to their position

## Code Snippet

https://github.com/sherlock-audit/2023-05-blueberry/blob/main/blueberry-core/contracts/spell/ShortLongSpell.sol#L111-L151

## Tool used

Manual Review

## Recommendation

Burn token should be vault rather than vault.uToken

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 2/5 |
| Rarity Score | 1/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry Update #2 |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-05-blueberry-judging/issues/30
- **Contest**: https://app.sherlock.xyz/audits/contests/77

### Keywords for Search

`Coding-Bug`

