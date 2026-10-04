---
# Core Classification
protocol: Liquity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18037
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/LiquityProtocolandStabilityPoolFinalReport.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/LiquityProtocolandStabilityPoolFinalReport.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Alexander Remie
  - Maximilian Krüger
  - Michael Colburn
---

## Vulnerability Title

Under�low in _computeRewardsPerUnitStaked might cause DoS during liquidation

### Overview

See description below for full details.

### Original Finding Content

## Description

The rounding feedback mechanism of the `_computeRewardsPerUnitStaked` function might cause an underflow, leading the liquidation process to revert. The reversion could prevent certain liquidatable troves from being liquidated.

```solidity
uint LUSDLossNumerator = _debtToOffset.mul(DECIMAL_PRECISION).sub(lastLUSDLossError_Offset);
uint ETHNumerator = _collToAdd.mul(DECIMAL_PRECISION).add(lastETHError_Offset);
if (_debtToOffset >= _totalLUSDDeposits) {
    LUSDLossPerUnitStaked = DECIMAL_PRECISION; // When the Pool depletes to 0, so does each deposit
    lastLUSDLossError_Offset = 0;
} else {
    /*
    * Add 1 to make error in quotient positive. We want "slightly too much" LUSD loss,
    * which ensures the error in any given compoundedLUSDDeposit favors the Stability Pool.
    */
    LUSDLossPerUnitStaked = (LUSDLossNumerator.div(_totalLUSDDeposits)).add(1);
    lastLUSDLossError_Offset = (LUSDLossPerUnitStaked.mul(_totalLUSDDeposits)).sub(LUSDLossNumerator);
}
```
**Figure 5.1:** StabilityPool.sol#L535-L549

The `_computeRewardsPerUnitStaked` function is called from the offset function, which is called from the liquidation functions in the TroveManager. Whenever `_computeRewardsPerUnitStaked` is called, a rounding error “offset” is stored in `lastLUSDLossError_Offset`. During the next call of this function, `lastLUSDLossError_Offset` will be subtracted from `_debtToOffset.mul(DECIMAL_PRECISION)`. If this subtraction causes an underflow, the use of SafeMath will cause a revert, and the transaction will fail.

There are several safeguards, such as a minimum trove debt amount, that should prevent a very low `_debtToOffset` value from being used and causing an underflow. However, they do not eliminate that possibility.

## Exploit Scenario

The TroveManager liquidates a trove, which saves a rounding “offset” value of X. The TroveManager tries to liquidate another trove with a debt, Y, such that `(Y * 1e18) < X`. The transaction reverts because of an underflow. As a result, the trove cannot be liquidated.

## Recommendation

- **Short term:** Calculate the `LUSDLossNumerator` only when necessary, i.e., move it inside the `else`.
- **Long term:** Using Echidna, carry out property-based testing to ensure that unforeseen underflows cannot cause a temporary DoS in the system.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Liquity |
| Report Date | N/A |
| Finders | Alexander Remie, Maximilian Krüger, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/LiquityProtocolandStabilityPoolFinalReport.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/LiquityProtocolandStabilityPoolFinalReport.pdf

### Keywords for Search

`vulnerability`

