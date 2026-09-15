---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17899
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
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

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels
  - Natalie Chin
  - Maximilian Krüger
---

## Vulnerability Title

Curve AMO assumes the collateral ratio to be constant

### Overview

See description below for full details.

### Original Finding Content

## Type: Undefined Behavior
**Target:** FRAXStablecoin/Address.sol

**Difficulty:** N/A

## Description
When calculating the amount of collateral available to the AMO, the `CurveAMO_V3` contract assumes that the collateral ratio will not change. The protocol calculates the amount of underlying collateral the AMO has access to by finding the balance of USDC it can withdraw if the price of FRAX were to drop to the CR. Since FRAX is always backed by collateral at the value of the CR, it should never go below the value of the collateral itself. For example, FRAX should never go below $0.85 at an 85% CR. This calculation is the safest and most conservative way to calculate the amount of collateral the Curve AMO has access to. This allows the Curve AMO to mint FRAX to place inside the pool in addition to USDC collateral to tighten the peg while knowing exactly how much collateral it has access to if FRAX were to break its peg.

![Figure 19.1: Frax Curve Documentation](<link to figure>)

This assumption is evident in the `mintRedeemPart1` function, which is used to retrieve the global collateral ratio of the stablecoin protocol:

```solidity
// This is basically a workaround to transfer USDC from the FraxPool to this investor contract
// This contract is essentially marked as a 'pool' so it can call OnlyPools functions 
// like pool_mint and pool_burn_from on the main FRAX contract
// It mints FRAX from nothing, and redeems it on the target pool for collateral and FXS
// The burn can be called separately later on
function mintRedeemPart1(uint256 frax_amount) external onlyByOwnerOrGovernance {
    //require(allow_yearn || allow_aave || allow_compound, 'All strategies are currently off');
    uint256 redemption_fee = pool.redemption_fee();
    uint256 col_price_usd = pool.getCollateralPrice();
    uint256 global_collateral_ratio = FRAX.global_collateral_ratio();
    uint256 redeem_amount_E6 = (frax_amount.mul(uint256(1e6).sub(redemption_fee))).div(1e6).div(10 ** missing_decimals);
    uint256 expected_collat_amount = redeem_amount_E6.mul(global_collateral_ratio).div(1e6);
    expected_collat_amount = expected_collat_amount.mul(1e6).div(col_price_usd);
}
```

![Figure 19.2: contracts/Curve/CurveAMO_V3.sol#L310-L322](<link to figure>)

The contract uses the following formula to determine the value of `expected_collat_amount`:

```
expected_collat_amount = (frax_amount * 1e6 - redemption_fee) * (1e6 * missing_decimals) / 
                           (frax_amount * 1e6 - redemption_fee * global_collateral_ratio)
                           * (global_collateral_ratio / 1e6) * (1e6 / collateral price in USD)
```

The Curve AMO uses the pool to establish a price floor for FRAX. However, if the global collateral ratio changes (violating the contract’s assumption that it will not), the available collateral will scale up or down, depending on the change.

## Exploit Scenario
Alice, a Frax Finance administrator, calls `mintRedeemPart1` to transfer USDC from the `FraxPool` to the `CurveAMO_V3` contract. However, the global collateral ratio simultaneously decreases, so the contract receives less collateral than expected.

## Recommendations
- **Short term:** Analyze the effects of a change in the global collateral ratio on the expected value of collateral.
- **Long term:** Analyze the implications of transaction atomicity for all blockchains in which this code will be deployed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels, Natalie Chin, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf

### Keywords for Search

`vulnerability`

