---
# Core Classification
protocol: Kelp
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35994
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/review.pdf
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
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Use of Deprecated Chainlink Function

### Overview

See description below for full details.

### Original Finding Content

## Description
The ChainlinkPriceOracle contract uses the `latestAnswer` function from the Chainlink Aggregator Interface to fetch asset prices. This method is deprecated as per the Chainlink Data Feeds API, and its continued use may lead to compatibility issues or lack of support in the future.

## Recommendations
Consider replacing the deprecated `latestAnswer()` function with `latestRoundData()`.

## Resolution
This issue has been addressed in commit `b8b5bf6`.

## LRT-10 Miscellaneous General Comments
- **Asset:** All contracts
- **Status:** Closed: See Resolution
- **Rating:** Informational

## Description
This section details miscellaneous findings discovered by the testing team that do not have direct security implications:

1. **Strategy Defaults to Address(0)**
   - **Related Asset(s):** LRTConfig.sol
   - Prior to `updateAssetStrategy()` being called, the strategy for a supported asset will be `address(0)`, which will cause a revert when depositing assets.
   - Ensure that strategy is updated through `updateAssetStrategy()` each time a supported asset is added after initialisation or when adding a new supported asset.

2. **Check Return Value of `depositIntoStrategy()`**
   - **Related Asset(s):** NodeDelegator.sol
   - The return value for `depositIntoStrategy()` is not checked.
   - For safety reasons, it is recommended to check that the number of shares returned by the function `depositIntoStrategy()` is greater than 0.

3. **Potential Reversion With Large Approvals of Non-standard ERC20**
   - **Related Asset(s):** NodeDelegator.sol
   - In the NodeDelegator contract, the `maxApproveToEigenStrategyManager` function approves a maximum amount (`type(uint256).max`) of an ERC20 token. While this is a common pattern for convenience, certain ERC20 tokens, like UNI and COMP, might revert when approving values higher than `type(uint96).max`. This behaviour stems from their implementation peculiarities.
   - Ensure that any ERC20 tokens added to the supported list are evaluated for compatibility with large approvals.

4. **Location of `DEFAULT_ADMIN_ROLE` Definition**
   - **Related Asset(s):** LRTConfigRoleChecker.sol
   - In the LRTConfigRoleChecker contract, the `DEFAULT_ADMIN_ROLE` is defined as a constant with the value `0x00`.
   - While this is a functional approach, it might be more maintainable and clearer to define such constants in a centralised location, particularly if they are shared across multiple contracts or are fundamental to the system’s role-based access control.
   - Consider moving the `DEFAULT_ADMIN_ROLE` constant to LRTConstants.sol. This can improve code maintainability and readability, especially for constants that are fundamental to the system’s architecture.

5. **Prefer Use of `safeTransfer()` Over `transfer()`**
   - **Related Asset(s):** LRTDepositPool.sol & NodeDelegator.sol
   - In the LRTDepositPool and NodeDelegator contracts, using the `transfer()` and `transferFrom()` functions for ERC-20 tokens may not be the safest approach. While the `transfer()` function is a part of the ERC-20 standard, it does not always guarantee that the transfer will be successful, especially if the token contract does not follow the ERC-20 standard perfectly. In some cases, the `transfer()` function might not revert on failure, leading to a false assumption of a successful transaction.
   - Consider replacing the `transfer` function with `safeTransfer()` and `safeTransferFrom()` from OpenZeppelin’s SafeERC20 library. This provides additional checks that ensure the transfer was successful.

6. **High Centralisation Risk**
   - **Related Asset(s):** LRTConfig.sol
   - The LRTConfig contract allows changing the `rsETH` address through its setter function. This capability presents a high centralisation risk, as it gives significant power to the admin.
   - Thoroughly review the necessity of allowing the `rsETH` address to be updated after initialisation. If it’s crucial for upgradeability or administrative purposes, clearly document the rationale and ensure robust security measures.

7. **Lack of Synchrony when Adding a New Token**
   - **Related Asset(s):** LRTConfig.sol
   - Functions `getLSTToken()` and `setToken()` appear to pose as helper functions for external applications or end users to get the address of supported tokens based on bytes32 identifier on LRTConstants (i.e., R_ETH_TOKEN, ST_ETH_TOKEN, and CB_ETH_TOKEN).
   - However, there is a disconnect with the function `addNewSupportedAsset()`. In the function `initialize()`, `_setToken()` and `_addNewSupportedAsset()` are called subsequently with preset values, so the resulting values are synchronous. If a new token is added, the functions `addNewSupportedAsset()` and `setToken()` need to be called separately by different roles, allowing conflicting updates.
   - Furthermore, new tokens other than the preset tokens will have no values in LRTConstants. This can be a consideration whether the bytes32 identifier should be taken off LRTConstants so it can be flexibly added or removed.
   - Consider bundling all necessary actions in one call when adding a new token to minimise potential mistakes.

