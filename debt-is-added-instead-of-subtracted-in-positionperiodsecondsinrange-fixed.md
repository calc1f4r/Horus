---
# Core Classification
protocol: Ramses V3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43610
audit_firm: ConsenSys
contest_link: none
source_link: https://diligence.consensys.io/audits/2024/08/ramses-v3/
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  -  Arturo Roura
  -  Vladislav Yaroshuk
                        
  - Heiko Fisch
---

## Vulnerability Title

Debt Is Added Instead of Subtracted in positionPeriodSecondsInRange ✓ Fixed

### Overview


This report discusses a bug in the Ramses-V3 code, specifically in the `secondsDebtX96` member of the reward information. The bug causes incorrect calculations for the period-seconds a position has been in range, leading to incorrect rewards. The bug is caused by a careless mistake in the code, where the value is added instead of subtracted. This bug can be exploited by adding large amounts of liquidity to a low-liquidity position, resulting in inflated rewards. The recommendation is to fix the code by changing the addition to a subtraction and to implement a more rigorous testing methodology before deploying the code.

### Original Finding Content

#### Resolution



 Fixed in commit [1f0b7a520f7a9378affab0578d872779ad2562d2](https://github.com/RamsesExchange/Ramses-V3/commit/1f0b7a520f7a9378affab0578d872779ad2562d2)


#### Description


When liquidity is added to or removed from a position, the `secondsDebtX96` member of the reward information gets updated. The intention here is to have a *corrective* value that allows to calculate the period\-seconds the position has been in range from its liquidity and period\-SPL *at the end of the period*.


More specifically, when liquidity is *added* to a position, we’ll later *overestimate* the period\-seconds in range, and we’re *increasing* the `secondsDebt96`. If, on the other hand, liquidity is *removed* from a position, we’ll later *underestimate* the period seconds in range, and `secondsDebt96` is *decreased*:


**contracts/CL/core/libraries/Position.sol:L124\-L134**



```
int256 secondsDebtDeltaX96 = SafeCast.toInt256(
    FullMath.mulDivRoundingUp(
        liquidityDelta > 0 ? uint256(uint128(liquidityDelta)) : uint256(uint128(-liquidityDelta)),
        uint256(uint160(secondsPerLiquidityPeriodIntX128)),
        FixedPoint32.Q32
    )
);

self.periodRewardInfo[period].secondsDebtX96 = liquidityDelta > 0
    ? self.periodRewardInfo[period].secondsDebtX96 + secondsDebtDeltaX96
    : self.periodRewardInfo[period].secondsDebtX96 - secondsDebtDeltaX96; // can't overflow since each period is way less than uint31

```
Based on this logic – positive liquidity delta increases debt, negative liquidity delta decreases debt – the correct thing to do in `positionPeriodSecondsInRange` is *subtracting* `secondsDebtX96` from the product of the positions’s liquidity and its period\-SPL, both taken at the end of the period. However, what actually happens is that the value is *added*:


**contracts/CL/core/libraries/Position.sol:L246\-L255**



```
periodSecondsInsideX96 = FullMath.mulDiv(liquidity, secondsPerLiquidityInsideX128, FixedPoint32.Q32);

// Need to check if secondsDebtX96>periodSecondsInsideX96, since rounding can cause underflows
if (secondsDebtX96 < 0 || periodSecondsInsideX96 > uint256(secondsDebtX96)) {
    periodSecondsInsideX96 = secondsDebtX96 < 0
        ? periodSecondsInsideX96 - uint256(-secondsDebtX96)
        : periodSecondsInsideX96 + uint256(secondsDebtX96);
} else {
    periodSecondsInsideX96 = 0;
}

```
Note also that the conditon in the `if` statement is the correct one for subtracting, and, finally, that the name “debt” also suggests that the value should be subtracted instead of added. So this is clearly a careless mistake, and not a subtle error, but the consequences are severe: The result returned by `positionPeriodSecondsInRange` is wrong, unless `secondsDebtX96` happens to be 0\. As this value is used for the calculation of rewards, this also means that the rewards are generally wrong. Moreover, it is directly exploitable: By starting with a low\-liquidity position and adding a lot of liquidity a bit later, thereby creating a huge debt, the period\-seconds in range for the position – and therefore the rewards – can be excessively inflated.


#### Recommendation


The addition has to be changed to a subtraction. Concretely, the two lines



```
                ? periodSecondsInsideX96 - uint256(-secondsDebtX96)
                : periodSecondsInsideX96 + uint256(secondsDebtX96);

```
have to be replaced with



```
                ? periodSecondsInsideX96 + uint256(-secondsDebtX96)
                : periodSecondsInsideX96 - uint256(secondsDebtX96);

```
Since this mistake does not only surface for exotic edge cases but almost always leads to a wrong reward when positions are modified, the presence of this bug also exhibits deficiencies with the test methodology. We strongly recommend implementing a rigorous and comprehensive test methodology before considering a production deployment.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Ramses V3 |
| Report Date | N/A |
| Finders |  Arturo Roura,  Vladislav Yaroshuk
                        , Heiko Fisch |

### Source Links

- **Source**: https://diligence.consensys.io/audits/2024/08/ramses-v3/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

