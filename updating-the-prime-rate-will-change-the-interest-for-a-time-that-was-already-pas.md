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
solodit_id: 57347
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
finders_count: 10
finders:
  - pyro
  - theirrationalone
  - vs_
  - bigsam
  - valy001
---

## Vulnerability Title

Updating the prime rate will change the interest for a time that was already passed

### Overview


The bug report is about a problem in a code that updates the prime rate. When the prime rate is updated, it also changes the interest rate for a time period that has already passed. This can cause errors in the internal accounting and lead to sudden spikes or decreases in rates. The report suggests updating the rates before changing the prime rate to avoid this issue.

### Original Finding Content

## Summary
Updating the prime rate will change the interest for a time that was already passed

## Vulnerability Details

`setPrimeRate` doesn't update the interest before setting the new price.

https://github.com/Cyfrin/2025-02-raac/blob/main/contracts/libraries/pools/ReserveLibrary.sol#L399-L414
```solidity
    function setPrimeRate( ReserveData storage reserve,ReserveRateData storage rateData,uint256 newPrimeRate) internal {
        if (newPrimeRate < 1) revert PrimeRateMustBePositive();

        uint256 oldPrimeRate = rateData.primeRate;

        if (oldPrimeRate > 0) {
            uint256 maxChange = oldPrimeRate.percentMul(500); // Max 5% change
            uint256 diff = newPrimeRate > oldPrimeRate 
                ? newPrimeRate - oldPrimeRate 
                : oldPrimeRate - newPrimeRate;

            if (diff > maxChange) revert PrimeRateChangeExceedsLimit();
        }

        //@audit M should have updated rates before setting this rate
        // not whis will overcompound for time that it wasn't active
        rateData.primeRate = newPrimeRate;
        updateInterestRatesAndLiquidity(reserve, rateData, 0, 0);

        emit PrimeRateUpdated(oldPrimeRate, newPrimeRate);
    }
```

This will mean that if the lat update was at time T and prime is updated at T+1day, even though it is updated now it would take account for all of the interest generated between T and T+1day, aka. it will change the rate for time that has already passed.

## Impact

Updating the price will change rates for a time that has already passed. That is not good as it would cause an instant spike or decrease and internal accounting errors as some function take the rate without updating it, like `getNormalizedDebt`.

```solidity
    function getNormalizedDebt(ReserveData storage reserve, ReserveRateData storage rateData) internal view returns (uint256) {
        uint256 timeDelta = block.timestamp - uint256(reserve.lastUpdateTimestamp);
        if (timeDelta < 1) {
            return reserve.totalUsage;
        }

        // (e^((currentUsageRate * 1e27 / 1 year) * timeDelta / 1e27)) * reserve.usageIndex / 1e27
        return calculateCompoundedInterest(rateData.currentUsageRate, timeDelta).rayMul(reserve.usageIndex);
    }
```

## Tools Used

Manual review

## Recommendations

Update the rates before changing the prime rate.

```diff
+       updateInterestRatesAndLiquidity(reserve, rateData, 0, 0);
        rateData.primeRate = newPrimeRate;
-       updateInterestRatesAndLiquidity(reserve, rateData, 0, 0);
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
| Finders | pyro, theirrationalone, vs_, bigsam, valy001, x1485967, almur100, anonymousjoe, alexczm, nfmelendez |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

