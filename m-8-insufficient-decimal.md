---
# Core Classification
protocol: Yieldoor
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55046
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/791
source_link: none
github_link: https://github.com/sherlock-audit/2025-02-yieldoor-judging/issues/190

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
finders_count: 1
finders:
  - future2\_22
---

## Vulnerability Title

M-8: Insufficient Decimal

### Overview


The bug report discusses an issue with insufficient decimal precision in a project called Yieldoor. This leads to problems with calculating interest, especially for a specific type of currency called wbtc. The root cause of this issue is a function that may not update or may lose precision when dealing with large values. This can be exploited by an attacker who repeatedly deposits and redeems large amounts of wbtc, or by frequent interactions with the project. The report also includes a proof-of-concept scenario and the potential impact of this bug, which can result in reduced profits for users. The recommended solution is to increase the decimal precision of the collateral.

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-02-yieldoor-judging/issues/190 

## Found by 
future2\_22

### Summary
The decimal precision of the collateral is insufficient for calculating the interest, especially for wbtc.

### Root Cause
In `ReserveLogic::_updateIndexes::L156`, the totalBorrows may not update or may experience precision loss.
https://github.com/sherlock-audit/2025-02-yieldoor/blob/main/yieldoor/src/libraries/ReserveLogic.sol#L156
```solidity
156:        newTotalBorrows = newBorrowingIndex * (reserve.totalBorrows) / (reserve.borrowingIndex);
```
To change the `totalBorrows`, the unaccounted interest must be equal to or greater than 1 wei. 
To avoid precision loss, the interest must exceed 10,000 wei. 
If the collateral is wbtc, this value is not small.
And the `_updateIndexes` function could be executed every block(period = 15s), and the unaccounted interest may be less than the above value.

### Internal pre-conditions
N/A

### External pre-conditions
N/A

### Attack Path
An attacker can repeatedly deposit 1001 wei of wbtc and redeem the maximum amount of wbtc (type(uint256).max). 
Alternatively, users can interact with the `LendingPool` frequently

### PoC
Let's consider the following scenario.
LendingPool's asset = wbtc, BorrowingRateConfig: (0%, 0%) -> (80%, 20%) -> (90%, 50%) -> (100%, 150%)
totalLiquidityAndBorrows = 0.25 wbtc, totalBorrows = 0.126144 wbtc
currentUtilizationRate = 50.4576%, 
https://github.com/sherlock-audit/2025-02-yieldoor/blob/main/yieldoor/src/libraries/InterestRateUtils.sol#L28
currentBorrowingRate = 50.4576% * 20% / 80% = 12.6144%
https://github.com/sherlock-audit/2025-02-yieldoor/blob/main/yieldoor/src/libraries/InterestRateUtils.sol#L73
rate = 12.6144% = 0.126144e27, currentTimestamp = lastUpdateTimestamp + 15.
ratePerSecond = rate / SECONDS_PER_YEAR = 4e18
basePowerTwo = ratePerSecond * ratePerSecond / PRECISION = 16e9
basePowerThree = 64
secondTerm = exp * expMinusOne * basePowerTwo / 2 = 15 * 14 * 16e9 = 3360e9
thirdTerm = exp * expMinusOne * expMinusTwo * basePowerThree / 6 = 15 * 14 * 13 * 64 / 6 = 29120
CompoundedInterest = (PRECISION) + (ratePerSecond * exp) + (secondTerm) + (thirdTerm) = 
    = 1e27 + 4e18 * 15 + 3360e9 + 29120 = 1e27 + 60e18 + 3360e9 + 29120 < 1e27 + 60.1e18
https://github.com/sherlock-audit/2025-02-yieldoor/blob/main/yieldoor/src/libraries/ReserveLogic.sol#L115
latestBorrowingIndex = reserve.borrowingIndex * calculateCompoundedInterest / 1e27 < reserve.borrowingIndex * (1e27 + 60.1e18) / 1e27
https://github.com/sherlock-audit/2025-02-yieldoor/blob/main/yieldoor/src/libraries/ReserveLogic.sol#L156
newTotalBorrows = latestBorrowingIndex * (reserve.totalBorrows) / (reserve.borrowingIndex) < 
    < (reserve.borrowingIndex * (1e27 + 60.1e18) / 1e27) * (reserve.totalBorrows) / (reserve.borrowingIndex) = 
    = (1e27 + 60.1e18) / 1e27 * (reserve.totalBorrows) = 
    = reserve.totalBorrows + 60.1e-9 * 0.126144e8 < 
    < reserve.totalBorrows + 1;
Therefore, newTotalBorrows = reserve.totalBorrows

### Impact
The depositor of the LendingPool may not be able to take any profits at all or may receive reduced profits.

When `BorrowingRateConfig := (0%, 0%) -> (80%, 20%) -> (90%, 50%) -> (100%, 150%)`,
1. LendingPool's asset = wbtc, totalLiquidityAndBorrows = 0.25 wbtc, totalBorrows = 0.126144 wbtc
If the `_updateIndexes` function is executed every block, the interest is not collected. 
If it is executed every 100 blocks (25 mins), the calculation of interest experiences 1% precision loss.

2. LendingPool's asset = wbtc, totalLiquidityAndBorrows = 25 wbtc, totalBorrows = 12.6144 wbtc
If the `_updateIndexes` function is excuted every 100 block (25 mins), the calculation of interest experiences 0.01% precision loss.

3. LendingPool's asset = usdc, totalLiquidityAndBorrows = 250,000 usdc, totalBorrows = 126,144 usdc
If the `_updateIndexes` function is excuted every block, the calculation of interest experiences 0.01% precision loss.

### Mitigation
Consider increasing the decimal precision of the collateral.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Yieldoor |
| Report Date | N/A |
| Finders | future2\_22 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-02-yieldoor-judging/issues/190
- **Contest**: https://app.sherlock.xyz/audits/contests/791

### Keywords for Search

`vulnerability`

