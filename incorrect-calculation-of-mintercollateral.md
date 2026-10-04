---
# Core Classification
protocol: SOFA.org
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36039
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/sofa/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/sofa/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Incorrect Calculation Of minterCollateral

### Overview


This bug report discusses an issue with the calculation of minterCollateral in the LeverageDNTVault.sol function. This calculation is used to determine the trading fees and collateral ratios for users and market makers. The current calculation is incorrect and results in incorrect fees and ratios. The correct calculation has been identified and recommended by the development team. A resolution has been implemented in commit ef1e9b9. This bug causes a rounding issue that results in a small amount of collateral being locked, which is referred to as a "dust amount". 

### Original Finding Content

## Description

Following discussions with the development team, it was established that the calculation of `minterCollateral` within the function `_mint()` is incorrect. This will in turn produce incorrect calculations of trading fees and of the permitted collateral ratios between the user and the market maker.

## Original Calculation

```solidity
LeverageDNTVault.sol
uint256 minterCollateral = (totalCollateral - params.makerCollateral) * APR_BASE / (APR_BASE + LEVERAGE_RATIO * APR_BASE + LEVERAGE_RATIO * borrowAPR * (params.expiry - block.timestamp) / SECONDS_IN_YEAR);
```

Each time that a product is minted, the `borrowFee` and `spreadFee` will be incorrectly calculated as these variables are derived from `minterCollateral`.

## Correct Calculation

The correct calculation is derived from the following equation:

```solidity
LeverageDNTVault.sol
// (totalCollateral - makerCollateral) = minterCollateral + minterCollateral * LEVERAGE_RATIO * borrowAPR / SECONDS_IN_YEAR * (expiry - block.timestamp);
```

The left-hand side of this equation is the amount of collateral provided by the user. The right-hand side is a calculation of a simulation of leverage. It consists of a nominal amount of collateral provided by the user (`minterCollateral`) added to the borrow interest on borrowing that amount again `LEVERAGE_RATIO` times for the active duration of the minted product.

From this equation, the correct calculation can be derived:

```solidity
LeverageDNTVault.sol
uint256 minterCollateral = (totalCollateral - params.makerCollateral) * APR_BASE / (APR_BASE + LEVERAGE_RATIO * borrowAPR * (params.expiry - block.timestamp) / SECONDS_IN_YEAR);
```

## Recommendations

After discussions with the development team, it was established that the calculation of the `minterCollateral` should be revised to:

```solidity
LeverageDNTVault.sol
// (totalCollateral - makerCollateral) = minterCollateral + minterCollateral * LEVERAGE_RATIO * borrowAPR / SECONDS_IN_YEAR * (expiry - block.timestamp);
uint256 minterCollateral = (totalCollateral - params.makerCollateral) * APR_BASE / (APR_BASE + LEVERAGE_RATIO * borrowAPR * (params.expiry - block.timestamp) / SECONDS_IN_YEAR);
```

## Resolution

The development team have modified the calculation as described in commit `ef1e9b9`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | SOFA.org |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/sofa/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/sofa/review.pdf

### Keywords for Search

`vulnerability`

