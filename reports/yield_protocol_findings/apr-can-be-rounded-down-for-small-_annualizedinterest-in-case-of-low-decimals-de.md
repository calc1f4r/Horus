---
# Core Classification
protocol: Term Structure
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54901
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/6f373ea8-adf6-45d2-8d72-a76fe5b7f21e
source_link: https://cdn.cantina.xyz/reports/cantina_competition_term_structure_february2025.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - BengalCatBalu
---

## Vulnerability Title

Apr can be rounded down for small _annualizedInterest in case of low decimals debtToken 

### Overview


This bug report discusses an issue with the `Vault` function in the `TermMaxMarket` contract. The issue is related to the calculation of APR (Annual Percentage Rate) and how it can potentially round down to 0, causing the protocol to lose APR. This occurs when the `debtToken` has 6 decimals and the `annualizedInterest` is still small. The report recommends adding scaling to the calculation to avoid this issue. The bug has been addressed in two pull requests (PR 4 and PR 5) and has been verified as fixed by Cantina Managed.

### Original Finding Content

## Report

## Context
(No context files were provided by the reviewer)

## Summary
The first thing to notice is that the `ft`, `xt`, and `debtToken` decimals match. This is clear from the `_deployTokens` function in `TermMaxMarket`. Second, for the following report, let's assume that `debtToken` = USDC and has 6 decimals, so `ft` and `xt` also have 6 decimals. 

Next, let's look at the function that accrues APR in `Vault`:

```solidity
function _accruedPeriodInterest(uint256 startTime, uint256 endTime) internal {
    uint256 interest = (_annualizedInterest * (endTime - startTime)) / 365 days;
    uint256 _performanceFeeToCurator = (interest * _performanceFeeRate) / Constants.DECIMAL_BASE;
    // accrue interest
    _performanceFee += _performanceFeeToCurator;
    _accretingPrincipal += (interest - _performanceFeeToCurator);
}
```

In this entire function, we are interested in this particular line:

```solidity
uint256 interest = (_annualizedInterest * (endTime - startTime)) / 365 days;
```

We will assume that interactions with `Vault` are very frequent, so `endTime - startTime` is minimal:
- 365 days = 31,536,000 seconds

Consider the dimensionality of `_annualizedInterest`. It is changed in the `swapCallback` function:

```solidity
function swapCallback(int256 deltaFt) external onlyProxy {
    address orderAddress = msg.sender;
    /// @dev Check if the order is valid
    _checkOrder(orderAddress);
    uint64 maturity = _orderMapping[orderAddress].maturity;
    /// @dev Calculate interest from last update time to now
    _accruedInterest();
    /// @dev If ft increases, interest increases, and if ft decreases,
    /// interest decreases. Update the expected annualized return based on the change
    uint256 ftChanges;
    if (deltaFt > 0) {
        ftChanges = deltaFt.toUint256();
        _totalFt += ftChanges;
        uint256 deltaAnualizedInterest = (ftChanges * Constants.DAYS_IN_YEAR) / _daysToMaturity(maturity);
        _maturityToInterest[maturity] += deltaAnualizedInterest.toUint128();
        _annualizedInterest += deltaAnualizedInterest;
    } else {
        ftChanges = (-deltaFt).toUint256();
        _totalFt -= ftChanges;
        uint256 deltaAnualizedInterest = (ftChanges * Constants.DAYS_IN_YEAR) / _daysToMaturity(maturity);
        if (_maturityToInterest[maturity] < deltaAnualizedInterest || _annualizedInterest < deltaAnualizedInterest) {
            revert LockedFtGreaterThanTotalFt();
        }
        _maturityToInterest[maturity] -= deltaAnualizedInterest.toUint128();
        _annualizedInterest -= deltaAnualizedInterest;
    }
    /// @dev Ensure that the total assets after the transaction are
    /// greater than or equal to the principal and the allocated interest
    _checkLockedFt();
}
```

Each time it changes to the following value:
```solidity
deltaAnualizedInterest = (ftChanges * Constants.DAYS_IN_YEAR) / _daysToMaturity(maturity);
```

As we see, the dimensionality of `annualizedInterest` is equal to the dimensionality of `ft`, which in our case is 6.

So, from this, it becomes clear that at the initial stages of `Vault`, for a still small not yet accumulated `annualizedInterest`, with decimals = 6, `Vault` APR will suffer significantly from rounding down, potentially rounding to 0.

Suppose that the current `annualizedInterest` = 5 = 5 * 10 ** 6. So as long as it is equal to 5, for any time interval less than 20 when calculating APR, it will be rounded down to 0, causing the `Vault` to lose APR.

## Impact Explanation
The protocol loses APR due to downward rounding.

## Likelihood Explanation
This occurs in all cases where the `debtToken` has 6 decimals.

## Recommendation 
Add scaling to this calculation to avoid losing APR.

## Term Structure
Addressed in PR 4 and PR 5.

## Cantina Managed
Fixes verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Term Structure |
| Report Date | N/A |
| Finders | BengalCatBalu |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_term_structure_february2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/6f373ea8-adf6-45d2-8d72-a76fe5b7f21e

### Keywords for Search

`vulnerability`