8. **Zero Key Provides Default Value**
   - **Related Asset(s):** LRTConfig.sol
   - Functions `_setToken()` and `_setContract()` allow the input key to be zero. If a value is set with a zero key, then according to the current behaviour of function calling in Solidity, the getter will return the corresponding value when the user does not set any input on it (i.e., an empty byte as input).
   - Make sure this behaviour is understood. Consider preventing zero key on `_setToken()` and `_setContract()` if return values with zero or empty byte input of `getLSTToken()` and `getContract()` are undesirable.

9. **Initial Value of `rsETHPrice`**
   - **Related Asset(s):** LRTOracle.sol
   - Function `updatePriceOracleFor()` must be called at least once to initialise `rsETHPrice` to a non-zero value. If the value of `rsETHPrice` is zero, then function `LRTDepositPool.depositAsset()` will revert with division or modulo by 0.
   - Consider setting `rsETHPrice` to an initial value during initialisation or in the variable definition.

10. **Check for Nonzero Balance**
    - **Related Asset(s):** NodeDelegator.sol
    - Function `depositAssetIntoStrategy()` deposits the contract’s token balance into EigenLayer’s StrategyManager contract. This function is callable even if the balance is zero. If this occurs, the gas would be wasted.
    - Consider checking that the balance is more than zero before proceeding.

11. **Lack of Event Emission**
    (a) **Related Asset(s):** NodeDelegator.sol
    - In the NodeDelegator contract, the `transferBackToLRTDepositPool()` function, being state-changing, should ideally emit an event to ensure transparency and traceability of its actions on the blockchain.
    - Consider modifying the `transferBackToLRTDepositPool()` function to emit an event whenever it successfully changes the state.

    (b) **Related Asset(s):** LRTConfig.sol
    - Function `updateAssetStrategy()` is a state-changing function. The current implementation does not emit any event.
    - Consider emitting an event for better traceability and visibility.

12. **Redundant Function Override**
    - **Related Asset(s):** RSETH.sol
    - In the RSETH contract, the function `updateLRTConfig()` is overridden, but it appears to have the same functionality as `updateLRTConfig()` in the LRTConfigRoleChecker contract, which RSETH inherits from.
    - This redundancy might be unnecessary unless there is a specific requirement for different access controls or additional functionality in RSETH.
    - If the `updateLRTConfig()` function in RSETH does not add any new functionality or change the access control mechanism, consider removing this override to reduce redundancy. The inherited function from LRTConfigRoleChecker should suffice.

13. **Gas Efficiency in Zero Address Check**
    - **Related Asset(s):** UtilLib.sol
    - The UtilLib library contains a function `checkNonZeroAddress`, used to validate that an address is not the zero address. While this is a common and necessary check in smart contracts, the current implementation using high-level Solidity may not be the most gas-efficient approach. There’s an opportunity to optimise this check by using inline assembly.
    - Consider implementing the zero address check using Solidity inline assembly. Assembly can be more gas-efficient as it allows for lower-level manipulation of the EVM.

14. **Incorrect Parameter Description in the `initialize()` Function**
    - **Related Asset(s):** LRTConfig.sol
    - In the `initialize()` function of the LRTConfig contract, the parameter for `rsETH` is mistakenly described as `cbETH` address in the comment on line [40].
      ```solidity
      /// @param rsETH_ cbETH address
      ```
    - Correct the parameter description to accurately reflect that `rsETH_` is the `rsETH` address, not `cbETH` address. This change will improve the clarity and accuracy of the code documentation.

15. **Overlapping Getter Functions**
    - **Related Asset(s):** LRTConfig.sol
    - The contract LRTConfig has public state variables `tokenMap` and `contractMap` that automatically generate getter functions due to their public visibility. However, the contract also explicitly defines getter functions `getLSTToken(bytes32 tokenKey)` and `getContract(bytes32 contractKey)` which essentially serve the same purpose. This redundancy can lead to confusion and is not efficient in terms of contract design.
    - Consider removing the explicit getter functions `getLSTToken()` and `getContract()` to rely on the automatically generated getters for the public variables `tokenMap` and `contractMap`. This will streamline the contract, reducing redundancy and potential confusion.

## Recommendations
Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

## Resolution
The development team’s responses to the raised issues above are as follows:
1. **Strategy Defaults to Address(0):** `depositAssetIntoStrategy()` will revert with an appropriate revert message when the strategy is `address(0)`. This issue has been addressed in commit `2af8a04`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Kelp |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/kelp/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/kelp/review.pdf

### Keywords for Search

`vulnerability`

