---
# Core Classification
protocol: Ondo Finance: Ondo Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17493
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-shimacapital-ondo-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-shimacapital-ondo-securityreview.pdf
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
  - Damilola Edwards
  - Anish Naik
  - Justin Jacob
---

## Vulnerability Title

Risk of accounting errors due to missing check in the invest function

### Overview


This bug report is about an issue in the invest function in the Treasury.sol contract. The issue is that the invest function is not doing a sufficient check to ensure that the collateralToken address of the supplied collateralIndex value matches the token accepted by the strategy. This could result in incorrect profit-and-loss (PnL) reporting, leading to the loss of user or protocol funds. 

The exploit scenario involves a fund manager, Bob, triggering investments into the Compound strategy using FRAX tokens instead of USDC, which should be the accepted token. Because of insufficient validation of the collateralToken value, the transaction succeeds, causing a mismatch between the treasury’s account and the total value of assets in the strategy.

To address this issue, a short-term recommendation is to implement a check within the invest function to ensure that the collateralToken address of the supplied collateralIndex value matches the token accepted by the strategy. A long-term recommendation is to carefully review token usage across all contracts to ensure that each token’s decimal places are taken into consideration.

### Original Finding Content

## Diﬃculty: Low

## Type: Data Validation

## Description
Because of a missing check in the invest function, investing multiple tokens with different decimals in the same strategy will result in incorrect profit-and-loss (PnL) reporting, which could result in the loss of user or protocol funds.

The invest function is responsible for transferring funds from the treasury to a strategy and for updating the strategy’s investment balance (i.e., `strategyInvestedAmount`). However, the invest function accepts any token in the collateral array alongside the token amounts to be transferred. Therefore, if multiple tokens with different decimals are used to invest in the same strategy, the treasury’s investment records would not accurately reflect the true balance of the strategy, resulting in accounting errors within the protocol.

```solidity
IERC20 collateralToken = collateral[collateralIndex].collateralToken;
require(
function invest(
    address strategy,
    uint256 collateralAmount,
    uint256 collateralIndex
    address(collateralToken) != address(0),
    "Treasury: Cannot used a removed collateral token"
);
// Require that the strategy address is approved
require(
    hasRole(strategy, Roles.STRATEGY_CONTRACT),
    "Treasury: Must send funds to approved strategy contract"
// Transfer collateral to strategy
collateralToken.safeTransfer(strategy, collateralAmount);
// Account for investment in strategyInvestedAmounts
strategyInvestedAmounts[strategy] += collateralAmount;
// Scale up invested amount
investedAmount += _scaleUp(collateralAmount, collateralIndex);
);
```
*Figure 2.1: The invest function in Treasury.sol#L694–719*

## Exploit Scenario
The CompoundStrategy contract is supposed to accept only USDC as its investment token. However, the fund manager, Bob, triggers investments into the Compound strategy using FRAX tokens instead. Due to insufficient validation of the `collateralToken` value, the transaction succeeds, causing a mismatch between the treasury’s account and the total value of assets in the strategy.

## Recommendations
- **Short term:** Implement a check within the invest function to ensure that the `collateralToken` address of the supplied `collateralIndex` value matches the token accepted by the strategy.
  
- **Long term:** Carefully review token usage across all contracts to ensure that each token’s decimal places are taken into consideration.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Ondo Finance: Ondo Protocol |
| Report Date | N/A |
| Finders | Damilola Edwards, Anish Naik, Justin Jacob |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-shimacapital-ondo-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-shimacapital-ondo-securityreview.pdf

### Keywords for Search

`vulnerability`

