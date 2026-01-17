---
# Core Classification
protocol: Aave Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16939
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/aaveprotocol.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/aaveprotocol.pdf
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
  - Gustavo Grieco
  - Dominik Czarnota
  - Michael Colburn
---

## Vulnerability Title

There is no way to redeem all available tokens when Lending Pool parameters are close to the redemption limit

### Overview


This bug report is about the redeem function in the LendingPool.sol smart contract. The redeem function provides no way to specify to redeem the maximum amount of available tokens, forcing the user to guess this amount. A user can get back their deposited funds using the redeem function, but it is restricted in two ways: the user must have enough aToken balance to cover the amount to redeem, and the health liquidation factor should be above a certain threshold. This can be a significant obstacle for the user trying to redeem their tokens. 

In an exploit scenario, Alice has a large amount of tokens and during a bank run, she tries to redeem all of them. She repeatedly fails to do so, since she specifies too many tokens to redeem, and is forced to redeem her tokens in small batches, which costs more gas. 

The recommendation is to properly implement a mechanism to redeem all the available tokens, given the current liquidity and health liquidation factor. As an alternative, document this behavior to warn users about this constraint. In the long term, consider using Echidna and Manticore to test that users can redeem the maximum amount of their token using redeem.

### Original Finding Content

## Type: Timing
**Target:** LendingPool.sol

**Difficulty:** High

## Description
If the available liquidity or health metric are close to the acceptable limits, the redeem function provides no way to specify to redeem the maximum amount of available tokens, forcing the user to guess this amount.

Users can get back their deposited funds using the redeem function:

```solidity
function redeem( address _aToken, uint256 _aTokenAmount) external nonReentrant {
    AToken aToken = AToken(_aToken);
    address reserve = aToken.getUnderlyingAssetAddress();
    uint256 underlyingAmountToRedeem = 0;
    uint256 aTokenBalance = aToken.balanceOf(msg.sender);
    require (
        aTokenBalance >= _aTokenAmount && _aTokenAmount > 0,
        "The aToken user balance is not enough to cover the amount to redeem or the amount to redeem is 0"
    );

    // calculate underlying to redeem
    underlyingAmountToRedeem = aToken.aTokenAmountToUnderlyingAmount(_aTokenAmount);
    aToken.burnOnRedeem(msg.sender, _aTokenAmount);
    uint256 currentAvailableLiquidity = core.getReserveAvailableLiquidity(reserve);
    require (currentAvailableLiquidity >= underlyingAmountToRedeem,
        "There is not enough liquidity available to redeem"
    );

    // compound liquidity and variable borrow interests
    core.updateReserveCumulativeIndexes(reserve);
    (,,,,, uint256 healthFactor) = dataProvider.calculateUserGlobalData(msg.sender);
    
    // at this point, the withdraw should not trigger the liquidation
    require (
        healthFactor > dataProvider.getHealthFactorLiquidationThreshold(),
        "Redeem would bring the loan in a liquidation state thus cannot be accepted"
    );

    /**
    @dev update reserve data
    */
    core.decreaseReserveTotalLiquidity(reserve, underlyingAmountToRedeem);
    core.updateReserveInterestRates(reserve);
    core.setReserveLastUpdate(reserve);
    core.transferToUser(reserve, msg.sender, underlyingAmountToRedeem);
    emit Redeem(_aToken, msg.sender, _aTokenAmount, underlyingAmountToRedeem);
}
```
**Figure 11.1:** redeem function in LendingPool.sol

However, redemption is restricted: it should have enough liquidity available and the health liquidation factor should be above a certain threshold. When a user tries to redeem all their tokens while the Lending Pool parameters are close to the redemption limit, it is very difficult for the user to determine how many tokens can be redeemed. There is no option to specify to redeem as much as possible, as in the repay function. This can be a significant obstacle for the user trying to redeem their tokens.

## Exploit Scenario
Alice has a large amount of tokens. During a bank run, she tries to redeem all of them. She repeatedly fails to do so, since she specifies too many tokens to redeem. As a result, Alice is forced to redeem her tokens in small batches, which costs more gas.

## Recommendation
**Short term:** Properly implement a mechanism to redeem all the available tokens, given the current liquidity and health liquidation factor. As an alternative, document this behavior to warn users about this constraint.

**Long term:** Consider using Echidna and Manticore to test that users can redeem the maximum amount of their token using redeem.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Aave Protocol |
| Report Date | N/A |
| Finders | Gustavo Grieco, Dominik Czarnota, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/aaveprotocol.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/aaveprotocol.pdf

### Keywords for Search

`vulnerability`

