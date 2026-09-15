---
# Core Classification
protocol: Blueberry Update
chain: everychain
category: economic
vulnerability_type: slippage

# Attack Vector Details
attack_type: slippage
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18485
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/69
source_link: none
github_link: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/124

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
  - slippage
  - sandwich_attack
  - flash_loan

protocol_categories:
  - lending
  - leveraged_farming
  - options_vault

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Ch\_301
  - 0x52
  - Breeje
  - n1punp
---

## Vulnerability Title

H-5: ConvexSpell#closePositionFarm removes liquidity without any slippage protection

### Overview


This bug report is about the ConvexSpell and CurveSpell smart contracts, which are used to remove liquidity from Curve pools. The issue is that these smart contracts remove liquidity without any slippage protection, which makes them vulnerable to sandwich attacks. This means that user withdrawals can be sandwiched and stolen. The code snippets which are vulnerable to this attack are ConvexSpell.sol#L147-L230 and CurveSpell.sol#L143-L223. The bug was found by 0x52, Breeje, Ch_301, and n1punp. The recommended solution is to allow users to specify a minimum out.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/124 

## Found by 
0x52, Breeje, Ch\_301, n1punp
## Summary

ConvexSpell#closePositionFarm removes liquidity without any slippage protection allowing withdraws to be sandwiched and stolen. Curve liquidity has historically been strong but for smaller pairs their liquidity is getting low enough that it can be manipulated via flashloans. 

## Vulnerability Detail

[ConvexSpell.sol#L204-L208](https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/spell/ConvexSpell.sol#L204-L208)

            ICurvePool(pool).remove_liquidity_one_coin(
                amountPosRemove,
                int128(tokenIndex),
                0
            );

Liquidity is removed as a single token which makes it vulnerable to sandwich attacks but no slippage protection is implemented. The same issue applies to CurveSpell.

## Impact

User withdrawals can be sandwiched

## Code Snippet

[ConvexSpell.sol#L147-L230](https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/spell/ConvexSpell.sol#L147-L230)

[CurveSpell.sol#L143-L223](https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/spell/CurveSpell.sol#L143-L223)

## Tool used

Manual Review

## Recommendation

Allow user to specify min out

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry Update |
| Report Date | N/A |
| Finders | Ch\_301, 0x52, Breeje, n1punp |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/124
- **Contest**: https://app.sherlock.xyz/audits/contests/69

### Keywords for Search

`Slippage, Sandwich Attack, Flash Loan`

