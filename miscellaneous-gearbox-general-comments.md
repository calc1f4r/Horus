---
# Core Classification
protocol: Gearbox
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19400
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf
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

Miscellaneous Gearbox General Comments

### Overview

See description below for full details.

### Original Finding Content

## Description

This section details miscellaneous findings in the `contracts` repository discovered by the testing team that do not have direct security implications:

## 1. core/DataCompressor.sol

### 1a) Loop Limit Called Each Cycle
To save gas, these loop limits on line [79] and line [94] should be stored in a local variable rather than queried each cycle.

### 1b) Loop Increment Called in Checked Maths
To save gas, this loop incrementing on line [80] and line [95] can be placed in an unchecked block at the end of the loop as it is already restricted by the loop termination condition so will not overflow.

### 1c) Stale Code
There is stale code in the following lines; this should be removed to avoid confusion: line [139], line [153], and line [172].

### 1d) Typos
- line [68]: `particluar`, should be `particular`.
- line [68]: `account`, should be `accounts`.
- line [188]: `bborrower`, should be `borrower`.
- line [217]: `flg`, should be `flag`.
- line [270]: `particulr`, should be `particular`.
- line [325]: `non-standart`, should be `non-standard`.

### 1e) Missing Inheritance
Consider having `DataCompressor.sol` inherit from its interface `IDataCompressor.sol` to ensure that it is implemented correctly.

### 1f) Misleading Modifier Naming
Modifiers `registeredCreditManagerOnly(address creditManager)` and `registeredPoolOnly(address pool)` are intended to check that the target of the call is a credit manager or a pool. They do not check the caller of the function. Consider renaming to `targetIsCreditManager(address target)` to clarify intent.

### 1g) Unused Local Variables
The return value `ICreditFacade creditFacade` assigned to a local variable on line [125], line [227], line [360], and line [404] is not used and can be removed. The call assigning `uint256 allowedTokenCount` on line [151] can be removed.

## 2. core/ACL.sol

### 2a) Missing Inheritance
Consider having `ACL.sol` inherit from its interface `IACL.sol` to ensure that it is implemented correctly.

## 3. credit/CreditManager.sol

### 3a) Imports Hardhat Console
On line [25], there is an import that only functions when not on the mainnet and so should be removed.

### 3b) Confusing Comment
On line [38], the Account Factory is referred to as the account manager, which may get confusing as the Credit Manager is the manager for credit accounts. The comment should be edited to make the differing roles clearer.

### 3c) Typo in Variable Name
On line [84], the variable `forbidenTokenMask` is introduced; it should be named `forbiddenTokenMask` here and at other places of use.

### 3d) Confusing Comment
On line [89], the comment suggests we record which block we last used the fast check mechanism when, in fact, the mapping records how often we have used the fast check mechanism in the same block.

### 3e) Inconsistent Naming Scheme
On line [617], it refers to a variable `total`, whereas in other contracts this calculation is referred to as `twv`, short for Threshold Weighted Value, while `total` is reserved for calculations of total value as described in the whitepaper.

### 3f) Gas Optimization
On line [727] and line [783], `tokenMask > 0` can be replaced with `tokenMask != 0`, which is 3 gas cheaper and acts the same when acting on unsigned integers. The function `upgradeContracts` can be separated to upgrade `creditFacade` or `priceOracle` individually.

### 3g) Operation Order Unclear
On line [727] and line [783], multiple operations are carried out on the same line; use brackets to indicate the intended order of actions to improve readability.

### 3h) Missing Zero Address Checks
The function `upgradeContracts` prevents `creditFacade` or `priceOracle` from being set to the zero address. If this happens, important Gearbox functions will break. The mistake can be recovered by calling `upgradeContracts` again (wasting gas), but implementing zero address checks would be appropriate.

### 3i) Typos
- line [65]: `Miltiplier`, should be `Multiplier`.
- line [71]: `Adress`, should be `Address`.
- line [167]: `transffered`, should be `transferred`.
- line [227]: `liqution`, should be `liquidation`.
- line [279]: `addrss`, should be `address`.
- line [280]: `it it`, should be `if it`.
- line [345]: `cunulativeIndex`, should be `cumulativeIndex`.
- line [347]: `decresase`, should be `decrease`.
- line [348]: `particall`, should be `partial`.
- line [349]: `cumulativeIndex now`, should be `cumulativeIndexNow`.
- line [353]: `fto`, should be `to`.
- line [805]: `reverts of borrower has no one`, should be `reverts if borrower does not have one`.
- line [823]: `Foloowing`, should be `Following`.

