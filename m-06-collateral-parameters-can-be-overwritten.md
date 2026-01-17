---
# Core Classification
protocol: Yeti Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1210
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-yeti-finance-contest
source_link: https://code4rena.com/reports/2021-12-yetifinance
github_link: https://github.com/code-423n4/2021-12-yetifinance-findings/issues/198

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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cmichel
  - csanuragjain  gzeon
---

## Vulnerability Title

[M-06] Collateral parameters can be overwritten

### Overview


A bug has been discovered in the `Whitelist.addCollateral` function of a contract. The bug allows the first collateral token in the `validCollateral` array to be repeatedly added. This is because the `validCollateral[0] != _collateral` check will return false and skip further checks. This can cause the collateral parameters `collateralParams` to be re-initialized, which can break existing accounting. Additionally, the collateral token will exist multiple times in `validCollateral`.

To fix this bug, the check should be changed to something like: 
```solidity
if (validCollateral.length > 0) {
    require(collateralParams[_collateral].index == 0 && validCollateral[0] != _collateral, "collateral already exists");
}
```

### Original Finding Content

_Submitted by cmichel, also found by csanuragjain and gzeon_

It's possible to repeatedly add the first collateral token in `validCollateral` through the `Whitelist.addCollateral` function.
The `validCollateral[0] != _collateral` check will return false and skip further checks.

#### POC

Owner calls `addCollateral(collateral=validCollateral[0])`:

```solidity
function addCollateral(
    address _collateral,
    uint256 _minRatio,
    address _oracle,
    uint256 _decimals,
    address _priceCurve, 
    bool _isWrapped
) external onlyOwner {
    checkContract(_collateral);
    checkContract(_oracle);
    checkContract(_priceCurve);
    // If collateral list is not 0, and if the 0th index is not equal to this collateral,
    // then if index is 0 that means it is not set yet.
    // @audit evaluates validCollateral[0] != validCollateral[0] which is obv. false => skips require check
    if (validCollateral.length != 0 && validCollateral[0] != _collateral) {
        require(collateralParams[_collateral].index == 0, "collateral already exists");
    }

    validCollateral.push(_collateral);
    // overwrites parameters
    collateralParams[_collateral] = CollateralParams(
        _minRatio,
        _oracle,
        _decimals,
        true,
        _priceCurve,
        validCollateral.length - 1, 
        _isWrapped
    );
}
```

#### Impact

The collateral parameters `collateralParams` are re-initialized which can break the existing accounting.
The collateral token also exists multiple times in `validCollateral`.

#### Recommended Mitigation Steps

Fix the check. It should be something like:

```solidity
if (validCollateral.length > 0) {
    require(collateralParams[_collateral].index == 0 && validCollateral[0] != _collateral, "collateral already exists");
}
```




### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Yeti Finance |
| Report Date | N/A |
| Finders | cmichel, csanuragjain  gzeon |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-yetifinance
- **GitHub**: https://github.com/code-423n4/2021-12-yetifinance-findings/issues/198
- **Contest**: https://code4rena.com/contests/2021-12-yeti-finance-contest

### Keywords for Search

`vulnerability`

