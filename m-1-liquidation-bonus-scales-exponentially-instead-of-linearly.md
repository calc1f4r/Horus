---
# Core Classification
protocol: WagmiLeverage V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30633
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/281
source_link: none
github_link: https://github.com/sherlock-audit/2024-03-wagmileverage-v2-judging/issues/7

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - bughuntoor
---

## Vulnerability Title

M-1: Liquidation bonus scales exponentially instead of linearly.

### Overview


Summary:

The liquidation bonus in the Wagmi Leverage V2 protocol is currently calculated exponentially instead of linearly, leading to users overpaying the bonus when borrowing from multiple lenders. This could result in a loss of funds for users. The issue was identified by bughuntoor and confirmed by the team. The code snippet and tool used for review were provided. The team discussed and decided to fix the issue by making the bonus a percentage of the total borrowed amount. The fix has been implemented and reviewed by the Lead Senior Watson. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-03-wagmileverage-v2-judging/issues/7 

## Found by 
bughuntoor
## Summary
Liquidation bonus scales exponentially instead of linearly. 

## Vulnerability Detail
Let's look at the code of `getLiquidationBonus` 
```solidity
    function getLiquidationBonus(
        address token,
        uint256 borrowedAmount,
        uint256 times
    ) public view returns (uint256 liquidationBonus) {
        // Retrieve liquidation bonus for the given token
        Liquidation memory liq = liquidationBonusForToken[token];
        unchecked {
            if (liq.bonusBP == 0) {
                // If there is no specific bonus for the token
                // Use default bonus
                liq.minBonusAmount = Constants.MINIMUM_AMOUNT;
                liq.bonusBP = dafaultLiquidationBonusBP;
            }
            liquidationBonus = (borrowedAmount * liq.bonusBP) / Constants.BP;

            if (liquidationBonus < liq.minBonusAmount) {
                liquidationBonus = liq.minBonusAmount;
            }
            liquidationBonus *= (times > 0 ? times : 1);
        }
    }
```
As we can see, the liquidation bonus is based on the entire `borrowAmount`  and multiplied by the number of new loans added.
The problem is that it is unfair when the user makes a borrow against multiple lenders.

If a user takes a borrow for X against 1 lender, they'll have to pay a liquidation bonus of Y.
However, if they take a borrow for 3X against 3 lenders, they'll have to pay 9Y, meaning that taking a borrow against N lenders leads to overpaying liquidation bonus by N times. 

Furthermore, if the user simply does it in multiple transactions, they can avoid these extra fees (as they can simply call `borrow` for X 3 times and pay 3Y in Liquidation bonuses)

## Impact
Loss of funds

## Code Snippet
https://github.com/sherlock-audit/2024-03-wagmileverage-v2/blob/main/wagmi-leverage/contracts/LiquidityBorrowingManager.sol#L280

## Tool used

Manual Review

## Recommendation
make liquidation bonus simply a % of totalBorrowed



## Discussion

**fann95**

We discussed as a team multiplying the bonus depending on the method of taking out a loan and ultimately decided to abandon it completely.
a few days ago I made the corresponding commit https://github.com/RealWagmi/wagmi-leverage/commit/7575ab6659e99e59f5b7b7d1454649091c0295c6

**sherlock-admin4**

The protocol team fixed this issue in PR/commit https://github.com/RealWagmi/wagmi-leverage/commit/7575ab6659e99e59f5b7b7d1454649091c0295c6.

**sherlock-admin3**

2 comment(s) were left on this issue during the judging contest.

**WangAudit** commented:
> decided that it's a H not an M cause even if it's intended behaviour; user can easily bypass it; or if it's not intended' then it will be applied every time when times > 2

**takarez** commented:
>  i think that is a design choice to charge whenever there's a borrow.



**fann95**

> 2 comment(s) were left on this issue during the judging contest.
> 
> **WangAudit** commented:
> 
> > decided that it's a H not an M cause even if it's intended behaviour; user can easily bypass it; or if it's not intended' then it will be applied every time when times > 2
> 
> **takarez** commented:
> 
> > i think that is a design choice to charge whenever there's a borrow.

The liquidation bonus was charged more than initially expected, so the user’s cunning could only lead to a fair payment. But ultimately the bonus would still be returned to the trader. The trader paid a more liquidation bonus if he extracted more than one  NFT position, which in itself is a rare case... anyway, we removed it from the code..

**spacegliderrrr**

Fix looks good, liquidation bonus is now correctly proportional to borrow amount, no matter the number of lenders.

**sherlock-admin4**

The Lead Senior Watson signed off on the fix.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | WagmiLeverage V2 |
| Report Date | N/A |
| Finders | bughuntoor |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-03-wagmileverage-v2-judging/issues/7
- **Contest**: https://app.sherlock.xyz/audits/contests/281

### Keywords for Search

`vulnerability`

