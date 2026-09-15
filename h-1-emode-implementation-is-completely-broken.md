---
# Core Classification
protocol: Index
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20213
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/81
source_link: none
github_link: https://github.com/sherlock-audit/2023-05-Index-judging/issues/251

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
finders_count: 6
finders:
  - 0xStalin
  - Cryptor
  - volodya
  - 0x52
  - 0xGoodess
---

## Vulnerability Title

H-1: eMode implementation is completely broken

### Overview


This bug report is about the issue H-1, which is about the implementation of eMode being completely broken. eMode allows assets of the same class to be borrowed at a much higher loan-to-value (LTV) ratio. However, the current implementation makes the incorrect calls to the Aave V3 pool, which makes it impossible to take advantage of the higher LTV. The code snippet provided is from the file AaveLeverageStrategyExtension.sol, lines 1095-1109. 

The vulnerability was found by 0x52, 0xGoodess, 0xStalin, Cryptor, hildingr, and volodya. The impact of this bug is that usage of eMode, a core function of the contracts, is unusable, which causes erratic and dangerous behavior. The bug was found through manual review, and the recommendation is to pull the adjusted eMode settings rather than the base pool settings. 

The bug was fixed by ckoopmann in the pull request 142, which keeps track of the current eMode category id and then gets the data for that specific eMode (if eMode category is not 0).

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-05-Index-judging/issues/251 

## Found by 
0x52, 0xGoodess, 0xStalin, Cryptor, hildingr, volodya
## Summary

Enabling eMode allows assets of the same class to be borrowed at much higher a much higher LTV. The issue is that the current implementation makes the incorrect calls to the Aave V3 pool making so that the pool can never take advantage of this higher LTV.

## Vulnerability Detail

[AaveLeverageStrategyExtension.sol#L1095-L1109](https://github.com/sherlock-audit/2023-05-Index/blob/main/index-coop-smart-contracts/contracts/adapters/AaveLeverageStrategyExtension.sol#L1095-L1109)

    function _calculateMaxBorrowCollateral(ActionInfo memory _actionInfo, bool _isLever) internal view returns(uint256) {
        
        // Retrieve collateral factor and liquidation threshold for the collateral asset in precise units (1e16 = 1%)
        ( , uint256 maxLtvRaw, uint256 liquidationThresholdRaw, , , , , , ,) = strategy.aaveProtocolDataProvider.getReserveConfigurationData(address(strategy.collateralAsset));

        // Normalize LTV and liquidation threshold to precise units. LTV is measured in 4 decimals in Aave which is why we must multiply by 1e14
        // for example ETH has an LTV value of 8000 which represents 80%
        if (_isLever) {
            uint256 netBorrowLimit = _actionInfo.collateralValue
                .preciseMul(maxLtvRaw.mul(10 ** 14))
                .preciseMul(PreciseUnitMath.preciseUnit().sub(execution.unutilizedLeveragePercentage));

            return netBorrowLimit
                .sub(_actionInfo.borrowValue)
                .preciseDiv(_actionInfo.collateralPrice);

When calculating the max borrow/repay allowed, the contract uses the getReserveConfigurationData subcall to the pool. 

[AaveProtocolDataProvider.sol#L77-L100](https://github.com/aave/aave-v3-core/blob/29ff9b9f89af7cd8255231bc5faf26c3ce0fb7ce/contracts/misc/AaveProtocolDataProvider.sol#L77-L100)

    function getReserveConfigurationData(
      address asset
    )
      external
      view
      override
      returns (
          ...
      )
    {
      DataTypes.ReserveConfigurationMap memory configuration = IPool(ADDRESSES_PROVIDER.getPool())
        .getConfiguration(asset);
  
      (ltv, liquidationThreshold, liquidationBonus, decimals, reserveFactor, ) = configuration
        .getParams();

The issue with using getReserveConfigurationData is that it always returns the default settings of the pool. It never returns the adjusted eMode settings. This means that no matter the eMode status of the set token, it will never be able to borrow to that limit due to calling the incorrect function.

It is also worth considering that the set token as well as other integrated modules configurations/settings would assume this higher LTV. Due to this mismatch, the set token would almost guaranteed be misconfigured which would lead to highly dangerous/erratic behavior from both the set and it's integrated modules. Due to this I believe that a high severity is appropriate.

## Impact

Usage of eMode, a core function of the contracts, is completely unusable causing erratic/dangerous behavior 

## Code Snippet

[AaveLeverageStrategyExtension.sol#L1095-L1109](https://github.com/sherlock-audit/2023-05-Index/blob/main/index-coop-smart-contracts/contracts/adapters/AaveLeverageStrategyExtension.sol#L1095-L1109)

## Tool used

Manual Review

## Recommendation

Pull the adjusted eMode settings rather than the base pool settings



## Discussion

**ckoopmann**

Yep, this is correct, and will be addressed. 

Btw: I think I saw a bunch of duplicates of this issue when looking through the unfiltered list.

**0xffff11**

Agree with sponsor, valid high. Added missing duplicates

**ckoopmann**

Fixed in below pr by keeping track of the current eMode category id and then getting the data for that specific eMode (if eMode category is not 0):
https://github.com/IndexCoop/index-coop-smart-contracts/pull/142

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Index |
| Report Date | N/A |
| Finders | 0xStalin, Cryptor, volodya, 0x52, 0xGoodess, hildingr |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-05-Index-judging/issues/251
- **Contest**: https://app.sherlock.xyz/audits/contests/81

### Keywords for Search

`vulnerability`

