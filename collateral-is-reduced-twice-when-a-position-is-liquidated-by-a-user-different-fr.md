---
# Core Classification
protocol: Filament
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45607
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
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
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Collateral is reduced twice when a position is liquidated by a user different from `protocolLiquidator`.

### Overview


The `liquidatePosition()` function in the `Escrow.sol` smart contract is used to liquidate a position. However, there is a missing `else` statement that leads to a critical impact on the protocol's global reserves. This can cause issues when users are decreasing positions and the reserves are checked. The recommendation is to add an `else` statement to only reduce collateral once.

### Original Finding Content

**Severity**: Critical 	

**Status**: Resolved

**Description**

The function `liquidatePosition()` within the `Escrow.sol` smart contract is used to liquidate a position. This function differentiates if the caller is `protocolLiquidator` or any other user. However, there is an `else` statement missing: 
```solidity
if (msg.sender != protocolLiquidator) {
           require(actualCollateralRequired <= _collateralAmount, "less collateral");
           uint256 positionSize = position.size;
           require(positionSize >= _collateralAmount, "position size should be greater than collateral");
           uint256 userleverage = positionSize / _collateralAmount;
           require(userleverage <= 20, "exceeds 20X leverage");
           position.collateral = positionSize / userleverage;

           IERC20(usdc).transferFrom(msg.sender, address(this), _collateralAmount);  
           IERC20(usdc).approve(diamond, _collateralAmount);

           ITrade(diamond).updateCollateralFromLiquidation(
               _decreasedCollateralValue, _collateralAmount, position, newKey
           );
       } 

       ITrade(diamond).updateCollateralFromLiquidation(_decreasedCollateralValue, 0, position, newKey);
```
 
It can be observed that is caller is not `protocolLiquidator` `updateCollateralFromLiquidation() is executed twice:

1st: ` ITrade(diamond).updateCollateralFromLiquidation(
               _decreasedCollateralValue, _collateralAmount, position, newKey``
2nd: `ITrade(diamond).updateCollateralFromLiquidation(_decreasedCollateralValue, 0, position, newKey);`

This means that `_decreasedCollateralValue` is decreased twice from the global reserves:
```solidity
function updateCollateralFromLiquidation(
       uint256 _decreaseCollateralValue,
       uint256 _collateralAmount,
       Position memory _position,
       bytes32 _key
   ) external onlyEscrow {
       if (_position.isLong) {
           s.longCollateral[_position._indexToken] -= _decreaseCollateralValue;
           s.longCollateral[_position._indexToken] += _collateralAmount;
       } else {
           s.shortCollateral[_position._indexToken] -= _decreaseCollateralValue;
           s.shortCollateral[_position._indexToken] += _collateralAmount;
       }
       s.positions[_key] = _position;
   }
```


Reducing two times the collateral value leads to a wrong accounting of the global reserves for the long and short positions. This has a critical impact on other functions of the protocol when users are decreasing positions and the reserves are checked.

**Recommendation**:

Add an ´else´ statement to only reduce collateral once.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Filament |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

