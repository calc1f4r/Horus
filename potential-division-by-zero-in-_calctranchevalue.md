---
# Core Classification
protocol: Growth Labs GSquared
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17358
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-GSquared-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-GSquared-securityreview.pdf
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
finders_count: 4
finders:
  - Damilola Edwards
  - Gustavo Grieco
  - Anish Naik
  - Michael Colburn
---

## Vulnerability Title

Potential division by zero in _calcTrancheValue

### Overview

See description below for full details.

### Original Finding Content

## GTranche Solidity Vulnerability Analysis

## Difficulty
Low

## Type
Data Validation

## Target
GTranche.sol

## Description
Junior tranche withdrawals may fail due to an unexpected division by zero error. One of the key steps performed during junior tranche withdrawals is to identify the dollar value of the tranche tokens that will be burned by calling `_calcTrancheValue` (figure 14.1).

```solidity
function _calcTrancheValue(
    bool _tranche,
    uint256 _amount,
    uint256 _total
) public view returns (uint256) {
    uint256 factor = getTrancheToken(_tranche).factor(_total);
    uint256 amount = (_amount * DEFAULT_FACTOR) / factor;
    if (amount > _total) return _total;
    return amount;
}
```
*Figure 14.1: The `_calcTrancheValue` function in GTranche.sol#L559-568*

To calculate the dollar value, the `factor` function is called to identify how many tokens represent one dollar. The dollar value, `amount`, is then the token amount provided, `_amount`, divided by `factor`.

However, an edge case in the `factor` function will occur if the total supply of tranche tokens (junior or senior) is non-zero while the amount of assets backing those tokens is zero. Practically, this can happen only if the system is exposed to a loss large enough that the assets backing the junior tranche tokens are completely wiped. In this edge case, the `factor` function returns zero (figure 14.2). The subsequent division by zero in `_calcTrancheValue` will cause the transaction to revert.

```solidity
function factor(uint256 _totalAssets) public view override returns (uint256) {
    if (totalSupplyBase() == 0) {
        return getInitialBase();
    }
    if (_totalAssets > 0) {
        return totalSupplyBase().mul(BASE).div(_totalAssets);
    }
    // This case is totalSupply > 0 && totalAssets  == 0, and only occurs on system loss
    return 0;
}
```
*Figure 14.2: The `factor` function in GToken.sol#L525-541*

It is important to note that if the system enters a state where there are no assets backing the junior tranche, junior tranche token holders would be unable to withdraw anyway. However, this division by zero should be caught in `_calcTrancheValue`, and the requisite error code should be thrown.

## Recommendations
**Short term:** Add a check before the division to ensure that `factor` is greater than zero. If `factor` is zero, throw a custom error code specifically created for this situation.

**Long term:** Expand the unit test suite to cover additional edge cases and to ensure that the system behaves as expected.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Growth Labs GSquared |
| Report Date | N/A |
| Finders | Damilola Edwards, Gustavo Grieco, Anish Naik, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-GSquared-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-GSquared-securityreview.pdf

### Keywords for Search

`vulnerability`

