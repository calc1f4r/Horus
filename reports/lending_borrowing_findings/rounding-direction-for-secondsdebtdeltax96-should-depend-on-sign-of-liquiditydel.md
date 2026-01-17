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
solodit_id: 43614
audit_firm: ConsenSys
contest_link: none
source_link: https://diligence.consensys.io/audits/2024/08/ramses-v3/
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  -  Arturo Roura
  -  Vladislav Yaroshuk
                        
  - Heiko Fisch
---

## Vulnerability Title

Rounding Direction for secondsDebtDeltaX96 Should Depend on Sign of liquidityDelta ✓ Fixed

### Overview


This bug report discusses an issue with the debt mechanism in the Ramses-V3 platform. The code is rounding in a way that favors the user instead of the platform, which could potentially lead to an exploit. The recommended solution is to round in the direction that benefits the platform instead. This bug has been fixed in a recent commit.

### Original Finding Content

#### Resolution



 Fixed in commit [0e0d40c6f715520ebb179acbebbd229ec9372cda](https://github.com/RamsesExchange/Ramses-V3/pull/3/commits/0e0d40c6f715520ebb179acbebbd229ec9372cda).
 

#### Description


The debt mechanism to calculate the period\-seconds the position has been in range from its liquidity and period\-SPL at the end of the period has already been discussed briefly in [issue 6\.1](#debt-is-added-instead-of-subtracted-in-positionperiodsecondsinrange)​. As a reminder, when liquidity is *added* to a position, we’ll later *overestimate* the period\-seconds in range, and we’re *increasing* the `secondsDebt96`. If, on the other hand, liquidity is *removed* from a position, we’ll later *underestimate* the period seconds in range, and `secondsDebt96` is *decreased*:


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
As can be seen in the code above, when calculating the `secondsDebtX96Delta`, we’re always rounding up. Since rounding should occur in the direction that favors the protocol – which, in our case, means the value `secondsDebtX96` should always be rounded up because it has to be subtracted at the end – a value that is added to `secondsDebtX96` should be rounded up, and a value that is subtracted from `secondsDebtX96` should be rounded down. However, in the code above, the same (rounded\-up) value is used for both cases, giving the liquidity provider a rounding advantage.


#### Recommendation


Rounding in the direction that benefits the user instead of the protocol is dangerous. There have been several cases in the past where a small rounding error could be amplified in some way or other and led to a massive exploit. So even if a rounding error seems small and not amplifiable, we always recommend rounding in the direction that benefits the protocol.


Specifically, in the situation above, `secondsDebtDeltaX96` should be rounded down when `liquidityDelta` is negative.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

