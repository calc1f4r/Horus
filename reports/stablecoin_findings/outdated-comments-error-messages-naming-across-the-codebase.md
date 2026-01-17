---
# Core Classification
protocol: BadgerDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54639
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/e7dac53a-6098-4aa1-aa0f-ea44ee87050e
source_link: https://cdn.cantina.xyz/reports/cantina_badger_august2023.pdf
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
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - hyh
  - StErMi
---

## Vulnerability Title

Outdated comments, error messages, naming across the codebase 

### Overview

See description below for full details.

### Original Finding Content

## Code Review Summary

## Context

- **CdpManagerStorage.sol**: Lines 160-163, 328-331, 500-502
- **PriceFeed.sol**: Lines 783-789, 789-806
- **LeverageMacroBase.sol**: Line 26
- **BorrowerOperations.sol**: Lines 81-92, 162-165, 176-178, 189-191, 219-223, 439-442, 605-624

## Description

Comments, error messages, and naming can be corrected, as per the list below.

## Recommendations 

### Error Message Corrections

- **_closeCdpWithoutRemovingSortedCdps() error message**:

  **CdpManagerStorage.sol**: Lines 160-163:
  ```solidity
  require(
      closedStatus != Status.nonExistent && closedStatus != Status.active,
      - "CdpManagerStorage: close non-exist or non-active CDP!"
      + "CdpManagerStorage: close non-exist or active CDP!"
  );
  ```

  Check is already done in the only caller above, **_closeCdpWithoutRemovingSortedCdps()**:

  **CdpManagerStorage.sol**: Lines 328-331:
  ```solidity
  - require(
  - cdpStatus != Status.nonExistent && cdpStatus != Status.active,
  - "CdpManagerStorage: remove non-exist or non-active CDP!"
  - );
  ```

### Naming Corrections

- **CdpManagerStorage.sol**: Lines 500-502:
  ```solidity
  - function _requireMoreThanOneCdpInSystem(uint CdpOwnersArrayLength) internal view {
  + function _requireMoreThanOneCdpInSystem(uint CdpIdsArrayLength) internal view {
  require(
  - CdpOwnersArrayLength > 1 && sortedCdps.getSize() > 1,
  + CdpIdsArrayLength > 1 && sortedCdps.getSize() > 1,
  ```

### PriceFeed Function Description

- **_formatClAggregateAnswer()** description can substitute `stETH:BTC` feed that aren't used with `stETH:ETH` one in `_stEthEthAnswer` and `_stEthEthDecimals` params:

  **PriceFeed.sol**: Lines 783-789:
  ```solidity
  // @notice Returns the price of stETH:BTC in 18 decimals denomination
  // @param _ethBtcAnswer CL price retrieve from ETH:BTC feed
  // @param _stEthEthAnswer CL price retrieve from stETH:BTC feed
  // @param _ethBtcDecimals ETH:BTC feed decimals
  // @param _stEthEthDecimals stETH:BTC feed decimals
  // @return The aggregated calculated price for stETH:BTC
  function _formatClAggregateAnswer(
  ```

### LeverageMacroBase Implementation

- **LeverageMacroBase can implement IERC3156FlashBorrower**:

  **LeverageMacroBase.sol**: Line 26
  ```solidity
  contract LeverageMacroBase {
  ```

### Simplification of _formatClAggregateAnswer Logic

- **_formatClAggregateAnswer()** logic can be simplified to:
  ```solidity
  (uint256(_ethBtcAnswer) * uint256(_stEthEthAnswer) * LiquityMath.DECIMAL_PRECISION) /
  10 ** (_stEthEthDecimals + _ethBtcDecimals)
  ```

  Current implementation is a bit more prone to overflows (can break when a bigger decimals number exceeds 30):

  **PriceFeed.sol**: Lines 789-806
  ```solidity
  function _formatClAggregateAnswer(
      int256 _ethBtcAnswer,
      int256 _stEthEthAnswer,
      uint8 _ethBtcDecimals,
      uint8 _stEthEthDecimals
  ) internal view returns (uint256) {
      uint256 _decimalDenominator = _stEthEthDecimals > _ethBtcDecimals
          ? _stEthEthDecimals
          : _ethBtcDecimals;
      uint256 _scaledDecimal = _stEthEthDecimals > _ethBtcDecimals
          ? 10 ** (_stEthEthDecimals - _ethBtcDecimals)
          : 10 ** (_ethBtcDecimals - _stEthEthDecimals);
      return
          (_scaledDecimal *
          uint256(_ethBtcAnswer) *
          uint256(_stEthEthAnswer) *
          LiquityMath.DECIMAL_PRECISION) / 10 ** (_decimalDenominator * 2);
  }
  ```