### 3j) Public Function Could Be External
The public function `fullCollateralCheck()` can be declared as external.

## 4. core/WETHGateway.sol

### 4a) Typos
- line [117]: `has`, should be `have`.

### 4b) Misleading Function Name
The function `_checkAllowance()` has side effects. It both checks the allowance and approves the maximum amount. Consider renaming the function to `_checkAndApproveAllowance()` to clarify the intent of the function.

### 4c) Misleading Modifier Name
The modifier `creditManagerOnly(address creditManager)` is intended to check that the caller is a creditManager. However, it expects that `msg.sender` be passed in as a parameter. Consider removing the parameter and instead check the caller directly to clarify usage.

### 4d) Unused Modifier
The modifier `wethCreditManagerOnly(address creditManager)` is not used and can be removed.

## 5. credit/CreditAccount.sol

### 5a) Inconsistent Use of approve() and safeApprove()
On line [95] and line [109], we have an inconsistent use of ERC20’s function `approve()` and the Open Zeppelin wrapper `safeApprove()`.

### 5b) Typos
- line [54]: `cause`, should be `because`.
- line [59]: `Connects credit account to credit account address.`, should be `Connects credit account to credit manager address.`.

### 5c) Misleading Access Control
The functions `connectTo()` and `cancelAllowance()` do not have any modifiers and may be assumed to be callable by anyone. However, a `require` statement in the function restricts access to calls from factory. Consider implementing a `factoryOnly` modifier to clarify the access control.

## 6. credit/CreditConfigurator.sol

### 6a) Typo in Variable Name
On line [216], the variable `forbidenTokenMask` is introduced; it should be named `forbiddenTokenMask` here and at other places of use.

### 6b) Typos
- line [70]: `condigures`, should be `configures`.
- line [134]: `revers`, should be `reverts`.
- line [159], line [219], line [246]: `cause`, should be `because`.
- line [244]: `undelrying`, should be `underlying`.
- line [445]: `undelrying`, should be `underlying`.
- line [491]: `This internal function is check the need of additional sanity checks`, should be `This internal function conducts additional sanity checks`.

### 6c) Conflict Between Documentation and Implementation
Comments on line [63] through line [73] describe the correct deployment flow for `CreditManager`, `CreditFacade`, and `CreditConfigurator` contracts. However, these steps occur out of order in the factory contracts. Step 3 does not occur until Step 6, in the constructor of `CreditConfigurator`.

## 7. pool/LinearInterestRateModel.sol

### 7a) Inconsistent Notation
On line [20], line [36] until line [39], and line [107], a mix of commas and periods are used to denote a thousands separator. Both should be avoided as, depending on which country the reader is from, they can be interpreted as decimal places. If writing clarity is needed, prefer `10_000` or `10 000`.

### 7b) Mismatched Naming Scheme
On line [79], the variable name `U_WAD` naming style may lead readers to assume it is a constant.

### 7c) Constant Interest Model Parameters
It is not possible to update the interest model parameters and so if an asset is being over/underutilized, this cannot be fixed by governance.

### 7d) Suitable Future Interest Models
The current interest model is a piecewise continuous function; it is important that if a different interest model is adopted, it must also be a continuous function. Otherwise, it may be possible to disproportionately affect the paid interest rate by donating a small amount of the underlying token to the pool.

### 7e) Typos
- line [50]: `percetns`, should be `percents`.

## 8. credit/CreditFacade.sol

### 8a) Identical Function Names
Both `CreditFacade.sol` and `CreditManager.sol` contain a function called `transferAccountOwnership()`, one of these should be changed to avoid confusion.

### 8b) Type In Variable Name
The `tvw` return variable assigned on line [283] should be called `twv` to match usage in other places.

### 8c) Typos
- line [403]: `Requires`, should be `Required`.
- line [428]: `cause account trasfership were trasffered here`, should be `because account ownership was transferred here`.
- line [436]: `cause address(this) has no sense`, should be `because address(this) makes no sense`.
- line [477]: `powerfull`, should be `powerful`.
- line [532]: `who unexpect this`, should be `who does not expect this`.
- line [548]: `borbidden`, should be `forbidden`.

### 8d) Public Functions Could Be External
The public functions `calcCreditAccountHealthFactor()` and `hasOpenedCreditAccount()` could be declared external.

### 8e) Unused Local Variables
The call assigning `address creditAccount` on line [522] can be removed.

## 9. core/AccountFactory.sol

