---
# Core Classification
protocol: Timeless
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6760
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Timeless-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Timeless-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - yield
  - yield_aggregator
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - JayJonah
  - Christoph Michel
---

## Vulnerability Title

xPYT auto-compound does not take pounder reward into account

### Overview


This bug report is about the xPYT.sol#L179 function in the xPYT contract. It outlines the steps taken by the function and the impact of the bug. The function claims yieldAmount yield for itself, deposits the yield back to receive more PYT/NYT (Gate.claimYieldEnter), buys xPYT with the NYT, performs a ERC4626.redeem(xPYT) with the bought amount, burning xPYT and receiving pytAmountRedeemed PYT, and performs a ERC4626.deposit(pytAmountRedeemed + yieldAmount = pytCompounded). The assetBalance is correctly updated for the first four steps but does not decrease by the pounder reward which is transferred out in the last step.

The impact of this bug is that the contract has a smaller assets (PYT) balance than what is tracked in assetBalance. This means that future depositors will have to make up for it as sweep computes the difference between these two values. Additionally, the xPYT exchange ratio is wrongly updated and withdrawers can redeem xPYT for more assets than they should until the last withdrawer is left holding valueless xPYT.

The recommendation is that the assetBalance should also decrease by the pounderReward. Consider adding a test that verifies correct assetBalance updates. The bug has been implemented in PR #2 and acknowledged.

### Original Finding Content

## High Risk Report

## Severity
**High Risk**

## Context
`xPYT.sol#L179`

## Description
Conceptually, the `xPYT.pound` function performs the following steps:

1. Claims `yieldAmount` yield for itself, deposits the yield back to receive more PYT/NYT (Gate.claimYieldEnter).
2. Buys `xPYT` with the NYT.
3. Performs a `ERC4626.redeem(xPYT)` with the bought amount, burning `xPYT` and receiving `pytAmountRedeemed` PYT.
4. Performs a `ERC4626.deposit(pytAmountRedeemed + yieldAmount = pytCompounded)`.
5. Pays out a reward in PYT to the caller.

The `assetBalance` is correctly updated for the first four steps but does not decrease by the pounder reward, which is transferred out in the last step. 

### Impact
- The contract has a smaller assets (PYT) balance than what is tracked in `assetBalance`.
- Future depositors will have to make up for it as `sweep` computes the difference between these two values.
- The `xPYT` exchange ratio is wrongly updated and withdrawers can redeem `xPYT` for more assets than they should until the last withdrawer is left holding valueless `xPYT`.

### Example
Consider the following example and assume 100% fees for simplicity, i.e., `pounderReward = pytCompounded`.

- **Vault total**: 1k assets, 1k shares total supply.
- **Pound with 100% fee**:
  - Claims `YPYT/NYT`.
  - Swaps `YNYT` to `XxPYT`.
  - Redeems `XxPYT` for `XPYT` by burning `XxPYT` (supply -= X, exchange ratio is 1-to-1 in example).
  - `assetBalance` is increased by claimed `YPYT`.
  - Pounder receives a pounder reward of `X + Y PYT` but does not decrease `assetBalance` by pounder reward `X+Y`.

- **Vault totals** should be `1k-X` assets, `1k-X` shares, keeping the same share price.
- Nevertheless, vault totals actually are `1k+Y` assets, `1k-X` shares. Although pounder receives 100% of pounding rewards, the `xPYT` price `(assets / shares)` increased.

## Recommendation
The `assetBalance` should also decrease by the `pounderReward`.

```solidity
- unchecked {
- assetBalance += yieldAmount;
- }
+ // using unchecked should still be fine? as pounderReward <= yieldAmount + pytAmountRedeemed. and pytAmountRedeemed must have already been in the contract because of the implicit /grave.ts1redeem /grave.ts1, i.e., assetBalance >= pytAmountRedeemed, !, !
+ assetBalance = assetBalance + yieldAmount - pounderReward;
```

Consider adding a test that verifies correct `assetBalance` updates.

## Timeless
Implemented in PR #2.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Timeless |
| Report Date | N/A |
| Finders | JayJonah, Christoph Michel |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Timeless-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Timeless-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