## Comments to Be Revised or Removed

- **closeCdp() description**:
  
  **BorrowerOperations.sol**: Lines 439-442:
  ```solidity
  /**
  - allows a borrower to repay all debt, withdraw all their collateral, and close their Cdp. Requires the
  borrower have a eBTC balance sufficient to repay their cdp ' s debt, excluding gas compensation - i.e.
  ` (debt - 50) ` eBTC.
  ,→
  ,→
  + allows a borrower to repay all debt, withdraw all their collateral, and close their Cdp.
  */
  function closeCdp(bytes32 _cdpId) external override {
  ```

- **Constructor comments**:

  **BorrowerOperations.sol**: Lines 81-92
  ```solidity
  constructor(
  // ...
  ) LiquityBase(_activePoolAddress, _priceFeedAddress, _collTokenAddress) {
  // This makes impossible to open a cdp with zero withdrawn EBTC
  // TODO: Re-evaluate this
  // ...
  ```

- **Withdraw Collateral description**:

  **BorrowerOperations.sol**: Lines 162-165
  ```solidity
  /**
  Withdraws ` _collWithdrawal ` amount of collateral from the callers Cdp. Executes only if the user has an active
  Cdp, the withdrawal would not pull the users Cdp below the minimum collateralization ratio, and the
  resulting total collateralization ratio of the system is above 150%.
  ,→
  ,→
  */
  function withdrawColl(
  ```

- **Withdraw eBTC description**:

  **BorrowerOperations.sol**: Lines 176-178
  ```solidity
  // ...
  Issues ` _amount ` of eBTC from the callers Cdp to the caller. Executes only if the Cdp ' s collateralization
  ratio would remain above the minimum, and the resulting total collateralization ratio is above 150%.
  ,→
  */
  function withdrawEBTC(
  ```

- **Repay eBTC description**:

  **BorrowerOperations.sol**: Lines 189-191
  ```solidity
  // ...
  repay ` _amount ` of eBTC to the callers Cdp, subject to leaving 50 debt in the Cdp (which corresponds to the 50
  eBTC gas compensation).,→
  */
  function repayEBTC(
  ```

- **Adjust CDP description**:

  **BorrowerOperations.sol**: Lines 219-223
  ```solidity
  /**
  enables a borrower to simultaneously change both their collateral and debt, subject to all the restrictions
  that apply to individual increases/decreases of each quantity with the following particularity: if the
  adjustment reduces the collateralization ratio of the Cdp, the function only executes if the resulting
  total collateralization ratio is above 150%. The borrower has to provide a ` _maxFeePercentage ` that he/she
  is willing to accept in case of a fee slippage, i.e. when a redemption transaction is processed first,
  driving up the issuance fee. The parameter is ignored if the debt is not increased with the transaction.
  ,→
  ,→
  ,→
  ,→
  ,→
  */
  // TODO optimization candidate
  function adjustCdpWithColl(
  ```

- **Adjustment validation function comments**:

  **BorrowerOperations.sol**: Lines 605-624
  ```solidity
  function _requireValidAdjustmentInCurrentMode(
      bool _isRecoveryMode,
      uint _collWithdrawal,
      bool _isDebtIncrease,
      LocalVariables_adjustCdp memory _vars
  ) internal view {
      /*
      *In Recovery Mode, only allow:
      *
      * - Pure collateral top-up
      * - Pure debt repayment
      * - Collateral top-up with debt repayment
      * - A debt increase combined with a collateral top-up which makes the
      * ICR >= 150% and improves the ICR (and by extension improves the TCR).
      *
      * In Normal Mode, ensure:
      *
      * - The new ICR is above MCR
      * - The adjustment won ' t pull the TCR below CCR
      */
  ```

## Acknowledgements 

- **BadgerDao**: Some comments may still be off. Acknowledged.
- **Cantina**: Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | BadgerDAO |
| Report Date | N/A |
| Finders | hyh, StErMi |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_badger_august2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/e7dac53a-6098-4aa1-aa0f-ea44ee87050e

### Keywords for Search

`vulnerability`

