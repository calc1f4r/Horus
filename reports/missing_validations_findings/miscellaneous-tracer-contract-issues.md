---
# Core Classification
protocol: Tracer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19701
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/tracer/tracer-2/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/tracer/tracer-2/review.pdf
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
  - dexes
  - cdp
  - yield
  - services
  - derivatives

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Miscellaneous Tracer Contract Issues

### Overview

See description below for full details.

### Original Finding Content

## Description

This section details miscellaneous findings discovered by the testing team that do not have direct security implications:

1. **Unnecessary Casting:**
   - `lastPriceTimestamp` in `LeveragedPool.sol` is stored as `uint256` and thus does not need to be cast to `uint40` before automatically being cast back to `uint256`. Noting that it is used in the event `IPoolCommitter.Commit` for the field created as `uint40`.
   - The line in `uint256 scaler = uint256(10**(MAX_DECIMALS - _decimals));` of `PoolSwapLibrary.fromWad()` does not need explicit casting to `uint256` as all numbers are already of type `uint256`.
   - `LeveragedPool.payKeeperFromBalances()` performs an unnecessary `uint256` cast of the amount input. Consider removing the `uint256` cast in line [117] of `LeveragedPool.sol`.

2. **Duplicate Modifiers:**
   - Modifiers `onlyKeeper` and `onlyPoolKeeper` perform the same functionality in `LeveragedPool.sol`. Therefore, one of these modifiers can be safely removed, and all instances of its use can be replaced with the other modifier.

3. **Lack of SPDX Licence Identifier:**
   - The `IPoolToken.sol` interface contract is missing an SPDX identifier which correctly licenses the contract for open source development.

4. **List of Typos:**
   - At `PoolCommitter.sol` line [64], line [67], line [70], and line [261], there is a typo in the function comments and the `onlyFactory` revert message. "commiter" should be "committer" in the first three instances. The `onlyFactory` revert message should be updated to "Committer: not factory".
   - At `PoolFactory.sol` line [116] and line [117], there is a typo in the function comments. "commiter" should be "committer".
   - `PoolCommitter.sol` and `LeveragedPool.sol` contracts contain inaccurate title comments. These should be updated to better reflect the segregation of functionality between the two contracts.
   - By default, `feeReceiver` in `PoolFactory.sol` is a public state variable; however, to be consistent, the testing team recommends adding a specific `public` keyword to line [26].
   - The revert message in `LeveragedPool.initialize()` line [56-59] does not correctly reflect the fee check’s behavior. In its current implementation, a pool’s fee cannot be initialized to 100%. This is likely intended behavior; therefore, it would be useful to update the revert message to better reflect this. Consider updating the revert message on line [56-59] from "Fee is greater than 100%" to "Fee is greater than or equal to 100%" or similar.

5. **Lack of Zero Address Validation:**
   - A number of contracts lack proper zero address validation and therefore may be initialized into an unexpected state. Ensure that contracts `PoolCommitter.sol`, `ChainlinkOracleWrapper.sol`, `PoolFactory.sol`, and `PoolCommitterDeployer.sol` perform proper zero address validation in their constructors.

6. **Use of Default CommitType:**
   - If an invalid `CommitType` is selected when calling `PoolCommitter.commit()`, `PoolCommitter.commitTypeToUint()` will default to `ShortMint`. This may inhibit overall user experience and should be ideally avoided and replaced with a relevant revert message if an invalid `CommitType` is selected.

7. **Pause Mechanism:**
   - `LeveragedPool.sol` holds all assets related to open long and short positions and plays a key role in TracerDAO’s perpetual pool system. Therefore, it may be useful to have a Pausable mechanism where the only `Gov` role can trigger an emergency stop to all deposits and withdrawals. The OpenZeppelin library contains an implementation of such a mechanism and can be applied by including the `whenNotPaused` and `whenPaused` modifiers to any target function.

8. **Potential Unexpected States:**
   - `PoolFactory.setMaxLeverage()` should not be settable to 0 as it puts the leveraged pool in a state where pools are no longer able to be deployed via `PoolFactory.deployPool()`. Ensure `maxLeverage` is never set to anything less than 1.
   - If the initial oracle price queried in `PoolKeeper.newPool()` is <= 0, then keepers will be unable to perform their duties as the upkeep will fail at the following line in `LeveragedPool.executePriceChange()`:
     ```solidity
     if (_oldPrice <= 0 || _newPrice <= 0) { emit PriceChangeError(_oldPrice, _newPrice); }
     ```
     Users can still mint and burn tokens as expected, but the market itself will become unusable. Consider adding a check in `PoolKeeper.newPool()` that ensures the starting price is a positive value.

9. **Unchecked ERC20 Return Value:**
   - `PoolCommitter.setQuoteAndPool()` makes an external ERC20 call to `approve()` the pool address as a spender to the `PoolCommitter.sol` contract. Consider checking the return value of this external call.

10. **Keeper Frontrunning:**
    - The `PoolKeeper.performUpkeepSinglePool()` function is a public and unrestricted function allowing anyone to perform the duties of a keeper and be rewarded for their work. This helps to maintain a high availability network that is able to deal with a large number of leveraged pools. There is potential for keepers to frontrun each other as they compete for blockspace. Ensure this is understood by users wishing to interact with the `PoolKeeper.sol` contract.

11. **Unclear Keeper Payments:**
    - `LeveragedPool.payKeeperFromBalances()` utilizes `PoolSwapLibrary.getBalancesAfterFees()` to determine the pool balances after the keeper’s fees have been deducted. The following comment in `PoolSwapLibrary.sol` line [39] specifies that reward may be equal to the sum of the two pool balances:
      ```solidity
      @dev Assumes shortBalance + longBalance >= reward
      ```
      Consider updating the following check in `payKeeperFromBalances()` or the aforementioned dev comment in `PoolSwapLibrary.sol` to correctly match the intended behavior:
      ```solidity
      // If the rewards are more than the balances of the pool, the keeper does not get paid
      if (amount >= _shortBalance + _longBalance) {
          return false;
      }
      ```

## Recommendations

Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Tracer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/tracer/tracer-2/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/tracer/tracer-2/review.pdf

### Keywords for Search

`vulnerability`

