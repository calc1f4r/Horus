---
# Core Classification
protocol: Tempus Raft
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17572
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-04-tempus-raft-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-04-tempus-raft-securityreview.pdf
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
finders_count: 2
finders:
  - Justin Jacob
  - Michael Colburn
---

## Vulnerability Title

Inconsistent use of safeTransfer for collateralToken

### Overview


This bug report details a Denial of Service vulnerability in the PositionManager and PositionManagerStETH contracts. These contracts rely on ERC-20 tokens as collateral that must be deposited in order to mint R tokens. However, there are a few places in the code where the safeTransfer function is missing. This means that if an ERC-20 token is approved that returns a Boolean on failure, a liquidator would not receive any collateral for performing a liquidation. 

To fix this issue, the SafeERC20 library's safeTransfer function should be used for the collateralToken. In addition, unit test coverage should be improved to uncover edge cases and ensure intended behavior throughout the protocol.

### Original Finding Content

## Security Assessment Report

## Difficulty: High

## Type: Denial of Service

## Target: 
- PositionManager.sol
- PositionManagerStETH.sol

## Description
The Raft contracts rely on ERC-20 tokens as collateral that must be deposited in order to mint R tokens. However, although the SafeERC20 library is used for collateral token transfers, there are a few places where the `safeTransfer` function is missing:

- The transfer of `collateralToken` in the `liquidate` function in the PositionManager contract:
  
  ```solidity
  if (!isRedistribution) {
      rToken.burn(msg.sender, entirePositionDebt);
      _totalDebt -= entirePositionDebt;
      emit TotalDebtChanged(_totalDebt);
      // Collateral is sent to protocol as a fee only in case of liquidation
      collateralToken.transfer(feeRecipient, collateralLiquidationFee);
  }
  collateralToken.transfer(msg.sender, collateralToSendToLiquidator);
  ```

  **Figure 4.1: Unchecked transfers in PositionManager.liquidate**

- The transfer of stETH in the `managePositionStETH` function in the PositionManagerStETH contract:
  
  ```solidity
  if (isCollateralIncrease) {
      stETH.transferFrom(msg.sender, address(this), collateralChange);
      stETH.approve(address(wstETH), collateralChange);
      uint256 wstETHAmount = wstETH.wrap(collateralChange);
      _managePosition(...);
  } else {
      _managePosition(...);
      uint256 stETHAmount = wstETH.unwrap(collateralChange);
      stETH.transfer(msg.sender, stETHAmount);
  }
  ```

  **Figure 4.2: Unchecked transfers in PositionManagerStETH.managePositionStETH**

## Exploit Scenario
Governance approves an ERC-20 token that returns a Boolean on failure to be used as collateral. However, since the return values of this ERC-20 token are not checked, Alice, a liquidator, does not receive any collateral for performing a liquidation.

## Recommendations
- **Short term**: Use the SafeERC20 library’s `safeTransfer` function for the `collateralToken`.
- **Long term**: Improve unit test coverage to uncover edge cases and ensure intended behavior throughout the protocol.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Tempus Raft |
| Report Date | N/A |
| Finders | Justin Jacob, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-04-tempus-raft-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-04-tempus-raft-securityreview.pdf

### Keywords for Search

`vulnerability`

