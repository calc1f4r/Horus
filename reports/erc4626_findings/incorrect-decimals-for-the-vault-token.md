---
# Core Classification
protocol: Chateau Capital
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40526
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/28efed32-c673-470b-9681-d3764088109f
source_link: https://cdn.cantina.xyz/reports/cantina_chateau_apr2024.pdf
github_link: none

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
finders_count: 2
finders:
  - m4rio
  - high byte
---

## Vulnerability Title

Incorrect decimals for the vault token 

### Overview


This bug report is about a problem in the code that calculates the number of decimals for a particular asset. Currently, the code returns the decimals for the asset, but it should actually return 18 decimals. This can cause incorrect calculations, especially for assets with a different number of decimals, such as USDC. The report suggests changing the code to use a variable for the number of decimals and to avoid dividing before multiplying. The severity of the bug has been lowered, but it could still be critical for external contracts that rely on the decimals for accounting.

### Original Finding Content

## Context 

4626.sol#L244-L244

## Description 

The current implementation returns the asset's decimals as decimals:

```solidity
function decimals() 
    public 
    view 
    virtual 
    override(IERC20Metadata, ERC20) 
    returns (uint8) 
{
    return _underlyingDecimals + _decimalsOffset();
}
```

The `_decimalsOffset` is 0. While this can be a way of defining the vault token's decimals, we can see from the `_convertToShares` and `_convertToAssets` functions that the intention was actually to have 18 decimals. If the asset has different decimals than 18, the calculations will result in returning erroneous amounts of shares/assets.

For example, if the asset used is USDC, which has 6 decimals, converting 1 asset to shares will generate 1e12 shares instead of 1 share. Imagine a user wants to convert:

1 USDC = 1e6 to 1 share == 1e6:

```
1e6 * 1e12 / 1e18 * 1e18 = 1e18
```

This means 1e12 after transformation. 

Furthermore, we see that a division before multiplication is performed in the `_convertToShares`, which should always be avoided to prevent rounding issues. 

## Recommendation 

Consider defining the `_decimalsOffset` as a variable that can be used in the conversion functions. This variable should be initialized in the constructor as `_decimalsOffset = 18 - _underlyingDecimals;`. For example:

```solidity
function _convertToShares(uint256 assets, Math.Rounding rounding) 
    public 
    view 
    virtual 
    returns (uint256) 
{
    return ((assets * 10**_decimalsOffset) / _price) * 1e18; // Adjust asset value based on price
}
```

The same change should be made in the `_convertToAssets`. Instead of dividing by 1e30, it should actually divide by `10 ** (18 + _decimalsOffset)`. We must warn that tokens with decimals greater than 18 should be avoided, as they will not work with this implementation.

Alternatively, consider deleting the `decimals()` function and let the ERC20 implementation return 18 decimals. We propose to choose the first approach as it is more generic.

Furthermore, for the division before multiplication, always multiply first, then divide.

The Chateau team noted that this is indeed a bug, but it does not affect the current implementation; therefore, the severity is lowered on this report. However, if an external contract relies on decimals for accounting, the issue will be noted as critical.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Chateau Capital |
| Report Date | N/A |
| Finders | m4rio, high byte |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_chateau_apr2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/28efed32-c673-470b-9681-d3764088109f

### Keywords for Search

`vulnerability`

