---
# Core Classification
protocol: Blueberry Update
chain: everychain
category: logic
vulnerability_type: configuration

# Attack Vector Details
attack_type: configuration
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18491
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/69
source_link: none
github_link: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/135

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
  - configuration
  - business_logic
  - liquidation

protocol_categories:
  - lending
  - leveraged_farming
  - options_vault

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Ch\_301
  - 0x52
---

## Vulnerability Title

H-11: ShortLongSpell#openPosition can cause user unexpected liquidation when increasing position size

### Overview


This bug report is about ShortLongSpell#openPosition, a function in the ShortLongSpell.sol contract, which can cause users to experience unexpected liquidation when increasing their position size. The bug was discovered by 0x52 and Ch_301 using manual review.

The bug occurs when all of the collateral is sent to the user rather than kept in the position. This can lead to serious issues as the collateral is needed to prevent liquidation. As a result, users may find themselves on the brink of liquidation and a small change in price could lead to their liquidation.

The code snippet for this issue is found in ShortLongSpell.sol#L129-L141. Here, all of the collateral is burned and the user is sent the underlying tokens. This is problematic as it sends all the collateral to the user, leaving the position collateralized by only the isolated collateral.

The impact of this bug is that users may experience unfair liquidation. The recommendation is to not burn the collateral.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/135 

## Found by 
0x52, Ch\_301
## Summary

When increasing a position, all collateral is sent to the user rather than being kept in the position. This can cause serious issues because this collateral keeps the user from being liquidated. It may unexpectedly leave the user on the brink of liquidation where a small change in price leads to their liquidation.

## Vulnerability Detail

[ShortLongSpell.sol#L129-L141](https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/spell/ShortLongSpell.sol#L129-L141)

        {
            IBank.Position memory pos = bank.getCurrentPositionInfo();
            address posCollToken = pos.collToken;
            uint256 collSize = pos.collateralSize;
            address burnToken = address(ISoftVault(strategy.vault).uToken());
            if (collSize > 0) {
                if (posCollToken != address(wrapper))
                    revert Errors.INCORRECT_COLTOKEN(posCollToken);
                bank.takeCollateral(collSize);
                wrapper.burn(burnToken, collSize);
                _doRefund(burnToken);
            }
        }

In the above lines we can see that all collateral is burned and the user is sent the underlying tokens. This is problematic as it sends all the collateral to the user, leaving the position collateralized by only the isolated collateral.

Best case the user's transaction reverts but worst case they will be liquidated almost immediately.  

## Impact

Unfair liquidation for users

## Code Snippet

[ShortLongSpell.sol#L111-L151](https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/spell/ShortLongSpell.sol#L111-L151)

## Tool used

Manual Review

## Recommendation

Don't burn the collateral

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry Update |
| Report Date | N/A |
| Finders | Ch\_301, 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/135
- **Contest**: https://app.sherlock.xyz/audits/contests/69

### Keywords for Search

`Configuration, Business Logic, Liquidation`

