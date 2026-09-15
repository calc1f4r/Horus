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
solodit_id: 16936
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/aaveprotocol.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/aaveprotocol.pdf
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
  - Gustavo Grieco
  - Dominik Czarnota
  - Michael Colburn
---

## Vulnerability Title

redeem does not properly validate parameters and allows drainage of funds

### Overview


This bug report concerns a data validation issue in the LendingPool.sol smart contract. It is classified as a low difficulty issue. The attacker could use the redeem function with a specially crafted AToken contract to steal all the available liquidity. The redeem function allows users to get back their funds, given the address of an AToken contract and the amount to redeem. However, since it does not check the validity of the supplied AToken contract, it allows any user to control the amount of liquidity to redeem in the underlyingAmountToRedeem variable. 

The exploit scenario is that an attacker can create a specially crafted AToken contract to redeem any user funds, given there is enough liquidity. Such contract just return arbitrary amounts when the balanceOf and the aTokenAmountToUnderlyingAmount functions are called, in order to perform the exploit.

The recommendation is to short-term properly validate the provided _aToken address using the corresponding reserve and long-term add proper unit tests to simulate this attack, in order to test that current redeem implementation is not vulnerable.

### Original Finding Content

## Data Validation

**Target:** LendingPool.sol

**Difficulty:** Low

## Description

An attacker could use the redeem function with a specially crafted AToken contract to steal all the available liquidity.

The redeem function (Figure 8.1) allows users to get back their funds, given the address of an AToken contract and the amount to redeem.

```solidity
function redeem(address _aToken, uint256 _aTokenAmount) external nonReentrant {
    AToken aToken = AToken(_aToken);
    address reserve = aToken.getUnderlyingAssetAddress();
    uint256 underlyingAmountToRedeem = 0;
    uint256 aTokenBalance = aToken.balanceOf(msg.sender);
    require(
        aTokenBalance >= _aTokenAmount && _aTokenAmount > 0,
        "The aToken user balance is not enough to cover the amount to redeem or the amount to redeem is 0"
    );

    // calculate underlying to redeem
    underlyingAmountToRedeem = aToken.aTokenAmountToUnderlyingAmount(_aTokenAmount);
    aToken.burnOnRedeem(msg.sender, _aTokenAmount);
    uint256 currentAvailableLiquidity = core.getReserveAvailableLiquidity(reserve);
    require(currentAvailableLiquidity >= underlyingAmountToRedeem, "There is not enough liquidity available to redeem");

    // compound liquidity and variable borrow interests
    core.updateReserveCumulativeIndexes(reserve);
    (,,,,, uint256 healthFactor) = dataProvider.calculateUserGlobalData(msg.sender);
    
    // at this point, the withdraw should not trigger the liquidation
    require(
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

**Figure 8.1:** redeem function in LendingPool.sol

However, since it does not check the validity of the supplied AToken contract, it allows any user to control the amount of liquidity to redeem in the `underlyingAmountToRedeem` variable.

## Exploit Scenario

An attacker can create a specially crafted AToken contract to redeem any user funds, given there is enough liquidity. Such a contract returns arbitrary amounts when the `balanceOf` and the `aTokenAmountToUnderlyingAmount` functions are called, in order to perform the exploit.

## Recommendation

- **Short term:** Properly validate the provided `_aToken` address using the corresponding reserve.
- **Long term:** Add proper unit tests to simulate this attack, in order to test that the current redeem implementation is not vulnerable.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

