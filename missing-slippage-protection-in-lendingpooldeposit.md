---
# Core Classification
protocol: Core Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57379
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

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
finders_count: 4
finders:
  - olami9783
  - 0xalexsr
  - kupiasec
  - hailthelord
---

## Vulnerability Title

Missing Slippage Protection in `LendingPool.deposit()`

### Overview


The `deposit()` function in `LendingPool` does not have protection against slippage, which allows attackers to manipulate the `liquidityIndex` and reduce the amount of `rToken` that users receive. This results in fewer rewards for users in the `StabilityPool`. The vulnerability can be exploited by front-running the deposit process and increasing the `liquidityIndex` through borrowing, resulting in a lower `rToken` amount for the user. This can impact the fairness and predictability of the deposit process. To fix this issue, it is recommended to implement slippage protection by requiring a minimum `rToken` output or allowing users to specify an expected `rToken` amount. 

### Original Finding Content

## Summary

The `deposit()` function in `LendingPool` lacks slippage protection, allowing an attacker to manipulate the `liquidityIndex` and reduce the amount of `rToken` minted for a user. This results in fewer reward tokens (`raacToken`) in the `StabilityPool`.

## Vulnerability Details

In `LendingPool.deposit()`, when a user deposits `X` amount of `crvUSD`, they receive `rToken` based on the `liquidityIndex`. However, this value can be front-run by a malicious actor who increases utilization by borrowing the present crvUSD, thereby increasing `liquidityIndex` and reducing the user's expected `rToken` amount.

## PoC

### Affected Code

<https://github.com/Cyfrin/2025-02-raac/blob/89ccb062e2b175374d40d824263a4c0b601bcb7f/contracts/core/pools/LendingPool/LendingPool.sol#L225C5-L236C6>

Since `liquidityIndex` can be manipulated before execution, the final `rTokenAmount` is uncertain.

1. Assume `liquidityIndex = 1e27` at the time of deposit.
2. A user deposits `100 crvUSD` into `LendingPool.deposit()`, expecting:
   ```solidity
   rTokenAmount = (100 * 1e27) / 1e27 = 100 rToken;
   ```
3. A malicious actor front-runs the deposit by borrowing `crvUSD`, increasing `liquidityIndex` due to the formula:
   ```solidity
   liquidityIndex = previousLiquidityIndex * (1 + currentLiquidityRate)
   ```
4. If `liquidityIndex` increases to `1.1e27`, the user now gets:
   ```solidity
   rTokenAmount = (100 * 1e27) / 1.1e27 ≈ 90.9 rToken;
   ```
5. The user unknowingly receives fewer `rToken`, leading to a reduced amount of `raacToken` rewards in the `StabilityPool`.

## Impact

* Users receive fewer `rToken` than expected.
* This results in lower `deToken` and `raacToken` rewards in `StabilityPool`.
* The manipulation affects the fairness and predictability of the deposit process.

## Tools Used

Manual Review

## Recommendations

Implement slippage protection by requiring a minimum `rToken` output, either:

1. Specifying an expected `rToken` amount in BPS (basis points).
2. Allowing users to provide a `minRTokenAmount` parameter, reverting if not met:
```diff
- function deposit(uint256 amount) external nonReentrant whenNotPaused onlyValidAmount(amount) {
+ function deposit(uint256 amount, uint256 expected) external nonReentrant whenNotPaused onlyValidAmount(amount) {
       ReserveLibrary.updateReserveState(reserve, rateData);
       uint256 mintedAmount = ReserveLibrary.deposit(reserve, rateData, amount, msg.sender);
+      if (mintedAmount < expected) revert();
         _rebalanceLiquidity();
       emit Deposit(msg.sender, amount, mintedAmount);
}
```
This prevents deposits from being executed under manipulated conditions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | olami9783, 0xalexsr, kupiasec, hailthelord |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

