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
solodit_id: 57316
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
finders_count: 6
finders:
  - newspacexyz
  - 0x23r0
  - agbanusijohn
  - farismaulana
  - dimah7
---

## Vulnerability Title

When the prime rate is updated by the oracle, the values of the sub-rates are not ajdusted accordingly, which can cause loss of assets for borrowers

### Overview


This report discusses a bug in the `LendingPool` code, which can cause loss of assets for borrowers. The bug occurs when the prime rate is updated by the oracle, but the values of the sub-rates (base, optimal, max) are not adjusted accordingly. This means that users will still operate with outdated rates, leading to potential loss of funds. The bug can also artificially inflate debt, force borrowers into liquidations, and leave them undercollateralized. The bug was identified through manual review and the recommendation is to adjust the sub-rates properly when the prime rate is updated. 

### Original Finding Content

## Summary

When the `LendingPool` is deployed there is an initial prime rate set and the other sub-rates (base, optimal, max) are derived from the prime rate's value.

* 

```javascript
LendingPool::constructor()...

// Prime Rate
        rateData.primeRate = uint256(_initialPrimeRate);
        rateData.baseRate = rateData.primeRate.percentMul(25_00); // 25% of prime rate
        rateData.optimalRate = rateData.primeRate.percentMul(50_00); // 50% of prime rate
        rateData.maxRate = rateData.primeRate.percentMul(400_00); // 400% of prime rate
```

However when the prime rate is updated by the prime rate oracle, the sub-rates values are not ajdusted based on the new prime rate value. This means the users will still operate with the outdated rates, which can lead to loss of funds

## Vulnerability Details

* 
* 

```javascript
LendingPool:

function setPrimeRate(uint256 newPrimeRate) external onlyPrimeRateOracle {
        ReserveLibrary.setPrimeRate(reserve, rateData, newPrimeRate);
    }

ReserveLibrary:

function setPrimeRate( ReserveData storage reserve,ReserveRateData storage rateData,uint256 newPrimeRate) internal {
        if (newPrimeRate < 1) revert PrimeRateMustBePositive();

        uint256 oldPrimeRate = rateData.primeRate;

        if (oldPrimeRate > 0) {
            uint256 maxChange = oldPrimeRate.percentMul(500); // Max 5% change
            uint256 diff = newPrimeRate > oldPrimeRate ? newPrimeRate - oldPrimeRate : oldPrimeRate - newPrimeRate;
            if (diff > maxChange) revert PrimeRateChangeExceedsLimit();
        }

        rateData.primeRate = newPrimeRate;
        updateInterestRatesAndLiquidity(reserve, rateData, 0, 0);

        emit PrimeRateUpdated(oldPrimeRate, newPrimeRate);
    }
```

As we can see only the new value is updated. The base, optimal and max rates remain the same. The "sub-rates" are used when calculating the borrow rate:

* 

```javascript
ReserveLibrary:

function calculateBorrowRate(
        uint256 primeRate,
        uint256 baseRate,
        uint256 optimalRate,
        uint256 maxRate,
        uint256 optimalUtilizationRate,
        uint256 utilizationRate
    ) internal pure returns (uint256) {
        if (primeRate <= baseRate || primeRate >= maxRate || optimalRate <= baseRate || optimalRate >= maxRate) {
            revert InvalidInterestRateParameters();
        }

        uint256 rate;
        if (utilizationRate <= optimalUtilizationRate) {
            uint256 rateSlope = primeRate - baseRate;
            uint256 rateIncrease = utilizationRate.rayMul(rateSlope).rayDiv(optimalUtilizationRate);
            // 0
            rate = baseRate + rateIncrease;
        } else {
            uint256 excessUtilization = utilizationRate - optimalUtilizationRate;
            uint256 maxExcessUtilization = WadRayMath.RAY - optimalUtilizationRate;
            uint256 rateSlope = maxRate - primeRate;
            uint256 rateIncrease = excessUtilization.rayMul(rateSlope).rayDiv(maxExcessUtilization);
            rate = primeRate + rateIncrease;
        }
        return rate;
    }
```

1. Let's say that the initial prime rate is `0.1` (1e26) in RAY, base rate will be `0.025` (25% of prime rate).
2. if `utilizationRate <= optimalUtilizationRate` the initial rate slope will be `0.075`
3. Now if the oracle updates with the allowed 5% deviation the oracle can set the new rate as `0.095` or `0.105`, the slope must be `0.07` or `0.08` (this is with the old base rate, which is 25% of `0.1`), which is wrong
4. BUT if the base rate's value is updated accordingly to new prime rate value, the base rate must be `0.02375` or `0.02625`, and the slope must be `0.06875` or `0.07125`
5. This is will affect the rate increase as can be seen in the code snippet above

The result of the `calculateBorrowRate` is stored as the `currentUsageRate` in `ReserveLibrary::updateInterestRatesAndLiquidity()`. The `currentUsageRate` is used for calculating the `usageIndex (debtIndex)`, the compounded interest.

## Impact

Overall will inflate the debt index, liquidity rate and the accrued interest, here is more detailed explanation:

1. Will artificially inflate the users debt, that means the borrowers will be forced to repay more assets than they should. Which means loss of funds for borrowers.
2. Will force borrowers into liquidations, which again results loss of funds, because their collateral will be seized.
3. Will leave borrowers undercollateralized, means they will not be able to borrow new assets with their current deposited collateral.

* Impact: `High`, loss of assets for borrowers
* Likelihood: `Medium`, i consider the likelihood as medium, because the oracle can update the rate frequently based on utilization rate, interest rate
* Overall: `High`

## Tools Used

Manual Review

## Recommendations

Adjust the "sub-rates" properly when the prime rate is updated:

```diff
ReserveLibrary:

function setPrimeRate( ReserveData storage reserve,ReserveRateData storage rateData,uint256 newPrimeRate) internal {
        if (newPrimeRate < 1) revert PrimeRateMustBePositive();

        uint256 oldPrimeRate = rateData.primeRate;

        if (oldPrimeRate > 0) {
            uint256 maxChange = oldPrimeRate.percentMul(500); // Max 5% change
            uint256 diff = newPrimeRate > oldPrimeRate ? newPrimeRate - oldPrimeRate : oldPrimeRate - newPrimeRate;
            if (diff > maxChange) revert PrimeRateChangeExceedsLimit();
        }

        rateData.primeRate = newPrimeRate;
+       rateData.baseRate = rateData.primeRate.percentMul(25_00); // 25% of prime rate
+       rateData.optimalRate = rateData.primeRate.percentMul(50_00); // 50% of prime rate
+       rateData.maxRate = rateData.primeRate.percentMul(400_00); // 400% of prime rate       
        updateInterestRatesAndLiquidity(reserve, rateData, 0, 0);

        emit PrimeRateUpdated(oldPrimeRate, newPrimeRate);
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | newspacexyz, 0x23r0, agbanusijohn, farismaulana, dimah7, 0xmystery |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

