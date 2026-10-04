---
# Core Classification
protocol: Opyn Gamma Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18178
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/Opyn-Gamma-Protocol.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/Opyn-Gamma-Protocol.pdf
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
  - Dominik Teiml
  - Mike Martel
---

## Vulnerability Title

getProceed returns absolute value of required collateral

### Overview


This bug report is about a data validation problem in the contracts of the Opyn Gamma Protocol. The problem lies in the function getExcessCollateral which returns an absolute value of a signed integer. This value is used to return the amount of collateral required or excess collateral in the getExcessCollateral function. The issue is that when the vault is undercollateralized, the function will return a positive value instead of a negative one, leading to unintended consequences. 

The short term recommendation is to change the semantics of getExcessCollateral and getProceed to return signed integers with negative numbers representing undercollateralized vaults. Alternatively, the outputs of getExcessCollateral should not be discarded or used in logic that requires the function. The long term recommendation is to avoid coercion of negative values into positive ones.

### Original Finding Content

## Data Validation

**Type:** Data Validation  
**Target:** contracts/*  

**Difficulty:** Undetermined  

## Description

As mentioned in TOB-OPYN-012, a function that returns the absolute value of a signed integer is used to return the amount of required collateral or excess collateral in `getExcessCollateral`.

```solidity
FPI.FixedPointInt memory excessCollateral = collateralAmount.sub(collateralRequired);
bool isExcess = excessCollateral.isGreaterThanOrEqual(ZERO);
uint256 collateralDecimals = vaultDetails.hasLong
    ? vaultDetails.longCollateralDecimals
    : vaultDetails.shortCollateralDecimals;

// if is excess, truncate the tailing digits in excessCollateralExternal calculation
uint256 excessCollateralExternal = excessCollateral.toScaledUint(collateralDecimals, isExcess);
return (excessCollateralExternal, isExcess);
```

**Figure 13.1:** MarginCalculator.getExcessCollateral

This function is used in the Controller’s `getProceed` function:

```solidity
function getProceed(address _owner, uint256 _vaultId) external view returns (uint256) {
    (MarginVault.Vault memory vault, uint256 typeVault, ) = getVault(_owner, _vaultId);
    (uint256 netValue, ) = calculator.getExcessCollateral(vault, typeVault);
    return netValue;
}
```

**Figure 13.2:** Controller.getProceed

It follows that `getProceed` will return a positive value even if a vault is undercollateralized, as it does not use a boolean that could indicate a negative underlying value.

## Exploit Scenario

Eve creates a vault that becomes undercollateralized. An external system checks her vault and assumes that it is overcollateralized, leading to unintended consequences.

## Recommendations

**Short term:** Consider changing the semantics of `getExcessCollateral` and `getProceed` to return signed integers, with negative numbers representing undercollateralized vaults. Alternatively, ensure that the outputs of `getExcessCollateral` are not discarded or used in logic that requires that function.

**Long term:** Avoid the coercion of negative values into positive ones.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Opyn Gamma Protocol |
| Report Date | N/A |
| Finders | Dominik Teiml, Mike Martel |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/Opyn-Gamma-Protocol.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/Opyn-Gamma-Protocol.pdf

### Keywords for Search

`vulnerability`