### 9a) Typos
- line [157]: `if no one in stock`, should be `if there are none in stock`.
- line [323]: `accoutn`, should be `account`.
- line [345]: `desinged`, should be `designed`.

## 10. oracles/PriceOracle.sol

### 10a) Inaccurate Comment
Line [56] and line [147] suggest that the Chainlink price feed should be a TOKENETH pair, however, discussions with the Gearbox team suggested TOKENUSD price feeds were preferred due to better update characteristics. This is important to document clearly as ETH price feeds use 18 decimal points while USD price feeds use only 8 decimal points.

### 10b) Gas Optimizations
On line [152], we load `priceFeeds[token]` from storage, then again on line [163]. The first instance should be stored in a local variable, then accessed via that on line [163] to save gas. On line [161], we create a local variable `timeStamp`; however, this is never used.

### 10c) Public Function Could Be External
The public function `convert()` could be declared external.

## 11. adapters/yearn/YearnV2.sol

### 11a) Magic Constants
On line [105] and line [187], the function selectors are hardcoded without an explanation of what they are. These should be turned into constant variables with suitable names and explanations of how they are derived.

### 11b) Conflict Between Documentation and Implementation
Comments on line [161] and line [162] suggest that the `uint256 maxLoss` parameter of `withdraw(uint256, address, uint256)` function should specify the maximum acceptable loss that can be sustained on withdrawal. However, the function does not implement such logic.

## 12. pool/PoolService.sol

### 12a) Public Functions Could Be External
The public functions `updateInterestRateModel()` and `setWithdrawFee()` could be declared external.

### 12b) Typos
- line [143]: `amoung`, should be `amount`.
- line [309]: `corretly`, should be `correctly`.
- line [317]: `profitabe`, should be `profitable`.
- line [458]: `undelying`, should be `underlying`.
- line [468]: `Credif`, should be `Credit`.
- line [469], line [490], line [491]: `credif`, should be `credit`.
- line [490]: `particulat`, should be `particular`.

## 13. adapters/convex/ConvexV1_Booster.sol

### 13a) Stale Code
`_amount` input on line [136] is never used.

## 14. adapters/convex/ConvexV1_BaseRewardPool.sol

### 14a) Constant Return Statements
Several functions in this contract return bools; however, they always return true. This affects functions `_stake()` on line [144], `_withdraw()` on line [196], `_withdrawAndUnwrap()` on line [243], `getReward()` on line [282], and `getReward()` on line [302]. The return statements should either be removed or have multiple outcomes.

## 15. adapters/curve/CurveV1_stETH.sol

### 15a) Typo
- line [50]: `Deisgned`, should be `Designed`.

## 16. adapters/curve/CurveV1_stETHGateway.sol

### 16a) Lack of ReentrancyGuard and no nonReentrant modifier
on `exchange()`, `add_liquidity()`, and `remove_liquidity()` functions.

## 17. adapters/lido/LidoV1.sol

### 17a) Incorrect global variable value
line [38]: `_gearboxAdapterType` is incorrectly set to `AdapterType.CONVEX_V1_CLAIM_ZAP`.

### 17b) No nonReentrant modifier onsubmit() function.

## 18. adapters/lido/LidoV1_WETHGateway.sol

### 18a) Lack of ReentrancyGuard and no nonReentrant modifier onsubmit() function.

## 19. oracles/curve/CurveLP2PriceFeed.sol

### 19a) Magic Constant
On line [89], there is a magic constant `10**18`; this should be replaced with a named constant to improve readability.

## 20. oracles/yearn/YearnPriceFeed.sol

### 20a) Gas Optimization
On line [117], replace `_lowerBound > 0` with `_lowerBound != 0` as this is 3 gas cheaper and acts the same when acting on unsigned integers.

## 21. libraries/Errors.sol

### 21a) Typo in Error Message
- line [48]: `CM_CAN_LIQUIDATE`, should be `CM_CANNOT_LIQUIDATE`.

## 22. tokens/GearToken.sol

### 22a) Typo
- line [184]: `to spends`, should be `to spend`.

### 22b) Redundant Check
Line [430] of `_transferTokens()` prevents the zero address from sending tokens. However, it is impossible for the zero address to hold tokens. Therefore, this check can be removed.

## 23. factories/PoolFactory.sol

### 23a) Typo
- line [104]: `destroy`, should be `destroy`.

## Recommendations
Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

## Resolution
The development team has acknowledged the comments detailed above, but is currently prioritizing improvement of contract efficiency and security. The issues will be addressed before production release.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Gearbox |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf

### Keywords for Search

`vulnerability`

