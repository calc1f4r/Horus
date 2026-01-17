---
# Core Classification
protocol: Geode Wm
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44069
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Geode-WM-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[L-02] Withdrawal Request Could be Assigned a Wrong New Owner

### Overview

See description below for full details.

### Original Finding Content

## Severity

Low Risk

## Description

The `transferRequest()` function is used to assign a new owner to a request who can later dequeue it. However, since dequeuing ultimately facilitates the claim of ETH, setting a wrong new request owner by mistake can result in a loss of funds.

## Location of Affected Code

File: [contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol#L424](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol#L424)

```solidity
function transferRequest(
  PooledWithdrawal storage self,
  uint256 index,
  address newOwner
) external {
  address oldOwner = self.requests[index].owner;
  require(msg.sender == oldOwner, "WML:not owner");
  require(newOwner != address(0), "WML:cannot transfer to zero address");

  self.requests[index].owner = newOwner;

  emit RequestTransfer(index, oldOwner, newOwner);
}
```

## Recommendation

Implement a two-step transfer of the request's ownership. This would include adding a new `address proposedOwner` variable and `proposeNewOwner()` function. The implementation would also require a change in the functionality of the `transferRequest()`.

```diff
struct Request {
  address owner;
  uint256 trigger;
  uint256 size;
  uint256 fulfilled;
  uint256 claimableETH;
+ address proposedNewOwner;
}

+ function proposeNewOwner(PoolWithdrawal storage self, uint256 index, address proposedNewOwner) external {
+   require(msg.sender == self.requests[index].owner, "WML:not owner");
+   require(proposedNewOwner != address(0), "WML:zero address");

+   self.requests[index].proposedNewOwner = proposedNewOwner;
+ }

+ function transferRequest(PoolWithdrawal storage self, uint256 index) external {
+   require (msg.sender == self.requests[index].proposedNewOwner, "WML:only proposed owner");

+   address oldOwner = self.requests[index].owner;

+   self.requests[index].owner = msg.sender;
+   self.requests[index].proposedNewOwner = address(0);

+   emit RequestTransfer(index, oldOwner, msg.sender);
+ }
```

## Team Response

Acknowledged, will not be mitigated.

## [I-01] Misleading `require` Message

## Severity

Informational

## Description

The validation check ensures that `size` is greater or equal to `MIN_REQUEST_SIZE`, and reverts with an incorrect message.

## Location of Affected Code

File: [contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol#L339](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol#L339)

```solidity
require(size >= MIN_REQUEST_SIZE, "WML:min 0.01 gETH");
```

## Recommendation

The message should be `WML:min 0.05 gETH`.

## Team Response

Mitigated.

## [I-02] Missing Event Emission in `processValidators()`

## Severity

Informational

## Description

Emitting events upon the execution of the core contract is a good practice and can aid the debugging process if the function is used in a multi-call further into the project's development.

## Location of Affected Code

File: [contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol#L688](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol#L688)

```solidity
function processValidators(
  PooledWithdrawal storage self,
  bytes[] calldata pubkeys,
  uint256[] calldata beaconBalances,
  uint256[] calldata withdrawnBalances,
  bytes32[][] calldata balanceProofs
) external {
```

## Recommendation

Consider implementing an event, corresponding to the `processValidators` function.

## Team Response

Acknowledged, will be implemented.

## [I-03] Missing Check for the New Variable in `setExitThreshold`

## Severity

Informational

## Description

The `setExitThreshold` function lacks a check if the new threshold is the same as the current one. Although this is not harmful, it can lead to unnecessary transactions and gas costs, impacting the user experience.

## Location of Affected Code

File: [contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol#L271](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol#L271)

```solidity
function setExitThreshold(PooledWithdrawal storage self, uint256 newThreshold) external {
```

## Recommendation

Consider adding a check if `self.EXIT_THRESHOLD != newThreshold`;

```diff
function setExitThreshold(PooledWithdrawal storage self, uint256 newThreshold) external {
  require(newThreshold >= MIN_EXIT_THRESHOLD, "WML:min threshold is 60%");
  require(newThreshold <= PERCENTAGE_DENOMINATOR, "WML:max threshold is 100%");
+ require(self.EXIT_THRESHOLD != newThreshold), "New threshold is the same as the current one."

  self.EXIT_THRESHOLD = newThreshold;
  emit NewExitThreshold(newThreshold);
}
```

## Team Response

Acknowledged, will not be mitigated.

## [I-04] Remove Unused Variables

## Severity

Informational

## Description

In `WithdrawalModule.sol` variable `size` in `enqueueBatch()` function is unused.
In `WithdrawalContract.sol` variable `data` in `initialize()` function is unused.

## Location of Affected Code

File: [contracts/Portal/modules/WithdrawalModule/WithdrawalModule.sol#L203](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/modules/WithdrawalModule/WithdrawalModule.sol#L203)

File: [contracts/Portal/packages/WithdrawalContract.sol#L64](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/packages/WithdrawalContract.sol#L64)

## Recommendation

Consider removing them

## Team Response

Mitigated.

## [I-05] Use Scientific Notation Rather Than Exponentiation

## Severity

Informational

## Description

- `1e10` Instead of `10 ** 10`
- `1e6` Instead of `10 ** 6`
- `0.05 ether` Instead of `10 ** 16`

## Location of Affected Code

File: [contracts/Portal/globals/macros.sol#L5](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/globals/macros.sol#L5)

```solidity
uint256 constant PERCENTAGE_DENOMINATOR = 10 ** 10;
```

File: [contracts/Portal/modules/StakeModule/libs/StakeModuleLib.sol#L195](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/modules/StakeModule/libs/StakeModuleLib.sol#L195)

```solidity
uint256 internal constant MAX_ALLOWANCE = 10 ** 6 + 1;
```

File: [contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol#L177](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol#L177)

```solidity
uint256 constant MIN_REQUEST_SIZE = 5 * 10 ** 16;
```

## Recommendation

Consider using scientific notation.

## Team Response

Mitigated appropriately.

## [I-06] Variables Naming does not Follow the Solidity Style Guide

## Severity

Informational

## Description

One of the guidelines mentioned in the Style Guide is to name functions and variables in a specific way to improve readability and avoid confusion. By following this, you can achieve consistency in your contract code.

## Location of Affected Code

File: [contracts/Portal/modules/WithdrawalModule/WithdrawalModule.sol](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/modules/WithdrawalModule/WithdrawalModule.sol)

File: [contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol)

## Recommendation

Consider using mixedCase for the following variables:

- `Qrealized, Qfulfilled` in the `fulfillable()` function in `WithdrawalModule.sol`.
- `Qrealized`, `Qfulfilled`, `Qprice` in the `_fulfillBatch()` function in `WithdrawalModuleLib.sol`
- `Qrealized`, `Qfulfilled`, `Rtrigger`, `Rsize`, `Rfulfilled`, `Rfloor`, `Rceil` in the `fulfillable()` function in `WithdrawalModuleLib.sol`

## Team Response

Mitigated

## [I-07] Open TODOs

## Severity

Informational

## Description

Open TO-DOs can point to architecture or programming issues that still need to be resolved. Often these kinds of comments indicate areas of complexity or confusion for developers. This provides value and insight to an attacker who aims to cause damage to the protocol.

## Location of Affected Code

File: [contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol#L384](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol#L384)

```solidity
* @dev TODO:  create and use _requestExitBatch to save gas
```

File: [contracts/Portal/packages/WithdrawalContract.sol#L20](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/packages/WithdrawalContract.sol#L20)

```solidity
* TODO: this can be renamed to withdrawalQueue or ValidatorCustodian
```

## Recommendation

Consider resolving the TO-DOs before deploying code to a production context. Use an independent issue tracker or other project management software to track development tasks.

## Team Response

Acknowledged, will be mitigated before the mainnet.

## [I-08] Typos

## Severity

Informational

## Recommendation

`WithdawalModuleLibMock` -> `WithdrawalModuleLibMock`

`lenghts` -> `lengths`

`well maintained` -> `well-maintained`

`preventa` -> `prevent a`

`there is remaining votes` -> `there are remaining votes`

`preferance` -> `preference`

`upto` -> `up to`

`Derisked Requests that is` -> `Derisked Requests that are`

`we have came up` -> `we have come up`

`profitablity` -> `profitability`

`distrupting` -> `disrupting`

`became is processed in relative to` -> `became processed in relation to`

## Team Response

Acknowledged, will be mitigated before the mainnet.

## [G-01] No Need to Initialize Variables with Default Values

## Severity

Gas Optimization

## Description

If a variable is not set/initialized, the default value is assumed (0, false, 0x0 … depending on the data type). Saves 8 gas per instance.

## Location of Affected Code

File: [contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol)

```solidity
399: for (uint256 i = 0; i < len; i++) {
507: for (uint256 i = 0; i < indexes.length; i++) {
603: for (uint256 i = 0; i < indexes.length; i++) {
704: for (uint256 i = 0; i < pubkeys.length; i++) {
```

## Recommendation

Do not initialize variables with their default values.

```diff
- for (uint256 i = 0; ...
+ for (uint256 i; ...
```

## Team Response

Mitigated.

## [G-02] Use `calldata` Instead of `memory` for Function Arguments that do not get Mutated

## Severity

Gas Optimization

## Description

When a function parameter of a reference type is marked as read-only, utilizing calldata instead of memory incurs lower gas costs. Calldata serves as an immutable and temporary storage location for function arguments, functioning in a manner largely similar to memory.

## Location of Affected Code

File: [contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol#L222](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol#L222)

```solidity
function _requestExit(PooledWithdrawal storage self, bytes memory pubkey) internal {
```

File: [contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol#L231](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol#L231)

```solidity
function _finalizeExit(PooledWithdrawal storage self, bytes memory pubkey) internal {
```

## Recommendation

To optimize gas costs, it is recommended to mark the data type as calldata instead of memory.

## Team Response

Acknowledged, will be implemented.

## [G-03] Cache Array Length Outside of Loops

## Severity

Gas Optimization

## Description

In the absence of caching, the Solidity compiler will consistently retrieve the array's length in every iteration. Specifically, for storage arrays, this entails an additional "sload" operation (resulting in 100 extra gas for each iteration, excluding the first one), while for memory arrays, it leads to an additional "mload" operation (resulting in 3 extra gas for each iteration, excluding the first one).

## Location of Affected Code

File: [contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol)

```solidity
507: for (uint256 i = 0; i < indexes.length; i++) {
603: for (uint256 i = 0; i < indexes.length; i++) {
704: for (uint256 i = 0; i < pubkeys.length; i++) {
717: for (uint256 j = 0; j < pubkeys.length; j++) {
```

## Recommendation

To optimize gas costs, it is recommended to instantiate a variable in every function that has a for loop, before the loop itself.

## Team Response

Mitigated.

## [G-04] Revert Strings Can be Shortened

## Severity

Gas Optimization

## Description

Since the initial proposal from the first audit to use custom errors instead of `require` statements is rather cumbersome for implementation, the current revert strings could be shortened. Keeping them `<= 32 bytes` in length will save gas.

## Location of Affected Code

File: [contracts/Portal/middlewares/ERC20RebaseMiddleware.sol](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/middlewares/ERC20RebaseMiddleware.sol)

```solidity
306: require(currentAllowance >= subtractedValue, "ERC20R: decreased allowance below zero");
331: require(from != address(0), "ERC20R: transfer from the zero address");
332: require(to != address(0), "ERC20R: transfer to the zero address");
337: require(fromBalance >= amount, "ERC20R: transfer amount exceeds balance");
360: require(owner != address(0), "ERC20R: approve from the zero address");
361: require(spender != address(0), "ERC20R: approve to the zero address");
```

File: [contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol)

```solidity
340: require(owner != address(0), "WML:owner can not be zero address");
431: require(newOwner != address(0), "WML:cannot transfer to zero address");
572: require(receiver != address(0), "WML:receiver can not be zero address");
592: require(receiver != address(0), "WML:receiver can not be zero address");
```

## Recommendation

Keep revert strings as short as possible. Alternatively, to unify all of them at a certain length, you can represent the revert string as Error codes, for which you can create a dedicate `Error codes` section in the documentation, which would include a table with the meaning of all error codes. Inspiration can be taken from [here:] (https://docs.stackup.sh/docs/erc-4337-bundler-rpc-methods#json-rpc-errors).

## Team Response

Acknowledged, will be implemented.

## [G-05] `++i` Costs Less Gas Than `i++`

## Severity

Gas Optimization

## Description

The pre-increment operator `++i` is a more gas-efficient choice compared to post-increment `i++` when employed within for-loops. Utilizing `++i` in loops results in a gas savings of 5 units per iteration.

## Location of Affected Code

File: [contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol)

```solidity
399: for (uint256 i = 0; i < len; i++) {
507: for (uint256 i = 0; i < indexes.length; i++) {
603: for (uint256 i = 0; i < indexes.length; i++) {
704: for (uint256 i = 0; i < pubkeys.length; i++) {
717: for (uint256 j = 0; j < pubkeys.length; j++) {
```

## Recommendation

Change the post-increment operators in the for-loops to pre-increment ones.

## Team Response

We decided to use `unchecked` at the end of the day.

## [G-06] Use `!= 0` Instead of `> 0` for Unsigned Integer Comparison

## Severity

Gas Optimization

## Description

In the context of unsigned integer types, opting for the `!= 0` comparison over `> 0` is typically more gas-efficient. This preference arises from the compiler's capacity to optimize the `!= 0` comparison into a straightforward bitwise operation. In contrast, the `> 0` comparison necessitates an extra subtraction operation. Consequently, choosing `!= 0` can enhance gas efficiency and contribute to lowering the overall contract expenditure.

## Location of Affected Code

File: [contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol)

```solidity
485: if (toFulfill > 0) {
509: if (toFulfill > 0) {
555: require(claimableETH > 0, "WML:not claimable");
661: if (internalPrice > 0) {
663: if (claimable > 0) {
740: if (processed > 0) {
```

## Recommendation

Consider changing the `>` to `!=` in the places, outlined above.

## Team Response

Acknowledged, will be reconsidered. However, we are planning to bump solidity above `0.8.13`, which mitigates the issue.

## [G-07] Do not Calculate Constants

## Severity

Gas Optimization

## Description

Due to how constant variables are implemented (replacements at compile-time), an expression assigned to a constant variable is recomputed each time the variable is used, which wastes some gas.

## Location of Affected Code

File: [contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol#L175](https://github.com/Geodefi/Portal-Eth/blob/8b5c94317bd2b09567cb6ed00d50305b9d923bd0/contracts/Portal/modules/WithdrawalModule/libs/WithdrawalModuleLib.sol#L175)

```solidity
uint256 constant MIN_EXIT_THRESHOLD = (6 * PERCENTAGE_DENOMINATOR) / 10;
```

## Team Response

Acknowledged, will be reconsidered.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Geode Wm |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Geode-WM-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

